# 分野2: 信頼性と事業継続性

配点は **22%** です。旧版の 16% から増えました。

スケーリング、高可用性、バックアップと復元の 3 つです。設計そのものより、設定と、失敗したときの切り分けが問われます。

この分野に限らず、コース全体で使うサービスは[サービス一覧](services.md)から確認できます。

## タスク 2.1: スケーラビリティと伸縮性を実装する {#task-2-1}

### 2.1.1 コンピューティングのスケーリング {#skill-2-1-1}

| ポリシー | 動作 | 選ぶ場面 |
|---|---|---|
| ターゲット追跡 | メトリクスを目標値に保つ | 第一候補 |
| ステップ | 超過量に応じて段階的に増減 | 細かく制御したい |
| スケジュール | 決まった時刻に容量を変える | 毎朝 9 時の増加など、予定がある |
| 予測 | 過去のパターンから先回りする | 周期的な負荷 |
| シンプル | 1 回の調整とクールダウン | 古い方式で、AWS は勧めていない |

**SQS の処理:** キューの長さそのものではなく、インスタンスあたりのバックログをカスタムメトリクスにして、ターゲット追跡します。

**その他の機能:**

| 課題 | 機能 |
|---|---|
| 起動に時間がかかる | ウォームプール |
| 起動後の準備や終了前のログ保存 | ライフサイクルフック |
| 新しい AMI を順に適用する | インスタンスの更新 |
| 調査中のインスタンスを消されたくない | `ReplaceUnhealthy` の一時停止、スタンバイ |
| スポットの中断に備える | 混合インスタンスと Capacity Rebalancing |

**他のコンピューティング:**

| 対象 | 仕組み |
|---|---|
| ECS サービス | Application Auto Scaling でタスク数を増減 |
| Lambda | 同時実行で自動。予約と Provisioned Concurrency で調整 |

| 症状 | 原因 |
|---|---|
| 起動と終了を繰り返す | ヘルスチェックの猶予期間が短い。CLI と SDK の既定は 0 秒、コンソールは 300 秒 |
| 起動テンプレートのエラー | AMI、セキュリティグループ、キーペアが削除済み |
| 起動できない | 容量不足、クォータ、暗号化キーの権限 |

原因は `describe-scaling-activities` で確認します。

詳細: [EC2 Auto Scaling](../../services/ec2-beanstalk.md#auto-scaling)、[クールダウン](../../services/ec2-beanstalk.md#asg-cooldown)、[ウォームアップ](../../services/ec2-beanstalk.md#instance-warmup)、[ライフサイクルフック](../../services/operations.md#lifecycle-hooks)、[ウォームプール](../../services/operations.md#warm-pools)、[インスタンスの更新](../../services/operations.md#instance-refresh)、[プロセスの一時停止](../../services/operations.md#suspend-processes)、[予測スケーリング](../../services/operations.md#predictive-scaling)、[失敗の調査](../../services/operations.md#asg-troubleshooting)、[ECS のサービスの Auto Scaling](../../services/containers.md#service-auto-scaling)、[Lambda の同時実行](../../services/lambda.md#concurrency)

### 2.1.2 キャッシュ {#skill-2-1-2}

| 要件 | 選択 |
|---|---|
| DynamoDB の読み取りを最小のコード変更で速く | DAX |
| RDS のクエリ結果をキャッシュ | ElastiCache |
| 複数の EC2 でセッションを共有 | ElastiCache |
| 世界中へ画像や API の GET を速く配信 | CloudFront |

**ElastiCache の設定:**

| 項目 | 内容 |
|---|---|
| Valkey、Redis OSS | レプリカと Multi-AZ、永続化、ソート済みセット |
| Memcached | レプリケーションなし。ノードが落ちるとそのデータは消える |
| 読み取りの増加 | レプリカを追加 |
| 書き込みやメモリの増加 | クラスターモードでシャードを追加 |
| 追い出し（`Evictions`）が多い | ノードを大きくする、TTL を見直す |

**戦略:** 遅延読み込みは必要なものだけ載りますが、ミスの直後は遅く、古い値が残ることがあります。書き込みスルーは常に新しいものの、使わないデータも載ります。TTL を組み合わせます。

**CloudFront:** ヒット率を上げるには、キャッシュキーに入れる値を絞ります。詳しくは [5.3.3](domain5.md#skill-5-3-3) を確認します。

詳細: [DAX、ElastiCache、CloudFront の使い分け](../../services/databases.md#cache-comparison)、[キャッシュ戦略](../../services/databases.md#caching-strategies)、[ElastiCache](../../services/databases.md#elasticache)、[クラスターモード](../../services/databases.md#cluster-mode)、[追い出し](../../services/databases.md#eviction)、[DAX](../../services/dynamodb.md#dax)、[キャッシュキー](../../services/networking.md#cache-keys)

### 2.1.3 マネージドデータベースのスケーリング {#skill-2-1-3}

| サービス | 読み取り | 書き込み、全体 | ストレージ |
|---|---|---|---|
| RDS | リードレプリカ（手動、最大 15 個） | インスタンスクラスの変更 | ストレージの自動スケーリング |
| Aurora | Aurora Auto Scaling でレプリカを増減（最大 15） | ライターのクラス変更 | 自動 |
| Aurora Serverless v2 | ACU で自動 | ACU で自動。0.5 ACU 単位、最大 256 | 自動 |
| DynamoDB | Auto Scaling、オンデマンド | Auto Scaling、オンデマンド | 自動 |

**RDS のストレージの自動スケーリング:** 次の条件をすべて満たすと、ストレージを増やします。

- 空き容量が割り当ての 10% 以下です。
- その状態が 5 分以上続いています。
- 前回の変更の最適化が完了し、過去 24 時間の変更が 4 回未満です。

増やす量は、10 GiB、割り当ての 10%、今後 7 時間の予測増加分のうち、最も大きい値です。最大ストレージしきい値を、現在の割り当てより 10% 以上大きくします。

**Aurora Auto Scaling:** ライターの負荷には効きません。読み取りのレプリカだけを増減します。

**DynamoDB:**

| 設定 | 内容 |
|---|---|
| オンデマンド | 容量計画が不要。読めない負荷に |
| プロビジョンド + Auto Scaling | 目標使用率は 20〜90%、推奨 70% |
| GSI | テーブルとは別に設定する |
| CLI や CloudFormation | Auto Scaling は自動で入らない。自分で設定する |
| 減らす回数 | 1 日最大 27 回 |

**例:** 急増で `ProvisionedThroughputExceededException` が出ます。Auto Scaling は数分かかるので、短い急増ならオンデマンドや DAX も検討します。パーティションキーの偏りでも発生します。

ストレージの自動スケーリングと Aurora Auto Scaling は、公式ドキュメントで確認して書いています。

詳細: [リードレプリカ](../../services/databases.md#read-replicas)、[Aurora](../../services/databases.md#aurora)、[Aurora Serverless v2](../../services/databases.md#aurora-serverless-v2)、[キャパシティモード](../../services/dynamodb.md#capacity)、[DynamoDB の Auto Scaling](../../services/dynamodb.md#provisioned-auto-scaling)。公式: [ストレージの自動スケーリング](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_PIOPS.Autoscaling.html)、[Aurora Auto Scaling](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/Aurora.Integrating.AutoScaling.html)

## タスク 2.2: 高可用で回復力のある環境を実装する {#task-2-2}

### 2.2.1 ELB と Route 53 のヘルスチェック {#skill-2-2-1}

| 項目 | ALB のターゲットグループ | Route 53 |
|---|---|---|
| 確認元 | ロードバランサーの各ノード | インターネット上のチェッカー |
| 既定の間隔 | 30 秒 | 30 秒（Fast は 10 秒） |
| 判定 | 異常 2 回、正常 5 回（既定） | 連続 3 回（既定）。チェッカーの 18% 超が正常なら正常 |
| プライベートのリソース | 確認できる | 届かない。CloudWatch アラーム型を使う |

ALB は、すべてのターゲットが異常になると、全ターゲットへ転送します（フェイルオープン）。

**ALB の理由コード:**

| コード | 確認すること |
|---|---|
| `Target.ResponseCodeMismatch` | パスの誤り、認証が必要なパス、`Matcher` |
| `Target.Timeout` | セキュリティグループ、アプリの応答速度 |
| `Target.FailedHealthChecks` | ポート、アプリの起動 |

**ターゲットの状態が `unused`** なら、リスナールールの対象外、有効でない AZ、停止中などです。

**Auto Scaling との連携:** ELB ヘルスチェックを有効にしないと、アプリが 500 を返し続けても、EC2 が正常なら置き換えません。

**Route 53 の落とし穴:**

- エンドポイントのファイアウォールで、ヘルスチェッカーの IP を許可します。
- CloudWatch アラーム型は、標準解像度と基本の統計に限られます。
- 文字列の一致は、応答の先頭 5,120 バイトの中を探します。

詳細: [ALB のヘルスチェック](../../services/networking.md#alb-health-checks)、[ヘルスチェックの計算](../../services/networking.md#health-check-calc)、[ALB のエラーの原因](../../services/networking.md#alb-error-detail)、[Route 53 のヘルスチェック](../../services/networking.md#route53-health-checks)、[Auto Scaling のヘルスチェック](../../services/ec2-beanstalk.md#asg-health-checks)、[Route 53 のフェイルオーバー設計](../../services/resilience.md#route53-failover)

### 2.2.2 耐障害性のある構成 {#skill-2-2-2}

| サービス | Multi-AZ の方法 | 注意 |
|---|---|---|
| EC2 | Auto Scaling を複数 AZ に | 1 AZ だと全停止する |
| ALB、NLB | 複数 AZ のサブネット | NLB のクロスゾーンは既定で無効 |
| RDS Multi-AZ DB インスタンス | 同期スタンバイ | スタンバイは読めない。切り替えは通常 60〜120 秒 |
| RDS Multi-AZ DB クラスター | 読み取り可のリーダー 2 台 | 切り替えは通常 35 秒未満 |
| Aurora | 3 AZ の 6 ストレージノード | レプリカの昇格の優先度を設定できる |
| ElastiCache | レプリカと Multi-AZ | レプリカ 0 で故障すると全データを失う |
| NAT ゲートウェイ | AZ ごとに作る | 1 つだと、その AZ の障害で他の AZ の外向き通信も止まる |
| EFS | Regional タイプ | One Zone は 1 AZ |
| EBS | 1 AZ のみ | スナップショットで別の AZ へ |

**DNS の切り替え:** RDS のフェイルオーバーは DNS で切り替わります。IP を保持せず、DNS の TTL を短くします。JVM なら TTL を 60 秒以下にします。

**ARC（Amazon Application Recovery Controller）:** AZ の障害ではゾーンシフトで、その AZ へのトラフィックを外します。リージョンの切り替えはルーティングコントロールで行います。

**データプレーンで切り替えます。** 障害のときは、作成や更新の API が使えないことがあります。Route 53 のヘルスチェックに基づく切り替えは、レコードの編集が不要です。

**容量の計算:** 3 AZ で常に 6 台が必要なら、AZ を 1 つ失っても 6 台残るよう、AZ あたり 3 台、合計 9 台にします。

詳細: [サービスごとの Multi-AZ と Multi-Region](../../services/resilience.md#patterns-by-service)、[高可用性のための Auto Scaling](../../services/resilience.md#auto-scaling-ha)、[静的安定性](../../services/resilience.md#static-stability)、[ARC](../../services/resilience.md#arc)、[ゾーンシフト](../../services/resilience.md#arc-zonal)、[データプレーン](../../services/resilience.md#failover-data-plane)、[クロスゾーン負荷分散](../../services/networking.md#cross-zone)、[ElastiCache のレプリケーション](../../services/databases.md#elasticache-replication)

## タスク 2.3: バックアップと復元の戦略を実装する {#task-2-3}

### 2.3.1 スナップショットとバックアップの自動化 {#skill-2-3-1}

| 手段 | 対象 | 選ぶ場面 |
|---|---|---|
| AWS Backup | EC2、EBS、RDS、Aurora、DynamoDB、EFS、FSx、S3 など | 複数サービスを一元管理、別リージョン、別アカウント |
| Data Lifecycle Manager | EBS スナップショット、EBS の AMI | EBS と AMI だけを追加料金なしで |
| RDS の自動バックアップ | RDS | 保持期間 0〜35 日で設定する |
| DynamoDB の PITR | DynamoDB | 既定は無効。1〜35 日 |

**AWS Backup の設定:**

| 設定 | 内容 |
|---|---|
| プランとルール | 頻度は最短 1 時間。毎日のバックアップで RPO 1 時間は満たせない |
| リソースの割り当て | タグで選ぶと、新しいリソースも対象になる |
| ボールト | KMS キーとアクセスポリシー |
| コピー | 別リージョン、別アカウントのボールトへ |
| コールドへの移行 | 最低 90 日。保持期間は移行日数 + 90 日以上 |
| 継続的バックアップ | PITR、最大 35 日 |
| Vault Lock | 削除や保持期間の短縮を防ぐ |

**落とし穴:** RDS の保持期間を 0 と 0 以外の間で変更すると、停止が発生します。保持期間が 0 だと、リードレプリカも作れません。

**組織全体:** Organizations のバックアップポリシーで統一します。

Data Lifecycle Manager と RDS の保持期間は公式ドキュメントで確認して書いています。

詳細: [AWS Backup](../../services/resilience.md#backup)、[プランとルール](../../services/resilience.md#backup-plans)、[割り当て](../../services/resilience.md#backup-assignment)、[ボールト](../../services/resilience.md#backup-vaults)、[Vault Lock](../../services/resilience.md#vault-lock)、[リージョン間コピー](../../services/resilience.md#backup-cross-region)、[EBS のスナップショット](../../services/storage.md#ebs-snapshots)、[DynamoDB のバックアップ](../../services/dynamodb.md#backup)。公式: [Data Lifecycle Manager](https://docs.aws.amazon.com/ebs/latest/userguide/snapshot-lifecycle.html)、[RDS の保持期間](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_WorkingWithAutomatedBackups.BackupRetention.html)

### 2.3.2 データベースの復元 {#skill-2-3-2}

RTO、RPO、費用で方法を選びます。

| 方法 | RPO の目安 | 復元先 | 注意 |
|---|---|---|---|
| RDS の PITR | トランザクションログの S3 へのアップロードは 5 分ごと | **新しい DB インスタンス** | エンドポイントが変わる |
| RDS のスナップショットの復元 | 取得した時点 | **新しい DB インスタンス** | 既存のインスタンスへは上書きできない |
| Aurora のバックトラック | ウィンドウ内の時点 | **同じクラスター**（Aurora MySQL のみ） | バックアップから復元せず速い。変更記録に時間課金 |
| DynamoDB の PITR | 通常は現在の約 5 分前まで | **新しいテーブル** | Auto Scaling、アラーム、タグ、TTL などは再設定する |
| リードレプリカの昇格 | 複製の遅延ぶん | 昇格したレプリカ | 誤削除も複製されるので、それには使えない |

**復元直後の性能:** RDS のスナップショットから復元した DB は、データをバックグラウンドで読み込みます。読み込み前のデータへの初回アクセスは遅くなります。全表スキャンで先に読み込むと影響を減らせます。

**例:** 10 分前に誤ってテーブルを消しました。RPO は数分で、本番の接続先は変えたくありません。Aurora MySQL でバックトラックが有効なら、それで戻します。RDS なら PITR で新しいインスタンスを作り、アプリの接続先か、DNS を切り替えます。

**例:** 手動の毎日のスナップショットしかない DB が壊れると、最大 1 日分のデータを失います。RPO を短くするには、自動バックアップを有効にして PITR を使います。

RDS の PITR、スナップショットの復元、Aurora のバックトラックは公式ドキュメントで確認して書いています。

詳細: [RTO と RPO](../../services/resilience.md#rto-rpo)、[達成できるかの計算](../../services/resilience.md#rto-rpo-budget)、[DynamoDB のバックアップと復元](../../services/dynamodb.md#backup)、[Aurora](../../services/databases.md#aurora)。公式: [RDS の PITR](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_PIT.html)、[スナップショットからの復元](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_RestoreFromSnapshot.html)、[バックトラック](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/AuroraMySQL.Managing.Backtrack.html)

### 2.3.3 ストレージのバージョニング {#skill-2-3-3}

**S3 のバージョニング:**

| 動作 | 内容 |
|---|---|
| 削除 | 削除マーカーが付くだけ。マーカーを消すと戻る |
| 上書き | 新しいバージョンが増える。前のバージョンも課金される |
| 一度有効にすると | 無効にできない。一時停止だけ |
| 古いバージョンの整理 | ライフサイクルの `NoncurrentVersionExpiration` |
| レプリケーション | 両方のバケットでバージョニングが必要 |

**FSx の世代管理:**

| タイプ | ユーザーが戻す | バックアップ | 別リージョン |
|---|---|---|---|
| Windows | シャドウコピー（既定で無効） | 自動は既定で有効、0〜90 日 | バックアップのコピー |
| Lustre | なし（S3 のバージョニングを使う） | Persistent で S3 にリンクなしのみ | バックアップのコピー |
| ONTAP | スナップショット | 自動と手動、最大 90 日 | SnapMirror |

**例:** Windows のユーザーが、自分で昨日のファイルを戻したいです。FSx for Windows File Server のシャドウコピーを有効にします。

詳細: [S3 のバージョニング](../../services/s3.md#versioning)、[削除マーカー](../../services/s3.md#delete-markers)、[レプリケーション](../../services/s3.md#replication)、[FSx のバックアップと世代管理](../../services/storage-advanced.md#fsx-protection)、[Windows の機能](../../services/storage-advanced.md#fsx-windows-features)

### 2.3.4 災害復旧の手順 {#skill-2-3-4}

| 戦略 | 待機側の状態 | RTO、RPO の目安 | 費用 |
|---|---|---|---|
| バックアップと復元 | データのコピーのみ | 時間単位 | 最小 |
| パイロットライト | データは複製。アプリは停止か未作成 | 数十分 | 小 |
| ウォームスタンバイ | 縮小した完全なコピーが稼働 | 数分 | 中 |
| マルチサイトアクティブ/アクティブ | 全量が稼働 | ほぼ 0 | 最大 |

**見分け方:** パイロットライトはそのままではリクエストを処理できません。ウォームスタンバイは、容量は少なくても、すぐ処理できます。

**手順のベストプラクティス:**

| 項目 | 内容 |
|---|---|
| 復元のテスト | 試していないバックアップは当てにならない。AWS Backup の復元テストを使う |
| インフラ | CloudFormation などの IaC で再作成する |
| クォータと容量 | DR リージョンで事前に確認する |
| 破損への備え | レプリケーションは破損も複製する。時点復旧のバックアップも持つ |
| 切り替え | データプレーンの操作で行う |
| 演習 | Fault Injection Service で障害を試す |

**例:** 本番 12 台、DR に 2 台が常時稼働しています。これはウォームスタンバイです。障害時は 2 台で処理を始めながら 12 台に増やします。

**例:** Aurora のセカンダリだけが動き、Auto Scaling グループは希望 0 台です。これはパイロットライトです。

詳細: [4 つの DR 戦略](../../services/resilience.md#dr-strategies)、[バックアップと復元](../../services/resilience.md#backup-restore)、[パイロットライト](../../services/resilience.md#pilot-light)、[ウォームスタンバイ](../../services/resilience.md#warm-standby)、[アクティブ/アクティブ](../../services/resilience.md#active-active)、[復元テスト](../../services/resilience.md#backup-testing)、[Fault Injection Service](../../services/resilience.md#fis)、[選び方の比較](../../services/resilience.md#choosing)

## 確認問題 {#self-check}

??? question "問1: CLI で作った Auto Scaling グループで、ELB ヘルスチェックを有効にした直後から、起動と終了を繰り返すようになりました。アプリの起動には 4 分かかります。原因と対処は？"
    ヘルスチェックの猶予期間が CLI の既定の 0 秒のままで、起動中に異常と判定されています。猶予期間を起動時間より長い値（例: 300 秒）にします。

??? question "問2: 本番の RDS for PostgreSQL で、早朝のバッチの後に空き容量が 10% を切ることがあり、人手で容量を増やしています。停止を避けて自動化するには？"
    ストレージの自動スケーリングを有効にし、最大ストレージしきい値を設定します。空き容量が 10% 以下で 5 分以上続くと増えます。過去 24 時間の変更が 4 回以上なら増えないので、増加が速い場合は余裕を持った割り当ても検討します。

??? question "問3: Route 53 のフェイルオーバーレコードで、プライベートサブネットの内部 ALB の正常性を確認したいです。エンドポイント型のヘルスチェックが常に異常になります。どう直しますか？"
    ヘルスチェッカーはインターネット上にあるので、内部のリソースには届きません。ALB の `HealthyHostCount` に CloudWatch アラームを作り、アラーム型のヘルスチェックを使います。アラームは標準解像度と基本の統計で作ります。

??? question "問4: Multi-AZ の RDS DB インスタンスで、読み取りの負荷を下げたくてスタンバイへ接続しようとしましたが、接続できません。正しい対処は？"
    Multi-AZ DB インスタンスのスタンバイは読み取れません。リードレプリカを作ってアプリの接続先を分けるか、読み取り可能なリーダーを持つ Multi-AZ DB クラスターに移します。

??? question "問5: 本番の EBS、RDS、DynamoDB、EFS のバックアップを、タグで指定して別リージョンにも残し、誤削除も防ぎたいです。何を使いますか？"
    AWS Backup です。プランのルールでスケジュールとコピー先を指定し、タグでリソースを割り当てます。ボールトに Vault Lock を設定すると、削除を防げます。Data Lifecycle Manager は EBS スナップショットと AMI が対象なので、この要件には足りません。

??? question "問6: DR 側で Aurora のセカンダリだけを動かしています。RTO を 30 分から 5 分に短くするよう求められました。最小の変更はどれですか？"
    DR 側で、縮小した台数のアプリを常時動かすウォームスタンバイに変えます。今の構成はパイロットライトで、起動を待つぶん時間がかかります。切り替えは Route 53 のヘルスチェックや ARC のように、データプレーンの操作で行えるようにします。

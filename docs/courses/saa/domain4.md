# 分野4: コストを最適化したアーキテクチャの設計

配点は **20%** です。ストレージ、コンピューティング、データベース、ネットワークの 4 つで、要件を満たす中で最も安いものを選びます。

「最も費用対効果が高い」という問題でも、要件を満たさない安い選択肢は誤りです。まず可用性や保持の要件で絞り、残った中で費用を比べます。

コスト管理のツールは 4 つのタスクすべてに出てきます。詳しい説明は[タスク 4.1](#t4-1-cost-tools)に置き、他のタスクでは使い方の違いを扱います。

各見出しの「ガイドの項目」は、試験ガイドの Knowledge of（知識）と Skills in（スキル）を、ガイドに載っている順の番号で示したものです。

この分野に限らず、コース全体で使うサービスは[サービス一覧](services.md)から確認できます。

## タスク 4.1: コストを最適化したストレージを設計する {#task-4-1}

### コスト管理の機能とツール {#t4-1-cost-tools}

**ガイドの項目:** 知識2 コスト管理の機能（コスト配分タグ、複数アカウントの請求） / 知識3 コスト管理ツールの適切な用途（Cost Explorer、Budgets、Cost and Usage Report）

| 要件 | 選択 |
|---|---|
| 過去の費用をグラフで分析、予測 | Cost Explorer |
| しきい値を超えたら、または超えそうなら通知 | Budgets |
| 行単位の最も詳しいデータを Athena で分析 | Cost and Usage Report（CUR） |
| いつものパターンから外れた費用を検出 | Cost Anomaly Detection |
| 部門ごとに費用を分ける | コスト配分タグ |
| 複数アカウントの請求をまとめる、割引を共有 | Organizations の一括請求 |

コスト配分タグは、リソースに付けるだけでは請求データに出ません。**有効化が必要**です。

ストレージでは、S3 の使用状況と傾向を S3 Storage Lens で確認できます。

!!! note "Cost and Usage Report の状況"
    ガイドの Cost and Usage Report は引き続き使えますが、現在の推奨は Data Exports で作る CUR 2.0 です。列のスキーマが固定で、Parquet にも対応します。

詳細: [Cost Explorer](../../services/cost-management.md#cost-explorer)、[Budgets](../../services/cost-management.md#budgets)、[Data Exports と CUR](../../services/cost-management.md#data-exports)、[Cost Anomaly Detection](../../services/cost-management.md#cost-anomaly-detection)、[コスト配分タグ](../../services/cost-management.md#cost-allocation-tags)、[一括請求](../../services/cost-management.md#consolidated-billing)、[推奨を出すサービスの違い](../../services/cost-management.md#recommendation-tools)

### 最も費用対効果の高いストレージサービス {#t4-1-services}

**ガイドの項目:** 知識4 ストレージサービスの適切な用途（FSx、EFS、S3、EBS） / 知識11 ストレージの種類と特徴（オブジェクト、ファイル、ブロック） / スキル10 ワークロードに最も費用対効果の高いストレージサービスの選択

| サービス | 課金の中心 | 費用を下げる手段 |
|---|---|---|
| S3 | 使った容量とリクエスト | ストレージクラス、ライフサイクル |
| EFS | 使った容量 | IA と Archive へのライフサイクル、One Zone |
| EBS | 確保した容量 | `gp2` から `gp3` へ、使っていないボリュームの削除 |
| FSx | 確保した容量と性能 | タイプの選択、ONTAP の階層化 |
| インスタンスストア | インスタンス料金に含む | 消えてよい一時データに使う |

**例**: 再作成できるデータを 1 つの AZ で共有するなら、EFS One Zone で費用を下げられます。失えないデータには使いません。

詳細: [EBS、EFS、S3、FSx の比較](../../services/storage-advanced.md#storage-comparison)、[EFS のライフサイクル](../../services/storage.md#efs-lifecycle)、[FSx for ONTAP の階層化](../../services/storage-advanced.md#fsx-ontap-tiering)、[S3 のストレージ費用](../../services/cost-management.md#s3-cost)

### アクセスパターンとストレージ階層 {#t4-1-tiers}

**ガイドの項目:** 知識9 ストレージのアクセスパターン / 知識10 ストレージの階層化（オブジェクトストレージのコールド階層） / スキル8 適切なストレージ階層の選択

| アクセス | クラス | 最小保存期間 | 取得 |
|---|---|---|---|
| 頻繁 | Standard | なし | ミリ秒 |
| 不明、変わる | Intelligent-Tiering | なし | ミリ秒（アーカイブ階層は復元が必要）。取得料金なし |
| 月 1 回程度、失えない | Standard-IA | 30 日 | ミリ秒、取得料金あり |
| 月 1 回程度、再作成できる | One Zone-IA | 30 日 | ミリ秒、取得料金あり |
| 四半期に 1 回、すぐ読みたい | Glacier Instant Retrieval | 90 日 | ミリ秒 |
| 年 1 回程度 | Glacier Flexible Retrieval | 90 日 | 分から時間 |
| 年 1 回未満、長期保管 | Glacier Deep Archive | 180 日 | 12 時間以内（Bulk は 48 時間以内） |

- 平均 20 KB の小さなオブジェクトを大量に Standard-IA に置くと、128 KB 分で課金されるので不利です。
- 30 日の Standard-IA を 10 日で消しても、30 日分課金されます。
- 頻繁に読むのに IA に置くと、取得料金で割高になります。

詳細: [ストレージクラス](../../services/s3.md#storage-classes)、[Glacier のデータ取得](../../services/s3.md#glacier-retrieval)

### データのライフサイクル {#t4-1-lifecycle}

**ガイドの項目:** 知識7 データのライフサイクル / スキル5 S3 オブジェクトのライフサイクル管理 / スキル9 ストレージの適切なデータライフサイクルの選択

アクセスの傾向が分かっているなら、ライフサイクルルールで移します。

| 要件 | ルール |
|---|---|
| 30 日後に Standard-IA、1 年で削除 | 移行アクションと失効アクション |
| 古いバージョンを残しすぎない | `NoncurrentVersionExpiration` |
| 未完了のマルチパートを片付ける | `AbortIncompleteMultipartUpload` |

- 移行は Standard から低コスト側への一方向です。Deep Archive から戻すルールは作れません。
- 128 KB 未満のオブジェクトは、既定では移行しません。
- アクセスの傾向が読めないなら、ルールではなく Intelligent-Tiering を選びます。

他のサービスにもライフサイクルがあります。

| サービス | 仕組み |
|---|---|
| EFS | 既定で 30 日アクセスなしで IA、90 日で Archive |
| EBS スナップショット | Data Lifecycle Manager、Snapshots Archive |
| CloudWatch Logs | 保持期間 |
| DynamoDB | TTL |

詳細: [S3 ライフサイクル](../../services/s3.md#lifecycle)、[ライフサイクルのルール要素](../../services/s3.md#lifecycle-elements)、[データの保持](../../services/storage.md#retention)、[DynamoDB の TTL](../../services/dynamodb.md#ttl)

### ブロックストレージと適切なサイズ {#t4-1-block}

**ガイドの項目:** 知識6 ブロックストレージの選択肢（HDD、SSD のボリュームタイプ） / スキル2 ワークロードに合う正しいストレージサイズの判断

| 要件 | 最も安い選択 |
|---|---|
| 一般的なブート、DB | `gp3` |
| 大きなファイルの順次読み書き、ログ | `st1` |
| アクセスの少ないデータ | `sc1` |
| 非常に高い IOPS が必須 | `io2` Block Express |

HDD はブートボリュームにできません。ランダムアクセスの多い DB にも向きません。

サイズは次の順に決めます。

1. 必要な容量と IOPS、スループットを見積もります。
2. `gp3` では性能を容量と別に買えるので、容量は実データに合わせます。
3. 使用率を監視します。EBS は増やせますが減らせないので、小さく始めます。
4. Compute Optimizer の推奨で EBS も見直します。

**例**: 500 GiB を割り当てて 80 GiB しか使わない EBS は、500 GiB 分の費用がかかります。縮小するには、小さなボリュームを作ってデータを移します。

詳細: [EBS のボリュームタイプ](../../services/storage.md#ebs-volume-types)、[ボリュームの変更](../../services/storage.md#ebs-modify)、[Compute Optimizer](../../services/cost-management.md#compute-optimizer)

### ストレージの自動スケーリング {#t4-1-autoscale}

**ガイドの項目:** スキル4 ストレージの自動スケーリングが必要な場面の判断

| サービス | 容量の増え方 |
|---|---|
| S3、EFS | 自動。使った分だけの課金 |
| Aurora | クラスターボリュームが自動で増減 |
| RDS | ストレージの自動スケーリングを有効にする |
| EBS | 自動では増えない。Elastic Volumes で変更する |

RDS のストレージの自動スケーリングは、予測しにくい増加に向きます。

| 項目 | 内容 |
|---|---|
| 発動の条件 | 空きが割り当ての 10% 以下で、5 分以上続き、前回の変更の最適化が完了していて、過去 24 時間の変更が 4 回未満 |
| 増える量 | 10 GiB、割り当ての 10%、今後 7 時間の予測増加分のうち最大のもの |
| 最大しきい値 | 割り当てより 10% 以上大きく設定する。公式の推奨は 26% 以上 |
| 減らせるか | 減らせない |
| 限界 | 大量のロードでは間に合わないことがある |

最初から大きなストレージを確保するより、小さく始めて自動スケーリングに任せたほうが安くなります。

詳細: [RDS のストレージの自動スケーリング（公式）](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_PIOPS.Autoscaling.html)、[Aurora のストレージ（公式）](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/Aurora.Overview.StorageReliability.html)

### アクセスのオプション {#t4-1-access}

**ガイドの項目:** 知識1 アクセスのオプション（リクエスタ支払いの S3 バケット）

通常はバケット所有者がリクエストとダウンロードの費用を払います。リクエスタ支払いでは利用者が払います。ストレージの費用は常に所有者です。

- 匿名アクセスはできず、すべて認証が必要です。
- リクエストは `x-amz-request-payer` で同意を示します。付けないと 403 です。

**例**: 別の会社に大きなデータセットを公開し、ダウンロードの費用を負担したくないなら、リクエスタ支払いです。

他のアカウントのユーザーに読ませるだけなら、署名付き URL やアクセスポイントも候補ですが、費用の負担先は変わりません。

詳細: [リクエスタ支払い](../../services/s3.md#requester-pays)、[アクセスポイント](../../services/s3.md#access-points)

### アップロードの戦略 {#t4-1-uploads}

**ガイドの項目:** スキル1 適切なストレージ戦略の設計（S3 へのバッチアップロードと個別アップロードの比較）

S3 はリクエストごとに課金されます。小さなファイルを 1 つずつ `PUT` すると、リクエストの費用が増えます。

| 状況 | 戦略 |
|---|---|
| 小さなログが大量にある | Firehose でまとめて 1 つのオブジェクトにする |
| 小さなファイルを IA に置きたい | まとめてから置く（128 KB の最小課金を避ける） |
| 100 MB 以上のファイル | マルチパートで失敗した部分だけ再送する |
| 5 GB を超えるファイル | マルチパートが必須 |
| 既存の多数のオブジェクトを一括処理 | S3 Batch Operations |

まとめると、Athena で読むときの性能も上がります。

詳細: [マルチパートアップロード](../../services/s3.md#multipart-upload)、[片付けの設定](../../services/s3.md#abort-multipart)、[Firehose のバッファ](../../services/streaming.md#firehose-buffering)、[S3 のストレージ費用](../../services/cost-management.md#s3-cost)

### バックアップとアーカイブ {#t4-1-backup}

**ガイドの項目:** 知識5 バックアップの戦略 / スキル6 適切なバックアップやアーカイブのソリューションの選択

| 要件 | 選択 |
|---|---|
| 複数のサービスのバックアップを一元管理 | AWS Backup |
| 長期のアーカイブを最小の費用で | S3 Glacier Deep Archive |
| 90 日以上保持する EBS スナップショット | Snapshots Archive（費用を最大 75% 削減） |
| 物理テープをやめて既存のソフトを使う | Tape Gateway |
| 誤って消したスナップショットを戻す | Recycle Bin |

バックアップの頻度と保持期間は RPO と規制から決めます。必要以上に長く残すと費用が増えます。AWS Backup ならプランでコールドストレージへの移行も設定できます。

詳細: [AWS Backup](../../services/resilience.md#backup)、[バックアッププランとルール](../../services/resilience.md#backup-plans)、[EBS スナップショット](../../services/storage.md#ebs-snapshots)、[Storage Gateway](../../services/migration.md#storage-gateway)

### データの移行とハイブリッド {#t4-1-transfer}

**ガイドの項目:** 知識8 ハイブリッドストレージの選択肢（DataSync、Transfer Family、Storage Gateway） / スキル3 ワークロードのデータを AWS ストレージへ転送する最も安い方法の判断 / スキル7 ストレージサービスへのデータ移行に適したサービスの選択

まず転送にかかる日数を計算します。

```text
日数 = (データ量のバイト数 × 8) ÷ (回線の bps × 利用率 × 3600 × 1 日に使える時間)
```

1 Gbps、利用率 80%、24 時間で、100 TB が約 12 日です。あとは比例で計算できます。

| 条件 | 選択 |
|---|---|
| 既存の回線で期限に間に合う | DataSync か、インターネットでのアップロード（受信のデータ転送は無料） |
| ファイルサーバーを S3、EFS、FSx へ移す | DataSync |
| 取引先の SFTP を変えずに S3 へ | Transfer Family |
| オンプレミスのアプリが使い続ける | Storage Gateway |
| 回線が足りないが増やせる | 期間限定の Direct Connect と DataSync |
| 回線に乗らない、数十 TB 以上 | Snow Family の役割（下の状況を参照） |
| DB の移行 | DMS |
| サーバーの移行 | Application Migration Service |

!!! note "移行サービスの状況"
    - **Snow Family**: 新規のお客様には提供されません。試験では「回線が細く、オフラインで転送する」という役割で覚えます。実務の代替は DataSync、Data Transfer Terminal、パートナーのオフライン転送、エッジ処理なら Outposts です。
    - **Application Discovery Service**: オンプレミスのサーバーの構成と依存関係を集めるサービスです。新規受付を終了しました。後継は AWS Transform です。
    - **Application Migration Service**: AWS Transform MGN に名前が変わりました。ブロック単位の継続的な複製で、サーバーを EC2 へ移す役割は同じです。

詳細: [転送方法の選び方](../../services/migration.md#choosing-transfer)、[計算式](../../services/migration.md#transfer-formula)、[DataSync](../../services/migration.md#datasync)、[Transfer Family](../../services/migration.md#transfer-family)、[Storage Gateway](../../services/migration.md#storage-gateway)、[Snow Family](../../services/migration.md#snow-family)、[Application Discovery Service](../../services/migration.md#application-discovery)、[MGN](../../services/migration.md#mgn)、[Data Transfer Terminal](../../services/migration.md#data-transfer-terminal)

## タスク 4.2: コストを最適化したコンピューティングを設計する {#task-4-2}

### コンピューティングの費用の把握 {#t4-2-tools}

**ガイドの項目:** 知識1 コスト管理の機能（コスト配分タグ、複数アカウントの請求） / 知識2 コスト管理ツールの適切な用途（Cost Explorer、Budgets、Cost and Usage Report）

| 確認すること | ツール |
|---|---|
| Savings Plans と RI の購入の推奨 | Cost Explorer |
| Savings Plans の使用率が落ちていないか | Budgets の使用率の予算 |
| インスタンスのサイズが大きすぎないか | Compute Optimizer |
| 幅広い点検 | Trusted Advisor |
| 開発環境の費用を部門で分ける | コスト配分タグ |
| RI と Savings Plans を組織で共有する | 一括請求 |

詳細: [推奨を出すサービスの違い](../../services/cost-management.md#recommendation-tools)、[予算の種類](../../services/cost-management.md#budget-types)、[Compute Optimizer](../../services/cost-management.md#compute-optimizer)、[Trusted Advisor](../../services/cloud-foundations.md#trusted-advisor)

### 購入オプション {#t4-2-purchase}

**ガイドの項目:** 知識4 購入オプション（スポットインスタンス、リザーブドインスタンス、Savings Plans）

| オプション | 割引の上限 | 向くもの |
|---|---|---|
| オンデマンド | なし | 短期、予測できない負荷 |
| Compute Savings Plans | 66% | 構成が変わる定常負荷。EC2、Fargate、Lambda |
| EC2 Instance Savings Plans | 72% | ファミリーが決まった定常負荷 |
| スタンダード RI | 72% | 構成が変わらない負荷 |
| コンバーティブル RI | 66% | 構成を交換する可能性 |
| スポット | 90% | 中断できるバッチ、CI |
| Capacity Reservation | なし | 容量の確保が必須 |
| Dedicated Hosts | - | ソケットやコア単位の BYOL |

- スポットの中断は 2 分前に通知されます。複数のインスタンスタイプと AZ を指定し、`price-capacity-optimized` で配分します。
- Savings Plans に容量の確保はありません。必要なら Capacity Reservation と併用します。
- 定常の部分には確約割引、変動の部分にはオンデマンド、中断できる部分にはスポットと組み合わせます。

**例**: 3 年間稼働するが、将来 Fargate へ移す可能性がある負荷には、Compute Savings Plans が合います。EC2 Instance Savings Plans は EC2 のファミリーに縛られます。

詳細: [購入オプション](../../services/cost-management.md#purchase-options)、[Savings Plans](../../services/cost-management.md#savings-plans)、[Reserved Instances](../../services/cost-management.md#reserved-instances)、[スポットインスタンス](../../services/cost-management.md#spot)、[選び方](../../services/cost-management.md#purchase-choice)、[スポットの中断への対応](../../services/operations.md#spot-interruptions)

### 費用対効果の高いコンピューティングと利用率の最適化 {#t4-2-compute-choice}

**ガイドの項目:** 知識8 コンピューティングの利用率の最適化（コンテナ、サーバーレス、マイクロサービス） / スキル3 費用対効果の高いコンピューティングサービスの判断（Lambda、EC2、Fargate）

| 負荷の形 | 安い選択 |
|---|---|
| まばら、アイドルが長い | Lambda（実行分のみ課金） |
| 変動があるコンテナ、管理を減らしたい | Fargate、Fargate Spot |
| 常に高い負荷が続く | EC2 と Savings Plans |
| 中断できるバッチ | Batch とスポット |
| 静的な Web サイト | S3 と CloudFront |

- コンテナに集約すれば、1 台の EC2 に複数のタスクを詰められ、余った容量を減らせます。
- マイクロサービスに分けると、負荷の高い部分だけをスケールできます。
- Lambda は `arm64`（Graviton）を選ぶと、計算の多い処理で価格性能が良くなることがあります。

詳細: [Lambda のメモリと CPU の最適化](../../services/lambda.md#memory-tuning)、[Lambda のアーキテクチャ](../../services/lambda.md#architecture)、[Fargate と EC2](../../services/containers.md#fargate-vs-ec2)、[キャパシティプロバイダー](../../services/containers.md#capacity-providers)、[AWS Batch](../../services/other-services.md#batch)、[静的ウェブサイトホスティング](../../services/s3.md#static-website)

### インスタンスのファミリーとサイズ {#t4-2-instances}

**ガイドの項目:** 知識7 インスタンスのタイプ、ファミリー、サイズ（メモリ最適化、コンピューティング最適化、仮想化） / スキル5 ワークロードに適したインスタンスファミリーの選択 / スキル6 ワークロードに適したインスタンスサイズの選択

ファミリーをワークロードに合わせると、同じ性能を安く買えます。

| ワークロード | ファミリー | 誤った選択の例 |
|---|---|---|
| インメモリの DB | R、X | M の大きなサイズでメモリを賄う |
| 動画のエンコード | C | M で CPU を賄う |
| 一般の Web | M、T | 負荷が低いのに C |
| 負荷が低く、時々の急増 | T | 常に高負荷なら CPU クレジットが尽きる |
| 機械学習の学習 | P、G | CPU だけで長時間 |
| 高 IOPS のローカルディスク | I、D | EBS に高い IOPS を買い続ける |

インスタンスタイプは次のように読みます。`m7g.xlarge` なら、M がファミリー、7 が世代、g が Graviton、xlarge がサイズです。

サイズは計測で決めます。`CPUUtilization` だけでなく、エージェントでメモリも取ります。Compute Optimizer で過剰なサイズを見つけて、小さくします。

仮想化については、現在のタイプの多くが Nitro を基盤にしています。ベアメタルは、ライセンスや性能の理由で物理サーバーへの直接のアクセスが必要なときに選びます。

詳細: [インスタンスタイプ](../../services/ec2-beanstalk.md#instance-types)、[最小のメモリとコンピューティングを決める](../../services/ec2-beanstalk.md#sizing)、[リソース使用量の最適化](../../services/observability.md#resource-optimization)、[Compute Optimizer と適正サイズ](../../services/cost-management.md#compute-optimizer)

### スケーリングと休止 {#t4-2-scaling}

**ガイドの項目:** 知識9 スケーリング戦略（Auto Scaling、休止） / スキル2 弾力的なワークロードのスケーリング方法と戦略の判断（水平と垂直、EC2 の休止）

| 状況 | 方法 |
|---|---|
| 負荷に応じて台数を変える | 水平の Auto Scaling |
| 夜間は不要 | スケジュールで 0 台に、または停止 |
| 水平にできない DB など | 垂直に上げる |
| 起動が遅いアプリを夜間に止めたい | 休止 |
| 起動が遅いアプリをすぐ増やしたい | ウォームプール |

休止は、メモリの内容を EBS のルートボリュームに保存して停止します。再開すると、メモリの状態から続けられます。

| 休止の条件 | 値 |
|---|---|
| 有効化 | 起動時のみ。既存のインスタンスには設定できない |
| RAM | Linux は 150 GiB 未満、Windows は 16 GiB 以下 |
| ルートボリューム | 暗号化が必須で、RAM が入る空きが必要 |
| 課金 | `stopped` の間はインスタンス料金なし。EBS の料金はかかる |

スケーリングの指標が適切でないと、過剰な台数になって費用が増えます。

詳細: [休止](../../services/operations.md#hibernate)、[EC2 Auto Scaling](../../services/ec2-beanstalk.md#auto-scaling)、[ウォームプール](../../services/operations.md#warm-pools)、[混合インスタンス](../../services/operations.md#mixed-instances)、[スケーリングの失敗の調査](../../services/operations.md#asg-troubleshooting)

### 負荷分散の選択 {#t4-2-lb}

**ガイドの項目:** スキル1 適切な負荷分散の戦略の判断（レイヤー 7 の ALB、レイヤー 4 の NLB、Gateway Load Balancer の比較）

| | ALB | NLB | GWLB |
|---|---|---|---|
| 層 | 7 | 4 | 3 |
| 振り分け | パス、ホスト、ヘッダー | ポート | 全ポートの IP パケット |
| 向く場面 | Web、マイクロサービス | 固定 IP、非 HTTP、高負荷 | ファイアウォールの仮想アプライアンス |

費用の観点では、要件に合う最小のものを選びます。HTTP のパスで振り分けるだけなら、サービスごとに ALB を立てず、1 つの ALB のリスナールールにまとめます。ALB の後ろの Lambda で済むなら、常時動く EC2 が要らないこともあります。

詳細: [ALB と NLB の違い](../../services/networking.md#alb-vs-nlb)、[リスナーとルール](../../services/networking.md#alb-listeners)、[GWLB](../../services/networking.md#gwlb)

### ワークロードの種類ごとの可用性 {#t4-2-availability}

**ガイドの項目:** 知識3 グローバルインフラストラクチャ（AZ、リージョン） / スキル4 ワークロードの種類ごとに必要な可用性の判断（本番、非本番）

本番と同じ構成を全環境に持つ必要はありません。

| 環境 | 構成の例 |
|---|---|
| 本番 | 複数 AZ、Multi-AZ の DB、Savings Plans |
| ステージング | 複数 AZ、必要な時間だけ起動 |
| 開発、テスト | 1 AZ、シングル AZ の DB、夜間停止、スポット |
| 中断できるバッチ | スポット、再実行できる形に |

AZ の数を増やすと可用性は上がりますが、AZ 間の転送料と余分な容量がかかります。リージョンごとに料金が違うことも、配置の判断材料です。データの所在の制約がなければ、安いリージョンを選べます。

詳細: [リージョン](../../services/cloud-foundations.md#regions)、[アベイラビリティーゾーン](../../services/cloud-foundations.md#availability-zones)、[データ転送の費用](../../services/cost-management.md#data-transfer)、[サービスごとの Multi-AZ と Multi-Region](../../services/resilience.md#patterns-by-service)

### エッジとハイブリッドのコンピューティング {#t4-2-edge-hybrid}

**ガイドの項目:** 知識5 分散コンピューティングの戦略（エッジ処理） / 知識6 ハイブリッドコンピューティングの選択肢（Outposts）

| 要件 | 選択 |
|---|---|
| エッジで簡単なリクエスト処理をし、オリジンの負荷を減らす | CloudFront Functions、Lambda@Edge |
| データをオンプレミスに置き、AWS の API で動かす | Outposts |
| 5G 端末向けの低遅延 | Wavelength |
| オンプレミスのサーバーを活かして ECS や EKS を動かす | ECS Anywhere、EKS Anywhere |
| ソフトウェアのライセンスの超過を防ぐ | License Manager |
| VMware の運用をそのまま移す | VMware Cloud on AWS |

!!! note "VMware Cloud on AWS の状況"
    2024 年 4 月 30 日から AWS は再販していません。Broadcom と認定販売店が販売します。AWS のサービスとして VPC 内で VMware を動かすなら、Amazon Elastic VMware Service（EVS）があります。

詳細: [Lambda@Edge と CloudFront Functions](../../services/networking.md#edge-functions)、[Outposts](../../services/cloud-foundations.md#outposts)、[Wavelength](../../services/cloud-foundations.md#wavelength)、[ECS Anywhere](../../services/operations.md#ecs-anywhere)、[EKS Anywhere](../../services/operations.md#eks-anywhere)、[License Manager](../../services/governance.md#license-manager)、[VMware の移行](../../services/migration.md#vmware)

## タスク 4.3: コストを最適化したデータベースを設計する {#task-4-3}

### データベースの費用の把握 {#t4-3-tools}

**ガイドの項目:** 知識1 コスト管理の機能（コスト配分タグ、複数アカウントの請求） / 知識2 コスト管理ツールの適切な用途（Cost Explorer、Budgets、Cost and Usage Report）

| 確認すること | ツール |
|---|---|
| RDS の RI や Database Savings Plans の推奨 | Cost Explorer |
| I/O の費用が大きくないか | CUR、Cost Explorer の使用タイプ |
| RDS のスナップショットの費用を DB ごとに分ける | スナップショットに付けたコスト配分タグ |
| 組織で RI と Savings Plans を共有する | 一括請求 |

スナップショットの費用はスナップショットの単位で計上されます。元の DB のタグは自動では付かないので、タグのコピーを有効にします。

詳細: [Cost Explorer](../../services/cost-management.md#cost-explorer)、[Data Exports と CUR](../../services/cost-management.md#data-exports)、[Savings Plans](../../services/cost-management.md#savings-plans)、[コスト配分タグ](../../services/cost-management.md#cost-allocation-tags)

### 費用対効果の高いデータベースサービス {#t4-3-services}

**ガイドの項目:** 知識9 データベースの種類とサービス（リレーショナルと非リレーショナル、Aurora、DynamoDB） / スキル3 費用対効果の高いデータベースサービスの判断（DynamoDB と RDS の比較、サーバーレス）

| 要件 | 安い選択 |
|---|---|
| キーで引くだけ、負荷がまばら | DynamoDB オンデマンド |
| キーで引く、安定した大量のトラフィック | DynamoDB プロビジョンドと Auto Scaling |
| 古いデータが多く、アクセスが少ない DynamoDB | `STANDARD_INFREQUENT_ACCESS` のテーブルクラス |
| 結合が必要で、規模は小さく一定 | RDS と RI |
| 負荷の変動が大きい SQL | Aurora Serverless v2（夜間は最小 0 ACU と自動一時停止） |
| I/O の費用が Aurora の総額の 25% 以上 | Aurora I/O-Optimized |
| I/O が少ない Aurora | Aurora Standard |

Database Savings Plans は最大 35% の割引で、Aurora、RDS、DynamoDB、ElastiCache などに使えます。エンジン、ファミリー、リージョンを問いません。

詳細: [DynamoDB のキャパシティモード](../../services/dynamodb.md#capacity)、[テーブルクラス](../../services/dynamodb.md#table-classes)、[Aurora Serverless v2](../../services/databases.md#aurora-serverless-v2)、[Savings Plans](../../services/cost-management.md#savings-plans)、[Aurora のストレージ（公式）](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/Aurora.Overview.StorageReliability.html)

### データベースの形式 {#t4-3-types}

**ガイドの項目:** スキル4 費用対効果の高いデータベースの種類の判断（時系列形式、列形式）

目的に合わない DB に無理に入れると、費用も性能も悪くなります。

| データ | 形式 | サービス |
|---|---|---|
| 大規模な集計、BI | 列形式 | Redshift（Redshift Serverless なら使う分だけ） |
| S3 上のログへの単発の SQL | 列形式のファイル | Athena と Parquet |
| IoT、メトリクス | 時系列 | Timestream |
| 関係のたどり | グラフ | Neptune |

**例**: RDS で分析の集計をしていて、本番が遅く高いなら、Redshift に移します。列形式なので、必要な列だけ読めます。

!!! note "Timestream の状況"
    Timestream for LiveAnalytics は 2025 年 6 月 20 日に新規受付を終了しました。新規の時系列ワークロードには Timestream for InfluxDB を検討します。

詳細: [Redshift](../../services/data-engineering.md#redshift)、[Redshift Serverless](../../services/data-engineering.md#redshift-serverless)、[データ形式](../../services/data-engineering.md#data-formats)、[Athena](../../services/streaming.md#athena)、[Timestream](../../services/databases-specialized.md#timestream)、[Neptune](../../services/databases-specialized.md#neptune)

### 容量の計画 {#t4-3-capacity}

**ガイドの項目:** 知識5 データベースの容量計画（キャパシティユニット）

| 方法 | 効果 |
|---|---|
| DynamoDB の RCU と WCU を計算する | プロビジョンドの過剰を避ける |
| 結果整合性の読み取りを使う | 強い整合性の半分の RCU |
| GSI を必要最小限にする | 書き込みのたびに GSI の WCU も消費する |
| RDS のインスタンスを適正なサイズに | Compute Optimizer などで確認 |
| ストレージを `gp3` に | 容量と IOPS を別に買う |

詳細: [計算方法](../../services/dynamodb.md#capacity-calculation)、[LSI と GSI](../../services/dynamodb.md#indexes)、[読み取りの整合性](../../services/dynamodb.md#read-consistency)、[Compute Optimizer](../../services/cost-management.md#compute-optimizer)

### キャッシュとレプリケーション {#t4-3-caching-replica}

**ガイドの項目:** 知識3 キャッシュの戦略 / 知識8 データベースのレプリケーション（リードレプリカ）

大きなインスタンスを買う前に、読み取りを減らします。

| 方法 | 費用の効き方 |
|---|---|
| ElastiCache | DB のインスタンスを小さくできる。TTL で必要なものだけ残す |
| DAX | DynamoDB の読み取りの RCU を減らせる |
| リードレプリカ | 読み取りを逃がせるが、レプリカ分のインスタンスとストレージの料金がかかる |
| リージョン間のレプリカ | 転送料も加わる |

キャッシュでは TTL を付け、古くて読まれないデータを残しません。

詳細: [キャッシュ戦略](../../services/databases.md#caching-strategies)、[キャッシュの使い分け](../../services/databases.md#cache-comparison)、[DAX](../../services/dynamodb.md#dax)、[リードレプリカと Multi-AZ](../../services/databases.md#read-replicas)

### 接続とプロキシ {#t4-3-proxy}

**ガイドの項目:** 知識6 データベースの接続とプロキシ

接続を効率よく使うと、DB を大きくせずに済みます。

| 状況 | 判断 |
|---|---|
| 接続数のためだけに大きなインスタンスを使っている | RDS Proxy で接続を共有して小さくする |
| Lambda が接続を毎回作っている | ハンドラーの外で再利用し、RDS Proxy も検討する |
| 接続の問題がない | RDS Proxy の費用を足す必要はない |

詳細: [接続プーリングと RDS Proxy](../../services/databases.md#connection-pooling)、[RDS Proxy](../../services/databases.md#rds-proxy)

### エンジンの選択と費用 {#t4-3-engine}

**ガイドの項目:** 知識7 データベースエンジンの適切な用途（異種間移行、同種間移行） / スキル2 適切なデータベースエンジンの判断（MySQL と PostgreSQL の比較）

| 判断 | 費用への影響 |
|---|---|
| Oracle、SQL Server のライセンス | 商用エンジンの費用がかかる |
| MySQL、PostgreSQL、Aurora へ移行 | ライセンス費用をなくせるが、異種間の変換の費用がかかる |
| MySQL か PostgreSQL か | どちらもライセンス費用はかからない。既存の資産、スキル、必要な機能で決める |
| 同種間の移行 | 変換が要らず、作業の費用が小さい |

詳細: [RDS](../../services/databases.md#rds)、[Aurora](../../services/databases.md#aurora)、[移行の 7 つの R](../../services/migration.md#seven-rs)

### バックアップと保持のポリシー {#t4-3-backup}

**ガイドの項目:** 知識4 データの保持ポリシー / スキル1 適切なバックアップと保持のポリシーの設計（スナップショットの頻度）

| サービス | 設定 |
|---|---|
| RDS の自動バックアップ | 0〜35 日。0 で無効。コンソールの既定は 7 日 |
| RDS の手動スナップショット | 削除するまで残る。DB を消しても残り、課金も続く |
| DynamoDB の PITR | 1〜35 日。期間を短くしても費用は下がらない |
| DynamoDB のオンデマンドバックアップ | 削除するまで残る |
| AWS Backup | ルールで頻度、保持、コールドストレージへの移行を設定 |

RDS のバックアップストレージは、プロビジョニングしたストレージの 100% まで無料です。超えた分が課金されます。

| 要件 | 設計 |
|---|---|
| RPO 5 分 | 自動バックアップの時点復旧 |
| 7 年の保管 | 自動バックアップでは足りない。AWS Backup のプランか手動スナップショット |
| 開発環境 | 保持を短くする |

詳細: [DynamoDB のバックアップと復元](../../services/dynamodb.md#backup)、[バックアッププランとルール](../../services/resilience.md#backup-plans)、[AWS Backup](../../services/resilience.md#backup)、[RDS のバックアップ保持（公式）](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_WorkingWithAutomatedBackups.BackupRetention.html)

### スキーマとデータの移行 {#t4-3-migration}

**ガイドの項目:** スキル5 別の場所や別のエンジンへのスキーマとデータの移行

| 移行 | 必要なもの |
|---|---|
| Oracle から Aurora PostgreSQL | SCT か DMS Schema Conversion でスキーマ、DMS でデータ |
| SQL Server から Aurora MySQL | 同上 |
| MySQL から Aurora MySQL | DMS（変換は不要） |
| 別のリージョンへ | スナップショットのコピー、またはクロスリージョンリードレプリカの昇格 |
| 停止を最小に | DMS の `full-load-and-cdc` |
| 停止を取れる | DMS の `full-load` |

SCT はスキーマとコードを変換し、データは移しません。データは DMS が移します。DMS だけではストアドプロシージャなどは変換できません。

詳細: [AWS DMS](../../services/migration.md#dms)、[移行タイプ](../../services/migration.md#dms-migration-types)、[CDC の前提](../../services/migration.md#dms-cdc)、[SCT と DMS Schema Conversion](../../services/migration.md#sct)

## タスク 4.4: コストを最適化したネットワークを設計する {#task-4-4}

### ネットワーク費用の把握と見直し {#t4-4-tools}

**ガイドの項目:** 知識1 コスト管理の機能（コスト配分タグ、複数アカウントの請求） / 知識2 コスト管理ツールの適切な用途（Cost Explorer、Budgets、Cost and Usage Report） / スキル5 既存のワークロードのネットワーク最適化の見直し

| 確認すること | 使うもの |
|---|---|
| データ転送の内訳 | Cost Explorer や CUR の `UsageType` |
| どの通信が多いか | VPC フローログ |
| 部門やアカウントごとのネットワーク費用 | コスト配分タグ、一括請求 |
| 使っていない NAT や IP | Trusted Advisor、Cost Explorer |

見直しの定番は次のとおりです。

| 見つかったもの | 改善 |
|---|---|
| S3 への通信が NAT を通っている | ゲートウェイエンドポイント |
| AZ 間の通信が多い | 同じ AZ で処理を完結させる（可用性とのトレードオフ） |
| インターネットへの配信が多い | CloudFront |
| アイドルのパブリック IPv4 | 解放する。使用中でもアイドルでも 0.005 USD/時 |

詳細: [データ転送の費用](../../services/cost-management.md#data-transfer)、[Data Exports と CUR](../../services/cost-management.md#data-exports)、[VPC フローログ](../../services/networking.md#flow-logs)、[Elastic IP](../../services/network-connectivity.md#elastic-ip)

### NAT ゲートウェイの構成 {#t4-4-nat}

**ガイドの項目:** 知識4 NAT ゲートウェイ（NAT インスタンスと NAT ゲートウェイの費用の比較） / スキル1 ネットワークに適切な NAT ゲートウェイ構成の設定（共有の 1 つと AZ ごと）

| 構成 | 費用 | 可用性 |
|---|---|---|
| 共有の NAT ゲートウェイ 1 つ | 時間料金は 1 つ分。他の AZ からは AZ 間の転送料がかかる | その AZ の障害で全体の外向き通信が止まる |
| AZ ごとの NAT ゲートウェイ | 時間料金は AZ の数だけ。AZ 間の転送料は避けられる | AZ に独立 |
| リージョン型の NAT ゲートウェイ | AZ ごとに作らずに済む | 複数の AZ に自動で広がる（最大 60 分） |

本番は AZ ごと、開発環境は共有の 1 つで費用を下げる、という使い分けが基本です。

| | NAT ゲートウェイ | NAT インスタンス |
|---|---|---|
| 費用 | 数、時間、処理したデータ量 | インスタンスの数、時間、タイプとサイズ |
| 帯域 | 最大 100 Gbps | インスタンスタイプによる |
| 管理 | AWS | 利用者（パッチ、フェイルオーバーのスクリプト） |
| SG | 付けられない | 付けられる |
| ポートフォワード、踏み台 | できない | できる |

公式は NAT ゲートウェイを推奨しています。NAT インスタンスが正解になるのは、通信量がとても少なく、処理料金を避けて、運用の手間を受け入れられるときです。

詳細: [NAT ゲートウェイ](../../services/network-connectivity.md#nat-gateway)、[データ転送の費用](../../services/cost-management.md#data-transfer)、[NAT ゲートウェイと NAT インスタンスの比較（公式）](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-nat-comparison.html)

### 接続の種類と帯域 {#t4-4-connectivity}

**ガイドの項目:** 知識5 ネットワーク接続（プライベート回線、専用線、VPN） / スキル2 適切なネットワーク接続の設定（Direct Connect、VPN、インターネットの比較） / スキル7 ネットワーク機器の適切な帯域の選択（1 つの VPN と複数の VPN、Direct Connect の速度）

| 接続 | 費用 | 向く場面 |
|---|---|---|
| インターネット | 受信は無料。送信はデータ量 | 暗号化はアプリの TLS で足りる、少量 |
| Site-to-Site VPN | 接続の時間と送信データ量 | 少量から中量、すぐ必要 |
| Direct Connect | ポートの時間と送信データ量 | 定常的に大量のデータ、安定した帯域 |
| Direct Connect のホスト接続 | 小さな帯域から買える | 1 Gbps は要らない |

帯域は必要な量に合わせて選びます。

| 必要な帯域 | 選択 |
|---|---|
| 1.25 Gbps 以内 | VPN 接続 1 本 |
| 1.25 Gbps を超える VPN | Transit Gateway と ECMP で複数の VPN を束ねる。または Large Bandwidth Tunnel（最大 5 Gbps） |
| 500 Mbps の安定した専用線 | Direct Connect のホスト接続 |
| 10 Gbps 以上 | Direct Connect の専用接続（1、10、100、400 Gbps）、LAG で束ねる |

**例**: 標準のトンネルで 8 Gbps が必要なら、`8 / 1.25 = 6.4` なので 7 本以上、つまり VPN 接続 4 本（8 トンネル）を BGP と ECMP で使います。VGW は ECMP に対応しないので、Transit Gateway が必要です。

ホスト接続は速度をパートナーが対応していれば変更できますが、専用接続は新しい接続を作り直します。

詳細: [オンプレミスとの接続の選び方](../../services/network-connectivity.md#choosing-hybrid)、[Direct Connect の接続の種類](../../services/network-connectivity.md#dx-connections)、[LAG](../../services/network-connectivity.md#dx-lag)、[VPN のトンネル](../../services/network-connectivity.md#vpn-tunnels)、[データ転送の費用](../../services/cost-management.md#data-transfer)

### 転送費用を抑える経路 {#t4-4-routes}

**ガイドの項目:** スキル3 転送費用を最小にするネットワーク経路の設定（リージョン間、AZ 間、プライベートからパブリック、Global Accelerator、VPC エンドポイント）

| 経路 | 料金 |
|---|---|
| インターネットから AWS へ | 無料 |
| 同じ AZ 内 | 無料 |
| AZ 間 | 有料（送受信の両方） |
| リージョン間 | 送信元の送信分が有料 |
| AWS からインターネットへ | 有料（月 100 GB まで無料） |

| 経路の改善 | 効果 |
|---|---|
| S3、DynamoDB へゲートウェイエンドポイント | 追加料金なし。NAT の処理料金が消える |
| 他のサービスへインターフェイスエンドポイント | 時間とデータ量がかかるので、NAT と比較する |
| NAT をリソースと同じ AZ に | AZ 間の転送料を避ける |
| 同じリージョンの S3 や DB を使う | リージョン間の転送料を避ける |

Global Accelerator は費用を下げるサービスではありません。アクセラレーターの時間料金と Data Transfer-Premium が、通常の転送料に加わります。性能と固定 IP の要件があるときに選びます。

詳細: [データ転送の費用](../../services/cost-management.md#data-transfer)、[VPC エンドポイントと PrivateLink](../../services/networking.md#vpc-endpoints)、[Global Accelerator](../../services/network-connectivity.md#global-accelerator)、[Global Accelerator の料金（公式）](https://aws.amazon.com/global-accelerator/pricing/)

### ルーティングとトポロジー {#t4-4-topology}

**ガイドの項目:** 知識6 ネットワークのルーティング、トポロジー、ピアリング（Transit Gateway、VPC ピアリング）

| | VPC ピアリング | Transit Gateway |
|---|---|---|
| 料金 | 作成は無料。同じ AZ の転送は無料で、AZ 間とリージョン間は転送料 | アタッチメントの時間料金とデータ処理料金 |
| 関係 | 1 対 1。推移的なルーティングなし | ハブアンドスポーク |
| 向く場面 | 2、3 個の VPC で通信量が多い | 多数の VPC、VPN や Direct Connect の共有 |

**例**: 大量のデータを 2 つの VPC の間で送るだけなら、ピアリングが安くなります。Transit Gateway ではデータ処理料金が加わるからです。VPC が多いなら、管理の手間を含めて Transit Gateway を選びます。

サブネットの共有（RAM）なら、VPC 間の接続を増やさずにアカウントを分けられます。

詳細: [VPC 同士の接続の選び方](../../services/network-connectivity.md#choosing-multi-vpc)、[VPC ピアリング](../../services/network-connectivity.md#vpc-peering)、[Transit Gateway](../../services/network-connectivity.md#transit-gateway)、[VPC サブネットの共有](../../services/governance.md#ram-vpc-sharing)

### 負荷分散の費用 {#t4-4-lb}

**ガイドの項目:** 知識3 負荷分散の概念（ALB）

- 1 つの ALB のルールでサービスをまとめると、ロードバランサーの数を減らせます。パブリック IPv4 の費用も減ります。
- ALB は、クロスゾーン負荷分散の AZ 間の転送料がかかりません。
- NLB のクロスゾーン負荷分散は既定で無効です。有効にすると、別の AZ のターゲットとの通信に転送料がかかります。無効にすると負荷が偏りやすくなるので、トレードオフです。

詳細: [ALB と NLB の違い](../../services/networking.md#alb-vs-nlb)、[クロスゾーン負荷分散](../../services/networking.md#cross-zone)、[Elastic IP](../../services/network-connectivity.md#elastic-ip)

### DNS などのネットワークサービス {#t4-4-dns}

**ガイドの項目:** 知識7 ネットワークサービスの適切な用途（DNS）

| 要件 | 選択 |
|---|---|
| ALB や CloudFront をドメインの頂点で公開 | Route 53 のエイリアス（CNAME は頂点に置けない） |
| 費用を抑えて遅延を減らす | レイテンシーベースのルーティングで最寄りのリージョンへ |
| 問い合わせの回数を減らす | 適切な TTL。短すぎるとクエリが増える |
| VPC 内の名前解決 | プライベートホストゾーン |

詳細: [Route 53 のレコード](../../services/networking.md#route53-records)、[TTL とエイリアスの違い](../../services/networking.md#route53-ttl)、[ルーティングポリシー](../../services/networking.md#routing-policies)、[プライベートホストゾーン](../../services/network-connectivity.md#private-hosted-zones)

### CDN とエッジキャッシュの戦略 {#t4-4-cdn}

**ガイドの項目:** スキル4 CDN とエッジキャッシュの戦略的な必要性の判断

CloudFront を入れる理由は、速度だけではありません。

| 効果 | 内容 |
|---|---|
| オリジンの負荷を下げる | キャッシュのヒット率が上がると、EC2 や S3 へのリクエストが減る |
| 転送料 | CloudFront と AWS のオリジンの間の転送料はかかりません |
| 保護 | WAF、Shield と組み合わせられる |

キャッシュのヒット率を上げるには、キャッシュキーに必要なものだけを入れます。ヘッダーやクッキーを増やすと分散して、ヒット率が下がります。

全員に違う内容を返す API や、一部の国だけの少量の配信なら、CloudFront の効果は小さくなります。

詳細: [CloudFront](../../services/networking.md#cloudfront)、[キャッシュキーとポリシー](../../services/networking.md#cache-keys)、[TTL とキャッシュの期間](../../services/networking.md#cloudfront-ttl)、[圧縮](../../services/networking.md#cloudfront-compression)、[CloudFront の料金（公式）](https://aws.amazon.com/cloudfront/pricing/)

### スロットリングの戦略 {#t4-4-throttling}

**ガイドの項目:** スキル6 適切なスロットリング戦略の選択

スロットリングは、想定外の利用で費用とバックエンドの負荷が増えるのを防ぎます。

| 場所 | 方法 |
|---|---|
| API Gateway | 使用量プランと API キーでクライアントごとに制限。超えると 429 |
| API Gateway のアカウント | リージョンごとに既定 10,000 リクエスト/秒、バースト 5,000（一部のリージョンは小さい） |
| CloudFront、ALB の前 | WAF のレートベースルール |
| Lambda | 予約済み同時実行で上限を決める |
| バックエンド | SQS でバッファし、処理の速度を制限する |
| クライアント | 指数バックオフとジッター |

**例**: 外部の取引先が API を呼びすぎて Lambda の費用が増えているなら、取引先ごとの使用量プランで制限します。

詳細: [スロットリングの階層](../../services/api-gateway.md#throttling)、[使用量プランと API キー](../../services/api-gateway.md#usage-plans)、[レートベースルール](../../services/certificates.md#rate-based-rules)、[予約済み同時実行](../../services/lambda.md#reserved-concurrency)、[指数バックオフとジッター](../../services/sdk-resilience.md#backoff-jitter)

## 確認問題 {#self-check}

??? question "問1: S3 に保存したログは最初の 30 日は頻繁に読み、その後の 1 年はほとんど読みませんが、読むときはすぐ必要です。1 年を過ぎたら 7 年保管し、取得に 2 日かかってもかまいません。最も安い設計は？"
    ライフサイクルルールで、30 日後に Glacier Instant Retrieval、1 年後に Glacier Deep Archive へ移し、8 年で失効させます。すぐ読みたい期間にはミリ秒で読めるクラスが必要です。Deep Archive は Bulk で 48 時間以内なので、2 日の要件を満たします。アクセスの傾向が分かっているので、Intelligent-Tiering の監視料金は不要です。

??? question "問2: 24 時間動く本番の API と、毎晩 2 時間で中断してもやり直せるバッチ、平日の日中だけの開発環境があります。それぞれの購入オプションは？"
    本番の定常部分は Savings Plans、バッチはスポット、開発環境はオンデマンドで業務時間外に停止します。開発環境に 3 年の確約を付けると、止めている時間の分も払うことになります。

??? question "問3: 起動に 15 分かかるアプリを、夜間は止めて費用を下げたいです。翌朝はすぐに使いたいです。既存のインスタンスには設定がなく、ルートボリュームは暗号化されていません。どう進めますか？"
    休止が適しています。ただし休止は起動時にしか有効にできず、ルートボリュームの暗号化が必須です。暗号化した AMI から、休止を有効にして起動し直します。停止中はインスタンス料金がかからず、EBS の料金はかかります。

??? question "問4: 使用量が読めず、夜間はほとんどアクセスのない SQL アプリの DB を選びます。費用を最小にしつつ、MySQL 互換は維持したいです。何を選びますか？"
    Aurora Serverless v2 です。対応するバージョンで最小 0 ACU と自動一時停止を使えば、アイドルの費用を抑えられます。RDS に RI を付ける方法は、一定の負荷に向くので、この要件には合いません。

??? question "問5: 開発環境の VPC には 3 つの AZ があり、AZ ごとに NAT ゲートウェイがあります。外向きの通信はごくわずかで、費用を下げたいです。開発環境は AZ の障害で止まってもかまいません。どうしますか？"
    NAT ゲートウェイを 1 つに減らし、全 AZ のルートをそこへ向けます。時間料金は 1 つ分になり、通信がわずかなので AZ 間の転送料も小さくて済みます。本番なら AZ の障害の影響を受けるので、AZ ごとの構成を残します。S3 や DynamoDB への通信があれば、ゲートウェイエンドポイントも追加します。

??? question "問6: 本社と AWS の間で毎日 2 TB を送り、回線の品質が安定しないことも問題です。10 Gbps は要りません。最も費用対効果の高い接続は？"
    パートナー経由の Direct Connect のホスト接続で、必要な帯域（たとえば 500 Mbps）を選びます。定常の大量通信で安定性が必要なら VPN より適します。専用接続の 10 Gbps は過剰で、VPN はインターネット経由なので品質の問題を解決しません。暗号化が必要なら、Direct Connect の上に VPN を重ねます。

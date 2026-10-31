# 分野3: コストを最適化したアーキテクチャの設計

SAP-C03 の配点は **15%** です。購入オプション、データ転送、コストの配分、ストレージとデータベースの費用を扱います。

設問は「費用を最小に」だけでなく、「性能を落とさず」「3 年の確約はできない」「中断は許されない」のような条件が付きます。条件を満たさない安い選択肢を外してから比べます。

この分野に限らず、コース全体で使うサービスは[サービス一覧](services.md)から確認できます。

## タスク 3.1: 料金モデルに基づいてアーキテクチャを設計する {#task-3-1}

### 3.1.1 使用パターンに応じた購入オプション {#skill-3-1-1}

| 使用パターン | 選択 | 割引の上限 |
|---|---|---|
| 中断してよい、柔軟に動かせる | スポット | |
| 短期間、変動が読めない | オンデマンド | なし |
| 1 年以上、インスタンスファミリーやリージョンが変わるかも | Compute Savings Plans | 66% |
| 1 年以上、ファミリーとリージョンが固定 | EC2 Instance Savings Plans | 72% |
| 特定の AZ で容量も確保 | ゾーナル RI、または Capacity Reservation と Savings Plans | |
| SageMaker AI を継続利用 | SageMaker AI Savings Plans | 64% |
| データベースを継続利用 | Database Savings Plans | 35% |
| Bedrock の固定の大きな処理量 | Provisioned Throughput、Reserved ティア | |

**割引と容量は別の話です。** Savings Plans は割引だけで、容量は確保しません。「DR のリージョンで必ず起動できる」が要件なら、Capacity Reservation が必要です。

**組み合わせ:** 常に動く土台を Savings Plans、ピークをオンデマンド、中断してよい部分をスポットにします。確約は、最低の利用量に合わせます。

公式は RI より Savings Plans を推奨しています。適用の順序は RI、Savings Plans の順です。

詳細: [購入オプション](../../services/cost-management.md#purchase-options)、[Savings Plans](../../services/cost-management.md#savings-plans)、[Reserved Instances](../../services/cost-management.md#reserved-instances)、[スポットインスタンス](../../services/cost-management.md#spot)、[向いているものの選び方](../../services/cost-management.md#purchase-choice)

### 3.1.2 要件に合うコスト最適化のアーキテクチャ {#skill-3-1-2}

| 選択 | 下がる費用 | 向く場面 | 注意 |
|---|---|---|---|
| Graviton | 価格性能 | ARM で動くワークロード | ソフトウェアの対応を確認。Lambda は `arm64` |
| Step Functions Standard | 状態遷移の課金 | 長時間、低頻度 | 大量の短い処理では割高 |
| Step Functions Express | 実行回数、時間、メモリの課金 | 大量で短い処理 | 最大 5 分 |
| Lambda | 使った分だけ | 断続的な処理 | 常に高負荷なら Fargate や EC2 が安いこともある |

**具体例:** 毎秒数千回の短いイベント処理に Standard を使うと、状態遷移の課金が大きくなります。Express に変えると安くなります。ただし Express には `.sync` や `waitForTaskToken` がありません。

**Lambda と常時稼働の比較:** 使用率が低いなら Lambda が有利で、一定の負荷が続くならコンテナが有利です。Lambda の課金はメモリと時間なので、メモリを増やして時間が短くなると、費用が下がることもあります。

詳細: [Standard と Express](../../services/step-functions.md#standard-express)、[アーキテクチャ](../../services/lambda.md#architecture)、[メモリと CPU の最適化](../../services/lambda.md#memory-tuning)、[Fargate と EC2](../../services/containers.md#fargate-vs-ec2)

### 3.1.3 性能メトリクスに基づく適正化とスケーリング {#skill-3-1-3}

| 手段 | 効果 | 使う場面 |
|---|---|---|
| Compute Optimizer | 実績のメトリクスから、EC2、EBS、Lambda、ECS on Fargate の推奨を出す | 過剰な確保を見つける |
| スケジュールスケーリング | 既知の時間帯だけ増やす | 営業時間、夜間の停止 |
| ターゲット追跡 | メトリクスを目標に保つ | 最初の選択肢 |
| Fargate Spot | Fargate を割安に。2 分前の警告で中断 | 中断してよいタスク |

**順序が大事です。** 適正化してから、Savings Plans を買います。過剰な構成に確約すると、後で小さくしても費用が残ります。

**Fargate Spot の組み合わせ:** キャパシティプロバイダーの `base` と `weight` で、`FARGATE` に最低数を残し、残りを `FARGATE_SPOT` へ割り振ります。

**推奨サービスの違い:** Compute Optimizer は適正サイズ、Cost Optimization Hub は推奨の集約と優先付けです。

詳細: [Compute Optimizer と適正サイズ](../../services/cost-management.md#compute-optimizer)、[推奨を出すサービスの違い](../../services/cost-management.md#recommendation-tools)、[キャパシティプロバイダー](../../services/containers.md#capacity-providers)、[EC2 Auto Scaling](../../services/ec2-beanstalk.md#auto-scaling)

### 3.1.4 AI と ML のワークロードのコスト最適化 {#skill-3-1-4}

**Bedrock のサービスティア:**

| ティア | 料金（多くのプロバイダー） | 向く処理 |
|---|---|---|
| Standard | 基準 | 日常の処理 |
| Priority | Standard より割高 | 応答速度が重要 |
| Flex | Standard より割安 | 時間に余裕がある（評価、要約） |
| Reserved | 容量の確保（入力 100,000 TPM、出力 10,000 TPM 以上） | ダウンタイムを許せない |
| バッチ | 非同期で割安 | 大量で急がない |

**キャッシュ:**

| 種類 | 効く場面 |
|---|---|
| プロンプトキャッシュ | 長い固定の指示や文書を繰り返す |
| 完全一致 | 同じ質問（DynamoDB、ElastiCache） |
| セマンティックキャッシュ | 言い換えの質問（MemoryDB、OpenSearch） |

**モデルの選択:** 簡単な処理を安いモデルに回すだけで、費用が大きく下がることがあります。出力の単価は一般に入力より高いので、最大トークンも制限します。

**SageMaker AI:** 断続的ならサーバーレス推論か、0 台まで縮小できる非同期推論です。継続利用は SageMaker AI Savings Plans です。常時動くエンドポイントの使用率が低いのが、最もよくある無駄です。

詳細: [Amazon Bedrock の料金](../../services/cost-management.md#bedrock-pricing)、[スループットの選択肢](../../services/ai.md#throughput-options)、[コストと遅延の最適化](../../services/genai-apps.md#optimization)、[キャッシュの種類](../../services/genai-apps.md#caching)、[SageMaker の最適化](../../services/sagemaker.md#optimization)

## タスク 3.2: データ転送とネットワークの費用を最適化する {#task-3-2}

### 3.2.1 コンテンツ配信とキャッシュ戦略 {#skill-3-2-1}

| 手段 | 効果 |
|---|---|
| キャッシュヒット率を上げる | キャッシュキーを必要最小限にする |
| OAC で S3 オリジンを保護 | 直接のアクセスを止める |
| オリジンフェイルオーバー | オリジングループで GET の障害時に切り替える |
| Origin Shield | オリジンの前のキャッシュ層で負荷を下げる |

**Origin Shield** は、リージョナルエッジキャッシュとオリジンの間にあるキャッシュ層です。

| 項目 | 内容 |
|---|---|
| 効果 | ヒット率の向上。同じオブジェクトへの要求を束ね、オリジンへの要求を減らす |
| 向く場面 | 利用者が世界に分散、動画のパッケージングや画像の変換、帯域が限られるオンプレミスのオリジン、複数の CDN の併用 |
| 向かない場面 | 動的なコンテンツ、キャッシュしにくいもの、まれにしか要求されないもの |
| リージョン | オリジンとの遅延が最も小さいリージョンを選ぶ |
| 料金 | 追加料金がかかる。オリジンの処理と転送の費用の削減と比べる |

キャッシュキーにヘッダーや Cookie を増やすと、ヒット率が下がります。Cookie を全部オリジンへ渡すなら、オリジンリクエストポリシーでキーと分けます。

詳細: [キャッシュキーとポリシー](../../services/networking.md#cache-keys)、[オリジンの設定](../../services/networking.md#origin-settings)、[オリジンフェイルオーバー](../../services/networking.md#origin-failover)、[OAC](../../services/networking.md#oac)、[Origin Shield（公式）](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/origin-shield.html)

### 3.2.2 プライベート接続と AZ、リージョンの転送費用 {#skill-3-2-2}

| 経路 | 料金 |
|---|---|
| インターネットから AWS へ | 無料 |
| 同じ AZ 内 | 無料 |
| AZ 間 | 有料。リソースごとに送受信の両方に課金 |
| リージョン間 | 送信元リージョンの送信分が有料 |
| AWS からインターネットへ | 有料 |

**費用の大きな原因と対策:**

| 症状 | 対策 |
|---|---|
| S3、DynamoDB への通信で NAT の費用が高い | ゲートウェイエンドポイント（無料） |
| その他のサービスへ NAT 経由で大量に通信 | インターフェイスエンドポイントと比較 |
| NAT を 1 つの AZ に置き、他の AZ から通す | AZ ごとに NAT を置き、AZ 間の転送をなくす |
| マイクロサービスが AZ をまたいで大量に通信 | AZ を意識したルーティング（ECS Service Connect の zone-aware routing など） |
| インターネットへの送信が多い | CloudFront を挟む。大量のオンプレミスとの通信は Direct Connect |

**トレードオフ:** 1 つの AZ に集めると転送費用は下がりますが、可用性が落ちます。設問の可用性の要件を確認します。

詳細: [データ転送の費用](../../services/cost-management.md#data-transfer)、[NAT ゲートウェイ](../../services/network-connectivity.md#nat-gateway)、[VPC エンドポイントと PrivateLink](../../services/networking.md#vpc-endpoints)、[クロスゾーン負荷分散](../../services/networking.md#cross-zone)

### 3.2.3 コストを考えたマルチリージョンのレプリケーション {#skill-3-2-3}

費用は、保管の倍増、リージョン間の転送、書き込みの複製の 3 つで増えます。

| サービス | 費用を抑える手段 |
|---|---|
| S3 CRR | フィルターで必要なプレフィックスやタグだけ複製。複製先を安いストレージクラスに |
| DynamoDB グローバルテーブル | 本当に複数リージョンで書くかを確認。書き込みは複製先でも課金される |
| Aurora グローバルデータベース | 待機リージョンの構成を小さくする |
| AWS Backup のコピー | 複製ではなくコピーで済むなら、RPO を緩めて安くする |

**RPO を基準に選びます。** 「RPO は 24 時間で十分」なのに CRR やグローバルテーブルを選ぶのは過剰です。定期のバックアップのコピーで足ります。

詳細: [S3 のレプリケーション](../../services/s3.md#replication)、[グローバルテーブル](../../services/dynamodb.md#global-tables)、[Aurora グローバルデータベース](../../services/databases.md#aurora-global-database)、[リージョン間コピー](../../services/resilience.md#backup-cross-region)

### 3.2.4 費用対効果の高いネットワーク {#skill-3-2-4}

| 選択 | 課金 | 向く場面 |
|---|---|---|
| VPC ピアリング | データ転送のみ。時間課金なし | 通信量の多い少数の VPC |
| Transit Gateway | アタッチメントの時間とデータ処理 | 多数の VPC で管理を簡単に |
| PrivateLink | エンドポイントの時間とデータ処理 | 少数のサービスの公開 |
| Cloud WAN | コアネットワークとアタッチメント | 多数のリージョン |
| VPC 共有 | 接続の費用なし | 同じ VPC を複数のアカウントで |
| Direct Connect | ポート料金と送信データ | 大量の定常的な通信 |

**具体例:** 2 つの VPC の間で大量のデータが流れるなら、Transit Gateway を残したまま、その 2 つだけピアリングを足すと、データ処理料金を避けられます。

**集中型の出口:** NAT を中央の VPC に集めると NAT の時間課金は減りますが、Transit Gateway のデータ処理料金が増えます。通信量で比べます。

詳細: [VPC 同士の接続](../../services/network-connectivity.md#choosing-multi-vpc)、[Transit Gateway](../../services/network-connectivity.md#transit-gateway)、[VPC ピアリング](../../services/network-connectivity.md#vpc-peering)、[Direct Connect](../../services/network-connectivity.md#direct-connect)

### 3.2.5 AI と ML のデータ転送費用 {#skill-3-2-5}

Bedrock のクロスリージョン推論には、ルーティングの追加料金がありません。料金は、呼び出し元のリージョンを基準に計算します。

| | 地理的プロファイル | グローバルプロファイル |
|---|---|---|
| 処理の範囲 | US、EU、APAC などの範囲内 | 世界の商用リージョン |
| 料金 | 標準 | 約 10% 安い（モデルによる） |
| 向く場面 | データレジデンシーの要件がある | 制約がなく費用を優先 |

通信は AWS のネットワーク内を通り、リージョン間は暗号化されます。

**費用以外の要素:**

- 処理のリージョンはリクエストごとに変わります。規制があれば [2.4.4](domain2.md#skill-2-4-4) を確認します。
- 入力データと同じリージョンにモデルを置けるなら、S3 などからのリージョン間の転送を避けられます。
- Provisioned Throughput は推論プロファイルに対応しません。

詳細: [推論の容量とプロファイル](../../services/genai-apps.md#inference-profiles)、[モデル ID と推論プロファイル](../../services/ai.md#model-identifiers)、[クロスリージョン推論（公式）](https://docs.aws.amazon.com/bedrock/latest/userguide/cross-region-inference.html)

## タスク 3.3: コストの配分と可視化を設計する {#task-3-3}

### 3.3.1 コスト配分のタグ戦略 {#skill-3-3-1}

| 決めること | 例 |
|---|---|
| 必須のタグ | `CostCenter`、`Project`、`Environment`、`Owner` |
| 値の形式 | 大文字小文字を統一。`prod` と `Prod` を混ぜない |
| 付ける方法 | IaC で一括して付ける |

コスト配分タグは、タグを付けるだけでは使えません。管理アカウントで **有効化** が必要です。有効化の前の費用には反映されません。

タグが付かない費用もあります。共有の費用はコストカテゴリで配分します。

詳細: [コスト配分タグ](../../services/cost-management.md#cost-allocation-tags)、[タグ戦略](../../services/governance.md#tagging-strategy)、[Resource Groups とタグ付け](../../services/governance.md#resource-groups)

### 3.3.2 詳細な請求データの報告と分析 {#skill-3-3-2}

| 要件 | 選択 |
|---|---|
| 画面で傾向と予測を確認 | Cost Explorer |
| 明細を SQL で分析 | Data Exports（CUR 2.0）を S3 へ出力し、Athena で問い合わせ |
| 経営層向けのダッシュボード | Quick Sight と組み合わせる |

現在の推奨は Data Exports の CUR 2.0 です。固定のスキーマで、列と行を SQL で選べます。従来の CUR は列が月ごとに変わります。試験ガイドは AWS Cost and Usage Reports の名前で書いています。

!!! note "Quick Sight の名称"
    試験ガイドの Amazon QuickSight は、現在は Amazon Quick Sight です。

詳細: [Cost Explorer](../../services/cost-management.md#cost-explorer)、[Data Exports と CUR](../../services/cost-management.md#data-exports)、[Quick Sight](../../services/data-engineering.md#quick-sight)、[S3 上のログを問い合わせる](../../services/streaming.md#athena-logs)

### 3.3.3 ポリシーによるタグの強制 {#skill-3-3-3}

| 手段 | 動作 | 段階 |
|---|---|---|
| SCP | タグのない作成を拒否（`aws:RequestTag` と `Null`） | 予防 |
| タグポリシー | 値と大文字小文字を標準化 | 標準化。強制は対象のサービスとリソースのみ |
| Config ルール（`required-tags`） | タグのないリソースを検出 | 検出 |
| Config の修復 | タグを自動で付ける | 修復 |

**タグポリシーの落とし穴:** タグポリシーだけでは、タグのないリソースの作成を止められません。付いたタグの値を標準化するものです。「タグがないと作成できない」には SCP を使います。

SCP で強く拒否すると、タグに対応しないサービスの作成まで止めることがあります。対象のアクションを絞ります。

詳細: [タグポリシー](../../services/governance.md#tag-policies)、[SCP](../../services/governance.md#scp)、[Config ルール](../../services/governance.md#config-rules)

### 3.3.4 チャージバックとショーバック {#skill-3-3-4}

**ショーバック**は費用を見せるだけ、**チャージバック**は部門へ実際に請求します。

| 手段 | 役割 |
|---|---|
| コストカテゴリ | アカウント、タグなどのルールで費用をまとめる。共有費用の配分ルールも作れる |
| 分割コスト配分データ | ECS タスク、Kubernetes Pod の単位に費用を分ける |
| Bedrock のトークン監視 | アプリケーション推論プロファイルのタグでコストを追跡 |

**分割コスト配分データ（split cost allocation data）** は、コンテナの費用をチームに配分する機能です。

- CUR にタスクや Pod の単位のレコードが追加されます。インスタンスの償却後の費用と、CPU とメモリの使用率から計算します。
- EKS のアクセラレーテッドインスタンスでは GPU なども対象です。
- EKS では `aws:eks:namespace` などのコスト配分タグが作られます。

**具体例:** 1 つの EKS クラスターを 5 チームで共有しているときは、ノードのタグでは分けられません。分割コスト配分データで、名前空間ごとに配分します。

**Bedrock:** チームごとにアプリケーション推論プロファイルを作り、タグを付けます。`InputTokenCount` と `OutputTokenCount` の CloudWatch メトリクスで使用量も監視します。

詳細: [コストカテゴリ](../../services/cost-management.md#cost-categories)、[CloudWatch のメトリクス](../../services/ai.md#bedrock-metrics)、[モデル ID と推論プロファイル](../../services/ai.md#model-identifiers)、[分割コスト配分データ（公式）](https://docs.aws.amazon.com/cur/latest/userguide/split-cost-allocation-data.html)

### 3.3.5 コストの監視とアラート {#skill-3-3-5}

| 要件 | 選択 |
|---|---|
| 予算を超えそうなら通知 | AWS Budgets（実績と予測） |
| 超えたら自動で止める | 予算アクション（IAM ポリシーや SCP の適用、EC2 や RDS の停止） |
| いつもと違う費用の急増を検出 | Cost Anomaly Detection |
| 請求額のアラーム | CloudWatch の請求アラーム（`us-east-1`） |

**Budgets と Anomaly Detection:** Budgets は決めたしきい値で通知し、Anomaly Detection は機械学習で異常な動きを見つけます。しきい値を決めにくいサービスの急増は Anomaly Detection が向きます。

詳細: [AWS Budgets](../../services/cost-management.md#budgets)、[予算アクション](../../services/cost-management.md#budget-actions)、[Cost Anomaly Detection](../../services/cost-management.md#cost-anomaly-detection)、[請求アラーム](../../services/cost-management.md#billing-alarms)

## タスク 3.4: ストレージとデータベースの費用を最適化する {#task-3-4}

### 3.4.1 ストレージの階層化とライフサイクル {#skill-3-4-1}

| クラス | 向くデータ | 最低保存期間 | 取り出し |
|---|---|---|---|
| Intelligent-Tiering | アクセスパターンが不明 | なし | 監視料あり。取り出し料なし |
| Standard-IA | 月 1 回程度 | 30 日 | 取り出し料あり |
| One Zone-IA | 再作成できるデータ | 30 日 | 取り出し料あり |
| Glacier Instant Retrieval | 四半期に 1 回、ミリ秒で取得 | 90 日 | 取り出し料あり |
| Glacier Flexible Retrieval | 年 1 回、分から時間で取得 | 90 日 | 取り出し料あり |
| Glacier Deep Archive | 年 1 回未満、時間単位で取得 | 180 日 | 取り出し料あり |

**ライフサイクルと Intelligent-Tiering:** パターンが分かっていればライフサイクルで移します。不明なら Intelligent-Tiering です。

**落とし穴:**

- 小さなオブジェクトが多いと、IA では最低課金サイズ（128 KB）で割高になります。
- 最低保存期間の前に消すと、残りの期間分が課金されます。
- 古いバージョンと未完了のマルチパートも、ライフサイクルで消します。

**EFS のライフサイクル:** アクセスのないファイルを低頻度アクセスやアーカイブへ移します。Intelligent-Tiering の設定で、アクセスがあれば標準へ戻せます。

詳細: [S3 のストレージ費用](../../services/cost-management.md#s3-cost)、[ライフサイクル](../../services/s3.md#lifecycle)、[ストレージクラス](../../services/s3.md#storage-classes)、[EFS のライフサイクル](../../services/storage.md#efs-lifecycle)

### 3.4.2 ブロックストレージの費用 {#skill-3-4-2}

| タイプ | 特徴 | 最大 IOPS | 向く場面 |
|---|---|---|---|
| `gp3` | IOPS とスループットをサイズと独立に設定 | 80,000 | 多くの場合の第一候補 |
| `gp2` | IOPS はサイズに比例 | 16,000 | 古い構成 |
| `io2` Block Express | 低遅延、高耐久 | 256,000 | 重要なデータベース |
| `st1` | スループット最適化 HDD | 500 | ログ、ビッグデータ |
| `sc1` | 最低コストの HDD | 250 | アクセスの少ないデータ |

**定番の最適化:**

- `gp2` から `gp3` への変更は、多くの場合で費用が下がり、オンラインで実施できます。
- IOPS のためだけに `gp2` を大きくしている場合は、`gp3` にすれば容量を減らせる可能性があります。容量の縮小は直接できないので、別のボリュームへ移します。
- `io2` の IOPS が実際には使われていなければ、`gp3` へ移します。Compute Optimizer で確認します。
- 使っていないボリュームや古いスナップショットを削除します。

詳細: [EBS のボリュームタイプ](../../services/storage.md#ebs-volume-types)、[IOPS とスループットの設定](../../services/storage.md#ebs-performance-settings)、[ボリュームの変更と AZ の制約](../../services/storage.md#ebs-modify)、[スナップショット](../../services/storage.md#ebs-snapshots)

### 3.4.3 データベースのキャパシティモードと予約 {#skill-3-4-3}

| 選択 | 向く場面 |
|---|---|
| DynamoDB オンデマンド | 予測しにくい、急な負荷 |
| DynamoDB プロビジョンドと Auto Scaling | 予測できる安定した負荷 |
| DynamoDB リザーブドキャパシティ | プロビジョンドの長期利用 |
| DynamoDB Standard-IA テーブルクラス | アクセスが少なく保管が多いデータ |
| RDS リザーブド DB インスタンス | 長期の固定の構成 |
| Aurora Serverless v2 | 変動する負荷。自動で ACU を調整 |
| Aurora I/O-Optimized | I/O の費用が大きいとき |
| Database Savings Plans | 複数のデータベース、エンジンの変更を見込む |

**Aurora Standard と I/O-Optimized:** Standard は I/O ごとに課金され、I/O-Optimized は I/O 料金なしで、インスタンスとストレージの単価が上がります。I/O の費用が全体の Aurora の費用の 25% 以上なら、I/O-Optimized が目安です。

**Database Savings Plans:**

| 項目 | 内容 |
|---|---|
| 割引の上限 | 35% |
| 対象 | Aurora、RDS、DynamoDB、ElastiCache、DocumentDB、Timestream、Neptune、Keyspaces、DMS、OpenSearch Service |
| 柔軟性 | エンジン、ファミリー、サイズ、AZ、リージョンを問わない。サーバーレスにも適用 |
| 適用先 | 新しい世代のプロビジョンドインスタンス |

RDS から Aurora へ、または RDS から DynamoDB へ移すなら、Database Savings Plans の割引を保てます。構成が固定なら、RI の割引と比べます。

詳細: [キャパシティモードと RCU/WCU](../../services/dynamodb.md#capacity)、[テーブルクラス](../../services/dynamodb.md#table-classes)、[Aurora Serverless v2](../../services/databases.md#aurora-serverless-v2)、[Savings Plans](../../services/cost-management.md#savings-plans)、[Aurora の応用](../../services/databases-specialized.md#aurora-advanced)

### 3.4.4 保持期間を最適化したバックアップと DR {#skill-3-4-4}

| 選択 | 対象 | 向く場面 |
|---|---|---|
| AWS Backup | 多くのサービスをまとめて | 組織の統一のポリシー、コールドストレージ |
| Data Lifecycle Manager | EBS スナップショット、EBS を使う AMI | EBS だけを単純に自動化 |

**費用を減らす手段:**

- AWS Backup のコールドストレージへ移します。最低保存期間は 90 日です。
- 階層で保持を分けます。例: 日次は 35 日、月次は 1 年、年次は 7 年です。
- リージョン間のコピーは、必要な復旧ポイントだけにします。
- DR の戦略を RTO、RPO に合わせ、過剰なウォームスタンバイを避けます。

要件より長い保持は、そのまま費用になります。

詳細: [AWS Backup](../../services/resilience.md#backup)、[バックアッププランとルール](../../services/resilience.md#backup-plans)、[スナップショット](../../services/storage.md#ebs-snapshots)、[データの保持](../../services/storage.md#retention)、[4 つの DR 戦略](../../services/resilience.md#dr-strategies)

### 3.4.5 コストを抑えたオブザーバビリティ {#skill-3-4-5}

| 費用の原因 | 対策 |
|---|---|
| ログの取り込みが多い | ログレベルを見直す。不要なログを送らない |
| 保管が増え続ける | 保持期間を設定（既定は無期限）。古いものは S3 へ |
| 使われないカスタムメトリクス | 整理する。ディメンションの組み合わせを減らす |
| 高解像度のメトリクス | 必要なものだけ |
| トレースが多い | X-Ray のサンプリング |

**ログクラス:** Essentials（旧 Infrequent Access）は取り込みが安い代わりに、メトリクスフィルターとサブスクリプションフィルターが使えません。作成時に選び、後から変更できません。

**メトリクスに集約:** ログを全文で残す代わりに、EMF やメトリクスフィルターで数値にすると、長期の傾向が安く分かります。

**具体例:** 調査用のログは 30 日で期限切れにし、監査用は S3 の Glacier へ送ります。すべてを CloudWatch Logs に 7 年置くのが最も高くなります。

詳細: [ログクラス](../../services/observability.md#log-classes)、[保持期間の設定](../../services/observability.md#log-retention)、[S3 へのエクスポート](../../services/observability.md#logs-export)、[メトリクスフィルター](../../services/observability.md#metric-filters)、[サンプリング](../../services/observability.md#xray-sampling)、[EMF](../../services/observability.md#emf)

## 確認問題 {#self-check}

??? question "問1: EC2 の費用を減らしたいです。今後 1 年で一部を Fargate へ移し、東京から大阪へ移す計画もあります。何を購入しますか？"
    Compute Savings Plans です。インスタンスファミリー、リージョン、EC2 と Fargate の違いを問わず適用されます。EC2 Instance Savings Plans は割引が大きいですが、ファミリーとリージョンを固定するので、この計画に合いません。

??? question "問2: S3 への大量のデータ送信で NAT ゲートウェイの費用が高くなっています。アプリを変更せずに減らすにはどうしますか？"
    S3 のゲートウェイエンドポイントを作り、ルートテーブルに追加します。エンドポイント自体は無料で、NAT の処理料金がなくなります。インターフェイスエンドポイントでも経路は変わりますが、時間とデータの料金がかかります。

??? question "問3: 1 つの EKS クラスターを 6 チームで共有しています。チームごとの費用を、Pod の使用量に基づいて請求したいです。何を使いますか？"
    分割コスト配分データです。CUR に Pod の単位の費用が追加され、`aws:eks:namespace` などのタグで分けられます。ノードのタグでは、ノードを共有するチームを分けられません。

??? question "問4: 全アカウントで、`CostCenter` タグがないと EC2 を作成できないようにしたいです。タグポリシーを適用しましたが、タグのないインスタンスが作られます。なぜですか？"
    タグポリシーは付いたタグの値を標準化するもので、タグのない作成を止めません。`aws:RequestTag/CostCenter` の `Null` 条件で `ec2:RunInstances` を拒否する SCP を使います。

??? question "問5: Aurora の請求のうち、I/O の費用が大半を占めています。性能とコードを変えずに費用を減らしたいです。どうしますか？"
    Aurora I/O-Optimized に変更します。I/O の料金がなくなり、インスタンスとストレージの単価が上がります。I/O の費用が全体の 25% 以上のときが目安です。Serverless v2 や RI は、I/O 料金の問題を解決しません。

??? question "問6: 社内文書の要約を毎晩まとめて Bedrock で処理しています。結果は翌朝で構いません。同じ長いシステムプロンプトを毎回使います。費用を下げる設計は？"
    バッチ推論か Flex ティアで処理します。急がない処理が割安になります。あわせてプロンプトキャッシュで固定の部分を再利用します。ただしモデルや機能の組み合わせによって対応が異なるので、使うモデルの対応を確認します。Provisioned Throughput は固定の容量の課金なので、夜間だけの処理には過剰です。

# 分野1: 監視、ログ、分析、修復、性能の最適化

配点は **22%** です。分野2、分野3と並んで最大です。

CloudWatch を中心に、異常を見つけ、原因を調べ、自動で直すまでの流れが問われます。旧版の分野6（コストと性能）の性能の部分は、タスク 1.3 に移りました。

この分野に限らず、コース全体で使うサービスは[サービス一覧](services.md)から確認できます。

## タスク 1.1: 監視とログのメトリクス、アラーム、フィルターを実装する {#task-1-1}

### 1.1.1 ワークロードの監視とログの設定 {#skill-1-1-1}

試験はワークロードの種類ごとに、何を有効にするかを問います。「誰が何をしたか」は CloudTrail、「性能と状態」は CloudWatch です。

| ワークロード | まず使うもの | 設定のポイント |
|---|---|---|
| EC2 | 既定メトリクス、CloudWatch エージェント | メモリとディスクはエージェントが必要 |
| Lambda | 既定メトリクス、Logs、Lambda Insights | `Errors`、`Throttles`、`Duration` を見る |
| ECS、EKS | Container Insights | タスクやノードの単位で見る |
| Kubernetes の既存資産 | Managed Service for Prometheus、Managed Grafana | PromQL をそのまま使う |
| AI（Bedrock） | Bedrock のメトリクス、モデル呼び出しログ | ログは既定で無効。送信先は CloudWatch Logs と S3 |
| API の監査 | CloudTrail の証跡 | データイベントは追加で選ぶ |

ログの運用では次の機能を区別します。

| 機能 | 用途 |
|---|---|
| メトリクスフィルター | ログの文字列を数え、アラームの元にする |
| サブスクリプションフィルター | ログをほぼリアルタイムで Lambda や Firehose へ送る |
| Logs Insights | 調査のために対話的に検索する |
| S3 へのエクスポート | 長期保存。リアルタイムではない |

**例:** アプリのログの `ERROR` が 5 分で 10 件を超えたら通知したいなら、メトリクスフィルターとアラームを組み合わせます。

**例:** ルートユーザーの利用を検知するなら、CloudTrail を CloudWatch Logs に送り、メトリクスフィルターとアラームを作ります。

!!! note "CloudTrail Lake の状況"
    CloudTrail Lake は 2026年5月31日で新規顧客の受付を終了しました。既存の顧客は使い続けられます。

詳細: [CloudWatch メトリクス](../../services/observability.md#cloudwatch-metrics)、[CloudWatch Logs](../../services/observability.md#cloudwatch-logs)、[メトリクスフィルター](../../services/observability.md#metric-filters)、[サブスクリプションフィルター](../../services/observability.md#subscription-filters)、[CloudWatch と CloudTrail の違い](../../services/observability.md#cloudtrail-vs-cloudwatch)、[証跡](../../services/observability.md#cloudtrail-trails)、[Managed Service for Prometheus](../../services/operations.md#managed-prometheus)、[Managed Grafana](../../services/operations.md#managed-grafana)、[Bedrock のメトリクス](../../services/ai.md#bedrock-metrics)、[モデル呼び出しログ](../../services/ai.md#invocation-logging)

### 1.1.2 CloudWatch エージェント {#skill-1-1-2}

`AWS/EC2` にメモリのメトリクスはありません。OS の中の値は、エージェントで送ります。詳細モニタリングを有効にしても間隔が 1 分になるだけで、メモリは増えません。

| 手順 | 内容 |
|---|---|
| 権限 | インスタンスのロールに `CloudWatchAgentServerPolicy` |
| 導入 | Run Command の `AWS-ConfigureAWSPackage`、または Distributor |
| 設定の共有 | 設定の JSON を Parameter Store に置き、全台で読む |
| 開始と反映 | `amazon-cloudwatch-agent-ctl -a fetch-config` |

コンテナでは導入の方法が変わります。

| 環境 | 方法 |
|---|---|
| ECS | コンソールか CLI で Container Insights を有効にする。EC2 のインスタンス単位の値は、エージェントをデーモンサービスとして動かす |
| EKS | Amazon CloudWatch Observability EKS アドオン。エージェントと Fluent Bit が入る |

| 症状 | 確認すること |
|---|---|
| メトリクスが見つからない | 名前空間が `CWAgent` か（`AWS/EC2` ではない） |
| 設定を変えても反映されない | `-a fetch-config` を再実行したか |
| グループ全体のアラームが作れない | `aggregation_dimensions` に `AutoScalingGroupName` があるか |
| ロググループが無期限で残る | `retention_in_days` を指定したか |
| コンテナで起動が遅い | IMDS のホップ制限 |

詳細: [CloudWatch エージェント](../../services/operations.md#cloudwatch-agent)、[EC2 の既定メトリクス](../../services/observability.md#ec2-metrics)、[ダッシュボードとインサイト](../../services/observability.md#dashboards)

### 1.1.3 アラームの設定とトラブルシューティング {#skill-1-1-3}

アラームが呼べるものを正確に覚えます。特に、単体のアラームと複合アラームの違いが問われます。

| アクション | メトリクスアラーム | 複合アラーム |
|---|---|---|
| SNS | 可 | 可 |
| Lambda | 可 | 可 |
| Systems Manager の OpsItem、インシデント | 可 | 可 |
| EC2 の停止、終了、再起動、復旧 | 可 | 不可 |
| Auto Scaling のポリシー | 可（異常検知のアラームは不可） | 不可 |

それ以外のサービスを動かすには、アラームの状態変化を EventBridge で受けます。Automation のランブックを動かす場合もこの方法です。

**複合アラームの使いどころ:** CPU とメモリが両方高いときだけ通知します。子のアラームには通知を付けず、複合アラームにだけ SNS を付けます。子にも付けると、通知は減りません。

| 症状 | 確認すること |
|---|---|
| 短いスパイクで鳴り続ける | M out of N（例: 5 回中 3 回）に変える |
| データが来ないと `INSUFFICIENT_DATA` になる | `TreatMissingData` を `missing` 以外にする |
| 同じ状態の間に再通知されない | 仕様。アクションは状態の変化で動く |
| 通知が届かない | SNS のトピックポリシー、サブスクリプションの確認状態、暗号化したトピックのキーポリシー |
| 複数アカウントの子を組み合わせたい | 複合アラームの子は同じアカウント、同じリージョン |

詳細: [アラーム](../../services/observability.md#alarms)、[M out of N](../../services/observability.md#alarm-evaluation)、[欠落データの扱い](../../services/observability.md#treat-missing-data)、[アラームのアクション](../../services/observability.md#alarm-actions)、[複合アラーム](../../services/observability.md#composite-alarms)、[EventBridge による修復](../../services/operations.md#eventbridge-remediation)

### 1.1.4 複数アカウント、複数リージョンのダッシュボード {#skill-1-1-4}

1 つのダッシュボードに、複数リージョンのメトリクスを載せられます。複数アカウントにするには、クロスアカウントオブザーバビリティを設定します。

| 用語 | 意味 |
|---|---|
| 監視アカウント | データを見る中央のアカウント。シンクを持つ |
| ソースアカウント | データを共有する側。リンクを管理する |
| 共有できるもの | メトリクス、ロググループ、X-Ray のトレース、Application Signals、Application Insights、Internet Monitor |
| 範囲 | リージョンごとに設定する。シンクはアカウントのリージョンあたり 1 つ |

Organizations で組織や OU をリンクすると、後から作ったアカウントも自動でソースアカウントになります。AWS はこの方法を勧めています。

**アカウントを持たない人への共有:**

| 方法 | 内容 |
|---|---|
| メールアドレスの指定 | 1 つのダッシュボードを最大 5 人へ。各自がパスワードを作る |
| 公開リンク | リンクを知る全員が見られる |
| SSO | 全ダッシュボードを SAML の SSO で共有する。Amazon Cognito と連携する |

**落とし穴:** 共有された人は、アカウントの全メトリクスと、全 EC2 の名前とタグを照会できます。この権限は絞れません。

**落とし穴:** アラームの注釈が付いたメトリクスウィジェットは、共有先では表示されません。

**落とし穴:** Logs Insights のウィジェットは、更新のたびにスキャン料金がかかります。

この節のクロスアカウントオブザーバビリティの構成要素と共有の方法は、公式ドキュメントで確認して書いています。

詳細: [ダッシュボードの設定](../../services/observability.md#dashboard-settings)。公式: [クロスアカウントオブザーバビリティ](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch-Unified-Cross-Account.html)、[ダッシュボードの共有](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/cloudwatch-dashboard-sharing.html)

### 1.1.5 SNS への通知 {#skill-1-1-5}

多くのサービスは、SNS のトピックへ通知できます。届かないときは、まずトピックのアクセスポリシーを疑います。

| 送信元 | 設定 |
|---|---|
| CloudWatch アラーム | `AlarmActions` にトピックの ARN |
| S3 | Event Notifications。トピックのポリシーで `s3.amazonaws.com` を許可 |
| AWS Health、Config、Trusted Advisor など | EventBridge ルールのターゲットに SNS |
| Slack、Teams | SNS から Amazon Q Developer in chat applications（旧 AWS Chatbot） |

**例:** S3 のイベント通知を設定しようとして、送信先の検証でエラーになります。トピックのポリシーで S3 に `sns:Publish` を許可していません。

**例:** 暗号化したトピックに AWS サービスから送れません。サービスに KMS キーの利用を許可します。

| 迷う組み合わせ | 見分け方 |
|---|---|
| SNS と User Notifications | AWS の通知を人に届けるだけなら User Notifications、アプリや他のサービスへ配信するなら SNS |
| SNS と EventBridge | 内容で振り分けて処理を動かすなら EventBridge、多数の宛先へ同時に配るなら SNS |

詳細: [SNS](../../services/messaging.md#sns)、[トピックのアクセスポリシーと暗号化](../../services/messaging.md#sns-access)、[配信の再試行](../../services/messaging.md#sns-retries)、[S3 の Event Notifications](../../services/s3.md#event-notifications)、[User Notifications](../../services/operations.md#user-notifications)、[Q Developer in chat applications](../../services/operations.md#q-chat)

## タスク 1.2: メトリクスで問題を特定し、修復する {#task-1-2}

[![イベントから自動修復までの流れ](../../assets/diagrams/operations-remediation.png)](../../assets/diagrams/operations-remediation.png)

### 1.2.1 性能の分析と修復の自動化 {#skill-1-2-1}

検知、判断、修復を組み合わせます。問いの条件で手段を選びます。

| きっかけ | 手段 |
|---|---|
| EC2 のシステムステータスチェックの失敗 | `StatusCheckFailed_System` のアラームで EC2 の復旧アクション |
| AWS API の呼び出し（SG の変更など） | CloudTrail 経由のイベントを EventBridge で受け、Lambda か Automation |
| Config の非準拠 | Config ルールの修復で Automation を実行 |
| AWS Health の予定 | EventBridge で受け、Automation で対処 |
| 人の判断を入れたい | OpsItem を作る、または `aws:approve` を入れる |

**修復のループに注意します。** 修復が別のイベントを起こし、また修復が動く構成にしません。ランブックのロールは最小権限にします。

AI の支援も、スキルの例に挙がっています。

| ツール | 役割 |
|---|---|
| AWS DevOps Agent | アラートなどを受けて調査を始め、テレメトリ、コード、デプロイの情報から根本原因を探し、緩和の手順を示す |
| Kiro | 仕様駆動の AI 開発環境。修復の自動化に使うコードや手順の作成を支援する |

!!! note "運用系サービスの状況"
    Amazon DevOps Guru は 2026年10月29日で新規受付を終了しました。Incident Manager と Change Manager は 2025年11月7日に新規受付を終了しています。DevOps Agent のインシデント調査は一般提供で、リリース管理はプレビューです。

詳細: [EventBridge による修復パターン](../../services/operations.md#eventbridge-remediation)、[ステータスチェック](../../services/operations.md#status-checks)、[Config の修復](../../services/governance.md#config-remediation)、[AWS Health イベント](../../services/operations.md#health-events)、[DevOps Agent](../../services/operations.md#devops-agent)、[Kiro](../../services/ai.md#kiro)、[提供状況](../../services/operations.md#status)

### 1.2.2 EventBridge のルーティング、エンリッチメント、配信 {#skill-1-2-2}

| やりたいこと | 機能 |
|---|---|
| 内容で振り分ける | ルールのイベントパターン |
| ターゲットに必要な項目だけ渡す | 入力トランスフォーマー |
| 1 対 1 の連携の途中で情報を足す | Pipes のエンリッチメント（Lambda など） |
| 配信できないイベントを残す | ターゲットの DLQ（SQS 標準） |
| 古いイベントを捨てる | `MaximumEventAgeInSeconds`（既定 24 時間） |

**ルールが動かないときの切り分け:**

| 症状 | 原因と対処 |
|---|---|
| ルールが一度も一致しない | イベントのバスが違う、パターンのキーや値の誤り。サンドボックスで実際のイベントを試す |
| 一致するがターゲットが動かない | ターゲットの権限。Lambda なら `events.amazonaws.com` を許可するリソースベースポリシー |
| 再試行されずイベントが消える | 権限不足や宛先なしは再試行しない。DLQ がなければ捨てられる |
| DLQ に届かない | キューポリシーで EventBridge に `sqs:SendMessage` を許可する。FIFO は使えない |
| 入力の形式エラー | 入力トランスフォーマーのクォートの誤り。DLQ の `ERROR_CODE` が `INVALID_JSON` |

ターゲットの再試行の既定は、185 回か 24 時間です。DLQ の属性 `ERROR_MESSAGE` で原因を確認できます。

詳細: [EventBridge](../../services/messaging.md#eventbridge)、[イベントバス](../../services/messaging.md#event-buses)、[ルールとイベントパターン](../../services/messaging.md#eventbridge-rules)、[入力トランスフォーマー](../../services/messaging.md#input-transformer)、[ターゲットの再試行と DLQ](../../services/messaging.md#target-retry-dlq)、[Pipes](../../services/messaging.md#eventbridge-pipes)

### 1.2.3 Automation ランブック {#skill-1-2-3}

Run Command はノードの中で動きます。Automation は AWS API も呼べて、複数の手順を実行できます。

| 定義済みのランブック | 用途 |
|---|---|
| `AWS-RestartEC2Instance` | インスタンスの再起動 |
| `AWS-UpdateLinuxAmi` | Linux AMI にパッチを当てて新しい AMI を作る |
| `AWS-DisableS3BucketPublicReadWrite` | S3 バケットの公開を止める |
| `AWSSupport-TroubleshootSSH` | SSH の接続の問題を調べる |

カスタムランブックは次のアクションを組み合わせます。

| アクション | 用途 |
|---|---|
| `aws:executeAwsApi` | 任意の AWS API を呼ぶ |
| `aws:executeScript` | Python などのスクリプトを実行する |
| `aws:runCommand` | ノードで Run Command を実行する |
| `aws:branch` | 条件で分岐する |
| `aws:approve` | 人の承認を待つ。既定 7 日、最大 30 日 |

**起動の方法:** コンソール、CLI や SDK、EventBridge のターゲット、Config の修復、Maintenance Windows から起動できます。

| 落とし穴 | 内容 |
|---|---|
| `AutomationAssumeRole` を指定しない | 実行者の権限で動く。実行時間は最大 12 時間 |
| 複数アカウントで失敗する | カスタムランブックを対象のアカウントに共有していない。各アカウントに `AWS-SystemsManager-AutomationExecutionRole` が必要 |
| 複数アカウントの実行で承認を使う | `aws:approve` は使えない |
| 多数のリソースへの実行 | 同時実行数とエラーしきい値でレートを制御する |

詳細: [Automation](../../services/operations.md#automation)、[複数アカウント、複数リージョンの実行](../../services/operations.md#automation-multi-account)、[レート制御](../../services/operations.md#automation-rate-control)、[選び方の比較](../../services/operations.md#choosing)

## タスク 1.3: コンピューティング、ストレージ、データベースの性能を最適化する {#task-1-3}

### 1.3.1 コンピューティングの最適化 {#skill-1-3-1}

メトリクスで傾向を見て、タグで対象を絞り、ツールの推奨で判断します。

| ツール | 主な役割 |
|---|---|
| Compute Optimizer | EC2、Auto Scaling グループ、EBS、Lambda、Fargate などのサイズの推奨。オプトインが必要 |
| Trusted Advisor | 費用、性能、セキュリティなどの幅広い点検 |
| Cost Explorer の推奨 | Savings Plans と RI の購入 |
| Cost Optimization Hub | 上の推奨をまとめて優先順位を付ける |

**Compute Optimizer のデータ条件:** EC2 は過去 14 日間に 30 時間以上、Lambda は 50 回以上の呼び出し、Fargate の ECS サービスは 24 時間以上です。メモリを含めた推奨には、CloudWatch エージェントのメトリクスが役立ちます。

**症状と対処:**

| 症状 | 対処 |
|---|---|
| CPU が低く費用が高い | 小さいタイプへ変更する |
| T 系のクレジットが尽きて遅くなる（standard モード） | `CPUCreditBalance` を確認し、`unlimited` モードか M 系などへ変更する |
| Lambda の `Duration` が長い | メモリを増やす。CPU も比例して増える |
| Lambda の `Throttles` が増える | 同時実行の上限と予約を確認する |
| タグで対象を選びたい | タグで Run Command や Automation の対象を指定する |

コストの詳細な分析は受験者に求められていません。推奨の出どころを選べれば十分です。

詳細: [Compute Optimizer](../../services/cost-management.md#compute-optimizer)、[推奨を出すサービスの違い](../../services/cost-management.md#recommendation-tools)、[Trusted Advisor](../../services/cloud-foundations.md#trusted-advisor)、[代表的なメトリクスと原因](../../services/observability.md#bottleneck-metrics)、[リソース使用量の最適化](../../services/observability.md#resource-optimization)、[Lambda の同時実行](../../services/lambda.md#concurrency)、[タグ戦略](../../services/governance.md#tagging-strategy)

### 1.3.2 EBS の性能とコスト {#skill-1-3-2}

まず CloudWatch の `AWS/EBS` で症状を読みます。

| メトリクス | 意味 | 読み方 |
|---|---|---|
| `VolumeQueueLength` | 完了を待つ I/O の数 | 高いまま続くなら、性能が足りない |
| `BurstBalance` | クレジットの残り（`gp2`、`st1`、`sc1` のみ） | 0 に近いならベースラインまで落ちている |
| `VolumeIOPSExceededCheck` | 設定の IOPS を超えて要求したか | `1` なら超過。Nitro のみ |
| `VolumeThroughputExceededCheck` | 設定のスループットを超えて要求したか | `1` なら超過。Nitro のみ |
| `VolumeStalledIOCheck` | I/O が止まっていないか | `1` なら失敗。Nitro のみ |
| `InstanceEBSIOPSExceededCheck` | インスタンス側の EBS の IOPS 上限を超えたか | ボリュームを変えても直らない。タイプを変える |
| `VolumeIdleTime` | I/O がなかった秒数 | 使われていないなら削除を検討する |

**ボリュームタイプの選択:**

| 要件 | 選択 |
|---|---|
| 汎用で、サイズと性能を別に決めたい | `gp3`。基準は 3,000 IOPS、125 MiB/s |
| `gp2` のバーストが尽きる | `gp3` へ稼働中に変更する。GiB 単価は最大 20% 低い |
| 高い IOPS と低遅延の DB | `io2` Block Express（最大 256,000 IOPS） |
| 順次読み取りのログ、ビッグデータ | `st1`（ブートは不可） |
| アクセスの少ないデータを最低コストで | `sc1`（ブートは不可） |

**計算の例:** 100 GiB で 6,000 IOPS が必要なとき、`gp2` は 3 IOPS/GiB なので 2,000 GiB 必要です。`gp3` なら 100 GiB のまま指定できます。

| 落とし穴 | 内容 |
|---|---|
| サイズを減らしたい | Elastic Volumes は増やすだけ。小さいボリュームへデータを移す |
| 変更の回数 | 24 時間で 4 回まで。前の変更の完了を待つ |
| 拡張の後 | OS でファイルシステムを拡張する |
| 別の AZ で使いたい | スナップショットから作り直す |
| スナップショットからの最初の読み取りが遅い | Fast Snapshot Restore |

EBS のメトリクス名は公式ドキュメントで確認して書いています。

詳細: [ボリュームタイプ](../../services/storage.md#ebs-volume-types)、[IOPS とスループット](../../services/storage.md#ebs-performance-settings)、[ボリュームの変更](../../services/storage.md#ebs-modify)、[スナップショット](../../services/storage.md#ebs-snapshots)。公式: [EBS の CloudWatch メトリクス](https://docs.aws.amazon.com/ebs/latest/userguide/using_cloudwatch_ebs.html)

### 1.3.3 S3 の性能戦略 {#skill-1-3-3}

| 課題 | 手段 | ポイント |
|---|---|---|
| 大きなファイルのアップロード | マルチパートアップロード | 100 MB 以上で推奨、5 GB 超で必須 |
| 遠隔地からのアップロードが遅い | Transfer Acceleration | エッジ経由。同じリージョン内では速くならない |
| オンプレミスから大量の移行、定期同期 | DataSync | 検証、スケジュール、帯域制限 |
| リクエストが集中して 503 が出る | プレフィックスを分ける | プレフィックスあたりの上限に合わせる |
| アクセスの少ないデータの費用 | ライフサイクルと Intelligent-Tiering | 頻度が読めないなら Intelligent-Tiering |
| 失敗したマルチパートの残骸 | ライフサイクルの `AbortIncompleteMultipartUpload` | 残ると課金される |
| ダウンロードを世界へ速く | CloudFront | キャッシュが中心 |

**DataSync の速度:** タスクあたり、エージェントありで 10 Gbps、エージェントなしで 5 Gbps です。回線に余力があるのに遅いなら、データを分けて複数のタスクで流します。

詳細: [リクエストレート](../../services/s3.md#request-rate)、[マルチパートアップロード](../../services/s3.md#multipart-upload)、[片付けの設定](../../services/s3.md#abort-multipart)、[Transfer Acceleration](../../services/s3.md#transfer-acceleration)、[ライフサイクル](../../services/s3.md#lifecycle)、[ストレージクラス](../../services/s3.md#storage-classes)、[DataSync](../../services/migration.md#datasync)、[DataSync の速度](../../services/migration.md#datasync-performance)

### 1.3.4 共有ストレージの選択と最適化 {#skill-1-3-4}

| 要件 | 選択 |
|---|---|
| Linux の複数台で共有、容量管理をしたくない | EFS |
| Windows の共有フォルダ、NTFS の ACL、AD | FSx for Windows File Server |
| HPC や ML、S3 のデータを高速に並列処理 | FSx for Lustre |
| NFS、SMB、iSCSI を同時に使う、NetApp から移行 | FSx for NetApp ONTAP |
| 正本を S3 に置いたままファイルとして共有 | S3 Files |

FSx for OpenZFS は、このガイドでは対象外のサービスです。

**EFS の最適化:**

| 設定 | 選び方 |
|---|---|
| ライフサイクル | 既定は 30 日で IA、90 日で Archive。「初回アクセス時」を選ぶと Standard へ戻る |
| スループットモード | 予測しにくいなら Elastic（既定、推奨）。量がわかっているなら Provisioned |
| Bursting の監視 | `BurstCreditBalance` が尽きるとベースラインまで落ちる |

**FSx の最適化:** ONTAP は階層化ポリシーで、アクセスの少ないデータを安い階層へ移します。Lustre は S3 とリンクして、必要なデータだけ読み込みます。

**S3 Files の設定:** 高性能ストレージへ読み込むサイズのしきい値（既定 1 MiB）と、読まれないデータを外す期限（既定 30 日）で費用を調整します。

詳細: [比較](../../services/storage.md#comparison)、[EFS のスループットモード](../../services/storage.md#efs-throughput-mode)、[EFS のライフサイクル](../../services/storage.md#efs-lifecycle)、[FSx の選び方](../../services/storage-advanced.md#fsx-selection)、[ストレージの比較](../../services/storage-advanced.md#storage-comparison)、[ONTAP の階層化](../../services/storage-advanced.md#fsx-ontap-tiering)、[S3 Files](../../services/storage-advanced.md#s3-files)

### 1.3.5 RDS の監視と性能の改善 {#skill-1-3-5}

!!! note "Performance Insights と Database Insights"
    試験ガイドは Performance Insights と書いています。現在の RDS のドキュメントは、DB 負荷の分析を CloudWatch Database Insights として説明しています。役割は同じと考えて学習します。

| 手段 | 分かること |
|---|---|
| CloudWatch メトリクス | `CPUUtilization`、`FreeableMemory`、`FreeStorageSpace`、`DatabaseConnections`、`ReplicaLag`、`ReadLatency` |
| Performance Insights、Database Insights | DB 負荷を待機、SQL、ホスト、ユーザーで分解する |
| プロアクティブ推奨 | しきい値を超えたメトリクスから、問題になる前に推奨を出す |
| Enhanced Monitoring | OS レベルのプロセスや CPU の値 |

**読み方:** DB 負荷が Max vCPU の線を頻繁に超え、主な待機が CPU なら、CPU が過負荷です。接続を絞る、負荷の高い SQL を直す、大きいインスタンスにするといった対策を検討します。

**保持期間:** Database Insights の性能データは既定で 7 日です。1〜24 か月を購入できます。

**症状と対処:**

| 症状 | 対処 |
|---|---|
| 接続数の急増で失敗する、Lambda から多数接続する | RDS Proxy |
| 特定の SQL が重い | Performance Insights で特定して SQL やインデックスを直す |
| 読み取りが多い | リードレプリカ。接続先をアプリで変える |
| RDS Proxy の効果が低い | `DatabaseConnectionsCurrentlySessionPinned` でピン留めを確認する |
| 空き容量が減り続ける | ストレージの自動スケーリング（[2.1.3](domain2.md#skill-2-1-3)） |

**RDS Proxy の制約:** DB と同じ VPC に置きます。パブリックアクセスはできません。レプリケーション構成の RDS では、ライターだけに関連付けます。

詳細: [RDS Proxy](../../services/databases.md#rds-proxy)、[RDS Proxy の設定](../../services/databases.md#rds-proxy-settings)、[リードレプリカ](../../services/databases.md#read-replicas)。公式: [Database Insights](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_PerfInsights.html)、[RDS の推奨](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/monitoring-recommendations.html)

### 1.3.6 EC2 とストレージ、ネットワークの最適化 {#skill-1-3-6}

| 戦略 | 配置 | 向くもの |
|---|---|---|
| クラスター | 1 AZ 内で近くに | HPC、ノード間の低レイテンシー |
| パーティション | パーティションごとに別のハードウェア。AZ ごとに 7 個 | HDFS、HBase、Cassandra |
| スプレッド | 1 台ずつ別のラック。AZ ごとに 7 台 | 少数の重要なインスタンス |

**クラスターの容量エラー:** `InsufficientInstanceCapacity` を避けるには、必要な台数を 1 回のリクエストで、同じタイプで起動します。エラーが出たら、全台を止めて再開すると移れる場合があります。

**ネットワークの性能:**

| 機能 | 内容 |
|---|---|
| ENA | 拡張ネットワーキング。Nitro のインスタンスは ENA を使う |
| EFA | HPC や ML のノード間通信向けのアダプター |
| ジャンボフレーム | VPC 内で MTU 9001。経路の外では 1500 に注意 |

**ストレージの組み合わせ:**

| 要件 | 選択 |
|---|---|
| 最小の遅延、データは消えてよい | インスタンスストア |
| 永続が必要 | EBS の `gp3` か `io2` |
| インスタンス側の EBS の帯域が足りない | EBS の帯域が大きいタイプへ変える |

**購入オプションの運用:** スポットの中断は 2 分前に通知されます。休止はメモリの内容を保って止める機能で、起動時の有効化とルートボリュームの暗号化が必要です。

ENA と EFA は公式ドキュメントで確認して書いています。

詳細: [プレイスメントグループ](../../services/operations.md#placement-groups)、[インスタンスのトラブルシューティング](../../services/operations.md#instance-troubleshooting)、[インスタンスストア](../../services/storage-advanced.md#instance-store)、[MTU とジャンボフレーム](../../services/network-connectivity.md#mtu)、[スポットの中断](../../services/operations.md#spot-interruptions)、[休止](../../services/operations.md#hibernate)。公式: [拡張ネットワーキング](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/enhanced-networking.html)、[EFA](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/efa.html)

## 確認問題 {#self-check}

??? question "問1: Auto Scaling グループの EC2 のメモリ使用率でスケールしたいのですが、`AWS/EC2` に該当するメトリクスがありません。詳細モニタリングは有効です。どうしますか？"
    CloudWatch エージェントを導入し、`mem_used_percent` を送ります。`aggregation_dimensions` で `AutoScalingGroupName` の集約を有効にすると、グループ全体の値でアラームやスケーリングを設定できます。詳細モニタリングは間隔を 1 分にするだけで、OS の中の値は増えません。

??? question "問2: CPU が高く、かつ DB の接続数が多いときだけ、インスタンスを再起動したいです。複合アラームのアクションに EC2 の再起動を指定しましたが、設定できません。どう直しますか？"
    複合アラームのアクションに EC2 の操作はありません。使えるのは SNS、Lambda、Systems Manager の OpsItem とインシデント、CloudWatch の調査の開始です。複合アラームの状態変化を EventBridge で受け、ターゲットの Automation で `AWS-RestartEC2Instance` を実行します。

??? question "問3: セキュリティグループが変更されたら、自動で元に戻したいです。EventBridge ルールは一致しているのに Lambda が動かず、DLQ もありません。まず何を確認しますか？"
    Lambda のリソースベースポリシーで `events.amazonaws.com` を許可しているかを確認します。権限不足は再試行されず、DLQ がなければイベントは捨てられます。調査のためにターゲットに SQS 標準キューの DLQ を付け、`ERROR_CODE` を見ます。

??? question "問4: 100 GiB の `gp2` の DB ボリュームで、昼だけ遅くなります。`BurstBalance` が 0 に近づいています。費用を抑えて直すには？"
    `gp3` に Elastic Volumes で変更し、必要な IOPS を指定します。`gp3` はサイズと独立に IOPS を決められ、基準でも 3,000 IOPS あります。`gp2` のままサイズで補うと、必要以上の容量を買うことになります。`io2` はこの要件では高価です。

??? question "問5: Lambda から RDS for MySQL に接続するアプリで、同時実行が増えると `Too many connections` が出ます。プロキシを入れましたが、改善が小さいです。何を確認しますか？"
    `DatabaseConnectionsCurrentlySessionPinned` を確認します。セッションの状態を変える処理でピン留めが起きると、接続を再利用できません。接続ごとに同じ `SET` を実行しているなら、プロキシの初期化クエリに移します。

??? question "問6: 東京のバケットへ、海外の拠点から数十 GB のファイルをアップロードすると遅く、失敗すると最初からやり直しです。設定を変えるだけで改善するには？"
    マルチパートアップロードで失敗したパートだけ再送できるようにし、Transfer Acceleration を有効にしてエッジ経由にします。残ったパートの課金を防ぐため、ライフサイクルで未完了のアップロードを中止します。CloudFront はダウンロードのキャッシュが中心なので、この問いの第一候補ではありません。

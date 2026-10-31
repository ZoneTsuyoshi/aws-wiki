# 分野5: インシデントとイベントへの対応

配点は **14%** で、6分野の中で最も小さい分野です。イベントの受け取り、設定の自動修正、障害の調査を扱います。

分野4の監視と重なります。分野4が「どう検知するか」、この分野は「検知した後にどう動くか」です。

この分野に限らず、コース全体で使うサービスは[サービス一覧](services.md)から確認できます。

## タスク 5.1: イベントソースを管理し、イベントの処理、通知、対応を行う {#task-5-1}

### イベントを生成するサービスと統合 {#t5-1-event-sources}

**ガイドの項目:** 知識「イベントを生成、取得、処理する AWS サービス（AWS Health、EventBridge、CloudTrail など）」、スキル「AWS のイベントソースの統合（AWS Health、EventBridge、CloudTrail など）」

| ソース | 分かること | 受け取り方 |
|---|---|---|
| AWS Health | AWS 側の障害、予定されたメンテナンス | EventBridge の `aws.health` |
| CloudTrail | API の呼び出し | EventBridge の `AWS API Call via CloudTrail` |
| AWS のサービス | 状態の変化 | EventBridge の `aws.ec2` など |
| CloudWatch | アラームの状態の変化 | EventBridge、SNS |

統合で問われる点をまとめます。

| 点 | 内容 |
|---|---|
| AWS Health のルール | 受けたいリージョンごとに作る。米国西部（オレゴン）が他のリージョンのバックアップ |
| 組織全体の AWS Health | 組織ビューと委任管理者 |
| AWS Health API | 特定のサポートプランが必要。EventBridge での受信には不要 |
| CloudTrail 経由のイベント | 有効な証跡が必要で、既定のイベントバスにだけ届く |
| 読み取り専用の管理イベント | 既定の `ENABLED` のルールでは一致しない。`ENABLED_WITH_ALL_CLOUDTRAIL_MANAGEMENT_EVENTS` にする |
| 複数のアカウントのイベント | 既定のバスのルールから、中央のイベントバスへ転送する |

**例:** `AWS_EC2_INSTANCE_RETIREMENT_SCHEDULED` のイベントで Automation を動かし、インスタンスを停止して再開し、別のホストへ移します。

詳細: [AWS Health イベントの自動化](../../services/operations.md#health-events)、[AWS Health Dashboard](../../services/cloud-foundations.md#health)、[イベントバス](../../services/messaging.md#event-buses)、[ルールとイベントパターン](../../services/messaging.md#eventbridge-rules)

### イベント駆動アーキテクチャ {#t5-1-architectures}

**ガイドの項目:** 知識「イベント駆動アーキテクチャ（ファンアウト、イベントストリーミング、キューイングなど）」

| パターン | 動き | サービス | 向く場面 |
|---|---|---|---|
| ファンアウト | 1 件を複数の宛先へ | SNS と SQS、EventBridge | 通知と処理を同時に |
| イベントストリーミング | 順序のある記録を複数が読む | Kinesis Data Streams | 再読み取り、順序の必要な処理 |
| キューイング | 処理側のペースで取り出す | SQS | 負荷の平準化、再試行 |

SNS と SQS のファンアウトでは、宛先ごとにキューがあるので、1 つの宛先が止まっても他に影響しません。

詳細: [ファンアウト](../../services/messaging.md#fanout)、[Kinesis Data Streams](../../services/streaming.md#kinesis-data-streams)、[SQS](../../services/messaging.md#sqs)、[選び方](../../services/messaging.md#how-to-choose)

### イベント処理のワークフロー {#t5-1-workflows}

**ガイドの項目:** スキル「イベント処理のワークフローの構築（SQS、Kinesis、SNS、Lambda、Step Functions など）」

| 要件 | 選択 |
|---|---|
| 短い処理を 1 回動かす | EventBridge と Lambda |
| 大量のイベントをまとめて処理する | SQS と Lambda のバッチ |
| 複数の工程、分岐、人の承認 | Step Functions |
| 順序を保って処理する | Kinesis、SQS FIFO |
| 一部のレコードの失敗だけ再試行する | 部分バッチレスポンス |

失敗の扱いが設計の中心です。

| 場所 | 失敗の受け皿 |
|---|---|
| EventBridge のターゲット | 再試行ポリシーと DLQ |
| SQS | リドライブポリシーと DLQ |
| Lambda の非同期呼び出し | デスティネーション、DLQ |
| Kinesis と Lambda | `BisectBatchOnFunctionError`、失敗の送信先 |
| Step Functions | `Retry`、`Catch` |

SQS と Lambda では、可視性タイムアウトを関数のタイムアウトの 6 倍以上にします。

詳細: [ターゲットの再試行と DLQ](../../services/messaging.md#target-retry-dlq)、[デッドレターキュー](../../services/messaging.md#sqs-dlq)、[デスティネーションと DLQ](../../services/lambda.md#destinations-dlq)、[部分バッチレスポンス](../../services/lambda.md#partial-batch-response)、[ストリームのエラー処理](../../services/lambda.md#esm-stream-errors)、[Lambda から使うときの設定](../../services/messaging.md#sqs-lambda-settings)

## タスク 5.2: イベントに応じて構成を変更する {#task-5-2}

### フリート管理のサービス {#t5-2-fleet}

**ガイドの項目:** 知識「フリート管理のサービス（Systems Manager、AWS Auto Scaling など）」

| サービス | 機能 | 使う場面 |
|---|---|---|
| Systems Manager | Run Command、Automation、State Manager | 動いているサーバーを変更する |
| Fleet Manager | ノードの確認と操作 | コンソールから調べる |
| Auto Scaling | インスタンスの更新、ライフサイクルフック | サーバーを入れ替える |

ライフサイクルフックは、起動や終了の途中でインスタンスを待機させます。終了の前にログを退避する、といった処理に使います。

詳細: [Systems Manager](../../services/operations.md#systems-manager)、[Fleet Manager](../../services/operations.md#fleet-manager)、[Auto Scaling の運用](../../services/operations.md#auto-scaling)、[ライフサイクルフック](../../services/operations.md#lifecycle-hooks)

### 構成管理のサービス {#t5-2-config}

**ガイドの項目:** 知識「構成管理のサービス（AWS Config など）」

AWS Config は、リソースの設定の履歴を記録し、ルールで評価します。

- 設定レコーダーが変更を記録します。
- 準拠の状態が変わると、`Config Rules Compliance Change` のイベントが発生します。
- 全社の状況はアグリゲーターで見ます。

詳細: [AWS Config](../../services/governance.md#config)、[アグリゲーター](../../services/governance.md#config-aggregators)、[設定レコーダー](../../services/governance.md#config-recorder)

### システムへの構成変更の適用 {#t5-2-apply-changes}

**ガイドの項目:** スキル「システムへの構成変更の適用」

| 変更の内容 | 手段 | 安全策 |
|---|---|---|
| サーバーの中のコマンド | Run Command | 同時実行数とエラーのしきい値 |
| AWS API を含む手順 | Automation | レート制御、ロールバックの手順 |
| アプリの設定 | AppConfig | 段階的な配布、アラームで戻す |
| AMI、起動テンプレート | インスタンスの更新 | `MinHealthyPercentage`、`AutoRollback` |
| インフラ全体 | CloudFormation | 変更セット |

最初は小さく適用します。タグで対象を絞り、`MaxConcurrency` を小さくし、`MaxErrors` を超えたら止めます。

詳細: [Run Command](../../services/operations.md#run-command)、[レート制御](../../services/operations.md#automation-rate-control)、[AppConfig のデプロイ戦略](../../services/secrets.md#deployment-strategies)、[インスタンスの更新](../../services/operations.md#instance-refresh)

### イベントに応じたインフラの変更 {#t5-2-respond}

**ガイドの項目:** スキル「イベントに応じたインフラの構成の変更」

| きっかけ | ターゲット | 処理 |
|---|---|---|
| セキュリティグループの変更（CloudTrail 経由） | Lambda、Automation | 許可しない規則を削除 |
| スポットの中断の警告 | Lambda | ログの退避、ジョブの再キュー |
| AWS Health の予定 | Automation | 事前にインスタンスを移す |
| Auto Scaling の起動の失敗 | OpsItem | 人が調査 |
| GuardDuty の検出結果 | Step Functions | インスタンスの隔離 |

EventBridge のターゲットには、Automation、OpsItem、Run Command を直接指定できます。Lambda を書かなくて済むなら、そのほうが運用の手間が減ります。

詳細: [EventBridge による修復パターン](../../services/operations.md#eventbridge-remediation)、[スポットの中断への対応](../../services/operations.md#spot-interruptions)、[EC2 の隔離](../../services/threat-detection.md#ir-ec2-isolation)、[EventBridge による自動化](../../services/threat-detection.md#ir-eventbridge)

### 望ましくない状態の修復 {#t5-2-remediate}

**ガイドの項目:** スキル「望ましくないシステムの状態の修復」

| 対象 | 検出 | 修復 |
|---|---|---|
| AWS リソースの設定 | Config ルール | Config の自動修復（Automation） |
| サーバーの中の状態 | State Manager の準拠 | State Manager の関連付け |
| スタックのドリフト | ドリフト検出 | テンプレートへの反映、再デプロイ |
| 異常なインスタンス | ヘルスチェック | Auto Scaling の置き換え |
| 異常なタスク、Pod | ヘルスチェック、プローブ | ECS、EKS の置き換え |

定型の修復は Automation を直接呼びます。人の判断が必要なものは OpsCenter に OpsItem を作ります。

詳細: [Config の修復](../../services/governance.md#config-remediation)、[State Manager](../../services/operations.md#state-manager)、[ドリフトの運用](../../services/operations.md#drift-operations)、[OpsCenter](../../services/operations.md#opscenter)

## タスク 5.3: システムとアプリケーションの障害を調査する {#task-5-3}

### メトリクスとログのサービス {#t5-3-observability}

**ガイドの項目:** 知識「AWS のメトリクスとログのサービス（CloudWatch、X-Ray など）」

| 手がかり | サービス | 問いへの答え |
|---|---|---|
| メトリクス | CloudWatch | いつ、どれくらい悪いか |
| ログ | CloudWatch Logs | 何が起きたか |
| トレース | X-Ray | どこで遅い、どこで失敗したか |
| API の履歴 | CloudTrail | 誰が何を変更したか |
| 設定の履歴 | AWS Config | 設定がどう変わったか |

詳細: [メトリクス、ログ、トレースの読み解き](../../services/observability.md#interpret-signals)、[サービス統合の問題を調べる](../../services/observability.md#debug-integration)、[サービスマップの読み方](../../services/observability.md#service-map)

### AWS のサービスの状態 {#t5-3-service-health}

**ガイドの項目:** 知識「AWS のサービスの状態を見るサービス（AWS Health、CloudWatch、Systems Manager OpsCenter など）」

| サービス | 見るもの |
|---|---|
| AWS Health | AWS 側の障害が自分のリソースに影響するか |
| CloudWatch | 自分のリソースのメトリクス。AWS 側の障害情報は分からない |
| OpsCenter | 運用の課題を OpsItem で一か所に集める |

OpsItem では、関連する Config の変更、CloudTrail ログ、アラームを一緒に確認でき、ランブックも実行できます。

!!! note "関連する運用サービスの状況"
    Systems Manager の Incident Manager と Change Manager は、2025 年 11 月 7 日に新規受付を終了しました。Amazon DevOps Guru は 2026 年 10 月 29 日で新規受付を終了しました。いずれもガイドのタスクには名前がありません。

詳細: [OpsCenter](../../services/operations.md#opscenter)、[AWS Health Dashboard](../../services/cloud-foundations.md#health)、[2026 年 10 月時点の提供状況](../../services/operations.md#status)

### 根本原因の分析 {#t5-3-root-cause}

**ガイドの項目:** 知識「根本原因の分析」

症状に対処するだけでなく、原因を特定して再発を防ぎます。

1. 影響の範囲と開始の時刻を確かめます。メトリクスで見ます。
2. その時刻の変更を調べます。デプロイ、CloudTrail、Config の履歴です。
3. ログとトレースで失敗の場所を絞ります。
4. AWS Health で AWS 側の問題を除外します。
5. 恒久の対策を決め、自動のテストやアラームに反映します。

**例:** 14 時から 5xx が増えた場合、`HTTPCode_Target_5XX_Count` でアプリ側と分かります。CodeDeploy の履歴で 13 時 58 分にデプロイがあり、X-Ray で新しい版の DynamoDB 呼び出しの失敗が見つかれば、原因は新しい版です。

詳細: [デバッグとエラー診断](../../services/observability.md#debugging)、[代表的なエラーコード](../../services/observability.md#error-codes)、[Config と CloudTrail の違い](../../services/governance.md#config-vs-cloudtrail)

### 失敗したデプロイの分析 {#t5-3-failed-deployments}

**ガイドの項目:** スキル「失敗したデプロイの分析（CodePipeline、CodeBuild、CodeDeploy、CloudFormation、CloudWatch の外形監視など）」

| サービス | 最初に見る場所 | よくある原因 |
|---|---|---|
| CodePipeline | 失敗したアクション、実行の履歴 | 権限、接続の状態、トリガーの条件 |
| CodeBuild | ビルドログのフェーズの詳細 | テストの失敗、特権モード、権限 |
| CodeDeploy | デプロイのイベント、`scripts.log` | エージェント、フックのスクリプト、ヘルスチェック |
| CloudFormation | スタックイベントの最初の失敗 | 権限、名前の衝突、依存関係 |
| Synthetics | カナリアのログ、スクリーンショット | デプロイ後の画面や API の異常 |

**CloudFormation の見方:** 最初の `CREATE_FAILED` か `UPDATE_FAILED` の理由を読みます。後に続く失敗は、ロールバックの結果であることが多いです。`UPDATE_ROLLBACK_FAILED` の状態なら、原因を直して `continue-update-rollback` を実行します。

**Synthetics の使い方:** デプロイの後の監視にカナリアを使います。アラームを CodeDeploy やパイプラインのステージ条件につなげば、失敗したときに自動で戻せます。

詳細: [デプロイ失敗の診断](../../services/cicd.md#troubleshooting-deployments)、[よくある失敗と対処](../../services/iac.md#common-failures)、[スタックのロールバックと失敗](../../services/iac.md#stack-failures)、[Synthetics](../../services/operations.md#synthetics)、[CodeDeploy のロールバック](../../services/cicd.md#codedeploy-rollback)

### プロセスの障害の分析 {#t5-3-failed-processes}

**ガイドの項目:** スキル「失敗したプロセスのインシデントの分析（Auto Scaling、ECS、EKS など）」

| 対象 | 見る場所 | 症状と原因 |
|---|---|---|
| Auto Scaling | `describe-scaling-activities` | 起動の繰り返しはヘルスチェックの猶予。起動できないのは容量、上限、キーの権限 |
| ECS | サービスイベント、タスクの停止理由 | `unable to place a task` は配置の制約や容量。イメージ取得の失敗は実行ロールや経路 |
| EKS | `kubectl describe pod`、イベント | `Pending` はスケジュール待ちで、ノードの不足など。`CrashLoopBackOff` はコンテナの起動後の異常終了の繰り返しで、アプリ、設定、プローブ、メモリ不足など。`ImagePullBackOff` はイメージや権限 |

ECS では、デプロイサーキットブレーカーが、起動できないデプロイを止めて前の版に戻します。

EKS の Liveness プローブが依存先を確認していると、データベースの障害でコンテナが再起動を繰り返します。

詳細: [スケーリングの失敗の調査](../../services/operations.md#asg-troubleshooting)、[サーキットブレーカー](../../services/containers.md#circuit-breaker)、[タスクの配置](../../services/containers.md#task-placement)、[ヘルスチェックとプローブ](../../services/containers.md#probes)

## 確認問題 {#self-check}

??? question "問1: 組織の全アカウントの AWS Health のイベントを一か所に集めて、担当へ通知したいです。アカウントごとのルールは避けたいです。何を使いますか？"
    AWS Health の組織ビューと委任管理者を使います。EventBridge のルールは自分のアカウントのイベントしか受けないので、組織全体を見る仕組みが必要です。受け取ったイベントは SNS などで通知します。

??? question "問2: 本番の VPC で SSH を 0.0.0.0/0 に開けるセキュリティグループの規則が追加されたら、数分以内に自動で消したいです。何を使いますか？"
    EventBridge で CloudTrail の `AuthorizeSecurityGroupIngress` を受け、Lambda か Automation で規則を削除する構成か、Config のマネージドルールと自動修復の構成です。修復の結果を SNS で通知します。ループを避けるため、削除の呼び出しで同じルールが動かないことも確認します。

??? question "問3: 注文のイベントを在庫、請求、通知の 3 つで処理します。請求だけ止まっても、他を止めず、後から処理したいです。どう構成しますか？"
    SNS と SQS のファンアウトです。処理ごとにキューを作り、請求が止まってもメッセージはキューに残ります。処理できないものには DLQ を設定します。

??? question "問4: CloudFormation の更新が UPDATE_ROLLBACK_FAILED で止まりました。手で削除したリソースが原因です。どう復旧しますか？"
    `continue-update-rollback` を実行します。原因のリソースを戻すか、`--resources-to-skip` で飛ばします。スキップしたリソースはテンプレートと食い違うので、後で揃えます。

??? question "問5: Auto Scaling グループで、インスタンスが起動と終了を繰り返しています。CLI で作ったグループで、アプリの起動に 3 分かかります。原因と対策は？"
    ヘルスチェックの猶予期間です。CLI の既定は 0 秒なので、起動中に ELB ヘルスチェックで異常と判定されます。猶予期間を 180 秒より長くします。

??? question "問6: EKS で新しいイメージのデプロイ後に Pod が CrashLoopBackOff になりました。ImagePullBackOff ではありません。何を調べますか？"
    イメージの取得は成功しており、コンテナが起動後に異常終了しています。`kubectl logs --previous` で前のコンテナのログを見ます。設定やシークレットの不足、Liveness プローブが早すぎないかを確認します。

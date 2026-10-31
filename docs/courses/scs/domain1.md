# 分野1: 検出

配点は **16%** です。何を監視し、どこにログを集め、検出できないときにどう直すかを問います。

サービス名を当てるより、組織全体での集約、データの保持、誤設定の切り分けといった制約の下での判断が中心です。

[![検出結果を集約して自動対応する流れ](../../assets/diagrams/threat-detection-response.png)](../../assets/diagrams/threat-detection-response.png)

!!! note "CloudTrail Lake の状況"
    CloudTrail Lake は 2026年5月31日で新規受付を終了しました。既存の顧客は使い続けられます。新規の環境で長期の検索が必要なら、証跡を S3 に残して Athena で検索するか、Security Lake を使います。

!!! note "Security Hub の名前"
    2025年12月に新しい Security Hub が一般提供され、従来の製品は **Security Hub CSPM** になりました。基準に対する準拠のチェックは CSPM、検出結果の関連付けとリスクの優先付けは新しい Security Hub です。古い教材の「Security Hub」は CSPM を指します。

## タスク 1.1: アカウントや組織の監視とアラートを設計して実装する {#task-1-1}

### 1.1.1 監視要件の分析 {#skill-1-1-1}

ワークロードの構成から、「何が起きたら困るか」を決め、それを見るサービスを選びます。

| 守りたいもの | 脅威の例 | 見るもの |
|---|---|---|
| 認証情報 | 漏えいしたキーの利用 | GuardDuty、CloudTrail |
| EC2、EKS、ECS | マルウェア、暗号通貨の採掘 | GuardDuty Runtime Monitoring、Malware Protection |
| 既知の脆弱性 | CVE、開いたポート | Inspector |
| S3 の機密データ | 個人情報の保管、公開設定 | Macie、Access Analyzer |
| 設定の基準 | CIS や PCI DSS からの逸脱 | Security Hub CSPM、Config |
| Web アプリ | SQL インジェクション、DDoS | WAF のログ、Shield のメトリクス |

選ぶときの軸は、対象の範囲、費用、検出までの時間です。たとえば S3 の全オブジェクトを Macie のジョブで毎日検査すると費用が大きくなるので、全体は自動検出のサンプリングで見て、重要なバケットだけジョブにします。

詳細: [サービスの一覧](../../services/threat-detection.md#choosing)、[どのログを見るか](../../services/threat-detection.md#log-sources)

### 1.1.2 ワークロードの監視戦略 {#skill-1-1-2}

ヘルスチェックは可用性の監視ですが、攻撃の兆候にもなります。層ごとに使い分けます。

| 手段 | 見るもの | 主な用途 |
|---|---|---|
| ALB のヘルスチェック | ターゲットの応答 | 異常なターゲットを外す |
| Route 53 ヘルスチェック | 外部からの到達性 | DNS フェイルオーバー、Shield Advanced のヘルスベース検出 |
| CloudWatch Synthetics | 利用者の操作の再現 | 外形監視 |
| CloudWatch アラーム | メトリクスのしきい値 | 通知と自動対応 |

Shield Advanced のヘルスベース検出は Route 53 ヘルスチェックを使います。設定すると誤検知が減り、検出が早くなります。SRT のプロアクティブエンゲージメントの前提でもあります。

詳細: [ヘルスチェックとプローブ](../../services/observability.md#health-checks)、[Route 53 ヘルスチェック](../../services/networking.md#route53-health-checks)、[Synthetics](../../services/operations.md#synthetics)、[Shield Advanced](../../services/threat-detection.md#shield-advanced)

### 1.1.3 セキュリティイベントの集約 {#skill-1-1-3}

組織全体の集約は、**委任管理者**と**リージョンの扱い**を問われます。管理アカウントで日常の運用をしないのが基本です。

| サービス | 組織での有効化 | リージョンの注意 |
|---|---|---|
| GuardDuty | 委任管理者と自動有効化（`ALL`、`NEW`、`NONE`） | リージョンごとに指定する |
| Security Hub CSPM | 委任管理者と中央設定 | ホームリージョンとリンクリージョンで集約する |
| Inspector | 委任管理者。新しいメンバーを自動で有効化 | |
| Macie | 委任管理者がリージョンごとにメンバーを追加 | |
| Config | アグリゲーターで集約 | 組織全体を 1 か所で閲覧できる |
| Security Lake | 委任管理者。ロールアップリージョンで集約 | サブスクライバーは作成したリージョンのデータだけ見える |

CSPM の「ローカル設定」は新規アカウントと現在のリージョンだけが対象です。全アカウントの全リージョンで標準を統一するなら**中央設定**を選びます。

集約した検出結果を動かすのが EventBridge です。GuardDuty の委任管理者の EventBridge にはメンバーの検出結果も届くので、自動対応を 1 か所に置けます。

詳細: [GuardDuty の複数アカウント](../../services/threat-detection.md#guardduty-multi-account)、[Security Hub の組織と集約](../../services/threat-detection.md#security-hub-org)、[Config アグリゲーター](../../services/governance.md#config-aggregators)、[委任管理者](../../services/governance.md#delegated-admin)

### 1.1.4 メトリクス、アラート、ダッシュボード {#skill-1-1-4}

サービスごとに、異常の検出の仕組みが違います。

| サービス | 検出するもの | 通知の経路 | 注意点 |
|---|---|---|---|
| GuardDuty | 脅威。重要度 Critical は 9.0 以上、High は 7.0 以上 | EventBridge、S3 エクスポート | 検出結果の保持は 90 日。同じ検出結果の更新の通知は既定で 6 時間ごと |
| Security Hub | 露出の検出結果、攻撃経路 | 自動化ルール、EventBridge | 自動化ルールは EventBridge より先に適用される |
| Macie | 機密データ、バケットの設定変更 | EventBridge、Security Hub CSPM | CSPM へは既定でポリシーの検出結果のみ送る |
| Security Lake | 検出はしない。ログの集約 | サブスクライバー | 検出は SIEM や Athena のクエリで行う |

CloudTrail や VPC フローログを CloudWatch Logs に送れば、**メトリクスフィルター**で特定の操作をメトリクスにできます。たとえば `StopLogging` やルートユーザーの利用にアラームを設定します。傾向の変化には CloudWatch の異常検知と CloudTrail Insights を使います。

人に届けるだけなら AWS User Notifications、修復まで動かすなら EventBridge です。

詳細: [GuardDuty の検出結果](../../services/threat-detection.md#guardduty-findings)、[イベント連携](../../services/threat-detection.md#guardduty-events)、[メトリクスフィルター](../../services/observability.md#metric-filters)、[異常検知](../../services/observability.md#anomaly-detection)、[CloudTrail Insights](../../services/observability.md#cloudtrail-insights)、[User Notifications](../../services/operations.md#user-notifications)

### 1.1.5 定期的な評価と調査の自動化 {#skill-1-1-5}

| 手段 | 何を定期的に行うか | 向いている場面 |
|---|---|---|
| Config 適合パック | ルールと修復をまとめて組織へ展開 | 基準を一括で評価する |
| Security Hub CSPM の標準 | コントロールを継続的にチェック | スコアで全体を把握する |
| Systems Manager State Manager | ノードの状態を定期的に望ましい状態へ戻す | エージェントの設定や OS の設定 |
| Inspector | CVE を継続的にスキャン | 新しい CVE が出たときも自動で再評価する |
| Macie のジョブ | 定期的に S3 を検査 | 特定のバケットの詳しい検査 |

Config のルール自体は止めるものではなく、評価するだけです。修復には Systems Manager Automation を付けます。CSPM の多くのコントロールは Config のサービスリンクルールで動くので、Config を有効にしていないと結果が出ません。

!!! note "Audit Manager の状況"
    AWS は Audit Manager の代替として Config の適合パックを案内しています。詳しくは[スキル 6.3.2](domain6.md#skill-6-3-2) を参照してください。

詳細: [適合パック](../../services/governance.md#config-conformance-packs)、[CSPM の標準](../../services/threat-detection.md#security-hub-cspm)、[State Manager](../../services/operations.md#state-manager)、[Macie の検出方法](../../services/threat-detection.md#macie-discovery)

## タスク 1.2: ログの仕組みを設計して実装する {#task-1-2}

### 1.2.1 ログの取り込み元と保存先の選択 {#skill-1-2-1}

取り込み元は「何を知りたいか」で決めます。保存先は、検索の頻度、保持期間、費用で決めます。

| 保存先 | 向いている場面 | トレードオフ |
|---|---|---|
| CloudWatch Logs | すぐ検索したい、メトリクスフィルターを使いたい | 取り込みと保管の費用が高い |
| S3 | 長期の保管、改ざん防止 | 検索には Athena などが要る |
| Security Lake | 複数ソースの正規化、SIEM への配信 | OCSF と Parquet に変換するための基盤が増える |
| OpenSearch Service | 全文検索とダッシュボード | クラスターの運用と費用 |

監査で数年の保持が必要なら、S3 に送ってライフサイクルで安いクラスへ移し、Object Lock で保護します。CloudWatch Logs のロググループは既定で無期限に保持されるので、保持期間を決めないと費用が増え続けます。

詳細: [どのログを見るか](../../services/threat-detection.md#log-sources)、[ロググループと保持期間](../../services/observability.md#log-groups)、[ログクラス](../../services/observability.md#log-classes)

### 1.2.2 サービスとアプリケーションのログの設定 {#skill-1-2-2}

試験ガイドの例は、組織の証跡、ログ専用アカウント、CloudWatch Logs エージェントの3つです。

**組織の証跡:** 管理アカウントなどで作成すると、全メンバーのイベントを記録します。出力先はログ保管アカウントの S3 にし、SCP で `StopLogging` や `DeleteTrail` を拒否します。

| 設定 | 内容 | 落とし穴 |
|---|---|---|
| イベントの種類 | 管理イベントは既定。データイベントは別途有効にする | S3 のオブジェクト操作や Lambda の呼び出しは、既定では記録されない |
| ログファイルの検証 | ダイジェストファイルで改ざんや削除を検出 | 確認には `validate-logs` の実行が必要 |
| 暗号化 | KMS キーを指定できる | キーポリシーで CloudTrail を許可する |
| CloudWatch Logs への配信 | IAM ロールが必要 | 証跡の設定と一致するイベントだけが届く |

**ログ専用アカウント:** 各アカウントのロググループにサブスクリプションフィルターを付け、別アカウント向けの論理的な宛先（`PutDestination`）を経由して、ログ専用アカウントの Kinesis Data Streams や Firehose へ送ります。S3 にまとめる場合は、バケットポリシーで各アカウントからの書き込みを許可します。

**エージェント:** CloudWatch エージェントは OS のログファイルとメモリなどのメトリクスを送ります。設定は Parameter Store に置いて全台で共有します。インスタンスのロールに `CloudWatchAgentServerPolicy` が必要です。

詳細: [証跡](../../services/observability.md#cloudtrail-trails)、[イベントの種類](../../services/observability.md#cloudtrail-events)、[サブスクリプションフィルターの設定](../../services/observability.md#subscription-settings)、[CloudWatch エージェント](../../services/operations.md#cloudwatch-agent)、[マルチアカウントのパターン](../../services/governance.md#multi-account-patterns)

### 1.2.3 ログの保管、データレイク、他社ツールとの統合 {#skill-1-2-3}

Security Lake はセキュリティログを自分のアカウントの S3 に集め、Parquet と OCSF に変換します。

| 設定 | 内容 |
|---|---|
| AWS のソース | CloudTrail、S3 と Lambda のデータイベント、EKS 監査ログ、Route 53 Resolver クエリログ、Security Hub CSPM の検出結果、VPC フローログ、WAF ログ |
| カスタムソース | OCSF の Parquet で S3 へ書き込む。1 オブジェクトに 1 つの OCSF クラス |
| ロールアップリージョン | 複数リージョンのデータを 1 つに集める |
| 保持 | リージョンごとにライフサイクルを設定 |

他社の SIEM には、次のどちらかで渡します。

| サブスクライバー | 受け取り方 | 選ぶ場面 |
|---|---|---|
| データアクセス | 新しいオブジェクトの通知を HTTPS か SQS で受け取る | SIEM に取り込む |
| クエリアクセス | Lake Formation のテーブルを Athena などで直接検索 | データを複製せずに分析する |

複数リージョンのデータを渡すには、サブスクライバーをロールアップリージョンで作ります。

詳細: [Security Lake](../../services/threat-detection.md#security-lake)

### 1.2.4 ログの分析 {#skill-1-2-4}

| ツール | 向いている分析 | 注意点 |
|---|---|---|
| CloudWatch Logs Insights | ロググループを対話的に検索 | CloudWatch Logs に入っているログだけが対象 |
| Athena | S3 上の大量のログを SQL で検索 | パーティションがないと走査量と費用が増える |
| Security Hub | 検出結果の絞り込みと優先付け | 生ログは見られない |

フローログの拒否された通信を Logs Insights で集計する、漏えいしたキーの操作を Athena で検索する、といった使い方を押さえます。

詳細: [Logs Insights](../../services/observability.md#logs-insights)、[Athena](../../services/streaming.md#athena)、[CloudTrail の調査](../../services/threat-detection.md#investigate-cloudtrail)、[フローログの調査](../../services/threat-detection.md#investigate-flow-logs)

### 1.2.5 ログの正規化、解析、関連付け {#skill-1-2-5}

| ツール | 役割 |
|---|---|
| Lambda | サブスクリプションフィルターで受けたログを変換、整形して転送する |
| OpenSearch Service | 異なるログを検索、関連付け、ダッシュボードで可視化する |
| Managed Grafana | CloudWatch や OpenSearch などをデータソースにして可視化する。データの保管先ではない |
| Security Lake | OCSF に統一して、ソースをまたいだクエリを可能にする |

Managed Grafana の認証は SAML 2.0 か IAM Identity Center で、IAM ユーザーでは直接ログインしません。

詳細: [サブスクリプションフィルター](../../services/observability.md#subscription-filters)、[OpenSearch Service](../../services/databases.md#opensearch)、[Managed Grafana](../../services/operations.md#managed-grafana)

### 1.2.6 ネットワーク設計と脅威に合うログの選択 {#skill-1-2-6}

| 知りたいこと | ログ | 残らないもの |
|---|---|---|
| VPC の IP 通信と許可、拒否 | VPC フローログ | 中身、Amazon DNS への通信、メタデータへの通信 |
| Transit Gateway を通る通信 | Transit Gateway フローログ | |
| どのドメインを問い合わせたか | Route 53 Resolver クエリログ | 自前の DNS サーバーへの問い合わせ |
| HTTP の内容 | ALB、CloudFront、WAF のログ | |
| ドメインやシグネチャの一致 | Network Firewall のアラートログ | ステートレスで Pass や Drop した通信 |
| ペイロード | Traffic Mirroring | |

DNS トンネリングによる持ち出しが疑われるなら Resolver クエリログ、NAT の裏の元の IP を知りたいならカスタム形式の `pkt-srcaddr` です。集中型の Transit Gateway 構成で VPC 間の通信を調べるなら、各 VPC のフローログより Transit Gateway フローログが効率的です。

フローログは作成後に形式を変更できません。必要なフィールドが足りなければ作り直します。

詳細: [VPC フローログ](../../services/networking.md#flow-logs)、[フローログの分析](../../services/network-connectivity.md#flow-log-analysis)、[Network Firewall のログ](../../services/threat-detection.md#nfw-logging)、[Traffic Mirroring](../../services/network-connectivity.md#traffic-mirroring)

## タスク 1.3: 監視、ログ、アラートのトラブルシューティング {#task-1-3}

### 1.3.1 機能、権限、設定の分析 {#skill-1-3-1}

ログが出ない原因の多くは、権限か、そもそも有効にしていないことです。

| 対象 | 必要な設定 | よくある原因 |
|---|---|---|
| Lambda | 実行ロールにログの権限 | ロールの権限不足。`Text` 形式のままログレベルを変えても効かない |
| API Gateway（REST） | アカウント設定の `cloudWatchRoleArn` を**リージョンごと**に。ステージで `loggingLevel` | ロール未設定だと、ステージで有効にしても書かれない |
| CloudFront | 標準ログ、リアルタイムログの設定 | 標準ログはベストエフォートで遅れることがある |
| WAF | 送信先の名前を `aws-waf-logs-` で始める | 接頭辞が違うと送信先に選べない |
| ヘルスチェック | セキュリティグループで検査元を許可 | ALB からの通信やパスの設定を誤る |

API Gateway の `dataTraceEnabled` は本文までログに残すので、機密情報が残らないよう本番では使いません。

詳細: [Lambda のログ設定](../../services/lambda.md#logging-config)、[Lambda の実行ロール](../../services/lambda.md#execution-role)、[API Gateway のログ](../../services/api-gateway.md#logging-metrics)、[CloudFront のログ](../../services/networking.md#cloudfront-logs)、[WAF のログ](../../services/certificates.md#waf-logging)、[ALB のヘルスチェック](../../services/networking.md#alb-health-checks)

### 1.3.2 誤設定の修正 {#skill-1-3-2}

切り分けの順番を押さえます。まず有効か、次に権限か、最後に配信の遅れかを確認します。

| 症状 | 確認すること |
|---|---|
| CloudWatch エージェントのメトリクスがない | 名前空間が `CWAgent` か、`fetch-config` を再実行したか、ロールの権限 |
| コンテナでエージェントが遅い | IMDS のホップ制限 |
| CloudTrail のログが S3 に届かない | バケットポリシー、KMS のキーポリシー。配信は平均約 5 分遅れる |
| S3 のオブジェクト操作が記録されない | データイベントが無効 |
| ロググループの KMS 関連付けが失敗 | キーポリシーに `logs.<region>.amazonaws.com` がない |
| GuardDuty の DNS の検出結果が出ない | EC2 が AWS のリゾルバーを使っていない |
| CSPM のコントロールの結果が出ない | Config が無効か、対象のリソースタイプを記録していない |
| EventBridge のルールが動かない | `detail-type` の綴り、リージョン、ターゲットの権限。抑制された検出結果はイベントにならない |
| フローログが S3 に届かない | 配信の遅れ（CloudWatch Logs は約 5 分、S3 は約 10 分） |
| 許可と拒否の原因が分からない | フローログでは SG か NACL か判別できない。戻りだけ `REJECT` なら NACL を疑う |

詳細: [エージェントのよくある問題](../../services/operations.md#cloudwatch-agent)、[KMS による暗号化](../../services/observability.md#logs-kms)、[GuardDuty のデータソース](../../services/threat-detection.md#guardduty-data-sources)、[EventBridge による自動化](../../services/threat-detection.md#ir-eventbridge)

## 確認問題 {#self-check}

??? question "問1: 組織の全アカウントで GuardDuty を有効にしました。東京リージョンの委任管理者では全メンバーが見えますが、大阪リージョンで作られた不審なリソースが検出されていません。原因と対策は？"
    委任管理者の指定は**リージョンごと**です。大阪リージョンでも委任管理者を指定し、自動有効化を設定します。使っていないリージョンで攻撃者がリソースを作る場合に備えて、全リージョンで有効にするのが推奨です。

??? question "問2: 監査のため、S3 のオブジェクトの読み取りを7年間記録し、改ざんされていないことを示す必要があります。費用も抑えたいです。どう構成しますか？"
    組織の証跡で S3 のデータイベントを有効にし、ログ保管アカウントの S3 に出力します。ログファイルの検証を有効にし、Object Lock のコンプライアンスモードで保護して、ライフサイクルで安いクラスへ移します。データイベントは既定では記録されず、CloudWatch Logs に7年残すのは費用が大きくなります。

??? question "問3: 複数のアカウントとリージョンの CloudTrail、VPC フローログ、WAF ログを共通の形式で他社 SIEM に渡したいです。独自の変換処理は作りたくありません。何を使いますか？"
    Security Lake です。OCSF と Parquet に変換し、ロールアップリージョンに集約します。SIEM はそのリージョンで作ったデータアクセスのサブスクライバーとして、SQS か HTTPS の通知で取り込みます。別のリージョンで作ると、そのリージョンのデータしか見えません。

??? question "問4: REST API のステージでログレベルを INFO にしましたが、CloudWatch Logs に何も出ません。IAM ユーザーの権限には問題がありません。何を確認しますか？"
    API Gateway のアカウント設定の `cloudWatchRoleArn` です。`apigateway.amazonaws.com` を信頼し `AmazonAPIGatewayPushToCloudWatchLogs` を付けたロールを、リージョンごとに指定します。ログを書くのは呼び出し元の IAM ユーザーではなく API Gateway です。

??? question "問5: EC2 からの DNS トンネリングによる持ち出しを調べたいのですが、VPC フローログには該当の通信が見当たりません。なぜですか？また何を見ますか？"
    Amazon DNS サーバーへの通信はフローログの対象外です。Route 53 Resolver クエリログで問い合わせたドメインを確認します。GuardDuty の `Trojan:EC2/DNSDataExfiltration` も手がかりになりますが、EC2 が自前の DNS を使っていると検出されません。

??? question "問6: Security Hub CSPM で標準を有効にしたのに、多くのコントロールで結果が出ません。別のアカウントでは全リージョンの標準をバラバラに設定していて、統一もしたいです。どうしますか？"
    結果が出ないのは、大半のコントロールが Config のサービスリンクルールで動くので、Config の有効化が必要だからです。統一には委任管理者から中央設定を使い、設定ポリシーでアカウント、OU、リージョンをまたいで管理します。ローカル設定は既存のアカウントには効きません。

# 分野4: CloudWatch Logs

ログをどう数値にし、どこへ流し、どう守るかを問います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [ログの暗号化](../../domain4.md#t4-1-encryption) | 保存時、転送時の暗号化の選択肢、ログデータの暗号化の設定 |
| [ログ収集の権限](../../domain4.md#t4-1-permissions) | ログ収集のセキュリティの構成 |
| [メトリクスフィルター](../../domain4.md#t4-1-metric-filters) | メトリクスフィルター |
| [ライフサイクル](../../domain4.md#t4-1-lifecycle) | ログの保存のライフサイクル |
| [サブスクリプション](../../domain4.md#t4-1-subscriptions) | サブスクリプションによるログ処理 |
| [ログの検索](../../domain4.md#t4-1-search) | フィルターと Logs Insights の検索 |

## 学習の順番 {#study-order}

1. [メトリクスフィルター](../../../../services/observability.md#metric-filters): 作成後のログだけが対象であることを確認します。
2. [サブスクリプションフィルターの設定](../../../../services/observability.md#subscription-settings): 宛先、権限、アカウントをまたぐ配信を理解します。
3. [Logs Insights でログを検索する](../../../../services/observability.md#logs-insights): 集計の書き方を確認します。
4. [保持期間の設定](../../../../services/observability.md#log-retention): 既定が無期限であることを押さえます。
5. [KMS による暗号化](../../../../services/observability.md#logs-kms): キーポリシーの条件を確認します。
6. [データ保護ポリシー](../../../../services/observability.md#logs-data-protection): マスクの仕組みを覚えます。

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 過去のログを集計する | Logs Insights |
| ログを継続して S3 へ送る | サブスクリプションフィルターと Firehose |
| 全アカウントのログを集める | 論理的な宛先と宛先ポリシー |
| 関連付けが `AccessDenied` | キーポリシーでサービスプリンシパルを許可する |
| ログの機密情報を隠す | データ保護ポリシー |

## 引っかかりやすい点 {#traps}

- 受け取るデータは Base64 と gzip でエンコードされています。
- `CreateExportTask` はリアルタイムではありません。
- `awslogs` の権限はタスク実行ロールに付けます。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [cloudwatch-logs 問1](../../exercises/cloudwatch-logs.md#q1) | ログの暗号化 | 監査の要件で、既存のロググループをカスタマー管理の KMS キーで暗号化します。aws logs a… |
| [cloudwatch-logs 問2](../../exercises/cloudwatch-logs.md#q2) | ログの暗号化 | アプリのログに誤ってメールアドレスやカード番号が含まれることがあります。アプリの修正には時間がかかり… |
| [cloudwatch-logs 問3](../../exercises/cloudwatch-logs.md#q3) | ログの暗号化 | ログの暗号化について、担当者の説明のうち正しいものを選んでください。（2つ選択） |
| [cloudwatch-logs 問4](../../exercises/cloudwatch-logs.md#q4) | ログ収集の権限 | EC2 の CloudWatch エージェントと ECS の Fargate のタスクから、ログが届… |
| [cloudwatch-logs 問5](../../exercises/cloudwatch-logs.md#q5) | ログ収集の権限 | VPC フローログと CloudTrail を、宛先ごとに設定します。(1) フローログを Clou… |
| [cloudwatch-logs 問6](../../exercises/cloudwatch-logs.md#q6) | ログ収集の権限 | 全アカウントのログを、ログ保管アカウントの Kinesis Data Streams へ集めます。送… |
| [cloudwatch-logs 問7](../../exercises/cloudwatch-logs.md#q7) | メトリクスフィルター | アプリのログの ERROR を数えるメトリクスフィルターを今日作りました。先週の障害の回数を確認した… |
| [cloudwatch-logs 問8](../../exercises/cloudwatch-logs.md#q8) | メトリクスフィルター | JSON 形式のログの latencyMs の値をカスタムメトリクスにして、status が 500… |
| [cloudwatch-logs 問9](../../exercises/cloudwatch-logs.md#q9) | メトリクスフィルター | ERROR の数のメトリクスフィルターにアラームを付けました。ERROR がない時間はデータが発行さ… |
| [cloudwatch-logs 問10](../../exercises/cloudwatch-logs.md#q10) | ライフサイクル | CloudWatch Logs の費用が増え続けています。調べると、Lambda や ECS が自動… |
| [cloudwatch-logs 問11](../../exercises/cloudwatch-logs.md#q11) | ライフサイクル | ログの保存方針は次のとおりです。CloudWatch Logs では 30 日だけ検索し、その後は … |
| [cloudwatch-logs 問12](../../exercises/cloudwatch-logs.md#q12) | ライフサイクル | ログを継続して S3 へ送り、S3 で 7 年保管します。担当者は 1 時間ごとに CreateEx… |
| [cloudwatch-logs 問13](../../exercises/cloudwatch-logs.md#q13) | サブスクリプション | 監査のログを、ほぼリアルタイムで検索基盤へ、同時に別の担当の Lambda へも送ります。受け取る … |
| [cloudwatch-logs 問14](../../exercises/cloudwatch-logs.md#q14) | サブスクリプション | 全アカウントのログを中央へ集めて、(1) S3 へ配信する、(2) 複数のコンシューマーが順序を保っ… |
| [cloudwatch-logs 問15](../../exercises/cloudwatch-logs.md#q15) | サブスクリプション | あるロググループで、ERROR のログだけをリアルタイムに OpenSearch Service へ… |
| [cloudwatch-logs 問16](../../exercises/cloudwatch-logs.md#q16) | ログの検索 | 複数の Lambda のロググループで、過去 24 時間の ERROR を 5 分ごとに数え、多い順… |
| [cloudwatch-logs 問17](../../exercises/cloudwatch-logs.md#q17) | ログの検索 | 次の調査で手段を選びます。(1) スペース区切りのアクセスログで、ステータスが 5xx の行を対象に… |
| [cloudwatch-logs 問18](../../exercises/cloudwatch-logs.md#q18) | ログの検索 | 3 年分の VPC フローログと ALB のアクセスログは S3 にあります。別途、直近 2 週間の… |

<!-- questions:end -->

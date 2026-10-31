# 分野1: CloudWatch

何を有効にするか、アラームが何を呼べるか、複数アカウントでどう見るかを問います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [1.1.1](../../domain1.md#skill-1-1-1) | ワークロードの監視とログの設定 |
| [1.1.2](../../domain1.md#skill-1-1-2) | CloudWatch エージェントの設定と管理 |
| [1.1.3](../../domain1.md#skill-1-1-3) | アラームの設定、特定、トラブルシューティング |
| [1.1.4](../../domain1.md#skill-1-1-4) | 複数アカウント、複数リージョンのダッシュボード |

## 学習の順番 {#study-order}

1. [CloudWatch と CloudTrail の違い](../../../../services/observability.md#cloudtrail-vs-cloudwatch): 「誰が何をしたか」と「性能と状態」を分けます。
2. [EC2 の既定メトリクスとエージェント](../../../../services/observability.md#ec2-metrics)と[CloudWatch エージェント](../../../../services/operations.md#cloudwatch-agent): `AWS/EC2` にメモリがないことと、エージェントの導入の手順を確認します。
3. [メトリクスフィルター](../../../../services/observability.md#metric-filters)と[サブスクリプションフィルター](../../../../services/observability.md#subscription-filters): ログを数える機能と転送する機能を区別します。
4. [評価の仕組みと M out of N](../../../../services/observability.md#alarm-evaluation)と[欠落データの扱い](../../../../services/observability.md#treat-missing-data): M out of N と欠落データの 4 つの値を覚えます。
5. [アラームのアクション](../../../../services/observability.md#alarm-actions)と[複合アラーム](../../../../services/observability.md#composite-alarms): アクションの違いを表で覚えます。
6. [ダッシュボードの設定](../../../../services/observability.md#dashboard-settings): 共有の 3 つの方法と注意点を確認します。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| `AWS/EC2` の詳細モニタリング | 1 分間隔 | メモリは増えない |
| エージェントの既定の名前空間 | `CWAgent` | `AWS/EC2` を探さない |
| メールアドレスでの共有 | 1 ダッシュボードに最大 5 人 | 各自がパスワードを作る |
| シンク | アカウントのリージョンごとに 1 つ | リージョンごとに設定する |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| ログの文字列の件数で通知する | メトリクスフィルターとアラーム |
| ログをほぼリアルタイムで Firehose へ送る | サブスクリプションフィルター |
| ルートユーザーの利用を検知する | CloudTrail を CloudWatch Logs へ送り、メトリクスフィルターとアラーム |
| グループ全体のメモリでスケールする | エージェントの `aggregation_dimensions` に `AutoScalingGroupName` |
| データが来ない時間を正常として扱う | `TreatMissingData` を `notBreaching` |
| 複合アラームから再起動する | EventBridge で受けて Automation |
| 組織の全アカウントを 1 か所で見る | クロスアカウントオブザーバビリティで組織か OU をリンク |

## 引っかかりやすい点 {#traps}

- 複合アラームのアクションに EC2 と Auto Scaling はありません。
- 異常検知のアラームは Auto Scaling のアクションに使えません。
- 子アラームに通知を残すと、複合アラームを作っても通知は減りません。
- 設定を変えたら `-a fetch-config` を再実行します。
- Bedrock のモデル呼び出しログは既定で無効です。
- 共有された人はアカウントの全メトリクスと全 EC2 の名前とタグを照会できます。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [cloudwatch 問1](../../exercises/cloudwatch.md#q1) | 1.1.1 | アプリケーションのログは CloudWatch Logs に届いています。ログに ERROR が 5… |
| [cloudwatch 問2](../../exercises/cloudwatch.md#q2) | 1.1.1 | 監査担当者から、ルートユーザーの API 利用を検知してアラームで通知するよう求められました。組み合… |
| [cloudwatch 問3](../../exercises/cloudwatch.md#q3) | 1.1.1 | ロググループに届くログを、ほぼリアルタイムで Data Firehose へ流し、分析用の S3 に… |
| [cloudwatch 問4](../../exercises/cloudwatch.md#q4) | 1.1.1 | Amazon Bedrock を使うアプリケーションのプロンプトと応答を、監査のために残すよう求めら… |
| [cloudwatch 問5](../../exercises/cloudwatch.md#q5) | 1.1.1 | EKS のクラスターで PromQL のクエリと Grafana のダッシュボードをすでに運用してい… |
| [cloudwatch 問6](../../exercises/cloudwatch.md#q6) | 1.1.1 | S3 の特定のバケットについて、オブジェクトの GetObject を誰が実行したかを記録したいと考… |
| [cloudwatch 問7](../../exercises/cloudwatch.md#q7) | 1.1.2 | Auto Scaling グループの EC2 のメモリ使用率でスケールしたいと考えています。AWS/… |
| [cloudwatch 問8](../../exercises/cloudwatch.md#q8) | 1.1.2 | CloudWatch エージェントを導入しましたが、担当者が mem_used_percent を … |
| [cloudwatch 問9](../../exercises/cloudwatch.md#q9) | 1.1.2 | 数百台の EC2 に CloudWatch エージェントを導入し、同じ設定を使いたいと考えています。… |
| [cloudwatch 問10](../../exercises/cloudwatch.md#q10) | 1.1.2 | Parameter Store の設定を変更して収集するメトリクスを増やしましたが、稼働中のインスタ… |
| [cloudwatch 問11](../../exercises/cloudwatch.md#q11) | 1.1.2 | EKS のクラスターに Container Insights を導入し、アプリケーションのログも送り… |
| [cloudwatch 問12](../../exercises/cloudwatch.md#q12) | 1.1.3 | CPU が高く、かつ接続数も多いときだけ EC2 を再起動したいと考えています。複合アラームのアクシ… |
| [cloudwatch 問13](../../exercises/cloudwatch.md#q13) | 1.1.3 | 1 分間隔の CPU のアラームが、短いスパイクのたびに鳴ります。5 分のうち 3 回以上しきい値を… |
| [cloudwatch 問14](../../exercises/cloudwatch.md#q14) | 1.1.3 | 毎時 1 回だけ動くバッチがカスタムメトリクスを送ります。データが来ない間にアラームが INSUFF… |
| [cloudwatch 問15](../../exercises/cloudwatch.md#q15) | 1.1.3 | SNS の通知付きのアラームが ALARM になり、メールが 1 通届きました。その後 3 時間 A… |
| [cloudwatch 問16](../../exercises/cloudwatch.md#q16) | 1.1.3 | 複合アラームを作り、そこへ SNS を付けましたが、通知の数が減りません。CPU とメモリの子アラー… |
| [cloudwatch 問17](../../exercises/cloudwatch.md#q17) | 1.1.3 | アラームと呼び出せるアクションの組み合わせとして正しいものを選んでください。（2つ選択） |
| [cloudwatch 問18](../../exercises/cloudwatch.md#q18) | 1.1.4 | 組織の 30 アカウントのメトリクスとログを、監視用の 1 アカウントのダッシュボードで見たいと考え… |
| [cloudwatch 問19](../../exercises/cloudwatch.md#q19) | 1.1.4 | クロスアカウントオブザーバビリティを東京リージョンで設定しました。監視アカウントで、ソースアカウント… |
| [cloudwatch 問20](../../exercises/cloudwatch.md#q20) | 1.1.4 | AWS アカウントを持たない社外の監査担当 3 名に、1 つのダッシュボードだけを見せたいと考えてい… |
| [cloudwatch 問21](../../exercises/cloudwatch.md#q21) | 1.1.4 | ダッシュボードをメールアドレスの指定で共有するときの注意点として正しいものはどれですか。 |

<!-- questions:end -->

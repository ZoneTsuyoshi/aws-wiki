# 分野1: 監視とログのトラブルシューティング

ログや検出結果が出ないときに、有効か、権限か、配信の遅れかの順に切り分ける力を問います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [1.3.1](../../domain1.md#skill-1-3-1) | 機能、権限、設定の分析 |
| [1.3.2](../../domain1.md#skill-1-3-2) | 誤設定の修正 |

## 学習の順番 {#study-order}

1. [Lambda の実行ロール](../../../../services/lambda.md#execution-role)と[ログ設定](../../../../services/lambda.md#logging-config): 誰がログを書くかと、ログレベルが効く条件を確認します。
2. [API Gateway のログ](../../../../services/api-gateway.md#logging-metrics): `cloudWatchRoleArn` がリージョンごとであることと、データトレースの注意点を押さえます。
3. [CloudFront のログ](../../../../services/networking.md#cloudfront-logs)と [WAF のログ](../../../../services/certificates.md#waf-logging): 配信の性質と、送信先の名前とリージョンの条件を覚えます。
4. [ALB のヘルスチェック](../../../../services/networking.md#alb-health-checks): セキュリティグループで検査元を許可します。
5. [CloudWatch エージェント](../../../../services/operations.md#cloudwatch-agent): 名前空間、設定の読み込み、ホップ制限を確認します。
6. [KMS による暗号化](../../../../services/observability.md#logs-kms): キーポリシーと、過去のログの扱いを押さえます。
7. [GuardDuty のデータソース](../../../../services/threat-detection.md#guardduty-data-sources)、[抑制ルール](../../../../services/threat-detection.md#guardduty-suppression)、[CSPM の標準](../../../../services/threat-detection.md#security-hub-cspm): 検出結果が出ない、または届かない理由を整理します。
8. [フローログの分析](../../../../services/network-connectivity.md#flow-log-analysis): `ACCEPT` と `REJECT` の組み合わせから、セキュリティグループとネットワーク ACL を見分けます。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| CloudTrail の再配信 | 最大 30 日 | バケットの設定を直せば届く |
| WAF のログの送信先の名前 | `aws-waf-logs-` で始める | CloudFront の Firehose は `us-east-1` |
| エージェントの既定の名前空間 | `CWAgent` | `AWS/EC2` にはない |
| IMDS のホップ制限 | コンテナでは 2 | IMDSv2 の必須は維持できる |
| KMS キーの関連付けの反映 | 最大 5 分 | 新しく取り込むログが対象 |
| Lambda のログ形式の既定 | plain text | ログレベルは JSON のときだけ効く |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| Lambda のログが出ない | 実行ロールにログの権限があるか |
| ログレベルを変えても効かない | ログ形式が JSON か |
| REST API のログが新しいリージョンで出ない | そのリージョンの `cloudWatchRoleArn` |
| 本番の API で機密データが残る | データトレースを無効にし、実行ログを `ERROR` か `INFO` にする |
| WAF のログの送信先が選べない | 名前の接頭辞とリージョン |
| 標準ログに抜けや遅れがある | ベストエフォートなのでリアルタイムアクセスログを検討 |
| ALB の全ターゲットが異常 | ターゲットの SG で ALB からのヘルスチェックを許可 |
| エージェントのメトリクスが見つからない | 名前空間 `CWAgent` と `fetch-config` |
| 証跡のログが届かない | バケットポリシーと KMS のキーポリシー |
| CSPM のコントロールの結果が出ない | Config とリソースの記録 |
| 一部の EC2 で DNS の検出結果が出ない | AWS のリゾルバーを使っているか |
| アーカイブ済みの検出結果で EventBridge が動かない | 抑制ルール |
| 戻りの通信だけ `REJECT` | ネットワーク ACL |

## 引っかかりやすい点 {#traps}

- API Gateway のログを書くのは呼び出し元ではなく API Gateway です。呼び出し元に権限を足しても直りません。
- 抑制された検出結果は EventBridge にも Security Hub CSPM にも S3 にも送られません。手動でアーカイブした検出結果の動きとは違います。
- GuardDuty は Resolver クエリログの設定とは独立しています。設定を変えても、自前の DNS の分析はできません。
- `associate-kms-key` の失敗はキーポリシーを疑います。過去のログは再暗号化されません。
- セキュリティグループはステートフルです。戻りの `REJECT` をセキュリティグループのせいにしません。
- 新しい Security Hub と CSPM を両方使うと、CSPM がサービスリンクのレコーダーを自動で作ります。CSPM だけなら Config を手動で有効にします。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [monitoring-troubleshooting 問1](../../exercises/monitoring-troubleshooting.md#q1) | 1.3.1 | 新しい Lambda 関数を作成し、最小権限のカスタムの実行ロールを付けました。関数は正常に動いてい… |
| [monitoring-troubleshooting 問2](../../exercises/monitoring-troubleshooting.md#q2) | 1.3.1 | Lambda の本番関数で、費用を抑えるためアプリケーションのログレベルを WARN にしました。し… |
| [monitoring-troubleshooting 問3](../../exercises/monitoring-troubleshooting.md#q3) | 1.3.1 | 東京リージョンの REST API は実行ログが CloudWatch Logs に出ています。同じ… |
| [monitoring-troubleshooting 問4](../../exercises/monitoring-troubleshooting.md#q4) | 1.3.1 | 障害の調査のために、本番の REST API のステージでデータトレースを有効にしました。セキュリテ… |
| [monitoring-troubleshooting 問5](../../exercises/monitoring-troubleshooting.md#q5) | 1.3.1 | CloudFront に関連付けたウェブ ACL のログを、東京リージョンの Firehose wa… |
| [monitoring-troubleshooting 問6](../../exercises/monitoring-troubleshooting.md#q6) | 1.3.1 | CloudFront の標準ログを不正の検知に使っていますが、一部のリクエストの記録が遅れて届き、と… |
| [monitoring-troubleshooting 問7](../../exercises/monitoring-troubleshooting.md#q7) | 1.3.1 | セキュリティの強化でアプリのインスタンスのセキュリティグループを絞ったところ、ALB のターゲットが… |
| [monitoring-troubleshooting 問8](../../exercises/monitoring-troubleshooting.md#q8) | 1.3.2 | CloudWatch エージェントは動作しており、ログにエラーはありません。担当者はメモリの使用率を… |
| [monitoring-troubleshooting 問9](../../exercises/monitoring-troubleshooting.md#q9) | 1.3.2 | EC2 上のコンテナで CloudWatch エージェントを動かすと起動が遅く、ログに Please… |
| [monitoring-troubleshooting 問10](../../exercises/monitoring-troubleshooting.md#q10) | 1.3.2 | 組織の証跡のバケットポリシーを別のチームが書き換えたあと、ログが S3 に届かなくなりました。翌日に… |
| [monitoring-troubleshooting 問11](../../exercises/monitoring-troubleshooting.md#q11) | 1.3.2 | 新しい Security Hub は使わず、Security Hub CSPM だけを有効にしたアカ… |
| [monitoring-troubleshooting 問12](../../exercises/monitoring-troubleshooting.md#q12) | 1.3.2 | GuardDuty を有効にしていますが、一部の EC2 で DNS に関する検出結果が他のインスタ… |
| [monitoring-troubleshooting 問13](../../exercises/monitoring-troubleshooting.md#q13) | 1.3.2 | EventBridge ルールで GuardDuty の検出結果を受けて Lambda を起動してい… |
| [monitoring-troubleshooting 問14](../../exercises/monitoring-troubleshooting.md#q14) | 1.3.2 | 既存のロググループに KMS のカスタマー管理キーを関連付けるため associate-kms-ke… |
| [monitoring-troubleshooting 問15](../../exercises/monitoring-troubleshooting.md#q15) | 1.3.2 | あるインスタンスへの ping が失敗します。VPC フローログには、受信の ACCEPT の記録と… |

<!-- questions:end -->

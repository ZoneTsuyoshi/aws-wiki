# 分野6: 監査とログの設定

記録の範囲と、監査の仕組みそのものの保護を問います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [監査](../../domain6.md#t6-3-audit-services) | セキュリティ監査のサービスと機能、堅牢なセキュリティ監査の実装 |
| [ログの設定](../../domain6.md#t6-3-logging) | サービスとアプリのログの設定 |

## 学習の順番 {#study-order}

1. [CloudTrail の設定](../../../../services/observability.md#cloudtrail): 証跡の設定を確認します。
2. [VPC フローログ](../../../../services/networking.md#flow-logs): 通信の記録を確認します。
3. [ドリフト検出](../../../../services/iac.md#drift): IaC の外の変更を確認します。
4. [ログ](../../../../services/certificates.md#waf-logging): フィールドの編集を確認します。
5. [ロギング戦略](../../../../services/observability.md#logging-strategy): アプリのログの方針を確認します。

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 誰がいつ何をしたか | CloudTrail |
| 通信が許可されたか | VPC フローログ |
| CloudTrail の停止を防ぐ | 組織の証跡と SCP |
| CloudWatch Logs で検索とアラームを使う | 証跡の送信 |

## 引っかかりやすい点 {#traps}

- データイベントは費用がかかるので対象を絞ります。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [security-audit 問7](../../exercises/security-audit.md#q7) | 監査 | 監査で次の問いが出ました。(1) 誰がいつこの操作をしたか。(2) この EC2 への通信は許可され… |
| [security-audit 問8](../../exercises/security-audit.md#q8) | 監査 | 管理者が誤って CloudTrail を止め、監査の空白が生まれました。全アカウントで再発を防ぎ、改… |
| [security-audit 問9](../../exercises/security-audit.md#q9) | 監査 | 監査人の依頼で、EBS の暗号化の基準の準拠を過去 1 年で示します。全アカウントの結果を 1 か所… |
| [security-audit 問10](../../exercises/security-audit.md#q10) | ログの設定 | S3 の機密バケットの GetObject を監査します。全バケットで有効にすると費用が高くなります… |
| [security-audit 問11](../../exercises/security-audit.md#q11) | ログの設定 | インシデントの調査に備えて、ALB、CloudFront、WAF のログを有効にします。WAF が判… |
| [security-audit 問12](../../exercises/security-audit.md#q12) | ログの設定 | EC2 のアプリのログに顧客のメールアドレスが含まれます。組織の基準はアプリのログの集約、機密情報の… |

<!-- questions:end -->

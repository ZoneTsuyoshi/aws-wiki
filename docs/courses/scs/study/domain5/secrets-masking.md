# 分野5: シークレットとマスキング

シークレットの保管先とローテーションの方式、機密データをログやメッセージに残さない方法を問います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [5.3.1](../../domain5.md#skill-5-3-1) | 認証情報とシークレットの管理とローテーション |
| [5.3.4](../../domain5.md#skill-5-3-4) | 機密データのマスキング |

## 学習の順番 {#study-order}

1. [3 つのサービスの比較](../../../../services/secrets.md#comparison): Secrets Manager と Parameter Store を選ぶ基準を覚えます。
2. [ローテーション](../../../../services/secrets.md#rotation)と [Lambda ローテーションの動き](../../../../services/secrets.md#lambda-rotation-steps): マネージドと Lambda の違い、戦略の違いを理解します。
3. [クロスアカウント](../../../../services/secrets.md#secrets-cross-account): 3 つの条件を覚えます。
4. [CloudWatch Logs のデータ保護](../../../../services/secrets.md#cloudwatch-data-protection)と[データ保護ポリシー](../../../../services/observability.md#logs-data-protection): 取り込み時のマスクと `logs:Unmask` を押さえます。
5. [サニタイズとマスキング](../../../../services/secrets.md#sanitization-masking)と[データ分類](../../../../services/secrets.md#data-classification): SNS のポリシーと、Macie の検出の役割を確認します。
6. [フィールドレベル暗号化](../../../../services/networking.md#field-level-encryption)と [WAF のログ](../../../../services/certificates.md#waf-logging): エッジとログの保護を確認します。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| ローテーションの最短 | 4 時間ごと | 間隔を短くしても瞬間の拒否は残る |
| ローテーションの段階 | `createSecret`、`setSecret`、`testSecret`、`finishSecret` | Lambda の方式 |
| フィールドレベル暗号化 | 1 リクエストで最大 10 フィールド | POST の指定のフィールド |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| RDS のマスターユーザーの認証情報を実装なしで自動更新 | マネージドローテーション |
| ローテーションの瞬間も失敗させない | 交代ユーザーと管理者のシークレット |
| 自動ローテーションが不要で費用を抑える | Parameter Store の SecureString |
| 別のアカウントからシークレットを読む | リソースポリシー、IAM、カスタマー管理キー |
| VPC 内のローテーション関数がタイムアウト | Secrets Manager への経路 |
| 過去のログにマスクが効かない | 取り込み時のマスク。過去のログは別に対処 |
| 特定の人だけ元の値を見る | `logs:Unmask` |
| カード番号をエッジで暗号化 | フィールドレベル暗号化 |
| S3 の中の機密データを探す | Macie。検出だけでマスクしない |

## 引っかかりやすい点 {#traps}

- `aws/secretsmanager` はクロスアカウントで使えません。
- アカウント全体のデータ保護ポリシーは、既存と将来のロググループの両方に適用されます。
- SNS のメッセージデータ保護は新規の顧客に提供されません。既存の顧客は使い続けられます。
- SNS の発行は `Inbound`、配信は `Outbound` です。Audit は記録だけです。
- WAF のルールではログの値を消せません。ログのフィールドの編集を使います。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [secrets-masking 問1](../../exercises/secrets-masking.md#q1) | 5.3.1 | RDS for MySQL のマスターユーザーの認証情報を 30 日ごとに自動でローテーションします… |
| [secrets-masking 問2](../../exercises/secrets-masking.md#q2) | 5.3.1 | 24 時間動く決済アプリでは、ローテーションの瞬間にも接続を失敗させられません。データベースにはテー… |
| [secrets-masking 問3](../../exercises/secrets-masking.md#q3) | 5.3.1 | 別のアカウントの Lambda に、自アカウントの Secrets Manager のシークレットを… |
| [secrets-masking 問4](../../exercises/secrets-masking.md#q4) | 5.3.1 | VPC 内のサブネットで動くカスタムのローテーション関数が、createSecret のステップでタ… |
| [secrets-masking 問5](../../exercises/secrets-masking.md#q5) | 5.3.1 | アプリの設定値を保存します。一覧の中で、機能フラグの文字列と API の接続先の URL は暗号化不… |
| [secrets-masking 問6](../../exercises/secrets-masking.md#q6) | 5.3.4 | アプリのログにメールアドレスが出力されていました。CloudWatch Logs のアカウント全体の… |
| [secrets-masking 問7](../../exercises/secrets-masking.md#q7) | 5.3.4 | CloudWatch Logs のデータ保護ポリシーを、セキュリティチームの一部の調査員だけがマスク… |
| [secrets-masking 問8](../../exercises/secrets-masking.md#q8) | 5.3.4 | Web のフォームで入力されたクレジットカード番号を、エッジで暗号化し、オリジンのアプリのログに平文… |
| [secrets-masking 問9](../../exercises/secrets-masking.md#q9) | 5.3.4 | 既存の SNS トピックにメッセージデータ保護を設定しています。組織は発行時に個人情報を含むメッセー… |
| [secrets-masking 問10](../../exercises/secrets-masking.md#q10) | 5.3.4 | WAF のログに Authorization ヘッダーが残っており、監査で指摘されました。また、S3… |

<!-- questions:end -->

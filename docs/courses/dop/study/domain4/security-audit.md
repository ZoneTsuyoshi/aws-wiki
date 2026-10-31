# 分野4: ログの保管と CloudTrail

ログの保護と、記録の範囲を問います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [安全な保管](../../domain4.md#t4-1-secure-storage) | ログの安全な保管と管理 |
| [CloudTrail](../../domain4.md#t4-2-cloudtrail) | CloudTrail のログイベント |

## 学習の順番 {#study-order}

1. [Object Lock](../../../../services/s3.md#object-lock): モードの違いを覚えます。
2. [証跡とイベント履歴](../../../../services/observability.md#cloudtrail-trails): 組織の証跡を確認します。
3. [イベントの種類](../../../../services/observability.md#cloudtrail-events): 3 種類のイベントを押さえます。
4. [CloudTrail Insights](../../../../services/observability.md#cloudtrail-insights): 量の異常の検知を確認します。
5. [Config と CloudTrail の違い](../../../../services/governance.md#config-vs-cloudtrail): 2 つの問いの違いを確認します。

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 7 年間誰にも消させない | コンプライアンスモード |
| 改ざんを検知する | ログファイルの検証 |
| オブジェクトの操作を記録する | 対象を絞ったデータイベント |
| 誰が変更したか | CloudTrail |

## 引っかかりやすい点 {#traps}

- CloudTrail Lake は新規受付を終了しました。90 日より長く残すなら証跡です。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [security-audit 問1](../../exercises/security-audit.md#q1) | 安全な保管 | 組織のログは、ログ保管アカウントの S3 に集めています。規制で、7 年間は誰にも削除や上書きができ… |
| [security-audit 問2](../../exercises/security-audit.md#q2) | 安全な保管 | 監査人は、CloudTrail のログファイルが配信の後に変更されていないことを確かめたいと考えてい… |
| [security-audit 問3](../../exercises/security-audit.md#q3) | 安全な保管 | 中央のログバケットの読み取りを、監査ロールだけに限ります。S3 の管理者であっても、KMS の復号の… |
| [security-audit 問4](../../exercises/security-audit.md#q4) | CloudTrail | S3 の特定のバケットで、誰がどのオブジェクトをダウンロードしたかが必要になりました。既定の証跡には… |
| [security-audit 問5](../../exercises/security-audit.md#q5) | CloudTrail | 次の要件に合う CloudTrail の機能の組み合わせはどれですか。(1) 通常と違う量の Run… |
| [security-audit 問6](../../exercises/security-audit.md#q6) | CloudTrail | 本番のセキュリティグループが昨夜変更され、接続の障害が起きました。(1) 誰が変更したか。(2) 変… |

<!-- questions:end -->

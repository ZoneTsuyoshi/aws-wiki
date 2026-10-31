# 分野1: データ API

データ API の利用と作成、Redshift Data API の非同期の流れを問います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [1.1.4](../../domain1.md#skill-1-1-4) | データ API の利用 |
| [1.2.8](../../domain1.md#skill-1-2-8) | データ API の作成 |

## 学習の順番 {#study-order}

1. [ページネーション](../../../../services/sdk-resilience.md#pagination): 全件をたどる方法を確認します。
2. [バックオフとジッター](../../../../services/sdk-resilience.md#backoff-jitter): 429 への対応を覚えます。
3. [統合タイプ](../../../../services/api-gateway.md#integration-types): タイムアウトと構成を確認します。
4. [Redshift](../../../../services/data-engineering.md#redshift): Data API の使いどころを確認します。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| Data API の結果の保持 | 24 時間 | 必要なら別に保存 |
| Data API の結果のサイズ | 500 MB（gzip 後） |  |
| SQL 文のサイズ | 200 KB |  |
| API Gateway の統合のタイムアウト | 既定 29 秒 | 重いクエリは API を分ける |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 対応 SaaS の定型的な取得 | AppFlow |
| 独自の REST API の定期取得 | EventBridge Scheduler と Lambda |
| 大量のページの取得と変換 | Glue |
| キーで引く低遅延の API | API Gateway、Lambda、DynamoDB |
| 数分かかるレポート | 受付と結果の取得で API を分ける |

## 引っかかりやすい点 {#traps}

- `ExecuteStatement` の戻り値に結果は入りません。
- API キーを環境変数に平文で置きません。Secrets Manager を使います。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [data-apis 問1](../../exercises/data-apis.md#q1) | 1.1.4 | 外部の REST API から全件を読みます。1 回 100 件で、次のページのトークンが返り、時々… |
| [data-apis 問2](../../exercises/data-apis.md#q2) | 1.1.4 | 独自の REST API を 1 時間ごとに読みます。処理は数分で、API キーをコードに書きません… |
| [data-apis 問3](../../exercises/data-apis.md#q3) | 1.1.4 | SaaS の API から数百万ページを取得して変換します。1 回の取得は数時間かかります。実行先は… |
| [data-apis 問4](../../exercises/data-apis.md#q4) | 1.2.8 | 顧客 ID で最新のスコアを数十ミリ秒で返す API を作ります。運用は最小です。どの構成ですか。 |
| [data-apis 問5](../../exercises/data-apis.md#q5) | 1.2.8 | Lambda から Redshift へ、ドライバーと常時接続なしで SQL を送り、結果を返します… |
| [data-apis 問6](../../exercises/data-apis.md#q6) | 1.2.8 | 数分かかる Redshift のレポートを API で提供します。API Gateway の統合のタ… |

<!-- questions:end -->

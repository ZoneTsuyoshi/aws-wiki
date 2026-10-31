# 分野4: DynamoDB

スロットリングの原因の見分け方と、DAX によるキャッシュの動きが問われます。キー設計や API の使い方は[分野1](../domain1/dynamodb.md)で扱います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [4.1.1](../../domain4.md#skill-4-1-1) | エラーコードからの切り分け |
| [4.3.4](../../domain4.md#skill-4-3-4) | DAX によるキャッシュ |
| [4.3.5](../../domain4.md#skill-4-3-5) | 容量不足の検出 |

## 学習の順番 {#study-order}

1. [スロットリング](../../../../services/dynamodb.md#throttling): 原因ごとのエラーと対処を結びつけます。
2. [エラー名の一覧](../../../../services/dynamodb.md#error-names): 再試行してよいエラーと、いけないエラーを分けます。
3. [GSI のキャパシティとバックプレッシャー](../../../../services/dynamodb.md#gsi-backpressure): テーブルに余裕があるのに抑制される理由を理解します。
4. [高カーディナリティのパーティションキー](../../../../services/dynamodb.md#high-cardinality): 特定のキーへの集中を避ける考え方を確認します。
5. [DAX](../../../../services/dynamodb.md#dax): 2 種類のキャッシュと、素通りする操作を覚えます。
6. [DAX の設定](../../../../services/dynamodb.md#dax-settings): TTL の変更方法と、作成後に変えられない設定を確認します。
7. [キャッシュの使い分け](../../../../services/databases.md#cache-comparison): ElastiCache や CloudFront と比べて、DAX を選ぶ場面をつかみます。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| `record-ttl-millis` | 既定 5 分（300,000 ms） | 項目キャッシュの TTL です |
| `query-ttl-millis` | 既定 5 分（300,000 ms） | クエリキャッシュの TTL で、0 ならキャッシュしません |
| DAX のノード数 | 1〜11 | 高可用性には複数の AZ に 3 ノード以上が推奨です |
| DAX のポート | 8111 | セキュリティグループで TCP を許可します |
| GSI の WCU | テーブル以上にする | 不足するとテーブルの書き込みも抑制されます |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 読み取りをコードの変更を抑えてマイクロ秒単位にしたい | DAX クライアントに切り替えます |
| DAX 経由の `Query` が更新後も古い | クエリキャッシュは書き込みで無効化されません。`query-ttl-millis` を短くします |
| DAX で必ず最新の値を読みたい | DAX ではできません。`ConsistentRead=True` は DynamoDB へ転送され、キャッシュされません |
| DAX の TTL を変えたい | `default.dax.1.0` は変更できないので、カスタムのパラメータグループを作ります |
| DAX が `ThrottlingException` を返す | 過負荷です。`ThrottledRequestCount` を監視し、ノードを増やします |
| テーブルに余裕があるのに `ProvisionedThroughputExceededException` になる | GSI の WCU 不足を疑い、テーブル以上にします。`WriteThrottleEvents` と `ThrottledRequests` も監視します |
| 特定のキーだけスロットリングされる | パーティションキーを高カーディナリティにするか、書き込みシャーディングを使います |
| オンデマンドで `ThrottlingException` になる | 最大スループットの設定値を見直します。特定のキーへの集中やクォータの超過でも出るので、`ThrottlingReason` で確かめます |
| `RequestLimitExceeded` が返る | アカウントの上限を超えています。クォータの引き上げを申請します |
| スロットリングの理由を特定したい | 例外の `ThrottlingReason` で理由と対象リソースを確認します |

## 引っかかりやすい点 {#traps}

- **DAX が古い値を返し続ける:** DAX を経由しない更新は検知されません。TTL が切れるまで古い値を返します。
- **作ったはずの項目が見つからない:** 存在しないという結果もキャッシュされます（ネガティブキャッシュ）。
- **DAX のサイズや暗号化を後から変えられない:** ノードタイプは稼働中に変更できず、転送中の暗号化も既存のクラスターでは有効にできません。
- **`TransactWriteItems` で RCU が増える:** DAX 経由だと、キャッシュ更新のために読み取りの RCU を追加で消費します。
- **再試行しても直らない:** `ConditionalCheckFailedException` と `ValidationException` は再試行の対象ではありません。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [dynamodb 問4](../../exercises/dynamodb.md#q4) | 4.1.1 | 開発者が GSI に対して ConsistentRead=True を指定して Query を実行す… |
| [dynamodb 問6](../../exercises/dynamodb.md#q6) | 4.1.1 | プロビジョンドモードのテーブルに 1,000 WCU を設定していますが、毎秒 500 件の書き込み… |
| [dynamodb 問15](../../exercises/dynamodb.md#q15) | 4.3.4 | あるアプリは DAX クライアントで Query と PutItem を実行しています。PutIte… |

<!-- questions:end -->

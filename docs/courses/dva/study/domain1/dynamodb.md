# 分野1: DynamoDB

分野1では、テーブルの設計と、コードからの読み書きを問われます。キー、整合性、Query と Scan、インデックスが中心です。スロットリングの調査や性能の調整は[分野4](../domain4/dynamodb.md)で扱います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [1.1.5](../../domain1.md#skill-1-1-5) | SDK でのバッチとトランザクション |
| [1.1.6](../../domain1.md#skill-1-1-6) | DynamoDB Streams |
| [1.3.1](../../domain1.md#skill-1-3-1) | TTL とバックアップによるデータの管理 |
| [1.3.3](../../domain1.md#skill-1-3-3) | DAX によるキャッシュ |
| [1.3.4](../../domain1.md#skill-1-3-4) | キー、整合性、Query と Scan、インデックス |

## 学習の順番 {#study-order}

1. [キーの設計](../../../../services/dynamodb.md#keys)、[高カーディナリティのパーティションキー](../../../../services/dynamodb.md#high-cardinality): 複合キーの意味と、ホットキーの避け方を理解します。
2. [読み取りの整合性](../../../../services/dynamodb.md#read-consistency): 3 つの読み方と RCU、使える場所を覚えます。
3. [Query と Scan](../../../../services/dynamodb.md#query-vs-scan)、[射影式とフィルター式](../../../../services/dynamodb.md#expressions)、[ページネーション](../../../../services/dynamodb.md#pagination): 消費量が減らない操作と、次のページの取り方を学びます。
4. [LSI と GSI](../../../../services/dynamodb.md#indexes)、[射影とフェッチ](../../../../services/dynamodb.md#projection): 作成時期、整合性、射影外の属性の違いを比べます。
5. [計算方法](../../../../services/dynamodb.md#capacity-calculation)、[オンデマンドの設定と動作](../../../../services/dynamodb.md#on-demand): RCU と WCU を計算できるようにします。
6. [条件付き書き込み](../../../../services/dynamodb.md#conditional-writes)、[アトミックカウンター](../../../../services/dynamodb.md#atomic-counter)、[楽観的ロック](../../../../services/dynamodb.md#optimistic-locking): 同時更新の扱いを学びます。
7. [トランザクション](../../../../services/dynamodb.md#transactions)、[バッチ操作](../../../../services/dynamodb.md#batch): 原子性の有無と未処理分の再送を比べます。
8. [TTL](../../../../services/dynamodb.md#ttl)、[DynamoDB Streams](../../../../services/dynamodb.md#streams)、[DAX](../../../../services/dynamodb.md#dax)、[バックアップと復元](../../../../services/dynamodb.md#backup): 期限切れの削除、変更の検知、キャッシュ、復元を確認します。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| 項目サイズ | 400 KB | 属性名も含みます |
| 1 RCU | 4 KB を強力な整合性で 1 回、結果整合性で 2 回 | サイズは 4 KB の倍数に切り上げます |
| 1 WCU | 1 KB を 1 回 | サイズは 1 KB の倍数に切り上げます |
| トランザクション | 読み書きとも 2 倍、100 アクション、4 MB | |
| 1 パーティションの上限 | 毎秒 3,000 読み込み、1,000 書き込み | テーブルに余裕があっても超えると絞られます |
| GSI、LSI の数 | デフォルト 20 個、5 個 | LSI はテーブル作成時のみです |
| LSI の項目コレクション | 10 GB | |
| Query、Scan の 1 回の読み取り | 1 MB | 続きは `LastEvaluatedKey` です |
| `BatchGetItem`、`BatchWriteItem` | 100 項目、25 件（いずれも 16 MB） | |
| 新しいオンデマンドテーブル | 毎秒 4,000 書き込み、12,000 読み取り | 瞬時に対応できるのは過去のピークの 2 倍までです |
| TTL の属性 | Number 型のエポック秒 | 5 年より古い値は対象外です |
| Streams の保持 | 24 時間 | |
| DAX の TTL | 項目、クエリとも 5 分 | |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 特定のキーでスロットリングする | 高カーディナリティのキーにするか、サフィックスで書き込みシャーディングをします |
| 6 KB の項目を強力な整合性で毎秒 100 件読む | 8 KB に切り上げて 2 RCU × 100 で、200 RCU です。結果整合性なら 100、トランザクションなら 400 です |
| 2.5 KB の項目を毎秒 50 件書く | 3 KB に切り上げて 150 WCU です。トランザクションなら 300 WCU です |
| 書いた直後に最新を読みたい | `ConsistentRead=True` にします。テーブルか LSI でのみ使えます |
| 既存テーブルに別のキーで検索したい | GSI を追加します。LSI は後から追加できません |
| Scan が遅く RCU を消費する | GSI を作って Query にします。全件処理なら並列スキャンで速くできますが、RCU は減りません |
| 同時更新の上書きを防ぎたい | バージョン属性と条件付き書き込みで楽観的ロックにします |
| 閲覧数を増やしたい、多少の誤差は許す | `UpdateItem` のアトミックカウンターにします |
| 複数の項目をすべて成功か全失敗にする | `TransactWriteItems` を使います。再試行は同じ `ClientRequestToken` を 10 分以内に送ります |
| 変更前後の値で処理する | Streams の `NEW_AND_OLD_IMAGES` と Lambda を使います |

## 引っかかりやすい点 {#traps}

- フィルター式と `ProjectionExpression` では RCU は減りません。どちらも読み取る量を変えません。
- `Limit=10` はフィルター前の評価件数です。フィルターと併用すると 10 件未満しか返らないことがあります。
- GSI に `ConsistentRead=True` を指定すると `ValidationException` になります。
- TTL に `Date.now()` のミリ秒をそのまま入れると、期待した時刻に削除されません。削除は通常数日以内なので、読むときはフィルターで除きます。
- `BatchWriteItem` は成功応答でも `UnprocessedItems` が残ることがあります。Update や条件式は使えません。
- PITR で復元したテーブルには Streams や TTL が引き継がれません。DAX のクエリキャッシュは項目の更新では無効化されません。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [dynamodb 問1](../../exercises/dynamodb.md#q1) | 1.3.4 | ある商品カタログのテーブルでは、1 項目の平均サイズが 7 KB です。アプリは GetItem を… |
| [dynamodb 問2](../../exercises/dynamodb.md#q2) | 1.3.4 | 決済処理では、1 項目 2.5 KB の項目を TransactWriteItems で毎秒 20 … |
| [dynamodb 問3](../../exercises/dynamodb.md#q3) | 1.3.4 | 開発者は、配送済みの注文を 1 ページ 10 件で表示するために、Limit=10 と Filter… |
| [dynamodb 問5](../../exercises/dynamodb.md#q5) | 1.3.4 | INCLUDE で total だけを射影した GSI があります。新しい画面で address も… |
| [dynamodb 問7](../../exercises/dynamodb.md#q7) | 1.3.4 | オンデマンドモードのテーブルで、これまでのピークは毎秒 50,000 読み取りです。来週のキャンペー… |
| [dynamodb 問8](../../exercises/dynamodb.md#q8) | 1.3.4 | 開発者が CloudFormation で作ったプロビジョンドモードのテーブルで、負荷が増えても容量… |
| [dynamodb 問9](../../exercises/dynamodb.md#q9) | 1.3.4 | 記事の閲覧数を数える機能があります。閲覧ごとに数を 1 増やし、増やした後の値を画面に表示します。多… |
| [dynamodb 問10](../../exercises/dynamodb.md#q10) | 1.3.4 | 注文の更新に楽観的ロックを実装しています。ConditionExpression="version … |
| [dynamodb 問11](../../exercises/dynamodb.md#q11) | 1.1.5 | 低レベルクライアントで BatchWriteItem を実行すると、HTTP 200 が返りましたが… |
| [dynamodb 問12](../../exercises/dynamodb.md#q12) | 1.1.5 | TransactWriteItems の呼び出しが、ネットワークエラーで応答を受け取れませんでした。… |
| [dynamodb 問13](../../exercises/dynamodb.md#q13) | 1.3.1 | セッションのテーブルで TTL を有効にし、属性 expiresAt に Date.now() の値… |
| [dynamodb 問14](../../exercises/dynamodb.md#q14) | 1.1.6 | 価格が変更されたときだけ、変更前と変更後の価格を通知する Lambda 関数を、DynamoDB S… |
| [dynamodb 問16](../../exercises/dynamodb.md#q16) | 1.3.1 | 誤った更新があったので、PITR で 5 分前の状態を Orders-restored に復元しまし… |
| [dynamodb 問18](../../exercises/dynamodb.md#q18) | 1.3.4 | 東京とバージニアのレプリカを持つ、デフォルト設定のグローバルテーブルで、同じ項目を両方のリージョンか… |
| [dynamodb 問19](../../exercises/dynamodb.md#q19) | 1.3.4 | 開発者は大きなテーブルの全項目を、4 つのワーカーで処理したいと考えています。並列スキャンの設定とし… |

<!-- questions:end -->

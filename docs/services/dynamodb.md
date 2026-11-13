# Amazon DynamoDB

[:material-sprout: CLF](../courses/clf/services.md){ .exam-badge .exam-foundational } [:material-sprout: AIF](../courses/aif/services.md){ .exam-badge .exam-foundational } [:material-certificate: SAA](../courses/saa/services.md){ .exam-badge .exam-associate } [:material-certificate: DVA](../courses/dva/services.md){ .exam-badge .exam-associate } [:material-certificate: SOA](../courses/soa/services.md){ .exam-badge .exam-associate } [:material-certificate: DEA](../courses/dea/services.md){ .exam-badge .exam-associate } [:material-certificate: MLA](../courses/mla/services.md){ .exam-badge .exam-associate } [:material-star-circle: SAP](../courses/sap/services.md){ .exam-badge .exam-professional } [:material-star-circle: DOP](../courses/dop/services.md){ .exam-badge .exam-professional } [:material-star-circle: AIP](../courses/aip/services.md){ .exam-badge .exam-professional }

フルマネージドのキーバリュー型 NoSQL データベースです。アクセスパターンが決まっていて、規模が変わっても一定の低レイテンシで読み書きしたいときに使います。

**提供単位**: テーブルはリージョン単位で VPC の外にあり、AZ は選びません。VPC からはゲートウェイエンドポイントか NAT 経由で呼びます([リソースの提供単位](resource-scope.md#scope-regional-outside))。

[![DynamoDBの読み書きと周辺機能](../assets/diagrams/dynamodb-read-write.png)](../assets/diagrams/dynamodb-read-write.png)

## なぜ DynamoDB はこういう作りなのか {#design-intent}

リレーショナルデータベース（RDB）は、どんな検索でも SQL で書ける代わりに、データが増えると結合や全体の検索が重くなります。1 台のサーバーを大きくするのにも限界があります。

DynamoDB は逆に、「キーで引く」読み書きに絞ることで、データ量やアクセス数が増えても応答の速さを一定に保つ設計です。データはキーで多数のパーティションに分けて置き、パーティションの追加や分割は DynamoDB が裏で自動で行います。各パーティションは、リージョンの複数の AZ に複製されます。

| 困りごと | RDB で起きやすいこと | DynamoDB の答え |
| --- | --- | --- |
| アクセスが 100 倍になった | DB サーバーを大きくするか、手作業でシャーディングする | パーティションを自動で増やす |
| データが増えると遅くなる | 結合やインデックスの検索が重くなる | キーでパーティションを直接引くので、量に左右されにくい |
| DB サーバーの運用が重い | OS、パッチ、冗長化、ディスクの管理 | サーバーがない。テーブルを作るだけ |
| 検索の自由度 | SQL で何でも書ける | キーとインデックスで決めた引き方しか速くない |

最後の行がトレードオフです。DynamoDB では、**先にアクセスパターンを決めてからキーを設計**します。RDB のように後から好きな検索を足すことは得意ではありません。

**オンプレミスとの対比**:

| | 自前の RDB サーバー | DynamoDB |
| --- | --- | --- |
| データの単位 | 表、行、列（スキーマは固定） | テーブル、項目、属性（キー以外は自由） |
| 検索 | SQL、結合 | キーの `GetItem`、`Query`。結合はない |
| 性能の決め方 | サーバーのスペック | 読み書きのユニット（キャパシティモード） |
| 冗長化 | レプリカやクラスタを自分で組む | 複数の AZ に自動で複製 |
| 考え方が近いもの | MySQL、PostgreSQL | Cassandra のような分散データベース。ただしノードの運用は AWS が持つ |

## 使いどころと具体例 {#use-cases}

「何で引くか」が先に決まっていて、件数やアクセス数が大きく変わるデータに向きます。逆に、検索条件が後から増える帳票や分析には向きません。

**使う場面:**

| 場面 | 具体例 | 使う機能 |
| --- | --- | --- |
| 受付開始の瞬間に急増する | 市の給付金のオンライン申請で、受付開始の 9 時に平常の 150 倍の申請が来る | [オンデマンド](#on-demand) |
| キーで 1 件を速く引く | ネットスーパーのカートとログインセッション | [キーの設計](#keys) |
| 時間が経てば要らないデータ | 動画配信の視聴トークンを 6 時間、ワンタイムパスワードを 5 分で消す | [TTL](#ttl) |
| 同じ枠の二重登録を防ぐ | 公共施設の予約で、同じ時間枠を 2 人が同時に押す | [条件付き書き込み](#conditional-writes) |
| 複数の項目を一緒に更新する | 共通ポイントを家族の会員 A から B へ移す | [トランザクション](#transactions) |
| 変更をきっかけに後続を動かす | 宅配の荷物が「配達完了」になったら受取人に通知する | [DynamoDB Streams](#streams) |
| 利用者に自分のデータだけを触らせる | 家計簿アプリのスマホから、自分の明細だけを直接読み書きさせる | [細かいアクセス制御](#fine-grained-access) |
| 複数の国で近くに置く | 日本と北米で遊べる対戦ゲームのプレイヤー情報 | [グローバルテーブル](#global-tables) |
| 同じ項目を大量に読む | セールの目玉商品の詳細を毎秒 5 万回読む | [DAX](#dax) |
| 多数の顧客を 1 つの基盤に載せる | 3,000 社が使う勤怠管理の SaaS | [単一テーブル設計](#single-table)、[細かいアクセス制御](#fine-grained-access) |
| 古いが消せないデータを安く持つ | 2 年分の注文履歴を、月に数回の問い合わせ対応だけで読む | [テーブルクラス](#table-classes) |

**使わない方がよい場面:**

| 場面 | 理由 | 代わりの選択肢 |
| --- | --- | --- |
| 検索条件が後から自由に増える帳票 | キーとインデックスで決めた引き方しか速くない。それ以外は Scan で全件を読む | [RDS、Aurora](databases.md#rds) |
| 伝票、明細、得意先を結合する販売管理 | 結合がない。画面ごとに何度も読むことになる | [RDS、Aurora](databases.md#rds) |
| 商品名のあいまい検索や全文検索 | `contains` の Scan になり、読んだ量だけ課金される | [OpenSearch Service](databases.md#opensearch) |
| 画像や PDF そのものを保存する | 1 項目は 400 KB まで | [S3](s3.md)。項目にはキーだけを持つ |
| つながりを何段もたどる | 段数の分だけ `Query` を繰り返す | [Neptune](databases-specialized.md#neptune) |
| 大量の履歴を SQL で集計する | 集計のたびに全件を読む | S3 と Athena、Redshift（[データエンジニアリング](data-engineering.md)） |

### 例: 市の給付金オンライン申請 {#use-case-municipality}

**状況:** 人口 80 万人の市が、給付金の申請を 2 か月間オンラインで受け付けます。平常は毎秒 10 件ほどですが、受付開始の 9 時から 30 分間は毎秒最大 1,500 件になります。担当は情報政策課の 3 人と委託先で、サーバーの運用はしたくありません。1 世帯 1 回の申請に限ります。

**構成:**

```mermaid
flowchart TD
    U["申請画面"] --> API["API Gateway と Lambda"]
    API -- "条件付き PutItem" --> T["申請テーブル<br/>オンデマンド"]
    T --> S["Streams"]
    S --> L["Lambda"]
    L --> R["審査システム（RDS）"]
    T -. "PITR 35 日" .-> B["復元"]
```

**設定値:**

| 項目 | 値 | 理由 |
| --- | --- | --- |
| キャパシティモード | オンデマンド | 受付開始の急増と、その後の平常時の差が大きい。新しいテーブルでも毎秒 4,000 書き込みまで受けられる |
| `MaxWriteRequestUnits` | 3,000 | 想定ピークの 2 倍。不正なツールの大量送信で費用が膨らむのを止める |
| キー | `PK = HOUSEHOLD#<世帯番号のハッシュ>`、`SK = APPLICATION` | 世帯の番号をそのままキーに入れない。値の種類が多いので書き込みが散らばる |
| 書き込みの条件 | `attribute_not_exists(PK)` | 同じ世帯の 2 回目の申請を `ConditionalCheckFailedException` で断る |
| PITR | `RecoveryPeriodInDays=35` | 審査中の誤操作に備える。期間を延ばしても費用は変わらない |
| Streams | `NEW_IMAGE` | 申請の内容を審査システムへ渡す |

**なぜこのサービスか:** 審査システムの RDS に直接受けると、受付開始の 30 分のために大きなインスタンスを 2 か月借りることになります。申請の受付は「世帯で 1 件を書く」だけなので、DynamoDB で受け、審査に必要な結合や帳票は RDS 側で行います。

**つまずきやすい点:**

- 審査画面のために `status` をキーにした GSI を作ると、値が 3 種類しかないので 1 つのキーに書き込みが集中します。GSI の不足で申請の書き込みまで止まります（[GSI のバックプレッシャー](#gsi-backpressure)）。状態別の一覧は審査システム側で作ります。
- `MaxWriteRequestUnits` を平常時の値に合わせて低くすると、9 時の正常な申請が `ThrottlingException` になります。
- Streams を読む Lambda が 24 時間以上失敗し続けると、その間の申請が審査システムへ届きません。失敗をアラームで知らせます。

### 例: ネットスーパーのカートとセッション {#use-case-netsuper}

**状況:** 会員 50 万人のネットスーパーです。注文は夕方 17〜19 時に集中し、カートの読み取りが毎秒 2,000 件、書き込みが毎秒 800 件になります。1 つのカートは 2 KB ほどで、夜間はその 1 割以下です。カートは 30 日、ログインセッションは 1 時間で消します。

**構成:**

| データ | キー | 期限 |
| --- | --- | --- |
| カート | `PK = MEMBER#<会員 ID>`、`SK = CART` | 最後の更新から 30 日 |
| セッション | `PK = SESSION#<ランダムな ID>` | 1 時間 |

**設定値:**

| 項目 | 値 | 理由 |
| --- | --- | --- |
| キャパシティモード | プロビジョンドと Auto Scaling | 毎日ほぼ同じ時間帯に、なだらかに増える |
| 読み取りの容量 | 最小 100、最大 2,000 RCU | 2 KB の結果整合性は 0.5 RCU なので、毎秒 2,000 件で 1,000 RCU。目標使用率 70% で約 1,430 RCU になり、余裕を持たせる |
| 書き込みの容量 | 最小 200、最大 3,000 WCU | 2 KB の書き込みは 2 WCU なので、毎秒 800 件で 1,600 WCU。70% なら約 2,290 WCU |
| TTL | `expiresAt` に現在時刻 + 2,592,000 秒（カート）、+ 3,600 秒（セッション） | 削除のバッチを書かずに済み、TTL の削除は WCU を消費しない |
| 追加の条件 | `size(#i) < :max`、`:max=100` | カートに 100 品目までしか入らないようにする |

**なぜこのサービスか:** カートは会員 ID で 1 件を読むだけで、結合が要りません。ElastiCache に置くと速いものの、ノードの障害でカートが消えます。DynamoDB なら複数の AZ に保存され、期限切れの削除も TTL に任せられます。

**つまずきやすい点:**

- `expiresAt` にミリ秒を入れると、遠い未来の時刻として扱われ、カートが消えずにストレージが増え続けます。
- Auto Scaling は消費が 2 分続けて目標を超えてから動きます。チラシの公開時刻に一斉に人が来ると、間に合わずスロットリングします。公開時刻が決まっているなら、事前に最小値を上げます。
- GSI を足したら、GSI にも同じ Auto Scaling を設定します。忘れると、GSI の不足でカートの書き込みが止まります。

### 例: 宅配の荷物追跡 {#use-case-delivery}

**状況:** 1 日 30 万個の荷物を扱う地域の宅配会社です。ドライバー 1,500 人がスマホのアプリで集荷、輸送中、配達完了を記録します。1 個あたり平均 5 件の記録で、昼前と夕方に毎秒 100 件ほどになります。配達完了の時点で受取人にメールで知らせます。追跡情報は 90 日で消して構いません。

**構成:**

```mermaid
flowchart TD
    A["ドライバーのアプリ"] -- "記録を追加" --> T["荷物テーブル"]
    T -- "GSI: ドライバーと日付" --> G["当日の担当一覧"]
    T --> S["Streams<br/>NEW_AND_OLD_IMAGES"]
    S --> L["Lambda"]
    L -- "配達完了に変わったときだけ" --> N["受取人へメール"]
    W["追跡ページ"] -- "Query: 伝票番号" --> T
```

**設定値:**

| 項目 | 値 | 理由 |
| --- | --- | --- |
| テーブルのキー | `PK = PARCEL#<伝票番号>`、`SK = EVENT#<時刻>` | 1 回の `Query` で荷物の経過が時刻順に返る |
| GSI のキー | `PK = DRIVER#<ID>#2026-11-13`、`SK = <配達順>` | ドライバーの当日の一覧を Scan せずに読む。日付を含めて 1 キーの量を抑える |
| `StreamViewType` | `NEW_AND_OLD_IMAGES` | 変更前が「配達完了」でなく、変更後が「配達完了」のときだけ通知する |
| TTL | 現在時刻 + 7,776,000 秒（90 日） | 問い合わせの期間を過ぎた記録を自動で消す |
| キャパシティモード | オンデマンド | 年末や大型セールの時期に件数が大きく変わる |

**なぜこのサービスか:** 読み方が「伝票番号で経過を見る」「ドライバーの当日の一覧を見る」の 2 つに決まっています。どちらもキーと GSI で `Query` 1 回になります。通知を Streams に任せると、ドライバーのアプリは記録を書くだけで済みます。

**つまずきやすい点:**

- 通知、集計、検索への同期の 3 つの Lambda を同じストリームにつなぐと、1 シャードを読むのは 2 プロセスまでという目安を超え、読み取りが詰まります。1 つの関数で受けて、EventBridge や SNS へ広げます。
- `KEYS_ONLY` にすると、Lambda が項目を読み直す時点で次の記録が入っていて、通知の判断を誤ることがあります。
- 通知の Lambda が失敗し続けると、24 時間を超えたレコードは失われ、その日の通知が抜けます。

### 例: 共通ポイントの利用と移動 {#use-case-points}

**状況:** 会員 300 万人、加盟店 1 万店の共通ポイントです。加盟店の端末からポイントを使うと、残高を減らし、利用の履歴を残します。家族の会員の間でポイントを移すこともできます。キャンペーンの日は毎秒 1,500 件の利用があり、残高の誤差は許されません。

**構成:**

| 操作 | 1 回のトランザクションに入れるもの |
| --- | --- |
| ポイントの利用 | 残高の `Update`（条件: 残高 ≥ 利用額）、履歴の `Put`（条件: 同じ取引番号がない） |
| 家族への移動 | 送る側の残高の `Update`（条件: 残高 ≥ 移す量）、受ける側の残高の `Update`、履歴の `Put` |
| 確認画面の表示 | 2 人の残高を `TransactGetItems` で読む |

**設定値:**

| 項目 | 値 | 理由 |
| --- | --- | --- |
| `ClientRequestToken` | 端末の取引番号（36 文字以内） | 通信の切断で端末が再送しても、10 分以内なら 1 回だけ反映される |
| 利用の容量 | 毎秒 1,500 件 × 2 項目 × 1 KB × 2 倍 = 6,000 WCU | トランザクションは通常の 2 倍を消費する |
| 確認画面の読み取り | `TransactGetItems` | `BatchGetItem` では、移動の途中で片方だけ更新後の値が見えることがある |
| PITR | 35 日 | 不具合で残高を誤って書き換えたときに戻す |

**なぜこのサービスか:** キャンペーンの日だけ毎秒の件数が大きく増え、読み書きは会員 ID で決まります。RDS ではピークに合わせた大きさのインスタンスと、端末からの接続数の管理が要ります。月次の集計や監査の SQL は、Streams で分析の基盤へ流して行います。

**つまずきやすい点:**

- 残高を `ADD` のアトミックカウンターで減らすと、再試行で二重に引かれることがあります。残高は条件付きのトランザクションで書きます（[アトミックカウンター](#atomic-counter)）。
- 端末が 10 分を過ぎてから同じ取引番号で再送すると、新しいリクエストとして二重に処理されます。履歴の `Put` の `attribute_not_exists` が最後の防波堤になります。
- 社員の利用をまとめる法人会員のように、1 つの残高の項目に多くの端末から同時に書くと `TransactionConflictException` が増えます。

### 例: 日本と北米の対戦ゲーム {#use-case-game}

**状況:** 日本と北米で遊べる対戦ゲームで、プレイヤーは 200 万人です。プレイヤー情報（名前、レベル、所持コイン）を、どちらの地域からも 1 桁ミリ秒で読み、片方のリージョンが使えなくなっても遊べるようにします。

**構成:** 東京とバージニア北部に、グローバルテーブルのレプリカを置きます（[グローバルテーブル](#global-tables)の図）。

**設定値:**

| 項目 | 値 | 理由 |
| --- | --- | --- |
| モード | MREC | 書き込みの応答を速くする。MRSC は書き込みごとに別リージョンと同期する分だけ遅くなる |
| 書き込むリージョン | プレイヤーの「ホーム」の地域だけ | 同じ項目を 2 か所で書かないので、最後の書き込みが優先されても更新が消えない |
| 読み取り | 近いリージョンのレプリカ | 対戦相手の情報は少し古くても困らない |
| TTL | 対戦の一時データにだけ付ける | TTL の削除は他のリージョンへの複製分の書き込みとして課金される |

**なぜこのサービスか:** Aurora のグローバルデータベースは書き込みがプライマリのリージョンだけなので、北米のプレイヤーの書き込みは太平洋を越えます。グローバルテーブルならどちらのレプリカにも書けます。

**つまずきやすい点:**

- 日本のイベントと北米のショップが、同じプレイヤーの所持コインを同時に `SET` すると、片方の加算が消えます。コインのように両方を反映したい値は、ホームのリージョンだけで書きます。
- トランザクションで「コインを減らしてアイテムを足す」を書いても、もう一方のリージョンでは片方だけ先に見えることがあります。
- Streams を読む関数は、グローバルテーブルでは 1 シャード 1 つが推奨です。集計の関数を増やすときは 1 つの関数から広げます。

### 例: 勤怠管理 SaaS のテナント分離 {#use-case-saas}

**状況:** 3,000 社が使う勤怠管理の SaaS です。社員は合計 40 万人で、最大の顧客は 2 万人の会社です。朝 8 時 50 分から 9 時に打刻が集中します。開発は 6 人で、テナントの取り違えは契約上の重大事故になります。

**構成:** すべてのテナントを 1 つのテーブルに入れるプールモデルです（[マルチテナントのデータアクセス](databases.md#multi-tenant)）。

| `PK` | `SK` | 内容 |
| --- | --- | --- |
| `TENANT#123` | `EMP#456#2026-11-13` | 社員 456 のその日の打刻 |
| `TENANT#123` | `SETTING` | 会社ごとの就業規則 |

**設定値:**

| 項目 | 値 | 理由 |
| --- | --- | --- |
| IAM の条件 | `dynamodb:LeadingKeys` を `TENANT#${aws:PrincipalTag/tenant}` に限る | アプリのコードを誤っても、他社のキーは `AccessDeniedException` になる |
| 許可する操作 | `GetItem`、`Query`、`PutItem`、`UpdateItem` | `Scan` は `LeadingKeys` に関係なく全件を返すので許可しない |
| キャパシティモード | オンデマンド | 打刻の 10 分間とそれ以外の差が大きい |

**なぜこのサービスか:** テナントごとにテーブルを作ると、3,000 個のテーブルの設定とアラームを管理することになります。1 つのテーブルで、パーティションキーの先頭とロールのタグで分ければ、分離を IAM で強制できます。

**つまずきやすい点:**

- 最大の顧客の 2 万人が 10 分で打刻すると、1 つのパーティションキーに毎秒約 33 件です。上限の 1,000 WCU には遠いものの、10 万人規模の顧客が入ったらキーにサフィックスを付けて分けます（[高カーディナリティのパーティションキー](#high-cardinality)）。
- 運用の調査用に `Scan` を許可したロールをアプリにも使い回すと、全社のデータが読めてしまいます。
- 1 社の一括取り込みが容量を使うと、他社の打刻が遅くなります。取り込みの速さを API 側でテナントごとに制限します。

## キーの設計 {#keys}

テーブルの主キーは次の 2 種類です。テーブル作成後に変更できないので、最初にアクセスパターンから決めます。

| 種類 | 構成 | 特徴 |
| --- | --- | --- |
| シンプル | パーティションキーのみ | キーの値で項目を 1 つ特定する |
| 複合 | パーティションキー + ソートキー | 同じパーティションキーの項目がソートキー順に並び、範囲検索できる |

キー属性に使える型は文字列 (S)、数値 (N)、バイナリ (B) だけです。サイズ上限はパーティションキーが 2,048 バイト、ソートキーが 1,024 バイトです。

**例**:

- **シンプル**: セッションを `sessionId` だけで引くなら、`GetItem` で 1 件を取るだけなのでパーティションキーのみで足ります。
- **複合**: 顧客の注文を期間で引くなら、`customerId` と `orderedAt` にします。`customerId = C-42 AND orderedAt BETWEEN 2026-10-01 AND 2026-10-31` のように 1 回の `Query` で読めます。
- **長さ**: 3,000 バイトの URL をそのままパーティションキーにすると、2,048 バイトを超えて `ValidationException` になります。SHA-256 の 16 進表記(64 文字)をキーにして、URL は別の属性に入れます。

**誤ると**: シンプルなキーで作った後に「顧客ごとの一覧」が必要になっても、キーは変更できません。GSI を足すか、新しいテーブルへ移行します。

### 高カーディナリティのパーティションキー {#high-cardinality}

パーティションキーの値はハッシュされ、データの配置先が決まります。1 パーティションの上限は 1 秒あたり 3,000 読み込みユニットと 1,000 書き込みユニットです。テーブル全体に余裕があっても、特定のキーにアクセスが集中するとスロットリングが起きます。

```mermaid
flowchart TD
    I["項目 userId = U-42"] --> H["ハッシュ関数"]
    H --> P1["パーティション 1"]
    H -.-> P2["パーティション 2"]
    H -.-> P3["パーティション 3"]
    Q["Query: userId = U-42"] --> H2["同じハッシュ関数"] --> P1
```

**スーパーのレジにたとえる**と、パーティションはレジ、パーティションキーは「どのレジに並ぶか」を決める札です。レジが 10 台あっても、全員が同じ札を持っていれば 1 台に行列ができます。札の種類が多い（高カーディナリティ）ほど、客は自然に散らばります。

ハッシュで散らすのは、どのキーの項目も計算 1 回で置き場所が分かり、データが何億件でも探す手間が増えないようにするためです。その代わり、ハッシュの順序には意味がないので、パーティションキーをまたいだ並べ替えや範囲検索はできません。

値の種類が多く、アクセスが均等に分散するキーを選びます。

| 良い例 | 避けたい例 | 理由 |
| --- | --- | --- |
| `userId`、`orderId`、`deviceId` | `status`、`gender` | 値の種類が少ないと、同じキーに書き込みが集中する |
| `date#3`(サフィックスで分散) | `date` | 当日分にだけ書き込みが集まるホットキーになる |

時系列データのように偏りを避けられない場合は、キーに乱数や計算したサフィックスを付けて分散させます。これを書き込みシャーディングと呼びます。

**計算の例**: 1 KB 以下のイベントを毎秒 5,000 件書き、キーを `2026-10-31` だけにすると、1 パーティションの上限 1,000 WCU の 5 倍が集中します。サフィックスを 0〜9 の 10 種類にすると、5,000 ÷ 10 で 1 キーあたり 500 WCU に収まります。

```python
import zlib

# 同じ order_id は常に同じサフィックスになるので、後から 1 件を引ける
suffix = zlib.crc32(order_id.encode()) % 10
item = {"PK": f"2026-10-31#{suffix}", "SK": order_id}
```

**代償**: その日の全件を読むには、`#0` から `#9` まで 10 回 `Query` します。

**誤ると**: テーブル全体の `ConsumedWriteCapacityUnits` には余裕があるのに、スロットリングが続きます。`status` のように値が 3 種類のキーでは、容量を増やしても解消しません。

### 属性とデータ型 {#attributes}

キー以外の属性はスキーマレスで、項目ごとに違っていても構いません。項目の最大サイズは 400 KB です。

| 区分 | 型 |
| --- | --- |
| スカラー | String、Number、Binary、Boolean、Null |
| ドキュメント | List、Map |
| セット | String Set、Number Set、Binary Set |

型には次の細かい決まりがあります。

| 項目 | 内容 |
| --- | --- |
| Number の精度 | 最大 38 桁。超えると例外になるので、それ以上は文字列で持つ |
| ネスト | List と Map は 32 階層まで |
| 空の値 | 空の String と Binary はキー以外なら可。空のセットは不可。空の List と Map は可 |
| セット | 要素は同じ型で一意。順序は保たれない |

**例**:

- **Number の精度**: 38 桁の整数は保存できますが、39 桁は例外になります。40 桁の識別子は String で持ちます。
- **ネスト**: `order.items[0].options.color` は 4 階層です。33 階層のドキュメントは書き込めません。
- **空の値**: `{"memo": ""}` と `{"tags": []}` は保存できます。`{"colors": set()}` のような空のセットは例外になり、キー属性を空文字列にしても例外になります。
- **セット**: `{"red", "red"}` は重複で拒否されます。`{"red", 1}` のように型を混ぜることもできません。順序を残したいなら List を使います。

### 項目サイズの数え方 {#item-size}

項目のサイズは、属性名と値の長さの合計です。1 KB は 1,024 バイトで数えます。

| 型 | サイズ |
| --- | --- |
| String | 属性名の UTF-8 バイト数 + 値の UTF-8 バイト数 |
| Number | 属性名 + 有効桁 2 桁につき約 1 バイト + 1 バイト |
| Binary | 属性名 + 元のバイト数(base64 後の長さではない) |
| Boolean、Null | 属性名 + 1 バイト |
| List、Map | 属性名 + 要素の合計 + 3 バイト |
| セット | 属性名 + 要素の合計 |

**例**: `customerEmailAddressVerified` という 28 バイトの属性名を `cev` に変えると、1 項目あたり 25 バイト減ります。1,010 バイトの項目に 28 バイトの属性名の Boolean を足すと 1,039 バイトになり、1 回の書き込みは 1 WCU から 2 WCU に増えます。

**計算の例**: `{"orderId": "A-1001", "total": 1980, "paid": true}` は次の合計で約 26 バイトです。

| 属性 | 計算 | バイト |
| --- | --- | --- |
| `orderId` | 属性名 7 + 値 6 | 13 |
| `total` | 属性名 5 + 有効桁 3 桁(末尾の 0 は数えない)で 2 + 1 | 8 |
| `paid` | 属性名 4 + 1 | 5 |

**落とし穴**: 属性名はすべての項目で繰り返し保存され、400 KB の上限にも数えられます。上限を超える書き込みは拒否されます。大きなデータは S3 に置き、項目にはキーだけを持たせます。

### 単一テーブル設計の基本 {#single-table}

関連するエンティティを 1 つのテーブルに入れ、`Query` 1 回でまとめて取得する設計です。開発者として押さえるのは次の点です。

DynamoDB には結合がないので、RDB のように表を分けると、画面 1 つに何度も読み取りが要ります。「一緒に読むものを、一緒に置く」のが単一テーブル設計の考え方です。RDB の正規化が「重複をなくす」ことを優先するのに対し、こちらは「読む回数を減らす」ことを優先します。

- `PK` と `SK` のような汎用名のキーを使い、`USER#42`、`ORDER#2026-10-31` のような接頭辞で種類を区別します。
- 先にアクセスパターンを洗い出し、それに合わせてキーと GSI を決めます。
- 結合がないため、まとめて読みたいデータは同じパーティションキーに置きます。

**例**: ユーザーと注文を同じテーブルに入れます。

| `PK` | `SK` | 内容 |
| --- | --- | --- |
| `USER#42` | `PROFILE` | 氏名、メール |
| `USER#42` | `ORDER#2026-10-30#A-1001` | 注文 1 |
| `USER#42` | `ORDER#2026-10-31#A-1002` | 注文 2 |

`PK = USER#42` だけで `Query` すると、プロフィールと注文が 1 回で返ります。`begins_with(SK, "ORDER#")` を足すと注文だけになり、`ScanIndexForward=False` で新しい順に並びます。

**誤ると**: 接頭辞を付けずに `SK` へ日付だけを入れると、プロフィールと注文をキーで区別できず、`FilterExpression` に頼ることになります。読んだ分の RCU は減りません。

## 読み取りの整合性 {#read-consistency}

| モデル | 指定 | 消費 RCU | 使える場所 |
| --- | --- | --- | --- |
| 結果整合性 | デフォルト | 4 KB あたり 0.5 | テーブル、LSI、GSI、Streams |
| 強力な整合性 | `ConsistentRead=True` | 4 KB あたり 1 | テーブル、LSI のみ |
| トランザクション | `TransactGetItems` | 4 KB あたり 2 | テーブル |

結果整合性の読み取りは、直前の書き込みを反映していない可能性があります。書いた直後に必ず最新を読みたいときだけ強力な整合性を選びます。

整合性を選べるのは、データを複数の AZ に複製しているためです。複製に更新が届くまでの短い間を許せば、半分のユニットで読めます。許せない読み取りだけ、最新を保証する読み方を選び、2 倍のユニットを払います。すべての読み取りに最新を保証しない設計なので、大半を占める「少し古くてもよい読み取り」を安くできます。

| | 結果整合性 | 強力な整合性 |
| --- | --- | --- |
| たとえ | 各支店に配った掲示板を見る。本社の変更が少し遅れて届く | 本社に電話して最新を聞く |
| 費用 | 半分 | 2 倍 |
| 向く場面 | 一覧、ランキング、プロフィールの表示 | 注文の確定直後の画面、残高の確認 |

!!! warning "GSI は強力な整合性を使えない"
    GSI に `ConsistentRead=True` を指定することはできません。指定すると `ValidationException` になります。最新の値が必須ならテーブルか LSI を読みます。

### ConsistentRead の指定 {#consistent-read}

`GetItem`、`Query`、`Scan` に指定します。デフォルトは `false`(結果整合性)です。`BatchGetItem` はテーブルごとに指定します。

**例**: 注文を確定した直後に、同じ人が画面で注文を読むなら `ConsistentRead=True` にします。4 KB 以下の項目を毎秒 100 件読むと、消費は 50 RCU から 100 RCU に倍増します。必要な画面だけに絞ります。

**3 つの読み方の比較**: 4 KB 以下の項目を 10 件読むと、結果整合性は 5 RCU、強力な整合性は 10 RCU、`TransactGetItems` は 20 RCU です。

`BatchGetItem` では、テーブルごとに指定します。

```python
client.batch_get_item(RequestItems={
    "Orders": {"Keys": keys, "ConsistentRead": True},
    "Products": {"Keys": product_keys},  # こちらは結果整合性のまま
})
```

**誤ると**: 既定のまま「書いた直後の読み取り」をすると、更新前の値を画面に出すことがあります。逆に全画面で `ConsistentRead=True` にすると、読み取りの費用が 2 倍になります。

**落とし穴**: 存在しない項目を読んでも RCU は消費されます。

## Query と Scan {#query-vs-scan}

| 観点 | Query | Scan |
| --- | --- | --- |
| 対象 | 1 つのパーティションキーの値 | テーブルまたはインデックス全体 |
| 必須の指定 | パーティションキーの等価条件 | なし |
| 順序 | ソートキー順(`ScanIndexForward=False` で降順) | パーティション間は順不同 |
| 消費 | 読んだ分のみで効率的 | 全項目を評価するため大きい |

Scan は大きなテーブルでは遅く、高コストです。定常的なアクセスには、GSI を作って Query に置き換えます。

**図書館にたとえる**と、Query は請求記号で棚を直接探すこと、Scan は全部の棚を端から見ることです。Scan の料金は、見つかった件数ではなく見た量で決まります。

```mermaid
flowchart TD
    A["読みたいもの"] --> B{"1 件で、キーが全部分かる?"}
    B -- "はい" --> G["GetItem"]
    B -- "いいえ" --> C{"パーティションキーの値が分かる?"}
    C -- "はい" --> Q["Query（テーブル）"]
    C -- "いいえ" --> D{"別の属性で引く?"}
    D -- "はい、定常的に" --> I["GSI を作って Query"]
    D -- "いいえ: 全件の集計や移行" --> S["Scan（並列スキャン）"]
```

### Query のパラメータ {#query-params}

| パラメータ | 値とデフォルト | 動作 | 落とし穴 |
| --- | --- | --- | --- |
| `KeyConditionExpression` | パーティションキーの等価条件は必須 | ソートキーには `=`、`<`、`<=`、`>`、`>=`、`BETWEEN`、`begins_with` が使える | キー以外の属性は書けない。Number のソートキーに `begins_with` は使えない |
| `FilterExpression` | 省略可 | 読んだ後、返す前に絞る | キー属性は書けない。RCU は減らない |
| `ProjectionExpression` | 省略可 | 返す属性を絞る | RCU は減らない。1 MB の計算にも影響しない |
| `Limit` | 1 以上 | 評価する項目の最大数 | 一致する件数の上限ではない |
| `ExclusiveStartKey` | 省略可 | 前回の `LastEvaluatedKey` を渡す | 自分で組み立てず、応答の値をそのまま渡す |
| `ScanIndexForward` | デフォルト `true`(昇順) | `false` で降順 | Query 専用。Scan にはない |
| `ConsistentRead` | デフォルト `false` | 強力な整合性で読む | GSI では `ValidationException` |
| `ReturnConsumedCapacity` | `NONE`(デフォルト)、`TOTAL`、`INDEXES` | 消費した RCU を応答に含める | `INDEXES` でインデックスごとの内訳が出る |
| `Select` | 下の表を参照 | 返す内容を選ぶ | `COUNT` でも読んだ分の RCU を消費する |
| `IndexName` | 省略可 | テーブルの代わりにインデックスを読む | キー条件はインデックスのキーで書く |

`Select` の値は次の 4 つです。

| 値 | 返すもの | 補足 |
| --- | --- | --- |
| `ALL_ATTRIBUTES` | 項目の全属性 | テーブルのデフォルト。LSI では親テーブルから取得することがある |
| `ALL_PROJECTED_ATTRIBUTES` | 射影された属性 | インデックスのデフォルト。インデックス専用 |
| `SPECIFIC_ATTRIBUTES` | `ProjectionExpression` で指定した属性 | `ProjectionExpression` と併用できる唯一の値 |
| `COUNT` | 件数のみ | 項目を返すときと同じ量の RCU を消費する |

**例**: 1 人のユーザーの注文から、最新の配送済みを 10 件取りたいとします。

```python
from boto3.dynamodb.conditions import Attr, Key

resp = table.query(
    KeyConditionExpression=Key("PK").eq("USER#42") & Key("SK").begins_with("ORDER#"),
    FilterExpression=Attr("status").eq("SHIPPED"),
    ScanIndexForward=False,
    Limit=10,
    ReturnConsumedCapacity="TOTAL",
)
```

`Limit=10` はフィルター前の 10 件を意味します。その中に配送済みが 3 件しかなければ、`Items` は 3 件で、`LastEvaluatedKey` が付いて返ります。10 件そろうまでページを読み進めるか、配送済みだけをスパースインデックスに入れます。

パラメータごとの値の例です。

- **`KeyConditionExpression`**: `PK = :u AND SK BETWEEN :from AND :to` に `:from=ORDER#2026-10-01`、`:to=ORDER#2026-10-31` を渡します。**誤ると**: `status = :s` のようにキー以外を書くと `ValidationException` です。
- **`FilterExpression`**: 1 KB の項目を 100 件読んで 3 件に絞っても、100 KB ÷ 4 KB × 0.5 で 12.5 RCU のままです。
- **`ProjectionExpression`**: `"orderId, #t"`(`total` は予約語なので `#t` に置き換える)で 2 属性に絞っても、30 KB の項目を強力な整合性で読めば 32 KB ÷ 4 KB で 8 RCU です。減るのは転送量だけです。
- **`ExclusiveStartKey`**: 応答の `{"PK": "USER#42", "SK": "ORDER#2026-09-30#A-0900"}` をそのまま渡します。**誤ると**: 値を組み立て間違えると、続きと違う位置から読みます。
- **`ScanIndexForward`**: 省略すると古い順なので、`Limit=1` では最古の 1 件が返ります。最新の 1 件には `False` を指定します。
- **`ReturnConsumedCapacity`**: `TOTAL` なら応答に `{"TableName": "Orders", "CapacityUnits": 12.5}` が付きます。`INDEXES` なら GSI や LSI ごとの内訳も付きます。既定の `NONE` では何も付きません。
- **`Select`**: `COUNT` で 1 KB の項目 200 件を数えると、200 KB ÷ 4 KB × 0.5 で 25 RCU です。項目を返さなくても同じ消費です。**誤ると**: `ALL_ATTRIBUTES` と `ProjectionExpression` を併用すると `ValidationException` です。
- **`IndexName`**: `IndexName="status-index"` と `Key("status").eq("PENDING")` を組み合わせます。**誤ると**: テーブルの `PK` で条件を書くと、インデックスのキーと合わず `ValidationException` です。

### 並列スキャン {#parallel-scan}

通常の Scan は順番に処理するため、大きなテーブルでは時間がかかります。並列スキャンは複数のワーカーがそれぞれ次のパラメータを指定して Scan します。

**使う場面:** 会員 300 万件のテーブルを新しいキー設計のテーブルへ移すとき、夜間に 8 つのワーカーで分担して全件を読みます。

- `TotalSegments`: 全体のセグメント数(ワーカー数と同じ値)
- `Segment`: そのワーカーが担当する番号(0 始まり)

```python
import boto3

# このページの例の table はこのリソースを指す
table = boto3.resource("dynamodb").Table("Orders")
resp = table.scan(Segment=worker_no, TotalSegments=4, Limit=100)
```

プロビジョンドスループットを使い切りやすいので、本番トラフィックがあるときは `Limit` で 1 リクエストの量を抑えます。セグメントはパーティションキーのハッシュで決まるため偏ることがあり、セグメントを増やしても速くなるとは限りません。

| パラメータ | 範囲 | 注意 |
| --- | --- | --- |
| `TotalSegments` | 1〜1,000,000 | 1 なら順次スキャンと同じ |
| `Segment` | 0 以上、`TotalSegments` 未満 | 片方だけの指定はできない |

**例**: 4 つのワーカーなら `TotalSegments=4` で、`Segment` は 0、1、2、3 です。

**計算の例**: 1 回の Scan が上限の 1 MB を読むと、1,024 KB ÷ 4 KB × 0.5 で 128 RCU です。4 ワーカーが同時に読めば 512 RCU になり、500 RCU のテーブルでは超えます。1 KB の項目で `Limit=100` にすると、1 回は 100 KB ÷ 4 KB × 0.5 で 12.5 RCU に下がります。

**誤ると**: `Segment=4` と `TotalSegments=4` の組み合わせは `ValidationException` です。番号は 3 までです。

**Scan の RCU の例**: 1 KB の項目を 1,000 件評価する場合、合計 1,000 KB を 4 KB で割って 250 とし、結果整合性なので半分の 125 RCU です。`FilterExpression` で 1 件に絞っても 125 RCU のままです。Scan も強力な整合性を指定できます(GSI を除く)。その場合は 250 RCU です。

### 射影式とフィルター式 {#expressions}

| 式 | 役割 | 消費 RCU への影響 |
| --- | --- | --- |
| `KeyConditionExpression` | Query で読む範囲をキーで絞る | 読む量が減るので下がる |
| `FilterExpression` | 読んだ後に結果を絞る | 変わらない |
| `ProjectionExpression` | 返す属性を絞る | 変わらない |
| `ConditionExpression` | 書き込みの実行条件 | 不成立でも WCU を消費する |

!!! tip "フィルターは節約にならない"
    1 MB の上限と `Limit` は、フィルターを適用する前の読み取り量に対して働きます。そのため `FilterExpression` を付けると、結果が 0 件なのに `LastEvaluatedKey` が返るページが発生します。

予約語と同じ名前の属性は `ExpressionAttributeNames` で置き換えます(`#s` に `status` を割り当てるなど)。値は `ExpressionAttributeValues` で渡します(`:v` など)。

```python
table.query(
    KeyConditionExpression="PK = :u",
    FilterExpression="#s = :v",
    ExpressionAttributeNames={"#s": "status"},
    ExpressionAttributeValues={":u": "USER#42", ":v": "SHIPPED"},
)
```

**誤ると**: `FilterExpression="status = :v"` と直接書くと、`status` が予約語なので `ValidationException` です。`FilterExpression` にキー属性を書いた場合も同じです。キーの絞り込みは `KeyConditionExpression` に移します。

### ページネーション {#pagination}

1 回の Query または Scan で返せるのは最大 1 MB です。続きがあると応答に `LastEvaluatedKey` が含まれるので、次のリクエストの `ExclusiveStartKey` に渡します。

```python
from boto3.dynamodb.conditions import Key

kwargs = {
    "KeyConditionExpression": Key("PK").eq("USER#42") & Key("SK").begins_with("ORDER#"),
    "ScanIndexForward": False,
}
while True:
    resp = table.query(**kwargs)
    handle(resp["Items"])
    last_key = resp.get("LastEvaluatedKey")
    if not last_key:
        break
    kwargs["ExclusiveStartKey"] = last_key
```

- 最後のページかどうかの判定は、`LastEvaluatedKey` が無いことだけで行います。
- `Count` はフィルター後の件数、`ScannedCount` はフィルター前に評価した件数です。差が大きいなら非効率なアクセスです。
- `ReturnConsumedCapacity` を `TOTAL` または `INDEXES` にすると、消費したキャパシティを確認できます。

**例**: 1 人の注文の合計が 3.5 MB なら、1 MB ずつ 3 ページと 0.5 MB の 1 ページで、4 回の `Query` になります。

**例**: `Count=3`、`ScannedCount=1000` なら、1,000 件読んで 3 件しか使っていません。GSI やキー設計を見直します。

**誤ると**: `Items` が 0 件になった時点で打ち切ると、後ろのページにある一致を取りこぼします。1 ページ目の `Count` を総数として表示すると、件数も少なく出ます。

## LSI と GSI {#indexes}

テーブルは主キーでしか速く引けません。「顧客 ID で作ったテーブルを、注文の状態でも引きたい」ときに、Scan せずに済むよう別のキーで並べ直したコピーを持つのがインデックスです。

| | 本の索引でのたとえ | 実体 |
| --- | --- | --- |
| LSI | 同じ章（パーティションキー）の中で、別の順に並べた目次 | テーブルと同じパーティションに置く |
| GSI | 本とは別に作った、まったく別の観点の索引 | テーブルとは別のパーティションに置く、自動で同期されるコピー |

GSI がテーブルとは別に置かれる設計なので、いつでも追加でき、キーも自由です。その代わり、同期は非同期で結果整合性になり、キャパシティも別に要ります。LSI はテーブルと一緒に置くので強力な整合性を使えますが、作成時にしか作れません。

| 観点 | LSI(ローカルセカンダリインデックス) | GSI(グローバルセカンダリインデックス) |
| --- | --- | --- |
| キー | パーティションキーはテーブルと同じ、ソートキーが別 | パーティションキーもソートキーも自由 |
| 作成時期 | テーブル作成時のみ。後から追加も削除もできない | いつでも追加、削除できる |
| 数の上限 | 1 テーブル 5 個 | デフォルトで 1 テーブル 20 個 |
| 整合性 | 結果整合性と強力な整合性を選べる | 結果整合性のみ |
| キャパシティ | テーブルのものを消費 | インデックス独自 |
| 射影外の属性 | テーブルから自動で取得する(RCU を追加消費) | 取得できない |
| サイズ制限 | パーティションキーの値ごとに 10 GB | なし |
| クエリ範囲 | 1 つのパーティションキーの値 | テーブル全体 |

射影の種類は `KEYS_ONLY`、`INCLUDE`、`ALL` の 3 つです。よく読む属性だけを `INCLUDE` で射影すると、ストレージと書き込みの費用を抑えられます。`INCLUDE` で指定する非キー属性は、テーブルのセカンダリインデックス全体で合計 100 個までです。

```mermaid
flowchart TD
    A["別のキーで検索したい"] --> B{"パーティションキーはテーブルと同じ?"}
    B -- "いいえ" --> G["GSI"]
    B -- "はい" --> C{"強力な整合性が必要?"}
    C -- "はい" --> L["LSI (テーブル作成時に定義)"]
    C -- "いいえ" --> D{"同じキーで 10 GB を超える可能性がある、または既存テーブルに追加したい?"}
    D -- "はい" --> G
    D -- "いいえ" --> L
```

押さえておきたい動作は次のとおりです。

- **スパースインデックス**: インデックスのキー属性を持たない項目はインデックスに入りません。未処理の注文にだけ `pendingAt` を付ければ、未処理分だけを効率よく検索できます。
- **LSI の 10 GB 上限**: 超えると `ItemCollectionSizeLimitExceededException` が発生します。
- **GSI のキーは一意でなくて構いません**: 同じキー値を持つ項目が複数入ります。
- **複数属性キー**: GSI はパーティションキーとソートキーをそれぞれ最大 4 属性で構成できます。文字列を連結した合成キーを作らずに済みます。

**例**:

- **LSI**: `customerId` が同じ注文を、`orderedAt` に加えて `total` の順でも読みたいなら、テーブル作成時に `total` をソートキーとする LSI を定義します。
- **GSI**: `sku` から注文を引くなら、パーティションキーがテーブルと違うので GSI です。
- **LSI の 10 GB**: 1 人の顧客の項目とその LSI の合計が 10 GB に達すると、その顧客への書き込みだけが `ItemCollectionSizeLimitExceededException` になります。他の顧客は書けます。
- **複数属性キー**: `tenantId` と `region` をパーティションキーに、`status` と `createdAt` をソートキーにすれば、`tenantId#region` のような連結が不要です。

**スパースインデックスの計算**: 1 KB の注文 100 万件のうち未処理が 2,000 件だとします。Scan で探すと、1,000,000 KB ÷ 4 KB × 0.5 で 125,000 RCU です。`pendingAt` のスパース GSI なら、2,000 KB ÷ 4 KB × 0.5 で 250 RCU です。

**誤ると**: 処理が終わっても `pendingAt` を `REMOVE` しないと、インデックスに残り続けて処理済みも検索されます。

### 射影とフェッチ {#projection}

`ProjectionType` で、インデックスにコピーする属性を決めます。

| 値 | コピーする属性 | 向く場面 |
| --- | --- | --- |
| `KEYS_ONLY` | インデックスのキーとテーブルのキー | 属性は後で `GetItem` すればよい。最も安い |
| `INCLUDE` | 上に加えて `NonKeyAttributes` で指定した属性 | 読む属性が決まっている |
| `ALL` | すべての属性 | テーブルと同じように読みたい。ストレージと書き込みが最も高い |

`NonKeyAttributes` は 1 インデックスで最大 20 個、テーブルの全インデックス合計で最大 100 個です。同じ属性を 2 つのインデックスに射影すると 2 個に数えます。この上限は `INCLUDE` のときだけで、`ALL` には関係しません。

射影されていない属性を読もうとしたときの動作が、LSI と GSI で違います。

| 対象 | 動作 | 影響 |
| --- | --- | --- |
| LSI | 親テーブルから自動で取得する(フェッチ) | 追加の RCU と遅延が発生する |
| GSI | 取得できない | 属性は返らない。別途 `GetItem` する |

**例**: 注文の一覧画面で `orderedAt` と `total` だけを表示するなら、GSI を `INCLUDE` にして `NonKeyAttributes=["total"]` とします。後から `address` も必要になると、射影は作成後に変更できないので、GSI を作り直します。

**計算の例**: 8 KB の項目を毎秒 100 件追加します。`ALL` なら GSI に 8 KB ずつ書くので 8 WCU × 100 で 800 WCU です。200 バイトだけ `INCLUDE` すれば 1 WCU × 100 で 100 WCU です。

```yaml
GlobalSecondaryIndexes:
  - IndexName: by-orderedAt
    KeySchema:
      - {AttributeName: customerId, KeyType: HASH}
      - {AttributeName: orderedAt, KeyType: RANGE}
    Projection:
      ProjectionType: INCLUDE
      NonKeyAttributes: [total]
```

**誤ると**: LSI を `KEYS_ONLY` にして全属性を読む画面に使うと、毎回フェッチが起きます。4 KB の項目を強力な整合性で 10 件フェッチすれば、インデックスの分に加えて約 10 RCU 増えます。

### GSI のキャパシティとバックプレッシャー {#gsi-backpressure}

GSI はテーブルとは別のキャパシティを持ちます。テーブルへの書き込みは非同期で GSI に反映されますが、GSI の書き込み容量が足りないと **テーブルの書き込みまで抑制** されます。これをバックプレッシャーと呼びます。

テーブルだけ書き込みを受け続けると、GSI への反映待ちがたまり続け、GSI がいつまでも古いままになります。テーブル側を止めて、両者のずれが広がらないようにする仕組みです。

```mermaid
flowchart LR
    W["書き込み 500/秒"] --> T["テーブル<br/>1,000 WCU"]
    T -- "非同期で反映" --> G["GSI<br/>200 WCU"]
    G -. "足りないと抑制を返す" .-> T
    T -. "ProvisionedThroughputExceeded" .-> W
```

**例**: テーブルが 1,000 WCU、GSI が 200 WCU のプロビジョンドで、毎秒 500 件を書くとします。テーブルには余裕があるのに、GSI の不足でテーブルへの書き込みが `ProvisionedThroughputExceededException` になります。GSI をテーブル以上の WCU にします。

GSI への書き込み回数は、更新の内容で変わります。

| テーブルの更新 | GSI の消費 |
| --- | --- |
| 新しい項目を追加(キー属性あり) | 1 回の書き込み |
| インデックスのキー値を変更 | 削除と追加の 2 回 |
| 射影された属性だけを変更 | 1 回 |
| 射影もキーも関係ない属性だけを変更 | 消費しない |

GSI の消費は、項目全体ではなくインデックスの項目サイズで計算します。8 KB の項目でも、GSI に 500 バイトだけ射影していれば GSI への書き込みは 1 WCU です。

**計算の例**: 毎秒 500 件の更新のうち、400 件が射影された属性の変更、100 件がインデックスのキー値の変更だとします。射影は 1 KB 以下です。GSI の消費は 400 × 1 + 100 × 2 で 600 WCU です。テーブルと同じ 500 WCU にしても足りません。

既存のテーブルに GSI を追加すると、状態は `CREATING` になり、既存データをコピーするバックフィルが行われます。この間はクエリできません。

- 進捗は CloudWatch の `OnlineIndexPercentageProgress` で確認します。
- ベーステーブルの `WriteThrottleEvents` と `ThrottledRequests` を監視します。
- 作成中の GSI には Auto Scaling が効きません。`ACTIVE` になるまでは手動で容量を管理します。
- キーの型が合わない既存項目はインデックスに入りません。新しい書き込みで型が合わないと `ValidationException` になります。

**例**: `price` を Number のキーとして GSI を作ると、`price` を文字列 `"1980"` で持つ既存項目はインデックスに入りません。クエリの件数がテーブルより少なくなります。同じ形で新しく書くと、書き込み自体が失敗します。

LSI はテーブルのキャパシティを消費するので、独自の設定はありません。`ReturnItemCollectionMetrics=SIZE` を指定すると、項目コレクションの推定サイズが応答に含まれ、10 GB の上限に近づいていないか確認できます。

## キャパシティモードと RCU/WCU {#capacity}

DynamoDB の性能は、サーバーのスペックではなく「1 秒にどれだけ読み書きするか」で決めます。サーバーがないので、性能も料金も読み書きの量の単位（ユニット）で表します。

モードが 2 つあるのは、負荷が読めるかどうかで最適な払い方が違うためです。

| | 電気料金でのたとえ | 得をする場面 | 損をする場面 |
| --- | --- | --- | --- |
| オンデマンド | 使った分だけの従量制 | 負荷が読めない、夜は 0 | 一日中高い負荷が続く |
| プロビジョンド | 契約アンペアの基本料金制 | 安定した負荷 | 確保したのに使わない、急増で足りない |

**オンプレミスとの対比**: 自前の DB サーバーでは、ピークに合わせてサーバーを買い、余った性能も払い続けます。DynamoDB のプロビジョンドはこれに近く、オンデマンドは「性能を買わず、処理した量だけ払う」点が違います。

| 観点 | オンデマンド | プロビジョンド |
| --- | --- | --- |
| 位置付け | デフォルトで推奨 | 明示的に選択 |
| 課金 | リクエスト数 | 確保したキャパシティの時間数 |
| 容量計画 | 不要 | 必要(Auto Scaling を併用可能) |
| 向く負荷 | 予測しにくい、増減が大きい | 安定して予測できる |
| 上限 | テーブル単位のデフォルトクォータと任意の最大スループット | 設定値とアカウントのクォータ |

テーブルと GSI の 1 テーブルあたりのデフォルトクォータは、どちらのモードでも読み書き各 40,000 ユニットです。引き上げを申請できます。

**例**: 開店直後のセールで負荷が読めないなら、オンデマンドにします。日中ずっと毎秒 800 件前後で安定しているなら、プロビジョンドと Auto Scaling を比べます。

**誤ると**: 夜間に 0 件、昼に数千件という負荷を固定のプロビジョンドにすると、夜は未使用分に課金され、昼はスロットリングします。

### オンデマンドの設定と動作 {#on-demand}

`BillingMode=PAY_PER_REQUEST` で選びます。単位は RRU と WRU ですが、数え方は RCU と WCU と同じです。

| 項目 | 値 |
| --- | --- |
| 新しいテーブルの初期性能 | 毎秒 4,000 書き込み、12,000 読み取りまで |
| 瞬時に対応できる範囲 | 過去のピークの 2 倍まで |
| ピークの 2 倍を超える増加 | 30 分以内に超えるとスロットリングの可能性がある |
| 任意の上限 | `OnDemandThroughput` の `MaxReadRequestUnits`、`MaxWriteRequestUnits` |
| モード切り替え | プロビジョンドからオンデマンドへは 24 時間で 4 回まで。逆方向はいつでも |

**例**: 過去のピークが毎秒 50,000 読み取りなら、100,000 までは瞬時に対応できます。セールで 300,000 に増えるなら、30 分以上かけて増やすか事前にウォームアップします。

上限を毎秒 1,000 WRU に設定すると、超えた分は `ThrottlingException` になり、`ThrottlingReason` は `IndexWriteMaxOnDemandThroughputExceeded` のような形式になります。費用の暴走を防げますが、低すぎると正常な負荷でも失敗します。

```bash
aws dynamodb update-table --table-name Orders \
  --on-demand-throughput MaxReadRequestUnits=10000,MaxWriteRequestUnits=1000
```

**例**: 新しいテーブルに毎秒 10,000 件を最初から書くと、初期性能の 4,000 件を超えるのでスロットリングすることがあります。移行のように開始時から大量に書くなら、徐々に増やします。

**例**: プロビジョンドからオンデマンドへの切り替えは、24 時間で 4 回までです。検証で 5 回目を試すと拒否されます。

!!! note "切り替え回数は緩和された"
    古い資料には切り替えは 24 時間に 1 回とあります。現在はプロビジョンドからオンデマンドへの切り替えは 24 時間で 4 回まで、逆方向は制限なしです。

### プロビジョンドと Auto Scaling {#provisioned-auto-scaling}

`BillingMode=PROVISIONED` で、`ReadCapacityUnits` と `WriteCapacityUnits` を指定します。最小は各 1 です。使わなくても確保した分が課金されます。

| 設定 | 値 | 動作 |
| --- | --- | --- |
| 増やす | 制限なし | 必要なだけ何度でも |
| 減らす | 1 日最大 27 回 | UTC の 1 日の始めに 4 回分あり、1 時間ごとに 1 回分増える。テーブルと GSI で別に数える |
| アカウント上限 | デフォルト 80,000 ずつ | 全テーブルと GSI の合計 |
| 目標使用率 | 20〜90%、推奨 70% | Auto Scaling が維持する、消費/確保 の割合 |
| バーストキャパシティ | 未使用分を最大 5 分(300 秒)保持 | 短い急増を吸収する。将来変わる可能性がある |

Auto Scaling は Application Auto Scaling の機能です。コンソールで作るとデフォルトで有効ですが、CLI や CloudFormation では自分で設定します。テーブルと GSI、読み取りと書き込みはそれぞれ別に設定します。

```bash
aws application-autoscaling register-scalable-target \
  --service-namespace dynamodb \
  --resource-id table/Orders \
  --scalable-dimension dynamodb:table:WriteCapacityUnits \
  --min-capacity 100 --max-capacity 1000

aws application-autoscaling put-scaling-policy \
  --service-namespace dynamodb \
  --resource-id table/Orders \
  --scalable-dimension dynamodb:table:WriteCapacityUnits \
  --policy-name orders-write \
  --policy-type TargetTrackingScaling \
  --target-tracking-scaling-policy-configuration \
    '{"TargetValue": 70, "PredefinedMetricSpecification": {"PredefinedMetricType": "DynamoDBWriteCapacityUtilization"}}'
```

**例**: 確保 200 WCU で消費が 150 WCU だと使用率は 75% です。目標の 70% を超えているので、150 ÷ 0.7 で約 215 WCU に増やします。

設定ごとの値の例です。

- **`--max-capacity`**: 上限 1,000 で消費が 900 WCU になると、900 ÷ 0.7 で約 1,286 WCU が必要ですが、1,000 で止まります。使用率は 90% になり、急増に耐える余裕がなくなります。
- **`--min-capacity`**: 下限 100 なら、夜間に消費が 5 WCU でも 100 WCU 分の課金が続きます。
- **`TargetValue`**: 20 は余裕が大きく費用が高めです。消費 100 WCU なら 500 WCU を確保します。90 なら約 112 WCU ですが、急増の吸収が難しくなります。
- **減らす回数**: 1 日の始めの 4 回と、残り 23 時間に 1 回ずつで、計 27 回です。4 回分を使い切ると、次は 1 時間待ちます。
- **バースト**: 確保 100 RCU で 5 分間まったく読まなければ、100 × 300 で最大 30,000 RCU 分が残ります。これを前提に容量を設計してはいけません。
- **アカウント上限**: 既存の合計が読み取り 50,000 で上限が 80,000 なら、40,000 の新しいテーブルは合計 90,000 になるので作れません。先にクォータを引き上げます。

**落とし穴**:

- 消費が目標を 2 分続けて超えてから動きます。数秒の急増には間に合わないので、バーストかオンデマンドで吸収します。
- GSI に同じ設定をしないと、テーブルだけ増えて GSI がバックプレッシャーを起こします。コンソールには同じ設定を GSI に適用するオプションがあります。
- テーブルを削除しても、スケーリングターゲット、ポリシー、アラームは自動で消えません。

### 計算方法 {#capacity-calculation}

| 操作 | 1 ユニットあたりの単位 | 消費量 |
| --- | --- | --- |
| 強力な整合性の読み取り | 4 KB | 1 RCU |
| 結果整合性の読み取り | 4 KB | 0.5 RCU |
| トランザクション読み取り | 4 KB | 2 RCU |
| 標準の書き込み | 1 KB | 1 WCU |
| トランザクション書き込み | 1 KB | 2 WCU |

**手順**: 項目サイズを単位の倍数に切り上げ、単位で割り、整合性の係数と 1 秒あたりの件数を掛けます。

| 問題 | 計算 | 答え |
| --- | --- | --- |
| 6 KB の項目を強力な整合性で毎秒 100 件読む | 8 KB に切り上げ、2 RCU × 100 | 200 RCU |
| 同じ条件で結果整合性 | 200 ÷ 2 | 100 RCU |
| 同じ条件でトランザクション | 200 × 2 | 400 RCU |
| 2.5 KB の項目を毎秒 50 件書く | 3 KB に切り上げ、3 WCU × 50 | 150 WCU |
| 同じ条件でトランザクション | 150 × 2 | 300 WCU |

操作によって切り上げ方が異なります。

| 操作 | 切り上げの単位 | 例(強力な整合性) |
| --- | --- | --- |
| `GetItem` | 項目ごと | 10 KB は 12 KB 扱いで 3 RCU |
| `BatchGetItem` | 項目ごとに切り上げてから合計 | 1.5 KB と 6.5 KB は 4 + 8 = 12 KB で 3 RCU |
| `Query` | 全項目の合計を切り上げ | 合計 40.8 KB は 44 KB 扱いで 11 RCU |
| `Scan` | 評価した項目の合計 | 返した量ではなく読んだ量で決まる |
| `UpdateItem` | 更新前後の大きい方 | 一部の属性だけの更新でも項目全体のサイズで消費 |
| `BatchWriteItem` | 項目ごとに切り上げてから合計 | 500 バイトと 3.5 KB は 1 + 4 = 5 WCU |

GSI への反映はインデックスの WCU を別途消費します。インデックスのキー値を A から B に変える更新は、削除と追加の 2 回の書き込みになります。

**切り上げの差の例**: 1.5 KB の項目 10 件を強力な整合性で読みます。`Query` なら合計 15 KB を 16 KB に切り上げて 4 RCU です。`BatchGetItem` なら 1 件ごとに 4 KB へ切り上げて 10 RCU です。同じパーティションキーの項目なら `Query` が安く済みます。

3 つの読み方を同じ条件で比べた計算と、複合の例です。

| 条件 | 結果整合性 | 強力な整合性 | トランザクション |
| --- | --- | --- | --- |
| 3 KB を毎秒 80 件 | 40 RCU | 80 RCU | 160 RCU |
| 10 KB を毎秒 20 件 | 12 KB なので 30 RCU | 60 RCU | 120 RCU |
| 500 バイトを毎秒 100 件 | 50 RCU | 100 RCU | 200 RCU |

| 問題 | 計算 | 答え |
| --- | --- | --- |
| 512 バイトを毎秒 100 件書く | 1 KB に切り上げ、1 WCU × 100 | 100 WCU |
| 1.6 KB の項目を削除する | 2 KB に切り上げ | 2 WCU |
| 1.5 KB、2 KB、500 バイトを 1 つのトランザクションで書く | (2 + 2 + 1) × 2 | 10 WCU |
| 5 KB を `TransactGetItems` で 3 件読む | 8 KB なので 2 × 3 × 2 | 12 RCU |
| 50 KB の項目 1 件を `Query` で結果整合性 | 52 KB ÷ 4 × 0.5 | 6.5 RCU |

トランザクションの 2 倍は、準備とコミットの 2 段階を行うためです。条件不成立で書き込みが失敗しても、WCU は消費されます。

## スロットリング {#throttling}

スロットリングは、上限を超えた分をエラーで返して、テーブル全体やほかの利用者への影響を防ぐ仕組みです。上限を超えたまま受け続けると、全部の応答が遅くなります。断られた側は、少し待って再試行すれば成功することが多いので、エラーの種類は「再試行できる」ものになっています。

```mermaid
flowchart TD
    A["スロットリングが起きた"] --> B{"テーブル全体の使用量は上限に近い?"}
    B -- "はい" --> C{"モードは?"}
    C -- "プロビジョンド" --> D["容量を増やす、Auto Scaling"]
    C -- "オンデマンド" --> E["最大スループット設定とクォータを確認"]
    B -- "いいえ" --> F{"GSI の書き込みは足りている?"}
    F -- "いいえ" --> G["GSI の WCU を増やす"]
    F -- "はい" --> H["ホットキー: キー設計、シャーディング"]
```

| 原因 | 主なエラー | 対処 |
| --- | --- | --- |
| プロビジョンドの設定値を超えた | `ProvisionedThroughputExceededException` | キャパシティ増強、Auto Scaling |
| 特定のパーティションに集中した | 同上、または `ThrottlingException` | キー設計の見直し、シャーディング |
| アカウントやテーブルのクォータを超えた | `RequestLimitExceeded`、`ThrottlingException` | クォータ引き上げの申請 |
| オンデマンドの最大スループット設定を超えた | `ThrottlingException` | 設定値の見直し |
| GSI の書き込みが足りない | ベーステーブルの書き込みも抑制される | GSI の WCU をテーブル以上にする |

例外の `ThrottlingReason` フィールドで理由と対象リソースを確認できます。AWS SDK はこの種のエラーを自動で再試行しますが、応答しきれないほどの負荷なら、再試行の前にリクエスト頻度を下げます。再試行の設定は [SDK とレジリエンス](sdk-resilience.md) を参照してください。

`ThrottlingReason` は、リソースの種類、操作、上限の種類をつなげた形式です。

**例**: `TableReadKeyRangeThroughputExceeded` は、テーブルの読み取りが特定のキー範囲の上限を超えたという意味です。テーブルの容量を増やす前に、ホットキーを探します。`IndexWriteMaxOnDemandThroughputExceeded` なら、GSI の書き込みがオンデマンドの最大値を超えたので、`MaxWriteRequestUnits` を見直します。

### エラー名の一覧 {#error-names}

| エラー | 状態 | 再試行 | 意味と対処 |
| --- | --- | --- | --- |
| `ProvisionedThroughputExceededException` | 400 | 可 | テーブルやインデックスの容量超過。SDK が自動で再試行する |
| `ThrottlingException` | 400 | 可 | オンデマンドの上限超過や、管理系 API の呼びすぎ |
| `RequestLimitExceeded` | 400 | 可 | アカウントのスループット上限を超えた |
| `LimitExceededException` | 400 | 可 | `CREATING`、`DELETING`、`UPDATING` のテーブルとインデックスが合計 500 を超えた |
| `ItemCollectionSizeLimitExceededException` | 400 | 可 | LSI がある項目コレクションが 10 GB を超えた |
| `ConditionalCheckFailedException` | 400 | 不可 | 条件式が偽。読み直して判断する |
| `ValidationException` | 400 | 不可 | 必須パラメータの不足、型の不一致、GSI の強力な整合性など |
| `ResourceNotFoundException` | 400 | 不可 | テーブルがない、または `CREATING` の初期段階 |
| `ResourceInUseException` | 400 | 不可 | 既存のテーブルを作ろうとした、`CREATING` 中のテーブルを消そうとしたなど |
| `AccessDeniedException` | 400 | 不可 | 権限不足。IAM を確認する |
| `ReplicatedWriteConflictException` | 400 | 可 | MRSC で同じ項目を別リージョンが更新中 |
| `InternalServerError` | 500 | 可 | 書き込みは成否が不明。単一項目の書き込みは冪等にしてから再試行する |
| `ServiceUnavailable` | 503 | 可 | 一時的な障害 |

**例**:

- **`ResourceNotFoundException`**: `CreateTable` の直後に `PutItem` すると、テーブルがまだ `CREATING` で失敗します。boto3 なら `client.get_waiter("table_exists").wait(TableName="Orders")` で待ちます。
- **`LimitExceededException`**: デプロイで 600 個のテーブルを同時に作ると、500 個の上限を超えます。順に作ります。
- **`InternalServerError`**: `UpdateItem` で 500 が返ると、加算が反映されたか分かりません。条件式やバージョンを付けて、再試行しても二重にならないようにします。

## 条件付き書き込み {#conditional-writes}

`PutItem`、`UpdateItem`、`DeleteItem` に `ConditionExpression` を指定すると、条件が成立したときだけ書き込みます。不成立なら `ConditionalCheckFailedException` が発生し、WCU は消費されます。

複数のアプリが同じ項目を同時に書くと、「読んでから書く」間に他の更新が入り、片方の変更が消えます。DynamoDB には RDB のような行ロックや `SELECT ... FOR UPDATE` がないので、代わりに「書くときに条件を確かめる」ことで同時更新を安全にします。確認と書き込みを 1 回の操作で行うので、間に他の更新は入りません。

```mermaid
sequenceDiagram
    participant A as 処理 A
    participant D as DynamoDB
    participant B as 処理 B
    A->>D: 読む（在庫 10、version 3）
    B->>D: 読む（在庫 10、version 3）
    A->>D: 在庫 9 に更新（条件 version = 3）
    D-->>A: 成功（version 4）
    B->>D: 在庫 9 に更新（条件 version = 3）
    D-->>B: ConditionalCheckFailed
    B->>D: 読み直して再計算
```

```python
from botocore.exceptions import ClientError

# 新規作成のみ許可する(上書き防止)
table.put_item(
    Item={"PK": "USER#42", "SK": "PROFILE", "name": "Aiko"},
    ConditionExpression="attribute_not_exists(PK)",
)

# バージョン番号による楽観的ロック
try:
    table.update_item(
        Key={"PK": "ORDER#123", "SK": "META"},
        UpdateExpression="SET #s = :new, #v = :next",
        ConditionExpression="#v = :cur",
        ExpressionAttributeNames={"#s": "status", "#v": "version"},
        ExpressionAttributeValues={":new": "SHIPPED", ":cur": 3, ":next": 4},
    )
except ClientError as e:
    if e.response["Error"]["Code"] != "ConditionalCheckFailedException":
        raise
    # 他の処理が先に更新した。読み直して再試行する
```

数を増やすだけなら `UpdateExpression="ADD #c :n"` のようなアトミックカウンターも使えます。ただしリクエストの再試行で二重に加算される可能性があり、厳密な数が必要な用途には向きません。

### UpdateExpression {#update-expression}

| 句 | 動作 | 例 | 注意 |
| --- | --- | --- | --- |
| `SET` | 属性を追加または上書き | `SET price = :p` | 加算、`if_not_exists`、`list_append` も使える |
| `REMOVE` | 属性を削除 | `REMOVE tags[1]` | リストの要素も消せる |
| `ADD` | 数値を加算、セットに追加 | `ADD viewCount :one` | Number とセットのみ。属性がなければ作る |
| `DELETE` | セットから要素を削除 | `DELETE colors :c` | セット専用 |

各句は 1 回ずつ使えます。順序は自由です。

| 関数 | 用途 | 例 |
| --- | --- | --- |
| `if_not_exists(path, value)` | 属性がなければ既定値を使う | `SET viewCount = if_not_exists(viewCount, :zero) + :one` |
| `list_append(a, b)` | リストを連結 | `SET hist = list_append(hist, :new)` で末尾に追加 |

**例**: 更新前が `{"viewCount": 5, "price": 100, "tags": {"a", "b"}, "memo": "x"}` の項目に、次の式を実行します。

```text
SET price = :p  ADD viewCount :one, tags :new  REMOVE memo
```

`:p=120`、`:one=1`、`:new={"c"}` なら、結果は `{"viewCount": 6, "price": 120, "tags": {"a", "b", "c"}}` です。

**例**: `SET a = :x, b = a` の `b` には、更新前の `a` が入ります。同じ式の中の動作は、左から順に適用されません。

**落とし穴**: `SET viewCount = viewCount + :one` は、`viewCount` がない項目では失敗します。初回も考えるなら `if_not_exists` を付けるか `ADD` を使います。予約語と同じ属性名は `ExpressionAttributeNames` で置き換えないと `ValidationException` になります。

**誤ると**: `SET a = :x SET b = :y` のように `SET` を 2 回書くと `ValidationException` です。`SET a = :x, b = :y` とカンマで続けます。

### ConditionExpression {#condition-expression}

使える演算子は比較、`BETWEEN`、`IN`、`AND`、`OR`、`NOT` です。関数は次の 6 つです。

| 関数 | 真になる条件 | 用途 |
| --- | --- | --- |
| `attribute_exists(a)` | 属性がある | 既存の項目だけ更新する |
| `attribute_not_exists(a)` | 属性がない | 新規作成のみ許可する |
| `attribute_type(a, t)` | 属性の型が一致 | 型の確認 |
| `contains(a, s)` | 文字列を含む、セットの要素にある | 重複の確認 |
| `begins_with(a, s)` | 文字列で始まる | 接頭辞の確認 |
| `size(a)` | 長さを返す。比較と組み合わせる | `size(items) < :max` |

**例**: `attribute_not_exists(PK)` を付けた `PutItem` は、同じキーの項目があるときに `ConditionalCheckFailedException` になります。条件がなければ既存の項目を丸ごと上書きします。`PutItem` は部分更新ではないので、一部の属性だけ変えたいなら `UpdateItem` を使います。

条件の書き方の例です。

- **比較と `BETWEEN`**: `qty >= :n`(`:n=1`)で在庫切れの注文を防ぎます。`price BETWEEN :a AND :b` で価格の範囲を確かめます。
- **`IN`**: `#s IN (:new, :paid)` で、発送済みの注文の取り消しを防ぎます。
- **`attribute_type`**: `attribute_type(price, :t)` に `:t=N` を渡すと、`price` が Number のときだけ更新します。
- **`contains`**: `NOT contains(tags, :t)` で、同じタグの重複登録を防ぎます。
- **`size`**: `size(#i) < :max` に `:max=10` を渡すと(`items` は予約語なので `#i` に置き換える)、10 個目までしか追加できないカートになります。

### ReturnValues {#return-values}

| API | 使える値 | 補足 |
| --- | --- | --- |
| `UpdateItem` | `NONE`(デフォルト)、`ALL_OLD`、`UPDATED_OLD`、`ALL_NEW`、`UPDATED_NEW` | 更新前後の値を取れる |
| `PutItem`、`DeleteItem` | `NONE`(デフォルト)、`ALL_OLD` | 上書き前、削除前の項目を取れる |

`ReturnValues` で RCU は消費しません。**例**: カウンターを増やして新しい値を使うなら、`UpdateItem` に `ReturnValues="UPDATED_NEW"` を付けます。読み直すと、その間に他の処理が増やした値を読むおそれがあります。

`ReturnValuesOnConditionCheckFailure=ALL_OLD` を指定すると、条件不成立のときに現在の項目を例外に含めて返します。読み直しの RCU を節約できます。

**値ごとの例**: `{"id": "c1", "n": 5, "name": "a"}` に `ADD n :one` を実行します。

| 値 | 返る `Attributes` |
| --- | --- |
| `NONE` | なし |
| `ALL_OLD` | `{"id": "c1", "n": 5, "name": "a"}` |
| `UPDATED_OLD` | `{"n": 5}` |
| `ALL_NEW` | `{"id": "c1", "n": 6, "name": "a"}` |
| `UPDATED_NEW` | `{"n": 6}` |

### アトミックカウンター {#atomic-counter}

`UpdateItem` の `SET n = n + :inc` や `ADD n :inc` は、他の書き込みと干渉せずに値を増やします。読み取りは不要です。

ただし冪等ではありません。応答を受け取れずに再試行すると 2 回加算される可能性があります。

| 用途 | 向くもの |
| --- | --- |
| ページビュー、いいね数(多少の誤差を許せる) | アトミックカウンター |
| 残高、在庫(誤差を許せない) | 条件付き書き込み、トランザクション |

**例**: ページビュー 100 万回のうち 0.01% が再試行で二重になっても、1,000,000 × 0.0001 で 100 回の誤差です。集計には許容できます。同じ割合で残高が二重に増えるのは許容できません。

### 楽観的ロック {#optimistic-locking}

ロックを取らず、更新時にバージョンが変わっていないことを確認します。

1. 項目を読み、`version` を覚えます(例: 3)。
2. `ConditionExpression="version = :cur"` を付けて、`version` を 4 に更新します。
3. `ConditionalCheckFailedException` なら、他の処理が先に更新しています。読み直して、値を計算し直してから再試行します。

**落とし穴**: 同じ値のまま再送すると、また失敗します。失敗しても WCU は消費されるので、競合が多い項目では費用も増えます。

## トランザクション {#transactions}

複数の項目をすべて成功またはすべて失敗として処理します。複数テーブルにまたがれますが、同じアカウントかつ同じリージョン内に限ります。

注文の作成と在庫の減算のように、片方だけ成功すると困る更新のためにあります。RDB のトランザクションと目的は同じですが、DynamoDB では 1 回の API 呼び出しで完結し、`BEGIN` から `COMMIT` まで接続を持ち続ける形ではありません。そのため、途中で別の読み取りの結果を見て処理を変えることはできず、条件はすべて事前に書きます。費用は通常の読み書きの 2 倍です。

| 項目 | `TransactWriteItems` | `TransactGetItems` |
| --- | --- | --- |
| アクション | `Put`、`Update`、`Delete`、`ConditionCheck` | `Get` |
| 上限 | 100 アクション、合計 4 MB | 100 アクション、合計 4 MB |
| 消費 | 項目ごとに 2 倍 | 項目ごとに 2 倍 |

```python
import boto3

client = boto3.client("dynamodb")
client.transact_write_items(
    ClientRequestToken=order_id,
    TransactItems=[
        {"Update": {
            "TableName": "Stock",
            "Key": {"sku": {"S": "A-1"}},
            "UpdateExpression": "SET qty = qty - :n",
            "ConditionExpression": "qty >= :n",
            "ExpressionAttributeValues": {":n": {"N": "1"}},
        }},
        {"Put": {
            "TableName": "Orders",
            "Item": {"orderId": {"S": order_id}},
            "ConditionExpression": "attribute_not_exists(orderId)",
        }},
    ],
)
```

- **冪等性**: `ClientRequestToken` は完了から 10 分間有効です。同じトークンで別のパラメータを送ると `IdempotentParameterMismatch` になります。AWS SDK を使う場合は自動で付与されます。
- **失敗**: `TransactionCanceledException` の `CancellationReasons` に、項目の順番どおりに理由が入ります。条件不成立は `ConditionalCheckFailed` です。
- **競合**: 実行中のトランザクションと競合した標準の書き込みは `TransactionConflictException` になります。
- **キャパシティ**: 条件不成立でキャンセルされても消費します。
- **制約**: 同じ項目を 1 つのトランザクションで 2 回指定できません。インデックスを対象にできません。Streams や GSI への反映は順次行われるため、消費側でアトミック性を前提にしないでください。

**例**:

- **合計サイズ**: 50 KB の項目を 100 件まとめると 5 MB で、4 MB の上限を超えて拒否されます。80 件(4 MB)以下に分けます。
- **`CancellationReasons`**: 上のコードで在庫が足りないと、1 番目が `ConditionalCheckFailed`、2 番目が `None` です。順番で、どの動作が原因か分かります。
- **`ConditionCheck`**: 会員が有効なときだけ注文するなら、書き換えない会員の項目に `ConditionCheck` を入れます。同じ会員の項目に `Update` も足すと、同じ項目の 2 回指定になり拒否されます。
- **消費**: 1 KB 以下の 3 項目を書くトランザクションは、3 × 2 で 6 WCU です。条件不成立でも消費します。

### ClientRequestToken {#client-request-token}

長さは 1〜36 文字です。**例**: `ClientRequestToken=order_id` で送信し、ネットワークエラーで 3 分後に同じ内容を再送しても、書き込みは 1 回だけです。10 分を過ぎると新しいリクエストとして扱われます。

| 状況 | 結果 |
| --- | --- |
| 10 分以内に同じトークンと同じパラメータ | 成功として扱われ、書き込みは繰り返されない |
| 10 分以内に同じトークンと別のパラメータ | `IdempotentParameterMismatchException` |
| 最初のリクエストが実行中に再送 | `TransactionInProgressException` |
| 10 分経過後に同じトークン | 新しいリクエスト。二重実行のおそれ |

### 分離レベル {#transaction-isolation}

| 組み合わせ | 分離レベル |
| --- | --- |
| トランザクションと `GetItem`、`PutItem`、`UpdateItem`、`DeleteItem` | SERIALIZABLE |
| `TransactWriteItems` と `TransactGetItems` | SERIALIZABLE |
| トランザクションと `BatchWriteItem`、`BatchGetItem` の個々の項目 | SERIALIZABLE |
| トランザクションと `BatchGetItem`、`Query`、`Scan` の全体 | READ-COMMITTED |
| トランザクションと `BatchWriteItem` の全体 | 直列化されない |

複数の項目を一貫した状態で読みたいなら、`BatchGetItem` ではなく `TransactGetItems` を使います。

**例**: 口座 A から B へ 1,000 円を移すトランザクションの実行中に `BatchGetItem` で両方を読むと、A は移動後、B は移動前の値が返ることがあります。コミット済みの値ですが、合計が 1,000 円ずれて見えます。`TransactGetItems` なら起きません。

## バッチ操作 {#batch}

1 件ずつ API を呼ぶと、往復の待ち時間が件数分かかります。バッチは複数の要求を 1 回の往復にまとめて、待ち時間を減らすためのものです。トランザクションと違って、全部成功か全部失敗かは保証しません。失敗した分は応答で返るので、その分だけ再送します。

**使う場面:** 小売の本部が毎晩、仕入れ先から届いた商品マスタ 5 万件を取り込みます。25 件ずつの `BatchWriteItem` で、1 件ずつ書くより往復が 25 分の 1 になります。

| | バッチ | トランザクション |
| --- | --- | --- |
| 目的 | 往復を減らして速くする | 全部成功か全部失敗かを保証する |
| 一部の失敗 | ありうる（未処理分を再送） | ない |
| 費用 | 通常と同じ | 2 倍 |

| 項目 | `BatchGetItem` | `BatchWriteItem` |
| --- | --- | --- |
| 上限 | 100 項目、16 MB | 25 件、16 MB |
| 操作 | 取得 | `Put` と `Delete` のみ。Update は不可 |
| 条件式 | 指定不可 | 指定不可 |
| 未処理分 | `UnprocessedKeys` | `UnprocessedItems` |
| 原子性 | なし | なし(各項目の操作だけが原子的) |

バッチの呼び出しが成功しても、一部が未処理のまま返ることがあります。未処理分は指数バックオフを挟んで再送します。

```python
import random
import time

request = {"Orders": [{"PutRequest": {"Item": item}} for item in chunk]}
attempt = 0
while request:
    resp = client.batch_write_item(RequestItems=request)
    request = resp.get("UnprocessedItems", {})
    if request:
        time.sleep(random.uniform(0, 2 ** attempt * 0.1))
        attempt += 1
```

全件が処理できないときは `ProvisionedThroughputExceededException` などが返ります。次の場合はバッチ全体が拒否されます。テーブルが存在しない、キーがスキーマに合わない、同じ項目を複数回指定した、25 件を超えた、1 項目が 400 KB を超えた、全体が 16 MB を超えた、のいずれかです。

boto3 の `table.batch_writer()` は分割と未処理分の再送を自動で行います。

**例**: 300 KB の項目を `BatchGetItem` で 100 件要求すると、16 MB を超えないように 52 件だけ返り、残りは `UnprocessedKeys` に入ります。呼び出し自体は成功するので、`UnprocessedKeys` を見ないと 48 件が消えたように見えます。

`BatchGetItem` はデフォルトで結果整合性です。強力な整合性はテーブルごとに `ConsistentRead=True` で指定します。

バッチの呼び出しは原子的ではありません。呼び出しが成功しても、途中までしか処理されていない場合があります。

**例**: 60 件を書くなら、25 件、25 件、10 件の 3 回に分けます。30 件を 1 回で送ると、呼び出し全体が拒否されます。

**例**: 25 件のうち 5 件が `UnprocessedItems` に残ったら、その 5 件だけを再送します。再送しないと、エラーなしで 5 件が抜けます。

**費用の例**: 500 バイトの項目 25 件は、1 WCU × 25 で 25 WCU です。`PutItem` を 25 回呼ぶのと同じで、まとめても WCU は減りません。減るのは通信の往復です。

## TTL {#ttl}

項目ごとの期限切れ時刻を指定すると、DynamoDB が自動で削除します。WCU を消費しません。

セッションや一時トークンのように、時間が経てば要らないデータを消すためにあります。自分で消すなら、古い項目を Scan で探して削除するバッチが必要で、その読み書きにも費用がかかります。オンプレミスで cron の削除ジョブを動かしていたものを、テーブルの設定に置き換える機能です。

```python
import time

client.update_time_to_live(
    TableName="Sessions",
    TimeToLiveSpecification={"Enabled": True, "AttributeName": "expiresAt"},
)
table.put_item(Item={"PK": "SESSION#1", "expiresAt": int(time.time()) + 3600})
```

- 属性は Number 型で、秒単位の Unix エポック時刻にします。ミリ秒や文字列は期待どおりに動きません。Number 以外の型は無視されます。
- 削除は期限後すぐではなく、通常は数日以内です。期限切れでも削除前の項目は読めるので、正確さが必要ならフィルター式で除外します。
- 値が 5 年以上過去の時刻だと、削除の対象になりません。
- `UpdateTimeToLive` は冪等ではありません。既に有効な場合や、同じテーブルに 1 時間以内にもう一度呼んだ場合は `ValidationException` になります。
- 削除前なら更新で期限を延ばせます。属性を消せば期限切れではなくなります。
- GSI と LSI からも削除され、Streams にはサービスによる削除として記録されます。グローバルテーブルでは他のリージョンへの複製分の書き込み費用が発生します。

TTL で削除された項目を S3 に保存するには、Streams と Lambda を組み合わせ、`userIdentity.type` が `Service`、`principalId` が `dynamodb.amazonaws.com` のレコードだけを処理します。

**例**: セッションを 1 時間で切りたいなら、書き込むときに現在時刻 + 3,600 秒を入れ、読むときに次のフィルターで期限切れを除きます。

```python
import time
from boto3.dynamodb.conditions import Attr, Key

resp = table.query(
    KeyConditionExpression=Key("PK").eq("SESSION#1"),
    FilterExpression=Attr("expiresAt").gt(int(time.time())),
)
```

**値の例**: 2026 年 10 月 31 日 0 時(UTC)は `1793404800` です。30 日後に期限を切るなら、30 × 86,400 = 2,592,000 を足して `1795996800` にします。

**落とし穴**: `Date.now()` のミリ秒をそのまま入れると、必要な秒単位の形式にならず、期待した時刻に削除されません。`2026-10-31T00:00:00Z` のような文字列は無視されます。

**誤ると**: `1793404800000` のようなミリ秒は、秒として読むと遠い未来なので期限が来ません。項目が消えず、ストレージの費用が増え続けます。

## DynamoDB Streams {#streams}

[:material-star-circle: AIP](../courses/aip/services.md){ .exam-badge .exam-professional }

項目の変更を時系列で記録します。テーブルの性能には影響しません。

「注文が入ったらメールを送る」「変更を検索エンジンにも反映する」といった後続の処理を、書き込むアプリから切り離すためにあります。アプリが全部の後続処理を呼ぶと、処理が増えるたびにアプリを直し、1 つの失敗で書き込みまで失敗します。

**オンプレミスとの対比**: RDB の変更データキャプチャ（CDC）や、MySQL のバイナリログを読む仕組みに当たります。違いは、保持が 24 時間に限られる点と、Lambda がそのまま読み手になれる点です。

```mermaid
flowchart LR
    A["アプリ"] -- "PutItem" --> T["テーブル"]
    T -- "変更を記録" --> S["Streams（24 時間）"]
    S --> L["Lambda"]
    L --> M["メール送信"]
    L --> O["OpenSearch へ同期"]
```

| 特性 | 内容 |
| --- | --- |
| 保持期間 | 24 時間 |
| 重複 | 各レコードはストリームに 1 度だけ現れる |
| 順序 | 同じ項目への変更の順序を保証する(パーティションや項目コレクション全体では保証しない) |
| 整合性 | 読み取りは結果整合性 |
| 同時読み取り | 1 シャードあたり 2 プロセスまで(グローバルテーブルでは 1 を推奨) |

`StreamViewType` は次の 4 つです。作成後に変えるには、ストリームを無効にして作り直します。

| 値 | 記録する内容 |
| --- | --- |
| `KEYS_ONLY` | キー属性のみ |
| `NEW_IMAGE` | 変更後の項目全体 |
| `OLD_IMAGE` | 変更前の項目全体 |
| `NEW_AND_OLD_IMAGES` | 変更前後の両方 |

**例**:

- **`KEYS_ONLY`**: 「変わった ID だけ」を別の処理へ渡し、受け手が最新の値を読み直す場合です。レコードが小さく済みます。
- **`NEW_IMAGE`**: 検索用の OpenSearch へ最新の状態を同期します。
- **`OLD_IMAGE`**: 削除された項目を監査用に S3 へ残します。削除のレコードには変更後の項目がありません。
- **`NEW_AND_OLD_IMAGES`**: 価格が 1,000 円から 800 円に下がったときだけ通知します。

**誤ると**: 1 つのシャードを 3 つの Lambda 関数で読むと、2 プロセスまでの目安を超えてスロットリングすることがあります。1 つの関数から EventBridge や SNS へ広げます。

データを変更しない `PutItem` や `UpdateItem` はレコードを作りません。Lambda はイベントソースマッピングで読み取り、シャードの親子関係も順序も処理してくれます。詳しくは [Lambda](lambda.md) と [ストリーミング](streaming.md) を参照してください。

### StreamSpecification {#stream-specification}

`CreateTable` または `UpdateTable` で指定します。

```bash
aws dynamodb update-table --table-name Orders \
  --stream-specification StreamEnabled=true,StreamViewType=NEW_AND_OLD_IMAGES
```

| 操作 | 結果 |
| --- | --- |
| 既にストリームがあるのに有効化 | `ValidationException` |
| ストリームがないのに無効化 | `ValidationException` |
| `StreamViewType` の変更 | できない。無効化して作り直す |
| 無効化 | 開いているシャードは閉じる。データは 24 時間読める |
| 無効化して再度有効化 | 新しいストリームになり、ARN が変わる |

**例**: 価格の変更を通知するなら、変更前後を比べるので `NEW_AND_OLD_IMAGES` が必要です。`KEYS_ONLY` を選ぶと、Lambda が項目を読み直す必要があり、その時点では既に別の値になっているかもしれません。

**落とし穴**: 処理の遅れが 24 時間を超えるとレコードは失われます。Streams の有効化はテーブルの性能に影響しません。

## DAX {#dax}

[:material-certificate: SOA](../courses/soa/services.md){ .exam-badge .exam-associate }

DynamoDB 専用のインメモリキャッシュで、VPC 内で動きます。アプリケーションは DAX クライアントに切り替えるだけで、ほぼ同じ API で使えます。

DynamoDB の応答はミリ秒単位ですが、同じ項目を大量に読む処理では、マイクロ秒単位の応答や読み取りユニットの節約が欲しくなります。汎用のキャッシュ（ElastiCache など）を使うと、キャッシュの読み書きと無効化をアプリに書く必要があります。DAX は DynamoDB と同じ API の前に置くことで、アプリの変更を最小にしています。

**使う場面:** EC のタイムセールで、目玉商品 20 点の詳細を毎秒 5 万回読みます。同じ項目への読み取りが集中するので、DAX の項目キャッシュで DynamoDB の RCU とホットキーを避けます。

| | アプリで組む汎用キャッシュ | DAX |
| --- | --- | --- |
| アプリの変更 | キャッシュを読む、なければ DB を読む、を自分で書く | クライアントを差し替えるだけ |
| 対象 | 何でも | DynamoDB の読み取りだけ |
| 強力な整合性 | 自分で決める | キャッシュせず素通り |

**提供単位**: クラスターはリージョンの VPC の中に作り、ノードはサブネットグループの AZ に置きます。AZ の障害に備えて自分で複数の AZ に分けます([リソースの提供単位](resource-scope.md#scope-zonal))。

| キャッシュ | 保存するもの | 更新 |
| --- | --- | --- |
| 項目キャッシュ | `GetItem`、`BatchGetItem` の結果 | デフォルトの TTL は 5 分。DAX 経由の書き込みで更新 |
| クエリキャッシュ | `Query`、`Scan` の結果セット | デフォルトの TTL は 5 分。TTL まで更新されない。項目の更新では無効化されない |

```mermaid
sequenceDiagram
    participant App as アプリ
    participant DAX
    participant DDB as DynamoDB
    App->>DAX: GetItem (結果整合性)
    DAX-->>App: ヒットならキャッシュから返す
    App->>DAX: GetItem (ConsistentRead=True)
    DAX->>DDB: そのまま転送
    DDB-->>DAX: 結果
    DAX-->>App: 返すがキャッシュしない
```

注意点は次のとおりです。

- **強力な整合性の読み取りと `TransactGetItems`** は素通りし、キャッシュされません。DAX は結果整合性の読み取りを速くする仕組みです。
- **書き込みはライトスルー**です。DynamoDB への書き込みが成功した後にキャッシュを更新します。書き込みが失敗すればキャッシュされません。
- **DAX を経由しない更新**は検知されず、TTL が切れるまで古い値を返します。
- **ネガティブキャッシュ**: 存在しないという結果もキャッシュします。
- **`TransactWriteItems` を DAX 経由で実行**すると、キャッシュ更新のために読み取りの RCU を追加で消費します。
- テーブルの作成など管理系の API は DynamoDB に直接送ります。
- 高可用性のために、複数の AZ に 3 ノード以上を置くことが推奨されています。

### DAX の設定 {#dax-settings}

| 設定 | 値 | 動作と落とし穴 |
| --- | --- | --- |
| `record-ttl-millis` | デフォルト 5 分(300,000 ミリ秒) | 項目キャッシュの TTL。0 にすると、LRU か書き込みでしか更新されない |
| `query-ttl-millis` | デフォルト 5 分(300,000 ミリ秒) | クエリキャッシュの TTL。0 にするとキャッシュしない |
| ノード数(レプリケーション係数) | 1〜11(プライマリ + 最大 10 のレプリカ) | 稼働中に増減できる。読み取りをスケールする |
| ノードタイプ | 作成時に指定 | 稼働中のクラスターでは変更できない。新しいクラスターを作る |
| 保存時の暗号化 | 作成時に指定 | AWS マネージドキーのみ。カスタマーマネージドキーは使えない |
| 転送中の暗号化 | 作成時に指定 | 既存のクラスターでは有効にできない。エンドポイントは `daxs://` |
| ポート | 8111 | セキュリティグループのインバウンドで TCP を許可する |
| パラメータグループ | `default.dax.1.0` は変更不可 | TTL を変えるならカスタムのグループを作る |

TTL は次のように設定します。

```bash
aws dax create-parameter-group --parameter-group-name custom-ttl
aws dax update-parameter-group --parameter-group-name custom-ttl \
  --parameter-name-values "ParameterName=record-ttl-millis,ParameterValue=600000"
aws dax update-parameter-group --parameter-group-name custom-ttl \
  --parameter-name-values "ParameterName=query-ttl-millis,ParameterValue=180000"
```

**例**: アプリが DAX 経由で `DocId=101` を `Query` した後に `PutItem` で新しい版を追加しても、同じ `Query` は古い結果を返します。`query-ttl-millis` が 3 分なら、最大 3 分は古いままです。一方、`GetItem` の結果は項目キャッシュが書き込みで更新されるので新しくなります。

| 動作 | 内容 |
| --- | --- |
| ノード間の整合性 | プライマリからレプリカへ非同期。通常 1 秒未満。読むノードで値が違うことがある |
| ネガティブキャッシュ | 項目がないという結果も TTL までキャッシュする |
| LRU | 常に有効で設定できない。満杯なら TTL 前でも追い出す |
| 過負荷 | `ThrottlingException` を返す。`ThrottledRequestCount` を監視し、ノードを増やす |
| 管理系 API | `CreateTable` などは認識しない。DynamoDB に直接送る |

設定ごとの値の例です。

- **`record-ttl-millis`**: 600,000 なら 10 分です。商品名のように変わらない項目に向きます。**誤ると**: 別のアプリが DynamoDB へ直接書くと、最大 10 分は古い値を返します。
- **`query-ttl-millis`**: 0 にすると `Query` と `Scan` の結果をキャッシュしません。**誤ると**: 3,600,000(1 時間)にすると、新しい注文が一覧に最大 1 時間出ません。
- **ノード数**: 3 ならプライマリ 1 とレプリカ 2 です。`aws dax increase-replication-factor --cluster-name app --new-replication-factor 5` で 5 ノードに増やします。新しいノードはピアからキャッシュを同期するので、ピークの前に増やします。
- **ノードタイプ**: 1 つのクラスターのノードは同じタイプです。大きくするときは、新しいクラスターを作って切り替えます。
- **保存時と転送中の暗号化**: 後から付けられないので、作成時に決めます。**誤ると**: 既存のクラスターで `daxs://` に変えても接続できず、作り直しになります。
- **ポート 8111**: **誤ると**: アプリのセキュリティグループから許可していないと、DAX クライアントの接続がタイムアウトします。
- **ネガティブキャッシュ**: `GetItem` で「なし」と返った項目を、DynamoDB へ直接追加しても、TTL が切れるまで「なし」と返ります。

ElastiCache や CloudFront との使い分けは [データベースとキャッシュ](databases.md) にまとめています。

## グローバルテーブル {#global-tables}

複数リージョンにレプリカを持つマルチアクティブのテーブルです。どのレプリカにも読み書きできます。

世界中の利用者に近いリージョンで読み書きさせたいとき、またはリージョン全体の障害でも止めたくないときのためにあります。自分で複製を作るなら、Streams を読んで別リージョンに書く処理と、競合の解決を自前で用意することになります。

**使う場面:** 日本と欧州で使う旅行予約アプリのお気に入りや閲覧履歴を、利用者に近いリージョンで読み書きします。リージョン障害のときは、もう一方のリージョンへアプリの接続先を切り替えます。

[![DynamoDB グローバルテーブル](../assets/diagrams/dynamodb-global-tables.png)](../assets/diagrams/dynamodb-global-tables.png)

どのリージョンでも書けるので、同じ項目を 2 か所で同時に書くと競合します。MREC は「速さ」を取って最後の書き込みを残し、MRSC は「正しさ」を取って書き込みのたびに別リージョンと同期します。その分、MRSC は書き込みの応答が遅くなります。

**提供単位**: グローバルテーブルは、各リージョンのテーブルを同期する機能です。レプリカはそれぞれリージョン単位で、VPC の外にあります([リソースの提供単位](resource-scope.md#scope-regional-outside))。

| モード | 複製 | 整合性 | 補足 |
| --- | --- | --- | --- |
| MREC(マルチリージョン結果整合性) | 非同期。通常は 1 秒以内 | リージョン間は結果整合性 | デフォルト。競合は最後の書き込みが優先 |
| MRSC(マルチリージョン強整合性) | 応答前に別リージョンへ同期 | どのレプリカでも強力な整合性の読み取りで最新 | 同一アカウントのみ |

モードはテーブル作成時に決まり、後から変更できません。トランザクションの ACID 保証は書き込んだリージョン内だけです。他のリージョンでは途中の状態が見えることがあります。

| 設定や動作 | 内容 |
| --- | --- |
| 競合の解決(MREC) | 項目ごとに内部タイムスタンプが最新のものが残る(最後の書き込みが優先) |
| 競合のエラー(MRSC) | 別リージョンが同じ項目を更新中だと `ReplicatedWriteConflictException`。再試行できる |
| Streams | MREC は複製に使うのでデフォルトで有効。MRSC はデフォルトで無効 |
| アカウント構成 | 同一アカウントか複数アカウント。MRSC は同一アカウントのみ |
| TTL | 削除は全レプリカに複製され、複製先では書き込みとして課金される |

**例**: 東京とバージニアで同じ項目をほぼ同時に更新すると、MREC では最新のタイムスタンプの更新だけが残り、もう片方は消えます。在庫の増減のように両方を反映したいなら、書き込むリージョンを 1 つに決めるか、MRSC を検討します。

**例**: 在庫 10 の項目を、東京が 9 に、バージニアが 8 に `SET` します。後から書いた 8 だけが残り、1 個分の減算が消えます。MRSC なら片方が `ReplicatedWriteConflictException` になるので、読み直して再試行します。

**TTL の費用の例**: 3 リージョンのテーブルで TTL が 100 万件を削除すると、他の 2 リージョンへの複製は 1,000,000 × 2 で 200 万件分の書き込みとして課金されます。

**誤ると**: トランザクションで注文と在庫を同時に更新しても、別のリージョンでは片方だけ先に見えることがあります。別リージョンの読み取りで整合性を前提にしてはいけません。

## テーブルクラス {#table-classes}

| 値 | 特徴 | 向く場面 |
| --- | --- | --- |
| `STANDARD`(デフォルト) | スループットが安い | ほとんどのテーブル |
| `STANDARD_INFREQUENT_ACCESS` | ストレージが安い。リクエストは高い | ストレージ費用が中心のテーブル |

性能、耐久性、API は同じで、セカンダリインデックスも同じクラスになります。変更は 30 日間に 2 回までで、バックグラウンドで行われ、その間もテーブルは使えます。

**例**: ストレージ費用が、Standard でのスループット費用の 50% を超えるなら Standard-IA を検討します。過去の注文履歴やログのようなテーブルです。

**判断の計算**: 架空の金額で、Standard のストレージが月 60、スループットが月 100 なら、60 ÷ 100 で 60% なので検討の対象です。ストレージが月 20 なら 20% なので Standard のままにします。

```bash
aws dynamodb update-table --table-name OrderHistory \
  --table-class STANDARD_INFREQUENT_ACCESS
```

**誤ると**: 読み書きの多いテーブルを Standard-IA にすると、リクエストの単価が上がって総額が増えます。30 日に 2 回の制限があるので、すぐには戻せないことがあります。

## バックアップと復元 {#backup}

複数の AZ への複製は機器の故障には強いものの、誤った `DeleteItem` やバグによる上書きも、そのまま全部の複製に反映されます。バックアップは「壊れる前の時点」に戻すためのもので、複製とは守るものが違います。

| | 守るもの | オンプレミスでのたとえ |
| --- | --- | --- |
| AZ への複製（自動） | ディスクや AZ の故障 | RAID、DB のレプリカ |
| PITR | 操作ミス、バグ。直前の任意の秒に戻す | トランザクションログを使った時点復旧 |
| オンデマンドバックアップ | 長期の保管、リリース前の控え | 夜間のフルバックアップのテープ |

| 方式 | 内容 | 設定 |
| --- | --- | --- |
| PITR | 秒単位で過去の状態に復元。デフォルトは無効 | `RecoveryPeriodInDays` は 1〜35 日 |
| オンデマンドバックアップ | 手動の完全バックアップ。削除するまで保持 | `CreateBackup` または AWS Backup |

```bash
aws dynamodb update-continuous-backups --table-name Orders \
  --point-in-time-recovery-specification \
  PointInTimeRecoveryEnabled=true,RecoveryPeriodInDays=7
```

| 動作 | 内容 |
| --- | --- |
| 復元先 | 常に新しいテーブル。同じ名前のまま上書きはできない |
| 復元できる最新の時点 | `LatestRestorableDateTime`。通常は現在の約 5 分前 |
| 引き継ぐもの | データ、GSI、LSI、プロビジョンドキャパシティ、暗号化の設定 |
| 手動で再設定するもの | Auto Scaling、IAM ポリシー、CloudWatch のメトリクスとアラーム、タグ、Streams、TTL、PITR |
| PITR を有効にしたテーブルの削除 | システムバックアップ `テーブル名$DeletedTableBackup` を 35 日間無料で保持 |
| 費用 | テーブルサイズで決まる。期間を 35 日から 1 日にしても安くならない |
| 性能 | バックアップも PITR も読み書きの性能に影響しない |

**例**: テストスクリプトが本番テーブルを 10 時 05 分に壊したら、10 時 04 分を指定して `Orders-restored` に復元します。アプリの接続先を変えるか、データを戻します。Streams や TTL は引き継がれないので、付け直さないとトリガーが動かず、期限切れの項目も消えません。

```bash
aws dynamodb restore-table-to-point-in-time \
  --source-table-name Orders --target-table-name Orders-restored \
  --restore-date-time 2026-10-31T10:04:00Z

# スキーマ移行の前に、期限なしのバックアップを取る
aws dynamodb create-backup --table-name Orders --backup-name before-migration
```

**例**: `RecoveryPeriodInDays=7` なら、8 日前の時点には戻せません。監査で 30 日前に戻す要件があるなら 30 以上にします。費用は変わりません。

**誤ると**: `LatestRestorableDateTime` は通常、現在の約 5 分前です。10 時 06 分の時点では 10 時 04 分を指定できないことがあるので、少し待ってから復元します。

## 暗号化 {#encryption}

保存データは常に暗号化されていて、無効にはできません。対象はプライマリキー、インデックス、Streams、グローバルテーブル、バックアップです。

| キーの種類 | 保管場所 | 費用 | 使いどころ |
| --- | --- | --- | --- |
| AWS 所有キー | DynamoDB 側(デフォルト) | 追加なし | 特に要件がない |
| AWS マネージドキー | 自分のアカウントの KMS | KMS の料金 | 利用状況を監査したい |
| カスタマーマネージドキー | 自分のアカウントの KMS | KMS の料金 | キーの制御が必要 |

キーの種類は後からでも切り替えられます。詳しくは [KMS](kms.md) を参照してください。

**例**: CloudTrail で「誰がいつキーを使ったか」を監査し、キーを自分で無効化できるようにしたいなら、カスタマーマネージドキーを指定します。AWS 所有キーでは自分のアカウントの CloudTrail に使用記録が残りません。

```bash
aws dynamodb update-table --table-name Orders \
  --sse-specification Enabled=true,SSEType=KMS,KMSMasterKeyId=alias/orders
```

**誤ると**: ソートキーに `user@example.com` のようなメールアドレスを入れると、下の注意のとおり一部が平文でメタデータに残ることがあります。ハッシュ値か内部の ID を使います。

**注意**: 新しい DAX クラスターの保存時の暗号化は AWS マネージドキーを使います。ソートキーのうち範囲の境界を示す一部の値は、平文でテーブルのメタデータに保存されます。機密データをソートキーに入れないようにします。

## 細かいアクセス制御 {#fine-grained-access}

IAM ポリシーの条件キーで、項目と属性の単位までアクセスを制限できます。

スマホアプリから DynamoDB を直接読ませると、テーブルへの権限だけでは他人の項目まで読めてしまいます。ユーザーごとにテーブルを分けるのは現実的ではないので、1 つのテーブルの中で「自分のパーティションキーの項目だけ」に絞るためにあります。RDB の行レベルセキュリティに近い考え方です。

```mermaid
flowchart LR
    U["ユーザー A<br/>（Cognito の ID: a-1）"] --> P{"LeadingKeys<br/>= a-1 ?"}
    P -- "PK = a-1 の項目" --> OK["許可"]
    P -- "PK = b-2 の項目" --> NG["拒否"]
```

| 条件キー | 制限する対象 |
| --- | --- |
| `dynamodb:LeadingKeys` | パーティションキーの値(項目単位) |
| `dynamodb:Attributes` | アクセスできる最上位の属性 |
| `dynamodb:Select` | `Select` パラメータの値 |
| `dynamodb:ReturnValues` | `ReturnValues` パラメータの値 |

次のポリシーは、Cognito の ID とパーティションキーが一致する項目だけを許可します。

```json
{
  "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Allow",
    "Action": [
      "dynamodb:GetItem",
      "dynamodb:Query",
      "dynamodb:PutItem",
      "dynamodb:UpdateItem",
      "dynamodb:DeleteItem"
    ],
    "Resource": "arn:aws:dynamodb:ap-northeast-1:111122223333:table/UserData",
    "Condition": {
      "ForAllValues:StringEquals": {
        "dynamodb:LeadingKeys": ["${cognito-identity.amazonaws.com:sub}"]
      }
    }
  }]
}
```

- `LeadingKeys` には `ForAllValues` 修飾子が必須です。
- `Scan` は `LeadingKeys` に関係なく全項目を返すので、許可しません。
- `dynamodb:Attributes` は、リクエストに書かれた属性だけを評価します。`ProjectionExpression` を省略すると全属性が返るため、`dynamodb:Select` を `SPECIFIC_ATTRIBUTES` に制限し、`dynamodb:ReturnValues` も併せて制限します。
- `dynamodb:Attributes` を使うときは、テーブルとインデックスのキー属性もリストに含めます。
- `dynamodb:FirstPartitionKeyValues` は `LeadingKeys` と同じ意味で使えます。複数属性のキーには `dynamodb:SecondPartitionKeyValues` なども用意されています。

**例**: ID プールで認証したユーザー `us-east-1:abc` は、パーティションキーが同じ値の項目だけを読めます。別のユーザーのキーで `GetItem` すると `AccessDeniedException` です。パーティションキーに Cognito の `sub` を使わず、メールアドレスなどを使っていると、この方法では制御できません。

**属性を絞る例**: `name` と `email` だけを読ませ、`salary` を隠します。条件は次のように書きます。

```json
{
  "ForAllValues:StringEquals": {
    "dynamodb:Attributes": ["userId", "name", "email"]
  },
  "StringEqualsIfExists": {
    "dynamodb:Select": "SPECIFIC_ATTRIBUTES",
    "dynamodb:ReturnValues": ["NONE", "UPDATED_OLD", "UPDATED_NEW"]
  }
}
```

**誤ると**: `dynamodb:Select` の制限がないと、`ProjectionExpression` を省略した `GetItem` で `salary` も返ります。`dynamodb:Attributes` はリクエストに書かれた属性だけを評価するからです。

## 既定値と上限のまとめ {#numbers}

| 項目 | 値 |
| --- | --- |
| 項目サイズの上限 | 400 KB(属性名を含む) |
| パーティションキー、ソートキーの長さ | 2,048 バイト、1,024 バイト |
| Number の精度、ネストの深さ | 38 桁、32 階層 |
| 1 パーティションの上限 | 毎秒 3,000 読み込みユニット、1,000 書き込みユニット |
| 1 RCU | 4 KB を強力な整合性で 1 回、結果整合性で 2 回 |
| 1 WCU | 1 KB を 1 回 |
| トランザクションの係数 | 読み書きとも 2 倍 |
| テーブル上限(デフォルト) | 各 40,000 ユニット |
| アカウント上限(プロビジョンド) | 各 80,000 ユニット |
| 新しいオンデマンドテーブル | 毎秒 4,000 書き込み、12,000 読み取り |
| オンデマンドへの切り替え | 24 時間で 4 回 |
| 容量の減少 | 1 日最大 27 回 |
| Auto Scaling の目標使用率 | 20〜90%(推奨 70%) |
| バーストキャパシティ | 最大 300 秒分 |
| GSI、LSI の数 | デフォルト 20 個、5 個 |
| 射影の非キー属性 | インデックスあたり 20 個、全インデックスの合計 100 個 |
| LSI の項目コレクション | 10 GB |
| Query、Scan の 1 回の読み取り | 1 MB |
| `TotalSegments` | 1〜1,000,000 |
| `BatchGetItem` | 100 項目、16 MB |
| `BatchWriteItem` | 25 件、16 MB |
| トランザクション | 100 アクション、4 MB |
| `ClientRequestToken` | 1〜36 文字、10 分間有効 |
| TTL の属性 | Number 型のエポック秒。5 年より古い値は対象外 |
| Streams の保持 | 24 時間 |
| DAX の TTL | 項目、クエリとも 5 分 |
| DAX のノード | 最大 11 |
| PITR の期間 | 1〜35 日 |
| テーブルクラスの変更 | 30 日間に 2 回 |

## 試験のポイント {#exam-points}

| こう問われたら | 答え |
| --- | --- |
| 特定のキーでスロットリングする | パーティションキーを高カーディナリティにする、書き込みシャーディング |
| 書いた直後に最新を読みたい | `ConsistentRead=True`(テーブルか LSI) |
| GSI を強力な整合性で読みたい | できない |
| 既存テーブルに別のソートキーを追加したい | LSI は不可なので GSI を追加 |
| Scan が遅く RCU を食う | GSI を作って Query に変える。全件処理なら並列スキャン |
| フィルターしたのに RCU が減らない | フィルターは読み取り後に適用される |
| `ProjectionExpression` で RCU を減らせるか | 減らない |
| 次のページの取り方 | `LastEvaluatedKey` を `ExclusiveStartKey` に渡す |
| 同時更新の上書きを防ぎたい | バージョン属性と条件付き書き込み(楽観的ロック) |
| 複数項目をすべて成功か全失敗にしたい | `TransactWriteItems` |
| `UnprocessedItems` が返った | 指数バックオフで再送する |
| 古いセッションを費用をかけずに消したい | TTL(Number 型のエポック秒) |
| 変更をトリガーに処理したい | Streams と Lambda |
| 変更前後の値が必要 | `NEW_AND_OLD_IMAGES` |
| 読み取りをマイクロ秒単位で返したい、コード変更は最小にしたい | DAX |
| DAX で最新を読みたい | できない。強力な整合性はキャッシュされず DynamoDB へ転送される |
| マルチリージョンで読み書きしたい | グローバルテーブル |
| ユーザーは自分の項目だけ操作できるように | `dynamodb:LeadingKeys` と Cognito の ID |
| GSI の書き込み不足でテーブルも遅い | GSI の WCU をテーブル以上にする |
| `Limit=10` なのに 10 件未満しか返らない | `Limit` はフィルター前の評価件数 |
| LSI で射影外の属性を読むと RCU が増える | フェッチが発生する。射影に加える |
| 新規作成のみ許可したい | `attribute_not_exists(PK)` |
| 更新後の値を読み直さず取りたい | `ReturnValues=UPDATED_NEW` または `ALL_NEW` |
| トランザクションを安全に再試行したい | 同じ `ClientRequestToken` を 10 分以内に送る |
| DAX の `Query` が更新後も古い | クエリキャッシュは書き込みで無効化されない。`query-ttl-millis` を短くする |
| ストレージ費用が中心のテーブル | `STANDARD_INFREQUENT_ACCESS` |
| 誤って更新したデータを戻す | PITR で新しいテーブルに復元する |
| 復元後に Streams が動かない | Streams や TTL は引き継がれない |

## 関連ページ {#related}

- [データベースとキャッシュ](databases.md)
- [Lambda](lambda.md)
- [ストリーミング](streaming.md)
- [SDK とレジリエンス](sdk-resilience.md)
- [IAM](iam.md)
- [Cognito](cognito.md)
- [KMS](kms.md)

## 参考 {#references}

- [Quotas in Amazon DynamoDB](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/ServiceQuotas.html)
- [DynamoDB read and write operations](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/read-write-operations.html)
- [DynamoDB read consistency](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/HowItWorks.ReadConsistency.html)
- [Scanning tables in DynamoDB](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Scan.html)
- [Paginating table query results](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Query.Pagination.html)
- [Secondary indexes](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/SecondaryIndexes.html)
- [Local secondary indexes](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/LSI.html)
- [Using Global Secondary Indexes](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/GSI.html)
- [DynamoDB throughput capacity](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/capacity-mode.html)
- [Troubleshooting throttling](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/TroubleshootingThrottling.html)
- [Partition key best practices](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/bp-partition-key-design.html)
- [Transactions: how it works](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/transaction-apis.html)
- [BatchWriteItem](https://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_BatchWriteItem.html)
- [BatchGetItem](https://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_BatchGetItem.html)
- [Time to live (TTL)](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/TTL.html)
- [DynamoDB Streams and TTL](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/time-to-live-ttl-streams.html)
- [Change data capture for DynamoDB Streams](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Streams.html)
- [DAX: How it works](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/DAX.concepts.html)
- [DAX and DynamoDB consistency models](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/DAX.consistency.html)
- [Global tables](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/GlobalTables.html)
- [Encryption at rest](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/EncryptionAtRest.html)
- [Using IAM policy conditions for fine-grained access control](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/specifying-conditions.html)
- [DynamoDB item sizes and formats](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/CapacityUnitCalculations.html)
- [Query API reference](https://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_Query.html)
- [DynamoDB on-demand capacity mode](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/on-demand-capacity-mode.html)
- [Managing throughput capacity with auto scaling](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/AutoScaling.html)
- [Using update expressions](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Expressions.UpdateExpressions.html)
- [Error handling with DynamoDB](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Programming.Errors.html)
- [Managing DAX clusters](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/DAX.cluster-management.html)
- [Backup and restore for DynamoDB](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Backup-and-Restore.html)
- [Enable point-in-time recovery](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/PointInTimeRecovery_Howitworks.html)
- [Considerations when choosing a table class](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/WorkingWithTables.tableclasses.html)

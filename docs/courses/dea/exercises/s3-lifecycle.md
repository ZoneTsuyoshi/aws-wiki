# S3 のライフサイクルとオープンテーブル形式の問題集

対象の解説: [Amazon S3 と S3 Glacier](../../../services/s3.md)、[S3 Tables と Apache Iceberg](../../../services/data-engineering.md#s3-tables-iceberg)

### 問1 {#q1}

S3 のデータレイクで、同時の読み書き、行単位の `MERGE`、過去の時点の参照が要ります。どの形式を選びますか。

- A. Hive 形式のパーティション付きの Parquet
- B. gzip の CSV を日付のフォルダごとに置く形
- C. Apache Iceberg のテーブルとして S3 に置く形
- D. Avro のファイルを 1 つのフォルダに置く形

??? success "答えと解説"
    **正解: C**

    Iceberg は ACID、行レベルの更新、スナップショットを持ちます。

    - A: 誤り。行レベルの更新やタイムトラベルの機能がありません。
    - B: 誤り。テーブルの機能がありません。
    - C: 正しい。
    - D: 誤り。テーブルの機能がありません。

    **スキル:** [2.1.7](../domain2.md#skill-2-1-7) / **参照:** [Apache Iceberg](../../../services/data-engineering.md#iceberg)

### 問2 {#q2}

Iceberg の小さなファイルと古いスナップショットの保守を、自分で設定せず任せたいです。何を選びますか。

- A. S3 Tables のテーブルバケットに保存する
- B. テーブルバケットに置き、`s3` の権限だけをロールに付ける
- C. 汎用バケットに置き、ライフサイクルで古いファイルを消す
- D. 汎用バケットに置き、何も設定せずに自動の保守を待つ

??? success "答えと解説"
    **正解: A**

    S3 Tables は保守が既定で有効です。

    - A: 正しい。
    - B: 誤り。名前空間は `s3tables` で、別の権限が必要です。
    - C: 誤り。Iceberg のメタデータと不整合を起こします。
    - D: 誤り。汎用バケットでは Glue のテーブル最適化の設定が必要です。

    **スキル:** [2.1.7](../domain2.md#skill-2-1-7) / **参照:** [S3 Tables](../../../services/data-engineering.md#s3-tables)、[Apache Iceberg](../../../services/data-engineering.md#iceberg)

### 問3 {#q3}

Iceberg と S3 Tables の説明として正しいものはどれですか。（2つ選択）

- A. S3 Tables のテーブルバケットのテーブルは公開できない
- B. 汎用バケットの Iceberg では、スナップショットを使えない
- C. S3 Tables の圧縮の既定の目標は 16 GB である
- D. Iceberg の列の追加には、すべてのファイルの書き直しが必要である
- E. 隠しパーティションにより、クエリは区分の列を意識しなくてよい

??? success "答えと解説"
    **正解: A, E**

    機能と保守の違いを押さえます。

    - A: 正しい。公開の設定はありません。
    - B: 誤り。使えます。
    - C: 誤り。既定は 512 MB です。
    - D: 誤り。書き直しは不要です。
    - E: 正しい。`dt` の条件の書き忘れが減ります。

    **スキル:** [2.1.7](../domain2.md#skill-2-1-7) / **参照:** [Apache Iceberg](../../../services/data-engineering.md#iceberg)、[S3 Tables](../../../services/data-engineering.md#s3-tables)

### 問4 {#q4}

ログを 30 日後に Standard-IA、120 日後に Glacier へ移します。正しい要素はどれですか。

- A. `AbortIncompleteMultipartUpload` に移行先を 2 つ書く
- B. `Transitions` に `Days` と `StorageClass` を 2 つ書く
- C. `NoncurrentVersionExpiration` に移行先を 2 つ書く
- D. `Expiration` に `Days` と `StorageClass` を 2 つ書く

??? success "答えと解説"
    **正解: B**

    移行は `Transitions` です。

    - A: 誤り。未完了のマルチパートの片付けです。
    - B: 正しい。
    - C: 誤り。非現行の削除の要素です。
    - D: 誤り。`Expiration` は失効で、移行ではありません。

    **スキル:** [2.3.2](../domain2.md#skill-2-3-2) / **参照:** [ライフサイクル](../../../services/s3.md#lifecycle)、[ストレージクラス](../../../services/s3.md#storage-classes)

### 問5 {#q5}

ライフサイクルで Deep Archive へ移したのに、64 KB のログファイルが移行されません。説明として正しいものはどれですか。

- A. Deep Archive へ移せるのは 1 GB 以上のオブジェクトだけである
- B. ライフサイクルは Standard のオブジェクトを移行できない
- C. 移行のルールは最初にバージョニングを有効にしないと動かない
- D. 128 KB 未満のオブジェクトは既定で移行しない

??? success "答えと解説"
    **正解: D**

    サイズのフィルターで変更できます。

    - A: 誤り。そのような制限はありません。
    - B: 誤り。移行できます。
    - C: 誤り。バージョニングは必須ではありません。
    - D: 正しい。

    **スキル:** [2.3.2](../domain2.md#skill-2-3-2) / **参照:** [ライフサイクル](../../../services/s3.md#lifecycle)

### 問6 {#q6}

アクセスの頻度が読めないデータの費用を下げます。また、Deep Archive にあるオブジェクトを Standard へ戻すライフサイクルのルールは作れますか。正しいものはどれですか。

- A. Glacier Instant Retrieval に移す。戻すルールは `Expiration` で作れる
- B. One Zone-IA に移す。戻すルールは `Transitions` に `STANDARD` を書けば作れる
- C. Deep Archive に移す。読めるようにするルールは `AbortIncompleteMultipartUpload` で作れる
- D. Intelligent-Tiering を検討する。移行は低コスト側への一方向なので、戻すルールは作れない

??? success "答えと解説"
    **正解: D**

    頻度が読めないなら Intelligent-Tiering です。

    - A: 誤り。`Expiration` は失効です。
    - B: 誤り。戻すルールは作れません。
    - C: 誤り。未完了のマルチパートの片付けです。
    - D: 正しい。

    **スキル:** [2.3.2](../domain2.md#skill-2-3-2) / **参照:** [ライフサイクル](../../../services/s3.md#lifecycle)、[ストレージクラス](../../../services/s3.md#storage-classes)

### 問7 {#q7}

バージョニングが有効なバケットに `Expiration` だけ設定しました。1 年後も費用が下がりません。なぜですか。

- A. `Expiration` の実行には毎回の手動の承認が必要で、それを待っているから
- B. 削除マーカーのサイズが元のオブジェクトと同じで課金されるから
- C. 現行バージョンに削除マーカーが付くだけで、実データは非現行として残るから
- D. `Expiration` はバージョニングが有効なバケットでは完全に無視されるから

??? success "答えと解説"
    **正解: C**

    実データを消すには `NoncurrentVersionExpiration` も設定します。

    - A: 誤り。承認は不要です。
    - B: 誤り。実データが残っていることが原因です。
    - C: 正しい。
    - D: 誤り。無視はされず、削除マーカーが付きます。

    **スキル:** [2.3.3](../domain2.md#skill-2-3-3) / **参照:** [ライフサイクルのルール要素](../../../services/s3.md#lifecycle-elements)

### 問8 {#q8}

バケットの費用に、中断したマルチパートアップロードの断片が含まれています。何で片付けますか。

- A. `ExpiredObjectDeleteMarker`
- B. `AbortIncompleteMultipartUpload`
- C. `Transitions`
- D. `NoncurrentVersionExpiration`

??? success "答えと解説"
    **正解: B**

    未完了のパートはライフサイクルで片付けます。

    - A: 誤り。不要な削除マーカーの片付けです。
    - B: 正しい。
    - C: 誤り。ストレージクラスの移行です。
    - D: 誤り。非現行バージョンの削除です。

    **スキル:** [2.3.3](../domain2.md#skill-2-3-3) / **参照:** [片付けの設定](../../../services/s3.md#abort-multipart)、[ライフサイクルのルール要素](../../../services/s3.md#lifecycle-elements)

### 問9 {#q9}

バージョニングのあるバケットで、期限切れのデータを完全に消し、残骸も残さない設定の組み合わせはどれですか。（2つ選択）

- A. `Transitions` の `GLACIER`
- B. `AbortIncompleteMultipartUpload` の日数を 0 にする設定
- C. `ExpiredObjectDeleteMarker`
- D. Object Lock のコンプライアンスモード
- E. `NoncurrentVersionExpiration`

??? success "答えと解説"
    **正解: C, E**

    `Expiration` と組み合わせます。

    - A: 誤り。移行で、削除しません。
    - B: 誤り。未完了のパートの片付けで、この残骸とは別です。
    - C: 正しい。不要になった削除マーカーを消します。
    - D: 誤り。削除を防ぐ機能です。
    - E: 正しい。非現行バージョンを完全に削除します。

    **スキル:** [2.3.3](../domain2.md#skill-2-3-3) / **参照:** [ライフサイクルのルール要素](../../../services/s3.md#lifecycle-elements)、[状態ごとの動作と削除マーカー](../../../services/s3.md#delete-markers)

### 問10 {#q10}

バージョニングのあるバケットで、誤ってオブジェクトを削除しました。バージョン ID は指定していません。元に戻す操作はどれですか。

- A. 削除マーカーのバージョン ID を指定して `DELETE` する
- B. 元のオブジェクトをもう一度アップロードする以外に方法はない
- C. バージョニングを無効に戻すと、自動で元に戻る
- D. ライフサイクルの `Expiration` を 0 日に設定し、前の状態に戻す

??? success "答えと解説"
    **正解: A**

    マーカーを消すと前のバージョンが現行に戻ります。

    - A: 正しい。
    - B: 誤り。前のバージョンが残っています。
    - C: 誤り。未設定には戻せず、停止だけできます。
    - D: 誤り。戻す操作ではありません。

    **スキル:** [2.3.4](../domain2.md#skill-2-3-4) / **参照:** [バージョニング](../../../services/s3.md#versioning)、[状態ごとの動作と削除マーカー](../../../services/s3.md#delete-markers)

### 問11 {#q11}

DynamoDB の TTL を設定しましたが、項目が削除されません。属性は ISO 8601 の文字列です。どう直しますか。

- A. 属性を Number 型のミリ秒の Unix エポック時刻にする
- B. テーブルをプロビジョンドにして WCU を増やす
- C. 属性を String 型のままにして、`UpdateTimeToLive` を再度実行する
- D. 属性を Number 型の秒単位の Unix エポック時刻にする

??? success "答えと解説"
    **正解: D**

    属性は秒単位の Number です。

    - A: 誤り。秒単位です。
    - B: 誤り。TTL の削除は WCU を消費しません。
    - C: 誤り。文字列では動きません。
    - D: 正しい。

    **スキル:** [2.3.4](../domain2.md#skill-2-3-4) / **参照:** [TTL](../../../services/dynamodb.md#ttl)

### 問12 {#q12}

TTL で項目が消える前後に、次の要件があります。正しい対応はどれですか。（2つ選択）

- A. 削除した項目を S3 に残すなら、Streams と Lambda で `userIdentity.type` が `Service` のレコードを処理する
- B. TTL の削除は WCU を大量に消費するので、容量を増やす
- C. TTL の削除は Streams に記録されないので、別のテーブルに控える
- D. 期限切れの瞬間に確実に消えるので、読み取りでは何も考慮しない
- E. 期限切れの直後に読ませたくないなら、フィルター式で除く

??? success "答えと解説"
    **正解: A, E**

    TTL の性質に合わせて設計します。

    - A: 正しい。TTL の削除を見分けられます。
    - B: 誤り。WCU を消費しません。
    - C: 誤り。Streams に記録されます。
    - D: 誤り。直後とは限りません。
    - E: 正しい。削除は通常数日以内で、期限直後ではありません。

    **スキル:** [2.3.4](../domain2.md#skill-2-3-4) / **参照:** [TTL](../../../services/dynamodb.md#ttl)、[DynamoDB Streams](../../../services/dynamodb.md#streams)

### 問13 {#q13}

バージョニングを有効にした分析バケットの費用が増えています。日次で同じキーを上書きしています。説明として正しいものはどれですか。

- A. 各バージョンが丸ごと課金されるので、古いバージョンを失効させる
- B. 上書きは新しいバージョンを作らないので、原因は別にある
- C. 差分だけが課金されるので、上書きの回数は費用に影響しない
- D. バージョニングを未設定に戻せば、古いバージョンが自動で消えて費用も戻る

??? success "答えと解説"
    **正解: A**

    `NoncurrentVersionExpiration` で古いバージョンを片付けます。

    - A: 正しい。
    - B: 誤り。新しいバージョンを作ります。
    - C: 誤り。丸ごと課金されます。
    - D: 誤り。未設定には戻せず、停止しても残ります。

    **スキル:** [2.3.4](../domain2.md#skill-2-3-4) / **参照:** [バージョニング](../../../services/s3.md#versioning)

### 問14 {#q14}

別のリージョンのバケットへレプリケーションしたいのに、設定できません。前提として確認するものはどれですか。

- A. 送信元のバケットの Intelligent-Tiering の設定
- B. 送信先のバケットのストレージクラスの設定
- C. 送信元と送信先の両方のバージョニング
- D. 送信先の Object Lock のコンプライアンスモード

??? success "答えと解説"
    **正解: C**

    レプリケーションにはバージョニングが必要です。

    - A: 誤り。前提ではありません。
    - B: 誤り。送信先のストレージクラスは選べますが、前提ではありません。
    - C: 正しい。
    - D: 誤り。前提ではありません。

    **スキル:** [2.3.4](../domain2.md#skill-2-3-4) / **参照:** [バージョニング](../../../services/s3.md#versioning)、[レプリケーション](../../../services/s3.md#replication)

### 問15 {#q15}

規制で、7 年間はルートユーザーを含めて誰もログを消せないようにします。どの設定ですか。

- A. ライフサイクルの `Expiration` を 7 年に設定する
- B. Object Lock のコンプライアンスモードで 7 年の保持期間を設定する
- C. Object Lock のガバナンスモードで 7 年の保持期間を設定する
- D. バージョニングだけを有効にして、削除マーカーで守る

??? success "答えと解説"
    **正解: B**

    コンプライアンスモードは誰も削除できません。

    - A: 誤り。7 年後に消す設定で、それまで消せないようにはしません。
    - B: 正しい。
    - C: 誤り。権限があれば解除や削除ができます。
    - D: 誤り。権限があれば削除できます。

    **スキル:** [2.3.5](../domain2.md#skill-2-3-5) / **参照:** [Object Lock](../../../services/s3.md#object-lock)

### 問16 {#q16}

訴訟の調査中のデータを、期限を決めずに残し、調査が終わったら解除します。どの機能ですか。

- A. コンプライアンスモードの固定の保持期間
- B. Object Lock のリーガルホールド
- C. MFA Delete の代わりに使う S3 Access Points のポリシー
- D. ライフサイクルの `Transitions` の Glacier への移行

??? success "答えと解説"
    **正解: B**

    外すまで有効で、保持期間とは独立しています。

    - A: 誤り。期間が決まっており、短縮もできません。
    - B: 正しい。
    - C: 誤り。別の機能です。
    - D: 誤り。削除を防ぐ機能ではありません。

    **スキル:** [2.3.5](../domain2.md#skill-2-3-5) / **参照:** [Object Lock](../../../services/s3.md#object-lock)

### 問17 {#q17}

GDPR の削除要求で、特定の人の行を消します。データは Iceberg とそのバックアップにあります。正しい考え方はどれですか。

- A. `DELETE` の代わりに、対象の行を読み飛ばすビューを作れば削除の要求を満たせる
- B. `DELETE` は不要で、カタログのテーブル定義を消せば実データも消える
- C. `DELETE` の後に古いスナップショットを失効させ、バックアップや複製の扱いも確認する
- D. `DELETE` を実行すれば、過去のスナップショットとバックアップからも同時に、即時に消える

??? success "答えと解説"
    **正解: C**

    実データの複製の場所まで確認します。

    - A: 誤り。実データが残ります。
    - B: 誤り。定義だけが消えます。
    - C: 正しい。
    - D: 誤り。スナップショットや複製には残ります。

    **スキル:** [2.3.5](../domain2.md#skill-2-3-5) / **参照:** [Apache Iceberg](../../../services/data-engineering.md#iceberg)、[AWS Backup](../../../services/resilience.md#backup)

### 問18 {#q18}

リージョンの障害に備え、S3 のデータを別のリージョンにも置きます。RPO は短くしたいです。どの機能ですか。

- A. クロスリージョンレプリケーション
- B. ライフサイクルで同じリージョンの Glacier へ移行する構成
- C. S3 バージョニングだけを同じバケットで有効にする構成
- D. 週次の手動のダウンロードと再アップロードの運用

??? success "答えと解説"
    **正解: A**

    継続的な複製で RPO を短くします。

    - A: 正しい。
    - B: 誤り。リージョンの障害には備えられません。
    - C: 誤り。リージョンの障害には備えられません。
    - D: 誤り。RPO が長くなります。

    **スキル:** [2.3.6](../domain2.md#skill-2-3-6) / **参照:** [レプリケーション](../../../services/s3.md#replication)、[RTO と RPO](../../../services/resilience.md#rto-rpo)

### 問19 {#q19}

RDS、DynamoDB、EFS のバックアップをまとめて管理し、別のリージョンへもコピーします。どのサービスですか。

- A. AWS Config
- B. AWS Glue
- C. AWS DataSync
- D. AWS Backup

??? success "答えと解説"
    **正解: D**

    複数のサービスのバックアップを一元管理します。

    - A: 誤り。設定の記録と評価のサービスです。
    - B: 誤り。データの変換のサービスです。
    - C: 誤り。ファイルの転送のサービスです。
    - D: 正しい。

    **スキル:** [2.3.6](../domain2.md#skill-2-3-6) / **参照:** [AWS Backup](../../../services/resilience.md#backup)、[バックアップと復元](../../../services/dynamodb.md#backup)

### 問20 {#q20}

誤操作で DynamoDB の項目を消しました。2 日前の時点へ戻します。何を有効にしておくべきでしたか。また Redshift の自動スナップショットの既定の保持はどれですか。

- A. DAX。Redshift の既定の保持は 7 日
- B. TTL。Redshift の既定の保持は無期限
- C. PITR（1〜35 日）。Redshift の既定の保持は 1 日
- D. グローバルテーブル。Redshift の既定の保持は 35 日

??? success "答えと解説"
    **正解: C**

    守りたいものに合う方法を選びます。

    - A: 誤り。DAX はキャッシュです。
    - B: 誤り。TTL は自動削除の機能です。
    - C: 正しい。
    - D: 誤り。グローバルテーブルは誤操作も複製します。

    **スキル:** [2.3.6](../domain2.md#skill-2-3-6) / **参照:** [バックアップと復元](../../../services/dynamodb.md#backup)、[サービスごとの Multi-AZ と Multi-Region](../../../services/resilience.md#patterns-by-service)

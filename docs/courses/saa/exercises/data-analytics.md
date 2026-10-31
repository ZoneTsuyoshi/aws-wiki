# データの取り込みと分析の問題集

対象の解説: [ストリーミング](../../../services/streaming.md)、[データエンジニアリング](../../../services/data-engineering.md)

### 問1 {#q1}

順序付きのイベントを、複数のアプリが独自のコードで読み、24 時間以内なら読み直します。どれを選びますか。

- A. Amazon Data Firehose の S3 への配信
- B. Kinesis Data Streams
- C. SQS 標準キューのロングポーリング
- D. Athena の CTAS の定期実行

??? success "答えと解説"
    **正解: B**

    シャードの順序を保ち、複数のコンシューマーが読めます。

    - A: 誤り。配信のサービスで、独自のコードで読み直せない。
    - B: 正しい。
    - C: 誤り。順序がなく、読み直せない。
    - D: 誤り。クエリで、ストリームの読み取りではない。

    **スキル:** [ストリーミング](../domain3.md#t3-5-streaming) / **参照:** [Kinesis Data Streams](../../../services/streaming.md#kinesis-data-streams)、[Kinesis Data Streams、Firehose、SQS の選び方](../../../services/streaming.md#choosing)

### 問2 {#q2}

ログを S3 と OpenSearch Service に、コードなしで配信します。数十秒の遅れは許せます。どれが最も少ない運用負荷ですか。

- A. EC2 と cron の構成
- B. Kinesis Data Streams と自作のコンシューマーの構成
- C. Amazon Data Firehose
- D. MSK と Kafka Connect の自己管理の構成

??? success "答えと解説"
    **正解: C**

    Firehose はバッファして配信します。ほぼリアルタイムです。

    - A: 誤り。運用負荷が大きい。
    - B: 誤り。コードの管理が必要。
    - C: 正しい。
    - D: 誤り。管理が多い。

    **スキル:** [ストリーミング](../domain3.md#t3-5-streaming) / **参照:** [Amazon Data Firehose](../../../services/streaming.md#firehose)

### 問3 {#q3}

毎秒 5,000 件、1 件 1 KB のイベントを Kinesis に書きます。プロビジョンドモードで最小のシャード数はいくつですか。

- A. 5 シャード
- B. 50 シャード
- C. 2 シャード
- D. 1 シャード

??? success "答えと解説"
    **正解: A**

    書き込みは 5 MB/秒です。読めないなら、オンデマンドを選びます。

    - A: 正しい。
    - B: 誤り。過剰。
    - C: 誤り。足りない。
    - D: 誤り。1 シャードは 1 MB/秒、1,000 レコード/秒まで。

    **スキル:** [ストリーミング](../domain3.md#t3-5-streaming) / **参照:** [シャードの容量](../../../services/streaming.md#shards)、[シャード数の計算](../../../services/streaming.md#shard-calculation)

### 問4 {#q4}

同じストリームを 5 つのコンシューマーが読み、読み取りの遅延が増えています。シャードの共有の 2 MB/秒が足りません。どうしますか。

- A. パーティションキーを 1 つに固定する
- B. 保持期間を 365 日に伸ばす
- C. Firehose のバッファを小さくする設定にする
- D. 拡張ファンアウトのコンシューマーに変える

??? success "答えと解説"
    **正解: D**

    コンシューマーごとに、シャードあたり 2 MB/秒を使えます。

    - A: 誤り。偏りが増えるだけで、読み取りの帯域は増えない。
    - B: 誤り。帯域は増えない。
    - C: 誤り。別のサービスの設定。
    - D: 正しい。

    **スキル:** [ストリーミング](../domain3.md#t3-5-streaming) / **参照:** [消費者と拡張ファンアウト](../../../services/streaming.md#enhanced-fan-out)

### 問5 {#q5}

Kinesis で一部のシャードだけが `ProvisionedThroughputExceededException` になります。合計の容量には余裕があります。原因と対策はどれですか。

- A. シャードの数が多すぎるので、半分に減らす
- B. コンシューマーが多すぎるので、拡張ファンアウトをやめる
- C. パーティションキーの偏りなので、値の種類を増やす
- D. 保持期間が短いので、期間を伸ばす

??? success "答えと解説"
    **正解: C**

    ホットシャードの問題です。

    - A: 誤り。悪化する。
    - B: 誤り。書き込みの問題ではない。
    - C: 正しい。
    - D: 誤り。書き込みの偏りに関係しない。

    **スキル:** [取り込みの設定](../domain3.md#t3-5-ingestion) / **参照:** [パーティションキー](../../../services/streaming.md#partition-key)

### 問6 {#q6}

取り込みの頻度に合わせた選択として正しいものはどれですか。

- A. 夜間の 1 回の SaaS の取り込みは、Kinesis Data Streams のシャードで行う
- B. 連続の秒単位の処理は、毎日の Glue のトリガーで行う
- C. 1 回だけの大量の移行は、常時動く MSK クラスターで行う
- D. 分単位の遅れが許せる配信は Firehose、定期の SaaS の取り込みは AppFlow

??? success "答えと解説"
    **正解: D**

    頻度と遅れの要件で選びます。

    - A: 誤り。定期のバッチには AppFlow など。
    - B: 誤り。連続の要件に合わない。
    - C: 誤り。過剰で、一括の移行は DataSync や DMS。
    - D: 正しい。

    **スキル:** [取り込みの設定](../domain3.md#t3-5-ingestion) / **参照:** [Kinesis Data Streams、Firehose、SQS の選び方](../../../services/streaming.md#choosing)、[Amazon AppFlow](../../../services/data-engineering.md#appflow)

### 問7 {#q7}

Firehose から S3 への配信で、小さなファイルが多く、Athena が遅くなっています。遅れは数分まで許せます。どの設定を変えますか。

- A. バッファのサイズと時間を大きくする
- B. S3 のストレージクラスを One Zone-IA に変える
- C. Kinesis のシャードを増やす設定に変える
- D. バケットのリージョンを変える

??? success "答えと解説"
    **正解: A**

    バッファを大きくするとファイルがまとまります。その分だけ遅れます。

    - A: 正しい。
    - B: 誤り。ファイルのサイズは変わらない。
    - C: 誤り。Firehose の配信の単位は変わらない。
    - D: 誤り。関係ない。

    **スキル:** [取り込みの設定](../domain3.md#t3-5-ingestion) / **参照:** [バッファ](../../../services/streaming.md#firehose-buffering)

### 問8 {#q8}

Kinesis Data Streams への取り込みを保護します。適切な組み合わせを選んでください。（3つ選択）

- A. シャードごとに SG を付けて送信元を制限する
- B. IAM で書き込みのプロデューサーを制限する
- C. 全プロデューサーで同じ IAM ユーザーのキーを共有する
- D. インターフェイスエンドポイントで VPC から接続する
- E. KMS でサーバー側の暗号化を有効にする
- F. パーティションキーで暗号化の鍵を切り替える

??? success "答えと解説"
    **正解: B, D, E**

    認可、暗号化、経路を組み合わせます。

    - A: 誤り。シャードに SG は付けられない。
    - B: 正しい。
    - C: 誤り。長期の認証情報の共有は不適切。
    - D: 正しい。
    - E: 正しい。
    - F: 誤り。キーの用途はシャードの割り当て。

    **スキル:** [取り込みポイントの保護](../domain3.md#t3-5-secure) / **参照:** [暗号化](../../../services/streaming.md#kinesis-encryption)、[VPC エンドポイントと PrivateLink](../../../services/networking.md#vpc-endpoints)

### 問9 {#q9}

モバイルアプリから S3 へ直接アップロードさせます。AWS の認証情報は渡さず、有効期限も短くします。どれを使いますか。

- A. IAM ユーザーのキーをアプリに埋め込む
- B. バックエンドで発行した署名付き URL
- C. バケットを一時的に公開する
- D. S3 ライフサイクルで書き込みの期限を定める

??? success "答えと解説"
    **正解: B**

    署名付き URL は期限があり、オブジェクトと操作を限定します。

    - A: 誤り。長期の認証情報を配ることになる。
    - B: 正しい。
    - C: 誤り。公開になる。
    - D: 誤り。書き込みの認可の機能ではない。

    **スキル:** [取り込みポイントの保護](../domain3.md#t3-5-secure) / **参照:** [署名付き URL](../../../services/s3.md#presigned-urls)

### 問10 {#q10}

SFTP の受け口を VPC の内部からだけ使わせます。利用者ごとに書き込めるプレフィックスも分けます。どう設定しますか。（2つ選択）

- A. 利用者ごとの IAM ロール
- B. CloudFront を前に置いて SFTP をキャッシュする
- C. Transfer Family の VPC エンドポイント
- D. パブリックのエンドポイントで全員に同じロールを使う
- E. EC2 の SFTP サーバーと共有のユーザーを使う

??? success "答えと解説"
    **正解: A, C**

    ロールとセッションポリシーで権限を分けられます。

    - A: 正しい。
    - B: 誤り。SFTP を扱えない。
    - C: 正しい。
    - D: 誤り。VPC の内部に限定されず、分離もできない。
    - E: 誤り。管理が多く、分離もできない。

    **スキル:** [取り込みポイントの保護](../domain3.md#t3-5-secure) / **参照:** [AWS Transfer Family](../../../services/migration.md#transfer-family)

### 問11 {#q11}

S3 のデータレイクのスキーマを自動で検出し、Athena からテーブルとして使います。どの組み合わせですか。

- A. Glue クローラーと Data Catalog
- B. Macie の検出ジョブと Security Hub の組み合わせ
- C. CloudTrail Lake と Config
- D. DMS の CDC と Schema Conversion の組み合わせ

??? success "答えと解説"
    **正解: A**

    クローラーがスキーマを推定し、カタログに登録します。

    - A: 正しい。
    - B: 誤り。機密データの発見と集約。
    - C: 誤り。監査の記録と評価の機能。
    - D: 誤り。DB の移行の機能。

    **スキル:** [データレイク](../domain3.md#t3-5-lake) / **参照:** [クローラー](../../../services/data-engineering.md#glue-crawlers)、[Data Catalog](../../../services/data-engineering.md#glue-data-catalog)

### 問12 {#q12}

データレイクの列と行の権限を、属性で多数のテーブルにまとめて付けます。別のアカウントとも共有します。どれが適切ですか。

- A. Glue のジョブのブックマークを使う
- B. Lake Formation の LF タグ
- C. IAM のユーザーをテーブルごとに作る
- D. S3 のバケットポリシーをプレフィックスごとに増やす

??? success "答えと解説"
    **正解: B**

    LF タグで権限をまとめられ、アカウント間の共有もできます。

    - A: 誤り。増分処理の機能。
    - B: 正しい。
    - C: 誤り。管理できず、列も分けられない。
    - D: 誤り。列や行の制御ができない。

    **スキル:** [データレイク](../domain3.md#t3-5-lake) / **参照:** [LF タグ](../../../services/data-engineering.md#lake-formation-lf-tags)

### 問13 {#q13}

データレイクのクエリの費用を下げ、日付で絞る処理も速くします。どの設計が適切ですか。

- A. 全データを 1 つの大きな CSV にまとめて置き続ける
- B. すべて Deep Archive に移す
- C. JSON のまま S3 の Standard に置いて、ファイルを増やし続ける
- D. Parquet に変換し、日付でパーティションする

??? success "答えと解説"
    **正解: D**

    列指向とパーティションでスキャン量を減らします。

    - A: 誤り。列も日付も絞れない。
    - B: 誤り。クエリできない。
    - C: 誤り。スキャン量が減らない。
    - D: 正しい。

    **スキル:** [データレイク](../domain3.md#t3-5-lake) / **参照:** [パーティション](../../../services/data-engineering.md#partitioning)、[データ形式](../../../services/data-engineering.md#data-formats)

### 問14 {#q14}

S3 の CSV を定期的に Parquet に変換します。サーバーレスの Spark で、カタログとも連携します。どれを選びますか。

- A. EC2 に Spark を手で構築して、毎晩起動する
- B. Athena のワークグループの設定を変更する
- C. Glue の ETL ジョブとスケジュールのトリガー
- D. Lambda の 1 回の実行で全データを変換する

??? success "答えと解説"
    **正解: C**

    Glue はサーバーレスの ETL です。

    - A: 誤り。管理が多い。
    - B: 誤り。変換の処理ではない。
    - C: 正しい。
    - D: 誤り。15 分の上限があり、大きな処理に向かない。

    **スキル:** [変換と形式](../domain3.md#t3-5-transform) / **参照:** [ETL ジョブ](../../../services/data-engineering.md#glue-jobs)

### 問15 {#q15}

S3 上のテーブルを、単発の SQL で Parquet に変換します。サーバーの準備はしません。どれが最も手軽ですか。

- A. Redshift の新しいクラスターにロードする
- B. EMR のクラスターを新しく作って実行する
- C. Athena の CTAS クエリを 1 回実行する
- D. Kinesis Data Streams にレコードを流し直す

??? success "答えと解説"
    **正解: C**

    CTAS はクエリの結果を指定の形式で S3 に書きます。

    - A: 誤り。単発には過剰。
    - B: 誤り。クラスターの準備が必要。
    - C: 正しい。
    - D: 誤り。目的に合わない。

    **スキル:** [変換と形式](../domain3.md#t3-5-transform) / **参照:** [Amazon Athena](../../../services/streaming.md#athena)

### 問16 {#q16}

Firehose で受ける JSON を、配信のときに Parquet に変えます。どの機能を使いますか。

- A. Logs のメトリクスフィルター
- B. S3 Batch Operations のコピー
- C. S3 のライフサイクルルールの移行アクション
- D. Firehose のレコード形式の変換

??? success "答えと解説"
    **正解: D**

    Firehose は Glue のカタログのスキーマを使って変換します。

    - A: 誤り。ログの数値化の機能。
    - B: 誤り。形式の変換の機能ではない。
    - C: 誤り。クラスの移行で、形式は変えない。
    - D: 正しい。

    **スキル:** [変換と形式](../domain3.md#t3-5-transform) / **参照:** [その他の機能](../../../services/streaming.md#firehose-features)

### 問17 {#q17}

既存の Spark のジョブで、ノードの費用を下げます。一部のノードの中断は許せます。データは S3 にあります。どのノードを Spot にしますか。

- A. タスクノード
- B. HDFS を持つコアノードだけ
- C. クラスターのすべてのノード
- D. プライマリノード

??? success "答えと解説"
    **正解: A**

    タスクノードは HDFS を持たないので、Spot に向きます。

    - A: 正しい。
    - B: 誤り。HDFS のデータを失うリスクがある。
    - C: 誤り。プライマリの中断で全体が止まる。
    - D: 誤り。失うとクラスターに影響する。

    **スキル:** [データ処理](../domain3.md#t3-5-compute) / **参照:** [クラスターのノード](../../../services/data-engineering.md#emr-nodes)

### 問18 {#q18}

不定期に実行する Spark のジョブで、クラスターを管理せず、EMR のランタイムを使います。どれを選びますか。

- A. EMR on EC2 の常時稼働のクラスター
- B. EMR Serverless のアプリケーション
- C. ElastiCache のクラスターに処理を載せた構成
- D. EC2 上の自前の Spark

??? success "答えと解説"
    **正解: B**

    EMR Serverless はクラスターを持たずに実行できます。

    - A: 誤り。管理と待機の費用がかかる。
    - B: 正しい。
    - C: 誤り。用途が違う。
    - D: 誤り。管理が多い。

    **スキル:** [データ処理](../domain3.md#t3-5-compute) / **参照:** [EMR Serverless](../../../services/data-engineering.md#emr-serverless)

### 問19 {#q19}

EMR クラスターを止めてもデータを失わず、ジョブのときだけ起動します。データはどこに置きますか。

- A. インスタンスストア
- B. プライマリノードの EBS
- C. S3（EMRFS）
- D. コアノードの HDFS

??? success "答えと解説"
    **正解: C**

    S3 に置けば、計算とストレージを分けられます。

    - A: 誤り。同様に消える。
    - B: 誤り。クラスターと共に消える。
    - C: 正しい。
    - D: 誤り。クラスターを終了すると消える。

    **スキル:** [データ処理](../domain3.md#t3-5-compute) / **参照:** [HDFS と S3](../../../services/data-engineering.md#emr-hdfs-vs-s3)

### 問20 {#q20}

S3 のログに単発の SQL を投げます。インフラの準備はしません。どれを選びますか。

- A. Athena
- B. OpenSearch Service のドメイン
- C. RDS for PostgreSQL にすべてロードして実行
- D. Redshift のプロビジョンドクラスター

??? success "答えと解説"
    **正解: A**

    Athena はサーバーレスで、スキャン量で課金されます。

    - A: 正しい。
    - B: 誤り。取り込みとドメインの管理が要る。
    - C: 誤り。準備が必要。
    - D: 誤り。準備が必要で、定常の BI に向く。

    **スキル:** [分析と可視化](../domain3.md#t3-5-analytics) / **参照:** [Amazon Athena](../../../services/streaming.md#athena)

### 問21 {#q21}

業務のダッシュボードで、Athena のクエリの費用を抑えつつ表示を速くします。最新性は 1 時間前で十分です。どの設定が適切ですか。

- A. CloudWatch ダッシュボードに CSV を貼り付ける
- B. 直接クエリで全利用者のアクセスごとに実行する
- C. Managed Grafana のアラートを多数作成する
- D. Quick Sight の SPICE に定期的に取り込む

??? success "答えと解説"
    **正解: D**

    SPICE はインメモリに取り込むので、速く、Athena の費用も抑えられます。

    - A: 誤り。業務の BI に合わない。
    - B: 誤り。費用が増える。
    - C: 誤り。運用のメトリクスの可視化。
    - D: 正しい。

    **スキル:** [分析と可視化](../domain3.md#t3-5-analytics) / **参照:** [Amazon Quick Sight](../../../services/data-engineering.md#quick-sight)

### 問22 {#q22}

ダッシュボードで、地域の担当者には自分の地域の行だけを見せます。どの機能ですか。

- A. CloudFront の地理的制限で国を限定する
- B. Quick Sight の行レベルセキュリティ
- C. WAF のルールでダッシュボードの行を除外する
- D. S3 のバケットポリシーで行を限定する

??? success "答えと解説"
    **正解: B**

    ユーザーごとに見える行を制限できます。

    - A: 誤り。配信の国の制限。
    - B: 正しい。
    - C: 誤り。表示の行を扱えない。
    - D: 誤り。オブジェクトの単位で、行は限定できない。

    **スキル:** [分析と可視化](../domain3.md#t3-5-analytics) / **参照:** [Amazon Quick Sight](../../../services/data-engineering.md#quick-sight)

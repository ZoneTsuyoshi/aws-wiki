# 移行とデータ転送の問題集

対象の解説: [移行と転送](../../../services/migration.md)

### 問1 {#q1}

オンプレミスのアプリが NFS でファイルを書き、クラウド側ではそのファイルを S3 のオブジェクトとして分析します。どれを選びますか。

- A. Volume Gateway の保管型で iSCSI を使う構成
- B. S3 File Gateway の NFS 共有
- C. Tape Gateway
- D. Direct Connect のホスト接続だけを追加する構成

??? success "答えと解説"
    **正解: B**

    NFS、SMB でファイルを書き、S3 に保存します。

    - A: 誤り。ブロックで、S3 のオブジェクトとして使えない。
    - B: 正しい。
    - C: 誤り。バックアップソフト向け。
    - D: 誤り。接続の手段で、NFS を S3 に変換しない。

    **スキル:** [ハイブリッドストレージ](../domain3.md#t3-1-hybrid) / **参照:** [AWS Storage Gateway](../../../services/migration.md#storage-gateway)

### 問2 {#q2}

オンプレミスのストレージの容量は増やさず、頻繁に使うデータだけをローカルに置いて iSCSI で使います。全データは AWS にあります。どれを選びますか。

- A. Volume Gateway のキャッシュ型
- B. Volume Gateway の保管型
- C. DataSync のエージェントと定期タスク
- D. S3 File Gateway の SMB 共有

??? success "答えと解説"
    **正解: A**

    キャッシュ型は頻繁に使う部分だけをローカルに置きます。

    - A: 正しい。
    - B: 誤り。全データをローカルに置く型で、容量が必要。
    - C: 誤り。転送で、iSCSI のボリュームを提供しない。
    - D: 誤り。ファイルのプロトコルで、iSCSI ではない。

    **スキル:** [ハイブリッドストレージ](../domain3.md#t3-1-hybrid) / **参照:** [AWS Storage Gateway](../../../services/migration.md#storage-gateway)

### 問3 {#q3}

既存のバックアップソフトをそのまま使い、物理テープをやめます。どれを選びますか。

- A. DataSync のコピー
- B. AWS Backup の Vault Lock だけを有効にする構成
- C. Tape Gateway の仮想テープライブラリ
- D. S3 File Gateway に手でコピーする構成

??? success "答えと解説"
    **正解: C**

    Tape Gateway は仮想テープを iSCSI で提供し、既存のソフトを変えずに使えます。

    - A: 誤り。テープの置き換えにならない。
    - B: 誤り。テープのインターフェイスを提供しない。
    - C: 正しい。
    - D: 誤り。ソフトの変更を伴う。

    **スキル:** [ハイブリッドストレージ](../domain3.md#t3-1-hybrid) / **参照:** [AWS Storage Gateway](../../../services/migration.md#storage-gateway)

### 問4 {#q4}

NAS の 50 TB を S3 に移し、切り替えまで毎週差分を同期します。帯域の制限やスケジュールも設定します。どれを選びますか。

- A. Transfer Family の SFTP サーバーから手で転送する構成
- B. S3 コンソールからのアップロード
- C. Storage Gateway の S3 File Gateway にアプリを切り替える構成
- D. DataSync のエージェントとスケジュールのタスク

??? success "答えと解説"
    **正解: D**

    DataSync は NFS、SMB、HDFS などから AWS へ、スケジュールで転送します。

    - A: 誤り。外部の取引先向けのプロトコルの提供。
    - B: 誤り。大量のファイルに向かず、差分の同期もない。
    - C: 誤り。オンプレミスのアプリが使い続けるためのもの。
    - D: 正しい。

    **スキル:** [データ転送](../domain3.md#t3-5-transfer) / **参照:** [AWS DataSync](../../../services/migration.md#datasync)

### 問5 {#q5}

取引先が今の SFTP の手順を変えずにファイルを送り、S3 に保存します。どれを選びますか。

- A. Kinesis Data Firehose に PutRecord で送らせる構成
- B. Transfer Family の SFTP サーバー
- C. 署名付き URL のメール配布
- D. DataSync のエージェントを取引先に配布する構成

??? success "答えと解説"
    **正解: B**

    Transfer Family は SFTP、FTPS、FTP、AS2 を提供します。

    - A: 誤り。プロトコルの変更が要る。
    - B: 正しい。
    - C: 誤り。手順の変更が要る。
    - D: 誤り。取引先の変更が要る。

    **スキル:** [データ転送](../domain3.md#t3-5-transfer) / **参照:** [AWS Transfer Family](../../../services/migration.md#transfer-family)

### 問6 {#q6}

第三者の市場データのセットを購読し、更新を AWS で受け取ります。どれを使いますか。

- A. Transfer Family で提供者から SFTP で受ける構成
- B. AppFlow の接続を SaaS ごとに作る構成
- C. AWS Data Exchange
- D. Glue クローラーの実行

??? success "答えと解説"
    **正解: C**

    Data Exchange は第三者のデータを購読します。

    - A: 誤り。購読の仕組みがない。
    - B: 誤り。自社の SaaS からのデータの流れを作るもの。
    - C: 正しい。
    - D: 誤り。スキーマの検出で、購読ではない。

    **スキル:** [データ転送](../domain3.md#t3-5-transfer) / **参照:** [AWS Data Exchange](../../../services/data-engineering.md#data-exchange)

### 問7 {#q7}

1 Gbps の回線を利用率 80% で 24 時間使うとき、100 TB の転送にかかる日数はおよそどれですか。

- A. 約 12 日
- B. 約 120 日
- C. 約 50 日
- D. 約 1 日

??? success "答えと解説"
    **正解: A**

    `(100×10^12×8) ÷ (10^9×0.8×86400)` で約 11.6 日です。

    - A: 正しい。
    - B: 誤り。計算が合わない。
    - C: 誤り。計算が合わない。
    - D: 誤り。計算が合わない。

    **スキル:** [データの移行](../domain4.md#t4-1-transfer) / **参照:** [計算式](../../../services/migration.md#transfer-formula)

### 問8 {#q8}

既存の回線で期限内に転送できることを計算で確かめました。ファイルサーバーを最も安く EFS に移します。どれを選びますか。

- A. 新しく 10 Gbps の Direct Connect を契約する
- B. 別のリージョンの EC2 を経由して NFS でコピーする
- C. Storage Gateway の Volume Gateway に切り替える
- D. DataSync で転送する

??? success "答えと解説"
    **正解: D**

    データの受信の転送料はかかりません。回線が足りるなら、追加の回線は要りません。

    - A: 誤り。回線が足りるのに費用が増える。
    - B: 誤り。無駄な転送料がかかる。
    - C: 誤り。移行のサービスではなく、EFS にも移らない。
    - D: 正しい。

    **スキル:** [データの移行](../domain4.md#t4-1-transfer) / **参照:** [AWS DataSync](../../../services/migration.md#datasync)、[転送方法の選び方と時間の計算](../../../services/migration.md#choosing-transfer)

### 問9 {#q9}

期限に間に合わず、回線の増強はできます。データは 1 回だけ移します。最も費用を抑える選択はどれですか。

- A. 期間限定の Direct Connect と DataSync を使う
- B. 転送の間だけ S3 Transfer Acceleration を使う
- C. インターネット経由の VPN を 8 本束ねて、回線は今のままにする
- D. 長期契約の新しい回線を拠点ごとに複数引く

??? success "答えと解説"
    **正解: A**

    回線が足りないなら、必要な期間だけ増やします。

    - A: 正しい。
    - B: 誤り。回線の帯域を増やさない。
    - C: 誤り。回線の帯域の上限は変わらない。
    - D: 誤り。1 回の移行には過剰。

    **スキル:** [データの移行](../domain4.md#t4-1-transfer) / **参照:** [転送方法の選び方と時間の計算](../../../services/migration.md#choosing-transfer)

### 問10 {#q10}

新規の顧客が、回線に乗らない数百 TB を移します。Snow Family は新規のお客様に提供されていません。実務の代替として適切なものはどれですか。

- A. Snowball Edge を今から契約して発送を依頼する
- B. AWS Data Transfer Terminal
- C. CloudFront のアップロード
- D. S3 Transfer Acceleration だけで回線に流す

??? success "答えと解説"
    **正解: B**

    Data Transfer Terminal は施設に持ち込んで、高速に AWS へ転送します。現在は Enterprise Support のお客様が対象です。パートナーのオフライン転送も候補です。

    - A: 誤り。新規のお客様には提供されない。
    - B: 正しい。
    - C: 誤り。大容量の一括転送の手段ではない。
    - D: 誤り。回線に乗らないという問題を解決しない。

    **スキル:** [データの移行](../domain4.md#t4-1-transfer) / **参照:** [AWS Data Transfer Terminal](../../../services/migration.md#data-transfer-terminal)、[Snow Family の現在の状況](../../../services/migration.md#snow-family)

### 問11 {#q11}

オンプレミスのサーバーをブロック単位で継続して複製し、短い停止で EC2 に移します。どれを選びますか。

- A. DataSync のファイルの転送タスク
- B. DMS の `full-load-and-cdc` タスク
- C. Elastic Beanstalk の環境のクローン
- D. Application Migration Service（AWS Transform MGN）

??? success "答えと解説"
    **正解: D**

    ブロック単位の継続的な複製でサーバーを EC2 に移します。

    - A: 誤り。ファイルの転送で、サーバーを移せない。
    - B: 誤り。データベースの移行のサービス。
    - C: 誤り。既存の環境の複製の機能。
    - D: 正しい。

    **スキル:** [データの移行](../domain4.md#t4-1-transfer) / **参照:** [AWS Transform MGN(旧 Application Migration Service)](../../../services/migration.md#mgn)

### 問12 {#q12}

Oracle から Aurora PostgreSQL へ移します。ストアドプロシージャも変換します。正しい組み合わせを選んでください。（2つ選択）

- A. DMS だけで、データとストアドプロシージャの両方を変換して移す
- B. SCT か DMS Schema Conversion でスキーマを変換する
- C. SCT だけで、スキーマとデータの両方をすべて移す
- D. Glue クローラーでスキーマを作って、Athena で複製する
- E. DMS でデータを移す

??? success "答えと解説"
    **正解: B, E**

    スキーマは変換のツール、データは DMS と役割が分かれます。

    - A: 誤り。DMS だけではストアドプロシージャを変換できない。
    - B: 正しい。
    - C: 誤り。SCT はスキーマとコードが主で、データは DMS で移す。
    - D: 誤り。異種間の DB の移行の手順ではない。
    - E: 正しい。

    **スキル:** [スキーマの移行](../domain4.md#t4-3-migration) / **参照:** [AWS SCT と DMS Schema Conversion](../../../services/migration.md#sct)、[AWS DMS](../../../services/migration.md#dms)

### 問13 {#q13}

オンプレミスの MySQL を Aurora MySQL へ、停止を最小にして移します。どの設定ですか。

- A. SCT でスキーマを変換し、DMS の `full-load` で移す
- B. 夜間に mysqldump の結果をすべて手で流し込む
- C. DMS の `full-load-and-cdc`
- D. DMS の `cdc` だけで最初から移す

??? success "答えと解説"
    **正解: C**

    全量のあと差分を流し続け、短い停止で切り替えます。

    - A: 誤り。同種間なので変換は要らず、差分も移せない。
    - B: 誤り。停止が長くなる。
    - C: 正しい。
    - D: 誤り。初期データが移らない。

    **スキル:** [スキーマの移行](../domain4.md#t4-3-migration) / **参照:** [移行タイプ](../../../services/migration.md#dms-migration-types)

### 問14 {#q14}

RDS の DB を別のリージョンへ移します。スナップショットを使う以外の方法として適切なものはどれですか。

- A. クロスリージョンリードレプリカを作り、昇格する
- B. インスタンスタイプの変更でリージョンを指定する
- C. Multi-AZ のスタンバイの移動
- D. RDS Proxy の接続先を別のリージョンに変える

??? success "答えと解説"
    **正解: A**

    レプリカを昇格すれば独立した DB になります。

    - A: 正しい。
    - B: 誤り。そのような操作はない。
    - C: 誤り。スタンバイは同じリージョンの中。
    - D: 誤り。データは移らない。

    **スキル:** [スキーマの移行](../domain4.md#t4-3-migration) / **参照:** [リードレプリカと Multi-AZ](../../../services/databases.md#read-replicas)

# バッチ取り込みと接続の問題集

対象の解説: [AWS Glue](../../../services/data-engineering.md#glue)、[COPY と UNLOAD](../../../services/data-engineering.md#redshift-copy)、[移行と転送](../../../services/migration.md)

### 問1 {#q1}

営業部門は Salesforce のデータを毎晩 S3 へ増分で取り込みたいです。開発者はおらず、コードは書きません。何を選びますか。

- A. AppFlow のスケジュール実行で増分の転送を設定する
- B. Lambda で Salesforce の API を呼び、EventBridge Scheduler で毎晩起動する
- C. DMS の CDC タスクで、Salesforce をソースエンドポイントにする
- D. EMR のクラスターを毎晩起動し、Spark のコネクターで読み取る

??? success "答えと解説"
    **正解: A**

    AppFlow は、対応 SaaS からのコード不要の転送に向きます。

    - A: 正しい。
    - B: 誤り。動きますが、コードの作成と保守が必要です。
    - C: 誤り。DMS はデータベースの移行と複製のサービスです。
    - D: 誤り。クラスターの準備とコードが必要です。

    **スキル:** [1.1.2](../domain1.md#skill-1-1-2) / **参照:** [Amazon AppFlow](../../../services/data-engineering.md#appflow)、[変換エンジン](../../../services/data-engineering.md#choosing-transform)

### 問2 {#q2}

オンプレミスの PostgreSQL 10 TB を Aurora へ移します。切り替えまでの間に発生する変更も反映し、停止時間を短くします。DMS の移行タイプはどれですか。

- A. 全件ロードのみ
- B. 全件ロードと CDC
- C. スキーマ変換のみ
- D. CDC のみ

??? success "答えと解説"
    **正解: B**

    全件ロードの後に変更を適用し続ければ、短い停止で切り替えられます。

    - A: 誤り。移行中の変更が反映されません。
    - B: 正しい。
    - C: 誤り。DMS の移行タイプではなく、データも移りません。
    - D: 誤り。既存の 10 TB が移りません。

    **スキル:** [1.1.2](../domain1.md#skill-1-1-2) / **参照:** [移行タイプ](../../../services/migration.md#dms-migration-types)、[AWS DMS](../../../services/migration.md#dms)

### 問3 {#q3}

Redshift の集計結果を、SaaS の連携先が読む S3 へ毎日 CSV 以外の列指向形式で渡します。追加のサーバーは使いません。正しい方法はどれですか。

- A. Spectrum の外部テーブルに `INSERT` しないまま、`SELECT` の結果を自動で S3 へ保存させる
- B. `UNLOAD` を既定のまま実行し、拡張子だけ `.parquet` に変更する
- C. `UNLOAD` に `FORMAT AS PARQUET` を指定して S3 へ出力する
- D. `COPY` に `FORMAT AS PARQUET` を指定して S3 へ書き出す

??? success "答えと解説"
    **正解: C**

    `UNLOAD` の形式は `FORMAT` で指定します。

    - A: 誤り。`SELECT` だけでは S3 にファイルは出力されません。
    - B: 誤り。既定はパイプ区切りのテキストで、形式は変わりません。
    - C: 正しい。
    - D: 誤り。`COPY` は S3 から Redshift へのロードです。

    **スキル:** [1.1.2](../domain1.md#skill-1-1-2) / **参照:** [COPY と UNLOAD](../../../services/data-engineering.md#redshift-copy)、[データの共有](../../../services/data-engineering.md#choosing-sharing)

### 問4 {#q4}

毎日実行する Glue ジョブが、S3 の全ファイルを読み直しています。新しく届いたファイルだけを処理したいです。設定はどれですか。

- A. 実行クラスを Flex にして、開始を遅らせる
- B. 最大同時実行数を 2 にして、前回の実行と並べて動かす
- C. `--job-bookmark-option` を `job-bookmark-pause` にして状態を保持する
- D. `--job-bookmark-option` を `job-bookmark-enable` にする

??? success "答えと解説"
    **正解: D**

    ブックマークの既定は無効です。有効にすると続きから処理します。

    - A: 誤り。費用の設定で、処理対象は変わりません。
    - B: 誤り。ブックマークは同時実行に対応していません。
    - C: 誤り。状態を読みますが更新しないので、位置が進みません。
    - D: 正しい。

    **スキル:** [1.1.3](../domain1.md#skill-1-1-3) / **参照:** [ジョブのブックマーク](../../../services/data-engineering.md#glue-bookmarks)、[ETL ジョブ](../../../services/data-engineering.md#glue-jobs)

### 問5 {#q5}

Glue ジョブが 1 KB 程度のファイル数十万個を読むとき、ドライバーが OOM で失敗します。ワーカーの数は十分です。接続オプションの変更はどれですか。

- A. `push_down_predicate` に常に真になる条件を指定する
- B. `enableUpdateCatalog` を有効にし、カタログへ書き戻す
- C. `groupFiles` を `inPartition` にする
- D. `transformation_ctx` を読み取りの呼び出しから取り除く

??? success "答えと解説"
    **正解: C**

    大量の小さなファイルの一覧でドライバーのメモリが不足します。

    - A: 誤り。読むパーティションは減らず、ファイル数も変わりません。
    - B: 誤り。書き込み時のパーティション追加で、読み取りのメモリには効きません。
    - C: 正しい。
    - D: 誤り。ブックマークの設定で、メモリには効きません。

    **スキル:** [1.1.3](../domain1.md#skill-1-1-3) / **参照:** [DPU とワーカータイプ](../../../services/data-engineering.md#glue-dpu)

### 問6 {#q6}

夜間の `COPY` で、前日のファイルのうち 1 つが欠けていても成功してしまいました。指定したファイルが揃わなければ失敗させたいです。どうしますか。

- A. `NOLOAD` を付けて実行し、検証の結果を見てからロードする
- B. `MANIFEST` を使い、`mandatory` は既定のまま、ファイルの一覧だけを指定する
- C. `MAXERROR` を 0 に設定し、1 行でも不良があれば失敗させる
- D. `MANIFEST` を使い、各エントリの `mandatory` を `true` にする

??? success "答えと解説"
    **正解: D**

    マニフェストの `mandatory` の既定は `false` です。

    - A: 誤り。データの検証であり、欠けたファイルは検出できません。
    - B: 誤り。既定は `false` で、欠けていても失敗しません。
    - C: 誤り。既定値であり、行の不良の扱いで、ファイルの欠落は判定しません。
    - D: 正しい。

    **スキル:** [1.1.3](../domain1.md#skill-1-1-3) / **参照:** [COPY と UNLOAD](../../../services/data-engineering.md#redshift-copy)

### 問7 {#q7}

16 スライスのクラスターへ 1 つの大きな gzip ファイルを `COPY` すると遅いです。ロードを速くする方法はどれですか。

- A. ファイルをサイズのそろった 16 個に分割し、1 回の `COPY` で読む
- B. ファイルをサイズのそろった 15 個に分割し、ファイルごとに別の `COPY` を実行する
- C. 1 つのファイルのまま、`COPY` を 16 個のセッションで同時に実行する
- D. `INSERT` の複数行の文に変換し、スライスごとに送る

??? success "答えと解説"
    **正解: A**

    圧縮ファイルは分割し、ファイル数をスライス数の倍数にします。

    - A: 正しい。
    - B: 誤り。スライス数の倍数ではなく、別々の `COPY` では並列に読めません。
    - C: 誤り。同時に複数の `COPY` を実行すると直列になり、遅くなります。
    - D: 誤り。`COPY` より大幅に遅くなります。

    **スキル:** [1.1.3](../domain1.md#skill-1-1-3) / **参照:** [COPY と UNLOAD](../../../services/data-engineering.md#redshift-copy)、[構成](../../../services/data-engineering.md#redshift-architecture)

### 問8 {#q8}

VPC 内の Glue ジョブから取引先の API を呼びます。取引先は接続元 IP の許可リストを要求します。どうしますか。

- A. S3 のゲートウェイエンドポイントを追加し、経路を固定する
- B. NAT ゲートウェイの Elastic IP を許可リストに登録する
- C. Glue のワーカーの ENI の IP を調べて、取引先に登録してもらう
- D. セキュリティグループの ID を取引先に伝え、許可してもらう

??? success "答えと解説"
    **正解: B**

    固定の出口が必要なら NAT ゲートウェイを通します。

    - A: 誤り。S3 への経路で、取引先への通信には使えません。
    - B: 正しい。
    - C: 誤り。出口の IP は固定されません。
    - D: 誤り。別のネットワークのセキュリティグループは参照できません。

    **スキル:** [1.1.8](../domain1.md#skill-1-1-8) / **参照:** [NAT と Elastic IP](../../../services/network-connectivity.md#nat-eip)、[セキュリティグループのルール](../../../services/networking.md#security-group-rules)

### 問9 {#q9}

SFTP で S3 へ納品する取引先を、接続元 IP で制限します。Transfer Family のエンドポイントはどう構成しますか。

- A. VPC でホストするインターネット向けのエンドポイントにし、Elastic IP を割り当て、セキュリティグループで制限する
- B. 公開エンドポイントのまま、エンドポイントにセキュリティグループを関連付ける
- C. VPC の内部向けのエンドポイントにし、取引先にはインターネットから接続してもらう
- D. 公開エンドポイントのまま、S3 のバケットポリシーの `aws:SourceIp` に取引先の IP を書いて接続元を絞る

??? success "答えと解説"
    **正解: A**

    接続元の限定には VPC ホストのエンドポイントを使います。

    - A: 正しい。
    - B: 誤り。公開エンドポイントはセキュリティグループで制限できません。
    - C: 誤り。内部向けにはインターネットから到達できません。
    - D: 誤り。バケットへの接続元は取引先ではないので、取引先の制限になりません。

    **スキル:** [1.1.8](../domain1.md#skill-1-1-8) / **参照:** [AWS Transfer Family](../../../services/migration.md#transfer-family)、[セキュリティグループのルール](../../../services/networking.md#security-group-rules)

### 問10 {#q10}

バケットポリシーの `aws:SourceIp` で社内の CIDR だけ許可しました。VPC の S3 ゲートウェイエンドポイントを経由する EC2 からのアクセスが拒否されます。適切な修正はどれですか。

- A. Enhanced VPC Routing をバケットで有効にする
- B. `aws:SourceVpce` で、そのエンドポイントからのアクセスを許可する条件を加える
- C. `aws:SourceIp` にインスタンスのプライベート IP を追加する
- D. エンドポイントポリシーを削除し、既定のフルアクセスに戻す

??? success "答えと解説"
    **正解: B**

    VPC エンドポイント経由には `aws:SourceVpce` を使います。

    - A: 誤り。Redshift の機能で、S3 バケットの設定ではありません。
    - B: 正しい。
    - C: 誤り。エンドポイント経由には `aws:SourceIp` のパブリック IP の条件は効かず、プライベート IP の指定もこの場合の解決策として不適切です。
    - D: 誤り。拒否しているのはバケットポリシーです。

    **スキル:** [1.1.8](../domain1.md#skill-1-1-8) / **参照:** [エンドポイントポリシー](../../../services/networking.md#endpoint-policies)、[バケットポリシーとアクセス制御](../../../services/s3.md#bucket-policies)

### 問11 {#q11}

VPC 内の RDS を読む Glue ジョブが、接続テストで失敗します。ジョブのセキュリティグループの設定で、Glue の部品同士の通信に必要なものはどれですか。

- A. すべての TCP を、すべての送信元から許可するインバウンドルール
- B. データベースのポートだけを、VPC の CIDR から許可するアウトバウンドルール
- C. すべての TCP を、同じセキュリティグループから許可する自己参照ルール
- D. S3 のプレフィックスリストへの HTTPS を許可するインバウンドルール

??? success "答えと解説"
    **正解: C**

    自己参照ルールは同じセキュリティグループだけを許可します。

    - A: 誤り。通信はできますが、不要に公開します。
    - B: 誤り。部品同士の通信が許可されず、失敗します。
    - C: 正しい。
    - D: 誤り。S3 へはアウトバウンドで、部品同士の通信にはなりません。

    **スキル:** [1.2.2](../domain1.md#skill-1-2-2) / **参照:** [AWS Glue](../../../services/data-engineering.md#glue)、[セキュリティグループのルール](../../../services/networking.md#security-group-rules)

### 問12 {#q12}

JDBC の Glue ジョブを、インターネットへの経路のないプライベートサブネットで動かします。スクリプトは S3 にあり、起動後に読めず失敗します。何を追加しますか。

- A. データベースのリードレプリカ
- B. 別のリージョンの S3 クロスリージョンレプリケーション
- C. RDS Proxy のエンドポイント
- D. S3 のゲートウェイ VPC エンドポイント

??? success "答えと解説"
    **正解: D**

    VPC 内の Glue ジョブが S3 を読むには経路が必要です。

    - A: 誤り。S3 への経路とは関係しません。
    - B: 誤り。オブジェクトの複製で、VPC からの経路は作りません。
    - C: 誤り。データベース接続の共有で、S3 への経路は作りません。
    - D: 正しい。

    **スキル:** [1.2.2](../domain1.md#skill-1-2-2) / **参照:** [AWS Glue](../../../services/data-engineering.md#glue)、[VPC エンドポイントと PrivateLink](../../../services/networking.md#vpc-endpoints)

### 問13 {#q13}

BI ツールと Java のレポートアプリから、Athena と Redshift へ接続します。どのドライバーの説明が正しいですか。

- A. Java は JDBC、他の言語や BI ツールは ODBC を使い、Athena と Redshift は両方を提供する
- B. Redshift は ODBC だけで、Java のアプリからは接続できない
- C. Athena は HTTP の API だけに対応し、JDBC と ODBC のドライバーはどちらの言語向けにも提供されていない
- D. JDBC と ODBC の接続には、必ず Glue 接続の作成が必要である

??? success "答えと解説"
    **正解: A**

    JDBC は Java、ODBC はそれ以外の言語や BI ツールが使う標準です。

    - A: 正しい。
    - B: 誤り。JDBC ドライバーも提供されています。
    - C: 誤り。どちらのドライバーも提供されています。
    - D: 誤り。Glue 接続は Glue のクローラーとジョブのためのものです。

    **スキル:** [1.2.2](../domain1.md#skill-1-2-2) / **参照:** [AWS Glue](../../../services/data-engineering.md#glue)、[Amazon Redshift](../../../services/data-engineering.md#redshift)

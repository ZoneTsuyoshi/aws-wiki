# データベース の問題集

対象の解説: [データベース](../../../services/databases.md)、[DynamoDB](../../../services/dynamodb.md)、[専用データベース](../../../services/databases-specialized.md)、[移行サービス](../../../services/migration.md)

### 問1 {#q1}

SQL の結合とトランザクションが必要な業務システムのデータベースとして最も適切なものはどれですか。

- A. Amazon Neptune
- B. Amazon ElastiCache
- C. Amazon DynamoDB
- D. Amazon RDS

??? success "答えと解説"
    **正解: D**

    SQL と結合、トランザクションには RDS や Aurora を選びます。

    - A: 誤り。つながりを扱うグラフデータベース。
    - B: 誤り。インメモリのキャッシュ。
    - C: 誤り。キーで読み書きするデータベースで、複雑な結合には向かない。
    - D: 正しい。

    **スキル:** [データベースの全体像](../domain3.md#t3-4-overview) / **参照:** [データストアの選び方](../../../services/databases.md#choosing-data-store)

### 問2 {#q2}

SNS の友人関係のように、データのつながりをたどる処理に向くデータベースはどれですか。

- A. Amazon DocumentDB
- B. Amazon Neptune
- C. Amazon ElastiCache
- D. Amazon RDS

??? success "答えと解説"
    **正解: B**

    Neptune はグラフデータベースです。

    - A: 誤り。MongoDB 互換のドキュメントデータベース。
    - B: 正しい。
    - C: 誤り。インメモリのキャッシュ。
    - D: 誤り。リレーショナルデータベース。

    **スキル:** [データベースの全体像](../domain3.md#t3-4-overview) / **参照:** [Amazon Neptune](../../../services/databases-specialized.md#neptune)

### 問3 {#q3}

MongoDB を使うアプリを、なるべく変更せずマネージドのデータベースに移したいと考えています。最も適切なものはどれですか。

- A. Amazon Aurora
- B. Amazon ElastiCache
- C. Amazon DocumentDB
- D. Amazon Neptune

??? success "答えと解説"
    **正解: C**

    DocumentDB は MongoDB 互換のドキュメントデータベースです。

    - A: 誤り。MySQL と PostgreSQL に互換のリレーショナルデータベース。
    - B: 誤り。インメモリのキャッシュ。
    - C: 正しい。
    - D: 誤り。グラフデータベース。

    **スキル:** [データベースの全体像](../domain3.md#t3-4-overview) / **参照:** [Amazon DocumentDB](../../../services/databases-specialized.md#documentdb)

### 問4 {#q4}

特別な制約はなく、データベースの運用の手間を減らしたいと考えています。最も適切な選択はどれですか。

- A. マネージドデータベースのサービスを使う
- B. オンプレミスのサーバーを新しく買う
- C. EC2 にデータベースを自分で入れる
- D. インスタンスストアにデータを置く

??? success "答えと解説"
    **正解: A**

    特別な制約がなければ、マネージドデータベースが向きます。

    - A: 正しい。
    - B: 誤り。運用の手間は減らない。
    - C: 誤り。OS とエンジンのパッチや冗長化を自分で行う。
    - D: 誤り。停止で消えるので、データベースの保管先に向かない。

    **スキル:** [EC2 上の DB かマネージド DB か](../domain3.md#t3-4-ec2-vs-managed) / **参照:** [RDS](../../../services/databases.md#rds)、[サービスごとの違い](../../../services/cloud-foundations.md#responsibility-by-service)

### 問5 {#q5}

OS に接続して細かい設定が必要で、RDS が対応していないエンジンを使います。最も適切な選択はどれですか。

- A. Amazon DynamoDB を使う
- B. EC2 にデータベースを入れる
- C. Amazon ElastiCache を使う
- D. Amazon RDS を使う

??? success "答えと解説"
    **正解: B**

    対応していないエンジンや OS レベルの制御が必要なら、EC2 です。

    - A: 誤り。エンジンの選択肢がなく、OS への接続もできない。
    - B: 正しい。
    - C: 誤り。インメモリのキャッシュ。
    - D: 誤り。対応していないエンジンは使えず、OS への接続も基本はできない。

    **スキル:** [EC2 上の DB かマネージド DB か](../domain3.md#t3-4-ec2-vs-managed) / **参照:** [RDS](../../../services/databases.md#rds)

### 問6 {#q6}

EC2 上のデータベースとマネージドデータベースの違いの説明として正しいものはどれですか。

- A. EC2 上では、冗長化が既定で自動的に構成される
- B. EC2 上では OS のパッチを AWS が担当する
- C. マネージドでは OS とエンジンのパッチを AWS が担当する
- D. マネージドでは、データの権限の管理も AWS の担当になる

??? success "答えと解説"
    **正解: C**

    マネージドにすると、OS やエンジンの作業が AWS の担当になります。

    - A: 誤り。利用者が構成する。
    - B: 誤り。EC2 上では利用者の担当。
    - C: 正しい。
    - D: 誤り。データと権限は利用者の担当。

    **スキル:** [EC2 上の DB かマネージド DB か](../domain3.md#t3-4-ec2-vs-managed) / **参照:** [RDS](../../../services/databases.md#rds)、[サービスごとの違い](../../../services/cloud-foundations.md#responsibility-by-service)

### 問7 {#q7}

読み取りの負荷が増えた RDS のデータベースの読み取り性能を上げたいと考えています。最も適切な機能はどれですか。

- A. RDS のリードレプリカ
- B. AWS Backup のプラン
- C. Multi-AZ
- D. S3 のライフサイクルルール

??? success "答えと解説"
    **正解: A**

    読み取りを増やすならリードレプリカです。

    - A: 正しい。
    - B: 誤り。バックアップの機能。
    - C: 誤り。可用性を高める機能で、目的が違う。
    - D: 誤り。オブジェクトのための機能。

    **スキル:** [リレーショナルデータベース](../domain3.md#t3-4-relational) / **参照:** [リードレプリカと Multi-AZ](../../../services/databases.md#read-replicas)

### 問8 {#q8}

MySQL または PostgreSQL に互換で、共有ストレージを持つ AWS のデータベースはどれですか。

- A. Amazon DocumentDB
- B. Amazon DynamoDB
- C. Amazon Redshift
- D. Amazon Aurora

??? success "答えと解説"
    **正解: D**

    Aurora は MySQL と PostgreSQL に互換です。

    - A: 誤り。ドキュメントデータベース。
    - B: 誤り。キーバリューのデータベース。
    - C: 誤り。データウェアハウス。
    - D: 正しい。

    **スキル:** [リレーショナルデータベース](../domain3.md#t3-4-relational) / **参照:** [Aurora](../../../services/databases.md#aurora)

### 問9 {#q9}

Amazon RDS で動かせるデータベースエンジンはどれですか。（2つ選択）

- A. MongoDB
- B. Oracle
- C. SQL Server
- D. Redis OSS
- E. Neo4j

??? success "答えと解説"
    **正解: B, C**

    RDS は MySQL、PostgreSQL、MariaDB、Oracle、SQL Server、Db2 を動かします。

    - A: 誤り。RDS のエンジンではない。MongoDB 互換は DocumentDB。
    - B: 正しい。
    - C: 正しい。
    - D: 誤り。RDS のエンジンではない。ElastiCache のエンジン。
    - E: 誤り。RDS のエンジンではない。グラフは Neptune。

    **スキル:** [リレーショナルデータベース](../domain3.md#t3-4-relational) / **参照:** [RDS](../../../services/databases.md#rds)

### 問10 {#q10}

規模が読めないアプリで、キーを指定して低遅延で読み書きしたいと考えています。サーバーの管理はしたくありません。最も適切なデータベースはどれですか。

- A. Amazon DynamoDB
- B. Amazon Redshift
- C. EC2 上の MySQL
- D. Amazon RDS for Oracle

??? success "答えと解説"
    **正解: A**

    DynamoDB はサーバーレスのキーバリューデータベースです。

    - A: 正しい。
    - B: 誤り。データウェアハウスで、低遅延の読み書きが目的ではない。
    - C: 誤り。サーバーの管理が必要。
    - D: 誤り。インスタンスの管理と結合のためのデータベース。

    **スキル:** [NoSQL データベース](../domain3.md#t3-4-nosql) / **参照:** [キーの設計](../../../services/dynamodb.md#keys)、[データストアの選び方](../../../services/databases.md#choosing-data-store)

### 問11 {#q11}

複雑な結合が必要なレポートを主な用途とする場合、DynamoDB についての判断として正しいものはどれですか。

- A. 容量が小さければ DynamoDB で結合が自動で作られる
- B. 複雑な結合が多いほど DynamoDB が向く
- C. 複雑な結合が必要なら、RDS や Aurora を選ぶ
- D. DynamoDB の SQL の結合は RDS より常に速い

??? success "答えと解説"
    **正解: C**

    DynamoDB はキーでの読み書きに向き、複雑な結合には向きません。

    - A: 誤り。容量で機能は変わらない。
    - B: 誤り。結合が必要なら RDS や Aurora を選ぶ。
    - C: 正しい。
    - D: 誤り。そのような説明はできない。

    **スキル:** [NoSQL データベース](../domain3.md#t3-4-nosql) / **参照:** [データストアの選び方](../../../services/databases.md#choosing-data-store)

### 問12 {#q12}

Amazon DynamoDB の説明として正しいものはどれですか。（2つ選択）

- A. OS に接続して細かい設定ができる
- B. 規模によらず低遅延で読み書きできる
- C. MySQL と完全に互換である
- D. 複雑な結合のために設計されている
- E. サーバーレスのデータベースである

??? success "答えと解説"
    **正解: B, E**

    DynamoDB は NoSQL のデータベースです。

    - A: 誤り。サーバーレスで、OS には接続しない。
    - B: 正しい。
    - C: 誤り。それは Aurora の説明に近い。
    - D: 誤り。結合が必要なら RDS や Aurora。
    - E: 正しい。

    **スキル:** [NoSQL データベース](../domain3.md#t3-4-nosql) / **参照:** [キーの設計](../../../services/dynamodb.md#keys)、[データストアの選び方](../../../services/databases.md#choosing-data-store)

### 問13 {#q13}

データベースへの読み取りが増えて遅くなっています。よく読むデータをメモリに置いて、負荷を減らしたいと考えています。最も適切なサービスはどれですか。

- A. Amazon Neptune
- B. AWS DMS
- C. Amazon S3 Glacier
- D. Amazon ElastiCache

??? success "答えと解説"
    **正解: D**

    ElastiCache はインメモリのキャッシュです。

    - A: 誤り。グラフデータベース。
    - B: 誤り。データを移行するサービス。
    - C: 誤り。長期保管のストレージ。
    - D: 正しい。

    **スキル:** [メモリベースのデータベース](../domain3.md#t3-4-memory) / **参照:** [ElastiCache](../../../services/databases.md#elasticache)

### 問14 {#q14}

Amazon ElastiCache のエンジンはどれですか。（2つ選択）

- A. Oracle
- B. MongoDB
- C. Memcached
- D. Valkey
- E. PostgreSQL

??? success "答えと解説"
    **正解: C, D**

    エンジンには Valkey、Redis OSS、Memcached があります。

    - A: 誤り。RDS のエンジン。
    - B: 誤り。DocumentDB が互換を提供する。
    - C: 正しい。
    - D: 正しい。
    - E: 誤り。RDS や Aurora のエンジン。

    **スキル:** [メモリベースのデータベース](../domain3.md#t3-4-memory) / **参照:** [ElastiCache](../../../services/databases.md#elasticache)

### 問15 {#q15}

マイクロ秒の応答でセッションのデータを読みたいと考えています。最も適切なものはどれですか。

- A. AWS Backup
- B. Amazon ElastiCache
- C. Amazon Redshift
- D. Amazon S3 Standard-IA

??? success "答えと解説"
    **正解: B**

    マイクロ秒で読むキャッシュには ElastiCache を選びます。

    - A: 誤り。バックアップの管理のサービス。
    - B: 正しい。
    - C: 誤り。大量のデータの分析のためのデータウェアハウス。
    - D: 誤り。頻度の低いアクセスのためのストレージ。

    **スキル:** [メモリベースのデータベース](../domain3.md#t3-4-memory) / **参照:** [ElastiCache](../../../services/databases.md#elasticache)、[データストアの選び方](../../../services/databases.md#choosing-data-store)

### 問16 {#q16}

Oracle から Aurora PostgreSQL に移します。使うツールの組み合わせとして正しいものはどれですか。

- A. スキーマの変換に AWS DMS、データの移行に AWS Backup
- B. スキーマの変換に AWS SCT、データの移行に AWS DMS
- C. スキーマの変換に Amazon Inspector、データの移行に AWS SCT
- D. スキーマの変換に AWS Config、データの移行に Amazon Macie

??? success "答えと解説"
    **正解: B**

    エンジンが異なるので、スキーマの変換が必要です。

    - A: 誤り。バックアップのサービスは、異なるエンジンへの移行の手段ではない。
    - B: 正しい。
    - C: 誤り。Inspector は脆弱性を検出するサービス。
    - D: 誤り。Config は設定の記録、Macie は機密データの検出のサービス。

    **スキル:** [データベースの移行ツール](../domain3.md#t3-4-migration) / **参照:** [AWS SCT と DMS Schema Conversion](../../../services/migration.md#sct)、[AWS DMS](../../../services/migration.md#dms)

### 問17 {#q17}

MySQL から Aurora MySQL へ移します。必要な作業の説明として正しいものはどれですか。

- A. エンジンの系統が同じでも、SCT の変換が必ず必要である
- B. 同じ系統なので、移行のツールは一切使えない
- C. 同じ系統なのでスキーマの変換は不要で、データは DMS で移せる
- D. データは移せないので、新しくアプリで入力し直す

??? success "答えと解説"
    **正解: C**

    異なるエンジンのときだけ SCT のスキーマの変換が必要です。

    - A: 誤り。同じ系統なら変換は不要。
    - B: 誤り。DMS は使える。
    - C: 正しい。
    - D: 誤り。DMS などで移せる。

    **スキル:** [データベースの移行ツール](../domain3.md#t3-4-migration) / **参照:** [AWS SCT と DMS Schema Conversion](../../../services/migration.md#sct)、[AWS DMS](../../../services/migration.md#dms)

### 問18 {#q18}

AWS DMS の説明として正しいものはどれですか。

- A. データベースの性能の問題を自動で検出して直す
- B. 元のデータベースを必ず止めてから移行する
- C. アプリのコードをクラウド向けに自動で書き換える
- D. 元のデータベースを動かしたまま移行できる

??? success "答えと解説"
    **正解: D**

    DMS はデータを移すサービスです。

    - A: 誤り。それは DMS の役割ではない。
    - B: 誤り。動かしたまま移行できる。
    - C: 誤り。それは DMS の役割ではない。
    - D: 正しい。

    **スキル:** [データベースの移行ツール](../domain3.md#t3-4-migration) / **参照:** [AWS DMS](../../../services/migration.md#dms)

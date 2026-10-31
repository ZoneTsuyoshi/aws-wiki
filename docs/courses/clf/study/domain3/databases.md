# 分野3: データベース

データの形と運用の手間から、データベースと移行ツールを選びます。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [データベースの全体像](../../domain3.md#t3-4-overview) | 要件からの選択 |
| [EC2 上の DB かマネージド DB か](../../domain3.md#t3-4-ec2-vs-managed) | 担当の違い |
| [リレーショナルデータベース](../../domain3.md#t3-4-relational) | RDS、Aurora、Multi-AZ、リードレプリカ |
| [NoSQL データベース](../../domain3.md#t3-4-nosql) | DynamoDB |
| [メモリベースのデータベース](../../domain3.md#t3-4-memory) | ElastiCache |
| [データベースの移行ツール](../../domain3.md#t3-4-migration) | DMS と SCT |

## 学習の順番 {#study-order}

1. [データストアの選び方](../../../../services/databases.md#choosing-data-store): 要件とサービスの対応を覚えます。
2. [RDS](../../../../services/databases.md#rds)と[リードレプリカと Multi-AZ](../../../../services/databases.md#read-replicas): Multi-AZ とリードレプリカの目的を区別します。
3. [Aurora](../../../../services/databases.md#aurora)、[キーの設計](../../../../services/dynamodb.md#keys)、[ElastiCache](../../../../services/databases.md#elasticache): 特徴を確認します。
4. [Amazon DocumentDB](../../../../services/databases-specialized.md#documentdb)と[Amazon Neptune](../../../../services/databases-specialized.md#neptune): 名前と用途を対応させます。
5. [AWS DMS](../../../../services/migration.md#dms)と[AWS SCT と DMS Schema Conversion](../../../../services/migration.md#sct): 役割を区別します。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| RDS のエンジン | MySQL、PostgreSQL、MariaDB、Oracle、SQL Server、Db2 | MongoDB や Redis OSS は含まれない |
| Aurora の互換 | MySQL、PostgreSQL | |
| ElastiCache のエンジン | Valkey、Redis OSS、Memcached | |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| SQL と結合、トランザクション | RDS、Aurora |
| キーで低遅延に読み書き、規模が読めない | DynamoDB |
| 読み取りをメモリで速くする | ElastiCache |
| MongoDB 互換 | DocumentDB |
| つながりをたどる | Neptune |
| 可用性を上げる | Multi-AZ |
| 読み取りを増やす | リードレプリカ |
| OS の制御や未対応のエンジンが必要 | EC2 上のデータベース |
| Oracle から Aurora PostgreSQL へ | SCT と DMS |
| MySQL から Aurora MySQL へ | DMS。スキーマの変換は不要 |

## 引っかかりやすい点 {#traps}

- 特別な制約がなければ、マネージドデータベースが正解になりやすいです。
- マネージドでも、データと権限は利用者の担当です。
- DMS はデータを移し、SCT はスキーマとコードを変換します。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [databases 問1](../../exercises/databases.md#q1) | データベースの全体像 | SQL の結合とトランザクションが必要な業務システムのデータベースとして最も適切なものはどれですか。 |
| [databases 問2](../../exercises/databases.md#q2) | データベースの全体像 | SNS の友人関係のように、データのつながりをたどる処理に向くデータベースはどれですか。 |
| [databases 問3](../../exercises/databases.md#q3) | データベースの全体像 | MongoDB を使うアプリを、なるべく変更せずマネージドのデータベースに移したいと考えています。最… |
| [databases 問4](../../exercises/databases.md#q4) | EC2 上の DB かマネージド DB か | 特別な制約はなく、データベースの運用の手間を減らしたいと考えています。最も適切な選択はどれですか。 |
| [databases 問5](../../exercises/databases.md#q5) | EC2 上の DB かマネージド DB か | OS に接続して細かい設定が必要で、RDS が対応していないエンジンを使います。最も適切な選択はどれ… |
| [databases 問6](../../exercises/databases.md#q6) | EC2 上の DB かマネージド DB か | EC2 上のデータベースとマネージドデータベースの違いの説明として正しいものはどれですか。 |
| [databases 問7](../../exercises/databases.md#q7) | リレーショナルデータベース | 読み取りの負荷が増えた RDS のデータベースの読み取り性能を上げたいと考えています。最も適切な機能… |
| [databases 問8](../../exercises/databases.md#q8) | リレーショナルデータベース | MySQL または PostgreSQL に互換で、共有ストレージを持つ AWS のデータベースはど… |
| [databases 問9](../../exercises/databases.md#q9) | リレーショナルデータベース | Amazon RDS で動かせるデータベースエンジンはどれですか。（2つ選択） |
| [databases 問10](../../exercises/databases.md#q10) | NoSQL データベース | 規模が読めないアプリで、キーを指定して低遅延で読み書きしたいと考えています。サーバーの管理はしたくあ… |
| [databases 問11](../../exercises/databases.md#q11) | NoSQL データベース | 複雑な結合が必要なレポートを主な用途とする場合、DynamoDB についての判断として正しいものはど… |
| [databases 問12](../../exercises/databases.md#q12) | NoSQL データベース | Amazon DynamoDB の説明として正しいものはどれですか。（2つ選択） |
| [databases 問13](../../exercises/databases.md#q13) | メモリベースのデータベース | データベースへの読み取りが増えて遅くなっています。よく読むデータをメモリに置いて、負荷を減らしたいと… |
| [databases 問14](../../exercises/databases.md#q14) | メモリベースのデータベース | Amazon ElastiCache のエンジンはどれですか。（2つ選択） |
| [databases 問15](../../exercises/databases.md#q15) | メモリベースのデータベース | マイクロ秒の応答でセッションのデータを読みたいと考えています。最も適切なものはどれですか。 |
| [databases 問16](../../exercises/databases.md#q16) | データベースの移行ツール | Oracle から Aurora PostgreSQL に移します。使うツールの組み合わせとして正し… |
| [databases 問17](../../exercises/databases.md#q17) | データベースの移行ツール | MySQL から Aurora MySQL へ移します。必要な作業の説明として正しいものはどれですか… |
| [databases 問18](../../exercises/databases.md#q18) | データベースの移行ツール | AWS DMS の説明として正しいものはどれですか。 |

<!-- questions:end -->

# 分野2: データストアの選択

費用、性能、アクセスパターン、ユースケースに合う保存先と、インデックスやパーティションの実践を問います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [2.1.1](../../domain2.md#skill-2-1-1) | コストと性能の要件に合うストレージ |
| [2.1.2](../../domain2.md#skill-2-1-2) | アクセスパターンに合う設定 |
| [2.1.3](../../domain2.md#skill-2-1-3) | ユースケースに合うストレージ |
| [2.4.5](../../domain2.md#skill-2-4-5) | インデックス、パーティション、圧縮のベストプラクティス |

## 学習の順番 {#study-order}

1. [データの置き場と SQL エンジン](../../../../services/data-engineering.md#choosing-query): Athena と Redshift を比べます。
2. [全エンジンの比較表](../../../../services/databases-specialized.md#decision-table): 要件の言葉とエンジンを対応づけます。
3. [MemoryDB と ElastiCache](../../../../services/databases-specialized.md#memorydb-vs-elasticache): 耐久性の違いを覚えます。
4. [LSI と GSI](../../../../services/dynamodb.md#indexes): 作成時と後からの違いを確認します。
5. [パーティション](../../../../services/data-engineering.md#partitioning): 悪い設計の症状を確認します。

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 単発の分析で読んだ量だけ払う | S3 と Athena |
| クラスターを消してもデータを残す | 入出力は S3、中間データは HDFS |
| 読み取りを増やす | リードレプリカ。Multi-AZ は可用性 |
| テーブル作成後にキー以外で引く | GSI |
| 耐久性のあるインメモリの主データベース | MemoryDB |
| つながりをたどる | Neptune |

## 引っかかりやすい点 {#traps}

- Lake Formation はストレージではありません。実体は S3 です。
- `user_id` のように値の種類が多い列でパーティションを切ると遅くなります。
- DynamoDB の射影の `ALL` は費用が増えます。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [datastores 問1](../../exercises/datastores.md#q1) | 2.1.1 | ログを S3 に置き、月に数回だけ単発で SQL を実行します。クラスターは持たず、費用を読んだ量に… |
| [datastores 問2](../../exercises/datastores.md#q2) | 2.1.1 | 「データレイクを作る選択肢」として Lake Formation が挙がりました。正しい理解はどれで… |
| [datastores 問3](../../exercises/datastores.md#q3) | 2.1.1 | ストリームのデータを 30 日保持します。費用の説明として正しいものはどれですか。（2つ選択） |
| [datastores 問4](../../exercises/datastores.md#q4) | 2.1.2 | EMR で 1 日 1 回ジョブを実行し、終了後にクラスターを消します。入出力とシャッフルの中間デー… |
| [datastores 問5](../../exercises/datastores.md#q5) | 2.1.2 | RDS のレポートのクエリが本番の書き込みに影響します。読み取りを逃がす構成はどれですか。 |
| [datastores 問6](../../exercises/datastores.md#q6) | 2.1.2 | DynamoDB のテーブルを作成した後で、「メールアドレスで項目を引く」要件が増えました。どのイン… |
| [datastores 問7](../../exercises/datastores.md#q7) | 2.1.2 | Redshift の COMPOUND SORTKEY (sold_at, region) のテーブ… |
| [datastores 問8](../../exercises/datastores.md#q8) | 2.1.3 | キーと値の検索をマイクロ秒で読み、データは再起動後も失われないようにして、主データベースとして使いま… |
| [datastores 問9](../../exercises/datastores.md#q9) | 2.1.3 | 要件とサービスの組み合わせで正しいものはどれですか。 |
| [datastores 問10](../../exercises/datastores.md#q10) | 2.1.3 | 要件に合う保存先として正しい組み合わせはどれですか。（2つ選択） |
| [datastores 問11](../../exercises/datastores.md#q11) | 2.4.5 | S3 のデータを user_id でパーティションにしたところ、Athena が遅くなりました。ユー… |
| [datastores 問12](../../exercises/datastores.md#q12) | 2.4.5 | Spark で読む 200 GB の gzip の CSV 1 ファイルが遅いです。圧縮と形式の見直… |
| [datastores 問13](../../exercises/datastores.md#q13) | 2.4.5 | DynamoDB の GSI で、読む属性は 3 つだけです。ストレージと書き込みの費用を抑える設定… |

<!-- questions:end -->

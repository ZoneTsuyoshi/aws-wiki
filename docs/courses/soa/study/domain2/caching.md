# 分野2: キャッシュ

要件に合うキャッシュの選択、ElastiCache の設定を問います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [2.1.2](../../domain2.md#skill-2-1-2) | キャッシュの実装 |

## 学習の順番 {#study-order}

1. [DAX、ElastiCache、CloudFront の使い分け](../../../../services/databases.md#cache-comparison): 3 つの使い分けを確認します。
2. [Redis OSS、Valkey と Memcached](../../../../services/databases.md#engines)と[レプリケーションと Multi-AZ](../../../../services/databases.md#elasticache-replication): エンジンとレプリカの違いを確認します。
3. [クラスターモード](../../../../services/databases.md#cluster-mode)と[追い出しとメモリ](../../../../services/databases.md#eviction): 増やし方と追い出しを確認します。
4. [キャッシュ戦略](../../../../services/databases.md#caching-strategies): 戦略を区別します。
5. [DAX](../../../../services/dynamodb.md#dax)と[キャッシュキーとポリシー](../../../../services/networking.md#cache-keys): DAX と CloudFront の要点を確認します。

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| DynamoDB を最小の変更で速く | DAX |
| RDS のクエリとセッションの共有 | ElastiCache |
| 世界中へ画像を配信 | CloudFront |
| 読み取りを増やす | レプリカを追加 |
| 書き込みとメモリを増やす | クラスターモードでシャードを追加 |
| `Evictions` が多い | ノードを大きくする、TTL を見直す |

## 引っかかりやすい点 {#traps}

- ノードベースの Memcached はレプリケーションがなく、ノードが落ちるとそのデータは消えます。
- レプリカ 0 のノードが故障すると全データを失います。
- 遅延読み込みは古い値が残ることがあります。TTL を組み合わせます。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [caching 問1](../../exercises/caching.md#q1) | 2.1.2 | DynamoDB の読み取りが多いアプリケーションで、コードの変更を最小にしてマイクロ秒の応答にした… |
| [caching 問2](../../exercises/caching.md#q2) | 2.1.2 | 複数の EC2 でユーザーのセッションを共有し、RDS の重いクエリの結果もキャッシュしたいと考えて… |
| [caching 問3](../../exercises/caching.md#q3) | 2.1.2 | キャッシュに、レプリカと Multi-AZ、ソート済みセットが必要です。どのエンジンを選びますか。 |
| [caching 問4](../../exercises/caching.md#q4) | 2.1.2 | ElastiCache（Valkey）でメモリと書き込みの容量が足りなくなりました。読み取りのレプリ… |
| [caching 問5](../../exercises/caching.md#q5) | 2.1.2 | Evictions のメトリクスが増え、キャッシュのヒット率が下がっています。対処として適切なものを… |
| [caching 問6](../../exercises/caching.md#q6) | 2.1.2 | ElastiCache の戦略を選びます。必要なデータだけをキャッシュに載せたいと考えています。ミス… |
| [caching 問7](../../exercises/caching.md#q7) | 2.1.2 | 読み取りのたびに常に新しい値を返したいです。書き込みが少し遅くなること、使わないデータも載ることは許… |
| [caching 問8](../../exercises/caching.md#q8) | 2.1.2 | ノードベースの Memcached クラスターのノードの障害の説明として正しいものはどれですか。 |
| [caching 問9](../../exercises/caching.md#q9) | 2.1.2 | 世界中の利用者へ、画像と API の GET の応答を速く配信したいです。応答は全員に共通です。どれ… |
| [caching 問10](../../exercises/caching.md#q10) | 2.1.2 | ElastiCache（Redis OSS）で、レプリカ 0 のノードが故障しました。起きることと予… |

<!-- questions:end -->

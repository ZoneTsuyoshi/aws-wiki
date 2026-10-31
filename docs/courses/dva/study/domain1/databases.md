# 分野1: データベース

分野1では、アクセスパターンからデータストアを選ぶことと、データストアに合うキャッシュを選ぶことを問われます。接続の認証は[分野2](../domain2/databases.md)、接続数やキャッシュの指標の調査は[分野4](../domain4/databases.md)で扱います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [1.3.2](../../domain1.md#skill-1-3-2) | アクセスパターンに応じたデータストアの選択 |
| [1.3.3](../../domain1.md#skill-1-3-3) | データストアに合うキャッシュの選択 |

## 学習の順番 {#study-order}

1. [データストアの選び方](../../../../services/databases.md#choosing-data-store): 問題文のアクセスパターンから候補を絞る手順を覚えます。
2. [リードレプリカと Multi-AZ](../../../../services/databases.md#read-replicas): 読み取りのスケールと高可用性を区別します。
3. [Aurora](../../../../services/databases.md#aurora)、[エンドポイントの動作](../../../../services/databases.md#aurora-endpoints): 読み取りを分散するときの接続先を確認します。
4. [Redis OSS、Valkey と Memcached](../../../../services/databases.md#engines): 要件からエンジンを選べるようにします。
5. [キャッシュ戦略](../../../../services/databases.md#caching-strategies): 遅延読み込み、ライトスルー、TTL の長所と短所を比べます。
6. [DAX、ElastiCache、CloudFront の使い分け](../../../../services/databases.md#cache-comparison): データストアとキャッシュの組み合わせを覚えます。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| RDS のリードレプリカ（同一リージョン） | 最大 15 個 | 複製は非同期です |
| Aurora レプリカ | 最大 15 個 | |
| ElastiCache のシャード | クラスターモード有効で最大 500 | 1 ノードに収まらないときに使います |
| ElastiCache のレプリカ | シャードごとに最大 5 | |
| `maxmemory-policy` | デフォルト `volatile-lru` | TTL なしのキーは追い出せません |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| キーで引く、遅延を一定にしたい、規模が読めない | DynamoDB を選びます |
| 結合、複雑なクエリ、複数テーブルのトランザクションが必要 | RDS か Aurora を選びます |
| 全文検索、ログ分析、柔軟な検索条件 | OpenSearch Service を選びます |
| 大きなファイル、静的コンテンツ、アーカイブ | S3 を選びます |
| DynamoDB の読み取りを最小のコード変更で速くする | DAX を使います |
| RDS のクエリ結果をキャッシュする、複数の EC2 でセッションを共有する | ElastiCache を使います |
| ランキングを実装する | Valkey または Redis OSS のソート済みセットを使います |
| 世界中のユーザーに画像を速く配信する | CloudFront を使います |
| キャッシュに古いデータが残る | TTL を付けるか、ライトスルーにします |
| キャッシュが読まれないデータで埋まる | 遅延読み込みと TTL にします |
| 新しいノードのキャッシュが空でミスが多い | 遅延読み込みとライトスルーを併用します |

## 引っかかりやすい点 {#traps}

- Multi-AZ のスタンバイは読み取りに使えません（インスタンス配置の場合）。読み取りを増やすならリードレプリカです。
- リードレプリカから古い値が返るのは、非同期複製のためです。最新が必須ならプライマリを読みます。
- データ構造、永続性、フェイルオーバーのどれかが要件にあれば、Memcached ではなく Valkey か Redis OSS です。
- すべてのキーを同じ TTL にすると一斉に切れて、DB に負荷が集中します。秒数にランダムな値を足して散らします。
- デフォルトの `volatile-lru` で TTL を付けていないと、追い出せるキーがなくなり、書き込みが失敗することがあります。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [databases 問1](../../exercises/databases.md#q1) | 1.3.2 | 開発者が RDS for MySQL にリードレプリカを作ろうとすると、作成できません。ソースの D… |
| [databases 問6](../../exercises/databases.md#q6) | 1.3.2 | Aurora クラスターに、夜間レポート用の大きなインスタンス 2 台と、Web 用の小さなインスタ… |
| [databases 問8](../../exercises/databases.md#q8) | 1.3.2 | Aurora グローバルデータベースのセカンダリリージョンのアプリが、書き込みも行います。プライマリ… |
| [databases 問15](../../exercises/databases.md#q15) | 1.3.3 | アプリは遅延読み込みだけでキャッシュしています。DB を更新しても古い値が返り、キャッシュには読まれ… |
| [databases 問16](../../exercises/databases.md#q16) | 1.3.3 | DynamoDB の GetItem が中心の商品ページで、読み取りの遅延を数ミリ秒からマイクロ秒の… |
| [databases 問17](../../exercises/databases.md#q17) | 1.3.3 | データストアとキャッシュの組み合わせとして、適切なものはどれですか。（2つ選択） |

<!-- questions:end -->

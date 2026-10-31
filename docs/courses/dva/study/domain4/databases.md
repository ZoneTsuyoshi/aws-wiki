# 分野4: データベースとキャッシュ

接続プーリングと RDS Proxy による接続数の管理、ElastiCache などのキャッシュの選び方が問われます。データストアの選択は[分野1](../domain1/databases.md)、認証と暗号化は[分野2](../domain2/databases.md)で扱います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [4.3.1](../../domain4.md#skill-4-3-1) | コネクションプーリング、RDS Proxy |
| [4.3.4](../../domain4.md#skill-4-3-4) | ElastiCache によるキャッシュ、キャッシュの使い分け |

## 学習の順番 {#study-order}

1. [接続プーリングと RDS Proxy](../../../../services/databases.md#connection-pooling): プールの場所の違いと、サイズの計算を理解します。
2. [RDS Proxy](../../../../services/databases.md#rds-proxy): 多重化の効果と、ピン留めの原因を学びます。
3. [RDS Proxy の設定](../../../../services/databases.md#rds-proxy-settings): 接続の上限と、症状ごとの対処を確認します。
4. [キャッシュの使い分け](../../../../services/databases.md#cache-comparison): DAX、ElastiCache、CloudFront を要件から選べるようにします。
5. [キャッシュ戦略](../../../../services/databases.md#caching-strategies): 遅延読み込み、ライトスルー、TTL の長所と短所を比べます。
6. [アプリケーションレベルのキャッシュ](../../../../services/databases.md#application-caching): 層ごとの特徴と、キーの設計を押さえます。
7. [追い出しとメモリ](../../../../services/databases.md#eviction): `maxmemory-policy` とメトリクスの見方を確認します。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| プールサイズの上限 | プールの最大接続数 × インスタンス数 ≦ DB の最大接続数 | Auto Scaling で台数が増えると合計も増えます |
| `MaxConnectionsPercent` | 既定 100（SQL Server は 10） | DB の `max_connections` に対する割合です |
| `MaxIdleConnectionsPercent` | `MaxConnectionsPercent` の半分 | 低いほどアイドル接続を早く閉じます |
| `ConnectionBorrowTimeout` | 既定 120 秒、0〜300 秒 | 超えるとタイムアウトエラーです |
| `IdleClientTimeout` | 既定 1,800 秒 | アイドルのクライアント接続を閉じるまでの時間です |
| `maxmemory-policy` | 既定 `volatile-lru` | 純粋なキャッシュには `allkeys-lru` が向いています |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| Lambda の同時実行が増えて接続が枯渇する | RDS Proxy を置き、接続をハンドラーの外で作って再利用します |
| EC2 を増やすと DB の接続上限に達する | プールの最大接続数 × 台数が DB の最大接続数を超えないように、プールサイズを下げます |
| RDS Proxy の効果が出ない | `DatabaseConnectionsCurrentlySessionPinned` でピン留めを確認します。接続ごとの `SET` は `InitQuery` に移します |
| `Timed-out waiting to acquire database connection` が出る | ピン留めや長いトランザクションを確認し、`MaxConnectionsPercent` や DB の容量を増やします |
| 同じ DB に 2 つのプロキシを付ける | `max_connections` が 1,000 なら、それぞれ `MaxConnectionsPercent` を 40 にして、残りを管理者などに残します |
| RDS のクエリ結果をキャッシュしたい、複数の EC2 でセッションを共有したい | ElastiCache を使います |
| キャッシュの古いデータと未使用データの両方を抑えたい | 遅延読み込みとライトスルーを併用し、すべての書き込みに TTL を付けます |
| 同じ TTL のキーが一斉に切れて DB に負荷が集中する | `ex=300 + random.randint(0, 60)` のように TTL を散らします |
| `Evictions` が増え続ける | メモリ不足です。スケールアップやシャードの追加を考えます |
| `CacheHitRate` が低い | TTL やキーの設計を見直します |

## 引っかかりやすい点 {#traps}

- **書き込みが失敗する:** 既定の `volatile-lru` で TTL を付けていないと、追い出せるキーがなくなります。TTL を付けるか、`allkeys-lru` にします。
- **他人のデータが返る:** 結果に影響するテナント ID やユーザー ID をキーに含めていません。
- **リードレプリカにプロキシを付けられない:** レプリケーション構成の RDS で関連付けられるのはライターだけです。
- **プロキシへ外部から接続できない:** プロキシは DB と同じ VPC に置き、パブリックアクセスはできません。
- **DB を更新しても古い値が返る:** 遅延読み込みだけだと、TTL が切れるまで古い値のままです。
- **新しいノードでミスが続く:** ライトスルーだけだと、書かれるまでデータがありません。遅延読み込みと併用します。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [databases 問5](../../exercises/databases.md#q5) | 4.3.1 | Aurora クラスターのレプリカが 3 台あります。アプリは起動時に接続プールを作り、リーダーエン… |
| [databases 問7](../../exercises/databases.md#q7) | 4.3.2 | 開発環境の Aurora Serverless v2 を、夜間に接続がないときに最も安くしたいと考え… |
| [databases 問9](../../exercises/databases.md#q9) | 4.3.1 | max_connections が 1,000 の RDS for MySQL に、2 つのアプリが… |
| [databases 問10](../../exercises/databases.md#q10) | 4.1.1 | Lambda から RDS Proxy 経由で接続すると、ときどき Timed-out waitin… |
| [databases 問11](../../exercises/databases.md#q11) | 4.3.1 | RDS Proxy を導入しましたが、DB の接続数が減りません。DatabaseConnectio… |
| [databases 問12](../../exercises/databases.md#q12) | 4.3.4 | Valkey のキャッシュで、データが 1 ノードのメモリに収まらなくなりました。読み取りだけでなく… |
| [databases 問14](../../exercises/databases.md#q14) | 4.3.4 | ElastiCache のキャッシュでメモリが一杯になると、SET がエラーになります。アプリはキー… |

<!-- questions:end -->

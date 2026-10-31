# 分野1: RDS の監視と性能

接続の急増と、DB 負荷の読み方を問います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [1.3.5](../../domain1.md#skill-1-3-5) | RDS の監視と性能の改善 |

## 学習の順番 {#study-order}

1. [RDS](../../../../services/databases.md#rds)と[RDS Proxy](../../../../services/databases.md#rds-proxy): 主なメトリクスと RDS Proxy の役割を確認します。
2. [RDS Proxy の設定](../../../../services/databases.md#rds-proxy-settings): ピン留めの指標を覚えます。
3. [リードレプリカと Multi-AZ](../../../../services/databases.md#read-replicas): 読み取りの分散と接続先を確認します。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| Database Insights の保持 | 既定で 7 日 | 1〜24 か月を購入できる |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| `Too many connections` | RDS Proxy |
| プロキシの効果が低い | `DatabaseConnectionsCurrentlySessionPinned` |
| 読み取りが多い | リードレプリカ。接続先をアプリで変える |
| OS のプロセスを見たい | Enhanced Monitoring |
| DB 負荷を分解したい | Database Insights（試験ガイドの Performance Insights は提供を終了して移行済み） |

## 引っかかりやすい点 {#traps}

- Multi-AZ DB インスタンスのスタンバイは読めません。
- RDS Proxy は DB と同じ VPC に置き、パブリックアクセスはできません。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [databases 問1](../../exercises/databases.md#q1) | 1.3.5 | Lambda から RDS for MySQL に接続するアプリケーションで、同時実行が増えると T… |
| [databases 問2](../../exercises/databases.md#q2) | 1.3.5 | RDS Proxy を導入しましたが、接続の再利用の効果が低いです。何を確認しますか。 |
| [databases 問3](../../exercises/databases.md#q3) | 1.3.5 | RDS Proxy の制約として正しいものを選んでください。（2つ選択） |
| [databases 問4](../../exercises/databases.md#q4) | 1.3.5 | CPUUtilization は高いものの、DB の負荷の分析によると原因は読み取りのレポートの S… |
| [databases 問5](../../exercises/databases.md#q5) | 1.3.5 | DB 全体が遅いときの調査です。DB の負荷が Max vCPU の線を頻繁に超え、主な待機が CP… |

<!-- questions:end -->

# 分野2: リードレプリカとプロキシ

読み取りのスケールと、接続の問題を解決する部品を区別します。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [リードレプリカを使う場面](../../domain2.md#t2-1-read-replicas) | リードレプリカを使う場面 |
| [プロキシの概念](../../domain2.md#t2-2-proxy) | プロキシの概念 |

## 学習の順番 {#study-order}

1. [リードレプリカと Multi-AZ](../../../../services/databases.md#read-replicas): レプリカと Multi-AZ の目的の違いを確認します。
2. [RDS Proxy](../../../../services/databases.md#rds-proxy)と[RDS Proxy の設定](../../../../services/databases.md#rds-proxy-settings): プロキシの効果とピン留めを押さえます。

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 重いレポートを逃がす | リードレプリカ |
| 障害に備える | Multi-AZ |
| 接続の急増 | RDS Proxy |

## 引っかかりやすい点 {#traps}

- レプリカは非同期なので、書いた直後に古い値が返ることがあります。
- RDS Proxy はキャッシュではありません。パブリックアクセスもできません。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [databases 問1](../../exercises/databases.md#q1) | リードレプリカの場面 | RDS の夜間のレポートのクエリが本番に影響しています。レポートは数分の古さを許せます。どうしますか… |
| [databases 問2](../../exercises/databases.md#q2) | リードレプリカの場面 | 正しい対応を選んでください。読み取りのスケールにはこれ、障害への備えにはこれ、という組み合わせです。 |
| [databases 問3](../../exercises/databases.md#q3) | リードレプリカの場面 | アプリが書き込みの直後に、リードレプリカから読むと古い値が返ることがあります。原因はどれですか。 |
| [databases 問4](../../exercises/databases.md#q4) | プロキシの概念 | Lambda の急増で RDS に too many connections が出ます。アプリのロジ… |
| [databases 問5](../../exercises/databases.md#q5) | プロキシの概念 | RDS Proxy の説明として正しいものを選んでください。（2つ選択） |
| [databases 問6](../../exercises/databases.md#q6) | プロキシの概念 | RDS Proxy を入れましたが、接続の多重化の効果が小さいです。アプリはセッションの変数をよく変… |

<!-- questions:end -->

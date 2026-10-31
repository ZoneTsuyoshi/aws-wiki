# 分野2: ロードバランサー

負荷分散の構成とエラーの切り分けを問います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [負荷分散](../../domain2.md#t2-1-load-balancing) | 負荷分散（L4 と L7、リバースプロキシ、L3）、負荷分散の構成と実装 |

## 学習の順番 {#study-order}

1. [ヘルスチェックの計算](../../../../services/networking.md#health-check-calc): 異常の判定の時間を計算します。
2. [ALB のエラーの原因一覧](../../../../services/networking.md#alb-error-detail): 502、503、504 の違いを覚えます。
3. [アイドルタイムアウトとキープアライブ](../../../../services/networking.md#alb-idle-timeout): タイムアウトの関係を確認します。

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 502 がときどき出る | キープアライブを ALB より長く |
| 504 が出る | アイドルタイムアウト、NACL の戻り |

## 引っかかりやすい点 {#traps}

- `UnhealthyThresholdCount` の最小は 2 です。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [elb 問25](../../exercises/elb.md#q25) | 負荷分散 | ALB のターゲットの異常を 20 秒程度で検知したいと考えています。既定は間隔 30 秒、Unhe… |
| [elb 問26](../../exercises/elb.md#q26) | 負荷分散 | ALB でときどき HTTP 502 が出ます。ターゲットのログに異常はなく、負荷も低いです。ターゲ… |
| [elb 問27](../../exercises/elb.md#q27) | 負荷分散 | ALB から HTTP 504 が返ります。ターゲットは別のサブネットにあり、最近 NACL を変更… |

<!-- questions:end -->

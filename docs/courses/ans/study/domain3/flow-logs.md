# 分野3: フローログと Traffic Mirroring

フローログの読み方と、パケットの分析を問います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [収集と分析](../../domain3.md#t3-2-tools) | 収集と分析のツール（CloudWatch、フローログ、Traffic Mirroring）、ツールの出力の分析 |
| [パケットの分析](../../domain3.md#t3-2-packets) | パケットの分析（シェーピングの問題） |

## 学習の順番 {#study-order}

1. [フローログの分析](../../../../services/network-connectivity.md#flow-log-analysis): 読み方の表を確認します。
2. [Traffic Mirroring](../../../../services/network-connectivity.md#traffic-mirroring): 設定の手順を覚えます。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| `tcp-flags` | SYN=2、RST=4、FIN=1 | 集約期間で OR |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 受信 `ACCEPT`、送信 `REJECT` | NACL の戻りの通信 |
| ミラーに何も届かない | フィルターのルール |

## 引っかかりやすい点 {#traps}

- パケットは 1 回しかコピーされません。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [flow-logs 問4](../../exercises/flow-logs.md#q4) | 収集と分析 | フローログで、EC2 の受信の記録が ACCEPT、対応する送信の記録が REJECT です。SG … |
| [flow-logs 問5](../../exercises/flow-logs.md#q5) | 収集と分析 | フローログで tcp-flags=2 の記録が続き、相手からの応答の記録がありません。action … |
| [flow-logs 問6](../../exercises/flow-logs.md#q6) | 収集と分析 | フローログのレコードに log-status=SKIPDATA があります。同時に Amazon D… |
| [flow-logs 問7](../../exercises/flow-logs.md#q7) | パケットの分析 | アプリで再送が増えています。ウィンドウの縮小や断片化の有無を調べるため、Wireshark でパケッ… |
| [flow-logs 問8](../../exercises/flow-logs.md#q8) | パケットの分析 | Traffic Mirroring で 2 つのセッションを同じ ENI に設定し、片方は IDS … |
| [flow-logs 問9](../../exercises/flow-logs.md#q9) | パケットの分析 | インスタンスの帯域の上限に当たると、キューイングや破棄が起こるとされています。Traffic Mir… |

<!-- questions:end -->

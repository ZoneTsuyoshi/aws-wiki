# 分野4: FM に合わせた資源の割り当て

FM の容量はトークンで考えます。自前のホストでは、負荷の指標も変わります。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [4.2.5](../../domain4.md#skill-4-2-5) | FM に合わせた資源の割り当て |

## 学習の順番 {#study-order}

1. [スループット](../../../../services/genai-apps.md#throughput): 容量の計画の考え方を確認します。
2. [モデル呼び出しログ](../../../../services/ai.md#invocation-logging): 長さの分布の取り方を押さえます。
3. [自動スケーリング](../../../../services/sagemaker.md#autoscaling): 指標の選び方を理解します。

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 容量の見積もり | トークン数のピーク。平均やリクエスト数ではない |
| 推論コンポーネントの増減 | `ConcurrentRequestsPerCopy` |
| 入出力の比率が変わった | プロンプトの変更や不正利用を疑う |

## 引っかかりやすい点 {#traps}

- 長さの分布を見ないと、平均では見積もりを誤ります。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [custom-models 問14](../../exercises/custom-models.md#q14) | 4.2.5 | Bedrock の容量を計画します。担当者は Invocations の平均から必要な処理量を見積も… |
| [custom-models 問15](../../exercises/custom-models.md#q15) | 4.2.5 | 自前でホストした LLM の推論コンポーネントを、負荷に合わせて増減します。1 つのエンドポイントに… |
| [custom-models 問16](../../exercises/custom-models.md#q16) | 4.2.5 | ある月から、呼び出しの回数は同じなのに入力トークンが急に増え、スロットリングも出始めました。プロンプ… |

<!-- questions:end -->

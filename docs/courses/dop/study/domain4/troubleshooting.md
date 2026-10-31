# 分野4: X-Ray

トレースの有効化と検索、費用の調整を問います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [X-Ray](../../domain4.md#t4-2-xray) | X-Ray の設定 |

## 学習の順番 {#study-order}

1. [SDK と OpenTelemetry（現在の推奨）](../../../../services/observability.md#xray-opentelemetry): SDK とデーモンの状況を確認します。
2. [Lambda のアクティブトレース](../../../../services/observability.md#lambda-active-tracing): Lambda の設定を確認します。
3. [API Gateway での有効化](../../../../services/observability.md#xray-apigateway): ステージの設定を確認します。
4. [アノテーションとメタデータ](../../../../services/observability.md#annotations-metadata): 検索できる値の違いを覚えます。
5. [サンプリング](../../../../services/observability.md#xray-sampling): 費用の調整を確認します。

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 値で検索する | アノテーション |
| 費用を減らす | サンプリングのルール |
| 新しい計装 | OpenTelemetry（ADOT） |

## 引っかかりやすい点 {#traps}

- メタデータはインデックスされません。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [troubleshooting 問1](../../exercises/troubleshooting.md#q1) | X-Ray | 新規に作る ECS の API に、リクエストのトレースを入れます。既存の X-Ray の画面も使い… |
| [troubleshooting 問2](../../exercises/troubleshooting.md#q2) | X-Ray | API Gateway と Lambda の間のトレースが表示されません。API Gateway か… |
| [troubleshooting 問3](../../exercises/troubleshooting.md#q3) | X-Ray | 秒間 2,000 件の API で、全リクエストのトレースの費用が高くなっています。障害の調査では顧… |

<!-- questions:end -->

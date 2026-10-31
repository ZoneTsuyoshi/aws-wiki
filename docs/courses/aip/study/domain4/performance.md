# 分野4: 性能とパラメータの調整

体感の待ち時間と全体の時間を分けて改善します。パラメータの調整と流量の制御も扱います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [4.2.1](../../domain4.md#skill-4-2-1) | 応答性の高い AI システム |
| [4.2.3](../../domain4.md#skill-4-2-3) | FM のスループットの最適化 |
| [4.2.4](../../domain4.md#skill-4-2-4) | 用途に合わせた FM の調整 |
| [4.2.6](../../domain4.md#skill-4-2-6) | ワークフロー全体の性能 |

## 学習の順番 {#study-order}

1. [遅延の短縮](../../../../services/genai-apps.md#latency)と [CloudWatch のメトリクス](../../../../services/ai.md#bedrock-metrics): 指標の違いを確認します。
2. [クォータの計算例](../../../../services/ai.md#quotas-detail): 予約、消費、課金の計算をします。
3. [予約済み同時実行](../../../../services/lambda.md#reserved-concurrency)と [Map の設定](../../../../services/step-functions.md#map-settings): 流量の制御を押さえます。
4. [パラメータの調整](../../../../services/genai-apps.md#parameter-tuning)と [inferenceConfig](../../../../services/ai.md#inference-config): 用途ごとの値と `additionalModelRequestFields` を理解します。
5. [X-Ray](../../../../services/observability.md#xray)と[接続の再利用](../../../../services/sdk-resilience.md#connection-reuse): どこが遅いかの測り方を確認します。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| 抽出、分類、SQL の `temperature` | 0〜0.2 | 再現性 |
| 一般の質問応答 | 0.2〜0.5 |  |
| 文案、アイデア | 0.7 以上 | 多様性 |
| 開始時の予約 | 入力 + `max_tokens` | 完了時に戻る |
| 完了時の消費 | 入力 + 出力 × 消費率 | 課金は実際のトークン |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 最初の文字が遅い | `TimeToFirstToken` を調べる |
| 全体を短くする | 小さなモデル、短い入力 |
| 予測できる質問 | 事前計算 |
| 独立した処理 | 同時に実行 |
| `top_k` を渡す | `additionalModelRequestFields` |

## 引っかかりやすい点 {#traps}

- ストリーミングで `InvocationLatency` は変わりません。
- `temperature` を 0 にしても誤りはなくなりません。
- 測らずにモデルを小さくしません。検索、リランク、生成に分けて測ります。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [performance 問1](../../exercises/performance.md#q1) | 4.2.1 | 利用者から「最初の文字が出るまで遅い」と苦情があります。InvocationLatency は許容範… |
| [performance 問2](../../exercises/performance.md#q2) | 4.2.1 | ストリーミングに変えたところ、体感は改善しましたが、バックエンドの処理全体の時間を指標にしている S… |
| [performance 問3](../../exercises/performance.md#q3) | 4.2.1 | ニュースの要約の配信で、毎朝、よく読まれる上位 100 件の質問はほぼ決まっています。朝のピークに … |
| [performance 問4](../../exercises/performance.md#q4) | 4.2.1 | 1 つの依頼で、要約、翻訳、感情分析の 3 つの独立した処理を順に実行しており、15 秒かかります。… |
| [performance 問5](../../exercises/performance.md#q5) | 4.2.3 | 出力の消費率が 5 倍のモデルで、入力 1,000、max_tokens 8,000、実際の出力 1… |
| [performance 問6](../../exercises/performance.md#q6) | 4.2.3 | SQS から Lambda で FM を呼ぶ処理と、Step Functions の Map で文書… |
| [performance 問7](../../exercises/performance.md#q7) | 4.2.3 | 日中のチャットと、毎日の 50 万件の要約が同じモデルのクォータを取り合っています。要約は翌朝までに… |
| [performance 問8](../../exercises/performance.md#q8) | 4.2.4 | SQL を生成する機能、顧客向けの一般の質問応答、広告のアイデア出しの 3 つの機能があります。te… |
| [performance 問9](../../exercises/performance.md#q9) | 4.2.4 | Converse の inferenceConfig に top_k を入れたところ、Validat… |
| [performance 問10](../../exercises/performance.md#q10) | 4.2.4 | 抽出の処理で事実の誤りが目立つので、担当者が temperature を 0 にして「これで誤りはな… |
| [performance 問11](../../exercises/performance.md#q11) | 4.2.4 | 要約の出力に、不要な署名の定型文が付きます。定型文は必ず「---」で始まります。トークンの費用も抑え… |
| [performance 問12](../../exercises/performance.md#q12) | 4.2.6 | RAG のアプリの p95 の遅延が要件を超えました。チームは「生成が遅いはずだ」と考えて、すぐにモ… |
| [performance 問13](../../exercises/performance.md#q13) | 4.2.6 | Lambda で FM を呼ぶ関数で、X-Ray を見ると、毎回 TLS の接続の確立に時間がかかっ… |
| [performance 問14](../../exercises/performance.md#q14) | 4.2.6 | どの種類のプロンプトで応答が遅いのかを調べます。呼び出しログは有効です。プロンプトと応答の長さと遅延… |
| [performance 問15](../../exercises/performance.md#q15) | 4.2.3, 4.2.6 | 朝のピークに、チャットの応答が遅くなり、ThrottlingException も増えます。調査の結… |

<!-- questions:end -->

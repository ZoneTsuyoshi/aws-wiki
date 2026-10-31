# 分野1: LLM を使った処理

LLM の呼び出し方の選択を問います。モデルの学習は範囲外です。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [1.2.10](../../domain1.md#skill-1-2-10) | LLM を使ったデータ処理 |

## 学習の順番 {#study-order}

1. [Bedrock Runtime](../../../../services/ai.md#bedrock-runtime): Converse API を確認します。
2. [スループットの選択肢](../../../../services/ai.md#throughput-options): バッチ推論の条件を確認します。
3. [エラーとスロットリング](../../../../services/ai.md#errors-throttling): `ThrottlingException` の対処を覚えます。
4. [Data Automation](../../../../services/genai-apps.md#bda): PDF や音声の構造化を確認します。

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| パイプラインの中で 1 件ずつ呼ぶ | Lambda から Converse API |
| 大量のデータを非同期で処理する | Bedrock のバッチ推論 |
| PDF、画像、音声を構造化する | Bedrock Data Automation |
| 手順の連結と再試行 | Step Functions |

## 引っかかりやすい点 {#traps}

- バッチ推論はプロビジョンドのモデルでは使えません。
- レート制限には SQS とバックオフで対応します。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [genai-vector 問1](../../exercises/genai-vector.md#q1) | 1.2.10 | S3 に置いた 100 万件の問い合わせ文を、LLM で分類します。即時の応答は要らず、一度に処理し… |
| [genai-vector 問2](../../exercises/genai-vector.md#q2) | 1.2.10 | PDF の請求書と音声の記録を、パイプラインで構造化データにします。自分でモデルの呼び出しを組み立て… |
| [genai-vector 問3](../../exercises/genai-vector.md#q3) | 1.2.10 | Lambda から Converse API を呼ぶパイプラインで、急増時に ThrottlingE… |
| [genai-vector 問4](../../exercises/genai-vector.md#q4) | 1.2.10 | Bedrock のバッチ推論について正しいものはどれですか。 |

<!-- questions:end -->

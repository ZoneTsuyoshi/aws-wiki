# 分野1: FM の学習データ

カスタマイズの手法ごとに必要なデータが違います。形式の値も問われます。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [1.2.9](../../domain1.md#skill-1-2-9) | FM のカスタマイズ向けのデータ準備 |

## 学習の順番 {#study-order}

1. [モデルカスタマイズ](../../../../services/genai-apps.md#customization): 手法と必要なデータを対応させます。
2. [データの準備](../../../../services/genai-apps.md#fine-tuning-data): JSONL と `schemaVersion` を確認します。
3. [方法の比較](../../../../services/ai-fundamentals.md#customization-options): 手法の選び方をつかみます。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| 形式 | `.jsonl`、1 行 1 件 | S3 に置く |
| 会話形式 | `schemaVersion: bedrock-conversation-2024` | |

## こう問われたらこう考える {#decisions}

| 手法 | 必要なデータ |
|---|---|
| 教師ありファインチューニング | 入力と出力の組 |
| 強化ファインチューニング | プロンプトと報酬関数（Lambda） |
| 蒸留 | プロンプト。教師モデルの応答で調整する |
| 継続的な事前学習 | ラベルのない大量のデータ |

## 引っかかりやすい点 {#traps}

- 現在の Bedrock の一覧にあるのは教師あり、強化、蒸留の 3 つです。継続的な事前学習はガイドに残る用語として押さえます。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [fm-customization 問1](../../exercises/fm-customization.md#q1) | 1.2.9 | Bedrock の教師ありファインチューニングの学習データを準備します。形式と置き場所として正しいも… |
| [fm-customization 問2](../../exercises/fm-customization.md#q2) | 1.2.9 | 会話形式で学習データを作ります。各行に指定する schemaVersion はどれですか。 |
| [fm-customization 問3](../../exercises/fm-customization.md#q3) | 1.2.9 | 強化ファインチューニングに必要なものの組み合わせはどれですか。 |

<!-- questions:end -->

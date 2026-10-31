# 分野3: 選定と推論パラメータ

FM を選ぶ基準と、パラメータを変えたときの効果を問います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [3.1.1](../../domain3.md#obj-3-1-1) | FM を選ぶ基準 |
| [3.1.2](../../domain3.md#obj-3-1-2) | 推論パラメータの効果 |

## 学習の順番 {#study-order}

1. [選定の観点](../../../../services/genai-apps.md#fm-criteria): 基準の一覧と PoC の進め方を確認します。
2. [キャッシュの種類](../../../../services/genai-apps.md#caching): プロンプトキャッシュの効果を押さえます。
3. [推論パラメータ](../../../../services/ai-fundamentals.md#inference-parameters): 各パラメータの低いときと高いときの動きを覚えます。
4. [パラメータの調整](../../../../services/genai-apps.md#parameter-tuning): 用途ごとの temperature の目安を確認します。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| temperature（抽出、分類） | 0 に近く | 再現性を優先 |
| temperature（文案） | 高めに | 多様性を優先 |
| top-p = 0.8 の例 | A 0.50、B 0.30 まで | 累積が 0.8 に届くまで |
| top-k = 1 | 最も確率の高い 1 つ | 常に同じ候補 |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 候補を公平に比べる | 同じプロンプトと評価データで表にする |
| 対話の応答を速くする | 小さなモデルとストリーミング |
| 長い契約書を一度に読ませる | コンテキスト長の大きいモデル |
| 応答が途中で切れる | 最大トークンを増やす |
| 分類の結果を安定させる | temperature を 0 に近くする |

## 引っかかりやすい点 {#traps}

- 入力が長いと、費用と遅延が増え、上限にも近づきます。
- temperature は正しさを保証しません。
- 日本語の品質は日本語のデータで確かめます。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [model-selection 問5](../../exercises/model-selection.md#q5) | 3.1.1 | FM を比較するときの進め方として適切なものはどれですか。 |
| [model-selection 問6](../../exercises/model-selection.md#q6) | 3.1.1 | 音声の対話アプリで、利用者が話し終えてから応答が始まるまでの時間を重視します。選定の基準として最も重… |
| [model-selection 問7](../../exercises/model-selection.md#q7) | 3.1.1 | 100 ページの契約書を分割せずに読ませて要約したいと考えています。確認すべきモデルの基準はどれです… |
| [model-selection 問8](../../exercises/model-selection.md#q8) | 3.1.1 | 日本語の顧客対応に使う FM を選びます。多言語の基準での適切な確認はどれですか。 |
| [model-selection 問9](../../exercises/model-selection.md#q9) | 3.1.2 | 同じ FM で、広告の文案と問い合わせの分類の両方を行います。temperature の使い分けとし… |
| [model-selection 問10](../../exercises/model-selection.md#q10) | 3.1.2 | 次の語の候補が A 0.50、B 0.30、C 0.15、D 0.05 のとき、top-p = 0.… |
| [model-selection 問11](../../exercises/model-selection.md#q11) | 3.1.2 | 応答が文の途中で終わっています。まず調整するパラメータはどれですか。 |
| [model-selection 問12](../../exercises/model-selection.md#q12) | 3.1.2 | 入力のプロンプトを大幅に長くしたときの影響として正しいものを選んでください。（2つ選択） |

<!-- questions:end -->

# 分野1: データ品質とバイアス

データの品質をルールで検査し、ラベルの誤りとバイアス、不均衡に対応します。CI と DPL は計算で問われます。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [1.3.1](../../domain1.md#skill-1-3-1) | データ品質の検証 |
| [1.3.2](../../domain1.md#skill-1-3-2) | ラベル付けとアノテーション |
| [1.3.3](../../domain1.md#skill-1-3-3) | データのバイアスの特定と緩和 |
| [1.3.4](../../domain1.md#skill-1-3-4) | マルチモーダルデータの分布の最適化 |
| [1.3.5](../../domain1.md#skill-1-3-5) | クラス不均衡の解消 |

## 学習の順番 {#study-order}

1. [Glue Data Quality](../../../../services/data-engineering.md#glue-data-quality)と [DataBrew](../../../../services/data-engineering.md#databrew): DQDL の書き方と、画面での確認を区別します。
2. [Ground Truth](../../../../services/sagemaker.md#ground-truth): 自動ラベル付けと作業者の種類を確認します。提供状況にも注意します。
3. [バイアス指標](../../../../services/sagemaker.md#clarify-metrics): CI と DPL を計算できるようにします。
4. [Clarify](../../../../services/sagemaker.md#clarify): 新規に使えない場合の代替を覚えます。
5. [データ品質と不均衡](../../../../services/ai-fundamentals.md#data-quality)と[分類の指標](../../../../services/ai-fundamentals.md#classification-metrics): 手法の違いと評価の方法を押さえます。

## 覚える値 {#values}

| 項目 | 例 | 判断のポイント |
|---|---|---|
| CI | 800 人と 200 人で 0.6 | 集団の人数の差 |
| DPL | 0.6 と 0.3 で 0.3 | 陽性ラベルの割合の差 |
| DQDL | `Completeness "email" > 0.95` | `IsComplete` は全件の確認 |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| ETL の中で悪いデータを止める | Glue Data Quality |
| 分布と欠損を画面で確認する | DataBrew のプロファイルジョブ |
| 機密の画像のラベル付け | プライベートのワークフォース |
| ラベルの誤りが多い | 複数人の確認と判定者間の一致度 |
| CI が大きい | 少ない集団のデータを追加し、拡張する |
| DPL が大きい | ラベルの付け方を確認する |
| データを変えずに少数クラスを重視する | クラスの重み付け |

## 引っかかりやすい点 {#traps}

- Ground Truth と Clarify は新規顧客の受付を終了しています。試験には役割の理解が必要です。
- Bedrock Evaluations は表データのバイアス検出の代わりになりません。
- 再サンプリングは学習データだけに適用します。テストは本番に近い分布のまま残します。
- 不均衡なデータでは accuracy を使わず、適合率、再現率、PR 曲線を見ます。
- 時系列はシャッフルせず、時間順に分けます。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [data-quality 問1](../../exercises/data-quality.md#q1) | 1.3.1 | Glue の ETL ジョブの中で、注文 ID の欠損を検査し、基準を満たさないデータをロードの前に… |
| [data-quality 問2](../../exercises/data-quality.md#q2) | 1.3.1 | メールアドレスの列は 95% より多く値が入っていれば合格にします。DQDL の書き方はどれですか。 |
| [data-quality 問3](../../exercises/data-quality.md#q3) | 1.3.1 | 分析担当者が、コードなしで新しいデータセットの分布と欠損を画面で確認し、品質のルールも作ります。最も… |
| [data-quality 問4](../../exercises/data-quality.md#q4) | 1.3.2 | Ground Truth を既に利用しているチームが、大量の画像のラベル付けの費用を下げたいです。正… |
| [data-quality 問5](../../exercises/data-quality.md#q5) | 1.3.2 | 既に Ground Truth を利用しているチームが、機密の医療画像をラベル付けします。社外の人に… |
| [data-quality 問6](../../exercises/data-quality.md#q6) | 1.3.2 | ラベルの誤りが多いことが分かりました。品質を上げる対応として適切なものはどれですか。（2つ選択） |
| [data-quality 問7](../../exercises/data-quality.md#q7) | 1.3.3 | 学習データに男性が 800 人、女性が 200 人います。学習前のバイアス指標 CI（class i… |
| [data-quality 問8](../../exercises/data-quality.md#q8) | 1.3.3 | ある集団の陽性ラベルの割合は 0.6、別の集団は 0.3 です。DPL の値と、その指標が示すものの… |
| [data-quality 問9](../../exercises/data-quality.md#q9) | 1.3.3 | 新規に作るモデルで表データのバイアスを検査します。アカウントは SageMaker Clarify … |
| [data-quality 問10](../../exercises/data-quality.md#q10) | 1.3.4 | 画像の分類モデルで、撮影地域ごとの精度に差があります。画像のデータでも学習前のバイアスを確認したいで… |
| [data-quality 問11](../../exercises/data-quality.md#q11) | 1.3.4 | 問い合わせ文の話題分類のデータを言語ごとに集計したところ、CI が大きく、日本語の件数が少ないと分か… |
| [data-quality 問12](../../exercises/data-quality.md#q12) | 1.3.4 | 画像データの地域間で枚数は同じですが、ある地域だけ陽性ラベルの割合が極端に低いです。最初に確認すべき… |
| [data-quality 問13](../../exercises/data-quality.md#q13) | 1.3.5 | 陽性が 1% の表データです。データそのものは変えずに、少数クラスの誤りを重く扱いたいです。適切な手… |
| [data-quality 問14](../../exercises/data-quality.md#q14) | 1.3.5 | 不均衡な表データで SMOTE を試します。Data Wrangler で実行するときの正しい進め方… |
| [data-quality 問15](../../exercises/data-quality.md#q15) | 1.3.5 | ランダムオーバーサンプリングを使ったところ、検証の指標がよくありません。学習の指標だけ高いです。最も… |
| [data-quality 問16](../../exercises/data-quality.md#q16) | 1.3.3 | 時系列の売上データを学習用とテスト用に分けます。バイアスと漏えいを防ぐ正しい方法はどれですか。 |

<!-- questions:end -->

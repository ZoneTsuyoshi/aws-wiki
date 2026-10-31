# 分野4: 責任ある AI

状況の説明から特徴やリスクの名前を選びます。全体の精度だけでは見つからない問題に注意します。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [4.1.1](../../domain4.md#obj-4-1-1) | 責任ある AI の特徴 |
| [4.1.3](../../domain4.md#obj-4-1-3) | 責任あるモデルの選択 |
| [4.1.4](../../domain4.md#obj-4-1-4) | 生成 AI の法的なリスク |
| [4.1.5](../../domain4.md#obj-4-1-5) | データセットの特徴 |
| [4.1.6](../../domain4.md#obj-4-1-6) | バイアスとバリアンスの影響 |
| [4.1.7](../../domain4.md#obj-4-1-7) | バイアス、信頼性、真実性を検出し監視するツール |

## 学習の順番 {#study-order}

1. [AWS の 8 つの観点](../../../../services/ai-fundamentals.md#rai-dimensions): AWS の 8 つの観点と例を覚えます。
2. [バイアスと公平性](../../../../services/ai-fundamentals.md#fairness): バイアスが入る段階と検出の手法を押さえます。
3. [データ品質と不均衡](../../../../services/ai-fundamentals.md#data-quality): データの不均衡の影響を確認します。
4. [過学習、バイアス、バリアンス](../../../../services/ai-fundamentals.md#overfitting): 高バイアスと高バリアンスの違いを確認します。
5. [法的なリスク](../../../../services/ai-fundamentals.md#legal-risks): リスクと対応の組み合わせを覚えます。
6. [Bedrock Evaluations](../../../../services/genai-apps.md#bedrock-evaluations)と[Well-Architected Framework](../../../../services/cloud-foundations.md#well-architected): 評価の安全の指標と、サステナビリティの柱を確認します。

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 集団で結果が違わないか | 公平性 |
| 敵対的な入力でも動くか | 堅牢性 |
| 方言でも使えるか | 包摂性 |
| 他者の作品に酷似する | 知的財産の侵害の主張 |
| 差別的な結果で訴えられる | 偏ったモデルの出力。公平性の評価 |
| 誤った医療の助言 | 利用者への危険。免責と専門家への誘導 |
| 両方の精度が低い | 高バイアス（過少適合） |
| 新しいデータだけ精度が低い | 高バリアンス（過学習） |
| 特定の集団から不満が出る | サブグループ分析 |
| 判定者のラベルが食い違う | ラベル品質の分析 |
| FM の偏りを導入前に比較する | Bedrock の評価 |

## 引っかかりやすい点 {#traps}

- 統計のバイアスと公平性のバイアスは別の意味です。
- Clarify はバイアスの検出と SHAP による説明の機能ですが、新規顧客を受け付けていません。
- 足りる範囲で小さなモデルを選ぶと、費用と環境負荷の両方が下がります。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [responsible-ai 問1](../../exercises/responsible-ai.md#q1) | 4.1.1 | 地域によって融資の承認率が不当に違わないかを確認しています。責任ある AI のどの特徴に当たりますか… |
| [responsible-ai 問2](../../exercises/responsible-ai.md#q2) | 4.1.1 | 誤字だらけの入力や敵対的な入力を与えて、モデルの動作を確かめています。責任ある AI のどの特徴に当… |
| [responsible-ai 問3](../../exercises/responsible-ai.md#q3) | 4.1.1 | 音声アシスタントが方言の話者にも同じように使えるよう、データを増やしました。この取り組みの特徴はどれ… |
| [responsible-ai 問4](../../exercises/responsible-ai.md#q4) | 4.1.1 | AWS が責任ある AI の観点として挙げているものを選んでください。（3つ選択） |
| [responsible-ai 問5](../../exercises/responsible-ai.md#q5) | 4.1.3 | 単純な問い合わせの分類に、最大のモデルと、十分な性能の小さなモデルのどちらを使うかを検討しています。… |
| [responsible-ai 問6](../../exercises/responsible-ai.md#q6) | 4.1.3 | 責任あるモデルの選択で、環境への負荷を減らす実践を選んでください。（2つ選択） |
| [responsible-ai 問7](../../exercises/responsible-ai.md#q7) | 4.1.3 | AWS Well-Architected Framework の柱のうち、環境への影響に関わるものは… |
| [responsible-ai 問8](../../exercises/responsible-ai.md#q8) | 4.1.4 | 画像生成 AI で作った広告が、他社の作品に酷似していると指摘されました。このリスクはどれですか。 |
| [responsible-ai 問9](../../exercises/responsible-ai.md#q9) | 4.1.4 | チャットボットが誤った服薬の助言をして、利用者に害が出るおそれがあります。適切な備えはどれですか。 |
| [responsible-ai 問10](../../exercises/responsible-ai.md#q10) | 4.1.4 | 採用支援の AI が差別的な結果を出し、訴えられました。関係する法的なリスクと対応の組み合わせはどれ… |
| [responsible-ai 問11](../../exercises/responsible-ai.md#q11) | 4.1.4 | 公開のチャットボットの誤回答が SNS で拡散し、批判が集まりました。主に当たるリスクと対応はどれで… |
| [responsible-ai 問12](../../exercises/responsible-ai.md#q12) | 4.1.5 | 与信のモデルの学習データを、影響を受ける人々を広く含むよう見直しています。データセットのどの特徴を高… |
| [responsible-ai 問13](../../exercises/responsible-ai.md#q13) | 4.1.5 | 学習データの 9 割が特定の集団で占められています。起きやすい問題はどれですか。 |
| [responsible-ai 問14](../../exercises/responsible-ai.md#q14) | 4.1.5 | 権利の確認が取れていない Web のデータを学習に使おうとしています。不足している特徴はどれですか。 |
| [responsible-ai 問15](../../exercises/responsible-ai.md#q15) | 4.1.5 | データセットの望ましい特徴を選んでください。（2つ選択） |
| [responsible-ai 問16](../../exercises/responsible-ai.md#q16) | 4.1.6 | 学習データでも検証データでも精度が低いモデルがあります。この状態と原因はどれですか。 |
| [responsible-ai 問17](../../exercises/responsible-ai.md#q17) | 4.1.6 | 精度が学習データでは 99%、新しいデータでは 68% でした。対策として適切なものはどれですか。 |
| [responsible-ai 問18](../../exercises/responsible-ai.md#q18) | 4.1.6 | ある地域のデータばかりで学習した与信モデルを全国で使っています。全体の精度は高いのですが、起こりうる… |
| [responsible-ai 問19](../../exercises/responsible-ai.md#q19) | 4.1.6 | 「バイアス」の 2 つの意味の説明として正しいものはどれですか。 |
| [responsible-ai 問20](../../exercises/responsible-ai.md#q20) | 4.1.7 | 書類選考モデルの全体の精度は 92% ですが、特定の年齢層から不満が出ています。まず行うことはどれで… |
| [responsible-ai 問21](../../exercises/responsible-ai.md#q21) | 4.1.7 | 複数の判定者が付けたラベルが大きく食い違っています。この状況を調べる手法はどれですか。 |
| [responsible-ai 問22](../../exercises/responsible-ai.md#q22) | 4.1.7 | 指標に出にくい問題を見つけるために、人が出力を抜き取って確認しています。この手法はどれですか。 |
| [responsible-ai 問23](../../exercises/responsible-ai.md#q23) | 4.1.7 | FM の偏りと有害性を導入前に比較したいと考えています。適切な機能と指標の組み合わせはどれですか。 |

<!-- questions:end -->

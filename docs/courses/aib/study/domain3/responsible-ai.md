# 分野3: 責任ある AI

責任ある AI の観点を場面に当てはめ、事業の目標と対立したときの判断、企画の段階からの組み込み、人の監督を問います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [3.1.1](../../domain3.md#skill-3-1-1) | 責任ある AI の原則と観点 |
| [3.1.2](../../domain3.md#skill-3-1-2) | 事業目標と原則の対立 |
| [3.1.3](../../domain3.md#skill-3-1-3) | ガバナンス・バイ・デザイン |
| [3.1.4](../../domain3.md#skill-3-1-4) | 人の監督と安全策 |

## 学習の順番 {#study-order}

1. [AWS の 8 つの観点](../../../../services/ai-fundamentals.md#rai-dimensions): 場面から観点を言えるようにします。
2. [説明可能性と透明性](../../../../services/ai-fundamentals.md#explainability): 混同しやすい 2 つを区別します。
3. [役割と責任](../../../../services/ai-fundamentals.md#governance-roles): 企画の段階から統治を組み込む考え方を確認します。
4. [人による監督](../../../../services/ai-fundamentals.md#human-oversight): 人が判断すべき場面と、エスカレーションの基準を覚えます。
5. [Guardrails](../../../../services/ai.md#guardrails)、[コンテキストグラウンディング](../../../../services/genai-apps.md#contextual-grounding): 機能の名前と役割を押さえます。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| 観点の数 | AWS の責任ある AI のページは 8 つ、Lens は 10 個 | 個数より意味を押さえる |
| Responsible AI Lens | 8 つのフォーカスエリア | 順守のチェックリストではない |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 性別でスコアが違う | 公平性 |
| 否決の理由を示せない | 説明可能性 |
| AI と知らずに話している | 透明性 |
| 止める手段がない | 制御可能性 |
| 外部モデルの責任者がいない | ガバナンス |
| 説明が必須の審査 | 精度が少し下がっても説明できるモデル |
| 発売を急ぐが高リスクの部分がある | 低リスクの範囲を先に出し、高リスクは評価の後に |
| 引き継ぎの基準 | 信頼度、金額、話題で事前に決めて文書にする |
| 参照元に基づかない回答を検出する | コンテキストグラウンディング |

## 引っかかりやすい点 {#traps}

- 説明可能性は「なぜその出力か」、透明性は「AI を使っていること、その能力と限界を伝えているか」です。
- 免責の表示は評価の代わりになりません。
- 全面的な可否だけでなく、範囲を分ける選択肢を考えます。
- ハルシネーションの検査を入れても、人の確認の代わりにはなりません。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [responsible-ai 問1](../../exercises/responsible-ai.md#q1) | 3.1.1 | 応募者を採点する AI で、同じ経歴でも性別によってスコアが違うことがわかりました。責任ある AI … |
| [responsible-ai 問2](../../exercises/responsible-ai.md#q2) | 3.1.1 | 融資を断られた顧客から理由を聞かれましたが、担当者はモデルの判断の理由を示せません。どの観点の問題で… |
| [responsible-ai 問3](../../exercises/responsible-ai.md#q3) | 3.1.1 | 顧客は、チャットの相手を人間の担当者だと思って相談していました。会社は AI であることを伝えていま… |
| [responsible-ai 問4](../../exercises/responsible-ai.md#q4) | 3.1.1 | 本番の AI が誤った案内を続けているのに、誰も止める手段を持っていませんでした。どの観点が欠けてい… |
| [responsible-ai 問5](../../exercises/responsible-ai.md#q5) | 3.1.1 | 外部から調達したモデルについて、評価の責任者が決まっておらず、提供者と自社の役割分担も不明確です。ど… |
| [responsible-ai 問6](../../exercises/responsible-ai.md#q6) | 3.1.1 | 次の場面と観点の組み合わせのうち、正しいものはどれですか。（2つ選択） |
| [responsible-ai 問7](../../exercises/responsible-ai.md#q7) | 3.1.1 | 担当者が「Well-Architected の Responsible AI Lens を全項目満た… |
| [responsible-ai 問8](../../exercises/responsible-ai.md#q8) | 3.1.2 | 審査の結果を顧客と当局に説明する必要がある融資で、案 1 は精度がやや高いものの理由を示せず、案 2… |
| [responsible-ai 問9](../../exercises/responsible-ai.md#q9) | 3.1.2 | 事業部門は、保険金の支払いの判断をすべて AI で自動化して処理を速くしたいと考えています。一方、高… |
| [responsible-ai 問10](../../exercises/responsible-ai.md#q10) | 3.1.2 | マーケティング部門は、個人化の精度を上げるために、位置情報や閲覧の全履歴を集めたいと考えています。最… |
| [responsible-ai 問11](../../exercises/responsible-ai.md#q11) | 3.1.2 | 競合より先に発売したい顧客向けの機能に、医療の助言の部分が含まれています。安全性の評価はまだ終わって… |
| [responsible-ai 問12](../../exercises/responsible-ai.md#q12) | 3.1.3 | 責任ある AI の確認を、プロジェクトのどの時点から組み込むべきですか。 |
| [responsible-ai 問13](../../exercises/responsible-ai.md#q13) | 3.1.3 | ガバナンス・バイ・デザインの考え方で、企画の段階に行うこととして最も適切なものはどれですか。 |
| [responsible-ai 問14](../../exercises/responsible-ai.md#q14) | 3.1.3 | データの選定の段階で確認すべきこととして、最も適切なものはどれですか。 |
| [responsible-ai 問15](../../exercises/responsible-ai.md#q15) | 3.1.3 | 製品チームは「審査が遅いので、完成してから一度にガバナンスの確認を受けたい」と言っています。リスク部… |
| [responsible-ai 問16](../../exercises/responsible-ai.md#q16) | 3.1.4 | 人の監督が最も強く求められる場面はどれですか。 |
| [responsible-ai 問17](../../exercises/responsible-ai.md#q17) | 3.1.4 | 問い合わせの AI をいつ人の担当者に引き継ぐかについて、最も適切な決め方はどれですか。 |
| [responsible-ai 問18](../../exercises/responsible-ai.md#q18) | 3.1.4 | 顧客向けのチャットで、有害な内容を防ぎ、投資の助言の話題を断り、個人情報をマスクしたいと考えています… |
| [responsible-ai 問19](../../exercises/responsible-ai.md#q19) | 3.1.4, 3.3.4 | RAG のチャットボットで、参照元の文書に基づかない回答を検出したいと考えています。Amazon B… |
| [responsible-ai 問20](../../exercises/responsible-ai.md#q20) | 3.1.4 | 医療機関が、AI の診断の補助を導入します。適切な安全策はどれですか。（2つ選択） |

<!-- questions:end -->

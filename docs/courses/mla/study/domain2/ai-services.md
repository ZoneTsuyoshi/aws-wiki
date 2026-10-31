# 分野2: AI サービス

決まった作業には専用の AI サービスを選びます。FM や独自の学習とのトレードオフも問います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [2.1.4](../../domain2.md#skill-2-1-4) | 独自開発、マネージド、事前学習済み、FM のトレードオフ |
| [2.1.8](../../domain2.md#skill-2-1-8) | AWS の AI サービスの適用 |

## 学習の順番 {#study-order}

1. [AI の 3 階層](../../../../services/ai-managed-services.md#three-layers)と[マネージド AI サービスと Bedrock](../../../../services/ai-managed-services.md#vs-bedrock): 制御と手間の関係をつかみます。
2. [選び方](../../../../services/ai-managed-services.md#choosing): 業務とサービスの対応を覚えます。
3. [紛らわしい組み合わせ](../../../../services/ai-managed-services.md#confusing-pairs): Comprehend と Textract、Rekognition と Textract を区別します。

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| OCR を大量に確実に | Textract |
| 感情、固有表現 | Comprehend |
| 不適切な画像の検出 | Rekognition |
| レコメンド | Personalize |
| FHIR の医療データ | HealthLake |
| FM を自分のインスタンスで制御する | JumpStart |
| 独自の表データとアルゴリズム | SageMaker AI で独自に学習 |

## 引っかかりやすい点 {#traps}

- 決まった作業に FM を使うと、コストがかさみ、出力も揺れやすくなります。
- Comprehend は文の意味、Textract は文書の文字を扱います。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [ai-services 問4](../../exercises/ai-services.md#q4) | 2.1.4 | 請求書を毎日 10 万枚処理し、決まった項目を確実に抽出します。出力の形式は固定で、再現性を重視しま… |
| [ai-services 問5](../../exercises/ai-services.md#q5) | 2.1.4 | 自社の FM を選んで GPU の種類も細かく決め、VPC の中で運用します。多少の手間は問題ありま… |
| [ai-services 問6](../../exercises/ai-services.md#q6) | 2.1.4 | 自社の表データと独自のアルゴリズムで需要を予測します。制御を最大にし、運用の手間は受け入れます。どの… |
| [ai-services 問7](../../exercises/ai-services.md#q7) | 2.1.8 | 製品レビューの文章から、感情と製品名などの固有表現を取り出します。モデルの学習や運用はしたくありませ… |
| [ai-services 問8](../../exercises/ai-services.md#q8) | 2.1.8 | SNS に投稿された画像から不適切な内容を検出します。どのサービスですか。 |
| [ai-services 問9](../../exercises/ai-services.md#q9) | 2.1.8 | 次の業務とサービスの組み合わせとして正しいものを選んでください。（2つ選択） |
| [ai-services 問10](../../exercises/ai-services.md#q10) | 2.1.8 | FHIR 形式の医療データを、FHIR の API で保存、検索して分析します。データストアの運用は… |

<!-- questions:end -->

# 分野2: マネージド AI サービス

機能ごとの専用サービスがあれば、モデルを自分で作りません。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [マネージド AI サービスの用途](../../domain2.md#t2-2-managed-ai) | マネージドサービスの適切な用途、ワークロードに合う専用サービスの利用 |

## 学習の順番 {#study-order}

1. [Amazon Comprehend](../../../../services/ai-managed-services.md#comprehend)と[Amazon Translate](../../../../services/ai-managed-services.md#translate): テキストの分析と翻訳を確認します。
2. [Amazon Polly](../../../../services/ai-managed-services.md#polly)と[Amazon Transcribe](../../../../services/ai-managed-services.md#transcribe): 方向が逆の 2 つを区別します。
3. [Amazon Textract](../../../../services/ai-managed-services.md#textract)と[Amazon Rekognition](../../../../services/ai-managed-services.md#rekognition): 文書の抽出と画像の分析を区別します。
4. [Amazon Lex](../../../../services/ai-managed-services.md#lex): 会話型のボットの部品を確認します。

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 感情分析、固有表現の抽出 | Comprehend |
| テキストを音声に | Polly |
| 音声をテキストに | Transcribe |
| 文書から文字と表を抽出 | Textract |
| 画像や動画の分析 | Rekognition |
| 翻訳 | Translate |
| チャットボット | Lex |
| 独自のモデルの学習とデプロイ | SageMaker AI |

## 引っかかりやすい点 {#traps}

- SageMaker AI を選ぶのは、独自のモデルを作る要件があるときです。
- Polly と Transcribe は方向が逆です。
- Macie は S3 の機密データが対象で、画像の内容の判定には使いません。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [ai-services 問1](../../exercises/ai-services.md#q1) | マネージド AI | 顧客のレビューを肯定、否定に分類し、製品名も抽出します。モデルの学習はしません。どれを選びますか。 |
| [ai-services 問2](../../exercises/ai-services.md#q2) | マネージド AI | Web の記事をテキストから音声に変えて配信します。どれを選びますか。 |
| [ai-services 問3](../../exercises/ai-services.md#q3) | マネージド AI | コールセンターの録音を文字に起こして、検索できるようにします。どれを選びますか。 |
| [ai-services 問4](../../exercises/ai-services.md#q4) | マネージド AI | スキャンした請求書の PDF から、表とキーと値の組を抽出します。OCR のモデルは作りたくありませ… |
| [ai-services 問5](../../exercises/ai-services.md#q5) | マネージド AI | 投稿された画像に不適切な内容がないかを、モデルを学習せずに自動で判定します。どれを選びますか。 |
| [ai-services 問6](../../exercises/ai-services.md#q6) | マネージド AI | 製品マニュアルの英語のテキストを日本語にします。どれを選びますか。 |
| [ai-services 問7](../../exercises/ai-services.md#q7) | マネージド AI | 問い合わせの窓口で、音声とテキストで予約を受け付ける会話型のボットを作ります。どれを選びますか。 |
| [ai-services 問8](../../exercises/ai-services.md#q8) | マネージド AI | 自社の独自のデータと特徴量で需要予測のモデルを作り、学習からデプロイまで管理します。どれを選びますか… |
| [ai-services 問9](../../exercises/ai-services.md#q9) | マネージド AI | 外国語のコールの録音を、日本語の要約の分析につなげます。処理の順に正しいサービスの組み合わせはどれで… |
| [ai-services 問10](../../exercises/ai-services.md#q10) | マネージド AI | 専用のサービスを選ぶ判断として適切なものを選んでください。（2つ選択） |

<!-- questions:end -->

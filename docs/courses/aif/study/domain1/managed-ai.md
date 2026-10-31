# 分野1: マネージド AI サービス

入力と出力の組み合わせからサービスを選びます。名前の似たサービスの区別と、新規受付を終えたサービスの扱いが要点です。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [1.2.4](../../domain1.md#obj-1-2-4) | 実世界の AI の活用例 |
| [1.2.5](../../domain1.md#obj-1-2-5) | AWS のマネージド AI/ML サービスの機能 |

## 学習の順番 {#study-order}

1. [マネージド AI サービスと Bedrock](../../../../services/ai-managed-services.md#vs-bedrock): 決まった作業か、自由な生成かで分けます。
2. [紛らわしい組み合わせ](../../../../services/ai-managed-services.md#confusing-pairs): 紛らわしい組み合わせを表で覚えます。
3. [Amazon Comprehend](../../../../services/ai-managed-services.md#comprehend)と[Amazon Lex](../../../../services/ai-managed-services.md#lex): テキストの分析と、手続きの対話の違いを確認します。
4. [Amazon Textract](../../../../services/ai-managed-services.md#textract)と[Amazon Rekognition](../../../../services/ai-managed-services.md#rekognition): 文書と写真、動画を分けます。
5. [Amazon Transcribe](../../../../services/ai-managed-services.md#transcribe)と[Amazon Polly](../../../../services/ai-managed-services.md#polly): 音声と文字の向きを確認します。
6. [Amazon Translate](../../../../services/ai-managed-services.md#translate)と[Amazon Personalize](../../../../services/ai-managed-services.md#personalize): 翻訳とレコメンドの用途を押さえます。

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 音声 → 文字 | Transcribe |
| 文字 → 音声 | Polly |
| テキスト → 別の言語 | Translate |
| テキスト → 感情、固有表現、PII | Comprehend |
| 音声やテキストの手続きの対話 | Lex |
| 文書 → 文字と表 | Textract |
| 画像や動画 → ラベル、モデレーション | Rekognition |
| 行動履歴 → おすすめ | Personalize |
| データ → 独自のモデル | SageMaker AI |
| 社内規定への質問応答（新規） | Bedrock Knowledge Bases |

## 引っかかりやすい点 {#traps}

- Transcribe と Polly は向きが逆です。
- Fraud Detector、Forecast、Kendra、Q Business、Augmented AI は新規顧客を受け付けていません。新規の設計では代替を選びます。
- Comprehend はスキャンを読めません。先に Textract で文字にします。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [managed-ai 問1](../../exercises/managed-ai.md#q1) | 1.2.5 | コールセンターの通話の録音を文字にしたいと考えています。適切なサービスはどれですか。 |
| [managed-ai 問2](../../exercises/managed-ai.md#q2) | 1.2.5 | ニュース記事を自然な音声で読み上げるアプリを作ります。適切なサービスはどれですか。 |
| [managed-ai 問3](../../exercises/managed-ai.md#q3) | 1.2.5 | 商品レビューが肯定的か否定的かを判定し、レビューに含まれる人名なども取り出したいと考えています。適切… |
| [managed-ai 問4](../../exercises/managed-ai.md#q4) | 1.2.5 | ホテル予約の手続きを進めるチャットボットを作ります。利用者の目的を判定し、日付や人数を聞き返します。… |
| [managed-ai 問5](../../exercises/managed-ai.md#q5) | 1.2.5 | スキャンした請求書から、表の内容と合計金額を取り出したいと考えています。適切なサービスはどれですか。 |
| [managed-ai 問6](../../exercises/managed-ai.md#q6) | 1.2.5 | 自社の表データで独自のモデルを学習し、デプロイから監視まで管理したいと考えています。適切なサービスは… |
| [managed-ai 問7](../../exercises/managed-ai.md#q7) | 1.2.5 | 英語の通話の録音を日本語の文章にして、顧客の感情を分析します。処理の順番として正しいものはどれですか… |
| [managed-ai 問8](../../exercises/managed-ai.md#q8) | 1.2.4 | 投稿された画像から、不適切な内容を自動で検出したいと考えています。この用途の分野と AWS の選択肢… |
| [managed-ai 問9](../../exercises/managed-ai.md#q9) | 1.2.4 | 動画配信サービスが、視聴履歴に基づいて利用者ごとのおすすめを表示したいと考えています。適切なサービス… |
| [managed-ai 問10](../../exercises/managed-ai.md#q10) | 1.2.4 | 社内規定への質問に、文書に基づいて答えるアシスタントを新しく作ります。現在の AWS の選択肢として… |
| [managed-ai 問11](../../exercises/managed-ai.md#q11) | 1.2.4 | 実世界の AI の活用例と分野の組み合わせとして正しいものを選んでください。（2つ選択） |
| [managed-ai 問12](../../exercises/managed-ai.md#q12) | 1.2.4 | 新規に不正検知のモデルを作りたいと考えています。現在の AWS の選択肢として適切なものはどれですか… |

<!-- questions:end -->

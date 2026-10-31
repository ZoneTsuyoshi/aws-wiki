# 分野3: AI/ML と分析

目的のタスクからサービスを選びます。名前と役割の対応を覚えます。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [AI/ML のサービス](../../domain3.md#t3-7-ai-ml) | タスクからの選択 |
| [分析のサービス](../../domain3.md#t3-7-analytics) | 要件からの選択 |

## 学習の順番 {#study-order}

1. [開発環境](../../../../services/sagemaker.md#studio)と[Amazon Lex](../../../../services/ai-managed-services.md#lex): モデルを作るか、ボットを作るかを確認します。
2. [Amazon Polly](../../../../services/ai-managed-services.md#polly)と[Amazon Transcribe](../../../../services/ai-managed-services.md#transcribe): 向きが逆であることを覚えます。
3. [Amazon Comprehend](../../../../services/ai-managed-services.md#comprehend)と[Amazon Textract](../../../../services/ai-managed-services.md#textract): 意味の分析か、文書からの抽出かで区別します。
4. [Amazon Rekognition](../../../../services/ai-managed-services.md#rekognition)と[Amazon Translate](../../../../services/ai-managed-services.md#translate): 用途を確認します。
5. [Amazon Athena](../../../../services/streaming.md#athena)、[Kinesis Data Streams](../../../../services/streaming.md#kinesis-data-streams)、[AWS Glue](../../../../services/data-engineering.md#glue)、[Amazon Quick Sight](../../../../services/data-engineering.md#quick-sight): 分析の要件と対応させます。
6. [Amazon Redshift](../../../../services/data-engineering.md#redshift)、[Amazon EMR](../../../../services/data-engineering.md#emr)、[Amazon OpenSearch Service](../../../../services/streaming.md#opensearch): 残りの役割を確認します。

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 独自のモデルを作ってデプロイする | SageMaker AI |
| チャットボットを作る | Lex |
| 文字を音声にする | Polly |
| 音声を文字にする | Transcribe |
| テキストの感情を分析する | Comprehend |
| 文書から文字や表を抽出する | Textract |
| 画像や動画を分析する | Rekognition |
| S3 のデータに SQL で問い合わせる | Athena |
| ストリーミングデータを受ける | Kinesis |
| ETL とカタログ | Glue |
| ダッシュボードと BI | Amazon Quick |

## 引っかかりやすい点 {#traps}

- 古い教材の QuickSight は、現在 Amazon Quick の Quick Sight の機能です。
- Amazon Q は製品ごとに状況が変わっています。Q Business は新規顧客を受け付けていません。
- Comprehend はテキストの意味、Textract は文書からの抽出です。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [ai-analytics 問1](../../exercises/ai-analytics.md#q1) | AI/ML のサービス | データサイエンティストが、独自のモデルを作り、学習してデプロイしたいと考えています。最も適切なサービ… |
| [ai-analytics 問2](../../exercises/ai-analytics.md#q2) | AI/ML のサービス | Web サイトの問い合わせに答えるチャットボットを作りたいと考えています。最も適切なサービスはどれで… |
| [ai-analytics 問3](../../exercises/ai-analytics.md#q3) | AI/ML のサービス | ニュース記事の文章を読み上げる音声を作りたいと考えています。最も適切なサービスはどれですか。 |
| [ai-analytics 問4](../../exercises/ai-analytics.md#q4) | AI/ML のサービス | コールセンターの通話の録音を文字にしたいと考えています。最も適切なサービスはどれですか。 |
| [ai-analytics 問5](../../exercises/ai-analytics.md#q5) | AI/ML のサービス | 目的とサービスの組み合わせとして正しいものはどれですか。（2つ選択） |
| [ai-analytics 問6](../../exercises/ai-analytics.md#q6) | AI/ML のサービス | 投稿された画像に不適切な内容がないかを判定したいと考えています。最も適切なサービスはどれですか。 |
| [ai-analytics 問7](../../exercises/ai-analytics.md#q7) | AI/ML のサービス | Web サイトの商品説明を日本語から複数の言語に自動で変換したいと考えています。最も適切なサービスは… |
| [ai-analytics 問8](../../exercises/ai-analytics.md#q8) | 分析のサービス | S3 に置いたログに、サーバーを用意せずに SQL で問い合わせたいと考えています。最も適切なサービ… |
| [ai-analytics 問9](../../exercises/ai-analytics.md#q9) | 分析のサービス | クリックのデータをリアルタイムに受け取って処理したいと考えています。最も適切なサービスはどれですか。 |
| [ai-analytics 問10](../../exercises/ai-analytics.md#q10) | 分析のサービス | 複数のデータソースからデータを変換して読み込み（ETL）、データのカタログも管理したいと考えています… |
| [ai-analytics 問11](../../exercises/ai-analytics.md#q11) | 分析のサービス | 経営層向けに、売上のダッシュボードを作って共有したいと考えています。最も適切なサービスはどれですか。 |
| [ai-analytics 問12](../../exercises/ai-analytics.md#q12) | 分析のサービス | 要件とサービスの組み合わせとして正しいものはどれですか。（2つ選択） |

<!-- questions:end -->

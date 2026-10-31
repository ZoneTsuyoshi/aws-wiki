# 分野1: AI サービスと多様なデータ

文書、音声、動画、画像の原本を S3 に置き、用途に合わせてテキストや埋め込みに変換します。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [1.1.8](../../domain1.md#skill-1-1-8) | 多様なデータ型の取り込みと保存 |

## 学習の順番 {#study-order}

1. [マネージド AI サービスの選び方](../../../../services/ai-managed-services.md#choosing): データの種類ごとのサービスを覚えます。
2. [Bedrock Data Automation](../../../../services/genai-apps.md#bda): 図や表を含む文書の処理を確認します。
3. [Nova と Titan](../../../../services/genai-apps.md#nova-titan): マルチモーダルの埋め込みモデルを押さえます。
4. [DataSync](../../../../services/migration.md#datasync): ファイルサーバーからの移行を確認します。

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 音声を文字にする | Transcribe |
| スキャン文書から文字や項目を取り出す | Textract、Bedrock Data Automation |
| カメラの映像を取り込む | Kinesis Video Streams |
| 画像も意味検索する | マルチモーダルの埋め込みモデル |
| ファイルサーバーから S3 へ大量に移す | DataSync |

## 引っかかりやすい点 {#traps}

- Titan Text Embeddings V2 はテキスト専用です。画像を扱うならマルチモーダルのモデルを選びます。
- Polly は文字を音声にするサービスで、Transcribe と逆です。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [ai-services 問1](../../exercises/ai-services.md#q1) | 1.1.8 | コールセンターの通話の録音を、検索できるテキストにして S3 に保存します。どのサービスを使いますか… |
| [ai-services 問2](../../exercises/ai-services.md#q2) | 1.1.8 | オンプレミスのファイルサーバーから、スキャン文書を大量に S3 へ移します。移行の転送に使うサービス… |
| [ai-services 問3](../../exercises/ai-services.md#q3) | 1.1.8 | 図と表を含む文書と画像を、1 つのベクトルストアで意味検索します。埋め込みモデルの選択として適切なも… |

<!-- questions:end -->

# 問題集

話題ごとの本番形式の問題です。**MLA-C02** の範囲に沿って書いています。すべてオリジナルの問題で、実際の試験問題ではありません。答えは問題の下を開くと確認でき、選択肢ごとの解説と解説ページへのリンクがあります。

!!! warning "日本語で受ける人は、当面 MLA-C01 です（2026年10月31日時点）"
    日本語の試験は、MLA-C02 の一般提供（[AWS のブログ](https://aws.amazon.com/blogs/training-and-certification/september-2026-new-offerings/)によれば 2027年1月14日）までは **MLA-C01** です。この問題集は C02 を基準にしているので、C01 には出ない内容も含みます。

    - 問題に付いたスキルが[対応表](../coverage.md)で「追加」なら、C02 で追加された内容です。C01 で受ける人は、印のないスキルの問題を優先します。
    - C02 で削除された内容（独自コンテナ、Neo、モデルサイズの削減など）は、この問題集では十分に扱っていません。[C01 で受ける場合](../index.md#c01)の表で補います。
    - C01 の試験ガイドの本文は、このコースでは確認できていません。予約の前に[公式ページ](https://aws.amazon.com/certification/certified-machine-learning-engineer-associate/)を確認してください。

1. まず[分野のページ](../index.md#study-path)で範囲を確認します。
2. サービスの解説を読み、問題を解きます。
3. 間違えた問題は、解説のリンク先に戻って確認します。

分野とサービスの組み合わせで学ぶなら、[分野1](../study/domain1/index.md)、[分野2](../study/domain2/index.md)、[分野3](../study/domain3/index.md)、[分野4](../study/domain4/index.md)の学習ページから進めます。

提供状況が変わったサービス（Ground Truth、Clarify、Model Monitor、Debugger、Augmented AI、DevOps Guru、CodeGuru Security、Bedrock Agents）の問題は、役割の理解か、公式の移行先を問う形にしています。

## 分野1: ML と AI のためのデータ準備 {#domain1}

| 問題集 | 主な内容 |
|---|---|
| [データの収集と保存](data-ingestion.md) | 抽出、ストレージの選択、形式、結合、取り込みの問題の解決 |
| [ストリーミング](streaming.md) | Kinesis、Firehose、Flink、MSK、ストリームの変換 |
| [データ変換と特徴量](data-prep.md) | Data Wrangler、DataBrew、Feature Store、特徴量エンジニアリング、クリーニング |
| [データ品質とバイアス](data-quality.md) | Glue Data Quality、ラベル付け、CI と DPL、不均衡 |
| [ベクトルストアと埋め込み](vector-embeddings.md) | ストアの選択、次元、テキストの前処理、検索の最適化 |
| [機密データと安全策](guardrails.md) | Macie、Detect PII、Guardrails、学習データの検査、インジェクション対策 |

## 分野2: ML モデルと FM の開発 {#domain2}

| 問題集 | 主な内容 |
|---|---|
| [モデルの選択と基本の調整](ml-modeling.md) | 組み込みアルゴリズム、過学習、アンサンブル、ハイパーパラメータ |
| [SageMaker AI の学習](sagemaker-training.md) | スクリプトモード、AMT、スポット、分散学習、収束、ジョブの設定 |
| [モデルと AI の評価](evaluation.md) | MLflow、SHAP、指標の計算、NLP の指標、人の評価、LLM の採点 |
| [モデルの監視とテスト](model-monitoring.md) | ドリフト、シャドウテスト、データキャプチャ、A/B テスト |
| [AI サービス](ai-services.md) | Textract、Comprehend、Rekognition、Transcribe、FM との使い分け |
| [Bedrock の FM の選択とデプロイ](bedrock-fm.md) | 選定の観点、ライフサイクル、オンデマンド、Provisioned Throughput |
| [FM のカスタマイズ](fm-customization.md) | 学習データ、ファインチューニング、蒸留、LoRA、自動化 |
| [プロンプトと AI のテスト](prompts.md) | フューショット、Prompt Management、ゴールデンデータセット |

## 分野3: デプロイとオーケストレーション {#domain3}

| 問題集 | 主な内容 |
|---|---|
| [SageMaker AI の推論](sagemaker-inference.md) | 推論の方式、マルチモデル、API、自動スケーリング、インスタンスの選択 |
| [Knowledge Bases と RAG](knowledge-bases.md) | 文書の準備、RAG のパターン、検索の設定、同期、評価 |
| [エージェント](agents.md) | AgentCore、状態管理、バージョン管理、監視 |
| [MLOps](mlops.md) | デプロイガードレール、Pipelines、再学習、Model Registry |
| [CI/CD、コンテナ、IaC](cicd-iac.md) | スタック間の連携、ECR、Code シリーズ、脆弱性の検査 |

## 分野4: 運用、監視、保護 {#domain4}

| 問題集 | 主な内容 |
|---|---|
| [監視と調査](observability.md) | 遅延の切り分け、Bedrock の指標、X-Ray、CloudTrail、ダッシュボード |
| [コストと容量](cost-capacity.md) | Budgets、購入オプション、トークンの計算、キャッシュ |
| [セキュリティ](security.md) | VPC、最小権限、`iam:PassRole`、監査、API キー |

問題集は話題でまとめているので、1 つのファイルに複数の分野のスキルが入ることがあります。ここでは主な分野の表に載せています。

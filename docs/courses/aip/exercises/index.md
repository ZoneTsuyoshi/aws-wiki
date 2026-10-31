# 問題集

話題ごとの本番形式の問題です。基準は **AIP-C01** です。すべてオリジナルの問題で、実際の試験問題ではありません。答えは問題の下を開くと確認でき、選択肢ごとの解説と解説ページへのリンクがあります。

1. まず[分野のページ](../index.md#study-path)で範囲を確認します。
2. サービスの解説を読み、問題を解きます。
3. 間違えた問題は、解説のリンク先に戻って確認します。

複数の分野にまたがる話題は、中心となる分野に載せています。分野ごとの問題の一覧は、各分野のサービス別の学習ページにあります。

## 分野1: FM の統合、データ管理、コンプライアンス {#domain1}

| 問題集 | 主な内容 |
|---|---|
| [FM の選定と耐障害](fm-selection.md) | 要件の分析、PoC、標準化、モデルの切り替え、障害の備え |
| [データの検証と前処理](data-preparation.md) | Glue Data Quality、Textract、Transcribe、入力の形式 |
| [カスタムモデルとモデルのホスト](custom-models.md) | LoRA、Model Registry、Custom Model Import、スケーリング |
| [ベクトルストア](vector-stores.md) | ストアの選択、メタデータ、シャード、検索の調整と運用 |
| [Knowledge Bases と検索](knowledge-bases.md) | コネクタ、同期、チャンク、埋め込み、検索の改善 |
| [プロンプトと Flows](prompts.md) | テンプレート、対話の文脈、ガバナンス、品質保証、Flows |

## 分野2: 実装と統合 {#domain2}

| 問題集 | 主な内容 |
|---|---|
| [AgentCore とエージェント](agents.md) | Runtime、Memory、Policy、ツール連携、MCP、エージェントの評価 |
| [ワークフローとオーケストレーション](workflows.md) | ReAct、複数のモデルの協調、人の承認、実装の選択 |
| [企業システムとの統合](enterprise-integration.md) | 疎結合、Webhook、データの所在、UI、開発ツール |
| [GenAI ゲートウェイと CI/CD](genai-gateway.md) | 入口の集約、モデルの振り分け、品質ゲート、デプロイの検証 |
| [Bedrock の API 統合](bedrock-api.md) | 呼び方の選択、ストリーミング、再試行、エラーの切り分け |

## 分野3: AI の安全性、セキュリティ、ガバナンス {#domain3}

| 問題集 | 主な内容 |
|---|---|
| [Guardrails と入出力の安全対策](guardrails.md) | 層の選択、グラウンディング、多層防御、敵対的な入力、プライバシー |
| [アクセス制御とデータの保護](access-and-data-protection.md) | IAM、PrivateLink、Macie、ログの保護、組織の統制 |
| [ガバナンスと責任ある AI](governance.md) | Model Cards、データの追跡、継続的な監視、透明性、公平性 |

## 分野4: 運用効率と最適化 {#domain4}

| 問題集 | 主な内容 |
|---|---|
| [コストの最適化とキャッシュ](cost-optimization.md) | トークン、層の選択、容量、キャッシュ |
| [性能とパラメータの調整](performance.md) | 遅延の指標、流量の制御、推論パラメータ |
| [監視とオブザーバビリティ](observability.md) | 指標、ログ、異常検知、障害の調査、報告 |

## 分野5: テスト、検証、トラブルシューティング {#domain5}

| 問題集 | 主な内容 |
|---|---|
| [評価と Bedrock Evaluations](evaluations.md) | 指標、評価の方式、利用者の評価、取得のテスト |

トラブルシューティングの問題は、[Bedrock の API 統合](bedrock-api.md)、[プロンプトと Flows](prompts.md)、[ベクトルストア](vector-stores.md)にあります。

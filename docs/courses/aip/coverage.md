# スキル対応表

公式試験ガイドの全スキルと、このwikiのページの対応です。スキル名は日本語で要約しています。正確な文言は[試験ガイド](https://docs.aws.amazon.com/aws-certification/latest/ai-professional-01/ai-professional-01.html)で確認してください。

## AIP-C01（20タスク、98スキル） {#aip-c01}

各スキルは分野ページに見出しがあり、そこから詳しい解説へ進めます。

### 分野1: FM の統合、データ管理、コンプライアンス {#coverage-domain1}

| タスク | スキル | 内容 |
|---|---|---|
| [1.1 要件の分析と設計](domain1.md#task-1-1) | [1.1.1](domain1.md#skill-1-1-1) | 業務要件と技術的制約に合う設計 |
| | [1.1.2](domain1.md#skill-1-1-2) | PoC で実現性と価値を検証 |
| | [1.1.3](domain1.md#skill-1-1-3) | 標準化された部品 |
| [1.2 FM の選定と設定](domain1.md#task-1-2) | [1.2.1](domain1.md#skill-1-2-1) | FM の評価と選定 |
| | [1.2.2](domain1.md#skill-1-2-2) | コードを変えずにモデルを切り替える |
| | [1.2.3](domain1.md#skill-1-2-3) | 障害時も動き続ける設計 |
| | [1.2.4](domain1.md#skill-1-2-4) | カスタマイズしたモデルのデプロイとライフサイクル |
| [1.3 データの検証と処理](domain1.md#task-1-3) | [1.3.1](domain1.md#skill-1-3-1) | データ検証のワークフロー |
| | [1.3.2](domain1.md#skill-1-3-2) | 複雑なデータ型の処理 |
| | [1.3.3](domain1.md#skill-1-3-3) | モデルが要求する形式に整える |
| | [1.3.4](domain1.md#skill-1-3-4) | 入力の質を高める |
| [1.4 ベクトルストア](domain1.md#task-1-4) | [1.4.1](domain1.md#skill-1-4-1) | ベクトル DB の構成 |
| | [1.4.2](domain1.md#skill-1-4-2) | メタデータの枠組み |
| | [1.4.3](domain1.md#skill-1-4-3) | 大規模で高速なベクトル DB |
| | [1.4.4](domain1.md#skill-1-4-4) | データソースとの統合 |
| | [1.4.5](domain1.md#skill-1-4-5) | ベクトルストアの鮮度を保つ |
| [1.5 検索の仕組み](domain1.md#task-1-5) | [1.5.1](domain1.md#skill-1-5-1) | 文書の分割 |
| | [1.5.2](domain1.md#skill-1-5-2) | 埋め込みの選択と設定 |
| | [1.5.3](domain1.md#skill-1-5-3) | ベクトル検索のデプロイと設定 |
| | [1.5.4](domain1.md#skill-1-5-4) | 関連性を高める検索の構成 |
| | [1.5.5](domain1.md#skill-1-5-5) | 問い合わせの処理 |
| | [1.5.6](domain1.md#skill-1-5-6) | 一貫したアクセスの仕組み |
| [1.6 プロンプト](domain1.md#task-1-6) | [1.6.1](domain1.md#skill-1-6-1) | モデルへの指示の枠組み |
| | [1.6.2](domain1.md#skill-1-6-2) | 文脈を保つ対話システム |
| | [1.6.3](domain1.md#skill-1-6-3) | プロンプトの管理とガバナンス |
| | [1.6.4](domain1.md#skill-1-6-4) | プロンプトの品質保証 |
| | [1.6.5](domain1.md#skill-1-6-5) | プロンプトの反復的な改善 |
| | [1.6.6](domain1.md#skill-1-6-6) | 複雑なプロンプトシステム |

### 分野2: 実装と統合 {#coverage-domain2}

| タスク | スキル | 内容 |
|---|---|---|
| [2.1 エージェントとツール](domain2.md#task-2-1) | [2.1.1](domain2.md#skill-2-1-1) | 記憶と状態を持つ自律システム |
| | [2.1.2](domain2.md#skill-2-1-2) | 構造化された推論で問題を解く |
| | [2.1.3](domain2.md#skill-2-1-3) | 安全に制御されたワークフロー |
| | [2.1.4](domain2.md#skill-2-1-4) | 複数のモデルの協調 |
| | [2.1.5](domain2.md#skill-2-1-5) | 人の専門知識を組み込む |
| | [2.1.6](domain2.md#skill-2-1-6) | 信頼できるツール連携 |
| | [2.1.7](domain2.md#skill-2-1-7) | モデルの拡張の枠組み |
| [2.2 デプロイ戦略](domain2.md#task-2-2) | [2.2.1](domain2.md#skill-2-2-1) | 要件に応じた FM のデプロイ |
| | [2.2.2](domain2.md#skill-2-2-2) | LLM に特有のデプロイの課題 |
| | [2.2.3](domain2.md#skill-2-2-3) | 性能と資源の均衡 |
| [2.3 企業向けの統合](domain2.md#task-2-3) | [2.3.1](domain2.md#skill-2-3-1) | 既存の企業環境との接続 |
| | [2.3.2](domain2.md#skill-2-3-2) | 既存のアプリに生成 AI を組み込む |
| | [2.3.3](domain2.md#skill-2-3-3) | 安全なアクセスの枠組み |
| | [2.3.4](domain2.md#skill-2-3-4) | 法域をまたぐデータの準拠 |
| | [2.3.5](domain2.md#skill-2-3-5) | CI/CD と GenAI ゲートウェイ |
| [2.4 FM の API](domain2.md#task-2-4) | [2.4.1](domain2.md#skill-2-4-1) | 柔軟なモデル呼び出し |
| | [2.4.2](domain2.md#skill-2-4-2) | リアルタイムの応答 |
| | [2.4.3](domain2.md#skill-2-4-3) | 信頼性の高い FM システム |
| | [2.4.4](domain2.md#skill-2-4-4) | モデルの振り分け |
| [2.5 アプリと開発ツール](domain2.md#task-2-5) | [2.5.1](domain2.md#skill-2-5-1) | 生成 AI 向けの API |
| | [2.5.2](domain2.md#skill-2-5-2) | 利用しやすい AI のインターフェイス |
| | [2.5.3](domain2.md#skill-2-5-3) | 業務システムの強化 |
| | [2.5.4](domain2.md#skill-2-5-4) | 開発者の生産性を高める |
| | [2.5.5](domain2.md#skill-2-5-5) | 高度な生成 AI アプリ |
| | [2.5.6](domain2.md#skill-2-5-6) | トラブルシューティングの効率化 |

### 分野3: AI の安全性、セキュリティ、ガバナンス {#coverage-domain3}

| タスク | スキル | 内容 |
|---|---|---|
| [3.1 入出力の安全対策](domain3.md#task-3-1) | [3.1.1](domain3.md#skill-3-1-1) | 有害な入力への対策 |
| | [3.1.2](domain3.md#skill-3-1-2) | 有害な出力への対策 |
| | [3.1.3](domain3.md#skill-3-1-3) | ハルシネーションを減らす |
| | [3.1.4](domain3.md#skill-3-1-4) | 多層防御 |
| | [3.1.5](domain3.md#skill-3-1-5) | 敵対的な入力の検出 |
| [3.2 データの保護](domain3.md#task-3-2) | [3.2.1](domain3.md#skill-3-2-1) | 保護された AI 環境 |
| | [3.2.2](domain3.md#skill-3-2-2) | 機密情報を守る仕組み |
| | [3.2.3](domain3.md#skill-3-2-3) | 有用性を保ちつつプライバシーを守る |
| [3.3 ガバナンス](domain3.md#task-3-3) | [3.3.1](domain3.md#skill-3-3-1) | 規制に対応する枠組み |
| | [3.3.2](domain3.md#skill-3-3-2) | データソースの追跡 |
| | [3.3.3](domain3.md#skill-3-3-3) | 組織のガバナンス |
| | [3.3.4](domain3.md#skill-3-3-4) | 継続的な監視と高度な統制 |
| [3.4 責任ある AI](domain3.md#task-3-4) | [3.4.1](domain3.md#skill-3-4-1) | 透明性 |
| | [3.4.2](domain3.md#skill-3-4-2) | 公平性の評価 |
| | [3.4.3](domain3.md#skill-3-4-3) | ポリシーに準拠したシステム |

### 分野4: 運用効率と最適化 {#coverage-domain4}

| タスク | スキル | 内容 |
|---|---|---|
| [4.1 コストと資源](domain4.md#task-4-1) | [4.1.1](domain4.md#skill-4-1-1) | トークンの効率化 |
| | [4.1.2](domain4.md#skill-4-1-2) | 費用対効果の高いモデル選択 |
| | [4.1.3](domain4.md#skill-4-1-3) | 高い処理能力と資源の活用 |
| | [4.1.4](domain4.md#skill-4-1-4) | 賢いキャッシュ |
| [4.2 性能](domain4.md#task-4-2) | [4.2.1](domain4.md#skill-4-2-1) | 応答性の高い AI システム |
| | [4.2.2](domain4.md#skill-4-2-2) | 検索の性能を高める |
| | [4.2.3](domain4.md#skill-4-2-3) | FM のスループットの最適化 |
| | [4.2.4](domain4.md#skill-4-2-4) | 用途に合わせた FM の調整 |
| | [4.2.5](domain4.md#skill-4-2-5) | FM に合わせた資源の割り当て |
| | [4.2.6](domain4.md#skill-4-2-6) | ワークフロー全体の性能 |
| [4.3 監視](domain4.md#task-4-3) | [4.3.1](domain4.md#skill-4-3-1) | 全体を見渡す観測 |
| | [4.3.2](domain4.md#skill-4-3-2) | 生成 AI に特有の監視 |
| | [4.3.3](domain4.md#skill-4-3-3) | 実行につながる統合的な観測 |
| | [4.3.4](domain4.md#skill-4-3-4) | ツールの性能の枠組み |
| | [4.3.5](domain4.md#skill-4-3-5) | ベクトルストアの運用管理 |
| | [4.3.6](domain4.md#skill-4-3-6) | 生成 AI に特有の障害の調査 |

### 分野5: テスト、検証、トラブルシューティング {#coverage-domain5}

| タスク | スキル | 内容 |
|---|---|---|
| [5.1 評価](domain5.md#task-5-1) | [5.1.1](domain5.md#skill-5-1-1) | FM の出力の評価の枠組み |
| | [5.1.2](domain5.md#skill-5-1-2) | 最適な構成を見つけるモデル評価 |
| | [5.1.3](domain5.md#skill-5-1-3) | 利用者を中心にした評価 |
| | [5.1.4](domain5.md#skill-5-1-4) | 品質保証のプロセス |
| | [5.1.5](domain5.md#skill-5-1-5) | 多面的な評価 |
| | [5.1.6](domain5.md#skill-5-1-6) | 取得の品質のテスト |
| | [5.1.7](domain5.md#skill-5-1-7) | エージェントの性能の枠組み |
| | [5.1.8](domain5.md#skill-5-1-8) | 関係者への報告 |
| | [5.1.9](domain5.md#skill-5-1-9) | デプロイの検証 |
| [5.2 トラブルシューティング](domain5.md#task-5-2) | [5.2.1](domain5.md#skill-5-2-1) | 内容の処理の問題 |
| | [5.2.2](domain5.md#skill-5-2-2) | FM の統合の問題 |
| | [5.2.3](domain5.md#skill-5-2-3) | プロンプトの問題 |
| | [5.2.4](domain5.md#skill-5-2-4) | 検索システムの問題 |
| | [5.2.5](domain5.md#skill-5-2-5) | プロンプトの保守の問題 |

# スキル対応表

公式試験ガイドの全スキルと、このwikiのページの対応です。スキル名は日本語で要約しています。正確な文言は[試験ガイド](https://docs.aws.amazon.com/aws-certification/latest/sysops-administrator-associate-03/sysops-administrator-associate-03.html)で確認してください。

## SOA-C03（13タスク、53スキル） {#c03}

各スキルは分野ページに見出しがあり、そこから詳しい解説へ進めます。

### 分野1: 監視、ログ、分析、修復、性能の最適化（22%） {#domain1}

| タスク | スキル | 内容 |
|---|---|---|
| [1.1 メトリクス、アラーム、フィルター](domain1.md#task-1-1) | [1.1.1](domain1.md#skill-1-1-1) | ワークロードの監視とログの設定 |
| | [1.1.2](domain1.md#skill-1-1-2) | CloudWatch エージェントの設定と管理 |
| | [1.1.3](domain1.md#skill-1-1-3) | アラームの設定、特定、トラブルシューティング |
| | [1.1.4](domain1.md#skill-1-1-4) | 複数アカウント、複数リージョンのダッシュボード |
| | [1.1.5](domain1.md#skill-1-1-5) | SNS への通知 |
| [1.2 問題の特定と修復](domain1.md#task-1-2) | [1.2.1](domain1.md#skill-1-2-1) | 性能の分析と修復の自動化 |
| | [1.2.2](domain1.md#skill-1-2-2) | EventBridge のルーティングとルールの調査 |
| | [1.2.3](domain1.md#skill-1-2-3) | Automation ランブックの作成と実行 |
| [1.3 性能の最適化](domain1.md#task-1-3) | [1.3.1](domain1.md#skill-1-3-1) | コンピューティングの最適化 |
| | [1.3.2](domain1.md#skill-1-3-2) | EBS の性能とボリュームタイプ |
| | [1.3.3](domain1.md#skill-1-3-3) | S3 の性能戦略 |
| | [1.3.4](domain1.md#skill-1-3-4) | 共有ストレージの選択と最適化 |
| | [1.3.5](domain1.md#skill-1-3-5) | RDS の監視と性能の改善 |
| | [1.3.6](domain1.md#skill-1-3-6) | EC2 とストレージ、ネットワークの最適化 |

### 分野2: 信頼性と事業継続性（22%） {#domain2}

| タスク | スキル | 内容 |
|---|---|---|
| [2.1 スケーラビリティと伸縮性](domain2.md#task-2-1) | [2.1.1](domain2.md#skill-2-1-1) | コンピューティングのスケーリング |
| | [2.1.2](domain2.md#skill-2-1-2) | キャッシュの実装 |
| | [2.1.3](domain2.md#skill-2-1-3) | マネージドデータベースのスケーリング |
| [2.2 高可用性と回復力](domain2.md#task-2-2) | [2.2.1](domain2.md#skill-2-2-1) | ELB と Route 53 のヘルスチェック |
| | [2.2.2](domain2.md#skill-2-2-2) | 耐障害性のある構成 |
| [2.3 バックアップと復元](domain2.md#task-2-3) | [2.3.1](domain2.md#skill-2-3-1) | スナップショットとバックアップの自動化 |
| | [2.3.2](domain2.md#skill-2-3-2) | データベースの復元方法 |
| | [2.3.3](domain2.md#skill-2-3-3) | ストレージのバージョニング |
| | [2.3.4](domain2.md#skill-2-3-4) | 災害復旧の手順 |

### 分野3: デプロイ、プロビジョニング、自動化（22%） {#domain3}

| タスク | スキル | 内容 |
|---|---|---|
| [3.1 プロビジョニングと保守](domain3.md#task-3-1) | [3.1.1](domain3.md#skill-3-1-1) | AMI とコンテナイメージ |
| | [3.1.2](domain3.md#skill-3-1-2) | CloudFormation と CDK |
| | [3.1.3](domain3.md#skill-3-1-3) | デプロイの問題の特定と修復 |
| | [3.1.4](domain3.md#skill-3-1-4) | 複数リージョンと複数アカウントへの展開 |
| | [3.1.5](domain3.md#skill-3-1-5) | デプロイ戦略とサービス |
| | [3.1.6](domain3.md#skill-3-1-6) | Terraform と Git |
| [3.2 既存リソースの自動化](domain3.md#task-3-2) | [3.2.1](domain3.md#skill-3-2-1) | Systems Manager による自動化 |
| | [3.2.2](domain3.md#skill-3-2-2) | イベント駆動の自動化 |

### 分野4: セキュリティとコンプライアンス（16%） {#domain4}

| タスク | スキル | 内容 |
|---|---|---|
| [4.1 ツールとポリシー](domain4.md#task-4-1) | [4.1.1](domain4.md#skill-4-1-1) | IAM の機能 |
| | [4.1.2](domain4.md#skill-4-1-2) | アクセスの問題の調査と監査 |
| | [4.1.3](domain4.md#skill-4-1-3) | マルチアカウントの戦略 |
| | [4.1.4](domain4.md#skill-4-1-4) | Trusted Advisor のセキュリティチェックと修復 |
| | [4.1.5](domain4.md#skill-4-1-5) | コンプライアンスと継続的な監視 |
| [4.2 データとインフラの保護](domain4.md#task-4-2) | [4.2.1](domain4.md#skill-4-2-1) | データ分類 |
| | [4.2.2](domain4.md#skill-4-2-2) | 保存時の暗号化 |
| | [4.2.3](domain4.md#skill-4-2-3) | 転送時の暗号化 |
| | [4.2.4](domain4.md#skill-4-2-4) | シークレットの保存 |
| | [4.2.5](domain4.md#skill-4-2-5) | 検出結果のレポートと修復 |

### 分野5: ネットワークとコンテンツ配信（18%） {#domain5}

| タスク | スキル | 内容 |
|---|---|---|
| [5.1 ネットワークと接続](domain5.md#task-5-1) | [5.1.1](domain5.md#skill-5-1-1) | VPC の設定 |
| | [5.1.2](domain5.md#skill-5-1-2) | プライベート接続 |
| | [5.1.3](domain5.md#skill-5-1-3) | ネットワーク保護サービスの監査 |
| | [5.1.4](domain5.md#skill-5-1-4) | ネットワークのコスト最適化 |
| [5.2 ドメイン、DNS、配信](domain5.md#task-5-2) | [5.2.1](domain5.md#skill-5-2-1) | DNS の設定 |
| | [5.2.2](domain5.md#skill-5-2-2) | Route 53 のルーティングとクエリログ |
| | [5.2.3](domain5.md#skill-5-2-3) | CloudFront と Global Accelerator |
| [5.3 接続の問題の調査](domain5.md#task-5-3) | [5.3.1](domain5.md#skill-5-3-1) | VPC の設定の調査 |
| | [5.3.2](domain5.md#skill-5-3-2) | ネットワークログの収集と解釈 |
| | [5.3.3](domain5.md#skill-5-3-3) | CloudFront のキャッシュの問題 |
| | [5.3.4](domain5.md#skill-5-3-4) | ハイブリッド接続とプライベート接続の問題 |
| | [5.3.5](domain5.md#skill-5-3-5) | CloudWatch のネットワーク監視サービス |

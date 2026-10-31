# 問題集

話題ごとの本番形式の問題です。**SAP-C03** の試験ガイドを基準にしています。すべてオリジナルの問題で、実際の試験問題ではありません。答えは問題の下を開くと確認でき、選択肢ごとの解説と解説ページへのリンクがあります。

1. まず[分野のページ](../index.md#study-path)で範囲を確認します。
2. サービスの解説を読み、問題を解きます。
3. 間違えた問題は、解説のリンク先に戻って確認します。

## 分野1: クラウド向けのアーキテクチャの設計と実装 {#domain1}

| 問題集 | 主な内容 |
|---|---|
| [イベント駆動とワークフロー](events-workflows.md) | 冪等性と順序、状態の外部化、サーバーレスのデータ処理、永続的なワークフロー、アカウントをまたぐ転送 |
| [コンテナとスケーリング](containers.md) | ECS と EKS、Service Connect と VPC Lattice、ECR、スケーリング、入口のパターン |
| [エッジ、リアルタイム、マルチテナント](edge-tenancy.md) | エッジ関数、WebSocket、テナントの分離 |
| [AI と ML の組み込み](ai-ml.md) | Bedrock のマルチアカウント統制、AgentCore、推論の方式、RAG |
| [ハイブリッドの統合](hybrid.md) | Direct Connect の回復性、データ同期、レガシー統合、DNS、Outposts と Anywhere |
| [ネットワークアーキテクチャ](network.md) | VPC の接続方式、IPAM、検査の配置、IPv6、グローバルなルーティング |
| [データレイクと分析](data-analytics.md) | Lake Formation、Iceberg、MSK、EMR、Redshift、データの共有 |
| [データベースとストレージ](databases-storage.md) | 目的別データベース、グローバルな構成、FSx の選択、キャッシュ |

## 分野2: セキュリティ、コンプライアンス、ガバナンス {#domain2}

| 問題集 | 主な内容 |
|---|---|
| [ID のセキュリティ](identity.md) | フェデレーション、アプリの認可、最小権限、データ境界、ワークロード ID |
| [暗号化と鍵管理](encryption.md) | KMS のキーとローテーション、証明書、CloudHSM、耐量子暗号 |
| [マルチアカウントのガバナンス](org-governance.md) | Control Tower、ログの一元管理、RAM、SCP と RCP、準拠の監視、パッチ |
| [コンプライアンス](compliance.md) | データ保護、データ主権、監査証跡、レジデンシー、証拠、脅威モデリング |
| [責任ある AI の統制](responsible-ai.md) | Guardrails、エージェントのアクセス制御、人による承認 |

## 分野3: コストを最適化したアーキテクチャの設計 {#domain3}

| 問題集 | 主な内容 |
|---|---|
| [料金モデル](pricing.md) | 購入オプション、Standard と Express、適正化、Bedrock のティアとキャッシュ |
| [データ転送とネットワーク費用](data-transfer.md) | Origin Shield、NAT とエンドポイント、複製の費用、接続の選択 |
| [コストの配分と可視化](cost-allocation.md) | タグの強制、CUR 2.0、分割コスト配分データ、Budgets と異常検出 |
| [ストレージとデータベースの費用](storage-db-cost.md) | S3 の階層化、EBS のタイプ、データベースの課金、バックアップ、ログの費用 |

## 分野4: 回復性、移行、事業継続 {#domain4}

| 問題集 | 主な内容 |
|---|---|
| [移行戦略](migration.md) | 7 つの R、MGN、DMS、転送時間の計算、モダナイズ |
| [DR](dr.md) | DR 戦略の選択、DRS、Resilience Hub、ARC、DR の検証 |
| [回復性と事業継続](resilience.md) | バックアップの統制、RTO の計測、ランサムウェア対策、FIS |

## 分野5: 運用の優秀性と自動化 {#domain5}

| 問題集 | 主な内容 |
|---|---|
| [IaC](iac.md) | 安全な更新、Hooks と Aspects、シークレット、StackSets の同時実行 |
| [CI/CD と DevSecOps](cicd.md) | 成果物の昇格、スキャンと署名、AI の評価、ロールバック |
| [オブザーバビリティ](observability.md) | ADOT、ログの集約、複合アラーム、AI の監視、Synthetics と RUM、SLO |
| [運用の自動化](automation.md) | クォータと Health、レート制御、スケーリング、ヘルスチェック、ランブック |

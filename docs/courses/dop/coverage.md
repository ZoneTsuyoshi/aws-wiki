# 項目対応表

公式試験ガイドの全項目と、このコースの見出しの対応です。項目名は日本語で要約しています。正確な文言は[試験ガイド](https://docs.aws.amazon.com/aws-certification/latest/devops-engineer-professional-02/devops-engineer-professional-02.html)で確認してください。

DOP-C02 のガイドは、スキルに番号を付けていません。タスクごとに「知識」と「スキル」の箇条書きがあるので、ここでは掲載順に K1、S1 のように番号を振りました。この番号は公式のものではありません。

全部で 6 分野、19 タスク、140 項目です。

| 分野 | タスク | 項目数 |
|---|---|---|
| [分野1](#domain1) | 4 | 28 |
| [分野2](#domain2) | 3 | 18 |
| [分野3](#domain3) | 3 | 24 |
| [分野4](#domain4) | 3 | 34 |
| [分野5](#domain5) | 3 | 14 |
| [分野6](#domain6) | 3 | 22 |

## 分野1: SDLC の自動化 {#domain1}

### タスク 1.1: CI/CD パイプライン {#c-1-1}

| 項目 | 内容 | ページ |
|---|---|---|
| K1 | SDLC の概念、フェーズ、モデル | [SDLC の概念とモデル](domain1.md#t1-1-sdlc) |
| K2 | 単一、複数アカウントのパイプラインのパターン | [単一アカウントと複数アカウント](domain1.md#t1-1-multi-account) |
| S1 | コード、イメージ、成果物のリポジトリの設定 | [リポジトリ](domain1.md#t1-1-repositories) |
| S2 | バージョン管理とパイプラインの統合 | [バージョン管理](domain1.md#t1-1-version-control) |
| S3 | ビルドプロセスの設定 | [ビルドプロセス](domain1.md#t1-1-build) |
| S4 | ビルドとデプロイのシークレットの管理 | [シークレット](domain1.md#t1-1-secrets) |
| S5 | デプロイ戦略の判断 | [デプロイ戦略の判断](domain1.md#t1-1-deployment-strategy) |

### タスク 1.2: 自動テスト {#c-1-2}

| 項目 | 内容 | ページ |
|---|---|---|
| K1 | テストの種類 | [テストの種類と配置](domain1.md#t1-2-test-types) |
| K2 | 各段階でのテストの使い分け | [テストの種類と配置](domain1.md#t1-2-test-types) |
| S1 | PR やマージでのビルド、テスト | [PR とマージでのビルド](domain1.md#t1-2-pr-builds) |
| S2 | 負荷テスト、性能のベンチマーク | [負荷テスト](domain1.md#t1-2-load-testing) |
| S3 | 終了コードによる健全性の測定 | [終了コード](domain1.md#t1-2-exit-codes) |
| S4 | 単体テストとコードカバレッジの自動化 | [単体テストとカバレッジ](domain1.md#t1-2-unit-coverage) |
| S5 | パイプラインから AWS サービスを呼ぶ | [AWS サービスの呼び出し](domain1.md#t1-2-invoke-services) |

### タスク 1.3: 成果物 {#c-1-3}

| 項目 | 内容 | ページ |
|---|---|---|
| K1 | 成果物の用途と安全な管理 | [用途と安全な管理](domain1.md#t1-3-security) |
| K2 | 成果物の作成、生成の方法 | [成果物の作り方](domain1.md#t1-3-create) |
| K3 | 成果物のライフサイクル | [ライフサイクル](domain1.md#t1-3-lifecycle) |
| S1 | リポジトリの作成と設定 | [リポジトリの作成と設定](domain1.md#t1-3-repositories) |
| S2 | ビルドツールの設定（CodeBuild、Lambda） | [成果物の作り方](domain1.md#t1-3-create) |
| S3 | AMI とコンテナイメージのビルドの自動化 | [自動ビルド](domain1.md#t1-3-image-builder) |

### タスク 1.4: デプロイ戦略 {#c-1-4}

| 項目 | 内容 | ページ |
|---|---|---|
| K1 | 各プラットフォームのデプロイ方式 | [デプロイ方式](domain1.md#t1-4-methods) |
| K2 | アプリケーションのストレージパターン | [ストレージパターン](domain1.md#t1-4-storage) |
| K3 | ミュータブルとイミュータブル | [ミュータブルとイミュータブル](domain1.md#t1-4-mutable-immutable) |
| K4 | コードを配布するツール | [配布するツール](domain1.md#t1-4-distribution) |
| S1 | リポジトリへのアクセス権限 | [アクセス権限](domain1.md#t1-4-permissions) |
| S2 | デプロイエージェントの設定 | [エージェント](domain1.md#t1-4-agents) |
| S3 | デプロイの問題の解決 | [デプロイの問題の解決](domain1.md#t1-4-troubleshooting) |
| S4 | さまざまなデプロイ方式の使用 | [デプロイ方式](domain1.md#t1-4-methods) |

## 分野2: 構成管理と IaC {#domain2}

### タスク 2.1: インフラと再利用できる部品 {#c-2-1}

| 項目 | 内容 | ページ |
|---|---|---|
| K1 | IaC の選択肢とツール | [IaC の選択肢](domain2.md#t2-1-iac-options) |
| K2 | IaC の変更管理 | [変更管理](domain2.md#t2-1-change-management) |
| K3 | 構成管理のサービスと戦略 | [構成管理](domain2.md#t2-1-config-management) |
| S1 | IaC テンプレートの作成とデプロイ | [IaC の選択肢](domain2.md#t2-1-iac-options) |
| S2 | StackSets の適用 | [StackSets](domain2.md#t2-1-stacksets) |
| S3 | 最適な構成管理サービスの判断 | [構成管理](domain2.md#t2-1-config-management) |
| S4 | 統制を組み込んだ再利用できるテンプレート | [再利用できる部品](domain2.md#t2-1-reusable) |

### タスク 2.2: アカウントの自動化 {#c-2-2}

| 項目 | 内容 | ページ |
|---|---|---|
| K1 | アカウント構成とベストプラクティス | [アカウント構成](domain2.md#t2-2-structure) |
| S1 | アカウント発行の標準化と自動化 | [標準化と自動化](domain2.md#t2-2-provisioning) |
| S2 | アカウントの作成、統合、一元管理 | [Organizations と Control Tower](domain2.md#t2-2-org-ct) |
| S3 | 複数アカウントの IAM | [複数アカウントの IAM](domain2.md#t2-2-iam) |
| S4 | 統制とセキュリティの大規模な実装 | [統制とセキュリティ](domain2.md#t2-2-governance) |

### タスク 2.3: 複雑な作業の自動化 {#c-2-3}

| 項目 | 内容 | ページ |
|---|---|---|
| K1 | 自動化に使うサービス | [自動化に使うサービス](domain2.md#t2-3-automation-services) |
| K2 | AWS を操作する方法と戦略 | [AWS を操作する方法](domain2.md#t2-3-interfaces) |
| S1 | インベントリ、構成、パッチの自動化 | [インベントリとパッチ](domain2.md#t2-3-inventory-patch) |
| S2 | 複雑なシナリオの Lambda の自動化 | [Lambda と Step Functions](domain2.md#t2-3-lambda) |
| S3 | ソフトウェアを望ましい状態に保つ | [望ましい状態](domain2.md#t2-3-desired-state) |
| S4 | ソフトウェアの準拠の維持 | [準拠の維持](domain2.md#t2-3-compliance) |

## 分野3: 回復力のあるクラウドソリューション {#domain3}

### タスク 3.1: 高可用性 {#c-3-1}

| 項目 | 内容 | ページ |
|---|---|---|
| K1 | Multi-AZ と Multi-Region のデプロイ | [Multi-AZ と Multi-Region](domain3.md#t3-1-multi-az-region) |
| K2 | SLA | [SLA](domain3.md#t3-1-sla) |
| K3 | ステートフルなサービスの複製と切り替え | [複製と切り替え](domain3.md#t3-1-replication) |
| K4 | 高可用性を実現する手法 | [Multi-AZ と Multi-Region](domain3.md#t3-1-multi-az-region) |
| S1 | ビジネス要件から技術的な要件へ | [ビジネス要件](domain3.md#t3-1-business-requirements) |
| S2 | 単一障害点の特定と解消 | [単一障害点](domain3.md#t3-1-spof) |
| S3 | リージョンをまたぐ機能の有効化 | [リージョンをまたぐ機能](domain3.md#t3-1-cross-region) |
| S4 | AZ をまたぐ負荷分散の設定 | [負荷分散](domain3.md#t3-1-load-balancing) |
| S5 | ダウンタイムを抑えるアプリの構成 | [ダウンタイムを抑える](domain3.md#t3-1-minimize-downtime) |

### タスク 3.2: スケーラビリティ {#c-3-2}

| 項目 | 内容 | ページ |
|---|---|---|
| K1 | スケーリングに適したメトリクス | [スケーリングの指標](domain3.md#t3-2-metrics) |
| K2 | 疎結合で分散したアーキテクチャ | [疎結合](domain3.md#t3-2-loose-coupling) |
| K3 | サーバーレスアーキテクチャ | [サーバーレス](domain3.md#t3-2-serverless) |
| K4 | コンテナプラットフォーム | [コンテナ](domain3.md#t3-2-containers) |
| S1 | スケーリングの問題の特定と解消 | [スケーリングの問題](domain3.md#t3-2-scaling-issues) |
| S2 | Auto Scaling、負荷分散、キャッシュの実装 | [Auto Scaling とキャッシュ](domain3.md#t3-2-autoscaling-caching) |
| S3 | コンテナアプリケーションのデプロイ | [コンテナ](domain3.md#t3-2-containers) |
| S4 | 複数リージョンへのワークロードの配置 | [グローバルなスケール](domain3.md#t3-2-global) |
| S5 | サーバーレスアプリケーションの設定 | [サーバーレス](domain3.md#t3-2-serverless) |

### タスク 3.3: 自動復旧 {#c-3-3}

| 項目 | 内容 | ページ |
|---|---|---|
| K1 | DR の概念（RTO、RPO） | [RTO と RPO](domain3.md#t3-3-rto-rpo) |
| K2 | AWS Backup と復旧の戦略 | [DR 戦略](domain3.md#t3-3-dr-strategies) |
| K3 | 復旧の手順 | [復旧の手順](domain3.md#t3-3-recovery-procedures) |
| S1 | フェイルオーバーのテスト | [フェイルオーバーのテスト](domain3.md#t3-3-failover-testing) |
| S2 | リージョンをまたぐバックアップと復旧 | [バックアップと復旧](domain3.md#t3-3-backup) |
| S3 | バックエンド障害から復旧するロードバランサー | [ロードバランサー](domain3.md#t3-3-load-balancer) |

## 分野4: 監視とログ {#domain4}

### タスク 4.1: 収集、集約、保存 {#c-4-1}

| 項目 | 内容 | ページ |
|---|---|---|
| K1 | アプリとインフラの監視の方法 | [監視](domain4.md#t4-1-monitoring) |
| K2 | CloudWatch メトリクス | [メトリクスの基本](domain4.md#t4-1-metrics) |
| K3 | リアルタイムのログの取り込み | [リアルタイムの取り込み](domain4.md#t4-1-real-time) |
| K4 | 保存時、転送時の暗号化の選択肢 | [ログの暗号化](domain4.md#t4-1-encryption) |
| K5 | ログ収集のセキュリティの構成 | [ログ収集の権限](domain4.md#t4-1-permissions) |
| S1 | ログの安全な保管と管理 | [安全な保管](domain4.md#t4-1-secure-storage) |
| S2 | メトリクスフィルター | [メトリクスフィルター](domain4.md#t4-1-metric-filters) |
| S3 | メトリクスストリーム | [メトリクスストリーム](domain4.md#t4-1-metric-streams) |
| S4 | カスタムメトリクスの収集 | [カスタムメトリクス](domain4.md#t4-1-custom-metrics) |
| S5 | ログの保存のライフサイクル | [ライフサイクル](domain4.md#t4-1-lifecycle) |
| S6 | サブスクリプションによるログ処理 | [サブスクリプション](domain4.md#t4-1-subscriptions) |
| S7 | フィルターと Logs Insights の検索 | [ログの検索](domain4.md#t4-1-search) |
| S8 | ログデータの暗号化の設定 | [ログの暗号化](domain4.md#t4-1-encryption) |

### タスク 4.2: 監査、監視、分析 {#c-4-2}

| 項目 | 内容 | ページ |
|---|---|---|
| K1 | 異常検知アラーム | [異常検知](domain4.md#t4-2-anomaly) |
| K2 | よく使うメトリクスとログ | [よく使うメトリクス](domain4.md#t4-2-common-metrics) |
| K3 | Inspector と評価テンプレート | [Inspector](domain4.md#t4-2-inspector) |
| K4 | AWS Config ルール | [Config ルール](domain4.md#t4-2-config-rules) |
| K5 | CloudTrail のログイベント | [CloudTrail](domain4.md#t4-2-cloudtrail) |
| S1 | ダッシュボードと Quick Sight | [ダッシュボード](domain4.md#t4-2-dashboards) |
| S2 | アラームとメトリクスの関連付け | [アラーム](domain4.md#t4-2-alarms) |
| S3 | X-Ray の設定 | [X-Ray](domain4.md#t4-2-xray) |
| S4 | リアルタイムのログストリームの分析 | [リアルタイムの分析](domain4.md#t4-2-real-time-analysis) |
| S5 | AWS サービスでのログ分析 | [ログ分析](domain4.md#t4-2-log-analysis) |

### タスク 4.3: 監視とイベント管理の自動化 {#c-4-3}

| 項目 | 内容 | ページ |
|---|---|---|
| K1 | イベント駆動の非同期パターン | [イベントパターン](domain4.md#t4-3-event-patterns) |
| K2 | 各サービスの Auto Scaling の機能 | [Auto Scaling](domain4.md#t4-3-auto-scaling) |
| K3 | アラートの通知とアクション | [アラート](domain4.md#t4-3-alerts) |
| K4 | ヘルスチェックの機能 | [ヘルスチェック](domain4.md#t4-3-health-checks) |
| S1 | Auto Scaling の構成の設定 | [Auto Scaling](domain4.md#t4-3-auto-scaling) |
| S2 | カスタムメトリクス、フィルター、アラーム、通知 | [アラート](domain4.md#t4-3-alerts) |
| S3 | S3 イベントによるログ処理と配信 | [S3 イベント](domain4.md#t4-3-s3-logs) |
| S4 | EventBridge の通知 | [EventBridge](domain4.md#t4-3-eventbridge) |
| S5 | エージェントの導入と設定 | [エージェント](domain4.md#t4-3-agents) |
| S6 | Config ルールによる修復 | [Config の修復](domain4.md#t4-3-config-remediation) |
| S7 | ヘルスチェックの設定 | [ヘルスチェック](domain4.md#t4-3-health-checks) |

## 分野5: インシデントとイベントへの対応 {#domain5}

### タスク 5.1: イベントソース {#c-5-1}

| 項目 | 内容 | ページ |
|---|---|---|
| K1 | イベントを生成、取得、処理するサービス | [イベントソース](domain5.md#t5-1-event-sources) |
| K2 | イベント駆動アーキテクチャ | [アーキテクチャ](domain5.md#t5-1-architectures) |
| S1 | イベントソースの統合 | [イベントソース](domain5.md#t5-1-event-sources) |
| S2 | イベント処理のワークフロー | [ワークフロー](domain5.md#t5-1-workflows) |

### タスク 5.2: 構成の変更 {#c-5-2}

| 項目 | 内容 | ページ |
|---|---|---|
| K1 | フリート管理のサービス | [フリート管理](domain5.md#t5-2-fleet) |
| K2 | 構成管理のサービス | [構成管理](domain5.md#t5-2-config) |
| S1 | システムへの構成変更の適用 | [構成変更の適用](domain5.md#t5-2-apply-changes) |
| S2 | イベントに応じたインフラの変更 | [インフラの変更](domain5.md#t5-2-respond) |
| S3 | 望ましくない状態の修復 | [状態の修復](domain5.md#t5-2-remediate) |

### タスク 5.3: 障害の調査 {#c-5-3}

| 項目 | 内容 | ページ |
|---|---|---|
| K1 | メトリクスとログのサービス | [メトリクスとログ](domain5.md#t5-3-observability) |
| K2 | サービスの状態を見るサービス | [サービスの状態](domain5.md#t5-3-service-health) |
| K3 | 根本原因の分析 | [根本原因](domain5.md#t5-3-root-cause) |
| S1 | 失敗したデプロイの分析 | [失敗したデプロイ](domain5.md#t5-3-failed-deployments) |
| S2 | 失敗したプロセスのインシデントの分析 | [プロセスの障害](domain5.md#t5-3-failed-processes) |

## 分野6: セキュリティとコンプライアンス {#domain6}

### タスク 6.1: ID とアクセス管理 {#c-6-1}

| 項目 | 内容 | ページ |
|---|---|---|
| K1 | 人と機械に使う IAM の要素 | [IAM の要素](domain6.md#t6-1-entities) |
| K2 | ID フェデレーション | [フェデレーション](domain6.md#t6-1-federation) |
| K3 | 権限境界による委任 | [権限境界](domain6.md#t6-1-boundaries) |
| K4 | 組織の SCP | [SCP](domain6.md#t6-1-scp) |
| S1 | 最小権限のポリシー設計 | [最小権限](domain6.md#t6-1-least-privilege) |
| S2 | RBAC と ABAC | [RBAC と ABAC](domain6.md#t6-1-rbac-abac) |
| S3 | 認証情報のローテーションの自動化 | [ローテーション](domain6.md#t6-1-rotation) |
| S4 | MFA、STS、インスタンスプロファイル | [MFA と STS](domain6.md#t6-1-mfa-sts) |

### タスク 6.2: コントロールとデータ保護の自動化 {#c-6-2}

| 項目 | 内容 | ページ |
|---|---|---|
| K1 | ネットワークセキュリティの要素 | [ネットワーク](domain6.md#t6-2-network) |
| K2 | 証明書と PKI | [証明書](domain6.md#t6-2-certificates) |
| K3 | データ管理 | [データ管理](domain6.md#t6-2-data-management) |
| S1 | 複数アカウントへのコントロールの自動適用 | [自動適用](domain6.md#t6-2-automation) |
| S2 | 多層防御 | [多層防御](domain6.md#t6-2-defense-in-depth) |
| S3 | 機密データの検出の自動化 | [Macie](domain6.md#t6-2-macie) |
| S4 | 転送時と保存時の暗号化 | [暗号化](domain6.md#t6-2-encryption) |

### タスク 6.3: 監視と監査 {#c-6-3}

| 項目 | 内容 | ページ |
|---|---|---|
| K1 | セキュリティ監査のサービスと機能 | [監査](domain6.md#t6-3-audit-services) |
| K2 | 脆弱性とイベントを見つけるサービス | [検出のサービス](domain6.md#t6-3-vulnerability-services) |
| K3 | よくある脅威 | [脅威](domain6.md#t6-3-threats) |
| S1 | 堅牢なセキュリティ監査の実装 | [監査](domain6.md#t6-3-audit-services) |
| S2 | 異常なイベントの通知 | [通知](domain6.md#t6-3-alerting) |
| S3 | サービスとアプリのログの設定 | [ログの設定](domain6.md#t6-3-logging) |
| S4 | ログ、メトリクス、検出結果の分析 | [分析](domain6.md#t6-3-analysis) |

## 技術と概念 {#technologies}

[ガイドの一覧](https://docs.aws.amazon.com/aws-certification/latest/devops-engineer-professional-02/dop-technologies-concepts.html)にある項目です。

| 内容 | ページ |
|---|---|
| アプリケーションのデプロイ | [デプロイ方式](domain1.md#t1-4-methods) |
| アプリケーションの統合 | [疎結合](domain3.md#t3-2-loose-coupling) |
| アプリケーションのパイプライン | [単一アカウントと複数アカウント](domain1.md#t1-1-multi-account) |
| 自動化 | [自動化に使うサービス](domain2.md#t2-3-automation-services) |
| コードリポジトリのベストプラクティス | [バージョン管理](domain1.md#t1-1-version-control) |
| コストの最適化 | [Auto Scaling とキャッシュ](domain3.md#t3-2-autoscaling-caching) |
| デプロイの要件 | [デプロイ戦略の判断](domain1.md#t1-1-deployment-strategy) |
| ハイブリッドのデプロイ | [配布するツール](domain1.md#t1-4-distribution) |
| IAM ポリシー | [IAM の要素](domain6.md#t6-1-entities) |
| メトリクス、監視、アラーム、ログ | [監視](domain4.md#t4-1-monitoring) |
| ネットワーク ACL とセキュリティグループの設計と実装 | [ネットワーク](domain6.md#t6-2-network) |
| 運用のベストプラクティス | [構成変更の適用](domain5.md#t5-2-apply-changes) |
| ロールバックの手順 | [デプロイ方式](domain1.md#t1-4-methods) |

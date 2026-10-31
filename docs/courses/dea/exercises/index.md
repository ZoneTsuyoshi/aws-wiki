# 問題集

DEA-C01（試験ガイド バージョン 1.1）を基準にした話題ごとの本番形式の問題です。すべてオリジナルの問題で、実際の試験問題ではありません。答えは問題の下を開くと確認でき、選択肢ごとの解説と解説ページへのリンクがあります。

1. まず[分野のページ](../index.md#study-path)で範囲を確認します。
2. サービスの解説を読み、問題を解きます。
3. 間違えた問題は、解説のリンク先に戻って確認します。

1 つの問題集が複数の分野のスキルを含むことがあります。主な分野の表に載せています。分野ごとの問題の一覧は、各分野の[サービス別の学習](../study/domain1/index.md)にあります。

## 分野1: データの取り込みと変換 {#domain1}

| 問題集 | 主な内容 |
|---|---|
| [Kinesis とストリーミング](streaming.md) | 読み手、Lambda の設定、ファンアウト、リプレイ、状態 |
| [バッチ取り込みと接続](ingestion.md) | Glue と COPY の設定、接続元の制限、JDBC |
| [変換と処理](transform.md) | サービスの選択、形式、費用、失敗の調査 |
| [オーケストレーションとイベント](orchestration.md) | Step Functions、MWAA、Glue ワークフロー、EventBridge |
| [Lambda](lambda.md) | 最適化、同時実行、ストレージ、自動化 |
| [データ API と SDK](data-apis.md) | API の利用、作成、保守、SDK |
| [EMR、コンテナと分散処理](emr-containers.md) | コンテナ、分散処理、トレードオフ、保守 |
| [IaC、CI/CD と開発の実践](devops.md) | 言語、IaC、SAM、CI/CD |

## 分野2: データストアの管理 {#domain2}

| 問題集 | 主な内容 |
|---|---|
| [データストアの選択](datastores.md) | 保存先の選択、アクセスパターン、パーティション |
| [Redshift](redshift.md) | 遠隔アクセス、ロック、COPY、設計、権限、共有 |
| [データカタログとスキーマ](catalog.md) | クローラー、パーティションの同期、接続、スキーマの変化 |
| [S3 のライフサイクルとオープンテーブル形式](s3-lifecycle.md) | 階層、失効、バージョニング、削除、Iceberg |
| [移行とスキーマ変換](migration.md) | 転送ツール、SCT、DMS Schema Conversion |
| [LLM とベクトル](genai-vector.md) | バッチ推論、ベクトルインデックス、埋め込み |

## 分野3: データの運用とサポート {#domain3}

| 問題集 | 主な内容 |
|---|---|
| [Athena と SQL](athena.md) | 最適化、ビュー、Spark、集計 |
| [監視とトラブルシューティング](monitoring.md) | CloudTrail、CloudWatch、性能問題、ログの分析 |
| [データ品質とデータ準備](data-quality.md) | DataBrew、Data Quality、可視化、サンプリング、偏り |

## 分野4: データのセキュリティとガバナンス {#domain4}

| 問題集 | 主な内容 |
|---|---|
| [IAM とネットワークの権限](iam.md) | セキュリティグループ、ロール、ポリシー |
| [Lake Formation と認可の方式](lake-formation.md) | データフィルター、LF タグ、ABAC |
| [暗号化とシークレット](encryption-secrets.md) | Secrets Manager、KMS、転送時の暗号化 |
| [監査ログ](audit-logging.md) | 証跡、データ保護、ログの分析 |
| [プライバシーとコンプライアンス](privacy-compliance.md) | Macie、SCP、Config、データ主権 |
| [SageMaker Catalog とガバナンス](sagemaker-governance.md) | ビジネスカタログ、リネージ、プロジェクト、共有 |

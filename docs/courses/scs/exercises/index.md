# 問題集

SCS-C03 を基準にした、話題ごとの本番形式の問題です。すべてオリジナルの問題で、実際の試験問題ではありません。答えは問題の下を開くと確認でき、選択肢ごとの解説と解説ページへのリンクがあります。

1. まず[分野のページ](../index.md#study-path)で範囲を確認します。
2. 分野ごとの学習ページで要点を読み、問題を解きます。
3. 間違えた問題は、解説のリンク先に戻って確認します。

## 分野1: 検出 {#domain1}

| 問題集 | 主な内容 |
|---|---|
| [脅威の監視](threat-monitoring.md) | GuardDuty、Security Hub、Macie、Inspector、ヘルスチェック |
| [ログの仕組み](logging.md) | CloudTrail、CloudWatch Logs、Security Lake、Athena、フローログ |
| [監視のトラブルシューティング](monitoring-troubleshooting.md) | ログが出ない原因の切り分け、誤設定の修正 |

## 分野2: インシデント対応 {#domain2}

| 問題集 | 主な内容 |
|---|---|
| [インシデント対応計画](incident-planning.md) | ランブック、事前の備え、FIS、Resilience Hub、自動修復 |
| [フォレンジックと原因分析](forensics.md) | 証拠の取得と保管、ログの関連付け、Detective |
| [検証と封じ込め](containment.md) | 検出結果の検証、抑制、封じ込め、認証情報の失効、復旧 |

## 分野3: インフラストラクチャのセキュリティ {#domain3}

| 問題集 | 主な内容 |
|---|---|
| [エッジのセキュリティ](edge-security.md) | WAF、CloudFront、Shield、IoT ポリシー、OCSF |
| [コンピューティングの強化](compute-hardening.md) | Image Builder、ロール、Patch Manager、Session Manager |
| [脆弱性スキャン](vulnerability-scanning.md) | Inspector、Runtime Monitoring、パイプラインのスキャン |
| [生成 AI の保護](genai-security.md) | OWASP LLM Top 10、Guardrails、AgentCore |
| [ネットワークのセキュリティ](network-security.md) | SG、NACL、Network Firewall、MACsec、Verified Access、Network Access Analyzer |

## 分野4: ID とアクセス管理 {#domain4}

| 問題集 | 主な内容 |
|---|---|
| [認証](authentication.md) | IAM Identity Center、Cognito、STS、署名付き URL |
| [認可](authorization.md) | Verified Permissions、Roles Anywhere、ABAC、権限境界 |
| [アクセスの分析](access-analysis.md) | 拒否メッセージ、クロスアカウントの評価、Access Analyzer、データ境界 |

## 分野5: データ保護 {#domain5}

| 問題集 | 主な内容 |
|---|---|
| [転送時の暗号化](encryption-in-transit.md) | ELB、RDS、VPC エンドポイント、Nitro、EMR、SageMaker AI |
| [保存時のデータ](data-at-rest.md) | S3 の暗号化、CloudHSM、Object Lock、ライフサイクル、AWS Backup |
| [鍵と証明書の管理](key-management.md) | インポートした鍵素材、外部キーストア、マルチリージョンキー、ACM、Private CA |
| [シークレットとマスキング](secrets-masking.md) | Secrets Manager、Parameter Store、データ保護ポリシー |

## 分野6: セキュリティの基盤とガバナンス {#domain6}

| 問題集 | 主な内容 |
|---|---|
| [Organizations と Control Tower](organizations.md) | SCP、RCP、宣言型ポリシー、委任管理者、ルートの管理 |
| [一貫した展開](deployment.md) | StackSets、Guard、Hooks、タグ、Firewall Manager、Service Catalog、RAM |
| [準拠の評価](compliance.md) | Config、適合パック、Audit Manager、Artifact、Well-Architected Tool |

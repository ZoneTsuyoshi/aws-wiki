# 分野2: マルチアカウントのガバナンス

組織全体に統制を効かせる手段を問います。予防、検出、修復のどの段階の答えが求められているかを読み取ります。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [2.3.1](../../domain2.md#skill-2-3-1) | 組織構造、ガードレール、ランディングゾーン |
| [2.3.2](../../domain2.md#skill-2-3-2) | ログと設定の一元管理 |
| [2.3.3](../../domain2.md#skill-2-3-3) | アカウント間のリソース共有 |
| [2.3.4](../../domain2.md#skill-2-3-4) | SCP と RCP によるポリシーの強制 |
| [2.3.5](../../domain2.md#skill-2-3-5) | コンプライアンスの自動監視 |
| [2.3.6](../../domain2.md#skill-2-3-6) | 脆弱性スキャンとパッチ管理の自動化 |

## 学習の順番 {#study-order}

1. [OU の設計](../../../../services/governance.md#org-ous)と[ランディングゾーンの構造](../../../../services/governance.md#ct-landing-zone): OU をポリシーの違いで分ける理由を確認します。
2. [コントロール](../../../../services/governance.md#ct-controls)と[ドリフトと拡張](../../../../services/governance.md#ct-drift): 3 種類の動作、ドリフトの修復、AFT を押さえます。
3. [SCP](../../../../services/governance.md#scp)、[RCP](../../../../services/governance.md#rcp)、[SCP と RCP の例外](../../../../services/identity-directory.md#guardrail-exceptions): 対象の違いと、効かないものを表で覚えます。
4. [証跡とイベント履歴](../../../../services/observability.md#cloudtrail-trails)と[アグリゲーター](../../../../services/governance.md#config-aggregators): 操作の記録と設定の準拠の集め方を確認します。
5. [GuardDuty の複数アカウント](../../../../services/threat-detection.md#guardduty-multi-account)、[Security Hub の組織と集約](../../../../services/threat-detection.md#security-hub-org)、[Security Lake](../../../../services/threat-detection.md#security-lake): 委任管理者とリージョンの範囲を比べます。
6. [モデル呼び出しログ](../../../../services/ai.md#invocation-logging): 送信先の制約と、組織での集め方を確認します。
7. [AWS Resource Access Manager](../../../../services/governance.md#ram)と [VPC サブネットの共有](../../../../services/governance.md#ram-vpc-sharing): 共有するものと、参加者ができることを押さえます。
8. [Config ルール](../../../../services/governance.md#config-rules)、[修復](../../../../services/governance.md#config-remediation)、[適合パック](../../../../services/governance.md#config-conformance-packs): 検出から修復までの流れをつかみます。
9. [Inspector](../../../../services/threat-detection.md#inspector)、[実行の設定方法](../../../../services/operations.md#patch-methods)、[パッチベースライン](../../../../services/operations.md#patch-baselines): 見つける役と直す役を分けて覚えます。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| SCP のサイズと関連付け | 10,240 文字。各レベル 10 個 | |
| RCP のサイズと関連付け | 5,120 文字。各レベル 5 個 | `RCPFullAWSAccess` を含む |
| イベント履歴 | 90 日の管理イベント | 長期の保管は証跡 |
| `aws:approve` | 既定 7 日、最大 30 日 | 複数アカウントとリージョンの実行には非対応 |
| 定義済みのパッチベースライン | Amazon Linux 2023 などは 7 日後に承認 | 調整はカスタムベースライン |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| Git と Terraform でアカウントを発行する | Account Factory for Terraform |
| 違反するテンプレートを作成前に失敗させる | プロアクティブコントロール（CloudFormation Hooks） |
| 管理者でも止められない全アカウントの監査ログ | 組織の証跡を Log Archive へ。Object Lock を併用 |
| 全リージョンで GuardDuty を統一する | 使用するリージョンごとに委任管理者と自動有効化 |
| ログを OCSF で集めて SIEM へ渡す | Security Lake。ロールアップリージョンでサブスクライバーを作る |
| 全アカウントの準拠状況を一画面で見る | 組織の Config アグリゲーター |
| 同じ信頼の境界のアカウントが密に通信する | VPC サブネットの共有 |
| CIDR の重複を防ぎ、VPC の作成は任せる | IPAM のプールを RAM で共有 |
| 社内の主体に禁止する | SCP |
| 組織の外の主体を締め出す | RCP |
| ルールと修復を組織へ配布する | 組織の適合パック |
| 影響の大きい修復を確認してから実行する | Automation の `aws:approve` |
| 全アカウント、全リージョンの標準を統一する | Security Hub CSPM の中央設定 |
| 複数のアカウントとリージョンへパッチを配る | Quick Setup のパッチポリシー |

## 引っかかりやすい点 {#traps}

- SCP も RCP も管理アカウントには効きません。指定の書き方で変えることもできないので、ワークロードを置きません。
- どちらも権限を与えません。実際の許可は IAM ポリシーなどで行います。
- SCP の許可は、ルートからアカウントまでのすべてのレベルで必要です。
- RCP の Deny はバケットポリシーの Allow より優先されます。例外は Deny の条件に書きます。
- Control Tower のドリフトは自動で解消されません。独自の制限は別の SCP にします。
- モデル呼び出しログの送信先は同じアカウント、同じリージョンです。中央の S3 を直接指定できません。
- アグリゲーターはデータを集めて見るものです。ルールの配布はしません。
- GuardDuty は脅威、Inspector は脆弱性です。
- Security Hub CSPM のローカル設定は既存のアカウントに効きません。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [org-governance 問1](../../exercises/org-governance.md#q1) | 2.3.1 | ある持株会社は、事業会社ごとに OU を作り、その下に本番と開発のアカウントを混ぜて置いています。結… |
| [org-governance 問2](../../exercises/org-governance.md#q2) | 2.3.1 | あるプラットフォームチームは、Control Tower のランディングゾーンで年に約 60 のアカ… |
| [org-governance 問3](../../exercises/org-governance.md#q3) | 2.3.1 | ある会社の開発者は CloudFormation でリソースを作ります。「S3 バケットはアクセスロ… |
| [org-governance 問4](../../exercises/org-governance.md#q4) | 2.3.1 | ある管理者は緊急の対応として、Control Tower が管理する SCP を Organizat… |
| [org-governance 問5](../../exercises/org-governance.md#q5) | 2.3.2 | ある組織は 300 のアカウントの API の操作を監査します。メンバーアカウントの管理者であっても… |
| [org-governance 問6](../../exercises/org-governance.md#q6) | 2.3.2 | ある会社は東京リージョンで GuardDuty の委任管理者を指定し、組織の自動有効化を設定しました… |
| [org-governance 問7](../../exercises/org-governance.md#q7) | 2.3.2 | あるセキュリティチームは、CloudTrail、VPC フローログ、WAF ログを全アカウントと複数… |
| [org-governance 問8](../../exercises/org-governance.md#q8) | 2.3.2 | ある組織の 30 のアカウントで Bedrock を使っています。監査のために、全アカウントのモデル… |
| [org-governance 問9](../../exercises/org-governance.md#q9) | 2.3.2 | ある監査チームは、組織の全アカウントと全リージョンの Config の準拠状況を一画面で確認したいと… |
| [org-governance 問10](../../exercises/org-governance.md#q10) | 2.3.3 | ある会社では、12 のアプリのアカウントが互いに頻繁に通信します。同じ信頼の境界の中にあり、ネットワ… |
| [org-governance 問11](../../exercises/org-governance.md#q11) | 2.3.3 | ネットワークチームは中央のアカウントで Transit Gateway と Route 53 VPC… |
| [org-governance 問12](../../exercises/org-governance.md#q12) | 2.3.3 | ある組織では、各チームが勝手に CIDR を決めるので、重複で接続できない VPC が増えました。組… |
| [org-governance 問13](../../exercises/org-governance.md#q13) | 2.3.4 | ある組織は次の 2 つの統制を全メンバーアカウントへ入れます。社内の管理者が CloudTrail … |
| [org-governance 問14](../../exercises/org-governance.md#q14) | 2.3.4 | ある組織のルートに、未承認のリージョンの操作を拒否する SCP を関連付けました。後日、未承認のリー… |
| [org-governance 問15](../../exercises/org-governance.md#q15) | 2.3.4 | ある組織の構造は「ルート → Sandbox OU → アカウント X」です。ルートとアカウント X… |
| [org-governance 問16](../../exercises/org-governance.md#q16) | 2.3.4 | ある組織は、組織の外の主体による S3 へのアクセスを拒否する RCP を全 OU へ適用しています… |
| [org-governance 問17](../../exercises/org-governance.md#q17) | 2.3.5 | ある組織は、PCI DSS の社内基準に沿った Config のルールと修復をまとめて、全メンバーア… |
| [org-governance 問18](../../exercises/org-governance.md#q18) | 2.3.5 | ある会社は Config のルールで違反を検出しています。公開された開発用の S3 バケットは、すぐ… |
| [org-governance 問19](../../exercises/org-governance.md#q19) | 2.3.5 | ある組織は Security Hub CSPM で CIS の標準を使っています。ローカル設定で運用… |
| [org-governance 問20](../../exercises/org-governance.md#q20) | 2.3.6 | ある組織は 80 のアカウントと 3 つのリージョンに EC2 を持っています。マネージドノードのパ… |
| [org-governance 問21](../../exercises/org-governance.md#q21) | 2.3.6 | ある会社の Amazon Linux 2023 のサーバーでは、まず開発環境へパッチを適用し、問題が… |
| [org-governance 問22](../../exercises/org-governance.md#q22) | 2.3.6 | ある組織は EC2、ECR のイメージ、Lambda の脆弱性を全アカウントで継続して調べます。重大… |

<!-- questions:end -->

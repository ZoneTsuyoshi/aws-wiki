# 分野1: ガバナンスと責任共有

複数アカウントの統制、リージョンの選択、責任の分担、コンプライアンスの 4 つを扱います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [複数アカウントのセキュリティ戦略](../../domain1.md#t1-1-multi-account) | 複数アカウントにまたがるアクセス制御と管理、複数アカウントのセキュリティ戦略 |
| [グローバルインフラストラクチャとセキュリティ](../../domain1.md#t1-1-global-infra) | グローバルインフラストラクチャ |
| [責任共有モデル](../../domain1.md#t1-1-shared-responsibility) | 責任共有モデル |
| [コンプライアンス要件への対応](../../domain1.md#t1-3-compliance) | コンプライアンス要件に合わせた AWS 技術の選択 |

## 学習の順番 {#study-order}

1. [AWS Organizations](../../../../services/governance.md#organizations)と[SCP](../../../../services/governance.md#scp): OU と SCP の関係、SCP が効かない対象を確認します。
2. [RCP](../../../../services/governance.md#rcp)と[SCP と RCP の例外](../../../../services/identity-directory.md#guardrail-exceptions): SCP との違いと例外を押さえます。
3. [AWS Control Tower](../../../../services/governance.md#control-tower)と[AWS Resource Access Manager](../../../../services/governance.md#ram): 環境の組み立てとリソースの共有を区別します。
4. [リージョン](../../../../services/cloud-foundations.md#regions)と[アベイラビリティーゾーン](../../../../services/cloud-foundations.md#availability-zones): リージョンを選ぶ基準と AZ の性質を確認します。
5. [責任共有モデル](../../../../services/cloud-foundations.md#shared-responsibility)と[サービスごとの違い](../../../../services/cloud-foundations.md#responsibility-by-service): サービスごとに利用者の範囲がどう変わるかを表で覚えます。
6. [AWS Artifact](../../../../services/threat-detection.md#artifact)と[適合パック](../../../../services/governance.md#config-conformance-packs): AWS の報告書と自社の設定の評価を分けます。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| CloudTrail のイベント履歴 | 90 日 | 長期の保管には証跡が必要 |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 管理者でも特定の操作をさせない | SCP |
| 組織の外からのアクセスをリソース側で制限する | RCP |
| ベストプラクティスの環境をすばやく作る | Control Tower |
| サブネットを他のアカウントに使わせる | RAM の VPC サブネット共有 |
| 特定のリージョンの外に置かせない | `aws:RequestedRegion` を条件にした SCP |
| AWS の SOC レポートを入手する | AWS Artifact |
| 自社の設定を基準で評価して配布する | Config の適合パック |
| 単一テナントの HSM | CloudHSM |

## 引っかかりやすい点 {#traps}

- SCP は管理アカウントとサービスリンクロールには効きません。
- Artifact は AWS の報告書の入手先で、自社の環境を評価しません。
- RDS でも、SG、DB のユーザー、暗号化の設定、データは利用者の責任です。
- リージョンの制限を書くときは、IAM や Route 53 などのグローバルなサービスの除外を考えます。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [governance 問1](../../exercises/governance.md#q1) | 複数アカウントの戦略 | 全メンバーアカウントで、各アカウントの管理者を含めて CloudTrail の停止を禁止します。最も… |
| [governance 問2](../../exercises/governance.md#q2) | 複数アカウントの戦略 | SCP の説明として正しいものを選んでください。（2つ選択） |
| [governance 問3](../../exercises/governance.md#q3) | 複数アカウントの戦略 | 組織の S3 バケットに、組織の外のプリンシパルがアクセスできないよう、リソース側の上限を組織全体で… |
| [governance 問4](../../exercises/governance.md#q4) | 複数アカウントの戦略 | 新しい会社のマルチアカウント環境を、ベストプラクティスに沿ってすばやく構築します。ログ用と監査用のア… |
| [governance 問5](../../exercises/governance.md#q5) | 複数アカウントの戦略 | ネットワークチームのアカウントの VPC のサブネットを、複数のアプリのアカウントで使わせます。VP… |
| [governance 問6](../../exercises/governance.md#q6) | グローバルインフラ | 規制で、顧客データを東京と大阪のリージョンの外に置けません。誤って他のリージョンにリソースを作る操作… |
| [governance 問7](../../exercises/governance.md#q7) | グローバルインフラ | アベイラビリティーゾーン（AZ）の説明として正しいものはどれですか。 |
| [governance 問8](../../exercises/governance.md#q8) | グローバルインフラ | ある会社がリージョンを選びます。判断の材料として最も優先して確認すべきものはどれですか。 |
| [governance 問9](../../exercises/governance.md#q9) | 責任共有モデル | RDS for MySQL を使っています。責任共有モデルで利用者の責任になるものを選んでください。… |
| [governance 問10](../../exercises/governance.md#q10) | 責任共有モデル | EC2 で動かす Linux のセキュリティパッチの責任について、正しいものはどれですか。 |
| [governance 問11](../../exercises/governance.md#q11) | 責任共有モデル | 同じ処理を EC2、Lambda で動かす場合を比べます。Lambda に移すことで、利用者の責任か… |
| [governance 問12](../../exercises/governance.md#q12) | コンプライアンス | 監査人から、AWS の SOC 2 レポートと ISO の認証の提出を求められました。どこで入手しま… |
| [governance 問13](../../exercises/governance.md#q13) | コンプライアンス | 自社の全アカウントの設定が、規制の基準に合っているかを継続して評価し、結果を監査に示します。ルールの… |
| [governance 問14](../../exercises/governance.md#q14) | コンプライアンス | 規制で、単一テナントの HSM で鍵を管理し、FIPS 140 の検証済みの機器を自社だけで制御する… |
| [governance 問15](../../exercises/governance.md#q15) | コンプライアンス | API の操作の記録を 7 年間、改ざんされない形で保管します。最も適切なものを選んでください。（2… |

<!-- questions:end -->

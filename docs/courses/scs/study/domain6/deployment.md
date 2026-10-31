# 分野6: 一貫した展開

統制を組織全体に同じ形で配り、いつ何を検証するかを選ぶ力を問います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [6.2.1](../../domain6.md#skill-6-2-1) | IaC による一貫した展開 |
| [6.2.2](../../domain6.md#skill-6-2-2) | タグによる整理 |
| [6.2.3](../../domain6.md#skill-6-2-3) | ポリシーと設定の一元展開 |
| [6.2.4](../../domain6.md#skill-6-2-4) | アカウント間の安全な共有 |

## 学習の順番 {#study-order}

1. [StackSets の設定](../../../../services/iac.md#stacksets-settings): 2 つの権限モデルと自動デプロイを覚えます。
2. [検証方法のまとめ](../../../../services/iac.md#validate-iac)、[変更セット](../../../../services/iac.md#change-sets)、[ドリフト検出](../../../../services/iac.md#drift): ツールごとに、いつ何を確かめるかを整理します。
3. [タグ戦略](../../../../services/governance.md#tagging-strategy)と[タグポリシー](../../../../services/governance.md#tag-policies): 統一と強制の違いを押さえます。
4. [Resource Groups](../../../../services/governance.md#resource-groups)と[コスト配分タグ](../../../../services/cost-management.md#cost-allocation-tags): 検索と費用への反映を確認します。
5. [Firewall Manager](../../../../services/threat-detection.md#firewall-manager): 前提とポリシーの種類を覚えます。
6. [Service Catalog](../../../../services/governance.md#service-catalog)と [AWS RAM](../../../../services/governance.md#ram): 共有するものの違いを理解します。
7. [VPC サブネットの共有](../../../../services/governance.md#ram-vpc-sharing): オーナーと参加者の責任を確認します。

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 新しいアカウントにも自動で統制を配る | サービスマネージドの StackSets と自動デプロイ |
| パイプライン外のデプロイも止める | CloudFormation Hooks |
| Terraform や Kubernetes の設定も検証 | CloudFormation Guard |
| 適用の前に何が変わるかを見る | 変更セット |
| 手動の変更との差異を見る | ドリフト検出 |
| タグの表記を統一 | タグポリシー |
| タグなしの作成を止める | SCP の `aws:RequestTag` |
| 作成済みのタグの漏れを見つける | Config の `required-tags` |
| 全 ALB に共通の WAF を強制 | Firewall Manager の WAF ポリシー |
| Network Firewall のポリシーの展開が失敗 | AWS RAM の組織の共有 |
| 権限なしで承認済みの構成を作らせる | Service Catalog の起動制約 |

## 引っかかりやすい点 {#traps}

- Guard はサーバー側で強制しません。強制は Hooks です。
- タグのキーと値は大文字小文字を区別します。
- タグに機密情報を入れません。課金や診断のログに使われることがあります。
- Firewall Manager の内容の監査と使用状況の監査は、自動修復を無効にして始めます。
- Firewall Manager は展開の仕組みで、検査そのものは WAF や Network Firewall が行います。
- 起動制約がないと、利用者自身の権限で作成することになります。
- 組織を離れたアカウントは、既定で共有へのアクセスを失います。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [deployment 問1](../../exercises/deployment.md#q1) | 6.2.1 | 標準のロールと Config ルールを全アカウントへ CloudFormation で配ります。アカ… |
| [deployment 問2](../../exercises/deployment.md#q2) | 6.2.1 | KMS で既定の暗号化をしていない S3 バケットの作成を止めます。CI のチェックに加え、パイプラ… |
| [deployment 問3](../../exercises/deployment.md#q3) | 6.2.1 | Terraform も使うチームが、CloudFormation と同じ組織の基準でプランを検証した… |
| [deployment 問4](../../exercises/deployment.md#q4) | 6.2.1 | 本番のスタックで、IAM ロールの置き換えが起きないかを、デプロイの前に確認したいと考えています。別… |
| [deployment 問5](../../exercises/deployment.md#q5) | 6.2.2 | 費用の配賦のため、全アカウントのタグの CostCenter の値を統一します。costcenter… |
| [deployment 問6](../../exercises/deployment.md#q6) | 6.2.2 | チームの要望が 3 つあります。作成済みのリソースのタグの漏れを見つける、タグを費用のレポートに反映… |
| [deployment 問7](../../exercises/deployment.md#q7) | 6.2.2 | あるチームが、リソースの Customer タグに取引先の担当者のメールアドレスを入れて運用していま… |
| [deployment 問8](../../exercises/deployment.md#q8) | 6.2.3 | 全アカウントの ALB に、共通の WAF ルールグループを強制します。新しいアカウントや新しい A… |
| [deployment 問9](../../exercises/deployment.md#q9) | 6.2.3 | Firewall Manager の Network Firewall のポリシーを作成しましたが、… |
| [deployment 問10](../../exercises/deployment.md#q10) | 6.2.3 | 組織全体のセキュリティグループを整理します。過度に許可された内容の SG を見つけ、未使用の SG … |
| [deployment 問11](../../exercises/deployment.md#q11) | 6.2.3 | 検討中の要望を、最適な手段に対応させます。正しい組み合わせを選んでください。（2つ選択） |
| [deployment 問12](../../exercises/deployment.md#q12) | 6.2.4 | 開発者に EC2 の権限を与えずに、承認済みの構成だけをセルフサービスで作らせます。インスタンスタイ… |
| [deployment 問13](../../exercises/deployment.md#q13) | 6.2.4 | ネットワークチームが、ネットワークアカウントの VPC サブネットを他のアカウントへ共有します。ルー… |
| [deployment 問14](../../exercises/deployment.md#q14) | 6.2.4 | 3 つの要望を比べています。「別のアカウントのチームに Transit Gateway をそのまま使… |
| [deployment 問15](../../exercises/deployment.md#q15) | 6.2.4 | AWS RAM で OU に Transit Gateway を共有しています。買収したアカウントが… |

<!-- questions:end -->

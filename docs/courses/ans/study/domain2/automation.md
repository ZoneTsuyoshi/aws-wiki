# 分野2: ネットワークの自動化

ネットワークを IaC で作り、イベントで保つ問題です。全タスク 2.4 を含みます。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [自動化](../../domain2.md#t2-1-automation) | インフラの自動化 |
| [自動化](../../domain2.md#t2-2-automation) | インフラの自動化 |
| [IaC](../../domain2.md#t2-4-iac) | IaC（CDK、CloudFormation、CLI、SDK、API）、繰り返せるネットワーク構成の作成と管理 |
| [イベント駆動](../../domain2.md#t2-4-event) | イベント駆動のネットワーク自動化、イベント駆動の機能の統合 |
| [ハードコード](../../domain2.md#t2-4-hardcoding) | IaC でハードコードする問題 |
| [ハイブリッドの自動化](../../domain2.md#t2-4-hybrid) | ハイブリッドの自動化と IaC の統合 |
| [リスクとコスト](../../domain2.md#t2-4-risk-cost) | リスクを除き、効率と最低コストを両立 |
| [最適化](../../domain2.md#t2-4-optimize) | IaC によるネットワーク資源の最適化の自動化 |

## 学習の順番 {#study-order}

1. [CloudFormation テンプレート](../../../../services/iac.md#cloudformation-template): テンプレートの基本を確認します。
2. [ネストされたスタックと StackSets](../../../../services/iac.md#nested-stacks-stacksets): StackSets で多数のアカウントへ展開します。
3. [変更セット](../../../../services/iac.md#change-sets): 置き換えの確認に使います。
4. [カスタムリソース](../../../../services/iac.md#custom-resources): オンプレミスと連携する方法を押さえます。
5. [EventBridge による修復パターン](../../../../services/operations.md#eventbridge-remediation): イベントでの修復の流れを理解します。
6. [マッピングと条件](../../../../services/iac.md#mappings-conditions): 環境差の吸収を確認します。

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 新しいアカウントへ自動で展開 | サービスマネージドの StackSets |
| 置き換えの有無を実行前に確認 | 変更セット |
| 手動の変更の検出 | ドリフト検出 |
| オンプレミスの API を連動 | カスタムリソースと Lambda |
| CIDR のハードコードをなくす | IPAM のプール |

## 引っかかりやすい点 {#traps}

- シークレットは Secrets Manager の動的参照で渡します。
- 修復が同じルールを起動してループしないようにします。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [automation 問1](../../exercises/automation.md#q1) | 自動化 | ハイブリッド接続を全部 CloudFormation で展開する計画です。VIF、DX ゲートウェイ… |
| [automation 問2](../../exercises/automation.md#q2) | 自動化 | 20 の拠点の CGW と VPN 接続を、同じ形で作成します。拠点の IP と ASN は違います… |
| [automation 問3](../../exercises/automation.md#q3) | 自動化 | VPN のトンネルの事前共有キーを CloudFormation で指定します。リポジトリは社内で共… |
| [automation 問4](../../exercises/automation.md#q4) | 自動化 | 組織の全 VPC を Transit Gateway へ接続するテンプレートを展開します。新しいアカ… |
| [automation 問5](../../exercises/automation.md#q5) | 自動化 | 共有された Transit Gateway へのアタッチメントと VPC のルートを 1 つのスタッ… |
| [automation 問6](../../exercises/automation.md#q6) | 自動化 | StackSets で VPC アタッチメントを各アカウントに展開します。Transit Gatew… |
| [automation 問7](../../exercises/automation.md#q7) | IaC | ネットワークチームは 40 個の VPC と多数のサブネットを、TypeScript のループと共通… |
| [automation 問8](../../exercises/automation.md#q8) | IaC | 本番の VPC のスタックのサブネットの属性を変更します。停止につながる置き換えが起きないかを実行前… |
| [automation 問9](../../exercises/automation.md#q9) | IaC | ネットワークチームは CloudFormation で作ったルートテーブルが手動で変更されていないか… |
| [automation 問10](../../exercises/automation.md#q10) | イベント駆動 | SG に 0.0.0.0/0 の SSH が追加されたら、数分以内に自動で削除して通知します。組織の… |
| [automation 問11](../../exercises/automation.md#q11) | イベント駆動 | 全 VPC でフローログを必ず有効にします。作り忘れた VPC を継続的に評価し、自動で作成して、準… |
| [automation 問12](../../exercises/automation.md#q12) | イベント駆動 | EventBridge と Lambda で SG を修復しています。修復の変更がまた同じルールを起… |
| [automation 問13](../../exercises/automation.md#q13) | ハードコード | テンプレートにサブネットの AZ 名 ap-northeast-1a と ap-northeast-… |
| [automation 問14](../../exercises/automation.md#q14) | ハードコード | テンプレートに 10.0.0.0/16 を書いて複数のアカウントへ展開したところ、Transit G… |
| [automation 問15](../../exercises/automation.md#q15) | ハードコード | ネットワークのテンプレートのハードコードを減らします。置き換えとして正しいものを選んでください。（2… |
| [automation 問16](../../exercises/automation.md#q16) | ハイブリッドの自動化 | CloudFormation で VPN を作成するとき、オンプレミスのルーターの管理 API も呼… |
| [automation 問17](../../exercises/automation.md#q17) | ハイブリッドの自動化 | データセンターの管理サーバーでスクリプトを実行し、ネットワーク機器へ設定を流します。SSM Agen… |
| [automation 問18](../../exercises/automation.md#q18) | ハイブリッドの自動化 | 新しい VPC の作成をきっかけに、オンプレミスのルーターの経路を更新します。また、新しい VPN … |
| [automation 問19](../../exercises/automation.md#q19) | リスクとコスト | 本番の Transit Gateway のスタックで、更新時の重要なリソースの置き換えと、スタックの… |
| [automation 問20](../../exercises/automation.md#q20) | リスクとコスト | ネットワークの更新のあと、接続の確認を自動化します。また、更新の間にアラームが発報したら自動で戻しま… |
| [automation 問21](../../exercises/automation.md#q21) | リスクとコスト | ネットワークの費用を見直して、使っていない資源の課金を止めます。整理の対象として費用の削減につながる… |
| [automation 問22](../../exercises/automation.md#q22) | 最適化 | 同じテンプレートで本番と開発を作ります。本番は NAT ゲートウェイを AZ ごと、開発は費用を抑え… |
| [automation 問23](../../exercises/automation.md#q23) | 最適化 | 全 VPC で S3 への大量の通信が NAT ゲートウェイを通り、処理料金が大きくなっています。V… |
| [automation 問24](../../exercises/automation.md#q24) | 最適化 | 全 VPC に同じ種類のインターフェイスエンドポイントが重複して作られています。VPC は Tran… |

<!-- questions:end -->

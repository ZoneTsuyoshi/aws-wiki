# 分野2: Organizations と統制

複数アカウントの構成と、定義、配布、検出、修復の担当を切り分ける力を問います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [アカウント構成](../../domain2.md#t2-2-structure) | アカウント構成とベストプラクティス |
| [標準化と自動化](../../domain2.md#t2-2-provisioning) | アカウント発行の標準化と自動化 |
| [Organizations と Control Tower](../../domain2.md#t2-2-org-ct) | アカウントの作成、統合、一元管理 |
| [複数アカウントの IAM](../../domain2.md#t2-2-iam) | 複数アカウントの IAM |
| [統制とセキュリティ](../../domain2.md#t2-2-governance) | 統制とセキュリティの大規模な実装 |

## 学習の順番 {#study-order}

1. [マルチアカウントのパターン](../../../../services/governance.md#multi-account-patterns): アカウントを分ける理由と OU の例を確認します。
2. [委任管理者](../../../../services/governance.md#delegated-admin): 管理アカウントで作業しない理由を理解します。
3. [AWS Control Tower](../../../../services/governance.md#control-tower): ランディングゾーンと Account Factory を押さえます。
4. [ドリフトと拡張](../../../../services/governance.md#ct-drift): Control Tower の外の変更の扱いと拡張の手段を確認します。
5. [コントロール](../../../../services/governance.md#ct-controls): 予防的、プロアクティブ、検出的の違いを覚えます。
6. [SCP](../../../../services/governance.md#scp): 効く範囲と、権限を与えないことを確認します。
7. [組織と集約](../../../../services/threat-detection.md#security-hub-org): 中央設定と集約を押さえます。

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| Terraform と Git でアカウントを発行する | Account Factory for Terraform |
| CloudFormation で標準の設定を足す | Customizations for Control Tower |
| OU に入ると自動で作る | StackSets の自動デプロイ |
| 作成の前に止める | プロアクティブコントロール |
| 組織の主体だけに許可する | `aws:PrincipalOrgID` |
| 検出結果の影響範囲を調べる | Detective |

## 引っかかりやすい点 {#traps}

- SCP は管理アカウントに効きません。
- SCP を使うには、すべての機能の有効化が必要です。
- Control Tower の外で OU や SCP を変更すると、ドリフトになります。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [organizations 問1](../../exercises/organizations.md#q1) | アカウント構成 | 新しい組織のアカウント構成を決めます。条件は次のとおりです。監査ログを開発者が消せない、パイプライン… |
| [organizations 問2](../../exercises/organizations.md#q2) | アカウント構成 | 監査で、次の指摘を受けました。GuardDuty と Config の管理の作業を、毎回管理アカウン… |
| [organizations 問3](../../exercises/organizations.md#q3) | アカウント構成 | ある企業は、1 つのアカウントに 20 のチームのワークロードを同居させています。Lambda の同… |
| [organizations 問4](../../exercises/organizations.md#q4) | 標準化と自動化 | Control Tower を使う組織で、新しいアカウントの発行を Terraform と Git … |
| [organizations 問5](../../exercises/organizations.md#q5) | 標準化と自動化 | Control Tower を使わない組織で、OU にアカウントを追加すると、ログ転送のロールと S… |
| [organizations 問6](../../exercises/organizations.md#q6) | 標準化と自動化 | Control Tower の環境で、全新規アカウントへ CloudFormation テンプレート… |
| [organizations 問7](../../exercises/organizations.md#q7) | Organizations と Control Tower | Control Tower を導入済みの環境で、管理者が Organizations のコンソールか… |
| [organizations 問8](../../exercises/organizations.md#q8) | Organizations と Control Tower | 買収した会社の組織を統合します。その会社のアカウントは現在、別の組織にあり、一括請求の機能だけを使っ… |
| [organizations 問9](../../exercises/organizations.md#q9) | Organizations と Control Tower | 独自の OU と SCP を持つ既存の組織があります。ログと監査のアカウント、基本のコントロール、新… |
| [organizations 問10](../../exercises/organizations.md#q10) | 複数アカウントの IAM | 本番の OU で、次の SCP を適用した後も、各アカウントの管理者ロールが別のリージョンにリソース… |
| [organizations 問11](../../exercises/organizations.md#q11) | 複数アカウントの IAM | ツール用アカウントのロールが、本番アカウントのロールを引き受けて S3 を読もうとすると拒否されます… |
| [organizations 問12](../../exercises/organizations.md#q12) | 複数アカウントの IAM | S3 のログバケットを、組織の全アカウントのロールだけが読めるようにします。アカウント ID を列挙… |
| [organizations 問13](../../exercises/organizations.md#q13) | 統制とセキュリティ | 次の統制を実現します。(1) 暗号化していない S3 バケットの作成を CloudFormation… |
| [organizations 問14](../../exercises/organizations.md#q14) | 統制とセキュリティ | 200 アカウント、10 リージョンの組織で、Security Hub CSPM の標準の有効化と … |
| [organizations 問15](../../exercises/organizations.md#q15) | 統制とセキュリティ | セキュリティ担当の質問に、それぞれサービスで答えます。(1) この GuardDuty の検出結果に… |

<!-- questions:end -->

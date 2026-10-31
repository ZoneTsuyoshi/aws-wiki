# 分野6: Organizations と Control Tower

どのポリシーが何に効き、何に効かないかを問います。管理アカウントと委任管理者の違い、ルートの扱いも要点です。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [6.1.1](../../domain6.md#skill-6-1-1) | Organizations の展開と設定 |
| [6.1.2](../../domain6.md#skill-6-1-2) | Control Tower の実装 |
| [6.1.3](../../domain6.md#skill-6-1-3) | 組織のポリシー |
| [6.1.4](../../domain6.md#skill-6-1-4) | セキュリティサービスの一元管理 |
| [6.1.5](../../domain6.md#skill-6-1-5) | ルートユーザーの認証情報の管理 |

## 学習の順番 {#study-order}

1. [機能セット](../../../../services/governance.md#org-feature-sets)と [OU の設計](../../../../services/governance.md#org-ous): すべての機能の必要性と、OU の分け方を押さえます。
2. [ポリシーの種類](../../../../services/governance.md#org-policy-types)、[SCP](../../../../services/governance.md#scp)、[RCP](../../../../services/governance.md#rcp): 上限と効かないものを表で覚えます。
3. [SCP と RCP の例外](../../../../services/identity-directory.md#guardrail-exceptions): サービスリンクロールと管理アカウントを確認します。
4. [Control Tower](../../../../services/governance.md#control-tower)と[コントロール](../../../../services/governance.md#ct-controls): 3 種類の動作と実装を結びつけます。
5. [ドリフトと拡張](../../../../services/governance.md#ct-drift): CfCT と AFT、ドリフトの解消を理解します。
6. [委任管理者](../../../../services/governance.md#delegated-admin)と [GuardDuty の複数アカウント](../../../../services/threat-detection.md#guardduty-multi-account): サービスごとの違いを確認します。
7. [マルチリージョンと緊急アクセス](../../../../services/identity-directory.md#idc-multi-region): 緊急用の経路の設計を押さえます。

## 覚える値 {#values}

| ポリシー | 付けられる数 | サイズ |
|---|---|---|
| SCP | 10 個 | 10,240 文字 |
| RCP | 5 個（`RCPFullAWSAccess` を含む） | 5,120 文字 |
| 宣言型ポリシー | 10 個 | 10,000 文字 |
| AI サービスのオプトアウト | 5 個 | 2,500 文字 |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| SCP を使えない | 機能セットとポリシータイプの有効化 |
| SCP が管理アカウントに効かない | 設計どおり。IAM で絞り、ワークロードを置かない |
| 外部の主体のアクセスを組織で拒否 | RCP |
| サービスリンクロールを含めて設定を維持 | 宣言型ポリシー |
| 不適合なリソースの作成を止めるコントロール | プロアクティブ（CloudFormation Hooks） |
| Control Tower に独自のテンプレートを足す | CfCT |
| Terraform でアカウントを発行 | AFT |
| Control Tower の外で変更した | ドリフト。更新か再登録で解消 |
| 別のリージョンの GuardDuty が見えない | リージョンごとに委任管理者を指定 |
| 誤ったバケットポリシーでロックアウト | `AssumeRoot` と `S3UnlockBucketPolicy` |
| ルートの特権タスクを絞る | `sts:TaskPolicyArn` |

## 引っかかりやすい点 {#traps}

- 委任管理者はメンバーアカウントなので SCP が効きます。
- SCP の拒否は IAM で上書きできません。SCP は許可も与えません。
- `AssumeRoot` はグローバルエンドポイントでは呼べず、ルートの認証情報でも呼べません。
- Inspector の抑制ルールは委任管理者だけが作れます。
- 緊急用の経路は、Identity Center に依存せず、定期的に動作を確認します。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [organizations 問1](../../exercises/organizations.md#q1) | 6.1.1 | 合併で引き継いだ組織に SCP を適用しようとしましたが、ポリシーの作成や適用の画面が使えません。こ… |
| [organizations 問2](../../exercises/organizations.md#q2) | 6.1.1 | 人事の部署ごとに OU を作っていた会社で、同じ部署の本番と開発に別々の SCP を適用できず困って… |
| [organizations 問3](../../exercises/organizations.md#q3) | 6.1.1, 6.1.3 | SCP で全リージョンの操作を東京だけに制限しました。監査で、管理アカウントの IAM ユーザーがオ… |
| [organizations 問4](../../exercises/organizations.md#q4) | 6.1.1 | Organizations のアカウントの組織設計で、AWS の推奨に合う分け方を確認します。セキュ… |
| [organizations 問5](../../exercises/organizations.md#q5) | 6.1.2 | 既存の組織に Control Tower を導入します。予防的、検出的、プロアクティブの 3 種類の… |
| [organizations 問6](../../exercises/organizations.md#q6) | 6.1.2 | Control Tower のランディングゾーンで、独自の SCP とテンプレートを追加で展開します… |
| [organizations 問7](../../exercises/organizations.md#q7) | 6.1.2 | Control Tower を導入済みの組織で、ある担当者が Organizations のコンソー… |
| [organizations 問8](../../exercises/organizations.md#q8) | 6.1.2 | 既存の 100 アカウントの組織に Control Tower を導入します。アカウントを作り直さず… |
| [organizations 問9](../../exercises/organizations.md#q9) | 6.1.3 | 組織の外のパートナーが、S3 バケットのポリシーの誤りで組織のデータを読めていました。再発を防ぐ統制… |
| [organizations 問10](../../exercises/organizations.md#q10) | 6.1.3 | 組織全体で VPC からインターネットへの直接の出入りをなくします。サービスリンクロールが作るリソー… |
| [organizations 問11](../../exercises/organizations.md#q11) | 6.1.3 | AWS の AI サービスに送ったコンテンツがサービス改善に使われないようにする要件があります。全ア… |
| [organizations 問12](../../exercises/organizations.md#q12) | 6.1.3 | 開発者の組織離脱を禁止し、CloudTrail の停止も全員に禁止します。さらに、S3 の HTTP… |
| [organizations 問13](../../exercises/organizations.md#q13) | 6.1.4 | 組織の GuardDuty を Audit アカウントで運用します。委任管理者を東京で指定しましたが… |
| [organizations 問14](../../exercises/organizations.md#q14) | 6.1.4 | セキュリティサービスの委任管理者を Audit アカウントにまとめました。ある SCP を組織のルー… |
| [organizations 問15](../../exercises/organizations.md#q15) | 6.1.4 | Inspector の抑制ルールを、組織全体で統一します。各メンバーのチームが個別に検出結果を抑制し… |
| [organizations 問16](../../exercises/organizations.md#q16) | 6.1.4 | 組織の Firewall Manager の管理を、ネットワークチームとセキュリティチームで分担しま… |
| [organizations 問17](../../exercises/organizations.md#q17) | 6.1.5 | 組織の新しいメンバーアカウントでは、ルートユーザーの長期の認証情報を持たせないことにしました。既存の… |
| [organizations 問18](../../exercises/organizations.md#q18) | 6.1.5 | メンバーアカウントの S3 バケットポリシーを誤り、すべての主体を拒否してしまいました。そのアカウン… |
| [organizations 問19](../../exercises/organizations.md#q19) | 6.1.5 | 委任管理者のロールが AssumeRoot を呼べますが、監査は「ルートの特権タスクのうち、S3 と… |
| [organizations 問20](../../exercises/organizations.md#q20) | 6.1.5 | IAM Identity Center に障害が起きたときにも、管理者がアカウントへ入れるように、緊… |

<!-- questions:end -->

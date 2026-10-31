# 分野3: CloudFormation、CDK、Terraform

運用の機能の選択と、失敗の切り分けを問います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [3.1.2](../../domain3.md#skill-3-1-2) | CloudFormation と CDK |
| [3.1.3](../../domain3.md#skill-3-1-3) | デプロイの問題の特定と修復 |
| [3.1.4](../../domain3.md#skill-3-1-4) | 複数リージョンと複数アカウントへの展開 |
| [3.1.6](../../domain3.md#skill-3-1-6) | Terraform と Git |

## 学習の順番 {#study-order}

1. [変更セット](../../../../services/iac.md#change-sets)、[ドリフト検出](../../../../services/iac.md#drift)と[スタックポリシー](../../../../services/iac.md#stack-policy): 更新の前と後で使う機能を区別します。
2. [リソースの属性: DeletionPolicy](../../../../services/iac.md#deletion-policy)、[CreationPolicy](../../../../services/iac.md#creation-policy)と[ヘルパースクリプト](../../../../services/iac.md#cfn-helpers): データの保護と起動の待機を確認します。
3. [CDK のコマンド](../../../../services/iac.md#cdk-cli)と[ブートストラップ](../../../../services/iac.md#cdk-bootstrap): CDK の流れを確認します。
4. [ロールバックの既定動作](../../../../services/iac.md#stack-rollback)、[よくある失敗と対処](../../../../services/iac.md#common-failures)と[機能の承認(capabilities)](../../../../services/iac.md#capabilities): エラーと対処を結びます。
5. [VPC の CIDR](../../../../services/network-connectivity.md#vpc-cidr)と[iam:PassRole](../../../../services/iam.md#passrole): サブネットのサイズと権限を確認します。
6. [StackSets の設定](../../../../services/iac.md#stacksets-settings)、[AWS Resource Access Manager](../../../../services/governance.md#ram)と[VPC サブネットの共有](../../../../services/governance.md#ram-vpc-sharing): 複数アカウントへの展開と共有を確認します。
7. [AWS Service Catalog](../../../../services/governance.md#service-catalog)と[デプロイ環境でコードリポジトリを使う](../../../../services/cicd.md#repositories): Terraform の製品と Git の使い方を確認します。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| サブネットで使えない IP | 5 個 | `/28` なら 11 個使える |
| ALB のサブネット | `/27` 以上で空き 8 個以上 | サイズは作成後に変えられない |
| S3 のネイティブロック | `use_lockfile = true` | Terraform 1.11 以降 |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 更新の影響を事前に確認する | 変更セット |
| 手動の変更を見つける | ドリフト検出 |
| 起動の完了を待つ | `cfn-signal` と `CreationPolicy` |
| `ROLLBACK_COMPLETE` | スタックを削除して作り直す |
| `UPDATE_ROLLBACK_FAILED` | `continue-update-rollback` |
| `InsufficientCapabilities` | `CAPABILITY_IAM` など |
| 新しいアカウントへ自動で展開する | サービスマネージドの StackSets |
| `Error acquiring the state lock` | 別の実行が終わるのを待つ。S3 のロックの動作 |

## 引っかかりやすい点 {#traps}

- スタックイベントは最初の失敗から読みます。
- セルフマネージドの StackSets に自動デプロイはありません。
- `InstanceLimitExceeded` はクォータ、`InsufficientInstanceCapacity` は容量です。
- CodeCommit は 2025年11月に一般提供へ戻りました。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [iac 問1](../../exercises/iac.md#q1) | 3.1.2 | 本番のスタックを更新する前に、どのリソースが置き換えになるのかを確認したいです。どの機能を使いますか… |
| [iac 問2](../../exercises/iac.md#q2) | 3.1.2 | 担当者がコンソールでセキュリティグループを手で変更したようです。テンプレートとの違いを見つけたいです… |
| [iac 問3](../../exercises/iac.md#q3) | 3.1.2 | RDS のスタックを削除しても、データを残したいです。またスタックの更新でもデータベースを置き換えさ… |
| [iac 問4](../../exercises/iac.md#q4) | 3.1.2 | EC2 のユーザーデータの処理が終わるまでスタックの作成を完了させたくありません。処理が失敗したら、… |
| [iac 問5](../../exercises/iac.md#q5) | 3.1.2 | cdk deploy がブートストラップのスタックがないという理由で失敗します。新しいリージョンへの… |
| [iac 問6](../../exercises/iac.md#q6) | 3.1.2 | CDK のコマンドと用途の組み合わせとして正しいものを選んでください。（2つ選択） |
| [iac 問7](../../exercises/iac.md#q7) | 3.1.3 | 初めて作るスタックが失敗し、ROLLBACK_COMPLETE になりました。テンプレートを直して更… |
| [iac 問8](../../exercises/iac.md#q8) | 3.1.3 | スタックの更新が失敗し、ロールバックも失敗して UPDATE_ROLLBACK_FAILED になり… |
| [iac 問9](../../exercises/iac.md#q9) | 3.1.3 | IAM ロールを含むテンプレートをデプロイすると InsufficientCapabilities … |
| [iac 問10](../../exercises/iac.md#q10) | 3.1.3 | /28 のサブネット 2 つに ALB を作ったところ、スケールの途中で IP が足りないというエラ… |
| [iac 問11](../../exercises/iac.md#q11) | 3.1.3 | EC2 の起動のエラーと原因の組み合わせとして正しいものを選んでください。（2つ選択） |
| [iac 問12](../../exercises/iac.md#q12) | 3.1.3 | CloudFormation で EC2 インスタンスプロファイルを指定するスタックが、権限のエラー… |
| [iac 問13](../../exercises/iac.md#q13) | 3.1.4 | 組織の全アカウントに監査用のロールを展開します。新しいアカウントにも自動で入れたいです。何をどう設定… |
| [iac 問14](../../exercises/iac.md#q14) | 3.1.4 | StackSets で 100 アカウントに展開します。一度に 10 アカウントずつ処理し、失敗が … |
| [iac 問15](../../exercises/iac.md#q15) | 3.1.4 | 組織の別のアカウントに、VPC のサブネットを共有します。オーナーと参加者の責任の説明として正しいも… |
| [iac 問16](../../exercises/iac.md#q16) | 3.1.4 | 次の課題と手段の組み合わせとして正しいものはどれですか。 |
| [iac 問17](../../exercises/iac.md#q17) | 3.1.6 | チームが Terraform を使い始め、2 人が同時に apply して状態ファイルが壊れそうにな… |
| [iac 問18](../../exercises/iac.md#q18) | 3.1.6 | Terraform のコマンドと用途の組み合わせとして正しいものはどれですか。 |
| [iac 問19](../../exercises/iac.md#q19) | 3.1.6 | Terraform の状態を保存する S3 バケットの設定として適切なものを選んでください。（2つ選… |
| [iac 問20](../../exercises/iac.md#q20) | 3.1.6 | Terraform の定義を Service Catalog の製品にしたいです。正しい説明はどれで… |
| [iac 問21](../../exercises/iac.md#q21) | 3.1.6 | IaC のコードの管理の説明として正しいものを選んでください。（2つ選択） |

<!-- questions:end -->

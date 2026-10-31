# 分野2: IaC と StackSets

ツールの選択と、テンプレートの機能で更新を安全にする方法を問います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [IaC の選択肢](../../domain2.md#t2-1-iac-options) | IaC の選択肢とツール、IaC テンプレートの作成とデプロイ |
| [変更管理](../../domain2.md#t2-1-change-management) | IaC の変更管理 |
| [StackSets](../../domain2.md#t2-1-stacksets) | StackSets の適用 |
| [再利用できる部品](../../domain2.md#t2-1-reusable) | 統制を組み込んだ再利用できるテンプレート |

## 学習の順番 {#study-order}

1. [どれを使うか](../../../../services/iac.md#choosing): CloudFormation、SAM、CDK の使い分けを確認します。
2. [UpdatePolicy](../../../../services/iac.md#update-policy): `CreationPolicy` と合わせ、シグナルを待つ更新を理解します。
3. [変更セット](../../../../services/iac.md#change-sets): パイプラインでの作成、承認、実行の流れを押さえます。
4. [スタックポリシー](../../../../services/iac.md#stack-policy): 更新の禁止と削除保護の違いを確認します。
5. [ロールバックトリガー](../../../../services/iac.md#rollback-triggers): アラームで戻す仕組みを覚えます。
6. [StackSets の設定](../../../../services/iac.md#stacksets-settings): 権限のモデルと、同時実行、失敗の許容数を確認します。
7. [ネストとエクスポートの比較](../../../../services/iac.md#nested-vs-exports): ネスト、エクスポート、モジュールの違いを整理します。

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| データベースの置き換えを見逃さない | 変更セットの `Replacement` |
| 重要なリソースの更新を禁止する | スタックポリシー |
| 更新の後のアラームで戻す | ロールバックトリガー |
| 1 アカウントずつ進めて最初の失敗で止める | 同時実行 1、失敗の許容数 0 |
| 新しいアカウントへ自動で配る | サービスマネージド権限と自動デプロイ |
| 利用者に下位の権限を与えない | Service Catalog の起動制約 |
| アプリのスタックの中に部品を入れる | CloudFormation モジュール |

## 引っかかりやすい点 {#traps}

- ドリフト検出は見つけるだけで、直しません。
- ネストされたスタックは別のスタックになり、アカウントをまたげません。
- `OUTDATED` は実行ロール、固定名の衝突、クォータを確認します。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [iac 問1](../../exercises/iac.md#q1) | IaC の選択肢 | プラットフォームチームが、50 個のサービスに同じ形の VPC、ALB、ECS サービスを提供します… |
| [iac 問2](../../exercises/iac.md#q2) | IaC の選択肢 | CloudFormation で作る Auto Scaling グループの更新で、次を満たします。新… |
| [iac 問3](../../exercises/iac.md#q3) | IaC の選択肢 | ある CloudFormation スタックで、(1) スタックの作成時に外部の SaaS の AP… |
| [iac 問4](../../exercises/iac.md#q4) | 変更管理 | 本番のスタックの更新は、影響の確認と責任者の承認の後に実行します。特に、データベースが置き換えられる… |
| [iac 問5](../../exercises/iac.md#q5) | 変更管理 | 本番のスタックに、次の 2 つの保護を入れます。(1) RDS のインスタンスの置き換えや削除を伴う… |
| [iac 問6](../../exercises/iac.md#q6) | 変更管理 | 担当者がコンソールからセキュリティグループを直接変更することがあり、次の更新で意図せず戻っています。… |
| [iac 問7](../../exercises/iac.md#q7) | StackSets | 組織の全アカウントに、監査用のロールを配ります。新しいアカウントが OU に入ると自動で作り、アカウ… |
| [iac 問8](../../exercises/iac.md#q8) | StackSets | StackSets で 200 アカウントの基盤を更新します。誤りがあっても影響を最小にしたいので、… |
| [iac 問9](../../exercises/iac.md#q9) | StackSets | StackSets の更新で、3 つのアカウントのスタックインスタンスが OUTDATED のまま残… |
| [iac 問10](../../exercises/iac.md#q10) | 再利用できる部品 | セキュリティチームは、暗号化とログ設定を組み込んだ S3 バケットの定義を各チームへ配ります。各チー… |
| [iac 問11](../../exercises/iac.md#q11) | 再利用できる部品 | 開発者に EC2 や IAM の権限を与えずに、承認済みの構成だけを自分で作らせます。インスタンスタ… |
| [iac 問12](../../exercises/iac.md#q12) | 再利用できる部品 | プラットフォームチームが、社内標準の暗号化、ログ、アラームを組み込んだ「標準の API」の部品を配り… |

<!-- questions:end -->

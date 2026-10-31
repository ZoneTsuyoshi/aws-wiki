# 分野1: CodePipeline と複数アカウント

パイプラインをどこに置き、何をきっかけに動かし、どこで人や AWS サービスの判定を挟むかを問います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [SDLC の概念とモデル](../../domain1.md#t1-1-sdlc) | SDLC の概念、フェーズ、モデル |
| [バージョン管理](../../domain1.md#t1-1-version-control) | バージョン管理とパイプラインの統合 |
| [単一アカウントと複数アカウント](../../domain1.md#t1-1-multi-account) | 単一、複数アカウントのパイプラインのパターン |
| [AWS サービスの呼び出し](../../domain1.md#t1-2-invoke-services) | パイプラインから AWS サービスを呼ぶ |

## 学習の順番 {#study-order}

1. [サービスの役割](../../../../services/cicd.md#overview): CI、継続的デリバリー、継続的デプロイの違いと、手動承認の位置を押さえます。
2. [複数環境への展開](../../../../services/cicd.md#multi-environment): ツール用アカウントから宛先のロールを引き受ける形と、リージョンごとのアーティファクトバケットを確認します。
3. [アカウントをまたぐ暗号化](../../../../services/kms.md#cross-account): カスタマー管理キーとキーポリシーが必要な理由を理解します。
4. [リポジトリからの起動](../../../../services/cicd.md#pipeline-triggers): V2 のフィルターでブランチ、タグ、ファイルパスを絞る方法を覚えます。
5. [アクションの設定](../../../../services/cicd.md#pipeline-actions): Lambda と Step Functions のアクションの結果の返し方を確認します。
6. [ステージ条件](../../../../services/cicd.md#stage-conditions): `CloudWatchAlarm` のルールとロールバックの指定を押さえます。

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 本番の前に人の確認が必須 | 継続的デリバリーで手動承認を置く |
| 別アカウントのアクションが成果物を読めない | カスタマー管理キー、キーポリシー、バケットポリシーを確認する |
| `AssumeRole` が拒否される | 宛先のロールの信頼ポリシーと、呼び出し側の許可を確認する |
| モノレポで一部のサービスだけ動かす | V2 のファイルパスのフィルター |
| 検証済みのものを本番へ出す | ビルドし直さず、同じ成果物を昇格する |
| Lambda アクションが完了しない | `PutJobSuccessResult` の呼び出しと権限を確認する |

## 引っかかりやすい点 {#traps}

- AWS 管理キーのポリシーは変更できないので、アカウントをまたぐ成果物には使えません。
- 別リージョンのアクションには、そのリージョンのアーティファクトバケットが必要です。
- Express ワークフローの実行時間は最大 5 分で、長いテストには使えません。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [pipelines 問1](../../exercises/pipelines.md#q1) | SDLC の概念とモデル | 金融系の社内システムでは、監査の要件として、本番への反映の前に変更管理の担当者が内容を確認して記録を… |
| [pipelines 問2](../../exercises/pipelines.md#q2) | SDLC の概念とモデル | あるチームは、コミットごとにビルドと単体テストを実行し、失敗をすぐに開発者へ返しています。ただし、成… |
| [pipelines 問3](../../exercises/pipelines.md#q3) | SDLC の概念とモデル, バージョン管理 | SaaS を運営するチームは、main にマージされた変更を、テストに通れば人の操作なしで本番へ出し… |
| [pipelines 問4](../../exercises/pipelines.md#q4) | 単一アカウントと複数アカウント | ツール用アカウントの CodePipeline から、本番アカウントの CloudFormation… |
| [pipelines 問5](../../exercises/pipelines.md#q5) | 単一アカウントと複数アカウント | ある組織は、開発、検証、本番のアカウントを分け、パイプラインも 1 か所で管理したいと考えています。… |
| [pipelines 問6](../../exercises/pipelines.md#q6) | 単一アカウントと複数アカウント | パイプライン用アカウントの CodePipeline から本番アカウントの CodeDeploy を… |
| [pipelines 問7](../../exercises/pipelines.md#q7) | バージョン管理 | 1 つの GitHub リポジトリに 12 個のマイクロサービスがあります。現在はどのディレクトリを… |
| [pipelines 問8](../../exercises/pipelines.md#q8) | バージョン管理 | リリースの運用を変更します。main へのマージでは検証環境まで進め、v1.2.0 のようなタグが付… |
| [pipelines 問9](../../exercises/pipelines.md#q9) | バージョン管理 | 組織の方針で、GitHub Enterprise Cloud のリポジトリと CodePipelin… |
| [pipelines 問10](../../exercises/pipelines.md#q10) | AWS サービスの呼び出し | パイプラインのテストステージで Lambda の呼び出しアクションを使い、デプロイした API を確… |
| [pipelines 問11](../../exercises/pipelines.md#q11) | AWS サービスの呼び出し | 本番ステージのデプロイの後、30 分間のアラームの状態を見て、問題があればそのステージをロールバック… |
| [pipelines 問12](../../exercises/pipelines.md#q12) | AWS サービスの呼び出し | 結合テストは、テストデータの投入、3 つの API の並列の検証、10 分ごとの結果の確認、最後の後… |

<!-- questions:end -->

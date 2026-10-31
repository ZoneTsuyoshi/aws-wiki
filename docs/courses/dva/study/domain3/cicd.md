# 分野3: CI/CD

分野3では、リポジトリの変更をパイプラインで本番まで運ぶ方法と、デプロイ戦略、ロールバックの選び方が問われます。デプロイやビルドが失敗したときの切り分けは[分野4の CI/CD](../domain4/cicd.md) で扱います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [3.1.1](../../domain3.md#skill-3-1-1) | パッケージの依存関係（CodeArtifact） |
| [3.1.2](../../domain3.md#skill-3-1-2) | CodeBuild でのイメージのビルド |
| [3.1.3](../../domain3.md#skill-3-1-3) | コードリポジトリの利用 |
| [3.2.1](../../domain3.md#skill-3-2-1) | CodeBuild でのテストの実行とレポート |
| [3.2.4](../../domain3.md#skill-3-2-4) | 環境の分け方（Amplify のブランチなど） |
| [3.3.4](../../domain3.md#skill-3-3-4) | CodeDeploy によるデプロイ |
| [3.3.5](../../domain3.md#skill-3-3-5) | CodePipeline によるオーケストレーション |
| [3.3.6](../../domain3.md#skill-3-3-6) | デプロイ戦略 |
| [3.3.7](../../domain3.md#skill-3-3-7) | ロールバック |
| [3.3.8](../../domain3.md#skill-3-3-8) | ブランチとタグ |

## 学習の順番 {#study-order}

1. [サービスの役割](../../../../services/cicd.md#overview)と[リポジトリ](../../../../services/cicd.md#repositories): 各サービスの担当と、ソースごとの接続方法を押さえます。
2. [ブランチとタグ](../../../../services/cicd.md#branches-tags): 環境を分けるものと、リリースを固定するものを区別します。
3. [buildspec のセクション](../../../../services/cicd.md#buildspec-sections)と[テストレポート](../../../../services/cicd.md#build-reports): ビルドとテストの書き方を確認します。社内パッケージの共有は [CodeArtifact](../../../../services/cicd.md#codeartifact) で補います。
4. [ステージとアクション](../../../../services/cicd.md#pipeline-structure)、[パイプラインタイプ](../../../../services/cicd.md#pipeline-types)、[リポジトリからの起動](../../../../services/cicd.md#pipeline-triggers): V2 でできることとトリガーの絞り方を覚えます。
5. [手動承認](../../../../services/cicd.md#manual-approval)、[複数環境への展開](../../../../services/cicd.md#multi-environment)、[環境の管理](../../../../services/cicd.md#app-environments)、[Amplify](../../../../services/cicd.md#amplify): 同じ成果物を環境ごとに進める形をつかみます。
6. [AppSpec](../../../../services/cicd.md#appspec)と[ライフサイクルイベント](../../../../services/cicd.md#lifecycle-hooks): EC2、Lambda、ECS で使えるフックの違いを覚えます。
7. [デプロイ設定](../../../../services/cicd.md#deployment-configs)と[デプロイ戦略の比較](../../../../services/cicd.md#deployment-strategies): 設定名と戦略を対応させます。
8. [CodeDeploy のロールバック](../../../../services/cicd.md#codedeploy-rollback)、[ステージ条件](../../../../services/cicd.md#stage-conditions)、[ロールバックの方法](../../../../services/cicd.md#rollback): サービスごとの戻し方を比べます。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| CodeBuild のタイムアウト | 既定 60 分、5〜2,160 分 | 長い統合テストは `timeoutInMinutes` を増やす |
| テストレポート | 30 日で期限切れ、1 プロジェクトに 5 グループ | 残すなら生データを S3 へエクスポート |
| 手動承認 | 7 日 | 応答がなければ失敗扱い |
| CodeDeploy の既定の設定（EC2、オンプレミス） | `OneAtATime` | 未指定なら 1 台ずつ |
| AppSpec のスクリプト | 既定、上限ともイベントあたり 3,600 秒 | 超えるとそのインスタンスは失敗 |
| Lambda、ECS のフックの報告 | 1 時間以内 | 報告がなければデプロイは失敗 |
| 同じデプロイグループの同時デプロイ | 1 | 並行して実行できない |
| 元のインスタンスの終了待ち | 最大 48 時間 | `terminationWaitTimeInMinutes` |
| `QUEUED`、`PARALLEL` の同時実行 | 50 | 既定は `SUPERSEDED` |
| Amplify のブランチ | 50（増やせない） | Web プレビューも含む |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| GitHub で `v*` のタグを打ったときだけ本番へリリース | CodeConnections で接続し、V2 パイプラインのトリガーで Git タグを絞る |
| `services/orders/**` の変更だけで起動 | V2 のプッシュトリガーでブランチとファイルパスを指定する |
| 本番の前に人が確認 | Approval アクションと SNS の通知。承認者に `codepipeline:PutApprovalResult` |
| テストしたものと同じものを本番へ | 成果物を 1 回だけビルドし、環境ごとのステージへ進める。差はパラメータやパイプライン変数で渡す |
| Lambda の新版に 10% 流し、5 分後に残りを移す | `CodeDeployDefault.LambdaCanary10Percent5Minutes` |
| 毎分 10% ずつ移す | `CodeDeployDefault.LambdaLinear10PercentEvery1Minute`、ECS なら `ECSLinear10PercentEvery1Minutes` |
| ECS で本番の前にテストトラフィックで検証 | CodeDeploy なら `AfterAllowTestTraffic` のフック。AWS が勧める ECS 組み込みのブルー/グリーンならライフサイクルフック |
| エラーが増えたらデプロイを自動で戻す | デプロイグループに CloudWatch アラームを設定し、`DEPLOYMENT_STOP_ON_ALARM` のロールバックを有効にする |
| デプロイの後の 5XX でパイプラインのステージを戻す | `Prod` の On Success に `CloudWatchAlarm` のルールを置き、結果を `Rollback` にする（V2） |
| ブランチごとの Web 環境、PR ごとの確認 URL | Amplify のブランチデプロイ、Web プレビュー |

## 引っかかりやすい点 {#traps}

- **アラームで止まっても戻らない**: アラームが発火すると `Stopped` になるだけです。ロールバックを別に有効にします。
- **修正したのに `ApplicationStop` で失敗する**: このイベントは前回成功したデプロイの AppSpec のスクリプトを実行します。旧版のスクリプトが壊れていると、新版を直しても失敗します。初回デプロイでは動きません。
- **CodeDeploy のロールバックで ID が変わる**: 以前のリビジョンを新しいデプロイとして配布するので、新しいデプロイ ID が振られます。
- **`docker build` が `Cannot connect to the Docker daemon` で失敗する**: CodeBuild の `privilegedMode` が無効です。
- **`PARALLEL` で戻せない**: `PARALLEL` モードでは、ステージのロールバックも `Rollback` の結果を持つ条件も使えません。
- **古い教材との違い**: CodeCommit は 2025 年 11 月に一般提供へ戻りました。ECS のブルー/グリーンは、現在は CodeDeploy がなくても実行できます。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [cicd 問1](../../exercises/cicd.md#q1) | 3.1.1 | CodeBuild のプロジェクトで、buildspec.yml の APP_ENV が stagi… |
| [cicd 問4](../../exercises/cicd.md#q4) | 3.1.2 | Docker イメージをビルドする CodeBuild プロジェクトで、Cannot connect… |
| [cicd 問5](../../exercises/cicd.md#q5) | 3.3.5 | CodeBuild のプロジェクトのタイムアウトについて、正しいものはどれですか。（2つ選択） |
| [cicd 問6](../../exercises/cicd.md#q6) | 3.3.5, 3.1.3 | CodeBuild の Webhook を設定します。main へのプッシュで動かし、ただしファイル… |
| [cicd 問8](../../exercises/cicd.md#q8) | 3.2.1 | Python の 3.11 と 3.12 のすべての組み合わせでテストするバッチビルドを、最も簡潔に… |
| [cicd 問9](../../exercises/cicd.md#q9) | 3.3.4 | CodeDeploy の EC2 向けインプレースデプロイで、配置先に以前のデプロイに含まれないファ… |
| [cicd 問11](../../exercises/cicd.md#q11) | 3.3.4 | CodeDeploy の EC2 / オンプレミスのインプレースデプロイで、AppSpec にスクリ… |
| [cicd 問12](../../exercises/cicd.md#q12) | 3.3.4 | CodeDeploy の ECS のデプロイで、テストリスナーが置き換えのタスクセットへトラフィック… |
| [cicd 問13](../../exercises/cicd.md#q13) | 3.3.4 | 10 台の EC2 に CodeDeploy でデプロイします。最小正常ホストを FLEET_PER… |
| [cicd 問14](../../exercises/cicd.md#q14) | 3.3.7 | CodeDeploy のデプロイグループに CloudWatch アラームを関連付けました。アラーム… |
| [cicd 問15](../../exercises/cicd.md#q15) | 3.3.6 | CodeDeploy の定義済みの設定名として、実在するものはどれですか。（2つ選択） |
| [cicd 問16](../../exercises/cicd.md#q16) | 3.3.5, 3.3.8 | Git のタグ v* のプッシュでだけ本番パイプラインを起動し、新しい実行が古い実行を置き換えず順に… |
| [cicd 問17](../../exercises/cicd.md#q17) | 3.3.5 | CodeBuild のアクションがエクスポートした IMAGE_TAG を、次の Deploy アク… |
| [cicd 問18](../../exercises/cicd.md#q18) | 3.3.7 | 本番ステージのデプロイの後で 5XX のアラームが発火したら、前回成功した実行の版へ自動で戻します。… |
| [cicd 問19](../../exercises/cicd.md#q19) | 3.1.1 | CodeArtifact で、社内パッケージと同じ名前の公開パッケージが取り込まれるのを防ぎたいと考… |
| [cicd 問20](../../exercises/cicd.md#q20) | 3.2.4 | Amplify Hosting を使っているチームで、PR ごとの確認環境を増やしたところ、新しいブ… |
| [cicd 問21](../../exercises/cicd.md#q21) | 3.1.3 | CloudFormation で CodeConnections の GitHub 接続を作成し、C… |
| [cicd 問22](../../exercises/cicd.md#q22) | 3.1.3, 3.3.8 | ビルド中に git describe --tags でバージョン番号を作ります。GitHub の接続… |
| [cicd 問23](../../exercises/cicd.md#q23) | 3.3.8 | 本番パイプラインは、V2 のトリガーで v* のタグのプッシュだけを契機に起動します。開発者が gi… |

<!-- questions:end -->

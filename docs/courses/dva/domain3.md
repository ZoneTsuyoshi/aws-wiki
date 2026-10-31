# 分野3: テストとデプロイ

C03 の配点は **22%** です。パッケージ準備、テスト、CI/CD サービスによるデプロイを扱います。C02 の「デプロイ」から、テストの比重が明確になりました。

サービスごとに順を追って学ぶときは、[サービス別の学習ページ](study/domain3/index.md)から始めます。

この分野に限らず、コース全体で使うサービスは[サービス一覧](services.md)から確認できます。

## タスク 3.1: デプロイする成果物を準備する {#task-3-1}

### 3.1.1 コードモジュールの依存関係 {#skill-3-1-1}

ライブラリは Lambda レイヤーやコンテナイメージにまとめ、環境ごとに変わる値はコードの外に出します。

詳細: [Lambda のパッケージング](../../services/lambda.md#packaging)、[プロジェクト構成](../../services/iac.md#project-structure)、[環境変数](../../services/lambda.md#environment-variables)

### 3.1.2 コンテナイメージの作成と管理 {#skill-3-1-2}

Dockerfile でイメージを作り、ECR に push します。タグのイミュータブル設定で上書きを防ぎ、ライフサイクルポリシーで古いイメージを削除します。

詳細: [Dockerfile](../../services/containers.md#dockerfile)、[ECR](../../services/containers.md#ecr)、[イメージのタグ](../../services/containers.md#image-tags)、[ライフサイクルポリシー](../../services/containers.md#ecr-lifecycle)

### 3.1.3 コードリポジトリの利用 {#skill-3-1-3}

リポジトリへの push やマージをパイプラインの起点にします。

詳細: [リポジトリ](../../services/cicd.md#repositories)

### 3.1.4 環境ごとの設定管理 {#skill-3-1-4}

| 手段 | 向いているもの |
|---|---|
| AppConfig | 機能フラグ、検証しながら段階的に反映する設定 |
| Parameter Store | 環境ごとの設定値 |
| Secrets Manager | シークレット |
| API Gateway のステージ変数 | ステージごとの接続先 |
| Lambda のエイリアスと環境変数 | バージョンごとの切り替え |

詳細: [環境別の設定](../../services/secrets.md#environment-config)、[AppConfig](../../services/secrets.md#appconfig)、[ステージ変数](../../services/api-gateway.md#stage-variables)

### 3.1.5 API Gateway の機能 {#skill-3-1-5}

ステージごとに URL が分かれます。カスタムドメインとエンドポイントタイプの違いも押さえます。

詳細: [ステージ](../../services/api-gateway.md#stages)、[エンドポイントタイプ](../../services/api-gateway.md#endpoint-types)、[カスタムドメイン](../../services/api-gateway.md#custom-domains)

## タスク 3.2: テストを実装し自動化する {#task-3-2}

### 3.2.1 テストの開発と検証 {#skill-3-2-1}

`sam local invoke` や `sam validate`、CDK の assertions でテストします。CloudFormation テンプレートは事前に検証し、変更セットで影響を確認します。

詳細: [テスト](../../services/iac.md#testing)、[IaC の検証](../../services/iac.md#validate-iac)、[CDK のテスト](../../services/iac.md#cdk-testing)

### 3.2.2 外部依存のモック {#skill-3-2-2}

API Gateway の Mock 統合を使うと、バックエンドなしで固定の応答を返せます。

詳細: [Mock 統合](../../services/api-gateway.md#mock-integration)

### 3.2.3 テストイベントの作成 {#skill-3-2-3}

Lambda や API Gateway に渡す JSON を用意します。`sam local generate-event` でひな形を作れます。

詳細: [テストイベント](../../services/iac.md#test-events)、[Lambda のテスト](../../services/lambda.md#testing)、[API Gateway のテスト](../../services/api-gateway.md#test-endpoints)

### 3.2.4 アプリケーション環境の作成 {#skill-3-2-4}

Lambda エイリアス、コンテナイメージのタグ、Amplify のブランチ、API Gateway のステージで環境を分けます。

!!! note "AWS Copilot について"
    試験ガイドには載っていますが、AWS Copilot CLI は 2026年6月12日にサポートが終了しています。

詳細: [Lambda エイリアス](../../services/lambda.md#alias-environments)、[イメージのタグ](../../services/containers.md#environments-image-tags)、[Amplify](../../services/cicd.md#amplify)、[Copilot](../../services/containers.md#copilot)、[環境の管理](../../services/cicd.md#app-environments)

### 3.2.5 AI によるテストの自動化 {#skill-3-2-5}

テストの生成、実行、結果の分析に AI ツールを使います。実際に確認できる機能と一般的な活用方法を区別して、解説ページにまとめています。

詳細: [AI によるテスト](../../services/ai.md#ai-testing)

## タスク 3.3: CI/CD サービスでデプロイする {#task-3-3}

[![CI/CD パイプライン](../../assets/diagrams/cicd-pipeline.png)](../../assets/diagrams/cicd-pipeline.png)

### 3.3.1 Lambda のパッケージング {#skill-3-3-1}

.zip、コンテナイメージ、レイヤーの違いを押さえます。

詳細: [パッケージング](../../services/lambda.md#packaging)

### 3.3.2 コンテナアプリのデプロイ {#skill-3-3-2}

ECS のタスク定義、EKS のマニフェスト、Fargate、ローリング更新を押さえます。タスクロールはアプリの権限、タスク実行ロールはイメージの取得やログ出力の権限です。ECS はローリング更新に加えて、ブルー/グリーン、線形、カナリアも CodeDeploy なしで実行できます。

詳細: [タスク定義](../../services/containers.md#task-definition)、[Fargate と EC2](../../services/containers.md#fargate-vs-ec2)、[ローリング更新](../../services/containers.md#rolling-update)、[EKS のマニフェスト](../../services/containers.md#eks-manifests)

### 3.3.3 IaC テンプレート {#skill-3-3-3}

CloudFormation のセクションと組み込み関数、SAM の変換を押さえます。

詳細: [CloudFormation テンプレート](../../services/iac.md#cloudformation-template)、[SAM テンプレート](../../services/iac.md#sam-template)

### 3.3.4 CodeDeploy によるデプロイ {#skill-3-3-4}

`appspec` にライフサイクルフックを書きます。EC2、Lambda、ECS で使えるフックが異なります。

ECS のブルー/グリーンについて、AWS は現在 CodeDeploy ではなく ECS 組み込みのデプロイを勧めています。CodeDeploy の方式も引き続き使えるので、両方を区別します。

詳細: [CodeDeploy](../../services/cicd.md#codedeploy)、[ECS のブルー/グリーン](../../services/containers.md#ecs-blue-green)

### 3.3.5 CodePipeline によるオーケストレーション {#skill-3-3-5}

リポジトリの変更を起点に、ビルド、テスト、手動承認、本番へと進めます。

詳細: [CodePipeline](../../services/cicd.md#codepipeline)、[トリガー](../../services/cicd.md#pipeline-triggers)、[複数環境](../../services/cicd.md#multi-environment)

### 3.3.6 デプロイ戦略 {#skill-3-3-6}

| 戦略 | 特徴 |
|---|---|
| 一括 | 速いが、失敗の影響が全体に及ぶ |
| ローリング | 少しずつ置き換える。容量が一時的に減ることがある |
| ブルー/グリーン | 新環境を用意して切り替える。すぐ戻せる |
| カナリア | 一部のトラフィックで試してから全体に広げる |
| 線形 | 一定の割合ずつ広げる |

詳細: [デプロイ戦略](../../services/cicd.md#deployment-strategies)、[デプロイ設定](../../services/cicd.md#deployment-configs)、[Elastic Beanstalk](../../services/ec2-beanstalk.md#deployment-policies)

### 3.3.7 ロールバック {#skill-3-3-7}

CodeDeploy はアラームと連動して自動で戻せます。CloudFormation はスタックの更新に失敗すると元に戻します。

詳細: [ロールバック](../../services/cicd.md#rollback)、[CodeDeploy](../../services/cicd.md#codedeploy-rollback)、[スタック](../../services/iac.md#stack-rollback)、[ロールバックトリガー](../../services/iac.md#rollback-triggers)

### 3.3.8 ブランチとタグ {#skill-3-3-8}

ブランチで環境や作業を分け、タグでリリースを記録します。

詳細: [ブランチとタグ](../../services/cicd.md#branches-tags)

### 3.3.9 AI による CI/CD の支援 {#skill-3-3-9}

承認の判断材料の作成、環境の用意、デプロイ後の検証に AI ツールを使います。

詳細: [AI と CI/CD](../../services/ai.md#ai-cicd)

## 確認問題 {#self-check}

まず基本を確認する問題です。本番形式の問題は[問題集](exercises/index.md)にあります（[CI/CD](exercises/cicd.md)、[IaC と CLI](exercises/iac.md)、[コンテナ](exercises/containers.md) など）。

??? question "問1: Lambda の新バージョンに、まず 10% のトラフィックだけを流します。何を使いますか？"
    エイリアスの加重と CodeDeploy のカナリア設定です。SAM なら `DeploymentPreference` で指定できます。

??? question "問2: ECS タスクが ECR からイメージを取得できません。どのロールを確認しますか？"
    タスク実行ロールです。アプリが AWS API を呼ぶときの権限はタスクロールです。

??? question "問3: バックエンドの完成前に、フロントエンド開発者が API を呼べるようにしたいです。どうしますか？"
    API Gateway の Mock 統合で固定の応答を返します。

??? question "問4: 本番のスタック更新前に、どのリソースが置き換えられるか確認したいです。何を使いますか？"
    CloudFormation の変更セットです。

??? question "問5: デプロイ直後にエラー率が上がったら自動で戻したいです。何を設定しますか？"
    CodeDeploy のデプロイグループに CloudWatch アラームと自動ロールバックを設定します。ECS 組み込みのデプロイなら、サービスの `deploymentConfiguration` の `alarms` に、アラーム名とロールバックを設定します。

??? question "問6: ECR に古いイメージがたまっています。自動で削除するには？"
    ECR のライフサイクルポリシーを設定します。

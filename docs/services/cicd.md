# CI/CD（CodeBuild / CodeDeploy / CodePipeline）

[:material-sprout: CLF](../courses/clf/services.md){ .exam-badge .exam-foundational } [:material-certificate: SAA](../courses/saa/services.md){ .exam-badge .exam-associate } [:material-certificate: DVA](../courses/dva/services.md){ .exam-badge .exam-associate } [:material-certificate: DEA](../courses/dea/services.md){ .exam-badge .exam-associate } [:material-certificate: MLA](../courses/mla/services.md){ .exam-badge .exam-associate } [:material-star-circle: SAP](../courses/sap/services.md){ .exam-badge .exam-professional } [:material-star-circle: DOP](../courses/dop/services.md){ .exam-badge .exam-professional } [:material-star-circle: AIP](../courses/aip/services.md){ .exam-badge .exam-professional } [:material-certificate: SOA](../courses/soa/services.md){ .exam-badge .exam-associate .exam-badge--related }

コードの変更をビルド、テスト、デプロイまで自動で進める AWS の開発者ツール群です。リリースを繰り返し安全に行いたいときに、パイプライン、デプロイ戦略、ロールバックを組み合わせて使います。

[![CI/CD パイプラインの全体像](../assets/diagrams/cicd-pipeline.png)](../assets/diagrams/cicd-pipeline.png)

## サービスの役割 {#overview}

| サービス | 役割 | 設定の中心 |
|---|---|---|
| CodePipeline | 各工程をつなぐオーケストレーター | ステージとアクション |
| CodeBuild | コンパイル、テスト、イメージ作成 | `buildspec.yml` |
| CodeDeploy | EC2、オンプレミス、Lambda、ECS へのデプロイ | `appspec.yml`、デプロイ設定 |
| CodeArtifact | npm や pip などの私設パッケージリポジトリ | ドメインとリポジトリ |
| Amplify Hosting | Web アプリのブランチ単位のビルドとホスティング | `amplify.yml`、ブランチ設定 |

CloudFormation や SAM によるデプロイは [IaC](iac.md) で説明します。

## ソース管理 {#source-control}

### デプロイ環境でコードリポジトリを使う {#repositories}

[:material-certificate: MLA](../courses/mla/services.md){ .exam-badge .exam-associate }

リポジトリを「デプロイの正」にします。手元で作った成果物ではなく、コミットから作った成果物を配布すれば、本番で動くものを必ずコミットまでたどれます。

CodePipeline のソースにできる代表的なものは次のとおりです。

| ソース | 接続方法 | 変更の検知 |
|---|---|---|
| GitHub、GitLab、Bitbucket | CodeConnections の接続（`CodeStarSourceConnection` アクション） | Webhook。ブランチ、タグ、PR などのトリガーを設定可能 |
| CodeCommit | IAM | EventBridge ルール |
| S3 | IAM | EventBridge ルール。バージョニングが必要 |
| ECR | IAM | EventBridge ルール |

### CodeCommit の現状 {#codecommit-status}

[:material-certificate: MLA](../courses/mla/services.md){ .exam-badge .exam-associate } [:material-star-circle: SAP](../courses/sap/services.md){ .exam-badge .exam-professional }

CodeCommit は 2024 年に新規受付を止めましたが、**2025 年 11 月に一般提供へ戻り、新規利用者も使えるようになりました**。「CodeCommit は新規利用できない」という古い記述は現在は誤りです。なお、DVA-C02 と DVA-C03 の試験ガイドの対象サービス一覧に CodeCommit は載っていません（一覧は網羅的ではないとされています）。

IAM、VPC エンドポイント、CloudTrail と統合できるため、AWS の中でソースを管理したい場合の選択肢です。Git リポジトリなので、頻繁に変わる大きなファイル、データベース、監査ログの置き場には向きません。

**古い情報に注意**: 2024 年以降の教材には「CodeCommit は使えない」と書かれていることがあります。2025 年 11 月の一般提供への復帰で、この記述は古くなりました。

### ブランチとタグでバージョンとリリースを管理する {#branches-tags}

ブランチは「作業の流れ」、タグ（ラベル）は「特定の時点につける不変の名前」です。

| 使うもの | 用途 | 例 |
|---|---|---|
| ブランチ | 環境や開発の流れを分ける | `main` は本番、`develop` は結合テスト、`feature/*` は機能開発 |
| Git タグ | リリース版を固定する | `v1.4.2` |
| プルリクエスト | マージ前のレビューとテスト | PR で CodeBuild のテストを実行 |
| コンテナイメージタグ | デプロイするイメージを指定する | `1.4.2`、コミット SHA |
| Lambda のバージョンとエイリアス | 不変の版と、それを指す名前 | バージョン `7`、エイリアス `prod` |

```bash
git tag -a v1.4.2 -m "Release 1.4.2"
git push origin v1.4.2
```

パイプラインの起動条件に Git タグを指定すれば、タグを打ったときだけ本番へのリリースを始められます。

### コミットでビルド・テスト・デプロイを起動する {#commit-triggers}

流れは「コミットをプッシュする → トリガーが発火する → CodePipeline がその版を取得する → CodeBuild がビルドしてテストする → デプロイする」です。人がコマンドを実行する必要はありません。

CodeBuild だけで済む場合は、プロジェクトに Webhook を設定してプッシュや PR で直接ビルドを始めることもできます。承認や複数環境への展開が必要になったら CodePipeline を使います。

## CodeBuild {#codebuild}

[:material-sprout: CLF](../courses/clf/services.md){ .exam-badge .exam-foundational } [:material-certificate: DVA](../courses/dva/services.md){ .exam-badge .exam-associate } [:material-certificate: DEA](../courses/dea/services.md){ .exam-badge .exam-associate } [:material-certificate: MLA](../courses/mla/services.md){ .exam-badge .exam-associate } [:material-star-circle: SAP](../courses/sap/services.md){ .exam-badge .exam-professional } [:material-star-circle: DOP](../courses/dop/services.md){ .exam-badge .exam-professional } [:material-star-circle: AIP](../courses/aip/services.md){ .exam-badge .exam-professional }

フルマネージドのビルドサービスです。ビルドごとに新しい環境を用意するので、ビルドサーバーの管理が不要です。ビルド時の権限はプロジェクトのサービスロールで決まります。

### buildspec の構成 {#buildspec}

既定ではソースのルートにある `buildspec.yml` を読みます。別の名前や場所も指定できます。

```yaml
version: 0.2

env:
  variables:
    APP_ENV: "staging"
  parameter-store:
    API_URL: "/myapp/staging/api-url"
  secrets-manager:
    DB_PASSWORD: "myapp/staging/db:password"
  exported-variables:
    - IMAGE_TAG

phases:
  install:
    runtime-versions:
      python: 3.12
    commands:
      - pip install -r requirements.txt
  pre_build:
    commands:
      - pytest tests/unit --junitxml=reports/unit.xml
      - export IMAGE_TAG=$CODEBUILD_RESOLVED_SOURCE_VERSION
  build:
    commands:
      - sam build
    finally:
      - echo "build フェーズの後片付け"
  post_build:
    commands:
      - sam package --s3-bucket "$ARTIFACT_BUCKET" --output-template-file packaged.yaml

reports:
  unit-tests:
    files:
      - "unit.xml"
    base-directory: reports
    file-format: JUNITXML

artifacts:
  files:
    - packaged.yaml

cache:
  paths:
    - "/root/.cache/pip/**/*"
```

### buildspec のセクション {#buildspec-sections}

| セクション | 必須 | 役割と注意 |
|---|---|---|
| `version` | 必須 | `0.2` を推奨。`0.1` は各コマンドが別のシェルで動くので `cd` や `export` が次のコマンドに残らない |
| `run-as` | 任意 | 実行する Linux ユーザー。全体と `phases` ごとに書け、フェーズの指定が優先 |
| `env.shell` | 任意 | 使うシェル。Linux は `bash` など、Windows は `powershell.exe` など |
| `env.variables` | 任意 | 平文の環境変数。機密は入れない |
| `env.parameter-store` | 任意 | `変数名: パラメータ名`。ロールに `ssm:GetParameters` が必要 |
| `env.secrets-manager` | 任意 | `変数名: シークレットID:JSONキー:ステージ:バージョンID` |
| `env.exported-variables` | 任意 | CodePipeline の後続アクションへ渡す変数 |
| `env.git-credential-helper` | 任意 | `yes` で Git 認証情報ヘルパーを使う。公開リポジトリの Webhook 起動では使えない |
| `proxy` | 任意 | 明示的なプロキシ環境での設定。`upload-artifacts`、`logs` の既定は `no` |
| `batch` | 任意 | バッチビルドの設定 |
| `phases` | 必須 | `install`、`pre_build`、`build`、`post_build`。名前は変更できない |
| `reports` | 任意 | テストとカバレッジのレポート |
| `artifacts` | 任意 | 出力するファイル |
| `cache` | 任意 | キャッシュするパス |

`env` の値は、同じ名前なら**ビルド開始時の指定、プロジェクトの定義、buildspec の順に優先**されます。`CODEBUILD_` で始まる名前は予約されています。

**例**: `--environment-variables-override` でビルド開始時に `APP_ENV=prod` を渡すと、buildspec の `APP_ENV: staging` より優先されます。

エクスポートできるのは `install` から `post_build` までに更新した値です。`AWS_` で始まる変数や、プロジェクトに定義したシークレットはエクスポートできません。

#### secrets-manager の指定 {#buildspec-secrets}

```yaml
env:
  secrets-manager:
    DB_PASSWORD: "prod/db:password"
    OTHER_ACCOUNT: "arn:aws:secretsmanager:ap-northeast-1:111122223333:secret:prod/api-AbCdEf:key"
```

JSON キーを省くとシークレット全体を取得します。別のアカウントのシークレットは ARN で指定します。`version-stage` と `version-id` は同時に指定しません。

**症状**: サービスロールに読み取り権限がないと、ビルドは値を取得できずに権限エラーで失敗します。カスタマー管理キーで暗号化しているなら `kms:Decrypt` も確認します。

#### on-failure と finally {#buildspec-on-failure}

| `on-failure` の値 | 動作 |
|---|---|
| `ABORT` | ビルドを中止 |
| `CONTINUE` | 次のフェーズへ |
| `RETRY` | 最大 3 回再試行 |
| `RETRY-<回数>` | 指定回数(0〜100)再試行 |
| `RETRY-<正規表現>` | メッセージが一致すれば最大 3 回再試行 |
| `RETRY-<回数>-<正規表現>` | 両方を指定 |

CodeBuild 提供のイメージの EC2 コンピュートでだけ動き、Lambda コンピュートとリザーブドキャパシティでは使えません。`finally` は `commands` が失敗しても動きます。

#### artifacts と cache のキー {#buildspec-artifacts-cache}

| キー | 意味 |
|---|---|
| `artifacts.files` | 必須。`**/*` で配下すべて |
| `artifacts.name` | 成果物の名前 |
| `artifacts.base-directory` | 基準ディレクトリ |
| `artifacts.discard-paths` | `yes` でディレクトリ構造を捨てる。既定は `no` |
| `artifacts.exclude-paths` | `base-directory` からの相対で除外 |
| `artifacts.enable-symlinks` | `ZIP` の出力でシンボリックリンクを残す |
| `artifacts.s3-prefix` | S3 の接頭辞 |
| `artifacts.secondary-artifacts` | 複数の成果物。プロジェクトの識別子と一致させる |
| `cache.paths` | キャッシュするパス |

**例**: `files: ["**/*"]`、`base-directory: dist` なら `dist` の中身だけが、`dist/` を付けずに ZIP に入ります。

#### batch {#buildspec-batch}

| キー | 動作 |
|---|---|
| `batch.fast-fail` | 失敗したときに残りのタスクを止めるか |
| `batch.build-graph` | 依存関係のあるビルドの集まり |
| `batch.build-list` | 並列に動かす一覧 |
| `batch.build-matrix` | 変数の組み合わせごとにビルド |
| `batch.build-fanout` | テストを分割して並列実行 |

**例**: Python 3.11 と 3.12 の両方でテストするなら `build-matrix`、A のビルドの後で B を動かすなら `build-graph` の `depend-on` を使います。

### ビルドフェーズ {#build-phases}

ビルドは次の順に進みます。

```mermaid
flowchart TD
    A["SUBMITTED / QUEUED"] --> B[PROVISIONING]
    B --> C[DOWNLOAD_SOURCE]
    C --> D["INSTALL (install)"]
    D --> E["PRE_BUILD (pre_build)"]
    E --> F["BUILD (build)"]
    F --> G["POST_BUILD (post_build)"]
    G --> H[UPLOAD_ARTIFACTS]
    H --> I[FINALIZING]
    I --> J[COMPLETED]
```

| 設定 | 動作 |
|---|---|
| `install` | パッケージの導入に使う。`runtime-versions` で実行環境の版を指定 |
| `pre_build` | ECR へのログインや依存関係の準備 |
| `build` | ビルドとテストの本体 |
| `post_build` | イメージのプッシュや通知など |
| `finally` | 同じフェーズの `commands` が失敗しても実行される |
| `on-failure` | フェーズ失敗時の動作。`ABORT`、`CONTINUE`、`RETRY` など（CodeBuild 提供のイメージの EC2 コンピュートのみ。Lambda コンピュートとリザーブドキャパシティでは使えない） |

`UPLOAD_ARTIFACTS` は `BUILD` が失敗しても試行されます。`post_build` などで成否を判定したいときは、環境変数 `CODEBUILD_BUILD_SUCCEEDING`（`1` は成功、`0` は失敗）を見ます。

### プロジェクトの設定 {#codebuild-project}

| 設定 | 既定値、範囲 | 説明 |
|---|---|---|
| `environment.type` | `LINUX_CONTAINER`、`ARM_CONTAINER`、`LINUX_LAMBDA_CONTAINER` など | OS とコンピュートの種類 |
| `environment.computeType` | `BUILD_GENERAL1_SMALL`〜`2XLARGE`、`BUILD_LAMBDA_1GB`〜`10GB` | CPU とメモリ |
| `environment.image` | | ビルドイメージ |
| `environment.imagePullCredentialsType` | `CODEBUILD`、`SERVICE_ROLE` | 独自の ECR イメージなら `SERVICE_ROLE` にしてロールに権限を与える |
| `environment.privilegedMode` | 既定 `false` | Docker デーモンを動かすために必要 |
| `timeoutInMinutes` | 既定 60、5〜2160 | ビルドのタイムアウト |
| `queuedTimeoutInMinutes` | 5〜480 | キューで待てる時間 |
| `serviceRole` | 必須 | ビルドが使うロール |
| `vpcConfig` | 任意 | VPC、サブネット、セキュリティグループ |
| `cache` | 既定 `NO_CACHE` | `S3`、`LOCAL` |
| `logsConfig` | | CloudWatch Logs、S3 |
| `concurrentBuildLimit` | 任意 | プロジェクトの同時ビルド数 |

| コンピュート | 特徴 | 注意 |
|---|---|---|
| EC2 | 柔軟。特権モードや長いビルドに向く | 起動はやや遅い |
| Lambda | 起動が速い | `on-failure` が使えない。リザーブドキャパシティも同様 |

**例**: 90 分かかる統合テストは、`timeoutInMinutes` を 120 にします。既定の 60 分のままだと、`TIMED_OUT` で終わります。上限は 2,160 分(36 時間)です。

**症状**: 特権モードが無効で `docker build` を動かすと、`Cannot connect to the Docker daemon` になります。

#### VPC の設定 {#codebuild-vpc}

CodeBuild は既定では VPC の中のリソースに届きません。RDS にアクセスするテストなら `vpcConfig` を指定します。

**落とし穴**: サブネットはプライベートにして、NAT ゲートウェイか VPC エンドポイントを用意します。これがないと、ソースのダウンロードや `pip install` が失敗します。

#### Webhook とフィルターグループ {#codebuild-webhook}

GitHub などのイベントでビルドを始めます。**1 つのグループの中のフィルターは AND、グループどうしは OR** です。

| フィルター | パターン | 例 |
|---|---|---|
| `EVENT` | カンマ区切りのイベント | `PUSH`、`PULL_REQUEST_CREATED`、`PULL_REQUEST_UPDATED`、`PULL_REQUEST_MERGED`、`RELEASED` など |
| `HEAD_REF` | 正規表現 | `^refs/heads/main$`、`^refs/tags/v.*` |
| `BASE_REF` | 正規表現 | PR の宛先。`^refs/heads/main$` |
| `FILE_PATH` | 正規表現 | `^services/orders/.*` |
| `ACTOR_ACCOUNT_ID` | 正規表現 | 起動できるユーザー |
| `COMMIT_MESSAGE` | 正規表現 | `\[skip\]` |

`excludeMatchedPattern: true` で除外になります。パターンは RE2 で、先読み、後読み、後方参照は使えません。

```json
{"filterGroups": [[
  {"type": "EVENT", "pattern": "PUSH"},
  {"type": "HEAD_REF", "pattern": "^refs/heads/main$"},
  {"type": "FILE_PATH", "pattern": "^docs/.*", "excludeMatchedPattern": true}
]]}
```

`main` へのプッシュで動かし、ファイルパスが `^docs/.*` に一致するイベントは起動しません。`docs/` とそれ以外が混ざるプッシュの扱いは公式の説明にないので、実際に確認します。

**落とし穴**: `HEAD_REF` の `main` と書くと、`refs/heads/main-old` にも一致します。`^refs/heads/main$` と書きます。

#### 組み込みの環境変数 {#codebuild-built-in-vars}

| 変数 | 内容 |
|---|---|
| `CODEBUILD_BUILD_ID` | ビルド ID |
| `CODEBUILD_BUILD_SUCCEEDING` | `1` は成功、`0` は失敗 |
| `CODEBUILD_RESOLVED_SOURCE_VERSION` | コミット ID。`DOWNLOAD_SOURCE` の後で使える |
| `CODEBUILD_SOURCE_VERSION` | 指定したソースのバージョン |
| `CODEBUILD_SRC_DIR` | ソースのディレクトリ |
| `CODEBUILD_WEBHOOK_EVENT` | Webhook のイベント |

### 環境変数とシークレット {#build-env}

| 定義先 | 向いているもの | 注意 |
|---|---|---|
| `env.variables` | 秘密でない設定値 | buildspec にそのまま残る |
| `env.parameter-store` | Parameter Store の値 | サービスロールに `ssm:GetParameters` が必要 |
| `env.secrets-manager` | パスワードや API キー | 形式は `シークレットID:JSONキー:ステージ:バージョン`。サービスロールに読み取り権限が必要 |
| `env.exported-variables` | 後続のパイプラインアクションへ渡す値 | `install` から `post_build` の間に更新できる |

Parameter Store と Secrets Manager から取得した値はログでマスクされます。ただしマスクは保存値との完全一致です。Base64 にするなど値を加工して出力すると隠れません。

### アーティファクト {#build-artifacts}

`artifacts` で、ビルドの成果物として保存するファイルを指定します。

| キー | 意味 |
|---|---|
| `files` | 出力するファイル。`**/*` で配下すべて |
| `base-directory` | 基準ディレクトリ |
| `discard-paths` | `yes` でディレクトリ構造を捨てる |
| `secondary-artifacts` | 複数の成果物を分けて出力する |

CodePipeline では、この成果物がパイプラインの S3 バケットを経由して次のアクションに渡ります。

### キャッシュ {#build-cache}

| 種類 | 保存先 | 向いている場面 |
|---|---|---|
| S3 キャッシュ | S3 バケット | 複数のビルドホストで共有したいとき |
| ローカル: ソース | ビルドホスト | Git メタデータの再利用 |
| ローカル: Docker レイヤー | ビルドホスト | イメージのビルド短縮（Linux のみ、特権モードが必要） |
| ローカル: カスタム | ビルドホスト | buildspec の `cache.paths` で指定した依存関係 |

Docker イメージをビルドするプロジェクトでは特権モード（privileged）を有効にします。

### テストレポート {#build-reports}

`reports` にレポートグループ名とファイルを書くと、テスト結果をコンソールで確認できます。グループは事前に作らなくても自動で作成されます。

- テスト形式: JUnit XML、Cucumber JSON、NUnit、TestNG、Visual Studio TRX
- コードカバレッジレポートも作成可能
- レポートは作成から 30 日で期限切れ。残すには生データを S3 へエクスポートする

レポートの設定値です。

| キー | 値 |
|---|---|
| `files` | 必須 |
| `base-directory` | 基準 |
| `discard-paths` | `yes` で構造を捨てる |
| `file-format` | テストは `JUNITXML`、`CUCUMBERJSON`、`NUNITXML`、`NUNIT3XML`、`TESTNGXML`、`VISUALSTUDIOTRX`。カバレッジは `CLOVERXML`、`COBERTURAXML`、`JACOCOXML`、`SIMPLECOV` |

レポートグループは名前を書くと `プロジェクト名-グループ名` で作られます。1 プロジェクトに 5 グループまでです。

### ログ {#build-logs}

ビルドログは CloudWatch Logs、S3、またはその両方に出力できます。失敗時は、コンソールのフェーズ詳細でどのフェーズが落ちたかを確認し、そのログを読みます。

VPC 内でビルドすると、インターネットへ出る経路がなければ依存関係の取得に失敗します。NAT ゲートウェイや VPC エンドポイントを確認します。

## CodeDeploy {#codedeploy}

[:material-certificate: DVA](../courses/dva/services.md){ .exam-badge .exam-associate } [:material-certificate: DEA](../courses/dea/services.md){ .exam-badge .exam-associate } [:material-certificate: MLA](../courses/mla/services.md){ .exam-badge .exam-associate } [:material-star-circle: SAP](../courses/sap/services.md){ .exam-badge .exam-professional } [:material-star-circle: DOP](../courses/dop/services.md){ .exam-badge .exam-professional } [:material-star-circle: AIP](../courses/aip/services.md){ .exam-badge .exam-professional }

アプリケーションのリビジョンを、EC2、オンプレミス、Lambda、ECS へ配布するサービスです。

### 構成要素 {#codedeploy-concepts}

| 用語 | 意味 |
|---|---|
| アプリケーション | デプロイの入れ物。コンピューティングプラットフォームを持つ |
| デプロイグループ | 配布先の集まり。EC2 はタグや Auto Scaling グループ、ECS はサービス、Lambda は関数で指定 |
| リビジョン | 配布する内容。EC2 は S3 や GitHub のバンドルと AppSpec、Lambda と ECS は AppSpec |
| デプロイ設定 | 進め方（一度に何台か、どの速度でトラフィックを移すか） |
| デプロイタイプ | インプレース（EC2 とオンプレミスのみ）または Blue/Green |

**Blue/Green の設定**(`blueGreenDeploymentConfiguration`)です。

| 設定 | 意味 |
|---|---|
| `deploymentReadyOption.actionOnTimeout` | `CONTINUE_DEPLOYMENT` か `STOP_DEPLOYMENT`。切り替えを手動で待つときは後者 |
| `terminateBlueInstancesOnDeploymentSuccess.action` | `TERMINATE` か `KEEP_ALIVE` |
| `terminationWaitTimeInMinutes` | 元のインスタンスを終了するまでの待ち時間。上限は 48 時間 |

### AppSpec ファイル {#appspec}

プラットフォームごとに中身が違います。EC2 とオンプレミスでは `appspec.yml` という名前でリビジョンのルートに置きます。

**EC2 / オンプレミス**: ファイルの配置先とスクリプトを指定します。

```yaml
version: 0.0
os: linux
files:
  - source: /build
    destination: /var/www/app
hooks:
  ApplicationStop:
    - location: scripts/stop.sh
      timeout: 60
      runas: root
  AfterInstall:
    - location: scripts/configure.sh
  ApplicationStart:
    - location: scripts/start.sh
  ValidateService:
    - location: scripts/healthcheck.sh
      timeout: 120
```

`timeout` の既定値と上限はライフサイクルイベントごとに 3,600 秒です。

**Lambda**: どのエイリアスをどの版からどの版へ移すかを指定し、フックは Lambda 関数で書きます。

```yaml
version: 0.0
Resources:
  - MyFunction:
      Type: AWS::Lambda::Function
      Properties:
        Name: "my-function"
        Alias: "live"
        CurrentVersion: "6"
        TargetVersion: "7"
Hooks:
  - BeforeAllowTraffic: "PreTrafficCheck"
  - AfterAllowTraffic: "PostTrafficCheck"
```

**ECS**: 新しいタスク定義と、トラフィックを受けるコンテナを指定します。

```yaml
version: 0.0
Resources:
  - TargetService:
      Type: AWS::ECS::Service
      Properties:
        TaskDefinition: "<タスク定義の ARN>"
        LoadBalancerInfo:
          ContainerName: "web"
          ContainerPort: 8080
Hooks:
  - AfterAllowTestTraffic: "RunSmokeTest"
```

Lambda と ECS のフック関数は、結果を CodeDeploy に報告します。1 時間以内に報告がないとデプロイは失敗します。

```python
import boto3

codedeploy = boto3.client("codedeploy")

def handler(event, context):
    status = "Succeeded" if run_checks() else "Failed"
    codedeploy.put_lifecycle_event_hook_execution_status(
        deploymentId=event["DeploymentId"],
        lifecycleEventHookExecutionId=event["LifecycleEventHookExecutionId"],
        status=status,
    )
```

#### AppSpec の項目(EC2 / オンプレミス) {#appspec-ec2}

| セクション | 項目 | 内容 |
|---|---|---|
| `version` | `0.0` | 固定 |
| `os` | `linux`、`windows` | |
| `files` | `source`、`destination` | 配置するファイル |
| `file_exists_behavior` | `DISALLOW`、`OVERWRITE`、`RETAIN` | 既存ファイルの扱い |
| `permissions` | `object`、`except`、`owner`、`group`、`mode`、`acls`、`context`、`type` | 配置後の権限。Linux 系のみ |
| `hooks` | `location`、`timeout`、`runas` | スクリプト |

```yaml
permissions:
  - object: /var/www/app
    pattern: "**"
    owner: www-data
    mode: 755
    type:
      - file
```

| `file_exists_behavior` | 動作 |
|---|---|
| `DISALLOW` | デプロイが失敗する |
| `OVERWRITE` | リビジョンの版で上書き |
| `RETAIN` | 既存のファイルを残す |

`--file-exists-behavior` のエラーは、以前のデプロイに含まれないファイルが配置先にあるときに起きます。

**落とし穴**: 1 つのイベントのスクリプトの合計が 3,600 秒を超えると、そのインスタンスのデプロイは失敗します。

#### AppSpec の項目(ECS) {#appspec-ecs}

| 項目 | 必須 | 内容 |
|---|---|---|
| `TaskDefinition` | 必須 | タスク定義の ARN |
| `LoadBalancerInfo.ContainerName` | 必須 | トラフィックを受けるコンテナ |
| `LoadBalancerInfo.ContainerPort` | 必須 | ポート |
| `PlatformVersion` | 任意 | Fargate のプラットフォームバージョン |
| `NetworkConfiguration.AwsvpcConfiguration` | 任意 | サブネット、セキュリティグループ、パブリック IP |
| `CapacityProviderStrategy` | 任意 | キャパシティプロバイダー |

Lambda の AppSpec は `Name`、`Alias`、`CurrentVersion`、`TargetVersion` の 4 つです。

### ライフサイクルイベントの順序 {#lifecycle-hooks}

**EC2 / オンプレミスのインプレース**（ロードバランサーがある場合）

太字以外は AppSpec にスクリプトを書けません。ロードバランサーがなければ `Traffic` が付くイベントは実行されません。

| 順 | イベント | 用途 |
|---|---|---|
| 1 | Start | |
| 2 | **BeforeBlockTraffic** | ロードバランサーから外す前の処理 |
| 3 | BlockTraffic | 登録解除 |
| 4 | **AfterBlockTraffic** | 外した後の処理 |
| 5 | **ApplicationStop** | 旧版の停止 |
| 6 | DownloadBundle | リビジョンを一時領域へ取得 |
| 7 | **BeforeInstall** | バックアップや復号 |
| 8 | Install | ファイルを配置 |
| 9 | **AfterInstall** | 設定や権限の変更 |
| 10 | **ApplicationStart** | サービスの起動 |
| 11 | **ValidateService** | デプロイ成功の検証 |
| 12 | **BeforeAllowTraffic** | ロードバランサーへ戻す前の処理 |
| 13 | AllowTraffic | 登録 |
| 14 | **AfterAllowTraffic** | 戻した後の処理 |
| 15 | End | |

`ApplicationStop`、`BeforeBlockTraffic`、`AfterBlockTraffic` は、**前回成功したデプロイの AppSpec** のスクリプトを実行します。そのため初回デプロイでは `ApplicationStop` は動きません。旧版のスクリプトが壊れていると、新版を修正してもここで失敗します。

**EC2 の Blue/Green**: 置き換え先インスタンスで `ApplicationStop` から `AfterAllowTraffic` までを実行し、その後で元のインスタンスで `BeforeBlockTraffic`、`BlockTraffic`、`AfterBlockTraffic` を実行します。

**Lambda**

```mermaid
flowchart TD
    A[Start] --> B["BeforeAllowTraffic (フック可)"]
    B --> C[AllowTraffic]
    C --> D["AfterAllowTraffic (フック可)"]
    D --> E[End]
```

**ECS**

```mermaid
flowchart TD
    A[Start] --> B["BeforeInstall (フック可)"]
    B --> C[Install]
    C --> D["AfterInstall (フック可)"]
    D --> E[TestTraffic]
    E --> F["AfterAllowTestTraffic (フック可)"]
    F --> G["BeforeAllowTraffic (フック可)"]
    G --> H[AllowTraffic]
    H --> I["AfterAllowTraffic (フック可)"]
    I --> J[End]
```

ECS では、テストリスナーへ流したトラフィックで検証してから本番トラフィックを移せます。

なお、AWS は現在、ECS のブルー/グリーンには CodeDeploy ではなく [ECS 組み込みのデプロイ](containers.md#ecs-blue-green) を勧めています。

### デプロイ設定 {#deployment-configs}

| プラットフォーム | 定義済みの設定 | 動作 |
|---|---|---|
| EC2 / オンプレミス | `CodeDeployDefault.AllAtOnce` | できるだけ多くの台へ同時に配布 |
| | `CodeDeployDefault.HalfAtATime` | 最大半数ずつ |
| | `CodeDeployDefault.OneAtATime` | 1 台ずつ。未指定時の既定 |
| Lambda | `CodeDeployDefault.LambdaCanary10Percent5Minutes` | 10% を移し、5 分後に残り 90%（10、15、30 分版もある） |
| | `CodeDeployDefault.LambdaLinear10PercentEvery1Minute` | 毎分 10% ずつ（2、3、10 分間隔版もある） |
| | `CodeDeployDefault.LambdaAllAtOnce` | 一度にすべて |
| ECS | `CodeDeployDefault.ECSCanary10Percent5Minutes` | 10% を移し、5 分後に残り 90%（15 分版もある） |
| | `CodeDeployDefault.ECSLinear10PercentEvery1Minutes` | 毎分 10% ずつ（3 分間隔版もある） |
| | `CodeDeployDefault.ECSAllAtOnce` | 一度にすべて |

Lambda と ECS のカナリアや線形は独自の設定も作成できます。EC2 は最小正常インスタンス数を指定して独自設定を作ります。Network Load Balancer を使う ECS では `ECSAllAtOnce` のみ使えます。

**定義済みの設定の一覧**です。

| プラットフォーム | 名前 |
|---|---|
| Lambda のカナリア | `LambdaCanary10Percent5Minutes`、`10Minutes`、`15Minutes`、`30Minutes` |
| Lambda の線形 | `LambdaLinear10PercentEvery1Minute`、`2Minutes`、`3Minutes`、`10Minutes` |
| ECS のカナリア | `ECSCanary10Percent5Minutes`、`15Minutes` |
| ECS の線形 | `ECSLinear10PercentEvery1Minutes`、`3Minutes` |

名前の頭には `CodeDeployDefault.` が付きます。ECS の 1 分の線形だけ `Minutes` と複数形です。

#### 最小正常ホスト {#minimum-healthy-hosts}

EC2 の設定は `minimumHealthyHosts` の `type`(`HOST_COUNT` か `FLEET_PERCENT`)と `value` で決まります。

| 定義済みの設定 | 最小正常ホスト | 成功の条件 |
|---|---|---|
| `AllAtOnce` | 0 | 1 台以上に成功 |
| `HalfAtATime` | 50% | 半数以上(端数切り上げ)に成功 |
| `OneAtATime` | 1 | 全台に成功。ただし最後の 1 台だけは失敗しても全体は成功 |

```bash
aws deploy create-deployment-config \
  --deployment-config-name ThreeQuarters \
  --minimum-healthy-hosts type=FLEET_PERCENT,value=75
```

**計算例**: 10 台で `FLEET_PERCENT` が 85 なら、更新中の 1 台がオフラインで正常は 90% です。ここで 1 台でも失敗すると、失敗の 1 台とオフラインの 1 台で 80% になり、85% を下回るので全体が失敗します。

**落とし穴**: 値が 0 でも、最低 1 台の成功は必要です。Blue/Green では、この値は置き換え先の環境に適用されます。ただし、元のインスタンスの登録解除が 1 台でも失敗すると、全体が失敗になります。

### CodeDeploy のロールバック {#codedeploy-rollback}

ロールバックは、以前のリビジョンを**新しいデプロイとして**配布する処理です。新しいデプロイ ID が振られます。

自動ロールバックはデプロイグループまたはデプロイで設定します。

- デプロイが失敗したとき
- 指定した CloudWatch アラームのしきい値を超えたとき

手動の場合は、以前のリビジョンを指定して新規にデプロイします。

#### ロールバックとアラームの設定 {#codedeploy-rollback-settings}

```bash
aws deploy update-deployment-group \
  --application-name web --current-deployment-group-name prod \
  --auto-rollback-configuration enabled=true,events=DEPLOYMENT_FAILURE,DEPLOYMENT_STOP_ON_ALARM \
  --alarm-configuration enabled=true,ignorePollAlarmFailure=false,alarms=[{name=web-5xx}]
```

| 項目 | 内容 |
|---|---|
| `DEPLOYMENT_FAILURE` | 失敗したら戻す |
| `DEPLOYMENT_STOP_ON_ALARM` | アラームで止まったら戻す |
| `DEPLOYMENT_STOP_ON_REQUEST` | 手動で止めたら戻す |
| `ignorePollAlarmFailure` | アラームの状態を取得できなくても続ける。既定は `false` |

アラームが発火するとデプロイは `Stopped` になります。ロールバックを別に有効にしないと、**止まるだけで戻りません**。

**ロールバック時の既存ファイル**: エージェントは、前回のデプロイで入れたファイルを消します。それ以外のファイルが配置先にあれば、失敗、上書き、保持のいずれかになります。

### CodeDeploy エージェント {#codedeploy-agent}

エージェントが必要なのは EC2 とオンプレミスだけです。Lambda と ECS では不要です。

- インスタンスに CodeDeploy エージェントをインストールし、起動しておく
- インスタンスプロファイルに、リビジョンがある S3 などへのアクセス権を付ける
- エージェントは HTTPS（443 番）で外向きに通信する

| ログ（Linux） | 内容 |
|---|---|
| `/var/log/aws/codedeploy-agent/codedeploy-agent.log` | エージェント自体の動作 |
| `/opt/codedeploy-agent/deployment-root/<グループID>/<デプロイID>/logs/scripts.log` | フックスクリプトの出力 |
| `/opt/codedeploy-agent/deployment-root/deployment-logs/codedeploy-agent-deployments.log` | デプロイの記録 |

エージェントの主な設定は `/etc/codedeploy-agent/conf/codedeployagent.yml` にあります。`:verbose:` はデバッグログの出力で、既定は `false` です。

Auto Scaling と組み合わせると、新しいインスタンスへ自動でデプロイします。同じデプロイグループに同時に実行できるデプロイは 1 つです。

## CodePipeline {#codepipeline}

[:material-sprout: CLF](../courses/clf/services.md){ .exam-badge .exam-foundational } [:material-certificate: DVA](../courses/dva/services.md){ .exam-badge .exam-associate } [:material-certificate: DEA](../courses/dea/services.md){ .exam-badge .exam-associate } [:material-certificate: MLA](../courses/mla/services.md){ .exam-badge .exam-associate } [:material-star-circle: SAP](../courses/sap/services.md){ .exam-badge .exam-professional } [:material-star-circle: DOP](../courses/dop/services.md){ .exam-badge .exam-professional } [:material-star-circle: AIP](../courses/aip/services.md){ .exam-badge .exam-professional }

ソースから本番までの流れを定義し、自動で進めるサービスです。自身はビルドや配布を行わず、CodeBuild や CodeDeploy などを呼び出します。

### ステージとアクション {#pipeline-structure}

| 用語 | 意味 |
|---|---|
| ステージ | 環境や工程の単位。1 つのステージで同時に処理される実行は 1 つ |
| アクション | ステージ内の処理。種類は Source、Build、Test、Deploy、Approval、Invoke など |
| `runOrder` | 同じ値なら並列、違う値なら順に実行 |
| アーティファクト | アクション間で受け渡すファイル。S3 のアーティファクトバケットを経由 |
| 遷移 | ステージ間のつなぎ目。無効にすると次へ進まない |
| 変数 | アクションの出力を後続で参照する。CodeBuild の `exported-variables` もこれで渡す |

複数のリリースが同時に来たときの動きは実行モードで決まります。

| 実行モード | 動作 | パイプラインタイプ |
|---|---|---|
| `SUPERSEDED` | 待っている古い実行を新しい実行が置き換える | V1、V2 |
| `QUEUED` | 到着順に 1 つずつ処理 | V2 のみ |
| `PARALLEL` | 実行どうしが独立して同時に動く（ステージのロールバックは不可） | V2 のみ |

### パイプラインタイプ {#pipeline-types}

| 機能 | V1 | V2 |
|---|---|---|
| アクションレベルの変数 | 可 | 可 |
| パイプラインレベルの変数 | 不可 | 可 |
| `QUEUED`、`PARALLEL` モード | 不可 | 可 |
| ステージのロールバック | 不可 | 可 |
| ステージ条件 | 不可 | 可 |
| Git タグ、PR、ブランチ、パスのフィルター | 不可 | 可 |
| Commands アクション | 不可 | 可 |
| ソースリビジョンの上書き | 不可 | 可 |

既定の実行モードは `SUPERSEDED` です。`QUEUED` と `PARALLEL` の同時実行は 50 までです。

### アクションの設定 {#pipeline-actions}

```json
{
  "name": "Build",
  "actionTypeId": {"category": "Build", "owner": "AWS", "provider": "CodeBuild", "version": "1"},
  "runOrder": 1,
  "namespace": "BuildVariables",
  "inputArtifacts": [{"name": "SourceOutput"}],
  "outputArtifacts": [{"name": "BuildOutput"}],
  "configuration": {
    "ProjectName": "orders",
    "EnvironmentVariables": "[{\"name\":\"COMMIT\",\"value\":\"#{SourceVariables.CommitId}\",\"type\":\"PLAINTEXT\"}]"
  }
}
```

| 項目 | 意味 |
|---|---|
| `category` | `Source`、`Build`、`Test`、`Deploy`、`Approval`、`Invoke` |
| `owner` | `AWS`、`ThirdParty`、`Custom` |
| `provider` | `CodeBuild`、`CodeDeploy`、`CloudFormation`、`Lambda`、`S3` など |
| `runOrder` | 同じ値は並列 |
| `namespace` | 変数を参照するときの名前 |
| `inputArtifacts`、`outputArtifacts` | 名前で受け渡す。入力名は前のアクションの出力名と一致させる |
| `region`、`roleArn` | 別リージョン、別アカウント |

| アクション | タイムアウト |
|---|---|
| CodeBuild | 36 時間 |
| CodeDeploy | 5 日 |
| CloudFormation | 3 日 |
| Lambda の呼び出し | 24 時間 |
| Step Functions | 7 日 |
| 手動承認 | 7 日 |

**落とし穴**: CodeBuild のアクションに複数の入力を渡すなら `PrimarySource` が必要です。buildspec はこの入力から探します。CodeDeploy のアクションには `appspec.yml` を含む出力を渡します。入力名の誤りはパイプラインの作成か実行で失敗します。

### 変数 {#pipeline-variables}

| 種類 | 書き方 | 例 |
|---|---|---|
| アクション出力 | `#{名前空間.キー}` | `#{SourceVariables.CommitId}` |
| CodeBuild のエクスポート | `#{名前空間.変数名}` | `#{BuildVariables.IMAGE_TAG}` |
| パイプラインレベル | `#{variables.名前}` | `#{variables.Stage}` |
| 実行 ID | `#{codepipeline.PipelineExecutionId}` | |

**例**: `Source` の `namespace` を `SourceVariables` とすると、次の承認アクションの `CustomData` に `#{SourceVariables.CommitId}` を入れて、確認するコミットを示せます。

### CodeConnections の接続 {#codeconnections}

CodeConnections は、AWS のサービスと外部の Git リポジトリをつなぐ機能です。接続は ARN を持つ AWS リソースで、CodePipeline や CodeBuild などに渡して使います。

2024年3月29日に AWS CodeStar Connections から改称しました。古い `codestar-connections` の接続も引き続き使えます。

```mermaid
flowchart TD
    A["接続を作る"] --> B["外部サービス側で認可し、AWS のアプリをインストール"]
    B --> C["接続が AVAILABLE になる"]
    C --> D["CodePipeline などに接続の ARN を指定"]
    D --> E["コードの変更でパイプラインが起動"]
```

| 項目 | 内容 |
|---|---|
| 対応先 | GitHub.com、GitHub Enterprise Cloud と Server、GitLab.com と自己管理、Bitbucket Cloud、Azure DevOps |
| 自社環境に置く Git | GitHub Enterprise Server や自己管理の GitLab は、先に「ホスト」を作る |
| 状態 | CLI や CloudFormation で作ると `PENDING`。コンソールで認可を完了すると `AVAILABLE` |
| 利用の権限 | `codeconnections:UseConnection`。CodePipeline のサービスロールなどに付ける |
| 接続数の上限 | アカウントあたり既定で 250（リージョンごと、引き上げ可能） |
| 名前の長さ | 32 文字まで |
| ホスト数の上限 | アカウントあたり 50 |

**何がうれしいか**: 個人のアクセストークンをパラメータやシークレットに置かず、テンプレートには接続の ARN だけを書けます。CodeBuild、CodeDeploy のアプリケーション、CodePipeline で、接続へのアクセスを同じ方法で管理できます。

```yaml
# CodePipeline のソースアクションの例
ActionTypeId:
  Category: Source
  Owner: AWS
  Provider: CodeStarSourceConnection
  Version: "1"
Configuration:
  ConnectionArn: arn:aws:codeconnections:ap-northeast-1:111122223333:connection/aEXAMPLE-8aad-4d5d-8878-dfcab0bc441f
  FullRepositoryId: my-org/my-app
  BranchName: main
```

改称後も、CodePipeline のアクション名は `CodeStarSourceConnection` のままです。

**設定を誤ったときの症状**:

| 症状 | 原因 | 対処 |
|---|---|---|
| CloudFormation で接続を作ったのに、パイプラインのソースが使えない | 接続が `PENDING` のまま | コンソールで保留中の接続を更新し、認可を完了する |
| サービスロールで接続を使えない | `UseConnection` の許可がない | サービスロールに許可を足し、`Resource` に接続の ARN を指定する |
| IAM ポリシーを書いたのに拒否される | ポリシーのプレフィックスと接続の ARN が合っていない | `codeconnections` の接続には `codeconnections:` を、古い接続には `codestar-connections:` を使う |

### リポジトリからの起動 {#pipeline-triggers}

GitHub、GitLab、Bitbucket などは **CodeConnections** の接続で連携します（旧称 CodeStar Connections）。シークレットをテンプレートに書かず、接続の ARN を参照できる点が利点です。CLI で作った接続は保留状態なので、コンソールで認可を完了させます。

トリガーのフィルターは V2 パイプラインで設定します。

| イベント | フィルターできる項目 |
|---|---|
| プッシュ | Git タグ、ブランチ、ブランチとファイルパス |
| プルリクエスト | ブランチ、ブランチとファイルパス |

たとえば、`release/**` へのプッシュと、`services/orders/**` の変更だけで起動する設定ができます。

フィルターの値は glob 形式で、`includes` と `excludes` を書けます。

```yaml
triggers:
  - providerType: CodeStarSourceConnection
    gitConfiguration:
      sourceActionName: Source
      push:
        - branches:
            includes: ["release/**"]
          filePaths:
            includes: ["services/orders/**"]
            excludes: ["**/*.md"]
```

プッシュのトリガーは**プッシュ先のブランチ**のコミットを使います。PR のトリガーは**PR の元のブランチ**のコミットを使います。

アクションの `BranchName` は 1 つのブランチだけです。複数のブランチはトリガーで指定します。ポーリング(`PollForSourceChanges`)のパイプラインはリージョンあたり 300 までで、イベント方式が勧められています。

### 手動承認 {#manual-approval}

Approval アクションを置くと、そこでパイプラインが止まります。

- 承認すると次へ進む
- 却下、または **7 日以内に応答がないと**アクション失敗と同じ扱いになる
- 同じリージョンの SNS トピックへ通知し、確認用 URL とコメントを付けられる
- 承認者には `codepipeline:PutApprovalResult` の権限が必要

**手動承認の設定**: 設定項目は、SNS トピックの ARN、`CustomData`(コメント)、`ExternalEntityLink`(確認用 URL)です。承認アクションの中で `#{...}` の変数を使えます。

### 複数環境への展開 {#multi-environment}

同じ成果物を、環境ごとのステージへ順に進めます。ステージごとにビルドし直すと、テストしたものと本番のものが変わるおそれがあるためです。

```mermaid
flowchart TD
    A["Source: main へのプッシュ"] --> B["Build: ビルドと単体テスト"]
    B --> C["Dev: デプロイ"]
    C --> D["Staging: デプロイと結合テスト"]
    D --> E["Approval: 手動承認"]
    E --> F["Prod: カナリアでデプロイ"]
```

| 要件 | 方法 |
|---|---|
| 環境ごとの設定を変える | CloudFormation のパラメータ、パイプライン変数 |
| 別アカウントへデプロイ | 別アカウントの IAM ロールを引き受け、アーティファクトをカスタマー管理 KMS キーで暗号化 |
| 別リージョンへデプロイ | アクションにリージョンを指定。リージョンごとにアーティファクトバケットが必要 |
| 条件を満たしたときだけ進める | ステージ条件（CloudWatch アラームなどのルール） |

### ステージのロールバック {#pipeline-rollback}

CodePipeline は、以前に成功した実行の版を使ってステージを戻せます。

| 方法 | 内容 |
|---|---|
| 手動 | コンソールまたは `RollbackStage` API |
| 失敗時に自動 | ステージの On Failure 条件で結果を Rollback にする |
| 成功後の確認で戻す | On Success 条件のルールで結果を Rollback にする |

### ステージ条件 {#stage-conditions}

| 条件 | タイミング | 結果 |
|---|---|---|
| Entry | ステージに入る前 | `Fail`、`Skip` |
| On Failure | ステージが失敗したとき | `Rollback` |
| On Success | ステージが成功したとき | `Rollback`、`Fail` |

| ルール | 確認すること |
|---|---|
| `CloudWatchAlarm` | アラームの状態 |
| `DeploymentWindow` | 配置を許す時間帯(cron) |
| `LambdaInvoke` | 関数の判定 |
| `VariableCheck` | 変数の値 |
| `CodeBuild` | CodeBuild のビルド結果 |
| `Commands` | コマンドの結果 |

**例**: `Prod` ステージの On Success に `CloudWatchAlarm` のルールを置きます。デプロイの後に 5XX のアラームが `ALARM` になれば、前回成功した実行の版へ戻します。`PARALLEL` モードでは、ステージのロールバックも Rollback の結果を持つ条件も使えません。

ロールバックの実行は新しい実行として記録され、履歴には `rollback` の種類で表示されます。

## CodeArtifact {#codeartifact}

[:material-certificate: DVA](../courses/dva/services.md){ .exam-badge .exam-associate } [:material-certificate: MLA](../courses/mla/services.md){ .exam-badge .exam-associate } [:material-star-circle: DOP](../courses/dop/services.md){ .exam-badge .exam-professional } [:material-star-circle: AIP](../courses/aip/services.md){ .exam-badge .exam-professional }

npm、pip、Maven、NuGet などのパッケージを保管する私設リポジトリです。社内ライブラリの共有や、公開パッケージの取得元を一本化したいときに使います。

| 用語 | 意味 |
|---|---|
| ドメイン | リポジトリをまとめる単位。組織で 1 つが推奨 |
| リポジトリ | パッケージの保管場所。1 つで複数の形式を扱える |
| アップストリーム | 同じドメインの別リポジトリを参照する設定 |
| 外部接続 | npmjs や PyPI などから取得して保存する設定 |

```bash
aws codeartifact login --tool npm --domain my-org --repository shared
```

認証トークンの有効期間は既定で 12 時間です。15 分から 12 時間の範囲で指定できます。CodeBuild で使うときは `pre_build` でログインし、期限切れを避けます。リポジトリのパッケージを一般公開することはできません。

### ドメインとリポジトリの設定 {#codeartifact-settings}

| 項目 | 内容 |
|---|---|
| ドメイン | 同じアセットはドメイン内で 1 回だけ保存される(重複排除)。アカウントあたり既定で 10 |
| 暗号化 | ドメイン作成時に KMS キーを指定する |
| 直接のアップストリーム | 1 リポジトリに 10 個まで |
| 外部接続 | 公開リポジトリごとに、ドメインに 1 つのリポジトリで接続するのが想定の形 |
| 認証トークン | 既定 12 時間、15 分〜12 時間。`--duration-seconds` は 900〜43200 |
| 権限 | ドメインポリシー、リポジトリポリシーと IAM |

```bash
# CodeBuild の pre_build で使う例
export CODEARTIFACT_AUTH_TOKEN=$(aws codeartifact get-authorization-token \
  --domain my-org --domain-owner 111122223333 \
  --duration-seconds 3600 --query authorizationToken --output text)
aws codeartifact login --tool pip --domain my-org --repository shared
```

| コマンド | 使いどころ |
|---|---|
| `login` | npm、pip、twine など対応するツールを自動で設定 |
| `get-authorization-token` | Maven など `login` に対応しないツール |

**例**: ロールを引き受けて `login` を呼ぶなら、`--duration-seconds 0` で、トークンの寿命をセッションの残り時間と同じにできます。

**アップストリームと外部接続の違い**: アップストリームは同じドメインの別リポジトリを見る設定です。外部接続は npmjs や PyPI などの公開リポジトリを見る設定です。取得したパッケージは下流のリポジトリに保持されます。

**パッケージオリジンコントロール**: パッケージごとに、直接の公開とアップストリームからの取り込みを `ALLOW` か `BLOCK` で制御します。社内パッケージと同名の公開パッケージを取り込む、依存関係かく乱を防げます。

### Git リポジトリがあっても必要か {#codeartifact-need}

CodeCommit や GitHub と CodeArtifact は、置くものが違います。多くのプロジェクトでは、Git に置くのはソースコードとロックファイルまでで、依存パッケージそのものは入っていません。

たとえば `package-lock.json` はバージョンを固定しますが、中身は取りに行く必要があります。取得先は通常 npmjs などの公開リポジトリです。CodeArtifact は、この取得先を置き換えるサービスです。

```mermaid
flowchart TD
    A["Git: ソースとロックファイル"] --> B["ビルドで npm install"]
    B --> C["CodeArtifact"]
    C -->|"保存済みなら"| D["そのまま返す"]
    C -->|"未保存なら"| E["外部接続で npmjs から取得して保存"]
```

| 観点 | Git リポジトリ | CodeArtifact |
|---|---|---|
| 主に置くもの | ソースコード、ロックファイル | ビルド済みのパッケージ |
| バージョンの解決 | しない | npm や pip などのパッケージマネージャーの要求に応える |
| 社内ライブラリの配布 | ソースを渡すことになる | `npm publish` で公開し、`npm install` で使える |
| 公開パッケージの保持 | 自分で入れた場合だけ | 取得したバージョンをリポジトリに保存する |
| 同名の公開パッケージへの対策 | なし | パッケージオリジンコントロール |
| アクセス制御 | リポジトリ単位 | IAM、ドメインポリシー、リポジトリポリシー |

依存パッケージを Git に入れる方法（ベンダリング）でも、ビルドを公開リポジトリから切り離せます。その場合は、パッケージの更新や OS ごとのバイナリの扱い、リポジトリの肥大化を自分で管理します。

判断の目安は次のとおりです。

| 状況 | 判断 |
|---|---|
| 公開パッケージだけを使う小さなプロジェクト | なくてよいことが多い。ロックファイルで十分 |
| 社内ライブラリを複数のチームで共有する | 向いている |
| インターネットに出られない VPC でビルドする | 向いている。インターフェイス VPC エンドポイントで接続し、公開パッケージは CodeArtifact 経由で取得する |
| 使えるパッケージや取得元を組織で管理したい | 向いている |
| すでに GitHub Packages などを使っている | 同じ役割なので、IAM で統一したいなどの理由がなければ増やさなくてよい |

**例**: 社内ライブラリ `@my-org/utils` を CodeArtifact に公開すると、最初のバージョンの公開で、このパッケージの設定は `Publish: ALLOW`、`Upstream: BLOCK` になります。攻撃者が npmjs に同名で高いバージョンを公開しても、取り込まれません。

**設定を誤ったときの症状**: Git にロックファイルがあるだけで CodeArtifact や社内のリポジトリがないと、公開リポジトリの障害時やパッケージの削除時にビルドが失敗します。ロックファイルはバージョンを固定しますが、パッケージの保管はしないためです。

## Amplify Hosting とブランチ {#amplify}

[:material-sprout: CLF](../courses/clf/services.md){ .exam-badge .exam-foundational } [:material-certificate: SAA](../courses/saa/services.md){ .exam-badge .exam-associate } [:material-certificate: DVA](../courses/dva/services.md){ .exam-badge .exam-associate } [:material-star-circle: AIP](../courses/aip/services.md){ .exam-badge .exam-professional }

Git リポジトリと接続し、ブランチごとに Web アプリをビルドしてホスティングします。ビルド設定はコンソールまたはリポジトリの `amplify.yml` に保存します。

| 機能 | 内容 |
|---|---|
| ブランチデプロイ | ブランチごとに別の URL。例: `https://dev.<アプリID>.amplifyapp.com` |
| 自動検出 | `release**` などのパターンに合うブランチを自動でデプロイ |
| Web プレビュー | PR ごとに一意の URL を発行。レビュー用 |
| 環境変数 | ブランチごとに値を変えられる |

典型的な使い方は、`main` を本番、`develop` を結合テスト用とする構成です。Web プレビューも含めて、ブランチ数はアプリあたり 50 のクォータがあるので、不要な PR は閉じます。

### ビルド設定と環境変数 {#amplify-build-settings}

ビルド設定はコンソールかリポジトリのルートの `amplify.yml` に置きます。

```yaml
version: 1
env:
  variables:
    NEXT_PUBLIC_API: https://api.example.com
frontend:
  phases:
    preBuild:
      commands:
        - npm ci
    build:
      commands:
        - npm run build
  artifacts:
    baseDirectory: dist
    files:
      - "**/*"
  cache:
    paths:
      - node_modules/**/*
test:
  phases:
    preTest:
      commands:
        - npm ci
    test:
      commands:
        - npm test
  artifacts:
    baseDirectory: coverage
    files:
      - "**/*"
```

| 機能 | 内容 |
|---|---|
| `USER_DISABLE_TESTS` | 環境変数でテストの手順を飛ばす |
| `AWS_BRANCH` | 現在のブランチ名 |
| `AWS_PULL_REQUEST_SOURCE_BRANCH`、`AWS_PULL_REQUEST_DESTINATION_BRANCH` | Web プレビューの元と宛先のブランチ |
| ブランチのアクセス制御 | 開発中のブランチをユーザー名とパスワードで保護 |

**落とし穴**: `AWS` で始まる環境変数は作れません。シークレットを環境変数に入れないでください。Gen 2 のアプリなら Secret management を使います。

## アプリケーション環境の作成と管理 {#app-environments}

結合テストでは、**承認済みの同じ版**を環境ごとに名前で指す仕組みが役立ちます。

| 仕組み | 環境の分け方 | 詳細 |
|---|---|---|
| Lambda のエイリアス | `staging` をバージョン 7、`prod` をバージョン 6 へ向ける | [Lambda](lambda.md) |
| コンテナイメージタグ | 検証済みタグだけを本番のタスク定義で参照する | [コンテナ](containers.md) |
| Amplify のブランチ | ブランチごとに URL と環境変数を持つ | [上記](#amplify) |
| API Gateway のステージ | `dev`、`prod` のステージとステージ変数 | [API Gateway](api-gateway.md) |
| CloudFormation / SAM | 同じテンプレートをパラメータ違いで別スタックに | [IaC](iac.md) |
| Elastic Beanstalk の環境 | アプリケーションバージョンを環境へ割り当てる | [EC2 と Elastic Beanstalk](ec2-beanstalk.md) |

```bash
# ステージングで検証済みのバージョン 7 を本番へ昇格する
aws lambda update-alias --function-name orders --name prod --function-version 7
```

!!! warning "AWS Copilot のサポート終了"
    試験ガイドには AWS Copilot の環境が例として載っていますが、Copilot CLI は 2026 年 6 月 12 日にサポートを終了しました。新規の構成では ECS Express Mode や CDK が移行先として案内されています。

## デプロイ戦略の比較 {#deployment-strategies}

| 戦略 | 動き | ダウンタイム | 戻しやすさ | 追加コスト |
|---|---|---|---|---|
| 一括（all-at-once） | すべてを同時に更新 | ありうる | 再デプロイが必要で遅い | なし |
| ローリング（rolling） | 少しずつ順に更新 | なし（容量は一時的に減る） | 再度ローリングが必要 | なし、または少し |
| Blue/Green | 別環境を用意して切り替え | ほぼなし | 切り戻すだけで速い | 2 環境分の期間がある |
| カナリア（canary） | 一部へ流して確認後に残りを移す | なし | トラフィックを戻すだけ | 新旧の同時稼働 |
| 線形（linear） | 一定の割合と間隔で移す | なし | トラフィックを戻すだけ | 新旧の同時稼働 |

カナリアと線形は Blue/Green の一種として、新環境へのトラフィックの移し方を細かくしたものと考えると整理できます。

| 実現方法 | 戦略 |
|---|---|
| CodeDeploy（EC2） | `AllAtOnce`、`HalfAtATime`、`OneAtATime`、Blue/Green |
| CodeDeploy（Lambda） | カナリア、線形、一括 |
| CodeDeploy（ECS） | カナリア、線形、一括 |
| ECS の組み込みデプロイ | ローリング、Blue/Green、カナリア、線形（詳細は [コンテナ](containers.md)） |
| SAM の `DeploymentPreference` | Lambda のカナリア、線形、一括（詳細は [IaC](iac.md)） |
| API Gateway | ステージのカナリアリリース |
| Elastic Beanstalk | 一括、ローリング、追加バッチ、イミュータブル、トラフィック分割 |

選び方の目安は次のとおりです。

- 開発環境で速さ優先: 一括
- 追加コストを抑えつつ止めない: ローリング
- 本番で即座に戻したい: Blue/Green
- 少数の利用者で実データを確認したい: カナリア
- 問題を段階的に検知しながら広げたい: 線形

## ロールバックの方法 {#rollback}

| サービス | 自動 | 手動 |
|---|---|---|
| CodeDeploy | デプロイ失敗、アラーム発火 | 以前のリビジョンを再デプロイ |
| CodePipeline | ステージ条件の Rollback | `RollbackStage` |
| CloudFormation | 失敗時の自動ロールバック、ロールバックトリガー（[IaC](iac.md)） | 以前のテンプレートでスタックを更新 |
| SAM | `DeploymentPreference` の `Alarms` とフック | 以前のテンプレートを再デプロイ |
| Lambda | CodeDeploy 経由 | エイリアスを前のバージョンへ向ける |
| API Gateway | なし | ステージを以前のデプロイへ向ける |
| ECS | デプロイサーキットブレーカー | 以前のタスク定義でサービスを更新 |

「ロールバックを自動化する」問題では、**カナリアや線形でトラフィックを移し、CloudWatch アラームで発火させる**構成が定番です。データベースのスキーマ変更は戻せないことがあるので、新旧どちらの版でも動く形で進めます。

## デプロイ失敗の診断 {#troubleshooting-deployments}

まずどのサービスの、どの工程で落ちたかを確定し、その工程の出力ログを読みます。

| 症状 | 確認先 | よくある原因 |
|---|---|---|
| CodeBuild が失敗 | ビルドログ（フェーズ詳細） | テスト失敗、依存関係の取得失敗、権限不足、YAML の構文 |
| `docker` の実行で失敗 | ビルドログ | 特権モードが無効 |
| `Skipping install of runtimes` の警告 | ビルドログ | イメージが `runtime-versions` に未対応 |
| すべてのイベントが Skipped | インスタンス上のエージェント | エージェント未起動、インスタンスプロファイルなし、外向き通信不可 |
| `ApplicationStop` で失敗 | `scripts.log` | 前回の版のスクリプトが不正 |
| `DownloadBundle` で失敗 | エージェントログ | S3 の権限不足、リビジョンの場所が違う |
| `file already exists` | デプロイのイベント | `--file-exists-behavior` を `OVERWRITE` などにする |
| フックがタイムアウト | `scripts.log` | スクリプトがバックグラウンド処理を待ち続けている |
| `AllowTraffic` で失敗（ログに原因なし） | ターゲットグループ | ヘルスチェックの設定不備（[ネットワーク](networking.md)） |
| Lambda のカナリアが戻された | CloudWatch アラーム、関数のログ | 新版のエラー増加、フック関数の `Failed` 報告 |
| ECS のタスクが起動しない | ECS のサービスイベント、タスクの停止理由 | イメージ取得失敗、ヘルスチェック失敗 |
| CloudFormation のアクションが失敗 | スタックイベント | 最初の `CREATE_FAILED` または `UPDATE_FAILED` の理由 |
| パイプラインが起動しない | トリガー設定、接続の状態 | フィルターの不一致、接続が保留のまま |

EC2 へのデプロイのログは、インスタンスで直接見るか、CloudWatch エージェントで CloudWatch Logs に集約して見ます。CodeDeploy の **Lambda と ECS のデプロイにはこの種のログはない**ので、関数やタスク自体のログとデプロイのイベントを確認します。

!!! tip "切り分けの順序"
    コンソールで失敗したアクションを開く → リンク先のビルドやデプロイを開く → 失敗したフェーズやイベントのログを読む、という順に進めます。ログの検索は [オブザーバビリティ](observability.md) の Logs Insights が便利です。

## 既定値と上限のまとめ {#numbers}

| 項目 | 値 |
|---|---|
| CodeBuild のタイムアウト | 既定 60 分、5〜2,160 分 |
| CodeBuild のキューのタイムアウト | 5〜480 分 |
| `on-failure` の `RETRY` | 既定 3 回。回数は 0〜100 |
| レポートグループ | 1 プロジェクトに 5 個。レポートは 30 日で期限切れ |
| AppSpec のスクリプト | 既定と上限ともに、イベントあたり 3,600 秒 |
| CodeDeploy の既定の設定 | `OneAtATime` |
| 同じデプロイグループの同時デプロイ | 1 |
| 元のインスタンスの終了待ち | 最大 48 時間 |
| インプレースのデプロイ | 最長 12 時間 |
| Lambda のデプロイ | 最長 50 時間(移行の開始から終了まで 48 時間) |
| 手動承認 | 7 日 |
| パイプラインの同時実行(`QUEUED`、`PARALLEL`) | 50 |
| パイプラインのアクション | 1 ステージに並列 100、順次 100 |
| ソースのアーティファクト | S3 は 7 GB、CodeCommit と GitHub は 1 GB |
| CodeArtifact のトークン | 既定 12 時間、15 分〜12 時間 |
| CodeArtifact の直接のアップストリーム | 10 |
| Amplify のブランチ | 50(増やせない) |

## 試験のポイント {#exam-points}

| こう問われたら | 答え |
|---|---|
| ビルド手順を定義するファイルは | `buildspec.yml`（既定はソースのルート） |
| Lambda や ECS のデプロイ手順を定義するファイルは | AppSpec（`appspec.yml`） |
| ビルド中にシークレットを安全に使いたい | buildspec の `env.secrets-manager` |
| ビルドの依存関係取得を速くしたい | CodeBuild のキャッシュ（S3 またはローカル） |
| Docker レイヤーキャッシュの条件は | Linux 環境かつ特権モード |
| EC2 へのデプロイが全イベント Skipped | CodeDeploy エージェントとインスタンスプロファイルを確認 |
| 初回デプロイで動かないフックは | `ApplicationStop` |
| Lambda のデプロイで使えるフックは | `BeforeAllowTraffic` と `AfterAllowTraffic` |
| 新しい Lambda 版へ 10% 流し、5 分後に残りを移す | `LambdaCanary10Percent5Minutes` |
| 問題発生時に自動で戻したい | CodeDeploy の自動ロールバックと CloudWatch アラーム |
| CodeDeploy のロールバックの実体は | 以前のリビジョンの新規デプロイ（新しい ID） |
| 本番前に人の確認を入れたい | CodePipeline の Approval アクション（SNS で通知） |
| 承認されないまま放置すると | 7 日後に失敗扱い |
| GitHub からパイプラインを起動したい | CodeConnections の接続 |
| 特定のタグやパスの変更だけで起動したい | V2 パイプラインのトリガーフィルター |
| 別アカウントへデプロイしたい | クロスアカウントロールとカスタマー管理 KMS キー |
| ブランチごとにフロントエンドの環境が欲しい | Amplify Hosting のブランチデプロイ |
| PR ごとにプレビューしたい | Amplify の Web プレビュー |
| 社内 pip パッケージを共有したい | CodeArtifact |
| 追加コストなしで止めずに更新したい | ローリング |
| 即座に切り戻したい | Blue/Green |

## 関連ページ {#related}

- [IaC（CloudFormation / SAM / CDK）](iac.md)
- [オブザーバビリティ](observability.md)
- [Lambda](lambda.md)
- [コンテナ](containers.md)
- [EC2 と Elastic Beanstalk](ec2-beanstalk.md)
- [API Gateway](api-gateway.md)
- [ネットワーク](networking.md)

## 参考 {#references}

- [Build specification reference for CodeBuild](https://docs.aws.amazon.com/codebuild/latest/userguide/build-spec-ref.html)
- [Build phase transitions](https://docs.aws.amazon.com/codebuild/latest/userguide/view-build-details-phases.html)
- [Cache builds to improve performance](https://docs.aws.amazon.com/codebuild/latest/userguide/build-caching.html)
- [Test reports in AWS CodeBuild](https://docs.aws.amazon.com/codebuild/latest/userguide/test-reporting.html)
- [AppSpec 'hooks' section](https://docs.aws.amazon.com/codedeploy/latest/userguide/reference-appspec-file-structure-hooks.html)
- [AppSpec file examples](https://docs.aws.amazon.com/codedeploy/latest/userguide/reference-appspec-file-example.html)
- [Working with deployment configurations in CodeDeploy](https://docs.aws.amazon.com/codedeploy/latest/userguide/deployment-configurations.html)
- [Redeploy and roll back a deployment with CodeDeploy](https://docs.aws.amazon.com/codedeploy/latest/userguide/deployments-rollback-and-redeploy.html)
- [Working with the CodeDeploy agent](https://docs.aws.amazon.com/codedeploy/latest/userguide/codedeploy-agent.html)
- [Troubleshoot EC2/On-Premises deployment issues](https://docs.aws.amazon.com/codedeploy/latest/userguide/troubleshooting-deployments.html)
- [View log data for CodeDeploy EC2/On-Premises deployments](https://docs.aws.amazon.com/codedeploy/latest/userguide/deployments-view-logs.html)
- [CodePipeline concepts](https://docs.aws.amazon.com/codepipeline/latest/userguide/concepts.html)
- [Automate starting pipelines using triggers and filtering](https://docs.aws.amazon.com/codepipeline/latest/userguide/pipelines-triggers.html)
- [Add a manual approval action to a stage](https://docs.aws.amazon.com/codepipeline/latest/userguide/approvals.html)
- [Configure conditions for a stage](https://docs.aws.amazon.com/codepipeline/latest/userguide/stage-conditions.html)
- [What are connections?](https://docs.aws.amazon.com/dtconsole/latest/userguide/welcome-connections.html)
- [What is AWS CodeArtifact?](https://docs.aws.amazon.com/codeartifact/latest/ug/welcome.html)
- [The Future of AWS CodeCommit](https://aws.amazon.com/blogs/devops/aws-codecommit-returns-to-general-availability/)
- [Feature branch deployments and team workflows (Amplify)](https://docs.aws.amazon.com/amplify/latest/userguide/multi-environments.html)
- [Web previews for pull requests (Amplify)](https://docs.aws.amazon.com/amplify/latest/userguide/pr-previews.html)
- [Announcing the end-of-support for the AWS Copilot CLI](https://aws.amazon.com/blogs/containers/announcing-the-end-of-support-for-the-aws-copilot-cli/)
- [Amazon ECS linear deployments](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/deployment-type-linear.html)

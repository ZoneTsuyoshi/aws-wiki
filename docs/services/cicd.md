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

- **例:** `main` への push で CodePipeline が動き、CodeBuild が 3 分でテストとビルドをし、CodeDeploy が 6 台の EC2 に配布します。CodePipeline 自身はビルドも配布もしません。
- **誤ると:** Lambda の段階的な切り替えを CodePipeline だけで作ろうとしても、トラフィックは移せません。切り替えは CodeDeploy の役割です。

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

- **GitHub の例:** `my-org/my-app` の `main` を監視するなら、CodeConnections の接続の ARN を渡します。個人のアクセストークンは要りません。詳しくは [CodeConnections の接続](#codeconnections) を参照してください。
- **S3 の例:** `s3://my-artifacts/app.zip` をソースにするなら、バケットのバージョニングを有効にします。無効だとソースのアクションを使えません。
- **ECR の例:** `my-app:latest` のプッシュでパイプラインを起動し、ベースイメージの更新からデプロイまで流します。

### CodeCommit の現状 {#codecommit-status}

[:material-certificate: MLA](../courses/mla/services.md){ .exam-badge .exam-associate } [:material-star-circle: SAP](../courses/sap/services.md){ .exam-badge .exam-professional }

CodeCommit は 2024 年に新規受付を止めましたが、**2025 年 11 月に一般提供へ戻り、新規利用者も使えるようになりました**。「CodeCommit は新規利用できない」という古い記述は現在は誤りです。なお、DVA-C02 と DVA-C03 の試験ガイドの対象サービス一覧に CodeCommit は載っていません（一覧は網羅的ではないとされています）。

IAM、VPC エンドポイント、CloudTrail と統合できるため、AWS の中でソースを管理したい場合の選択肢です。Git リポジトリなので、頻繁に変わる大きなファイル、データベース、監査ログの置き場には向きません。

**提供単位**: リポジトリはリージョン単位で、VPC の外にあります（[2 つの軸](resource-scope.md#two-axes)）。VPC からはインターフェイスエンドポイントでも接続できます。

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

- **ブランチの例:** `feature/login` を `develop` にマージすると結合テストが動き、`main` にマージすると本番のパイプラインが動きます。
- **Git タグの例:** `v1.4.2` を打つと、パイプラインの起動条件 `v*` に合います。
- **コンテナイメージタグの例:** コミット `abc1234` から作ったイメージに `git-abc1234` と付けると、本番のイメージからコミットをたどれます。
- **Lambda の例:** エイリアス `prod` をバージョン `7` から `6` へ向け直すと、コードをビルドし直さずに戻せます。
- **誤ると:** タグを打ち直して別のコミットを指すと、`v1.4.2` が何を指すのかが分からなくなります。タグは動かしません。

### コミットでビルド・テスト・デプロイを起動する {#commit-triggers}

流れは「コミットをプッシュする → トリガーが発火する → CodePipeline がその版を取得する → CodeBuild がビルドしてテストする → デプロイする」です。人がコマンドを実行する必要はありません。

CodeBuild だけで済む場合は、プロジェクトに Webhook を設定してプッシュや PR で直接ビルドを始めることもできます。承認や複数環境への展開が必要になったら CodePipeline を使います。

- **CodeBuild だけの例:** PR ごとに `pytest` を走らせて結果を GitHub に返すだけなら、Webhook で足ります。
- **CodePipeline の例:** テスト、ステージングへのデプロイ、手動承認、本番へのデプロイと続くなら、ステージに分けます。

## CodeBuild {#codebuild}

[:material-sprout: CLF](../courses/clf/services.md){ .exam-badge .exam-foundational } [:material-certificate: DVA](../courses/dva/services.md){ .exam-badge .exam-associate } [:material-certificate: DEA](../courses/dea/services.md){ .exam-badge .exam-associate } [:material-certificate: MLA](../courses/mla/services.md){ .exam-badge .exam-associate } [:material-star-circle: SAP](../courses/sap/services.md){ .exam-badge .exam-professional } [:material-star-circle: DOP](../courses/dop/services.md){ .exam-badge .exam-professional } [:material-star-circle: AIP](../courses/aip/services.md){ .exam-badge .exam-professional }

フルマネージドのビルドサービスです。ビルドごとに新しい環境を用意するので、ビルドサーバーの管理が不要です。ビルド時の権限はプロジェクトのサービスロールで決まります。

**提供単位**: プロジェクトはリージョン単位です。ビルドは既定で VPC の外で動き、`vpcConfig` で自分の VPC に接続できます（[2 つの軸](resource-scope.md#two-axes)、[VPC の設定](#codebuild-vpc)）。

- **例:** 東京のプロジェクトは東京のコンソールに出ます。東京の RDS に接続するテストなら、`vpcConfig` に RDS へ届くサブネットを指定します。

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

キーごとの例です。

- **`version` の例:** `0.1` では次の 2 行が別のシェルで動くので、`npm ci` は `src` の外で動いて失敗します。`0.2` なら `src` の中で動きます。

```yaml
commands:
  - cd src
  - npm ci
```

- **`run-as` の例:** 全体に `run-as: builder` と書き、`install` にだけ `run-as: root` と書くと、`install` は `root` で、他は `builder` で動きます。
- **`env.shell` の例:** `shell: {linux: bash}` と書くと、Linux では `bash` を使います。`[[ ... ]]` を使うスクリプトに必要になります。
- **`env.variables` の例:** `APP_ENV: staging` は buildspec にそのまま残ります。パスワードを書くと、リポジトリに平文で残ります。
- **`env.parameter-store` の例:** `API_URL: /myapp/staging/api-url` で、ビルド中に `$API_URL` として読めます。
- **`env.exported-variables` の例:** `IMAGE_TAG` を挙げて `namespace` を `BuildVariables` にすると、次のアクションで `#{BuildVariables.IMAGE_TAG}` として読めます。
- **`env.git-credential-helper` の例:** プライベートなサブモジュールを取得するビルドに `yes` を使います。公開リポジトリの Webhook で起動したビルドでは使えません。
- **`proxy` の例:** 明示的なプロキシの背後にある VPC で、成果物をアップロードできないなら `upload-artifacts: yes` にします。ログも同様に `logs: yes` です。
- **`phases` の例:** `test` という名前のフェーズは作れません。テストは `build` か `pre_build` に書きます。

#### secrets-manager の指定 {#buildspec-secrets}

```yaml
env:
  secrets-manager:
    DB_PASSWORD: "prod/db:password"
    OTHER_ACCOUNT: "arn:aws:secretsmanager:ap-northeast-1:111122223333:secret:prod/api-AbCdEf:key"
```

JSON キーを省くとシークレット全体を取得します。別のアカウントのシークレットは ARN で指定します。`version-stage` と `version-id` は同時に指定しません。

**症状**: サービスロールに読み取り権限がないと、ビルドは値を取得できずに権限エラーで失敗します。カスタマー管理キーで暗号化しているなら `kms:Decrypt` も確認します。

- **JSON キーの例:** `prod/db` の中身が `{"password":"..."}` なら、`prod/db:password` で値だけを読みます。`prod/db` だけなら JSON 全体が `DB_PASSWORD` に入り、DB への接続に失敗します。
- **`version-stage` の例:** `prod/db:password:AWSPREVIOUS` は、ローテーション前の値を読みます。
- **`version-id` の例:** `prod/db:password::<バージョン ID>` のように、ステージを空にして指定します。

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

```yaml
phases:
  pre_build:
    on-failure: CONTINUE
    commands:
      - ./lint.sh
  build:
    on-failure: RETRY-3-.*connection timed out.*
    commands:
      - npm ci
    finally:
      - ./cleanup.sh
```

- **`ABORT` の例:** `pre_build` のテストが失敗した時点で止めます。`build` に進みません。
- **`CONTINUE` の例:** 上の `lint.sh` が失敗しても `build` に進みます。
- **`RETRY` の例:** どのメッセージでも最大 3 回です。
- **`RETRY-<回数>` の例:** `RETRY-8` は 8 回です。101 は範囲外です。
- **`RETRY-<正規表現>` の例:** `RETRY-.*Error: Unable to connect to database.*` は、メッセージが一致すれば最大 3 回です。一致しないテストの失敗では再試行しません。
- **`RETRY-<回数>-<正規表現>` の例:** 上の `build` は、`connection timed out` を含むときだけ 3 回です。
- **`finally` の例:** `commands` が 3 つで最初が失敗すると、残り 2 つを飛ばして `finally` を動かします。この場合、フェーズは失敗のままです。
- **誤ると:** `on-failure` を書いた buildspec を Lambda コンピュートで使っても、指定どおりには動きません。

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

- **`discard-paths` の例:** `dist/js/app.js` が `yes` では `app.js` になります。`dist/a/index.js` と `dist/b/index.js` は同じ名前になり、片方が残りません。
- **`exclude-paths` の例:** `**/*.map` でソースマップを除きます。
- **`name` の例:** `name: app-$(date +%Y-%m-%d)` で日付入りの名前にします。
- **`s3-prefix` の例:** `s3-prefix: builds/orders` で、成果物をこの接頭辞の下に置きます。
- **`enable-symlinks` の例:** `node_modules/.bin` のシンボリックリンクを、ZIP の中でもリンクのまま残します。
- **`secondary-artifacts` の例:** `web` と `api` の 2 つに分けます。buildspec のキーは、プロジェクトの `secondaryArtifacts` の識別子と合わせます。

`cache` には、S3 キャッシュの版を分けるキーもあります。

```yaml
cache:
  key: npm-key-$(codebuild-hash-files package-lock.json)
  fallback-keys:
    - npm-key-
    - npm-
  action: restore
  paths:
    - "node_modules/**/*"
```

- **`key` の例:** 完全一致で探します。`package-lock.json` が変わるとハッシュも変わり、新しいキャッシュになります。
- **`fallback-keys` の例:** `key` で見つからないと、上から順に接頭辞で探します。5 個までです。`key` がなければ無視されます。
- **`action` の例:** `restore` は読むだけ、`save` は保存するだけです。PR のビルドで本線のキャッシュを汚したくないなら `restore` です。

#### batch {#buildspec-batch}

| キー | 動作 |
|---|---|
| `batch.fast-fail` | 失敗したときに残りのタスクを止めるか |
| `batch.build-graph` | 依存関係のあるビルドの集まり |
| `batch.build-list` | 並列に動かす一覧 |
| `batch.build-matrix` | 変数の組み合わせごとにビルド |
| `batch.build-fanout` | テストを分割して並列実行 |

**例**: Python 3.11 と 3.12 の両方でテストするなら `build-matrix`、A のビルドの後で B を動かすなら `build-graph` の `depend-on` を使います。

- **`fast-fail` の例:** 既定は `false` で、1 つが失敗しても他は続きます。`true` なら、5 並列のうち 1 つが失敗した時点で残りを止めます。
- **`build-list` の例:** `lint` と `test` を依存なしで同時に動かします。
- **`build-matrix` の計算例:** Python が 2 種類、OS のイメージが 3 種類なら、2 × 3 = 6 ビルドです。
- **`build-fanout` の例:** `parallelism: 5` で、テストを 5 つのビルドに分けます。1,000 件を 5 分割すれば、1 つあたり約 200 件です。
- **`ignore-failure` の例:** 既定は `false` です。`true` のタスクは失敗しても、バッチ全体は成功できます。

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

- **`install` の例:** `runtime-versions: {python: 3.12}` を書き、`pip install -r requirements.txt` を実行します。
- **`pre_build` の例:** `aws ecr get-login-password ...` で ECR にログインし、`pytest` で単体テストを動かします。
- **`build` の例:** `docker build -t my-app .` を実行します。
- **`post_build` の例:** `docker push` の後で `imagedefinitions.json` を作ります。ビルドの成否を見ずにプッシュすると壊れたイメージが出るので、次のように判定します。

```bash
if [ "$CODEBUILD_BUILD_SUCCEEDING" = "1" ]; then docker push "$IMAGE"; fi
```

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

- **`environment.type` の例:** `ARM_CONTAINER` は Graviton で動きます。ARM 用のイメージをビルドしたいときに使います。
- **`environment.computeType` の例:** メモリ不足で `npm run build` が落ちるなら、`BUILD_GENERAL1_SMALL` を `BUILD_GENERAL1_MEDIUM` に上げます。ローカルキャッシュは `BUILD_GENERAL1_2XLARGE` では使えません。
- **Lambda コンピュートの例:** `BUILD_LAMBDA_1GB` は 1 分の単体テストの起動が速くなります。次の用途には使えません。15 分を超えるビルド、`docker build`、VPC への接続、キャッシュ、独自のタイムアウト、特権モードです。
- **`environment.image` の例:** 標準の `aws/codebuild/standard:7.0` には多くの言語が入っています。独自のツールが要るなら、自分の ECR イメージを指定します。
- **`imagePullCredentialsType` の例:** 別アカウントの ECR や非公開のレジストリのイメージは `SERVICE_ROLE` が必須です。CodeBuild 提供のイメージは `CODEBUILD` が必須です。
- **`queuedTimeoutInMinutes` の例:** 値が 30 なら、同時実行の上限で 30 分待つとビルドは実行されずに終わります。
- **`serviceRole` の例:** ロールに `s3:PutObject` がなければ、`UPLOAD_ARTIFACTS` で失敗します。
- **`logsConfig` の例:** CloudWatch Logs で直近を検索し、S3 に長期保存するなど、両方に出せます。
- **`concurrentBuildLimit` の例:** 値が 3 で 3 つが動いていると、4 つ目は動きません。同じ DB を使う結合テストの衝突を防げます。

#### VPC の設定 {#codebuild-vpc}

CodeBuild は既定では VPC の中のリソースに届きません。RDS にアクセスするテストなら `vpcConfig` を指定します。

**落とし穴**: サブネットはプライベートにして、NAT ゲートウェイか VPC エンドポイントを用意します。これがないと、ソースのダウンロードや `pip install` が失敗します。

- **`vpcConfig` の例:** `vpcId`、`subnets`、`securityGroupIds` を指定します。1a と 1c のプライベートサブネットを指定し、セキュリティグループの送信を許可し、RDS 側で 3306 の受信を許可します。
- **誤ると:** パブリックサブネットを指定しても、インターネットには出られません。CodeBuild はインターネットゲートウェイの代わりに NAT を必要とします。

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

フィルターごとの例です。

- **`EVENT` の例:** `PUSH, PULL_REQUEST_CREATED, PULL_REQUEST_UPDATED` のようにカンマで並べると、どれかで動きます。
- **`HEAD_REF` の例:** `^refs/tags/v.*` なら、`v1.4.2` のタグのプッシュで動きます。
- **`BASE_REF` の例:** PR のイベントと組み合わせて `^refs/heads/main$` にすると、`main` 宛ての PR だけで動きます。
- **`FILE_PATH` の例:** `^services/orders/.*` なら、`services/orders/app.py` の変更で動き、`README.md` だけの変更では動きません。
- **`ACTOR_ACCOUNT_ID` の例:** `^12345678$` のように GitHub のユーザー ID を指定し、外部からの PR で勝手にビルドが動くのを防ぎます。
- **`COMMIT_MESSAGE` の例:** `\[skip\]` と `excludeMatchedPattern: true` で、`docs: fix typo [skip]` のコミットでは動きません。
- **AND と OR の例:** 次の設定は「`main` への push」または「`main` 宛ての PR の作成」で動きます。

```json
{"filterGroups": [
  [{"type": "EVENT", "pattern": "PUSH"},
   {"type": "HEAD_REF", "pattern": "^refs/heads/main$"}],
  [{"type": "EVENT", "pattern": "PULL_REQUEST_CREATED"},
   {"type": "BASE_REF", "pattern": "^refs/heads/main$"}]
]}
```

#### 組み込みの環境変数 {#codebuild-built-in-vars}

| 変数 | 内容 |
|---|---|
| `CODEBUILD_BUILD_ID` | ビルド ID |
| `CODEBUILD_BUILD_SUCCEEDING` | `1` は成功、`0` は失敗 |
| `CODEBUILD_RESOLVED_SOURCE_VERSION` | コミット ID。`DOWNLOAD_SOURCE` の後で使える |
| `CODEBUILD_SOURCE_VERSION` | 指定したソースのバージョン |
| `CODEBUILD_SRC_DIR` | ソースのディレクトリ |
| `CODEBUILD_WEBHOOK_EVENT` | Webhook のイベント |

- **`CODEBUILD_RESOLVED_SOURCE_VERSION` の例:** `IMAGE_TAG=${CODEBUILD_RESOLVED_SOURCE_VERSION:0:7}` で、`abc1234` のような短いタグを作ります。
- **`CODEBUILD_BUILD_ID` の例:** `orders:` に続く ID の形で、ログや通知にビルドを特定する値として書きます。
- **`CODEBUILD_SOURCE_VERSION` の例:** ブランチの指定で起動すれば `main`、PR なら `pr/12` のような値です。解決後のコミット ID を使うなら `CODEBUILD_RESOLVED_SOURCE_VERSION` です。
- **`CODEBUILD_SRC_DIR` の例:** `cd "$CODEBUILD_SRC_DIR/services/orders"` のように、ソースのルートからの相対で移動します。
- **`CODEBUILD_WEBHOOK_EVENT` の例:** `PULL_REQUEST_CREATED` のときだけ結合テストを省く、といった分岐に使います。

### 環境変数とシークレット {#build-env}

| 定義先 | 向いているもの | 注意 |
|---|---|---|
| `env.variables` | 秘密でない設定値 | buildspec にそのまま残る |
| `env.parameter-store` | Parameter Store の値 | サービスロールに `ssm:GetParameters` が必要 |
| `env.secrets-manager` | パスワードや API キー | 形式は `シークレットID:JSONキー:ステージ:バージョン`。サービスロールに読み取り権限が必要 |
| `env.exported-variables` | 後続のパイプラインアクションへ渡す値 | `install` から `post_build` の間に更新できる |

Parameter Store と Secrets Manager から取得した値はログでマスクされます。ただしマスクは保存値との完全一致です。Base64 にするなど値を加工して出力すると隠れません。

- **マスクの例:** 値が `s3cret` のとき、`echo $DB_PASSWORD` のログは `***` です。`echo $DB_PASSWORD | base64` のログには `czNjcmV0Cg==` と出ます。値が変換されるとマスクされません。
- **優先順位の例:** buildspec の `APP_ENV: staging` より、プロジェクトの `APP_ENV=qa` が優先され、ビルド開始時の `APP_ENV=prod` はさらに優先されます。
- **誤ると:** `env.variables` にパスワードを書くと、buildspec のあるリポジトリを読める全員に見えます。

### アーティファクト {#build-artifacts}

`artifacts` で、ビルドの成果物として保存するファイルを指定します。

| キー | 意味 |
|---|---|
| `files` | 出力するファイル。`**/*` で配下すべて |
| `base-directory` | 基準ディレクトリ |
| `discard-paths` | `yes` でディレクトリ構造を捨てる |
| `secondary-artifacts` | 複数の成果物を分けて出力する |

CodePipeline では、この成果物がパイプラインの S3 バケットを経由して次のアクションに渡ります。

- **例:** `packaged.yaml` だけを `files` に書くと、次の CloudFormation のアクションはこのファイルだけを受け取ります。
- **誤ると:** `base-directory: dist` で `files: ["dist/**/*"]` と書くと、`dist/dist/...` を探すことになり、成果物が空になるか失敗します。

### キャッシュ {#build-cache}

| 種類 | 保存先 | 向いている場面 |
|---|---|---|
| S3 キャッシュ | S3 バケット | 複数のビルドホストで共有したいとき |
| ローカル: ソース | ビルドホスト | Git メタデータの再利用 |
| ローカル: Docker レイヤー | ビルドホスト | イメージのビルド短縮（Linux のみ、特権モードが必要） |
| ローカル: カスタム | ビルドホスト | buildspec の `cache.paths` で指定した依存関係 |

Docker イメージをビルドするプロジェクトでは特権モード（privileged）を有効にします。

- **S3 キャッシュの例:** `pip` の依存関係を `s3://my-cache/orders/` に置きます。別のビルドホストでも読めますが、取得と保存の時間がかかります。
- **`LOCAL_SOURCE_CACHE` の例:** 大きな Git リポジトリの取得を差分だけにします。
- **`LOCAL_DOCKER_LAYER_CACHE` の例:** ベースイメージのレイヤーを再利用します。Linux と特権モードが必須です。
- **`LOCAL_CUSTOM_CACHE` の例:** buildspec の `cache.paths` に `/root/.cache/pip/**/*` を書きます。
- **誤ると:** ローカルキャッシュは同じビルドホストに当たったときだけ効きます。毎回速くなることを前提にすると、たまに遅いビルドが出ます。

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

- **`file-format` の例:** `pytest --junitxml=reports/unit.xml` なら `JUNITXML` です。カバレッジの `coverage.xml` なら `COBERTURAXML` です。形式が合わないと、レポートは読み取れません。
- **グループ名の例:** プロジェクト `orders` に `unit-tests` と書くと、`orders-unit-tests` です。
- **`base-directory` の例:** `base-directory: reports`、`files: ["unit.xml"]` で `reports/unit.xml` を読みます。
- **期限の例:** 10 月 1 日のレポートは 10 月 31 日に期限切れです。監査で 1 年残すなら、S3 へエクスポートします。

### ログ {#build-logs}

ビルドログは CloudWatch Logs、S3、またはその両方に出力できます。失敗時は、コンソールのフェーズ詳細でどのフェーズが落ちたかを確認し、そのログを読みます。

VPC 内でビルドすると、インターネットへ出る経路がなければ依存関係の取得に失敗します。NAT ゲートウェイや VPC エンドポイントを確認します。

- **例:** CloudWatch Logs は `groupName: /codebuild/orders`、S3 は `location: my-logs/orders` に出します。
- **誤ると:** サービスロールに `logs:CreateLogStream`、`logs:PutLogEvents` がないと、CloudWatch Logs にログが出ません。

## CodeDeploy {#codedeploy}

[:material-certificate: DVA](../courses/dva/services.md){ .exam-badge .exam-associate } [:material-certificate: DEA](../courses/dea/services.md){ .exam-badge .exam-associate } [:material-certificate: MLA](../courses/mla/services.md){ .exam-badge .exam-associate } [:material-star-circle: SAP](../courses/sap/services.md){ .exam-badge .exam-professional } [:material-star-circle: DOP](../courses/dop/services.md){ .exam-badge .exam-professional } [:material-star-circle: AIP](../courses/aip/services.md){ .exam-badge .exam-professional }

アプリケーションのリビジョンを、EC2、オンプレミス、Lambda、ECS へ配布するサービスです。

**提供単位**: アプリケーションとデプロイグループはリージョン単位で、CodeDeploy 自体は VPC の外にあります（[2 つの軸](resource-scope.md#two-axes)）。配布先の EC2 は AZ のサブネットにあるので、エージェントから CodeDeploy へ出る経路が必要です。

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

用語と設定の例です。

- **アプリケーションの例:** `aws deploy create-application --application-name web --compute-platform Lambda` です。プラットフォームは `Server`、`Lambda`、`ECS` です。
- **デプロイグループの例:** EC2 のタグ `Env=prod` で 6 台を選びます。タグを付け忘れた新しいインスタンスには配布されません。
- **リビジョンの例:** EC2 なら `s3://my-artifacts/web-1.4.2.zip` です。中のルートに `appspec.yml` が必要です。
- **デプロイタイプの例:** 6 台のインプレースは既存の台を更新します。Blue/Green は別の 6 台を用意してトラフィックを移します。Lambda と ECS はインプレースを使えません。
- **`actionOnTimeout` の例:** `STOP_DEPLOYMENT` で `waitTimeInMinutes: 60` なら、新しいインスタンスを用意した後、60 分以内に `ContinueDeployment` を呼びます。呼ばないとデプロイは `Stopped` です。`CONTINUE_DEPLOYMENT` はすぐに登録します。
- **`terminateBlueInstancesOnDeploymentSuccess.action` の例:** `TERMINATE` で 60 分なら、切り替えの 1 時間後に旧インスタンスを終了します。`KEEP_ALIVE` は動かし続けるので、料金は続きます。ロードバランサーとデプロイグループからは外れます。
- **`terminationWaitTimeInMinutes` の範囲:** 上限は 2,880 分（48 時間）です。

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

- **`source`、`destination` の例:** `source: /build`、`destination: /var/www/app` なら、バンドルの `build/index.html` は `/var/www/app/index.html` に置かれます。
- **`pattern`、`except` の例:** `pattern: "*.sh"`、`mode: 755` でスクリプトだけに実行権限を付けます。`except: ["debug.sh"]` で除外します。`pattern` は文字列を `""` で囲みます。
- **`owner`、`group` の例:** `owner: www-data`、`group: www-data` です。指定しないと、コピーした元の所有者のままです。
- **`type` の例:** `file` だけなら、ディレクトリには適用しません。
- **`acls`、`context` の例:** Linux の ACL と SELinux のコンテキストを設定します。macOS のインスタンスでは使えず、デプロイが失敗します。
- **`location` の例:** `location: scripts/stop.sh` はバンドルのルートからの相対です。
- **`runas` の例:** `runas: www-data` で実行します。省くとエージェントと同じユーザー（通常は root）で動くので、最小権限なら指定します。
- **`timeout` の計算例:** `AfterInstall` のスクリプトが 2 つで、`timeout` が 2,000 秒ずつだと、合計 4,000 秒で 3,600 秒を超えます。そのインスタンスのデプロイは失敗します。
- **`OVERWRITE` の例:** 手で置いた `/var/www/app/config.json` を、リビジョンの版で置き換えます。
- **`RETAIN` の例:** 上の `config.json` を残して、次のデプロイの一部として扱います。
- **`DISALLOW` の例:** 既定の動作で、同じファイルがあるとデプロイは失敗します。

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

- **`ContainerName`、`ContainerPort` の例:** `web` と `8080` は、タスク定義の `name` と `containerPort` に合わせます。違うとデプロイが失敗します。
- **`PlatformVersion` の例:** `"1.4.0"` のように指定します。
- **`NetworkConfiguration` の例:** `Subnets`、`SecurityGroups`、`AssignPublicIp: DISABLED` を指定します。
- **`CapacityProviderStrategy` の例:** `FARGATE_SPOT` に `Weight: 1` を指定します。
- **Lambda の例:** `Alias: live`、`CurrentVersion: "6"`、`TargetVersion: "7"` は、`live` をバージョン 6 から 7 へ移します。

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

各フックの場面です。

- **`BeforeBlockTraffic` の例:** ロードバランサーから外す前に、処理中のジョブを止める準備をします。
- **`AfterBlockTraffic` の例:** 外れた後で、残りの接続が終わるのを待ちます。
- **`ApplicationStop` の例:** `systemctl stop web` を実行します。初回デプロイでは動きません。
- **`BeforeInstall` の例:** 設定ファイルのバックアップを取ります。
- **`AfterInstall` の例:** `chown -R www-data /var/www/app` で権限を変えます。
- **`ApplicationStart` の例:** `systemctl start web` を実行します。
- **`ValidateService` の例:** `curl -f http://localhost:8080/health` を実行します。失敗すると、このインスタンスのデプロイは失敗です。
- **`BeforeAllowTraffic`、`AfterAllowTraffic` の例:** Lambda なら、切り替え前にテスト呼び出しをし、切り替え後に 5XX の数を確かめます。
- **`AfterAllowTestTraffic` の例:** ECS で、テストリスナーの 8443 にリクエストを送って確かめます。
- **`ApplicationStop` の誤り:** 前の版の `stop.sh` が壊れていると、新しい版で直しても失敗します。`--ignore-application-stop-failures` で続けます。

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

9 台の EC2 での動きを比べます。

| 設定 | 同時に配布する台数 | 全体が成功する条件 |
|---|---|---|
| `AllAtOnce` | できるだけ多く(9 台) | 1 台以上に成功 |
| `HalfAtATime` | 4 台(端数切り捨て) | 5 台以上に成功(端数切り上げ) |
| `OneAtATime` | 1 台 | 全台に成功。最後の 1 台の失敗は全体の成功を妨げない |

Lambda と ECS の時間も計算できます。

- **`LambdaCanary10Percent15Minutes` の例:** 10% を移して 15 分待ち、残り 90% を移します。
- **`LambdaLinear10PercentEvery3Minutes` の例:** 3 分ごとに 10% なので、全部で 30 分ほどかかります。
- **`ECSLinear10PercentEvery1Minutes` の例:** 毎分 10% なので、10 分ほどです。
- **独自の設定の例:** 25% を移して 45 分待つ設定を作ります。

```bash
aws deploy create-deployment-config --deployment-config-name Canary25Percent45Minutes \
  --traffic-routing-config "type=TimeBasedCanary,timeBasedCanary={canaryPercentage=25,canaryInterval=45}" \
  --compute-platform Lambda
```

- **誤ると:** Network Load Balancer の ECS で `ECSCanary10Percent5Minutes` は使えません。`ECSAllAtOnce` だけです。

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

- **`HOST_COUNT` の例:** 9 台で 6 なら、同時に 3 台まで配布します。6 台以上に成功すれば全体が成功です。
- **`FLEET_PERCENT` の例:** 9 台で 40 なら、同時に 5 台まで配布します。4 台以上に成功すれば全体が成功です。
- **AZ ごとの例:** `--zonal-config` で、AZ ごとの最小正常台数と、次の AZ へ進むまでの待ち時間 `monitorDurationInSeconds` を指定できます。3,600 なら、1 つの AZ が終わってから 1 時間見ます。
- **誤ると:** `HOST_COUNT` を台数と同じ 9 にすると、1 台も止められません。

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

- **`DEPLOYMENT_FAILURE` の例:** リビジョン 7 のデプロイが失敗すると、リビジョン 6 を新しいデプロイ ID で配布します。履歴には失敗の 7 と、成功の 6 が並びます。
- **`DEPLOYMENT_STOP_ON_ALARM` の例:** `web-5xx` が `ALARM` になるとデプロイが止まり、前のリビジョンを配布します。`events` に書かないと、止まるだけです。
- **`DEPLOYMENT_STOP_ON_REQUEST` の例:** `aws deploy stop-deployment` で止めたときにも戻します。
- **`ignorePollAlarmFailure` の例:** `true` なら、CloudWatch からアラームの状態を読めなくてもデプロイを続けます。`false` なら、そこで止まります。
- **保持の誤りの例:** 前のデプロイで `RETAIN` で残したファイルも、失敗した `OVERWRITE` のデプロイで消えると、ロールバックの後にも戻りません。

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

- **`:verbose:` の例:** `true` にすると、デバッグメッセージがログに出ます。調査が終わったら戻します。
- **`:wait_between_runs:` の例:** 配布の確認の間隔です。エージェント 2.0 系の既定は 30 秒です。
- **`:max_revisions:` の例:** 2 にすると、古いリビジョンの保存を減らして、ディスクの空きを保てます。
- **`:proxy_uri:` の例:** プロキシ経由でしか 443 に出られない環境で指定します。
- **同時デプロイの例:** `prod` へのデプロイの実行中に 2 つ目を始めると、エラーになります。Auto Scaling のスケールアウトでの配布と重なることもあります。
- **誤ると:** エージェントが止まっていると、すべてのライフサイクルイベントが `Skipped` になり、`HEALTH_CONSTRAINTS` のエラーでデプロイが失敗することがあります。イベントの実行中に止まると、`Failed` と表示されるまで最大 1 時間かかることがあります。

## CodePipeline {#codepipeline}

[:material-sprout: CLF](../courses/clf/services.md){ .exam-badge .exam-foundational } [:material-certificate: DVA](../courses/dva/services.md){ .exam-badge .exam-associate } [:material-certificate: DEA](../courses/dea/services.md){ .exam-badge .exam-associate } [:material-certificate: MLA](../courses/mla/services.md){ .exam-badge .exam-associate } [:material-star-circle: SAP](../courses/sap/services.md){ .exam-badge .exam-professional } [:material-star-circle: DOP](../courses/dop/services.md){ .exam-badge .exam-professional } [:material-star-circle: AIP](../courses/aip/services.md){ .exam-badge .exam-professional }

ソースから本番までの流れを定義し、自動で進めるサービスです。自身はビルドや配布を行わず、CodeBuild や CodeDeploy などを呼び出します。

**提供単位**: パイプラインはリージョン単位で、VPC の外にあります（[2 つの軸](resource-scope.md#two-axes)）。アクションごとに別のリージョンを指定できます。パイプラインの名前はリージョンごとに一意です。

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

実行 A が `Deploy` にあり、B と C が続けて来たときの動きです。

- **`SUPERSEDED` の例:** `Build` の出口で B が待っているところに C が来ると、B は置き換えられます。A の次に `Deploy` へ進むのは C です。B はデプロイされません。
- **`QUEUED` の例:** A、B、C の順に 1 つずつ進みます。すべてのコミットを順に本番へ出す監査要件に向きます。同時実行は 50 までです。
- **`PARALLEL` の例:** A、B、C が同時に動きます。機能ブランチごとの検証環境に向きます。1 つの実行の中で同時に動くアクションは 5 個までです。
- **`runOrder` の例:** `Lint` と `Unit` を 1、`Package` を 2 にすると、2 つが並列に終わってから `Package` が動きます。範囲は 1〜999 です。
- **遷移の例:** `Prod` の手前の遷移を無効にすると、障害の対応中は本番へ進みません。
- **誤ると:** 同じステージに `Deploy` を 2 つ置いて同じ `runOrder` にすると、同時に動きます。順序があるなら値を変えます。

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

- **パイプラインレベルの変数の例:** 実行時に値を渡します。`Default` がなければ必須で、渡さないと実行は失敗します。50 個までです。

```bash
aws codepipeline start-pipeline-execution --name orders \
  --variables name=Stage,value=prod
```

- **ソースリビジョンの上書きの例:** 古いコミットを指定して出し直します。

```bash
aws codepipeline start-pipeline-execution --name orders \
  --source-revisions actionName=Source,revisionType=COMMIT_ID,revisionValue=abc1234
```

- **Commands アクションの例:** ビルドプロジェクトを作らず、`npm test` を実行します。ビルドのタイムアウトは 55 分です。
- **誤ると:** V1 のパイプラインに `QUEUED` やステージ条件を設定することはできません。先に V2 へ変えます。

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
| 手動承認 | 既定 7 日。アクションの `timeoutInMinutes` で 5 分〜60 日に変更可 |

**落とし穴**: CodeBuild のアクションに複数の入力を渡すなら `PrimarySource` が必要です。buildspec はこの入力から探します。CodeDeploy のアクションには `appspec.yml` を含む出力を渡します。入力名の誤りはパイプラインの作成か実行で失敗します。

- **`category`、`provider` の例:** `Deploy` の `CloudFormation` なら `ActionMode: CREATE_UPDATE` などを指定します。`Approval` の `Manual` ならソースは要りません。
- **`namespace` の例:** 上の `BuildVariables` なら、後続で `#{BuildVariables.IMAGE_TAG}` と書きます。
- **`inputArtifacts` の例:** 上の `SourceOutput` は、`Source` アクションの `outputArtifacts` の名前と同じにします。
- **`region` の例:** 東京のパイプラインから `us-east-1` にデプロイするなら、アクションに `"region": "us-east-1"` を書き、そのリージョンのアーティファクトバケットを用意します。
- **`roleArn` の例:** `arn:aws:iam::111122223333:role/CrossAccountDeploy` を書くと、そのアカウントのロールでアクションを動かします。
- **タイムアウトの例:** CodeBuild のアクションは最長 36 時間です。プロジェクトの `timeoutInMinutes` が 60 なら、60 分で先にビルドが失敗します。

### 変数 {#pipeline-variables}

| 種類 | 書き方 | 例 |
|---|---|---|
| アクション出力 | `#{名前空間.キー}` | `#{SourceVariables.CommitId}` |
| CodeBuild のエクスポート | `#{名前空間.変数名}` | `#{BuildVariables.IMAGE_TAG}` |
| パイプラインレベル | `#{variables.名前}` | `#{variables.Stage}` |
| 実行 ID | `#{codepipeline.PipelineExecutionId}` | |

**例**: `Source` の `namespace` を `SourceVariables` とすると、次の承認アクションの `CustomData` に `#{SourceVariables.CommitId}` を入れて、確認するコミットを示せます。

- **アクション出力の例:** CodeConnections のソースは `CommitId`、`BranchName` などを出力します。ソースの `namespace` が `SourceVariables` なら `#{SourceVariables.BranchName}` は `main` です。
- **パイプラインレベルの例:** `--variables name=Stage,value=prod` で起動すると、`#{variables.Stage}` は `prod` です。
- **実行 ID の例:** `#{codepipeline.PipelineExecutionId}` を CloudFormation のパラメータに渡し、どの実行で作ったかをタグに残します。
- **誤ると:** `namespace` を書かないアクションの変数は参照できません。

### CodeConnections の接続 {#codeconnections}

**提供単位:** リージョン。接続は VPC の外にあるリソースで、ARN にリージョンが入ります（[提供単位の一覧](resource-scope.md)）。

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
| 対応先 | GitHub.com、GitHub Enterprise Cloud と Server、GitLab.com と自己管理、Bitbucket Cloud、Azure DevOps。ただし CodePipeline のソースアクションの説明に Azure DevOps は載っていない |
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

ソースアクションの各設定は次のとおりです。

#### ConnectionArn {#connection-arn}

使う接続の ARN です。必須で、認可が終わった接続を指定します。

- **例:** `arn:aws:codeconnections:ap-northeast-1:111122223333:connection/aEXAMPLE-8aad-4d5d-8878-dfcab0bc441f`
- **誤ると:** 接続が `PENDING` のままだと、ソースのステージを実行できません。

#### FullRepositoryId {#full-repository-id}

監視するリポジトリを「所有者/リポジトリ名」で書きます。必須で、大文字と小文字も正確に書きます。

- **例:** GitHub の組織 `my-org` のリポジトリ `My-App` なら、`my-org/My-App` です。
- **誤ると:** `my-org/my-app` のように大文字と小文字が違うと、公式が推奨する値から外れます。ソースの取得やトリガーで問題が出たら、まずここを確認します。URL の `https://github.com/my-org/My-App` をそのまま入れるのも誤りです。

#### BranchName {#connection-branch-name}

変更を検知するブランチです。必須です。

- **例:** 本番用のパイプラインは `main`、検証用は `develop` と、ブランチごとにパイプラインを分けられます。
- **誤ると:** `master` と書いたまま `main` に push しても、パイプラインは起動しません。

#### DetectChanges {#connection-detect-changes}

新しいコミットでパイプラインを自動起動するかを決めます。省略時は `true` です。

| 値 | 動き | 使う場面 |
|---|---|---|
| `true` | コミットで自動起動する | 通常の CI/CD |
| `false` | 変更検知ではコミットで起動しない。フィルター付きのトリガーがあれば、その条件で起動する | 手動やスケジュールで起動する夜間リリース |

- **例:** 毎日 22 時にだけ本番へ出すなら `false` にし、EventBridge のスケジュールから `StartPipelineExecution` を呼びます。
- **誤ると:** トリガーを付けずに `false` のまま忘れると、push しても動かず、エラーも出ません。

#### OutputArtifactFormat {#connection-output-format}

後続のアクションへ渡す成果物の形式です。省略時は `CODE_ZIP` です。

| 値 | 中身 | 使う場面 |
|---|---|---|
| `CODE_ZIP` | ソースの ZIP。Git の履歴は含まない | 履歴が要らないビルドとデプロイ |
| `CODEBUILD_CLONE_REF` | リポジトリへの参照。CodeBuild が Git でクローンする | `git log` やタグを使うビルド |

- **例:** ビルドで `git describe --tags` を使い、`v1.4.2` のようなバージョンを作るなら `CODEBUILD_CLONE_REF` にします。`CODE_ZIP` には `.git` の情報がないので、このコマンドは失敗します。
- **誤ると:** `CODEBUILD_CLONE_REF` は後続が CodeBuild のときだけ使えます。CodeBuild のサービスロールにも、接続を使う権限を追加します。

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

- **`branches.includes` の例:** `release/**` は `release/1.4` と `release/2026/10` に一致します。`main` には一致しません。
- **`filePaths.excludes` の例:** 上の設定で `services/orders/README.md` だけを変えても起動しません。
- **Git タグの例:** `push: [{tags: {includes: ["v*"]}}]` なら、`v1.4.2` のプッシュで起動します。
- **上限の例:** `includes` と `excludes` はそれぞれ 8 個までです。1 つのソースアクションに置けるトリガーは 1 つです。
- **`DetectChanges` との関係:** フィルター付きのトリガーを追加すると、アクションの変更検知は `false` の扱いになります。この場合の起動はトリガーが担います。トリガーがなく `false` なら、コミットでは起動しません。
- **誤ると:** ファイルパスのフィルターがあると、ブランチを初めてプッシュしたときはパイプラインが動きません。変更したファイルの一覧を取得できないためです。プッシュと PR のトリガーが重なると、PR のマージで 2 回動くことがあります。

### 手動承認 {#manual-approval}

Approval アクションを置くと、そこでパイプラインが止まります。

- 承認すると次へ進む
- 却下、または **7 日(既定)以内に応答がないと**アクション失敗と同じ扱いになる
- 同じリージョンの SNS トピックへ通知し、確認用 URL とコメントを付けられる
- 承認者には `codepipeline:PutApprovalResult` の権限が必要

**手動承認の設定**: 設定項目は、SNS トピックの ARN、`CustomData`(コメント)、`ExternalEntityLink`(確認用 URL)です。承認アクションの中で `#{...}` の変数を使えます。

```json
"configuration": {
  "NotificationArn": "arn:aws:sns:ap-northeast-1:111122223333:release-approval",
  "ExternalEntityLink": "https://staging.example.com",
  "CustomData": "コミット #{SourceVariables.CommitId} を確認してください"
}
```

- **期限の例:** 既定なら、10 月 1 日 9 時に止まった承認は、10 月 8 日 9 時までに応答がなければ失敗です。`timeoutInMinutes: 1440` なら 1 日で失敗です。
- **却下の例:** 却下はアクションの失敗と同じなので、次のステージへ進みません。
- **`PutApprovalResult` の例:** 承認者のロールに、`Resource` を `arn:aws:codepipeline:ap-northeast-1:111122223333:orders/Approval/Manual` に絞って許可すると、このアクションだけ承認できます。
- **誤ると:** サービスロールに SNS への `sns:Publish` がないと、通知が届きません。

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

- **環境ごとの設定の例:** `ParameterOverrides` に `{"Stage": "prod"}` を渡し、同じテンプレートを別のスタックに適用します。
- **別アカウントの例:** パイプラインのアカウント `111122223333` からデプロイ先のロールを引き受けます。既定の AWS 管理キーではデプロイ先のアカウントが成果物を復号できないので、カスタマー管理キーを使い、キーポリシーとバケットポリシーで許可します。
- **別リージョンの例:** 東京のパイプラインから大阪へデプロイするなら、大阪にもアーティファクトバケットを置きます。
- **誤ると:** KMS キーをエイリアスで指定すると、別アカウントからは解決できません。キー ID か ARN を指定します。

### ステージのロールバック {#pipeline-rollback}

CodePipeline は、以前に成功した実行の版を使ってステージを戻せます。

| 方法 | 内容 |
|---|---|
| 手動 | コンソールまたは `RollbackStage` API |
| 失敗時に自動 | ステージの On Failure 条件で結果を Rollback にする |
| 成功後の確認で戻す | On Success 条件のルールで結果を Rollback にする |

- **手動の例:** 実行 ID を指定して `Prod` を戻します。

```bash
aws codepipeline rollback-stage --pipeline-name orders --stage-name Prod \
  --target-pipeline-execution-id <前回成功した実行 ID>
```

- **使われる内容の例:** 戻す先の実行の成果物と変数を使います。Git の `main` が進んでいても、リビルドはしません。
- **誤ると:** ソースのステージは戻せません。パイプラインの構造を変える前の実行にも戻せません。ロールバックの実行を戻す先にはできません。

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

ルールごとの例です。

- **`CloudWatchAlarm` の例:** `AlarmName: web-5xx`、`WaitTime: 20` で、状態の変化を 20 分待ってから判定します。
- **`DeploymentWindow` の例:** `Cron: 0 0 9-17 ? * MON-FRI *` は、月曜から金曜の日中に配置を許します。`TimeZone` を書かないと UTC です。`TimeZone` なしで日本時間の 9 時を意図すると、9 時間ずれます。
- **`VariableCheck` の例:** `Variable: #{SourceVariables.BranchName}`、`Operator: EQ`、`Value: main` です。
- **`LambdaInvoke` の例:** 関数で今日のリリース凍結の有無を読み、凍結中なら失敗を返します。
- **`CodeBuild`、`Commands` の例:** `Prod` に入る前に `./smoke.sh` を実行し、失敗なら入りません。
- **Entry の `Fail` の例:** アラームが `ALARM` なら、ステージに入らず失敗します。
- **Entry の `Skip` の例:** `VariableCheck` で `feature/*` ならステージを飛ばします。`Skip` で使えるルールは `LambdaInvoke` と `VariableCheck` だけです。
- **On Failure の例:** `Prod` のデプロイが失敗すると `Rollback` します。自動の再試行とは併用できません。
- **On Success の `Fail` の例:** デプロイは成功したがアラームが鳴ったときに、ステージを失敗にして次へ進ませません。

ロールバックの実行は新しい実行として記録され、履歴には `rollback` の種類で表示されます。

## CodeArtifact {#codeartifact}

[:material-certificate: DVA](../courses/dva/services.md){ .exam-badge .exam-associate } [:material-certificate: MLA](../courses/mla/services.md){ .exam-badge .exam-associate } [:material-star-circle: DOP](../courses/dop/services.md){ .exam-badge .exam-professional } [:material-star-circle: AIP](../courses/aip/services.md){ .exam-badge .exam-professional }

**提供単位:** リージョン。ドメインとリポジトリはリージョンごとに作り、VPC の外にあります（[提供単位の一覧](resource-scope.md)）。VPC からはインターフェイスエンドポイントでも接続できます。

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

**ドメインの例**: `frontend` と `backend` の 2 つのリポジトリが同じドメイン `my-org` にあり、どちらも `lodash@4.17.21` を取得したとします。リポジトリには 2 つ見えますが、アセットの実体はドメイン内に 1 つだけ保存されます。ドメインを `dev` と `prod` に分けると、この重複排除は効きません。AWS も、本番用のドメインは組織で 1 つにすることを推奨しています。

**暗号化の例**: `aws codeartifact create-domain --domain my-org --encryption-key arn:aws:kms:ap-northeast-1:111122223333:key/1234abcd-12ab-34cd-56ef-1234567890ab` のように指定します。ドメイン内のアセットとメタデータは 1 つのキーで暗号化されるので、リポジトリごとにキーを管理する必要はありません。対応するのは対称キーだけで、非対称キーは使えません。

**直接のアップストリームの例**: `--upstreams` に書いた順が優先順位です。

```bash
aws codeartifact update-repository --domain my-org --repository app \
  --upstreams repositoryName=internal repositoryName=npm-store
```

この設定で `app` が `react@19.0.0` を持っていなければ、先に `internal` を探し、なければ `npm-store` を探します。見つかった時点で探索は止まります。直接のアップストリームは 10 個までで、連なった先を含めて探索するのは 25 個までです。

**外部接続の例**: `npm-store` にだけ npmjs への外部接続を付け、他のリポジトリは `npm-store` をアップストリームにします。チームごとのリポジトリに外部接続を付けると、取得の経路が分かれ、同じパッケージを別々に取り込むことになります。

**認証トークンの例**: CodeBuild のビルドが最長 30 分なら、`--duration-seconds 3600` で足ります。900 秒（15 分）では、後半の `npm install` が認証エラーになります。

**権限の例**: トークンの発行には `codeartifact:GetAuthorizationToken` に加えて `sts:GetServiceBearerToken` も必要です。後者が足りないと、`aws codeartifact login` の時点で失敗します。

**上限**: 代表的な既定値は次のとおりです。

| 項目 | 既定値 | 引き上げ |
|---|---|---|
| アカウントあたりのドメイン | 10 | 可能 |
| ドメインあたりのリポジトリ | 1,000 | 可能 |
| アセットのファイルサイズ | 5 GB | 可能 |
| パッケージバージョンあたりのアセット | 350 | 不可 |
| 探索するアップストリーム | 25 | 不可 |

**アップストリームと外部接続の違い**: アップストリームは同じドメインの別リポジトリを見る設定です。外部接続は npmjs や PyPI などの公開リポジトリを見る設定です。取得したパッケージは下流のリポジトリに保持されます。

**パッケージオリジンコントロール**: パッケージごとに、直接の公開とアップストリームからの取り込みを `ALLOW` か `BLOCK` で制御します。社内パッケージと同名の公開パッケージを取り込む、依存関係かく乱を防げます。

既定値は、最初のバージョンの入り方で決まります。パッケージグループの制限がすべて `ALLOW` の場合です。

| 最初のバージョン | Publish | Upstream | 例 |
|---|---|---|---|
| 直接公開した | `ALLOW` | `BLOCK` | 社内の `@my-org/utils` |
| 公開リポジトリから取り込んだ | `BLOCK` | `ALLOW` | npmjs の `lodash` |
| 2022年5月ごろより前からある | `ALLOW` | `ALLOW` | 古いパッケージ。手動で見直す |

- **例:** `lodash` に社内で修正を加えた `4.17.21-patch.1` を公開したいとします。既定は `Publish: BLOCK` なので、公開は拒否されます。`Publish: ALLOW` に変えて公開し、新しい公開版を取り込まないなら `Upstream: BLOCK` にします。
- **誤ると:** 社内パッケージを `Upstream: ALLOW` に変えると、npmjs に公開された同名の `99.0.0` が取り込まれて、最新版として選ばれるおそれがあります。

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
| インターネットに出られない VPC でビルドする | 向いている。インターフェイス VPC エンドポイントで接続し、公開パッケージは CodeArtifact 経由で取得する。Python と Swift 以外は、アセットの取得に S3 ゲートウェイエンドポイントも要る |
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

**提供単位**: アプリはリージョン単位で作り、VPC の外にあります（[2 つの軸](resource-scope.md#two-axes)）。

- **自動検出の例:** パターンが `release*` なら `release-1.4` が自動でデプロイされます。`*` は全ブランチです。`release*, feature*` と複数も書けます。
- **Web プレビューの例:** PR #12 に一意の URL が付き、レビュアーはマージ前に動きを確認します。
- **環境変数の例:** `API_URL` を `main` では `https://api.example.com`、`develop` では `https://dev-api.example.com` にします。
- **クォータの計算例:** 本番と検証の 2 ブランチ、機能ブランチ 40 本、開いている PR 8 本で 50 です。次の PR のプレビューは作れません。増やすこともできません。

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

- **`artifacts.baseDirectory` の例:** `npm run build` の出力が `build/` なのに `dist` と書くと、公開するファイルが見つかりません。
- **`cache.paths` の例:** `node_modules/**/*` で 2 回目以降の `npm ci` を速くします。プロジェクトのルートの外は指定できません。サイズは 5 GB までです。
- **`USER_DISABLE_TESTS` の例:** 全ブランチで `true` にすると、テストの手順を飛ばします。特定のブランチだけ飛ばすなら、全体を `false` にして、そのブランチだけ `true` に上書きします。
- **`AWS_BRANCH` の例:** `if [ "$AWS_BRANCH" = "main" ]; then npm run build:prod; fi` のように分岐します。
- **`AWS_PULL_REQUEST_SOURCE_BRANCH` の例:** `feature/login` から `main` への PR のプレビューでは、値が `feature/login` です。
- **ブランチのアクセス制御の例:** `develop` にユーザー名とパスワードを設定し、公開前の画面を社外に見せません。ブランチとグローバルの両方にあれば、ブランチの設定が優先です。
- **誤ると:** `NEXT_PUBLIC_API` のようなフロントエンド用の変数に API キーを入れると、ブラウザに配信されます。

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

- **Lambda のエイリアスの例:** `staging` がバージョン 7、`prod` がバージョン 6 です。ステージングで確かめた後、下のコマンドで `prod` を 7 へ向けます。コードはビルドし直しません。
- **イメージタグの例:** 本番のタスク定義は `my-app:git-abc123` を指します。`latest` を指すと、何が動くかがプッシュの時点で変わります。
- **API Gateway の例:** ステージ変数 `lambdaAlias` を `dev` と `prod` で変え、同じ API の定義から別のエイリアスを呼びます。
- **CloudFormation の例:** 同じテンプレートから `orders-staging` と `orders-prod` の 2 つのスタックを作ります。

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

10 台の EC2 と 1,000 リクエスト毎秒の Web アプリで比べます。

| 戦略 | 更新中の様子 | 新版に当たるリクエスト |
|---|---|---|
| 一括 | 10 台を同時に更新。処理能力が一時的に落ちる | すぐに全部 |
| ローリング(2 台ずつ) | 8 台で処理を続ける | 2 台分ずつ増える |
| Blue/Green | 20 台が一時的に動く | 切り替えで一度に全部 |
| カナリア(10%、5 分) | 新旧が同時に動く | 最初の 5 分は毎秒 100 件 |
| 線形(毎分 10%) | 新旧が同時に動く | 毎分、毎秒 100 件ずつ増える |

- **誤ると:** 新版と旧版を同時に動かせないアプリに、ローリングやカナリアを選ぶと、更新中に片方の版でエラーになります。たとえば、新版だけが読める形式でセッションを保存する場合です。

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

- **CodeDeploy の例:** デプロイ ID `d-EXAMPLE` が失敗すると、前のリビジョンを新しい ID で配布します。
- **Lambda の例:** `aws lambda update-alias --function-name orders --name prod --function-version 6` で、ビルドし直さずに戻せます。
- **API Gateway の例:** ステージの `deploymentId` を前のデプロイへ戻します。
- **ECS の例:** `aws ecs update-service --cluster prod --service web --task-definition web:12` で前のリビジョンに戻します。
- **スキーマの例:** 列を削除する変更を先に出すと、旧版に戻せません。新しい列を足し、新旧の両方で動く版を出した後、次のリリースで古い列を消します。

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

- **切り分けの例:** パイプラインの `Deploy` が赤いなら、リンクからデプロイ `d-EXAMPLE` を開きます。`ValidateService` が失敗なら、インスタンスの `scripts.log` を読みます。`curl: (7) Failed to connect` なら、アプリが起動していないと分かります。
- **`DownloadBundle` の例:** インスタンスプロファイルに `s3:GetObject` がないと、`AccessDenied` のログが出ます。
- **`AllowTraffic` の例:** ヘルスチェックのパスが `/health` なのに `/` を見ていて、`/` が 404 を返すと、ターゲットが正常になりません。
- **`file already exists` の例:** 手で置いた `index.html` が配置先にあると起きます。`--file-exists-behavior OVERWRITE` を付けます。

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
| 手動承認 | 既定 7 日(5 分〜60 日に変更可) |
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
| 承認されないまま放置すると | 既定で 7 日後に失敗扱い |
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

# IaC（CloudFormation / SAM / CDK / CLI）

インフラをコードで定義し、同じ構成を繰り返し安全に作るための道具です。CloudFormation が土台で、サーバーレスなら SAM、プログラミング言語で書くなら CDK を選びます。

[![SAM でのデプロイの流れ](../assets/diagrams/iac-sam-deploy.png)](../assets/diagrams/iac-sam-deploy.png)

## どれを使うか {#choosing}

| ツール | 書き方 | 向いている場面 |
|---|---|---|
| CloudFormation | YAML / JSON | あらゆる AWS リソースを宣言的に管理 |
| SAM | CloudFormation の拡張 YAML | Lambda、API Gateway などサーバーレス構成 |
| CDK | TypeScript、Python など | ループや条件を使い、抽象化して再利用したい |
| AWS CLI | コマンド | API の単発実行、スクリプト、確認 |
| CloudShell | ブラウザ上のシェル | 環境構築なしで CLI を使う |

SAM も CDK も、最終的には CloudFormation のテンプレートとしてデプロイされます。

## CloudFormation テンプレート {#cloudformation-template}

### セクション {#template-sections}

必須は `Resources` だけです。

| セクション | 役割 |
|---|---|
| `AWSTemplateFormatVersion` | テンプレート形式のバージョン |
| `Description` | 説明 |
| `Metadata` | 追加情報 |
| `Parameters` | デプロイ時に渡す値 |
| `Rules` | パラメータの検証 |
| `Mappings` | キーと値の固定の対応表 |
| `Conditions` | リソースを作るかどうかの条件 |
| `Transform` | マクロの適用。SAM もこれを使う |
| `Resources` | 作成するリソース（必須） |
| `Outputs` | スタックの出力値 |

```yaml
AWSTemplateFormatVersion: "2010-09-09"
Description: Orders table

Parameters:
  Stage:
    Type: String
    AllowedValues: [dev, staging, prod]
    Default: dev

Mappings:
  StageConfig:
    dev:
      LogRetention: 7
    staging:
      LogRetention: 30
    prod:
      LogRetention: 365

Conditions:
  IsProd: !Equals [!Ref Stage, prod]

Resources:
  OrdersTable:
    Type: AWS::DynamoDB::Table
    DeletionPolicy: Retain
    UpdateReplacePolicy: Retain
    Properties:
      BillingMode: PAY_PER_REQUEST
      AttributeDefinitions:
        - AttributeName: pk
          AttributeType: S
      KeySchema:
        - AttributeName: pk
          KeyType: HASH
      PointInTimeRecoverySpecification:
        PointInTimeRecoveryEnabled: !If [IsProd, true, false]

  AppLogs:
    Type: AWS::Logs::LogGroup
    Properties:
      LogGroupName: !Sub "/myapp/${Stage}"
      RetentionInDays: !FindInMap [StageConfig, !Ref Stage, LogRetention]

Outputs:
  TableName:
    Value: !Ref OrdersTable
    Export:
      Name: !Sub "${Stage}-orders-table"
```

### パラメータ {#parameters}

- `Type`: `String`、`Number`、`List<Number>`、`CommaDelimitedList` など
- `AWS::EC2::VPC::Id` のような AWS 固有の型は、値を検証してくれる
- `AWS::SSM::Parameter::Value<String>` で Parameter Store の値を読める
- `AllowedValues`、`AllowedPattern`、`MinLength` などで入力を制限する
- `NoEcho: true` で値を画面やログに表示しない

シークレットをパラメータの既定値に書いてはいけません。動的参照を使います。

```yaml
MasterUserPassword: "{{resolve:secretsmanager:my-db-secret:SecretString:password}}"
```

### マッピングと条件 {#mappings-conditions}

`Mappings` はテンプレート内の固定の表で、`!FindInMap` で読みます。リージョンや環境ごとの値に使います。

`Conditions` は `!Equals`、`!And`、`!Or`、`!Not` で定義します。使い方は 2 つです。

- リソースや出力に `Condition: IsProd` と書き、作るかどうかを決める
- プロパティで `!If [IsProd, 値A, 値B]` として値を切り替える

### 出力とエクスポート {#outputs-exports}

`Outputs` の値に `Export` を付けると、別のスタックから `!ImportValue` で参照できます。

- エクスポート名はアカウントとリージョン内で一意
- `Fn::ImportValue` が参照できるのは同じアカウントとリージョンのみ
- 参照されている間は、エクスポート元のスタック削除や値の変更ができない
- 別アカウントや別リージョンのスタック出力は `Fn::GetStackOutput` で参照できる

### 組み込み関数 {#intrinsic-functions}

| 関数 | 用途 | 例 |
|---|---|---|
| `!Ref` | パラメータの値、リソースの主な識別子 | `!Ref Stage` |
| `!GetAtt` | リソースの属性 | `!GetAtt Table.Arn` |
| `!Sub` | 文字列への埋め込み | `!Sub "${AWS::StackName}-logs"` |
| `!Join` | 連結 | `!Join ["-", [a, b]]` |
| `!Select` / `!Split` | リストの要素選択、文字列の分割 | `!Select [0, !GetAZs ""]` |
| `!FindInMap` | マッピングの参照 | `!FindInMap [Map, Key, Name]` |
| `!ImportValue` | 他スタックのエクスポートの参照 | `!ImportValue dev-orders-table` |
| `!GetAZs` | リージョンの AZ 一覧 | `!GetAZs ""` |
| `!If` など | 条件 | `!If [IsProd, 3, 1]` |
| `!Base64` | Base64 変換（EC2 のユーザーデータ） | `!Base64 ...` |

擬似パラメータの `AWS::Region`、`AWS::AccountId`、`AWS::StackName` は `!Ref` や `!Sub` で使えます。

### リソースの属性: DeletionPolicy {#deletion-policy}

| 値 | スタック削除時の動作 |
|---|---|
| `Delete` | 削除する（通常の既定） |
| `Retain` | 残す。全リソースで指定可能 |
| `RetainExceptOnCreate` | 残す。ただし作成時のロールバックでは削除する |
| `Snapshot` | スナップショットを取って削除する（EBS、RDS など対応リソースのみ） |

既定は `Delete` ですが、`AWS::RDS::DBCluster` と、`DBClusterIdentifier` を指定しない `AWS::RDS::DBInstance` の既定は `Snapshot` です。

`DeletionPolicy` はテンプレートからリソースを外す更新でも効きます。一方、プロパティ変更による**置き換え**では効きません。置き換えで元のリソースを残すには `UpdateReplacePolicy` を使います。

他に `DependsOn`（作成順の指定）、`CreationPolicy`（起動完了の信号を待つ）、`UpdatePolicy`（Auto Scaling グループの更新方法）があります。

## テンプレートの更新と変更の確認 {#updating-stacks}

### 既存テンプレートの更新 {#update-templates}

更新時は、変更するプロパティごとに動作が決まっています。

| 更新動作 | 影響 |
|---|---|
| 中断なし | 物理 ID は同じで止まらない |
| 一時的な中断 | 再起動などが起きる |
| 置き換え | 新しいリソースを作り、古いものを消す。物理 ID が変わる |

更新時の注意点です。

- リソースの**論理 ID を変えると**、削除と新規作成として扱われる
- 固定の名前（`TableName` など）を付けていると、置き換えで名前が衝突して失敗する
- 本番では変更セットで置き換えの有無を確認してから実行する

### 変更セット {#change-sets}

スタックへの影響を実行前に確認する仕組みです。作成しただけでは何も変わらず、実行して初めて反映されます。`Replacement` の列で置き換えの有無が分かります。

```bash
aws cloudformation create-change-set \
  --stack-name orders-prod \
  --change-set-name release-142 \
  --template-body file://template.yaml \
  --parameters ParameterKey=Stage,ParameterValue=prod

aws cloudformation describe-change-set \
  --stack-name orders-prod --change-set-name release-142

aws cloudformation execute-change-set \
  --stack-name orders-prod --change-set-name release-142
```

変更セットは更新の成功を保証しません。実行時の条件による失敗は起こりえます。

### ドリフト検出 {#drift}

手作業の変更などで、実際の設定がテンプレートとずれた状態を検出します。

- `detect-stack-drift` で開始し、`describe-stack-resource-drifts` で差分を確認する
- 対応していないリソースは `NOT_CHECKED` になる
- 明示的に設定した値だけが比較の対象で、プロパティの既定値は対象外
- 親スタックの検出では、ネストされたスタックは検出されない。個別に実行する

ドリフトを検出するだけで自動修復はしません。差分を考慮して更新する機能として、ドリフト対応の変更セット（drift-aware change sets）もあります。

### ネストされたスタックと StackSets {#nested-stacks-stacksets}

| 機能 | 用途 |
|---|---|
| ネストされたスタック | 共通の構成を部品にする。`AWS::CloudFormation::Stack` で別テンプレートを呼ぶ |
| クロススタック参照 | 独立したスタック間で値を共有する（`Export` と `ImportValue`） |
| StackSets | 1 回の操作で複数のアカウントとリージョンへ展開する |

部品の再利用ならネスト、ライフサイクルの違うスタック間の共有ならエクスポートです。

## スタックのロールバックと失敗 {#stack-failures}

### ロールバックの既定動作 {#stack-rollback}

作成や更新が失敗すると、既定で自動的に元へ戻します。

| 操作 | 失敗後の状態 | 次にできること |
|---|---|---|
| 作成の失敗 | `ROLLBACK_COMPLETE` | 更新はできない。削除して作り直す |
| 更新の失敗 | `UPDATE_ROLLBACK_COMPLETE` | 修正して再度更新 |
| 更新のロールバックも失敗 | `UPDATE_ROLLBACK_FAILED` | `continue-update-rollback` |

開発時は「正常にプロビジョニングされたリソースを保持する」オプションを使うと、成功したリソースを残し、失敗した場所から再開できます。

### ロールバックトリガー {#rollback-triggers}

スタック操作の間と、完了後の監視時間に CloudWatch アラームを見張ります。アラームが `ALARM` になるとスタック全体を戻します。

- トリガーは最大 5 個
- 監視時間は 0 から 180 分（既定は 0）
- 指定できるのはメトリクスアラームと複合アラーム
- `INSUFFICIENT_DATA` では戻さない。戻すにはアラームで欠落データを `breaching` として扱う

```bash
aws cloudformation update-stack \
  --stack-name orders-prod \
  --template-body file://template.yaml \
  --rollback-configuration "RollbackTriggers=[{Arn=<アラームの ARN>,Type=AWS::CloudWatch::Alarm}],MonitoringTimeInMinutes=10"
```

### よくある失敗と対処 {#common-failures}

まずスタックイベントで**最初に**失敗したリソースの理由を読みます。後続の失敗はその連鎖であることが多いためです。

```mermaid
flowchart TD
    A[スタック更新が失敗] --> B[自動ロールバック開始]
    B --> C{元に戻せたか}
    C -->|はい| D[UPDATE_ROLLBACK_COMPLETE]
    C -->|いいえ| E[UPDATE_ROLLBACK_FAILED]
    E --> F[原因を直す]
    F --> G[continue-update-rollback]
    G --> H{直せないリソースがあるか}
    H -->|いいえ| D
    H -->|はい| I["resources-to-skip を指定して実行"]
    I --> D
```

| 症状 | 原因 | 対処 |
|---|---|---|
| `UPDATE_ROLLBACK_FAILED` | 戻す先のリソースが手動で削除された、権限不足など | 原因を直して `continue-update-rollback`。難しければ `--resources-to-skip` |
| `InsufficientCapabilities` | IAM リソースやマクロの承認なし | `--capabilities CAPABILITY_IAM`、`CAPABILITY_NAMED_IAM`、`CAPABILITY_AUTO_EXPAND` |
| `already exists` | 固定の名前が衝突 | 名前を指定せず自動生成に任せる |
| `DELETE_FAILED` | S3 バケットが空でない、依存リソースが残っている | 中身を消す、依存を外す、`--retain-resources` |
| エクスポートを消せない | 他スタックが `ImportValue` で参照中 | 参照側を先に更新 |
| `ROLLBACK_COMPLETE` で更新不可 | 初回作成の失敗 | スタックを削除して作り直す |
| `No updates are to be performed` | 差分なし | テンプレートやパラメータを確認 |
| `Circular dependency` | リソースの相互参照 | 参照の向きを整理する |
| `Template format error` | 構文エラー | `validate-template`、`sam validate --lint` |

!!! warning "スタック外の変更を避ける"
    スタックのリソースを手動で消すと、ロールバックが失敗する原因になります。変更はテンプレート経由で行い、重要なスタックは削除保護も有効にします。

## SAM {#sam}

サーバーレス向けの CloudFormation 拡張です。短い記述から、デプロイ時に IAM ロールなどを含む CloudFormation リソースへ展開されます。

### テンプレート {#sam-template}

`Transform: AWS::Serverless-2016-10-31` が SAM テンプレートの目印です。`Globals` で共通設定をまとめられます。

| リソース | 内容 |
|---|---|
| `AWS::Serverless::Function` | Lambda 関数 |
| `AWS::Serverless::Api` | REST API |
| `AWS::Serverless::HttpApi` | HTTP API |
| `AWS::Serverless::SimpleTable` | 単純な DynamoDB テーブル |
| `AWS::Serverless::LayerVersion` | Lambda レイヤー |
| `AWS::Serverless::StateMachine` | Step Functions |

```yaml
AWSTemplateFormatVersion: "2010-09-09"
Transform: AWS::Serverless-2016-10-31

Parameters:
  Stage:
    Type: String
    Default: dev

Globals:
  Function:
    Runtime: python3.12
    Timeout: 10
    Tracing: Active

Resources:
  OrdersFunction:
    Type: AWS::Serverless::Function
    Properties:
      CodeUri: src/orders/
      Handler: app.handler
      Environment:
        Variables:
          STAGE: !Ref Stage
      Events:
        CreateOrder:
          Type: Api
          Properties:
            Path: /orders
            Method: post
      AutoPublishAlias: live
      DeploymentPreference:
        Type: Canary10Percent5Minutes
        Alarms:
          - !Ref OrdersErrorsAlarm
        Hooks:
          PreTraffic: !Ref PreTrafficFunction
          PostTraffic: !Ref PostTrafficFunction
  # OrdersErrorsAlarm とフック関数の定義は省略
```

### プロジェクトのディレクトリ構成 {#project-structure}

`sam init` が作る形を基本に、関数のコード、イベント、テストを分けます。

```text
my-app/
├── template.yaml        # SAM テンプレート
├── samconfig.toml       # デプロイ設定（環境別）
├── src/
│   └── orders/
│       ├── app.py       # ハンドラー
│       └── requirements.txt
├── events/
│   └── create-order.json  # テストイベント
└── tests/
    ├── unit/
    └── integration/
```

`sam build` は `CodeUri` ごとの依存関係（`requirements.txt`、`package.json` など）を解決し、`.aws-sam/build` に成果物をまとめます。関数ごとにディレクトリを分けると、パッケージが小さくなります。

### SAM CLI のコマンド {#sam-cli}

| コマンド | 用途 |
|---|---|
| `sam init` | プロジェクトの雛形を作る |
| `sam validate` | テンプレートの検証。`--lint` で詳しく確認 |
| `sam build` | 依存関係の解決とビルド |
| `sam deploy` | パッケージしてデプロイ。`--guided` で対話設定 |
| `sam local invoke` | 関数を 1 回ローカル実行（Docker が必要） |
| `sam local start-api` | API をローカルの HTTP サーバーで起動 |
| `sam local start-lambda` | Lambda のローカルエンドポイントを起動 |
| `sam local generate-event` | サービス別のサンプルイベントを生成 |
| `sam remote invoke` | クラウド上のリソースを呼び出す |
| `sam remote test-event` | 共有テストイベントを管理する |
| `sam sync` | 開発環境へ素早く反映 |
| `sam logs` | 関数のログを取得 |

```bash
sam validate --lint
sam build
sam local invoke OrdersFunction -e events/create-order.json
sam local start-api
sam deploy --guided
```

### DeploymentPreference によるカナリア {#deployment-preference}

`AutoPublishAlias` と `DeploymentPreference` を組み合わせると、裏で CodeDeploy が作られ、段階的にトラフィックを移します。

| 項目 | 内容 |
|---|---|
| `AutoPublishAlias` | コード変更時に新バージョンを発行し、エイリアスを更新 |
| `Type` | `Canary10Percent5Minutes`（10、15、30 分）、`Linear10PercentEvery1Minute`（2、3、10 分）、`AllAtOnce` |
| `Alarms` | 発火すると自動ロールバック |
| `Hooks` | `PreTraffic` と `PostTraffic` の検証関数 |

```mermaid
sequenceDiagram
    participant S as SAM / CloudFormation
    participant C as CodeDeploy
    participant H as フック関数
    participant A as エイリアス live
    S->>C: 新バージョンのデプロイを開始
    C->>H: PreTraffic を実行
    H-->>C: Succeeded を報告
    C->>A: 10% を新バージョンへ
    Note over C,A: 5 分間アラームを監視
    C->>A: 残り 90% を移す
    C->>H: PostTraffic を実行
    H-->>C: Succeeded を報告
```

戦略全体の比較は [CI/CD](cicd.md) を参照してください。

### 別のステージへのデプロイ {#deploy-stages}

同じテンプレートを、パラメータとスタック名を変えて配布します。`samconfig.toml` に環境ごとの設定を書き、`--config-env` で選びます。

```toml
version = 0.1

[staging.deploy.parameters]
stack_name = "orders-staging"
resolve_s3 = true
capabilities = "CAPABILITY_IAM"
parameter_overrides = "Stage=staging"

[prod.deploy.parameters]
stack_name = "orders-prod"
resolve_s3 = true
capabilities = "CAPABILITY_IAM"
parameter_overrides = "Stage=prod"
confirm_changeset = true
```

```bash
sam build
sam deploy --config-env staging

# 設定ファイルを使わずに指定する場合
sam deploy --stack-name orders-staging --resolve-s3 \
  --capabilities CAPABILITY_IAM \
  --parameter-overrides Stage=staging
```

既存環境への更新も同じコマンドです。SAM が変更セットを作り、差分を適用します。`confirm_changeset` を有効にすると実行前に確認できます。

## テストの書き方と実行 {#testing}

### テストイベントの作成 {#test-events}

Lambda のテストは JSON のイベントを渡して行います。`sam local generate-event` で雛形を作れます。

```bash
sam local generate-event s3 put --bucket my-bucket --key input.csv > events/s3-put.json
sam local generate-event sqs receive-message > events/sqs.json
sam local generate-event apigateway aws-proxy > events/api.json
```

API Gateway のプロキシ統合で受け取るイベントの主要部分は次のような形です。

```json
{
  "httpMethod": "POST",
  "path": "/orders",
  "headers": {"Content-Type": "application/json"},
  "queryStringParameters": null,
  "pathParameters": null,
  "body": "{\"item\": \"book\", \"quantity\": 1}",
  "isBase64Encoded": false
}
```

`body` は JSON 文字列である点に注意します。SQS イベントは `Records` の配列です。

```json
{
  "Records": [
    {
      "messageId": "19dd0b57-b21e-4ac1-bd88-01bbb068cb78",
      "body": "{\"orderId\": \"o-1\"}",
      "eventSource": "aws:sqs"
    }
  ]
}
```

| 実行場所 | 方法 |
|---|---|
| ローカル | `sam local invoke -e events/api.json` |
| クラウド上の Lambda | `sam remote invoke`、コンソールのテストイベント |
| クラウド上の API Gateway | コンソールのメソッドテスト、`aws apigateway test-invoke-method` |

### 単体テスト {#unit-tests}

ハンドラーの中身を外部サービスから切り離して検証します。AWS への呼び出しは `botocore.stub.Stubber` やモックに置き換えます。

```python
import json
from src.orders import app

def test_create_order_returns_201(monkeypatch):
    monkeypatch.setattr(app, "save_order", lambda order: "o-1")
    event = {"body": json.dumps({"item": "book", "quantity": 1})}

    response = app.handler(event, None)

    assert response["statusCode"] == 201
    assert json.loads(response["body"])["orderId"] == "o-1"
```

### デプロイ済みコードの結合テスト {#integration-tests}

テスト用スタックへデプロイし、実際の AWS サービスで確認します。スタックの出力から URL を取得すると、環境に依存しないテストになります。

```python
import boto3
import requests

def get_output(stack, key):
    cfn = boto3.client("cloudformation")
    outputs = cfn.describe_stacks(StackName=stack)["Stacks"][0]["Outputs"]
    return next(o["OutputValue"] for o in outputs if o["OutputKey"] == key)

def test_post_order():
    url = get_output("orders-staging", "ApiUrl")
    response = requests.post(f"{url}/orders", json={"item": "book"}, timeout=10)
    assert response.status_code == 201
```

### イベント駆動アプリのテスト {#event-driven-tests}

非同期処理は呼び出しの応答だけでは検証できません。入口でイベントを発生させ、**出口の結果を待って確認**します。

| 確認対象 | 方法 |
|---|---|
| ハンドラー単体 | 生成したイベント JSON でローカル実行 |
| EventBridge のルール | `aws events test-event-pattern` でパターンの一致を確認 |
| SQS から Lambda | テストキューへ送信し、DynamoDB などの結果をポーリング |
| 失敗時の動作 | 不正なメッセージを送り、DLQ に届くことを確認 |
| 流れ全体 | X-Ray のトレースで経路を確認 |

```python
import json
import time
import boto3

def test_order_is_processed():
    boto3.client("sqs").send_message(
        QueueUrl=QUEUE_URL,
        MessageBody=json.dumps({"orderId": "test-1"}),
    )
    table = boto3.resource("dynamodb").Table(TABLE_NAME)
    for _ in range(10):
        item = table.get_item(Key={"pk": "test-1"}).get("Item")
        if item:
            break
        time.sleep(3)
    assert item["status"] == "DONE"
```

## CDK {#cdk}

プログラミング言語でインフラを定義し、CloudFormation テンプレートを生成します。CDK v2 が現行で、v1 のサポートは終了しています。

### コンストラクト {#cdk-constructs}

| レベル | 内容 | 例 |
|---|---|---|
| L1 | CloudFormation リソースと 1 対 1。名前は `Cfn` で始まる | `CfnBucket` |
| L2 | 既定値と便利なメソッドを備えた抽象化 | `s3.Bucket`、`bucket.grant_read(fn)` |
| L3 | 複数リソースをまとめたパターン | `ecs_patterns.ApplicationLoadBalancedFargateService` |

構造は App → Stack → Construct の階層です。

```python
from aws_cdk import Stack, aws_lambda as lambda_, aws_s3 as s3
from constructs import Construct

class OrdersStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)
        bucket = s3.Bucket(self, "Reports", versioned=True)
        fn = lambda_.Function(
            self, "Handler",
            runtime=lambda_.Runtime.PYTHON_3_12,
            handler="app.handler",
            code=lambda_.Code.from_asset("src/orders"),
            environment={"BUCKET": bucket.bucket_name},
        )
        bucket.grant_read(fn)
```

### CDK のコマンド {#cdk-cli}

| コマンド | 用途 |
|---|---|
| `cdk bootstrap` | デプロイに必要な資材をアカウントとリージョンに用意 |
| `cdk synth` | CloudFormation テンプレートを生成 |
| `cdk diff` | デプロイ済みスタックとの差分を表示 |
| `cdk deploy` | デプロイ |
| `cdk destroy` | スタックを削除 |

`cdk deploy` が初めて失敗するときは、`bootstrap` の未実行をまず疑います。

### assertions によるテスト {#cdk-testing}

`aws_cdk.assertions` は、生成されるテンプレートを検証します。AWS へのデプロイは不要です。

```python
import aws_cdk as cdk
from aws_cdk.assertions import Match, Template
from my_app.orders_stack import OrdersStack

def test_lambda_settings():
    app = cdk.App()
    template = Template.from_stack(OrdersStack(app, "TestStack"))

    template.has_resource_properties("AWS::Lambda::Function", {
        "Runtime": "python3.12",
        "Environment": Match.object_like({"Variables": Match.any_value()}),
    })
    template.resource_count_is("AWS::S3::Bucket", 1)
```

| テスト | 内容 |
|---|---|
| 詳細なアサーション | 特定のプロパティやリソース数を確認。`has_resource_properties`、`resource_count_is` |
| スナップショット | 前回のテンプレート全体との差分を検出 |

`has_resource_properties` は既定で部分一致です。`Match` で厳密さを調整できます。

### テンプレートの検証方法のまとめ {#validate-iac}

| ツール | 検証の方法 |
|---|---|
| CloudFormation | `aws cloudformation validate-template`、変更セット、cfn-lint |
| SAM | `sam validate --lint`、`sam local invoke`、`sam local start-api` |
| CDK | `cdk synth`、`cdk diff`、`assertions` によるテスト |

## AWS CLI {#aws-cli}

### プロファイル {#cli-profiles}

設定は `~/.aws/config` と `~/.aws/credentials` に保存します。`config` では `[profile 名前]`、`credentials` では `[名前]` と書きます。

```ini
[default]
region = ap-northeast-1
output = json

[profile staging]
region = ap-northeast-1
sso_session = my-sso
sso_account_id = 000000000000
sso_role_name = Developer
```

```bash
aws s3 ls --profile staging
export AWS_PROFILE=staging
aws sts get-caller-identity   # 今の認証情報を確認する
```

優先順位は、コマンドラインオプション、環境変数、設定ファイルの順です。

### 出力形式 {#cli-output}

| `--output` | 用途 |
|---|---|
| `json` | 既定。プログラムで処理 |
| `yaml` / `yaml-stream` | 読みやすい形式。`yaml-stream` は逐次出力 |
| `text` | タブ区切り。シェルで加工 |
| `table` | 人が読む |
| `off` | 標準出力を抑止。CI で終了コードだけ使う |

### --query で絞り込む {#cli-query}

`--query` は JMESPath で**クライアント側**で結果を絞り込みます。サービス側で絞る `--filters` などとは別です。

```bash
aws ec2 describe-instances \
  --filters "Name=instance-state-name,Values=running" \
  --query "Reservations[].Instances[].{Id:InstanceId,Type:InstanceType}" \
  --output table

aws lambda list-functions \
  --query "Functions[?Runtime=='python3.12'].FunctionName" --output text
```

大量のデータでは、サーバー側で絞れる `--filters` を先に使うほうが効率的です。

### ページネーション {#cli-pagination}

CLI は既定で複数の API 呼び出しを行い、全件を集めて返します。

| オプション | 動作 |
|---|---|
| `--page-size` | 1 回の API 呼び出しの件数を減らす。全件は取得する。タイムアウト対策 |
| `--max-items` | 出力の総数を制限。続きがあれば `NextToken` を表示 |
| `--starting-token` | `NextToken` の続きから取得 |
| `--no-paginate` | 最初の 1 ページだけ取得 |
| `--no-cli-pager` | 出力を `less` などのページャーに渡さない |

```bash
aws s3api list-objects-v2 --bucket my-bucket --max-items 100
aws s3api list-objects-v2 --bucket my-bucket --max-items 100 --starting-token <NextToken>
```

### ドライランで権限を確かめる {#cli-dry-run}

EC2 などの API は `--dry-run` で、実際に変更せず権限を確認できます。

| エラーコード | 意味 |
|---|---|
| `DryRunOperation` | 権限があり、実行すれば成功する見込み |
| `UnauthorizedOperation` | 権限がない |

```bash
aws ec2 run-instances --dry-run --image-id ami-12345678 --instance-type t3.micro
```

すべての API に `--dry-run` があるわけではありません。IAM ポリシーの検証には `aws iam simulate-principal-policy` も使えます。

## CloudShell {#cloudshell}

マネジメントコンソールから起動できるブラウザ上のシェルです。Amazon Linux 2023 ベースで、AWS CLI などが導入済みです。

| 項目 | 内容 |
|---|---|
| 認証 | コンソールのサインイン情報をそのまま使える |
| 永続ストレージ | リージョンごとに `$HOME` へ 1 GB（無料） |
| データ保持 | 最後のセッションから 120 日使わないと削除対象 |
| 非アクティブ時 | 20〜30 分操作がないとセッション終了 |
| 長時間実行 | 約 12 時間でセッション終了 |
| シェル | Bash、PowerShell、Z shell |
| VPC 環境 | VPC 内で起動可能。ただし永続ストレージなし |

## 試験のポイント {#exam-points}

| こう問われたら | 答え |
|---|---|
| テンプレートで必須のセクションは | `Resources` |
| 更新前に影響を確認したい | 変更セット |
| 手動変更によるずれを見つけたい | ドリフト検出 |
| スタック削除後もリソースを残したい | `DeletionPolicy: Retain` |
| 置き換え時に元のリソースを残したい | `UpdateReplacePolicy` |
| 他スタックの出力を使いたい | `Export` と `Fn::ImportValue` |
| `UPDATE_ROLLBACK_FAILED` から回復したい | `continue-update-rollback`、必要なら `--resources-to-skip` |
| 初回作成に失敗して `ROLLBACK_COMPLETE` | スタックを削除して作り直す |
| デプロイ後にアラームで自動で戻したい | ロールバックトリガー（最大 5 個、0〜180 分） |
| IAM を含むテンプレートのエラー | `--capabilities CAPABILITY_IAM` など |
| 複数アカウントへ一括展開 | StackSets |
| SAM テンプレートの目印は | `Transform: AWS::Serverless-2016-10-31` |
| Lambda をカナリアでデプロイしたい | `AutoPublishAlias` と `DeploymentPreference` |
| 関数をローカルで 1 回実行したい | `sam local invoke -e event.json` |
| API をローカルで試したい | `sam local start-api` |
| 別の環境へ同じ SAM アプリを配布したい | `sam deploy --config-env`、`--parameter-overrides` |
| テストイベントの雛形が欲しい | `sam local generate-event` |
| CDK が生成するテンプレートをテストしたい | `assertions` の `Template` |
| CDK でデプロイとの差分を見たい | `cdk diff` |
| CDK の初回デプロイ前に必要なのは | `cdk bootstrap` |
| CLI の結果をクライアント側で絞りたい | `--query` |
| CLI のタイムアウトを避けたい | `--page-size` |
| 権限があるかだけ確認したい | `--dry-run`（`DryRunOperation` なら権限あり） |
| 環境構築なしに CLI を使いたい | CloudShell |

## 関連ページ {#related}

- [CI/CD](cicd.md)
- [Lambda](lambda.md)
- [API Gateway](api-gateway.md)
- [オブザーバビリティ](observability.md)
- [シークレット管理](secrets.md)
- [IAM](iam.md)

## 参考 {#references}

- [CloudFormation template sections](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/template-anatomy.html)
- [Intrinsic function reference](https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/intrinsic-function-reference.html)
- [`DeletionPolicy` attribute](https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/aws-attribute-deletionpolicy.html)
- [Update CloudFormation stacks using change sets](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-changesets.html)
- [Detect unmanaged configuration changes with drift detection](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-stack-drift.html)
- [Roll back your CloudFormation stack on alarm breach with rollback triggers](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-rollback-triggers.html)
- [Choose how to handle failures when provisioning resources](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/stack-failure-options.html)
- [Continue rolling back an update](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-continueupdaterollback.html)
- [Troubleshooting CloudFormation](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/troubleshooting.html)
- [Get exported outputs from a deployed CloudFormation stack](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-stack-exports.html)
- [Split a template into reusable pieces using nested stacks](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-nested-stacks.html)
- [Managing stacks across accounts and Regions with StackSets](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/what-is-cfnstacksets.html)
- [Deploying serverless applications gradually with AWS SAM](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/automating-updates-to-serverless-apps.html)
- [sam deploy](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-cli-command-reference-sam-deploy.html)
- [Introduction to testing with sam local invoke](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/using-sam-cli-local-invoke.html)
- [Introduction to testing with sam local start-api](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/using-sam-cli-local-start-api.html)
- [Introduction to testing with sam local generate-event](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/using-sam-cli-local-generate-event.html)
- [Introduction to testing in the cloud with sam remote invoke](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/using-sam-cli-remote-invoke.html)
- [Test AWS CDK applications](https://docs.aws.amazon.com/cdk/v2/guide/testing.html)
- [AWS CDK Constructs](https://docs.aws.amazon.com/cdk/v2/guide/constructs.html)
- [Using the pagination options in the AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-usage-pagination.html)
- [Filtering AWS CLI output](https://docs.aws.amazon.com/cli/latest/userguide/cli-usage-filter.html)
- [Setting the output format in the AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-usage-output-format.html)
- [Configuration and credential file settings](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html)
- [AWS CloudShell limits](https://docs.aws.amazon.com/cloudshell/latest/userguide/limits.html)

# IaC（CloudFormation / SAM / CDK / CLI）

[:material-sprout: CLF](../courses/clf/services.md){ .exam-badge .exam-foundational } [:material-certificate: SAA](../courses/saa/services.md){ .exam-badge .exam-associate } [:material-certificate: DVA](../courses/dva/services.md){ .exam-badge .exam-associate } [:material-certificate: SOA](../courses/soa/services.md){ .exam-badge .exam-associate } [:material-certificate: DEA](../courses/dea/services.md){ .exam-badge .exam-associate } [:material-certificate: MLA](../courses/mla/services.md){ .exam-badge .exam-associate } [:material-star-circle: SAP](../courses/sap/services.md){ .exam-badge .exam-professional } [:material-star-circle: DOP](../courses/dop/services.md){ .exam-badge .exam-professional } [:material-star-circle: AIP](../courses/aip/services.md){ .exam-badge .exam-professional } [:material-target: ANS](../courses/ans/services.md){ .exam-badge .exam-specialty } [:material-target: SCS](../courses/scs/services.md){ .exam-badge .exam-specialty }

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

- **CloudFormation の例:** VPC、サブネット、RDS をまとめて管理し、YAML でレビューしたい基盤チームに向きます。
- **SAM の例:** Lambda 3 つと API を 40 行ほどで書き、`sam local invoke` で手元で試します。
- **CDK の例:** 同じ構成の S3 バケットを 20 個作るなら、Python の `for` で書けます。テンプレートに直接書くと 20 回繰り返します。
- **AWS CLI の例:** `aws s3 ls` で一覧を確認するだけなら、テンプレートは要りません。
- **CloudShell の例:** 手元の PC に CLI を入れられない環境で、コンソールから `aws sts get-caller-identity` を実行します。

## CloudFormation テンプレート {#cloudformation-template}

[:material-sprout: CLF](../courses/clf/services.md){ .exam-badge .exam-foundational } [:material-certificate: SAA](../courses/saa/services.md){ .exam-badge .exam-associate } [:material-certificate: DVA](../courses/dva/services.md){ .exam-badge .exam-associate } [:material-certificate: SOA](../courses/soa/services.md){ .exam-badge .exam-associate } [:material-certificate: DEA](../courses/dea/services.md){ .exam-badge .exam-associate } [:material-certificate: MLA](../courses/mla/services.md){ .exam-badge .exam-associate } [:material-star-circle: SAP](../courses/sap/services.md){ .exam-badge .exam-professional } [:material-star-circle: DOP](../courses/dop/services.md){ .exam-badge .exam-professional } [:material-star-circle: AIP](../courses/aip/services.md){ .exam-badge .exam-professional } [:material-target: ANS](../courses/ans/services.md){ .exam-badge .exam-specialty } [:material-target: SCS](../courses/scs/services.md){ .exam-badge .exam-specialty }

**提供単位**: スタックはリージョン単位で、CloudFormation 自体は VPC の外にあります（[2 つの軸](resource-scope.md#two-axes)）。スタックが作るリソースの単位は、リソースごとに決まります。

- **例:** 東京で作ったスタックは、東京のコンソールにしか出ません。同じ構成を大阪にも作るなら、大阪にも別のスタックを作ります。

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

### セクションの詳細 {#section-details}

| セクション | 書けるもの | 注意 |
|---|---|---|
| `AWSTemplateFormatVersion` | `2010-09-09` のみ | リテラルで書く。パラメータや関数は不可 |
| `Description` | 0〜1,024 バイトの文字列 | リテラルで書く |
| `Metadata` | 任意の情報 | `AWS::CloudFormation::Interface` でコンソールのパラメータを並べ替えられる |
| `Parameters` | 最大 200 個 | 値は 4,096 バイトまで |
| `Rules` | `RuleCondition`、`Assertions` | パラメータの組み合わせを作成前に検証 |
| `Mappings` | 最大 200 個。2 段階のキー | パラメータ、擬似パラメータ、関数は書けない |
| `Conditions` | `Fn::Equals` などの条件 | パラメータ、他の条件、マッピングを参照できる |
| `Transform` | マクロの一覧。書いた順に処理 | `AWS::Serverless-2016-10-31`、`AWS::Include`、`AWS::LanguageExtensions` など |
| `Resources` | 最大 500 個 | 必須 |
| `Outputs` | 最大 200 個 | `Condition` と `Export` を書ける |

```yaml
Rules:
  ProdNeedsLargeInstance:
    RuleCondition: !Equals [!Ref Stage, prod]
    Assertions:
      - Assert: !Contains [[m7g.large, m7g.xlarge], !Ref InstanceType]
        AssertDescription: "prod では m7g.large 以上を指定してください"
```

**例**: `Stage=prod`、`InstanceType=t3.micro` で作ると、リソースを作る前に検証で失敗し、`AssertDescription` が表示されます。

テンプレートの大きさは、リクエストの本文で 51,200 バイト、S3 経由で 1 MB までです。本文の上限を超えるなら、S3 に置いて `--template-url` か `aws cloudformation package` を使います。

セクションごとの例です。

- **`AWSTemplateFormatVersion` の例:** 値は `"2010-09-09"` だけです。今日の日付に書き換えるとエラーになります。
- **`Description` の例:** `Description: Orders table` です。1,024 バイトを超えるとエラーです。日本語は 1 文字が 3 バイトなので、342 文字で超えます。
- **`Metadata` の例:** `AWS::CloudFormation::Interface` で、コンソールの入力欄を「ネットワーク」「DB」のグループに分けます。動作は変わりません。
- **`Parameters` の例:** `Stage` を `dev` にして作り、`prod` にして別のスタックを作ります。テンプレートは同じです。
- **`Mappings` の例:** 冒頭の `StageConfig` で `Stage` が `prod` なら、`LogRetention` は 365 です。
- **`Conditions` の例:** 冒頭の `IsProd` は、`Stage` が `prod` のときだけ `true` です。
- **`Transform` の例:** `Transform: [AWS::LanguageExtensions, AWS::Serverless-2016-10-31]` なら、`AWS::LanguageExtensions` を先に処理します。
- **`Resources` の例:** 501 個目を書くとエラーです。ネストされたスタックに分けます。
- **`Outputs` の例:** `TableName` の値を `describe-stacks` で確認できます。`Condition: IsProd` を付けると、`prod` のときだけ出力します。
- **大きさの計算例:** 60,000 バイトのテンプレートは、本文の上限 51,200 バイトを 8,800 バイト超えます。`--template-body` では失敗するので、S3 に置きます。

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

| 属性 | 対象 | 意味 |
|---|---|---|
| `Type` | 必須 | `String`、`Number`、`List<Number>`、`CommaDelimitedList` など |
| `Default` | | 既定値 |
| `AllowedValues` | | 許可する値の一覧 |
| `AllowedPattern` | `String`、`CommaDelimitedList` | 値**全体**に一致する正規表現 |
| `MinLength`、`MaxLength` | `String` | 文字数 |
| `MinValue`、`MaxValue` | `Number` | 値の範囲 |
| `ConstraintDescription` | | 制約違反のときのメッセージ |
| `NoEcho` | | 値を `***` で隠す |
| `Description` | | 説明 |

**落とし穴**: YAML で `AllowedValues` に `Yes`、`No` と書くと真偽値になります。文字列にするには引用符で囲みます。`NoEcho` は `Outputs` や `Metadata` に書いた値までは隠しません。

属性ごとの例です。

- **`Type: String` の例:** `Stage` に `prod` を渡します。
- **`Type: Number` の例:** `MinValue: 1`、`MaxValue: 10` で `11` を渡すとエラーです。`!Ref` で読むと文字列の `"10"` になります。
- **`Type: List<Number>` の例:** `80,443` を渡すと、`!Ref` で文字列のリストになります。
- **`Type: CommaDelimitedList` の例:** `a,b,c` を渡し、`!Select [1, !Ref Names]` で `b` を読みます。
- **AWS 固有の型の例:** `Type: AWS::EC2::VPC::Id` に `vpc-12345678` を渡します。アカウントにない ID ならスタックの作成前に失敗します。
- **`AWS::SSM::Parameter::Value<String>` の例:** `Default: /app/image-id` と書くと、スタックの作成時に Parameter Store の値を読みます。渡すのはパラメータの名前で、値そのものではありません。
- **`Default` の例:** `Default: dev` なら、値を渡さないときは `dev` です。`Default` がなければ値が必須です。
- **`AllowedValues` の例:** `[dev, staging, prod]` で `qa` を渡すと、作成前に失敗します。
- **`AllowedPattern` の例:** `^[a-z0-9-]+$` は値全体に一致する必要があります。`Prod-1` は大文字を含むので拒否されます。`CommaDelimitedList` では各値を確かめます。
- **`MinLength`、`MaxLength` の例:** `MinLength: 3`、`MaxLength: 8` で `ab` は失敗します。
- **`ConstraintDescription` の例:** `小文字と数字だけ` と書くと、エラーに `Malformed input-Parameter Stage 小文字と数字だけ` のように出ます。書かないと正規表現だけが表示されます。
- **`NoEcho` の例:** `true` にすると、`describe-stacks` の結果は `*****` です。ただし、`Outputs` に同じ値を書くと平文で見えます。

動的参照の例です。

- **`ssm` の例:** `{{resolve:ssm:/app/url:3}}` はバージョン 3 に固定します。バージョンを省くと、スタックの作成や更新のたびに最新版を読みます。`Parameters` セクションでは省けません。
- **`ssm-secure` の例:** `MasterUserPassword` のように対応するプロパティでだけ使えます。カスタムリソースでは使えません。古いバージョンを消すと、更新のロールバックが失敗します。
- **`secretsmanager` の例:** `{{resolve:secretsmanager:my-db-secret:SecretString:password}}` は JSON の `password` を読みます。`password` を省くと、シークレットの全文を読みます。
- **上限の例:** 61 個目の動的参照はエラーです。

動的参照の種類は次のとおりです。テンプレートに 60 個まで書けます。

| 形式 | 取得先 |
|---|---|
| `{{resolve:ssm:/app/url:3}}` | Parameter Store の `String`、バージョン 3 |
| `{{resolve:ssm-secure:/app/pass:3}}` | Parameter Store の `SecureString`(対応するリソースのみ) |
| `{{resolve:secretsmanager:id:SecretString:password}}` | Secrets Manager |

**落とし穴**: `AWS::CloudFormation::Init` のメタデータと EC2 の `UserData` では解決されません。`AWS::Serverless` などのトランスフォームには解決前の文字列が渡ります。

### マッピングと条件 {#mappings-conditions}

`Mappings` はテンプレート内の固定の表で、`!FindInMap` で読みます。リージョンや環境ごとの値に使います。

`Conditions` は `!Equals`、`!And`、`!Or`、`!Not` で定義します。使い方は 2 つです。

- リソースや出力に `Condition: IsProd` と書き、作るかどうかを決める
- プロパティで `!If [IsProd, 値A, 値B]` として値を切り替える

- **`!FindInMap` の例:** 冒頭のテンプレートで `Stage` が `staging` なら、`!FindInMap [StageConfig, !Ref Stage, LogRetention]` は 30 です。
- **`Mappings` の誤り:** `StageConfig` に `qa` のキーがなければ、`Stage=qa` でスタックの操作が失敗します。`AllowedValues` で `qa` を弾きます。
- **`Condition` の例:** 監視用のアラームに `Condition: IsProd` を付けると、`dev` では作られません。その後 `prod` に更新すると、更新時に作られます。
- **`!If` の例:** `InstanceType: !If [IsProd, m7g.large, t3.micro]` なら、`prod` は `m7g.large`、それ以外は `t3.micro` です。
- **`!And`、`!Or`、`!Not` の例:** `!And [!Condition IsProd, !Equals [!Ref Region2, "true"]]` は両方が真のときだけ真です。
- **誤ると:** `Condition: IsProd` のリソースを、条件のない `Outputs` から `!Ref` すると、`dev` では参照先がなく失敗します。出力にも同じ `Condition` を付けます。

### 出力とエクスポート {#outputs-exports}

`Outputs` の値に `Export` を付けると、別のスタックから `!ImportValue` で参照できます。

- エクスポート名はアカウントとリージョン内で一意
- `Fn::ImportValue` が参照できるのは同じアカウントとリージョンのみ
- 参照されている間は、エクスポート元のスタック削除や値の変更ができない
- 別アカウントや別リージョンのスタック出力は `Fn::GetStackOutput` で参照できる

- **`Export` の例:** `Name: !Sub "${Stage}-orders-table"` なら、`Stage` が `dev` のとき名前は `dev-orders-table` です。別のスタックは `!ImportValue dev-orders-table` で読みます。
- **一意の例:** 同じリージョンの別のスタックが `dev-orders-table` をエクスポートすると、名前が重複して失敗します。
- **`Fn::GetStackOutput` の例:** `StackName`、`OutputName`、`Region`、`RoleArn` を指定します。`Export` がなくても読めます。
- **誤ると:** `Fn::GetStackOutput` は弱い参照です。参照先のスタックを消しても、消す操作は止まらず、参照側の更新もされません。値は参照側のスタックを作成や更新したときに解決します。パーティションをまたぐ参照はできません。

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

#### 関数の使用例 {#intrinsic-examples}

```yaml
# Ref と GetAtt の違い
BucketName: !Ref ReportBucket            # バケットの名前
BucketArn: !GetAtt ReportBucket.Arn      # 属性を指定

# Sub と変数マップ、リテラル
Url: !Sub "https://${Api}.execute-api.${AWS::Region}.${AWS::URLSuffix}/${Stage}"
Key: !Sub
  - "${Prefix}/${AWS::AccountId}"
  - Prefix: reports
Note: !Sub "echo ${!NOT_REPLACED}"       # ${NOT_REPLACED} のまま残る

# Select、Split、Join
FirstAz: !Select [0, !GetAZs ""]
First: !Select [0, !Split [",", "a,b,c"]]   # a
Name: !Join ["-", [!Ref Stage, orders]]     # prod-orders

# Cidr: /16 から 3 つの /24 を作る
Subnets: !Cidr ["10.0.0.0/16", 3, 8]

# If と NoValue
KmsKeyId: !If [IsProd, !Ref Key, !Ref AWS::NoValue]

# UserData
UserData: !Base64 |
  #!/bin/bash
  dnf install -y httpd
```

| 関数 | 注意 |
|---|---|
| `Fn::GetAZs` | `""` は `AWS::Region` と同じ |
| `Fn::Cidr` | 第 3 引数はホスト部のビット数。8 なら `/24`(IPv4) |
| `Fn::And`、`Fn::Or` | 条件は 2〜10 個 |
| `Fn::Not` | 1 個の条件を反転 |
| `Fn::ToJsonString`、`Fn::Length`、`Fn::ForEach` | `Transform: AWS::LanguageExtensions` が必要 |
| `Fn::Transform` | テンプレートの一部にマクロを適用 |
| `Fn::GetStackOutput` | 別アカウント、別リージョンのスタック出力を参照 |

関数の結果を値で確かめます。

- **`Fn::Cidr` の例:** `!Cidr ["10.0.0.0/16", 3, 8]` は `10.0.0.0/24`、`10.0.1.0/24`、`10.0.2.0/24` です。第 3 引数を 5 にすると、32 − 5 = 27 なので `/27` です。第 2 引数は 1〜256 です。
- **`Ref` と `GetAtt` の例:** S3 バケットなら `!Ref ReportBucket` は名前、`!GetAtt ReportBucket.Arn` は ARN です。ARN が要る `Resource` に `!Ref` を書くと、IAM ポリシーのエラーになります。
- **`Fn::Select` の例:** `!Select [0, !GetAZs ""]` は東京なら先頭の AZ です。`!Select [5, ...]` のように範囲外を指定すると失敗します。
- **`Fn::Sub` の例:** `${!NOT_REPLACED}` は置換されず `${NOT_REPLACED}` が残ります。シェルの変数を `UserData` に書くときに使います。
- **`Fn::Join` の例:** `!Join ["-", [prod, orders]]` は `prod-orders` です。
- **`Fn::Base64` の例:** `UserData` は Base64 が必要です。`!Base64` を付けないと、作成時にエラーになります。
- **`Fn::Not` の例:** `!Not [!Equals [!Ref Stage, prod]]` は `prod` 以外で真です。
- **`Fn::Length` の例:** `Transform: AWS::LanguageExtensions` がないと、`Fn::Length` は使えず、テンプレートのエラーになります。

#### 擬似パラメータ {#pseudo-parameters}

| 名前 | 値の例 |
|---|---|
| `AWS::AccountId` | `123456789012` |
| `AWS::NotificationARNs` | スタックの通知先 ARN の一覧 |
| `AWS::NoValue` | プロパティを削除する |
| `AWS::Partition` | `aws`、`aws-cn`、`aws-us-gov` |
| `AWS::Region` | `ap-northeast-1` |
| `AWS::StackId` | スタックの ARN |
| `AWS::StackName` | スタック名 |
| `AWS::URLSuffix` | `amazonaws.com` |

ARN を書くときは、`arn:aws:` と固定せず `arn:${AWS::Partition}:` にすると他のパーティションでも動きます。

値を入れた例です。スタック名は `orders-prod`、リージョンは `ap-northeast-1` とします。

- **`AWS::Region`、`AWS::URLSuffix` の例:** `!Sub "https://sqs.${AWS::Region}.${AWS::URLSuffix}"` は `https://sqs.ap-northeast-1.amazonaws.com` です。
- **`AWS::StackName` の例:** `!Sub "${AWS::StackName}-logs"` は `orders-prod-logs` です。同じテンプレートで `orders-dev` を作っても、名前が衝突しません。
- **`AWS::AccountId` の例:** `!Sub "${AWS::AccountId}-reports"` は、アカウントが `111122223333` なら `111122223333-reports` です。
- **`AWS::Partition` の例:** `arn:${AWS::Partition}:s3:::my-bucket` は、`aws-us-gov` のリージョンでは `arn:aws-us-gov:s3:::my-bucket` です。`arn:aws:` と固定すると、そのリージョンでは権限が効きません。
- **`AWS::NoValue` の例:** `!If [IsProd, !Ref Key, !Ref AWS::NoValue]` は、`dev` ではプロパティを書かなかったのと同じです。
- **`AWS::NotificationARNs` の例:** スタックの作成時に `--notification-arns` で SNS トピックを渡すと、その一覧を読めます。
- **`AWS::StackId` の例:** `Ref` で読むと `arn:aws:cloudformation:ap-northeast-1:111122223333:stack/orders-prod/...` の形です。

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

値ごとの例です。

- **`Delete` の例:** 開発用の S3 バケットです。ただし中身があると `DELETE_FAILED` になります。
- **`Retain` の例:** 注文テーブルに `DeletionPolicy: Retain` を付けると、スタックを消してもテーブルは残ります。料金は続きます。同じ名前で作り直すと `already exists` で失敗します。
- **`RetainExceptOnCreate` の例:** 初回の作成がロールバックしたときは、作りかけのテーブルを消します。作成に成功した後は `Retain` と同じです。
- **`Snapshot` の例:** RDS の DB インスタンスを消す前にスナップショットを取ります。スタックが `DELETE_COMPLETE` になっても、スナップショットは残って料金がかかります。S3 バケットは対応していません。
- **既定の例:** `AWS::RDS::DBInstance` で `DeletionPolicy` を書かないと、`DBClusterIdentifier` がなければ `Snapshot` です。`AWS::EC2::Volume` で書かないと `Delete` なので、データごと消えます。

### その他のリソース属性 {#resource-attributes}

#### DependsOn {#depends-on}

作成の順序を明示します。削除は逆の順序です。`!Ref` や `!GetAtt` を使うと依存は暗黙に決まるので、書く必要はありません。

**例**: `AWS::EC2::EIP` が VPC のインターネットゲートウェイのアタッチメントに依存するときなど、参照のない依存に使います。

- **誤ると:** `A` が `B` に、`B` が `A` に `DependsOn` を書くと、`Circular dependency` で失敗します。

#### UpdateReplacePolicy {#update-replace-policy}

`Delete`、`Retain`、`Snapshot` を指定します。**置き換えのとき**に古いリソースをどうするかを決めます。`DeletionPolicy` はスタックの削除とテンプレートからの除去のときに効きます。データを守るなら両方を書きます。

- **例:** 注文テーブルの `TableName` を変えると置き換えです。`UpdateReplacePolicy: Retain` なら、古いテーブルと 1,000 万件のデータは残ります。書かないと古いテーブルは消えます。
- **誤ると:** `DeletionPolicy: Retain` だけでは、置き換えからは守れません。

#### CreationPolicy {#creation-policy}

対象は `AWS::AutoScaling::AutoScalingGroup`、`AWS::EC2::Instance`、`AWS::CloudFormation::WaitCondition` です。

| 項目 | 既定値 | 説明 |
|---|---|---|
| `ResourceSignal.Count` | 1 | 待つ成功シグナルの数 |
| `ResourceSignal.Timeout` | `PT5M` | 待ち時間。最大 12 時間 |
| `AutoScalingCreationPolicy.MinSuccessfulInstancesPercent` | 100 | 成功が必要な割合 |

```yaml
WebGroup:
  Type: AWS::AutoScaling::AutoScalingGroup
  CreationPolicy:
    ResourceSignal:
      Count: 3
      Timeout: PT15M
```

**症状**: `cfn-signal` を送らない、タイムアウトが短い、またはインスタンスからエンドポイントに届かないと、シグナルが足りずに `CREATE_FAILED` になり、ロールバックします。

- **`Count` の例:** 上の例は 3 台のシグナルを待ちます。2 台だけ届いて 15 分たつと失敗です。
- **`Timeout` の例:** `PT15M` は 15 分、`PT1H30M` は 90 分です。起動に 20 分かかるなら、既定の `PT5M` では足りません。待ち時間はリソースが安定してから数えます。
- **`MinSuccessfulInstancesPercent` の例:** `DesiredCapacity` が 4 で 75 なら、4 × 0.75 = 3 台の成功で完了します。1 台が失敗しても続きます。

#### UpdatePolicy {#update-policy}

| ポリシー | 項目 | 既定値 |
|---|---|---|
| `AutoScalingRollingUpdate` | `MaxBatchSize` | 1(最大 100) |
| | `MinInstancesInService` | 0 |
| | `MinActiveInstancesPercent` | 100 |
| | `MinSuccessfulInstancesPercent` | 100 |
| | `PauseTime` | `WaitOnResourceSignals` が `true` なら `PT5M` |
| | `WaitOnResourceSignals` | `false` |
| | `SuspendProcesses` | 未指定 |
| `AutoScalingReplacingUpdate` | `WillReplace` | `true` で新しいグループを作る |
| `AutoScalingScheduledAction` | `IgnoreUnmodifiedGroupSizeProperties` | スケジュールアクションで変わった容量を更新で戻さない |
| `CodeDeployLambdaAliasUpdate` | `ApplicationName`、`DeploymentGroupName` など | エイリアスの更新で CodeDeploy を動かす |

`AutoScalingReplacingUpdate` の `WillReplace: true` は `AutoScalingRollingUpdate` より優先されます。

**例**: 6 台のグループで、`MaxBatchSize: 2`、`MinInstancesInService: 4`、`WaitOnResourceSignals: true`、`PauseTime: PT10M` なら、2 台ずつ置き換え、シグナルを最大 10 分待ちます。

- **`MaxBatchSize` の計算例:** 上の例は 6 ÷ 2 = 3 バッチです。各バッチで 10 分いっぱい待つと、更新に 30 分ほどかかります。
- **`MinInstancesInService` の例:** `MaxSize` より小さい値にします。`MaxSize: 6` で 6 にすると無効です。`MinSize` 以上にすると、更新中の容量不足を防げます。既定の 0 だと、1 台のグループは更新中に 0 台になります。
- **`MinActiveInstancesPercent` の例:** 5 台で 50 なら、少なくとも 3 台が `InService` である必要があります。
- **`MinSuccessfulInstancesPercent` の例:** 5 台を更新して 50 なら、3 台のシグナルが必要です。既定の 100 では 1 台でも失敗すると更新が失敗します。
- **`PauseTime` の例:** 上限は `PT1H` です。`WaitOnResourceSignals: false` なら単なる待ち時間です。`true` ならシグナルの待ち時間の上限です。
- **`WaitOnResourceSignals` の例:** `false` のままだと、新しいインスタンスのアプリが起動に失敗していても、次のバッチへ進みます。
- **`SuspendProcesses` の例:** `[HealthCheck, ReplaceUnhealthy, AZRebalance, AlarmNotification, ScheduledActions]` で、更新を邪魔する Auto Scaling の処理を止めます。書かないと、更新中にスケールアウトが動いて失敗することがあります。
- **`WillReplace` の例:** 6 台のグループで `true` なら、新しい 6 台のグループを作り、成功すれば古いグループを消します。一時的に 12 台分の容量が必要です。失敗すれば古いグループがそのまま残ります。
- **`IgnoreUnmodifiedGroupSizeProperties` の例:** テンプレートの `DesiredCapacity` が 2 で、スケジュールで 10 台に増えている 10 時に更新するとします。`true` なら 10 台のままで、未指定なら 2 台に戻ります。
- **`CodeDeployLambdaAliasUpdate` の例:** `AWS::Lambda::Alias` の更新で、`ApplicationName` と `DeploymentGroupName` の CodeDeploy を使ってトラフィックを移します。

#### Metadata 属性 {#metadata-attribute}

リソースに任意の JSON を付けます。`AWS::CloudFormation::Init` は `cfn-init` が読む設定です。

- **例:** `Metadata` に `Version: "1.4.2"` と書いて更新し、`cfn-hup` で検知してアプリを入れ替えます。
- **誤ると:** `Metadata` だけを変えた更新は、`UserData` を実行し直しません。`cfn-hup` がないと、動いているインスタンスには届きません。

### ヘルパースクリプト {#cfn-helpers}

| スクリプト | 役割 |
|---|---|
| `cfn-init` | `AWS::CloudFormation::Init` を読み、パッケージの導入やファイルの作成を行う |
| `cfn-signal` | `CreationPolicy` や `WaitCondition` にシグナルを送る |
| `cfn-get-metadata` | メタデータを取得する |
| `cfn-hup` | メタデータの変更を検知し、フックを動かすデーモン。確認の間隔は既定で 15 分 |

`cfn-init` は `packages`、`groups`、`users`、`sources`、`files`、`commands`、`services` の順に処理します。順序を変えるには `configSets` を使います。

```yaml
Instance:
  Type: AWS::EC2::Instance
  CreationPolicy:
    ResourceSignal: {Timeout: PT10M}
  Metadata:
    AWS::CloudFormation::Init:
      config:
        packages:
          dnf: {httpd: []}
        files:
          /var/www/html/index.html:
            content: "hello"
        services:
          systemd:
            httpd: {enabled: true, ensureRunning: true}
  Properties:
    ImageId: "{{resolve:ssm:/aws/service/ami-amazon-linux-latest/al2023-ami-kernel-6.1-x86_64}}"
    InstanceType: t3.micro
    UserData: !Base64
      Fn::Sub: |
        #!/bin/bash
        /opt/aws/bin/cfn-init -v --stack ${AWS::StackName} --resource Instance --region ${AWS::Region}
        /opt/aws/bin/cfn-signal -e $? --stack ${AWS::StackName} --resource Instance --region ${AWS::Region}
```

`-e $?` で `cfn-init` の終了コードを渡します。失敗すれば `FAILURE` のシグナルになります。

`cfn-hup` のフックは `triggers=post.add`、`post.update`、`post.remove` と `action=` を書きます。

- **`configSets` の例:** `install` を先に、`configure` を後に動かすなら `configSets: {default: [install, configure]}` と書きます。
- **処理順の例:** `files` は `services` より先なので、`/etc/nginx/nginx.conf` を置いてから `nginx` を起動します。
- **`cfn-signal` の例:** `-e 0` は成功、`-e 1` は失敗です。`-d` で wait condition へ渡せるデータは 4,096 バイトまでです。
- **`cfn-hup` の例:** `interval=5` で 5 分ごとに確認します。既定は 15 分なので、`Metadata` を更新してから反映まで最大で 15 分ほどかかります。
- **`cfn-get-metadata` の例:** インスタンス上で、自分のリソースの `Metadata` を確認します。
- **誤ると:** `UserData` で `cfn-init` のパスを誤ると、`cfn-signal` が失敗を送るか、シグナルなしで `CreationPolicy` が時間切れになります。

### カスタムリソース {#custom-resources}

CloudFormation にない処理を Lambda か SNS で実行します。種類は `AWS::CloudFormation::CustomResource` か `Custom::名前` です。

| 項目 | 内容 |
|---|---|
| `ServiceToken` | 必須。Lambda か SNS の ARN |
| `ServiceTimeout` | 1〜3,600 秒。既定は 3,600 秒 |
| リクエスト | `RequestType` が `Create`、`Update`、`Delete` |
| 応答先 | リクエストの署名付き S3 URL。`Status` は `SUCCESS` か `FAILED` |
| 応答の項目 | `Status`、`PhysicalResourceId`、`StackId`、`RequestId`、`LogicalResourceId`、`Data` |

**例**: スタック作成時に S3 へ初期データを入れる Lambda です。`Fn::GetAtt` で `Data` のキーを読めます。

**症状**: 関数が例外で落ちて応答を送らないと、スタックは `ServiceTimeout` まで待ち、既定では 1 時間動きません。`Delete` の処理を忘れるとスタックの削除でも止まります。必ず `try` と `finally` で応答し、短い `ServiceTimeout` を指定します。

- **`ServiceTimeout` の例:** 5 分以内に応答する関数なら `ServiceTimeout: 360` にします。応答がなければ 6 分で失敗し、1 時間待たずに済みます。
- **`Data` の例:** 応答に `"Data": {"Endpoint": "db.example.com"}` を入れると、`!GetAtt Init.Endpoint` で読めます。`Data` は 4,096 バイトまでです。
- **`PhysicalResourceId` の例:** `Update` で値を変えて返すと、CloudFormation は置き換えと見なし、古い ID に `Delete` を送ります。同じ値を返せば置き換えになりません。
- **`RequestType` の例:** `Create` で S3 に入れた初期データは、`Delete` で消して `SUCCESS` を返します。消さないと、バケットが空にならず `DELETE_FAILED` になります。

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

- **中断なしの例:** Lambda 関数の `MemorySize` を 128 から 1,024 に変えます。関数の ARN は変わりません。
- **一時的な中断の例:** EBS で起動する EC2 の `InstanceType` を変えると、インスタンスが停止して起動し直します。
- **置き換えの例:** EC2 の `ImageId` や DynamoDB の `TableName` を変えると、新しいリソースを作って古いものを消します。
- **論理 ID の例:** `OrdersTable` を `OrderTable` に直すと、新しいテーブルを作って古いテーブルを消します。データは新しいテーブルに移りません。
- **固定の名前の例:** `TableName: orders` のまま、置き換えになる変更をすると、同じ名前のテーブルが残っているので新しいテーブルを作れず失敗します。

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

`describe-change-set` の主な項目です。

| 項目 | 値 | 意味 |
|---|---|---|
| `Action` | `Add`、`Modify`、`Remove` | 変更の種類 |
| `Replacement` | `True`、`False`、`Conditional` | 置き換えの有無 |
| `Scope` | `Properties`、`Tags` など | 変更の範囲 |

`Conditional` は実行時の値で決まります。**例**: `!GetAtt` の値に依存するプロパティがあるときです。

`--change-set-type CREATE` で新しいスタックの変更セットも作れます。ネストされたスタックも確認するなら `--include-nested-stacks` を指定します。

- **`Action` の例:** テンプレートにテーブルを足すと `Add`、`Timeout` を変えると `Modify`、リソースを消すと `Remove` です。
- **`Replacement` の例:** `TableName` を変えると `True` です。`True` を見つけたら、実行を止めてデータの扱いを確認します。
- **`Scope` の例:** タグだけを変えた変更は `Tags` です。
- **誤ると:** 変更セットを作っただけでは反映されません。`execute-change-set` を忘れると、スタックは古いままです。

### スタックポリシー {#stack-policy}

更新時の保護です。削除からの保護ではありません。

| 状態 | 動作 |
|---|---|
| 設定なし(既定) | 全リソースの更新を許可 |
| 設定あり | **明示的に Allow したものだけ更新できる**。`Deny` は `Allow` より優先 |

```json
{
  "Statement": [
    {"Effect": "Allow", "Action": "Update:*", "Principal": "*", "Resource": "*"},
    {
      "Effect": "Deny",
      "Action": ["Update:Replace", "Update:Delete"],
      "Principal": "*",
      "Resource": "LogicalResourceId/OrdersTable"
    }
  ]
}
```

アクションは `Update:Modify`、`Update:Replace`、`Update:Delete`、`Update:*` です。

保護されたリソースを 1 回だけ更新するなら、`update-stack` の `--stack-policy-during-update-body` で一時的なポリシーを渡します。

**症状**: ポリシーで拒否された更新は失敗します。

- **`Update:Modify` の例:** 上のポリシーは `OrdersTable` の `BillingMode` の変更を許可します。これは置き換えを伴わないためです。
- **`Update:Replace` の例:** `OrdersTable` の `TableName` を変える更新は拒否され、スタックの更新は失敗します。
- **`Update:Delete` の例:** テンプレートから `OrdersTable` を消す更新も拒否されます。
- **`Allow` を忘れた例:** `Deny` の文だけのポリシーを設定すると、他のリソースも更新できません。設定した時点で、全リソースが既定で保護されるためです。
- **`--stack-policy-during-update-body` の例:** 今回だけ `OrdersTable` の置き換えを許可するポリシーを渡します。更新の後は、元のポリシーが効きます。
- **終了保護の例:** `aws cloudformation update-termination-protection --enable-termination-protection --stack-name orders-prod` の後は、`delete-stack` が失敗します。

**削除からの保護**には、スタックの終了保護(`--enable-termination-protection`)を使います。親で設定するとネストされたスタックにも適用され、ネストされたスタックに直接は設定できません。

### 機能の承認(capabilities) {#capabilities}

| 値 | 必要な場面 |
|---|---|
| `CAPABILITY_IAM` | IAM リソースを含む |
| `CAPABILITY_NAMED_IAM` | 名前を指定した IAM リソースを含む |
| `CAPABILITY_AUTO_EXPAND` | マクロやトランスフォームを含み、変更セットの確認なしで直接デプロイする |

**症状**: `RoleName` を指定したロールを `CAPABILITY_IAM` でデプロイすると、`InsufficientCapabilities` になります。`CAPABILITY_NAMED_IAM` にします。

- **`CAPABILITY_IAM` の例:** 名前のない `AWS::IAM::Role` を含むテンプレートは、`--capabilities CAPABILITY_IAM` で作れます。
- **`CAPABILITY_NAMED_IAM` の例:** `RoleName: orders-role` があると必須です。
- **`CAPABILITY_AUTO_EXPAND` の例:** `Transform: AWS::Serverless-2016-10-31` のテンプレートを、変更セットなしで `create-stack` するときに指定します。

### ドリフト検出 {#drift}

手作業の変更などで、実際の設定がテンプレートとずれた状態を検出します。

- `detect-stack-drift` で開始し、`describe-stack-resource-drifts` で差分を確認する
- 対応していないリソースは `NOT_CHECKED` になる
- 明示的に設定した値だけが比較の対象で、プロパティの既定値は対象外
- 親スタックの検出では、ネストされたスタックは検出されない。個別に実行する

ドリフトを検出するだけで自動修復はしません。差分を考慮して更新する機能として、ドリフト対応の変更セット（drift-aware change sets）もあります。

| 項目 | 値 |
|---|---|
| スタックの状態 | `DRIFTED`、`IN_SYNC`、`NOT_CHECKED` |
| リソースの状態 | `DELETED`、`MODIFIED`、`IN_SYNC`、`NOT_CHECKED` |
| プロパティの差分 | `ADD`、`NOT_EQUAL`、`REMOVE` |

値ごとの例です。テンプレートのロググループは `RetentionInDays: 7` とします。

- **`MODIFIED`、`NOT_EQUAL` の例:** コンソールで保持期間を 30 日にすると、期待値 7、実際の値 30 の `NOT_EQUAL` で、リソースは `MODIFIED` です。スタックは `DRIFTED` です。
- **`DELETED` の例:** ロググループを手で消すと `DELETED` です。
- **`ADD` の例:** テンプレートに 1 つだけ書いたセキュリティグループのルールに、手で 1 つ足すと `ADD` です。
- **`REMOVE` の例:** テンプレートに書いたプロパティを、実際の設定から外すと `REMOVE` です。
- **`IN_SYNC` の例:** テンプレートに書いていない設定を手で変えても `IN_SYNC` のままです。既定値は比較の対象外だからです。追跡したいプロパティは、既定値でも明示します。
- **`NOT_CHECKED` の例:** ドリフト検出に対応していないリソースです。
- **誤ると:** 親スタックが `IN_SYNC` でも、ネストされたスタックはずれていることがあります。

### ネストされたスタックと StackSets {#nested-stacks-stacksets}

| 機能 | 用途 |
|---|---|
| ネストされたスタック | 共通の構成を部品にする。`AWS::CloudFormation::Stack` で別テンプレートを呼ぶ |
| クロススタック参照 | 独立したスタック間で値を共有する（`Export` と `ImportValue`） |
| StackSets | 1 回の操作で複数のアカウントとリージョンへ展開する |

部品の再利用ならネスト、ライフサイクルの違うスタック間の共有ならエクスポートです。

- **ネストの例:** 3 つのアプリで同じ ALB の構成を使うなら、`alb.yaml` を子にして、各親から呼びます。
- **クロススタック参照の例:** ネットワークチームの VPC のスタックを、アプリの 5 つのスタックが参照します。
- **StackSets の例:** 全アカウントの全リージョンに、CloudTrail の設定を 1 回の操作で配ります。

#### ネストとエクスポートの比較 {#nested-vs-exports}

| 観点 | ネストされたスタック | エクスポートと `ImportValue` |
|---|---|---|
| 関係 | 親子。親と一緒に更新される | 独立したスタック |
| 値の渡し方 | `Parameters` と `!GetAtt Child.Outputs.Name` | `Export` と `!ImportValue` |
| 変更 | テンプレートを変えて親を更新 | 参照があると値を変更、削除できない |
| 向く場面 | 再利用する部品 | ネットワークなど別のチームが管理する基盤 |

ネストの子テンプレートは `TemplateURL` で S3 の URL を指定します。ローカルのファイルは `aws cloudformation package` で S3 に上げて URL に置き換えられます。

**例**: VPC のスタックが `prod-vpc-id` をエクスポートし、アプリのスタックが参照しています。参照されている間は、VPC のスタックでこの出力を変更すると失敗します。先に参照側を変えます。

- **ネストの例:** 親のテンプレートに `TemplateURL: https://s3.ap-northeast-1.amazonaws.com/my-bucket/vpc.yaml` の子を書きます。親で `!GetAtt Vpc.Outputs.VpcId` と読みます。
- **誤ると:** 子のスタックを直接更新すると、親のテンプレートとずれます。ルートのスタックから更新します。

#### StackSets の設定 {#stacksets-settings}

| 項目 | 内容 |
|---|---|
| セルフマネージド権限 | `AWSCloudFormationStackSetAdministrationRole` と `AWSCloudFormationStackSetExecutionRole` を自分で作る |
| サービスマネージド権限 | AWS Organizations と連携。ロールは自動。新しいアカウントへの自動デプロイが可能 |
| `MaxConcurrentCount`、`MaxConcurrentPercentage` | 同時に処理するアカウント数 |
| `FailureToleranceCount`、`FailureTolerancePercentage` | 許容する失敗の数 |
| `RegionConcurrencyType` | リージョンを順に、または並列に処理 |

**提供単位**: StackSet はリージョン単位です。東京で作った StackSet は、東京のコンソールでしか見えません。

**数え方の例:** 20 アカウント × 3 リージョンなら、スタックインスタンスは 60 個です。

- **セルフマネージド権限の例:** 管理アカウントに `AWSCloudFormationStackSetAdministrationRole` を、各ターゲットに `AWSCloudFormationStackSetExecutionRole` を作ります。Organizations を使わない 3 アカウントの構成に向きます。
- **サービスマネージド権限の例:** OU にアカウントを追加すると、自動デプロイを有効にしていれば、スタックが自動で作られます。
- **`MaxConcurrentCount` の例:** 既定は 1 で、1 アカウントずつ処理します。20 アカウントで 5 にすると、同時に 5 アカウントです。既定の `STRICT_FAILURE_TOLERANCE` では、同時実行は `FailureToleranceCount` + 1 が上限です。5 にするなら `FailureToleranceCount` を 4 にします。
- **`MaxConcurrentPercentage` の例:** 25 アカウントで 10 なら、2.5 を切り捨てて 2 です。25 アカウントで 3 なら、0.75 を切り捨てると 0 なので、1 になります。
- **`FailureToleranceCount` の例:** 既定は 0 で、1 アカウントでも失敗すると、そのリージョンの操作を止めます。後のリージョンにも進みません。
- **`FailureTolerancePercentage` の例:** 25 アカウントで 10 なら、切り捨てて 2 アカウントの失敗まで許します。
- **`RegionConcurrencyType` の例:** `SEQUENTIAL` は東京が終わってから大阪へ進むので、東京の失敗を見て止められます。`PARALLEL` は同時に進むので速く終わります。
- **同時指定の誤り:** `MaxConcurrentCount` と `MaxConcurrentPercentage` は同時に指定できません。`FailureTolerance` の 2 つも同じです。

## スタックのロールバックと失敗 {#stack-failures}

### ロールバックの既定動作 {#stack-rollback}

作成や更新が失敗すると、既定で自動的に元へ戻します。

| 操作 | 失敗後の状態 | 次にできること |
|---|---|---|
| 作成の失敗 | `ROLLBACK_COMPLETE` | 更新はできない。削除して作り直す |
| 更新の失敗 | `UPDATE_ROLLBACK_COMPLETE` | 修正して再度更新 |
| 更新のロールバックも失敗 | `UPDATE_ROLLBACK_FAILED` | `continue-update-rollback` |

開発時は「正常にプロビジョニングされたリソースを保持する」オプションを使うと、成功したリソースを残し、失敗した場所から再開できます。

- **作成の失敗の例:** 初回の作成が失敗して `ROLLBACK_COMPLETE` になると、`update-stack` は受け付けません。`delete-stack` の後で作り直します。
- **更新の失敗の例:** `MemorySize` を不正な値にして `UPDATE_ROLLBACK_COMPLETE` になっても、スタックは使えます。テンプレートを直して更新します。
- **ロールバックの失敗の例:** 更新の途中で、戻す先のセキュリティグループを手で消すと `UPDATE_ROLLBACK_FAILED` になります。
- **`resources-to-skip` の例:** `--resources-to-skip OrdersTable` と書きます。ネストされたスタックのリソースは `NestedStackName.ResourceLogicalID` の形です。
- **`--force-rollback` の例:** ロールバックに失敗したリソースを 1 つずつ書く代わりに、`aws cloudformation continue-update-rollback --stack-name orders-prod --force-rollback` で一括して飛ばします。飛ばしたリソースの実際の状態は、テンプレートと合わなくなります。
- **保持のオプションの例:** 20 個のうち 19 個作って 1 個失敗したら、19 個を残したまま原因を直して再開できます。最初から作り直す時間を省けます。

#### 作成の失敗時の動作 {#on-failure}

| 指定 | 動作 |
|---|---|
| `--on-failure ROLLBACK` | 既定。リソースを消す |
| `--on-failure DO_NOTHING` | そのまま残す。原因の調査に使う |
| `--on-failure DELETE` | スタックごと消す |
| `--disable-rollback` | 残す。`--on-failure` と同時に指定できない |
| `--timeout-in-minutes` | 指定時間で作成を失敗にする |

**例**: EC2 のユーザーデータの失敗を調べたいなら、`DO_NOTHING` で作り、残ったインスタンスの `/var/log/cfn-init.log` を確認します。

- **`ROLLBACK` の例:** 本番の自動化に向きます。失敗したスタックは `ROLLBACK_COMPLETE` で残り、作成したリソースは消えます。
- **`DELETE` の例:** 使い捨てのテスト環境です。失敗したスタックが残らないので、同じ名前で再実行できます。
- **`--disable-rollback` の例:** `--on-failure DO_NOTHING` と同じ目的です。両方を書くとエラーです。
- **`--timeout-in-minutes` の例:** 値が 30 なら、30 分で終わらないと `CREATE_FAILED` になります。ロールバックを無効にしていなければ、そのまま戻します。

### ロールバックトリガー {#rollback-triggers}

スタック操作の間と、完了後の監視時間に CloudWatch アラームを見張ります。アラームが `ALARM` になるとスタック全体を戻します。

- トリガーは最大 5 個
- 監視時間は 0 から 180 分（既定は 0）
- 指定できるのはメトリクスアラームと複合アラーム
- `INSUFFICIENT_DATA` では戻さない。戻すにはアラームで欠落データを `breaching` として扱う

- **`MonitoringTimeInMinutes` の例:** 10 なら、リソースの更新が終わってから 10 分間アラームを見ます。この間に 5XX のアラームが `ALARM` になると、スタック全体を戻します。既定の 0 なら、完了後は見ません。
- **`Arn` の例:** `Type` は `AWS::CloudWatch::Alarm` か `AWS::CloudWatch::CompositeAlarm` です。
- **誤ると:** 指定したアラームが存在しないと、スタック操作全体が失敗して戻ります。6 個目のトリガーも指定できません。

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
| `UPDATE_ROLLBACK_FAILED` | 戻す先のリソースが手動で削除された、権限不足など | 原因を直して `continue-update-rollback`。難しければ `--resources-to-skip` か `--force-rollback` |
| `InsufficientCapabilities` | IAM リソースやマクロの承認なし | `--capabilities CAPABILITY_IAM`、`CAPABILITY_NAMED_IAM`、`CAPABILITY_AUTO_EXPAND` |
| `already exists` | 固定の名前が衝突 | 名前を指定せず自動生成に任せる |
| `DELETE_FAILED` | S3 バケットが空でない、依存リソースが残っている | 中身を消す、依存を外す、`--retain-resources` |
| エクスポートを消せない | 他スタックが `ImportValue` で参照中 | 参照側を先に更新 |
| `ROLLBACK_COMPLETE` で更新不可 | 初回作成の失敗 | スタックを削除して作り直す |
| `No updates are to be performed` | 差分なし | テンプレートやパラメータを確認 |
| `Circular dependency` | リソースの相互参照 | 参照の向きを整理する |
| `Template format error` | 構文エラー | `validate-template`、`sam validate --lint` |

具体的な場面です。

- **`already exists` の例:** `BucketName: my-reports` を指定したテンプレートで、`dev` と `prod` の 2 つのスタックを作ると、2 つ目が失敗します。S3 バケットの名前は既定で全アカウント共通の空間にあるので、他のアカウントが使っていても失敗します。
- **`DELETE_FAILED` の例:** オブジェクトが 3 個あるバケットを消せません。中を空にするか、`aws cloudformation delete-stack --stack-name orders --retain-resources ReportBucket` で残します。
- **`No updates are to be performed` の例:** 同じテンプレートと同じパラメータで更新すると、エラーになります。
- **`Circular dependency` の例:** セキュリティグループ A のルールが B を参照し、B のルールが A を参照しています。ルールを `AWS::EC2::SecurityGroupIngress` に分けます。
- **`Template format error` の例:** `Resources` を `Resource` と書くと、`validate-template` で分かります。プロパティの値の誤りは、作成するまで分からないことがあります。

!!! warning "スタック外の変更を避ける"
    スタックのリソースを手動で消すと、ロールバックが失敗する原因になります。変更はテンプレート経由で行い、重要なスタックは削除保護も有効にします。

## SAM {#sam}

[:material-certificate: SAA](../courses/saa/services.md){ .exam-badge .exam-associate } [:material-certificate: DVA](../courses/dva/services.md){ .exam-badge .exam-associate } [:material-certificate: DEA](../courses/dea/services.md){ .exam-badge .exam-associate } [:material-star-circle: DOP](../courses/dop/services.md){ .exam-badge .exam-professional }

サーバーレス向けの CloudFormation 拡張です。短い記述から、デプロイ時に IAM ロールなどを含む CloudFormation リソースへ展開されます。

**提供単位**: SAM は CloudFormation のスタックとしてリージョンにデプロイされます（[2 つの軸](resource-scope.md#two-axes)）。Lambda は既定で VPC の外です（[VPC の中か、接続を選べるリソース](resource-scope.md#scope-regional-vpc)）。

- **例:** `AWS::Serverless::Function` を 1 つ書くと、関数と実行ロールの 2 つのリソースに展開されます。`Api` のイベントがあれば、API Gateway のリソースも増えます。
- **誤ると:** `Transform` の行を消すと、`AWS::Serverless::Function` は未知の種類としてエラーになります。

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

その他のリソースは次のとおりです。

| リソース | 内容 |
|---|---|
| `AWS::Serverless::Application` | 別の SAM アプリをネストする |
| `AWS::Serverless::Connector` | リソース間の権限を簡単に定義する |
| `AWS::Serverless::GraphQLApi` | AppSync の GraphQL API |
| `AWS::Serverless::WebSocketApi` | WebSocket API |

- **`AWS::Serverless::SimpleTable` の例:** `PrimaryKey` が 1 つの単純なテーブルです。GSI やソートキーが要るなら `AWS::DynamoDB::Table` を書きます。
- **`AWS::Serverless::Connector` の例:** `Source` に関数、`Destination` にテーブル、`Permissions: [Write]` と書くと、書き込みの権限が作られます。
- **`AWS::Serverless::HttpApi` と `Api` の例:** 使用量プランや API キーが要るなら `Api`(REST API)です。JWT 認可で足りるなら `HttpApi` です。
- **`AWS::Serverless::Application` の例:** Serverless Application Repository のアプリや S3 のテンプレートを、子のスタックとして組み込みます。

### Globals {#sam-globals}

共通の設定を 1 か所に書きます。対象は `AWS::Serverless::Api`、`Function`、`HttpApi`、`SimpleTable`、`StateMachine` などで、一覧にないリソースやプロパティは書けません。

```yaml
Globals:
  Function:
    Runtime: python3.12
    Timeout: 10
    Environment:
      Variables:
        STAGE: prod
    Layers:
      - !Ref Common
Resources:
  Orders:
    Type: AWS::Serverless::Function
    Properties:
      CodeUri: src/orders/
      Handler: app.handler
      Timeout: 30
      Environment:
        Variables:
          TABLE: orders
      Layers:
        - !Ref OrdersLayer
```

| 型 | 上書きの方法 | 上の例の結果 |
|---|---|---|
| 文字列、数値 | 置き換え | `Timeout` は 30 |
| マップ | マージ | `Variables` は `STAGE` と `TABLE` の両方 |
| リスト | 追加 | `Layers` は `Common` と `OrdersLayer` の両方 |

**落とし穴**: リソース側でグローバルのプロパティを消すことはできません。一部の関数だけで使うものは `Globals` に書かないようにします。

- **例:** 10 個の関数のうち 1 つだけ `Timeout` を 30 にするなら、`Globals` に `Timeout: 10` を書き、その関数の `Properties` に `Timeout: 30` を書きます。残りの 9 個は 10 です。
- **誤ると:** `Globals` の `Function` に `Layers` を書くと、全関数に付きます。リストは追加なので、1 つの関数だけ外すことはできません。`Globals` に対応していないプロパティを書くと、テンプレートのエラーです。

### Events {#sam-events}

`AWS::Serverless::Function` の `Events` の `Type` は次のとおりです。

| 種類 | 例 |
|---|---|
| API | `Api`、`HttpApi` |
| ポーリング | `SQS`、`Kinesis`、`DynamoDB`、`MSK`、`MQ`、`SelfManagedKafka`、`DocumentDB` |
| プッシュ | `S3`、`SNS`、`CloudWatchLogs`、`Cognito`、`IoTRule`、`AlexaSkill` |
| スケジュール、ルール | `Schedule`、`ScheduleV2`、`EventBridgeRule`、`CloudWatchEvent` |

```yaml
Events:
  Queue:
    Type: SQS
    Properties:
      Queue: !GetAtt OrdersQueue.Arn
      BatchSize: 10
  Daily:
    Type: ScheduleV2
    Properties:
      ScheduleExpression: "cron(0 15 * * ? *)"
  Upload:
    Type: S3
    Properties:
      Bucket: !Ref UploadBucket
      Events: s3:ObjectCreated:*
```

**落とし穴**: `S3` のイベントの `Bucket` は同じテンプレートのバケットを `!Ref` で指定します。

- **`SQS` の `BatchSize` の例:** 既定は 10、範囲は 1〜10,000 です。上の設定で 25 件が溜まれば、1 回の呼び出しで受け取るのは最大 10 件です。
- **`ScheduleV2` の例:** `cron(0 15 * * ? *)` は既定の UTC で 15 時、日本時間の 0 時です。`ScheduleExpressionTimezone: Asia/Tokyo` を足すと、日本時間の 15 時になります。
- **`S3` の例:** `Events: s3:ObjectCreated:*` はアップロードのたびに関数を呼びます。出力を同じバケットに書くと、関数が自分を呼び続けます。
- **`Api` の例:** `Path: /orders`、`Method: post` なら、`POST /orders` で関数が動きます。`GET /orders` は関数を呼びません。
- **`Kinesis`、`DynamoDB` の例:** `StartingPosition: LATEST` など、ストリームの読み始めの位置が必須です。

### Policies {#sam-policies}

```yaml
Policies:
  - AWSXRayDaemonWriteAccess          # AWS 管理ポリシーの名前
  - DynamoDBCrudPolicy:               # ポリシーテンプレート
      TableName: !Ref OrdersTable
  - S3ReadPolicy:
      BucketName: !Ref ReportBucket
  - SQSSendMessagePolicy:
      QueueName: !GetAtt OrdersQueue.QueueName
  - Statement:                        # インラインポリシー
      - Effect: Allow
        Action: ssm:GetParameter
        Resource: !Sub "arn:${AWS::Partition}:ssm:${AWS::Region}:${AWS::AccountId}:parameter/app/*"
```

| テンプレート | プレースホルダー |
|---|---|
| `DynamoDBReadPolicy`、`DynamoDBWritePolicy`、`DynamoDBCrudPolicy` | `TableName` |
| `S3ReadPolicy`、`S3WritePolicy`、`S3CrudPolicy` | `BucketName` |
| `SQSPollerPolicy`、`SQSSendMessagePolicy` | `QueueName` |
| `SNSPublishMessagePolicy` | `TopicName` |
| `KMSDecryptPolicy`、`KMSEncryptPolicy` | `KeyId` |
| `LambdaInvokePolicy` | `FunctionName` |
| `StepFunctionsExecutionPolicy` | `StateMachineName` |
| `SSMParameterReadPolicy` | `ParameterName` |
| `AWSSecretsManagerGetSecretValuePolicy` | `SecretArn` |
| `KinesisStreamReadPolicy` | `StreamName` |
| `EventBridgePutEventsPolicy` | `EventBusName` |

プレースホルダーがないテンプレートでも、空のオブジェクト `{}` を書きます。

- **`DynamoDBCrudPolicy` の例:** `TableName: !Ref OrdersTable` なら、このテーブルと、その配下のインデックスだけが対象です。
- **`SQSSendMessagePolicy` の例:** プレースホルダーは `QueueName` です。`!Ref OrdersQueue` は URL を返すので、`!GetAtt OrdersQueue.QueueName` と書きます。
- **`S3ReadPolicy` の例:** `BucketName: reports` と書きます。ARN を書くと、ポリシーの中の ARN が壊れて権限が効きません。
- **`{}` の例:** `- CloudWatchPutMetricPolicy: {}` と書きます。`{}` を省くと、ポリシーテンプレートとして認識されません。
- **インラインの例:** 上の `ssm:GetParameter` のように、テンプレートにない権限は `Statement` で書きます。
- **誤ると:** `Policies` を書かない関数からテーブルに書くと、`AccessDeniedException` になります。ログの出力だけは既定の実行ロールで動きます。

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

- **例:** `src/orders/` と `src/reports/` に分けると、`pandas` は `reports` のパッケージにだけ入ります。1 つの `src/` にまとめると、両方の関数に入ります。
- **誤ると:** `CodeUri: src/` のまま `Handler: app.handler` にすると、`src/orders/app.py` を見つけられず、関数の実行時に `Runtime.ImportModuleError` になります。

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

- **`sam validate --lint` の例:** `Runtime: python9` のような誤りを、デプロイの前に見つけます。
- **`sam local invoke` の例:** `sam local invoke OrdersFunction -e events/create-order.json` で 1 回動かします。Docker が動いていないとエラーです。
- **`sam local start-api` の例:** `http://127.0.0.1:3000/orders` に `curl` で送ります。
- **`sam local start-lambda` の例:** SDK のエンドポイントを `http://127.0.0.1:3001` にして、テストコードから関数を呼びます。
- **`sam remote invoke` の例:** `sam remote invoke OrdersFunction --stack-name orders-staging --event-file events/create-order.json` で、デプロイ済みの関数を呼びます。
- **`sam logs` の例:** `sam logs -n OrdersFunction --stack-name orders-staging --tail` でログを追います。

```bash
sam validate --lint
sam build
sam local invoke OrdersFunction -e events/create-order.json
sam local start-api
sam deploy --guided
```

#### その他の SAM コマンド {#sam-cli-more}

| コマンド | 用途 |
|---|---|
| `sam package` | コードを ZIP にして S3 に上げ、テンプレートを書き換える |
| `sam delete` | スタックと関連の成果物を削除 |
| `sam list` | `endpoints`、`resources`、`stack-outputs` を表示 |
| `sam traces` | X-Ray のトレースを取得 |
| `sam publish` | Serverless Application Repository に公開 |
| `sam pipeline bootstrap` | パイプラインに必要なリソースを作成 |
| `sam pipeline init` | CI/CD パイプラインの設定を生成 |

| オプション | 効果 |
|---|---|
| `sam build --use-container` | Lambda に近いコンテナの中でビルド。ネイティブ依存のあるパッケージに使う |
| `sam build --parallel`、`--cached` | ビルドの短縮 |
| `sam deploy --guided`、`-g` | 対話で設定し、`samconfig.toml` に保存 |
| `sam deploy --no-execute-changeset` | 変更セットを作るだけで適用しない |
| `sam deploy --no-confirm-changeset` | 確認なしで適用 |
| `sam deploy --no-fail-on-empty-changeset` | 差分なしでも成功で終わる。CI で使う |
| `sam deploy --resolve-s3` | S3 バケットを自動で作る |
| `sam deploy --on-failure` | `ROLLBACK`、`DELETE`、`DO_NOTHING` |
| `sam sync --watch` | ローカルの変更を監視して同期 |
| `sam sync --code` | コードだけを同期 |

**落とし穴**: `sam sync` は開発環境向けです。CloudFormation を迂回する更新があり、本番には `sam deploy` か CI/CD を使います。

オプションの場面です。

- **`--use-container` の例:** Mac で `numpy` を含む関数をビルドすると、Mac 用のバイナリが入り、Lambda で読み込めません。Lambda に近いコンテナの中でビルドします。
- **`--parallel`、`--cached` の例:** 関数が 20 個あるなら、既定の順次ビルドより `--parallel` が速くなります。`--cached` は変更のない部分を再利用します。依存先の新しい版は検知しないことがあるので、`requests=1.x` のような指定には注意します。
- **`--no-execute-changeset` の例:** 変更セットだけを作って終わります。人が確認した後で `aws cloudformation execute-change-set` を実行します。
- **`--confirm-changeset`、`--no-confirm-changeset` の例:** CI では待つ人がいないので `--no-confirm-changeset` です。手元で本番に出すなら `--confirm-changeset` で止めます。
- **`--no-fail-on-empty-changeset` の例:** 既定では、差分がないと非 0 で終わります。ドキュメントだけを直したコミットで CI が失敗するなら、これを付けます。
- **`--resolve-s3` の例:** `--s3-bucket` を指定しなくても、SAM が管理するバケットにコードを置きます。
- **`--on-failure` の例:** スタックの作成の失敗時に、`DO_NOTHING` なら調査用にそのまま残します。
- **`sam sync --code` の例:** 関数のコードだけを直接更新するので、数秒で反映できます。スタックの定義とのずれは、`sam sync --watch` か `sam deploy` で解消します。
- **`sam delete` の例:** `sam delete --stack-name orders-staging` でスタックを消します。S3 に上げた成果物も確認の上で消せます。
- **`sam list` の例:** `sam list stack-outputs --stack-name orders-prod` で `ApiUrl` などの出力を読みます。

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

`DeploymentPreference` のプロパティです。

| プロパティ | 既定値、例 |
|---|---|
| `Type` | 必須。`Canary10Percent5Minutes`、`Linear10PercentEvery1Minute`、`AllAtOnce`、カスタム設定の名前 |
| `Enabled` | `true` |
| `Alarms` | 発火でロールバックするアラーム |
| `Hooks` | `PreTraffic`、`PostTraffic` |
| `Role` | CodeDeploy が使うロール。省略すると自動で作られる |
| `TriggerConfigurations` | SNS の通知 |
| `PassthroughCondition` | `Enabled` のパラメータ化に使う |

| 関連のプロパティ | 効果 |
|---|---|
| `AutoPublishAlias` | コードの変更で新しいバージョンを作り、エイリアスを更新する |
| `AutoPublishCodeSha256` | バージョンの発行を決めるコードのハッシュを指定 |
| `AutoPublishAliasAllProperties` | `true` でコード以外の変更でも新しいバージョンを作る |

**落とし穴**: `AutoPublishAlias` がないと、`DeploymentPreference` で移すバージョンがありません。フック関数は結果を報告するので、`codedeploy:PutLifecycleEventHookExecutionStatus` の権限が必要です。

`Type` の時間を計算します。

| `Type` | 移し方 | すべて移るまでの目安 |
|---|---|---|
| `Canary10Percent5Minutes` | 10% を移し、5 分後に残り 90% | 5 分 |
| `Canary10Percent30Minutes` | 10% を移し、30 分後に残り 90% | 30 分 |
| `Linear10PercentEvery1Minute` | 毎分 10% | 約 10 分 |
| `Linear10PercentEvery10Minutes` | 10 分ごとに 10% | 約 100 分 |
| `AllAtOnce` | すぐに 100% | 0 分 |

- **`Alarms` の例:** 5 分のカナリアの間に `OrdersErrorsAlarm` が発火すると、エイリアスは前のバージョンに戻ります。
- **`Hooks` の例:** `PreTraffic` で新しいバージョンをテスト呼び出しし、`Failed` を報告すると、トラフィックを移さず戻します。
- **`Enabled` の例:** `dev` でカナリアを待ちたくないなら `Enabled: false` にします。`Type: AllAtOnce` でもすぐに移ります。
- **`Role` の例:** ARN を指定すると、ロールは作られません。権限が足りないと、デプロイが失敗します。
- **`TriggerConfigurations` の例:** デプロイの失敗を SNS トピックへ通知します。
- **`PassthroughCondition` の例:** `true` にすると、関数の `Condition` が CodeDeploy のリソースにも渡ります。`false` だと、関数が作られない環境でも CodeDeploy のリソースが作られることがあります。
- **`AutoPublishCodeSha256` の例:** 外部で作ったパッケージのハッシュを渡し、コードの同一性の判定に使います。
- **`AutoPublishAliasAllProperties` の例:** `false` のとき、新しいバージョンが出るのは `Environment`、`MemorySize`、`SnapStart`、コードの変更だけです。`Timeout` だけを変えるなら `true` にします。
- **誤ると:** `STAGE: !Ref Stage` のパラメータだけを変えても、テンプレートの文字列は同じなので、新しいバージョンは出ません。`true` にしても同じです。`Transform` に `AWS::LanguageExtensions` を先に書くと解消します。

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

- **`--config-env` の例:** `sam deploy --config-env prod` は、`orders-prod` に `Stage=prod` でデプロイし、実行前に確認で止まります。`staging` は確認なしです。
- **`capabilities` の例:** `AWS::Serverless::Function` が実行ロールを作るので、`CAPABILITY_IAM` が必要です。書かないと `InsufficientCapabilities` です。
- **誤ると:** `--config-env` を付け忘れると `default` の設定が使われます。`default` がなければ `--guided` なしで失敗し、`default` が本番を指していると本番に出てしまいます。

### samconfig の構造 {#samconfig}

既定の名前は `samconfig`、場所はプロジェクトのルート、形式は TOML です。

```toml
version = 0.1

[default.global.parameters]
stack_name = "orders"

[default.build.parameters]
parallel = true

[default.deploy.parameters]
resolve_s3 = true
capabilities = "CAPABILITY_IAM"

[default.sync.parameters]
watch = true

[default.local_start_api.parameters]
warm_containers = "EAGER"
```

形式は `[環境.コマンド.parameters]` です。`sam local start-api` のような複数語のコマンドは `local_start_api` と書きます。

優先順位は、コマンドライン、コマンドごとの設定、`global` の順です。`--parameter-overrides` か `parameter_overrides` はテンプレートの `Parameters` の `Default` より優先されます。別のファイルなら `--config-file`、環境なら `--config-env` です。

- **優先順位の例:** `global` が `stack_name = "orders"`、`deploy` が `stack_name = "orders-dev"` なら、`sam deploy` は `orders-dev` です。`sam deploy --stack-name orders-x` なら `orders-x` です。
- **`parameter_overrides` の例:** テンプレートの `Default` が `dev` で、`parameter_overrides = "Stage=prod"` なら、`Stage` は `prod` です。
- **`warm_containers` の例:** `EAGER` は起動時に全関数のコンテナを作るので、`sam local start-api` の最初の呼び出しが速くなります。
- **`--config-file` の例:** `sam deploy --config-file ci/samconfig.toml` で CI 用の設定を読みます。

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

- **`body` の例:** ハンドラーは `json.loads(event["body"])["quantity"]` で 1 を読みます。`event["body"]["quantity"]` と書くと、文字列なので `TypeError` です。
- **`Records` の例:** 10 件のバッチなら `event["Records"]` の長さは 10 です。`Records[0]` だけを処理すると、残り 9 件が処理されません。
- **`generate-event` の例:** `--bucket my-bucket --key input.csv` を変えれば、キーが違う場合の分岐を試せます。
- **実行場所の例:** `sam local invoke` は IAM の権限を本番と同じには確かめません。権限の確認は `sam remote invoke` でデプロイ済みの関数に対して行います。

### 単体テスト {#unit-tests}

ハンドラーの中身を外部サービスから切り離して検証します。AWS への呼び出しは `botocore.stub.Stubber` やモックに置き換えます。

- **例:** 下のテストは `save_order` を `"o-1"` を返す関数に差し替えます。DynamoDB がなくても 201 と `orderId` を確かめられ、1 秒以内で終わります。

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

- **例:** `orders-staging` の `ApiUrl` を読むので、API の ID が変わってもテストを直さずに済みます。単体テストでは見つからない権限の不足も、ここで `403` や `500` として分かります。

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

- **ポーリングの計算例:** 下のテストは 3 秒ごとに 10 回確認するので、最大 30 秒待ちます。処理に 40 秒かかるなら足りません。回数を増やすか、間隔を延ばします。
- **`test-event-pattern` の例:** `{"source": ["orders"]}` のパターンに `"source": "orders"` のイベントを渡すと `true` です。`"source": "billing"` なら `false` です。
- **DLQ の例:** `maxReceiveCount: 3` なら、壊れたメッセージは 3 回の受信の後で DLQ に届きます。可視性タイムアウトが 60 秒なら、届くまで数分かかるので、テストの待ち時間を合わせます。

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

[:material-certificate: DVA](../courses/dva/services.md){ .exam-badge .exam-associate } [:material-certificate: SOA](../courses/soa/services.md){ .exam-badge .exam-associate } [:material-certificate: DEA](../courses/dea/services.md){ .exam-badge .exam-associate } [:material-certificate: MLA](../courses/mla/services.md){ .exam-badge .exam-associate } [:material-star-circle: SAP](../courses/sap/services.md){ .exam-badge .exam-professional } [:material-star-circle: DOP](../courses/dop/services.md){ .exam-badge .exam-professional } [:material-star-circle: AIP](../courses/aip/services.md){ .exam-badge .exam-professional }

プログラミング言語でインフラを定義し、CloudFormation テンプレートを生成します。CDK v2 が現行で、v1 のサポートは終了しています。

**提供単位**: CDK は手元や CI で動くツールです。生成したスタックはリージョンにデプロイされます（[2 つの軸](resource-scope.md#two-axes)）。

### コンストラクト {#cdk-constructs}

| レベル | 内容 | 例 |
|---|---|---|
| L1 | CloudFormation リソースと 1 対 1。名前は `Cfn` で始まる | `CfnBucket` |
| L2 | 既定値と便利なメソッドを備えた抽象化 | `s3.Bucket`、`bucket.grant_read(fn)` |
| L3 | 複数リソースをまとめたパターン | `ecs_patterns.ApplicationLoadBalancedFargateService` |

- **L1 の例:** `CfnBucket(self, "B", versioning_configuration={"status": "Enabled"})` は、CloudFormation のプロパティをそのまま書きます。
- **L2 の例:** `s3.Bucket(self, "Reports", versioned=True)` は 1 行で書けます。`bucket.grant_read(fn)` で IAM ポリシーも作ります。
- **L3 の例:** `ApplicationLoadBalancedFargateService` は、ALB、タスク定義、サービスなどをまとめて作ります。細かい調整が多いなら、L2 で組み立てます。

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

### アプリとスタック {#cdk-app-stack}

| 階層 | 役割 | 例 |
|---|---|---|
| App | 全体の入れ物 | `app = cdk.App()` |
| Stack | CloudFormation のスタック 1 つに対応 | `OrdersStack(app, "Orders", env=...)` |
| Construct | リソースの部品 | `s3.Bucket(self, "Reports")` |

```python
app = cdk.App()
OrdersStack(app, "Orders-prod", env=cdk.Environment(account="111122223333", region="ap-northeast-1"))
app.synth()
```

**論理 ID の落とし穴**: コンストラクトの ID や親子関係を変えると論理 ID が変わります。CloudFormation はこれを別のリソースと見なし、置き換えます。データを持つリソースでは `removal_policy=RemovalPolicy.RETAIN` も確認します。

- **`env` の例:** `env` を省くと、アカウントとリージョンを特定しないスタックになります。`Vpc.from_lookup` は具体的な環境が必要なので、`env` がないと失敗します。
- **Stack の例:** `OrdersStack(app, "Orders-dev")` と `OrdersStack(app, "Orders-prod")` で、同じコードから 2 つのスタックを作ります。
- **論理 ID の例:** `s3.Bucket(self, "Reports")` を `"ReportBucket"` に直すと、新しいバケットができて、古いバケットは既定の削除ポリシーに従います。`cdk diff` に置き換えが出たら止めます。

### CDK のコマンド {#cdk-cli}

| コマンド | 用途 |
|---|---|
| `cdk bootstrap` | デプロイに必要な資材をアカウントとリージョンに用意 |
| `cdk synth` | CloudFormation テンプレートを生成 |
| `cdk diff` | デプロイ済みスタックとの差分を表示 |
| `cdk deploy` | デプロイ |
| `cdk destroy` | スタックを削除 |

`cdk deploy` が初めて失敗するときは、`bootstrap` の未実行をまず疑います。

追加のコマンドとオプションです。

| コマンド、オプション | 用途 |
|---|---|
| `cdk init app --language python` | プロジェクトの雛形 |
| `cdk ls` | スタックの一覧 |
| `cdk watch` | 変更を監視して自動でデプロイ |
| `cdk deploy --all` | すべてのスタック |
| `cdk deploy --hotswap` | 可能なら CloudFormation を迂回して更新。開発用 |
| `cdk deploy --require-approval` | 手動の承認が必要な変更を指定 |
| `cdk deploy --no-rollback` | 失敗してもロールバックしない |
| `cdk deploy --parameters`、`--outputs-file` | パラメータの指定、出力の保存 |
| `cdk diff --fail` | 差分があれば非 0 で終わる。CI で使う |

オプションの例です。

- **`--require-approval` の例:** 既定は `broadening` で、権限やセキュリティグループのルールが広がるときに確認します。`any-change` はすべての変更で確認します。CI で止めたくないなら `never` です。
- **`--hotswap` の例:** Lambda のコードだけを変えたとき、CloudFormation を使わず直接更新します。既定は `false` です。スタックとのずれが生じるので、本番には使いません。ECS のサービスでは、最小正常割合が `0` になります。
- **`--no-rollback` の例:** 開発中に失敗した状態を残して、原因を調べます。
- **`--all` の例:** `Orders-dev` と `Orders-prod` の両方が対象になります。`cdk deploy Orders-dev` のように名前を指定すれば 1 つだけです。
- **`--outputs-file` の例:** `--outputs-file out.json` で出力を保存し、結合テストが URL を読みます。
- **`cdk watch` の例:** ファイルの保存を検知してデプロイします。開発用です。
- **`cdk diff --fail` の例:** デプロイ済みと同じなら 0、差分があれば非 0 で終わるので、差分の検知に使えます。

### ブートストラップ {#cdk-bootstrap}

```bash
cdk bootstrap aws://111122223333/ap-northeast-1
```

アカウントとリージョンの組み合わせごとに必要です。S3 バケット(アセット)、ECR リポジトリ(イメージ)、IAM ロールを作ります。

**症状**: 実行していないと、`cdk deploy` がブートストラップの不足のエラーで失敗します。別のリージョンへ増やしたときにも発生します。

- **計算例:** 2 アカウントと 3 リージョンで使うなら、2 × 3 = 6 回のブートストラップが必要です。
- **例:** Docker のイメージを使わないアプリでも、同じコマンドで同じ資材を作ります。スタック名は既定で `CDKToolkit` です。

### コンテキスト {#cdk-context}

| 指定 | 内容 |
|---|---|
| `cdk.json` | プロジェクトの設定と機能フラグ |
| `cdk.context.json` | 自動で保存されるルックアップの結果 |
| `--context key=value`、`-c` | コマンドラインから。値は常に文字列 |
| `self.node.try_get_context("key")` | コードから読む |
| `cdk context --reset キー`、`--clear` | キャッシュの削除 |

**例**: `Vpc.from_lookup` の結果は `cdk.context.json` に保存されます。以後は再利用され、合成の結果が変わりません。

**落とし穴**: `cdk.context.json` もソース管理に入れます。入れないと、別の環境での合成で値が変わることがあります。ファイルを手で編集せず、`cdk context` を使います。

- **`--context` の例:** `cdk deploy -c stage=prod` で渡し、`self.node.try_get_context("stage")` で `"prod"` を読みます。`-c count=3` は文字列の `"3"` なので、計算するなら `int()` で変換します。
- **`cdk.json` の例:** `"context": {"stage": "dev"}` と書くと既定値になります。`try_get_context` はキーがなければ `None` を返します。
- **`--reset` の例:** VPC を作り直したのに古い ID が使われるなら、`cdk context --reset <キー>` で消して取り直します。

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

- **`resource_count_is` の例:** 上のテストは S3 バケットが 1 個のときだけ通ります。コードの変更で 2 個に増えると失敗します。
- **`Match.any_value` の例:** `Variables` の中身は問わず、あることだけを確かめます。
- **スナップショットの例:** 前回のテンプレートと比べるので、CDK の更新でテンプレートが変わっただけでも失敗します。意図した変更なら、スナップショットを更新します。

### テンプレートの検証方法のまとめ {#validate-iac}

| ツール | 検証の方法 |
|---|---|
| CloudFormation | `aws cloudformation validate-template`、変更セット、cfn-lint |
| SAM | `sam validate --lint`、`sam local invoke`、`sam local start-api` |
| CDK | `cdk synth`、`cdk diff`、`assertions` によるテスト |

- **`validate-template` の例:** `Resources` の綴りは見つけますが、`InstanceType: foo` のような値の誤りは、実際に作るまで分かりません。
- **cfn-lint の例:** `cfn-lint template.yaml` で、リソースのプロパティ名の綴りも確かめます。
- **`cdk diff` の例:** バケットの行に `[-]` の削除や `requires replacement` の表示が出たら、デプロイを止めて論理 ID の変更を確認します。

## AWS CLI {#aws-cli}

[:material-sprout: CLF](../courses/clf/services.md){ .exam-badge .exam-foundational } [:material-certificate: SAA](../courses/saa/services.md){ .exam-badge .exam-associate } [:material-certificate: DVA](../courses/dva/services.md){ .exam-badge .exam-associate } [:material-certificate: DEA](../courses/dea/services.md){ .exam-badge .exam-associate } [:material-star-circle: DOP](../courses/dop/services.md){ .exam-badge .exam-professional } [:material-star-circle: AIP](../courses/aip/services.md){ .exam-badge .exam-professional } [:material-target: ANS](../courses/ans/services.md){ .exam-badge .exam-specialty }

**提供単位**: AWS CLI は手元で動くツールで、呼び先のリージョンを `--region` や設定で決めます（[2 つの軸](resource-scope.md#two-axes)）。

- **例:** `--region us-east-1` を付けると、手元が日本でも、バージニア北部のリソースを見ます。東京に作ったインスタンスは一覧に出ません。

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

- **`[profile 名前]` の例:** `config` に `[staging]` と書くと、プロファイルとして読まれません。`[profile staging]` にします。`credentials` は `[staging]` です。
- **`sso_session` の例:** `aws sso login --profile staging` でブラウザから認証し、一時的な認証情報を使います。アクセスキーをファイルに置きません。
- **`AWS_PROFILE` の例:** `export AWS_PROFILE=staging` の後は `--profile` を省けます。別のシェルには引き継がれません。
- **`region` の例:** `aws --region ap-northeast-3 ec2 describe-instances` は、`config` の `ap-northeast-1` より優先します。

### 設定ファイルと優先順位 {#cli-config}

```ini
# ~/.aws/credentials
[default]
aws_access_key_id = <アクセスキー ID>
aws_secret_access_key = <シークレットアクセスキー>
```

```ini
# ~/.aws/config
[profile prod]
region = ap-northeast-1
output = json
role_arn = arn:aws:iam::111122223333:role/Deploy
source_profile = default
retry_mode = standard
max_attempts = 3
```

| 優先順 | 場所 |
|---|---|
| 1 | コマンドラインのオプション(`--region`、`--output`、`--profile`) |
| 2 | 環境変数 |
| 3 | ロールの引き受け |
| 4 | Web ID によるロールの引き受け |
| 5 | IAM Identity Center |
| 6 | `credentials` ファイル |
| 7 | カスタムプロセス |
| 8 | `config` ファイル |
| 9 | コンテナの認証情報 |
| 10 | EC2 のインスタンスプロファイル |

同じプロファイルの認証情報が両方のファイルにあれば、`credentials` が優先されます。

| 環境変数 | 意味 |
|---|---|
| `AWS_ACCESS_KEY_ID`、`AWS_SECRET_ACCESS_KEY` | 認証情報 |
| `AWS_SESSION_TOKEN` | 一時認証情報のトークン |
| `AWS_PROFILE` | プロファイル |
| `AWS_REGION` | リージョン。`AWS_DEFAULT_REGION` より優先 |
| `AWS_DEFAULT_OUTPUT` | 出力形式 |
| `AWS_PAGER` | ページャー。空にすると無効 |
| `AWS_CONFIG_FILE`、`AWS_SHARED_CREDENTIALS_FILE` | 設定ファイルの場所 |
| `AWS_MAX_ATTEMPTS`、`AWS_RETRY_MODE` | 再試行 |

**例**: `AWS_ACCESS_KEY_ID` が環境に残っていると、`credentials` の `[prod]` を入れ替えても環境変数の認証情報が使われます。`--profile prod` を指定すれば、プロファイルが優先されます。`aws sts get-caller-identity` で確かめます。

**再試行**: 既定の `standard` モードでは、最大 2 回の再試行で合計 3 回の呼び出しです。

- **`max_attempts` の例:** 最初の呼び出しも数えます。`max_attempts = 3` は最初の 1 回と再試行 2 回です。`1` にすると再試行しません。
- **`retry_mode` の例:** v2 の既定は `standard` です。`adaptive` は送信の速度も調整します。`legacy` は v1 の既定です。
- **`AWS_MAX_ATTEMPTS` の例:** `export AWS_MAX_ATTEMPTS=5` は `config` の `max_attempts` より優先します。
- **`AWS_REGION` の例:** `AWS_REGION=us-west-2`、`AWS_DEFAULT_REGION=us-east-1` なら、`us-west-2` です。
- **`AWS_SESSION_TOKEN` の例:** STS の一時認証情報では 3 つの値が必要です。キーの 2 つだけを設定すると、トークンがないので `InvalidClientTokenId` などのエラーになります。
- **`AWS_PAGER` の例:** `AWS_PAGER=""` にすると、CI で `less` の待ちで止まりません。
- **`AWS_CONFIG_FILE` の例:** `AWS_CONFIG_FILE=./ci/config` で CI 用の設定を読みます。

| ロールの設定 | 意味 |
|---|---|
| `role_arn` | 引き受けるロール |
| `source_profile` | 認証に使うプロファイル |
| `credential_source` | `Ec2InstanceMetadata` などの認証情報の取得元。`source_profile` の代わりに使う |

- **`role_arn` と `source_profile` の例:** 上の `[profile prod]` は、`default` の認証情報で `Deploy` ロールを引き受けます。`aws sts get-caller-identity --profile prod` の `Arn` は `assumed-role/Deploy/...` です。
- **`credential_source` の例:** EC2 の上で `credential_source = Ec2InstanceMetadata` と書くと、インスタンスプロファイルの権限でロールを引き受けます。
- **誤ると:** `source_profile` と `credential_source` を両方書くとエラーです。どちらも書かないと、ロールを引き受けられません。

### 出力形式 {#cli-output}

| `--output` | 用途 |
|---|---|
| `json` | 既定。プログラムで処理 |
| `yaml` / `yaml-stream` | 読みやすい形式。`yaml-stream` は逐次出力 |
| `text` | タブ区切り。シェルで加工 |
| `table` | 人が読む |
| `off` | 標準出力を抑止。CI で終了コードだけ使う |

同じ結果を出力形式ごとに見ます。

- **`json` の例:** `{"Functions": [{"FunctionName": "orders"}]}` のように、構造のまま出します。`jq` に渡せます。
- **`text` の例:** `--query "Functions[].FunctionName" --output text` は `orders	reports` とタブ区切りで出ます。`for fn in $(...)` で回せます。
- **`table` の例:** 枠線の付いた表です。行が崩れないので目視に向きますが、スクリプトで読むには向きません。
- **`yaml-stream` の例:** 大きな結果を順に出力するので、全件を待ちません。
- **`off` の例:** `aws s3api head-bucket --bucket my-bucket --output off` は何も出さず、`$?` でバケットの有無を判定します。

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

`--query` の主な書き方です。

| 書き方 | 意味 |
|---|---|
| `Reservations[].Instances[]` | 配列を平らにする |
| `Functions[?Runtime=='python3.12']` | 条件で絞る |
| `Functions[].{Name:FunctionName,Mem:MemorySize}` | 項目を選び、名前を付ける |
| `sort_by(Images, &CreationDate)[-1]` | 並べ替えて最後の 1 件 |
| `length(Functions)` | 件数 |

ページネーションのある API では、`--query` はサービス側の結果を受けた後に動きます。`--max-items` を使っても、絞り込みは取得した分に対して行われます。

- **`Functions[?Runtime=='python3.12']` の例:** 関数が 3 つで、`python3.12` が 2 つなら、2 件だけ返します。
- **`{Name:FunctionName,Mem:MemorySize}` の例:** `[{"Name": "orders", "Mem": 1024}]` のように、名前を変えて返します。
- **`sort_by` の例:** `aws ec2 describe-images --owners self --query "sort_by(Images, &CreationDate)[-1].ImageId" --output text` で、自分の最新の AMI の ID を読みます。
- **`length` の例:** `--query "length(Functions)"` は件数の数字だけを返します。
- **`--filters` との違いの例:** 10,000 台のうち `running` が 10 台なら、`--filters` はサーバー側で 10 台に絞って返します。`--query` だけなら 10,000 台分を受け取ってから絞ります。
- **誤ると:** シェルが `'` や `?` を解釈して失敗することがあります。式全体を引用符で囲みます。`--max-items 100 --query "...[?Runtime=='python3.12']"` は、100 件のうち条件に合う分しか返さないことがあります。

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

既定では S3 のページサイズは 1,000 です。大きなバケットで `--page-size 100` にすると、呼び出しが増えますが、1 回あたりの処理が軽くなり、タイムアウトを避けられます。

**スケルトンの生成**: `--generate-cli-skeleton` で入力の雛形を作り、`--cli-input-json file://input.json` か `--cli-input-yaml` で実行できます。原因の調査には `--debug` を使います。

**計算例**: オブジェクトが 3,500 個のバケットを `aws s3api list-objects-v2` で読みます。

| オプション | API 呼び出し | 出力 |
|---|---|---|
| なし | 3,500 ÷ 1,000 を切り上げて 4 回 | 3,500 個 |
| `--page-size 100` | 3,500 ÷ 100 = 35 回 | 3,500 個 |
| `--no-paginate` | 1 回 | 1,000 個 |
| `--max-items 100` | 必要な分だけ | 100 個と `NextToken` |

- **`--page-size` の誤り:** 件数を減らしたいときに `--page-size 100` を使っても、全件が返ります。出力を減らすなら `--max-items` です。
- **`--starting-token` の例:** `--max-items 100` の結果の `NextToken` を渡すと、101 個目から返します。
- **`--no-cli-pager` の例:** 長い出力でも `less` が開かないので、スクリプトが止まりません。

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

- **`DryRunOperation` の例:** 上のコマンドは実行できそうなら `DryRunOperation` のエラーで終わり、インスタンスは起動しません。エラーの形で返るので、終了コードは 0 以外です。
- **`UnauthorizedOperation` の例:** `ec2:RunInstances` の許可がなければこちらです。
- **`simulate-principal-policy` の例:** `--policy-source-arn arn:aws:iam::111122223333:role/Deploy --action-names s3:GetObject` で、`allowed` か `implicitDeny` などの結果を確かめます。

## CloudShell {#cloudshell}

[:material-certificate: DVA](../courses/dva/services.md){ .exam-badge .exam-associate } [:material-star-circle: DOP](../courses/dop/services.md){ .exam-badge .exam-professional }

マネジメントコンソールから起動できるブラウザ上のシェルです。Amazon Linux 2023 ベースで、AWS CLI などが導入済みです。

**提供単位**: 環境はリージョンごとで、既定では VPC の外です。VPC の中でも起動できます（[2 つの軸](resource-scope.md#two-axes)）。

| 項目 | 内容 |
|---|---|
| 認証 | コンソールのサインイン情報をそのまま使える |
| 永続ストレージ | リージョンごとに `$HOME` へ 1 GB（無料） |
| データ保持 | 最後のセッションから 120 日使わないと削除対象 |
| 非アクティブ時 | 20〜30 分操作がないとセッション終了 |
| 長時間実行 | 約 12 時間でセッション終了 |
| シェル | Bash、PowerShell、Z shell |
| VPC 環境 | VPC 内で起動可能。ただし永続ストレージなし |

環境の仕様と上限です。

| 項目 | 値 |
|---|---|
| コンピュート | 1 vCPU、2 GiB の RAM |
| 同時に開けるシェル | リージョンごとに 10 |
| 月の利用量 | リージョンごとにクォータあり。引き上げ可能 |
| VPC 環境の時間切れ | 20〜30 分の非アクティブ。`$HOME` が消える |

**落とし穴**: 非アクティブの判定はキーボードとポインターの操作だけです。プロセスが動いていても、操作がなければ終わります。長いジョブには向きません。

- **永続ストレージの例:** 東京の `$HOME` に置いたスクリプトは、大阪のシェルには見えません。リージョンごとに 1 GB です。2 GB のファイルは置けません。
- **データ保持の例:** 東京の CloudShell を 1 月 1 日に最後に使うと、120 日後の 5 月 1 日ごろに削除の対象になります。残すなら、その前に一度使います。
- **VPC 環境の例:** プライベートサブネットの RDS に接続するために使います。`$HOME` は 20〜30 分の非アクティブで消えるので、スクリプトは S3 などに置きます。
- **認証の例:** コンソールに `Developer` ロールでサインインしていれば、CloudShell の CLI も同じ権限です。`aws sts get-caller-identity` で確かめます。
- **セッションの例:** 3 時間のジョブを実行してポインターを動かさないと、20〜30 分で終わります。約 12 時間を超えるジョブは、操作していても終わります。

## 既定値と上限のまとめ {#numbers}

| 項目 | 値 |
|---|---|
| テンプレートの本文 / S3 | 51,200 バイト / 1 MB |
| リソース / パラメータ / 出力 / マッピング | 500 / 200 / 200 / 200 |
| パラメータの値 | 4,096 バイト |
| 動的参照 | テンプレートに 60 個 |
| ロールバックトリガー | 5 個、監視 0〜180 分 |
| `CreationPolicy` の `Count` / `Timeout` | 1 / `PT5M`(最大 12 時間) |
| `MaxBatchSize` / `MinInstancesInService` | 1(最大 100)/ 0 |
| `cfn-hup` の間隔 | 15 分 |
| カスタムリソースの `ServiceTimeout` | 既定 3,600 秒、1〜3,600 |
| Description | 1,024 バイト |
| `Fn::And`、`Fn::Or` の条件 | 2〜10 個 |
| CLI の再試行(`standard`) | 2 回(合計 3 回) |
| S3 の既定のページサイズ | 1,000 |
| CloudShell の永続ストレージ | リージョンごとに 1 GB |
| CloudShell のデータ保持 | 120 日 |
| CloudShell の非アクティブ / 長時間 | 20〜30 分 / 約 12 時間 |
| CloudShell の同時シェル | 10 |

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

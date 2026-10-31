# ガバナンス

[:material-sprout: CLF](../courses/clf/services.md){ .exam-badge .exam-foundational } [:material-sprout: AIF](../courses/aif/services.md){ .exam-badge .exam-foundational } [:material-certificate: SAA](../courses/saa/services.md){ .exam-badge .exam-associate } [:material-certificate: SOA](../courses/soa/services.md){ .exam-badge .exam-associate } [:material-certificate: DEA](../courses/dea/services.md){ .exam-badge .exam-associate } [:material-certificate: MLA](../courses/mla/services.md){ .exam-badge .exam-associate } [:material-star-circle: SAP](../courses/sap/services.md){ .exam-badge .exam-professional } [:material-star-circle: DOP](../courses/dop/services.md){ .exam-badge .exam-professional } [:material-star-circle: AIP](../courses/aip/services.md){ .exam-badge .exam-professional } [:material-target: ANS](../courses/ans/services.md){ .exam-badge .exam-specialty } [:material-target: SCS](../courses/scs/services.md){ .exam-badge .exam-specialty }

複数の AWS アカウントを、まとめて管理して統制するためのサービスです。組織の構造を作る Organizations、環境を整える Control Tower、設定を監査する Config を中心に扱います。

[![マルチアカウント構成の例](../assets/diagrams/governance-multi-account.png)](../assets/diagrams/governance-multi-account.png)

| サービス | 役割 | 一言で |
| --- | --- | --- |
| [Organizations](#organizations) | アカウントの階層化、ポリシー、一括請求 | 組織の土台 |
| [Control Tower](#control-tower) | ベストプラクティスの環境の構築と統制 | 土台の自動構築 |
| [Config](#config) | リソースの設定の記録と評価 | 設定の監査 |
| [Service Catalog](#service-catalog) | 承認済みの構成をセルフサービスで提供 | 社内カタログ |
| [Resource Access Manager](#ram) | リソースをアカウント間で共有 | 共有 |
| [License Manager](#license-manager) | ソフトウェアライセンスの追跡と制限 | ライセンス |
| [Resource Groups と Tag Editor](#resource-groups) | タグでリソースをまとめて操作 | 整理 |

## AWS Organizations {#organizations}

[:material-sprout: CLF](../courses/clf/services.md){ .exam-badge .exam-foundational } [:material-certificate: SAA](../courses/saa/services.md){ .exam-badge .exam-associate } [:material-certificate: SOA](../courses/soa/services.md){ .exam-badge .exam-associate } [:material-certificate: MLA](../courses/mla/services.md){ .exam-badge .exam-associate } [:material-star-circle: SAP](../courses/sap/services.md){ .exam-badge .exam-professional } [:material-star-circle: DOP](../courses/dop/services.md){ .exam-badge .exam-professional } [:material-target: ANS](../courses/ans/services.md){ .exam-badge .exam-specialty } [:material-target: SCS](../courses/scs/services.md){ .exam-badge .exam-specialty }

複数のアカウントを 1 つの組織にまとめるサービスです。追加料金はかかりません。

組織は、ルート 1 つの下に OU（組織単位）とアカウントを置く構造です。管理アカウントが 1 つあり、残りがメンバーアカウントです。

### 機能セット {#org-feature-sets}

| 機能セット | できること | 既定 |
| --- | --- | --- |
| すべての機能 | 一括請求、ポリシー、サービス連携 | 新規作成の既定で推奨 |
| 一括請求のみ | 1 枚の請求書にまとめるだけ | SCP や RCP は使えない |

一括請求のみからすべての機能へは移行できますが、逆には戻せません。

SCP を使おうとして使えない場合は、`aws organizations describe-organization` で `FeatureSet` を確認し、さらにルートでポリシータイプが有効かを確認します。

### OU の設計 {#org-ous}

ポリシーは OU に付けると配下へ継承されます。そのため、OU は人事上の部署ではなく、適用したいポリシーの違いで分けます。

ネストは 5 階層までです。深くすると SCP の評価が追いにくくなります。

### ポリシーの種類 {#org-policy-types}

| 種類 | 区分 | 管理アカウントへの影響 | 対象に付けられる数 | 最大サイズ |
| --- | --- | --- | --- | --- |
| SCP | 認可 | なし | 10 | 10,240 文字 |
| RCP | 認可 | なし | 5 | 5,120 文字 |
| タグポリシー | 宣言型 | あり | 10 | 10,000 文字 |
| バックアップポリシー | 宣言型 | あり | 10 | 10,000 文字 |
| 宣言型ポリシー（EC2） | 宣言型 | あり | 10 | 10,000 文字 |
| AI サービスのオプトアウト | 宣言型 | あり | 5 | 2,500 文字 |

このほか、チャットアプリ、Security Hub、Inspector、Bedrock、S3、GuardDuty、アップグレードのロールアウトのポリシーがあります。

SCP の値は、古い教材の「5 個、5,120 文字」から増えています。

### SCP {#scp}

[:material-certificate: SOA](../courses/soa/services.md){ .exam-badge .exam-associate }

組織内の IAM ユーザーとロールが使える権限の上限を決めるポリシーです。権限は与えません。実際に使うには、IAM ポリシーなどでの許可も必要です。

```mermaid
flowchart TD
  A["リクエスト"] --> B{"どの階層でも SCP の Deny があるか"}
  B -- "ある" --> X["拒否"]
  B -- "ない" --> C{"ルートから対象アカウントまで全階層に Allow があるか"}
  C -- "ない" --> X
  C -- "ある" --> D{"IAM ポリシーなどで許可されているか"}
  D -- "ない" --> X
  D -- "ある" --> E["許可"]
```

| 設定 | 動作 | 誤ったときの症状 |
| --- | --- | --- |
| `FullAWSAccess` | SCP を有効にすると既定で付く、全許可の SCP | 外して代わりを付けないと、メンバーアカウントの全操作が失敗する |
| Deny リスト方式 | `FullAWSAccess` を残して Deny を足す | 新サービスも既定で使える |
| Allow リスト方式 | `FullAWSAccess` を外して許可を列挙 | 途中の階層に Allow がないと、そのサービスが使えない |

次の例は、東京リージョン以外での EC2 起動を拒否します。

```json
{
  "Version": "2012-10-17",
  "Statement": [{
    "Sid": "DenyRunInstancesOutsideTokyo",
    "Effect": "Deny",
    "Action": "ec2:RunInstances",
    "Resource": "*",
    "Condition": {
      "StringNotEquals": {"aws:RequestedRegion": "ap-northeast-1"}
    }
  }]
}
```

SCP は次のものを制限できません。

- 管理アカウントのユーザーとロールの操作
- サービスリンクロールの権限で行う操作
- CloudFront の信頼された署名者の機能など、一部の操作

委任管理者のアカウントはメンバーアカウントなので、SCP の影響を受けます。

適用前に影響を試すには、ルートに直接付けず、テスト用の OU にアカウントを少しずつ移します。IAM の「最後にアクセスしたサービス」の情報で、使われているサービスを確認できます。

SCP と権限境界の違いは [IAM](iam.md#boundaries-scp) を参照してください。

### RCP {#rcp}

組織内のリソースに対する権限の上限を決めるポリシーです。SCP は主体（自分の組織のユーザーやロール）を制限し、RCP はリソースへのアクセス（外部の主体を含む）を制限します。

| 観点 | SCP | RCP |
| --- | --- | --- |
| 制限の対象 | メンバーアカウントの IAM ユーザーとロール | メンバーアカウントのリソース |
| 主な用途 | 自社の人に禁止したいことを止める | 外部からのアクセスを防ぐ |
| 既定のポリシー | `FullAWSAccess` | `RCPFullAWSAccess`（外せず、上限 5 個に含まれる） |
| Effect | Allow、Deny | Deny のみ（Allow は `RCPFullAWSAccess` のみ） |
| 効かないもの | 管理アカウント、サービスリンクロール | 管理アカウントのリソース、サービスリンクロール、AWS 管理の KMS キー |

対象サービスには S3、STS、KMS、SQS、Secrets Manager などがあります。対象は増えているので、公式の一覧で確認します。

次の例は、組織の外の主体による S3 アクセスを拒否します。バケットポリシーを誤って公開しても、外部からはアクセスできなくなります。

```json
{
  "Version": "2012-10-17",
  "Statement": [{
    "Sid": "EnforceOrgIdentities",
    "Effect": "Deny",
    "Principal": "*",
    "Action": "s3:*",
    "Resource": "*",
    "Condition": {
      "StringNotEqualsIfExists": {"aws:PrincipalOrgID": "o-exampleorgid"},
      "BoolIfExists": {"aws:PrincipalIsAWSService": "false"}
    }
  }]
}
```

外部のパートナーからのアクセスが必要な場合に例外を入れないと、その連携が止まります。SCP と同様に、テスト用の OU で試してから広げます。

### タグポリシー {#tag-policies}

組織内のタグを標準化するポリシーです。タグキーの大文字小文字と、使える値を決めます。

```json
{
  "tags": {
    "CostCenter": {
      "tag_key": {"@@assign": "CostCenter"},
      "tag_value": {"@@assign": ["HR", "Legal"]},
      "enforced_for": {"@@assign": ["ec2:instance"]}
    }
  }
}
```

| 機能 | 内容 | 注意 |
| --- | --- | --- |
| 基本のコンプライアンスルール | `enforced_for` で、不適合な値を持つ作成や変更を止める | タグなしのリソース作成は止めない |
| 必須タグキー | 必須のキーを定義する。CloudFormation、Terraform、Pulumi などの IaC で適用 | IaC 向けの機能 |
| レポート | 不適合のリソースを報告する | 報告だけでは止まらない |

「タグなしの作成を、IaC 以外も含めて止めたい」なら、SCP で `aws:RequestTag` を条件にして拒否します。

事後の検出には Config の `required-tags` ルールが使えます。

### 委任管理者 {#delegated-admin}

管理アカウントは、SCP が効かないため権限を強く絞りたいアカウントです。そこで、管理の業務をメンバーアカウントに委任します。

| 委任の範囲 | 方法 | 例 |
| --- | --- | --- |
| Organizations のポリシー管理 | リソースベースの委任ポリシー（最大 40,000 文字） | セキュリティ担当アカウントで SCP を管理 |
| 各サービスの組織管理 | 各サービスで委任管理者を登録 | Config、Security Hub、Health の組織ビュー |

ワークロードは管理アカウントに置かず、メンバーアカウントに置きます。

## AWS Control Tower {#control-tower}

[:material-sprout: CLF](../courses/clf/services.md){ .exam-badge .exam-foundational } [:material-certificate: SAA](../courses/saa/services.md){ .exam-badge .exam-associate } [:material-certificate: SOA](../courses/soa/services.md){ .exam-badge .exam-associate } [:material-star-circle: SAP](../courses/sap/services.md){ .exam-badge .exam-professional } [:material-star-circle: DOP](../courses/dop/services.md){ .exam-badge .exam-professional } [:material-target: ANS](../courses/ans/services.md){ .exam-badge .exam-specialty } [:material-target: SCS](../courses/scs/services.md){ .exam-badge .exam-specialty }

ベストプラクティスに沿ったマルチアカウント環境を構築し、統制するサービスです。Organizations、Service Catalog、IAM Identity Center などを組み合わせて動かします。

| 要素 | 内容 |
| --- | --- |
| ランディングゾーン | ベストプラクティスに沿った環境全体 |
| コントロール | 環境に適用する統制のルール。旧称はガードレール |
| Account Factory | 承認済みの設定で新しいアカウントを用意するテンプレート。Service Catalog 上に構築 |
| ダッシュボード | アカウント、コントロール、非準拠のリソースの概要 |

### ランディングゾーンの構造 {#ct-landing-zone}

コンソールから作ると、Security OU と任意の Sandbox OU が作られます。Security OU には、ログ保管（Log Archive）と監査（Audit）のアカウントが入ります。

ランディングゾーンのバージョン 4.0 では Security OU は必須でなくなり、自分の組織の構造を定義できます。バージョン 3.3 以前では、これらのアカウントは初回作成時に決まります。

### コントロール {#ct-controls}

動作で 3 種類、適用の方針で 3 種類に分かれます。

| 動作 | 働き | 実装 |
| --- | --- | --- |
| 予防的 | 操作を止める | SCP、RCP |
| 検出的 | 違反を見つける | Config ルール |
| プロアクティブ | 作成前に確認し、不適合なら作らない | CloudFormation Hooks |

| 適用の方針 | 内容 |
| --- | --- |
| 必須 | 常に適用され、変更できない |
| 強く推奨 | 任意で有効化 |
| 選択的 | 任意で有効化 |

コントロールは OU 単位で適用され、配下の全アカウントに影響します。

管理アカウントには予防的コントロールが適用されません。

### ドリフトと拡張 {#ct-drift}

Control Tower の外で OU やアカウント、SCP を変更すると、ドリフト（設定のずれ）になります。検出は自動ですが、解消は手動です。ランディングゾーン設定の **Reset**（バージョン 3.1 未満は **Update**）、OU の **Re-register OU**、アカウントの **Update account**、または `ResetEnabledControl`、`ResetEnabledBaseline` の API を使います。

| 拡張の方法 | 内容 |
| --- | --- |
| Account Factory for Terraform（AFT） | Terraform と Git でアカウントを発行、カスタマイズする。アプリのリソースのデプロイ用ではない |
| Customizations for Control Tower（CfCT） | テンプレートとポリシーを追加で展開する |

| 制限 | 値 |
| --- | --- |
| ランディングゾーンのアカウント数 | 最大 10,000 |
| OU あたりの SCP | 10 |
| 同時に進められるアカウント操作 | 5 |
| 同時に進められるコントロール操作 | 100 |

## AWS Config {#config}

[:material-sprout: CLF](../courses/clf/services.md){ .exam-badge .exam-foundational } [:material-sprout: AIF](../courses/aif/services.md){ .exam-badge .exam-foundational } [:material-certificate: SAA](../courses/saa/services.md){ .exam-badge .exam-associate } [:material-certificate: SOA](../courses/soa/services.md){ .exam-badge .exam-associate } [:material-certificate: DEA](../courses/dea/services.md){ .exam-badge .exam-associate } [:material-certificate: MLA](../courses/mla/services.md){ .exam-badge .exam-associate } [:material-star-circle: SAP](../courses/sap/services.md){ .exam-badge .exam-professional } [:material-star-circle: DOP](../courses/dop/services.md){ .exam-badge .exam-professional } [:material-target: ANS](../courses/ans/services.md){ .exam-badge .exam-specialty } [:material-target: SCS](../courses/scs/services.md){ .exam-badge .exam-specialty }

リソースの設定の履歴を記録し、ルールに合っているかを評価するサービスです。「いつ、どう設定が変わったか」と「今の設定が基準に合っているか」に答えます。

```mermaid
flowchart TD
  A["リソースの設定変更"] --> B["設定レコーダーが CI を記録"]
  B --> C["S3 へ履歴とスナップショットを配信"]
  B --> D["Config ルールで評価"]
  D --> E{"準拠しているか"}
  E -- "非準拠" --> F["通知、または SSM Automation で修復"]
  E -- "準拠" --> G["記録のみ"]
```

### 設定レコーダー {#config-recorder}

設定の状態を設定項目（CI）として記録します。リージョンごとに有効にします。

| 設定 | 動作 | 既定、範囲 | 誤ったときの症状 |
| --- | --- | --- | --- |
| 記録の範囲 | 記録するリソースタイプ | 既定で、そのリージョンのサポートされる全リソース | 除外すると、そのタイプはルールで評価されない |
| 記録頻度 | 継続的または日次 | 継続的は変更のたびに記録 | 変更が多い環境は継続的だと CI の費用が増える |
| 保持期間 | CI を保持する期間 | 30 日から 2,557 日。既定は 7 年 | 短いと、監査で古い履歴を確認できない |
| 配信チャネル | S3 と SNS | S3 のライフサイクルは別に管理 | バケットポリシーの不足で配信が失敗する |

料金は、CI とルールの評価の回数によります。バージニア北部の例では、継続的な CI が 0.003 USD、日次の CI が 0.012 USD です。

### Config ルール {#config-rules}

| 観点 | 種類 | 内容 |
| --- | --- | --- |
| 作り方 | マネージドルール | AWS が用意したルール。`s3-bucket-public-read-prohibited` など |
| 作り方 | カスタムルール | Lambda などで自分で作る |
| トリガー | 設定変更 | 対象リソースの変更時に評価 |
| トリガー | 定期 | 指定した間隔で評価。例: 24 時間ごと |
| トリガー | ハイブリッド | 両方 |
| 評価モード | 検出的 | 作成済みのリソースを評価 |
| 評価モード | プロアクティブ | 作成前のプロパティを評価 |

**ルールは止めません。** プロアクティブ評価でも、判定するだけで修復やデプロイの阻止はしません。止めるなら SCP や Control Tower のプロアクティブコントロールを使います。

複数のアカウントで同じルールを使う組織ルールは、API か CLI でしか作れません。コンソールには対応していません。

### 修復 {#config-remediation}

非準拠のリソースを、Systems Manager Automation のドキュメントで修復します。手動と自動を選べます。

```bash
aws configservice put-remediation-configurations --remediation-configurations '[{
  "ConfigRuleName": "s3-bucket-public-read-prohibited",
  "TargetType": "SSM_DOCUMENT",
  "TargetId": "AWS-DisableS3BucketPublicReadWrite",
  "Automatic": true,
  "MaximumAutomaticAttempts": 5,
  "RetryAttemptSeconds": 60,
  "Parameters": {
    "S3BucketName": {"ResourceValue": {"Value": "RESOURCE_ID"}},
    "AutomationAssumeRole": {"StaticValue": {"Values": ["arn:aws:iam::111122223333:role/ConfigRemediationRole"]}}
  }
}]'
```

| 項目 | 内容 | 既定、範囲 | 誤ったときの症状 |
| --- | --- | --- | --- |
| `Automatic` | 自動修復するか | 手動か自動を選択 | `false` のままだと修復が走らない |
| `MaximumAutomaticAttempts` | 失敗を許す回数 | 既定 5、1 から 25 | 超えると修復の例外が付いて、止まる |
| `RetryAttemptSeconds` | 上の回数を数える時間枠 | 1 から 2,678,000 秒 | 短いとすぐ例外になる |
| 実行ロール | Automation が使う IAM ロール | 自分で用意 | 権限不足で修復が失敗する |

サービスリンクルールの修復は管理できません。

### アグリゲーター {#config-aggregators}

複数のアカウントとリージョンの Config データを 1 か所で見るための仕組みです。追加料金はかかりません。

- 組織全体、または個別に指定したアカウントを対象にできる。
- 読み取り専用のビューで、ここからルールの展開や修復はできない。
- 個別指定の場合、ソースアカウント側の認可が必要。組織の場合は不要。
- 上限はアグリゲーター 50 個、1 つあたり 10,000 アカウント。

高度なクエリ（SQL に似た構文）で「暗号化されていない EBS ボリュームを全アカウントから探す」といった検索ができます。

### 適合パック {#config-conformance-packs}

ルールと修復アクションを 1 つにまとめて、アカウントや組織に展開する単位です。YAML のテンプレートで定義します。

```yaml
Resources:
  S3PublicReadProhibited:
    Type: AWS::Config::ConfigRule
    Properties:
      ConfigRuleName: s3-bucket-public-read-prohibited
      Source:
        Owner: AWS
        SourceIdentifier: S3_BUCKET_PUBLIC_READ_PROHIBITED
```

サンプルのテンプレートが公開されています。上限は 1 パックあたり 130 ルール、アカウントあたり 50 パックです。パック内のルールも、1 リージョンあたり 1,000 ルールの上限に数えられます。

| 違い | 見方 |
| --- | --- |
| 個別ルールとの違い | 複数ルールをまとめて展開、管理する |
| アグリゲーターとの違い | パックは展開、アグリゲーターは集約して閲覧 |

## Config と CloudTrail の違い {#config-vs-cloudtrail}

| 観点 | Config | CloudTrail | CloudWatch |
| --- | --- | --- | --- |
| 答える問い | 設定はどう変わり、基準に合っているか | 誰がいつどの API を呼んだか | 性能や動作はどうか |
| 記録するもの | 設定の状態（CI） | API の呼び出しイベント | メトリクス、ログ |
| 評価 | ルールで判定 | しない | アラームのしきい値 |
| 典型の問い | S3 が公開設定か | 誰がセキュリティグループを変更したか | CPU 使用率が高いか |

Config のタイムラインから、CloudTrail のイベントへたどることができます。両方を組み合わせると、「何がどう変わり、誰が変えたか」が分かります。

CloudTrail の設定は [オブザーバビリティ](observability.md#cloudtrail) を参照してください。

## AWS Service Catalog {#service-catalog}

[:material-sprout: CLF](../courses/clf/services.md){ .exam-badge .exam-foundational } [:material-certificate: SAA](../courses/saa/services.md){ .exam-badge .exam-associate } [:material-certificate: SOA](../courses/soa/services.md){ .exam-badge .exam-associate } [:material-certificate: MLA](../courses/mla/services.md){ .exam-badge .exam-associate } [:material-star-circle: DOP](../courses/dop/services.md){ .exam-badge .exam-professional } [:material-star-circle: AIP](../courses/aip/services.md){ .exam-badge .exam-professional } [:material-target: SCS](../courses/scs/services.md){ .exam-badge .exam-specialty }

組織が承認した構成をカタログにし、利用者がセルフサービスで作成できるようにするサービスです。

| 要素 | 内容 |
| --- | --- |
| 製品 | CloudFormation や Terraform で定義した構成 |
| ポートフォリオ | 製品の集まり。IAM のユーザーやグループにアクセス権を与える |
| 制約 | 製品の使い方を制限するルール |
| プロビジョニング済み製品 | 利用者が作成した実体 |

| 制約 | 内容 | 例 |
| --- | --- | --- |
| 起動 | 作成時に Service Catalog が引き受ける IAM ロール | 利用者に EC2 権限を与えずに作らせる |
| テンプレート | 指定できるパラメータの値を制限 | `InstanceType` を `t3.small` のみに |
| 通知 | スタックのイベントを SNS に送る | 作成を担当者に通知 |
| タグ更新 | 作成後のタグ変更を許可するか | 変更を禁止する |
| スタックセット | 複数のアカウントとリージョンへの展開 | 3 リージョンに同じ構成を作る |

**起動制約が最重要です。** 製品とポートフォリオの組み合わせごとに設定します。ないと、利用者自身の権限で作成することになり、CloudFormation や対象サービスの権限が必要です。

テンプレート制約と TagOption は、Terraform の製品には使えません。

共有は、アカウント間または Organizations で行えます。参照の共有なら元の更新が反映されます。コピーを配布するなら、CloudFormation で展開します。

## AWS Resource Access Manager {#ram}

[:material-sprout: CLF](../courses/clf/services.md){ .exam-badge .exam-foundational } [:material-certificate: SAA](../courses/saa/services.md){ .exam-badge .exam-associate } [:material-certificate: SOA](../courses/soa/services.md){ .exam-badge .exam-associate } [:material-star-circle: SAP](../courses/sap/services.md){ .exam-badge .exam-professional } [:material-star-circle: DOP](../courses/dop/services.md){ .exam-badge .exam-professional } [:material-target: ANS](../courses/ans/services.md){ .exam-badge .exam-specialty } [:material-target: SCS](../courses/scs/services.md){ .exam-badge .exam-specialty }

リソースをコピーせず、他のアカウントと共有するサービスです。追加料金はかかりません。

| 共有できる例 | 用途 |
| --- | --- |
| VPC サブネット | 複数のアカウントが 1 つの VPC を使う |
| Transit Gateway | 組織のネットワークのハブを共有 |
| Route 53 Resolver ルール | オンプレミスの名前解決を共有 |
| プレフィックスリスト、IPAM プール | IP の管理 |
| License Manager の設定 | ライセンス設定の共有 |
| Capacity Reservation、Dedicated Host | 確保した容量の共有 |

共有先の指定と動作です。

| 共有先 | 招待 | 条件 |
| --- | --- | --- |
| 組織、OU、組織内のアカウント | 不要（組織の共有を有効にしている場合） | 管理アカウントで `enable-sharing-with-aws-organization` を実行 |
| 組織外のアカウント | 必要 | 対象のリソースタイプのみ |

組織の共有が無効なままだと、招待が必要になったり、OU を指定できなかったりします。

既定では、組織を離れたアカウントは共有へのアクセスを失います。

### VPC サブネットの共有 {#ram-vpc-sharing}

オーナーのアカウントが VPC を管理し、参加者のアカウントがそのサブネットにリソースを作ります。

- オーナーと参加者のアカウントは Organizations の管理下にある必要がある。
- オーナーは、サブネット、ルートテーブルなどの VPC のリソースを管理する。
- 参加者は、自分が作ったリソースを管理し、そのリソースの費用を負担する。
- VPC を減らせるので、ネットワークの構成が簡単になる。

VPC ピアリングや Transit Gateway との使い分けは [ネットワーク接続](network-connectivity.md) を参照してください。

## AWS License Manager {#license-manager}

[:material-sprout: CLF](../courses/clf/services.md){ .exam-badge .exam-foundational } [:material-certificate: SAA](../courses/saa/services.md){ .exam-badge .exam-associate } [:material-star-circle: DOP](../courses/dop/services.md){ .exam-badge .exam-professional }

Microsoft、SAP、Oracle、IBM などのソフトウェアライセンスを、アカウントやリージョンをまたいで管理するサービスです。

- vCPU、物理コア、ソケット、マシン数で数えるライセンスを追跡できる。
- ルールで上限を決め、ハードリミットでは超過する起動を止められ、ソフトリミットでは通知する。
- BYOL の管理に使い、監査での超過リスクを減らせる。
- Marketplace の権利の配布や、ISV によるライセンスの配布（マネージドエンタイトルメント）にも使える。
- RAM でライセンス設定を共有できる。

「BYOL のライセンス超過を起動時に防ぎたい」なら License Manager です。

## Resource Groups とタグ付け {#resource-groups}

AWS Resource Groups は、複数のリソースをまとめて扱うためのサービスです。

| グループの種類 | メンバーの決まり方 |
| --- | --- |
| タグベース | リソースタイプとタグのクエリ |
| CloudFormation スタックベース | スタックに含まれるリソース |

Systems Manager などで、グループ単位の操作に使います。

### タグ戦略 {#tagging-strategy}

Tag Editor を使うと、複数のリソースをリージョンをまたいで検索し、まとめてタグを付けられます。

タグのキーと値は大文字小文字を区別します。`aws:` はプレフィックスとして予約されています。

| 目的 | タグの例 |
| --- | --- |
| 費用の配賦 | `CostCenter=1234` |
| 環境 | `Environment=Production` |
| 所有者 | `Owner=platform-team` |
| 自動化 | `Backup=daily` |
| アクセス制御 | `Project=alpha`（ABAC） |

統制の組み合わせは次のとおりです。

| 目的 | 手段 |
| --- | --- |
| 表記の統一 | タグポリシー |
| 作成時の強制 | SCP の `aws:RequestTag`、IaC の必須タグキー |
| 事後の検出 | Config の `required-tags` |
| 費用への反映 | [コスト配分タグ](cost-management.md#cost-allocation-tags)の有効化 |

## AWS Proton の状況 {#proton}

[:material-certificate: SAA](../courses/saa/services.md){ .exam-badge .exam-associate } [:material-star-circle: DOP](../courses/dop/services.md){ .exam-badge .exam-professional }

**AWS Proton は、公式の告知では 2026 年 10 月 7 日でサポート終了です。** この日以降はコンソールとリソースにアクセスできません。デプロイ済みのインフラはそのまま残ります。

DOP-C02 と SAA-C03 の対象サービス一覧には名前が残っていますが、新しい設計の選択肢にはなりません。

公式の移行先の案には、CloudFormation Git Sync、Harmonix on AWS などがあります。

## IAM Identity Center への案内 {#identity-center}

複数のアカウントに、社員が 1 か所からサインインする仕組みです。Control Tower は既定でこのディレクトリを作成します。

概要は [IAM](iam.md#identity-center)、詳細は [ID とディレクトリ](identity-directory.md) を参照してください。

## マルチアカウントのパターン {#multi-account-patterns}

アカウントを分けると、影響範囲、権限、費用、クォータを分離できます。公式の推奨の OU は次のとおりです。

| OU | 用途 |
| --- | --- |
| Security | ログ保管、セキュリティツール |
| Infrastructure | ネットワークなどの共有基盤 |
| Workloads | アプリの本番、開発 |
| Sandbox | 個人の実験 |
| Policy Staging | 新しいポリシーの検証 |
| Suspended | 停止したアカウントの隔離 |
| Exceptions | 標準から外れるワークロード |
| Transitional | 移行中のアカウント |
| Deployments | デプロイ用のパイプライン |

| やりたいこと | パターン |
| --- | --- |
| 全アカウントのログを改ざんから守る | ログ保管アカウントへ集約し、SCP で変更を拒否 |
| セキュリティ担当の集中管理 | 監査アカウントを各サービスの委任管理者に |
| ネットワークの集中管理 | ネットワークアカウントから RAM で共有 |
| アカウントの大量発行 | Control Tower の Account Factory |
| 他アカウントへの作業 | 手元のアカウントから IAM ロールを引き受ける |
| 外部からのデータアクセスの遮断 | SCP と RCP でデータ境界を作る |
| 新しいポリシーの安全な適用 | Policy Staging OU で試してから広げる |

## 選び方の比較 {#choosing}

| 迷うもの | 使い分け |
| --- | --- |
| Organizations / Control Tower | 組織の仕組み自体は Organizations、構築と統制の自動化まで欲しいなら Control Tower |
| SCP / IAM ポリシー | 組織として上限を決めるなら SCP、権限を与えるなら IAM ポリシー |
| SCP / RCP | 自社の主体の制限なら SCP、外部からのリソースアクセスの制限なら RCP |
| Config / CloudTrail | 設定の状態なら Config、API の呼び出し履歴なら CloudTrail |
| Config ルール / SCP | 発見して修復なら Config、操作を止めるなら SCP |
| 適合パック / アグリゲーター | 展開なら適合パック、集約して閲覧ならアグリゲーター |
| Service Catalog / CloudFormation | 利用者に承認済みの構成を提供するなら Service Catalog、構成の定義自体は CloudFormation |
| Service Catalog / Marketplace | 自社の承認済みの構成なら Service Catalog、サードパーティ製品の購入なら Marketplace |
| RAM / IAM クロスアカウントロール | リソース自体を他アカウントで使わせるなら RAM、他アカウントで操作させるならロール |
| タグポリシー / Config の `required-tags` | 値の表記の統一ならタグポリシー、タグのないリソースの検出なら Config |

## 既定値と上限のまとめ {#numbers}

| 項目 | 値 |
| --- | --- |
| 組織のアカウント数の既定クォータ | 10（引き上げ可） |
| ルートの数 | 1 |
| OU の数 | 2,000 |
| OU のネスト | 5 階層 |
| 同時に作成できるメンバーアカウント | 5 |
| 作成したアカウントを組織から外せるまでの期間 | 4 日 |
| 対象 1 つに付けられる SCP | 10 |
| SCP の最大サイズ | 10,240 文字 |
| 対象 1 つに付けられる RCP | 5（`RCPFullAWSAccess` を含む） |
| RCP の最大サイズ | 5,120 文字 |
| ルール数（リージョン、アカウントごと） | 1,000 |
| 適合パック | アカウントあたり 50、1 パック 130 ルール |
| アグリゲーター | 50 個、1 つあたり 10,000 アカウント |
| Config の保持期間 | 30 日から 2,557 日、既定は 7 年 |
| 自動修復の試行回数 | 既定 5、1 から 25 |

## 試験のポイント {#exam-points}

| こう問われたら | 答え |
| --- | --- |
| 複数アカウントの請求をまとめて割引を共有したい | Organizations の一括請求 |
| 特定リージョンの利用を全アカウントで禁止したい | SCP |
| SCP を付けたのにまだ管理アカウントで操作できる | SCP は管理アカウントに効かない |
| SCP で権限を与えられるか | 与えられない。上限を決めるだけ |
| 外部からの S3 アクセスを組織全体で防ぎたい | RCP の `aws:PrincipalOrgID` |
| ベストプラクティスのマルチアカウント環境をすぐ作りたい | Control Tower |
| Control Tower の予防的コントロールの実体 | SCP と RCP |
| Control Tower の検出的コントロールの実体 | Config ルール |
| アカウントの発行を標準化したい | Account Factory |
| 公開バケットを検出して自動で直したい | Config ルールと SSM Automation の自動修復 |
| 全アカウントの準拠状況を 1 か所で見たい | Config アグリゲーター |
| ルールと修復をまとめて組織に展開したい | 適合パック |
| 過去のある時点の設定を確認したい | Config |
| 誰がセキュリティグループを変更したか | CloudTrail |
| 利用者に強い権限を渡さず承認済みの構成を作らせたい | Service Catalog の起動制約 |
| サブネットを他アカウントと共有したい | RAM |
| Transit Gateway を複数アカウントで使いたい | RAM |
| ライセンスの超過を防ぎたい | License Manager |
| タグの表記を組織で統一したい | タグポリシー |
| タグなしリソースを作らせたくない | SCP の `aws:RequestTag` |
| Proton を提案してよいか | 2026 年 10 月にサポート終了なので提案しない |

## 関連ページ {#related}

- [クラウドの基礎](cloud-foundations.md)
- [コスト管理](cost-management.md)
- [IAM](iam.md)
- [ID とディレクトリ](identity-directory.md)
- [オブザーバビリティ](observability.md)
- [運用](operations.md)
- [ネットワーク接続](network-connectivity.md)
- [脅威検出](threat-detection.md)

## 参考 {#references}

- [Service control policies (SCPs)](https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_policies_scps.html)
- [SCP evaluation](https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_policies_scps_evaluation.html)
- [Resource control policies (RCPs)](https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_policies_rcps.html)
- [Managing organization policies](https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_policies.html)
- [Quotas and service limits for AWS Organizations](https://docs.aws.amazon.com/organizations/latest/userguide/orgs_reference_limits.html)
- [Enforcing tag policies](https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_policies_tag-policies-enforcement.html)
- [Delegated administrator for AWS Organizations](https://docs.aws.amazon.com/organizations/latest/userguide/orgs_delegate_policies.html)
- [What Is AWS Control Tower?](https://docs.aws.amazon.com/controltower/latest/userguide/what-is-control-tower.html)
- [How controls work](https://docs.aws.amazon.com/controltower/latest/userguide/how-controls-work.html)
- [Limitations and quotas in AWS Control Tower](https://docs.aws.amazon.com/controltower/latest/userguide/limits.html)
- [Components of an AWS Config rule](https://docs.aws.amazon.com/config/latest/developerguide/evaluate-config_components.html)
- [Remediating Noncompliant Resources](https://docs.aws.amazon.com/config/latest/developerguide/remediation.html)
- [RemediationConfiguration](https://docs.aws.amazon.com/config/latest/APIReference/API_RemediationConfiguration.html)
- [Multi-Account Multi-Region Data Aggregation](https://docs.aws.amazon.com/config/latest/developerguide/aggregate-data.html)
- [Conformance Packs](https://docs.aws.amazon.com/config/latest/developerguide/conformance-packs.html)
- [Service Limits for AWS Config](https://docs.aws.amazon.com/config/latest/developerguide/configlimits.html)
- [AWS Config pricing](https://aws.amazon.com/config/pricing/)
- [Using AWS Service Catalog Constraints](https://docs.aws.amazon.com/servicecatalog/latest/adminguide/constraints.html)
- [What is AWS Resource Access Manager?](https://docs.aws.amazon.com/ram/latest/userguide/what-is.html)
- [Shareable AWS resources](https://docs.aws.amazon.com/ram/latest/userguide/shareable.html)
- [Share your VPC subnets](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-sharing.html)
- [What is AWS License Manager?](https://docs.aws.amazon.com/license-manager/latest/userguide/license-manager.html)
- [What are resource groups?](https://docs.aws.amazon.com/ARG/latest/userguide/resource-groups.html)
- [Best Practices for Tagging AWS Resources](https://docs.aws.amazon.com/whitepapers/latest/tagging-best-practices/tagging-best-practices.html)
- [AWS Proton Service Deprecation and Migration Guide](https://docs.aws.amazon.com/proton/latest/userguide/proton-end-of-support.html)
- [Recommended OUs and accounts](https://docs.aws.amazon.com/whitepapers/latest/organizing-your-aws-environment/recommended-ous-and-accounts.html)

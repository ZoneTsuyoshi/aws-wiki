# 分野3: IaC

CloudFormation と SAM のテンプレートの読み書き、SAM と CDK によるテスト、変更の確認とロールバックが問われます。IaC を中心に扱うのはこの分野です。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [3.1.1](../../domain3.md#skill-3-1-1) | プロジェクト構成と依存関係 |
| [3.2.1](../../domain3.md#skill-3-2-1) | SAM、CDK、CloudFormation でのテストと検証 |
| [3.2.3](../../domain3.md#skill-3-2-3) | テストイベントの作成 |
| [3.2.4](../../domain3.md#skill-3-2-4) | 同じテンプレートによる環境の分離 |
| [3.3.3](../../domain3.md#skill-3-3-3) | CloudFormation、SAM のテンプレート |
| [3.3.6](../../domain3.md#skill-3-3-6) | `DeploymentPreference` によるカナリア |
| [3.3.7](../../domain3.md#skill-3-3-7) | スタックのロールバック |

## 学習の順番 {#study-order}

1. [どれを使うか](../../../../services/iac.md#choosing): CloudFormation、SAM、CDK の関係を押さえます。
2. [セクション](../../../../services/iac.md#template-sections)と[組み込み関数](../../../../services/iac.md#intrinsic-functions): テンプレートを読めるようにします。
3. [SAM のテンプレート](../../../../services/iac.md#sam-template)と[SAM CLI](../../../../services/iac.md#sam-cli): `Transform` とコマンドの使い分けを覚えます。
4. [プロジェクト構成](../../../../services/iac.md#project-structure)と[別のステージへのデプロイ](../../../../services/iac.md#deploy-stages): `samconfig.toml` で環境を分ける方法を確認します。
5. [テストイベント](../../../../services/iac.md#test-events)、[単体テスト](../../../../services/iac.md#unit-tests)、[結合テスト](../../../../services/iac.md#integration-tests)、[イベント駆動アプリのテスト](../../../../services/iac.md#event-driven-tests): テストの種類ごとの方法を比べます。
6. [CDK のテスト](../../../../services/iac.md#cdk-testing)と[検証方法のまとめ](../../../../services/iac.md#validate-iac): ツールごとの検証手段を整理します。
7. [既存テンプレートの更新](../../../../services/iac.md#update-templates)と[変更セット](../../../../services/iac.md#change-sets): 置き換えが起きる条件と確認方法を理解します。
8. [DeploymentPreference](../../../../services/iac.md#deployment-preference)、[ロールバックの既定動作](../../../../services/iac.md#stack-rollback)、[ロールバックトリガー](../../../../services/iac.md#rollback-triggers): 段階的な配布と戻し方を覚えます。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| 必須のセクション | `Resources` のみ | 他は任意 |
| テンプレートの大きさ | 本文 51,200 バイト、S3 経由 1 MB | 超えるなら S3 に置く |
| ロールバックトリガー | 最大 5 個、監視は 0〜180 分（既定 0） | 完了後も見張るなら監視時間を設定する |
| SAM の `Type` | `Canary10Percent5Minutes`（10、15、30 分）、`Linear10PercentEvery1Minute`（2、3、10 分）、`AllAtOnce` | CodeDeploy の設定名と対応する |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 本番の更新前に、置き換えられるリソースを確認 | 変更セットを作り、`describe-change-set` の `Replacement` を見る |
| 同じ SAM アプリを staging と prod へ | `samconfig.toml` に環境ごとの設定を書き、`sam deploy --config-env staging` |
| S3 や SQS のイベントの形でテスト | `sam local generate-event` で作り、`sam local invoke -e` で実行 |
| デプロイ済みの関数をテスト | `sam remote invoke` |
| 自動テストからローカルの関数を呼ぶ | `sam local start-lambda` |
| CDK の生成結果をデプロイせずに検証 | `aws_cdk.assertions` の `Template` と `has_resource_properties` |
| テンプレートの構文と記述を確認 | `sam validate --lint`、`aws cloudformation validate-template`、cfn-lint |
| Lambda をカナリアで配布し、異常なら戻す | `AutoPublishAlias` と `DeploymentPreference`（`Type`、`Alarms`、`Hooks`） |
| スタックの更新後 10 分はアラームで戻す | `--rollback-configuration` の `RollbackTriggers` と `MonitoringTimeInMinutes=10` |
| `UPDATE_ROLLBACK_FAILED` から回復 | 原因を直して `continue-update-rollback`。直せなければ `--resources-to-skip` |

## 引っかかりやすい点 {#traps}

- **`ROLLBACK_COMPLETE` で更新できない**: 初回作成の失敗です。スタックを削除して作り直します。
- **`InsufficientCapabilities`**: `RoleName` を指定したロールには `CAPABILITY_NAMED_IAM` が必要です。`CAPABILITY_IAM` では足りません。
- **更新で意図せず作り直される**: 論理 ID を変えると、削除と新規作成として扱われます。固定の名前を付けていると、置き換えのときに名前が衝突して失敗します。
- **置き換えで元のリソースが消える**: `DeletionPolicy` は置き換えでは効きません。残すには `UpdateReplacePolicy` を使います。
- **本番で `sam sync` を使う**: CloudFormation を迂回する更新があるので開発環境向けです。本番は `sam deploy` か CI/CD を使います。
- **アラームのデータがなくて戻らない**: `INSUFFICIENT_DATA` では戻しません。欠落データを `breaching` として扱うアラームにします。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [iac 問1](../../exercises/iac.md#q1) | 3.3.3 | 手作業の変更でスタックのリソースがテンプレートとずれていないか確認しました。あるリソースの Stac… |
| [iac 問2](../../exercises/iac.md#q2) | 3.3.3 | Stage が prod のときに、InstanceType が大きいサイズであることをリソース作成… |
| [iac 問4](../../exercises/iac.md#q4) | 3.3.7 | 本番のスタック更新の後 10 分間、5XX のアラームを監視し、発火したらスタック全体を戻したいと考… |
| [iac 問6](../../exercises/iac.md#q6) | 3.3.3 | DynamoDB テーブルのプロパティの変更で置き換えが起きても、古いテーブルを残したいと考えていま… |
| [iac 問7](../../exercises/iac.md#q7) | 3.3.3 | EC2 で動くアプリの起動が終わるまで、スタックの作成を完了させたくありません。インスタンスは起動に… |
| [iac 問8](../../exercises/iac.md#q8) | 3.3.3 | 本番スタックの更新の前に変更セットを確認すると、RDS インスタンスの Replacement が … |
| [iac 問9](../../exercises/iac.md#q9) | 3.3.3 | cfn-init が AWS::CloudFormation::Init の config を処理す… |
| [iac 問11](../../exercises/iac.md#q11) | 3.3.3 | スタックポリシーで OrdersTable の置き換えを拒否しています。今回だけ、承認を得た上で置き… |
| [iac 問13](../../exercises/iac.md#q13) | 3.3.3 | VPC のスタックが出力をエクスポートし、チームごとの複数のスタックが参照しています。ライフサイクル… |
| [iac 問15](../../exercises/iac.md#q15) | 3.3.3 | SAM の Globals に Timeout: 10 と Environment.Variable… |
| [iac 問17](../../exercises/iac.md#q17) | 3.3.7 | SAM で Lambda の新しい版へトラフィックを段階的に移し、エラーの増加で戻したいと考えていま… |
| [iac 問19](../../exercises/iac.md#q19) | 3.3.3 | CDK で次の要件があります。VPC の参照結果をチームで同じにし、別の AWS リージョンへ初めて… |
| [iac 問21](../../exercises/iac.md#q21) | 3.2.1 | CDK のスタックで、SQS キューの可視性タイムアウトが 360 秒であることをテストします。デプ… |
| [iac 問22](../../exercises/iac.md#q22) | 3.2.1 | CI で SAM テンプレートを検査しています。aws cloudformation validat… |
| [iac 問23](../../exercises/iac.md#q23) | 3.2.3 | S3 の ObjectCreated で動く関数をローカルで試します。S3 のイベントの JSON … |

<!-- questions:end -->

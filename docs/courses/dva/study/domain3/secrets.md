# 分野3: Secrets Manager、Parameter Store、AppConfig

分野3では、コードを変えずに環境ごとの設定を切り替える方法と、AppConfig の段階配布が問われます。暗号化、ローテーション、権限は[分野2のシークレット管理](../domain2/secrets.md) で扱います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [3.1.4](../../domain3.md#skill-3-1-4) | 環境ごとのアプリケーション設定 |

## 学習の順番 {#study-order}

1. [3 つのサービスの比較](../../../../services/secrets.md#comparison): どの値をどこに置くかの判断を押さえます。
2. [環境ごとの設定](../../../../services/secrets.md#environment-config): 手段ごとに向いている値を比べます。
3. [Parameter Store の階層](../../../../services/secrets.md#parameter-hierarchy): パスで環境を分ける方法を確認します。
4. [AppConfig](../../../../services/secrets.md#appconfig)、[設定プロファイル](../../../../services/secrets.md#config-profiles)、[機能フラグ](../../../../services/secrets.md#feature-flags): 用語と、デプロイと公開を分ける考え方を理解します。
5. [バリデーター](../../../../services/secrets.md#validators)と[デプロイ戦略](../../../../services/secrets.md#deployment-strategies): 配布前の検証と事前定義の戦略を覚えます。
6. [ロールバック](../../../../services/secrets.md#appconfig-rollback)と[アラームとロールバック](../../../../services/secrets.md#alarm-rollback): 自動で戻す条件を確認します。
7. [設定の取得](../../../../services/secrets.md#appconfig-retrieval)、[取得とポーリング](../../../../services/secrets.md#polling-settings)、[AppConfig Agent](../../../../services/secrets.md#appconfig-agent-settings): API の使い方と Agent の利点を押さえます。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| `AppConfig.Linear20PercentEvery6Minutes` | 6 分ごとに 20%、計 30 分、ベイク 30 分 | AWS 推奨 |
| `AppConfig.Canary10Percent20Minutes` | 成長率 10% で指数的に 20 分、ベイク 10 分 | AWS 推奨 |
| `AppConfig.AllAtOnce` | 即時、ベイク 10 分 | 急ぐとき |
| `AppConfig.Linear50PercentEvery30Seconds` | 30 秒ごとに 50%、1 分、ベイク 1 分 | テスト、デモ |
| バリデーター | プロファイルあたり 2 つ | JSON Schema、Lambda |
| AppConfig のトークン | 1 回限り、最大 24 時間 | 次回は `NextPollConfigurationToken` |
| AppConfig Agent | ポート 2772、ポーリング既定 45 秒 | Secrets Manager の Lambda 拡張は 2773 |
| パラメータの階層 | 15 | `/prod/orders/db/host` のように分ける |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 再デプロイせずに機能を段階的に公開 | AppConfig の機能フラグと段階的なデプロイ戦略 |
| 不正な設定を配布前に止める | バリデーター。フリーフォームなら JSON Schema、独自ロジックなら Lambda |
| 配布でエラーが増えたら自動で戻す | 環境の `Monitors` に `AlarmArn` と `AlarmRoleArn`。ロールに `cloudwatch:DescribeAlarms` |
| 完了後に前のバージョンへ戻す | `StopDeployment` の `AllowRevert` |
| 同じコードで環境ごとの値を読む | Parameter Store の `/prod/orders/` などを `GetParametersByPath` で取得。IAM もパスで絞る |
| 環境ごとの資格情報 | Secrets Manager に `prod/db` のように置き、環境変数には名前だけを渡す |
| ステージごとに統合先を変える | [API Gateway のステージ変数](../../../../services/api-gateway.md#stage-variables) |
| デプロイのときに環境名を渡す | SAM や CloudFormation のパラメータ。`!Sub "/${Stage}/orders/"` で参照先を組み立てる |
| Lambda から AppConfig を読む | AppConfig Agent の Lambda 拡張で `localhost:2772` から取得 |
| AppConfig Agent のコールドスタートを短くする | `AWS_APPCONFIG_EXTENSION_PREFETCH_LIST` |

## 引っかかりやすい点 {#traps}

- **2 回目の呼び出しで設定が空になる**: 空の応答は変更なしの意味です。前回の値を保持します。
- **`BadRequestException`**: トークンの期限切れです。毎回 `NextPollConfigurationToken` を使います。
- **API の呼び出しが増える**: `StartConfigurationSession` をループの中で呼んでいます。クライアントごとに 1 回だけ呼びます。
- **アラームが出たのに戻らない**: アラームのアクションが無効だと戻りません。`FinalBakeTimeInMinutes` が 0 なら、完了後のアラームでも戻りません。
- **同じ環境へ続けてデプロイできない**: 1 つの環境には一度に 1 つの設定だけです。別の環境には同時にデプロイできます。
- **ステージ変数や Lambda 環境変数に秘密情報を置く**: ステージ変数は機密データ向けではなく、Lambda 環境変数の平文も関数を閲覧できる人に見えます。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [secrets 問9](../../exercises/secrets.md#q9) | 3.1.4 | 既定のパラメータティアに Intelligent-Tiering を設定しました。次のうち、Adva… |
| [secrets 問10](../../exercises/secrets.md#q10) | 3.1.4 | 90 日後に削除される API トークンを Parameter Store に置き、削除の 15 日… |
| [secrets 問11](../../exercises/secrets.md#q11) | 3.1.4 | コードで get_parameters_by_path(Path="/prod/orders") を… |
| [secrets 問12](../../exercises/secrets.md#q12) | 3.1.4 | パラメータにはすでに 100 バージョンがあり、最古のバージョンにラベル prod が付いています。… |
| [secrets 問13](../../exercises/secrets.md#q13) | 3.1.4 | 100 個の Lambda が起動時に同時に GetParameter を呼ぶと、Throttlin… |
| [secrets 問14](../../exercises/secrets.md#q14) | 3.1.4 | AppConfig で LINEAR、GrowthFactor=25、DeploymentDurat… |
| [secrets 問15](../../exercises/secrets.md#q15) | 3.1.4 | 自前のコードで GetLatestConfiguration をポーリングすると、2 回目から設定が… |

<!-- questions:end -->

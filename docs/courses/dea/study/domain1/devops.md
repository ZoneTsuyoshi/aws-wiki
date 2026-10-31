# 分野1: IaC、CI/CD と開発の実践

言語の選択、ソフトウェアの実践、IaC と SAM と CI/CD の使い分けを問います。言語固有の構文は範囲外です。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [1.4.3](../../domain1.md#skill-1-4-3) | データエンジニアリングの言語とフレームワーク |
| [1.4.4](../../domain1.md#skill-1-4-4) | ソフトウェアエンジニアリングのベストプラクティス |
| [1.4.5](../../domain1.md#skill-1-4-5) | IaC によるソリューションのデプロイ |
| [1.4.6](../../domain1.md#skill-1-4-6) | AWS SAM によるサーバーレスパイプラインのデプロイ |
| [1.4.8](../../domain1.md#skill-1-4-8) | IaC による繰り返しのデプロイ（CloudFormation と CDK） |
| [1.4.9](../../domain1.md#skill-1-4-9) | データパイプラインの CI/CD |

## 学習の順番 {#study-order}

1. [CloudFormation テンプレート](../../../../services/iac.md#cloudformation-template): Glue のジョブの定義を確認します。
2. [パラメータ](../../../../services/iac.md#parameters): 環境ごとの差の扱いを覚えます。
3. [SAM](../../../../services/iac.md#sam): リソースの種類と CLI を確認します。
4. [DeletionPolicy](../../../../services/iac.md#deletion-policy): データを残す設定を確認します。
5. [変更セット](../../../../services/iac.md#change-sets): ドリフト検出と区別します。
6. [サービスの役割](../../../../services/cicd.md#overview): 3 つのサービスの違いを押さえます。

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 環境ごとにバケット名だけ違う | 1 つのテンプレートとパラメータ |
| スタックを消してもバケットを残す | `DeletionPolicy: Retain` |
| 更新の影響を事前に見る | 変更セット |
| 手作業の変更を見つける | ドリフト検出 |
| テストとパッケージ | CodeBuild と `buildspec.yml` |
| 本番の前の確認 | CodePipeline の手動承認 |

## 引っかかりやすい点 {#traps}

- `cdk bootstrap` は最初の準備に必要です。
- コンストラクトは CDK の単位で、CloudFormation の再利用はネストされたスタックです。
- ログに機密情報を書きません。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [devops 問1](../../exercises/devops.md#q1) | 1.4.3 | 使う言語とフレームワークの組み合わせとして適切なものはどれですか。 |
| [devops 問2](../../exercises/devops.md#q2) | 1.4.3 | 次の作業に適した言語はどれですか。「EMR のノードの起動時に OS のパッケージを入れ、CLI で… |
| [devops 問3](../../exercises/devops.md#q3) | 1.4.3 | Spark を使う場面として最も適切なものはどれですか。 |
| [devops 問4](../../exercises/devops.md#q4) | 1.4.4 | PySpark の変換のコードを本番前に確かめます。費用を抑えて素早く失敗を見つけるテストの組み合わ… |
| [devops 問5](../../exercises/devops.md#q5) | 1.4.4 | パイプラインのログの実践として正しいものはどれですか。（2つ選択） |
| [devops 問6](../../exercises/devops.md#q6) | 1.4.4 | ETL のスクリプトと DAG、SQL を管理します。正しい実践はどれですか。 |
| [devops 問7](../../exercises/devops.md#q7) | 1.4.5 | 開発と本番に同じ Glue のジョブ、クローラー、IAM ロールを作ります。バケット名だけが異なりま… |
| [devops 問8](../../exercises/devops.md#q8) | 1.4.5 | CloudFormation で AWS::Glue::Job を定義します。ETL のスクリプトは… |
| [devops 問9](../../exercises/devops.md#q9) | 1.4.5 | データ基盤の構築で、手作業ではなく IaC を選ぶ理由として最も適切なものはどれですか。 |
| [devops 問10](../../exercises/devops.md#q10) | 1.4.6 | Lambda、Step Functions、DynamoDB のパイプラインを短い定義でデプロイしま… |
| [devops 問11](../../exercises/devops.md#q11) | 1.4.6 | SAM のアプリケーションをパッケージにしてデプロイする CLI の手順はどれですか。 |
| [devops 問12](../../exercises/devops.md#q12) | 1.4.6 | デプロイの前に、SAM の関数を手元でサンプルのイベントで動かします。どのコマンドですか。 |
| [devops 問13](../../exercises/devops.md#q13) | 1.4.8 | データレイクのバケットをスタックで作りました。スタックを消してもバケットを残します。どの設定ですか。 |
| [devops 問14](../../exercises/devops.md#q14) | 1.4.8 | 本番のスタックの更新で、Redshift のクラスターが置き換わらないか事前に確認します。また手作業… |
| [devops 問15](../../exercises/devops.md#q15) | 1.4.8 | CDK と CloudFormation の説明として正しいものはどれですか。（2つ選択） |
| [devops 問16](../../exercises/devops.md#q16) | 1.4.9 | データパイプラインの CI で、PySpark の単体テストを実行し、スクリプトをパッケージにします… |
| [devops 問17](../../exercises/devops.md#q17) | 1.4.9 | ETL の変更を開発へ自動で出し、結合テストの後に、担当者の確認を経て本番へ出します。どの構成ですか… |
| [devops 問18](../../exercises/devops.md#q18) | 1.4.9 | CI/CD のサービスの役割の説明として正しいものはどれですか。 |

<!-- questions:end -->

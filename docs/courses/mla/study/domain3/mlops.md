# 分野3: MLOps

本番への段階的なデプロイと自動のロールバック、パイプラインの中のテスト、再学習のきっかけ、モデルのバージョン管理を問います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [3.3.1](../../domain3.md#skill-3-3-1) | 自動デプロイとロールバック |
| [3.3.4](../../domain3.md#skill-3-3-4) | CI/CD の自動テスト |
| [3.3.5](../../domain3.md#skill-3-3-5) | 再学習の仕組み |
| [3.3.6](../../domain3.md#skill-3-3-6) | モデルのバージョン管理 |

## 学習の順番 {#study-order}

1. [デプロイとテストの戦略](../../../../services/sagemaker.md#deployment-strategies): 4 つの方式の制約を覚えます。
2. [SageMaker Pipelines](../../../../services/sagemaker.md#pipelines): Condition ステップとキャッシュを確認します。
3. [CI/CD と再学習](../../../../services/sagemaker.md#cicd-retraining): 段階ごとのテストときっかけを押さえます。
4. [Model Registry](../../../../services/sagemaker.md#model-registry): 状態の値と自動化をつなげます。
5. [MLflow](../../../../services/sagemaker.md#mlflow)と [Model Cards](../../../../services/sagemaker.md#model-cards): 記録の手段を確認します。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| Canary | グリーンの 50% 以下 | ベイク期間に監視する |
| Linear の各段階 | グリーンの 10〜50% | |
| `ModelApprovalStatus` | `PendingManualApproval`、`Approved`、`Rejected` | |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 指標が悪化したら自動で戻す | ガードレールと CloudWatch アラーム |
| AUC が基準以上のときだけ登録する | Condition ステップと Fail ステップ |
| ドリフトで再学習する | CloudWatch アラーム、EventBridge、Pipelines |
| 定期の再学習 | EventBridge のスケジュール |
| 承認でデプロイを開始する | EventBridge、CodePipeline |
| 誰がいつ承認したか | CloudTrail と `ApprovalDescription` |

## 引っかかりやすい点 {#traps}

- ステップキャッシュは、属性が同じステップの結果を再利用します。
- Model Registry で戻すときは、`Approved` を `Rejected` に変えて、最新の `Approved` を再デプロイします。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [mlops 問1](../../exercises/mlops.md#q1) | 3.3.1 | 本番のエンドポイントのモデルを更新します。まず一部のトラフィックだけ新しいモデルへ移し、問題がなけれ… |
| [mlops 問2](../../exercises/mlops.md#q2) | 3.3.1 | デプロイガードレールの設定の値として有効なものを選んでください。（2つ選択） |
| [mlops 問3](../../exercises/mlops.md#q3) | 3.3.1 | 本番のモデルに問題が見つかりました。Model Registry の状態を使って、1 つ前の承認済み… |
| [mlops 問4](../../exercises/mlops.md#q4) | 3.3.4 | Pipelines の中で、AUC が 0.85 以上のときだけモデルを登録し、下回れば止めます。ど… |
| [mlops 問5](../../exercises/mlops.md#q5) | 3.3.4 | ML の CI/CD にテストを組み込みます。段階とテストの組み合わせとして正しいものを選んでくださ… |
| [mlops 問6](../../exercises/mlops.md#q6) | 3.3.4 | 新しいモデルを本番に出す前に、本番のトラフィックのコピーで遅延と安定性を確かめる段階を CI/CD … |
| [mlops 問7](../../exercises/mlops.md#q7) | 3.3.5 | ドリフトのアラームを検知して再学習を始めます。適切な流れはどれですか。 |
| [mlops 問8](../../exercises/mlops.md#q8) | 3.3.5 | 新しいデータが S3 に届くたびに再学習します。変更のない前処理のステップは再実行したくありません。… |
| [mlops 問9](../../exercises/mlops.md#q9) | 3.3.5 | 毎週月曜の朝に再学習します。ドリフトの有無には関係なく定期で動かします。どの方法ですか。 |
| [mlops 問10](../../exercises/mlops.md#q10) | 3.3.6 | Model Registry の状態の値として正しい組み合わせはどれですか。 |
| [mlops 問11](../../exercises/mlops.md#q11) | 3.3.6 | モデルの承認で本番へのデプロイを自動で開始し、承認の履歴を監査します。適切な組み合わせを選んでくださ… |
| [mlops 問12](../../exercises/mlops.md#q12) | 3.3.6 | 同じ解約予測のモデルの複数のバージョンをまとめて管理します。Model Registry の用語の組… |

<!-- questions:end -->

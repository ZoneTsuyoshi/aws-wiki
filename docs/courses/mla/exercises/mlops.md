# MLOps の問題集

対象の解説: [SageMaker Pipelines](../../../services/sagemaker.md#pipelines)、[Model Registry](../../../services/sagemaker.md#model-registry)、[CI/CD と再学習](../../../services/sagemaker.md#cicd-retraining)

### 問1 {#q1}

本番のエンドポイントのモデルを更新します。まず一部のトラフィックだけ新しいモデルへ移し、問題がなければ残りを移します。エラー率が上がったら自動で戻します。どの設定ですか。

- A. Canary とベイク期間、CloudWatch アラーム
- B. エンドポイントを削除して作り直す
- C. All at once のブルー/グリーンにアラームなしで更新する
- D. `UpdateEndpointWeightsAndCapacities` を手で実行する

??? success "答えと解説"
    **正解: A**

    デプロイガードレールの Canary では、ベイク期間に CloudWatch アラームが発報すると自動で元に戻ります。

    - A: 正しい。
    - B: 誤り。停止が発生し、段階的な移行でもありません。
    - C: 誤り。全トラフィックが一度に移り、自動で戻りません。
    - D: 誤り。配分の変更はできますが、自動のロールバックにはなりません。

    **スキル:** [3.3.1](../domain3.md#skill-3-3-1) / **参照:** [デプロイとテストの戦略](../../../services/sagemaker.md#deployment-strategies)

### 問2 {#q2}

デプロイガードレールの設定の値として有効なものを選んでください。（2つ選択）

- A. Canary のサイズをグリーンの 75% にする
- B. Linear の各段階をグリーンの 5% にする
- C. Linear の各段階をグリーンの 20% にする
- D. Linear の各段階をグリーンの 60% にする
- E. Canary のサイズをグリーンの 25% にする

??? success "答えと解説"
    **正解: C, E**

    カナリアは 50% 以下、リニアの各段階は 10〜50% です。

    - A: 誤り。50% を超えています。
    - B: 誤り。10% を下回っています。
    - C: 正しい。各段階はグリーンの 10〜50% です。
    - D: 誤り。50% を超えています。
    - E: 正しい。カナリアはグリーンの 50% 以下です。

    **スキル:** [3.3.1](../domain3.md#skill-3-3-1) / **参照:** [デプロイとテストの戦略](../../../services/sagemaker.md#deployment-strategies)

### 問3 {#q3}

本番のモデルに問題が見つかりました。Model Registry の状態を使って、1 つ前の承認済みのモデルに戻します。適切な方法はどれですか。

- A. モデルパッケージグループを削除して作り直す
- B. `Approved` を `Rejected` に変え、最新の `Approved` を再デプロイする
- C. 問題のモデルパッケージの S3 のファイルを手で上書きする
- D. 問題のバージョンの状態を `PendingManualApproval` に戻して放置する

??? success "答えと解説"
    **正解: B**

    Model Registry で `Approved` を `Rejected` に変え、最新の `Approved` を再デプロイします。

    - A: 誤り。履歴を失います。
    - B: 正しい。
    - C: 誤り。記録と実体がずれ、追跡もできません。
    - D: 誤り。本番のモデルは戻りません。

    **スキル:** [3.3.1](../domain3.md#skill-3-3-1) / **参照:** [Model Registry](../../../services/sagemaker.md#model-registry)

### 問4 {#q4}

Pipelines の中で、AUC が 0.85 以上のときだけモデルを登録し、下回れば止めます。どのステップの組み合わせですか。

- A. Transform ステップと Processing ステップ
- B. Training ステップだけ
- C. Condition ステップと Fail ステップ
- D. Lambda ステップと Tuning ステップ

??? success "答えと解説"
    **正解: C**

    Condition ステップで指標のしきい値を判定し、下回れば Fail ステップで止めます。

    - A: 誤り。条件の分岐と停止になりません。
    - B: 誤り。評価の条件を判定できません。
    - C: 正しい。
    - D: 誤り。条件の分岐と停止になりません。

    **スキル:** [3.3.4](../domain3.md#skill-3-3-4) / **参照:** [SageMaker Pipelines](../../../services/sagemaker.md#pipelines)

### 問5 {#q5}

ML の CI/CD にテストを組み込みます。段階とテストの組み合わせとして正しいものを選んでください。（2つ選択）

- A. 本番前の段階: Glue Data Quality で本番の応答の遅延を測る
- B. コードの段階: Macie でコードの単体テストを実行する
- C. データの段階: Glue Data Quality でスキーマと品質を検査する
- D. モデルの段階: CloudTrail で指標のしきい値を判定する
- E. コードの段階: CodeBuild で単体テストを実行する

??? success "答えと解説"
    **正解: C, E**

    コードは CodeBuild、データは Glue Data Quality や Processing、モデルは Condition ステップで検査します。

    - A: 誤り。データの品質の検査で、遅延は測れません。
    - B: 誤り。S3 の機密データの検出です。
    - C: 正しい。
    - D: 誤り。API の記録で、モデルの指標を判定しません。
    - E: 正しい。

    **スキル:** [3.3.4](../domain3.md#skill-3-3-4) / **参照:** [CI/CD と再学習](../../../services/sagemaker.md#cicd-retraining)

### 問6 {#q6}

新しいモデルを本番に出す前に、本番のトラフィックのコピーで遅延と安定性を確かめる段階を CI/CD に入れます。実装はどれですか。

- A. Model Cards の更新
- B. Glue Data Quality のルール
- C. 単体テストで本番のトラフィックを再現する
- D. シャドウテスト

??? success "答えと解説"
    **正解: D**

    本番前の段階はシャドウテストです。本番ではデプロイガードレールで段階的に出します。

    - A: 誤り。記録の機能で、テストになりません。
    - B: 誤り。データの検査です。
    - C: 誤り。単体テストはコードの段階の検査です。
    - D: 正しい。

    **スキル:** [3.3.4](../domain3.md#skill-3-3-4) / **参照:** [CI/CD と再学習](../../../services/sagemaker.md#cicd-retraining)、[デプロイとテストの戦略](../../../services/sagemaker.md#deployment-strategies)

### 問7 {#q7}

ドリフトのアラームを検知して再学習を始めます。適切な流れはどれですか。

- A. Model Monitor のスケジュール、CloudTrail、CodeDeploy
- B. CloudWatch アラーム、EventBridge、Pipelines
- C. CloudTrail のログ、Glue クローラー、S3 のライフサイクル
- D. SNS で担当者に通知するだけにする

??? success "答えと解説"
    **正解: B**

    ドリフトのきっかけは CloudWatch アラーム、EventBridge、Pipelines の順につなぎます。

    - A: 誤り。CloudTrail はアラームの受け取り口ではなく、CodeDeploy で再学習はできません。
    - B: 正しい。
    - C: 誤り。アラームから再学習を開始できません。
    - D: 誤り。仕組みとしての再学習になりません。

    **スキル:** [3.3.5](../domain3.md#skill-3-3-5) / **参照:** [CI/CD と再学習](../../../services/sagemaker.md#cicd-retraining)

### 問8 {#q8}

新しいデータが S3 に届くたびに再学習します。変更のない前処理のステップは再実行したくありません。実装の組み合わせを選んでください。（2つ選択）

- A. 毎回ステップを全部再実行する
- B. 再学習を CloudFormation のスタックの作成で行う
- C. S3 のイベントで Pipelines を開始する
- D. ステップキャッシュを有効にする
- E. 前処理をスキップするため、学習データを空にする

??? success "答えと解説"
    **正解: C, D**

    新しいデータのきっかけは S3 のイベントです。ステップキャッシュで同じ処理を再利用します。

    - A: 誤り。時間とコストが無駄になります。
    - B: 誤り。インフラの定義で、学習の実行の手段ではありません。
    - C: 正しい。
    - D: 正しい。属性が同じステップは前回の結果を再利用できます。
    - E: 誤り。学習できなくなります。

    **スキル:** [3.3.5](../domain3.md#skill-3-3-5) / **参照:** [CI/CD と再学習](../../../services/sagemaker.md#cicd-retraining)、[SageMaker Pipelines](../../../services/sagemaker.md#pipelines)

### 問9 {#q9}

毎週月曜の朝に再学習します。ドリフトの有無には関係なく定期で動かします。どの方法ですか。

- A. EventBridge のスケジュールで Pipelines を開始する
- B. S3 のイベント通知で Pipelines を開始する
- C. ステップキャッシュで Pipelines を開始する
- D. CloudWatch アラームで Pipelines を開始する

??? success "答えと解説"
    **正解: A**

    定期の再学習は EventBridge のスケジュールで開始します。

    - A: 正しい。
    - B: 誤り。データの到着がきっかけで、月曜の朝の定期にはなりません。
    - C: 誤り。同じステップの結果を再利用する機能で、開始のきっかけではありません。
    - D: 誤り。指標の変化がきっかけで、ドリフトの有無に関係しない定期の実行になりません。

    **スキル:** [3.3.5](../domain3.md#skill-3-3-5) / **参照:** [CI/CD と再学習](../../../services/sagemaker.md#cicd-retraining)

### 問10 {#q10}

Model Registry の状態の値として正しい組み合わせはどれですか。

- A. `Ok`、`Dropped`、`ProcessingFailed`
- B. `InService`、`Updating`、`RollingBack`、`OutOfService`
- C. `PendingManualApproval`、`Approved`、`Rejected`
- D. `Active`、`Legacy`、`EOL`

??? success "答えと解説"
    **正解: C**

    `ModelApprovalStatus` の値は `PendingManualApproval`、`Approved`、`Rejected` です。

    - A: 誤り。Firehose の変換の値です。
    - B: 誤り。エンドポイントの状態の値です。
    - C: 正しい。
    - D: 誤り。Bedrock のモデルのライフサイクルの値です。

    **スキル:** [3.3.6](../domain3.md#skill-3-3-6) / **参照:** [Model Registry](../../../services/sagemaker.md#model-registry)

### 問11 {#q11}

モデルの承認で本番へのデプロイを自動で開始し、承認の履歴を監査します。適切な組み合わせを選んでください。（2つ選択）

- A. 承認者が本番のエンドポイントへ手で配置する
- B. CloudTrail と `ApprovalDescription` に残す
- C. 状態の変更を EventBridge で検知して CodePipeline を起動する
- D. `Rejected` のときにだけデプロイする
- E. 承認の記録を EC2 のログファイルだけに残す

??? success "答えと解説"
    **正解: B, C**

    状態の変更を EventBridge で検知し、CodePipeline や Lambda を起動します。「誰がいつ承認したか」は CloudTrail と `ApprovalDescription` に残します。

    - A: 誤り。自動の開始になりません。
    - B: 正しい。誰がいつ承認したかを確認できます。
    - C: 正しい。
    - D: 誤り。承認の意味が逆です。
    - E: 誤り。改ざんや消失に弱く、監査に向きません。

    **スキル:** [3.3.6](../domain3.md#skill-3-3-6) / **参照:** [Model Registry](../../../services/sagemaker.md#model-registry)

### 問12 {#q12}

同じ解約予測のモデルの複数のバージョンをまとめて管理します。Model Registry の用語の組み合わせはどれですか。

- A. バージョンの集まりがシャード、1 つがレコード
- B. バージョンの集まりがワークグループ、1 つがクエリ
- C. バージョンの集まりがフィーチャーグループ、1 つのバージョンが最新の特徴レコード
- D. バージョンの集まりがモデルパッケージグループ、1 つがモデルパッケージ

??? success "答えと解説"
    **正解: D**

    モデルパッケージグループは同じモデルのバージョンの集まりで、モデルパッケージが 1 つのバージョンです。

    - A: 誤り。Kinesis の用語です。
    - B: 誤り。Athena の用語です。
    - C: 誤り。Feature Store の用語です。
    - D: 正しい。

    **スキル:** [3.3.6](../domain3.md#skill-3-3-6) / **参照:** [Model Registry](../../../services/sagemaker.md#model-registry)

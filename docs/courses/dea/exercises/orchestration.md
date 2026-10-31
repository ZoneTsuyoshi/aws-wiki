# オーケストレーションとイベントの問題集

対象の解説: [オーケストレーションの比較](../../../services/data-engineering.md#orchestration)、[AWS Step Functions](../../../services/step-functions.md)、[EventBridge](../../../services/messaging.md#eventbridge)

### 問1 {#q1}

毎朝 9 時（東京時間）に Lambda を起動します。新規の構築です。AWS が勧めている方法と書き方はどれですか。

- A. EventBridge のスケジュールされたルールで `cron(0 9 * * *)` の 5 項目を指定する
- B. Glue のスケジュールトリガーで Lambda を直接起動するように登録する
- C. EventBridge Scheduler で `cron(0 9 * * ? *)` とタイムゾーンを指定する
- D. MWAA の環境を作り、DAG の `schedule` に `rate(1 day)` を指定して Lambda を呼ぶ

??? success "答えと解説"
    **正解: C**

    Scheduler はタイムゾーンを指定できます。

    - A: 誤り。EventBridge の cron は 6 項目で、Scheduler が勧められています。
    - B: 誤り。Glue のトリガーの対象はジョブとクローラーです。
    - C: 正しい。
    - D: 誤り。1 つの関数の起動には過剰で、書き方も EventBridge のものです。

    **スキル:** [1.1.5](../domain1.md#skill-1-1-5) / **参照:** [スケジュール](../../../services/messaging.md#eventbridge-schedule)

### 問2 {#q2}

Airflow の DAG を毎日 2 時に実行します。DAG の `schedule` の書き方として正しいものはどれですか。

- A. `rate(24 hours)`
- B. `0 2 * * *`
- C. `at(02:00:00)`
- D. `cron(0 2 * * ? *)`

??? success "答えと解説"
    **正解: B**

    Airflow の cron は通常 5 項目です。

    - A: 誤り。EventBridge の書き方です。
    - B: 正しい。
    - C: 誤り。Scheduler の 1 回のみの書き方に似せたもので、日付も足りません。
    - D: 誤り。EventBridge の書き方です。

    **スキル:** [1.1.5](../domain1.md#skill-1-1-5) / **参照:** [Amazon MWAA](../../../services/data-engineering.md#mwaa)、[スケジュール](../../../services/messaging.md#eventbridge-schedule)

### 問3 {#q3}

毎晩のクローラーの後に Glue ジョブを実行します。Glue の中だけで完結させ、クローラーの完了を待ってからジョブを起動します。どう設定しますか。

- A. ワークフローでクローラーをスケジュールトリガーで起動し、成功を条件トリガーで受けてジョブを起動する
- B. ジョブのブックマークを有効にして、クローラーが終わるまで自動で待機するように設定する
- C. クローラーの `CRAWL_NEW_FOLDERS_ONLY` を設定して、完了時にジョブが自動で起動するようにする
- D. クローラーとジョブに同じ時刻のスケジュールトリガーを別々に設定し、同時に動かす

??? success "答えと解説"
    **正解: A**

    条件トリガーは、ジョブとクローラーの完了状態を監視できます。

    - A: 正しい。
    - B: 誤り。ブックマークは処理位置の追跡で、待機の機能はありません。
    - C: 誤り。再クロールの範囲の設定で、ジョブは起動しません。
    - D: 誤り。クローラーの完了を待てません。

    **スキル:** [1.1.5](../domain1.md#skill-1-1-5) / **参照:** [クローラー](../../../services/data-engineering.md#glue-crawlers)、[ワークフローとトリガー](../../../services/data-engineering.md#glue-workflows)

### 問4 {#q4}

Lambda が S3 の `raw/` に届いたファイルを変換し、同じ `raw/` に結果を書いたところ、関数が繰り返し起動して費用が急増しました。根本の対策はどれですか。

- A. 通知の宛先を SNS へ変更し、そこから関数を呼ぶように経路を変える
- B. 関数のタイムアウトを短くし、ループが長く続かないように打ち切る
- C. 関数のメモリを増やして、変換を早く終わらせ、起動の回数を減らす
- D. 出力先を入力と別のプレフィックスに分け、通知を `raw/` に絞る

??? success "答えと解説"
    **正解: D**

    入力と同じ場所に書くとイベントがループします。

    - A: 誤り。経路が変わるだけで、同じ起動のループです。
    - B: 誤り。書き込みが完了すればまた起動するので、ループは残ります。
    - C: 誤り。起動の回数は書き込みの数で決まり、ループは止まりません。
    - D: 正しい。

    **スキル:** [1.1.6](../domain1.md#skill-1-1-6) / **参照:** [Event Notifications](../../../services/s3.md#event-notifications)、[S3 イベント通知](../../../services/messaging.md#s3-events)

### 問5 {#q5}

S3 にファイルが届くと、Step Functions の起動、別の関数の呼び出し、SNS の通知の 3 つを行います。ファイルの種類で振り分けもします。どの方法が適切ですか。

- A. S3 イベント通知のサフィックスを 3 つ書き、同じ種類のファイルを 3 つの宛先に重ねて送る
- B. SQS を宛先にして、ワーカーが自分でファイルの種類を調べ、3 つのサービスを順に呼ぶ
- C. バケットで EventBridge への送信を有効にし、ルールのパターンで振り分ける
- D. ファイルの到着で Glue のクローラーを起動し、3 つのサービスを呼ぶ

??? success "答えと解説"
    **正解: C**

    内容での振り分けと複数のターゲットには EventBridge が向きます。

    - A: 誤り。同じイベントの種類で重なるプレフィックスとサフィックスの設定は作れません。
    - B: 誤り。振り分けのコードを自分で持つことになります。
    - C: 正しい。
    - D: 誤り。クローラーにそのような起動の機能はありません。

    **スキル:** [1.1.6](../domain1.md#skill-1-1-6) / **参照:** [ルールとイベントパターン](../../../services/messaging.md#eventbridge-rules)、[S3 イベント通知](../../../services/messaging.md#s3-events)

### 問6 {#q6}

小さなファイルが連続して届きます。Glue ワークフローを、100 個たまるか 10 分たつかの先に満たしたほうで開始します。何を設定しますか。

- A. 条件トリガーに、監視するジョブの状態として件数 100 を指定して、開始を遅らせる
- B. EventBridge イベントのトリガーでバッチの条件に、件数 100 とウィンドウ 600 秒を指定する
- C. ジョブの最大同時実行数を 100 にして、ファイルごとに別の実行を起動して動かす
- D. スケジュールトリガーに `rate(10 minutes)` を指定して、件数の条件は S3 の通知で補う

??? success "答えと解説"
    **正解: B**

    件数だけ指定するとウィンドウは 15 分になります。

    - A: 誤り。条件トリガーはジョブなどの完了状態を監視します。
    - B: 正しい。
    - C: 誤り。バッチにはならず、実行が増えて費用も増えます。
    - D: 誤り。Glue のスケジュールトリガーは cron で、件数の条件もありません。

    **スキル:** [1.1.6](../domain1.md#skill-1-1-6) / **参照:** [ワークフローとトリガー](../../../services/data-engineering.md#glue-workflows)

### 問7 {#q7}

パイプラインは Glue、Lambda、Redshift の Data API、SNS で構成されます。すべて AWS の中で完結し、新規の構築で、サーバーは持ちません。分岐と再試行が必要です。何を選びますか。

- A. EventBridge のルールの連鎖
- B. MWAA
- C. Glue ワークフロー
- D. Step Functions

??? success "答えと解説"
    **正解: D**

    AWS で完結する混在処理には Step Functions が向きます。

    - A: 誤り。開始のきっかけには向きますが、分岐や再試行の流れは持ちません。
    - B: 誤り。動きますが、環境の料金がかかり、既存の Airflow がない場合の第一候補ではありません。
    - C: 誤り。対象は Glue のジョブとクローラーで、分岐も条件トリガーのみです。
    - D: 正しい。

    **スキル:** [1.3.1](../domain1.md#skill-1-3-1) / **参照:** [オーケストレーションの比較](../../../services/data-engineering.md#orchestration)

### 問8 {#q8}

既存の Airflow の DAG が 200 個あり、オンプレミスの処理や他社クラウドのデータも扱います。DAG はできるだけ書き直しません。何を選びますか。

- A. MWAA に DAG を移して動かす
- B. Step Functions の Standard ワークフロー
- C. Glue のブループリント
- D. Lambda とステート保存用の DynamoDB テーブル

??? success "答えと解説"
    **正解: A**

    既存の Airflow や AWS 外との連携があるなら MWAA です。

    - A: 正しい。
    - B: 誤り。DAG を ASL に書き直す必要があります。
    - C: 誤り。対象は Glue の部品で、AWS の外の処理は扱えません。
    - D: 誤り。依存の管理を自作することになります。

    **スキル:** [1.3.1](../domain1.md#skill-1-3-1) / **参照:** [オーケストレーションの比較](../../../services/data-engineering.md#orchestration)、[Amazon MWAA](../../../services/data-engineering.md#mwaa)

### 問9 {#q9}

Step Functions で Glue ジョブの後に `COPY` を実行します。Glue の出力が揃う前に `COPY` が始まります。どう直しますか。

- A. Glue のタスクの `Resource` に `.waitForTaskToken` を付けて、Glue が自動で完了を通知するようにする
- B. ワークフローを Express に変更して、Glue のジョブの完了までを 5 分以内に収めるようにする
- C. Glue のタスクの後に `Wait` を 30 分入れて、普段の処理時間が過ぎるのを待つようにする
- D. Glue のタスクの `Resource` を `arn:aws:states:::glue:startJobRun.sync` にする

??? success "答えと解説"
    **正解: D**

    `.sync` がないと、ジョブの起動だけで次へ進みます。

    - A: 誤り。誰かがトークンを返す実装が必要で、Glue は自動で返しません。
    - B: 誤り。Express は `.sync` を使えません。
    - C: 誤り。処理時間が延びると同じ問題が起きます。
    - D: 正しい。

    **スキル:** [1.3.1](../domain1.md#skill-1-3-1) / **参照:** [サービス統合パターン](../../../services/step-functions.md#integration-patterns)、[オーケストレーションの比較](../../../services/data-engineering.md#orchestration)

### 問10 {#q10}

次の要件のうち、Glue ワークフローで十分なものはどれですか。

- A. 2 つの Glue ジョブが成功したらクローラーを実行し、すべて Glue の中で完結する
- B. Glue の後に ECS のタスクと SageMaker の処理を実行し、待ち合わせて通知する
- C. Glue のジョブの失敗時に、エラーの種類で分岐して、別のサービスの処理へ振り分ける
- D. オンプレミスのバッチの完了を待ってから、Python のカスタムセンサーで開始する

??? success "答えと解説"
    **正解: A**

    Glue だけで完結するならワークフローで足ります。

    - A: 正しい。
    - B: 誤り。Glue 以外の部品は Glue ワークフローの対象外です。
    - C: 誤り。エラー名での分岐は Step Functions が向きます。
    - D: 誤り。Airflow のセンサーのような使い方は MWAA が向きます。

    **スキル:** [1.3.1](../domain1.md#skill-1-3-1) / **参照:** [オーケストレーションの比較](../../../services/data-engineering.md#orchestration)、[ワークフローとトリガー](../../../services/data-engineering.md#glue-workflows)

### 問11 {#q11}

Glue のタスクが一時的な失敗で止まることがあります。3 回まで間隔を空けて再試行し、それでも失敗したら SNS に通知します。どの定義ですか。

- A. `Catch` だけを指定して通知の状態へ進め、再試行は Glue のブックマークに任せる
- B. `Choice` で実行の回数を比べ、`Wait` と `Pass` を組み合わせて再試行の流れを自分で作る
- C. `Retry` で `MaxAttempts` と `BackoffRate` を指定し、`Catch` で通知の状態へ進める
- D. `TimeoutSeconds` を長くして失敗を待ち、時間切れになったら自動で通知されるようにする

??? success "答えと解説"
    **正解: C**

    `Retry` と `Catch` を組み合わせます。

    - A: 誤り。ブックマークは再試行の機能ではありません。
    - B: 誤り。組み込みの `Retry` があるので、複雑になります。
    - C: 正しい。
    - D: 誤り。タイムアウトと通知は自動では結びつきません。

    **スキル:** [1.3.2](../domain1.md#skill-1-3-2) / **参照:** [エラー処理](../../../services/step-functions.md#error-handling)、[Catch](../../../services/step-functions.md#catch)

### 問12 {#q12}

EMR on EC2 の長期クラスターの可用性を高めます。正しい説明はどれですか。（2つ選択）

- A. プライマリを 3 台にして単一障害点をなくす
- B. プライマリを 2 台にして、片方をスタンバイにする
- C. コアノードをすべて Spot にして、中断があっても別の AZ で再開するようにする
- D. プライマリを 3 台にして、別々の AZ に配置し、AZ の障害に耐えるようにする
- E. 入出力を HDFS ではなく S3 に置き、クラスターが消えてもデータを残す

??? success "答えと解説"
    **正解: A, E**

    プライマリの冗長化と S3 の利用が基本です。

    - A: 正しい。ただしクラスターは 1 つの AZ に置きます。
    - B: 誤り。プライマリは 1 台または 3 台です。
    - C: 誤り。HDFS のブロックを失う恐れがあります。
    - D: 誤り。クラスターは 1 つの AZ またはサブネットに置きます。
    - E: 正しい。S3 はクラスターと独立して残ります。

    **スキル:** [1.3.2](../domain1.md#skill-1-3-2) / **参照:** [クラスターのノード](../../../services/data-engineering.md#emr-nodes)、[HDFS と S3](../../../services/data-engineering.md#emr-hdfs-vs-s3)

### 問13 {#q13}

Step Functions が失敗した Glue のロードを再試行すると、S3 のテーブルに同じ行が二重に入ることがあります。再実行しても壊れないようにするには何を使いますか。

- A. Step Functions の `Retry` を削除し、失敗のたびに人が手動で再実行するように変更する
- B. Iceberg の ACID と `MERGE` を使い、同じキーを上書きする書き込みにする
- C. Glue のジョブのタイムアウトを短くして、失敗したジョブが書き込みを終える前に止める
- D. 書き込みのたびに S3 のバージョニングを有効にし、古いバージョンを残しておくようにする

??? success "答えと解説"
    **正解: B**

    冪等な書き込みにすれば、再実行しても結果が変わりません。

    - A: 誤り。手動にしても書き込みの重複は防げません。
    - B: 正しい。
    - C: 誤り。中途半端な書き込みが残ります。
    - D: 誤り。バージョンが増えるだけで、行の重複は防げません。

    **スキル:** [1.3.2](../domain1.md#skill-1-3-2) / **参照:** [冪等性](../../../services/sdk-resilience.md#idempotency)、[Apache Iceberg](../../../services/data-engineering.md#iceberg)

### 問14 {#q14}

Glue ジョブの完了を待ち、数時間かかることもある ETL です。人の承認の手順も入ります。どのワークフローの種類ですか。

- A. Lambda の非同期呼び出しの連鎖
- B. Express の同期実行
- C. Standard
- D. Express の非同期実行

??? success "答えと解説"
    **正解: C**

    Standard は最大 1 年で、`.sync` を使えます。

    - A: 誤り。ワークフローの種類ではなく、状態も追跡できません。
    - B: 誤り。最大 5 分で、`.sync` も使えません。
    - C: 正しい。
    - D: 誤り。最大 5 分で、`.sync` も使えません。

    **スキル:** [1.3.3](../domain1.md#skill-1-3-3) / **参照:** [Standard と Express](../../../services/step-functions.md#standard-express)、[サービス統合パターン](../../../services/step-functions.md#integration-patterns)

### 問15 {#q15}

S3 の 1 万個のファイルをそれぞれ小さな Lambda で並列に処理します。Step Functions で使う状態はどれですか。

- A. `Choice` の中で `Pass` を繰り返し、1 件ずつ順番に処理を進める
- B. `Map` で `MaxConcurrency` に並列数を指定して、ファイルごとに繰り返す
- C. `Wait` の間に、別のスケジュールで関数を起動して並列にする
- D. `Parallel` にファイルの数だけ分岐を書き、定義を自動生成して更新する

??? success "答えと解説"
    **正解: B**

    大量のファイルを並列に処理するなら `Map` です。

    - A: 誤り。並列に処理できません。
    - B: 正しい。
    - C: 誤り。状態機械の外の仕組みになり、完了を追跡できません。
    - D: 誤り。分岐の数が固定で、データの数に合わせる用途ではありません。

    **スキル:** [1.3.3](../domain1.md#skill-1-3-3) / **参照:** [Map の設定](../../../services/step-functions.md#map-settings)、[Standard と Express](../../../services/step-functions.md#standard-express)

### 問16 {#q16}

Standard の実行が 10 段目で失敗しました。原因を直したので、9 段目までをやり直さず再開します。何を使いますか。

- A. 同じ入力で `StartExecution` を実行し、完了済みの段を自動でスキップさせる
- B. `Catch` の設定を追加してから、失敗済みの実行に自動で適用されるのを待つ
- C. Express に切り替えて過去の実行を再開させる
- D. `RedriveExecution` で失敗した状態から再開する

??? success "答えと解説"
    **正解: D**

    完了から 14 日以内なら redrive できます。

    - A: 誤り。最初から実行されます。
    - B: 誤り。定義の変更は完了した実行には適用されません。
    - C: 誤り。redrive は Standard の機能です。
    - D: 正しい。

    **スキル:** [1.3.3](../domain1.md#skill-1-3-3) / **参照:** [再実行とログ](../../../services/step-functions.md#redrive-logging)

### 問17 {#q17}

Glue ジョブが失敗したら、担当者にメールを送ります。コードは書きません。どの構成ですか。

- A. EventBridge のルールで失敗の状態変更を受け、SNS トピックへ送る
- B. CloudTrail の証跡で失敗を S3 へ出力する
- C. Glue のジョブの中に例外処理を書いて、SES の API でメールを送信する
- D. SQS のキューを Glue の失敗の宛先に設定して、担当者がポーリングで確認する

??? success "答えと解説"
    **正解: A**

    ジョブの状態変更は EventBridge で受けられます。

    - A: 正しい。
    - B: 誤り。API の記録で、失敗の通知にはなりません。
    - C: 誤り。コードが必要で、SES はこの試験の範囲外です。
    - D: 誤り。Glue にその宛先の設定はなく、メールにもなりません。

    **スキル:** [1.3.4](../domain1.md#skill-1-3-4) / **参照:** [ルールとイベントパターン](../../../services/messaging.md#eventbridge-rules)、[SNS](../../../services/messaging.md#sns)

### 問18 {#q18}

ジョブ失敗の通知を、運用担当のメールと自動修復の処理の 2 つへ送ります。修復の処理は止まっていても通知を失わないようにします。どの構成ですか。

- A. SNS のメールの配信だけにして、修復の処理は担当者がメールを見て手で実行する
- B. SNS から修復の Lambda を同期で呼び、失敗したらメールの配信も止める
- C. SNS からメールへ配信し、修復の処理には SNS の後ろに SQS を置く
- D. SQS だけを使い、メールの担当者と修復の処理が同じキューをポーリングする

??? success "答えと解説"
    **正解: C**

    確実に処理したいときは SNS の後ろに SQS を置きます。

    - A: 誤り。自動修復になりません。
    - B: 誤り。同期でも、通知同士を連動させる機能でもありません。
    - C: 正しい。
    - D: 誤り。1 通は 1 つの消費者にしか渡らず、メールも送れません。

    **スキル:** [1.3.4](../domain1.md#skill-1-3-4) / **参照:** [ファンアウト](../../../services/messaging.md#fanout)、[SQS](../../../services/messaging.md#sqs)

### 問19 {#q19}

Athena のワークグループで、1 日のスキャン量が 10 TB を超えたら管理者へ通知します。クエリを個別に止める必要はありません。何を設定しますか。

- A. ワークグループ全体のデータ使用量の制限を作り、SNS へ通知する
- B. CloudTrail のデータイベントを有効にして、スキャン量をログから毎日計算する
- C. クエリごとのデータ使用量の制限を 10 TB にして、超えたクエリの実行者に通知する
- D. Budgets のアクションでワークグループを無効にする

??? success "答えと解説"
    **正解: A**

    ワークグループ全体の制限は、期間の合計で通知できます。

    - A: 正しい。
    - B: 誤り。API の記録で、スキャン量の制限の機能ではありません。
    - C: 誤り。1 クエリの制限で、超えるとキャンセルされます。
    - D: 誤り。要件はスキャン量の通知で、クエリは止めません。

    **スキル:** [1.3.4](../domain1.md#skill-1-3-4) / **参照:** [ワークグループ](../../../services/streaming.md#athena-workgroups)、[アラームのアクション](../../../services/observability.md#alarm-actions)

### 問20 {#q20}

MWAA で DAG を更新します。ファイルを置く場所はどこですか。

- A. CodeBuild のアーティファクトのバケットの `requirements.txt` の中
- B. Airflow の Web サーバーのローカルディスクの `dags/` フォルダ
- C. 環境の VPC に作成した EFS の `/mnt/dags` フォルダ
- D. 環境に指定した S3 バケットの `dags/` フォルダ

??? success "答えと解説"
    **正解: D**

    DAG は S3 の `dags/`、依存は `requirements.txt` です。

    - A: 誤り。`requirements.txt` は依存パッケージの一覧です。
    - B: 誤り。DAG は S3 に置きます。
    - C: 誤り。MWAA の DAG の置き場ではありません。
    - D: 正しい。

    **スキル:** [3.1.1](../domain3.md#skill-3-1-1) / **参照:** [Amazon MWAA](../../../services/data-engineering.md#mwaa)

### 問21 {#q21}

MWAA の環境で、DAG 40 個を動かします。同時タスクの既定は 5 個で足ります。費用を抑えた環境クラスはどれですか。

- A. `mw1.medium`
- B. `mw1.small`
- C. `mw1.micro`
- D. `mw1.large`

??? success "答えと解説"
    **正解: B**

    `mw1.small` は DAG 50 個、同時タスク 5 が目安です。

    - A: 誤り。DAG 250 個の目安で、過剰です。
    - B: 正しい。
    - C: 誤り。DAG の目安は 25 個で、40 個には足りません。
    - D: 誤り。DAG 1,000 個の目安で、過剰です。

    **スキル:** [3.1.1](../domain3.md#skill-3-1-1) / **参照:** [Amazon MWAA](../../../services/data-engineering.md#mwaa)、[オーケストレーションの比較](../../../services/data-engineering.md#orchestration)

### 問22 {#q22}

パイプラインの定義方法の説明として正しいものはどれですか。（2つ選択）

- A. Step Functions の料金は MWAA と同じで、環境の起動時間で決まる
- B. MWAA の DAG は ASL の JSON で定義する
- C. MWAA はプロバイダーのオペレーターで Glue などを呼ぶ
- D. Step Functions は S3 の `dags/` に定義を置いて読み込む
- E. Step Functions は ASL の JSON で定義する

??? success "答えと解説"
    **正解: C, E**

    定義の形式と課金の違いを押さえます。

    - A: 誤り。Standard は状態遷移の数で決まります。
    - B: 誤り。DAG は Python です。
    - C: 正しい。`GlueJobOperator` などを使います。
    - D: 誤り。それは MWAA です。
    - E: 正しい。Amazon States Language です。

    **スキル:** [3.1.1](../domain3.md#skill-3-1-1) / **参照:** [サービス統合パターン](../../../services/step-functions.md#integration-patterns)、[オーケストレーションの比較](../../../services/data-engineering.md#orchestration)

### 問23 {#q23}

インターネットへの経路のない VPC の MWAA で、`requirements.txt` のインストールが失敗して DAG がインポートエラーになります。どう直しますか。

- A. DAG を `plugins/` に移して依存を解決する
- B. 環境クラスを `mw1.2xlarge` に上げて、同時タスクを増やしてから再度試す
- C. 依存パッケージを `plugins.zip` に同梱する
- D. `requirements.txt` の行を増やして、依存パッケージのバージョンをすべて最新にする

??? success "答えと解説"
    **正解: C**

    PyPI に届かないなら同梱します。

    - A: 誤り。依存の解決はされません。
    - B: 誤り。規模の問題ではありません。
    - C: 正しい。
    - D: 誤り。PyPI に届かないので解決しません。

    **スキル:** [3.1.2](../domain3.md#skill-3-1-2) / **参照:** [Amazon MWAA](../../../services/data-engineering.md#mwaa)

### 問24 {#q24}

MWAA の DAG でタスクがキューに長くたまり、スケジュールが遅れます。CPU の使用率は高い状態です。どの見直しが適切ですか。

- A. DAG の `schedule` を EventBridge の cron の形式に書き換えて実行する
- B. 環境クラスを大きくするか、最大ワーカー数を上げる
- C. Web サーバーを非公開に切り替える
- D. `requirements.txt` から不要な行を削り、DAG の数を変えずに待つ

??? success "答えと解説"
    **正解: B**

    タスクの詰まりには環境クラスとワーカーの上限が効きます。

    - A: 誤り。書き方は Airflow のものです。
    - B: 正しい。
    - C: 誤り。Web サーバーのアクセスの設定で、タスクの実行とは別です。
    - D: 誤り。依存の一覧の問題ではありません。

    **スキル:** [3.1.2](../domain3.md#skill-3-1-2) / **参照:** [Amazon MWAA](../../../services/data-engineering.md#mwaa)、[ロググループと保持期間](../../../services/observability.md#log-groups)

### 問25 {#q25}

Express の状態機械が失敗しますが、コンソールの実行履歴から原因を追えません。どうしますか。

- A. CloudTrail のデータイベントを有効にし、状態の入出力を記録する
- B. `GetExecutionHistory` を繰り返し呼び、Express の履歴を API で取得する
- C. `RedriveExecution` で再実行して確認する
- D. CloudWatch Logs へのログを有効にして確認する

??? success "答えと解説"
    **正解: D**

    Express は CloudWatch Logs で確認します。

    - A: 誤り。状態の入出力の記録には使えません。
    - B: 誤り。Standard の機能です。
    - C: 誤り。redrive は Standard の機能です。
    - D: 正しい。

    **スキル:** [3.1.2](../domain3.md#skill-3-1-2) / **参照:** [主なエラー名](../../../services/step-functions.md#error-names)、[再実行とログ](../../../services/step-functions.md#redrive-logging)

### 問26 {#q26}

EventBridge のルールのターゲットの Lambda に権限がなく、配信が失敗しています。失敗したイベントを失わないようにする設定はどれですか。

- A. ターゲットに SQS の DLQ を設定する
- B. ルールのイベントパターンを広げて、より多くのイベントが届くようにする
- C. Lambda の予約済み同時実行を 0 にする
- D. CloudWatch のアラームの欠落データの扱いを `breaching` に変更する

??? success "答えと解説"
    **正解: A**

    再試行の後に失敗したイベントは DLQ へ送れます。

    - A: 正しい。
    - B: 誤り。配信の失敗は解決しません。
    - C: 誤り。イベントは失われ、権限の問題も解決しません。
    - D: 誤り。監視の設定で、イベントの保持ではありません。

    **スキル:** [3.1.9](../domain3.md#skill-3-1-9) / **参照:** [ターゲットの再試行と DLQ](../../../services/messaging.md#target-retry-dlq)、[ルールとイベントパターン](../../../services/messaging.md#eventbridge-rules)

### 問27 {#q27}

下流のバグで 2 日前からのイベントを取りこぼしました。イベントを再送して処理し直します。事前に設定されていれば使える機能はどれですか。また注意点は何ですか。

- A. EventBridge Pipes。アーカイブがなくても、バスの過去のイベントを読み直す
- B. 入力トランスフォーマー。過去のイベントの内容を書き換えて、もう一度配信する
- C. スキーマレジストリ。イベントの過去のバージョンを、その順序どおりに再送する
- D. アーカイブとリプレイ。順序は保証されないので、処理を順序に依存させない

??? success "答えと解説"
    **正解: D**

    アーカイブに保存したイベントをリプレイできます。

    - A: 誤り。ソースとターゲットをつなぐ機能で、過去のイベントは読みません。
    - B: 誤り。渡す内容を変える機能で、過去のイベントの再送はしません。
    - C: 誤り。スキーマの管理で、イベントの再送はしません。
    - D: 正しい。

    **スキル:** [3.1.9](../domain3.md#skill-3-1-9) / **参照:** [アーカイブとリプレイ](../../../services/messaging.md#archive-replay)

### 問28 {#q28}

要件と機能の組み合わせとして正しいものはどれですか。

- A. 深夜に 1 回だけ実行する予約は、ルールのイベントパターンで指定する
- B. ジョブ失敗だけを SNS に送る振り分けは、Scheduler の `rate()` で指定する
- C. SQS のメッセージを 1 対 1 で Step Functions へ渡すのは Pipes
- D. 時間に余裕を持たせる柔軟な時間枠は、Pipes のフィルターで指定する

??? success "答えと解説"
    **正解: C**

    ルール、Scheduler、Pipes の役割を分けて考えます。

    - A: 誤り。1 回のみの予約は Scheduler の `at()` です。
    - B: 誤り。内容の振り分けはルールで行います。
    - C: 正しい。
    - D: 誤り。柔軟な時間枠は Scheduler の機能です。

    **スキル:** [3.1.9](../domain3.md#skill-3-1-9) / **参照:** [Pipes](../../../services/messaging.md#eventbridge-pipes)、[スケジュール](../../../services/messaging.md#eventbridge-schedule)

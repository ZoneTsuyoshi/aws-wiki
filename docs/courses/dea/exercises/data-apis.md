# データ API と SDKの問題集

対象の解説: [Amazon API Gateway](../../../services/api-gateway.md)、[SDK と耐障害性](../../../services/sdk-resilience.md)、[Amazon Redshift](../../../services/data-engineering.md#redshift)

### 問1 {#q1}

外部の REST API から全件を読みます。1 回 100 件で、次のページのトークンが返り、時々 429 が返ります。正しい実装はどれですか。

- A. 429 が返ったら間隔を空けずに同じ要求を繰り返し、先に全ページを読み切る
- B. トークンをたどり、429 には指数バックオフとジッターで再試行する
- C. 最初のページだけを読み、件数の合計から残りを推定して計算の対象を補う
- D. 429 が返ったページはエラーとして読み飛ばし、次のページのトークンへ進む

??? success "答えと解説"
    **正解: B**

    ページをたどり、レート制限にはバックオフで対応します。

    - A: 誤り。制限が長引きます。
    - B: 正しい。
    - C: 誤り。途中で切れてデータが欠けます。
    - D: 誤り。データが欠けます。

    **スキル:** [1.1.4](../domain1.md#skill-1-1-4) / **参照:** [ページネーション](../../../services/sdk-resilience.md#pagination)、[指数バックオフとジッター](../../../services/sdk-resilience.md#backoff-jitter)

### 問2 {#q2}

独自の REST API を 1 時間ごとに読みます。処理は数分で、API キーをコードに書きません。どの構成が適切ですか。

- A. EventBridge Scheduler で Lambda を起動し、API キーはデプロイのたびに環境変数へ平文で設定する
- B. AppFlow のスケジュールで起動して、対応していない独自の API を変換機能で呼ぶ
- C. EventBridge Scheduler で Lambda を起動し、API キーは Secrets Manager から取得する
- D. EC2 の cron で起動し、API キーは AMI の中のファイルに保存しておく

??? success "答えと解説"
    **正解: C**

    独自の API の定期実行は Scheduler と Lambda です。

    - A: 誤り。キーをコードの近くに平文で置くことになります。
    - B: 誤り。独自の API には Custom Connector の作成が必要です。
    - C: 正しい。
    - D: 誤り。運用が増え、キーの管理も不適切です。

    **スキル:** [1.1.4](../domain1.md#skill-1-1-4) / **参照:** [Secrets Manager](../../../services/secrets.md#secrets-manager)、[スケジュール](../../../services/messaging.md#eventbridge-schedule)

### 問3 {#q3}

SaaS の API から数百万ページを取得して変換します。1 回の取得は数時間かかります。実行先はどれですか。

- A. Glue の Python shell か Spark のジョブ
- B. Firehose の Lambda 変換の中でページをたどる
- C. 1 つの Lambda 関数で全ページを順に取得する
- D. API Gateway の統合で SaaS の API を呼び続ける

??? success "答えと解説"
    **正解: A**

    長い取得と変換は Glue に任せます。

    - A: 正しい。
    - B: 誤り。呼び出しの上限は 5 分で、取得の用途でもありません。
    - C: 誤り。実行時間の上限は 15 分です。
    - D: 誤り。統合のタイムアウトは既定で 29 秒です。

    **スキル:** [1.1.4](../domain1.md#skill-1-1-4) / **参照:** [Amazon AppFlow](../../../services/data-engineering.md#appflow)、[ETL ジョブ](../../../services/data-engineering.md#glue-jobs)

### 問4 {#q4}

顧客 ID で最新のスコアを数十ミリ秒で返す API を作ります。運用は最小です。どの構成ですか。

- A. API Gateway、Lambda、Athena
- B. CloudFront、Glue のジョブ、Redshift
- C. API Gateway、EMR、S3 のファイル
- D. API Gateway、Lambda、DynamoDB

??? success "答えと解説"
    **正解: D**

    キーで引く低遅延の API の定番です。

    - A: 誤り。クエリは非同期で、低遅延には向きません。
    - B: 誤り。ジョブは起動に時間がかかり、API には向きません。
    - C: 誤り。クラスターの運用があり、低遅延にも向きません。
    - D: 正しい。

    **スキル:** [1.2.8](../domain1.md#skill-1-2-8) / **参照:** [統合タイプ](../../../services/api-gateway.md#integration-types)、[キーの設計](../../../services/dynamodb.md#keys)

### 問5 {#q5}

Lambda から Redshift へ、ドライバーと常時接続なしで SQL を送り、結果を返します。呼び出しの流れとして正しいものはどれですか。

- A. `ExecuteStatement` の後に `DescribeStatement` で状態を確認し、`GetStatementResult` で取得する
- B. `GetQueryExecution` の後に `GetQueryResults` で取得し、Redshift の結果として返す
- C. `ExecuteStatement` の戻り値に結果が入るので、そのまま呼び出し元の API へ返す
- D. `StartJobRun` の後に `GetJobRun` で状態を確認し、S3 の出力ファイルを読んで返す

??? success "答えと解説"
    **正解: A**

    Redshift Data API は非同期です。

    - A: 正しい。
    - B: 誤り。Athena の API です。
    - C: 誤り。呼び出しは非同期です。
    - D: 誤り。Glue の API です。

    **スキル:** [1.2.8](../domain1.md#skill-1-2-8) / **参照:** [Amazon Redshift](../../../services/data-engineering.md#redshift)、[Amazon Athena](../../../services/streaming.md#athena)

### 問6 {#q6}

数分かかる Redshift のレポートを API で提供します。API Gateway の統合のタイムアウトは既定の 29 秒です。どう設計しますか。

- A. API Gateway のキャッシュを有効にして、1 回目の実行の待ち時間をなくすようにする
- B. 受付の API で実行 ID を返し、結果の取得の API を分ける
- C. Lambda のタイムアウトを 15 分に延ばして、API Gateway の応答もそれに合わせて待たせる
- D. 使用量プランのスロットリングを下げて、1 回の実行にかかる時間を短くするようにする

??? success "答えと解説"
    **正解: B**

    重いクエリは受付と結果の取得で API を分けます。

    - A: 誤り。1 回目の実行は速くなりません。
    - B: 正しい。
    - C: 誤り。統合のタイムアウトで先に切れます。
    - D: 誤り。実行時間は変わりません。

    **スキル:** [1.2.8](../domain1.md#skill-1-2-8) / **参照:** [統合タイプ](../../../services/api-gateway.md#integration-types)、[Amazon Redshift](../../../services/data-engineering.md#redshift)

### 問7 {#q7}

SDK で Athena のクエリを実行します。`start_query_execution` の直後に `get_query_results` を呼ぶとエラーになります。正しい流れはどれですか。

- A. `start_query_execution` の `QueryString` に待機のオプションを書き、同期で実行させる
- B. `execute_statement` に切り替えて、Athena のクエリを同期で実行する
- C. `get_query_results` を呼ぶ前に `start_job_run` を実行して、結果の準備を待つ
- D. `get_query_execution` で状態が `SUCCEEDED` になるのを確認してから結果を取る

??? success "答えと解説"
    **正解: D**

    データ系の API の多くは非同期です。

    - A: 誤り。API は非同期で、そのオプションはありません。
    - B: 誤り。Redshift Data API で、Athena には使えません。
    - C: 誤り。Glue の API です。
    - D: 正しい。

    **スキル:** [3.1.3](../domain3.md#skill-3-1-3) / **参照:** [AWS SDK の基本](../../../services/sdk-resilience.md#sdk-basics)、[Amazon Athena](../../../services/streaming.md#athena)

### 問8 {#q8}

SDK のページネーターとウェイターの説明として正しいものはどれですか。（2つ選択）

- A. ウェイターは、一時的な失敗のたびに別のリージョンへ自動で切り替える
- B. ウェイターは、クォータの上限を自動で引き上げる
- C. ページネーターは、一覧の API の続きのトークンをたどり全件を返す
- D. ページネーターは、S3 のオブジェクトを分割してアップロードする
- E. ウェイターは、リソースが目的の状態になるまで繰り返し確認する

??? success "答えと解説"
    **正解: C, E**

    どちらも SDK の便利機能です。

    - A: 誤り。状態の確認の機能です。
    - B: 誤り。クォータの変更はできません。
    - C: 正しい。自分でトークンを扱わずに済みます。
    - D: 誤り。マルチパートアップロードの話です。
    - E: 正しい。ポーリングを SDK に任せられます。

    **スキル:** [3.1.3](../domain3.md#skill-3-1-3) / **参照:** [ページネーション](../../../services/sdk-resilience.md#pagination)、[ウェイター](../../../services/sdk-resilience.md#waiters)

### 問9 {#q9}

Lambda から boto3 で Glue ジョブを起動します。一時的な失敗に耐え、認証情報はコードに書きません。どの実装が適切ですか。

- A. `AssumeRole` の代わりに root ユーザーのキーを Secrets Manager に置いて使う
- B. アクセスキーを環境変数に書き、例外が出たらループで間隔なく再試行する
- C. 実行ロールの権限で `start_job_run` を呼び、SDK の再試行モードを設定する
- D. アクセスキーをコードに書き、一時的な失敗は再試行せず呼び出し元に返す

??? success "答えと解説"
    **正解: C**

    認証情報は IAM ロールから取得します。

    - A: 誤り。root のキーを使うのは不適切です。
    - B: 誤り。長期の認証情報を置くことになり、再試行も不適切です。
    - C: 正しい。
    - D: 誤り。認証情報をコードに書いています。

    **スキル:** [3.1.3](../domain3.md#skill-3-1-3) / **参照:** [SDK の再試行モード](../../../services/sdk-resilience.md#retry-modes)、[Lambda の実行ロール](../../../services/iam.md#lambda-execution-role)

### 問10 {#q10}

データ API を取引先に公開します。取引先ごとに 1 日のリクエスト数を制限します。REST API で使う機能はどれですか。

- A. ステージ変数と Lambda のエイリアスの組み合わせ
- B. カナリアリリースの割合の設定を取引先ごとに分ける
- C. 使用量プランと API キー
- D. リクエストの検証で、ヘッダーの形式を確認する設定

??? success "答えと解説"
    **正解: C**

    使用量プランでスロットリングとクォータを設定します。

    - A: 誤り。環境の切り替えに使う機能です。
    - B: 誤り。変更を安全に出す機能です。
    - C: 正しい。
    - D: 誤り。不正な入力を止める機能です。

    **スキル:** [3.1.5](../domain3.md#skill-3-1-5) / **参照:** [使用量プランと API キー](../../../services/api-gateway.md#usage-plans)、[エラーコード](../../../services/api-gateway.md#errors)

### 問11 {#q11}

データ API の呼び出し元に、次のエラーが返りました。対応として正しいものはどれですか。（2つ選択）

- A. 504 は統合のタイムアウトなので、処理を分割するか非同期にする
- B. 429 は認証の失敗なので、API キーを作り直して送る
- C. 429 は統合先の障害なので、別のリージョンへ切り替える
- D. 504 はリクエスト形式の誤りなので、JSON を直して送る
- E. 429 は呼び出しの制限なので、バックオフして再試行する

??? success "答えと解説"
    **正解: A, E**

    エラーコードから、どちらの側の問題かを判断します。

    - A: 正しい。バックエンドが間に合っていません。
    - B: 誤り。認証の失敗は 401 や 403 です。
    - C: 誤り。呼び出しの制限です。
    - D: 誤り。形式の誤りは 400 です。
    - E: 正しい。スロットリングです。

    **スキル:** [3.1.5](../domain3.md#skill-3-1-5) / **参照:** [エラーコード](../../../services/api-gateway.md#errors)、[ログとメトリクス](../../../services/api-gateway.md#logging-metrics)

### 問12 {#q12}

Step Functions から Redshift Data API の `ExecuteStatement` を呼び、`Retry` を設定します。再試行で同じ SQL を二重に実行しないために何を渡しますか。

- A. `ClientToken`
- B. `StatementName`
- C. `SecretArn`
- D. `WithEvent`

??? success "答えと解説"
    **正解: A**

    `ClientToken` は 8 時間有効です。

    - A: 正しい。
    - B: 誤り。文に付ける名前で、重複の防止には使いません。
    - C: 誤り。認証に使う値です。
    - D: 誤り。完了のイベントを送るかの指定です。

    **スキル:** [3.1.5](../domain3.md#skill-3-1-5) / **参照:** [Amazon Redshift](../../../services/data-engineering.md#redshift)、[エラー処理](../../../services/step-functions.md#error-handling)

### 問13 {#q13}

Redshift Data API を使うアプリが、前の日の `GetStatementResult` の結果を読もうとして失敗します。また同じ問い合わせの費用も下げたいです。正しい対応はどれですか。

- A. 結果は 24 時間で消えるので `ClientToken` で延長し、費用はステージ変数で切り替えて減らす
- B. 結果は 7 日間残るので呼び直しの権限だけを確認し、費用はリトライの回数を増やして下げる
- C. 結果は無期限に残るので Statement ID を確認し、費用はカナリアリリースの割合を下げて減らす
- D. 結果は 24 時間で消えるので必要なら S3 などに保存し、同じ問い合わせは API Gateway のキャッシュで減らす

??? success "答えと解説"
    **正解: D**

    結果の保持は 24 時間です。

    - A: 誤り。`ClientToken` は結果の保持を延ばしません。
    - B: 誤り。保持は 24 時間で、リトライは費用を下げません。
    - C: 誤り。保持は 24 時間で、カナリアは費用削減の機能ではありません。
    - D: 正しい。

    **スキル:** [3.1.5](../domain3.md#skill-3-1-5) / **参照:** [Amazon Redshift](../../../services/data-engineering.md#redshift)、[キャッシュ](../../../services/api-gateway.md#caching)

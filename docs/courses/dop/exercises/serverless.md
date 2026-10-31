# サーバーレスの問題集

対象の解説: [サーバーレス](../../../services/lambda.md)

### 問1 {#q1}

全 300 アカウントのセキュリティグループを調べて、許可しないルールを削除します。処理はアカウントごとにロールを引き受け、1 アカウント最大 5 分かかります。失敗したアカウントは別に記録して、残りは続けます。最適な設計はどれですか。

- A. 300 個の EventBridge ルールを作り、アカウントごとに別々の Lambda を動かす
- B. Step Functions の Standard の `Map` で関数を並行に呼び、`Retry` と `Catch` で失敗を記録する
- C. 1 つの Lambda のループで全アカウントを順に処理し、失敗は例外として全体を止める
- D. Express のワークフローで全アカウントを処理し、タイムアウトしたら最初からやり直す

??? success "答えと解説"
    **正解: B**

    `Map` で分散し、`Retry` と `Catch` で失敗を分けます。長い運用の工程には Standard が向きます。

    - A: 誤り。管理が増え、全体の失敗の集約もできない。
    - B: 正しい。
    - C: 誤り。15 分を超え、失敗で全体が止まる。
    - D: 誤り。Express は最大 5 分で、この規模に向かない。

    **スキル:** [Lambda と Step Functions](../domain2.md#t2-3-lambda) / **参照:** [Standard と Express](../../../services/step-functions.md#standard-express)、[エラー処理](../../../services/step-functions.md#error-handling)

### 問2 {#q2}

本番の設定を変える自動化で、変更の前に担当者の承認を最大 3 日待ちます。Lambda は再実行されても二重に変更しないようにします。どの設計が適切ですか。

- A. SQS の可視性タイムアウトを 3 日にして、承認の間はメッセージを隠しておく
- B. `Wait` 状態で 3 日間待ち、担当者が応答しなくても処理を進める
- C. Lambda を 3 日間実行し続け、ループの中でメールの返信を確認する
- D. `waitForTaskToken` で承認を待ち、更新の処理は冪等にする

??? success "答えと解説"
    **正解: D**

    `waitForTaskToken` はトークンが返るまで待機します。再試行に備えて処理を冪等にします。

    - A: 誤り。上限は 12 時間で、承認の仕組みにもならない。
    - B: 誤り。承認の結果を受けられない。
    - C: 誤り。Lambda の上限は 15 分。
    - D: 正しい。

    **スキル:** [Lambda と Step Functions](../domain2.md#t2-3-lambda) / **参照:** [人の承認](../../../services/step-functions.md#human-approval)、[冪等性](../../../services/sdk-resilience.md#idempotency)

### 問3 {#q3}

Lambda で複数のアカウントの API を大量に呼ぶ自動化が、`ThrottlingException` で失敗します。対象の API のクォータの引き上げはできません。同時に処理する数を制限しつつ、処理の完了を確実にします。適切な組み合わせはどれですか。（2つ選択）

- A. 関数の予約済み同時実行か `Map` の最大同時実行で並行数を制限する
- B. 例外を握りつぶして、関数を常に成功として終わらせる
- C. SDK の再試行とバックオフの設定を増やす
- D. Provisioned Concurrency で実行環境を増やす
- E. 関数のメモリを最大にして、呼び出しの速さを上げる

??? success "答えと解説"
    **正解: A, C**

    スロットリングには再試行と並行数の制限で対応します。

    - A: 正しい。
    - B: 誤り。処理が完了せず、失敗も見えなくなる。
    - C: 正しい。
    - D: 誤り。同時に呼ぶ数を増やす方向で、制限にならない。
    - E: 誤り。呼び出しが速くなるとスロットリングは悪化しやすい。

    **スキル:** [Lambda と Step Functions](../domain2.md#t2-3-lambda) / **参照:** [リトライ](../../../services/sdk-resilience.md#retries)、[同時実行とスケーリング](../../../services/lambda.md#concurrency)

### 問4 {#q4}

注文 API は同期で在庫システムを呼んでいます。在庫システムの更新は秒間 100 件が限界で、セールの時は注文が秒間 500 件になり、API がタイムアウトします。注文の受け付けは止めず、処理は遅れてもよいと決まりました。どう変えますか。

- A. SNS で在庫システムへ通知し、失敗したら利用者に再送を依頼する
- B. 在庫システムを呼ぶ API の Lambda の同時実行を 500 に増やす
- C. API Gateway のスロットリングを秒間 100 件にして、超えた注文を拒否する
- D. API と在庫システムの間に SQS を挟み、ワーカーのペースで処理する

??? success "答えと解説"
    **正解: D**

    キューを挟むと負荷を平準化でき、各層が別々にスケールします。

    - A: 誤り。SNS はキューではなく平準化にならない。
    - B: 誤り。在庫システムの限界は変わらず、タイムアウトが増える。
    - C: 誤り。注文の受け付けを止めることになり、条件に反する。
    - D: 正しい。

    **スキル:** [疎結合](../domain3.md#t3-2-loose-coupling) / **参照:** [密結合と疎結合](../../../services/messaging.md#coupling)、[SQS](../../../services/messaging.md#sqs)

### 問5 {#q5}

注文の完了イベントを、在庫、請求、通知の 3 つで処理します。将来の処理の追加でも注文サービスを変更せず、請求が止まっても他に影響しないようにします。処理の順序は問いません。どの構成が適切ですか。

- A. SNS のトピックから処理ごとの SQS キューへ配る
- B. Kinesis Data Streams の 1 つのシャードへ入れて、1 つのコンシューマーで順に処理する
- C. 注文サービスから 3 つの API を順に同期で呼ぶ
- D. 3 つの処理を 1 つの Lambda にまとめ、失敗したら全体を再実行する

??? success "答えと解説"
    **正解: A**

    ファンアウトなら、処理ごとにキューがあるので、止まっても他に影響しません。

    - A: 正しい。
    - B: 誤り。順序は不要で、処理も 1 か所に結合する。
    - C: 誤り。依存が強く、1 つの停止で全体が止まる。
    - D: 誤り。追加のたびに変更が必要で、失敗も波及する。

    **スキル:** [疎結合](../domain3.md#t3-2-loose-coupling) / **参照:** [選び方](../../../services/messaging.md#how-to-choose)、[疎結合と耐障害性](../../../services/resilience.md#loose-coupling)

### 問6 {#q6}

数千の IoT デバイスのイベントを順序を保って複数のアプリで読み、過去 24 時間分は読み直します。一方、保険の審査は複数の工程と人の判断を経ます。それぞれの適切なサービスはどれですか。

- A. イベントは DynamoDB、審査は SQS の FIFO キュー
- B. イベントは SQS の標準キュー、審査は SNS
- C. イベントは EventBridge のアーカイブとリプレイ、審査は Kinesis のコンシューマー
- D. イベントは Kinesis Data Streams、審査は Step Functions

??? success "答えと解説"
    **正解: D**

    順序のある大量のデータは Kinesis、工程の管理は Step Functions です。

    - A: 誤り。ストリームの読み直しに向かず、FIFO は工程を管理しない。
    - B: 誤り。順序と読み直しを保てず、SNS は工程を管理しない。
    - C: 誤り。大量の順序付きの読み取りに向かず、Kinesis は工程を管理しない。
    - D: 正しい。

    **スキル:** [疎結合](../domain3.md#t3-2-loose-coupling) / **参照:** [Standard と Express](../../../services/step-functions.md#standard-express)、[選び方](../../../services/messaging.md#how-to-choose)

### 問7 {#q7}

Java の Lambda の API で、コールドスタートの遅延が要件の 500 ms を超えています。午前の短いピーク以外は呼び出しが少なく、ピークの同時実行は予想できます。アプリのコードの変更は避けたいと考えています。また、同じアカウントの他の関数がバッチの実行で同時実行を奪うこともあります。適切な組み合わせはどれですか。（2つ選択）

- A. API の関数に予約済み同時実行を設定する
- B. 関数のタイムアウトを 15 分に延ばす
- C. SnapStart か Provisioned Concurrency で初期化の遅延を減らす
- D. 全関数の `/tmp` を 10 GB に増やす
- E. API Gateway の統合のタイムアウトを短くする

??? success "答えと解説"
    **正解: A, C**

    初期化の遅延には SnapStart か Provisioned Concurrency を使います。他の関数に奪われないよう、予約済み同時実行を設定します。

    - A: 正しい。
    - B: 誤り。遅延の短縮にならない。
    - C: 正しい。
    - D: 誤り。同時実行にもコールドスタートにも直接効かない。
    - E: 誤り。遅いリクエストがエラーになるだけ。

    **スキル:** [サーバーレス](../domain3.md#t3-2-serverless) / **参照:** [コールドスタートを減らす](../../../services/lambda.md#cold-start)、[同時実行とスケーリング](../../../services/lambda.md#concurrency)

### 問8 {#q8}

API Gateway の後ろの Lambda と RDS が、特定の取引先の大量のアクセスで過負荷になります。取引先ごとの上限を決めて超過は 429 を返し、同じ内容の読み取りは Lambda を呼ばずに返します。適切な組み合わせはどれですか。

- A. Lambda の予約済み同時実行と CloudFront の署名付き URL
- B. 使用量プランと API キー、API Gateway のキャッシュ
- C. WAF のマネージドルールとステージのカナリア
- D. リクエストの検証とオーソライザーのキャッシュ

??? success "答えと解説"
    **正解: B**

    使用量プランで取引先ごとの上限を決め、ステージのキャッシュで同じ読み取りを返します。

    - A: 誤り。取引先ごとの制限にならない。
    - B: 正しい。
    - C: 誤り。取引先ごとの上限の設定と応答のキャッシュにならない。
    - D: 誤り。オーソライザーのキャッシュは認可の結果の保存で、応答のキャッシュではない。

    **スキル:** [サーバーレス](../domain3.md#t3-2-serverless) / **参照:** [使用量プランとスロットリング](../../../services/api-gateway.md#usage-plans-throttling)、[キャッシュ](../../../services/api-gateway.md#caching)

### 問9 {#q9}

Lambda から RDS へ接続すると、ピークで `too many connections` になります。別の Fargate の API は負荷に応じてタスク数を増やす必要があります。適切な組み合わせはどれですか。

- A. Lambda のメモリを増やして、Fargate は手動で `desired count` を変更する
- B. RDS Proxy で接続をプールし、Fargate は Application Auto Scaling を使う
- C. 関数をコールドスタートのたびに切断するよう変更し、Fargate は Lambda へ移す
- D. ElastiCache にデータベースの接続を保存して、Fargate は EC2 Auto Scaling を使う

??? success "答えと解説"
    **正解: B**

    接続数の問題は RDS Proxy です。ECS のタスク数は Application Auto Scaling で増やします。

    - A: 誤り。接続数の問題は残り、自動にならない。
    - B: 正しい。
    - C: 誤り。接続の問題の解決にならず、移行の必要もない。
    - D: 誤り。接続を保存する仕組みではなく、Fargate のタスクは EC2 Auto Scaling の対象でもない。

    **スキル:** [サーバーレス](../domain3.md#t3-2-serverless) / **参照:** [RDS Proxy](../../../services/databases.md#rds-proxy)、[サービスの Auto Scaling](../../../services/containers.md#service-auto-scaling)

### 問10 {#q10}

API Gateway の同期の統合で、レポートの生成に 5 分かかる処理がタイムアウトします。利用者には受付の結果をすぐに返し、完了は後から確認させます。処理は Fargate や Lambda で実行できます。適切な設計はどれですか。

- A. CloudFront の前段でオリジンの応答の待ち時間を延ばし、全リクエストを同期のまま待たせる
- B. 受付を返して SQS か Step Functions へ渡し、状態の確認用の API を用意する
- C. 統合のタイムアウトの上限を超えられるよう、関数のタイムアウトを 15 分に延ばして同期のまま待たせる
- D. クライアントのブラウザからデータベースへ直接接続して、処理の完了を待たせる

??? success "答えと解説"
    **正解: B**

    統合のタイムアウトより長い処理は、同期で待たずにキューや Step Functions へ渡します。

    - A: 誤り。API Gateway の統合のタイムアウトの問題は残る。
    - B: 正しい。
    - C: 誤り。統合のタイムアウトは関数の設定で延びず、同期で待つ設計も残る。
    - D: 誤り。安全でなく、処理の設計にもならない。

    **スキル:** [サーバーレス](../domain3.md#t3-2-serverless) / **参照:** [同時実行とスケーリング](../../../services/lambda.md#concurrency)、[SQS](../../../services/messaging.md#sqs)

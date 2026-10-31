# Step Functions の問題集

対象の解説: [AWS Step Functions](../../../services/step-functions.md)

### 問1 {#q1}

`Task` 状態に次の `Retry` を設定しました。`IntervalSeconds: 2`、`MaxAttempts: 3`、`BackoffRate: 2`、`MaxDelaySeconds: 5`。すべての再試行が失敗する場合、再試行の待ち時間の合計は何秒ですか。

- A. 6 秒
- B. 11 秒
- C. 14 秒
- D. 15 秒

??? success "答えと解説"
    **正解: B**

    待ち時間は 2 秒、4 秒、8 秒と増えますが、`MaxDelaySeconds` で 3 回目は 5 秒に抑えられます。合計は 2 + 4 + 5 = 11 秒です。

    - A: 2 秒ずつ 3 回とした値で、倍率を反映していません。
    - B: 上限を反映した値です。
    - C: `MaxDelaySeconds` を無視した値です。
    - D: 上限の 5 秒が 3 回続くとした値です。

    **スキル:** C03 1.1.3 / **参照:** [Retry のフィールド](../../../services/step-functions.md#retry)

### 問2 {#q2}

開発者が `Retry` に `"ErrorEquals": ["States.TaskFailed"]` だけを書きました。他のフィールドは省略しています。このときの再試行の動きはどれですか。

- A. 再試行しない
- B. 1 秒間隔で 3 回再試行する
- C. 1 秒後、2 秒後、4 秒後の計 3 回再試行する
- D. 最初は 2 秒後で、次に 4 秒後、8 秒後の計 3 回再試行する

??? success "答えと解説"
    **正解: C**

    既定は `IntervalSeconds` 1、`MaxAttempts` 3、`BackoffRate` 2.0 です。

    - A: 再試行しないのは `MaxAttempts` を 0 にしたときです。
    - B: `BackoffRate` が 1 のときの動きです。
    - C: 既定値の動きです。
    - D: `IntervalSeconds` が 2 のときの動きです。

    **スキル:** C03 1.1.3 / **参照:** [Retry のフィールド](../../../services/step-functions.md#retry)

### 問3 {#q3}

`Catch` の配列に、`["States.ALL"]` の項目を先頭に、`["PaymentDeclined"]` の項目を 2 番目に書きました。適切な修正はどれですか。

- A. `States.ALL` の項目を配列の最後に移す
- B. `States.ALL` と `PaymentDeclined` を同じ項目にまとめる
- C. `PaymentDeclined` を `States.PaymentDeclined` に変更する
- D. `States.ALL` を `States.TaskFailed` に置き換える

??? success "答えと解説"
    **正解: A**

    `States.ALL` は `ErrorEquals` の中で単独で書き、配列の最後の項目にする必要があります。

    - A: 正しい書き方です。
    - B: `States.ALL` は他のエラー名と一緒に書けません。
    - C: `States.` で始まる名前は組み込み用で、独自のエラーには使えません。
    - D: 順序の問題が残り、タイムアウトも捕まらなくなります。

    **スキル:** C03 1.1.3 / **参照:** [主なエラー名](../../../services/step-functions.md#error-names)

### 問4 {#q4}

ある `Task` の `Catch` に `States.ALL` を設定しています。タスクの出力が 256 KiB を超えたとき、`Catch` に移らず実行が失敗しました。この失敗を捕まえるのに最も適切な修正はどれですか。

- A. `TimeoutSeconds` を増やす
- B. `BackoffRate` を増やす
- C. `Retry` の `MaxAttempts` を増やしてから `Catch` に移るようにする
- D. `States.DataLimitExceeded` を明示した項目を足す

??? success "答えと解説"
    **正解: D**

    `States.DataLimitExceeded` は `States.ALL` では捕まりませんが、名前を明示すれば捕まえられます。根本的な解決としては、大きなデータを S3 に置いて参照を渡します。

    - A: サイズの問題で、時間は関係ありません。
    - B: 再試行の間隔で、エラーの一致には関係ありません。
    - C: `Retry` も `States.ALL` では一致しないので、回数を増やしても解決しません。
    - D: 公式に説明されている方法です。

    **スキル:** C03 1.1.3 / **参照:** [主なエラー名](../../../services/step-functions.md#error-names)

### 問5 {#q5}

外部の処理を待つ `Task` に `TimeoutSeconds` を設定し、`Catch` に `States.TaskFailed` だけを書きました。時間切れのときに `Catch` に移りません。最も適切な修正はどれですか。

- A. `TimeoutSeconds` を削除する
- B. `HeartbeatSeconds` を `TimeoutSeconds` より大きくする
- C. `ErrorEquals` に `States.Timeout` を追加する
- D. `Catch` を `Retry` の前に書き換える

??? success "答えと解説"
    **正解: C**

    `States.TaskFailed` は `States.Timeout` 以外の既知のエラーに一致します。タイムアウトも捕まえるには名前を足します。

    - A: 時間切れがなくなるだけで、外部が応答しないと実行が止まり続けます。
    - B: `HeartbeatSeconds` は `TimeoutSeconds` より小さい値にします。
    - C: 正しい修正です。
    - D: JSON の順序は動きに関係しません。

    **スキル:** C03 1.1.3 / **参照:** [主なエラー名](../../../services/step-functions.md#error-names)

### 問6 {#q6}

JSONPath の `Task` で `Catch` に移ったとき、次の状態で元の入力の `orderId` とエラーの情報の両方を使いたいと考えています。どの設定が最も適切ですか。

- A. `Catch` に `"ResultPath": "$.error"` を指定する
- B. `Catch` に `"ResultPath": null` を指定する
- C. `Task` に `"OutputPath": "$.orderId"` を指定する
- D. `Catch` の `ResultPath` を省略する

??? success "答えと解説"
    **正解: A**

    `$.error` を指定すると、入力を残したままエラー情報を `error` に追加できます。

    - A: 入力とエラー情報の両方を次へ渡せます。
    - B: 入力は残りますが、エラー情報が失われます。
    - C: `Catch` の出力には `Task` の `OutputPath` が適用されません。
    - D: 省略は `$` と同じで、入力はエラー情報で置き換えられます。

    **スキル:** C03 1.1.3 / **参照:** [Catch](../../../services/step-functions.md#catch)

### 問7 {#q7}

JSONPath の `Task` で、タスクの結果を使わず、状態の入力をそのまま次の状態に渡したいと考えています。最も適切な設定はどれですか。

- A. `"ResultPath": "$.result"`
- B. `"ResultPath": null`
- C. `"OutputPath": null`
- D. `"InputPath": null`

??? success "答えと解説"
    **正解: B**

    `ResultPath` を `null` にすると結果を捨て、入力をそのまま出力します。

    - A: 結果を入力の `result` に追加して出力します。
    - B: 目的の動きです。
    - C: 出力が空の JSON になります。
    - D: タスクへの入力が空の JSON になります。

    **スキル:** C03 1.1.7 / **参照:** [JSONPath の入出力処理](../../../services/step-functions.md#io-jsonpath)

### 問8 {#q8}

`.waitForTaskToken` で SQS にジョブを送り、外部のワーカーからの応答を待つ `Task` を設計しています。ワーカーが落ちたときに実行が止まり続けないようにするには、どの設定をしますか。（2つ選択）

- A. `TimeoutSeconds` を設定する
- B. `HeartbeatSeconds` を設定し、ワーカーに `SendTaskHeartbeat` を呼ばせる
- C. `Retry` の `MaxAttempts` を 0 にする
- D. ステートマシンを Express に変更する
- E. `Resource` の末尾を `.sync` に変更する

??? success "答えと解説"
    **正解: A, B**

    `.waitForTaskToken` には既定のタイムアウトがなく、実行の上限まで待つことがあります。`TimeoutSeconds` で全体の上限を決め、`HeartbeatSeconds` で生存確認をします。

    - A: 応答がないときに `States.Timeout` になります。
    - B: 途絶を早く検知できます。
    - C: 再試行の回数で、待ち時間は制限できません。
    - D: Express はコールバックに対応していません。
    - E: SQS は `.sync` に対応していません。

    **スキル:** C03 1.1.3 / **参照:** [タイムアウトとハートビート](../../../services/step-functions.md#timeouts)

### 問9 {#q9}

JSONPath の `Task` を JSONata に変更します。`Parameters` でタスクの入力を組み立て、`ResultSelector` と `OutputPath` で出力を整えていました。JSONata での正しい書き方はどれですか。

- A. `Arguments` と `Output` を使い、式を `{% %}` で囲む
- B. `Parameters` と `OutputPath` を残し、キーに `.$` を付ける
- C. `InputPath` と `Output` を使い、式を `$$` で始める
- D. `Arguments` と `ResultPath` を使い、式を `${ }` で囲む

??? success "答えと解説"
    **正解: A**

    JSONata では 5 つの JSONPath のフィールドが `Arguments` と `Output` に置き換わります。式は `{% %}` で囲み、キーに `.$` は付けません。

    - A: JSONata の書き方です。
    - B: JSONPath の書き方です。
    - C: `InputPath` は JSONPath のフィールドで、`$$` はコンテキストオブジェクトの書き方です。
    - D: `ResultPath` は JSONPath のフィールドで、`${ }` は式の書き方ではありません。

    **スキル:** C03 1.1.7 / **参照:** [JSONata](../../../services/step-functions.md#jsonata)

### 問10 {#q10}

JSONata の状態で `Assign` に `{"total": "{% $states.result.Payload.total %}"}` を書き、同じ状態の `Output` で `$total` を使いました。期待した値が出力されません。最も適切な説明はどれですか。

- A. 変数の名前に `.$` が付いていない
- B. `Assign` は `Task` の状態では使えない
- C. 変数のサイズの上限が 1 KB である
- D. 同じ状態の `Output` からは読めない

??? success "答えと解説"
    **正解: D**

    `Assign` と `Output` は並行して評価されます。同じ状態の `Output` では、同じ式を書き直します。新しい値は次の状態から読めます。

    - A: JSONata では `.$` を使いません。
    - B: `Task` でも使えます。
    - C: 変数の上限は 256 KiB です。
    - D: 公式に説明されている動きです。

    **スキル:** C03 1.1.7 / **参照:** [変数](../../../services/step-functions.md#variables)

### 問11 {#q11}

S3 にある数百万行の CSV を、行ごとに処理します。同時実行は 500 にしたいと考えています。最も適切な構成はどれですか。

- A. Inline の `Map` で `MaxConcurrency` を 500 にする
- B. `Parallel` に 500 のブランチを定義する
- C. Distributed の `Map` と `ItemReader` を使う
- D. Express のステートマシンで Inline の `Map` を使う

??? success "答えと解説"
    **正解: C**

    Distributed の `Map` は S3 のデータを `ItemReader` で読み、子実行で最大 10,000 まで並列に処理できます。

    - A: Inline は同時 40 までで、入力は JSON の配列のみです。
    - B: `Parallel` は固定のブランチ用で、データの件数に合わせられません。
    - C: この規模のための機能で、`MaxConcurrency` を 500 にします。
    - D: Inline の制限は同じで、Express は 5 分で終わる必要があります。

    **スキル:** C03 1.1.6 / **参照:** [Map の設定](../../../services/step-functions.md#map-settings)

### 問12 {#q12}

配列の各要素で外部 API を呼ぶ `Map` があります。API は同時に多くのリクエストを受けられないので、順番に 1 件ずつ呼びたいと考えています。`MaxConcurrency` はどの値にしますか。

- A. 0
- B. 1
- C. 40
- D. 省略する

??? success "答えと解説"
    **正解: B**

    `MaxConcurrency` が 1 なら、入力の順に 1 件ずつ処理します。

    - A: 0 は制限なしです。
    - B: 順番に 1 件ずつ処理します。
    - C: 同時に 40 件を処理できる値です。
    - D: 省略すると既定の 0 と同じです。

    **スキル:** C03 4.3.1 / **参照:** [Map の設定](../../../services/step-functions.md#map-settings)

### 問13 {#q13}

Distributed の `Map` で 100 万件を処理しています。一部の不良データでは止めず、失敗が全体の 5% を超えたら止めたいと考えています。最も適切な設定はどれですか。

- A. `Retry` の `MaxAttempts` を 5 にする
- B. `MaxConcurrency` を 5 にする
- C. `ItemBatcher` の `MaxItemsPerBatch` を 5 にする
- D. `ToleratedFailurePercentage` を 5 にする

??? success "答えと解説"
    **正解: D**

    失敗の割合が値を超えると、Map は `States.ExceedToleratedFailureThreshold` で失敗します。

    - A: 再試行の回数で、割合の判定はできません。
    - B: 同時に処理する数の上限です。
    - C: 1 回の子実行にまとめる要素の数です。
    - D: 失敗の許容率を決める設定です。

    **スキル:** C03 1.1.3 / **参照:** [Map の設定](../../../services/step-functions.md#map-settings)

### 問14 {#q14}

`Parallel` の 2 つのブランチで Lambda 関数を呼んでいます。ブランチ A が `Catch` のないエラーで失敗したときの動きとして正しいものはどれですか。（2つ選択）

- A. `Parallel` 全体が失敗する
- B. 既に動いているブランチ B の Lambda 関数は途中で止まらず最後まで動く
- C. ブランチ B は完了するまで次の状態に進まず、その結果が次の状態に渡される
- D. ブランチ B の Lambda 関数は Step Functions が強制的に終了する
- E. ブランチ A の失敗は無視され、ブランチ B の結果だけが次の状態に渡される

??? success "答えと解説"
    **正解: A, B**

    どれかのブランチが失敗すると、`Parallel` 全体が失敗してブランチは止まります。ただし、既に呼んだ Lambda 関数は実行を続けます。

    - A: 公式に説明されている動きです。
    - B: Lambda 関数そのものは止まりません。後続の処理は重複に備えます。
    - C: ブランチは止まり、結果は渡されません。
    - D: Step Functions は Lambda を強制終了しません。
    - E: 失敗は無視されません。

    **スキル:** C03 1.1.3 / **参照:** [Parallel の設定](../../../services/step-functions.md#parallel-settings)

### 問15 {#q15}

ある会社は、短時間で大量に発生するイベントの処理を非同期の Express ワークフローに移行します。移行で注意すべき点として正しいものはどれですか。（2つ選択）

- A. 少なくとも 1 回の実行なので、処理を冪等にする
- B. `.waitForTaskToken` は使えないので、Request Response で設計する
- C. 実行履歴は `GetExecutionHistory` で 90 日間取得できる
- D. 実行は最大 1 年まで続けられる
- E. 失敗した実行は redrive で 14 日以内に再開できる

??? success "答えと解説"
    **正解: A, B**

    非同期 Express は少なくとも 1 回の実行で、同じイベントが複数回動くことがあります。統合パターンは Request Response のみです。

    - A: 公式の実行の保証に沿った注意点です。
    - B: Express は `.sync` と `.waitForTaskToken` に対応しません。
    - C: Standard の機能です。Express は CloudWatch Logs で確認します。
    - D: Express の上限は 5 分です。
    - E: redrive は Standard の機能です。

    **スキル:** C03 1.1.2 / **参照:** [Standard と Express](../../../services/step-functions.md#standard-express)

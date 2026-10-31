# 分野1: Step Functions

分野1では、ワークフローの種類の選択、`Retry` と `Catch` による耐障害性、状態の間のデータの受け渡しを問われます。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [1.1.1](../../domain1.md#skill-1-1-1) | オーケストレーションによる連携 |
| [1.1.2](../../domain1.md#skill-1-1-2) | 同期と非同期の起動、ワークフローの種類 |
| [1.1.3](../../domain1.md#skill-1-1-3) | 再試行、エラー処理、タイムアウト |
| [1.1.6](../../domain1.md#skill-1-1-6) | S3 の大量データの処理 |
| [1.1.7](../../domain1.md#skill-1-1-7) | 入出力の処理 |

## 学習の順番 {#study-order}

1. [オーケストレーションとコレオグラフィー](../../../../services/step-functions.md#orchestration-choreography): EventBridge での連携との違いを比べます。
2. [Standard と Express](../../../../services/step-functions.md#standard-express): 実行時間と実行の保証、使える統合パターンの違いを覚えます。
3. [状態の種類](../../../../services/step-functions.md#state-types): `Task`、`Choice`、`Map`、`Parallel` の役割を区別します。
4. [JSONPath の入出力処理](../../../../services/step-functions.md#io-jsonpath): 5 つのフィールドが働く順番と `ResultPath` の値を覚えます。
5. [JSONata](../../../../services/step-functions.md#jsonata)、[変数](../../../../services/step-functions.md#variables): `Arguments` と `Output` への置き換えを確認します。
6. [Retry のフィールド](../../../../services/step-functions.md#retry)、[Catch](../../../../services/step-functions.md#catch)、[主なエラー名](../../../../services/step-functions.md#error-names): 待ち時間の計算と、何が捕まるかを押さえます。
7. [タイムアウトとハートビート](../../../../services/step-functions.md#timeouts)、[コールバック](../../../../services/step-functions.md#wait-for-callback): 待ち続けないための設定を学びます。
8. [Map の設定](../../../../services/step-functions.md#map-settings): Inline と Distributed の使い分けと、失敗の許容を確認します。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| 最大実行時間 | Standard 1 年、Express 5 分 | 種類は作成後に変えられません |
| 入出力の上限 | 256 KiB | 超えるなら S3 に置いて参照を渡します |
| `IntervalSeconds`、`MaxAttempts`、`BackoffRate` | 既定 1、3、2.0 | 既定なら 1 秒、2 秒、4 秒待ちます |
| `JitterStrategy` | 既定 `NONE` | 同時の再試行を散らすなら `FULL` です |
| HTTP タスク | 60 秒 | `TimeoutSeconds` に関係なく上限です |
| Inline Map | 同時 40 | 超えるなら Distributed です |
| Distributed Map | 子実行 10,000 | |
| 実行履歴 | 25,000 イベント、終了後 90 日 | |
| redrive | 14 日以内（Standard） | 失敗した状態から再開します |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 人の承認を含む、長時間の業務 | Standard で `.waitForTaskToken` を使い、`SendTaskSuccess` で再開します |
| 大量で短い、冪等な処理 | Express にします |
| 冪等でない処理を正確に1回動かす | Standard にします |
| `IntervalSeconds: 2`、`MaxAttempts: 3`、`BackoffRate: 2`、`MaxDelaySeconds: 5` の待ち時間 | 2 秒、4 秒、5 秒で、合計 11 秒です |
| 失敗時に元の入力とエラー情報の両方を次へ渡す | `Catch` に `"ResultPath": "$.error"` を指定します |
| タスクの結果を捨てて入力をそのまま渡す | `ResultPath: null` にします |
| 外部の処理の生存を確認する | `HeartbeatSeconds` と `SendTaskHeartbeat` を使います |
| S3 の数百万行の CSV を行ごとに処理する | Distributed の `Map` で `ItemReader` と `MaxConcurrency` を設定します |
| 不良データでは止めず、失敗が 5% を超えたら止める | `ToleratedFailurePercentage: 5` にします |

## 引っかかりやすい点 {#traps}

- `Catch` が `States.TaskFailed` だけだとタイムアウトを捕まえられません。`States.Timeout` も書きます。
- `States.ALL` では `States.DataLimitExceeded` を捕まえられません。名前を明示します。`States.Runtime` は再試行もキャッチもできません。
- `States.ALL` は単独で最後の項目に書きます。
- `.sync` と `.waitForTaskToken` は既定のタイムアウトがなく、最大 1 年止まることがあります。`TimeoutSeconds` を必ず設定します。
- Express は Request Response しか使えません。コールバックが必要なら Standard で作り直します。
- `"id": "$.id"` は文字列のまま渡ります。パスを値にするキーは `id.$` のように `.$` で終えます。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [step-functions 問1](../../exercises/step-functions.md#q1) | 1.1.3 | Task 状態に次の Retry を設定しました。IntervalSeconds: 2、MaxAtt… |
| [step-functions 問2](../../exercises/step-functions.md#q2) | 1.1.3 | 開発者が Retry に "ErrorEquals": ["States.TaskFailed"] … |
| [step-functions 問3](../../exercises/step-functions.md#q3) | 1.1.3 | Catch の配列に、["States.ALL"] の項目を先頭に、["PaymentDecline… |
| [step-functions 問4](../../exercises/step-functions.md#q4) | 1.1.3 | ある Task の Catch に States.ALL を設定しています。タスクの出力が 256 … |
| [step-functions 問5](../../exercises/step-functions.md#q5) | 1.1.3 | 外部の処理を待つ Task に TimeoutSeconds を設定し、Catch に States… |
| [step-functions 問6](../../exercises/step-functions.md#q6) | 1.1.3 | JSONPath の Task で Catch に移ったとき、次の状態で元の入力の orderId … |
| [step-functions 問7](../../exercises/step-functions.md#q7) | 1.1.7 | JSONPath の Task で、タスクの結果を使わず、状態の入力をそのまま次の状態に渡したいと考… |
| [step-functions 問8](../../exercises/step-functions.md#q8) | 1.1.3 | .waitForTaskToken で SQS にジョブを送り、外部のワーカーからの応答を待つ Ta… |
| [step-functions 問9](../../exercises/step-functions.md#q9) | 1.1.7 | JSONPath の Task を JSONata に変更します。Parameters でタスクの入… |
| [step-functions 問10](../../exercises/step-functions.md#q10) | 1.1.7 | JSONata の状態で Assign に {"total": "{% $states.result… |
| [step-functions 問11](../../exercises/step-functions.md#q11) | 1.1.6 | S3 にある数百万行の CSV を、行ごとに処理します。同時実行は 500 にしたいと考えています。… |
| [step-functions 問13](../../exercises/step-functions.md#q13) | 1.1.3 | Distributed の Map で 100 万件を処理しています。一部の不良データでは止めず、失… |
| [step-functions 問14](../../exercises/step-functions.md#q14) | 1.1.3 | Parallel の 2 つのブランチで Lambda 関数を呼んでいます。ブランチ A が Cat… |
| [step-functions 問15](../../exercises/step-functions.md#q15) | 1.1.2 | ある会社は、短時間で大量に発生するイベントの処理を非同期の Express ワークフローに移行します… |

<!-- questions:end -->

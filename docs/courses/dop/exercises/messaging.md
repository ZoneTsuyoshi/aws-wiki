# イベントとメッセージングの問題集

対象の解説: [イベントとメッセージング](../../../services/messaging.md#how-to-choose)

### 問1 {#q1}

S3 に PDF が届いたときの処理です。条件は、(1) オブジェクトのサイズが 1 MB より大きいものだけ、(2) 3 つの別のターゲットへ送る、(3) 将来の再処理のために、イベントを再生できる、の 3 つです。適切な構成はどれですか。

- A. S3 のイベント通知を 3 個作り、同じ条件で 3 つの関数を指定する
- B. S3 のイベント通知にサフィックス `.pdf` だけを指定して、Lambda へ送る
- C. S3 のイベント通知を SNS へ送り、購読のフィルターで 1 MB より大きいものに絞る
- D. EventBridge を有効にして、ルールのパターンとアーカイブを使う

??? success "答えと解説"
    **正解: D**

    内容のパターン、複数のターゲット、再生が必要なら EventBridge です。

    - A: 誤り。同じ条件の重複は指定できない。
    - B: 誤り。サイズの条件と複数の宛先、再生の条件を満たせない。
    - C: 誤り。S3 のイベント通知にサイズの条件はなく、SNS の標準トピックではイベントを再生できない。
    - D: 正しい。

    **スキル:** [イベントパターン](../domain4.md#t4-3-event-patterns) / **参照:** [S3 イベント通知](../../../services/messaging.md#s3-events)、[Event Notifications](../../../services/s3.md#event-notifications)

### 問2 {#q2}

EC2 の状態の変化イベントで Lambda を動かし、Lambda の中で SNS へ通知しています。単純な通知の文に Lambda を書く必要がなくなるように見直します。また、過去のイベントでバグの修正後に再処理できるようにします。適切な組み合わせはどれですか。（2つ選択）

- A. ルールのターゲットに Step Functions を置き、SNS へ発行する `Task` を 1 つだけ実行する
- B. EventBridge のターゲットを直接 SNS にして、入力トランスフォーマーで文を整える
- C. ルールのターゲットを CloudWatch Logs にして、後で Logs Insights の結果から再処理する
- D. CloudTrail の全イベントを Athena で毎日検索して、結果を通知する
- E. イベントバスのアーカイブとリプレイを使う

??? success "答えと解説"
    **正解: B, E**

    EventBridge はターゲットに SNS を直接指定できます。アーカイブとリプレイで再処理できます。

    - A: 誤り。動くが部品が増え、文を整えるだけの要件に過剰で、再処理にもならない。
    - B: 正しい。
    - C: 誤り。ログに残るだけで、ルールへイベントを再生できない。
    - D: 誤り。遅く、イベント駆動にならない。
    - E: 正しい。

    **スキル:** [イベントパターン](../domain4.md#t4-3-event-patterns) / **参照:** [EventBridge](../../../services/messaging.md#eventbridge)、[アーカイブとリプレイ](../../../services/messaging.md#archive-replay)

### 問3 {#q3}

画像のアップロードの完了を、サムネイル、タグ付け、監査の 3 つのチームが非同期に処理します。S3 のイベント通知を 1 つだけ使い、チームの追加で通知の設定を変えないようにします。あるチームの障害が他へ影響しないようにします。適切な構成はどれですか。

- A. S3 の通知を 1 つの SNS トピックへ送り、チームごとの SQS キューで購読する
- B. S3 の通知を 1 つの SQS キューへ送り、3 チームのワーカーで共有する
- C. S3 の通知を 1 つの Lambda へ送り、その中で 3 チームの API を順に呼ぶ
- D. チームごとにプレフィックスを分けてイベント通知を 3 つ作り、各チームの関数へ送る

??? success "答えと解説"
    **正解: A**

    通知を SNS へ送り、チームごとのキューへファンアウトします。

    - A: 正しい。
    - B: 誤り。1 件のメッセージを 1 つのワーカーだけが処理し、3 チームへ届かない。
    - C: 誤り。依存が強く、障害が波及する。
    - D: 誤り。通知を 1 つにする条件に反し、チームの追加のたびに設定が変わる。

    **スキル:** [イベントパターン](../domain4.md#t4-3-event-patterns) / **参照:** [ファンアウト](../../../services/messaging.md#fanout)、[S3 イベント通知](../../../services/messaging.md#s3-events)

### 問4 {#q4}

組織には 40 本の CodePipeline があり、成功の通知が多すぎてチームが読まなくなりました。実行全体が失敗したときだけ通知します。追加のコードは書きません。適切なイベントパターンはどれですか。

- A. `source` が `aws.codepipeline`、`detail-type` が `CodePipeline Pipeline Execution State Change`、`detail.state` が `FAILED`
- B. `source` が `aws.cloudtrail`、`detail-type` が `FAILED`、`detail.state` が `CodePipeline`
- C. `source` が `aws.codepipeline`、`detail-type` は省略、`detail.state` は省略
- D. `source` が `aws.sns`、`detail-type` が `Notification`、`detail.pipeline` が `FAILED`

??? success "答えと解説"
    **正解: A**

    `source`、`detail-type`、`detail` の値で絞ります。

    - A: 正しい。
    - B: 誤り。項目の値の使い方が誤っている。
    - C: 誤り。すべてのイベントが通知される。
    - D: 誤り。パイプラインのイベントの形式ではない。

    **スキル:** [EventBridge](../domain4.md#t4-3-eventbridge) / **参照:** [ルールとイベントパターン](../../../services/messaging.md#eventbridge-rules)

### 問5 {#q5}

EventBridge のルールは一致しており、CloudWatch の `Invocations` も増えますが、SNS のメールが届きません。`FailedInvocations` が増えています。メールは読みやすい形にします。適切な修正の組み合わせはどれですか。（2つ選択）

- A. SNS のアクセスポリシーで、`events.amazonaws.com` からの発行を許可する
- B. ルールのイベントバスをカスタムのバスへ変更する
- C. 入力トランスフォーマーで通知の文を整える
- D. SNS のトピックを FIFO に変更する
- E. `aws.sns` のイベントパターンを追加する

??? success "答えと解説"
    **正解: A, C**

    SNS のターゲットには、EventBridge からの発行を許可するアクセスポリシーが必要です。

    - A: 正しい。
    - B: 誤り。権限の問題で、バスを変えても解決しない。
    - C: 正しい。
    - D: 誤り。権限の問題を解決せず、メールの購読にも使えない。
    - E: 誤り。パターンは一致している。

    **スキル:** [EventBridge](../domain4.md#t4-3-eventbridge) / **参照:** [入力トランスフォーマー](../../../services/messaging.md#input-transformer)、[トピックのアクセスポリシーと暗号化](../../../services/messaging.md#sns-access)

### 問6 {#q6}

デプロイの結果をチャットの Lambda へ送るルールがあります。関数のリソースベースポリシーの更新の誤りで呼び出しが拒否されていた間のイベントが失われました。CodeDeploy の失敗のイベントだけを送り、届かなかったものを後で調べられるようにします。適切な設定はどれですか。

- A. ルールのパターンを `aws.codedeploy` に絞り、ターゲットの再試行の回数を最大にする
- B. ターゲットの再試行ポリシーと DLQ を設定し、`aws.codedeploy` の状態の変化を絞る
- C. CloudTrail のイベント履歴を障害の後に手で読み直し、失われた分のイベントを再投入する
- D. 関数の非同期呼び出しのデスティネーションを設定し、`aws.codedeploy` の状態の変化を絞る

??? success "答えと解説"
    **正解: B**

    EventBridge のターゲットには再試行ポリシーと DLQ を設定できます。

    - A: 誤り。再試行が尽きたイベントの受け皿がなく、後で調べられない。
    - B: 正しい。
    - C: 誤り。手間がかかり、配信の設計にならない。
    - D: 誤り。関数が受け付けた後の失敗の受け皿で、呼び出しが拒否されたイベントは届かない。

    **スキル:** [EventBridge](../domain4.md#t4-3-eventbridge) / **参照:** [ターゲットの再試行と DLQ](../../../services/messaging.md#target-retry-dlq)、[デプロイが完了したとき](../../../services/observability.md#deployment-alerts)

### 問7 {#q7}

組織の全アカウントの AWS Health のイベントを一か所に集めて担当へ通知します。アカウントごとにルールを作るのは避けます。サポートプランの制限により AWS Health API は使えません。どの構成が適切ですか。

- A. 組織ビューと委任管理者で、組織のイベントを委任管理者の EventBridge で受ける
- B. 各アカウントの既定のイベントバスにルールを作り、それぞれの SNS へ通知する
- C. 各アカウントの既定のバスに、Health のイベントを中央のバスへ転送するルールを作る
- D. `DescribeEvents` を 5 分ごとに呼ぶ Lambda を各アカウントに置く

??? success "答えと解説"
    **正解: A**

    組織ビューと委任管理者で集約します。EventBridge での受信にサポートプランの条件はありません。

    - A: 正しい。
    - B: 誤り。アカウントごとのルールを避けるという条件に反する。
    - C: 誤り。動くが、アカウントごとのルールを避けるという条件に反する。
    - D: 誤り。AWS Health API が前提で、条件に合わない。

    **スキル:** [イベントソース](../domain5.md#t5-1-event-sources) / **参照:** [AWS Health イベントの自動化](../../../services/operations.md#health-events)、[AWS Health Dashboard](../../../services/cloud-foundations.md#health)

### 問8 {#q8}

本番の VPC で `ModifyVpcAttribute` が呼ばれたら通知します。また、読み取り専用の `DescribeInstances` の異常な呼び出しもルールで受けようとしましたが、一致しません。原因と対応はどれですか。（2つ選択）

- A. 読み取り専用の API は CloudTrail Insights を有効にすれば、既定のルールで受けられる
- B. 読み取り専用の管理イベントは `ENABLED_WITH_ALL_CLOUDTRAIL_MANAGEMENT_EVENTS` のルールで受ける
- C. CloudTrail のデータイベントを全 S3 バケットで有効にすれば、`DescribeInstances` が受けられる
- D. CloudTrail 経由のイベントには有効な証跡が必要で、既定のイベントバスに届く
- E. カスタムのイベントバスにルールを作れば、CloudTrail のイベントが直接届く

??? success "答えと解説"
    **正解: B, D**

    CloudTrail のイベントは既定のバスに届きます。読み取り専用のイベントは既定のルールでは一致しません。

    - A: 誤り。Insights は呼び出しの量の異常の検知で、ルールの一致の条件を変えない。
    - B: 正しい。
    - C: 誤り。データイベントの設定で、管理イベントを受ける条件ではない。
    - D: 正しい。
    - E: 誤り。CloudTrail 経由のイベントは既定のバスに届く。

    **スキル:** [イベントソース](../domain5.md#t5-1-event-sources) / **参照:** [ルールとイベントパターン](../../../services/messaging.md#eventbridge-rules)

### 問9 {#q9}

全アカウントの GuardDuty と AWS Config のイベントを、セキュリティアカウントの 1 つのイベントバスへ集めて処理します。さらに `AWS_EC2_INSTANCE_RETIREMENT_SCHEDULED` のイベントで、インスタンスを別のホストへ移す Automation を動かします。適切な構成はどれですか。

- A. GuardDuty と Config の集約のイベントを委任管理者で受け、Health のルールのターゲットに Automation を指定する
- B. 全アカウントの Lambda からセキュリティアカウントの SNS を呼び、Automation は担当者が実行する
- C. 既定のバスのルールから中央のバスへ転送し、Health のルールのターゲットに Automation を指定する
- D. セキュリティアカウントのルールで他のアカウントのイベントを直接読み取り、Health は Personal Health Dashboard で見る

??? success "答えと解説"
    **正解: C**

    複数のアカウントのイベントは、既定のバスのルールから中央のイベントバスへ転送します。

    - A: 誤り。Config のアグリゲーターは評価の集約で、各アカウントのイベントを中央のバスへ届けない。
    - B: 誤り。自作の処理が増え、自動にならない。
    - C: 正しい。
    - D: 誤り。ルールは他のアカウントのイベントを直接受けない。

    **スキル:** [イベントソース](../domain5.md#t5-1-event-sources) / **参照:** [イベントバス](../../../services/messaging.md#event-buses)、[AWS Health イベントの自動化](../../../services/operations.md#health-events)

### 問10 {#q10}

EC サイトの注文のイベントを在庫、請求、通知の 3 つのチームが処理します。請求のシステムは月に一度、数時間止まります。その間も他を止めず、請求の分は復旧後に処理します。順序は問いません。どの形が適切ですか。

- A. 3 つの API を Lambda から順に同期で呼ぶ
- B. SNS と処理ごとの SQS のファンアウト
- C. Kinesis のストリームを 1 つのコンシューマーで順に読む
- D. 1 つの SQS の標準キューを 3 つのワーカーで共有する

??? success "答えと解説"
    **正解: B**

    処理ごとにキューがあれば、止まってもメッセージはキューに残ります。

    - A: 誤り。1 つの停止が他へ波及する。
    - B: 正しい。
    - C: 誤り。処理が結合し、1 つの停止で全体が遅れる。
    - D: 誤り。1 件を 1 つのワーカーしか処理しない。

    **スキル:** [アーキテクチャ](../domain5.md#t5-1-architectures) / **参照:** [ファンアウト](../../../services/messaging.md#fanout)

### 問11 {#q11}

次の 2 つの処理のパターンを選びます。(1) クリックのログを順序どおりに複数のアプリが読み、過去のデータを再読み取りする。(2) 夜間の PDF の生成を、ワーカーのペースで取り出す。適切な組み合わせはどれですか。

- A. (1) SQS、(2) SNS
- B. (1) EventBridge のスケジュール、(2) Step Functions の Express
- C. (1) Kinesis Data Streams、(2) SQS
- D. (1) SNS、(2) Kinesis Data Streams

??? success "答えと解説"
    **正解: C**

    イベントストリーミングは順序と再読み取り、キューイングは処理側のペースが特徴です。

    - A: 誤り。SQS は読み終えたメッセージを再読み取りできず、SNS はキューではない。
    - B: 誤り。どちらもこの処理の基本のパターンではない。
    - C: 正しい。
    - D: 誤り。順序と再読み取り、ペースの制御が入れ違っている。

    **スキル:** [アーキテクチャ](../domain5.md#t5-1-architectures) / **参照:** [Kinesis Data Streams](../../../services/streaming.md#kinesis-data-streams)、[SQS](../../../services/messaging.md#sqs)

### 問12 {#q12}

SaaS からのイベントと AWS のサービスのイベントを同じ仕組みで受け、内容のパターンで振り分け、スキーマも共有します。1 秒あたりのイベントは少なく、順序は不要です。何を中心に使いますか。

- A. EventBridge のイベントバスとルール、スキーマレジストリ
- B. Kinesis Data Streams のシャードを増やし、コンシューマーで内容を分岐する
- C. SQS の FIFO キューを SaaS ごとに作る
- D. S3 のイベント通知で全イベントを受ける

??? success "答えと解説"
    **正解: A**

    内容のパターンと複数のターゲット、スキーマの共有は EventBridge の特徴です。

    - A: 正しい。
    - B: 誤り。順序と大量の処理の仕組みで、この要件には過剰。
    - C: 誤り。内容のパターンでの振り分けができない。
    - D: 誤り。S3 のイベントに限られる。

    **スキル:** [アーキテクチャ](../domain5.md#t5-1-architectures) / **参照:** [選び方](../../../services/messaging.md#how-to-choose)、[EventBridge](../../../services/messaging.md#eventbridge)

### 問13 {#q13}

SQS と Lambda のバッチ処理で、1 件の失敗でバッチ全体が再処理され、処理の重複が増えています。また、関数のタイムアウトは 60 秒で、可視性タイムアウトは 60 秒です。適切な修正の組み合わせはどれですか。（2つ選択）

- A. 部分バッチレスポンスで、失敗したメッセージだけを返す
- B. バッチサイズを 1 にして、スループットの低下を許容して全件を別々に処理する
- C. 関数の中で失敗を握りつぶし、バッチ全体を成功として返す
- D. 可視性タイムアウトを関数のタイムアウトの 6 倍以上にする
- E. 関数のタイムアウトを可視性タイムアウトより長くする

??? success "答えと解説"
    **正解: A, D**

    部分バッチレスポンスで失敗分だけを再処理します。可視性タイムアウトは関数のタイムアウトの 6 倍以上にします。

    - A: 正しい。
    - B: 誤り。動くが、部分バッチレスポンスで足りる場面で効率を落とす。
    - C: 誤り。失敗したメッセージが消え、再処理されない。
    - D: 正しい。
    - E: 誤り。処理中のメッセージが再度見えるようになり、重複が増える。

    **スキル:** [ワークフロー](../domain5.md#t5-1-workflows) / **参照:** [部分バッチレスポンス](../../../services/lambda.md#partial-batch-response)、[Lambda から使うときの設定](../../../services/messaging.md#sqs-lambda-settings)

### 問14 {#q14}

イベント処理の失敗の受け皿を設計します。(1) EventBridge から Lambda への非同期呼び出しが届かないとき。(2) Lambda の中で例外が起きたときに、結果の内容を別のキューへ送る。それぞれの設定の組み合わせはどれですか。

- A. (1) Lambda のデスティネーション、(2) EventBridge の DLQ
- B. (1) イベントソースマッピングの `BisectBatchOnFunctionError`、(2) Step Functions の `Catch`
- C. (1) SQS のリドライブポリシー、(2) ステージ条件
- D. (1) ターゲットの再試行ポリシーと DLQ、(2) Lambda のデスティネーション

??? success "答えと解説"
    **正解: D**

    配信の失敗はターゲットの DLQ、関数の失敗は非同期呼び出しのデスティネーションで受けます。

    - A: 誤り。配置が逆で、届かないときに関数のデスティネーションは動かない。
    - B: 誤り。ストリームと Step Functions の設定で、この経路の設定ではない。
    - C: 誤り。SQS を経由しない経路で、ステージ条件も無関係。
    - D: 正しい。

    **スキル:** [ワークフロー](../domain5.md#t5-1-workflows) / **参照:** [ターゲットの再試行と DLQ](../../../services/messaging.md#target-retry-dlq)、[デスティネーションと DLQ](../../../services/lambda.md#destinations-dlq)

### 問15 {#q15}

Kinesis を読む Lambda で 1 件の不正なレコードのためにシャードの処理が止まっています。一方、別のワークフローでは、外部の API の一時的な失敗は再試行し、回数を超えたら担当に通知する処理を求められています。適切な組み合わせはどれですか。

- A. 関数のメモリを増やす。ワークフローは手動承認にする
- B. ストリームの保持期間を短くして不正なレコードの期限切れを待つ。ワークフローは Lambda の中で `sleep` する
- C. `BisectBatchOnFunctionError` と失敗の送信先を使う。ワークフローは `Retry` と `Catch` を使う
- D. シャードを増やす。ワークフローは Express で同じ処理を無限に繰り返す

??? success "答えと解説"
    **正解: C**

    ストリームの失敗はバッチの分割と失敗の送信先で分離します。Step Functions は `Retry` と `Catch` で扱います。

    - A: 誤り。不正なレコードの問題を解決せず、自動にならない。
    - B: 誤り。データを失い、再試行も自作になる。
    - C: 正しい。
    - D: 誤り。止まっている原因を解決せず、無限の繰り返しも不適切。

    **スキル:** [ワークフロー](../domain5.md#t5-1-workflows) / **参照:** [ストリームのエラー処理の設定](../../../services/lambda.md#esm-stream-errors)、[エラー処理](../../../services/step-functions.md#error-handling)

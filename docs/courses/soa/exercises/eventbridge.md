# EventBridge と通知の問題集

対象の解説: [EventBridge](../../../services/messaging.md#eventbridge)、[SNS](../../../services/messaging.md#sns)、[EventBridge による修復パターン](../../../services/operations.md#eventbridge-remediation)、[AWS User Notifications](../../../services/operations.md#user-notifications)

### 問1 {#q1}

S3 のイベント通知の送信先に SNS トピックを指定したところ、設定の保存時に送信先の検証エラーになりました。トピックは同じアカウント、同じリージョンにあり、暗号化はしていません。何を直しますか。

- A. トピックのアクセスポリシーで `s3.amazonaws.com` に `sns:Publish` を許可する
- B. トピックを FIFO に変更して、メッセージの順序が保たれるようにする
- C. S3 バケットのバージョニングを有効にして、もう一度イベント通知を保存する
- D. 設定を行う IAM ユーザーに `AdministratorAccess` を付けて、S3 のコンソールからもう一度同じ設定を保存する

??? success "答えと解説"
    **正解: A**

    S3 から発行するには、トピックのリソースポリシーで S3 を許可します。

    - A: 正しい。
    - B: 誤り。S3 の通知の検証の問題は順序と関係がない。
    - C: 誤り。イベント通知の送信先の検証とバージョニングは関係がない。
    - D: 誤り。S3 サービスからの発行の許可はトピックの側で決まる。

    **スキル:** [1.1.5](../domain1.md#skill-1-1-5) / **参照:** [Event Notifications](../../../services/s3.md#event-notifications)、[トピックのアクセスポリシーと暗号化](../../../services/messaging.md#sns-access)

### 問2 {#q2}

KMS のカスタマー管理キーで暗号化した SNS トピックに、CloudWatch アラームの通知が届かなくなりました。暗号化する前は届いていました。何を確認しますか。

- A. トピックのサブスクリプションのプロトコルが、暗号化に対応した HTTPS になっているか
- B. KMS のキーポリシーで、CloudWatch のサービスプリンシパルにキーの利用を許可しているか
- C. CloudWatch Logs の保持期間が、KMS キーのローテーションの期間より長く設定されていて、発行が止まっているか
- D. アラームの統計が、暗号化に対応した `Average` になっているか

??? success "答えと解説"
    **正解: B**

    暗号化したトピックに AWS サービスから送るには、そのサービスに KMS キーの利用を許可します。

    - A: 誤り。暗号化はトピックの保存時の話で、プロトコルは発行の失敗の原因にならない。
    - B: 正しい。
    - C: 誤り。ログの保持期間は無関係である。
    - D: 誤り。統計は発行の権限と関係がない。

    **スキル:** [1.1.5](../domain1.md#skill-1-1-5) / **参照:** [トピックのアクセスポリシーと暗号化](../../../services/messaging.md#sns-access)

### 問3 {#q3}

AWS Health の通知を、担当者のメールとコンソールで一か所で管理したいと考えています。アプリケーションへの連携は不要で、なるべく作り込みたくありません。どれを選びますか。

- A. SES の設定セットを作り、Health のイベントをメールとして送信する処理を書く
- B. SNS トピックと Lambda を組み合わせ、Health の API を定期的に呼んで通知する
- C. S3 のイベント通知で Health のログを受け取る構成にする
- D. AWS User Notifications で通知を設定する

??? success "答えと解説"
    **正解: D**

    AWS の通知を人に届けるだけなら User Notifications です。アプリや他のサービスへ配るなら SNS を使います。

    - A: 誤り。メール送信の基盤であり、AWS の通知の管理には作り込みが必要になる。
    - B: 誤り。作り込みが多く、要件より大がかりである。
    - C: 誤り。Health のイベントは S3 のイベント通知の対象ではない。
    - D: 正しい。

    **スキル:** [1.1.5](../domain1.md#skill-1-1-5) / **参照:** [AWS User Notifications](../../../services/operations.md#user-notifications)、[SNS](../../../services/messaging.md#sns)

### 問4 {#q4}

CloudWatch アラームの通知を、運用チームの Slack のチャンネルへ届けたいと考えています。コードを書かない方法はどれですか。

- A. アラームのアクションに Slack の URL を直接指定する
- B. CloudWatch エージェントの設定ファイルに Slack の Webhook の URL を送信先として記述し、全台へ配布する
- C. SNS トピックを Amazon Q Developer in chat applications につなぐ
- D. CloudTrail の証跡の送信先に Slack のチャンネルを選択する

??? success "答えと解説"
    **正解: C**

    Amazon Q Developer in chat applications は、旧称 AWS Chatbot です。SNS から Slack や Teams へ届けられます。

    - A: 誤り。アラームのアクションに外部の URL は指定できない。
    - B: 誤り。エージェントはメトリクスとログを収集するもので、通知はしない。
    - C: 正しい。
    - D: 誤り。証跡の送信先は S3 と CloudWatch Logs である。

    **スキル:** [1.1.5](../domain1.md#skill-1-1-5) / **参照:** [Amazon Q Developer in chat applications](../../../services/operations.md#q-chat)、[SNS](../../../services/messaging.md#sns)

### 問5 {#q5}

EC2 の状態変化を受けるルールを作りましたが、ターゲットの Lambda が動きません。メトリクスの `MatchedEvents` は増えており、`FailedInvocations` も増えています。Lambda のログは出ていません。最初に確認することはどれですか。

- A. Lambda のリソースベースポリシーで `events.amazonaws.com` を許可しているか
- B. Lambda の実行ロールに `events:PutEvents` が付いていて、EventBridge へ結果を返せる状態になっているか
- C. ルールが正しいイベントバスに作られているか
- D. イベントパターンのキーと値が、イベントの内容と一致しているか

??? success "答えと解説"
    **正解: A**

    一致するのに動かないなら、ターゲットの権限を疑います。Lambda はリソースベースポリシーで許可します。

    - A: 正しい。
    - B: 誤り。EventBridge が Lambda を呼ぶ権限は、実行ロールでは決まらない。
    - C: 誤り。イベントがルールに一致しているので、バスの誤りではない。
    - D: 誤り。一致はしているので、パターンの問題ではない。

    **スキル:** [1.2.2](../domain1.md#skill-1-2-2) / **参照:** [ルールとイベントパターン](../../../services/messaging.md#eventbridge-rules)、[EventBridge による修復パターン](../../../services/operations.md#eventbridge-remediation)

### 問6 {#q6}

EventBridge のターゲットに権限が足りず、イベントが失われています。原因の調査のために、配信できなかったイベントを残したいと考えています。正しい設定はどれですか。

- A. 再試行の回数を 185 回より大きくして、権限が直るまで再試行を続けさせる
- B. ターゲットの DLQ に SQS の標準キューを指定し、キューポリシーで EventBridge に `sqs:SendMessage` を許可する
- C. ルールを無効にして再度有効にし、失われたイベントがもう一度配信されるのを待つ
- D. ターゲットの DLQ に SQS の FIFO キューを指定し、キューポリシーで EventBridge に送信を許可して順序も保つ

??? success "答えと解説"
    **正解: B**

    DLQ は SQS の標準キューです。キューポリシーで EventBridge に送信を許可します。

    - A: 誤り。権限不足は再試行されず、回数の上限も 185 回である。
    - B: 正しい。
    - C: 誤り。無効化と再有効化では、失われたイベントは戻らない。
    - D: 誤り。DLQ に FIFO キューは使えない。

    **スキル:** [1.2.2](../domain1.md#skill-1-2-2) / **参照:** [ターゲットの再試行と DLQ](../../../services/messaging.md#target-retry-dlq)

### 問7 {#q7}

宛先の API が停止している間に、古いイベントが配信されるのを避けたいと考えています。1 時間を過ぎたイベントには価値がありません。どの設定を変更しますか。

- A. ターゲットの入力トランスフォーマーで、イベントの時刻の項目を取り除く
- B. ルールのイベントパターンに時刻の条件を追加して、1 時間ごとに書き換える
- C. `MaximumEventAgeInSeconds` を 3,600 に変更する
- D. `MaximumRetryAttempts` を既定の 185 から 186 以上の大きな値へ増やす

??? success "答えと解説"
    **正解: C**

    既定は 86,400 秒（24 時間）です。縮めると、その時間を過ぎたイベントの再試行をやめます。

    - A: 誤り。項目を除いても配信は止まらない。
    - B: 誤り。再試行中のイベントには効かず、運用も難しい。
    - C: 正しい。
    - D: 誤り。上限は 185 で、増やしても古いイベントは減らない。

    **スキル:** [1.2.2](../domain1.md#skill-1-2-2) / **参照:** [ターゲットの再試行と DLQ](../../../services/messaging.md#target-retry-dlq)

### 問8 {#q8}

入力トランスフォーマーを設定したところ、ターゲットが呼ばれなくなりました。DLQ のメッセージの属性 `ERROR_CODE` は `INVALID_JSON` です。何が原因と考えられますか。

- A. ターゲットの Lambda の同時実行数の上限を超えたため
- B. SQS の DLQ が FIFO キューで、メッセージグループ ID が足りないため
- C. イベントバスのリソースポリシーが、イベントの送信を拒否しているため
- D. 入力テンプレートのクォートなどの誤りで、JSON として不正になっているため

??? success "答えと解説"
    **正解: D**

    入力テンプレートの誤りで JSON が不正になると、`INVALID_JSON` として DLQ に残ります。

    - A: 誤り。呼び出しの前に入力の形式で失敗している。
    - B: 誤り。DLQ にメッセージが届いているので、この説明には当たらない。
    - C: 誤り。配信の段階まで進んでいるので、送信の拒否ではない。
    - D: 正しい。

    **スキル:** [1.2.2](../domain1.md#skill-1-2-2) / **参照:** [入力トランスフォーマー](../../../services/messaging.md#input-transformer)、[ターゲットの再試行と DLQ](../../../services/messaging.md#target-retry-dlq)

### 問9 {#q9}

SQS キューのメッセージに、顧客マスタの情報を Lambda で付け足してから、Step Functions のステートマシンへ渡したいと考えています。ソースとターゲットは 1 対 1 です。コードを最小にする構成はどれですか。

- A. EventBridge Pipes のエンリッチメントに Lambda を指定する
- B. ルールの入力トランスフォーマーで顧客マスタを検索するように設定する
- C. SQS をポーリングするコンテナを常時動かし、顧客マスタの検索とステートマシンの起動まで自作する
- D. SNS トピックのサブスクリプションフィルターポリシーで情報を付け足す

??? success "答えと解説"
    **正解: A**

    1 対 1 の連携の途中で情報を足すのは、Pipes のエンリッチメントです。

    - A: 正しい。
    - B: 誤り。入力トランスフォーマーはイベントの形を変えるだけで、外部の情報を取りに行けない。
    - C: 誤り。1 対 1 の連携のために、運用する部品が増えてしまう。
    - D: 誤り。フィルターは受け取るメッセージを絞るだけで、情報は足せない。

    **スキル:** [1.2.2](../domain1.md#skill-1-2-2) / **参照:** [Pipes](../../../services/messaging.md#eventbridge-pipes)、[入力トランスフォーマー](../../../services/messaging.md#input-transformer)

### 問10 {#q10}

ルールの `MatchedEvents` が 0 のままです。パートナーのイベントが届くはずのルールを `default` のバスに作っていました。正しい理解を選んでください。（2つ選択）

- A. ルールが一致しないときはイベントが DLQ に送られるので、DLQ の中を確かめる
- B. パートナーのイベントは、パートナーイベントソースに関連付けたバスに届くので、そのバスにルールを作る
- C. サンドボックスに実際のイベントの例を入れて、パターンの誤りを確かめる
- D. 再試行の回数を増やすと、一致しなかったイベントがもう一度評価される
- E. ターゲットの権限が足りないと `MatchedEvents` は増えないので、権限を先に足す

??? success "答えと解説"
    **正解: B, C**

    一度も一致しないときは、バスとパターンの誤りを疑います。

    - A: 誤り。DLQ はターゲットへの配信の失敗に使われ、不一致では送られない。
    - B: 正しい。
    - C: 正しい。
    - D: 誤り。再試行はターゲットへの配信の話で、不一致のイベントは再評価されない。
    - E: 誤り。権限の不足は一致の後の問題で、`MatchedEvents` は増える。

    **スキル:** [1.2.2](../domain1.md#skill-1-2-2) / **参照:** [イベントバス](../../../services/messaging.md#event-buses)、[ルールとイベントパターン](../../../services/messaging.md#eventbridge-rules)

### 問11 {#q11}

画像が S3 にアップロードされたら Lambda で処理します。`.jpg` だけを対象にしたいです。最も単純な設定はどれですか。

- A. `AWS/S3` のアラームから Lambda を呼び出し、オブジェクト名をメトリクスのディメンションの値から取得して処理する
- B. S3 Event Notifications でサフィックスに `.jpg` を指定して、Lambda を送信先にする
- C. 証跡のデータイベントを有効にし、ログを 5 分おきに検索する Lambda をスケジュールで動かす
- D. 全オブジェクトの一覧を取得する Lambda を毎分動かし、前回との差分から処理する対象を決める

??? success "答えと解説"
    **正解: B**

    プレフィックスとサフィックスの絞り込みなら、S3 Event Notifications で足ります。

    - A: 誤り。メトリクスにオブジェクト名は含まれない。
    - B: 正しい。
    - C: 誤り。仕組みが複雑で、遅延も大きい。
    - D: 誤り。ポーリングは無駄が多く、要件に対して複雑である。

    **スキル:** [3.2.2](../domain3.md#skill-3-2-2) / **参照:** [Event Notifications](../../../services/s3.md#event-notifications)、[S3 イベント通知](../../../services/messaging.md#s3-events)

### 問12 {#q12}

S3 のオブジェクト作成イベントを、SQS の FIFO キューへ順序付きで送りたいと考えています。Event Notifications の送信先に FIFO キューを選べません。どの構成にしますか。

- A. バケットのバージョニングを有効にして、もう一度 FIFO キューを Event Notifications の送信先に指定して保存する
- B. S3 のレプリケーションを設定して、FIFO キューをレプリケーション先に指定する
- C. Event Notifications の送信先に SNS の FIFO トピックを指定し、そこから FIFO キューに配信する
- D. バケットで EventBridge を有効にし、ルールのターゲットに FIFO キューを指定する

??? success "答えと解説"
    **正解: D**

    Event Notifications の SQS は標準キューのみです。EventBridge のルールなら FIFO キューをターゲットにできます。

    - A: 誤り。バージョニングで FIFO キューが送信先になることはない。
    - B: 誤り。レプリケーションの送信先はバケットである。
    - C: 誤り。SNS の FIFO トピックも Event Notifications の送信先にできない。
    - D: 正しい。

    **スキル:** [3.2.2](../domain3.md#skill-3-2-2) / **参照:** [Event Notifications](../../../services/s3.md#event-notifications)、[S3 イベント通知](../../../services/messaging.md#s3-events)

### 問13 {#q13}

S3 のイベント通知で Lambda を呼び出せません。担当者は関数の実行ロールに `s3:*` を追加しましたが、直りませんでした。正しい対処はどれですか。

- A. S3 のブロックパブリックアクセスを無効にして、外部から呼び出せるようにする
- B. バケットポリシーで Lambda の実行ロールに `s3:GetObject` を許可する
- C. 関数のリソースベースポリシーで S3 に `lambda:InvokeFunction` を許可する
- D. 実行ロールに `lambda:InvokeFunction` を追加して、関数が S3 のイベントを受けて自分を呼べるようにする設定を入れる

??? success "答えと解説"
    **正解: C**

    呼び出す側の許可はリソースベースポリシーで行います。実行ロールは関数が他のサービスを呼ぶための権限です。

    - A: 誤り。ブロックパブリックアクセスはイベント通知の呼び出しと関係がない。
    - B: 誤り。読み取りの権限で、呼び出しの権限ではない。
    - C: 正しい。
    - D: 誤り。S3 が呼び出す権限は実行ロールでは決まらない。

    **スキル:** [3.2.2](../domain3.md#skill-3-2-2) / **参照:** [Lambda の実行ロール](../../../services/iam.md#lambda-execution-role)、[S3 イベント通知](../../../services/messaging.md#s3-events)

### 問14 {#q14}

開発環境の EC2 を、平日の夜に自動で止めたいと考えています。対象はタグで決まっています。コードを書かずに実現できる方法はどれですか。

- A. `AWS/EC2` の CPU のアラームで EC2 の停止アクションを実行し、夜に CPU が下がったインスタンスから順に止める
- B. EventBridge のスケジュールで Automation の `AWS-StopEC2Instance` をタグの対象に実行する
- C. インスタンスの中の cron で、OS のシャットダウンをスケジュールしておく
- D. Auto Scaling のウォームプールに開発環境のインスタンスをすべて移す

??? success "答えと解説"
    **正解: B**

    定期実行はスケジュールで行い、対象のタグは Automation で指定します。

    - A: 誤り。CPU の値で止めるので、夜に止めるという要件に合わない。
    - B: 正しい。
    - C: 誤り。各インスタンスの設定が要り、タグでの一元管理もできない。
    - D: 誤り。既存の EC2 を夜に止める機能ではない。

    **スキル:** [3.2.2](../domain3.md#skill-3-2-2) / **参照:** [スケジュール](../../../services/messaging.md#eventbridge-schedule)、[EventBridge による修復パターン](../../../services/operations.md#eventbridge-remediation)

### 問15 {#q15}

セキュリティグループの変更を検知したら、変更内容の確認、元に戻す処理、通知を順番に実行します。途中の失敗では再試行と分岐も必要です。どれが適切ですか。

- A. EventBridge のルールで Step Functions のステートマシンを起動する
- B. Lambda のレイヤーに手順を書き、順番と再試行と分岐の処理を関数どうしで共有して実行する
- C. S3 のイベント通知で各手順の Lambda を順番に呼ぶ
- D. CloudWatch の複合アラームで手順の順序を定義する

??? success "答えと解説"
    **正解: A**

    複数の手順と再試行、分岐は Step Functions に向きます。API の呼び出しは CloudTrail 経由で EventBridge が受けます。

    - A: 正しい。
    - B: 誤り。レイヤーはコードの共有の仕組みである。
    - C: 誤り。S3 のイベントがきっかけではなく、順序の制御もできない。
    - D: 誤り。複合アラームはアラームの状態の組み合わせで、手順を管理しない。

    **スキル:** [3.2.2](../domain3.md#skill-3-2-2) / **参照:** [AWS Step Functions](../../../services/step-functions.md)、[EventBridge による修復パターン](../../../services/operations.md#eventbridge-remediation)

### 問16 {#q16}

アラートをきっかけにインシデントの調査を自動で始めさせ、テレメトリとデプロイの情報から根本原因の候補と緩和の手順を得たいと考えています。どのサービスが適していますか。

- A. AWS Compute Optimizer
- B. Amazon Inspector
- C. AWS Trusted Advisor
- D. AWS DevOps Agent

??? success "答えと解説"
    **正解: D**

    DevOps Agent はアラートなどを受けて調査を始め、根本原因を探して緩和の手順を示します。

    - A: 誤り。サイズの推奨で、インシデントの調査はしない。
    - B: 誤り。脆弱性の検査で、インシデントの調査はしない。
    - C: 誤り。設定の点検と助言で、インシデントの調査はしない。
    - D: 正しい。

    **スキル:** [3.2.2](../domain3.md#skill-3-2-2) / **参照:** [AWS DevOps Agent](../../../services/operations.md#devops-agent)、[EventBridge による修復パターン](../../../services/operations.md#eventbridge-remediation)

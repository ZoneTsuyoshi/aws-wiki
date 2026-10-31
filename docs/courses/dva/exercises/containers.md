# コンテナの問題集

対象の解説: [コンテナ(ECR、ECS、EKS)](../../../services/containers.md)

### 問1 {#q1}

Dockerfile に `ENTRYPOINT ["python", "app.py"]` と `CMD ["--port", "8080"]` があります。`docker run my-app --port 9090` を実行すると、どのコマンドが動きますか。

- A. `--port 9090`
- B. `python app.py --port 8080 --port 9090`
- C. `python app.py --port 9090`
- D. `python app.py --port 8080`

??? success "答えと解説"
    **正解: C**

    `docker run` の引数は `CMD` だけを置き換えます。`ENTRYPOINT` は残り、`python app.py --port 9090` が動きます。

    - A: `ENTRYPOINT` を置き換えるには `--entrypoint` が必要です。
    - B: `CMD` は追加ではなく置き換えです。
    - C: 正しい結果です。
    - D: 引数を渡しているので `CMD` は使われません。

    **スキル:** C03 3.1.2 / **参照:** [命令の詳細](../../../services/containers.md#dockerfile-instructions)

### 問2 {#q2}

CI で夜間にビルドするジョブが、ビルドに 14 時間かかり、最後の `docker push` が認証エラーで失敗しています。IAM の権限は正しく、ジョブの最初に `aws ecr get-login-password` でログインしています。最も適切な対応はどれですか。

- A. プッシュの直前にもう一度ログインする
- B. `ecr:GetAuthorizationToken` をリポジトリの ARN に限定する
- C. リポジトリのタグを `MUTABLE` に変更する
- D. `docker login` のユーザー名を IAM ユーザー名にする

??? success "答えと解説"
    **正解: A**

    認証トークンの有効期間は 12 時間です。14 時間後には切れているので、プッシュの直前に取り直します。

    - A: 正しい対応です。
    - B: このアクションはリソース `*` に対して許可するもので、限定できません。
    - C: タグの設定で、認証エラーには関係しません。
    - D: ユーザー名は `AWS` です。

    **スキル:** C03 3.1.2 / **参照:** [認証とプッシュ、プル](../../../services/containers.md#ecr-auth)

### 問3 {#q3}

リポジトリに `IMMUTABLE` を設定したところ、CI の `docker push my-app:latest` が失敗するようになりました。発生するエラーと、本番のタグの上書きを防いだまま CI を動かす対応の組み合わせで、最も適切なものはどれですか。

- A. `ImageAlreadyExistsException`。イメージを毎回削除する
- B. `RepositoryPolicyNotFoundException`。リポジトリポリシーを追加して許可する
- C. `LayerAlreadyExistsException`。レイヤーを再アップロードする
- D. `ImageTagAlreadyExistsException`。コミット SHA のタグでプッシュする

??? success "答えと解説"
    **正解: D**

    不変タグのリポジトリに既存のタグでプッシュすると `ImageTagAlreadyExistsException` です。コミット SHA のような一意のタグを使えば解決します。

    - A: このエラーではなく、イメージの削除は運用が危険です。
    - B: ポリシーの問題ではありません。
    - C: 不変タグで発生するエラーではありません。
    - D: 正しい組み合わせです。

    **スキル:** C03 3.1.2 / **参照:** [タグと不変タグ](../../../services/containers.md#image-tags)

### 問4 {#q4}

次のライフサイクルルールの適用を検討しています。`tagStatus` が `tagged`、`tagPatternList` が `["prod*"]`、`countType` が `imageCountMoreThan`、`countNumber` が 10 です。`prod` で始まるタグのイメージが 15 個あります。結果として正しいものはどれですか。

- A. 新しい 5 個が直ちに期限切れになる
- B. 古い 5 個が 24 時間以内に期限切れになる
- C. 古い 10 個が 24 時間以内に期限切れになる
- D. `countUnit` がないのでルールがエラーになる

??? success "答えと解説"
    **正解: B**

    10 個を超える分が対象で、古いものから期限切れになります。条件を満たしてから 24 時間以内に実行されます。`countUnit` は日数の `countType` だけで使います。

    - A: 古いものから順で、直ちにではありません。
    - B: 正しい結果です。
    - C: 残すのが 10 個で、消すのは 5 個です。
    - D: `imageCountMoreThan` に `countUnit` は不要で、指定するとエラーになります。

    **スキル:** C03 3.1.2 / **参照:** [ライフサイクルポリシー](../../../services/containers.md#ecr-lifecycle)

### 問5 {#q5}

プログラミング言語のパッケージの脆弱性も検出し、新しい CVE が公開されたらプッシュ済みのイメージも再評価したいと考えています。最も適切な設定はどれですか。

- A. 基本スキャンをスキャンオンプッシュで有効にする
- B. 基本スキャンを手動で毎日実行する
- C. 拡張スキャンを継続スキャンのフィルターで有効にする
- D. ライフサイクルポリシーで古いイメージを毎日自動で削除する

??? success "答えと解説"
    **正解: C**

    拡張スキャンは Amazon Inspector と連携し、OS と言語パッケージを検査します。フィルターで継続スキャンを選べます。

    - A: 基本スキャンはプッシュ時か手動で、継続的に再評価しません。
    - B: 手動のスキャンは同じイメージで 24 時間に 1 回までで、運用負荷も高くなります。
    - C: 正しい設定です。
    - D: 脆弱性の検出にはなりません。

    **スキル:** C03 3.1.2 / **参照:** [イメージスキャン](../../../services/containers.md#ecr-scanning)

### 問6 {#q6}

アカウント A の ECR から、アカウント B の別リージョンへイメージを複製します。設定について正しいものはどれですか。（2つ選択）

- A. アカウント B のレジストリ許可ポリシーでアカウント A を許可する
- B. レプリケーションルールはアカウント A のレジストリに設定する
- C. アカウント A の各リポジトリにリポジトリポリシーが必要である
- D. 設定前にプッシュしたイメージも自動で複製される
- E. リポジトリのライフサイクルポリシーも一緒に複製される

??? success "答えと解説"
    **正解: A, B**

    ルールは送信元のレジストリ設定に書き、権限は宛先のレジストリ許可ポリシーで与えます。

    - A: 宛先側で必要な設定です。
    - B: 送信元で必要な設定です。
    - C: 送信元のリポジトリに特別なポリシーは不要です。
    - D: 設定後にプッシュ、または復元したものだけが対象です。
    - E: ライフサイクルポリシーは複製されません。

    **スキル:** C03 3.1.2 / **参照:** [レプリケーション](../../../services/containers.md#ecr-replication)

### 問7 {#q7}

Fargate のタスクがイメージを取得できず、`CannotPullContainerError` で停止します。プライベート ECR を使っており、アプリは S3 にも書き込みます。ネットワークは正常です。権限を確認すべきロールはどれですか。

- A. タスクロール
- B. 実行ロール
- C. コンテナインスタンスのロール
- D. サービスリンクロールだけ

??? success "答えと解説"
    **正解: B**

    イメージの取得はタスクの起動前の処理で、実行ロールの権限を使います。

    - A: タスクロールはアプリのコードが使うもので、S3 への書き込みに使います。
    - B: 正しいロールです。
    - C: Fargate にコンテナインスタンスはありません。
    - D: ECR の取得権限は実行ロールで与えます。

    **スキル:** C03 3.3.2 / **参照:** [タスクロールと実行ロール](../../../services/containers.md#task-role-vs-execution-role)

### 問8 {#q8}

EC2 で動く ECS タスクのコンテナは、普段 128 MiB で、まれに 256 MiB まで使います。インスタンスのメモリを効率的に使い、暴走したときは 300 MiB で止めたいと考えています。最も適切な設定はどれですか。

- A. `memory: 128`、`memoryReservation: 300`
- B. `memory: 300`、`memoryReservation` なし
- C. `memoryReservation: 300`、`memory` なし
- D. `memoryReservation: 128`、`memory: 300`

??? success "答えと解説"
    **正解: D**

    `memoryReservation` はソフトリミットで、インスタンスから予約する量です。`memory` はハードリミットで、超えるとコンテナが止まります。`memory` は `memoryReservation` より大きくします。

    - A: 大小が逆で、登録できません。
    - B: 300 MiB を常に予約するので効率が悪くなります。
    - C: ハードリミットがなく、300 MiB で止まりません。
    - D: 正しい設定です。

    **スキル:** C03 4.3.2 / **参照:** [memory と memoryReservation](../../../services/containers.md#memory-settings)

### 問9 {#q9}

Fargate のタスク定義を登録します。`cpu` と `memory` の組み合わせとして、**有効な**ものはどれですか。（2つ選択）

- A. `cpu: 256`、`memory: 4096`
- B. `cpu: 512`、`memory: 512`
- C. `cpu: 1024`、`memory: 3072`
- D. `cpu: 2048`、`memory: 2048`
- E. `cpu: 4096`、`memory: 8192`

??? success "答えと解説"
    **正解: C, E**

    1024 (1 vCPU) は 2〜8 GB、4096 (4 vCPU) は 8〜30 GB です。

    - A: 256 は 512 MiB、1 GB、2 GB のみです。
    - B: 512 は 1〜4 GB です。
    - C: 有効です。
    - D: 2048 は 4〜16 GB です。
    - E: 有効です。

    **スキル:** C03 4.3.2 / **参照:** [Fargate と EC2](../../../services/containers.md#fargate-vs-ec2)

### 問10 {#q10}

タスク内の `migrate` コンテナで DB を初期化し、正常終了したら `app` コンテナを起動します。`migrate` は終了した後も、タスクを止めたくありません。最も適切な設定はどれですか。

- A. `migrate` に `essential: true`、`app` に `dependsOn` の `COMPLETE`
- B. `migrate` に `essential: true`、`app` に `dependsOn` の `HEALTHY`
- C. `migrate` に `essential: false`、`app` に `dependsOn` の `START`
- D. `migrate` に `essential: false`、`app` に `dependsOn` の `SUCCESS`

??? success "答えと解説"
    **正解: D**

    `SUCCESS` は終了コード 0 で終わるのを待ちます。`essential: false` なら、`migrate` の終了でタスクは止まりません。

    - A: `COMPLETE` は必須コンテナに設定できません。
    - B: 必須コンテナの終了でタスク全体が止まります。
    - C: 起動しただけで `app` が始まり、完了を待ちません。
    - D: 正しい設定です。

    **スキル:** C03 3.3.2 / **参照:** [dependsOn](../../../services/containers.md#depends-on)

### 問11 {#q11}

タスク定義の `healthCheck` の既定値と範囲について、正しいものはどれですか。（2つ選択）

- A. `startPeriod` の既定は 60 秒で、最大 600 秒である
- B. `startPeriod` は 0〜300 秒で、この間の失敗は再試行の回数に数えない
- C. `interval` の既定は 5 秒で、最大 30 秒である
- D. `retries` の既定は 3 で、1〜10 の範囲で指定できる
- E. `startPeriod` を設定すると ALB のヘルスチェックの失敗も無視する

??? success "答えと解説"
    **正解: B, D**

    `startPeriod` は既定でオフで、0〜300 秒です。`retries` の既定は 3 です。`interval` の既定は 30 秒で、5〜300 秒です。

    - A: 既定と範囲が違います。
    - B: 正しい説明です。
    - C: 既定と範囲が違います。
    - D: 正しい説明です。
    - E: ALB の失敗を無視するのはサービスの `healthCheckGracePeriodSeconds` です。

    **スキル:** C03 4.2.5 / **参照:** [healthCheck](../../../services/containers.md#ecs-healthcheck)

### 問12 {#q12}

ALB の背後にある ECS サービスのタスクは、起動に 90 秒かかります。デプロイのたびに、準備が終わる前にタスクが異常と判定されて置き換えられます。最も適切な対応はどれですか。

- A. `minimumHealthyPercent` を 0 にして、古いタスクを先にすべて止める
- B. `maximumPercent` を 400 にする
- C. `healthCheckGracePeriodSeconds` を 120 にする
- D. `stopTimeout` を 120 にする

??? success "答えと解説"
    **正解: C**

    `healthCheckGracePeriodSeconds` は、起動後にヘルスチェックを無視する時間です。既定は 0 秒です。起動時間より長くします。

    - A: 動いているタスクが減るだけで、原因は解消しません。
    - B: 同時に増やせるタスクの数で、判定は変わりません。
    - C: 正しい対応です。
    - D: 停止時の猶予で、起動時の判定には関係しません。

    **スキル:** C03 3.3.2 / **参照:** [サービスの設定](../../../services/containers.md#service-settings)

### 問13 {#q13}

`desiredCount` が 4、`minimumHealthyPercent` が 50、`maximumPercent` が 100 のサービスをローリング更新します。動作として正しいものはどれですか。

- A. 2 つを止めてから、新しい 2 つを起動する
- B. 新しい 4 つを先に起動し、古い 4 つを止める
- C. 全タスクを止めてから、新しい 4 つを起動する
- D. デプロイが始まらない

??? success "答えと解説"
    **正解: A**

    下限が 2、上限が 4 です。4 つ動いている状態から増やせないので、2 つまで止めて新しいものを起動します。

    - A: 正しい動作です。
    - B: `maximumPercent` が 200 のときの動作です。
    - C: `minimumHealthyPercent` が 0 のときの動作です。
    - D: 少なくとも 1 つを止められるので進みます。

    **スキル:** C03 3.3.6 / **参照:** [ローリング更新](../../../services/containers.md#rolling-update)

### 問14 {#q14}

`capacityProviderStrategy` を、`FARGATE` は `base: 2`、`weight: 1`、`FARGATE_SPOT` は `weight: 3` とします。`desiredCount` が 10 のとき、`FARGATE` で動くタスク数はいくつですか。

- A. 2
- B. 3
- C. 4
- D. 6

??? success "答えと解説"
    **正解: C**

    先に `base` の 2 を `FARGATE` に置きます。残り 8 を 1:3 に分けると `FARGATE` が 2、`FARGATE_SPOT` が 6 です。`FARGATE` は合計 4 です。

    - A: `base` の分だけで、残りの配分を含めていません。
    - B: 10 を 1:3 にしておおよそ 2.5 とする誤りです。
    - C: 正しい計算です。
    - D: `FARGATE_SPOT` の数です。

    **スキル:** C03 3.3.2 / **参照:** [キャパシティプロバイダー](../../../services/containers.md#capacity-providers)

### 問15 {#q15}

Fargate Spot のタスクが中断されたときに、処理中のデータを保存したいと考えています。適切な設計はどれですか。（2つ選択）

- A. アプリで `SIGTERM` を処理して保存する
- B. `stopTimeout` を保存に必要な時間に合わせ、最大 120 秒にする
- C. `stopTimeout` を 600 秒にする
- D. `placementConstraints` で中断されないインスタンスを選ぶ
- E. `healthCheckGracePeriodSeconds` を長くする

??? success "答えと解説"
    **正解: A, B**

    中断の 2 分前に `SIGTERM` が届きます。`stopTimeout` の後は `SIGKILL` です。既定は 30 秒、最大は 120 秒です。

    - A: 正しい設計です。
    - B: 正しい設計です。
    - C: 最大は 120 秒です。
    - D: Fargate に配置の制約はありません。
    - E: 起動時のヘルスチェックの設定です。

    **スキル:** C03 1.1.3 / **参照:** [キャパシティプロバイダー](../../../services/containers.md#capacity-providers)

### 問16 {#q16}

EC2 の ECS サービスで、AZ に均等に分けた上で、各 AZ ではインスタンス数を減らしたいと考えています。また、GPU のインスタンスだけに置きます。最も適切な設定はどれですか。

- A. `binpack` の後に `spread`、制約は `distinctInstance`
- B. `random` のみ、制約は `memberOf`
- C. `spread` の後に `binpack`、制約は `memberOf`
- D. `spread` の後に `binpack`、制約は `distinctInstance`

??? success "答えと解説"
    **正解: C**

    戦略は配列の順に適用します。AZ への `spread`、その後に `binpack` です。インスタンスの絞り込みは `memberOf` の式で行います。

    - A: 順序が逆で、制約も絞り込みになりません。
    - B: `random` では AZ に均等にならず、詰めることもできません。
    - C: 正しい設定です。
    - D: `distinctInstance` は別のインスタンスに置く制約で、GPU に絞れません。

    **スキル:** C03 3.3.2 / **参照:** [タスクの配置](../../../services/containers.md#task-placement)

### 問17 {#q17}

ECS サービスのタスク数を CPU 使用率 60% に保ちたいと考えています。使う仕組みとして最も適切なものはどれですか。

- A. EC2 Auto Scaling のターゲット追跡ポリシーを使い、`ASGAverageCPUUtilization` を目標値 60 で指定する
- B. Application Auto Scaling のターゲット追跡を使い、`ECSServiceAverageCPUUtilization` を指定する
- C. CloudWatch アラームから `UpdateService` を直接呼び、`desiredCount` を変える
- D. `maximumPercent` を 200 にして、自動で 2 倍まで増やす

??? success "答えと解説"
    **正解: B**

    ECS のサービスは Application Auto Scaling で、`ecs:service:DesiredCount` を増減します。

    - A: Auto Scaling グループのインスタンス数の設定です。
    - B: 正しい方法です。
    - C: アラームから直接 API は呼べず、運用負荷も高くなります。
    - D: デプロイ中の上限で、スケーリングではありません。

    **スキル:** C03 4.3.1 / **参照:** [サービスの Auto Scaling](../../../services/containers.md#service-auto-scaling)

### 問18 {#q18}

Kubernetes の Deployment を `replicas: 10` で、`maxSurge` と `maxUnavailable` を既定値のまま更新します。更新中の Pod 数の上限と、最低限利用可能な Pod 数の組み合わせはどれですか。

- A. 上限 13、最低 8
- B. 上限 12、最低 7
- C. 上限 13、最低 7
- D. 上限 20、最低 5

??? success "答えと解説"
    **正解: A**

    既定は両方 25% です。`maxSurge` は切り上げで 3、`maxUnavailable` は切り捨てで 2 です。

    - A: 正しい組み合わせです。
    - B: 丸めが逆です。
    - C: `maxUnavailable` を切り上げた誤りです。
    - D: ECS の 200% と 50% の感覚で、既定ではありません。

    **スキル:** C03 3.3.2 / **参照:** [Deployment のフィールド](../../../services/containers.md#deployment-fields)

### 問19 {#q19}

Kubernetes で起動に最長 5 分かかるアプリがライブネスプローブの失敗で再起動を繰り返しています。起動後の障害を素早く検知する設定を変えずに解決します。最も適切な設定はどれですか。

- A. ライブネスの `failureThreshold` を 30 にし、`periodSeconds` を 10 のままにして再起動を遅らせる
- B. レディネスプローブだけに変更する
- C. `startupProbe` を `failureThreshold: 30`、`periodSeconds: 10` で追加する
- D. ライブネスの `timeoutSeconds` を 300 にする

??? success "答えと解説"
    **正解: C**

    スタートアッププローブが成功するまでライブネスは止まります。30 × 10 で 300 秒まで待ちます。

    - A: 起動後の検知も遅くなります。
    - B: レディネスは再起動しないので、固まった Pod を直せません。
    - C: 正しい設定です。
    - D: 起動後の検知が遅くなり、要件に反します。

    **スキル:** C03 4.2.5 / **参照:** [プローブのタイミング](../../../services/containers.md#probe-timing)

### 問20 {#q20}

複数の EKS クラスターで同じアプリを動かし、Pod に同じ IAM ロールを使わせます。OIDC プロバイダーを管理せず、信頼ポリシーをクラスターごとに変更したくありません。Pod は Linux の EC2 ノードで動きます。最も適切な方法はどれですか。

- A. ServiceAccount に `eks.amazonaws.com/role-arn` の注釈を付ける
- B. ノードのインスタンスプロファイルに権限を付ける
- C. アクセスキーを Kubernetes の Secret に保存する
- D. EKS Pod Identity のアソシエーションをクラスターごとに作る

??? success "答えと解説"
    **正解: D**

    Pod Identity は OIDC プロバイダーが不要で、`pods.eks.amazonaws.com` を信頼するだけなので、ポリシーをクラスターごとに変える必要がありません。

    - A: IRSA の方法で、クラスターごとの OIDC プロバイダーが必要です。
    - B: ノード上のすべての Pod に権限が渡ります。
    - C: 長期のアクセスキーは避けます。
    - D: 正しい方法です。

    **スキル:** C03 2.1.6 / **参照:** [Pod に IAM 権限を与える](../../../services/containers.md#pod-identity)

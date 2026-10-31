# コンテナの問題集

対象の解説: [コンテナ](../../../services/containers.md#ecs)

### 問1 {#q1}

ECS のタスクで、最初に初期化コンテナがスキーマの移行を実行し、成功した場合にだけアプリのコンテナを起動します。アプリのコンテナは、起動後に `curl -f` で自身の状態を確認します。設定の組み合わせとして正しいものはどれですか。

- A. 初期化コンテナの `essential` を `true` にして、アプリの `dependsOn` の条件を `START` にする
- B. アプリの `dependsOn` を初期化コンテナの `SUCCESS` にし、アプリの `healthCheck` に `curl -f` を設定する
- C. ターゲットグループのヘルスチェックで移行の完了を判定し、アプリの `command` の中で `sleep` して移行の時間を待つ
- D. 初期化コンテナの `healthCheck` で移行の完了を確認し、アプリの `dependsOn` の条件を `COMPLETE` にする

??? success "答えと解説"
    **正解: B**

    `SUCCESS` は依存先が 0 で終了した場合だけ満たされます。`healthCheck` は 0 以外を失敗として数えます。

    - A: 誤り。`START` は起動しただけで満たされ、移行の成功を待たない。
    - B: 正しい。
    - C: 誤り。ターゲットグループはコンテナの起動順を制御しない。
    - D: 誤り。`COMPLETE` は終了コードを問わないので、失敗でも起動する。

    **スキル:** [終了コード](../domain1.md#t1-2-exit-codes) / **参照:** [dependsOn](../../../services/containers.md#depends-on)、[healthCheck](../../../services/containers.md#ecs-healthcheck)

### 問2 {#q2}

Fargate のタスクが `CannotPullContainerError` で起動しません。アプリは起動後に S3 を読みます。担当者は、タスクロールに ECR の読み取りと S3 の読み取りを付けましたが、解決しません。正しい修正はどれですか。

- A. サービスリンクロールを削除して作り直し、ECS に権限を再作成させる
- B. タスクロールに `AdministratorAccess` を付けて、すべての権限不足を解消する
- C. ECR の権限をタスク実行ロールに付け、S3 の権限はタスクロールに残す
- D. ECR のリポジトリポリシーで、タスクロールの `ecr:BatchGetImage` を許可する

??? success "答えと解説"
    **正解: C**

    イメージの取得とログの送信はタスク**実行**ロール、アプリの AWS 呼び出しはタスクロールです。

    - A: 誤り。原因はサービスリンクロールではない。
    - B: 誤り。イメージの取得にタスクロールは使われない。
    - C: 正しい。
    - D: 誤り。取得の主体はタスク実行ロールで、タスクロールの許可では解決しない。

    **スキル:** [アクセス権限](../domain1.md#t1-4-permissions) / **参照:** [タスクロールと実行ロール](../../../services/containers.md#task-role-vs-execution-role)、[認証とプッシュ、プル](../../../services/containers.md#ecr-auth)

### 問3 {#q3}

ECS（Fargate）の本番サービスで、新しい版を本番の通信の 10% に 15 分流して確認してから切り替えます。CodeDeploy のデプロイグループなどの追加の部品は増やさず、アラームで自動的に戻します。また、新しいタスクが起動できないときも戻します。適切な設定はどれですか。

- A. ECS の組み込みのカナリアデプロイとアラーム、デプロイサーキットブレーカーを設定する
- B. `forceNewDeployment` を夜間に実行し、翌朝にログを確認して戻すかどうかを判断する
- C. 新旧のサービスを別の ALB に置き、Route 53 の重み付けを手で変更する
- D. ローリング更新の `maximumPercent` を 110 にして、新しいタスクが全体の 10% になるようにする

??? success "答えと解説"
    **正解: A**

    ECS は組み込みで Blue/Green、カナリア、線形に対応しています。アラームとサーキットブレーカーで自動で戻せます。

    - A: 正しい。
    - B: 誤り。段階的に流す仕組みがなく、自動で戻らない。
    - C: 誤り。部品が増え、手作業の切り替えになる。
    - D: 誤り。タスクの比率は通信の割合の制御にならず、確認の時間も取れない。

    **スキル:** [デプロイ方式](../domain1.md#t1-4-methods) / **参照:** [デプロイ](../../../services/containers.md#ecs-deployments)、[デプロイサーキットブレーカー](../../../services/containers.md#circuit-breaker)

### 問4 {#q4}

EKS の Deployment を更新すると、準備の整っていない Pod に通信が流れて 503 が増えます。更新中に利用可能な Pod の数を保ち、問題があれば前の版に戻せるようにします。適切な組み合わせはどれですか。

- A. Liveness プローブを追加して異常な Pod を再起動させ、問題があれば `kubectl delete deployment` で作り直す
- B. `strategy.type` を `Recreate` にして、古い Pod をすべて止めてから新しい Pod を起動し、新旧の混在をなくす
- C. CodeDeploy エージェントを各ノードに導入し、Pod の入れ替えを任せる
- D. Readiness プローブと `maxUnavailable`、`maxSurge` を設定し、問題があれば `kubectl rollout undo` を実行する

??? success "答えと解説"
    **正解: D**

    Readiness プローブが通るまで通信は流れません。ローリング更新の幅を指定し、`rollout undo` で戻します。

    - A: 誤り。Liveness は再起動の判断で通信の振り分けに使われず、削除は前の版への復旧にならない。
    - B: 誤り。更新中に全 Pod が止まり、利用可能な数を保てない。
    - C: 誤り。EKS の Deployment の更新に CodeDeploy エージェントは使わない。
    - D: 正しい。

    **スキル:** [デプロイ方式](../domain1.md#t1-4-methods) / **参照:** [マニフェストとローリング更新](../../../services/containers.md#eks-manifests)、[ヘルスチェックとプローブ](../../../services/containers.md#probes)

### 問5 {#q5}

コンテナで動くアプリで、障害の調査のために本番のコンテナへ入ってライブラリを更新する運用があり、タスクが置き換わると修正が消えて問題が再発します。イミュータブルの考え方に沿った対応はどれですか。

- A. 修正を Dockerfile に入れて新しいイメージを作り、タスク定義の新しいリビジョンでデプロイする
- B. ECS Exec の利用者を増やし、すべてのタスクへ同じコマンドを実行するスクリプトを用意して運用する
- C. タスクの停止を禁止するため、サービスの Auto Scaling を無効にして、手で修正したタスクを保つ
- D. コンテナのファイルシステムを EFS にして、修正したファイルを次のタスクでも使えるようにする

??? success "答えと解説"
    **正解: A**

    コンテナでは動いているものを変更せず、新しいイメージで置き換えます。

    - A: 正しい。
    - B: 誤り。動いているものを直接変える運用のままになる。
    - C: 誤り。問題を隠すだけで、可用性も下がる。
    - D: 誤り。変更がイメージの外に蓄積し、再現性を失う。

    **スキル:** [ミュータブルとイミュータブル](../domain1.md#t1-4-mutable-immutable) / **参照:** [タグと不変タグ](../../../services/containers.md#image-tags)、[デプロイ](../../../services/containers.md#ecs-deployments)

### 問6 {#q6}

ECS の更新で新しいタスクが起動と停止を繰り返し、デプロイが何時間も完了しません。タスクの停止理由には `CannotPullContainerError` が出ています。デプロイは失敗として止め、前の版へ自動で戻してほしいと考えています。適切な組み合わせはどれですか。（2つ選択）

- A. タスクロールに ECR の権限を追加して、アプリのコードから取得するように変える
- B. イメージの取得元の URI とタスク実行ロールの権限、経路を確認する
- C. ターゲットグループのヘルスチェックの猶予期間を延ばす
- D. サービスのタスク数を増やし、起動に成功するタスクが出るまで試行を増やす
- E. デプロイサーキットブレーカーとロールバックを有効にする

??? success "答えと解説"
    **正解: B, E**

    取得の失敗は実行ロールか経路が原因です。サーキットブレーカーを有効にすれば、起動できないデプロイを止めて戻せます。

    - A: 誤り。取得に使うのはタスク実行ロールで、コードでの取得にもならない。
    - B: 正しい。
    - C: 誤り。起動の前の取得の失敗なので、猶予期間は関係ない。
    - D: 誤り。取得の問題は再試行では直らず、失敗の数が増える。
    - E: 正しい。

    **スキル:** [デプロイの問題の解決](../domain1.md#t1-4-troubleshooting) / **参照:** [デプロイ失敗の診断](../../../services/cicd.md#troubleshooting-deployments)、[デプロイサーキットブレーカー](../../../services/containers.md#circuit-breaker)

### 問7 {#q7}

新しい Web API をコンテナで動かします。Kubernetes の経験者はおらず、ノードの OS のパッチは運用したくありません。AWS の他のサービスと統合しやすいことも条件です。デプロイは Blue/Green を使います。どれが最も適切ですか。

- A. EKS のマネージドノードグループ
- B. ECS と Fargate
- C. ROSA のクラスター
- D. ECS と EC2 起動タイプ、毎週のパッチの運用

??? success "答えと解説"
    **正解: B**

    AWS に統合された形で運用を簡単にするなら ECS、サーバーの管理をなくすなら Fargate です。

    - A: 誤り。Kubernetes の知識が必要で、ノードの運用も残る。
    - B: 正しい。
    - C: 誤り。OpenShift の要件がなく、経験者もいない。
    - D: 誤り。OS のパッチの運用が残る。

    **スキル:** [コンテナ](../domain3.md#t3-2-containers) / **参照:** [Fargate と EC2](../../../services/containers.md#fargate-vs-ec2)、[ECS](../../../services/containers.md#ecs)

### 問8 {#q8}

すでに Helm のチャートと Kubernetes の運用の経験があり、Pod の起動の順番を調整して、準備のできていない Pod に通信を流しません。AWS の中でコントロールプレーンの運用を任せます。適切な組み合わせはどれですか。

- A. EKS と Readiness プローブ
- B. ECS とタスク定義の `dependsOn`
- C. App Runner と自動スケーリング
- D. EKS Distro を自社のサーバーで動かし、Liveness プローブだけを使う

??? success "答えと解説"
    **正解: A**

    Kubernetes の API が必要なら EKS です。通信の振り分けは Readiness プローブで制御します。

    - A: 正しい。
    - B: 誤り。Kubernetes の資産を活かせない。
    - C: 誤り。Kubernetes の資産を使えない。
    - D: 誤り。コントロールプレーンを AWS に任せられず、通信の制御もできない。

    **スキル:** [コンテナ](../domain3.md#t3-2-containers) / **参照:** [ヘルスチェックとプローブ](../../../services/containers.md#probes)、[EKS](../../../services/containers.md#eks)

### 問9 {#q9}

3 つのチームの要件があります。(1) 既存の OpenShift の資産を AWS のマネージド環境で使う。(2) データセンターで、EKS と同じ Kubernetes の配布版を動かす。(3) 新規の案件で、シンプルなマネージドのコンテナの基盤を使う。このアカウントはこれまで App Runner を使ったことがなく、App Runner は新規の利用者の受付を終了しています。適切な組み合わせはどれですか。

- A. (1) ROSA、(2) EKS Distro、(3) ECS と Fargate
- B. (1) EKS のマネージドノード、(2) ECS Anywhere、(3) App Runner
- C. (1) ROSA、(2) ROSA、(3) App Runner
- D. (1) Copilot、(2) EKS Distro、(3) ROSA

??? success "答えと解説"
    **正解: A**

    OpenShift は ROSA、自社環境で同じ配布版を動かすのは EKS Distro です。App Runner は既存の利用者だけが使えるので、新規の案件では ECS を選びます。

    - A: 正しい。
    - B: 誤り。OpenShift の資産を活かせず、配布版の要件にも合わない。
    - C: 誤り。EKS Distro の用途を満たせず、新規の利用者が受付を終了した App Runner を選んでいる。
    - D: 誤り。Copilot はサポートが終了している。

    **スキル:** [コンテナ](../domain3.md#t3-2-containers) / **参照:** [Red Hat OpenShift Service on AWS (ROSA)](../../../services/operations.md#rosa)、[Amazon EKS Distro](../../../services/operations.md#eks-distro)、[AWS App Runner](../../../services/other-services.md#app-runner)

### 問10 {#q10}

ECS（EC2 起動）のサービスイベントに `unable to place a task` が出ています。別のサービスでは、イメージの取得の失敗が繰り返されています。確認先の組み合わせはどれですか。（2つ選択）

- A. ターゲットグループのヘルスチェックの猶予期間としきい値
- B. タスクロールの ECR の権限と、アプリの SDK の再試行の設定
- C. タスク実行ロールの権限と ECR への経路
- D. Application Auto Scaling の最大タスク数とクールダウン
- E. 配置の制約とクラスターの CPU、メモリの容量

??? success "答えと解説"
    **正解: C, E**

    `unable to place a task` は配置の制約や容量、イメージ取得の失敗は実行ロールや経路です。

    - A: 誤り。ヘルスチェックは配置と起動の後の判定で、配置や取得の失敗の確認先ではない。
    - B: 誤り。イメージの取得に使うのはタスク実行ロールで、SDK の再試行はアプリの起動後の話。
    - C: 正しい。
    - D: 誤り。タスク数の目標の設定で、置けない原因の容量や制約は分からない。
    - E: 正しい。

    **スキル:** [プロセスの障害](../domain5.md#t5-3-failed-processes) / **参照:** [タスクの配置](../../../services/containers.md#task-placement)、[デプロイサーキットブレーカー](../../../services/containers.md#circuit-breaker)

### 問11 {#q11}

EKS の Pod の状態を確認します。(1) `Pending` のまま。(2) 新しいイメージのデプロイの後に `CrashLoopBackOff`。適切な調査の組み合わせはどれですか。

- A. (1) Fargate プロファイルを追加してノードを増やす、(2) ALB のヘルスチェックの間隔を延ばして再起動を抑える
- B. (1) `ImagePullBackOff` と同じとみて ECR の権限と経路を確認する、(2) クラスターの Kubernetes のバージョンを更新して様子を見る
- C. (1) `kubectl describe pod` でイベントを確認する、(2) `kubectl logs --previous` で終了の原因を確認する
- D. (1) `kubectl logs --previous` でコンテナのログを確認する、(2) ノードグループの最大サイズを増やす

??? success "答えと解説"
    **正解: C**

    `Pending` はスケジュール待ちで、ノードの不足などの理由は `describe` のイベントに出ます。`CrashLoopBackOff` は起動後の異常終了の繰り返しで、設定やプローブの誤りを前回のログで確かめます。

    - A: 誤り。`Pending` の原因を確かめておらず、`CrashLoopBackOff` は ALB の間隔では直らない。
    - B: 誤り。`Pending` は取得の失敗とは別の状態で、(2) も原因の調査にならない。
    - C: 正しい。
    - D: 誤り。(1) はまだ起動していないのでログがなく、(2) はノードの不足を示さない。

    **スキル:** [プロセスの障害](../domain5.md#t5-3-failed-processes) / **参照:** [ヘルスチェックとプローブ](../../../services/containers.md#probes)、[EKS](../../../services/containers.md#eks)

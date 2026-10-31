# スケーリングの問題集

対象の解説: [スケーリング](../../../services/resilience.md#auto-scaling-ha)

### 問1 {#q1}

SQS のワーカーを ECS で動かします。処理は I/O 待ちが多く、CPU が上がらないのでキューが溜まり続けます。1 タスクあたり 100 件のバックログを保つようにスケールします。適切な指標はどれですか。

- A. `ApproximateNumberOfMessagesVisible` をタスク数で割った値
- B. `NumberOfMessagesDeleted` の 1 分の合計値
- C. ECS サービスの `CPUUtilization` のターゲット追跡の目標値を 10% に下げた値
- D. ALB の `ALBRequestCountPerTarget` の値

??? success "答えと解説"
    **正解: A**

    実際に限界になる指標でスケールします。ターゲットあたりのバックログをメトリクス計算かカスタムメトリクスで作ります。

    - A: 正しい。
    - B: 誤り。処理できた数で、溜まっている量を表さない。
    - C: 誤り。I/O 待ちの処理の負荷を CPU では正しく表せない。
    - D: 誤り。キューのワーカーは ALB のリクエストを受けない。

    **スキル:** [スケーリングの指標](../domain3.md#t3-2-metrics) / **参照:** [EC2 Auto Scaling](../../../services/ec2-beanstalk.md#auto-scaling)、[メトリクス計算](../../../services/observability.md#metric-math)

### 問2 {#q2}

Web アプリは 1 リクエストの処理の負荷がほぼ同じで、CPU の使用率は低いままなのに接続数の上限で遅くなります。ALB の後ろの EC2 Auto Scaling で、最も適切なターゲット追跡の指標はどれですか。

- A. `HTTPCode_ELB_5XX_Count` の 1 分の合計
- B. `NetworkOut` の平均
- C. `ALBRequestCountPerTarget`
- D. `CPUUtilization` の平均

??? success "答えと解説"
    **正解: C**

    リクエスト数に比例する負荷には `ALBRequestCountPerTarget` が向きます。

    - A: 誤り。エラーの指標で、容量の指標ではない。
    - B: 誤り。応答のサイズに左右され、リクエスト数の負荷を表さない。
    - C: 正しい。
    - D: 誤り。問題文のとおり CPU は限界の指標ではない。

    **スキル:** [スケーリングの指標](../domain3.md#t3-2-metrics) / **参照:** [EC2 Auto Scaling](../../../services/ec2-beanstalk.md#auto-scaling)、[ALB と NLB の違い](../../../services/networking.md#alb-vs-nlb)

### 問3 {#q3}

ストリーム処理の負荷の増大を監視します。(1) Lambda が Kinesis のレコードの処理に追いつかない。(2) プロデューサーの書き込みがシャードの上限を超えている。(3) 関数の同時実行の余裕がない。それぞれの指標の組み合わせはどれですか。

- A. (1) `Errors`、(2) `ReadProvisionedThroughputExceeded`、(3) `DeadLetterErrors`
- B. (1) `ConcurrentExecutions`、(2) `IteratorAge`、(3) `IncomingBytes`
- C. (1) `IteratorAge`、(2) `WriteProvisionedThroughputExceeded`、(3) `ConcurrentExecutions` と `Throttles`
- D. (1) `Duration`、(2) `IncomingRecords`、(3) `Invocations`

??? success "答えと解説"
    **正解: C**

    遅れは `IteratorAge`、書き込みの超過は `WriteProvisionedThroughputExceeded` です。

    - A: 誤り。(2) は読み取りの超過で、他も指標の用途が違う。
    - B: 誤り。指標の対象が入れ違っている。
    - C: 正しい。
    - D: 誤り。どれも直接の指標にならない。

    **スキル:** [スケーリングの指標](../domain3.md#t3-2-metrics) / **参照:** [Lambda の既定メトリクス](../../../services/observability.md#lambda-metrics)、[エラーと監視](../../../services/streaming.md#kinesis-errors)

### 問4 {#q4}

朝 9 時に毎日、負荷が急増します。インスタンスの起動に 8 分かかり、ピークに間に合いません。起動に時間がかかるのは初期化のデータの読み込みが大半です。負荷は平日に周期的です。費用を抑えて間に合わせる組み合わせはどれですか。（2つ選択）

- A. ウォームプールで初期化済みのインスタンスを停止状態で待機させる
- B. 予測スケーリングで周期の負荷に先回りする
- C. ターゲット追跡の目標値を 90% に上げて、急増の検知を遅らせる
- D. ヘルスチェックの猶予期間を 0 秒に短くする
- E. 全インスタンスを固定の最大台数で 24 時間動かす

??? success "答えと解説"
    **正解: A, B**

    起動に時間がかかる場合はウォームプールが有効です。周期の負荷には予測スケーリングが向きます。

    - A: 正しい。
    - B: 正しい。
    - C: 誤り。スケールが遅くなり逆効果。
    - D: 誤り。起動が速くならず、誤って異常と判定される。
    - E: 誤り。費用を抑えるという条件に反する。

    **スキル:** [スケーリングの問題](../domain3.md#t3-2-scaling-issues) / **参照:** [ウォームプール](../../../services/operations.md#warm-pools)、[予測スケーリング](../../../services/operations.md#predictive-scaling)

### 問5 {#q5}

CLI で作った Auto Scaling グループで、インスタンスが起動と終了を繰り返しています。アプリの起動に 3 分かかります。`describe-scaling-activities` では ELB ヘルスチェックの失敗が理由になっています。修正はどれですか。

- A. ヘルスチェックの猶予期間を 180 秒より長くする
- B. ターゲット追跡の目標値を下げて、インスタンスを増やす
- C. ALB をやめて、EC2 のステータスチェックだけで判定する
- D. `max` の台数を増やして、置き換えの余裕を作る

??? success "答えと解説"
    **正解: A**

    CLI の既定の猶予期間は 0 秒です。起動中に異常と判定されないよう、起動時間より長くします。

    - A: 正しい。
    - B: 誤り。繰り返しの原因を解決しない。
    - C: 誤り。アプリの異常に気づかなくなる。
    - D: 誤り。起動中に異常と判定される問題が残る。

    **スキル:** [スケーリングの問題](../domain3.md#t3-2-scaling-issues) / **参照:** [スケーリングの失敗の調査](../../../services/operations.md#asg-troubleshooting)、[ヘルスチェック](../../../services/ec2-beanstalk.md#asg-health-checks)

### 問6 {#q6}

負荷テストで次の結果が出ました。(1) DynamoDB でテーブル全体の容量には余裕があるのに `ThrottlingException` が出る。(2) Kinesis の 1 つのシャードだけ `WriteProvisionedThroughputExceeded` が出る。両方に共通する原因と対策はどれですか。

- A. リージョンの障害で、別のリージョンへ切り替える
- B. キーの偏りで、パーティションキーの設計を見直す
- C. SDK の再試行の不足で、再試行の回数を 100 回に増やす
- D. 全体の容量の不足で、プロビジョンドの容量やシャード数を一律に倍にする

??? success "答えと解説"
    **正解: B**

    どちらも特定のキーへの集中が典型の原因です。キーを分散させます。

    - A: 誤り。容量の偏りの典型の症状で、障害を示していない。
    - B: 正しい。
    - C: 誤り。再試行だけでは偏りを解消できない。
    - D: 誤り。全体には余裕があり、偏りが残る限り解決しない。

    **スキル:** [スケーリングの問題](../domain3.md#t3-2-scaling-issues) / **参照:** [スロットリング](../../../services/dynamodb.md#throttling)、[エラーと監視](../../../services/streaming.md#kinesis-errors)

### 問7 {#q7}

EC2 の Web 層のスケーリングのポリシーを決めます。(1) 基本は CPU 50% を保つ。(2) 毎週金曜 18 時のセールの前に必ず 30 台へ増やす。(3) 超過の幅が大きいときに一度に多く増やす方式は、ターゲット追跡の代わりに使える。組み合わせはどれですか。

- A. (1) 予測、(2) ステップ、(3) ターゲット追跡
- B. (1) ステップ、(2) 予測、(3) スケジュール
- C. (1) ターゲット追跡、(2) スケジュール、(3) ステップ
- D. (1) スケジュール、(2) ターゲット追跡、(3) シンプルスケーリング

??? success "答えと解説"
    **正解: C**

    値を保つならターゲット追跡、決まった時間ならスケジュール、超過の大きさで変えるならステップです。

    - A: 誤り。指定の時刻に増やすのはスケジュールの役割。
    - B: 誤り。値を保つならターゲット追跡が基本で、(3) はステップの説明。
    - C: 正しい。
    - D: 誤り。(1) と (2) の役割が逆。

    **スキル:** [Auto Scaling とキャッシュ](../domain3.md#t3-2-autoscaling-caching) / **参照:** [ステップスケーリングの調整](../../../services/ec2-beanstalk.md#step-adjustments)、[予測スケーリング](../../../services/operations.md#predictive-scaling)

### 問8 {#q8}

次のキャッシュを選びます。(1) DynamoDB のマイクロ秒の読み取りを、アプリの変更を少なく実現する。(2) RDS の複雑なクエリの結果をアプリ側で一時的に保存する。(3) グローバルな利用者への静的コンテンツ。適切な組み合わせはどれですか。

- A. (1) DAX、(2) ElastiCache、(3) CloudFront
- B. (1) API Gateway のキャッシュ、(2) CloudFront、(3) ElastiCache
- C. (1) CloudFront、(2) S3 Transfer Acceleration、(3) DAX
- D. (1) ElastiCache、(2) DAX、(3) API Gateway のキャッシュ

??? success "答えと解説"
    **正解: A**

    DynamoDB の手前は DAX、アプリとデータベースの間は ElastiCache、利用者の近くは CloudFront です。

    - A: 正しい。
    - B: 誤り。置く場所と対象が合わない。
    - C: 誤り。それぞれ目的が違う。
    - D: 誤り。DAX は DynamoDB 専用で、(3) も静的コンテンツの配信に向かない。

    **スキル:** [Auto Scaling とキャッシュ](../domain3.md#t3-2-autoscaling-caching) / **参照:** [DAX、ElastiCache、CloudFront の使い分け](../../../services/databases.md#cache-comparison)、[キャッシュ](../../../services/api-gateway.md#caching)

### 問9 {#q9}

費用の最適化を進めます。条件は次のとおりです。過大なインスタンスの候補を見つける。未使用の EIP やロードバランサーも確認する。常時動く分は安くする。中断に耐えるワーカーも安くする。適切な組み合わせはどれですか。

- A. CloudTrail と Config、オンデマンドとキャパシティ予約
- B. Cost Anomaly Detection と Config、Reserved Instances と Dedicated Hosts
- C. Compute Optimizer と Trusted Advisor、Savings Plans とスポット
- D. Inspector と Detective、Savings Plans とオンデマンド

??? success "答えと解説"
    **正解: C**

    過大の候補は Compute Optimizer、未使用は Trusted Advisor、常時の分は Savings Plans、中断に耐える分はスポットです。

    - A: 誤り。候補の特定の道具ではなく、節約にならない。
    - B: 誤り。前の 2 つは候補の特定の道具ではなく、後の 2 つも中断に耐えるワーカーの節約に向かない。
    - C: 正しい。
    - D: 誤り。候補の特定の道具ではなく、ワーカーの節約にもならない。

    **スキル:** [Auto Scaling とキャッシュ](../domain3.md#t3-2-autoscaling-caching) / **参照:** [Compute Optimizer と適正サイズ](../../../services/cost-management.md#compute-optimizer)、[購入オプション](../../../services/cost-management.md#purchase-options)、[Trusted Advisor](../../../services/cloud-foundations.md#trusted-advisor)

### 問10 {#q10}

EC2 起動の ECS で、タスク数の増加に対してインスタンスが追いつかず、タスクが `PROVISIONING` のままです。アプリのバックログに応じてタスクを増やし、インスタンスも必要な分だけ増やします。適切な組み合わせはどれですか。

- A. タスク数は Application Auto Scaling、インスタンスはキャパシティプロバイダーのマネージドスケーリング
- B. タスク数は Karpenter、インスタンスは Cluster Autoscaler
- C. タスク数は EC2 Auto Scaling、インスタンスは Application Auto Scaling
- D. タスク数は手動、インスタンスは予測スケーリングだけ

??? success "答えと解説"
    **正解: A**

    ECS サービスのタスク数は Application Auto Scaling、クラスターの EC2 はキャパシティプロバイダーで増やします。

    - A: 正しい。
    - B: 誤り。どちらも Kubernetes の仕組みで、ECS に使わない。
    - C: 誤り。対象が逆。
    - D: 誤り。タスクが増えず、バックログに追従しない。

    **スキル:** [Auto Scaling](../domain4.md#t4-3-auto-scaling) / **参照:** [キャパシティプロバイダー](../../../services/containers.md#capacity-providers)、[サービスの Auto Scaling](../../../services/containers.md#service-auto-scaling)

### 問11 {#q11}

RDS のストレージの Auto Scaling は有効ですが、大量のデータロードの途中でストレージがいっぱいになりました。上限の `MaxAllocatedStorage` には余裕があります。原因の説明と対策として適切なものはどれですか。

- A. 上限に余裕があるので自動で無限に増える。ログの誤りなので再実行する
- B. 変更の後の最適化の間などは拡張されないので、ロードの前に容量を増やす
- C. 自動の拡張は Multi-AZ で使えないので、Single-AZ へ変更する
- D. 自動の拡張はストレージを減らす機能が前提なので、ロードの後で自動で減る設定を有効にする

??? success "答えと解説"
    **正解: B**

    空きが 10% 以下、5 分以上、前回の最適化の完了などの条件があります。大量のロードでは間に合わないことがあります。

    - A: 誤り。変更後の最適化の完了や回数の制限で、増えないことがある。
    - B: 正しい。
    - C: 誤り。そのような制約の問題ではない。
    - D: 誤り。割り当てた容量は減らせない。

    **スキル:** [Auto Scaling](../domain4.md#t4-3-auto-scaling) / **参照:** [RDS](../../../services/databases.md#rds)

### 問12 {#q12}

次の 2 つの要件で、スケーリングの手段を選びます。(1) DynamoDB のプロビジョンドのテーブルで、読み書きの増加に容量を追従させる。(2) EKS で、ノードの作成と削除を AWS に任せ、Pod の要件に合うインスタンスを柔軟に使う。適切な組み合わせはどれですか。

- A. (1) Application Auto Scaling、(2) EKS Auto Mode
- B. (1) EC2 Auto Scaling、(2) Cluster Autoscaler
- C. (1) DAX の追加、(2) ECS のキャパシティプロバイダー
- D. (1) Lambda の予約済み同時実行、(2) Horizontal Pod Autoscaler

??? success "答えと解説"
    **正解: A**

    DynamoDB のプロビジョンドは Application Auto Scaling です。EKS のノードの運用を任せるなら Auto Mode です。

    - A: 正しい。
    - B: 誤り。DynamoDB に EC2 Auto Scaling は使えず、(2) は既存のノードグループを活かす手段。
    - C: 誤り。DAX はキャッシュで、(2) は ECS の機能。
    - D: 誤り。同時実行は容量の管理ではなく、HPA は Pod の数の制御。

    **スキル:** [Auto Scaling](../domain4.md#t4-3-auto-scaling) / **参照:** [プロビジョンドと Auto Scaling](../../../services/dynamodb.md#provisioned-auto-scaling)、[EKS](../../../services/containers.md#eks)

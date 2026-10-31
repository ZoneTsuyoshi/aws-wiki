# CloudWatch メトリクスとアラームの問題集

対象の解説: [CloudWatch メトリクスとアラーム](../../../services/observability.md#cloudwatch-metrics)

### 問1 {#q1}

EC2 のアプリで次を見ます。(1) メモリとディスクの使用率。(2) リクエストがどのサービスで遅くなるか。(3) 利用者の視点でのログインの可用性を定期的に確認する。(4) サービスの SLO の達成状況。手段の組み合わせはどれですか。

- A. (1) 標準メトリクス、(2) CloudTrail、(3) Config、(4) Inspector
- B. (1) CloudWatch エージェント、(2) X-Ray、(3) Synthetics、(4) Application Signals
- C. (1) X-Ray、(2) CloudWatch エージェント、(3) RUM、(4) Trusted Advisor
- D. (1) Inspector、(2) Synthetics、(3) Application Signals、(4) Macie

??? success "答えと解説"
    **正解: B**

    見たいものごとに手段を分けます。

    - A: 誤り。標準メトリクスにメモリはなく、他も目的が違う。
    - B: 正しい。
    - C: 誤り。(1) と (2) が逆で、RUM は実際の利用者のデータを見る。
    - D: 誤り。目的が違う。

    **スキル:** [監視](../domain4.md#t4-1-monitoring) / **参照:** [ロギング、モニタリング、オブザーバビリティの違い](../../../services/observability.md#logging-monitoring-observability)、[Application Signals](../../../services/observability.md#application-signals)

### 問2 {#q2}

EKS で Prometheus の指標をすでに使っています。自前の Prometheus と Grafana の運用をなくし、CloudWatch とも同じ画面で見ます。適切な組み合わせはどれですか。

- A. CloudWatch の詳細モニタリングとダッシュボードだけに移し、Prometheus の指標はやめる
- B. OpenSearch Service と Quick Sight で指標を集める
- C. EC2 に Prometheus と Grafana を立てて、Auto Scaling で冗長にする
- D. Amazon Managed Service for Prometheus と Amazon Managed Grafana

??? success "答えと解説"
    **正解: D**

    Prometheus の指標は Managed Service for Prometheus、複数のソースの可視化は Managed Grafana です。

    - A: 誤り。既存の指標を捨てることになる。
    - B: 誤り。Prometheus の指標のマネージドな置き場にならない。
    - C: 誤り。自前の運用が残る。
    - D: 正しい。

    **スキル:** [監視](../domain4.md#t4-1-monitoring) / **参照:** [Amazon Managed Service for Prometheus](../../../services/operations.md#managed-prometheus)、[Amazon Managed Grafana](../../../services/operations.md#managed-grafana)

### 問3 {#q3}

EKS と ECS のコンテナごとの CPU とメモリ、および Web の利用者のページ読み込みの体験を見ます。自前の指標の計算は避けます。適切な組み合わせはどれですか。

- A. Inspector と Synthetics
- B. Container Insights と CloudWatch RUM
- C. Application Auto Scaling と CloudFront のアクセスログ
- D. X-Ray と CloudTrail

??? success "答えと解説"
    **正解: B**

    コンテナの状態は Container Insights、ブラウザでの体験は RUM です。

    - A: 誤り。Inspector は脆弱性のスキャンで、Synthetics は実際の利用者の体験を測らない。
    - B: 正しい。
    - C: 誤り。指標を見る仕組みではなく、ページの読み込みも測らない。
    - D: 誤り。コンテナの資源の指標にも、ブラウザの体験にもならない。

    **スキル:** [監視](../domain4.md#t4-1-monitoring) / **参照:** [CloudWatch RUM](../../../services/operations.md#rum)、[EKS](../../../services/containers.md#eks)

### 問4 {#q4}

CloudWatch エージェントでインスタンスごとのメモリを送っています。Auto Scaling グループ全体の平均で見たいのに、`AutoScalingGroupName` でグラフを作れません。エージェントの設定でどう直しますか。

- A. `force_flush_interval` を増やして、送信をまとめる
- B. `aggregation_dimensions` で `AutoScalingGroupName` を指定する
- C. 名前空間を `AWS/EC2` に変更する
- D. `metrics_collection_interval` を 1 秒に短くして、詳細なデータを送る

??? success "答えと解説"
    **正解: B**

    ディメンションが違うと別のメトリクスです。エージェントの `aggregation_dimensions` で追加の集計を指定します。

    - A: 誤り。送信の間隔で、集計の軸は変わらない。
    - B: 正しい。
    - C: 誤り。`AWS/` の名前空間はカスタムメトリクスに使わず、集計の軸も変わらない。
    - D: 誤り。収集の間隔で、集計の軸は変わらない。

    **スキル:** [メトリクスの基本](../domain4.md#t4-1-metrics) / **参照:** [基本の用語](../../../services/observability.md#metrics-concepts)、[CloudWatch エージェント](../../../services/operations.md#cloudwatch-agent)

### 問5 {#q5}

CloudWatch のメトリクスの保持について、1 分のデータを 1 年後に確認しようとすると、どう見えますか。また、3 年分の分析を残すにはどうしますか。

- A. 3 時間で消える。3 年分は高解像度に変える
- B. 5 分の粒度で見える。3 年分は詳細モニタリングを有効にする
- C. 1 分の粒度のまま 15 か月保持される。3 年分はメトリクスの保持の設定で延ばす
- D. 1 時間の粒度で見える。3 年分はメトリクスストリームなどで S3 へ流す

??? success "答えと解説"
    **正解: D**

    60 秒のデータは 15 日、300 秒は 63 日、3,600 秒は 455 日です。15 か月より長く残すなら S3 へ流します。

    - A: 誤り。3 時間は 60 秒未満のデータの期間。
    - B: 誤り。5 分は 63 日までで、監視の粒度の設定は保持を延ばさない。
    - C: 誤り。粒度は集約され、保持の延長の設定もない。
    - D: 正しい。

    **スキル:** [メトリクスの基本](../domain4.md#t4-1-metrics) / **参照:** [解像度と保持期間](../../../services/observability.md#metrics-resolution)

### 問6 {#q6}

決済のエラーを 10 秒周期で検知するアラームを作ります。アプリは `PutMetricData` で送っています。必要な設定の組み合わせはどれですか。（2つ選択）

- A. アラームの `Period` を 10 秒にする
- B. メトリクスフィルターのデフォルト値を 0 にする
- C. EC2 の詳細モニタリングを有効にする
- D. `PutMetricData` の `StorageResolution` を 1 にして高解像度で送る
- E. 標準の解像度のまま送り、アラームの `Period` を 10 秒にする

??? success "答えと解説"
    **正解: A, D**

    高解像度のアラームには元のメトリクスの高解像度が必要です。

    - A: 正しい。
    - B: 誤り。欠落の扱いで、周期を短くしない。
    - C: 誤り。EC2 の標準メトリクスの話で、カスタムメトリクスの解像度を変えない。
    - D: 正しい。
    - E: 誤り。元のメトリクスも高解像度にする必要がある。

    **スキル:** [メトリクスの基本](../domain4.md#t4-1-metrics) / **参照:** [解像度と保持期間](../../../services/observability.md#metrics-resolution)、[PutMetricData でカスタムメトリクスを送る](../../../services/observability.md#put-metric-data)

### 問7 {#q7}

全アカウントの CloudWatch メトリクスを、ほぼリアルタイムで Datadog へ送ります。自作のポーリングは避けます。監視アカウントから一括で流します。何を使いますか。

- A. 監視アカウントのメトリクスストリームで、ソースアカウントのメトリクスを含める
- B. アラームを全メトリクスに作り、SNS で状態の変化を送る
- C. Lambda で `GetMetricData` を 1 分ごとに呼び、結果を API で送る
- D. `get-metric-statistics` の結果を S3 に毎日置いて、Datadog に読ませる

??? success "答えと解説"
    **正解: A**

    メトリクスストリームは継続して流します。監視アカウントのストリームにソースアカウントのメトリクスを含められます。

    - A: 正しい。
    - B: 誤り。値そのものを送る仕組みにならない。
    - C: 誤り。自作のポーリングで、遅れと費用も出る。
    - D: 誤り。ほぼリアルタイムではない。

    **スキル:** [メトリクスストリーム](../domain4.md#t4-1-metric-streams) / **参照:** [2026 年 10 月時点の提供状況](../../../services/operations.md#status)、[Amazon Data Firehose](../../../services/streaming.md#firehose)

### 問8 {#q8}

CloudWatch のメトリクスを Firehose 経由で S3 へ流し、3 年分を Athena で分析します。名前空間のうち `AWS/EC2` と `AWS/RDS` だけに絞ります。独自の統計も増やしません。適切な設定はどれですか。

- A. 包含のフィルターに `AWS/EC2` と `AWS/RDS` を指定し、形式は JSON にする
- B. フィルターは指定せず、形式を OpenTelemetry 0.7.0 にすれば名前空間が自動で絞られる
- C. 包含のフィルターに全名前空間を指定して、Firehose の変換で捨てる
- D. 除外のフィルターに `AWS/EC2` と `AWS/RDS` を指定し、包含と併用する

??? success "答えと解説"
    **正解: A**

    1 つのストリームには包含か除外のどちらかだけを置きます。

    - A: 正しい。
    - B: 誤り。形式は絞り込みをしない。
    - C: 誤り。不要な更新の費用がかかる。
    - D: 誤り。除外では逆の動きになり、包含と除外の併用もできない。

    **スキル:** [メトリクスストリーム](../domain4.md#t4-1-metric-streams) / **参照:** [Amazon Data Firehose](../../../services/streaming.md#firehose)、[Amazon Athena](../../../services/streaming.md#athena)

### 問9 {#q9}

メトリクスストリームを検討中のチームの発言のうち、正しいものはどれですか。（2つ選択）

- A. メトリクスストリームの宛先は CloudTrail Lake だけである
- B. メトリクス計算の結果も自動で計算して流される
- C. 料金はメトリクスの更新数と Firehose の費用がかかる
- D. `Minimum`、`Maximum`、`SampleCount`、`Sum` が常に含まれる
- E. 少数のメトリクスをたまに取得するなら、ポーリングよりストリームが必ず安い

??? success "答えと解説"
    **正解: C, D**

    ストリームの料金と標準の統計を押さえます。少数をたまに取得するならポーリングのほうが向きます。

    - A: 誤り。Firehose 経由で S3 などへ流す。
    - B: 誤り。ストリームの統計の対象の説明に合わない。
    - C: 正しい。
    - D: 正しい。
    - E: 誤り。その場合は `GetMetricData` のほうが向く。

    **スキル:** [メトリクスストリーム](../domain4.md#t4-1-metric-streams) / **参照:** [Amazon Data Firehose](../../../services/streaming.md#firehose)、[メトリクス計算](../../../services/observability.md#metric-math)

### 問10 {#q10}

500 台の EC2 のメモリ使用率を CloudWatch で見ます。設定は全台で揃え、新しいインスタンスにも自動で入れます。SSH で入る作業はしません。適切な手順はどれですか。

- A. 各サーバーへ SSH で入り、ウィザードを 1 台ずつ実行する
- B. 詳細モニタリングを全台で有効にして、メモリの指標を発行する
- C. `UserData` に長いスクリプトを書き、変更のたびに全インスタンスを作り直す
- D. 設定を Parameter Store に置き、`AWS-ConfigureAWSPackage` と State Manager で導入と適用を行う

??? success "答えと解説"
    **正解: D**

    エージェントの設定は Parameter Store で共有し、導入は Systems Manager で行います。

    - A: 誤り。SSH で入らないという条件に反する。
    - B: 誤り。詳細モニタリングは 1 分の粒度で、メモリは含まれない。
    - C: 誤り。変更のたびに入れ替えが必要で、既存の 500 台に適用されない。
    - D: 正しい。

    **スキル:** [カスタムメトリクス](../domain4.md#t4-1-custom-metrics) / **参照:** [EC2 の既定メトリクスとエージェント](../../../services/observability.md#ec2-metrics)、[CloudWatch エージェント](../../../services/operations.md#cloudwatch-agent)

### 問11 {#q11}

Lambda で注文の金額と処理の時間をメトリクスとして残します。同じ内容をログでも見られるようにします。呼び出しのたびの `PutMetricData` の遅延と API の呼び出しは避けます。適切な手段はどれですか。

- A. Embedded Metric Format で構造化ログに書く
- B. X-Ray のアノテーションに値を入れて、メトリクスとして見る
- C. 関数の中で `PutMetricData` を同期で呼び、1 件ごとに待つ
- D. CloudWatch エージェントを関数のレイヤーで動かして、メモリを送る

??? success "答えと解説"
    **正解: A**

    EMF はログからメトリクスを自動で抽出します。呼び出しの追加は要りません。

    - A: 正しい。
    - B: 誤り。アノテーションはトレースの検索用で、メトリクスにならない。
    - C: 誤り。遅延と API の呼び出しが増える。
    - D: 誤り。関数には向かず、業務の値も送れない。

    **スキル:** [カスタムメトリクス](../domain4.md#t4-1-custom-metrics) / **参照:** [Embedded Metric Format (EMF)](../../../services/observability.md#emf)、[PutMetricData でカスタムメトリクスを送る](../../../services/observability.md#put-metric-data)

### 問12 {#q12}

カスタムメトリクスをサービス、環境、顧客 ID の 3 つのディメンションで `PutMetricData` しています。顧客が 10 万人いて、メトリクスの費用が急増しました。適切な見直しはどれですか。

- A. 全メトリクスに異常検知を追加して、使われていないメトリクスを自動で消す
- B. 高解像度に変更して、1 秒ごとに送るようにする
- C. 顧客 ID を維持したまま、名前空間だけを変更する
- D. 顧客 ID をディメンションから外し、顧客別の分析はログで行う

??? success "答えと解説"
    **正解: D**

    ディメンションの値の組み合わせごとに別のメトリクスになり、課金されます。

    - A: 誤り。異常検知はメトリクスを消さない。
    - B: 誤り。さらに費用が増える。
    - C: 誤り。メトリクスの数は変わらない。
    - D: 正しい。

    **スキル:** [カスタムメトリクス](../domain4.md#t4-1-custom-metrics) / **参照:** [PutMetricData の全パラメータ](../../../services/observability.md#put-metric-data-params)、[基本の用語](../../../services/observability.md#metrics-concepts)

### 問13 {#q13}

受注の数は平日の昼に多く、夜と週末に少なくなります。固定のしきい値のアラームでは、夜の急減に気づけません。季節性に合わせて自動で判定します。また、運用チームは、これを Auto Scaling のアクションに使おうとしています。正しい判断はどれですか。

- A. ログの異常検知を使い、Auto Scaling のグループに `CPUUtilization` のしきい値を指定する
- B. 異常検知のアラームを使うが、Auto Scaling のアクションは付けられない
- C. 固定のしきい値を時間帯ごとに 24 個のアラームで作り、Auto Scaling のアクションにも使う
- D. 複合アラームで昼と夜を組み合わせて、Auto Scaling のアクションにも使う

??? success "答えと解説"
    **正解: B**

    異常検知は過去のデータから帯を学習します。ただし Auto Scaling のアクションは付けられません。

    - A: 誤り。メトリクスの判定にならず、問題の解決にもならない。
    - B: 正しい。
    - C: 誤り。手間が増え、周期の変化にも追従しない。
    - D: 誤り。学習による判定にならない。

    **スキル:** [異常検知](../domain4.md#t4-2-anomaly) / **参照:** [異常検知](../../../services/observability.md#anomaly-detection)

### 問14 {#q14}

異常検知のアラームを本番で使い始めましたが、深夜のメンテナンスの時間帯にも鳴ります。メンテナンスの時間のデータで学習の帯も広がっています。どうしますか。

- A. モデルの除外期間にメンテナンスの時間を指定する
- B. 異常検知のしきい値の帯を最大の幅に広げ続ける
- C. アラームを削除して、メトリクスを Datadog にだけ流す
- D. メトリクスの解像度を 1 秒に上げて学習を増やす

??? success "答えと解説"
    **正解: A**

    学習から外す期間を指定できます。特殊な時間帯を除くと帯が正しくなります。

    - A: 正しい。
    - B: 誤り。検知の感度が落ちるだけで、原因を解決しない。
    - C: 誤り。検知の仕組みを失う。
    - D: 誤り。除外の問題を解決しない。

    **スキル:** [異常検知](../domain4.md#t4-2-anomaly) / **参照:** [異常検知](../../../services/observability.md#anomaly-detection)、[評価の仕組みと M out of N](../../../services/observability.md#alarm-evaluation)

### 問15 {#q15}

ログイン数が低いのに通知が届きません。アラームは異常検知の帯の「上限より大きい」で設定されています。担当者は急減も検知したいと考えています。また、エラー率が同時に高いときだけページングします。適切な組み合わせはどれですか。（2つ選択）

- A. メトリクスの統計を `Maximum` に変更する
- B. アラームの `DatapointsToAlarm` を 0 にする
- C. 複合アラームで異常検知とエラー率のアラームを AND で組み合わせる
- D. 比較の演算子を「帯の下限より小さい」か「帯の外」にする
- E. 帯の幅を 0 にして、少しの変化で必ず鳴らす

??? success "答えと解説"
    **正解: C, D**

    帯の下側を判定するよう演算子を選びます。組み合わせは複合アラームで書きます。

    - A: 誤り。急減の検知の条件を変えない。
    - B: 誤り。有効な設定ではない。
    - C: 正しい。
    - D: 正しい。
    - E: 誤り。誤報が増え、演算子の問題も残る。

    **スキル:** [異常検知](../domain4.md#t4-2-anomaly) / **参照:** [異常検知](../../../services/observability.md#anomaly-detection)、[複合アラーム](../../../services/observability.md#composite-alarms)

### 問16 {#q16}

ALB の `HTTPCode_ELB_5XX_Count` だけが増え、`HTTPCode_Target_5XX_Count` は増えていません。アプリのログにエラーは出ていません。まず何を調べますか。

- A. CloudFront のキャッシュのヒット率とオリジンの設定
- B. アプリのコードの例外とスタックトレース
- C. 正常なターゲットの有無、接続の失敗、ターゲットの応答のタイムアウト
- D. ターゲットのインスタンスの EBS の `VolumeQueueLength`

??? success "答えと解説"
    **正解: C**

    `ELB_5XX` は ALB 自身が返すエラーです。正常なターゲットや接続を確認します。

    - A: 誤り。ALB が返すエラーの調査の最初の対象ではない。
    - B: 誤り。アプリが 500 を返すなら Target のメトリクスが増える。
    - C: 正しい。
    - D: 誤り。アプリがエラーを返していないので、最初の対象ではない。

    **スキル:** [よく使うメトリクス](../domain4.md#t4-2-common-metrics) / **参照:** [代表的なメトリクスと原因](../../../services/observability.md#bottleneck-metrics)、[ALB のエラーコード](../../../services/networking.md#alb-errors)

### 問17 {#q17}

次の状況でメトリクスを選びます。(1) RDS で I/O が追いつかず、書き込みが待たされている。(2) SQS の処理が遅れている。(3) EC2 の OS がハングしている。適切な組み合わせはどれですか。

- A. (1) `FreeableMemory`、(2) `SentMessageSize`、(3) `NetworkIn`
- B. (1) `DiskQueueDepth`、(2) `ApproximateAgeOfOldestMessage`、(3) `StatusCheckFailed_Instance`
- C. (1) `CPUCreditBalance`、(2) `NumberOfMessagesSent`、(3) `StatusCheckFailed_System`
- D. (1) `DatabaseConnections`、(2) `NumberOfEmptyReceives`、(3) `CPUUtilization`

??? success "答えと解説"
    **正解: B**

    症状と指標を対応させて覚えます。

    - A: 誤り。いずれも症状の指標ではない。
    - B: 正しい。
    - C: 誤り。直接の指標ではなく、(3) は AWS 側の問題の指標。
    - D: 誤り。接続数や空の受信は、それぞれの原因を示さない。

    **スキル:** [よく使うメトリクス](../domain4.md#t4-2-common-metrics) / **参照:** [ステータスチェック](../../../services/operations.md#status-checks)、[代表的なメトリクスと原因](../../../services/observability.md#bottleneck-metrics)

### 問18 {#q18}

夜間の API の遅延を調査します。`TargetResponseTime` は正常ですが、利用者は遅いと報告しています。別の Lambda の処理では `Throttles` が増え、`Errors` は増えていません。正しい読み方はどれですか。

- A. ALB の負荷の問題なので Auto Scaling を増やす。Lambda はタイムアウトを延ばす
- B. RDS の問題なので Multi-AZ を有効にする。Lambda は `/tmp` を増やす
- C. ターゲットが遅いのでアプリを最適化する。Lambda はコードの例外を調べる
- D. ALB より前の区間を確認する。Lambda は同時実行の不足を調べる

??? success "答えと解説"
    **正解: D**

    `TargetResponseTime` はターゲットの遅さを示します。`Throttles` は同時実行の上限によるものです。

    - A: 誤り。ターゲットは遅くなく、スロットルにタイムアウトは効かない。
    - B: 誤り。根拠がなく、指標と関係がない。
    - C: 誤り。応答時間は正常で、スロットルは例外とは別に数えられる。
    - D: 正しい。

    **スキル:** [よく使うメトリクス](../domain4.md#t4-2-common-metrics) / **参照:** [Lambda の既定メトリクス](../../../services/observability.md#lambda-metrics)、[ALB のエラーコード](../../../services/networking.md#alb-errors)

### 問19 {#q19}

運用チームは、全アカウント、全リージョンの主要な API のエラー率とアラームを 1 つの画面で見ます。ログインのない来客用の画面にも特定のダッシュボードを見せます。適切な手段はどれですか。

- A. リージョンごとに Quick Sight のアカウントを作り、毎週の PDF を来客と運用チームに配る
- B. 各アカウントのコンソールのタブをブラウザで並べて開く
- C. クロスアカウント対応の CloudWatch ダッシュボードと、ダッシュボードの共有
- D. CloudTrail のイベント履歴を画面に映す

??? success "答えと解説"
    **正解: C**

    CloudWatch ダッシュボードは複数のリージョンとアカウントを扱えます。共有の設定もあります。

    - A: 誤り。運用の監視に向かず、リアルタイムでもない。
    - B: 誤り。運用の手間が大きく、1 つの画面にもならない。
    - C: 正しい。
    - D: 誤り。メトリクスとアラームの表示にならない。

    **スキル:** [ダッシュボード](../domain4.md#t4-2-dashboards) / **参照:** [ダッシュボードの設定](../../../services/observability.md#dashboard-settings)

### 問20 {#q20}

経営層向けに、ALB のアクセスログから月別の利用者数と地域別の傾向を示すレポートを作ります。ログは S3 にあります。自動で更新し、IT の担当者でなくても操作します。適切な構成はどれですか。

- A. Athena でテーブルにし、Quick Sight で可視化する
- B. Lambda で毎日 HTML を作り、S3 の静的ウェブサイトで公開する
- C. X-Ray のサービスマップと Trace Map を共有する
- D. CloudWatch ダッシュボードにログの全行を表示して、スクリーンショットを配る

??? success "答えと解説"
    **正解: A**

    ログを Athena でテーブルにし、Quick Sight で可視化するのが定番です。

    - A: 正しい。
    - B: 誤り。独自の実装で、操作もできない。
    - C: 誤り。ログの分析ではなく、ビジネスのレポートにならない。
    - D: 誤り。ビジネスの分析に向かない。

    **スキル:** [ダッシュボード](../domain4.md#t4-2-dashboards) / **参照:** [Amazon Quick Sight](../../../services/data-engineering.md#quick-sight)、[S3 上のログを問い合わせる](../../../services/streaming.md#athena-logs)

### 問21 {#q21}

CloudWatch、Prometheus、Athena のデータを 1 枚で見たいチームと、CloudWatch のアラームの状態を見るだけのチームがあります。それぞれに適切な手段はどれですか。

- A. 前者は Live Tail、後者は Athena
- B. 前者は Security Hub のダッシュボード、後者は Trusted Advisor のチェックの画面
- C. 前者は Quick Sight の埋め込み、後者は CloudTrail の検索
- D. 前者は Managed Grafana、後者は CloudWatch ダッシュボード

??? success "答えと解説"
    **正解: D**

    複数のソースの可視化は Managed Grafana、CloudWatch の範囲ならダッシュボードで足ります。

    - A: 誤り。どちらも画面の要件に合わない。
    - B: 誤り。目的が違う。
    - C: 誤り。運用のメトリクスの画面にならず、後者は目的が違う。
    - D: 正しい。

    **スキル:** [ダッシュボード](../domain4.md#t4-2-dashboards) / **参照:** [Amazon Managed Grafana](../../../services/operations.md#managed-grafana)、[ダッシュボードの設定](../../../services/observability.md#dashboard-settings)

### 問22 {#q22}

CPU が一瞬だけ跳ね上がるたびにアラームが鳴ります。1 分周期のメトリクスで、直近 5 分のうち 3 回超えたときだけ鳴らします。設定はどれですか。

- A. `EvaluationPeriods` 5、`DatapointsToAlarm` 3、`Period` 60
- B. `EvaluationPeriods` 1、`DatapointsToAlarm` 1、`Period` 300
- C. `EvaluationPeriods` 3、`DatapointsToAlarm` 5、`Period` 60
- D. `EvaluationPeriods` 5、`DatapointsToAlarm` 5、`Period` 60

??? success "答えと解説"
    **正解: A**

    M out of N で、一時的な値では鳴らないようにします。

    - A: 正しい。
    - B: 誤り。5 分の平均の判定で、3 回の条件にならない。
    - C: 誤り。`DatapointsToAlarm` が `EvaluationPeriods` を超えており、設定が逆。
    - D: 誤り。5 回すべての条件になり、要件より厳しい。

    **スキル:** [アラーム](../domain4.md#t4-2-alarms) / **参照:** [評価の仕組みと M out of N](../../../services/observability.md#alarm-evaluation)

### 問23 {#q23}

エラーの「数」のアラームでは、利用者の多い時間に誤報が増えます。エラー率が 5% を超えたときに鳴らします。夜間のバッチはデータが欠落するので、欠落では鳴らしません。適切な組み合わせはどれですか。

- A. メトリクス計算の `Errors / Invocations` で判定し、`treatMissingData` を `notBreaching` にする
- B. `Invocations` のしきい値で判定して、`treatMissingData` を `missing` にする
- C. 異常検知で `Errors` を判定し、`treatMissingData` を `ignore` にする
- D. `Errors` の数のしきい値を時間帯ごとに手で変更し、`treatMissingData` を `breaching` にして欠落も検知する

??? success "答えと解説"
    **正解: A**

    計算した値で判定できます。間欠の処理は `notBreaching` が向きます。

    - A: 正しい。
    - B: 誤り。エラーの比率にならない。
    - C: 誤り。比率の要件に合わない。`ignore` も状態を保つ動きで、要件と異なる。
    - D: 誤り。手間がかかり、欠落でも鳴ってしまう。

    **スキル:** [アラーム](../domain4.md#t4-2-alarms) / **参照:** [メトリクス計算](../../../services/observability.md#metric-math)、[欠落データの扱い](../../../services/observability.md#treat-missing-data)

### 問24 {#q24}

1 つの障害で、API のエラー、遅延、キューの滞留の 3 つのアラームが同時に鳴り、当番に 3 回の通知が届きます。通知を 1 回に減らし、個別のアラームの履歴は残します。適切な方法はどれですか。

- A. SNS のトピックに購読のフィルターを追加し、3 回の通知のうち 2 回を捨てる
- B. 個別のアラームのアクションを外し、複合アラームから SNS へ通知する
- C. 個別のアラームを削除して、1 つのメトリクスだけを監視する
- D. 個別のアラームの評価の周期を 1 時間に延ばす

??? success "答えと解説"
    **正解: B**

    複合アラームで条件を組み合わせ、通知を減らします。

    - A: 誤り。3 つのアラームの関係を判定できない。
    - B: 正しい。
    - C: 誤り。検知の範囲が狭まり、履歴も失う。
    - D: 誤り。検知が遅くなるだけ。

    **スキル:** [アラーム](../domain4.md#t4-2-alarms) / **参照:** [複合アラーム](../../../services/observability.md#composite-alarms)、[アラームのアクション](../../../services/observability.md#alarm-actions)

### 問25 {#q25}

EBS ベースの EC2 で、`StatusCheckFailed_System` と `StatusCheckFailed_Instance` のアラームに自動の対応を付けます。適切な組み合わせはどれですか。

- A. どちらも SNS の通知だけにして、夜間は翌朝に対応する
- B. システムは `reboot` で再起動し、インスタンスは `recover` で別のホストへ移す
- C. どちらも `terminate` にして、作り直しは手で行う
- D. システムは `recover`、インスタンスは `reboot`

??? success "答えと解説"
    **正解: D**

    AWS 側の問題は別のホストへ復旧、OS の問題は再起動で対応します。

    - A: 誤り。自動の対応の要件を満たさない。
    - B: 誤り。AWS 側の問題と OS の問題で対応が逆。
    - C: 誤り。手作業が残り、ID なども失う。
    - D: 正しい。

    **スキル:** [アラート](../domain4.md#t4-3-alerts) / **参照:** [ステータスチェック](../../../services/operations.md#status-checks)、[アラームのアクション](../../../services/observability.md#alarm-actions)

### 問26 {#q26}

EC2 の自動復旧を設定した担当者が、「復旧後も何も失わない」と説明しています。正しい理解はどれですか。

- A. インスタンス ID などは保たれるが、メモリの内容とインスタンスストアのデータは失われる
- B. インスタンス ID が変わるので、ALB のターゲットグループへの再登録が必要になる
- C. EBS の内容も失われるので、復旧の後はスナップショットからの復元が必要になる
- D. インスタンス ID も IP もメモリの内容もすべて保たれるので、アプリの再起動も要らない

??? success "答えと解説"
    **正解: A**

    復旧ではインスタンス ID などを保ちます。メモリの内容とインスタンスストアのデータは失われます。

    - A: 正しい。
    - B: 誤り。ID は保たれる。
    - C: 誤り。EBS のデータは残る。
    - D: 誤り。メモリの内容は失われる。

    **スキル:** [アラート](../domain4.md#t4-3-alerts) / **参照:** [ステータスチェック](../../../services/operations.md#status-checks)、[アラームのアクション](../../../services/observability.md#alarm-actions)

### 問27 {#q27}

アプリのログの `PAYMENT_FAILED` を数え、1 分に 10 件を超えたら当番へ通知し、運用の記録も残して、修復の Lambda も動かします。追加のサーバーは使いません。流れとして適切なものはどれですか。

- A. EC2 に cron を置いて、`filter-log-events` の結果でメールする
- B. X-Ray のアノテーションで数えて、SNS へ直接送る
- C. Logs Insights を毎分手で実行して、件数を確認したら担当者へ電話する
- D. メトリクスフィルター、アラーム、SNS と Lambda、OpsItem の作成

??? success "答えと解説"
    **正解: D**

    ログをメトリクスにしてアラームを作り、アクションで通知と修復を動かします。

    - A: 誤り。サーバーの運用が増える。
    - B: 誤り。アノテーションは通知の仕組みにならない。
    - C: 誤り。自動の流れにならない。
    - D: 正しい。

    **スキル:** [アラート](../domain4.md#t4-3-alerts) / **参照:** [通知アラートの実装](../../../services/observability.md#alerts)、[メトリクスフィルター](../../../services/observability.md#metric-filters)、[OpsCenter](../../../services/operations.md#opscenter)

### 問28 {#q28}

インターネットに出られないサブネットの EC2 を Systems Manager で管理します。ノードが Fleet Manager に出てきません。AMI には SSM Agent が入っています。必要なものの組み合わせはどれですか。（2つ選択）

- A. インスタンスのロールに `AmazonSSMManagedInstanceCore`
- B. SSH の 22 番を VPC のエンドポイントから許可するセキュリティグループのルール
- C. CloudWatch エージェントの設定を Parameter Store に保存する作業
- D. `ssm`、`ssmmessages`、`ec2messages` の VPC エンドポイント
- E. EC2 の Elastic IP と公開サブネットへの移動

??? success "答えと解説"
    **正解: A, D**

    インターネットに出られないサブネットでは VPC エンドポイントを使います。

    - A: 正しい。
    - B: 誤り。SSM Agent は SSH を使わない。
    - C: 誤り。CloudWatch の話で、SSM の登録に必要ない。
    - D: 正しい。
    - E: 誤り。インターネットに出られないという前提を変え、必須でもない。

    **スキル:** [エージェント](../domain4.md#t4-3-agents) / **参照:** [マネージドノードの条件](../../../services/operations.md#managed-nodes)、[VPC エンドポイントと PrivateLink](../../../services/networking.md#vpc-endpoints)

### 問29 {#q29}

新しいインスタンスに CloudWatch エージェントが自動で入らず、起動の直後のログが欠けます。AMI を再度作る時間はありません。全社の既存の Auto Scaling グループにも適用します。適切な方法はどれですか。

- A. 全台を Lambda へ移行して、エージェントを不要にする
- B. 担当者がインスタンスの起動の通知を受けて、Run Command を都度手で実行し、結果を記録する
- C. ALB のアクセスログを有効にして、代わりにログを確保する
- D. State Manager の関連付けで、タグが一致するノードに導入と設定の適用を行う

??? success "答えと解説"
    **正解: D**

    State Manager の関連付けなら、新しいノードにも適用されます。

    - A: 誤り。変更が大きすぎる。
    - B: 誤り。手作業が残る。
    - C: 誤り。アプリのログの代わりにならない。
    - D: 正しい。

    **スキル:** [エージェント](../domain4.md#t4-3-agents) / **参照:** [CloudWatch エージェント](../../../services/operations.md#cloudwatch-agent)、[State Manager](../../../services/operations.md#state-manager)

### 問30 {#q30}

SSM Agent と CloudWatch エージェントの違いについて、正しい説明はどれですか。

- A. SSM Agent を入れれば、追加の設定なしでメモリのメトリクスが自動で CloudWatch へ送られる
- B. どちらも同じロールの権限 `AmazonEC2ReadOnlyAccess` で動く
- C. SSM Agent は Systems Manager の操作を受け、CloudWatch エージェントは指標とログを送る
- D. CloudWatch エージェントを入れれば、Run Command の実行先になる

??? success "答えと解説"
    **正解: C**

    役割と必要な権限が別です。

    - A: 誤り。メモリのメトリクスには CloudWatch エージェントが必要。
    - B: 誤り。それぞれ専用の権限が必要になる。
    - C: 正しい。
    - D: 誤り。Run Command の実行には SSM Agent が必要。

    **スキル:** [エージェント](../domain4.md#t4-3-agents) / **参照:** [マネージドノードの条件](../../../services/operations.md#managed-nodes)、[CloudWatch エージェント](../../../services/operations.md#cloudwatch-agent)

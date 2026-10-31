# 分野4: CloudWatch メトリクスとアラーム

メトリクスの読み方と、誤報を減らす判定、自動の対応を問います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [監視](../../domain4.md#t4-1-monitoring) | アプリとインフラの監視の方法 |
| [メトリクスの基本](../../domain4.md#t4-1-metrics) | CloudWatch メトリクス |
| [メトリクスストリーム](../../domain4.md#t4-1-metric-streams) | メトリクスストリーム |
| [カスタムメトリクス](../../domain4.md#t4-1-custom-metrics) | カスタムメトリクスの収集 |
| [異常検知](../../domain4.md#t4-2-anomaly) | 異常検知アラーム |
| [よく使うメトリクス](../../domain4.md#t4-2-common-metrics) | よく使うメトリクスとログ |
| [ダッシュボード](../../domain4.md#t4-2-dashboards) | ダッシュボードと Quick Sight |
| [アラーム](../../domain4.md#t4-2-alarms) | アラームとメトリクスの関連付け |
| [アラート](../../domain4.md#t4-3-alerts) | アラートの通知とアクション、カスタムメトリクス、フィルター、アラーム、通知 |
| [エージェント](../../domain4.md#t4-3-agents) | エージェントの導入と設定 |

## 学習の順番 {#study-order}

1. [解像度と保持期間](../../../../services/observability.md#metrics-resolution): 粒度ごとの保持を覚えます。
2. [CloudWatch エージェント](../../../../services/operations.md#cloudwatch-agent): エージェントの導入と `aggregation_dimensions` を確認します。
3. [Embedded Metric Format (EMF)](../../../../services/observability.md#emf): ログからメトリクスを作る方法を確認します。
4. [異常検知](../../../../services/observability.md#anomaly-detection): 帯の学習と制約を押さえます。
5. [評価の仕組みと M out of N](../../../../services/observability.md#alarm-evaluation): M out of N の設定を理解します。
6. [複合アラーム](../../../../services/observability.md#composite-alarms): 通知を減らす方法を確認します。
7. [ステータスチェック](../../../../services/operations.md#status-checks): システムとインスタンスのチェックの違いを覚えます。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| 60 秒未満のデータ | 3 時間 | 高解像度 |
| 60 秒のデータ | 15 日 | |  |
| 300 秒のデータ | 63 日 | |  |
| 3,600 秒のデータ | 455 日 | 15 か月より長くは S3 へ |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| メモリとディスクを見る | CloudWatch エージェント |
| メトリクスを外部へほぼリアルタイムで送る | メトリクスストリーム |
| 5 分のうち 3 回で鳴らす | `EvaluationPeriods` 5、`DatapointsToAlarm` 3 |
| 間欠のバッチで誤って鳴る | `treatMissingData` を `notBreaching` |
| `ELB_5XX` だけが増える | 正常なターゲットと接続を確認する |
| AWS 側の問題で自動で直す | `StatusCheckFailed_System` と `recover` |

## 引っかかりやすい点 {#traps}

- 異常検知のアラームには Auto Scaling のアクションを付けられません。
- ディメンションの値の組み合わせごとに別のメトリクスになり、課金されます。
- 1 つのメトリクスストリームには包含か除外のどちらかだけを置きます。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [cloudwatch-metrics 問1](../../exercises/cloudwatch-metrics.md#q1) | 監視 | EC2 のアプリで次を見ます。(1) メモリとディスクの使用率。(2) リクエストがどのサービスで遅… |
| [cloudwatch-metrics 問2](../../exercises/cloudwatch-metrics.md#q2) | 監視 | EKS で Prometheus の指標をすでに使っています。自前の Prometheus と Gr… |
| [cloudwatch-metrics 問3](../../exercises/cloudwatch-metrics.md#q3) | 監視 | EKS と ECS のコンテナごとの CPU とメモリ、および Web の利用者のページ読み込みの体… |
| [cloudwatch-metrics 問4](../../exercises/cloudwatch-metrics.md#q4) | メトリクスの基本 | CloudWatch エージェントでインスタンスごとのメモリを送っています。Auto Scaling… |
| [cloudwatch-metrics 問5](../../exercises/cloudwatch-metrics.md#q5) | メトリクスの基本 | CloudWatch のメトリクスの保持について、1 分のデータを 1 年後に確認しようとすると、ど… |
| [cloudwatch-metrics 問6](../../exercises/cloudwatch-metrics.md#q6) | メトリクスの基本 | 決済のエラーを 10 秒周期で検知するアラームを作ります。アプリは PutMetricData で送… |
| [cloudwatch-metrics 問7](../../exercises/cloudwatch-metrics.md#q7) | メトリクスストリーム | 全アカウントの CloudWatch メトリクスを、ほぼリアルタイムで Datadog へ送ります。… |
| [cloudwatch-metrics 問8](../../exercises/cloudwatch-metrics.md#q8) | メトリクスストリーム | CloudWatch のメトリクスを Firehose 経由で S3 へ流し、3 年分を Athen… |
| [cloudwatch-metrics 問9](../../exercises/cloudwatch-metrics.md#q9) | メトリクスストリーム | メトリクスストリームを検討中のチームの発言のうち、正しいものはどれですか。（2つ選択） |
| [cloudwatch-metrics 問10](../../exercises/cloudwatch-metrics.md#q10) | カスタムメトリクス | 500 台の EC2 のメモリ使用率を CloudWatch で見ます。設定は全台で揃え、新しいイン… |
| [cloudwatch-metrics 問11](../../exercises/cloudwatch-metrics.md#q11) | カスタムメトリクス | Lambda で注文の金額と処理の時間をメトリクスとして残します。同じ内容をログでも見られるようにし… |
| [cloudwatch-metrics 問12](../../exercises/cloudwatch-metrics.md#q12) | カスタムメトリクス | カスタムメトリクスをサービス、環境、顧客 ID の 3 つのディメンションで PutMetricDa… |
| [cloudwatch-metrics 問13](../../exercises/cloudwatch-metrics.md#q13) | 異常検知 | 受注の数は平日の昼に多く、夜と週末に少なくなります。固定のしきい値のアラームでは、夜の急減に気づけま… |
| [cloudwatch-metrics 問14](../../exercises/cloudwatch-metrics.md#q14) | 異常検知 | 異常検知のアラームを本番で使い始めましたが、深夜のメンテナンスの時間帯にも鳴ります。メンテナンスの時… |
| [cloudwatch-metrics 問15](../../exercises/cloudwatch-metrics.md#q15) | 異常検知 | ログイン数が低いのに通知が届きません。アラームは異常検知の帯の「上限より大きい」で設定されています。… |
| [cloudwatch-metrics 問16](../../exercises/cloudwatch-metrics.md#q16) | よく使うメトリクス | ALB の HTTPCode_ELB_5XX_Count だけが増え、HTTPCode_Target… |
| [cloudwatch-metrics 問17](../../exercises/cloudwatch-metrics.md#q17) | よく使うメトリクス | 次の状況でメトリクスを選びます。(1) RDS で I/O が追いつかず、書き込みが待たされている。… |
| [cloudwatch-metrics 問18](../../exercises/cloudwatch-metrics.md#q18) | よく使うメトリクス | 夜間の API の遅延を調査します。TargetResponseTime は正常ですが、利用者は遅い… |
| [cloudwatch-metrics 問19](../../exercises/cloudwatch-metrics.md#q19) | ダッシュボード | 運用チームは、全アカウント、全リージョンの主要な API のエラー率とアラームを 1 つの画面で見ま… |
| [cloudwatch-metrics 問20](../../exercises/cloudwatch-metrics.md#q20) | ダッシュボード | 経営層向けに、ALB のアクセスログから月別の利用者数と地域別の傾向を示すレポートを作ります。ログは… |
| [cloudwatch-metrics 問21](../../exercises/cloudwatch-metrics.md#q21) | ダッシュボード | CloudWatch、Prometheus、Athena のデータを 1 枚で見たいチームと、Clo… |
| [cloudwatch-metrics 問22](../../exercises/cloudwatch-metrics.md#q22) | アラーム | CPU が一瞬だけ跳ね上がるたびにアラームが鳴ります。1 分周期のメトリクスで、直近 5 分のうち … |
| [cloudwatch-metrics 問23](../../exercises/cloudwatch-metrics.md#q23) | アラーム | エラーの「数」のアラームでは、利用者の多い時間に誤報が増えます。エラー率が 5% を超えたときに鳴ら… |
| [cloudwatch-metrics 問24](../../exercises/cloudwatch-metrics.md#q24) | アラーム | 1 つの障害で、API のエラー、遅延、キューの滞留の 3 つのアラームが同時に鳴り、当番に 3 回… |
| [cloudwatch-metrics 問25](../../exercises/cloudwatch-metrics.md#q25) | アラート | EBS ベースの EC2 で、StatusCheckFailed_System と StatusCh… |
| [cloudwatch-metrics 問26](../../exercises/cloudwatch-metrics.md#q26) | アラート | EC2 の自動復旧を設定した担当者が、「復旧後も何も失わない」と説明しています。正しい理解はどれです… |
| [cloudwatch-metrics 問27](../../exercises/cloudwatch-metrics.md#q27) | アラート | アプリのログの PAYMENT_FAILED を数え、1 分に 10 件を超えたら当番へ通知し、運用… |
| [cloudwatch-metrics 問28](../../exercises/cloudwatch-metrics.md#q28) | エージェント | インターネットに出られないサブネットの EC2 を Systems Manager で管理します。ノ… |
| [cloudwatch-metrics 問29](../../exercises/cloudwatch-metrics.md#q29) | エージェント | 新しいインスタンスに CloudWatch エージェントが自動で入らず、起動の直後のログが欠けます。… |
| [cloudwatch-metrics 問30](../../exercises/cloudwatch-metrics.md#q30) | エージェント | SSM Agent と CloudWatch エージェントの違いについて、正しい説明はどれですか。 |

<!-- questions:end -->

# 分野3: スケーリング

実際に限界になる指標を選び、スケールしない原因を切り分ける力を問います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [スケーリングの指標](../../domain3.md#t3-2-metrics) | スケーリングに適したメトリクス |
| [スケーリングの問題](../../domain3.md#t3-2-scaling-issues) | スケーリングの問題の特定と解消 |
| [Auto Scaling とキャッシュ](../../domain3.md#t3-2-autoscaling-caching) | Auto Scaling、負荷分散、キャッシュの実装 |

## 学習の順番 {#study-order}

1. [EC2 Auto Scaling](../../../../services/ec2-beanstalk.md#auto-scaling): ポリシーの種類を確認します。
2. [メトリクス計算](../../../../services/observability.md#metric-math): バックログの計算を理解します。
3. [ウォームプール](../../../../services/operations.md#warm-pools): 起動が遅いときの対策を押さえます。
4. [予測スケーリング](../../../../services/operations.md#predictive-scaling): 周期の負荷への先回りを確認します。
5. [スケーリングの失敗の調査](../../../../services/operations.md#asg-troubleshooting): 起動と終了の繰り返しの原因を覚えます。
6. [DAX、ElastiCache、CloudFront の使い分け](../../../../services/databases.md#cache-comparison): キャッシュを置く場所の違いを確認します。

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| I/O 待ちのキューのワーカー | ターゲットあたりのバックログ |
| リクエスト数に比例する負荷 | `ALBRequestCountPerTarget` |
| 周期のある負荷で起動が遅い | 予測スケーリングとウォームプール |
| 起動と終了を繰り返す | ヘルスチェックの猶予期間 |
| 全体に余裕があるのにスロットリング | キーの偏りを見直す |
| 過大なインスタンスの候補 | Compute Optimizer |

## 引っかかりやすい点 {#traps}

- CLI で作ると猶予期間の既定は 0 秒です。
- DAX は DynamoDB の専用で、RDS の手前には置けません。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [scaling 問1](../../exercises/scaling.md#q1) | スケーリングの指標 | SQS のワーカーを ECS で動かします。処理は I/O 待ちが多く、CPU が上がらないのでキュ… |
| [scaling 問2](../../exercises/scaling.md#q2) | スケーリングの指標 | Web アプリは 1 リクエストの処理の負荷がほぼ同じで、CPU の使用率は低いままなのに接続数の上… |
| [scaling 問3](../../exercises/scaling.md#q3) | スケーリングの指標 | ストリーム処理の負荷の増大を監視します。(1) Lambda が Kinesis のレコードの処理に… |
| [scaling 問4](../../exercises/scaling.md#q4) | スケーリングの問題 | 朝 9 時に毎日、負荷が急増します。インスタンスの起動に 8 分かかり、ピークに間に合いません。起動… |
| [scaling 問5](../../exercises/scaling.md#q5) | スケーリングの問題 | CLI で作った Auto Scaling グループで、インスタンスが起動と終了を繰り返しています。… |
| [scaling 問6](../../exercises/scaling.md#q6) | スケーリングの問題 | 負荷テストで次の結果が出ました。(1) DynamoDB でテーブル全体の容量には余裕があるのに T… |
| [scaling 問7](../../exercises/scaling.md#q7) | Auto Scaling とキャッシュ | EC2 の Web 層のスケーリングのポリシーを決めます。(1) 基本は CPU 50% を保つ。(… |
| [scaling 問8](../../exercises/scaling.md#q8) | Auto Scaling とキャッシュ | 次のキャッシュを選びます。(1) DynamoDB のマイクロ秒の読み取りを、アプリの変更を少なく実… |
| [scaling 問9](../../exercises/scaling.md#q9) | Auto Scaling とキャッシュ | 費用の最適化を進めます。条件は次のとおりです。過大なインスタンスの候補を見つける。未使用の EIP … |

<!-- questions:end -->

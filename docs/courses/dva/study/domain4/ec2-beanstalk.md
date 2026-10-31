# 分野4: EC2 と Beanstalk

EC2 Auto Scaling の調整、インスタンスのサイズの決め方、ヘルスチェックの設定が問われます。Beanstalk のデプロイポリシーなどは[分野3](../domain3/ec2-beanstalk.md)で扱います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [4.2.4](../../domain4.md#skill-4-2-4) | Beanstalk での X-Ray の有効化 |
| [4.2.5](../../domain4.md#skill-4-2-5) | Auto Scaling のヘルスチェック |
| [4.3.1](../../domain4.md#skill-4-3-1) | EC2 Auto Scaling |
| [4.3.2](../../domain4.md#skill-4-3-2) | メモリとコンピューティング能力 |

## 学習の順番 {#study-order}

1. [EC2 Auto Scaling](../../../../services/ec2-beanstalk.md#auto-scaling): ポリシーの種類と、メトリクスの選び方を学びます。
2. [容量の設定](../../../../services/ec2-beanstalk.md#asg-capacity): 最小、最大、希望の関係を確認します。
3. [クールダウン](../../../../services/ec2-beanstalk.md#asg-cooldown)と[ウォームアップ](../../../../services/ec2-beanstalk.md#instance-warmup): 台数が増えすぎる理由と防ぎ方を理解します。
4. [ヘルスチェック](../../../../services/ec2-beanstalk.md#asg-health-checks): ELB の有効化と、猶予期間の既定値を覚えます。
5. [インスタンスタイプ](../../../../services/ec2-beanstalk.md#instance-types)と[サイズの決め方](../../../../services/ec2-beanstalk.md#sizing): 計測からサイズを選ぶ手順を確認します。
6. [EC2 の既定メトリクスとエージェント](../../../../services/observability.md#ec2-metrics): 取得できる値と、エージェントが必要な値を分けます。
7. [ログと X-Ray の設定](../../../../services/ec2-beanstalk.md#logs-xray): Beanstalk のログの種類と X-Ray の設定を押さえます。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| Auto Scaling のクールダウン | 既定 300 秒 | 影響を強く受けるのはシンプルスケーリングです |
| ヘルスチェックの猶予期間 | コンソール 300 秒、CLI や SDK 0 秒 | 起動の遅いアプリでは CLI の既定値が問題になります |
| `DefaultInstanceWarmup` | 既定では無効 | ターゲット追跡とステップでは設定が強く勧められています |
| EC2 の監視間隔 | 基本 5 分、詳細 1 分 | 詳細にしてもメモリのメトリクスは増えません |
| Beanstalk のテールログ | 最後の 100 行、15 分で削除 | 残すならログの公開か CloudWatch Logs です |
| Beanstalk の `RetentionInDays` | 既定 7 | `StreamLogs` の既定は `false` です |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 負荷に応じて台数を調整したい、設定は簡単にしたい | ターゲット追跡を選び、`ASGAverageCPUUtilization` を 50 などに保ちます |
| 決まった時刻の負荷に備えたい | スケジュールを使います。周期的な負荷なら予測も候補です |
| キューの長さで EC2 を増減したい | インスタンスあたりのバックログをカスタムメトリクスにして、ターゲット追跡します |
| 起動直後の CPU 100% で台数が増えすぎる | `--default-instance-warmup 120` のようにウォームアップを設定します |
| 起動に 4 分かかるアプリが終了と起動を繰り返す | `--health-check-grace-period 300` にします |
| アプリが 500 を返し続けるのに置き換えられない | Auto Scaling で ELB ヘルスチェックを有効にします |
| メモリ使用率を監視したい | CloudWatch エージェントで `mem_used_percent` を送ります |
| T 系で `CPUCreditBalance` が尽きて遅くなる | 常に高負荷なら M や C に変えます |
| CPU 重視の処理、メモリ重視の処理のタイプを選ぶ | CPU は C、大きなヒープやインメモリキャッシュは R、X を選びます |
| Beanstalk のログを CloudWatch Logs に送りたい、X-Ray を使いたい | `StreamLogs: true` と `XRayEnabled: true` を設定します |

## 引っかかりやすい点 {#traps}

- **ポリシーを作ったのに台数が変わらない:** `MinSize` と `MaxSize` が同じ値です。
- **クールダウンを短くしたら台数が増えすぎた:** 新しいインスタンスが負荷を受ける前に、アラームがまた発火しています。
- **インスタンスを増やしたら DB につながらない:** 台数の分だけ接続も増えます。[接続プール](databases.md)の上限を確認します。
- **インスタンスを減らすとセッションが消える:** インスタンスはいつでも削除されるので、セッションは ElastiCache や DynamoDB に置きます。
- **`XRayEnabled` にしてもアプリのトレースが足りない:** この設定はデーモンを動かすだけで、アプリ側の計装は別に必要です。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [ec2-beanstalk 問2](../../exercises/ec2-beanstalk.md#q2) | 4.2.5 | 開発者は Auto Scaling グループを AWS CLI で作成し、ELB ヘルスチェックを有… |
| [ec2-beanstalk 問3](../../exercises/ec2-beanstalk.md#q3) | 4.3.1 | Auto Scaling グループに設定する内容について、シンプルスケーリングのクールダウンの説明と… |
| [ec2-beanstalk 問10](../../exercises/ec2-beanstalk.md#q10) | 4.1.4 | インスタンスのデプロイで、次の処理が実行される順序として正しいものはどれですか。 |
| [ec2-beanstalk 問11](../../exercises/ec2-beanstalk.md#q11) | 4.3.3 | ワーカー環境で 1 件の処理に約 10 分かかるジョブを実行しています。設定は既定のままで、同じメッ… |
| [ec2-beanstalk 問12](../../exercises/ec2-beanstalk.md#q12) | 4.3.3 | 毎晩のバッチをワーカー環境の cron.yaml で実行しようとしています。既存の SQS FIFO… |
| [ec2-beanstalk 問15](../../exercises/ec2-beanstalk.md#q15) | 4.1.2 | Beanstalk 環境のログについて、インスタンスが終了しても後で調査できるように残したいと考えて… |

<!-- questions:end -->

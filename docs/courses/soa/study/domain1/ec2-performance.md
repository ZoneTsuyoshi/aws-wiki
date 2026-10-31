# 分野1: EC2 と性能の最適化

推奨の出どころ、インスタンスの配置、ストレージとネットワークの組み合わせを問います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [1.3.1](../../domain1.md#skill-1-3-1) | コンピューティングの最適化 |
| [1.3.6](../../domain1.md#skill-1-3-6) | EC2 とストレージ、ネットワークの最適化 |

## 学習の順番 {#study-order}

1. [Compute Optimizer と適正サイズ](../../../../services/cost-management.md#compute-optimizer)と[推奨を出すサービスの違い](../../../../services/cost-management.md#recommendation-tools): データの条件と、推奨を出すサービスの違いを確認します。
2. [代表的なメトリクスと原因](../../../../services/observability.md#bottleneck-metrics)と[リソース使用量の最適化](../../../../services/observability.md#resource-optimization): 症状とメトリクスを結びます。
3. [同時実行とスケーリング](../../../../services/lambda.md#concurrency): メモリ、CPU、同時実行の関係を確認します。
4. [プレイスメントグループ](../../../../services/operations.md#placement-groups): 3 つの戦略と上限を表で覚えます。
5. [インスタンスのトラブルシューティング](../../../../services/operations.md#instance-troubleshooting)と[MTU とジャンボフレーム](../../../../services/network-connectivity.md#mtu): 容量のエラーと MTU を確認します。
6. [インスタンスストア](../../../../services/storage-advanced.md#instance-store)、[スポットの中断への対応](../../../../services/operations.md#spot-interruptions)と[休止](../../../../services/operations.md#hibernate): 消えるデータ、中断の通知、休止の条件を確認します。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| Compute Optimizer の EC2 | 過去 14 日間に 30 時間以上 | データが足りないと推奨が出ない |
| スプレッド | AZ ごとに 7 台 | 少数の重要なインスタンス |
| パーティション | AZ ごとに 7 個 | HDFS、HBase、Cassandra |
| ジャンボフレーム | MTU 9001 | VPC の外は 1500 |
| スポットの中断 | 2 分前に通知 | ログの退避などに使う |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| CPU が低く費用が高い | 小さいタイプへ変更。推奨は Compute Optimizer |
| T 系のクレジットが尽きた | `unlimited` か M 系へ |
| Lambda の処理が CPU で遅い | メモリを増やす |
| ノード間の遅延を最小にする | クラスター |
| `InsufficientInstanceCapacity` | 同じタイプをまとめて起動、全台を止めて再開 |
| 最小の遅延で消えてよいデータ | インスタンスストア |

## 引っかかりやすい点 {#traps}

- Compute Optimizer はオプトインが必要です。
- 詳細モニタリングではメモリは増えません。
- 予約済み同時実行で CPU は増えません。
- 休止には起動時の有効化とルートボリュームの暗号化が必要です。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [ec2-performance 問1](../../exercises/ec2-performance.md#q1) | 1.3.1 | EC2 の適切なインスタンスタイプの推奨を、利用状況のメトリクスに基づいて得たいと考えています。これ… |
| [ec2-performance 問2](../../exercises/ec2-performance.md#q2) | 1.3.1 | Compute Optimizer の EC2 の推奨で、メモリも考慮してほしいと考えています。どう… |
| [ec2-performance 問3](../../exercises/ec2-performance.md#q3) | 1.3.1 | 次の要件と、使うツールの組み合わせとして正しいものを選んでください。（2つ選択） |
| [ec2-performance 問4](../../exercises/ec2-performance.md#q4) | 1.3.1 | t3.medium の Web サーバーが、CPU を使い続ける処理の間だけ遅くなります。クレジット… |
| [ec2-performance 問5](../../exercises/ec2-performance.md#q5) | 1.3.1 | Lambda の処理時間が長く、ログには CPU を使う処理が多いと表れています。外部の待ち時間はほ… |
| [ec2-performance 問6](../../exercises/ec2-performance.md#q6) | 1.3.1 | Env=dev のタグが付いた EC2 だけに診断のコマンドを実行します。対象は日々増減します。どの… |
| [ec2-performance 問7](../../exercises/ec2-performance.md#q7) | 1.3.6 | HPC のジョブで、ノード間の遅延を最小にしたいと考えています。どのプレイスメントグループを選びます… |
| [ec2-performance 問8](../../exercises/ec2-performance.md#q8) | 1.3.6 | 少数の重要なインスタンスを、ハードウェアの障害の影響を受けないように分けたいと考えています。1 つの… |
| [ec2-performance 問9](../../exercises/ec2-performance.md#q9) | 1.3.6 | クラスタープレイスメントグループへ追加で起動すると InsufficientInstanceCapa… |
| [ec2-performance 問10](../../exercises/ec2-performance.md#q10) | 1.3.6 | HBase のような分散ストアで、レプリカを別のハードウェアに分けたいと考えています。台数は 1 A… |
| [ec2-performance 問11](../../exercises/ec2-performance.md#q11) | 1.3.6 | 同じ VPC 内の EC2 の間でジャンボフレームを使っています。インターネット宛の通信で、大きなパ… |
| [ec2-performance 問12](../../exercises/ec2-performance.md#q12) | 1.3.6 | ML の分散学習で、ノード間の通信の性能を高くしたいです。どのネットワークの機能が目的に合っています… |
| [ec2-performance 問13](../../exercises/ec2-performance.md#q13) | 1.3.6 | 再生成できる一時データを扱うジョブで、最小の遅延のローカルストレージが必要です。インスタンスの停止で… |
| [ec2-performance 問14](../../exercises/ec2-performance.md#q14) | 1.3.6 | スポットの中断と休止について正しいものを選んでください。（2つ選択） |

<!-- questions:end -->

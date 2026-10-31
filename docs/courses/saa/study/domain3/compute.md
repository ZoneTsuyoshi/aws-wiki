# 分野3: コンピューティングとスケーリング

サービスの選択、スケーリングの指標、インスタンスとサイズを扱います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [コンピューティングサービスの選択](../../domain3.md#t3-2-compute-services) | コンピューティングサービスの適切な用途、サーバーレスの技術とパターン、コンテナのオーケストレーション |
| [グローバルインフラとエッジでの分散処理](../../domain3.md#t3-2-edge) | グローバルインフラとエッジサービスを使う分散コンピューティングの概念 |
| [スケーリングの機能](../../domain3.md#t3-2-auto-scaling) | スケーラビリティの機能の適切な用途 |
| [スケーリングの指標と条件](../../domain3.md#t3-2-metrics) | スケーリングのアクションを行う指標と条件の特定 |
| [インスタンスタイプと機能の選択](../../domain3.md#t3-2-instance) | 業務要件を満たすコンピューティングの選択肢と機能の選択 |
| [リソースのタイプとサイズ](../../domain3.md#t3-2-sizing) | 業務要件を満たすリソースのタイプとサイズの選択 |

## 学習の順番 {#study-order}

1. [AWS Batch](../../../../services/other-services.md#batch)と[Amazon EMR](../../../../services/data-engineering.md#emr): ジョブとデータ処理の選択を確認します。
2. [Lambda@Edge と CloudFront Functions](../../../../services/networking.md#edge-functions)と[Local Zones](../../../../services/cloud-foundations.md#local-zones): エッジと利用者の近くでの実行を比べます。
3. [EC2 Auto Scaling](../../../../services/ec2-beanstalk.md#auto-scaling)と[予測スケーリング](../../../../services/operations.md#predictive-scaling): ポリシーの種類と使いどころを押さえます。
4. [ウォームプール](../../../../services/operations.md#warm-pools)と[インスタンスのウォームアップ](../../../../services/ec2-beanstalk.md#instance-warmup): 起動が遅いときの対策と、ウォームアップを確認します。
5. [EC2 の既定メトリクスとエージェント](../../../../services/observability.md#ec2-metrics): 標準のメトリクスにないものを確認します。
6. [インスタンスタイプとメモリ、CPU の要件](../../../../services/ec2-beanstalk.md#instance-types)と[プレイスメントグループ](../../../../services/operations.md#placement-groups): ファミリーと配置の機能を覚えます。
7. [メモリ](../../../../services/lambda.md#memory)と[メモリと CPU の最適化](../../../../services/lambda.md#memory-tuning): メモリと CPU の関係を確認します。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| Lambda のメモリ | 128〜10,240 MB | 1,769 MB で 1 vCPU 相当 |
| Batch の配列ジョブ | 2〜10,000 | 多数のジョブを並べる |
| スプレッド | AZ ごとに 7 台 | 少数の重要なインスタンス |
| パーティション | AZ ごとに 7 パーティション | HDFS、Cassandra |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 15 分を超えるジョブを多数 | Batch |
| 既存の Spark | EMR |
| ヘッダーの書き換えを 1 ミリ秒未満で | CloudFront Functions |
| エッジでネットワーク接続が要る | Lambda@Edge |
| 決まった時刻の急増 | スケジュールされたアクション |
| 複数サービスのスケーリングを 1 か所で | AWS Auto Scaling のスケーリングプラン |
| SQS のワーカーをスケールする | インスタンスあたりのバックログ |
| ノード間の低遅延 | クラスタープレイスメントグループと EFA |

## 引っかかりやすい点 {#traps}

- 良い指標は、台数を 2 倍にすると半分になるものです。
- メモリの使用率には CloudWatch エージェントが必要です。
- CPU だけを増やす Lambda の設定はありません。
- T 系は `CPUCreditBalance` が尽きると制限されます。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [compute 問1](../../exercises/compute.md#q1) | コンピューティングの選択 | 数千の独立した計算ジョブを、キューとスケジューラーの管理なしで実行します。1 つのジョブは 2 時間… |
| [compute 問2](../../exercises/compute.md#q2) | コンピューティングの選択 | 既存の Spark のジョブを、クラスターの設定を細かく調整しながら移行します。どれを選びますか。 |
| [compute 問3](../../exercises/compute.md#q3) | コンピューティングの選択 | アプリのコードだけを用意し、キャパシティの設定やデプロイは簡単に任せます。OS には触れますが、環境… |
| [compute 問4](../../exercises/compute.md#q4) | コンピューティングの選択 | コンピューティングの選択として正しい組み合わせを選んでください。（2つ選択） |
| [compute 問5](../../exercises/compute.md#q5) | エッジでの分散処理 | CloudFront でヘッダーを書き換える軽い処理を、1 ミリ秒未満で大量に実行します。どれを選び… |
| [compute 問6](../../exercises/compute.md#q6) | エッジでの分散処理 | CloudFront のオリジンリクエストのイベントで、外部サービスへのネットワーク呼び出しを含む処… |
| [compute 問7](../../exercises/compute.md#q7) | エッジでの分散処理 | 配置の要件に合う組み合わせはどれですか。5G 端末向けの超低遅延のアプリ、自社の施設に置くデータ、特… |
| [compute 問8](../../exercises/compute.md#q8) | スケーリングの機能 | 毎朝 9 時の決まった急増に備え、事前に台数を増やします。周期は読めています。どのポリシーが最も直接… |
| [compute 問9](../../exercises/compute.md#q9) | スケーリングの機能 | 起動に 10 分かかるアプリで、急増への反応を速くします。既に初期化を済ませたインスタンスをすぐに使… |
| [compute 問10](../../exercises/compute.md#q10) | スケーリングの機能 | Aurora のレプリカ、ECS のタスク、DynamoDB の容量のスケーリングを 1 か所で計画… |
| [compute 問11](../../exercises/compute.md#q11) | スケーリングの指標と条件 | SQS のワーカーの EC2 をスケールします。処理時間は一定で、目標の遅れの範囲があります。どの指… |
| [compute 問12](../../exercises/compute.md#q12) | スケーリングの指標と条件 | メモリが足りなくなるアプリで、メモリの使用率でスケールします。EC2 の標準メトリクスに見当たりませ… |
| [compute 問13](../../exercises/compute.md#q13) | スケーリングの指標と条件 | ターゲット追跡で、台数が増えすぎる症状があります。インスタンスの起動に 5 分かかり、メトリクスに反… |
| [compute 問14](../../exercises/compute.md#q14) | インスタンスタイプ | インメモリのキャッシュや大きなヒープの Java アプリに合うファミリーはどれですか。 |
| [compute 問15](../../exercises/compute.md#q15) | インスタンスタイプ | HPC のノード間の通信を低遅延にします。同じ AZ に配置し、MPI を OS をバイパスして使い… |
| [compute 問16](../../exercises/compute.md#q16) | インスタンスタイプ | 少数の重要なインスタンスを物理的に分離し、ハードウェアの障害を同時に受けないようにします。どのプレイ… |
| [compute 問17](../../exercises/compute.md#q17) | インスタンスタイプ | HDFS や Cassandra のような大規模な分散ワークロードで、ラック障害の影響を区切ります。… |
| [compute 問18](../../exercises/compute.md#q18) | リソースのタイプとサイズ | CPU を多く使う Lambda 関数が遅くなっています。CPU だけを増やす設定はありますか。正し… |
| [compute 問19](../../exercises/compute.md#q19) | リソースのタイプとサイズ | t3 インスタンスの CPU が突然遅くなりました。CPUCreditBalance が 0 です。… |
| [compute 問20](../../exercises/compute.md#q20) | リソースのタイプとサイズ | Lambda 関数の設定の範囲と、Fargate のタスクのサイズについて正しいものはどれですか。 |

<!-- questions:end -->

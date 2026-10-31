# 分野2: SageMaker AI の学習

スクリプトモードの決まり、AMT の戦略、時間とコストの短縮、収束のデバッグを問います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [2.1.6](../../domain2.md#skill-2-1-6) | ML の性能、学習時間、コストのトレードオフ |
| [2.2.2](../../domain2.md#skill-2-2-2) | スクリプトモードの設定 |
| [2.2.3](../../domain2.md#skill-2-2-3) | ハイパーパラメータの最適化 |
| [2.2.4](../../domain2.md#skill-2-2-4) | 学習時間の短縮 |
| [2.3.5](../../domain2.md#skill-2-3-5) | 収束の問題のデバッグ |

## 学習の順番 {#study-order}

1. [スクリプトモード](../../../../services/sagemaker.md#script-mode): パスと環境変数を覚えます。
2. [自動モデルチューニング](../../../../services/sagemaker.md#amt): 戦略の違い、スケーリング、ウォームスタートを確認します。
3. [マネージドスポット学習](../../../../services/sagemaker.md#spot-training): 設定と節約率の計算を押さえます。
4. [分散学習と時間短縮](../../../../services/sagemaker.md#distributed-training)と[入力モード](../../../../services/sagemaker.md#input-modes): 遅い原因ごとの手段を選びます。
5. [収束の問題](../../../../services/sagemaker.md#convergence)と [Debugger](../../../../services/sagemaker.md#debugger): 症状と対応、移行先を覚えます。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| モデルの保存先 | `/opt/ml/model`（`SM_MODEL_DIR`） | 外に保存すると失われる |
| 入力データ | `/opt/ml/input/data/<チャネル名>` | `SM_CHANNEL_<チャネル名>` |
| スポットの割引 | 最大 90% | 課金 100 秒、学習 500 秒で 80% |
| ウォームスタートの親 | 最大 5 | 同じデータは `IDENTICAL_DATA_AND_ALGORITHM` |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 少ない試行で探す | Bayesian |
| エポックごとの指標で効率よく | Hyperband（`Off`） |
| カテゴリの値を網羅する | Grid |
| 桁が変わる範囲を探す | `Logarithmic` |
| データが大きい | SMDDP |
| モデルが 1 枚の GPU に載らない | SMP |
| 長時間の大規模な FM の学習 | HyperPod |
| 損失が `NaN` | 学習率を下げる、勾配クリッピング |

## 引っかかりやすい点 {#traps}

- `MaxWaitTimeInSeconds` は `MaxRuntimeInSeconds` より大きくします。容量がなくてもオンデマンドには切り替わりません。
- Hyperband には内部の早期停止があるので、`TrainingJobEarlyStoppingType` は `Off` です。
- Grid はカテゴリのパラメータだけです。
- Debugger は新規顧客の受付を終了しています。移行先は MLflow、TensorBoard、CloudWatch です。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [sagemaker-training 問1](../../exercises/sagemaker-training.md#q1) | 2.1.6 | 学習ジョブの結果を見ると、TrainingTimeInSeconds は 500、BillableT… |
| [sagemaker-training 問2](../../exercises/sagemaker-training.md#q2) | 2.1.6 | GPU の学習を Managed Spot で行います。中断に備え、安く済ませます。必要な設定の組み… |
| [sagemaker-training 問3](../../exercises/sagemaker-training.md#q3) | 2.1.6 | 複雑な深層学習モデルが精度で少し勝ちますが、学習は 10 倍、コストも 10 倍です。週次の再学習で… |
| [sagemaker-training 問4](../../exercises/sagemaker-training.md#q4) | 2.2.2 | スクリプトモードで学習します。モデルを保存すると S3 に model.tar.gz で出力される場… |
| [sagemaker-training 問5](../../exercises/sagemaker-training.md#q5) | 2.2.2 | スクリプトモードで Python の追加パッケージを使います。OS のライブラリは不要です。最も手間… |
| [sagemaker-training 問6](../../exercises/sagemaker-training.md#q6) | 2.2.2 | train チャネルでデータを渡しました。スクリプトの中でデータのパスを取得する方法はどれですか。 |
| [sagemaker-training 問7](../../exercises/sagemaker-training.md#q7) | 2.2.3 | ニューラルネットの調整で、エポックごとに指標を出せます。少ない計算資源で多くの候補を試し、見込みのな… |
| [sagemaker-training 問8](../../exercises/sagemaker-training.md#q8) | 2.2.3 | 学習率の探索範囲は 0.0001〜0.1 です。桁で広く探したいです。ScalingType はどれ… |
| [sagemaker-training 問9](../../exercises/sagemaker-training.md#q9) | 2.2.3 | 前回のチューニングの結果を活かして、データは同じまま探索範囲だけ広げます。ウォームスタートの設定とし… |
| [sagemaker-training 問10](../../exercises/sagemaker-training.md#q10) | 2.2.4 | データが大きすぎて 1 台では学習が間に合いません。モデルは 1 枚の GPU に載ります。どの手法… |
| [sagemaker-training 問11](../../exercises/sagemaker-training.md#q11) | 2.2.4 | 数週間かかる大規模な FM の学習で、ノードの障害が起きても自動で回復して続けたいです。どの選択が適… |
| [sagemaker-training 問12](../../exercises/sagemaker-training.md#q12) | 2.2.4 | 学習ジョブの開始までが長く、CloudWatch を見るとデータのダウンロードに時間がかかっています… |
| [sagemaker-training 問13](../../exercises/sagemaker-training.md#q13) | 2.3.5 | 学習の開始直後から損失が NaN になります。原因の候補と対応の組み合わせを選んでください。（2つ選… |
| [sagemaker-training 問14](../../exercises/sagemaker-training.md#q14) | 2.3.5 | 深いネットワークで、入力に近い層の勾配がほぼ 0 になり、学習が進みません。適切な対応はどれですか。 |
| [sagemaker-training 問15](../../exercises/sagemaker-training.md#q15) | 2.3.5 | 新規に作るプロジェクトで、学習の指標とプロファイルを監視します。SageMaker Debugger… |

<!-- questions:end -->

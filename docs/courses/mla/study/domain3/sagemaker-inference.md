# 分野3: SageMaker AI の推論

入力のサイズと処理時間で推論の方式を決めます。1 つのエンドポイントに複数のモデルを載せる方式の区別と、スケーリングの指標が問われます。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [3.1.1](../../domain3.md#skill-3-1-1) | コンピューティング環境とデプロイ先の選択 |
| [3.1.2](../../domain3.md#skill-3-1-2) | オーケストレーターとマルチモデルの戦略 |
| [3.1.3](../../domain3.md#skill-3-1-3) | 推論の戦略の選択 |
| [3.1.5](../../domain3.md#skill-3-1-5) | AWS の外で作ったモデルのデプロイ |
| [3.2.5](../../domain3.md#skill-3-2-5) | プログラムによるデプロイとホスティング |
| [3.2.6](../../domain3.md#skill-3-2-6) | 自動スケーリングの指標の選択 |
| [3.2.10](../../domain3.md#skill-3-2-10) | GPU ワークロードのスケーリング |

## 学習の順番 {#study-order}

1. [エンドポイントと推論](../../../../services/sagemaker.md#endpoints): 4 つの方式と API の順序を覚えます。
2. [サーバーレス](../../../../services/sagemaker.md#serverless)、[非同期](../../../../services/sagemaker.md#async)、[バッチ変換](../../../../services/sagemaker.md#batch-transform): 上限と制約を確認します。
3. [マルチモデル](../../../../services/sagemaker.md#multi-model): 4 つの方式と呼び出しの指定を区別します。
4. [JumpStart と持ち込み](../../../../services/sagemaker.md#jumpstart)と [Custom Model Import](../../../../services/genai-apps.md#custom-model-import): 外部のモデルの動かし方を押さえます。
5. [自動スケーリング](../../../../services/sagemaker.md#autoscaling): 指標とクールダウンを覚えます。
6. [SageMaker Pipelines と使い分け](../../../../services/sagemaker.md#pipelines)と [Step Functions](../../../../services/step-functions.md#orchestration-choreography): オーケストレーターを選びます。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| リアルタイム | 6 MB（API リファレンス。FAQ は 25 MB）、60 秒 | 50〜60 秒ならソケットタイムアウトを 70 秒に |
| 非同期 | 1 GB、1 時間 | 0 台まで縮小できる |
| バッチの `MaxPayloadInMB` | 既定 6、最大 100 | データセット全体 |
| サーバーレスのメモリ | 1,024〜6,144 MB | GPU と VPC は不可 |
| 推論パイプライン | 2〜15 コンテナ | 順に実行する |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 入力 500 MB、処理 20 分 | 非同期 |
| 断続的でコールドスタートを許せる | サーバーレス |
| 似たモデルが数千ある | マルチモデル（`TargetModel`） |
| 別のフレームワークを同居させる | マルチコンテナ（`TargetContainerHostname`） |
| 複数の FM に資源を割り当てる | 推論コンポーネント（`InferenceComponentName`） |
| 外部のモデルを Bedrock の API で | Custom Model Import |
| LLM の急増に 10 秒で反応する | 高解像度の同時リクエスト数の指標 |
| 非同期のスケーリング | `ApproximateBacklogSizePerInstance` |

## 引っかかりやすい点 {#traps}

- 呼び出しは `sagemaker-runtime` の `InvokeEndpoint` です。`sagemaker` とはクライアントが別です。
- 非同期で 0 台から起動するには、`HasBacklogWithoutCapacity` のステップスケーリングも要ります。
- Custom Model Import はバッチ推論に対応しません。
- `ScaleInCooldown` が短すぎると増減を繰り返します。
- マルチモデルは初回の呼び出しで S3 から読み込むので遅延が出ます。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [sagemaker-inference 問1](../../exercises/sagemaker-inference.md#q1) | 3.1.1 | 会社は既に EKS でアプリを運用しており、同じクラスターの運用手順でモデルも動かしたいです。デプロ… |
| [sagemaker-inference 問2](../../exercises/sagemaker-inference.md#q2) | 3.1.1 | 小さなモデルの推論が 1 日に数十回だけ発生し、処理は数秒です。コンテナは 1 つで、GPU は不要… |
| [sagemaker-inference 問3](../../exercises/sagemaker-inference.md#q3) | 3.1.1 | コンテナで動く夜間の特徴量計算と推論のジョブを、キューに入れて順に実行します。SageMaker A… |
| [sagemaker-inference 問4](../../exercises/sagemaker-inference.md#q4) | 3.1.2 | 顧客ごとの似たモデルが 3,000 個あり、同じフレームワークです。各モデルの利用はまれです。費用を… |
| [sagemaker-inference 問5](../../exercises/sagemaker-inference.md#q5) | 3.1.2 | 多様な AWS サービスと人の承認を含む業務の流れの中で、学習を 1 ステップとして実行します。どの… |
| [sagemaker-inference 問6](../../exercises/sagemaker-inference.md#q6) | 3.1.2 | 前処理の scikit-learn と推論の XGBoost を順に実行し、呼び出し側は 1 回の呼… |
| [sagemaker-inference 問7](../../exercises/sagemaker-inference.md#q7) | 3.1.3 | 動画の解析です。入力は 500 MB、処理は 20 分です。利用者は結果を後で受け取ります。どの推論… |
| [sagemaker-inference 問8](../../exercises/sagemaker-inference.md#q8) | 3.1.3 | 毎晩、S3 の数百万件のデータセット全体にスコアを付けます。常時稼働のエンドポイントは不要です。どの… |
| [sagemaker-inference 問9](../../exercises/sagemaker-inference.md#q9) | 3.1.3 | 断続的な負荷でサーバーレス推論を検討しています。次の要件のうち、サーバーレスでは満たせないものを選ん… |
| [sagemaker-inference 問10](../../exercises/sagemaker-inference.md#q10) | 3.1.5 | 社外で PyTorch で学習した重みを SageMaker AI で動かします。特殊な依存関係はあ… |
| [sagemaker-inference 問11](../../exercises/sagemaker-inference.md#q11) | 3.1.5 | Hugging Face で調整した Llama 系のモデルを、サーバーを管理せず Bedrock … |
| [sagemaker-inference 問12](../../exercises/sagemaker-inference.md#q12) | 3.1.5 | 社外で作ったモデルに、独自の C++ のライブラリが必要です。SageMaker AI で動かすとき… |
| [sagemaker-inference 問13](../../exercises/sagemaker-inference.md#q13) | 3.2.5 | Boto3 でリアルタイムエンドポイントを作ります。API を呼ぶ順序はどれですか。 |
| [sagemaker-inference 問14](../../exercises/sagemaker-inference.md#q14) | 3.2.5 | Boto3 で sagemaker クライアントの invoke_endpoint を呼ぶと、メソッ… |
| [sagemaker-inference 問15](../../exercises/sagemaker-inference.md#q15) | 3.2.5 | リアルタイムのモデルの処理に 50〜60 秒かかります。クライアント側でタイムアウトが出ています。正… |
| [sagemaker-inference 問16](../../exercises/sagemaker-inference.md#q16) | 3.2.6 | 1 件の処理時間が安定した XGBoost のエンドポイントです。標準のターゲット追跡の指標はどれで… |
| [sagemaker-inference 問17](../../exercises/sagemaker-inference.md#q17) | 3.2.6 | 非同期のエンドポイントで夜間は 0 台にします。キューが溜まったら増やします。必要な設定を選んでくだ… |
| [sagemaker-inference 問18](../../exercises/sagemaker-inference.md#q18) | 3.2.6 | ターゲット追跡でインスタンスの増減を短い間隔で繰り返しています。適切な調整はどれですか。 |
| [sagemaker-inference 問19](../../exercises/sagemaker-inference.md#q19) | 3.2.10 | LLM のストリーミングのエンドポイントで、急増に 10 秒程度で反応してスケールさせます。どの指標… |
| [sagemaker-inference 問20](../../exercises/sagemaker-inference.md#q20) | 3.2.10 | 推論コンポーネントで複数の FM を共有しています。モデルごとにコピーの数を増減します。どの指標を使… |
| [sagemaker-inference 問21](../../exercises/sagemaker-inference.md#q21) | 3.2.10 | HyperPod の EKS クラスターで、推論の GPU ノードを自動で増減し、アイドル時はノード… |

<!-- questions:end -->

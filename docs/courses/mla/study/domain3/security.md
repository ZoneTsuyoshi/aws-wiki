# 分野3: VPC とネットワーク分離

SageMaker AI のエンドポイントを VPC に置くときの設定と、作成の失敗の切り分けを問います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [3.2.4](../../domain3.md#skill-3-2-4) | VPC 内の SageMaker AI エンドポイント |

## 学習の順番 {#study-order}

1. [VPC とネットワーク分離](../../../../services/sagemaker.md#vpc-isolation): `VpcConfig` と `EnableNetworkIsolation` の違いを押さえます。
2. [VPC エンドポイント](../../../../services/networking.md#vpc-endpoints): ゲートウェイとインターフェイスを区別します。
3. [リアルタイム](../../../../services/sagemaker.md#realtime): 可用性のための台数を確認します。

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| プライベートサブネットに置く | `CreateModel` の `VpcConfig` |
| VPC 内からモデルを取得する | S3 ゲートウェイエンドポイント |
| VPC 内から SageMaker API を呼ぶ | インターフェイスエンドポイント |
| 外向きの通信を一切禁止する | `EnableNetworkIsolation` |
| 作成が失敗する | ECR と S3 への到達、実行ロールの権限を確認 |

## 引っかかりやすい点 {#traps}

- `VpcConfig` だけでは外向きの通信は止まりません。経路があれば外に出られます。
- インスタンスを 2 台以上にすると、複数の AZ に分散します。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [security 問1](../../exercises/security.md#q1) | 3.2.4 | プライベートサブネットにモデルを配置してエンドポイントを作ります。インターネットには出ません。モデル… |
| [security 問2](../../exercises/security.md#q2) | 3.2.4 | コンテナからの外向きの通信を一切禁止します。どの設定ですか。 |
| [security 問3](../../exercises/security.md#q3) | 3.2.4 | VPC 内のエンドポイントの作成が失敗しました。最初に確認する項目の組み合わせはどれですか。 |

<!-- questions:end -->

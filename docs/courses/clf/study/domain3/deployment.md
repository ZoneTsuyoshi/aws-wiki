# 分野3: デプロイと運用の方法

どの方法で作り、操作するかを、作業の回数と目的から判断します。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [プロビジョニングと運用の方法](../../domain3.md#t3-1-provisioning) | 手で作る、スクリプト、IaC、基盤を任せる |
| [運用を支えるサービス](../../domain3.md#t3-1-operating-tools) | Systems Manager、Health、Service Quotas |
| [AWS へのアクセス方法](../../domain3.md#t3-1-access) | コンソール、CLI、SDK、API、IaC |
| [一度きりか、繰り返しか](../../domain3.md#t3-1-one-time-repeatable) | 回数からの判断 |
| [デプロイモデル](../../domain3.md#t3-1-deployment-models) | クラウド、ハイブリッド、オンプレミス |

## 学習の順番 {#study-order}

1. [マネジメントコンソールとアクセス方法](../../../../services/cloud-foundations.md#access-methods): アクセス方法と向く場面を覚えます。
2. [どれを使うか](../../../../services/iac.md#choosing)と[CloudFormation テンプレート](../../../../services/iac.md#cloudformation-template): IaC で環境を再現する考え方を確認します。
3. [デプロイモデルとサービスモデル](../../../../services/cloud-foundations.md#deployment-models): デプロイモデルとサービスモデルを区別します。
4. [AWS Systems Manager](../../../../services/operations.md#systems-manager)と[AWS Health Dashboard](../../../../services/cloud-foundations.md#health): 運用のサービスの役割を確認します。

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 一度だけ状態を確認する | コンソール |
| 毎晩同じ処理を実行する | CLI のスクリプトなどで自動化する |
| 開発、検証、本番に同じ構成を作る | IaC |
| アプリから AWS を呼ぶ | SDK |
| コードをアップロードするだけで動かす | Elastic Beanstalk |
| サービスの上限を確認して申請する | Service Quotas |
| 基幹は自社に残し、Web を AWS に置く | ハイブリッド |

## 引っかかりやすい点 {#traps}

- CLI と SDK は内部で API を呼びます。API が土台です。
- EC2 は IaaS、Elastic Beanstalk は PaaS、完成したソフトウェアは SaaS です。
- CloudWatch では AWS 側の予定は分かりません。AWS Health Dashboard で確認します。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [deployment 問1](../../exercises/deployment.md#q1) | プロビジョニングと運用の方法 | 環境の再現と変更の管理をテンプレートで行いたいと考えています。この方法に当たるものはどれですか。 |
| [deployment 問2](../../exercises/deployment.md#q2) | プロビジョニングと運用の方法 | 開発者が、基盤の設定を任せて、コードをアップロードするだけで Web アプリを動かしたいと考えていま… |
| [deployment 問3](../../exercises/deployment.md#q3) | プロビジョニングと運用の方法 | クラウドの経験が少ない担当者が、小さな Web サイトを数クリックで公開したいと考えています。最も適… |
| [deployment 問4](../../exercises/deployment.md#q4) | 運用を支えるサービス | 多数のサーバーへのパッチの適用やコマンドの実行を、まとめて行いたいと考えています。最も適切なサービス… |
| [deployment 問5](../../exercises/deployment.md#q5) | 運用を支えるサービス | EC2 インスタンスの起動数がサービスの上限に近づいています。上限を確認して引き上げを申請する場所と… |
| [deployment 問6](../../exercises/deployment.md#q6) | 運用を支えるサービス | 予定されたメンテナンスで、自分のどのリソースが影響を受けるかを知りたいと考えています。確認する場所と… |
| [deployment 問7](../../exercises/deployment.md#q7) | AWS へのアクセス方法 | 自社のアプリの中から Python のライブラリで S3 にファイルを置きたいと考えています。最も適… |
| [deployment 問8](../../exercises/deployment.md#q8) | AWS へのアクセス方法 | 運用担当者が、シェルスクリプトで AWS の操作を繰り返したいと考えています。最も適切なアクセス方法… |
| [deployment 問9](../../exercises/deployment.md#q9) | AWS へのアクセス方法 | API、SDK、CLI の関係の説明として正しいものはどれですか。 |
| [deployment 問10](../../exercises/deployment.md#q10) | AWS へのアクセス方法 | 要件とアクセス方法の組み合わせとして正しいものはどれですか。（2つ選択） |
| [deployment 問11](../../exercises/deployment.md#q11) | 一度きりか、繰り返しか | 一度だけ、特定のリソースの状態を確認したいと考えています。最も手軽な方法はどれですか。 |
| [deployment 問12](../../exercises/deployment.md#q12) | 一度きりか、繰り返しか | 開発、検証、本番に同じ構成を作る必要があります。最も適切な方法はどれですか。 |
| [deployment 問13](../../exercises/deployment.md#q13) | 一度きりか、繰り返しか | 毎晩、同じ手順で不要なスナップショットを削除しています。担当者のミスが増えています。最も適切な改善は… |
| [deployment 問14](../../exercises/deployment.md#q14) | デプロイモデル | 新しいサービスをすべて AWS 上だけで作ることにしました。この形はどれですか。 |
| [deployment 問15](../../exercises/deployment.md#q15) | デプロイモデル | 工場の制御システムは自社の施設に残し、分析の処理だけ AWS に送ります。両者はネットワークで接続し… |
| [deployment 問16](../../exercises/deployment.md#q16) | デプロイモデル | サービスモデルの例の組み合わせとして正しいものはどれですか。（2つ選択） |

<!-- questions:end -->

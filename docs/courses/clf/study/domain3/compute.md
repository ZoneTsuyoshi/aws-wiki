# 分野3: コンピューティング

要件からサービスとインスタンスのカテゴリを選びます。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [コンピューティングの全体像](../../domain3.md#t3-3-overview) | EC2、Lambda、Beanstalk、Lightsail、Batch、Outposts |
| [EC2 のインスタンスタイプ](../../domain3.md#t3-3-instance-types) | 5 つのカテゴリ |
| [コンテナの選択肢](../../domain3.md#t3-3-containers) | ECS、EKS、ECR |
| [サーバーレスの選択肢](../../domain3.md#t3-3-serverless) | Lambda と Fargate |
| [Auto Scaling と弾力性](../../domain3.md#t3-3-auto-scaling) | 台数の増減 |
| [ロードバランサーの目的](../../domain3.md#t3-3-load-balancers) | 振り分けと ALB、NLB |

## 学習の順番 {#study-order}

1. [インスタンスタイプとメモリ、CPU の要件](../../../../services/ec2-beanstalk.md#instance-types): カテゴリと向く処理を覚えます。
2. [Elastic Beanstalk の環境](../../../../services/ec2-beanstalk.md#beanstalk-environments)、[Amazon Lightsail](../../../../services/cloud-foundations.md#lightsail)、[AWS Batch](../../../../services/other-services.md#batch): 基盤を任せるサービスを区別します。
3. [ECS](../../../../services/containers.md#ecs)、[EKS](../../../../services/containers.md#eks)、[ECR](../../../../services/containers.md#ecr): 役割を区別します。
4. [実行モデル](../../../../services/lambda.md#execution-model)と[Fargate と EC2](../../../../services/containers.md#fargate-vs-ec2): 動かすものの違いを確認します。
5. [EC2 Auto Scaling](../../../../services/ec2-beanstalk.md#auto-scaling)と[ALB と NLB の違い](../../../../services/networking.md#alb-vs-nlb): 弾力性と振り分けを確認します。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| Lambda の実行時間 | 最大 15 分 | 動かし続けるなら Fargate |
| 汎用 | T、M | Web サーバー |
| コンピューティング最適化 | C | エンコード、バッチ |
| メモリ最適化 | R、X | インメモリキャッシュ |
| ストレージ最適化 | I、D | 高 IOPS のローカルディスク |
| 高速コンピューティング | P、G | GPU |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| OS から細かく制御する | EC2 |
| イベントで短い処理を動かす | Lambda |
| コンテナをサーバー管理なしで動かす | Fargate |
| Kubernetes の資産を使う | EKS |
| シンプルにコンテナを動かす | ECS |
| コンテナイメージの置き場 | ECR |
| 数千のジョブを順に処理する | Batch |
| パスで振り分ける | ALB |
| 固定 IP、非 HTTP、高負荷 | NLB |

## 引っかかりやすい点 {#traps}

- ECR は保管先で、コンテナを動かしません。
- ECS も EKS も、実行場所として EC2 や Fargate を選べます。
- Auto Scaling が増減するのは台数で、インスタンスのタイプではありません。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [compute 問1](../../exercises/compute.md#q1) | コンピューティングの全体像 | OS から細かく制御できる仮想サーバーが必要です。最も適切なサービスはどれですか。 |
| [compute 問2](../../exercises/compute.md#q2) | コンピューティングの全体像 | 数千のジョブを並べて、順に実行する処理を任せたいと考えています。最も適切なサービスはどれですか。 |
| [compute 問3](../../exercises/compute.md#q3) | コンピューティングの全体像 | 要件とサービスの組み合わせとして正しいものはどれですか。（2つ選択） |
| [compute 問4](../../exercises/compute.md#q4) | EC2 のインスタンスタイプ | 動画のエンコードで CPU を長時間多く使います。適切なインスタンスのカテゴリはどれですか。 |
| [compute 問5](../../exercises/compute.md#q5) | EC2 のインスタンスタイプ | 大きなインメモリキャッシュを動かすサーバーに向くインスタンスのカテゴリはどれですか。 |
| [compute 問6](../../exercises/compute.md#q6) | EC2 のインスタンスタイプ | GPU を使う機械学習の学習に向くインスタンスのカテゴリはどれですか。 |
| [compute 問7](../../exercises/compute.md#q7) | EC2 のインスタンスタイプ | 処理とインスタンスのカテゴリの組み合わせとして正しいものはどれですか。（2つ選択） |
| [compute 問8](../../exercises/compute.md#q8) | コンテナの選択肢 | 既存の Kubernetes の知識と資産を AWS で使いたいと考えています。最も適切なサービスは… |
| [compute 問9](../../exercises/compute.md#q9) | コンテナの選択肢 | コンテナイメージを AWS で保管したいと考えています。最も適切なサービスはどれですか。 |
| [compute 問10](../../exercises/compute.md#q10) | コンテナの選択肢 | シンプルに AWS でコンテナを動かしたいと考えています。Kubernetes を使う要件はありませ… |
| [compute 問11](../../exercises/compute.md#q11) | コンテナの選択肢 | ECS と EKS の実行場所の説明として正しいものはどれですか。 |
| [compute 問12](../../exercises/compute.md#q12) | サーバーレスの選択肢 | S3 にファイルが置かれたら、短い処理を自動で実行したいと考えています。サーバーを管理したくありませ… |
| [compute 問13](../../exercises/compute.md#q13) | サーバーレスの選択肢 | コンテナのアプリを長時間動かし続けます。サーバーを管理せずに実行したいと考えています。最も適切なもの… |
| [compute 問14](../../exercises/compute.md#q14) | サーバーレスの選択肢 | AWS Lambda の 1 回の実行時間の上限はどれですか。 |
| [compute 問15](../../exercises/compute.md#q15) | サーバーレスの選択肢 | Lambda と Fargate に共通する説明はどれですか。 |
| [compute 問16](../../exercises/compute.md#q16) | Auto Scaling と弾力性 | EC2 Auto Scaling の説明として正しいものはどれですか。（2つ選択） |
| [compute 問17](../../exercises/compute.md#q17) | Auto Scaling と弾力性 | 夜間は負荷が下がるのに、昼のピークに合わせた台数を動かし続けています。費用を減らす方法として最も適切… |
| [compute 問18](../../exercises/compute.md#q18) | Auto Scaling と弾力性 | EC2 Auto Scaling が直接実現する性質として最も適切なものはどれですか。 |
| [compute 問19](../../exercises/compute.md#q19) | ロードバランサーの目的 | Web アプリで、URL のパスによって振り分け先を変えたいと考えています。最も適切なものはどれです… |
| [compute 問20](../../exercises/compute.md#q20) | ロードバランサーの目的 | 固定の IP アドレスが必要で、HTTP ではない TCP の通信を高い負荷で受けます。最も適切なも… |
| [compute 問21](../../exercises/compute.md#q21) | ロードバランサーの目的 | ロードバランサーの目的として正しいものはどれですか。（2つ選択） |

<!-- questions:end -->

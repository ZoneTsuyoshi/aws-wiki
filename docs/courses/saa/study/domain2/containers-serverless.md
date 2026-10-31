# 分野2: コンテナとサーバーレス

実行時間、管理の範囲、既存の資産で、コンテナとサーバーレスを選びます。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [コンテナ](../../domain2.md#t2-1-containers) | アプリケーションをコンテナに移行する方法、コンテナのオーケストレーション、コンテナを使うべき場面の判断 |
| [サーバーレス](../../domain2.md#t2-1-serverless) | サーバーレスの技術とパターン、サーバーレスを使うべき場面の判断 |

## 学習の順番 {#study-order}

1. [ECS](../../../../services/containers.md#ecs)と[EKS](../../../../services/containers.md#eks): ECS と EKS の選び方を確認します。
2. [Fargate と EC2](../../../../services/containers.md#fargate-vs-ec2): Fargate と EC2 の起動タイプの違いを表で比べます。
3. [Dockerfile の基本](../../../../services/containers.md#dockerfile)と[ECR](../../../../services/containers.md#ecr): コンテナへの移行の流れを確認します。
4. [実行モデル](../../../../services/lambda.md#execution-model)と[タイムアウト](../../../../services/lambda.md#timeout): Lambda の使いどころと上限を押さえます。
5. [SAM CLI のコマンド](../../../../services/iac.md#sam-cli)と[Amplify Hosting とブランチ](../../../../services/cicd.md#amplify): 再利用と静的 Web の公開の手段を確認します。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| Lambda のタイムアウト | 最大 900 秒（15 分） | 超えるなら Fargate、Batch、分割 |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| Kubernetes の資産を使う | EKS |
| AWS に統合された簡単なオーケストレーション | ECS |
| サーバーを管理したくない | Fargate |
| GPU、特権コンテナ | EC2 起動タイプ |
| 短いイベント処理 | Lambda |
| 長時間のコンテナ | Fargate |
| 増減が大きく、アイドルが長い | Lambda と DynamoDB オンデマンド |

## 引っかかりやすい点 {#traps}

- 状態はコンテナの外（S3、EFS、DB）に出します。
- 15 分を超える処理に Lambda を選ぶ選択肢は誤りです。
- App2Container は新規受付を終了しました。移行の答えにしません。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [containers-serverless 問1](../../exercises/containers-serverless.md#q1) | コンテナ | Kubernetes のマニフェストと Helm の資産を AWS で使い続けます。コントロールプレ… |
| [containers-serverless 問2](../../exercises/containers-serverless.md#q2) | コンテナ | Kubernetes の資産はなく、AWS と統合された簡単なコンテナの運用をしたいと考えています。… |
| [containers-serverless 問3](../../exercises/containers-serverless.md#q3) | コンテナ | GPU を使い、特権コンテナも必要なワークロードを ECS で動かします。適切な起動タイプはどれです… |
| [containers-serverless 問4](../../exercises/containers-serverless.md#q4) | コンテナ | 既存のアプリをコンテナに移します。正しい流れはどれですか。 |
| [containers-serverless 問5](../../exercises/containers-serverless.md#q5) | コンテナ | 次の処理のうち、Lambda よりコンテナを選ぶべきものはどれですか。 |
| [containers-serverless 問6](../../exercises/containers-serverless.md#q6) | サーバーレス | Lambda で実行したい処理が最長 40 分かかります。分割はできません。サーバーの管理はしたくあ… |
| [containers-serverless 問7](../../exercises/containers-serverless.md#q7) | サーバーレス | 負荷の増減が大きく、夜間はほぼアクセスがない API を作ります。インフラの管理を最小にします。適切… |
| [containers-serverless 問8](../../exercises/containers-serverless.md#q8) | サーバーレス | Fargate と Lambda の選択で、Fargate を選ぶ手がかりはどれですか。 |
| [containers-serverless 問9](../../exercises/containers-serverless.md#q9) | サーバーレス | 既存の React の静的な Web アプリを Git から自動でビルドして公開します。CDN の設… |
| [containers-serverless 問10](../../exercises/containers-serverless.md#q10) | サーバーレス | 組織内で再利用するサーバーレスのアプリの部品を、SAM テンプレートとして公開し、他のチームがコンソ… |

<!-- questions:end -->

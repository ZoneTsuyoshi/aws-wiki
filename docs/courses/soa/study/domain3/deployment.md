# 分野3: イメージとデプロイ戦略

AMI とイメージの運用、更新の方法の選択を問います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [3.1.1](../../domain3.md#skill-3-1-1) | AMI とコンテナイメージ |
| [3.1.5](../../domain3.md#skill-3-1-5) | デプロイ戦略とサービス |

## 学習の順番 {#study-order}

1. [AMI の管理](../../../../services/operations.md#amis): コピーと共有の注意点を確認します。
2. [EC2 Image Builder](../../../../services/operations.md#image-builder): 構成要素を覚えます。
3. [ECR](../../../../services/containers.md#ecr)、[タグと不変タグ](../../../../services/containers.md#image-tags)と[ライフサイクルポリシー](../../../../services/containers.md#ecr-lifecycle): イメージの運用を確認します。
4. [デプロイ戦略の比較](../../../../services/cicd.md#deployment-strategies)と[ロールバックの方法](../../../../services/cicd.md#rollback): 戦略を比較します。
5. [インスタンスの更新](../../../../services/operations.md#instance-refresh)、[デプロイ](../../../../services/containers.md#ecs-deployments)と[デプロイポリシー](../../../../services/ec2-beanstalk.md#deployment-policies): 対象ごとの実現方法を確認します。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| インスタンスの更新の最小正常割合 | 既定 90% | 順に置き換える |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 別のリージョンで使う | `copy-image`。起動許可は引き継がれない |
| 暗号化した AMI を共有する | カスタマー管理キーと、キーの利用の許可 |
| ビルドがタイムアウトする | インフラストラクチャ設定のロールと SSM への経路 |
| 一部へ流して確認する | カナリア |
| 切り戻すだけで戻す | Blue/Green |
| リージョンの割合を変える | Global Accelerator のトラフィックダイヤル |

## 引っかかりやすい点 {#traps}

- 自動ロールバックでは `$Latest` と `$Default` を使えません。
- AWS 管理キーで暗号化した AMI は共有できません。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [deployment 問1](../../exercises/deployment.md#q1) | 3.1.1 | 東京の AMI を大阪で使いたいです。また、コピー先で別のアカウントにも起動させます。正しいものを選… |
| [deployment 問2](../../exercises/deployment.md#q2) | 3.1.1 | 暗号化された AMI を別のアカウントへ共有しましたが、相手が起動できません。AWS 管理キーで暗号… |
| [deployment 問3](../../exercises/deployment.md#q3) | 3.1.1 | EC2 Image Builder のビルドがタイムアウトで失敗します。コンポーネントの内容は正しい… |
| [deployment 問4](../../exercises/deployment.md#q4) | 3.1.1 | Image Builder で、作ったイメージを別のリージョンへコピーし、別のアカウントに起動許可を… |
| [deployment 問5](../../exercises/deployment.md#q5) | 3.1.1 | ECR で古いイメージの費用を減らし、同じタグの上書きも防ぎたいです。組み合わせとして正しいものはど… |
| [deployment 問6](../../exercises/deployment.md#q6) | 3.1.1 | docker pull で no basic auth credentials が出ます。プライベー… |
| [deployment 問7](../../exercises/deployment.md#q7) | 3.1.1 | 最新の Amazon Linux の AMI の ID を、テンプレートに固定で書かずに参照したいで… |
| [deployment 問8](../../exercises/deployment.md#q8) | 3.1.5 | 新しいバージョンをまず 10% の利用者に流して問題がなければ全体へ広げます。問題があればトラフィッ… |
| [deployment 問9](../../exercises/deployment.md#q9) | 3.1.5 | 新しい環境をあらかじめ用意し、問題があれば切り戻すだけで戻したいです。2 環境分の費用が一時的にかか… |
| [deployment 問10](../../exercises/deployment.md#q10) | 3.1.5 | Auto Scaling グループのインスタンスの更新で、自動ロールバックを有効にしたいです。起動テ… |
| [deployment 問11](../../exercises/deployment.md#q11) | 3.1.5 | 新しい AMI を、Auto Scaling グループの全台へ順に適用します。何を使いますか。また、… |
| [deployment 問12](../../exercises/deployment.md#q12) | 3.1.5 | リージョン間でトラフィックの割合を少しずつ移します。DNS のキャッシュに影響されたくありません。ど… |
| [deployment 問13](../../exercises/deployment.md#q13) | 3.1.5 | デプロイの手段の説明として正しいものを選んでください。（2つ選択） |

<!-- questions:end -->

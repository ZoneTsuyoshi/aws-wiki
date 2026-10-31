# 分野3: コンテナ

経験、運用負荷、既存の資産から基盤を選ぶ力を問います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [コンテナ](../../domain3.md#t3-2-containers) | コンテナプラットフォーム、コンテナアプリケーションのデプロイ |

## 学習の順番 {#study-order}

1. [ECS](../../../../services/containers.md#ecs): ECS の構成要素を確認します。
2. [Fargate と EC2](../../../../services/containers.md#fargate-vs-ec2): サーバーの管理をなくす条件を押さえます。
3. [EKS](../../../../services/containers.md#eks): Kubernetes が必要な場面を確認します。
4. [Amazon EKS Distro](../../../../services/operations.md#eks-distro): 自社環境で同じ配布版を動かす方法を確認します。
5. [Red Hat OpenShift Service on AWS (ROSA)](../../../../services/operations.md#rosa): OpenShift の選択を押さえます。

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| Kubernetes の経験がなく運用を減らす | ECS と Fargate |
| Helm の資産を活かす | EKS |
| OpenShift の資産を活かす | ROSA |

## 引っかかりやすい点 {#traps}

- App Runner は新規の利用者の受付を終了し（移行先は ECS Express Mode）、Copilot はサポートが終了しました。新しい構成の選択肢にしません。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [containers 問7](../../exercises/containers.md#q7) | コンテナ | 新しい Web API をコンテナで動かします。Kubernetes の経験者はおらず、ノードの O… |
| [containers 問8](../../exercises/containers.md#q8) | コンテナ | すでに Helm のチャートと Kubernetes の運用の経験があり、Pod の起動の順番を調整… |
| [containers 問9](../../exercises/containers.md#q9) | コンテナ | 3 つのチームの要件があります。(1) 既存の OpenShift の資産を AWS のマネージド環… |

<!-- questions:end -->

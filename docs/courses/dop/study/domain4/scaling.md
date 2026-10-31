# 分野4: 各サービスの Auto Scaling

何を増やす仕組みかを区別する力を問います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [Auto Scaling](../../domain4.md#t4-3-auto-scaling) | 各サービスの Auto Scaling の機能、Auto Scaling の構成の設定 |

## 学習の順番 {#study-order}

1. [キャパシティプロバイダー](../../../../services/containers.md#capacity-providers): クラスターの EC2 の増減を確認します。
2. [サービスの Auto Scaling](../../../../services/containers.md#service-auto-scaling): タスク数の増減を確認します。
3. [プロビジョンドと Auto Scaling](../../../../services/dynamodb.md#provisioned-auto-scaling): 容量の追従を確認します。
4. [RDS](../../../../services/databases.md#rds): ストレージの Auto Scaling の条件を確認します。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| RDS の拡張の条件 | 空きが 10% 以下、5 分以上 | 最適化の完了後 |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| タスクが起動待ちのまま | キャパシティプロバイダーのマネージドスケーリング |
| ノードの運用を任せる | EKS Auto Mode |

## 引っかかりやすい点 {#traps}

- RDS の割り当て済みの容量は減らせません。大量のロードの前に増やします。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [scaling 問10](../../exercises/scaling.md#q10) | Auto Scaling | EC2 起動の ECS で、タスク数の増加に対してインスタンスが追いつかず、タスクが PROVISI… |
| [scaling 問11](../../exercises/scaling.md#q11) | Auto Scaling | RDS のストレージの Auto Scaling は有効ですが、大量のデータロードの途中でストレージ… |
| [scaling 問12](../../exercises/scaling.md#q12) | Auto Scaling | 次の 2 つの要件で、スケーリングの手段を選びます。(1) DynamoDB のプロビジョンドのテー… |

<!-- questions:end -->

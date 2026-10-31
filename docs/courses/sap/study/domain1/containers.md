# 分野1: コンテナとスケーリング

ECS と EKS の選択、サービス間の通信、イメージの管理、スケーリング、入口を、組織の技能と運用の負荷から判断します。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [1.1.6](../../domain1.md#skill-1-1-6) | マネージドサービスによるコンテナオーケストレーション |
| [1.1.7](../../domain1.md#skill-1-1-7) | サービスメッシュとマイクロサービス間の通信 |
| [1.1.8](../../domain1.md#skill-1-1-8) | コンテナイメージの管理 |
| [1.1.9](../../domain1.md#skill-1-1-9) | サーバーレスとコンテナのスケーリング |
| [1.1.10](../../domain1.md#skill-1-1-10) | 入口のパターンとリソースの最適化 |

## 学習の順番 {#study-order}

1. [ECS](../../../../services/containers.md#ecs)、[EKS](../../../../services/containers.md#eks)、[Fargate と EC2](../../../../services/containers.md#fargate-vs-ec2): 技能と持ち運びの要件で選びます。
2. [キャパシティプロバイダー](../../../../services/containers.md#capacity-providers): GPU やスポットの選び方を確認します。
3. [VPC Lattice](../../../../services/network-connectivity.md#vpc-lattice)と [App Mesh の状況](../../../../services/network-connectivity.md#app-mesh): 新しい構成の選択肢を整理します。
4. [イメージスキャン](../../../../services/containers.md#ecr-scanning)、[ライフサイクルポリシー](../../../../services/containers.md#ecr-lifecycle)、[タグと不変タグ](../../../../services/containers.md#image-tags)、[レプリケーション](../../../../services/containers.md#ecr-replication): 要件ごとの設定を覚えます。
5. [Lambda のクォータ](../../../../services/lambda.md#concurrency-quota)と[予約済みと Provisioned の違い](../../../../services/lambda.md#reserved-provisioned): 枠の確保と事前の初期化を区別します。
6. [ECS サービスの Auto Scaling](../../../../services/containers.md#service-auto-scaling): タスクとインスタンスの 2 段を確認します。
7. [ALB と NLB の違い](../../../../services/networking.md#alb-vs-nlb)と[ターゲットタイプ](../../../../services/networking.md#target-types): 入口の選択と、Fargate の IP ターゲットを押さえます。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| Lambda の同時実行の既定 | リージョンで 1,000 | クォータは引き上げられる |
| Lambda のスケーリング速度 | 関数ごとに 10 秒あたり 1,000 実行環境 | 急増の見積もりに使う |
| App Mesh のサポート終了 | 2026 年 9 月 30 日 | 新しい構成の答えにしない |
| EKS Auto Mode のノードの最大寿命 | 21 日 | 短くはできるが、更新される前提で設計 |
| Service Connect の証明書のローテーション | 既定 5 日 | 短期の証明書モードを推奨 |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| Kubernetes の経験なし、AWS に限定、サーバー管理なし | ECS と Fargate |
| Helm やオペレーターの資産、ノードの運用は減らす | EKS Auto Mode |
| GPU とスポット | EC2 のキャパシティプロバイダー |
| ECS だけで完結、短い名前と TLS | Service Connect と Private CA |
| EC2、Lambda、Pod が混在、IAM で認可 | VPC Lattice |
| 言語のパッケージまで継続的にスキャン | レジストリのレベルの拡張スキャン |
| 別のアカウントとリージョンへイメージを複製 | レジストリのレプリケーションと、送り先の権限ポリシー |
| 既存のノードグループを変えない | Cluster Autoscaler |
| 急増、多様なタイプ、ノードを細かく制御 | Karpenter |
| 開始の時刻が決まった急増の遅延対策 | Provisioned Concurrency をスケジュールで増やす |
| Lambda の枠の確保と上限の両方 | 予約済み同時実行 |
| Ingress ごとの ALB の費用 | `IngressGroup` |
| 独自の TCP、固定 IP、PrivateLink | NLB |

## 引っかかりやすい点 {#traps}

- HPA が Pod を増やしても、ノードに空きがなければ Pending のままです。Pod とノードの 2 段で考えます。
- タグの不変性はライフサイクルによる削除を防ぎません。環境ごとの接頭辞でルールを分けます。
- Service Connect の名前は、名前空間の外や ECS の外から解決できません。ALB などを追加します。
- 予約済み同時実行は事前の初期化をしません。Provisioned Concurrency は上限になりません。
- AWS Load Balancer Controller がないと、`type: LoadBalancer` で Classic Load Balancer が作られます。
- Karpenter のコントローラーの可用性は利用者の責任です。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [containers 問1](../../exercises/containers.md#q1) | 1.1.6 | 社内業務のアプリをコンテナで動かす新しいプラットフォームを作ります。運用は 3 人のチームで、Kub… |
| [containers 問2](../../exercises/containers.md#q2) | 1.1.6 | ある事業者は、自社で作った Helm チャートと Kubernetes のオペレーターを多数持ち、他… |
| [containers 問3](../../exercises/containers.md#q3) | 1.1.6 | 画像の検査バッチを ECS で動かします。タスクは GPU を必要とし、中断されても再実行できます。… |
| [containers 問4](../../exercises/containers.md#q4) | 1.1.7 | ある SaaS の 12 個のマイクロサービスは、すべて同じリージョンの ECS にあり、2 つのク… |
| [containers 問5](../../exercises/containers.md#q5) | 1.1.7 | グループ会社の 3 つのアカウントに、EC2、Lambda、EKS の Pod で動くサービスがあり… |
| [containers 問6](../../exercises/containers.md#q6) | 1.1.7 | ECS のサービス群に Service Connect を導入しました。同じ VPC の EC2 で… |
| [containers 問7](../../exercises/containers.md#q7) | 1.1.8 | 100 を超える ECR リポジトリがあり、作成はチームに任せています。OS と言語のパッケージの脆… |
| [containers 問8](../../exercises/containers.md#q8) | 1.1.8 | 開発の過程で ECR のイメージが増え続け、ストレージの費用が問題になっています。開発用のイメージは… |
| [containers 問9](../../exercises/containers.md#q9) | 1.1.8 | ビルド用のアカウントの ECR から、本番のアカウントの別のリージョンへイメージを自動で複製します。… |
| [containers 問10](../../exercises/containers.md#q10) | 1.1.9 | EKS で、Horizontal Pod Autoscaler により Pod を増やしています。ノ… |
| [containers 問11](../../exercises/containers.md#q11) | 1.1.9 | EKS のクラスターの負荷は急増が多く、多様なインスタンスタイプとスポットで短時間にノードを増やした… |
| [containers 問12](../../exercises/containers.md#q12) | 1.1.9 | チケット販売の API は Lambda で動きます。販売開始の時刻は事前に決まっていて、開始直後に… |
| [containers 問13](../../exercises/containers.md#q13) | 1.1.9 | ある Lambda 関数は、接続数の上限が 100 のレガシーなデータベースを呼びます。同じアカウン… |
| [containers 問14](../../exercises/containers.md#q14) | 1.1.9 | ECS のサービスが SQS キューのメッセージを処理します。タスクは EC2 で動きます。バックロ… |
| [containers 問15](../../exercises/containers.md#q15) | 1.1.10 | EKS で 40 のマイクロサービスがあり、サービスごとに Ingress を作ったところ、ALB … |
| [containers 問16](../../exercises/containers.md#q16) | 1.1.10 | EKS の Pod を Fargate で動かし、TCP のサービスとして公開します。type: L… |
| [containers 問17](../../exercises/containers.md#q17) | 1.1.10 | 社内の Lambda の API は JSON を返すだけで、毎秒 2 万リクエストが常時流れていま… |
| [containers 問18](../../exercises/containers.md#q18) | 1.1.10 | 取引先の機器が、独自のバイナリプロトコルの TCP で接続してきます。取引先は接続先を固定 IP で… |

<!-- questions:end -->

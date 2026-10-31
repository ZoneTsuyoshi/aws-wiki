# 分野4: コンピューティングの費用

購入オプション、サービス、ファミリー、休止の組み合わせで費用を下げます。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [購入オプション](../../domain4.md#t4-2-purchase) | 購入オプション |
| [費用対効果の高いコンピューティングと利用率の最適化](../../domain4.md#t4-2-compute-choice) | コンピューティングの利用率の最適化、費用対効果の高いコンピューティングサービスの判断 |
| [インスタンスのファミリーとサイズ](../../domain4.md#t4-2-instances) | インスタンスのタイプ、ファミリー、サイズ、ワークロードに適したインスタンスファミリーの選択、ワークロードに適したインスタンスサイズの選択 |
| [スケーリングと休止](../../domain4.md#t4-2-scaling) | スケーリング戦略、弾力的なワークロードのスケーリング方法と戦略の判断 |
| [負荷分散の選択](../../domain4.md#t4-2-lb) | 適切な負荷分散の戦略の判断 |
| [ワークロードの種類ごとの可用性](../../domain4.md#t4-2-availability) | グローバルインフラストラクチャ、ワークロードの種類ごとに必要な可用性の判断 |
| [エッジとハイブリッドのコンピューティング](../../domain4.md#t4-2-edge-hybrid) | 分散コンピューティングの戦略、ハイブリッドコンピューティングの選択肢 |

## 学習の順番 {#study-order}

1. [購入オプション](../../../../services/cost-management.md#purchase-options)と[Savings Plans](../../../../services/cost-management.md#savings-plans): 割引の上限と適用範囲を比べます。
2. [スポットインスタンス](../../../../services/cost-management.md#spot)と[スポットの中断への対応](../../../../services/operations.md#spot-interruptions): 中断への備えを確認します。
3. [メモリと CPU の最適化](../../../../services/lambda.md#memory-tuning)と[キャパシティプロバイダー](../../../../services/containers.md#capacity-providers): サーバーレスとコンテナの利用率を確認します。
4. [インスタンスタイプとメモリ、CPU の要件](../../../../services/ec2-beanstalk.md#instance-types)と[Compute Optimizer と適正サイズ](../../../../services/cost-management.md#compute-optimizer): ファミリーの読み方とサイズの見直しを確認します。
5. [休止](../../../../services/operations.md#hibernate)と[ウォームプール](../../../../services/operations.md#warm-pools): 休止の条件を覚えます。
6. [リスナーとルール](../../../../services/networking.md#alb-listeners)と[GWLB](../../../../services/networking.md#gwlb): ロードバランサーをまとめる方法を確認します。
7. [サービスごとの Multi-AZ と Multi-Region](../../../../services/resilience.md#patterns-by-service)と[データ転送の費用](../../../../services/cost-management.md#data-transfer): 環境ごとの可用性と費用を比べます。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| Compute Savings Plans | 最大 66% | EC2、Fargate、Lambda |
| EC2 Instance Savings Plans | 最大 72% | ファミリーが決まった負荷 |
| スポット | 最大 90%。2 分前に通知 | 中断できるバッチ |
| 休止の RAM | Linux は 150 GiB 未満、Windows は 16 GiB 以下 | ルートボリュームの暗号化が必須 |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 将来 Fargate へ移す定常の負荷 | Compute Savings Plans |
| 容量の確保が必須 | Capacity Reservation |
| ソケット単位の BYOL | Dedicated Hosts |
| まばらでアイドルが長い | Lambda |
| 動画のエンコード | C ファミリー |
| 夜間に止め、メモリから再開 | 休止 |
| 複数のサービスをパスで分ける | 1 つの ALB |

## 引っかかりやすい点 {#traps}

- Savings Plans に容量の確保はありません。
- 休止は起動時にしか有効にできません。
- 開発環境に 3 年の確約を付けると、止めている時間の分も払います。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [compute-cost 問1](../../exercises/compute-cost.md#q1) | 購入オプション | 3 年間動きますが、将来 Fargate へ移す可能性がある定常の負荷です。最も合う割引はどれですか… |
| [compute-cost 問2](../../exercises/compute-cost.md#q2) | 購入オプション | 中断してもやり直せる夜間のバッチです。最も安い選択はどれですか。 |
| [compute-cost 問3](../../exercises/compute-cost.md#q3) | 購入オプション | スポットの中断の影響を減らす設定を選んでください。（2つ選択） |
| [compute-cost 問4](../../exercises/compute-cost.md#q4) | 購入オプション | 特定の AZ で必ず台数を確保したいと考えています。割引の Savings Plans は既に買って… |
| [compute-cost 問5](../../exercises/compute-cost.md#q5) | 購入オプション | ソケットやコア単位のライセンスを持ち込みます（BYOL）。どれを選びますか。 |
| [compute-cost 問6](../../exercises/compute-cost.md#q6) | コンピューティングの選択 | 1 日に数百回、数秒だけ動く処理です。アイドルの時間が長いです。最も安いのはどれですか。 |
| [compute-cost 問7](../../exercises/compute-cost.md#q7) | コンピューティングの選択 | 常に高い負荷が続く定常のアプリです。最も安い可能性が高い組み合わせはどれですか。 |
| [compute-cost 問8](../../exercises/compute-cost.md#q8) | コンピューティングの選択 | 静的な Web サイトを最も安く公開します。サーバーの管理もしません。どの組み合わせですか。 |
| [compute-cost 問9](../../exercises/compute-cost.md#q9) | コンピューティングの選択 | コンピューティングの利用率を上げ、費用を下げる方法として適切なものを選んでください。（2つ選択） |
| [compute-cost 問10](../../exercises/compute-cost.md#q10) | ファミリーとサイズ | 動画のエンコードのバッチを M ファミリーで動かしており、CPU が足りずに大きなサイズを使っていま… |
| [compute-cost 問11](../../exercises/compute-cost.md#q11) | ファミリーとサイズ | m6i.xlarge で動く Java のアプリは、arm64 でも動くことを確認済みです。CPU … |
| [compute-cost 問12](../../exercises/compute-cost.md#q12) | ファミリーとサイズ | EC2 のサイズを小さくする前に確認すべきことを選んでください。（2つ選択） |
| [compute-cost 問13](../../exercises/compute-cost.md#q13) | スケーリングと休止 | 起動に 15 分かかるアプリを夜間に止め、翌朝はメモリの状態から再開します。正しい組み合わせを選んで… |
| [compute-cost 問14](../../exercises/compute-cost.md#q14) | スケーリングと休止 | 休止の条件として正しいものはどれですか。 |
| [compute-cost 問15](../../exercises/compute-cost.md#q15) | スケーリングと休止 | 開発環境の EC2 20 台は、平日の日中（週 50 時間）だけ使います。購入の確約はせず、費用を最… |
| [compute-cost 問16](../../exercises/compute-cost.md#q16) | 負荷分散の選択 | 3 つのサービスで、各サービスが HTTP のパスで分かれています。今は ALB を 3 台使ってい… |
| [compute-cost 問17](../../exercises/compute-cost.md#q17) | 負荷分散の選択 | 要件に合うロードバランサーの組み合わせはどれですか。TCP で固定 IP が必要なもの、HTTP の… |
| [compute-cost 問18](../../exercises/compute-cost.md#q18) | 負荷分散の選択 | ファイアウォールの仮想アプライアンスを複数台で動かすときに最も合うものはどれですか。 |
| [compute-cost 問19](../../exercises/compute-cost.md#q19) | 環境ごとの可用性 | 本番と開発の構成の使い分けとして適切なものはどれですか。 |
| [compute-cost 問20](../../exercises/compute-cost.md#q20) | 環境ごとの可用性 | 本番の Web 層を 2 AZ から 3 AZ に増やす案を評価します。可用性は上がります。増える費… |
| [compute-cost 問21](../../exercises/compute-cost.md#q21) | 環境ごとの可用性 | データの所在の制約がない夜間のバッチを東京リージョンで動かしています。結果は S3 に置くだけで、利… |
| [compute-cost 問22](../../exercises/compute-cost.md#q22) | エッジとハイブリッド | CloudFront でビューワーのヘッダーを書き換えてオリジンへのリクエストを減らします。軽い処理… |
| [compute-cost 問23](../../exercises/compute-cost.md#q23) | エッジとハイブリッド | 既存のオンプレミスのサーバーを活かして ECS を動かし、コントロールプレーンは AWS を使います… |
| [compute-cost 問24](../../exercises/compute-cost.md#q24) | エッジとハイブリッド | ソフトウェアのライセンスの使用数を追跡し、超過を防ぎます。どれを選びますか。 |

<!-- questions:end -->

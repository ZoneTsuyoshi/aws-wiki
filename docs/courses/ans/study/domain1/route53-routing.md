# 分野1: Route 53 のルーティングと高可用性

Route 53 の機能と、グローバルなトラフィック管理の選択を問います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [Route 53 の機能](../../domain1.md#t1-2-features) | Route 53 の機能（エイリアス、トラフィックポリシー、リゾルバー、ヘルスチェック） |
| [グローバルなトラフィック管理](../../domain1.md#t1-2-global) | Route 53 によるグローバルなトラフィック管理 |

## 学習の順番 {#study-order}

1. [ルーティングポリシー](../../../../services/networking.md#routing-policies): ポリシーの一覧を確認します。
2. [ルーティングポリシーの設定](../../../../services/networking.md#routing-settings): 設定値と誤りやすい点を押さえます。
3. [Route 53 ヘルスチェック](../../../../services/networking.md#route53-health-checks): ヘルスチェックの 3 種類を覚えます。
4. [Route 53 のフェイルオーバー設計](../../../../services/resilience.md#route53-failover): フェイルオーバーの設計を確認します。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| 複数値回答 | 最大 8 個 | ヘルスチェックを付ける |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 1% だけ新環境へ | 加重（`99` と `1`） |
| 国ごとに宛先を固定 | 位置情報と既定のレコード |
| 複数の DNS の木を版で管理 | Traffic Flow |
| DNS のキャッシュに左右されない切り替え | Global Accelerator |

## 引っかかりやすい点 {#traps}

- 位置情報に既定のレコードがないと、対応のない場所には答えが返りません。
- エイリアスのターゲットの正常性は `Evaluate Target Health` で反映します。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [route53-routing 問1](../../exercises/route53-routing.md#q1) | Route 53 の機能 | Web アプリのフェイルオーバーで「ALB の 5xx の割合が高い」または「依存する Dynamo… |
| [route53-routing 問2](../../exercises/route53-routing.md#q2) | Route 53 の機能 | 5 リージョンの構成で、レイテンシー、加重、フェイルオーバーを組み合わせた DNS の木を複数のドメ… |
| [route53-routing 問3](../../exercises/route53-routing.md#q3) | Route 53 の機能 | Route 53 のエイリアスレコードで ALB を指し、ALB の配下のターゲットが全滅したときは… |
| [route53-routing 問4](../../exercises/route53-routing.md#q4) | グローバルなトラフィック管理 | 新バージョンのアプリへ、最初に全体の 1% だけを流します。旧環境と新環境はどちらも同じリージョンの… |
| [route53-routing 問5](../../exercises/route53-routing.md#q5) | グローバルなトラフィック管理 | 利用者を国ごとに決められたリージョンへ固定します（法的な要件）。位置情報レコードで日本とドイツだけを… |
| [route53-routing 問6](../../exercises/route53-routing.md#q6) | グローバルなトラフィック管理 | グローバルな API を 2 リージョンで運用しています。切り替えは数十秒以内で確実に行いたい一方、… |

<!-- questions:end -->

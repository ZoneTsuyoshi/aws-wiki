# 分野3: Global Accelerator と分散

Global Accelerator の運用と、分散のパターンを問います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [Global Accelerator](../../domain3.md#t3-3-global-accelerator) | Global Accelerator による性能と可用性の向上 |
| [分散のパターン](../../domain3.md#t3-3-lb) | 負荷分散と分散のパターン |

## 学習の順番 {#study-order}

1. [Global Accelerator](../../../../services/network-connectivity.md#global-accelerator): ダイヤル、重み、ヘルスチェックを確認します。
2. [クロスゾーン負荷分散](../../../../services/networking.md#cross-zone): クロスゾーンの計算を確認します。
3. [リスナーとルール](../../../../services/networking.md#alb-listeners): 加重ターゲットグループの動作を押さえます。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| 重み | 既定 128、0〜255 | `1` と `255` で約 0.4% |
| トラフィックダイヤル | 既定 100% | 新しい接続にのみ効く |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| リージョンの保守 | ダイヤルを 0 |
| 処理時間のばらつき | `least_outstanding_requests` |

## 引っかかりやすい点 {#traps}

- ping にはエッジが応答するので、性能の測定に使えません。
- 加重の先の片方が異常でも、自動で他方へは切り替わりません。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [global-accelerator 問4](../../exercises/global-accelerator.md#q4) | Global Accelerator | 東京と大阪のエンドポイントグループを持つアクセラレーターで、大阪の ALB を保守します。保守の前に… |
| [global-accelerator 問5](../../exercises/global-accelerator.md#q5) | Global Accelerator | 1 つのエンドポイントグループに同じ規模の ALB を 2 台登録しています。新しいバージョンの A… |
| [global-accelerator 問6](../../exercises/global-accelerator.md#q6) | Global Accelerator | アクセラレーターの EC2 エンドポイントがすべて異常と表示されます。アプリは正常に応答しており、A… |
| [global-accelerator 問7](../../exercises/global-accelerator.md#q7) | Global Accelerator | 保守で Global Accelerator を一時的に止める計画です。性能の測定の方法も運用の手順… |
| [global-accelerator 問8](../../exercises/global-accelerator.md#q8) | 分散のパターン | ALB のターゲットの処理時間のばらつきが大きく、一部のターゲットに処理中のリクエストが集中していま… |
| [global-accelerator 問9](../../exercises/global-accelerator.md#q9) | 分散のパターン | NLB の AZ A に 2 台、AZ B に 8 台のターゲットがあります。クロスゾーンは無効で、… |
| [global-accelerator 問10](../../exercises/global-accelerator.md#q10) | 分散のパターン | ALB の加重ターゲットグループで新バージョンへ 10% を流しています。新のターゲットがすべて異常… |
| [global-accelerator 問11](../../exercises/global-accelerator.md#q11) | 分散のパターン | 非 HTTP のサービスを複数のリージョンで提供しています。低遅延と固定 IP が必要で、AZ の台… |

<!-- questions:end -->

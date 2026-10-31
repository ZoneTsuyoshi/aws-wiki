# 分野1: Global Accelerator と分散

グローバルなトラフィック管理で、CloudFront や Route 53 との違いを問います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [グローバルなトラフィック管理](../../domain1.md#t1-1-global-traffic) | グローバルなトラフィック管理の設計パターン |

## 学習の順番 {#study-order}

1. [Global Accelerator](../../../../services/network-connectivity.md#global-accelerator): 固定 IP とエンドポイントの種類を確認します。
2. [Global Accelerator との比較](../../../../services/resilience.md#global-accelerator): 他のサービスとの比較を押さえます。

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 固定 IP の許可リストと UDP | 標準アクセラレーターと NLB |
| 特定の EC2 へ決定的に送る | カスタムルーティング |

## 引っかかりやすい点 {#traps}

- エンドポイントに API Gateway や S3 は指定できません。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [global-accelerator 問1](../../exercises/global-accelerator.md#q1) | グローバルなトラフィック管理 | 取引先がファイアウォールに接続先の IP を登録する必要がある MQTT のサービスを、東京とフラン… |
| [global-accelerator 問2](../../exercises/global-accelerator.md#q2) | グローバルなトラフィック管理 | オンラインゲームで、マッチメイキングのサーバーが利用者を特定のセッションの EC2 へ決定的に割り当… |
| [global-accelerator 問3](../../exercises/global-accelerator.md#q3) | グローバルなトラフィック管理 | ある企業は Web アプリの配信の改善を検討しています。Global Accelerator と C… |

<!-- questions:end -->

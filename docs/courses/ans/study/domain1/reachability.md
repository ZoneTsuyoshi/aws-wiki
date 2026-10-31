# 分野1: 到達性の検証とトポロジー

Network Manager と Reachability Analyzer の設計での位置付けを問います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [Network Manager](../../domain1.md#t1-4-network-manager) | Transit Gateway Network Manager |
| [Reachability Analyzer](../../domain1.md#t1-4-reachability) | Reachability Analyzer |

## 学習の順番 {#study-order}

1. [Route Analyzer](../../../../services/network-connectivity.md#route-analyzer): Global Networks で何が見えるかを確認します。
2. [Reachability Analyzer](../../../../services/network-connectivity.md#reachability-analyzer): 解析の範囲と制約を覚えます。

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 世界の拠点を 1 画面で | Network Manager のグローバルネットワーク |
| 変更のたびに 2 点の到達性を確認 | Reachability Analyzer |

## 引っかかりやすい点 {#traps}

- Network Manager で個々のフローは見えません。
- Reachability Analyzer は OS のファイアウォールを見ません。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [reachability 問1](../../exercises/reachability.md#q1) | Network Manager | 世界に 40 の拠点と 5 リージョンの Transit Gateway があります。複数のアカウン… |
| [reachability 問2](../../exercises/reachability.md#q2) | Network Manager | Network Manager を導入したチームが、特定の 2 台の間の通信の量と拒否の有無を知りた… |
| [reachability 問3](../../exercises/reachability.md#q3) | Network Manager | 複数のリージョンの Transit Gateway を運用するチームが、Global Network… |
| [reachability 問4](../../exercises/reachability.md#q4) | Reachability Analyzer | 新しい VPC の設計で「変更のたびに本番の DB への到達性を確認する」と決めます。本番へ通信を流… |
| [reachability 問5](../../exercises/reachability.md#q5) | Reachability Analyzer | VPC 内の 2 台の EC2 について、Reachability Analyzer が「到達可能」… |
| [reachability 問6](../../exercises/reachability.md#q6) | Reachability Analyzer | Reachability Analyzer の設計の段階での制約を確認しています。正しいものを選んで… |

<!-- questions:end -->

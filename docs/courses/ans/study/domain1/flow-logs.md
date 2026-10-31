# 分野1: フローログと Traffic Mirroring

フローログと Traffic Mirroring を、取得するものと費用で使い分ける問題です。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [フローログと Traffic Mirroring](../../domain1.md#t1-4-flow-mirror) | フローログと Traffic Mirroring |

## 学習の順番 {#study-order}

1. [フローログの分析](../../../../services/network-connectivity.md#flow-log-analysis): 形式と作成後の変更の制限を確認します。
2. [Traffic Mirroring](../../../../services/network-connectivity.md#traffic-mirroring): 対象の絞り方を押さえます。

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 常時の記録 | フローログ |
| IDS とフォレンジック | Traffic Mirroring を必要な ENI に |

## 引っかかりやすい点 {#traps}

- フローログは作成後に変更できません。追加のフィールドが要るときは作り直します。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [flow-logs 問1](../../exercises/flow-logs.md#q1) | フローログと Traffic Mirroring | 全 VPC の通信の有無を常に記録し、特定の ENI のパケットだけは IDS へ送ります。ログの費… |
| [flow-logs 問2](../../exercises/flow-logs.md#q2) | フローログと Traffic Mirroring | 既定の形式のフローログを作成済みです。NAT の裏の元の IP を見るため pkt-srcaddr … |
| [flow-logs 問3](../../exercises/flow-logs.md#q3) | フローログと Traffic Mirroring | 不審なホストの通信を調査します。通信先と時刻は既に分かり、次にペイロードを確認します。TLS ではな… |

<!-- questions:end -->

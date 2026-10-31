# 分野1: Transit Gateway と SD-WAN

SD-WAN とオーバーレイの設計を問います。Connect の条件を押さえます。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [SD-WAN とオーバーレイ](../../domain1.md#t1-5-sdwan) | オーバーレイネットワーク、SD-WAN の統合（Connect、オーバーレイ） |

## 学習の順番 {#study-order}

1. [Connect](../../../../services/network-connectivity.md#tgw-connect): 土台、帯域、ECMP の条件を確認します。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| Connect の帯域 | ピアあたり 5 Gbps、4 ピアで 20 Gbps | 同じ AS_PATH と ASN |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| SD-WAN を VPN より大きな帯域で | Connect |

## 引っかかりやすい点 {#traps}

- GRE に暗号化はありません。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [transit-gateway 問1](../../exercises/transit-gateway.md#q1) | SD-WAN とオーバーレイ | SD-WAN の仮想アプライアンスを VPC に置き、Transit Gateway と接続します。… |
| [transit-gateway 問2](../../exercises/transit-gateway.md#q2) | SD-WAN とオーバーレイ | Connect のピア 4 つで最大の帯域を得る計画です。アプライアンスは同じプレフィックスを広告し… |
| [transit-gateway 問3](../../exercises/transit-gateway.md#q3) | SD-WAN とオーバーレイ | SD-WAN のオーバーレイの土台（アンダーレイ）を設計します。データセンターのルーターから直接 T… |

<!-- questions:end -->

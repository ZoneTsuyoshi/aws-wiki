# 分野3: Direct Connect

接続方式の運用を問います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [接続方式の運用](../../domain3.md#t3-1-connectivity) | 接続方法（DX ゲートウェイ、Transit Gateway、VIF） |

## 学習の順番 {#study-order}

1. [Direct Connect ゲートウェイ](../../../../services/network-connectivity.md#dx-gateway): 許可プレフィックスと関連付けを確認します。
2. [DX の VIF](../../../../services/network-connectivity.md#choosing-vif): VIF の範囲を確認します。

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 新しい VPC の経路がオンプレミスへ来ない | 許可プレフィックスを確認 |

## 引っかかりやすい点 {#traps}

- スーパーネットの広告で、関連付け同士が通信できることがあります。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [direct-connect 問10](../../exercises/direct-connect.md#q10) | 接続方式の運用 | Transit Gateway と DX ゲートウェイをトランジット VIF で接続しています。新し… |
| [direct-connect 問11](../../exercises/direct-connect.md#q11) | 接続方式の運用 | DX ゲートウェイに VGW と Transit Gateway の両方を関連付けようとしています。… |
| [direct-connect 問12](../../exercises/direct-connect.md#q12) | 接続方式の運用 | DX ゲートウェイに関連付けた 2 つの VGW の VPC が、互いに通信できるようになってしまい… |

<!-- questions:end -->

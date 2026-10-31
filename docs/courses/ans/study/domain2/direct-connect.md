# 分野2: Direct Connect

物理接続の開通と、既存のネットワークとの接続の実装を問います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [物理接続](../../domain2.md#t2-1-physical) | L1 とハードウェア（LOA、コロケーション、DX）、L2、L3（VLAN、IP、ゲートウェイ、ルーティング、スイッチング）、物理のネットワーク要件の構成 |
| [既存のネットワーク](../../domain2.md#t2-1-onprem) | 既存のオンプレミスネットワークの接続 |

## 学習の順番 {#study-order}

1. [接続の種類](../../../../services/network-connectivity.md#dx-connections): 開通の手順を確認します。
2. [VIF の種類](../../../../services/network-connectivity.md#dx-vif-types): VIF の設定を覚えます。
3. [経路数の上限に当たったとき](../../../../services/network-connectivity.md#bgp-route-limits): 経路数の上限を押さえます。
4. [MTU と MSS](../../../../services/network-connectivity.md#vpn-mtu): MSS の調整を確認します。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| ポートの割り当て | 最大 72 営業時間 | 審査を含む |
| 課金の開始 | 有効化か、LOA 発行から 90 日 | 早いほう |
| 既存の経路 | 上限 100 | 集約する |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 接続が down | L1 を確認 |
| 接続は up で VIF が down | VLAN を確認 |
| BGP が確立しない | ASN、ピア IP、MD5 を確認 |

## 引っかかりやすい点 {#traps}

- ファイアウォールでは UDP 500、UDP 4500、TCP 179 を確認します。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [direct-connect 問4](../../exercises/direct-connect.md#q4) | 物理接続 | 新しい専用接続で、ポートの状態は down です。LOA-CFA をコロケーション事業者に渡してクロ… |
| [direct-connect 問5](../../exercises/direct-connect.md#q5) | 物理接続 | 新しい DX で、接続は up なのにプライベート VIF が down のままです。BGP はまだ… |
| [direct-connect 問6](../../exercises/direct-connect.md#q6) | 物理接続 | データセンターの移転で DX の専用接続を発注しましたが、配線の工事は 4 か月後です。その間の費用… |
| [direct-connect 問16](../../exercises/direct-connect.md#q16) | 既存のネットワーク | オンプレミスの 10.1.0.0/24 から 10.1.255.0/24 までを 1 つずつ VPN… |
| [direct-connect 問17](../../exercises/direct-connect.md#q17) | 既存のネットワーク | 既存の企業ネットワークに Site-to-Site VPN を追加します。ファイアウォールで許可すべ… |
| [direct-connect 問18](../../exercises/direct-connect.md#q18) | 既存のネットワーク | 既存のオンプレミスの 192.168.0.0/16 と AWS の VPC を接続します。接続の前の… |

<!-- questions:end -->

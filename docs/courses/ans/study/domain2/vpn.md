# 分野2: VPN とカプセル化

VPN の設定と Client VPN の認証を問います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [VPN](../../domain2.md#t2-1-vpn) | VPN（セキュリティ、アクセラレーション） |
| [認証と認可](../../domain2.md#t2-2-auth) | 認証と認可（SAML、Active Directory） |

## 学習の順番 {#study-order}

1. [トンネル](../../../../services/network-connectivity.md#vpn-tunnels): 帯域とトンネルの本数を確認します。
2. [トンネルオプション](../../../../services/network-connectivity.md#vpn-tunnel-options): DPD と開始アクションを覚えます。
3. [アクセラレーション](../../../../services/network-connectivity.md#vpn-accelerated): アクセラレーションの制約を押さえます。
4. [Client VPN](../../../../services/network-connectivity.md#client-vpn): 認証と 3 点セットを確認します。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| トンネルの帯域 | 標準 1.25 Gbps、LBT 5 Gbps | LBT は Transit Gateway と Cloud WAN |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 接続できるのに届かない | ルート、認可ルール、SG |

## 引っかかりやすい点 {#traps}

- アクセラレーションは作成時にしか有効にできません。
- Client VPN の認可ルールは既定で何もなく、全部拒否です。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [vpn 問1](../../exercises/vpn.md#q1) | VPN | 既存の Transit Gateway の VPN 接続で、遠隔地からの通信の品質を上げるためアクセ… |
| [vpn 問2](../../exercises/vpn.md#q2) | VPN | 通信がしばらくないと VPN のトンネルが落ち、次に通信を始めると遅れます。CGW からは定期的な通… |
| [vpn 問3](../../exercises/vpn.md#q3) | VPN | Site-to-Site VPN を 1 接続だけ作り、CGW にはトンネル 1 だけを設定しました… |
| [vpn 問13](../../exercises/vpn.md#q13) | 認証と認可 | Client VPN に接続できる利用者が、VPC の DB サーバーへ届きません。Active D… |
| [vpn 問14](../../exercises/vpn.md#q14) | 認証と認可 | Client VPN で、社内の SAML の IdP と連携して利用者を認証します。証明書の配布は… |
| [vpn 問15](../../exercises/vpn.md#q15) | 認証と認可 | 社内の AD の管理者に、複数の AWS アカウントのネットワークの管理を許可します。AD のアカウ… |

<!-- questions:end -->

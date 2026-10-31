# 分野2: ネットワークのセキュリティ

境界のセキュリティとアプライアンスの実装を問います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [アプライアンス](../../domain2.md#t2-1-appliances) | セキュリティアプライアンス |
| [境界のセキュリティ](../../domain2.md#t2-2-security) | セキュリティ（SG、NACL、Network Firewall）、ネットワーク境界のセキュリティの実装 |

## 学習の順番 {#study-order}

1. [アプライアンスモード](../../../../services/network-connectivity.md#tgw-appliance-mode): アプライアンスモードの設定場所を確認します。
2. [ネットワーク機能アタッチメント](../../../../services/network-connectivity.md#tgw-network-function): ネットワーク機能アタッチメントを覚えます。
3. [ステートフルのルール順序](../../../../services/network-connectivity.md#nfw-rule-order): Strict の既定アクションを押さえます。
4. [セキュリティグループとネットワーク ACL](../../../../services/networking.md#security-groups-nacls): 層と状態を整理します。

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| AZ をまたぐ通信だけ切れる | 検査 VPC のアタッチメントでアプライアンスモード |
| スポークの通信がルールに一致しない | `HOME_NET` を上書き |

## 引っかかりやすい点 {#traps}

- ステートレスの既定を `Pass` にするとステートフルが評価されません。
- `RuleOrder` はポリシーの作成時にしか指定できません。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [network-security 問1](../../exercises/network-security.md#q1) | アプライアンス | スポーク VPC の通信を、Transit Gateway の検査 VPC の Network Fi… |
| [network-security 問2](../../exercises/network-security.md#q2) | アプライアンス | Transit Gateway の VPC 間の通信を Network Firewall で検査しま… |
| [network-security 問3](../../exercises/network-security.md#q3) | アプライアンス | 第三者の仮想ファイアウォールで VPC の全ポートの通信を透過的に検査します。ファイアウォールは冗長… |
| [network-security 問4](../../exercises/network-security.md#q4) | 境界のセキュリティ | 集中型の Network Firewall で、スポーク VPC の通信がステートフルのルールに一致… |
| [network-security 問5](../../exercises/network-security.md#q5) | 境界のセキュリティ | Network Firewall の Strict のルール順序で、特定のドメインへの HTTPS … |
| [network-security 問6](../../exercises/network-security.md#q6) | 境界のセキュリティ | 3 層のアプリと複数の VPC の間の境界を設計します。戻りの通信で過去に障害がありました。手段の説… |

<!-- questions:end -->

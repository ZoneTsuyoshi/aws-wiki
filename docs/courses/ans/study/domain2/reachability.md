# 分野2: 到達性の検証とトポロジー

接続のテストのツールの使い分けと、マルチアカウントの注意を問います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [テストと検証](../../domain2.md#t2-1-testing) | 接続のテスト（Route Analyzer、Reachability Analyzer）、環境間の接続のテストと検証 |
| [接続のテスト](../../domain2.md#t2-2-testing) | 接続のテスト（Route Analyzer、Reachability Analyzer、ツール） |

## 学習の順番 {#study-order}

1. [接続の調査](../../../../services/network-connectivity.md#network-analysis): ツールの一覧を確認します。
2. [Route Analyzer](../../../../services/network-connectivity.md#route-analyzer): 同じリージョンのピアリングの制約を押さえます。
3. [Network Access Analyzer](../../../../services/network-connectivity.md#network-access-analyzer): 環境全体の確認を理解します。

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 環境間の検証の順序 | 物理、BGP、ルート、SG と NACL、アプリ |
| 別のアカウントの解析 | 信頼されたアクセスを有効に |

## 引っかかりやすい点 {#traps}

- Route Analyzer は SG と NACL を見ません。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [reachability 問7](../../exercises/reachability.md#q7) | テストと検証 | Transit Gateway の VPC と VPN の間で、Transit Gateway のル… |
| [reachability 問8](../../exercises/reachability.md#q8) | テストと検証 | オンプレミスから VPC の EC2 への通信が失敗します。DX の接続、VIF、BGP、VPC と… |
| [reachability 問9](../../exercises/reachability.md#q9) | テストと検証 | EC2 からオンプレミスのサーバーへ、DX と VPN の経路ごとに経路の MTU を確認します。I… |
| [reachability 問10](../../exercises/reachability.md#q10) | 接続のテスト | 組織の全 VPC で「本番から開発へ到達する経路がない」ことを定期的に確認します。特定の 2 点を列… |
| [reachability 問11](../../exercises/reachability.md#q11) | 接続のテスト | 別のアカウントのリソースへの経路を Reachability Analyzer で解析します。両方の… |
| [reachability 問12](../../exercises/reachability.md#q12) | 接続のテスト | 同じリージョンの 2 つの Transit Gateway をピアリングしています。Route An… |

<!-- questions:end -->

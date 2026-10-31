# 分野1: マルチ VPC とマルチアカウント

VPC の接続パターン、VPC 共有、IP の重複、アカウント間の共有を問います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [接続パターン](../../domain1.md#t1-6-patterns) | 接続パターンと用途（ピアリング、Transit Gateway、PrivateLink）、要件に合う方法で複数の VPC を接続 |
| [VPC 共有](../../domain1.md#t1-6-vpc-sharing) | VPC 共有の機能と利点、マルチアカウントでの VPC 共有 |
| [IP の重複](../../domain1.md#t1-6-overlap) | IP サブネットと重複への対処、IP の重複の管理（NAT、PrivateLink、Transit Gateway のルーティング） |
| [リソース共有](../../domain1.md#t1-5-sharing) | アカウント間のリソース共有 |

## 学習の順番 {#study-order}

1. [VPC 同士の接続](../../../../services/network-connectivity.md#choosing-multi-vpc): 接続の単位、推移、CIDR の重複で比較します。
2. [VPC Lattice](../../../../services/network-connectivity.md#vpc-lattice): サービス単位の接続と認証ポリシーを確認します。
3. [VPC サブネットの共有](../../../../services/governance.md#ram-vpc-sharing): オーナーと参加者の権限の分担を覚えます。
4. [1:1 NAT](../../../../services/network-connectivity.md#tgw-nat): 1:1 NAT の制約を押さえます。
5. [NAT ゲートウェイ](../../../../services/network-connectivity.md#nat-gateway): プライベート NAT の配置を確認します。
6. [IPAM](../../../../services/network-connectivity.md#ipam): 重複の予防の方法を確認します。
7. [AWS Resource Access Manager](../../../../services/governance.md#ram): 共有できるものと方法を整理します。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| メッシュのピアリングの本数 | `n(n-1)/2` | 10 個で 45 本 |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| SaaS を顧客の VPC へ公開 | PrivateLink |
| アカウントを分け、VPC は中央で管理 | VPC 共有 |
| 重複があり、VPC から外へ | プライベート NAT ゲートウェイ |
| 重複があり、全体で両方向 | Transit Gateway の 1:1 NAT |
| 別のアカウントの Transit Gateway と DX ゲートウェイ | 関連付けの提案と承認 |

## 引っかかりやすい点 {#traps}

- 参加者はルートテーブル、NACL を変更できず、NAT ゲートウェイも作れません。
- DX ゲートウェイは RAM では共有しません。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [multi-account 問1](../../exercises/multi-account.md#q1) | 接続パターン | SaaS の事業者が API を多数の顧客の VPC へ公開します。顧客の CIDR は事業者と重複… |
| [multi-account 問2](../../exercises/multi-account.md#q2) | 接続パターン | 20 の VPC にまたがるマイクロサービスで、サービス単位の接続と IAM の認可を使います。一部… |
| [multi-account 問3](../../exercises/multi-account.md#q3) | 接続パターン | 10 個の VPC が相互に通信し、今後も増える見込みです。ネットワークチームはオンプレミスの接続も… |
| [multi-account 問4](../../exercises/multi-account.md#q4) | VPC 共有 | 5 つのアプリチームをアカウントで分け、請求も分けます。ネットワークは中央のチームが管理し、アプリ同… |
| [multi-account 問5](../../exercises/multi-account.md#q5) | VPC 共有 | VPC 共有の参加者のアプリチームが、共有サブネットで作業します。参加者のアカウントでできることを選… |
| [multi-account 問6](../../exercises/multi-account.md#q6) | VPC 共有 | オーナーのアカウントが RAM でサブネットを共有しようとしましたが、組織を共有先に選べません。オー… |
| [multi-account 問7](../../exercises/multi-account.md#q7) | IP の重複 | VPC（10.0.0.0/16）がオンプレミスと重複しています。VPC からオンプレミスのサーバーへ… |
| [multi-account 問8](../../exercises/multi-account.md#q8) | IP の重複 | 買収した会社の VPC と CIDR が重複しています。ネットワーク全体で両方向に通信する必要があり… |
| [multi-account 問9](../../exercises/multi-account.md#q9) | IP の重複 | 組織の各アカウントが VPC を自由に作っており、重複の問題が繰り返されています。今後の VPC の… |
| [multi-account 問10](../../exercises/multi-account.md#q10) | リソース共有 | ネットワークアカウントが Transit Gateway とそのルートテーブルを管理し、各アプリのア… |
| [multi-account 問11](../../exercises/multi-account.md#q11) | リソース共有 | アカウント X の Transit Gateway を、ネットワークアカウントの DX ゲートウェイ… |
| [multi-account 問12](../../exercises/multi-account.md#q12) | リソース共有 | ネットワークアカウントが物理の DX を持ち、別のアカウントが所有する DX ゲートウェイを使うチー… |

<!-- questions:end -->

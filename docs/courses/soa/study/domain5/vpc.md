# 分野5: VPC の設定と調査

経路とフィルターの切り分け、費用の削減を問います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [5.1.1](../../domain5.md#skill-5-1-1) | VPC の設定 |
| [5.1.4](../../domain5.md#skill-5-1-4) | ネットワークのコスト最適化 |
| [5.3.1](../../domain5.md#skill-5-3-1) | VPC の設定の調査 |

## 学習の順番 {#study-order}

1. [サブネットとルートテーブル](../../../../services/networking.md#subnets-route-tables)と[セキュリティグループとネットワーク ACL](../../../../services/networking.md#security-groups-nacls): 部品の役割を確認します。
2. [NAT ゲートウェイ](../../../../services/network-connectivity.md#nat-gateway)と[IPv6 と Egress-only インターネットゲートウェイ](../../../../services/network-connectivity.md#ipv6): 外向きの通信を確認します。
3. [VPC の DNS 属性](../../../../services/networking.md#vpc-dns-attributes): 2 つの属性を確認します。
4. [データ転送の費用](../../../../services/cost-management.md#data-transfer)と[Elastic IP](../../../../services/network-connectivity.md#elastic-ip): 料金を確認します。
5. [接続できないときの切り分け](../../../../services/networking.md#vpc-troubleshooting)と[Reachability Analyzer](../../../../services/network-connectivity.md#reachability-analyzer): 調査の順序を確認します。
6. [ルートテーブル](../../../../services/network-connectivity.md#tgw-route-tables)と[アプライアンスモード](../../../../services/network-connectivity.md#tgw-appliance-mode): Transit Gateway の確認を押さえます。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| パブリック IPv4 | 0.005 USD/時 | 使わないものを解放する |
| インターネットへの転送 | 月 100 GB まで無料 | 超えると有料 |
| NAT の同時接続 | 同じ宛先に IP あたり 55,000 | `ErrorPortAllocation` |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| IPv6 の外向きのみ | Egress-only インターネットゲートウェイ |
| 特定の IP を拒否する | ネットワーク ACL |
| NAT 経由の S3 の費用が高い | ゲートウェイエンドポイント |
| 受信 `ACCEPT`、送信 `REJECT` | NACL のエフェメラルポート |
| 本番に影響なく経路を確認する | Reachability Analyzer |
| ALB の 503 | 登録済みのターゲットがない |

## 引っかかりやすい点 {#traps}

- セキュリティグループはステートフルで、許可のみです。
- NAT ゲートウェイにセキュリティグループは付けられません。
- Transit Gateway は両方の VPC のルートテーブルも確認します。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [vpc 問1](../../exercises/vpc.md#q1) | 5.1.1 | プライベートサブネットの EC2 からインターネットへ出られません。NAT ゲートウェイはあります。… |
| [vpc 問2](../../exercises/vpc.md#q2) | 5.1.1 | IPv6 の EC2 から外へだけ通信させ、インターネットからの接続は受けたくありません。どれを使い… |
| [vpc 問3](../../exercises/vpc.md#q3) | 5.1.1 | 特定の IP アドレスからの通信だけをサブネットの単位で拒否したいです。どこで設定しますか。 |
| [vpc 問4](../../exercises/vpc.md#q4) | 5.1.1 | インターフェイスエンドポイントのプライベート DNS を使うために、VPC で有効にする属性の組み合… |
| [vpc 問5](../../exercises/vpc.md#q5) | 5.1.1 | パブリックサブネットの EC2 にインターネットから届きません。IGW と SG は正しいです。確認… |
| [vpc 問6](../../exercises/vpc.md#q6) | 5.1.4 | プライベートサブネットから S3 へ毎日数 TB を転送し、NAT ゲートウェイの費用が高くなってい… |
| [vpc 問7](../../exercises/vpc.md#q7) | 5.1.4 | AZ 間のデータ転送の費用が高いです。a の AZ の NAT ゲートウェイを、b と c の AZ… |
| [vpc 問8](../../exercises/vpc.md#q8) | 5.1.4 | パブリック IPv4 の費用が増えています。使用状況を確認して減らしたいです。正しいものを選んでくだ… |
| [vpc 問9](../../exercises/vpc.md#q9) | 5.1.4 | データ転送の料金の説明として正しいものを選んでください。（2つ選択） |
| [vpc 問10](../../exercises/vpc.md#q10) | 5.1.4 | プライベートサブネットで NAT 経由の DynamoDB の通信が大半を占めています。インターフェ… |
| [vpc 問11](../../exercises/vpc.md#q11) | 5.3.1 | VPC フローログに、受信の ACCEPT と送信の REJECT が並んでいます。セキュリティグル… |
| [vpc 問12](../../exercises/vpc.md#q12) | 5.3.1 | 本番に影響なく、EC2 からデータベースまでの経路が設定上通るかを確認し、どの設定が止めているかを知… |
| [vpc 問13](../../exercises/vpc.md#q13) | 5.3.1 | デプロイの直後から、ALB が 503 を返すようになりました。ターゲットのアプリのプロセスは動いて… |
| [vpc 問14](../../exercises/vpc.md#q14) | 5.3.1 | Transit Gateway でつないだ 2 つの VPC の間が通りません。アタッチメントは両方… |
| [vpc 問15](../../exercises/vpc.md#q15) | 5.3.1 | Transit Gateway の AZ の問題です。検査用の機器を置いた VPC を通ると、一部の… |
| [vpc 問16](../../exercises/vpc.md#q16) | 5.3.1 | NAT ゲートウェイの ErrorPortAllocation が増え、同じ宛先への接続に失敗します… |

<!-- questions:end -->

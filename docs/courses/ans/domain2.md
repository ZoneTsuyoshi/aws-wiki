# 分野2: ネットワークの実装

配点は **26%** です。分野1で選んだ設計を、設定値のレベルで実装する力を問います。

症状から設定の誤りを見つける問題が多く出ます。VLAN、ASN、MD5、関連付けと伝播など、「どこに何を設定するか」を手順で覚えます。

この分野に限らず、コース全体で使うサービスは[サービス一覧](services.md)から確認できます。

## タスク 2.1: オンプレミスと AWS の接続とルーティングを実装する {#task-2-1}

### ルーティングプロトコルの設定 {#t2-1-routing}

| 接続 | 静的 | 動的 |
|---|---|---|
| Direct Connect | 不可。VIF は BGP | BGP（MD5 は既定で有効） |
| Site-to-Site VPN | VPN 接続に手で登録 | BGP。ECMP は Transit Gateway で動的のみ |
| Transit Gateway ピアリング | **静的のみ** | 不可 |
| Transit Gateway Connect | 不可 | BGP のみ |

**VPC 側の忘れやすい設定:**

- VGW の経路をサブネットへ反映するには、ルートテーブルで伝播を有効にします。
- Transit Gateway は VPC のルートテーブルを自動では変えません。宛先と `tgw-` を追加します。

**BGP の症状:**

| 症状 | 確認すること |
|---|---|
| BGP が確立しない | ASN、ピア IP、MD5 キー |
| `idle` で DOWN になり全経路が消えた | 広告した経路が上限（既定 100）を超えた |
| 経路は来ているが通信できない | VPC 側のルートテーブル、SG、NACL |

詳細: [VPN のルーティング](../../services/network-connectivity.md#vpn-routing)、[ルートテーブル](../../services/network-connectivity.md#tgw-route-tables)、[経路数の上限](../../services/network-connectivity.md#bgp-route-limits)

### VPN の設定とセキュリティ {#t2-1-vpn}

| 項目 | 押さえる値 |
|---|---|
| トンネル | 1 接続に 2 本、別々の AZ。**両方を設定する** |
| 帯域 | 標準 1.25 Gbps、Large Bandwidth Tunnel 5 Gbps（Transit Gateway、Cloud WAN のみ） |
| IKE | IKEv2 を推奨。AWS から開始できるのは IKEv2 のみ |
| フェーズのライフタイム | フェーズ 1 は 28,800 秒、フェーズ 2 は 3,600 秒 |
| DPD のアクション | `Clear`（既定）、`None`、`Restart` |
| 開始アクション | `Add`（既定、CGW が開始）、`Start` |

**アクセラレーションの制約:** Transit Gateway のみで、作成時にしか有効にできません。既存の接続は作り直します。Large Bandwidth Tunnel とは併用できません。

**帯域の計算:** 標準トンネルで 8 Gbps なら `8 / 1.25 = 6.4` で 7 本以上、つまり VPN 接続 4 本を BGP と ECMP で束ねます。VGW は ECMP に対応しないので Transit Gateway を使います。

**症状:** 通信がしばらくないとトンネルが落ちる場合は、`StartupAction=start` と `DPDTimeoutAction=restart` にするか、キープアライブを流します。

詳細: [トンネル](../../services/network-connectivity.md#vpn-tunnels)、[トンネルオプション](../../services/network-connectivity.md#vpn-tunnel-options)、[アクセラレーション](../../services/network-connectivity.md#vpn-accelerated)

### 物理接続の構成 {#t2-1-physical}

**専用接続を開通させる流れ:**

1. コンソールで接続を要求します。審査とポート割り当てに最大 72 営業時間かかります。
2. LOA-CFA をダウンロードし、ネットワーク事業者かコロケーション事業者にクロスコネクトを発注します。
3. ポートが有効になると課金が始まります。有効にならなくても、LOA の発行から 90 日で始まります。
4. VIF を作り、ルーターで VLAN と BGP を設定します。

| 層 | 設定 | 誤ったときの症状 |
|---|---|---|
| L1 | シングルモード、対応する光モジュール、オートネゴシエーション | 接続が down |
| L2 | 802.1Q の VLAN（1〜4094）。作成後は変更不可 | 接続は up だが VIF が down |
| L3 | ピア IP、ゲートウェイ、BGP の ASN | BGP が確立しない |

**ホスト接続:** Direct Connect パートナーから申し込みます。VIF は **1 個**だけで、コンソールからは発注できません。超過分はポリシングで破棄されます。

詳細: [接続の種類](../../services/network-connectivity.md#dx-connections)、[VIF の種類](../../services/network-connectivity.md#dx-vif-types)

### トラフィック管理と SD-WAN {#t2-1-sdwan}

Connect の実装手順です。

1. Transit Gateway に CIDR を設定します（例: `192.0.2.0/24`）。
2. VPC か DX のアタッチメントを土台に、Connect アタッチメントを作ります。
3. ピアを作り、`169.254.0.0/16` の /29 を内部 CIDR に指定します。
4. アプライアンスの VPC のルートテーブルに `192.0.2.0/24 → tgw-` を入れます。
5. アプライアンスに GRE と BGP を設定します。内部 CIDR が `169.254.6.0/29` なら、BGP アドレスは `169.254.6.1` です。

eBGP は `ebgp-multihop`（TTL 2）にします。MTU は外部 1500 なら内側を 1476 にします。

詳細: [Connect](../../services/network-connectivity.md#tgw-connect)

### ハイブリッドの名前解決 {#t2-1-dns}

既存のオンプレミス DNS を AWS とつなぐ手順です。

| 目的 | AWS 側 | オンプレミス側 |
|---|---|---|
| オンプレミスから AWS を引く | インバウンドエンドポイント、PHZ の関連付け | `aws.example.com` を条件付き転送 |
| AWS からオンプレミスを引く | アウトバウンドエンドポイント、Forward ルール、VPC への関連付け | DNS サーバーへの通信を許可 |

**オンプレミスから VPC+2 へは転送しません。** 公式に非対応です。

**条件付き転送の例外:** `example.com` を転送しつつ `acme.example.com` だけ VPC で解決するなら、System ルールを足します。最も具体的なルールが使われます。

**遅いとき:** ターゲット IP のどれかに届かないと解決が延びます。全ターゲットへの経路と SG を確認します。

詳細: [転送ルール](../../services/network-connectivity.md#resolver-rules)、[ハイブリッド DNS](../../services/network-connectivity.md#hybrid-dns)

### セキュリティアプライアンス {#t2-1-appliances}

オンプレミスと AWS の境界に置くファイアウォールの実装です。

| 方式 | 実装のポイント |
|---|---|
| Network Firewall を検査 VPC に | Transit Gateway の検査 VPC のアタッチメントでアプライアンスモードを有効に |
| ネットワーク機能アタッチメント | Network Firewall を Transit Gateway に直接付ける。アプライアンスモードは自動 |
| 第三者のファイアウォール | GWLB とエンドポイント |
| VPC 内のアプライアンスへの経路 | VPC Route Server で BGP の経路を反映 |

**アプライアンスモードがないと:** 行きと戻りが別の AZ の機器を通り、ステートフルな機器が破棄します。同じ AZ の通信は通るのに AZ をまたぐと切れる、という症状になります。

詳細: [アプライアンスモード](../../services/network-connectivity.md#tgw-appliance-mode)、[ネットワーク機能アタッチメント](../../services/network-connectivity.md#tgw-network-function)、[VPC Route Server](../../services/network-connectivity.md#route-server)

### 負荷分散の実装 {#t2-1-load-balancing}

| 層 | 実装 | 使いどころ |
|---|---|---|
| L3 | GWLB | 全ポートのパケットをアプライアンスへ |
| L4 | NLB | 固定 IP、非 HTTP、TLS パススルー |
| L7 | ALB | リバースプロキシとして、パスやホストで振り分け |

**ヘルスチェックの計算:** ALB の既定なら、異常と判定されるまで `30 × 2 = 60` 秒です。間隔 10 秒、`UnhealthyThresholdCount` 2 にすれば約 20 秒です。

**ALB のエラーの切り分け:**

| コード | 意味 | 確認すること |
|---|---|---|
| 502 | 応答がおかしい | ターゲットのキープアライブが ALB より短くないか |
| 503 | 送り先がいない | 登録済みのターゲット |
| 504 | 応答が来ない | アイドルタイムアウト、NACL のエフェメラルポート |

詳細: [ヘルスチェックの計算](../../services/networking.md#health-check-calc)、[ALB のエラーの原因一覧](../../services/networking.md#alb-error-detail)、[アイドルタイムアウト](../../services/networking.md#alb-idle-timeout)、[負荷分散の設計](domain1.md#t1-3-choose)

### インフラの自動化 {#t2-1-automation}

ハイブリッド接続のうち、AWS 側のリソースはコードで作れます。

| 作れるもの | 作れないもの、人手が要るもの |
|---|---|
| VIF、DX ゲートウェイ、Transit Gateway、VPN 接続、ルートテーブル | 物理の配線、クロスコネクト |
| Resolver エンドポイントとルール | パートナーやオンプレミス側の設定 |

全体の進め方は [タスク 2.4](#task-2-4) で扱います。

詳細: [CloudFormation テンプレート](../../services/iac.md#cloudformation-template)、[StackSets](../../services/iac.md#nested-stacks-stacksets)

### Organizations と RAM による共有 {#t2-1-org-ram}

| リソース | 共有の仕組み | 手順 |
|---|---|---|
| Transit Gateway | RAM | 共有先がアタッチメントを作る。`AutoAcceptSharedAttachments` が無効なら所有者が承認 |
| Direct Connect ゲートウェイ | 関連付けの提案 | 相手のアカウントが提案し、所有者が承認。承認時に許可プレフィックスを変更できる |
| VPC のサブネット | RAM | 参加者がサブネットにリソースを作る |
| Route 53 の Resolver ルール | RAM | 共有先が自分の VPC に関連付ける |
| PHZ | 関連付けの許可（RAM ではない） | CLI か API で許可し、相手が関連付ける |

**組織の共有:** 管理アカウントで `enable-sharing-with-aws-organization` を実行します。無効のままだと招待が必要になったり、OU を指定できなかったりします。

詳細: [AWS Resource Access Manager](../../services/governance.md#ram)、[プライベートホストゾーン](../../services/network-connectivity.md#private-hosted-zones)、[マルチアカウントのパターン](../../services/governance.md#multi-account-patterns)

### 接続のテストと検証 {#t2-1-testing}

| ツール | 調べること | 調べないこと |
|---|---|---|
| Route Analyzer | Transit Gateway のルートテーブルの経路 | SG、NACL |
| Reachability Analyzer | SG、NACL、ルートを含む 2 点間 | OS のファイアウォール、Connect の先 |
| `ping`、`traceroute`、`tracepath` | 実パケットの到達と MTU | ICMP を止めている機器の先 |
| DX のフェイルオーバーテスト | BGP を止めたときの切り替え | |

**環境間の検証の順序:** 物理（接続と VIF の状態）→ BGP（受信した経路）→ AWS のルートテーブル → SG と NACL → アプリの順に確かめます。

詳細: [接続の調査](../../services/network-connectivity.md#network-analysis)、[Route Analyzer](../../services/network-connectivity.md#route-analyzer)、[回復性のモデル](../../services/network-connectivity.md#dx-resiliency)

### VPC のネットワークサービス {#t2-1-vpc-services}

| 部品 | 役割 |
|---|---|
| IGW | インターネットとの入口 |
| NAT ゲートウェイ | 内から外へ。同じ宛先へ IP あたり 55,000 接続 |
| Egress-only IGW | IPv6 で内から外へ |
| VGW | VPN と DX の VPC 側の終端 |
| VPC エンドポイント | AWS サービスへプライベートに接続 |
| DHCP オプションセット | DNS サーバーやドメイン名を配布 |

**経路の制約:** オンプレミスから VGW 経由で NAT ゲートウェイへは出られません。Transit Gateway 経由なら集中型の出口にできます。ゲートウェイエンドポイントには VPC の外から届きません。オンプレミスから S3 へプライベートに接続するならインターフェイスエンドポイントです。

詳細: [VPC の基本](../../services/networking.md#vpc)、[NAT と Elastic IP](../../services/network-connectivity.md#nat-eip)、[IPv6](../../services/network-connectivity.md#ipv6)、[エンドポイントの選び方](../../services/networking.md#endpoint-settings)

### 既存のオンプレミスネットワークとの接続 {#t2-1-onprem}

既存のネットワークに AWS をつなぐときの確認項目です。

| 確認項目 | 内容 |
|---|---|
| CIDR | 既存と重複しないか。重複するなら [IP の重複への対処](domain1.md#t1-6-overlap) |
| 経路の数 | 上限の 100 に収まるか。超えるなら集約する |
| ファイアウォール | IKE（UDP 500）、NAT-T（UDP 4500）、BGP（TCP 179） |
| CGW の機能 | BGP、MD5、ジャンボフレーム、DPD、IKEv2 |
| MTU | CGW で MSS を調整する。AES-GCM-16 で NAT-T なしなら MSS 1406 |

**集約の例:** `10.1.0.0/24` から `10.1.255.0/24` までを 1 つずつ広告すると 256 経路です。`10.1.0.0/16` にまとめれば 1 経路です。

詳細: [MTU と MSS](../../services/network-connectivity.md#vpn-mtu)、[経路数の上限](../../services/network-connectivity.md#bgp-route-limits)

### ネットワークの監視とログの設定 {#t2-1-monitoring}

| 対象 | 設定 |
|---|---|
| VPC | フローログを CloudWatch Logs か S3、Firehose へ |
| Transit Gateway | Transit Gateway フローログ |
| VPN | トンネルログを CloudWatch Logs へ。IKE と DPD の調査に使う |
| Client VPN | 接続ログを CloudWatch Logs へ |
| Direct Connect | メトリクスとアラーム |

詳細: [フローログの分析](../../services/network-connectivity.md#flow-log-analysis)、[要件の特定](domain1.md#t1-4-requirements)

## タスク 2.2: マルチアカウント、マルチリージョン、マルチ VPC の接続を実装する {#task-2-2}

### VPC 間とアカウント間の接続 {#t2-2-multi-vpc}

| 方法 | 実装の要点 |
|---|---|
| VPC ピアリング | 要求、承認（7 日で失効）、**両方**のルートテーブルに経路 |
| Transit Gateway | アタッチメント、関連付け、伝播、VPC 側の経路 |
| Transit Gateway ピアリング | 静的ルートのみ。両側に追加。ASN は別々 |
| VPN | Transit Gateway に VPN をアタッチして ECMP |
| 第三者製、SD-WAN | Connect か、GWLB |
| MPLS | 事業者の網と Direct Connect を接続し、MPLS の拠点を AWS へつなぐ |

**Transit Gateway の分離の例:**

| ルートテーブル | 関連付け | 伝播元 | 結果 |
|---|---|---|---|
| `rt-prod` | 本番 VPC | 共有 VPC、DX ゲートウェイ | 本番同士は通らない |
| `rt-dev` | 開発 VPC | 共有 VPC、DX ゲートウェイ | 開発から本番へは通らない |
| `rt-shared` | 共有 VPC、DX ゲートウェイ | 本番 VPC、開発 VPC | どちらへも戻れる |

**既定の関連付けと伝播が有効のままだと**、新しい VPC が全 VPC と通信できてしまいます。

詳細: [VPC ピアリング](../../services/network-connectivity.md#vpc-peering)、[ルートテーブル](../../services/network-connectivity.md#tgw-route-tables)、[ピアリング](../../services/network-connectivity.md#tgw-peering)

### PrivateLink によるアプリの接続 {#t2-2-privatelink}

**提供側:** NLB の裏にサービスを置き、エンドポイントサービスを作ります。接続を許可するプリンシパルを指定します。

**利用側:** インターフェイスエンドポイントを作り、提供者が承認します。

| 確認項目 | 内容 |
|---|---|
| 向き | 利用側から提供側へのみ |
| SG | エンドポイントの SG で、クライアントからの通信を許可 |
| AZ | 両側の AZ が重なること |
| DNS | プライベート DNS、または Regional と zonal の DNS 名 |
| オンプレミスから | DX か VPN で到達できる。名前はインバウンドエンドポイント経由で引く |

詳細: [VPC エンドポイントと PrivateLink](../../services/networking.md#vpc-endpoints)、[エンドポイントポリシー](../../services/networking.md#endpoint-policies)

### Organizations と RAM で接続を広げる {#t2-2-expansion}

**広げ方の例:** ネットワークアカウントの Transit Gateway を組織へ共有します。新しいアカウントは Control Tower で作り、StackSets でアタッチメントと経路を展開します。

Cloud WAN ならタグでセグメントへ自動で割り当てられます。

| | Transit Gateway の共有 | Cloud WAN |
|---|---|---|
| 新しい VPC の接続 | アタッチメントとルート操作 | タグで自動 |
| リージョン間 | ピアリングと静的ルート | 自動のフルメッシュ |

**落とし穴:** Cloud WAN でタグの値がセグメント名と違うと、エラーにならずアタッチメントが宙に浮きます。

詳細: [Cloud WAN](../../services/network-connectivity.md#cloud-wan)、[Control Tower](../../services/governance.md#control-tower)、[AWS Resource Access Manager](../../services/governance.md#ram)

### ホストとサービスの名前解決 {#t2-2-name-resolution}

| 方式 | 向く場面 |
|---|---|
| PHZ | VPC 内の固定の名前 |
| Forward ルール | オンプレミスの名前 |
| AWS Cloud Map | 動的に増減するサービスの発見 |
| VPC ピアリングの DNS オプション | 相手の公開 DNS 名をプライベート IP へ解決 |
| Transit Gateway の `DnsSupport` | アタッチした VPC の間の公開 DNS 名を解決 |

**AWS Cloud Map:** 論理名とリソースを対応付けるサービスディスカバリです。

| 要素 | 内容 |
|---|---|
| 名前空間 | サービスのまとまり。API のみ、VPC 内の DNS、公開 DNS のどれで発見するかを決める |
| サービス | リソースの種類ごとのひな形。DNS レコードの種類やヘルスチェックを定義 |
| サービスインスタンス | `RegisterInstance` で登録するリソース |
| 発見 | `DiscoverInstances` の API か、DNS。ヘルスチェックを指定すると正常なものだけを返す |

**Route 53 との使い分け:** 固定の名前を人が管理するなら Route 53 です。アプリがインスタンスを登録、解除するなら Cloud Map です。

詳細: [プライベートホストゾーン](../../services/network-connectivity.md#private-hosted-zones)、[作成時の設定](../../services/network-connectivity.md#tgw-options)

!!! info "公式の出典"
    Cloud Map は [What Is AWS Cloud Map?](https://docs.aws.amazon.com/cloud-map/latest/dg/what-is-cloud-map.html) によります。

### インフラの自動化 {#t2-2-automation}

マルチアカウントでは StackSets が中心です。組織の OU を対象にすれば、新しいアカウントへも自動で展開できます。

**依存の順序:** Transit Gateway の共有、アタッチメント、承認、ルートの順に進みます。CloudFormation の `DependsOn` や、スタックの分割で順序を守ります。

詳細: [StackSets の運用](../../services/operations.md#stacksets-operations)、[ネストされたスタックと StackSets](../../services/iac.md#nested-stacks-stacksets)

### 認証と認可 {#t2-2-auth}

| 場面 | 仕組み |
|---|---|
| Client VPN の利用者 | Active Directory、相互証明書、SAML |
| Client VPN の宛先の制御 | 認可ルール。**既定では何もなく全部拒否** |
| VPC Lattice | IAM の認証ポリシー |
| AWS の管理操作 | IAM Identity Center（SAML）、Directory Service |
| 別アカウントの管理 | IAM ロール |

**Client VPN の 3 点セット:** ルート、認可ルール、SG がすべて要ります。接続できるのに届かないときは、ルートと認可ルールを確認します。サーバー証明書は認証方式に関係なく ACM に必要です。

詳細: [Client VPN](../../services/network-connectivity.md#client-vpn)、[ID ソース](../../services/identity-directory.md#idc-identity-sources)、[Directory Service](../../services/identity-directory.md#directory-service)

### ネットワーク境界のセキュリティ {#t2-2-security}

| 手段 | 層 | 状態 | 付ける場所 |
|---|---|---|---|
| SG | L3、L4 | ステートフル | ENI |
| NACL | L3、L4 | ステートレス | サブネット |
| Network Firewall | L3〜L7 | 両方 | VPC のエンドポイント |
| エンドポイントポリシー | API | | VPC エンドポイント |

**Network Firewall の実装で間違えやすい点:**

- ファイアウォールのサブネットは専用にします。
- ステートレスの既定は `Forward to stateful` にします。`Pass` にするとステートフルのルールが評価されません。
- 集中型では `HOME_NET` を上書きします。スポークの CIDR が含まれないと、ルールが一致しません。
- `RuleOrder` はポリシーの作成時にしか指定できません。
- Strict でドメインを絞るなら、既定アクションは `Drop established` です。

**境界の例:** 共有 VPC は SG の参照で通信を制御します。ピアリングでも同じリージョンなら相手の SG を指定できます。

詳細: [セキュリティグループと NACL](../../services/networking.md#security-groups-nacls)、[Network Firewall](../../services/network-connectivity.md#network-firewall)、[ステートフルのルール順序](../../services/network-connectivity.md#nfw-rule-order)、[検査の配置](../../services/network-connectivity.md#choosing-inspection)

### 接続のテスト {#t2-2-testing}

| ツール | マルチアカウントでの注意 |
|---|---|
| Reachability Analyzer | 同じ組織なら別のアカウントも可（信頼されたアクセスを有効に） |
| Route Analyzer | Transit Gateway の経路を調べる。同じリージョン内のピアリングには非対応 |
| Network Access Analyzer | 望まない経路がないかを環境全体で調べる |
| `dig`、`nslookup` | 名前解決の確認 |
| `tracepath` | 経路の MTU の確認 |

詳細: [Reachability Analyzer](../../services/network-connectivity.md#reachability-analyzer)、[Network Access Analyzer](../../services/network-connectivity.md#network-access-analyzer)

### 単一 VPC とマルチ VPC の構成 {#t2-2-single-multi-vpc}

**DHCP オプションセット:** VPC 内の機器へ配布する設定です。

| 項目 | 内容 |
|---|---|
| ドメインネームサーバー | 既定は `AmazonProvidedDNS` |
| ドメイン名 | ホスト名の解決に使う |
| NTP サーバー | 既定では Amazon Time Sync を使う |
| NetBIOS | Windows 向け |
| 関連付け | 1 つのセットを複数の VPC に関連付けられる。**VPC に 1 つ** |

**独自の DNS サーバーを指定すると:** PHZ の名前は、そのサーバーが VPC+2 へ転送しない限り引けません。NAT64 用の DNS64 や DNS Firewall も VPC Resolver を通るときだけ効きます。

**設計の順序:** CIDR、サブネットと AZ、ルートテーブル、SG と NACL、エンドポイントの順に決めます。Transit Gateway のアタッチメント用には、AZ ごとに `/28` の専用サブネットを作ります。

詳細: [サブネットとルートテーブル](../../services/networking.md#subnets-route-tables)、[セキュリティグループのルール](../../services/networking.md#security-group-rules)、[アタッチメント](../../services/network-connectivity.md#tgw-attachments)

!!! info "公式の出典"
    DHCP オプションセットは [DHCP option sets in Amazon VPC](https://docs.aws.amazon.com/vpc/latest/userguide/VPC_DHCP_Options.html) によります。

### 第三者製品とのハイブリッド接続 {#t2-2-third-party}

| 既存の製品 | つなぎ方 |
|---|---|
| 第三者の VPN 機器 | Site-to-Site VPN の CGW にする。設定ファイルをダウンロードできる |
| SD-WAN の仮想アプライアンス | Connect で GRE と BGP |
| 第三者のファイアウォール | GWLB、または Firewall Manager の対応製品 |
| ポリシーベースの VPN 機器 | AWS はルートベースのみ。トラフィックセレクターの扱いに注意 |

詳細: [Site-to-Site VPN](../../services/network-connectivity.md#site-to-site-vpn)、[Connect](../../services/network-connectivity.md#tgw-connect)、[Firewall Manager](../../services/threat-detection.md#firewall-manager)

### ハブアンドスポーク {#t2-2-hub-spoke}

| | Transit Gateway | トランジット VPC |
|---|---|---|
| ハブ | マネージドのリージョンルーター | ハブの VPC と EC2 の仮想ルーター |
| スポーク | アタッチメント | スポークの VGW から VPN |
| 帯域 | VPC アタッチメントで AZ あたり最大 100 Gbps | トンネルとインスタンスに依存 |
| 運用 | AWS が管理 | 仮想ルーターの更新と冗長化を自分で |
| 向く場面 | 新規の構成 | 第三者のルーティング機能が必須な既存の構成 |

トランジット VPC は Transit Gateway より前からある手法です。古い問題文に出ても、新規の構成では Transit Gateway を優先します。

詳細: [Transit Gateway](../../services/network-connectivity.md#transit-gateway)、[Global Networks](../../services/network-connectivity.md#route-analyzer)

### 名前解決でハイブリッド接続を成立させる {#t2-2-dns-hybrid}

**マルチアカウントの DNS の実装順序:**

1. 共有サービス VPC に Resolver のインバウンドとアウトバウンドを置きます。
2. オンプレミス向けの Forward ルールを作り、RAM で組織へ共有します。
3. 各アカウントでルールを自分の VPC に関連付けます。
4. 各 VPC の PHZ を共有サービス VPC に関連付けます。
5. オンプレミスの DNS で AWS の名前を条件付き転送します。

詳細は [タスク 2.3](#task-2-3) で扱います。

詳細: [ハイブリッド DNS](../../services/network-connectivity.md#hybrid-dns)

### 監視とログの設定 {#t2-2-monitoring}

| 目的 | 設定 |
|---|---|
| 全アカウントのフローログを集める | ログ用アカウントの S3 へ配信する |
| アタッチメントの間の通信 | Transit Gateway フローログ |
| トポロジーとルートの変更 | Global Networks for Transit Gateways |
| Network Firewall の判定 | Alert、Flow ログ。**設定しないとアラートは見えない** |

詳細: [フローログの分析](../../services/network-connectivity.md#flow-log-analysis)、[Network Firewall のルーティングとログ](../../services/network-connectivity.md#nfw-routing)

## タスク 2.3: 複雑なハイブリッド、マルチアカウント DNS を実装する {#task-2-3}

### ホストゾーンの選択と条件付き転送 {#t2-3-zones}

| 要件 | 選択 |
|---|---|
| インターネットから解決する | 公開ホストゾーン |
| VPC 内だけで解決する | PHZ |
| 内外で別の答え | 同名の両方（スプリットビュー） |
| オンプレミスの名前 | Forward ルール |

**Resolver ルールは PHZ より優先されます。** `example.com` の PHZ と同名の Forward ルールが同じ VPC にあると、オンプレミスへ転送されます。

詳細: [プライベートホストゾーン](../../services/network-connectivity.md#private-hosted-zones)、[転送ルール](../../services/network-connectivity.md#resolver-rules)

### DNS によるトラフィック管理の実装 {#t2-3-traffic}

| ポリシー | 設定 | 誤りやすい点 |
|---|---|---|
| 加重 | `Weight`、`SetIdentifier` | 比率は重み / 合計。0 だけなら均等 |
| レイテンシー | `Region` | 距離ではなく測定値 |
| 位置情報 | 大陸、国 | 既定のレコードが必要 |
| 地理的近接性 | `Bias`（-99〜99） | 正で範囲が広がる |
| フェイルオーバー | `PRIMARY`、`SECONDARY` | プライマリにヘルスチェック |

PHZ でも主要なルーティングポリシーを使えます。ヘルスチェックは CloudWatch アラーム型です。

**組み合わせ:** レイテンシーのエイリアスの先に加重を置くと、リージョンを選んでから版を分けられます。Traffic Flow なら、この木をポリシーとして管理できます。

詳細: [ルーティングポリシーの設定](../../services/networking.md#routing-settings)、[Traffic Flow](domain1.md#t1-2-features)

### DNS の委任と転送 {#t2-3-delegation}

| | 委任 | 転送 |
|---|---|---|
| 仕組み | 親のゾーンの NS レコードで子を指す | リゾルバーが別のリゾルバーへ問い合わせを渡す |
| 誰の設定か | 権威 DNS | リゾルバー |
| AWS の例 | サブドメインのゾーンの NS を親に登録 | Forward ルール、条件付き転送 |

**親が他社の DNS のまま Route 53 にサブドメインを作る手順:**

1. サブドメインのホストゾーンを作ります。
2. レコードを追加します。
3. 親の DNS に、ゾーンの 4 つの NS レコードを登録します。

変更は通常 60 秒以内に Route 53 のネームサーバーへ伝わります。

VPC Resolver には Delegate ルールもあり、サブドメインの権限をオンプレミスへ委任できます。

詳細: [転送ルール](../../services/network-connectivity.md#resolver-rules)

!!! info "公式の出典"
    手順は [Creating a subdomain](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/CreatingNewSubdomain.html) によります。

### レコードの種類と設定 {#t2-3-records}

| レコード | 用途 | 注意 |
|---|---|---|
| `A`、`AAAA` | IPv4、IPv6 | デュアルスタックには両方 |
| `CNAME` | 別名 | ゾーンの頂点に作れない |
| エイリアス | AWS リソースを指す | 頂点に作れる。AWS リソース向けの TTL は指定不可 |
| `TXT` | 所有の確認、SPF など | |
| `PTR` | IP から名前を引く（逆引き） | `in-addr.arpa`、`ip6.arpa` のゾーン |
| `NS` | 委任 | |
| `MX` | メール | |

**逆引きが要るとき:** オンプレミスのメールやログの解析で IP から名前を引きます。VPC の中で PHZ に `in-addr.arpa` のゾーンを作る方法があります。

詳細: [レコード](../../services/networking.md#route53-records)、[TTL とエイリアス](../../services/networking.md#route53-ttl)

### DNSSEC {#t2-3-dnssec}

DNSSEC には**署名**と**検証**の 2 つがあり、設定する場所が違います。

| | 署名 | 検証 |
|---|---|---|
| 目的 | 自分のゾーンの応答に署名 | 受け取った応答の署名を確かめる |
| 場所 | 公開ホストゾーン | VPC（VPC Resolver の設定） |
| 対象外 | **PHZ は署名できない** | PHZ、転送先が解決する名前（転送先で検証する） |

**署名の鍵:**

| 鍵 | 管理者 | 内容 |
|---|---|---|
| KSK | お客様 | `us-east-1` の非対称 KMS キー（`ECC_NIST_P256`）が元。ゾーンあたり 2 つまで |
| ZSK | Route 53 | 自動で管理 |

**署名を有効にする手順:**

1. 準備します。ゾーンの可用性を監視し、最大 TTL を 1 時間に、SOA の TTL も下げます。
2. KSK を作り、署名を有効にします。
3. 親ゾーンに **DS レコード**を登録して、信頼の連鎖を作ります。

**落とし穴:**

| 状況 | 結果 |
|---|---|
| 親の DNS が DS に対応しない | 子のゾーンが解決できなくなる |
| KMS キーを削除、権限を変更 | KSK が `ACTION_NEEDED`。放置するとゾーンの障害 |
| マルチベンダーの構成 | 非対応 |
| 1 週間を超える TTL | 1 週間に制限される |
| 検証を有効にする | 署名に問題のある公開名が引けなくなることがある。反映に数分 |

**監視:** `DNSSECInternalFailure` と `DNSSECKeySigningKeysNeedingAction` に CloudWatch アラームを設定します。

**VPC Resolver の制限:** 検証はしますが、DO ビットと CD ビットを無視し、DNSSEC レコードも AD ビットも返しません。自分で検証したいなら、自分で再帰解決をします。

詳細: [DNSSEC の項目](../../services/network-connectivity.md#private-hosted-zones)

!!! info "公式の出典"
    [Configuring DNSSEC signing](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/dns-configuring-dnssec.html)、[Enabling DNSSEC signing](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/dns-configuring-dnssec-enable-signing.html)、[Enabling DNSSEC validation](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/resolver-dnssec-validation.html)、[Troubleshooting](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/dns-configuring-dnssec-troubleshoot.html) によります。

### DNS サービスの共有と集中型、分散型の構成 {#t2-3-sharing}

| 方法 | 共有するもの |
|---|---|
| RAM | Resolver ルール、Route 53 Profiles |
| 関連付けの許可 | PHZ と別のアカウントの VPC |
| Route 53 Profiles | PHZ、ルール、DNS Firewall のルールグループをまとめて |

| | 集中型 | 分散型 |
|---|---|---|
| エンドポイント | 共有サービス VPC に集約 | VPC ごと |
| 費用 | 少ない | ENI の数だけ増える |
| 容量 | 集中点の QPS に注意 | 分散する |
| 向く場面 | 多数のアカウント | 分離の要件が強い |

**別のアカウントの VPC に PHZ を関連付ける手順:** コンソールではできません。ゾーンの所有者が `create-vpc-association-authorization` を実行し、VPC の所有者が `associate-vpc-with-hosted-zone` を実行します。終わったら許可を消します。

**上限:** PHZ の関連付けはゾーンあたり VPC 300 個です。それ以上なら Profiles です。

詳細: [プライベートホストゾーン](../../services/network-connectivity.md#private-hosted-zones)、[ハイブリッド DNS](../../services/network-connectivity.md#hybrid-dns)

### インバウンドとアウトバウンドの実装 {#t2-3-endpoints}

| 要件 | インバウンド | アウトバウンド |
|---|---|---|
| SG | 受信 TCP、UDP の 53 | 送信 TCP、UDP の 53 |
| IP | API では最低 2 個、2 つの AZ を推奨 | 同じ |
| VPC | 自分が所有する VPC。専有テナンシーは不可 | 同じ |
| 追加の設定 | オンプレミスの条件付き転送 | ルールと VPC の関連付け |
| 経路 | DX か VPN | DX か VPN、または NAT ゲートウェイ |

**症状:**

| 症状 | 確認すること |
|---|---|
| オンプレミスから PHZ が引けない | PHZ とエンドポイントの VPC の関連付け、SG の受信 53 |
| VPC からオンプレミスが引けない | ルールと VPC の関連付け、SG の送信 53、ターゲットへの経路 |
| 特定のサブドメインだけ NXDOMAIN | より具体的な PHZ があり、レコードがない |

詳細: [エンドポイント](../../services/network-connectivity.md#resolver-endpoints)

### DNS の監視とログの設定 {#t2-3-logging}

| 設定 | 手順 |
|---|---|
| 公開クエリログ | `us-east-1` の CloudWatch Logs のロググループを指定。リソースポリシーで Route 53 に書き込みを許可 |
| Resolver クエリログ | クエリログ設定を作り、VPC に関連付ける。送信先は CloudWatch Logs、S3、Firehose |
| ヘルスチェックの監視 | `HealthCheckStatus` にアラーム |
| DNS Firewall | ログと CloudWatch メトリクスで確認 |

**分析:** Logs Insights で、応答コード `NXDOMAIN` や `SERVFAIL` の多い名前を探します。

詳細: [DNS のログと監視](domain1.md#t1-2-logging)、[DNS Firewall](../../services/network-connectivity.md#dns-firewall)、[Logs Insights](../../services/observability.md#logs-insights)

## タスク 2.4: ネットワークの自動化と構成 {#task-2-4}

### IaC の道具と繰り返せる構成 {#t2-4-iac}

| 道具 | 向く場面 |
|---|---|
| CloudFormation | 宣言的なテンプレート。StackSets で多数のアカウントへ |
| CDK | ループや抽象化で、多数のサブネットや VPC を生成 |
| CLI | スクリプトや単発の操作 |
| SDK、API | Lambda や独自の自動化ツールから呼ぶ |

**繰り返せる構成の作り方:**

- 共通のネットワークをテンプレートにし、`Parameters` と `Mappings` で環境差を吸収します。
- `Outputs` と `Fn::ImportValue`、または Parameter Store で ID を渡します。
- IPAM のプールから CIDR を割り当て、テンプレートに値を書きません。
- 変更セットで置き換えの有無を確認します。ネットワークの置き換えは停止につながります。
- ドリフト検出で手動変更を見つけます。

詳細: [CloudFormation テンプレート](../../services/iac.md#cloudformation-template)、[CDK](../../services/iac.md#cdk)、[変更セット](../../services/iac.md#change-sets)、[ドリフト検出](../../services/iac.md#drift)、[AWS CLI](../../services/iac.md#aws-cli)

### イベント駆動の自動化 {#t2-4-event}

| きっかけ | 仕組み | 処理の例 |
|---|---|---|
| SG の変更 | EventBridge（CloudTrail 経由） | Lambda で許可しない規則を削除 |
| Config の非準拠 | Config ルールと修復 | Automation で修正 |
| 新しいアカウント | Control Tower のイベントや StackSets | Transit Gateway へのアタッチ |
| VPN のトンネルの断 | CloudWatch アラームと SNS | 通知、切り替え |

**注意:** 修復が別のイベントを発生させて、ループにならないようにします。失敗時の DLQ や再試行も決めておきます。

詳細: [EventBridge による修復パターン](../../services/operations.md#eventbridge-remediation)、[ルールとイベントパターン](../../services/messaging.md#eventbridge-rules)、[修復](../../services/governance.md#config-remediation)、[ターゲットの再試行と DLQ](../../services/messaging.md#target-retry-dlq)

### IaC でハードコードする問題 {#t2-4-hardcoding}

| ハードコードするもの | 問題 | 代わりの手段 |
|---|---|---|
| AZ 名（`ap-northeast-1a`） | 別のリージョンやアカウントで使えない | `Fn::GetAZs`、パラメータ |
| AMI ID | リージョンで違い、古くなる | Parameter Store の公開パラメータ |
| VPC、サブネットの ID | 環境ごとに違う | パラメータ、エクスポート |
| CIDR | 重複を生む | IPAM のプール |
| リソース名 | 再作成や別リージョンで衝突 | 名前を指定しない |
| アカウント ID、リージョン | 移植できない | `AWS::AccountId`、`AWS::Region` |
| シークレット（BGP の MD5 キー、PSK） | テンプレートに残る | Secrets Manager の動的参照 |

詳細: [パラメータ](../../services/iac.md#parameters)、[擬似パラメータ](../../services/iac.md#pseudo-parameters)、[マッピングと条件](../../services/iac.md#mappings-conditions)、[IPAM](../../services/network-connectivity.md#ipam)

### ハイブリッドの自動化と IaC の統合 {#t2-4-hybrid}

オンプレミスの機器の設定は、CloudFormation だけでは完結しません。

| 方法 | 内容 |
|---|---|
| カスタムリソース | CloudFormation から Lambda を呼び、機器の API や外部の仕組みを操作する |
| Systems Manager Automation、Run Command | ハイブリッドノードの設定 |
| VPN の設定のダウンロード | CGW 用の設定を取得し、構成管理ツールへ渡す |
| EventBridge | VPC の作成をきっかけにオンプレミスの経路を更新 |

詳細: [カスタムリソース](../../services/iac.md#custom-resources)、[オンプレミスと他クラウド](../../services/operations.md#hybrid-nodes)、[Run Command](../../services/operations.md#run-command)

### リスクを除き、効率と最低コストを両立する {#t2-4-risk-cost}

| 目的 | 手段 |
|---|---|
| 変更の失敗を減らす | 変更セット、スタックポリシーで重要リソースを保護、ロールバックトリガー |
| 誤削除を防ぐ | `DeletionPolicy`、終了保護 |
| 接続の確認を自動化 | デプロイ後に Reachability Analyzer を実行 |
| 使わない資源の課金を防ぐ | 未使用の Elastic IP、NAT、エンドポイント、Traffic Mirroring のセッションを消す |
| 費用を比較する | Cost Explorer で NAT とデータ転送を確認 |

詳細: [スタックポリシー](../../services/iac.md#stack-policy)、[DeletionPolicy](../../services/iac.md#deletion-policy)、[ロールバックトリガー](../../services/iac.md#rollback-triggers)、[Cost Explorer](../../services/cost-management.md#cost-explorer)、[データ転送の費用](../../services/cost-management.md#data-transfer)

### IaC でネットワーク資源を最適化する {#t2-4-optimize}

| 最適化 | IaC での実現 |
|---|---|
| S3 への NAT の費用を減らす | ゲートウェイエンドポイントを全 VPC のテンプレートへ |
| NAT の数を調整 | 環境で条件分岐。本番は AZ ごと、開発は 1 つ |
| インターフェイスエンドポイントの集約 | 共有 VPC に置き、PHZ で共有 |
| Transit Gateway の経路の集約 | プレフィックスリストをテンプレートで管理 |

**NAT の例:** `Conditions` で `IsProd` を判定し、本番だけ AZ ごとに NAT ゲートウェイを作ります。リージョン型 NAT ゲートウェイなら 1 つの ID で済みます。

詳細: [マッピングと条件](../../services/iac.md#mappings-conditions)、[NAT ゲートウェイ](../../services/network-connectivity.md#nat-gateway)、[VPC エンドポイント](../../services/networking.md#vpc-endpoints)

## 確認問題 {#self-check}

??? question "問1: 新しい DX 専用接続で、接続の状態は up なのにプライベート VIF が down のままです。最初に確認するものは何ですか。"
    VLAN タグと ARP など、レイヤー 2 の設定です。接続が up なら物理は通っています。ルーターの VLAN が VIF と一致しないと VIF は down になります。BGP の ASN や MD5 は、その次の段階で確認します。

??? question "問2: Transit Gateway のスポーク VPC から検査 VPC の Network Firewall を通す構成で、同じ AZ の VPC 間は通信できますが、AZ をまたぐ通信が一部失敗します。どう直しますか。"
    検査 VPC のアタッチメントでアプライアンスモードを有効にします。既定では戻りが別の AZ に入るので、ステートフルなエンジンが行きの通信を知らずに破棄します。設定する場所は検査 VPC の VPC アタッチメントです。ネットワーク機能アタッチメントを使うなら自動で有効です。

??? question "問3: 公開ホストゾーンで DNSSEC 署名を有効にしました。その後、KMS キーのポリシーを変更したところ、KSK の状態が Action needed になりました。放置するとどうなりますか。監視はどう設定しますか。"
    Route 53 が KMS キーへアクセスできず、やがて検証するリゾルバーの利用者からゾーンが解決できなくなります。キーを有効にして権限を戻し、KSK を再度有効にします。`DNSSECKeySigningKeysNeedingAction` と `DNSSECInternalFailure` に CloudWatch アラームを設定します。

??? question "問4: 組織の全 VPC からオンプレミスの `corp.example.com` を引けるようにしたいです。VPC は 200 個あり、DNS の ENI の費用を抑えたいです。どう構成しますか。"
    共有サービス VPC にアウトバウンドエンドポイントを置き、Forward ルールを RAM で組織へ共有して、各 VPC に関連付けます。VPC ごとにエンドポイントを作る必要はありません。多数の VPC へまとめて適用するなら Route 53 Profiles も候補です。容量は集約点の QPS で見積もります。

??? question "問5: CloudFormation のテンプレートに AZ 名、AMI ID、VPC の CIDR を直接書いています。別のリージョンへ展開すると失敗し、別の VPC とも CIDR が重複しました。どう直しますか。"
    AZ は `Fn::GetAZs` かパラメータ、AMI は Parameter Store の公開パラメータ、CIDR は IPAM のプールから割り当てます。アカウントやリージョンは擬似パラメータで参照します。こうすると同じテンプレートをどこへでも展開できます。

??? question "問6: オンプレミスの DNS から `10.0.0.2`（VPC+2）へ転送していますが、解決が不安定です。どう変えますか。SG はどう設定しますか。"
    Route 53 のインバウンドエンドポイントを 2 つの AZ に作り、条件付き転送の先をエンドポイントの IP に変えます。オンプレミスから VPC+2 への転送は公式に非対応です。エンドポイントの SG は TCP と UDP の 53 の受信を、オンプレミスの DNS サーバーから許可します。PHZ をそのエンドポイントの VPC に関連付けることも確認します。

# 分野3: ネットワークのセキュリティ

通信の制御、ハイブリッド接続の暗号化、アプリへのアクセス、分割、不要な経路の発見を問います。似た統制の使い分けが中心です。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [3.3.1](../../domain3.md#skill-3-3-1) | 通信の許可と拒否の設計 |
| [3.3.2](../../domain3.md#skill-3-3-2) | ハイブリッドとマルチクラウドの安全な接続 |
| [3.3.3](../../domain3.md#skill-3-3-3) | ハイブリッド環境の通信要件 |
| [3.3.4](../../domain3.md#skill-3-3-4) | ネットワークの分割 |
| [3.3.5](../../domain3.md#skill-3-3-5) | 不要なネットワークアクセスの特定 |

## 学習の順番 {#study-order}

1. [SG と NACL](../../../../services/networking.md#security-groups-nacls)と [NACL のルール](../../../../services/networking.md#nacl-rules): ステートフルとステートレスの違いを確認します。
2. [Network Firewall の構成](../../../../services/threat-detection.md#nfw-architecture)と[ルールの評価](../../../../services/threat-detection.md#nfw-rules): 経路、既定アクション、`HOME_NET`、順序を押さえます。
3. [DNS Firewall](../../../../services/network-connectivity.md#dns-firewall): Network Firewall との違いと、障害時の動作を確認します。
4. [MACsec](../../../../services/network-connectivity.md#dx-macsec)と[プライベート IP VPN](../../../../services/network-connectivity.md#vpn-private-ip): Direct Connect の暗号化の方法を比べます。
5. [トンネルオプション](../../../../services/network-connectivity.md#vpn-tunnel-options): トンネルの帯域と接続先を覚えます。
6. [Verified Access](../../../../services/identity-directory.md#verified-access)と [Client VPN](../../../../services/network-connectivity.md#client-vpn): アプリ単位かネットワーク単位かで選びます。
7. [Transit Gateway のルートテーブル](../../../../services/network-connectivity.md#tgw-route-tables)と[アプライアンスモード](../../../../services/network-connectivity.md#tgw-appliance-mode): 分割と集中検査の設定を確認します。
8. [検査の配置](../../../../services/network-connectivity.md#choosing-inspection)と [GWLB による検査](../../../../services/network-connectivity.md#gwlb-inspection): Network Firewall か他社製かを判断します。
9. [Network Access Analyzer](../../../../services/network-connectivity.md#network-access-analyzer)と[ネットワーク到達性](../../../../services/threat-detection.md#inspector-network): 不要な経路を見つけるツールを比べます。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| MACsec の対象 | 10、100、400 Gbps の専用接続 | 1 Gbps とホスト接続は対象外 |
| MACsec の既定モード | `should_encrypt` | 確立に失敗すると暗号化なしで続く |
| CKN/CAK の保持 | 接続あたり 3 組 | ローテーションは手動 |
| VPN のトンネル | 標準 1.25 Gbps。Large Bandwidth は 5 Gbps | 後者は Transit Gateway か Cloud WAN |
| VPN Concentrator のトンネル | 最大 100 Mbps | 小規模な拠点向け |
| Inspector のネットワーク到達性 | 12 時間ごと | EC2 のみ |
| エフェメラルポート | 1024-65535 を許可すると多くの場合に対応 | NACL の戻り通信 |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| ドメインの許可リストで外向き通信を絞り、IP 直接も止める | Network Firewall のドメインリスト |
| DNS の問い合わせだけを止めたい | DNS Firewall |
| ステートフルのルールとログが効かない | ステートレスの既定アクションが `pass` |
| 集中型で `HOME_NET` のルールが一致しない | ポリシーの変数で範囲を広げる |
| 厳密な順序に変えたい | 新しいポリシーを作る。`RuleOrder` は作成時のみ |
| DNS Firewall の障害でも名前解決を続ける | fail open を有効にする |
| DX で公開 IP なしに IP 層で暗号化 | トランジット VIF の上のプライベート IP VPN |
| 暗号化なしを認めない DX | `must_encrypt`。確立を確認してから変更 |
| アプリ単位でリクエストごとに判定 | Verified Access |
| Client VPN で届かない | ルートと認可ルールの両方 |
| 行きと戻りが別の AZ で破棄される | アプライアンスモード |
| 他社のファイアウォールをそのまま使う | GWLB |
| 自分の要件に反する経路を探す | Network Access Analyzer |
| スコープなしで開いた経路を継続的に見る | Inspector のネットワーク到達性 |

## 引っかかりやすい点 {#traps}

- セキュリティグループのルールを変えても、追跡中の接続はすぐには切れません。
- DNS Firewall は VPC Resolver を通る問い合わせだけを見ます。IP の直接指定は止まりません。
- MACsec はレイヤー 2 の区間の暗号化で、エンドツーエンドではありません。
- Verified Access はポリシーがなければ全拒否です。Identity Center を使うなら組織インスタンスが必要です。
- Client VPN の認可ルールは許可だけで、制限には使えません。
- Network Access Analyzer の結果は、`MatchPaths` に一致し `ExcludePaths` に一致しない経路です。
- Firewall Manager の監査ポリシーは、自動修復を無効にして始めます。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [network-security 問1](../../exercises/network-security.md#q1) | 3.3.1 | プライベートサブネットの EC2 が、NAT ゲートウェイ経由で外部へ HTTPS の通信をしていま… |
| [network-security 問2](../../exercises/network-security.md#q2) | 3.3.1 | Network Firewall を導入し、ステートフルルールグループで不審な宛先を DROP にし… |
| [network-security 問3](../../exercises/network-security.md#q3) | 3.3.1 | 中央の検査 VPC（10.100.0.0/16）に Network Firewall を置き、Tra… |
| [network-security 問4](../../exercises/network-security.md#q4) | 3.3.1 | 既定のアクション順序で運用しているファイアウォールポリシーがあります。チームは、pass が他のルー… |
| [network-security 問5](../../exercises/network-security.md#q5) | 3.3.1 | 重要な決済システムの VPC に DNS Firewall を導入します。可用性の要件が厳しく、DN… |
| [network-security 問6](../../exercises/network-security.md#q6) | 3.3.1 | パブリックサブネットの NACL に、インバウンドで 443 番の許可と、アウトバウンドで 443 … |
| [network-security 問7](../../exercises/network-security.md#q7) | 3.3.2 | Direct Connect のトランジット VIF で Transit Gateway に接続して… |
| [network-security 問8](../../exercises/network-security.md#q8) | 3.3.2 | 100 Gbps の Direct Connect 専用接続に MACsec を設定しました。監査は… |
| [network-security 問9](../../exercises/network-security.md#q9) | 3.3.2 | ある拠点は 1 Gbps のホスト接続で Direct Connect を使っています。通信を暗号化… |
| [network-security 問10](../../exercises/network-security.md#q10) | 3.3.2 | 他社のクラウドと AWS を IPsec でつなぎます。1 トンネルで 3 Gbps を出すことが要… |
| [network-security 問11](../../exercises/network-security.md#q11) | 3.3.3 | 従業員は Client VPN で VPC に入り、社内の Web アプリを使っています。監査で、接… |
| [network-security 問12](../../exercises/network-security.md#q12) | 3.3.3 | AWS Verified Access のインスタンス、信頼プロバイダー、グループ、エンドポイントを… |
| [network-security 問13](../../exercises/network-security.md#q13) | 3.3.3 | 運用者が AWS Verified Access で社内の管理画面に接続します。ID プロバイダーは… |
| [network-security 問14](../../exercises/network-security.md#q14) | 3.3.3 | Client VPN で VPC A のサブネットに関連付けたエンドポイントがあります。利用者は接続… |
| [network-security 問15](../../exercises/network-security.md#q15) | 3.3.4 | 中央の検査 VPC に他社のステートフルなアプライアンスを置き、Transit Gateway で … |
| [network-security 問16](../../exercises/network-security.md#q16) | 3.3.4 | Transit Gateway に本番の VPC 群、開発の VPC 群、共有サービスの VPC が… |
| [network-security 問17](../../exercises/network-security.md#q17) | 3.3.4 | データベースの階層を分離サブネットに置きます。インターネットへの経路は作りません。この階層のバッチは… |
| [network-security 問18](../../exercises/network-security.md#q18) | 3.3.4 | 東西の通信を検査します。既存の他社のファイアウォールのルールと運用を維持し、その製品を AWS でそ… |
| [network-security 問19](../../exercises/network-security.md#q19) | 3.3.4 | 3 層の Web アプリの東西の通信を絞ります。Web 層と AP 層、AP 層と DB 層のサブネ… |
| [network-security 問20](../../exercises/network-security.md#q20) | 3.3.5 | 監査で、次の要件の実証を求められました。本番の VPC と開発の VPC の間にネットワークの経路が… |
| [network-security 問21](../../exercises/network-security.md#q21) | 3.3.5 | Network Access Analyzer のスコープを作ります。「インターネットゲートウェイか… |
| [network-security 問22](../../exercises/network-security.md#q22) | 3.3.5 | セキュリティチームは、VPC の端から EC2 のポートに届く経路を、スコープを作らずに継続的に見つ… |
| [network-security 問23](../../exercises/network-security.md#q23) | 3.3.5 | 組織の全アカウントで、使われていないセキュリティグループと冗長なセキュリティグループを減らします。自… |

<!-- questions:end -->

# 分野4: ネットワークのセキュリティ

受信、送信、VPC 間の保護と、要件を満たす構成を問います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [受信](../../domain4.md#t4-1-inbound) | 受信の保護（WAF、Shield、Network Firewall） |
| [送信](../../domain4.md#t4-1-outbound) | 送信の保護（Network Firewall、プロキシ、GWLB） |
| [VPC 間](../../domain4.md#t4-1-inter-vpc) | VPC 間の保護（SG、NACL、エンドポイントポリシー） |
| [ネットワーク構成](../../domain4.md#t4-1-architecture) | 要件を満たすネットワーク構成、要件を満たす構成の実装（信頼できないネットワーク、境界 VPC、3 層） |
| [通信を守る仕組み](../../domain4.md#t4-1-flows) | アプリの通信を守る仕組み |
| [脅威モデル](../../domain4.md#t4-1-threat-models) | アーキテクチャごとの脅威モデル、一般的な脅威、脅威モデルの作成と緩和策の特定 |

## 学習の順番 {#study-order}

1. [Shield Advanced](../../../../services/threat-detection.md#shield-advanced): 保護の指定と支援を確認します。
2. [似た機能との比較](../../../../services/certificates.md#waf-comparison): 似た機能との比較を押さえます。
3. [Network Firewall](../../../../services/network-connectivity.md#network-firewall): 構成を確認します。
4. [DNS Firewall](../../../../services/network-connectivity.md#dns-firewall): 限界を理解します。
5. [エンドポイントポリシー](../../../../services/networking.md#endpoint-policies): 権限の上限を覚えます。
6. [検査の配置](../../../../services/network-connectivity.md#choosing-inspection): 検査の配置を確認します。
7. [Verified Access](../../../../services/identity-directory.md#verified-access): 端末からの接続を確認します。

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| SQL インジェクションとレート制限 | AWS WAF |
| NLB の大きな DDoS と費用の保護 | Shield Advanced で Elastic IP を保護 |
| ドメインと IP の両方で制限 | Network Firewall の Strict |
| ドメインの解決を止める | DNS Firewall |
| インターネットの受信を一括で止める | VPC Block Public Access |

## 引っかかりやすい点 {#traps}

- DNS Firewall は IP 直接の通信を止めません。
- エンドポイントポリシーは権限を与えません。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [network-security 問7](../../exercises/network-security.md#q7) | 受信 | 非 HTTP の公開サービスを NLB で提供しています。大規模な DDoS の費用を保護し、攻撃時… |
| [network-security 問8](../../exercises/network-security.md#q8) | 受信 | ALB の Web アプリで、SQL インジェクションと特定の IP の過剰なリクエストを止めます。… |
| [network-security 問9](../../exercises/network-security.md#q9) | 受信 | Shield Advanced を契約して CloudFront と ALB を保護します。誤検知を… |
| [network-security 問10](../../exercises/network-security.md#q10) | 送信 | プライベートサブネットの EC2 から、許可したドメインだけに HTTPS で出します。IP 直接の… |
| [network-security 問11](../../exercises/network-security.md#q11) | 送信 | EC2 のマルウェアが、悪意のあるドメインを VPC Resolver で解決することを止めます。D… |
| [network-security 問12](../../exercises/network-security.md#q12) | 送信 | スポーク VPC からインターネットへの通信を集中して検査します。NAT の変換の前に元の IP で… |
| [network-security 問13](../../exercises/network-security.md#q13) | VPC 間 | 別のアカウントのバケットへの持ち出しを防ぐため、VPC エンドポイントのポリシーで S3 の宛先を絞… |
| [network-security 問14](../../exercises/network-security.md#q14) | VPC 間 | Transit Gateway で本番と開発を分離します。誤設定に強い設計にします。アタッチメント用… |
| [network-security 問15](../../exercises/network-security.md#q15) | VPC 間 | 組織全体で VPC 間の SG と NACL の基準を強制します。新しいアカウントにも適用し、違反は… |
| [network-security 問16](../../exercises/network-security.md#q16) | ネットワーク構成 | 規制データの VPC からインターネットへの経路を一切なくします。AWS サービスへはプライベートで… |
| [network-security 問17](../../exercises/network-security.md#q17) | ネットワーク構成 | 複数のパートナーから VPN で接続を受け、検査してから内部へ通します。パートナーの CIDR は信… |
| [network-security 問18](../../exercises/network-security.md#q18) | ネットワーク構成 | アカウントのリージョン単位で、インターネットからの受信を一括で止めます。NAT の外向きは残し、特定… |
| [network-security 問19](../../exercises/network-security.md#q19) | 通信を守る仕組み | 別の VPC のサービスへの通信を、呼び出す側の IAM ロールで制御します。CIDR は重複してお… |
| [network-security 問20](../../exercises/network-security.md#q20) | 通信を守る仕組み | 社員の端末から社内の Web アプリへ、VPN なしで接続します。ID とデバイスの状態を評価して、… |
| [network-security 問21](../../exercises/network-security.md#q21) | 通信を守る仕組み | 3 層のアプリで、Web から App へ、App から DB へのみ通します。Auto Scali… |
| [network-security 問22](../../exercises/network-security.md#q22) | 脅威モデル | 公開の非 HTTP サービスと、VPC エンドポイント経由の S3 の両方について脅威モデルを作って… |
| [network-security 問23](../../exercises/network-security.md#q23) | 脅威モデル | 内部の多層のシステムで、1 台のホストが侵害された場合の被害の拡大を抑えます。外部への通信は既に検査… |
| [network-security 問24](../../exercises/network-security.md#q24) | 脅威モデル | 新しいハイブリッド構成の脅威モデルを作ります。チームはまず対策の製品を決めようとしています。手順とし… |

<!-- questions:end -->

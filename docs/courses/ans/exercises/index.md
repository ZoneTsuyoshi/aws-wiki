# 問題集

ANS-C01 を基準にした、話題ごとの本番形式の問題です。すべてオリジナルの問題で、実際の試験問題ではありません。答えは問題の下を開くと確認でき、選択肢ごとの解説と解説ページへのリンクがあります。

1. まず[学習の順番](../index.md#study-path)で範囲を確認します。
2. 分野のページとサービスの解説を読み、問題を解きます。
3. 間違えた問題は、解説のリンク先に戻って確認します。

分野をまたぐ話題は、主な分野に載せています。分野ごとの問題の一覧は、[分野1](../study/domain1/index.md)、[分野2](../study/domain2/index.md)、[分野3](../study/domain3/index.md)、[分野4](../study/domain4/index.md)の学習ページで確認できます。

!!! warning "この試験は 2026年12月31日で終了します"
    受験の予定は[コースの最初のページ](../index.md)で確認してください。

## 分野1: ネットワーク設計 {#domain1}

| 問題集 | 主な内容 |
|---|---|
| [CloudFront と配信設計](cloudfront.md) | キャッシュ、オリジンの保護、統合、配信方式の選択、帯域 |
| [Global Accelerator と分散](global-accelerator.md) | 固定 IP、ダイヤル、重み、分散のパターン |
| [ロードバランサー](elb.md) | ALB、NLB、GWLB の選択、設定、ターゲット、TLS |
| [ルーティングと BGP](routing-bgp.md) | ルートの優先順位、BGP 属性、経路の最適化 |
| [Direct Connect](direct-connect.md) | 物理接続、LAG、冗長構成、VIF、運用 |
| [マルチ VPC とマルチアカウント](multi-account.md) | 接続パターン、VPC 共有、IP の重複、RAM |

## 分野2: ネットワークの実装 {#domain2}

| 問題集 | 主な内容 |
|---|---|
| [Route 53 のゾーンとレコード](route53-zones.md) | TTL、ドメイン登録、PHZ、委任、レコード、DNSSEC |
| [Route 53 のルーティングと高可用性](route53-routing.md) | ポリシー、ヘルスチェック、Traffic Flow、ARC |
| [VPC Resolver とハイブリッド DNS](resolver.md) | エンドポイント、ルール、Profiles、Cloud Map、クエリログ |
| [VPN とカプセル化](vpn.md) | トンネル、IPsec、DX の上の VPN、Client VPN |
| [Transit Gateway と SD-WAN](transit-gateway.md) | Connect、ハブアンドスポーク、上限、マルチキャスト |
| [VPC の構成とエンドポイント](vpc-endpoints.md) | PrivateLink、VPC のサービス、DHCP、AWS サービスへのアクセス |
| [ネットワークの自動化](automation.md) | IaC、StackSets、イベント駆動、ハードコード |

## 分野3: ネットワークの管理と運用 {#domain3}

| 問題集 | 主な内容 |
|---|---|
| [MTU と性能の最適化](performance.md) | MTU、ジャンボフレーム、スループット、インターフェイス、サブネット、費用 |
| [到達性の検証とトポロジー](reachability.md) | Reachability Analyzer、Route Analyzer、Network Manager、検証の自動化 |
| [CloudWatch とログの要件](cloudwatch.md) | メトリクス、アラーム、アクセスログ、監視の設定 |

## 分野4: セキュリティ、コンプライアンス、ガバナンス {#domain4}

| 問題集 | 主な内容 |
|---|---|
| [ネットワークのセキュリティ](network-security.md) | WAF、Shield、Network Firewall、DNS Firewall、構成、脅威モデル |
| [フローログと Traffic Mirroring](flow-logs.md) | フィールド、ログの配信、相関分析、パケットの分析 |
| [監査と通知の自動化](security-operations.md) | テスト、通知、監視サービスの区別、複数アカウントの監査 |
| [暗号化と証明書](encryption.md) | MACsec、IPsec、TLS、ACM、Private CA、責任共有 |

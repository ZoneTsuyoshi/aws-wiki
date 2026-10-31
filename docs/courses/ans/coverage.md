# 項目対応表

公式試験ガイドの全項目と、このコースのページの対応です。項目名は日本語で要約しています。正確な文言は[試験ガイド](https://docs.aws.amazon.com/aws-certification/latest/advanced-networking-specialty-01/advanced-networking-specialty-01.html)で確認してください。

ANS-C01 のガイドはスキルに番号を付けていないので、ガイドの順に「知識」「スキル」を並べ、各項目を扱う節へリンクします。全 16 タスクです。

!!! warning "最終受験日は 2026年12月31日です"
    詳しくは[コースの最初のページ](index.md)を参照してください。

## 分野1: ネットワーク設計 {#domain1}

### タスク 1.1: エッジサービス {#c-task-1-1}

| 種類 | 項目 | ページ |
|---|---|---|
| 知識 | CDN の設計パターン | [CDN の設計パターン](domain1.md#t1-1-cdn) |
| 知識 | グローバルなトラフィック管理の設計パターン | [グローバルなトラフィック管理](domain1.md#t1-1-global-traffic) |
| 知識 | CDN、トラフィック管理と他サービスの統合 | [他のサービスとの統合](domain1.md#t1-1-integration) |
| スキル | 送受信の要件から配信方式を設計 | [要件から配信方式を選ぶ](domain1.md#t1-1-requirements) |

### タスク 1.2: DNS の設計 {#c-task-1-2}

| 種類 | 項目 | ページ |
|---|---|---|
| 知識 | DNS プロトコル（レコード、TTL、DNSSEC、委任、ゾーン） | [DNS プロトコルの基礎](domain1.md#t1-2-dns-protocol) |
| 知識 | DNS のログと監視 | [DNS のログと監視](domain1.md#t1-2-logging) |
| 知識 | Route 53 の機能（エイリアス、トラフィックポリシー、リゾルバー、ヘルスチェック） | [Route 53 の機能](domain1.md#t1-2-features) |
| 知識 | Route 53 と VPC などの統合 | [公開とプライベート、VPC との統合](domain1.md#t1-2-public-private) |
| 知識 | ハイブリッド、マルチアカウント、マルチリージョンの統合 | [ハイブリッドとマルチアカウント](domain1.md#t1-2-hybrid) |
| 知識 | ドメイン登録 | [ドメイン登録](domain1.md#t1-2-domains) |
| スキル | 公開ホストゾーンの利用 | [公開とプライベート](domain1.md#t1-2-public-private) |
| スキル | プライベートホストゾーンの利用 | [公開とプライベート](domain1.md#t1-2-public-private) |
| スキル | Resolver エンドポイントの利用 | [ハイブリッドとマルチアカウント](domain1.md#t1-2-hybrid) |
| スキル | Route 53 によるグローバルなトラフィック管理 | [グローバルなトラフィック管理](domain1.md#t1-2-global) |
| スキル | ドメイン登録の作成と管理 | [ドメイン登録](domain1.md#t1-2-domains) |

### タスク 1.3: 負荷分散の設計 {#c-task-1-3}

| 種類 | 項目 | ページ |
|---|---|---|
| 知識 | L3、L4、L7 の負荷分散の仕組み | [L3、L4、L7 と選択](domain1.md#t1-3-choose) |
| 知識 | ロードバランサーの種類と要件 | [L3、L4、L7 と選択](domain1.md#t1-3-choose) |
| 知識 | 内部、外部の接続パターン | [内部と外部](domain1.md#t1-3-patterns) |
| 知識 | スケーリングの要因 | [スケーリング](domain1.md#t1-3-scaling) |
| 知識 | 他サービスとの統合 | [他のサービスとの統合](domain1.md#t1-3-integrations) |
| 知識 | 設定（プロキシプロトコル、クロスゾーン、スティッキー、アルゴリズム） | [ロードバランサーの設定](domain1.md#t1-3-config) |
| 知識 | ターゲットグループの設定（TCP、GENEVE、IP と instance） | [ターゲットグループの設定](domain1.md#t1-3-target-groups) |
| 知識 | AWS Load Balancer Controller | [AWS Load Balancer Controller](domain1.md#t1-3-lbc) |
| 知識 | 暗号化と認証（TLS の終端、パススルー） | [暗号化と認証](domain1.md#t1-3-tls) |
| スキル | 用途に合うロードバランサーの選択 | [L3、L4、L7 と選択](domain1.md#t1-3-choose) |
| スキル | Auto Scaling との統合 | [スケーリング](domain1.md#t1-3-scaling) |
| スキル | 既存のアプリへの統合 | [他のサービスとの統合](domain1.md#t1-3-integrations) |

### タスク 1.4: ログと監視の要件 {#c-task-1-4}

| 種類 | 項目 | ページ |
|---|---|---|
| 知識 | CloudWatch のメトリクス、エージェント、ログ、アラーム、ダッシュボード、インサイト | [CloudWatch](domain1.md#t1-4-cloudwatch) |
| 知識 | Transit Gateway Network Manager | [Network Manager](domain1.md#t1-4-network-manager) |
| 知識 | Reachability Analyzer | [Reachability Analyzer](domain1.md#t1-4-reachability) |
| 知識 | フローログと Traffic Mirroring | [フローログと Traffic Mirroring](domain1.md#t1-4-flow-mirror) |
| 知識 | アクセスログ（ロードバランサー、CloudFront） | [アクセスログ](domain1.md#t1-4-access-logs) |
| スキル | ログと監視の要件の特定 | [要件の特定](domain1.md#t1-4-requirements) |
| スキル | 状態を示すメトリクスの推奨 | [メトリクスとベースライン](domain1.md#t1-4-metrics) |
| スキル | ベースラインの取得 | [メトリクスとベースライン](domain1.md#t1-4-metrics) |

### タスク 1.5: ハイブリッドの設計 {#c-task-1-5}

| 種類 | 項目 | ページ |
|---|---|---|
| 知識 | ルーティングの基礎（動的と静的、BGP） | [ルーティングの基礎](domain1.md#t1-5-routing) |
| 知識 | 物理接続の L1、L2（VLAN、LAG、光、ジャンボフレーム） | [物理接続](domain1.md#t1-5-physical) |
| 知識 | カプセル化と暗号化（GRE、IPsec） | [カプセル化と暗号化](domain1.md#t1-5-encapsulation) |
| 知識 | アカウント間のリソース共有 | [リソース共有](domain1.md#t1-5-sharing) |
| 知識 | オーバーレイネットワーク | [SD-WAN とオーバーレイ](domain1.md#t1-5-sdwan) |
| スキル | ハイブリッド接続の要件の特定 | [要件の特定](domain1.md#t1-5-requirements) |
| スキル | 冗長な接続の設計（DX、VPN） | [冗長な接続](domain1.md#t1-5-redundancy) |
| スキル | BGP 属性による制御（負荷分散、active/passive） | [BGP 属性](domain1.md#t1-5-bgp) |
| スキル | SD-WAN の統合（Connect、オーバーレイ） | [SD-WAN とオーバーレイ](domain1.md#t1-5-sdwan) |

### タスク 1.6: マルチアカウントの設計 {#c-task-1-6}

| 種類 | 項目 | ページ |
|---|---|---|
| 知識 | 接続パターンと用途（ピアリング、Transit Gateway、PrivateLink） | [接続パターン](domain1.md#t1-6-patterns) |
| 知識 | VPC 共有の機能と利点 | [VPC 共有](domain1.md#t1-6-vpc-sharing) |
| 知識 | IP サブネットと重複への対処 | [IP の重複](domain1.md#t1-6-overlap) |
| スキル | 要件に合う方法で複数の VPC を接続 | [接続パターン](domain1.md#t1-6-patterns) |
| スキル | マルチアカウントでの VPC 共有 | [VPC 共有](domain1.md#t1-6-vpc-sharing) |
| スキル | IP の重複の管理（NAT、PrivateLink、Transit Gateway のルーティング） | [IP の重複](domain1.md#t1-6-overlap) |

## 分野2: ネットワークの実装 {#domain2}

### タスク 2.1: ハイブリッドの実装 {#c-task-2-1}

| 種類 | 項目 | ページ |
|---|---|---|
| 知識 | ルーティングプロトコル（静的、動的） | [ルーティングプロトコル](domain2.md#t2-1-routing) |
| 知識 | VPN（セキュリティ、アクセラレーション） | [VPN](domain2.md#t2-1-vpn) |
| 知識 | L1 とハードウェア（LOA、コロケーション、DX） | [物理接続](domain2.md#t2-1-physical) |
| 知識 | L2、L3（VLAN、IP、ゲートウェイ、ルーティング、スイッチング） | [物理接続](domain2.md#t2-1-physical) |
| 知識 | トラフィック管理と SD-WAN（Connect） | [SD-WAN](domain2.md#t2-1-sdwan) |
| 知識 | DNS（条件付き転送、ホストゾーン、リゾルバー） | [名前解決](domain2.md#t2-1-dns) |
| 知識 | セキュリティアプライアンス | [アプライアンス](domain2.md#t2-1-appliances) |
| 知識 | 負荷分散（L4 と L7、リバースプロキシ、L3） | [負荷分散](domain2.md#t2-1-load-balancing) |
| 知識 | インフラの自動化 | [自動化](domain2.md#t2-1-automation) |
| 知識 | Organizations と RAM（Transit Gateway、DX、VPC、Route 53） | [Organizations と RAM](domain2.md#t2-1-org-ram) |
| 知識 | 接続のテスト（Route Analyzer、Reachability Analyzer） | [テストと検証](domain2.md#t2-1-testing) |
| 知識 | VPC のネットワークサービス | [VPC のサービス](domain2.md#t2-1-vpc-services) |
| スキル | 物理のネットワーク要件の構成 | [物理接続](domain2.md#t2-1-physical) |
| スキル | 静的、動的ルーティングの構成 | [ルーティングプロトコル](domain2.md#t2-1-routing) |
| スキル | 既存のオンプレミスネットワークの接続 | [既存のネットワーク](domain2.md#t2-1-onprem) |
| スキル | 既存のオンプレミスの名前解決との接続 | [名前解決](domain2.md#t2-1-dns) |
| スキル | 負荷分散の構成と実装 | [負荷分散](domain2.md#t2-1-load-balancing) |
| スキル | 監視とログの構成 | [監視とログ](domain2.md#t2-1-monitoring) |
| スキル | 環境間の接続のテストと検証 | [テストと検証](domain2.md#t2-1-testing) |

### タスク 2.2: マルチアカウントの実装 {#c-task-2-2}

| 種類 | 項目 | ページ |
|---|---|---|
| 知識 | VPC 間、アカウント間の接続（ピアリング、Transit Gateway、VPN、第三者、SD-WAN、MPLS） | [VPC 間の接続](domain2.md#t2-2-multi-vpc) |
| 知識 | アプリのプライベート接続（PrivateLink） | [PrivateLink](domain2.md#t2-2-privatelink) |
| 知識 | 接続を広げる方法（Organizations、RAM） | [接続を広げる](domain2.md#t2-2-expansion) |
| 知識 | ホストとサービスの名前解決 | [名前解決](domain2.md#t2-2-name-resolution) |
| 知識 | インフラの自動化 | [自動化](domain2.md#t2-2-automation) |
| 知識 | 認証と認可（SAML、Active Directory） | [認証と認可](domain2.md#t2-2-auth) |
| 知識 | セキュリティ（SG、NACL、Network Firewall） | [境界のセキュリティ](domain2.md#t2-2-security) |
| 知識 | 接続のテスト（Route Analyzer、Reachability Analyzer、ツール） | [接続のテスト](domain2.md#t2-2-testing) |
| スキル | 単一、複数の VPC の構成（DHCP、ルーティング、SG） | [単一と複数の VPC](domain2.md#t2-2-single-multi-vpc) |
| スキル | 既存の第三者製品とのハイブリッド接続 | [第三者製品](domain2.md#t2-2-third-party) |
| スキル | ハブアンドスポークの構成（Transit Gateway、トランジット VPC） | [ハブアンドスポーク](domain2.md#t2-2-hub-spoke) |
| スキル | ハイブリッド接続を成立させる DNS の構成 | [名前解決でハイブリッド接続](domain2.md#t2-2-dns-hybrid) |
| スキル | ネットワーク境界のセキュリティの実装 | [境界のセキュリティ](domain2.md#t2-2-security) |
| スキル | 監視とログの構成 | [監視とログ](domain2.md#t2-2-monitoring) |

### タスク 2.3: DNS の実装 {#c-task-2-3}

| 種類 | 項目 | ページ |
|---|---|---|
| 知識 | プライベートと公開のホストゾーンの使い分け | [ゾーンの選択と転送](domain2.md#t2-3-zones) |
| 知識 | トラフィック管理の方法（レイテンシー、地域、重み） | [トラフィック管理](domain2.md#t2-3-traffic) |
| 知識 | DNS の委任と転送 | [委任と転送](domain2.md#t2-3-delegation) |
| 知識 | レコードの種類（A、AAAA、TXT、PTR、エイリアス） | [レコード](domain2.md#t2-3-records) |
| 知識 | DNSSEC | [DNSSEC](domain2.md#t2-3-dnssec) |
| 知識 | アカウント間の DNS の共有（RAM） | [共有と構成](domain2.md#t2-3-sharing) |
| 知識 | インバウンド、アウトバウンドの要件と実装 | [エンドポイント](domain2.md#t2-3-endpoints) |
| スキル | DNS ゾーンと条件付き転送の構成 | [ゾーンの選択と転送](domain2.md#t2-3-zones)、[委任と転送](domain2.md#t2-3-delegation) |
| スキル | DNS によるトラフィック管理の構成 | [トラフィック管理](domain2.md#t2-3-traffic) |
| スキル | ハイブリッドの DNS の構成 | [エンドポイント](domain2.md#t2-3-endpoints) |
| スキル | 適切なレコードの構成 | [レコード](domain2.md#t2-3-records) |
| スキル | Route 53 の DNSSEC の構成 | [DNSSEC](domain2.md#t2-3-dnssec) |
| スキル | 集中型、分散型の DNS の構成 | [共有と構成](domain2.md#t2-3-sharing) |
| スキル | Route 53 の監視とログの構成 | [監視とログ](domain2.md#t2-3-logging) |

### タスク 2.4: 自動化 {#c-task-2-4}

| 種類 | 項目 | ページ |
|---|---|---|
| 知識 | IaC（CDK、CloudFormation、CLI、SDK、API） | [IaC](domain2.md#t2-4-iac) |
| 知識 | イベント駆動のネットワーク自動化 | [イベント駆動](domain2.md#t2-4-event) |
| 知識 | IaC でハードコードする問題 | [ハードコード](domain2.md#t2-4-hardcoding) |
| スキル | 繰り返せるネットワーク構成の作成と管理 | [IaC](domain2.md#t2-4-iac) |
| スキル | イベント駆動の機能の統合 | [イベント駆動](domain2.md#t2-4-event) |
| スキル | ハイブリッドの自動化と IaC の統合 | [ハイブリッドの自動化](domain2.md#t2-4-hybrid) |
| スキル | リスクを除き、効率と最低コストを両立 | [リスクとコスト](domain2.md#t2-4-risk-cost) |
| スキル | IaC によるネットワーク資源の最適化の自動化 | [最適化](domain2.md#t2-4-optimize) |

## 分野3: ネットワークの管理と運用 {#domain3}

### タスク 3.1: ルーティングと接続の維持 {#c-task-3-1}

| 種類 | 項目 | ページ |
|---|---|---|
| 知識 | 業界標準のルーティングプロトコル（DX の BGP） | [BGP の管理](domain3.md#t3-1-bgp) |
| 知識 | 接続方法（DX ゲートウェイ、Transit Gateway、VIF） | [接続方式の運用](domain3.md#t3-1-connectivity) |
| 知識 | 上限とクォータの影響 | [上限とクォータ](domain3.md#t3-1-quotas) |
| 知識 | カスタムサービスへのアクセス方法（PrivateLink、ピアリング） | [プライベートアクセス](domain3.md#t3-1-private-access) |
| 知識 | リージョン間、リージョン内の通信パターン | [通信パターン](domain3.md#t3-1-patterns) |
| スキル | ルーティングプロトコルの管理（DX、VPN） | [BGP の管理](domain3.md#t3-1-bgp) |
| スキル | カスタムサービスへのプライベートアクセスの維持 | [プライベートアクセス](domain3.md#t3-1-private-access) |
| スキル | ルートテーブルによる制御（伝播、BGP） | [ルートテーブル](domain3.md#t3-1-route-tables) |
| スキル | AWS サービスへのプライベート、パブリックアクセスの設定 | [AWS サービスへのアクセス](domain3.md#t3-1-access-aws) |
| スキル | 動的、静的ルーティングの最適化（集約、CIDR の重複） | [経路の最適化](domain3.md#t3-1-route-optimization) |

### タスク 3.2: 監視と分析 {#c-task-3-2}

| 種類 | 項目 | ページ |
|---|---|---|
| 知識 | 性能の指標と到達性の制約（ルーティング、パケットサイズ） | [指標と制約](domain3.md#t3-2-metrics) |
| 知識 | 性能と到達性を調べるログとメトリクス | [ログとメトリクス](domain3.md#t3-2-logs) |
| 知識 | 収集と分析のツール（CloudWatch、フローログ、Traffic Mirroring） | [収集と分析](domain3.md#t3-2-tools) |
| 知識 | 経路の分析ツール（Reachability Analyzer、Network Manager） | [経路の分析](domain3.md#t3-2-routing-tools) |
| スキル | ツールの出力の分析 | [収集と分析](domain3.md#t3-2-tools) |
| スキル | トポロジーの把握 | [トポロジー](domain3.md#t3-2-topology) |
| スキル | パケットの分析（シェーピングの問題） | [パケットの分析](domain3.md#t3-2-packets) |
| スキル | 設定の誤りによる接続の問題の切り分け | [設定の誤り](domain3.md#t3-2-misconfig) |
| スキル | 設計要件を満たすかの検証 | [検証と自動化](domain3.md#t3-2-verify) |
| スキル | 接続の意図の検証の自動化 | [検証と自動化](domain3.md#t3-2-verify) |
| スキル | VPC のパケットサイズの不一致の解決 | [パケットサイズ](domain3.md#t3-2-mtu) |

### タスク 3.3: 最適化 {#c-task-3-3}

| 種類 | 項目 | ページ |
|---|---|---|
| 知識 | VPC ピアリングと Transit Gateway が適する状況 | [ピアリング、プロキシ、Transit Gateway](domain3.md#t3-3-peer-vs-tgw) |
| 知識 | 帯域の使用量を減らす方法（マルチキャスト、CloudFront） | [帯域の使用量](domain3.md#t3-3-bandwidth) |
| 知識 | VPC とオンプレミスの間の費用の低い接続 | [費用の低い接続](domain3.md#t3-3-cost) |
| 知識 | ネットワークインターフェイスの種類 | [インターフェイス](domain3.md#t3-3-interfaces) |
| 知識 | Route 53 の高可用性の機能 | [Route 53 の高可用性](domain3.md#t3-3-route53-ha) |
| 知識 | Route 53 の信頼性の選択肢 | [Route 53 の高可用性](domain3.md#t3-3-route53-ha) |
| 知識 | 負荷分散と分散のパターン | [分散のパターン](domain3.md#t3-3-lb) |
| 知識 | VPC サブネットの最適化 | [サブネット](domain3.md#t3-3-subnets) |
| 知識 | 接続の種類ごとのフレームサイズの最適化 | [フレームサイズ](domain3.md#t3-3-frames) |
| スキル | スループットの最適化 | [スループット](domain3.md#t3-3-throughput) |
| スキル | 性能に合うインターフェイスの選択（ENI、ENA、EFA） | [インターフェイス](domain3.md#t3-3-interfaces) |
| スキル | ピアリング、プロキシ、Transit Gateway の選択 | [ピアリング、プロキシ、Transit Gateway](domain3.md#t3-3-peer-vs-tgw) |
| スキル | 要件に合う接続サービスの実装 | [ピアリング、プロキシ、Transit Gateway](domain3.md#t3-3-peer-vs-tgw) |
| スキル | VPC とオンプレミスのマルチキャストの実装 | [マルチキャスト](domain3.md#t3-3-multicast) |
| スキル | 可用性を高めるゾーンとレコードの作成（プライベートの zonal DNS など） | [Route 53 の高可用性](domain3.md#t3-3-route53-ha) |
| スキル | Auto Scaling に合わせたサブネットの更新と最適化 | [サブネット](domain3.md#t3-3-subnets) |
| スキル | IP の枯渇を防ぐサブネットの更新（セカンダリ CIDR） | [サブネット](domain3.md#t3-3-subnets) |
| スキル | 接続の種類ごとのジャンボフレームの構成 | [フレームサイズ](domain3.md#t3-3-frames) |
| スキル | Global Accelerator による性能と可用性の向上 | [Global Accelerator](domain3.md#t3-3-global-accelerator) |

## 分野4: セキュリティ、コンプライアンス、ガバナンス {#domain4}

### タスク 4.1: セキュリティとコンプライアンス {#c-task-4-1}

| 種類 | 項目 | ページ |
|---|---|---|
| 知識 | アーキテクチャごとの脅威モデル | [脅威モデル](domain4.md#t4-1-threat-models) |
| 知識 | 一般的な脅威 | [脅威モデル](domain4.md#t4-1-threat-models) |
| 知識 | アプリの通信を守る仕組み | [通信を守る仕組み](domain4.md#t4-1-flows) |
| 知識 | 要件を満たすネットワーク構成 | [ネットワーク構成](domain4.md#t4-1-architecture) |
| スキル | 受信の保護（WAF、Shield、Network Firewall） | [受信](domain4.md#t4-1-inbound) |
| スキル | 送信の保護（Network Firewall、プロキシ、GWLB） | [送信](domain4.md#t4-1-outbound) |
| スキル | VPC 間の保護（SG、NACL、エンドポイントポリシー） | [VPC 間](domain4.md#t4-1-inter-vpc) |
| スキル | 要件を満たす構成の実装（信頼できないネットワーク、境界 VPC、3 層） | [ネットワーク構成](domain4.md#t4-1-architecture) |
| スキル | 脅威モデルの作成と緩和策の特定 | [脅威モデル](domain4.md#t4-1-threat-models) |
| スキル | 要件を満たすかのテスト（フェイルオーバー、回復性） | [テスト](domain4.md#t4-1-testing) |
| スキル | インシデントの報告と通知の自動化 | [通知の自動化](domain4.md#t4-1-automation) |

### タスク 4.2: 検証と監査 {#c-task-4-2}

| 種類 | 項目 | ページ |
|---|---|---|
| 知識 | 監視とログのサービス（CloudWatch、CloudTrail、Traffic Mirroring、フローログ、Network Manager） | [サービス](domain4.md#t4-2-services) |
| 知識 | 通知の仕組み（CloudWatch アラーム） | [通知の仕組み](domain4.md#t4-2-alerts) |
| 知識 | サービスごとのログの作成 | [ログの作成](domain4.md#t4-2-log-creation) |
| 知識 | ログの配信（Kinesis、Route 53、CloudWatch） | [ログの配信](domain4.md#t4-2-delivery) |
| 知識 | 設定の監査（SG、Firewall Manager、Trusted Advisor） | [設定の監査](domain4.md#t4-2-audit) |
| スキル | フローログの作成と分析（基本と拡張のフィールド） | [フローログ](domain4.md#t4-2-flow-logs) |
| スキル | Traffic Mirroring の作成と分析 | [Traffic Mirroring](domain4.md#t4-2-mirroring) |
| スキル | CloudWatch の自動アラームの実装 | [通知の仕組み](domain4.md#t4-2-alerts) |
| スキル | CloudWatch のカスタムメトリクスの実装 | [通知の仕組み](domain4.md#t4-2-alerts) |
| スキル | 複数のログの相関分析 | [相関分析](domain4.md#t4-2-correlation) |
| スキル | ログ配信の実装 | [ログの配信](domain4.md#t4-2-delivery) |
| スキル | 複数のサービス、アカウントの監査戦略の実装 | [設定の監査](domain4.md#t4-2-audit) |

### タスク 4.3: 機密性 {#c-task-4-3}

| 種類 | 項目 | ページ |
|---|---|---|
| 知識 | AWS の暗号化の選択肢 | [暗号化の選択肢](domain4.md#t4-3-options) |
| 知識 | DX の上の VPN | [DX の上の VPN](domain4.md#t4-3-vpn-dx) |
| 知識 | 転送時の暗号化の方式（IPsec） | [暗号化の方式](domain4.md#t4-3-ipsec) |
| 知識 | 責任共有モデルと暗号化 | [責任共有モデル](domain4.md#t4-3-shared-responsibility) |
| 知識 | DNS の通信の保護（DNSSEC） | [DNS の保護](domain4.md#t4-3-dns) |
| スキル | 要件を満たす暗号化の実装（IPsec、TLS） | [暗号化の選択肢](domain4.md#t4-3-options) |
| スキル | 転送時の暗号化の実装（CloudFront、ALB、NLB、VPN over DX、マネージド DB、S3、EC2、Transit Gateway） | [サービスごとの暗号化](domain4.md#t4-3-in-transit) |
| スキル | 証明書管理の実装（ACM、Private CA） | [証明書の管理](domain4.md#t4-3-certificates) |
| スキル | 安全な DNS 通信の実装 | [DNS の保護](domain4.md#t4-3-dns) |

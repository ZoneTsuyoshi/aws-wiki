# 分野1: ハイブリッド

オンプレミスと AWS をつなぐ回線、データ、アプリ、DNS、計算資源を、既存のシステムを変えられないという制約のもとで設計します。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [1.3.1](../../domain1.md#skill-1-3-1) | 冗長性とフェイルオーバーを備えたハイブリッド接続 |
| [1.3.2](../../domain1.md#skill-1-3-2) | ハイブリッドのデータ同期 |
| [1.3.3](../../domain1.md#skill-1-3-3) | レガシーシステムの統合 |
| [1.3.4](../../domain1.md#skill-1-3-4) | ハイブリッド環境の DNS |
| [1.3.5](../../domain1.md#skill-1-3-5) | ハイブリッドのコンピューティング |

## 学習の順番 {#study-order}

1. [回復性のモデル](../../../../services/network-connectivity.md#dx-resiliency)と [Direct Connect](../../../../services/network-connectivity.md#direct-connect): SLA と構成の対応を覚えます。
2. [DX を主、VPN を従にする](../../../../services/network-connectivity.md#bgp-dx-vpn)と[オンプレミスとの接続](../../../../services/network-connectivity.md#choosing-hybrid): 経路の優先と暗号化の選択を確認します。
3. [DataSync](../../../../services/migration.md#datasync)、[Storage Gateway](../../../../services/migration.md#storage-gateway)、[Transfer Family](../../../../services/migration.md#transfer-family)、[サービスの比較](../../../../services/migration.md#transfer-comparison): 移行か継続利用か、取引先かで選びます。
4. [Amazon MQ](../../../../services/other-services.md#mq)、[リクエストとレスポンスの変換](../../../../services/api-gateway.md#transformations)、[AppFlow](../../../../services/data-engineering.md#appflow): コードを変えられないときの手段を整理します。
5. [エンドポイント](../../../../services/network-connectivity.md#resolver-endpoints)、[転送ルール](../../../../services/network-connectivity.md#resolver-rules)、[プライベートホストゾーン](../../../../services/network-connectivity.md#private-hosted-zones): 方向と優先順位を確認します。
6. [ECS Anywhere](../../../../services/operations.md#ecs-anywhere)、[EKS Anywhere](../../../../services/operations.md#eks-anywhere)、[Outposts](../../../../services/cloud-foundations.md#outposts)、[Local Zones](../../../../services/cloud-foundations.md#local-zones): 機器とデータの置き場所で選びます。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| Maximum resiliency | 99.99%。2 ロケーション × 各 2 デバイス | ロケーションの障害にも耐える |
| High resiliency | 99.9%。2 ロケーションに 1 接続ずつ | 費用とのバランス |
| MACsec の対応 | 専用接続の 10、100、400 Gbps | ロケーションの機器までのレイヤー 2 |
| Tape Gateway の保管先 | S3 Glacier Flexible Retrieval、Deep Archive | 既存のバックアップソフトのまま |
| VPN の MTU | 約 1400 | DX は 8500 まで。切り替え時に注意 |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 多数の VPC へ DX、費用を抑えたバックアップ | トランジット VIF と DX ゲートウェイ、VPN は BGP で |
| VPC まで暗号化、公開 IP なし | プライベート IP VPN |
| 大きな帯域でルーターまで暗号化 | MACsec |
| ファイル共有を移行し、差分を同期 | DataSync |
| オンプレミスのアプリが NFS を使い続ける | S3 File Gateway |
| 取引先の SFTP、AS2 を変えない | Transfer Family |
| バックアップソフトとテープの手順を変えない | Tape Gateway |
| RabbitMQ や JMS のコードを変えない | Amazon MQ |
| SOAP を REST で公開 | REST API の非プロキシ統合とマッピングテンプレート |
| 機能ごとに少しずつ置き換える | ストラングラーフィグ。前段のパスで振り分け |
| 60 アカウントからオンプレミスの名前を引く | 中央のアウトバウンドエンドポイントと、RAM で共有するルール |
| データを施設に置き、AWS と同じ API | Outposts |
| 既存のサーバーを ECS で統一 | ECS Anywhere |
| 接続が限られた環境で Kubernetes | EKS Anywhere |
| 都市の近くの遅延だけ | Local Zones |

## 引っかかりやすい点 {#traps}

- Transit Gateway で VPN を静的にすると、DX の伝播した経路に勝ち、平常時も VPN を使います。
- MACsec はロケーションの機器までで、VPC までの暗号化ではありません。
- プライベートホストゾーンにレコードがないと NXDOMAIN を返し、公開 DNS には流れません。
- 同じ名前の転送ルールは、プライベートホストゾーンより優先されます。
- FSx File Gateway は新規受付を終了しました。FSx for Windows File Server へ直接接続します。
- EKS のハイブリッドノードと Outposts のローカルクラスターは、機器やコントロールプレーンの置き場所が EKS Anywhere と異なります。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [hybrid 問1](../../exercises/hybrid.md#q1) | 1.3.1 | 証券の基幹システムは、オンプレミスと AWS の接続に 99.99% の SLA を求めています。デ… |
| [hybrid 問2](../../exercises/hybrid.md#q2) | 1.3.1 | 製造業は、200 の VPC を複数のリージョンで Transit Gateway につないでいます… |
| [hybrid 問3](../../exercises/hybrid.md#q3) | 1.3.1 | 規制の要件で、オンプレミスから Transit Gateway までの通信を暗号化します。Direc… |
| [hybrid 問4](../../exercises/hybrid.md#q4) | 1.3.1 | 映像制作の会社が、100 Gbps の専用接続で大容量のデータを送っています。監査の結果、データセン… |
| [hybrid 問5](../../exercises/hybrid.md#q5) | 1.3.2 | オンプレミスの NAS にある 200 TB のファイルを Amazon EFS へ移します。切り替… |
| [hybrid 問6](../../exercises/hybrid.md#q6) | 1.3.2 | 工場の検査装置は、結果を NFS で書き込みます。装置の設定は変更できず、工場で続けて使います。デー… |
| [hybrid 問7](../../exercises/hybrid.md#q7) | 1.3.2 | 物流の会社は、毎日 300 社の取引先から SFTP と AS2 でファイルを受け取っています。取引… |
| [hybrid 問8](../../exercises/hybrid.md#q8) | 1.3.2 | 金融機関の既存のバックアップソフトは、物理のテープライブラリへ書き込みます。テープの保管と搬送の費用… |
| [hybrid 問9](../../exercises/hybrid.md#q9) | 1.3.3 | 物流の基幹システムは、複数のアプリが RabbitMQ で AMQP のメッセージをやり取りします。… |
| [hybrid 問10](../../exercises/hybrid.md#q10) | 1.3.3 | オンプレミスの基幹システムは SOAP の API だけを提供し、変更できません。Direct Co… |
| [hybrid 問11](../../exercises/hybrid.md#q11) | 1.3.3 | 大規模なオンプレミスのモノリスを、数年かけて機能ごとにマイクロサービスへ置き換えます。利用者の UR… |
| [hybrid 問12](../../exercises/hybrid.md#q12) | 1.3.3 | 営業部門は Salesforce の商談データを、毎晩 S3 のデータレイクに取り込みたいと考えてい… |
| [hybrid 問13](../../exercises/hybrid.md#q13) | 1.3.4 | ハイブリッド環境の DNS を整備します。オンプレミスのサーバーから aws.example.int… |
| [hybrid 問14](../../exercises/hybrid.md#q14) | 1.3.4 | 組織に 60 のアカウントがあり、どの VPC からもオンプレミスの名前を解決する必要があります。各… |
| [hybrid 問15](../../exercises/hybrid.md#q15) | 1.3.4 | example.com の公開ホストゾーンと、同じ名前のプライベートホストゾーンを VPC に関連付… |
| [hybrid 問16](../../exercises/hybrid.md#q16) | 1.3.4 | VPC に corp.example.com のプライベートホストゾーンを関連付け、api.corp… |
| [hybrid 問17](../../exercises/hybrid.md#q17) | 1.3.5 | 病院グループは、院内の医療機器と数ミリ秒でやり取りし、患者データは法令により院内に置く必要があります… |
| [hybrid 問18](../../exercises/hybrid.md#q18) | 1.3.5 | 小売の会社は、各店舗に既存のサーバーを持っています。AWS の機器を置く予算はありません。レジ周辺の… |
| [hybrid 問19](../../exercises/hybrid.md#q19) | 1.3.5 | 防衛関連の工場は、外部との接続が制限された環境で Kubernetes を動かします。AWS の機器… |
| [hybrid 問20](../../exercises/hybrid.md#q20) | 1.3.5 | ライブ配信の制作ツールは、ある大都市の利用者に 1 桁ミリ秒の遅延を提供する必要があります。最寄りの… |

<!-- questions:end -->

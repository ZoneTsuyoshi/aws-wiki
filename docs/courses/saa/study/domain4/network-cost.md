# 分野4: ネットワークの費用

経路ごとの料金を知り、要件を満たす最も安い経路を選びます。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [NAT ゲートウェイの構成](../../domain4.md#t4-4-nat) | NAT ゲートウェイ、ネットワークに適切な NAT ゲートウェイ構成の設定 |
| [接続の種類と帯域](../../domain4.md#t4-4-connectivity) | ネットワーク接続、適切なネットワーク接続の設定、ネットワーク機器の適切な帯域の選択 |
| [転送費用を抑える経路](../../domain4.md#t4-4-routes) | 転送費用を最小にするネットワーク経路の設定 |
| [ルーティングとトポロジー](../../domain4.md#t4-4-topology) | ネットワークのルーティング、トポロジー、ピアリング |
| [負荷分散の費用](../../domain4.md#t4-4-lb) | 負荷分散の概念 |
| [DNS などのネットワークサービス](../../domain4.md#t4-4-dns) | ネットワークサービスの適切な用途 |
| [CDN とエッジキャッシュの戦略](../../domain4.md#t4-4-cdn) | CDN とエッジキャッシュの戦略的な必要性の判断 |
| [スロットリングの戦略](../../domain4.md#t4-4-throttling) | 適切なスロットリング戦略の選択 |

## 学習の順番 {#study-order}

1. [NAT ゲートウェイ](../../../../services/network-connectivity.md#nat-gateway)と[データ転送の費用](../../../../services/cost-management.md#data-transfer): NAT の構成と経路の料金を比べます。
2. [オンプレミスとの接続](../../../../services/network-connectivity.md#choosing-hybrid)と[接続の種類](../../../../services/network-connectivity.md#dx-connections): 接続の選び方を確認します。
3. [トンネル](../../../../services/network-connectivity.md#vpn-tunnels)と[LAG](../../../../services/network-connectivity.md#dx-lag): 帯域の増やし方を確認します。
4. [VPC エンドポイントと PrivateLink](../../../../services/networking.md#vpc-endpoints)と[Global Accelerator](../../../../services/network-connectivity.md#global-accelerator): 経路の改善と、費用が増えるものを区別します。
5. [VPC ピアリング](../../../../services/network-connectivity.md#vpc-peering)と[Transit Gateway](../../../../services/network-connectivity.md#transit-gateway): VPC の接続の費用を比べます。
6. [TTL とエイリアスの違い](../../../../services/networking.md#route53-ttl)と[プライベートホストゾーン](../../../../services/network-connectivity.md#private-hosted-zones): DNS の費用と内部の名前解決を確認します。
7. [キャッシュキーとポリシー](../../../../services/networking.md#cache-keys)と[TTL とキャッシュの期間](../../../../services/networking.md#cloudfront-ttl): ヒット率を上げる設定を確認します。
8. [使用量プランと API キー](../../../../services/api-gateway.md#usage-plans)と[レートベースルール](../../../../services/certificates.md#rate-based-rules): スロットリングの置き場所を確認します。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| 同じ AZ の中 | 無料 | プライベート IP の通信 |
| AZ 間 | 送受信の両方が有料 | NAT と NLB のターゲットの配置に注意。ALB のクロスゾーンにはかからない |
| インターネットからの受信 | 無料 | 送信は有料（月 100 GB まで無料） |
| VPN のトンネル | 1.25 Gbps | 8 Gbps なら 4 接続を ECMP で |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 開発環境の NAT を安く | 共有の 1 つ |
| 本番の NAT | AZ ごと |
| 定常の大量の通信 | Direct Connect |
| 小さな帯域の専用線 | ホスト接続 |
| S3 への通信を安く | ゲートウェイエンドポイント |
| 2 つの VPC で大量に送る | VPC ピアリング |
| ドメインの頂点を ALB に向ける | Route 53 のエイリアス |
| 取引先ごとに制限する | 使用量プランと API キー |

## 引っかかりやすい点 {#traps}

- VGW は ECMP に対応しません。Transit Gateway が必要です。
- Global Accelerator は費用を下げるサービスではありません。
- ピアリングに推移的なルーティングはありません。
- キャッシュキーを増やすと、ヒット率が下がります。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [network-cost 問1](../../exercises/network-cost.md#q1) | NAT ゲートウェイの構成 | 開発環境の VPC には 3 つの AZ があり、AZ ごとに NAT ゲートウェイがあります。通信… |
| [network-cost 問2](../../exercises/network-cost.md#q2) | NAT ゲートウェイの構成 | NAT インスタンスが NAT ゲートウェイより合うのはどの条件ですか。 |
| [network-cost 問3](../../exercises/network-cost.md#q3) | NAT ゲートウェイの構成 | 本番で、NAT ゲートウェイの AZ 間の転送料と AZ の障害の影響を避けます。どの構成ですか。 |
| [network-cost 問4](../../exercises/network-cost.md#q4) | 接続と帯域 | オンプレミスのシステムが AWS から毎日 5 TB を取得しています。今はインターネット経由で、送… |
| [network-cost 問5](../../exercises/network-cost.md#q5) | 接続と帯域 | 500 Mbps の安定した専用線が必要です。10 Gbps は要りません。どれを選びますか。 |
| [network-cost 問6](../../exercises/network-cost.md#q6) | 接続と帯域 | 標準のトンネルの Site-to-Site VPN で 8 Gbps が必要です。正しい構成はどれで… |
| [network-cost 問7](../../exercises/network-cost.md#q7) | 接続と帯域 | 接続の帯域の設計について正しいものはどれですか。 |
| [network-cost 問8](../../exercises/network-cost.md#q8) | 転送費用の経路 | データ転送の料金について正しいものを選んでください。（2つ選択） |
| [network-cost 問9](../../exercises/network-cost.md#q9) | 転送費用の経路 | プライベートサブネットの EC2 の通信が NAT ゲートウェイを通っています。処理量の 9 割は … |
| [network-cost 問10](../../exercises/network-cost.md#q10) | 転送費用の経路 | Global Accelerator の費用について正しいものを選んでください。（2つ選択） |
| [network-cost 問11](../../exercises/network-cost.md#q11) | 転送費用の経路 | 東京のアプリが米国のバケットを読み続け、転送料が大きくなっています。最も直接の改善はどれですか。 |
| [network-cost 問12](../../exercises/network-cost.md#q12) | ルーティング | 2 つの VPC の間で大量のデータを送るだけです。費用が最も安い接続はどれですか。 |
| [network-cost 問13](../../exercises/network-cost.md#q13) | ルーティング | VPC A と B、B と C をピアリングしています。A から C に接続できません。VPC は … |
| [network-cost 問14](../../exercises/network-cost.md#q14) | ルーティング | 複数のアカウントで同じネットワークを使い、VPC 間の接続の費用を増やしたくありません。どの方法が合… |
| [network-cost 問15](../../exercises/network-cost.md#q15) | 負荷分散の費用 | サービスごとに ALB を立てており、費用とパブリック IPv4 が増えています。どうしますか。 |
| [network-cost 問16](../../exercises/network-cost.md#q16) | 負荷分散の費用 | NLB の AZ ごとのターゲット数が違うので、クロスゾーン負荷分散を有効にしました。負荷は均等にな… |
| [network-cost 問17](../../exercises/network-cost.md#q17) | 負荷分散の費用 | NLB のクロスゾーン負荷分散を無効に戻して、AZ 間の転送料を減らします。そのときのトレードオフは… |
| [network-cost 問18](../../exercises/network-cost.md#q18) | DNS | example.com（ドメインの頂点）を ALB に向けます。問い合わせの費用も抑えます。どの設定… |
| [network-cost 問19](../../exercises/network-cost.md#q19) | DNS | Route 53 の TTL を 1 秒に下げたところ、DNS のクエリの費用が増えました。正しい説… |
| [network-cost 問20](../../exercises/network-cost.md#q20) | DNS | VPC の内部のサービスの名前を、パブリックに公開せず解決します。オンプレミスからの解決は要りません… |
| [network-cost 問21](../../exercises/network-cost.md#q21) | CDN | CloudFront を入れる費用面の理由として正しいものを選んでください。（2つ選択） |
| [network-cost 問22](../../exercises/network-cost.md#q22) | CDN | CloudFront のヒット率が 20% で、オリジンの ALB の費用が増えています。応答を変え… |
| [network-cost 問23](../../exercises/network-cost.md#q23) | CDN | CloudFront の効果が小さいのはどのケースですか。 |
| [network-cost 問24](../../exercises/network-cost.md#q24) | スロットリング | 取引先が API を呼びすぎて、Lambda の費用が増えています。取引先ごとに制限します。どう設定… |
| [network-cost 問25](../../exercises/network-cost.md#q25) | スロットリング | 1 つの送信元からの大量のリクエストを CloudFront の前段で抑えます。どれを使いますか。 |
| [network-cost 問26](../../exercises/network-cost.md#q26) | スロットリング | 下流のサービスの処理能力に合わせて流量を抑え、急増の処理も失いたくありません。どの戦略ですか。 |

<!-- questions:end -->

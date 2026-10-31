# 分野1: CloudFront と配信設計

配信の要件から、CloudFront の設計を選ぶ問題です。キャッシュ、オリジンの保護、証明書と WAF のリージョンが中心です。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [CDN の設計パターン](../../domain1.md#t1-1-cdn) | CDN の設計パターン |
| [他のサービスとの統合](../../domain1.md#t1-1-integration) | CDN、トラフィック管理と他サービスの統合 |
| [要件から配信方式を選ぶ](../../domain1.md#t1-1-requirements) | 送受信の要件から配信方式を設計 |

## 学習の順番 {#study-order}

1. [CloudFront](../../../../services/networking.md#cloudfront): CDN の役割とオリジンの種類を確認します。
2. [S3 オリジンの保護: OAC](../../../../services/networking.md#oac): S3 への直接のアクセスを防ぐ方法を押さえます。
3. [キャッシュキーとポリシー](../../../../services/networking.md#cache-keys): キャッシュキーとオリジンリクエストポリシーの違いを理解します。
4. [オリジンフェイルオーバー](../../../../services/networking.md#origin-failover): 切り替えの時間の計算と短くする方法を確認します。
5. [リージョンのルール](../../../../services/certificates.md#region-rules): 証明書のリージョンの規則を覚えます。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| オリジンの接続の失敗 | 既定で最大 30 秒 | 10 秒 × 3 回 |
| CloudFront の証明書と Web ACL | `us-east-1` | ALB の証明書は ALB のリージョン |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| ヒット率が低く、キーにヘッダーが多い | オリジンリクエストポリシーへ移す |
| ALB を CloudFront 経由に限定 | カスタムヘッダーとマネージドプレフィックスリスト |
| 大きなファイルを世界から S3 へ | S3 Transfer Acceleration |
| 自前の CloudFront の裏に API | リージョナル API |

## 引っかかりやすい点 {#traps}

- OAC は S3 の Web サイトエンドポイントには使えません。
- TTL を伸ばしても、キャッシュキーのばらつきは解決しません。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [cloudfront 問1](../../exercises/cloudfront.md#q1) | CDN の設計パターン | 静的ファイルを S3 に置き、世界へ配信します。監査の要件で、S3 への直接のアクセスは禁止し、配信… |
| [cloudfront 問2](../../exercises/cloudfront.md#q2) | CDN の設計パターン | EC サイトでキャッシュのヒット率が 20% しかありません。ビヘイビアのキャッシュポリシーで、全ク… |
| [cloudfront 問3](../../exercises/cloudfront.md#q3) | CDN の設計パターン | 2 リージョンの S3 バケットをオリジングループに設定しました。プライマリの障害時に、利用者の G… |
| [cloudfront 問4](../../exercises/cloudfront.md#q4) | CDN の設計パターン | ライブ配信で、世界の複数のリージョナルエッジキャッシュから、1 つのオリジンへ同時に多くのリクエスト… |
| [cloudfront 問5](../../exercises/cloudfront.md#q5) | 他のサービスとの統合 | 大阪リージョンの ALB をオリジンとする CloudFront に、独自ドメインの HTTPS を… |
| [cloudfront 問6](../../exercises/cloudfront.md#q6) | 他のサービスとの統合 | API Gateway の API の前に、自社で管理する CloudFront を置きます。キャッ… |
| [cloudfront 問7](../../exercises/cloudfront.md#q7) | 他のサービスとの統合 | CloudFront に AWS WAF の Web ACL を付けます。ディストリビューションと … |
| [cloudfront 問8](../../exercises/cloudfront.md#q8) | 他のサービスとの統合 | インターネット向け ALB が CloudFront の背後にあります。利用者が ALB の DNS… |
| [cloudfront 問9](../../exercises/cloudfront.md#q9) | 要件から配信方式を選ぶ | 世界中の工場が、数 GB のログファイルを東京の S3 バケットへ毎日アップロードします。遅延が大き… |
| [cloudfront 問10](../../exercises/cloudfront.md#q10) | 要件から配信方式を選ぶ | 動的な HTTP API を世界へ提供します。応答はキャッシュできません。SQL インジェクション対… |
| [cloudfront 問11](../../exercises/cloudfront.md#q11) | 要件から配信方式を選ぶ | 50 個の VPC がそれぞれ NAT ゲートウェイを持ち、費用と出口の管理が問題になっています。全… |

<!-- questions:end -->

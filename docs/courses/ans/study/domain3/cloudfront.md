# 分野3: CloudFront と配信設計

帯域の使用量を減らす方法を問います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [帯域の使用量](../../domain3.md#t3-3-bandwidth) | 帯域の使用量を減らす方法（マルチキャスト、CloudFront） |

## 学習の順番 {#study-order}

1. [圧縮](../../../../services/networking.md#cloudfront-compression): 圧縮の条件を確認します。
2. [マルチキャスト](../../../../services/network-connectivity.md#tgw-multicast): マルチキャストの効果を確認します。
3. [データ転送の費用](../../../../services/cost-management.md#data-transfer): 転送の費用を確認します。

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 同じ応答を多くの利用者へ | CloudFront のキャッシュと圧縮 |
| S3 への通信の NAT の費用 | ゲートウェイエンドポイント |

## 引っかかりやすい点 {#traps}

- インスタンスを大きくしても使用量は減りません。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [cloudfront 問12](../../exercises/cloudfront.md#q12) | 帯域の使用量 | EC2 のオリジンから直接 JSON を配信しており、データ転送の費用が大きくなっています。同じ応答… |
| [cloudfront 問13](../../exercises/cloudfront.md#q13) | 帯域の使用量 | VPC 内の 1 台のサーバーから、同じ市場データを 80 台の受信者へ UDP で送っています。ユ… |
| [cloudfront 問14](../../exercises/cloudfront.md#q14) | 帯域の使用量 | プライベートサブネットの EC2 が、同じリージョンの S3 へ月に数百 TB を転送しています。C… |

<!-- questions:end -->

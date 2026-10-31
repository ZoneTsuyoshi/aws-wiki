# 分野2: CloudFront と VPC エンドポイント

CloudFront の署名付き URL と Cookie、配信経路の TLS、VPC エンドポイントによる閉域接続を問います。接続できないときの切り分けやキャッシュの調整は[分野4](../domain4/networking.md)で扱います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [2.1.4](../../domain2.md#skill-2-1-4) | CloudFront の署名付き URL と Cookie |
| [2.2.1](../../domain2.md#skill-2-2-1) | CloudFront の HTTPS |
| [2.2.6](../../domain2.md#skill-2-2-6) | フィールドレベル暗号化 |
| [2.3.2](../../domain2.md#skill-2-3-2) | VPC エンドポイントによるプライベート接続 |

## 学習の順番 {#study-order}

1. [署名付き URL と署名付き Cookie](../../../../services/networking.md#signed-urls-cookies): 使い分け、ポリシーの種類、S3 の署名付き URL との違いを確認します。
2. [署名付き URL の仕様](../../../../services/networking.md#signed-url-details): クエリの名前とキーグループの上限を見ます。
3. [S3 オリジンの保護: OAC](../../../../services/networking.md#oac): 迂回を防ぐ設定と、SSE-KMS のときの追加の許可を押さえます。
4. [HTTPS](../../../../services/networking.md#cloudfront-https): 2 つの区間の設定と証明書のリージョンを覚えます。
5. [フィールドレベル暗号化](../../../../services/networking.md#field-level-encryption): HTTPS では守れないものを理解します。
6. [VPC エンドポイントと PrivateLink](../../../../services/networking.md#vpc-endpoints)と[選び方と制約](../../../../services/networking.md#endpoint-settings): ゲートウェイとインターフェイスの違いを整理します。
7. [エンドポイントポリシー](../../../../services/networking.md#endpoint-policies)と [VPC の DNS 属性](../../../../services/networking.md#vpc-dns-attributes): 権限の上限であることと、プライベート DNS の条件を確認します。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| キーグループ | ディストリビューションに 4 個、1 グループに公開鍵 5 個 | 旧方式のキーペアは推奨されない |
| `Expires` | エポック秒 | |
| CloudFront の独自ドメインの証明書 | `us-east-1` | ALB の証明書は ALB のリージョン |
| フィールドレベル暗号化 | 10 フィールド、本文 1 MB | 公開鍵暗号 |
| ゲートウェイエンドポイントの対象 | S3、DynamoDB | 追加料金なし |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 1 ファイルを限定配信する | CloudFront の署名付き URL |
| HLS の動画や会員エリアを URL を変えずに配信する | CloudFront の署名付き Cookie |
| 開始日時や IP の範囲も指定する | カスタムポリシー。既定（canned）は終了日時のみ |
| S3 を CloudFront 経由だけに限定する | OAC とバケットポリシーの `AWS:SourceArn` |
| 利用者の通信を HTTPS にする | ビューワープロトコルポリシーを HTTPS へのリダイレクトか HTTPS のみにする |
| カード番号を社内のログやサーバーで平文にしたくない | フィールドレベル暗号化 |
| プライベートサブネットから Secrets Manager へ接続する | インターフェイスエンドポイント（PrivateLink） |
| プライベート DNS を有効にできない | `enableDnsSupport` と `enableDnsHostnames` の両方を `true` にする |
| VPN の先から S3 へプライベートに接続する | S3 のインターフェイスエンドポイント |
| S3 を特定のエンドポイントからのアクセスに限定する | バケットポリシーの `aws:SourceVpce` |

## 引っかかりやすい点 {#traps}

- 通常の URL に `Expires`、`Policy`、`Signature`、`Key-Pair-Id`、`Hash-Algorithm` のクエリがあると、署名付き URL とみなされます。
- 署名付き URL と Cookie の両方があると、署名付き URL が優先されます。
- OAC は S3 の Web サイトエンドポイントでは使えません。SSE-KMS なら KMS のキーポリシーでも CloudFront を許可します。
- エンドポイントポリシーは権限を与えません。IAM やバケットポリシーの許可に対する上限です。
- ゲートウェイエンドポイントは VPC の外（VPN、ピアリング、Direct Connect の先）からは使えません。
- エンドポイント経由のリクエストには `aws:SourceIp` に使うパブリック IP がありません。`aws:SourceVpce` に書き換えます。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [networking 問16](../../exercises/networking.md#q16) | 2.1.4 | CloudFront で配信するインストーラーを、ファイルごとに、指定した日時から、顧客の IP ア… |

<!-- questions:end -->

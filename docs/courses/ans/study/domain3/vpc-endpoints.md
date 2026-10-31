# 分野3: VPC の構成とエンドポイント

カスタムサービスと AWS サービスへのアクセスの維持を問います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [プライベートアクセス](../../domain3.md#t3-1-private-access) | カスタムサービスへのアクセス方法（PrivateLink、ピアリング）、カスタムサービスへのプライベートアクセスの維持 |
| [AWS サービスへのアクセス](../../domain3.md#t3-1-access-aws) | AWS サービスへのプライベート、パブリックアクセスの設定 |

## 学習の順番 {#study-order}

1. [VPC エンドポイントと PrivateLink](../../../../services/networking.md#vpc-endpoints): PrivateLink の症状を確認します。
2. [エンドポイントの選び方と制約](../../../../services/networking.md#endpoint-settings): オンプレミスからの利用を押さえます。
3. [公開 VIF の経路制御](../../../../services/network-connectivity.md#bgp-public-vif): 公開 VIF の経路の絞り方を確認します。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| 同じリージョンの公開経路 | `7224:8100` | ルーターで受け入れる |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| オンプレミスから S3 へプライベートに | インターフェイスエンドポイント |
| 公開 IP を使わず経路も暗号化 | プライベート IP VPN とインターフェイスエンドポイント |

## 引っかかりやすい点 {#traps}

- ゲートウェイエンドポイントは VPC の外から使えません。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [vpc-endpoints 問4](../../exercises/vpc-endpoints.md#q4) | プライベートアクセス | 提供者の VPC と利用者の VPC は CIDR が重複しています。提供者の 1 つの TCP サ… |
| [vpc-endpoints 問5](../../exercises/vpc-endpoints.md#q5) | プライベートアクセス | 運用中の PrivateLink で、利用者の一部の接続がタイムアウトします。提供者の NLB のタ… |
| [vpc-endpoints 問6](../../exercises/vpc-endpoints.md#q6) | プライベートアクセス | VPC ピアリングで共有サービスへ接続しています。VPC A が B とピアリングし、B が C と… |
| [vpc-endpoints 問7](../../exercises/vpc-endpoints.md#q7) | AWS サービスへのアクセス | オンプレミスから DX 経由で、S3 へプライベートの IP で接続します。公開 VIF は作れず、… |
| [vpc-endpoints 問8](../../exercises/vpc-endpoints.md#q8) | AWS サービスへのアクセス | 公開 VIF で S3 へ大量に転送します。受信した経路に、すべてのリージョンの公開プレフィックスが… |
| [vpc-endpoints 問9](../../exercises/vpc-endpoints.md#q9) | AWS サービスへのアクセス | 規制で「公開 IP を使わず、経路も暗号化する」ことを求められています。オンプレミスから KMS の… |

<!-- questions:end -->

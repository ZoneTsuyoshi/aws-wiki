# 分野1: VPC Resolver とハイブリッド DNS

ハイブリッドの DNS の設計と、DNS のログを問います。向きとエンドポイントを対応させます。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [ハイブリッドとマルチアカウント](../../domain1.md#t1-2-hybrid) | ハイブリッド、マルチアカウント、マルチリージョンの統合、Resolver エンドポイントの利用 |
| [DNS のログと監視](../../domain1.md#t1-2-logging) | DNS のログと監視 |

## 学習の順番 {#study-order}

1. [VPC Resolver](../../../../services/network-connectivity.md#vpc-resolver): VPC Resolver の役割を確認します。
2. [エンドポイント](../../../../services/network-connectivity.md#resolver-endpoints): インバウンドとアウトバウンドの違いと容量を押さえます。
3. [ハイブリッド DNS](../../../../services/network-connectivity.md#hybrid-dns): 共有サービス VPC に集約する構成を理解します。
4. [フローログの分析](../../../../services/network-connectivity.md#flow-log-analysis): DNS の記録がフローログに残らないことを確認します。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| エンドポイントの容量 | IP あたり UDP で 10,000 QPS | 接続追跡が働くと下がる |
| 公開クエリログ | `us-east-1` の CloudWatch Logs | 他の送信先は不可 |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 多数の VPC からオンプレミスを引く | 共有サービス VPC と RAM で共有したルール |
| オンプレミスから PHZ を引く | エンドポイントの VPC に PHZ を関連付ける |
| VPC からの問い合わせの調査 | Resolver クエリログ |

## 引っかかりやすい点 {#traps}

- Transit Gateway は PHZ の名前を解決しません。
- どちらのクエリログもキャッシュから答えたものは記録しません。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [resolver 問1](../../exercises/resolver.md#q1) | ハイブリッドとマルチアカウント | 200 個の VPC を複数のアカウントで運用しています。各 VPC は Transit Gatew… |
| [resolver 問2](../../exercises/resolver.md#q2) | ハイブリッドとマルチアカウント | VPC Resolver のインバウンドエンドポイントの容量を設計します。オンプレミスから UDP … |
| [resolver 問3](../../exercises/resolver.md#q3) | ハイブリッドとマルチアカウント | PHZ aws.example.com はワークロード VPC にのみ関連付いています。インバウンド… |
| [resolver 問4](../../exercises/resolver.md#q4) | ハイブリッドとマルチアカウント | 東京と大阪の VPC を Transit Gateway ピアリングで接続しています。大阪の EC2… |
| [resolver 問5](../../exercises/resolver.md#q5) | DNS のログと監視 | 公開サイト example.com について、権威 DNS への問い合わせの件数と問い合わせ元のリゾ… |
| [resolver 問6](../../exercises/resolver.md#q6) | DNS のログと監視 | EC2 が不審なドメインへ問い合わせた疑いがあります。VPC は既定の DNS を使っています。フロ… |
| [resolver 問7](../../exercises/resolver.md#q7) | DNS のログと監視 | Resolver クエリログを全 VPC で有効にしましたが、同じ EC2 が同じドメインを何度も問… |

<!-- questions:end -->

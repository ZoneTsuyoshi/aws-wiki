# 分野2: CloudWatch とログの要件

ハイブリッドとマルチアカウントの監視とログの設定を問います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [監視とログ](../../domain2.md#t2-1-monitoring) | 監視とログの構成 |
| [監視とログ](../../domain2.md#t2-2-monitoring) | 監視とログの構成 |

## 学習の順番 {#study-order}

1. [フローログの分析](../../../../services/network-connectivity.md#flow-log-analysis): 対象ごとのログを確認します。
2. [ルーティング](../../../../services/network-connectivity.md#nfw-routing): ファイアウォールのログの設定を押さえます。
3. [Route Analyzer](../../../../services/network-connectivity.md#route-analyzer): Global Networks の使い方を確認します。

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| IKE と DPD の調査 | VPN のトンネルログ |
| アタッチメントの間の通信 | Transit Gateway フローログ |
| 全アカウントのフローログの集約 | ログ用アカウントの S3 |

## 引っかかりやすい点 {#traps}

- Network Firewall のアラートはログを設定しないと見えません。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [cloudwatch 問13](../../exercises/cloudwatch.md#q13) | 監視とログ | VPN のトンネルが不安定で、IKE の交渉と DPD の動きを詳しく調べたいと考えています。CGW… |
| [cloudwatch 問14](../../exercises/cloudwatch.md#q14) | 監視とログ | 在宅の利用者と本社の DX の両方を監視します。VPN の接続の履歴と物理の接続の状態を確認します。… |
| [cloudwatch 問15](../../exercises/cloudwatch.md#q15) | 監視とログ | オンプレミスと VPC の間の通信で、どのアタッチメントを通ったかを記録します。VPC の中のログを… |
| [cloudwatch 問16](../../exercises/cloudwatch.md#q16) | 監視とログ | 300 のアカウントのフローログをログ用アカウントへ集め、長期保存します。各アカウントの管理者には変… |
| [cloudwatch 問17](../../exercises/cloudwatch.md#q17) | 監視とログ | Network Firewall でドメインの拒否を設定しました。通信は止まっていますが、どのルール… |
| [cloudwatch 問18](../../exercises/cloudwatch.md#q18) | 監視とログ | マルチリージョンの Transit Gateway で、トポロジーとルートの変更をネットワークチーム… |

<!-- questions:end -->

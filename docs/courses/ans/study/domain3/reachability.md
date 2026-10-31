# 分野3: 到達性の検証とトポロジー

監視と分析のうち、経路とトポロジー、設定の誤りの切り分けを問います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [経路の分析](../../domain3.md#t3-2-routing-tools) | 経路の分析ツール（Reachability Analyzer、Network Manager） |
| [トポロジー](../../domain3.md#t3-2-topology) | トポロジーの把握 |
| [設定の誤り](../../domain3.md#t3-2-misconfig) | 設定の誤りによる接続の問題の切り分け |
| [検証と自動化](../../domain3.md#t3-2-verify) | 設計要件を満たすかの検証、接続の意図の検証の自動化 |

## 学習の順番 {#study-order}

1. [接続の調査](../../../../services/network-connectivity.md#network-analysis): ツールの質問の違いを確認します。
2. [Reachability Analyzer](../../../../services/network-connectivity.md#reachability-analyzer): 制約と自動化を押さえます。
3. [Network Access Analyzer](../../../../services/network-connectivity.md#network-access-analyzer): 要件の検証を確認します。
4. [接続できないときの切り分け](../../../../services/networking.md#vpc-troubleshooting): 切り分けの流れを覚えます。

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 到達可能なのに接続できない | OS とアプリ |
| 大きなパケットだけ失敗 | MTU |
| 変更のたびに確認 | `AWS::EC2::NetworkInsightsPath`、EventBridge、分析の実行 |

## 引っかかりやすい点 {#traps}

- Transit Gateway の TCP は行きだけ解析します。
- IPv4 のみで、同じリージョンが対象です。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [reachability 問13](../../exercises/reachability.md#q13) | 経路の分析 | 運用チームが次の 3 つの質問に答えます。質問 1: A から B へ届くか、何が止めているか。質問… |
| [reachability 問14](../../exercises/reachability.md#q14) | 経路の分析 | オンプレミスの一部の拠点へ通信できなくなりました。BGP の経路が消えたのか、Transit Gat… |
| [reachability 問15](../../exercises/reachability.md#q15) | 経路の分析 | VPC A から VPC B へ Transit Gateway を経由する TCP の通信で、Re… |
| [reachability 問16](../../exercises/reachability.md#q16) | トポロジー | 大規模な障害で、影響を受けた拠点を素早く把握します。拠点は数十か所あり、Transit Gatewa… |
| [reachability 問17](../../exercises/reachability.md#q17) | トポロジー | ネットワークチームは、トポロジーの把握と Transit Gateway の経路の解析を 1 か所で… |
| [reachability 問18](../../exercises/reachability.md#q18) | トポロジー | オンプレミスの拠点とリンクをトポロジーに追加し、Transit Gateway との関係を図で見ます… |
| [reachability 問19](../../exercises/reachability.md#q19) | 設定の誤り | Reachability Analyzer で到達不能と表示され、止めている部品として NACL が… |
| [reachability 問20](../../exercises/reachability.md#q20) | 設定の誤り | Reachability Analyzer は到達可能で、フローログにも REJECT はありません… |
| [reachability 問21](../../exercises/reachability.md#q21) | 設定の誤り | ピアリングした 2 つの VPC の間で、片方向の通信だけが失敗します。ピアリングは active … |
| [reachability 問22](../../exercises/reachability.md#q22) | 検証と自動化 | ネットワークの変更のたびに、接続の意図を自動で確認します。確認する経路はコードで管理します。パケット… |
| [reachability 問23](../../exercises/reachability.md#q23) | 検証と自動化 | 設計要件は「IGW への経路には必ずファイアウォールがある」ことです。全 VPC について要件を満た… |
| [reachability 問24](../../exercises/reachability.md#q24) | 検証と自動化 | 自動の分析の結果が期待と違ったときの動作を組みます。結果を運用チームへ伝え、必要なら変更を戻します。… |

<!-- questions:end -->

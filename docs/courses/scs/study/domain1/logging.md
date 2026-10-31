# 分野1: ログの仕組み

何を知りたいかでログを選び、検索の頻度と保持期間で保存先を決め、ソースをまたいで分析する判断を問います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [1.2.1](../../domain1.md#skill-1-2-1) | ログの取り込み元と保存先の選択 |
| [1.2.2](../../domain1.md#skill-1-2-2) | サービスとアプリケーションのログの設定 |
| [1.2.3](../../domain1.md#skill-1-2-3) | ログの保管、データレイク、他社ツールとの統合 |
| [1.2.4](../../domain1.md#skill-1-2-4) | ログの分析 |
| [1.2.5](../../domain1.md#skill-1-2-5) | ログの正規化、解析、関連付け |
| [1.2.6](../../domain1.md#skill-1-2-6) | ネットワーク設計と脅威に合うログの選択 |

## 学習の順番 {#study-order}

1. [どのログを見るか](../../../../services/threat-detection.md#log-sources): 知りたいこととログの対応を表で覚えます。
2. [証跡](../../../../services/observability.md#cloudtrail-trails)と[イベントの種類](../../../../services/observability.md#cloudtrail-events): 組織の証跡、データイベント、ログファイルの検証を押さえます。
3. [ログの保持](../../../../services/observability.md#log-retention)と[ログクラス](../../../../services/observability.md#log-classes): 既定の無期限と、Essentials で使えない機能を確認します。
4. [サブスクリプションフィルターの設定](../../../../services/observability.md#subscription-settings): クロスアカウントの宛先と、リージョンの制約を理解します。
5. [CloudWatch エージェント](../../../../services/operations.md#cloudwatch-agent): OS のログとメモリの収集、Parameter Store での設定の共有を確認します。
6. [Security Lake](../../../../services/threat-detection.md#security-lake): OCSF、ロールアップリージョン、2 種類のサブスクライバー、カスタムソースの条件を押さえます。
7. [Logs Insights](../../../../services/observability.md#logs-insights)と [Athena のパーティション](../../../../services/streaming.md#athena-partitions): ログの場所で検索のツールを選び、走査量を減らす方法を確認します。
8. [OpenSearch Service](../../../../services/databases.md#opensearch)と [Managed Grafana](../../../../services/operations.md#managed-grafana): データを保管するものと、可視化するものを区別します。
9. [VPC フローログ](../../../../services/networking.md#flow-logs)と[フローログの分析](../../../../services/network-connectivity.md#flow-log-analysis): 残らない通信と、作成後に形式を変えられないことを覚えます。
10. [Route 53 Resolver](../../../../services/network-connectivity.md#route53-resolver)、[Network Firewall のログ](../../../../services/threat-detection.md#nfw-logging)、[Traffic Mirroring](../../../../services/network-connectivity.md#traffic-mirroring): ログごとに残らないものを確認します。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| CloudWatch Logs の既定の保持 | 無期限 | 保持期間を決めないと費用が増え続ける |
| 保持期間の超過後の削除 | 通常 72 時間以内 | すぐには消えない |
| Event history | 直近 90 日の管理イベント | データイベントはなく、長期は証跡 |
| CloudTrail の配信 | 平均約 5 分 | 保証された時間ではない |
| ダイジェストファイル | 1 時間ごと | 確認は `validate-logs` |
| フローログの集約間隔 | 既定 10 分。1 分も可 | 調査の粒度に合わせる |
| フローログの配信の目安 | CloudWatch Logs は約 5 分、S3 は約 10 分 | 遅延を考慮する |
| Security Lake のカスタムソース | Parquet、1 オブジェクトに 1 OCSF クラス | 送信側で変換する |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 数年の保管と改ざん防止、検索はまれ | S3、ライフサイクル、Object Lock |
| メトリクスフィルターが必要なログの費用を下げたい | Essentials は使えない。Standard のまま保持期間を見直す |
| 全アカウントの API をログ保管アカウントへ集める | 組織の証跡 |
| 特定のバケットのオブジェクトの操作を記録する | 高度なイベントセレクターで S3 データイベント |
| 全アカウントのログをほぼリアルタイムで集める | 論理的な宛先とサブスクリプションフィルター |
| 共通の形式で他社 SIEM へ渡す | Security Lake とロールアップリージョン、データアクセスのサブスクライバー |
| データを複製せず検索させる | クエリアクセスのサブスクライバー |
| CloudWatch Logs のログを対話的に集計する | Logs Insights |
| S3 のログを SQL で検索する | Athena とパーティション射影 |
| 全文検索とダッシュボードが必要 | OpenSearch Service |
| 既存のデータを複製せず可視化する | Managed Grafana |
| DNS トンネリングを調べる | Route 53 Resolver クエリログ |
| NAT の裏の元の IP を調べる | カスタム形式の `pkt-srcaddr`。フローログは作り直す |
| Transit Gateway の中で消えるパケットを調べる | Transit Gateway フローログ |
| ペイロードを外部の IDS で検査する | Traffic Mirroring |

## 引っかかりやすい点 {#traps}

- データイベントは既定で記録されません。S3 のオブジェクトの操作や Lambda の呼び出しは別途有効にします。
- ログファイルの検証は変更を検出するもので、防ぐものではありません。有効にしても自動では確認されません。
- ロググループと論理的な宛先は同じリージョンに置きます。宛先の先のリソースは別のリージョンでも構いません。
- サブスクライバーは作成したリージョンのデータだけを見られます。複数のリージョンを渡すならロールアップリージョンで作ります。
- Security Lake のソースは別途の設定が不要です。例外は CloudTrail の管理イベントです。
- サブスクリプションフィルターのデータは Base64 と gzip です。Lambda で元に戻してから読みます。
- Amazon DNS への通信とメタデータへの通信は、フローログに残りません。
- Resolver クエリログは、キャッシュから応答した問い合わせと、自前の DNS への問い合わせを記録しません。
- Network Firewall のログはステートフルエンジンに転送された通信だけが対象です。ステートレスの Drop は残りません。
- Managed Grafana に IAM ユーザーで直接ログインはできません。SAML か IAM Identity Center を使います。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [logging 問1](../../exercises/logging.md#q1) | 1.2.1 | ある金融機関は、監査のために API の記録を 7 年間保持し、保持期間中は誰にも消されないようにす… |
| [logging 問2](../../exercises/logging.md#q2) | 1.2.1 | ある企業は CloudWatch Logs の費用を下げるため、2 種類のログの保存先を見直していま… |
| [logging 問3](../../exercises/logging.md#q3) | 1.2.1 | 大量の VPC フローログを 3 年間保管します。月に数回、特定の期間だけを SQL で調べます。既… |
| [logging 問4](../../exercises/logging.md#q4) | 1.2.1 | CloudWatch Logs の費用が毎月増えています。調べると、作成時に何も指定していないロググ… |
| [logging 問5](../../exercises/logging.md#q5) | 1.2.2 | 組織の全アカウントの API を記録し、ログ保管アカウントの S3 に集めます。個別のメンバーアカウ… |
| [logging 問6](../../exercises/logging.md#q6) | 1.2.2 | 機密データのバケットは 2 つだけで、読み取りと削除の操作を記録する必要があります。組織の証跡はあり… |
| [logging 問7](../../exercises/logging.md#q7) | 1.2.2 | 30 のアカウントのアプリのロググループを、ログ専用アカウントへほぼリアルタイムで集めます。送信元の… |
| [logging 問8](../../exercises/logging.md#q8) | 1.2.2 | 東京のロググループのログを、別のアカウントのバージニア北部にある Firehose へ送りたいと考え… |
| [logging 問9](../../exercises/logging.md#q9) | 1.2.2 | 数百台の EC2 の OS ログとメモリの使用率を CloudWatch に集め、設定を全台で同じに… |
| [logging 問10](../../exercises/logging.md#q10) | 1.2.2 | 調査のために、CloudTrail のログが配信後に変更されていないことを示す必要があります。担当者… |
| [logging 問11](../../exercises/logging.md#q11) | 1.2.3 | 複数のアカウントと 4 つのリージョンの CloudTrail、VPC フローログ、WAF ログを、… |
| [logging 問12](../../exercises/logging.md#q12) | 1.2.3 | 外部の調査会社に、Security Lake のログを一定期間だけ分析してもらいます。データを複製し… |
| [logging 問13](../../exercises/logging.md#q13) | 1.2.3 | オンプレミスのファイアウォールのログを Security Lake に取り込みます。カスタムソースを… |
| [logging 問14](../../exercises/logging.md#q14) | 1.2.3 | すでに VPC フローログを S3 に出力しています。Security Lake を導入するとき、フ… |
| [logging 問15](../../exercises/logging.md#q15) | 1.2.4 | VPC フローログを CloudWatch Logs に配信しています。直近 1 時間に拒否された通… |
| [logging 問16](../../exercises/logging.md#q16) | 1.2.4 | Athena で組織の CloudTrail を検索していますが、クエリの走査量と費用が大きく、日付… |
| [logging 問17](../../exercises/logging.md#q17) | 1.2.4 | 漏えいしたアクセスキーの ID が判明しました。4 か月前まで遡って、そのキーによる管理操作とデータ… |
| [logging 問18](../../exercises/logging.md#q18) | 1.2.4 | WAF のログは S3 に 5 分ごとに出力しています。過去 30 日で最も多く通信を拒否したルール… |
| [logging 問19](../../exercises/logging.md#q19) | 1.2.5 | アプリのログをサブスクリプションフィルターで Lambda に送り、機密の項目を除いて整形してから、… |
| [logging 問20](../../exercises/logging.md#q20) | 1.2.5 | SOC は、異なる形式のアプリのログと監査ログを 1 か所に入れて全文検索し、不審な文字列を手がかり… |
| [logging 問21](../../exercises/logging.md#q21) | 1.2.5 | CloudWatch と OpenSearch Service のデータをまとめて可視化するため、M… |
| [logging 問22](../../exercises/logging.md#q22) | 1.2.5 | CloudTrail、Route 53 Resolver クエリログ、VPC フローログをまたいで、… |
| [logging 問23](../../exercises/logging.md#q23) | 1.2.6 | あるインスタンスから DNS トンネリングで情報を持ち出している疑いがあります。インスタンスは VP… |
| [logging 問24](../../exercises/logging.md#q24) | 1.2.6 | Resolver クエリログを VPC で有効にしています。同じインスタンスが短時間に同じドメインを… |
| [logging 問25](../../exercises/logging.md#q25) | 1.2.6 | NAT Gateway の裏のインスタンスからの通信を調べています。既定の形式のフローログでは、NA… |
| [logging 問26](../../exercises/logging.md#q26) | 1.2.6 | ハブアンドスポークの Transit Gateway に 30 の VPC を接続しています。特定の… |
| [logging 問27](../../exercises/logging.md#q27) | 1.2.6 | Network Firewall でステートフルのドメインルールを使って通信を拒否しています。アラー… |
| [logging 問28](../../exercises/logging.md#q28) | 1.2.6 | あるサーバーへの通信で、ペイロードの内容を外部の IDS で検査したいと考えています。インスタンスに… |

<!-- questions:end -->

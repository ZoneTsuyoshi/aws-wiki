# 分野3: 監視とトラブルシューティング

監査と追跡のログ、通知、性能問題の切り分け、ログの分析を問います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [3.3.1](../../domain3.md#skill-3-3-1) | 監査のためのログの抽出 |
| [3.3.2](../../domain3.md#skill-3-3-2) | 監査と追跡のためのログと監視 |
| [3.3.3](../../domain3.md#skill-3-3-3) | 監視からの通知 |
| [3.3.4](../../domain3.md#skill-3-3-4) | 性能問題のトラブルシューティング |
| [3.3.5](../../domain3.md#skill-3-3-5) | CloudTrail による API の追跡 |
| [3.3.7](../../domain3.md#skill-3-3-7) | CloudWatch Logs によるアプリケーションログ |
| [3.3.8](../../domain3.md#skill-3-3-8) | AWS サービスによるログの分析 |

## 学習の順番 {#study-order}

1. [イベントの種類](../../../../services/observability.md#cloudtrail-events): 管理、データ、Insights を区別します。
2. [証跡とイベント履歴](../../../../services/observability.md#cloudtrail-trails): 長期の保存を確認します。
3. [Config と CloudTrail の違い](../../../../services/governance.md#config-vs-cloudtrail): 問いで分けます。
4. [メトリクスフィルター](../../../../services/observability.md#metric-filters): ログからアラームまでの流れを覚えます。
5. [欠落データの扱い](../../../../services/observability.md#treat-missing-data): 死活の監視の設定を確認します。
6. [Logs Insights](../../../../services/observability.md#logs-insights): その場の検索を確認します。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| イベント履歴 | 90 日 | 管理イベント |
| CloudTrail の配信の遅れ | 平均で約 5 分 | 即時の反応は EventBridge |
| ロググループの保持の既定 | 無期限 | 費用のために設定する |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 誰がいつどの API を呼んだか | CloudTrail |
| 設定はどう変わったか | Config |
| S3 のオブジェクトの操作の記録 | データイベントを有効にする |
| データが来ないことを検知する | `breaching` |
| Kinesis の消費が遅れる | `IteratorAge` を確認し、並列度を上げる |
| Redshift の実行前の待ち | `total_queue_time` を確認し、キューを見直す |

## 引っかかりやすい点 {#traps}

- データイベントを後から有効にしても、過去の分は残りません。
- ログクラスは作成時に選び、後から変更できません。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [monitoring 問1](../../exercises/monitoring.md#q1) | 3.3.1 | 監査のため、今後の API の記録を 1 年以上残し、SQL で検索できるようにします。まだ何も設定… |
| [monitoring 問2](../../exercises/monitoring.md#q2) | 3.3.1 | Redshift の監査で、誰が接続し、どんな SQL を実行したかを記録します。何を有効にしますか… |
| [monitoring 問3](../../exercises/monitoring.md#q3) | 3.3.1 | ログの取り出し方で正しいものはどれですか。（2つ選択） |
| [monitoring 問4](../../exercises/monitoring.md#q4) | 3.3.2 | 次の問いとサービスの組み合わせで正しいものはどれですか。 |
| [monitoring 問5](../../exercises/monitoring.md#q5) | 3.3.2 | 監査ログの改ざんと削除を検出できるようにし、ログ自体を守ります。どの組み合わせですか。 |
| [monitoring 問6](../../exercises/monitoring.md#q6) | 3.3.2 | 全アカウントのパイプライン関連の操作と設定の変更を追跡します。組み合わせとして適切なものはどれですか… |
| [monitoring 問7](../../exercises/monitoring.md#q7) | 3.3.3 | アプリのログに ERROR が 5 分で 10 回出たら通知します。どの構成ですか。 |
| [monitoring 問8](../../exercises/monitoring.md#q8) | 3.3.3 | 毎時のバッチが出すメトリクスで、データが来ないこと自体を障害として検知します。アラームの欠落データの… |
| [monitoring 問9](../../exercises/monitoring.md#q9) | 3.3.3 | 通知の対象と方法の組み合わせで正しいものはどれですか。 |
| [monitoring 問10](../../exercises/monitoring.md#q10) | 3.3.4 | Kinesis の Lambda で IteratorAge が増え続けています。消費が遅れています… |
| [monitoring 問11](../../exercises/monitoring.md#q11) | 3.3.4 | Redshift のクエリが遅いという報告があります。stl_wlm_query の total_q… |
| [monitoring 問12](../../exercises/monitoring.md#q12) | 3.3.4 | Firehose の配信が遅く、S3 に 15 分遅れで届きます。バッファの条件の説明として正しいも… |
| [monitoring 問13](../../exercises/monitoring.md#q13) | 3.3.5 | S3 のオブジェクトを誰が削除したかを調べると、CloudTrail に記録がありません。既定の設定… |
| [monitoring 問14](../../exercises/monitoring.md#q14) | 3.3.5 | API のエラーの率が普段より急に上がったことを検知します。CloudTrail のどのイベントです… |
| [monitoring 問15](../../exercises/monitoring.md#q15) | 3.3.5 | CloudTrail の S3 への配信の遅れを踏まえ、特定の API の呼び出しに素早く反応します… |
| [monitoring 問16](../../exercises/monitoring.md#q16) | 3.3.7 | CloudWatch Logs の費用が増え続けています。ロググループの設定は既定のままです。まず何… |
| [monitoring 問17](../../exercises/monitoring.md#q17) | 3.3.7 | EC2 上の ETL のログを CloudWatch Logs へ送り、OpenSearch へリア… |
| [monitoring 問18](../../exercises/monitoring.md#q18) | 3.3.7 | ログの自動化の説明で正しいものはどれですか。（2つ選択） |
| [monitoring 問19](../../exercises/monitoring.md#q19) | 3.3.8 | CloudWatch Logs のエラーを、5 分ごとの件数でその場で調べます。追加の構築はしません… |
| [monitoring 問20](../../exercises/monitoring.md#q20) | 3.3.8 | S3 に数か月分ある ALB のアクセスログを SQL で分析します。最も適切なものはどれですか。 |
| [monitoring 問21](../../exercises/monitoring.md#q21) | 3.3.8 | 要件とツールの組み合わせで正しいものはどれですか。（2つ選択） |

<!-- questions:end -->

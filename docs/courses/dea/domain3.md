# 分野3: データの運用とサポート

配点は **22%** です。パイプラインを自動化し、データを分析し、監視とトラブルシューティングを行い、データの品質を保ちます。

Athena の使い方、CloudWatch と CloudTrail の使い分け、Glue Data Quality と DataBrew の使い分けがよく問われます。

この分野に限らず、コース全体で使うサービスは[サービス一覧](services.md)から確認できます。

## タスク 3.1: AWS サービスでデータ処理を自動化する {#task-3-1}

### 3.1.1 パイプラインの連結（MWAA、Step Functions） {#skill-3-1-1}

| 観点 | MWAA | Step Functions |
|---|---|---|
| 定義 | Python の DAG。S3 の `dags/` に置く | ASL（JSON） |
| 向く場面 | 既存の Airflow、複雑な依存、AWS 外との連携 | AWS で完結する処理 |
| 課金 | 環境の料金（Serverless は処理時間） | 状態遷移の数（Standard） |
| AWS との連携 | プロバイダーのオペレーター | 200 以上のサービスと統合 |

MWAA では環境クラスで規模を選びます。`mw1.small` は DAG 50 個が目安で、同時タスクの既定は5です。依存パッケージは `requirements.txt` に書きます。

詳細: [MWAA](../../services/data-engineering.md#mwaa)、[オーケストレーションの比較](../../services/data-engineering.md#orchestration)、[Step Functions の統合パターン](../../services/step-functions.md#integration-patterns)

### 3.1.2 マネージドワークフローのトラブルシューティング {#skill-3-1-2}

| 症状 | 原因の候補 | 対処 |
|---|---|---|
| MWAA で DAG がインポートエラー | `requirements.txt` の依存が解決できない | CloudWatch Logs を確認する |
| MWAA で PyPI に届かない | インターネットへの経路がない VPC | 依存を `plugins.zip` に同梱する |
| MWAA でタスクが詰まる | 環境クラスが小さい、ワーカーの最大数が低い | 環境クラスと最大ワーカー数を見直す |
| Step Functions が未完了のまま次へ進む | `.sync` がない | 統合パターンを直す |
| Step Functions が失敗で止まる | `Retry` と `Catch` がない | エラー名で再試行、分岐する |
| 途中で失敗した実行をやり直したい | | `redrive` で失敗した地点から再開する |

Step Functions の Standard は、実行履歴を API で取得できます。Express は CloudWatch Logs を有効にして確認します。

詳細: [MWAA](../../services/data-engineering.md#mwaa)、[エラー処理](../../services/step-functions.md#error-handling)、[主なエラー名](../../services/step-functions.md#error-names)、[再実行とログ](../../services/step-functions.md#redrive-logging)

### 3.1.3 SDK からの AWS 機能の呼び出し {#skill-3-1-3}

パイプラインの処理をコードから起動します。多くのデータ系の API は非同期です。

```python
import boto3

athena = boto3.client("athena")
qid = athena.start_query_execution(
    QueryString="SELECT status, COUNT(*) FROM alb_logs GROUP BY status",
    QueryExecutionContext={"Database": "logs"},
    WorkGroup="etl",
)["QueryExecutionId"]
# 完了を確認してから get_query_results を呼ぶ
```

| 目的 | 使うもの |
|---|---|
| Glue ジョブを起動する | `start_job_run` |
| Athena の完了を待つ | `get_query_execution` で状態を確認する |
| Redshift に SQL を送る | Redshift Data API の `execute_statement` |
| 一覧を全件取得する | ページネーター |
| 一時的な失敗に耐える | SDK の再試行モード |

認証情報はコードに書かず、IAM ロールから取得します。

詳細: [AWS SDK の基本](../../services/sdk-resilience.md#sdk-basics)、[ページネーション](../../services/sdk-resilience.md#pagination)、[ウェイター](../../services/sdk-resilience.md#waiters)、[再試行モード](../../services/sdk-resilience.md#retry-modes)、[Athena](../../services/streaming.md#athena)

### 3.1.4 サービスの機能を使ったデータ処理 {#skill-3-1-4}

| サービス | 機能 | 使いどころ |
|---|---|---|
| Glue | ETL ジョブ、ブックマーク、Data Quality | サーバーレスの変換 |
| EMR | ステップ、マネージドスケーリング、自動終了 | ジョブごとにクラスターを起動して終了する |
| Redshift | マテリアライズドビュー、ストリーミング取り込み | DWH の中で計算する |
| Redshift | WLM、SQA、同時実行スケーリング | ETL と BI のワークロードを分ける |

一時クラスターの EMR では、データを S3 に置き、ジョブの完了後にクラスターを終了します。費用はジョブの時間分だけです。

詳細: [Glue](../../services/data-engineering.md#glue)、[EMR のスケーリングと終了](../../services/data-engineering.md#emr-scaling)、[ワークロード管理](../../services/data-engineering.md#redshift-wlm)、[マテリアライズドビュー](../../services/data-engineering.md#redshift-materialized-views)

### 3.1.5 データ API の利用と保守 {#skill-3-1-5}

API を作った後の運用です。

| 課題 | 方法 |
|---|---|
| 過負荷を防ぐ | 使用量プランと API キー、スロットリング |
| 同じ問い合わせの費用を下げる | API Gateway のキャッシュ |
| 変更を安全に出す | ステージ、カナリアリリース |
| 不正な入力を止める | リクエストの検証 |
| 状況を見る | `4XXError`、`5XXError`、`Latency` のメトリクスとアクセスログ |
| 呼び出し元のエラー | 429 はスロットリング、504 は統合のタイムアウト |

Redshift Data API を呼ぶ側では、結果は24時間で消えます。`ThrottlingException` は SDK の再試行で扱います。Step Functions から呼ぶときは、再試行で重複しないように `ClientToken` を渡します。トークンは8時間有効です。

詳細: [使用量プラン](../../services/api-gateway.md#usage-plans)、[ステージ](../../services/api-gateway.md#stages)、[カナリアリリース](../../services/api-gateway.md#canary)、[ログとメトリクス](../../services/api-gateway.md#logging-metrics)、[エラーコード](../../services/api-gateway.md#errors)

### 3.1.6 変換の前のデータの準備 {#skill-3-1-6}

| ツール | 位置づけ | 向く場面 |
|---|---|---|
| DataBrew | 単独の視覚的な整形ツール。250種類以上の変換 | アナリストがコードなしで整形する |
| SageMaker Unified Studio | データ、分析、ML の統合環境。プロジェクト単位 | 同じ場所でデータ準備から分析、ML まで進める |
| Glue ETL | コードの本番変換 | データエンジニアの大規模処理 |

DataBrew では、プロジェクトで試し、レシピとして保存し、レシピジョブで全データに適用します。

詳細: [DataBrew](../../services/data-engineering.md#databrew)、[DataZone と Unified Studio](../../services/data-engineering.md#datazone-unified-studio)、[Unified Studio の位置づけ](../../services/sagemaker.md#unified-studio)

### 3.1.7 データのクエリ（Athena） {#skill-3-1-7}

S3 のデータに標準 SQL で問い合わせるサーバーレスのサービスです。スキャン量で課金されます。

| 目的 | 方法 |
|---|---|
| 費用と時間を減らす | Parquet、パーティション、必要な列だけ選ぶ |
| 同じクエリを安くする | クエリ結果の再利用 |
| 使いすぎを防ぐ | ワークグループのクエリごとの制限。超えるとキャンセルされる |
| 形式を変換する | CTAS |
| 結果の場所を強制する | ワークグループの「クライアント側の設定を上書き」 |
| 同時実行の上限 | 超えると `TooManyRequestsException` |

詳細: [Athena](../../services/streaming.md#athena)、[速く、安くするコツ](../../services/streaming.md#athena-performance)、[形式と料金](../../services/streaming.md#athena-formats-cost)、[ワークグループ](../../services/streaming.md#athena-workgroups)

### 3.1.8 Lambda によるデータ処理の自動化 {#skill-3-1-8}

| 起動元 | 処理の例 |
|---|---|
| S3 イベント | 届いたファイルの検証、Glue ジョブの起動 |
| Kinesis、DynamoDB Streams | レコードの変換、書き込み |
| Firehose | 配信前のレコードの変換 |
| EventBridge Scheduler | 定期的な API の取得、パーティションの追加 |
| Step Functions | パイプラインの1ステップ |

制限は15分、`/tmp` は最大 10,240 MB、メモリは最大 10,240 MB です。大きなデータの変換は Glue や EMR に任せ、Lambda は起動と小さな変換に使います。

詳細: [呼び出しの種類](../../services/lambda.md#invocation-types)、[ほぼリアルタイムの処理](../../services/lambda.md#near-real-time)、[Firehose の変換](../../services/streaming.md#firehose-transform)

### 3.1.9 イベントとスケジューラーの管理 {#skill-3-1-9}

| 機能 | 内容 |
|---|---|
| ルール | イベントパターンでターゲットへ振り分ける |
| Scheduler | cron、rate、1回のみ。タイムゾーンと柔軟な時間枠を指定できる |
| 再試行と DLQ | ターゲットへの配信に失敗したときの扱い |
| 入力トランスフォーマー | ターゲットに渡す内容を変える |
| アーカイブとリプレイ | イベントを保存して再送する |
| Pipes | SQS、Kinesis などのソースとターゲットをつなぐ |

例として、Glue のジョブの状態変更をルールで受け、失敗のときだけ SNS に送ります。

詳細: [EventBridge](../../services/messaging.md#eventbridge)、[ルール](../../services/messaging.md#eventbridge-rules)、[スケジュール](../../services/messaging.md#eventbridge-schedule)、[ターゲットの再試行と DLQ](../../services/messaging.md#target-retry-dlq)、[Pipes](../../services/messaging.md#eventbridge-pipes)

## タスク 3.2: AWS サービスでデータを分析する {#task-3-2}

### 3.2.1 データの可視化 {#skill-3-2-1}

| ツール | 見るもの | 向く場面 |
|---|---|---|
| DataBrew | 分布、欠損、相関（プロファイル） | 変換の前にデータを理解する |
| Quick Sight | ダッシュボード | 業務の利用者に見せる |
| Managed Grafana | メトリクスとログ | 運用の監視 |

Quick Sight のデータの読み方です。

| 方式 | 動作 | 向く場面 |
|---|---|---|
| SPICE | インメモリへ取り込む | 速さ、Athena の費用を抑える |
| 直接クエリ | 表示のたびに問い合わせる | 最新のデータが必須 |

更新したのに古いなら、SPICE の更新スケジュールを確認します。容量が足りないと取り込みが失敗します。

詳細: [Quick Sight](../../services/data-engineering.md#quick-sight)、[DataBrew](../../services/data-engineering.md#databrew)、[Managed Grafana](../../services/operations.md#managed-grafana)

### 3.2.2 データの検証とクリーニング {#skill-3-2-2}

| ツール | 向く場面 |
|---|---|
| Lambda | 届いたファイルの簡単な検証 |
| Athena | SQL で欠損や重複を調べる。`COUNT(*)` と `COUNT(col)` の差など |
| Quick Sight | グラフで外れ値を見つける |
| Jupyter ノートブック | 対話的に調べて試す |
| SageMaker Data Wrangler | ML の前処理を画面で試す |

!!! note "Data Wrangler の現在の形"
    Data Wrangler は SageMaker Canvas に統合され、自然言語でも変換できます。

詳細: [Data Wrangler](../../services/sagemaker.md#data-wrangler)、[Athena](../../services/streaming.md#athena)、[DataBrew](../../services/data-engineering.md#databrew)

### 3.2.3 Redshift と Athena の SQL とビュー {#skill-3-2-3}

| 操作 | Athena | Redshift |
|---|---|---|
| ビュー | `CREATE VIEW` | `CREATE VIEW` |
| 結果を保存 | CTAS（S3 に書く） | `CREATE TABLE AS`、マテリアライズドビュー |
| 外部のデータ | S3 のテーブル | Spectrum の外部スキーマ |

ビューは毎回元のデータを読むので、速くはなりません。結果を保存して速くするのがマテリアライズドビューです。

```sql
CREATE VIEW daily_sales AS
SELECT sold_at::date AS day, region, SUM(amount) AS total
FROM sales
GROUP BY 1, 2;
```

Athena の `SELECT` は `GROUPING SETS`、`CUBE`、`ROLLUP` にも対応します。

詳細: [マテリアライズドビュー](../../services/data-engineering.md#redshift-materialized-views)、[形式の変換](../../services/data-engineering.md#data-formats)、[S3 上のログを問い合わせる](../../services/streaming.md#athena-logs)

### 3.2.4 Athena の Spark ノートブック {#skill-3-2-4}

Athena では SQL のほかに、Apache Spark をサーバーレスで実行できます。クラスターの計画や管理は要りません。指定した上限まで、計算資源が自動で増減します。

| エンジン | 実行の場所 |
|---|---|
| PySpark エンジン バージョン 3 | Athena コンソールのノートブック。Jupyter 互換で、セルを順に実行する |
| Apache Spark バージョン 3.5 | SageMaker Unified Studio のノートブック、Spark Connect 対応のクライアント |

コンソールから Spark アプリケーションを送れるのは、PySpark エンジン バージョン 3 だけです。

| 比較 | 向く場面 |
|---|---|
| Athena の SQL | SQL で書ける分析 |
| Athena の Spark | Python で対話的に探索する |
| Glue、EMR | 本番の定期的な ETL |

詳細: [Athena](../../services/streaming.md#athena)

### 3.2.5 プロビジョンドとサーバーレスのトレードオフ {#skill-3-2-5}

| 観点 | プロビジョンド | サーバーレス |
|---|---|---|
| 費用 | 常に課金。高い稼働率で安くなる | 使った分。断続的な利用で安い |
| 性能の調整 | 細かくできる | 限られる |
| 運用 | 容量の管理が必要 | 少ない |
| 予測のしやすさ | 費用が一定 | 負荷に応じて変わる。上限を設定する |
| 開始の速さ | 常に起動済み | 起動の遅れがありうる |

| サービス | プロビジョンド | サーバーレス | 判断の例 |
|---|---|---|---|
| Redshift | クラスター | Serverless（RPU） | 断続的なら Serverless、常に負荷があり予約で安くしたいなら Provisioned |
| EMR | on EC2 | EMR Serverless | 細かな調整や Spot の活用なら on EC2 |
| MSK | Provisioned | Serverless | 既存の設定を持ち込むなら Provisioned。Serverless は IAM 認証のみ |
| Kinesis | プロビジョンド | オンデマンド | 負荷が読めないならオンデマンド |
| Aurora | インスタンス | Serverless v2 | 負荷の変動が大きいなら v2 |
| DynamoDB | プロビジョンド | オンデマンド | 読めないならオンデマンド |

詳細: [Redshift Serverless](../../services/data-engineering.md#redshift-serverless)、[EMR Serverless](../../services/data-engineering.md#emr-serverless)、[Kinesis のキャパシティモード](../../services/streaming.md#capacity-modes)、[Aurora Serverless v2](../../services/databases.md#aurora-serverless-v2)、[DynamoDB のキャパシティ](../../services/dynamodb.md#capacity)

### 3.2.6 集計、移動平均、グループ化、ピボット {#skill-3-2-6}

| 用語 | 意味 | SQL |
|---|---|---|
| 集計 | 複数の行を1つの値にまとめる | `SUM`、`AVG`、`COUNT` |
| グループ化 | キーごとに分けて集計する | `GROUP BY`、`HAVING` で絞る |
| 移動平均 | 直近の一定の範囲で平均する。短期の変動をならす | ウィンドウ関数 |
| ピボット | 行の値を列に変える | Redshift の `PIVOT`、または `CASE` の集計 |

```sql
-- 直近7日の移動平均
SELECT day, total,
       AVG(total) OVER (ORDER BY day ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) AS avg_7d
FROM daily_sales;

-- Redshift の PIVOT
SELECT *
FROM (SELECT partname, price FROM part)
PIVOT (AVG(price) FOR partname IN ('prop', 'rudder', 'wing'));

-- CASE で列に分ける
SELECT region,
       SUM(CASE WHEN quarter = 'Q1' THEN amount END) AS q1,
       SUM(CASE WHEN quarter = 'Q2' THEN amount END) AS q2
FROM sales
GROUP BY region;
```

Redshift には `UNPIVOT` もあり、列を行に戻せます。`PIVOT` の集計は `COUNT`、`SUM`、`MIN`、`MAX`、`AVG` に対応します。

詳細: [S3 上のログを問い合わせる](../../services/streaming.md#athena-logs)、[Redshift](../../services/data-engineering.md#redshift)

## タスク 3.3: パイプラインを保守して監視する {#task-3-3}

### 3.3.1 監査のためのログの抽出 {#skill-3-3-1}

| ログ | 取り出し方 |
|---|---|
| CloudTrail | 証跡で S3 へ出力し、Athena で検索する |
| CloudWatch Logs | S3 へエクスポート、サブスクリプションフィルターで転送 |
| Redshift の監査ログ | 接続ログ、ユーザーログ、ユーザーアクティビティログを S3 か CloudWatch へ |
| S3 のアクセス | CloudTrail のデータイベント |
| EMR | クラスターのログを S3 へ。終了後も調査できる |

詳細: [証跡とイベント履歴](../../services/observability.md#cloudtrail-trails)、[S3 へのエクスポート](../../services/observability.md#logs-export)、[Redshift のセキュリティ](../../services/data-engineering.md#redshift-security)、[ログの調査](../../services/threat-detection.md#log-investigation)

### 3.3.2 監査と追跡のためのログと監視 {#skill-3-3-2}

| 問い | サービス |
|---|---|
| 誰がいつどの API を呼んだか | CloudTrail |
| 設定はどう変わったか | Config |
| 性能や動作はどうか | CloudWatch |

組織全体の証跡を作り、ログファイルの検証を有効にすると、改ざんや削除を検出できます。ログは別のアカウントの S3 に集め、Object Lock で保護します。

詳細: [CloudTrail の設定](../../services/observability.md#cloudtrail)、[Config と CloudTrail の違い](../../services/governance.md#config-vs-cloudtrail)、[CloudWatch と CloudTrail の違い](../../services/observability.md#cloudtrail-vs-cloudwatch)

### 3.3.3 監視からの通知 {#skill-3-3-3}

| 対象 | 方法 |
|---|---|
| メトリクスのしきい値 | CloudWatch アラーム → SNS |
| ログの中のエラー | メトリクスフィルター → アラーム → SNS |
| ジョブの失敗 | EventBridge のルール → SNS |
| 特定の API の呼び出し | CloudTrail → CloudWatch Logs → メトリクスフィルター |
| 費用の超過 | Budgets の通知 |

データが届かないことを検知するには、アラームの欠落データの扱いを確認します。既定の `missing` では、データがないとアラームが `INSUFFICIENT_DATA` になります。

詳細: [アラーム](../../services/observability.md#alarms)、[欠落データの扱い](../../services/observability.md#treat-missing-data)、[メトリクスフィルター](../../services/observability.md#metric-filters)、[通知アラートの実装](../../services/observability.md#alerts)

### 3.3.4 性能問題のトラブルシューティング {#skill-3-3-4}

| サービス | 症状 | 確認すること |
|---|---|---|
| Kinesis | 消費が遅れる | `GetRecords.IteratorAgeMilliseconds` が増え続ける → 消費者の強化、並列度の増加 |
| Redshift | 実行前に待つ | `stl_wlm_query` の `total_queue_time` → キュー、同時実行スケーリング |
| Redshift | 特定のクエリが遅い | 分散スタイル、ソートキー、`ANALYZE`、`VACUUM` |
| Athena | 遅い、費用が高い | 小さなファイル、パーティション、形式 |
| Glue | 全パーティションを読む | `push_down_predicate` |
| Spark | 一部のタスクだけ遅い | データの偏り（[3.4.5](#skill-3-4-5)） |
| Lambda | タイムアウト | メモリを増やす、`Duration` のメトリクス |
| Firehose | 配信が遅い | バッファのサイズと時間 |

詳細: [Kinesis のエラー](../../services/streaming.md#kinesis-errors)、[ワークロード管理](../../services/data-engineering.md#redshift-wlm)、[Athena のコツ](../../services/streaming.md#athena-performance)、[Firehose のバッファ](../../services/streaming.md#firehose-buffering)、[性能の分析](../../services/observability.md#performance)

### 3.3.5 CloudTrail による API の追跡 {#skill-3-3-5}

| イベント | 記録するもの | 既定 |
|---|---|---|
| 管理イベント | リソースの設定操作 | イベント履歴で90日 |
| データイベント | S3 の `GetObject`、Lambda の `Invoke` など | 記録しない。追加料金で有効化 |
| Insights イベント | API の呼び出し率やエラー率の異常 | 記録しない |

「S3 のオブジェクトを誰が削除したか」を調べたいのに記録がないのは、データイベントが無効だからです。後から有効にしても、過去の分は残りません。

配信は平均で約5分遅れます。即時に反応したい処理は EventBridge を検討します。

詳細: [イベントの種類](../../services/observability.md#cloudtrail-events)、[証跡とイベント履歴](../../services/observability.md#cloudtrail-trails)

### 3.3.6 パイプラインのトラブルシューティングと保守 {#skill-3-3-6}

**Glue**

| 症状 | 対処 |
|---|---|
| OOM | [1.2.7](domain1.md#skill-1-2-7) の表を確認する |
| 長いジョブが途中で止まる | タイムアウトを確認する。既定は Glue 5.0 以降で480分 |
| クエリが失敗する | パーティションごとにスキーマがずれていないか。`InheritFromTable` |
| 実行が始まらない | ワークフローの同時実行の上限。超えたイベントは再試行されない |

**EMR**

| 症状 | 対処 |
|---|---|
| Spot の中断でジョブごと失敗する | Application Master を `CORE` か `ON_DEMAND` のノードに限定する |
| コアノードの Spot で HDFS のブロックを失う | コアは On-Demand、Spot はタスクノードに |
| ジョブが詰まる | マネージドスケーリングの上限を上げる |
| 使っていないのに課金が続く | 自動終了ポリシーを設定する |
| 終了後に調べたい | S3 のログを読む |

詳細: [Glue のワークフロー](../../services/data-engineering.md#glue-workflows)、[DPU と症状](../../services/data-engineering.md#glue-dpu)、[EMR のノード](../../services/data-engineering.md#emr-nodes)、[スケーリングと終了](../../services/data-engineering.md#emr-scaling)

### 3.3.7 CloudWatch Logs によるアプリケーションログ {#skill-3-3-7}

| 設定 | 内容 |
|---|---|
| ロググループの保持期間 | 既定は無期限。費用を抑えるために指定する |
| ログクラス | 頻繁に見ないログは安いクラスを選べる |
| KMS 暗号化 | ロググループにキーを関連付ける |
| データ保護ポリシー | 機密データを取り込み時にマスクする |
| CloudWatch エージェント | EC2 のログを送る |
| メトリクスフィルター | ログからメトリクスを作る |
| サブスクリプションフィルター | Lambda、Kinesis、Firehose、OpenSearch へリアルタイムに送る |

自動化のポイントは、保持期間とフィルターを IaC で定義することと、構造化ログ（JSON）にして検索しやすくすることです。

詳細: [ロググループと保持期間](../../services/observability.md#log-groups)、[ログクラス](../../services/observability.md#log-classes)、[サブスクリプションフィルター](../../services/observability.md#subscription-filters)、[CloudWatch エージェント](../../services/operations.md#cloudwatch-agent)、[構造化ログ](../../services/observability.md#structured-logging)

### 3.3.8 AWS サービスによるログの分析 {#skill-3-3-8}

| ツール | 向く場面 |
|---|---|
| CloudWatch Logs Insights | CloudWatch Logs を手軽にその場で検索する |
| Athena | S3 に置いたログを SQL で分析する。ALB、CloudTrail など |
| OpenSearch Service | 全文検索、ダッシュボード、ほぼリアルタイムの探索 |
| EMR | 非常に大量のログを Spark などで処理する |

```text
fields @timestamp, @message
| filter @message like /ERROR/
| stats count(*) by bin(5m)
```

詳細: [Logs Insights](../../services/observability.md#logs-insights)、[S3 上のログを問い合わせる](../../services/streaming.md#athena-logs)、[OpenSearch Service](../../services/streaming.md#opensearch)、[データの入れ方](../../services/streaming.md#opensearch-ingestion)

## タスク 3.4: データの品質を確保する {#task-3-4}

### 3.4.1 処理中のデータ品質チェック {#skill-3-4-1}

Glue の ETL ジョブの中で Data Quality を評価すると、ロードの前に悪いデータを止められます。不良レコードを隔離し、正常なデータだけを書き込めます。

```text
Rules = [
    IsComplete "order_id",
    Uniqueness "order_id" > 0.99,
    Completeness "email" > 0.95,
    RowCount > 1000
]
```

`IsComplete` は空のフィールドがないことを確認します。評価するとスコアが出ます。

| 入口 | タイミング |
|---|---|
| Data Catalog | 保存済みのデータを評価する |
| ETL ジョブ | パイプラインの途中で止める |

詳細: [Data Quality](../../services/data-engineering.md#glue-data-quality)

### 3.4.2 データ品質ルールの定義 {#skill-3-4-2}

| 観点 | DataBrew | Glue Data Quality |
|---|---|---|
| 書き方 | 画面でルールセットを作る | DQDL |
| 実行 | プロファイルジョブで検証する | Data Catalog、ETL ジョブ |
| 主な利用者 | アナリスト | データエンジニア |
| 例 | 列 `APY` の値は 0〜100、欠損は5%以下 | `ColumnValues "status" in [...]` |

DataBrew のルールは、複合型（配列、構造体）の列には定義できません。

詳細: [DataBrew](../../services/data-engineering.md#databrew)、[Data Quality](../../services/data-engineering.md#glue-data-quality)

### 3.4.3 データの一貫性の調査 {#skill-3-4-3}

同じはずのデータが食い違っていないかを調べます。

| 確認 | 方法 |
|---|---|
| 値の分布や欠損の変化 | DataBrew のプロファイルジョブを定期的に実行して比べる |
| 重複行 | DataBrew のプロファイルの設定で検出して数える |
| 列の間の関係 | DataBrew の相関行列 |
| 件数の一致 | ソースとターゲットの `COUNT(*)` を Athena と Redshift で比べる |
| 定期的な監視 | Glue Data Quality の機械学習による異常検出 |

データの読み方にも注意します。DynamoDB の読み取りは既定で結果整合性で、GSI は強い整合性に対応しません。

詳細: [DataBrew](../../services/data-engineering.md#databrew)、[Data Quality](../../services/data-engineering.md#glue-data-quality)、[DynamoDB の読み取りの整合性](../../services/dynamodb.md#read-consistency)

### 3.4.4 データのサンプリング手法 {#skill-3-4-4}

全件を調べる費用と時間を減らすために、一部を取り出します。

| 手法 | 動作 | 注意 |
|---|---|---|
| 単純ランダム | 各行を同じ確率で選ぶ | 少数のグループが抜けることがある |
| 層化 | グループごとに抽出する | 比率を保てる。キーの設計が必要 |
| 系統 | N 行ごとに選ぶ | 周期的なデータでは偏る |
| 先頭 N 行 | 最初の行を取る | 速いが、並び順で偏る |

AWS での実装です。

| サービス | 方法 |
|---|---|
| Athena | `TABLESAMPLE BERNOULLI (10)` は行単位で全ブロックをスキャンする。`TABLESAMPLE SYSTEM (10)` はセグメント単位で読むが、独立性は保証されない |
| DataBrew のプロジェクト | `FIRST_N`、`LAST_N`、`RANDOM`。最大 5,000 行 |
| DataBrew のプロファイルジョブ | 既定は `CUSTOM_ROWS` の 20,000 行。全件は `FULL_DATASET` |
| Macie の自動検出 | サンプリングで検査する |

プロファイルが既定の 20,000 行だと、まれな不良値を見落とすことがあります。全体の品質を確かめるときは `FULL_DATASET` にします。

詳細: [DataBrew](../../services/data-engineering.md#databrew)、[Macie の検出](../../services/threat-detection.md#macie-discovery)

### 3.4.5 データの偏りへの対応 {#skill-3-4-5}

分散処理では、特定のキーにデータが集中すると、そのノードだけ遅くなります。全体の性能は一番遅いノードで決まります。

| サービス | 検知 | 対処 |
|---|---|---|
| Redshift | `SVV_TABLE_INFO` の `skew_rows`（最大と最小のスライスの行数の比） | 値の種類が多い列を `DISTKEY` に。`DISTSTYLE AUTO` |
| Spark（Glue、EMR） | 一部のタスクだけ長い、特定のエグゼキューターが OOM | 偏ったキーに乱数を足す（ソルティング）、再パーティション、適応クエリ実行、小さいテーブルのブロードキャスト結合 |
| Kinesis | シャードレベルのメトリクスで一部だけスロットリング | パーティションキーの見直し、ランダムなキーの追加、シャード分割 |
| DynamoDB | 特定のキーでスロットリング | 値の種類が多いキー、書き込みのシャーディング |
| S3 のパーティション | ファイルの大きさがパーティションごとに大きく違う | パーティション列の見直し |

Redshift で日付列を `DISTKEY` にして狭い期間で絞ると、少数のスライスに処理が偏ります。行数の偏りだけでなく、フィルターの後の偏りも確認します。

詳細: [分散スタイル](../../services/data-engineering.md#redshift-distribution)、[Kinesis のパーティションキー](../../services/streaming.md#partition-key)、[DynamoDB のスロットリング](../../services/dynamodb.md#throttling)

## 確認問題 {#self-check}

??? question "問1: S3 の CSV のログを Athena で分析しています。費用を減らし、速くしたいです。最も効果が大きい変更は？"
    Parquet に変換し、日付でパーティションを切ることです。CTAS か Glue ジョブで変換します。列指向で必要な列だけ読み、パーティションで範囲を絞るので、スキャン量が大きく減ります。Athena の料金はスキャン量で決まります。

??? question "問2: 誰かが S3 の分析用バケットからオブジェクトを削除しました。CloudTrail を調べても記録がありません。なぜですか？今後どうしますか？"
    S3 のオブジェクト操作はデータイベントで、既定では記録されないからです。証跡でデータイベントを有効にします。後から有効にしても過去の分は記録されないので、バケットのバージョニングも有効にして復元に備えます。

??? question "問3: ETL の途中で不正なデータをロードしないようにし、不良レコードは隔離したいです。データエンジニアがパイプラインの中に組み込みます。何を使いますか？"
    Glue の ETL ジョブの中の Glue Data Quality です。DQDL でルールを書き、不良レコードを隔離して正常なデータだけを書き込めます。DataBrew はアナリストが画面で扱うのに向いています。

??? question "問4: Spark のジョブで1つのタスクだけ長時間かかり、そのエグゼキューターが OOM で落ちます。ワーカーを増やしても改善しません。原因と対処は？"
    結合や集計のキーにデータの偏りがあります。ワーカーを増やしても、同じキーは同じタスクに集まるので効きません。偏ったキーに乱数を足す、再パーティションする、小さいテーブルをブロードキャストして結合するなどで対処します。

??? question "問5: 利用が平日の日中に限られ、負荷が読めない分析用の DWH を新しく作ります。夜間と週末の費用を抑えたいです。何を選び、何を設定しますか？"
    Redshift Serverless を選び、ワークグループに最大 RPU を設定します。使っていない時間のコンピュート料金はかかりません。最大 RPU を指定しないと、負荷に応じて費用が増えます。常に負荷があるなら、予約で安くできる Provisioned が向きます。

??? question "問6: DataBrew のプロファイルでは問題なかったのに、本番で 0.1% の行に不正な値が見つかりました。何が考えられますか？どう直しますか？"
    プロファイルジョブは既定で 20,000 行のサンプルを対象にするので、まれな値を見落とした可能性があります。サンプルの設定を `FULL_DATASET` にします。パイプラインの中でも全件を検査するなら、Glue Data Quality を ETL ジョブに組み込みます。

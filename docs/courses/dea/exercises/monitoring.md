# 監視とトラブルシューティングの問題集

対象の解説: [オブザーバビリティ（CloudWatch / X-Ray / CloudTrail）](../../../services/observability.md)

### 問1 {#q1}

監査のため、今後の API の記録を 1 年以上残し、SQL で検索できるようにします。まだ何も設定していません。どの手順ですか。

- A. CloudWatch Logs Insights でイベント履歴を直接検索する手順
- B. CloudWatch のメトリクスに API の記録を出力して、グラフで確認する手順
- C. 証跡で S3 へ出力し、Athena でテーブルを作って検索する
- D. イベント履歴を 1 年分ダウンロードして、表計算で検索する手順

??? success "答えと解説"
    **正解: C**

    長期の記録は証跡で S3 に残します。証跡は作成の後のイベントを記録します。

    - A: 誤り。イベント履歴は Logs Insights の検索の対象ではなく、保持も 90 日です。
    - B: 誤り。API の記録の出力先ではありません。
    - C: 正しい。
    - D: 誤り。イベント履歴は 90 日分です。

    **スキル:** [3.3.1](../domain3.md#skill-3-3-1) / **参照:** [証跡とイベント履歴](../../../services/observability.md#cloudtrail-trails)、[S3 上のログを問い合わせる](../../../services/streaming.md#athena-logs)

### 問2 {#q2}

Redshift の監査で、誰が接続し、どんな SQL を実行したかを記録します。何を有効にしますか。

- A. 監査ログ（接続ログ、ユーザーログ、ユーザーアクティビティログ）を S3 か CloudWatch へ出す
- B. クエリモニタリングルールで全クエリを中止して、記録を残す設定
- C. 自動スナップショットの保持期間を延ばして、SQL の履歴を残す設定
- D. Enhanced VPC Routing を有効にして、`COPY` の通信を記録する設定

??? success "答えと解説"
    **正解: A**

    3 種類のログを出力できます。

    - A: 正しい。
    - B: 誤り。監査ログの機能ではありません。
    - C: 誤り。データのバックアップです。
    - D: 誤り。通信経路の機能です。

    **スキル:** [3.3.1](../domain3.md#skill-3-3-1) / **参照:** [暗号化とセキュリティ](../../../services/data-engineering.md#redshift-security)

### 問3 {#q3}

ログの取り出し方で正しいものはどれですか。（2つ選択）

- A. CloudWatch Logs のログを S3 へエクスポートする
- B. CloudWatch Logs のログは必ず 7 日で消えるので、毎日コピーする
- C. EMR のクラスターのログを S3 へ出し、終了後も調査する
- D. EMR のログはプライマリノードの終了後も SSH で読める
- E. S3 の `GetObject` は管理イベントなので、既定で 1 年残る

??? success "答えと解説"
    **正解: A, C**

    ログの場所と保持を確認します。

    - A: 正しい。長期の保存や分析に使えます。
    - B: 誤り。既定の保持は無期限です。
    - C: 正しい。S3 のログは残ります。
    - D: 誤り。終了後は接続できません。
    - E: 誤り。データイベントで、既定では記録しません。

    **スキル:** [3.3.1](../domain3.md#skill-3-3-1) / **参照:** [スケーリングと終了](../../../services/data-engineering.md#emr-scaling)、[S3 へのエクスポート](../../../services/observability.md#logs-export)

### 問4 {#q4}

次の問いとサービスの組み合わせで正しいものはどれですか。

- A. 「誰がバケットポリシーを変えたか」は CloudWatch のメトリクス
- B. 「誰がバケットポリシーを変えたか」は CloudTrail
- C. 「関数の実行時間はどう変わったか」は AWS Config
- D. 「設定は基準に合っているか」は CloudWatch Logs Insights

??? success "答えと解説"
    **正解: B**

    問いでサービスを分けます。

    - A: 誤り。CloudTrail の役割です。
    - B: 正しい。
    - C: 誤り。CloudWatch の役割です。
    - D: 誤り。Config の役割です。

    **スキル:** [3.3.2](../domain3.md#skill-3-3-2) / **参照:** [CloudWatch と CloudTrail の違い](../../../services/observability.md#cloudtrail-vs-cloudwatch)、[Config と CloudTrail の違い](../../../services/governance.md#config-vs-cloudtrail)

### 問5 {#q5}

監査ログの改ざんと削除を検出できるようにし、ログ自体を守ります。どの組み合わせですか。

- A. ログファイルの検証を無効にし、同じアカウントのバケットで公開の読み取りを許可する
- B. 証跡を削除し、イベント履歴の 90 日分だけを監査の根拠にして運用する
- C. 管理イベントを無効にし、データイベントだけをログとして同じバケットに残す
- D. ログファイルの検証を有効にし、別のアカウントの S3 に集めて Object Lock で保護する

??? success "答えと解説"
    **正解: D**

    組織全体の証跡と組み合わせます。

    - A: 誤り。改ざんを検出できず、公開も不適切です。
    - B: 誤り。長期の保護ができません。
    - C: 誤り。監査に必要な記録が残りません。
    - D: 正しい。

    **スキル:** [3.3.2](../domain3.md#skill-3-3-2) / **参照:** [CloudTrail の設定](../../../services/observability.md#cloudtrail)

### 問6 {#q6}

全アカウントのパイプライン関連の操作と設定の変更を追跡します。組み合わせとして適切なものはどれですか。（2つ選択）

- A. 各アカウントのイベント履歴だけを見る運用
- B. 組織全体の証跡
- C. CloudWatch のメトリクスフィルター
- D. Macie の自動検出
- E. Config のアグリゲーター

??? success "答えと解説"
    **正解: B, E**

    CloudTrail と Config を組み合わせます。

    - A: 誤り。90 日分で、組織全体の記録になりません。
    - B: 正しい。全アカウントと全リージョンの API を記録します。
    - C: 誤り。ログから数値を作る機能です。
    - D: 誤り。機密データの検出です。
    - E: 正しい。複数のアカウントの設定の情報を集約します。

    **スキル:** [3.3.2](../domain3.md#skill-3-3-2) / **参照:** [CloudTrail の設定](../../../services/observability.md#cloudtrail)、[AWS Config](../../../services/governance.md#config)

### 問7 {#q7}

アプリのログに `ERROR` が 5 分で 10 回出たら通知します。どの構成ですか。

- A. メトリクスフィルターでメトリクスを作り、アラームから SNS へ送る
- B. CloudTrail のデータイベントでアプリのログを記録する構成
- C. Logs Insights のクエリを人が 5 分ごとに実行して確認する構成
- D. サブスクリプションフィルターを Glue ジョブに直接向けて実行する構成

??? success "答えと解説"
    **正解: A**

    ログからメトリクスを作ります。

    - A: 正しい。
    - B: 誤り。API の記録で、アプリのログではありません。
    - C: 誤り。自動の通知になりません。
    - D: 誤り。Glue は送信先に使えません。

    **スキル:** [3.3.3](../domain3.md#skill-3-3-3) / **参照:** [メトリクスフィルター](../../../services/observability.md#metric-filters)、[アラーム](../../../services/observability.md#alarms)

### 問8 {#q8}

毎時のバッチが出すメトリクスで、データが来ないこと自体を障害として検知します。アラームの欠落データの扱いはどれですか。

- A. `notBreaching`
- B. `ignore`
- C. `missing`
- D. `breaching`

??? success "答えと解説"
    **正解: D**

    死活の監視には `breaching` を使います。

    - A: 誤り。正常とみなします。
    - B: 誤り。今の状態を維持します。
    - C: 誤り。既定で、全部欠落なら `INSUFFICIENT_DATA` になります。
    - D: 正しい。

    **スキル:** [3.3.3](../domain3.md#skill-3-3-3) / **参照:** [欠落データの扱い](../../../services/observability.md#treat-missing-data)

### 問9 {#q9}

通知の対象と方法の組み合わせで正しいものはどれですか。

- A. メトリクスのしきい値は Config のルール
- B. 特定の API の呼び出しは Glue Data Quality
- C. 月の費用の超過は Budgets の通知
- D. Glue のジョブの失敗は Budgets の通知

??? success "答えと解説"
    **正解: C**

    対象で方法を選びます。

    - A: 誤り。CloudWatch アラームで受けます。
    - B: 誤り。CloudTrail と CloudWatch Logs を組み合わせます。
    - C: 正しい。
    - D: 誤り。EventBridge のルールで受けます。

    **スキル:** [3.3.3](../domain3.md#skill-3-3-3) / **参照:** [通知アラートの実装](../../../services/observability.md#alerts)、[AWS Budgets](../../../services/cost-management.md#budgets)

### 問10 {#q10}

Kinesis の Lambda で `IteratorAge` が増え続けています。消費が遅れています。適切な対処はどれですか。

- A. 書き込み側の `PutRecords` のバッチを大きくする設定
- B. `ParallelizationFactor` を上げるか、関数の処理を速くする
- C. クラウドの料金のアラームを追加して様子を見る設定
- D. 保持期間を短くして、古いレコードを早く捨てる設定

??? success "答えと解説"
    **正解: B**

    `GetRecords.IteratorAgeMilliseconds` の増加は消費の遅れです。

    - A: 誤り。消費の遅れは解決しません。
    - B: 正しい。
    - C: 誤り。遅れは解決しません。
    - D: 誤り。データを失う恐れがあります。

    **スキル:** [3.3.4](../domain3.md#skill-3-3-4) / **参照:** [エラーと監視](../../../services/streaming.md#kinesis-errors)、[ストリームのエラー処理の設定](../../../services/lambda.md#esm-stream-errors)

### 問11 {#q11}

Redshift のクエリが遅いという報告があります。`stl_wlm_query` の `total_queue_time` が長く、実行時間は短いです。何から見直しますか。

- A. 分散スタイルの変更と `COPY` の分割
- B. WLM のキューと同時実行スケーリング
- C. ノードの追加とテーブルのソートキーの変更
- D. `VACUUM` の実行と `ANALYZE` の実行

??? success "答えと解説"
    **正解: B**

    実行前の待ちはキューの問題です。

    - A: 誤り。実行とロードの話です。
    - B: 正しい。
    - C: 誤り。待ちが原因なので、キューを先に確認します。
    - D: 誤り。実行が遅い場合の確認です。

    **スキル:** [3.3.4](../domain3.md#skill-3-3-4) / **参照:** [ワークロード管理](../../../services/data-engineering.md#redshift-wlm)

### 問12 {#q12}

Firehose の配信が遅く、S3 に 15 分遅れで届きます。バッファの条件の説明として正しいものはどれですか。

- A. バッファの時間は常に固定で変更できないので、シャードを増やす
- B. サイズと時間の両方を満たすまで配信しないので、両方を増やす
- C. 配信先を Glacier にすれば、バッファは不要になる
- D. サイズと時間のどちらか先に満たしたほうで配信するので、これらの値を下げる

??? success "答えと解説"
    **正解: D**

    バッファの設定が遅れを決めます。

    - A: 誤り。変更できます。
    - B: 誤り。先に満たしたほうで配信します。
    - C: 誤り。バッファの条件とは関係しません。
    - D: 正しい。

    **スキル:** [3.3.4](../domain3.md#skill-3-3-4) / **参照:** [バッファ](../../../services/streaming.md#firehose-buffering)、[性能の分析とボトルネックの検出](../../../services/observability.md#performance)

### 問13 {#q13}

S3 のオブジェクトを誰が削除したかを調べると、CloudTrail に記録がありません。既定の設定のままです。説明と対処で正しいものはどれですか。

- A. Insights イベントは既定で記録するので検索の条件を見直す。過去の分も見られる
- B. 管理イベントは既定で記録しないので有効にする。過去の分も後から見られる
- C. データイベントは既定で記録しないので有効にする。過去の分は残らない
- D. データイベントは既定で記録するので検索の条件を見直す。過去の分も見られる

??? success "答えと解説"
    **正解: C**

    S3 のオブジェクトの操作はデータイベントです。

    - A: 誤り。Insights は既定で記録しません。
    - B: 誤り。管理イベントは 90 日分見られます。
    - C: 正しい。
    - D: 誤り。既定では記録しません。

    **スキル:** [3.3.5](../domain3.md#skill-3-3-5) / **参照:** [イベントの種類](../../../services/observability.md#cloudtrail-events)

### 問14 {#q14}

API のエラーの率が普段より急に上がったことを検知します。CloudTrail のどのイベントですか。

- A. Insights イベント
- B. データイベント
- C. イベント履歴の 90 日分の一覧
- D. 管理イベント

??? success "答えと解説"
    **正解: A**

    Insights は呼び出し率やエラー率の異常を記録します。

    - A: 正しい。
    - B: 誤り。オブジェクトなどの操作です。
    - C: 誤り。異常の検知の機能ではありません。
    - D: 誤り。リソースの設定の操作です。

    **スキル:** [3.3.5](../domain3.md#skill-3-3-5) / **参照:** [イベントの種類](../../../services/observability.md#cloudtrail-events)

### 問15 {#q15}

CloudTrail の S3 への配信の遅れを踏まえ、特定の API の呼び出しに素早く反応します。どの方法ですか。

- A. S3 に届いたログを 1 日 1 回 Athena で検索する
- B. Config のアグリゲーターで、API の呼び出しのたびに受ける
- C. EventBridge のルールで API の呼び出しを受ける
- D. イベント履歴を毎週ダウンロードして確認する

??? success "答えと解説"
    **正解: C**

    配信は平均で約 5 分遅れます。

    - A: 誤り。素早く反応できません。
    - B: 誤り。設定の集約の機能です。
    - C: 正しい。
    - D: 誤り。素早く反応できません。

    **スキル:** [3.3.5](../domain3.md#skill-3-3-5) / **参照:** [証跡とイベント履歴](../../../services/observability.md#cloudtrail-trails)、[ルールとイベントパターン](../../../services/messaging.md#eventbridge-rules)

### 問16 {#q16}

CloudWatch Logs の費用が増え続けています。ロググループの設定は既定のままです。まず何を設定しますか。

- A. ロググループの保持期間
- B. メトリクスフィルターの数を増やす設定
- C. CloudWatch エージェントをすべての EC2 に入れる設定
- D. サブスクリプションフィルターを追加する設定

??? success "答えと解説"
    **正解: A**

    既定は無期限です。

    - A: 正しい。
    - B: 誤り。費用の削減にはなりません。
    - C: 誤り。送るログが増えます。
    - D: 誤り。転送の機能で、保存量は減りません。

    **スキル:** [3.3.7](../domain3.md#skill-3-3-7) / **参照:** [ロググループと保持期間](../../../services/observability.md#log-groups)

### 問17 {#q17}

EC2 上の ETL のログを CloudWatch Logs へ送り、OpenSearch へリアルタイムに流します。組み合わせはどれですか。

- A. X-Ray デーモンとトレース
- B. CloudWatch エージェントとサブスクリプションフィルター
- C. メトリクスフィルターとログのエクスポート
- D. CloudWatch エージェントとログのエクスポート

??? success "答えと解説"
    **正解: B**

    エージェントで送り、フィルターで転送します。

    - A: 誤り。リクエストの追跡で、ログの転送ではありません。
    - B: 正しい。
    - C: 誤り。リアルタイムの転送になりません。
    - D: 誤り。エクスポートはリアルタイムの転送になりません。

    **スキル:** [3.3.7](../domain3.md#skill-3-3-7) / **参照:** [CloudWatch エージェント](../../../services/operations.md#cloudwatch-agent)、[サブスクリプションフィルター](../../../services/observability.md#subscription-filters)

### 問18 {#q18}

ログの自動化の説明で正しいものはどれですか。（2つ選択）

- A. JSON の構造化ログにして検索しやすくする
- B. 保持期間とフィルターを IaC で定義する
- C. データ保護ポリシーは取り込み後のログしかマスクできない
- D. ロググループの KMS の暗号化は設定できない
- E. ログクラスは作成後に何度でも変更できる

??? success "答えと解説"
    **正解: A, B**

    設定は最初に揃えます。

    - A: 正しい。フィールドで絞れます。
    - B: 正しい。環境で揃えられます。
    - C: 誤り。取り込み時にマスクします。
    - D: 誤り。キーを関連付けられます。
    - E: 誤り。作成時に選び、後から変更できません。

    **スキル:** [3.3.7](../domain3.md#skill-3-3-7) / **参照:** [ログクラス](../../../services/observability.md#log-classes)、[構造化ログ](../../../services/observability.md#structured-logging)

### 問19 {#q19}

CloudWatch Logs のエラーを、5 分ごとの件数でその場で調べます。追加の構築はしません。どれを使いますか。

- A. OpenSearch のドメインとダッシュボードの組み合わせ
- B. EMR のクラスターと Spark
- C. Athena のワークグループと S3 へのエクスポートの組み合わせ
- D. CloudWatch Logs Insights で集計する

??? success "答えと解説"
    **正解: D**

    `stats count(*) by bin(5m)` で集計できます。

    - A: 誤り。構築が必要です。
    - B: 誤り。構築が必要です。
    - C: 誤り。エクスポートと構築が必要です。
    - D: 正しい。

    **スキル:** [3.3.8](../domain3.md#skill-3-3-8) / **参照:** [Logs Insights でログを検索する](../../../services/observability.md#logs-insights)

### 問20 {#q20}

S3 に数か月分ある ALB のアクセスログを SQL で分析します。最も適切なものはどれですか。

- A. CloudWatch Logs Insights
- B. Athena の SQL で検索する
- C. CloudTrail の Insights イベント
- D. Redshift のデータ共有

??? success "答えと解説"
    **正解: B**

    S3 のログの分析には Athena が向きます。

    - A: 誤り。対象は CloudWatch Logs です。
    - B: 正しい。
    - C: 誤り。API の異常の検出です。
    - D: 誤り。Redshift 同士の共有です。

    **スキル:** [3.3.8](../domain3.md#skill-3-3-8) / **参照:** [S3 上のログを問い合わせる](../../../services/streaming.md#athena-logs)

### 問21 {#q21}

要件とツールの組み合わせで正しいものはどれですか。（2つ選択）

- A. S3 のログの単発の SQL は OpenSearch のダッシュボードだけ
- B. 全文検索のダッシュボードは Glue のクローラー
- C. 非常に大量のログの複雑な処理は EMR
- D. ほぼリアルタイムの全文検索とダッシュボードは OpenSearch Service
- E. CloudWatch Logs の手軽な検索は EMR

??? success "答えと解説"
    **正解: C, D**

    量と使い方でツールを選びます。

    - A: 誤り。Athena が向きます。
    - B: 誤り。スキーマの推定です。
    - C: 正しい。Spark などで処理できます。
    - D: 正しい。探索に向きます。
    - E: 誤り。Logs Insights が向きます。

    **スキル:** [3.3.8](../domain3.md#skill-3-3-8) / **参照:** [Amazon OpenSearch Service](../../../services/streaming.md#opensearch)、[Amazon EMR](../../../services/data-engineering.md#emr)

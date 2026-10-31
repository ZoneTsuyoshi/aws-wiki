# 監査ログの問題集

対象の解説: [CloudTrail の設定](../../../services/observability.md#cloudtrail)、[どのログを見るか](../../../services/threat-detection.md#log-sources)

### 問1 {#q1}

監査の要件で、全アカウントと全リージョンの API の記録を 7 年残します。どの設定ですか。

- A. 1 つのアカウントの単一リージョンの証跡だけを作る設定
- B. 組織の証跡を作成し、S3 へ出力して保持する
- C. 各アカウントのイベント履歴を、そのまま 7 年保持する設定
- D. CloudWatch のアラームの履歴を、ログの代わりに保持する設定

??? success "答えと解説"
    **正解: B**

    90 日より長く残すなら証跡です。

    - A: 誤り。全範囲を記録できません。
    - B: 正しい。
    - C: 誤り。イベント履歴は 90 日分です。
    - D: 誤り。API の記録ではありません。

    **スキル:** [4.4.1](../domain4.md#skill-4-4-1) / **参照:** [証跡とイベント履歴](../../../services/observability.md#cloudtrail-trails)

### 問2 {#q2}

「誰が Lake Formation の権限を変えたか」を調べます。どのイベントですか。

- A. 管理イベントの `GrantPermissions` などを検索する
- B. Redshift のユーザーログを検索する
- C. Insights イベントの異常の一覧を検索する
- D. データイベントの `GetObject` を基に、変更者を推定して検索する

??? success "答えと解説"
    **正解: A**

    権限の変更は設定の操作で、管理イベントです。

    - A: 正しい。
    - B: 誤り。Redshift の記録です。
    - C: 誤り。異常の検出です。
    - D: 誤り。オブジェクトの読み取りの記録です。

    **スキル:** [4.4.1](../domain4.md#skill-4-4-1) / **参照:** [CloudTrail の調査](../../../services/threat-detection.md#investigate-cloudtrail)、[イベントの種類](../../../services/observability.md#cloudtrail-events)

### 問3 {#q3}

監査の要件と CloudTrail の設定の組み合わせで正しいものはどれですか。（2つ選択）

- A. 分析バケットの読み書きの記録にはデータイベントを有効にする
- B. ログの改ざんの検出にはログファイルの検証を有効にする
- C. 改ざんの検出にはデータイベントを無効にする
- D. 全リージョンの記録にはログファイルの検証を有効にする
- E. データの読み取りの記録には Insights イベントを有効にする

??? success "答えと解説"
    **正解: A, B**

    要件で設定を選びます。

    - A: 正しい。既定では記録しません。
    - B: 正しい。変更や削除を検出できます。
    - C: 誤り。関係しません。
    - D: 誤り。検証は改ざんの検出です。
    - E: 誤り。異常の検出です。

    **スキル:** [4.4.1](../domain4.md#skill-4-4-1) / **参照:** [イベントの種類](../../../services/observability.md#cloudtrail-events)、[CloudTrail の設定](../../../services/observability.md#cloudtrail)

### 問4 {#q4}

アプリのログを監査のため 3 年残し、1 か月より古いものは安く保存します。最も適切なものはどれですか。

- A. 保持期間を既定のまま、ログの本文を手で圧縮し直す運用
- B. メトリクスフィルターでログを数値にして、元のログは消す運用
- C. ログを Lambda の `/tmp` へコピーし、関数の中で 3 年残す運用
- D. 保持期間を設定し、S3 へエクスポートしてライフサイクルで移行する

??? success "答えと解説"
    **正解: D**

    長期保存は S3 が安くなります。

    - A: 誤り。費用は下がらず、手間が増えます。
    - B: 誤り。監査のログが残りません。
    - C: 誤り。一時的な領域です。
    - D: 正しい。

    **スキル:** [4.4.2](../domain4.md#skill-4-4-2) / **参照:** [ロググループと保持期間](../../../services/observability.md#log-groups)、[S3 へのエクスポート](../../../services/observability.md#logs-export)

### 問5 {#q5}

ログに個人のメールアドレスが入ることがあります。コードの変更なしに、取り込み時に隠します。何を設定しますか。

- A. ロググループのログクラスの変更
- B. ロググループの KMS キーの関連付け
- C. ロググループのデータ保護ポリシー
- D. サブスクリプションフィルターで別のロググループへ送る

??? success "答えと解説"
    **正解: C**

    機密データを取り込み時にマスクします。

    - A: 誤り。料金と機能の設定です。
    - B: 誤り。暗号化で、見る人には平文で表示されます。
    - C: 正しい。
    - D: 誤り。取り込まれた値は隠れません。

    **スキル:** [4.4.2](../domain4.md#skill-4-4-2) / **参照:** [データ保護ポリシー](../../../services/observability.md#logs-data-protection)、[CloudWatch Logs のデータ保護](../../../services/secrets.md#cloudwatch-data-protection)

### 問6 {#q6}

ログの要件と設定の組み合わせで正しいものはどれですか。

- A. 機密データのマスクには KMS キーをロググループに関連付けて使う
- B. 他のアカウントへ集めるにはサブスクリプションフィルターを使う
- C. ログの暗号化にはメトリクスフィルターを使う
- D. 監査の期間だけ残すにはログクラスを変更する

??? success "答えと解説"
    **正解: B**

    設定の役割を分けて覚えます。

    - A: 誤り。データ保護ポリシーを使います。
    - B: 正しい。
    - C: 誤り。KMS キーを関連付けます。
    - D: 誤り。保持期間で設定します。

    **スキル:** [4.4.2](../domain4.md#skill-4-4-2) / **参照:** [KMS による暗号化](../../../services/observability.md#logs-kms)、[サブスクリプションフィルター](../../../services/observability.md#subscription-filters)

### 問7 {#q7}

2026 年 5 月より前から CloudTrail Lake を使っている組織です。複数のアカウントのイベントを、S3 と Athena の環境なしで SQL で検索します。説明として正しいものはどれですか。

- A. イベントを DynamoDB に集め、キーの `GetItem` だけで検索する
- B. イベントを CSV のログストリームに集め、Logs Insights の構文だけで検索する
- C. イベントを Glue Data Catalog に保存し、S3 は常に必要になる
- D. イベントを ORC 形式のイベントデータストアに集め、SQL で検索する

??? success "答えと解説"
    **正解: D**

    既存の顧客は引き続き使えます。

    - A: 誤り。データストアは DynamoDB ではありません。
    - B: 誤り。ORC 形式のデータストアで、SQL を使います。
    - C: 誤り。S3 と Athena の環境を作らずに使えます。
    - D: 正しい。

    **スキル:** [4.4.3](../domain4.md#skill-4-4-3) / **参照:** [CloudTrail Lake](../../../services/observability.md#cloudtrail-lake)

### 問8 {#q8}

2026 年 10 月に新しく AWS を使い始めた顧客が、複数のアカウントの CloudTrail のイベントを SQL で検索します。現在の選択肢の説明として正しいものはどれですか。

- A. イベント履歴を有効にし、全アカウントの記録を 1 年以上 SQL で検索する
- B. CloudTrail Lake のイベントデータストアを新規に作成して検索する
- C. 証跡で S3 へ出力して Athena で検索するか、CloudWatch へ取り込んで検索する
- D. CloudTrail のイベントを CloudWatch のメトリクスに変換して、数式で検索する

??? success "答えと解説"
    **正解: C**

    新規の環境では、証跡と Athena、または AWS が移行先として勧める CloudWatch を使います。

    - A: 誤り。イベント履歴は 90 日分の管理イベントです。
    - B: 誤り。2026 年 5 月 31 日で新規顧客の受付を終了しました。
    - C: 正しい。
    - D: 誤り。メトリクスは数値で、API の記録の検索には使えません。

    **スキル:** [4.4.3](../domain4.md#skill-4-4-3) / **参照:** [CloudTrail Lake](../../../services/observability.md#cloudtrail-lake)、[証跡とイベント履歴](../../../services/observability.md#cloudtrail-trails)

### 問9 {#q9}

CloudTrail Lake と「証跡と Athena」の違いとして正しいものはどれですか。

- A. Lake は S3 や Athena の環境を自分で作らずに検索でき、証跡と Athena はそれらを自分で用意する
- B. Lake は S3 の証跡がないと使えず、証跡と Athena は S3 が不要である
- C. Lake は単一のアカウントだけで、証跡と Athena は常に全組織を自動で検索する
- D. Lake は SQL を使えず、証跡と Athena は Logs Insights の構文を使う

??? success "答えと解説"
    **正解: A**

    環境を用意する手間が違います。

    - A: 正しい。
    - B: 誤り。どちらも逆です。
    - C: 誤り。Lake も複数のアカウントを扱えます。
    - D: 誤り。どちらも SQL です。

    **スキル:** [4.4.3](../domain4.md#skill-4-4-3) / **参照:** [CloudTrail Lake](../../../services/observability.md#cloudtrail-lake)、[S3 上のログを問い合わせる](../../../services/streaming.md#athena-logs)

### 問10 {#q10}

「過去 90 日に、このバケットのポリシーを変えた人は誰か」を、S3 にある CloudTrail のログから調べます。何を使いますか。

- A. CloudWatch Logs Insights
- B. OpenSearch Service のドメインを常時起動して、ログをすべて取り込んで検索する
- C. Redshift のデータ共有
- D. S3 のログに Athena のテーブルを作り、SQL で検索する

??? success "答えと解説"
    **正解: D**

    S3 のログの検索に使います。

    - A: 誤り。対象は CloudWatch Logs です。
    - B: 誤り。単発の調査には構築と費用が過剰です。
    - C: 誤り。Redshift 同士の共有です。
    - D: 正しい。

    **スキル:** [4.4.4](../domain4.md#skill-4-4-4) / **参照:** [S3 上のログを問い合わせる](../../../services/streaming.md#athena-logs)、[どのログを見るか](../../../services/threat-detection.md#log-sources)

### 問11 {#q11}

Lambda の直近 1 時間のエラーの傾向を、その場で調べます。構築はしません。何を使いますか。

- A. CloudWatch Logs Insights で検索する
- B. OpenSearch のドメインを新しく作り、ログを入れて検索する
- C. EMR のクラスターを作り、Spark でログを処理する
- D. 証跡を作り、S3 のログを Athena で検索する

??? success "答えと解説"
    **正解: A**

    その場の検索に向きます。

    - A: 正しい。
    - B: 誤り。構築が必要です。
    - C: 誤り。構築が必要です。
    - D: 誤り。関数のアプリログではなく API の記録です。

    **スキル:** [4.4.4](../domain4.md#skill-4-4-4) / **参照:** [Logs Insights でログを検索する](../../../services/observability.md#logs-insights)

### 問12 {#q12}

セキュリティチームが、ログの全文検索とダッシュボードを常時使います。何を選びますか。

- A. Athena の単発のクエリをダッシュボードの代わりに毎回手で実行する運用
- B. OpenSearch Service にログを入れ、ダッシュボードを作る
- C. CloudWatch のアラームだけで内容を確認する運用
- D. Macie の自動検出の結果だけで確認する運用

??? success "答えと解説"
    **正解: B**

    全文検索とダッシュボードに向きます。

    - A: 誤り。単発の分析に向きます。
    - B: 正しい。
    - C: 誤り。全文検索はできません。
    - D: 誤り。機密データの検出です。

    **スキル:** [4.4.4](../domain4.md#skill-4-4-4) / **参照:** [Amazon OpenSearch Service](../../../services/streaming.md#opensearch)、[どのログを見るか](../../../services/threat-detection.md#log-sources)

### 問13 {#q13}

CloudWatch Logs のログを Parquet で S3 に集め、Athena で調べます。追加のコードは書きません。どの構成ですか。

- A. Logs Insights の結果を 1 件ずつ手でダウンロードして S3 へ置く構成
- B. メトリクスフィルターから Glue のクローラーへ送り、S3 へ配信する構成
- C. サブスクリプションフィルターから Firehose へ送り、解凍と形式の変換をして S3 へ配信する
- D. Config ルールから S3 レプリケーションへ送り、S3 へ配信する構成

??? success "答えと解説"
    **正解: C**

    フィルターで Firehose へ送り、Firehose で解凍と形式の変換を行います。

    - A: 誤り。自動の収集になりません。
    - B: 誤り。メトリクスの作成とスキーマの推定です。
    - C: 正しい。
    - D: 誤り。設定の評価と複製です。

    **スキル:** [4.4.5](../domain4.md#skill-4-4-5) / **参照:** [サブスクリプションフィルター](../../../services/observability.md#subscription-filters)、[Amazon Data Firehose](../../../services/streaming.md#firehose)

### 問14 {#q14}

毎日数十 TB のログを結合し、複雑な処理を Spark で行います。どれが適切ですか。

- A. CloudWatch Logs Insights のクエリ
- B. Firehose の Lambda 変換の処理
- C. EMR のクラスターで実行する Spark のジョブ
- D. Lambda の 1 つの関数

??? success "答えと解説"
    **正解: C**

    非常に大量で複雑な処理は EMR です。

    - A: 誤り。複雑な処理には向きません。
    - B: 誤り。レコードの変換で、結合や複雑な処理には向きません。
    - C: 正しい。
    - D: 誤り。実行時間とメモリの上限があります。

    **スキル:** [4.4.5](../domain4.md#skill-4-4-5) / **参照:** [スケーリングと終了](../../../services/data-engineering.md#emr-scaling)、[Amazon Athena](../../../services/streaming.md#athena)

### 問15 {#q15}

ログの使い方と選択の組み合わせで正しいものはどれですか。（2つ選択）

- A. サブスクリプションフィルターの送信先は S3 のバケットだけである
- B. S3 に集めたログの単発の調査は Athena
- C. Firehose は CloudWatch Logs からは受けられない
- D. CloudWatch Logs のほぼリアルタイムの検索は、サブスクリプションフィルターで OpenSearch へ送る
- E. EMR 自身のログは S3 に出力できず、SSH でしか見られない

??? success "答えと解説"
    **正解: B, D**

    使い方で組み合わせます。

    - A: 誤り。Kinesis、Lambda、Firehose、OpenSearch です。
    - B: 正しい。サーバーレスで検索できます。
    - C: 誤り。送信先に指定できます。
    - D: 正しい。Firehose 経由の OpenSearch への配信は CloudWatch Logs に対応していないので、直接送ります。
    - E: 誤り。S3 に出力できます。

    **スキル:** [4.4.5](../domain4.md#skill-4-4-5) / **参照:** [データの入れ方](../../../services/streaming.md#opensearch-ingestion)、[Amazon Data Firehose](../../../services/streaming.md#firehose)

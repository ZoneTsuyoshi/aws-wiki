# CloudWatch Logsの問題集

対象の解説: [CloudWatch Logs](../../../services/observability.md#cloudwatch-logs)

### 問1 {#q1}

監査の要件で、既存のロググループをカスタマー管理の KMS キーで暗号化します。`aws logs associate-kms-key` を実行すると、`AccessDeniedException` で失敗しました。実行者のロールには `logs:AssociateKmsKey` があります。何を直しますか。

- A. キーポリシーで、リージョンの CloudWatch Logs のサービスプリンシパルに権限を与える
- B. ロググループを削除して作り直し、作成時にキーを指定できるようにする
- C. キーを非対称の RSA キーへ変更して、公開鍵を CloudWatch Logs のロググループへ登録する
- D. CloudWatch Logs の VPC エンドポイントを作り、キーへの経路を確保する

??? success "答えと解説"
    **正解: A**

    CloudWatch Logs がキーを使えるよう、キーポリシーでサービスプリンシパルを許可します。

    - A: 正しい。
    - B: 誤り。作り直してもキーポリシーの問題は同じで、ログも失う。
    - C: 誤り。ログの暗号化には対称キーを使う。
    - D: 誤り。経路の問題ではなく、権限の拒否である。

    **スキル:** [ログの暗号化](../domain4.md#t4-1-encryption) / **参照:** [KMS による暗号化](../../../services/observability.md#logs-kms)

### 問2 {#q2}

アプリのログに誤ってメールアドレスやカード番号が含まれることがあります。アプリの修正には時間がかかります。CloudWatch Logs に届いたログで、権限のない担当者には見えないようにし、検出の結果も残します。さらに、別の監査ログは AWS に届く前に暗号化します。適切な組み合わせはどれですか。

- A. 前者は KMS キーの関連付け、後者は SSE-S3
- B. 前者はログの保持期間の短縮、後者は VPC エンドポイント
- C. 前者はデータ保護ポリシー、後者はクライアント側の暗号化
- D. 前者はメトリクスフィルター、後者は TLS の API エンドポイント

??? success "答えと解説"
    **正解: C**

    データ保護ポリシーは機密情報をマスクします。AWS に届く前の暗号化はクライアント側で行います。

    - A: 誤り。KMS の関連付けは権限のある利用者には平文を見せ、SSE-S3 は届いた後の暗号化。
    - B: 誤り。保持の短縮はマスクにならず、エンドポイントも暗号化の手段ではない。
    - C: 正しい。
    - D: 誤り。フィルターはマスクせず、TLS は転送の間だけの保護。

    **スキル:** [ログの暗号化](../domain4.md#t4-1-encryption) / **参照:** [データ保護ポリシー](../../../services/observability.md#logs-data-protection)、[クライアント側とサーバー側の暗号化](../../../services/kms.md#client-vs-server-side)

### 問3 {#q3}

ログの暗号化について、担当者の説明のうち正しいものを選んでください。（2つ選択）

- A. KMS キーを無効にしても、ログの読み取りは通常どおりに続けられる
- B. ロググループに KMS キーを関連付けると、以降に取り込むログの保存が暗号化される
- C. KMS キーの関連付けを解除すれば、以前のログの暗号化も即座に解かれて平文になる
- D. エージェントから CloudWatch Logs への転送は TLS の API エンドポイントで保護される
- E. KMS キーを関連付けない限り、CloudWatch Logs のログは保存時に暗号化されない

??? success "答えと解説"
    **正解: B, D**

    キーを関連付けると、以降のデータがそのキーで暗号化されます。転送は TLS で保護されます。

    - A: 誤り。無効にすると該当のログを読めなくなる。
    - B: 正しい。
    - C: 誤り。解除で平文に戻るわけではない。
    - D: 正しい。
    - E: 誤り。既定でも保存時に暗号化されている。

    **スキル:** [ログの暗号化](../domain4.md#t4-1-encryption) / **参照:** [KMS による暗号化](../../../services/observability.md#logs-kms)、[保存時と転送時の暗号化](../../../services/kms.md#at-rest-in-transit)

### 問4 {#q4}

EC2 の CloudWatch エージェントと ECS の Fargate のタスクから、ログが届きません。どちらのアプリも正常に動いています。権限の修正の組み合わせとして正しいものはどれですか。

- A. EC2 はアクセスキーをエージェントの設定へ書き、ECS は CloudWatch Logs のリソースポリシーで許可する
- B. EC2 と ECS の両方で、KMS のキーポリシーに `logs:PutLogEvents` を追加する
- C. EC2 はサービスリンクロール、ECS はタスクロールにログの権限を付ける
- D. EC2 はインスタンスのロールに `CloudWatchAgentServerPolicy`、ECS はタスク実行ロールにログの権限を付ける

??? success "答えと解説"
    **正解: D**

    エージェントはインスタンスのロール、`awslogs` はタスク実行ロールの権限で送ります。

    - A: 誤り。長期のキーを置くことになり、`awslogs` の権限の修正にもならない。
    - B: 誤り。ログの権限はキーポリシーで与えるものではない。
    - C: 誤り。エージェントはインスタンスのロールを使い、`awslogs` はタスク実行ロールを使う。
    - D: 正しい。

    **スキル:** [ログ収集の権限](../domain4.md#t4-1-permissions) / **参照:** [CloudWatch エージェント](../../../services/operations.md#cloudwatch-agent)、[logConfiguration](../../../services/containers.md#log-configuration)

### 問5 {#q5}

VPC フローログと CloudTrail を、宛先ごとに設定します。(1) フローログを CloudWatch Logs へ送る。(2) フローログを S3 へ送る。(3) 証跡を S3 へ送る。必要な権限の組み合わせはどれですか。

- A. (1) KMS のキーポリシー、(2) VPC エンドポイントのポリシー、(3) SCP
- B. (1) IAM ロール、(2) S3 のバケットポリシー、(3) S3 のバケットポリシー
- C. (1) S3 のバケットポリシー、(2) IAM ロール、(3) IAM ロール
- D. (1) IAM ユーザーのアクセスキー、(2) ACL の公開読み取り、(3) IAM ユーザーのアクセスキー

??? success "答えと解説"
    **正解: B**

    CloudWatch Logs へはロール、S3 へはバケットポリシーで許可します。

    - A: 誤り。いずれもログを書き込む権限の仕組みではない。
    - B: 正しい。
    - C: 誤り。宛先に必要なものが入れ違っている。
    - D: 誤り。長期のキーや公開の設定は不適切で、仕組みも違う。

    **スキル:** [ログ収集の権限](../domain4.md#t4-1-permissions) / **参照:** [VPC フローログ](../../../services/networking.md#flow-logs)、[証跡とイベント履歴](../../../services/observability.md#cloudtrail-trails)

### 問6 {#q6}

全アカウントのログを、ログ保管アカウントの Kinesis Data Streams へ集めます。送信元のアカウントのサブスクリプションフィルターが作成できません。必要な設定はどれですか。（2つ選択）

- A. 送信元のアカウントに Kinesis のストリームを作り、S3 のレプリケーションで転送する
- B. 宛先ポリシーで、送信元のアカウントや組織に `PutSubscriptionFilter` を許可する
- C. ログ保管アカウントで `PutDestination` で論理的な宛先を作り、Kinesis への書き込みを許可するロールを指定する
- D. 各ロググループに、ログ保管アカウントの KMS キーを関連付ける
- E. 送信元の全 Lambda の実行ロールに `kinesis:PutRecord` を追加する

??? success "答えと解説"
    **正解: B, C**

    アカウントをまたぐ配信は、宛先アカウントの論理的な宛先と宛先ポリシーで許可します。

    - A: 誤り。仕組みが別で、集約の構成にならない。
    - B: 正しい。
    - C: 正しい。
    - D: 誤り。暗号化の設定で、配信の権限ではない。
    - E: 誤り。サブスクリプションの配信はアプリのロールを使わない。

    **スキル:** [ログ収集の権限](../domain4.md#t4-1-permissions) / **参照:** [サブスクリプションフィルターの設定](../../../services/observability.md#subscription-settings)

### 問7 {#q7}

アプリのログの ERROR を数えるメトリクスフィルターを今日作りました。先週の障害の回数を確認したいのに、グラフが空です。何が原因で、先週の分はどう調べますか。

- A. 名前空間が `AWS/Logs` でないので見えない。名前空間を変更して作り直す
- B. フィルターは作成後のログだけを処理する。先週の分は Logs Insights で集計する
- C. ログの保持期間が短いので見えない。保持を延ばせば先週の分が再計算される
- D. メトリクスの解像度が 1 分なので見えない。高解像度に変更すれば先週の分も自動で再計算されて表示される

??? success "答えと解説"
    **正解: B**

    メトリクスフィルターは作成後のログだけを対象にします。

    - A: 誤り。名前空間は過去の処理に関係しない。
    - B: 正しい。
    - C: 誤り。保持に関係なく過去へさかのぼらない。
    - D: 誤り。解像度の問題ではない。

    **スキル:** [メトリクスフィルター](../domain4.md#t4-1-metric-filters) / **参照:** [メトリクスフィルター](../../../services/observability.md#metric-filters)

### 問8 {#q8}

JSON 形式のログの `latencyMs` の値をカスタムメトリクスにして、`status` が 500 のログも別に数えます。適切なフィルターパターンと設定の組み合わせはどれですか。

- A. Logs Insights のクエリをメトリクスフィルターへ貼り付けて、1 分ごとに実行する
- B. `{ $.latencyMs >= 0 }` で値に `$.latencyMs`、`{ $.status = 500 }` で値に 1 を指定する別々のフィルター
- C. 1 つのパターン `"latencyMs" "500"` でまとめて、メトリクスの値を 1 にする
- D. `[ip, user, status=500]` の 1 つのパターンでメトリクスの値に `$latencyMs` を指定する

??? success "答えと解説"
    **正解: B**

    JSON の項目は `$.項目` で指定し、メトリクスの値に項目の値を使えます。

    - A: 誤り。Insights の構文はフィルターパターンではない。
    - B: 正しい。
    - C: 誤り。文字列の一致で値を取れず、2 つのメトリクスにも分かれない。
    - D: 誤り。スペース区切りの形式で、JSON の値を扱えない。

    **スキル:** [メトリクスフィルター](../domain4.md#t4-1-metric-filters) / **参照:** [メトリクスフィルターの設定](../../../services/observability.md#metric-filter-settings)、[構造化ログ](../../../services/observability.md#structured-logging)

### 問9 {#q9}

ERROR の数のメトリクスフィルターにアラームを付けました。ERROR がない時間はデータが発行されず、アラームが `INSUFFICIENT_DATA` のままで、復旧の通知も届きません。修正の組み合わせはどれですか。（2つ選択）

- A. メトリクスフィルターのデフォルト値を 0 に設定する
- B. ログの保持期間を 1 日に短くして、古いデータをなくす
- C. 高解像度のメトリクスに変えて、1 秒ごとに発行する
- D. アラームの `treatMissingData` を `notBreaching` に設定する
- E. メトリクスの統計を `Average` から `p99` に変える

??? success "答えと解説"
    **正解: A, D**

    デフォルト値を指定すると一致がない期間に 0 が発行されます。欠落の扱いもアラームで指定できます。

    - A: 正しい。
    - B: 誤り。メトリクスのデータの欠落とは関係ない。
    - C: 誤り。ERROR がなければ発行されない点は同じ。
    - D: 正しい。
    - E: 誤り。欠落の扱いは変わらない。

    **スキル:** [メトリクスフィルター](../domain4.md#t4-1-metric-filters) / **参照:** [メトリクスフィルターの設定](../../../services/observability.md#metric-filter-settings)、[欠落データの扱い](../../../services/observability.md#treat-missing-data)

### 問10 {#q10}

CloudWatch Logs の費用が増え続けています。調べると、Lambda や ECS が自動で作るロググループの保持期間が無期限のままです。今後も含めて保持の基準を守らせ、違反を検知します。適切な構成はどれですか。

- A. ロググループの KMS キーを無効にすれば、古いログが保持の設定に関係なく自動で削除される
- B. ログクラスを変えるだけで、保持期間を自動で短くする
- C. IaC で保持期間を指定し、Config のルールで違反を検出して修復する
- D. 毎月の担当者の作業で、全ロググループの一覧を確認して保持を手で変更する

??? success "答えと解説"
    **正解: C**

    既定は無期限です。作成時に指定し、Config のルールで確認します。

    - A: 誤り。無効にしても削除されない。
    - B: 誤り。ログクラスは保持期間を自動で短くしない。
    - C: 正しい。
    - D: 誤り。手作業に頼り、新しいものへの適用も遅れる。

    **スキル:** [ライフサイクル](../domain4.md#t4-1-lifecycle) / **参照:** [保持期間の設定](../../../services/observability.md#log-retention)、[Config ルール](../../../services/governance.md#config-rules)

### 問11 {#q11}

ログの保存方針は次のとおりです。CloudWatch Logs では 30 日だけ検索し、その後は S3 に 7 年残します。最初の 90 日より後はほとんど読みません。ログの一部には Live Tail やメトリクスフィルターが不要なものがあり、費用を抑えます。適切な組み合わせはどれですか。

- A. 不要な分は低コストのログクラスに置き、S3 はライフサイクルで Glacier へ移して 7 年で削除する
- B. S3 の Standard に 7 年置いて、CloudWatch Logs の保持は無期限にする
- C. すべて無期限の Standard のログクラスに置き、S3 には送らない
- D. すべて `CreateExportTask` で毎時間 S3 へ送り、CloudWatch Logs のロググループは削除する

??? success "答えと解説"
    **正解: A**

    機能が要らないログは低コストのログクラスが向きます。S3 はライフサイクルで移します。

    - A: 正しい。
    - B: 誤り。費用の抑制にならない。
    - C: 誤り。費用が増え続け、方針に合わない。
    - D: 誤り。リアルタイムの検索ができなくなる。

    **スキル:** [ライフサイクル](../domain4.md#t4-1-lifecycle) / **参照:** [ログクラス](../../../services/observability.md#log-classes)、[ライフサイクル](../../../services/s3.md#lifecycle)

### 問12 {#q12}

ログを継続して S3 へ送り、S3 で 7 年保管します。担当者は 1 時間ごとに `CreateExportTask` を実行する案を出しました。遅れを小さくして、運用の手間も減らします。適切な案はどれですか。

- A. サブスクリプションフィルターと Firehose で S3 へ流す
- B. CloudWatch Logs の保持期間を 7 年にすれば S3 へ自動で複製される
- C. `CreateExportTask` の間隔を 1 分に短くして EventBridge で実行する
- D. Athena のクエリの結果を、S3 のロググループとして登録する

??? success "答えと解説"
    **正解: A**

    `CreateExportTask` はリアルタイムではありません。継続して送るならサブスクリプションフィルターと Firehose です。

    - A: 正しい。
    - B: 誤り。保持期間の設定で S3 へ複製されない。
    - C: 誤り。エクスポートはリアルタイムの配信の仕組みではない。
    - D: 誤り。ログの継続の配信にならない。

    **スキル:** [ライフサイクル](../domain4.md#t4-1-lifecycle) / **参照:** [S3 へのエクスポート](../../../services/observability.md#logs-export)、[Amazon Data Firehose](../../../services/streaming.md#firehose)

### 問13 {#q13}

監査のログを、ほぼリアルタイムで検索基盤へ、同時に別の担当の Lambda へも送ります。受け取る Lambda で、データを読めないというエラーが出ています。データの扱いとして正しいものはどれですか。

- A. データはロググループの KMS キーで暗号化されているので、`kms:Decrypt` の権限を関数へ追加する
- B. データは Base64 でエンコードされ gzip で圧縮されているので、両方を戻して処理する
- C. データは S3 のキーだけが届くので、関数で `GetObject` を呼ぶ
- D. データはそのまま JSON なので、関数のタイムアウトを延ばす

??? success "答えと解説"
    **正解: B**

    サブスクリプションフィルターのデータは Base64 と gzip でエンコードされています。

    - A: 誤り。サブスクリプションのペイロードの形式の問題で、復号の問題ではない。
    - B: 正しい。
    - C: 誤り。S3 のイベントと混同している。
    - D: 誤り。Base64 と gzip の処理が必要で、タイムアウトの問題でもない。

    **スキル:** [サブスクリプション](../domain4.md#t4-1-subscriptions) / **参照:** [サブスクリプションフィルター](../../../services/observability.md#subscription-filters)

### 問14 {#q14}

全アカウントのログを中央へ集めて、(1) S3 へ配信する、(2) 複数のコンシューマーが順序を保って読み、独自の処理をする、の 2 つのパイプラインを作ります。サブスクリプションの宛先の組み合わせはどれですか。

- A. (1) SQS、(2) EventBridge
- B. (1) Lambda、(2) SNS
- C. (1) Firehose、(2) Kinesis Data Streams
- D. (1) Kinesis Data Streams と Lambda、(2) Firehose の動的パーティショニング

??? success "答えと解説"
    **正解: C**

    S3 などへの配信は Firehose、複数のコンシューマーや独自の処理は Kinesis Data Streams です。

    - A: 誤り。どちらもサブスクリプションフィルターの宛先ではない。
    - B: 誤り。SNS はサブスクリプションフィルターの宛先ではない。
    - C: 正しい。
    - D: 誤り。用途が逆になっている。

    **スキル:** [サブスクリプション](../domain4.md#t4-1-subscriptions) / **参照:** [サブスクリプションフィルターの設定](../../../services/observability.md#subscription-settings)、[Kinesis Data Streams、Firehose、SQS の選び方](../../../services/streaming.md#choosing)

### 問15 {#q15}

あるロググループで、ERROR のログだけをリアルタイムに OpenSearch Service へ送り、検索と可視化を行います。全ログを転送する費用は避けます。運用する部品も少なくします。適切な構成はどれですか。

- A. フィルターパターンを `ERROR` にしたサブスクリプションフィルターを OpenSearch へ向ける
- B. `CreateExportTask` で 5 分ごとに S3 へ送り、Lambda で OpenSearch へ投入する
- C. すべてのログを Kinesis へ送り、OpenSearch の中のクエリで ERROR を抽出する
- D. メトリクスフィルターで ERROR を数えて、OpenSearch の可視化へ数値だけ送る

??? success "答えと解説"
    **正解: A**

    サブスクリプションフィルターにパターンを指定すると、一致するログだけが配信されます。

    - A: 正しい。
    - B: 誤り。リアルタイムではなく、部品も増える。
    - C: 誤り。全ログの転送の費用がかかる。
    - D: 誤り。ログの本文が届かず、検索に使えない。

    **スキル:** [サブスクリプション](../domain4.md#t4-1-subscriptions) / **参照:** [サブスクリプションフィルターの設定](../../../services/observability.md#subscription-settings)、[Amazon OpenSearch Service](../../../services/streaming.md#opensearch)

### 問16 {#q16}

複数の Lambda のロググループで、過去 24 時間の ERROR を 5 分ごとに数え、多い順に見ます。費用を抑えます。適切なものはどれですか。

- A. 全ロググループを毎回 S3 へエクスポートして、Athena で集計する
- B. Logs Insights で `filter @message like /ERROR/ | stats count(*) by bin(5m)` を、対象と時間を絞って実行する
- C. Live Tail を 24 時間開いて、画面に流れる ERROR を目で数える
- D. メトリクスフィルターを今から作り、24 時間待ってからグラフで確認する

??? success "答えと解説"
    **正解: B**

    その場の集計には Logs Insights が向きます。ロググループと時間を絞ると費用を抑えられます。

    - A: 誤り。手間と時間がかかり、この調査には過剰。
    - B: 正しい。
    - C: 誤り。過去を見られず、集計にもならない。
    - D: 誤り。過去 24 時間のログは対象にならない。

    **スキル:** [ログの検索](../domain4.md#t4-1-search) / **参照:** [Logs Insights でログを検索する](../../../services/observability.md#logs-insights)、[コマンドの詳細](../../../services/observability.md#insights-commands)

### 問17 {#q17}

次の調査で手段を選びます。(1) スペース区切りのアクセスログで、ステータスが 5xx の行を対象にメトリクスを作る。(2) 今デプロイした新しい版のログを、流れるままに見る。適切な組み合わせはどれですか。

- A. (1) `{ $.status = 5* }`、(2) Athena
- B. (1) Contributor Insights、(2) X-Ray のサービスマップ
- C. (1) `stats count(*) by status`、(2) `CreateExportTask`
- D. (1) `[ip, user, timestamp, request, status_code = 5*, size]`、(2) Live Tail

??? success "答えと解説"
    **正解: D**

    スペース区切りの形式は角かっこのパターンです。リアルタイムに見るなら Live Tail です。

    - A: 誤り。JSON の構文でスペース区切りに合わず、Athena はリアルタイムでない。
    - B: 誤り。目的が違う。
    - C: 誤り。Insights の構文でメトリクスフィルターではなく、エクスポートは見るための手段ではない。
    - D: 正しい。

    **スキル:** [ログの検索](../domain4.md#t4-1-search) / **参照:** [メトリクスフィルターの設定](../../../services/observability.md#metric-filter-settings)、[Live Tail](../../../services/observability.md#live-tail)

### 問18 {#q18}

3 年分の VPC フローログと ALB のアクセスログは S3 にあります。別途、直近 2 週間のアプリのログは CloudWatch Logs にあります。一度の調査で、それぞれをどう問い合わせますか。

- A. S3 のログは Athena、CloudWatch Logs のログは Logs Insights
- B. どちらも Logs Insights で問い合わせる。S3 のログも自動で検索の対象に入る
- C. どちらも Athena で問い合わせる。CloudWatch Logs のログも自動で S3 にある
- D. どちらも Live Tail を使って、3 年分を画面に流す

??? success "答えと解説"
    **正解: A**

    対象の場所で手段を選びます。S3 の長期のログは Athena、CloudWatch Logs は Logs Insights です。

    - A: 正しい。
    - B: 誤り。Logs Insights の対象は CloudWatch Logs。
    - C: 誤り。自動では S3 にない。
    - D: 誤り。Live Tail は現在のログを見るもの。

    **スキル:** [ログの検索](../domain4.md#t4-1-search) / **参照:** [S3 上のログを問い合わせる](../../../services/streaming.md#athena-logs)、[Logs Insights でログを検索する](../../../services/observability.md#logs-insights)

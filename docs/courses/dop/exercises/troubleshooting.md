# X-Ray と障害の調査の問題集

対象の解説: [X-Ray と障害の調査](../../../services/observability.md#debugging)

### 問1 {#q1}

新規に作る ECS の API に、リクエストのトレースを入れます。既存の X-Ray の画面も使い続けます。2026 年の状況で、新しい計装として推奨されるものはどれですか。

- A. X-Ray SDK を新たに導入して、デーモンをサイドカーで動かす
- B. CloudTrail のデータイベントで、リクエストの経路を追跡する
- C. OpenTelemetry（ADOT）で計装し、CloudWatch エージェントか Collector で送る
- D. アプリのログに `traceId` を手で出力して、Logs Insights で結合する

??? success "答えと解説"
    **正解: C**

    新しい計装では OpenTelemetry（ADOT）が推奨です。トレースの保存先としての X-Ray は使えます。

    - A: 誤り。SDK とデーモンはメンテナンスモードで、新しい計装の推奨ではない。
    - B: 誤り。リクエストのトレースにならない。
    - C: 正しい。
    - D: 誤り。計装の仕組みを自作することになる。

    **スキル:** [X-Ray](../domain4.md#t4-2-xray) / **参照:** [X-Ray デーモン](../../../services/observability.md#xray-daemon)、[SDK と OpenTelemetry（現在の推奨）](../../../services/observability.md#xray-opentelemetry)

### 問2 {#q2}

API Gateway と Lambda の間のトレースが表示されません。API Gateway から先が途切れています。有効にするものの組み合わせはどれですか。（2つ選択）

- A. API Gateway の実行ログを `INFO` で有効にする
- B. Lambda のアクティブトレースと実行ロールの権限
- C. API Gateway のステージのトレース
- D. Lambda に X-Ray デーモンのレイヤーを追加する
- E. CloudWatch Logs のサブスクリプションで API のログを X-Ray へ送る

??? success "答えと解説"
    **正解: B, C**

    ステージでトレースを有効にし、Lambda はアクティブトレースと権限を設定します。

    - A: 誤り。ログの設定で、トレースは生成されない。
    - B: 正しい。
    - C: 正しい。
    - D: 誤り。Lambda はアクティブトレースで実行環境が送信するので不要。
    - E: 誤り。サブスクリプションの宛先に X-Ray はない。

    **スキル:** [X-Ray](../domain4.md#t4-2-xray) / **参照:** [Lambda のアクティブトレース](../../../services/observability.md#lambda-active-tracing)、[API Gateway での有効化](../../../services/observability.md#xray-apigateway)

### 問3 {#q3}

秒間 2,000 件の API で、全リクエストのトレースの費用が高くなっています。障害の調査では顧客 ID で検索したいのに、該当のトレースを見つけられません。エラーの調査に必要な割合は残します。適切な組み合わせはどれですか。

- A. 顧客 ID をメタデータに入れて、サンプリングを 100% にする
- B. 顧客 ID を HTTP のレスポンスヘッダーに入れて、サンプリングを無効にする
- C. ログに顧客 ID を出力して、トレースはすべて止める
- D. 顧客 ID をアノテーションに入れて、サンプリングのルールで調整する

??? success "答えと解説"
    **正解: D**

    検索に使う値はアノテーションに入れます。費用はサンプリングで調整します。

    - A: 誤り。メタデータはインデックスされず、費用も減らない。
    - B: 誤り。検索の対象にならず、費用の要件にも合わない。
    - C: 誤り。トレースの機能を失う。
    - D: 正しい。

    **スキル:** [X-Ray](../domain4.md#t4-2-xray) / **参照:** [アノテーションとメタデータ](../../../services/observability.md#annotations-metadata)、[サンプリング](../../../services/observability.md#xray-sampling)

### 問4 {#q4}

午後から API が遅くなりました。次の問いに答える手段を選びます。(1) いつからどれくらい悪いか。(2) 呼び出しのどの区間で遅いか。(3) 誰がいつ設定を変更したか。適切な組み合わせはどれですか。

- A. (1) CloudTrail の管理イベント、(2) CloudWatch メトリクス、(3) X-Ray のトレース
- B. (1) AWS Config、(2) CloudTrail、(3) CloudWatch Logs
- C. (1) CloudWatch メトリクス、(2) X-Ray、(3) CloudTrail
- D. (1) AWS Health、(2) Trusted Advisor、(3) AWS Config

??? success "答えと解説"
    **正解: C**

    メトリクスはいつどれくらい、トレースはどこで、CloudTrail は誰がです。

    - A: 誤り。手がかりと問いが入れ違っている。
    - B: 誤り。問いに合わない。
    - C: 正しい。
    - D: 誤り。AWS Health は自社の変化の量を示さず、Trusted Advisor はトレースではない。Config も主体の確認には CloudTrail が向く。

    **スキル:** [メトリクスとログ](../domain5.md#t5-3-observability) / **参照:** [メトリクス、ログ、トレースの読み解き](../../../services/observability.md#interpret-signals)、[Config と CloudTrail の違い](../../../services/governance.md#config-vs-cloudtrail)

### 問5 {#q5}

マイクロサービスの呼び出しで、エラーの発生元が分かりません。サービスマップで見ると、サービス A から B への接続は赤く、B から DynamoDB は正常です。B のログにはリクエストが届いていません。何が考えられますか。

- A. DynamoDB のスロットリングが原因で、B がエラーを返している
- B. CloudTrail の証跡が停止しているので、B のログが書かれない
- C. X-Ray のサンプリングが原因で、B のログが書かれない
- D. A と B の間の経路、セキュリティグループ、ターゲットの異常

??? success "答えと解説"
    **正解: D**

    リクエストが届かないなら、呼び出しの間の経路や受け口を確認します。

    - A: 誤り。B から DynamoDB は正常で、リクエストも B に届いていない。
    - B: 誤り。CloudTrail はアプリのログを書かない。
    - C: 誤り。サンプリングはログの出力を止めない。
    - D: 正しい。

    **スキル:** [メトリクスとログ](../domain5.md#t5-3-observability) / **参照:** [サービスマップの読み方](../../../services/observability.md#service-map)、[サービス統合の問題を調べる](../../../services/observability.md#debug-integration)

### 問6 {#q6}

Lambda の呼び出しの一部が遅いことが分かりました。`Duration` の平均は正常ですが、p99 が悪化しています。ログで遅い呼び出しの特徴を見つけます。適切な手順はどれですか。（2つ選択）

- A. CloudTrail のデータイベントで遅い呼び出しの時間を計測する
- B. パーセンタイルの統計で p99 を確認して、外れ値を見る
- C. Logs Insights で `@duration` の遅いログの項目を調べる
- D. メトリクスの統計を `Average` のままにして、期間を短くする
- E. 関数の予約済み同時実行を増やして、遅い呼び出しをなくす

??? success "答えと解説"
    **正解: B, C**

    平均では外れ値が隠れます。パーセンタイルとログで調べます。

    - A: 誤り。処理時間の分析の手段ではない。
    - B: 正しい。
    - C: 正しい。
    - D: 誤り。平均では外れ値が隠れたままになる。
    - E: 誤り。調査の手順ではなく、遅い呼び出しの特徴は分からない。

    **スキル:** [メトリクスとログ](../domain5.md#t5-3-observability) / **参照:** [ログからボトルネックを見つける](../../../services/observability.md#logs-bottlenecks)、[代表的なメトリクスと原因](../../../services/observability.md#bottleneck-metrics)

### 問7 {#q7}

本番のアプリのエラーが 10 時から増えました。当日の変更はありません。AWS 側の障害の影響かを最初に確かめ、自社のリソースが受ける影響も確認します。どこを見ますか。

- A. CloudWatch のメトリクスだけで AWS の障害の有無を判断する
- B. AWS Health Dashboard の自社に関連するイベント
- C. Trusted Advisor のサービスの制限のチェックで、障害の有無を判断する
- D. CloudTrail のイベント履歴で API のエラーの増加を確認する

??? success "答えと解説"
    **正解: B**

    AWS Health は AWS 側の障害が自分のリソースに影響するかを示します。

    - A: 誤り。自社のリソースの値で、AWS 側の障害情報は分からない。
    - B: 正しい。
    - C: 誤り。クォータの使用状況で、障害の情報ではない。
    - D: 誤り。自社の API の記録で、AWS 側の障害かは分からない。

    **スキル:** [サービスの状態](../domain5.md#t5-3-service-health) / **参照:** [AWS Health Dashboard](../../../services/cloud-foundations.md#health)、[2026 年 10 月時点の提供状況](../../../services/operations.md#status)

### 問8 {#q8}

運用チームが、アラームと Config の変更、Trusted Advisor の警告を別々の画面で調査しています。担当者の割り当てと対応の履歴を 1 か所に残し、関連の情報からランブックも実行します。新しく導入する運用の基盤として、適切なものはどれですか。

- A. OpsCenter の OpsItem
- B. DevOps Guru の異常の検知を新規に有効にする
- C. Incident Manager のレスポンスプランを新規に作る
- D. CloudTrail Lake のイベントデータストアを新規に作る

??? success "答えと解説"
    **正解: A**

    OpsCenter は運用の課題を OpsItem で一か所に集め、関連する情報を確認し、ランブックも実行できます。

    - A: 正しい。
    - B: 誤り。新規受付を終了している。
    - C: 誤り。新規受付を終了している。
    - D: 誤り。新規受付を終了している。

    **スキル:** [サービスの状態](../domain5.md#t5-3-service-health) / **参照:** [OpsCenter](../../../services/operations.md#opscenter)

### 問9 {#q9}

次の説明のうち、正しいものを選んでください。（2つ選択）

- A. AWS Health のイベントはメールでしか受け取れない
- B. CloudWatch は自分のリソースのメトリクスを示し、AWS 側の障害情報は示さない
- C. OpsCenter は AWS の全顧客の障害の状況を一覧で示す
- D. CloudWatch のアラームがなければ AWS Health のイベントは発生しない
- E. AWS Health はアカウントに関連する障害や予定されたメンテナンスを示す

??? success "答えと解説"
    **正解: B, E**

    手がかりごとに見られる範囲が違います。

    - A: 誤り。EventBridge でも受けられる。
    - B: 正しい。
    - C: 誤り。自社の運用の課題を集めるサービス。
    - D: 誤り。別の仕組み。
    - E: 正しい。

    **スキル:** [サービスの状態](../domain5.md#t5-3-service-health) / **参照:** [AWS Health Dashboard](../../../services/cloud-foundations.md#health)、[CloudWatch メトリクス](../../../services/observability.md#cloudwatch-metrics)、[OpsCenter](../../../services/operations.md#opscenter)

### 問10 {#q10}

14 時から本番の API で 5xx が増えました。午前中にデプロイが 2 回あり、同じ時間帯に別のチームがネットワークの設定も変更しています。再起動で一時的に直る可能性もあります。調査の順番として最も適切なものはどれですか。

- A. 影響の範囲と時刻を確認し、その時刻の変更、ログとトレース、AWS Health の順に調べる
- B. まず全インスタンスを再起動して、改善するか確認する
- C. まずアプリを別のリージョンへ移し、後で原因を確認する
- D. まず AWS サポートへ連絡して回答を待ち、回答があるまでログとメトリクスの確認は保留にする

??? success "答えと解説"
    **正解: A**

    影響の範囲と開始の時刻から始め、変更を調べ、失敗の場所を絞り、AWS 側の問題を除外します。

    - A: 正しい。
    - B: 誤り。手がかりを消すおそれがあり、原因が分からない。
    - C: 誤り。根拠のない大きな変更で、原因の特定にならない。
    - D: 誤り。自社の調査が遅れる。

    **スキル:** [根本原因](../domain5.md#t5-3-root-cause) / **参照:** [デバッグとエラー診断](../../../services/observability.md#debugging)、[Config と CloudTrail の違い](../../../services/governance.md#config-vs-cloudtrail)

### 問11 {#q11}

14 時 02 分に `HTTPCode_Target_5XX_Count` が増えました。CodeDeploy の履歴では 13 時 58 分にデプロイがあり、X-Ray では新しい版の DynamoDB の呼び出しに失敗が出ています。AWS Health には関連のイベントはありません。根本原因の判断と恒久の対策はどれですか。

- A. 新しい版が原因で、戻した上で権限やスキーマを確認するテストとデプロイのアラームを追加する
- B. AWS の DynamoDB の障害なので、AWS Health の更新を待たずに別のリージョンへ切り替える
- C. ALB の障害なので、NLB へ置き換える
- D. 容量の不足なので、Auto Scaling の最大を増やして終える

??? success "答えと解説"
    **正解: A**

    時刻の一致と X-Ray から原因は新しい版です。再発の防止をテストとアラームに反映します。

    - A: 正しい。
    - B: 誤り。AWS Health にイベントがなく、根拠がない。
    - C: 誤り。`Target` のメトリクスが増えており、アプリ側の問題。
    - D: 誤り。新しい版の失敗を説明できない。

    **スキル:** [根本原因](../domain5.md#t5-3-root-cause) / **参照:** [デプロイ失敗の診断](../../../services/cicd.md#troubleshooting-deployments)、[X-Ray によるトレース](../../../services/observability.md#xray)

### 問12 {#q12}

夜間のバッチで RDS の接続エラーが毎週木曜に起きます。都度の再実行で直っており、担当者は再実行の自動化だけで済ませようとしています。根本原因の分析として適切なものはどれですか。

- A. インスタンスクラスをすぐに 2 倍にして、改善がなければ元に戻す作業を次の木曜に繰り返す
- B. 木曜の同時刻の変更やメンテナンス、接続数のメトリクス、他のジョブとの重なりを調べる
- C. 再実行の Lambda を追加して、エラーの通知を止める
- D. バッチを木曜だけ止める運用を恒久にする

??? success "答えと解説"
    **正解: B**

    症状に対処するだけでなく、周期の手がかりから原因を調べて再発を防ぎます。

    - A: 誤り。根拠のない変更で、原因が分からない。
    - B: 正しい。
    - C: 誤り。症状への対処だけで、原因が残る。
    - D: 誤り。業務への影響が残り、原因も分からない。

    **スキル:** [根本原因](../domain5.md#t5-3-root-cause) / **参照:** [代表的なエラーコード](../../../services/observability.md#error-codes)、[デバッグとエラー診断](../../../services/observability.md#debugging)

### 問13 {#q13}

CloudFormation の更新が失敗し、多数のイベントが `UPDATE_FAILED` と `Resource update cancelled` を示しています。原因を調べるにはどこを見ますか。また、`UPDATE_ROLLBACK_FAILED` で止まったら、手で削除したリソースが原因の場合はどうしますか。

- A. ドリフト検出で差分を確認し、スタックの状態を手で `UPDATE_COMPLETE` に変更する
- B. 最初の失敗の理由を読み、`continue-update-rollback` を実行する（必要なら `--resources-to-skip`）
- C. 最後のイベントの理由を読み、スタックを削除して同じテンプレートから作り直す
- D. CloudTrail の全イベントを読み、`UPDATE_ROLLBACK_FAILED` の解除を AWS サポートに依頼して回答を待ち、その間は更新を止める

??? success "答えと解説"
    **正解: B**

    最初の失敗の理由を読みます。`UPDATE_ROLLBACK_FAILED` は原因を直して `continue-update-rollback` です。

    - A: 誤り。ドリフト検出は状態を変更しない。
    - B: 正しい。
    - C: 誤り。後の失敗はロールバックなどの結果で、原因は最初の失敗にある。削除も過剰。
    - D: 誤り。最初の手がかりはスタックイベントで、自分で復旧できる。

    **スキル:** [失敗したデプロイ](../domain5.md#t5-3-failed-deployments) / **参照:** [スタックのロールバックと失敗](../../../services/iac.md#stack-failures)、[よくある失敗と対処](../../../services/iac.md#common-failures)

### 問14 {#q14}

次の失敗の最初の確認先を選びます。(1) CodeBuild が `BUILD` フェーズで失敗した。(2) CodeDeploy の `ApplicationStart` のスクリプトが失敗した。(3) CodePipeline の GitHub のソースアクションが失敗した。適切な組み合わせはどれですか。

- A. (1) AWS Health、(2) CloudWatch のアラームの履歴、(3) CodePipeline の Webhook の設定
- B. (1) ビルドログのフェーズの詳細、(2) デプロイのイベントと `scripts.log`、(3) 接続の状態と実行の履歴
- C. (1) X-Ray のトレース、(2) CloudTrail のイベント、(3) AWS Config の設定履歴
- D. (1) スタックイベント、(2) ターゲットグループの状態、(3) Route 53 のヘルスチェック

??? success "答えと解説"
    **正解: B**

    失敗したサービスの詳細から見ます。

    - A: 誤り。いずれも失敗の詳細が書かれた最初の確認先ではない。
    - B: 正しい。
    - C: 誤り。最初の確認先にならない。
    - D: 誤り。どれも対象が違う。

    **スキル:** [失敗したデプロイ](../domain5.md#t5-3-failed-deployments) / **参照:** [デプロイ失敗の診断](../../../services/cicd.md#troubleshooting-deployments)、[ログ](../../../services/cicd.md#build-logs)

### 問15 {#q15}

デプロイは正常に完了しますが、ログインの画面が壊れていることに利用者の報告で気づきました。デプロイの後の異常を自動で検知して、自動で戻します。適切な構成はどれですか。

- A. デプロイのフックで一度だけログインの画面を `curl` で確認し、完了後の監視は行わない
- B. CloudWatch RUM の画面を担当者が毎日確認し、異常が見えたら手で前の版へ戻す
- C. Synthetics のカナリアのアラームを CodeDeploy の自動ロールバックにつなぐ
- D. ALB のヘルスチェックのパスをログインの画面へ変えて、全台を新しい版のまま順に入れ替える

??? success "答えと解説"
    **正解: C**

    カナリアのアラームを CodeDeploy やステージ条件につなぐと、失敗したときに自動で戻せます。

    - A: 誤り。デプロイの時点だけの確認で、後の異常を検知しない。
    - B: 誤り。自動にならず、発見が遅い。
    - C: 正しい。
    - D: 誤り。全台が異常と判定され、原因の版への切り戻しにならない。

    **スキル:** [失敗したデプロイ](../domain5.md#t5-3-failed-deployments) / **参照:** [CloudWatch Synthetics](../../../services/operations.md#synthetics)、[CodeDeploy のロールバック](../../../services/cicd.md#codedeploy-rollback)

### 問16 {#q16}

Auto Scaling グループで新しいインスタンスが起動しません。`describe-scaling-activities` に `Client.InternalError` と KMS の鍵の状態の問題が出ています。起動テンプレートの EBS はカスタマー管理キーで暗号化されています。何を直しますか。

- A. インスタンスプロファイルに `kms:Decrypt` を許可する
- B. Auto Scaling のサービスリンクロールにキーの使用を許可する
- C. Auto Scaling グループのヘルスチェックの種類を ELB に変える
- D. グループの希望する容量を増やし、起動の再試行を増やす

??? success "答えと解説"
    **正解: B**

    起動できないのは容量、上限、キーの権限が典型です。

    - A: 誤り。暗号化されたボリュームの起動に使うのは Auto Scaling のサービスリンクロールで、インスタンスのロールではない。
    - B: 正しい。
    - C: 誤り。起動の後の判定で、起動の失敗に関係がない。
    - D: 誤り。キーの権限の問題は再試行では直らない。

    **スキル:** [プロセスの障害](../domain5.md#t5-3-failed-processes) / **参照:** [スケーリングの失敗の調査](../../../services/operations.md#asg-troubleshooting)

# コスト管理ツールの問題集

対象の解説: [コスト管理](../../../services/cost-management.md)

### 問1 {#q1}

過去 12 か月の S3 の費用の推移をグラフで確認し、来月の予測を見ます。どれを使いますか。

- A. Budgets
- B. Config のリソースの履歴
- C. Cost Explorer の推移と予測
- D. CloudTrail の証跡のログを集計する

??? success "答えと解説"
    **正解: C**

    Cost Explorer は過去の費用の分析と予測です。

    - A: 誤り。しきい値での動作の設定で、推移の分析ではない。
    - B: 誤り。設定の履歴。
    - C: 正しい。
    - D: 誤り。API の記録で、費用の分析ではない。

    **スキル:** [コスト管理ツール](../domain4.md#t4-1-cost-tools) / **参照:** [Cost Explorer](../../../services/cost-management.md#cost-explorer)

### 問2 {#q2}

S3 の月額がしきい値を超えそうなときに通知します。どれを使いますか。

- A. Budgets の実績と予測のアラート
- B. S3 Storage Lens
- C. Cost Explorer のレポートを毎日手で確認する
- D. Compute Optimizer の推奨を確認する

??? success "答えと解説"
    **正解: A**

    Budgets は実績や予測に基づいて通知します。

    - A: 正しい。
    - B: 誤り。使用状況の可視化で、費用の通知ではない。
    - C: 誤り。手作業で、通知しない。
    - D: 誤り。適正なサイズの推奨。

    **スキル:** [コスト管理ツール](../domain4.md#t4-1-cost-tools) / **参照:** [AWS Budgets](../../../services/cost-management.md#budgets)

### 問3 {#q3}

部門ごとの S3 の費用を請求データで分けます。バケットにタグ `Department` を付けましたが、Cost Explorer に出てきません。何が足りませんか。

- A. CloudWatch の請求アラームの作成
- B. コスト配分タグの有効化
- C. バケットのバージョニングの有効化
- D. Organizations のメンバーアカウントの作成

??? success "答えと解説"
    **正解: B**

    コスト配分タグは、付けるだけではなく有効化が必要です。

    - A: 誤り。通知の機能。
    - B: 正しい。
    - C: 誤り。関係ない。
    - D: 誤り。タグの分類には必須ではない。

    **スキル:** [コスト管理ツール](../domain4.md#t4-1-cost-tools) / **参照:** [コスト配分タグ](../../../services/cost-management.md#cost-allocation-tags)

### 問4 {#q4}

複数アカウントの Savings Plans の使用率が目標を下回ったら通知します。どれを使いますか。

- A. Trusted Advisor の無料のコアチェック
- B. CloudWatch の `CPUUtilization`
- C. Cost and Usage Report を毎週ダウンロードする
- D. Savings Plans の使用率の予算（Budgets）

??? success "答えと解説"
    **正解: D**

    Budgets には使用率やカバレッジの予算があります。

    - A: 誤り。使用率の通知の機能ではない。
    - B: 誤り。CPU の指標。
    - C: 誤り。通知しない。
    - D: 正しい。

    **スキル:** [コンピューティングの費用](../domain4.md#t4-2-tools) / **参照:** [予算の種類](../../../services/cost-management.md#budget-types)

### 問5 {#q5}

どのインスタンスがサイズ過剰かを、機械学習で分析した推奨で確認します。どれを使いますか。

- A. Compute Optimizer
- B. Budgets のアクション
- C. AWS Artifact のレポート
- D. Cost Anomaly Detection

??? success "答えと解説"
    **正解: A**

    Compute Optimizer は使用状況からサイズの推奨を出します。

    - A: 正しい。
    - B: 誤り。しきい値での動作。
    - C: 誤り。監査の報告書。
    - D: 誤り。費用の異常の検出。

    **スキル:** [コンピューティングの費用](../domain4.md#t4-2-tools) / **参照:** [Compute Optimizer と適正サイズ](../../../services/cost-management.md#compute-optimizer)、[推奨を出すサービスの違い](../../../services/cost-management.md#recommendation-tools)

### 問6 {#q6}

一括請求の利点として正しいものを選んでください。（2つ選択）

- A. 各アカウントの IAM ポリシーを自動で統一できる
- B. RI と Savings Plans の割引をアカウント間で共有できる
- C. 複数アカウントの使用量を合算してボリューム割引を受けられる
- D. データ転送の料金がアカウント間で常に無料になる
- E. メンバーアカウントのルートユーザーを無効にできる

??? success "答えと解説"
    **正解: B, C**

    Organizations の一括請求の主な利点です。

    - A: 誤り。請求の機能ではない。
    - B: 正しい。
    - C: 正しい。
    - D: 誤り。そのような割引ではない。
    - E: 誤り。請求の機能ではない。

    **スキル:** [コンピューティングの費用](../domain4.md#t4-2-tools) / **参照:** [一括請求](../../../services/cost-management.md#consolidated-billing)

### 問7 {#q7}

RDS の RI や Database Savings Plans の購入の推奨を確認します。どれを使いますか。

- A. Trusted Advisor の Fault Tolerance のチェック
- B. Cost Explorer の購入の推奨
- C. CloudWatch Logs Insights
- D. Config のマネージドルール

??? success "答えと解説"
    **正解: B**

    Cost Explorer に購入の推奨があります。

    - A: 誤り。耐障害性の点検。
    - B: 正しい。
    - C: 誤り。ログの分析。
    - D: 誤り。設定の評価。

    **スキル:** [データベースの費用](../domain4.md#t4-3-tools) / **参照:** [Cost Explorer](../../../services/cost-management.md#cost-explorer)、[Savings Plans](../../../services/cost-management.md#savings-plans)

### 問8 {#q8}

Aurora の I/O の費用が総額にどれだけ占めるかを、使用タイプの行単位で分析します。どれを使いますか。

- A. CloudWatch の `CPUUtilization` のグラフ
- B. Performance Insights のロードのグラフ
- C. Data Exports の CUR 2.0 を Athena で分析
- D. AWS Health のイベント

??? success "答えと解説"
    **正解: C**

    CUR は行単位で最も詳しいデータです。

    - A: 誤り。費用のデータではない。
    - B: 誤り。性能の分析で、費用の明細ではない。
    - C: 正しい。
    - D: 誤り。障害の情報。

    **スキル:** [データベースの費用](../domain4.md#t4-3-tools) / **参照:** [Data Exports と Cost and Usage Reports](../../../services/cost-management.md#data-exports)

### 問9 {#q9}

RDS のスナップショットの費用を DB ごとに分けます。正しい設定はどれですか。

- A. スナップショットの費用は分けられないので、諦める
- B. DB のタグはスナップショットの費用に自動で適用される
- C. スナップショットを S3 にエクスポートすれば自動で分かれる
- D. スナップショットへのタグのコピーを有効にし、コスト配分タグを有効化する

??? success "答えと解説"
    **正解: D**

    スナップショットの費用はスナップショットの単位で計上されます。

    - A: 誤り。タグで分けられる。
    - B: 誤り。自動では付かない。
    - C: 誤り。目的に合わない。
    - D: 正しい。

    **スキル:** [データベースの費用](../domain4.md#t4-3-tools) / **参照:** [コスト配分タグ](../../../services/cost-management.md#cost-allocation-tags)

### 問10 {#q10}

データ転送の費用が急に増えました。どのサービスの通信が増えたかを調べます。正しい組み合わせを選んでください。（2つ選択）

- A. Cost Explorer の `UsageType` で内訳を見る
- B. Config のルールで、ネットワークの転送量を評価する
- C. CloudTrail の管理イベントで、パケットの量を集計する
- D. VPC フローログで通信の元と先を調べる
- E. GuardDuty の検出結果で、月額の内訳を確認する

??? success "答えと解説"
    **正解: A, D**

    費用の内訳と通信の中身を別のツールで調べます。

    - A: 正しい。
    - B: 誤り。設定の評価で、転送量を見ない。
    - C: 誤り。API の記録で、パケットの量はない。
    - D: 正しい。
    - E: 誤り。脅威の検出で、費用の内訳ではない。

    **スキル:** [ネットワーク費用](../domain4.md#t4-4-tools) / **参照:** [データ転送の費用](../../../services/cost-management.md#data-transfer)、[VPC フローログ](../../../services/networking.md#flow-logs)

### 問11 {#q11}

プライベートサブネットの EC2 の S3 への通信が NAT を通り、費用が大きいと分かりました。見直しとして適切なものはどれですか。

- A. インターネットゲートウェイを削除する
- B. S3 のゲートウェイエンドポイントを追加する
- C. NAT ゲートウェイの数を AZ ごとに増やす
- D. S3 のストレージクラスを変更する

??? success "答えと解説"
    **正解: B**

    ゲートウェイエンドポイントに追加料金はなく、NAT の処理料金が消えます。

    - A: 誤り。他の通信が止まる。
    - B: 正しい。
    - C: 誤り。処理料金は減らない。
    - D: 誤り。通信の費用は変わらない。

    **スキル:** [ネットワーク費用](../domain4.md#t4-4-tools) / **参照:** [VPC エンドポイントと PrivateLink](../../../services/networking.md#vpc-endpoints)

### 問12 {#q12}

アカウントにパブリック IPv4 アドレスが 10 個あり、3 個は未使用の Elastic IP です。単価は 0.005 USD/時です。30 日（720 時間）の費用はどれですか。無料利用枠は考えません。

- A. 36 USD で、使用中の分も未使用の分も課金される
- B. 25.2 USD で、未使用の 3 個は課金されない
- C. 10.8 USD で、未使用の 3 個だけ課金される
- D. 0 USD で、パブリック IPv4 に料金はかからない

??? success "答えと解説"
    **正解: A**

    `10 × 720 × 0.005` で 36 USD です。使用中でもアイドルでも同じ単価なので、不要なアドレスは解放します。

    - A: 正しい。
    - B: 誤り。未使用の分も課金される。
    - C: 誤り。使用中の分も課金される。
    - D: 誤り。料金がかかる。

    **スキル:** [ネットワーク費用](../domain4.md#t4-4-tools) / **参照:** [Elastic IP](../../../services/network-connectivity.md#elastic-ip)

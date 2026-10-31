# SageMaker Catalog とガバナンスの問題集

対象の解説: [DataZone と SageMaker Unified Studio](../../../services/data-engineering.md#datazone-unified-studio)、[データの共有](../../../services/data-engineering.md#choosing-sharing)

### 問1 {#q1}

社内のアナリストが、データを意味で検索し、利用を申請し、承認を受けて使えるようにします。どのサービスですか。

- A. SageMaker Catalog
- B. Lake Formation のデータフィルター
- C. Quick Sight の SPICE
- D. Glue Data Catalog

??? success "答えと解説"
    **正解: A**

    DataZone を基盤にしたカタログとガバナンスの機能です。

    - A: 正しい。
    - B: 誤り。権限の仕組みで、検索と申請の機能ではありません。
    - C: 誤り。ダッシュボードのためのインメモリのエンジンです。
    - D: 誤り。エンジン向けのメタデータで、申請の流れはありません。

    **スキル:** [2.2.6](../domain2.md#skill-2-2-6) / **参照:** [DataZone と SageMaker Unified Studio](../../../services/data-engineering.md#datazone-unified-studio)

### 問2 {#q2}

SageMaker Catalog でデータを使えるようになるまでの順序はどれですか。

- A. プロデューサーがクローラーを実行するだけで、誰でも申請なしで読めるようになる
- B. コンシューマーが公開し、所有者が検索し、プロデューサーが削除して権限が付与される
- C. 所有者が Athena で分析し、プロデューサーが申請し、コンシューマーが公開する
- D. プロデューサーが公開し、コンシューマーが申請し、所有者が承認して権限が付与される

??? success "答えと解説"
    **正解: D**

    公開、検索と申請、承認の流れです。

    - A: 誤り。申請と承認があります。
    - B: 誤り。役割が逆です。
    - C: 誤り。順序が逆です。
    - D: 正しい。

    **スキル:** [2.2.6](../domain2.md#skill-2-2-6) / **参照:** [DataZone と SageMaker Unified Studio](../../../services/data-engineering.md#datazone-unified-studio)

### 問3 {#q3}

部門ごとに説明の項目がばらばらです。項目と用語を揃えます。SageMaker Catalog のどの機能ですか。

- A. Glue のテーブルのプロパティとクローラー
- B. LF タグとデータフィルター
- C. カタログの用語集とメタデータフォーム
- D. リネージとサブスクリプション

??? success "答えと解説"
    **正解: C**

    用語集とメタデータフォームで揃えます。

    - A: 誤り。Glue のメタデータで、用語は揃えません。
    - B: 誤り。Lake Formation の権限の機能です。
    - C: 正しい。
    - D: 誤り。由来の追跡と申請の機能です。

    **スキル:** [2.2.6](../domain2.md#skill-2-2-6) / **参照:** [DataZone と SageMaker Unified Studio](../../../services/data-engineering.md#datazone-unified-studio)

### 問4 {#q4}

データの品質の問題が見つかりました。どのダッシュボードが影響を受けるか、パイプライン全体でたどります。AWS の外の処理の情報も API で送れるようにします。何を使いますか。

- A. Glue のジョブブックマーク
- B. SageMaker Catalog のリネージ（OpenLineage 互換）
- C. SageMaker ML Lineage Tracking
- D. CloudWatch Logs のメトリクスフィルター

??? success "答えと解説"
    **正解: B**

    OpenLineage のイベントを取り込み、可視化します。

    - A: 誤り。処理位置の追跡で、データの由来の追跡ではありません。
    - B: 正しい。
    - C: 誤り。ML のワークフローの追跡です。
    - D: 誤り。ログからメトリクスを作る機能です。

    **スキル:** [2.4.4](../domain2.md#skill-2-4-4) / **参照:** [DataZone と SageMaker Unified Studio](../../../services/data-engineering.md#datazone-unified-studio)

### 問5 {#q5}

本番のモデルがどのデータセットと学習ジョブから作られたかを、監査で示します。何を使いますか。

- A. CloudTrail Lake の証跡
- B. Macie の機密データ検出ジョブ
- C. Glue Data Quality のルールセット
- D. SageMaker ML Lineage Tracking

??? success "答えと解説"
    **正解: D**

    データ準備からデプロイまでの手順の情報を保存します。

    - A: 誤り。API の記録で、データセットとモデルの関係は追いません。
    - B: 誤り。機密データの検出です。
    - C: 誤り。データの品質の評価です。
    - D: 正しい。

    **スキル:** [2.4.4](../domain2.md#skill-2-4-4) / **参照:** [SageMaker Pipelines](../../../services/sagemaker.md#pipelines)、[Model Registry](../../../services/sagemaker.md#model-registry)

### 問6 {#q6}

データリネージの目的として正しいものはどれですか。（2つ選択）

- A. API の呼び出し元の IP を記録する
- B. Redshift のクエリの実行を速くする
- C. 問題のあるデータの影響範囲を調べる
- D. S3 のオブジェクトを暗号化する
- E. データの由来を監査で説明する

??? success "答えと解説"
    **正解: C, E**

    由来、変換、利用者を追跡します。

    - A: 誤り。CloudTrail の役割です。
    - B: 誤り。性能の機能ではありません。
    - C: 正しい。どこへ流れたかをたどれます。
    - D: 誤り。暗号化の機能ではありません。
    - E: 正しい。どこから来て、どう変換されたかを示せます。

    **スキル:** [2.4.4](../domain2.md#skill-2-4-4) / **参照:** [DataZone と SageMaker Unified Studio](../../../services/data-engineering.md#datazone-unified-studio)、[SageMaker Unified Studio の位置づけ](../../../services/sagemaker.md#unified-studio)

### 問7 {#q7}

大きな組織で SageMaker Unified Studio を使います。事業部ごとにアセットを整理し、権限を委任します。どの単位を使いますか。

- A. Redshift の名前空間
- B. ドメインユニット
- C. プロジェクト
- D. Glue の接続

??? success "答えと解説"
    **正解: B**

    ドメインユニットはドメインの中を分け、権限を委任します。

    - A: 誤り。Redshift Serverless の単位です。
    - B: 正しい。
    - C: 誤り。共同作業の単位で、事業部の委任の単位ではありません。
    - D: 誤り。データストアへの接続の情報です。

    **スキル:** [4.1.7](../domain4.md#skill-4-1-7) / **参照:** [DataZone と SageMaker Unified Studio](../../../services/data-engineering.md#datazone-unified-studio)

### 問8 {#q8}

ドメインユニットで、ユーザーとグループに割り当てるポリシーはどれですか。

- A. カスタムアセットタイプの作成
- B. 用語集の作成
- C. プロジェクトの作成
- D. メタデータフォームの作成

??? success "答えと解説"
    **正解: C**

    割り当て先の違いを押さえます。

    - A: 誤り。プロジェクトに割り当てます。
    - B: 誤り。プロジェクトに割り当てます。
    - C: 正しい。
    - D: 誤り。プロジェクトに割り当てます。

    **スキル:** [4.1.7](../domain4.md#skill-4-1-7) / **参照:** [DataZone と SageMaker Unified Studio](../../../services/data-engineering.md#datazone-unified-studio)

### 問9 {#q9}

メタデータの品質を保つため、メタデータフォームを作れるプロジェクトを絞ります。どうしますか。

- A. ドメインユニットの認可ポリシーで、メタデータフォームの作成を特定のプロジェクトに割り当てる
- B. 全員をドメインの所有者にして、作成の結果を後から確認する
- C. Lake Formation の LF タグで、メタデータフォームの作成を制限する
- D. IAM のパスワードポリシーで、メタデータフォームを作れるユーザーを制限する

??? success "答えと解説"
    **正解: A**

    プロジェクトに割り当てるポリシーです。

    - A: 正しい。
    - B: 誤り。絞ることになりません。
    - C: 誤り。データの権限の機能です。
    - D: 誤り。パスワードの設定です。

    **スキル:** [4.1.7](../domain4.md#skill-4-1-7) / **参照:** [SageMaker Unified Studio の位置づけ](../../../services/sagemaker.md#unified-studio)、[DataZone と SageMaker Unified Studio](../../../services/data-engineering.md#datazone-unified-studio)

### 問10 {#q10}

SageMaker Catalog で、あるプロジェクトのアナリスト全員がアセットを読めるようにします。正しい管理の方法はどれですか。

- A. アナリストごとに S3 のバケットポリシーへ ARN を追加する
- B. プロジェクトで購読の申請をし、メンバーをプロジェクトに追加する
- C. アセットを公開せずに、アナリストに S3 のパスを共有する
- D. アナリストごとに Lake Formation の権限を手で付与する

??? success "答えと解説"
    **正解: B**

    プロジェクトのメンバーになれば使えます。

    - A: 誤り。個人ごとの管理になります。
    - B: 正しい。
    - C: 誤り。申請の流れを通りません。
    - D: 誤り。個人ごとの管理になります。

    **スキル:** [4.5.6](../domain4.md#skill-4-5-6) / **参照:** [DataZone と SageMaker Unified Studio](../../../services/data-engineering.md#datazone-unified-studio)

### 問11 {#q11}

コンシューマーの申請を所有者が承認しました。実際の権限はどこで働きますか。

- A. Macie が読み取りのたびに検査して、問題がなければ許可する
- B. CloudTrail が承認の記録を確認して、読み取りごとに通信を許可する
- C. SageMaker Catalog が S3 のデータをコピーして、独自の権限で配る
- D. Lake Formation や Redshift の権限が付与される

??? success "答えと解説"
    **正解: D**

    SageMaker Catalog は権限の上の申請の流れです。

    - A: 誤り。機密データの検出です。
    - B: 誤り。CloudTrail は記録です。
    - C: 誤り。権限の実体は Lake Formation や Redshift です。
    - D: 正しい。

    **スキル:** [4.5.6](../domain4.md#skill-4-5-6) / **参照:** [DataZone と SageMaker Unified Studio](../../../services/data-engineering.md#datazone-unified-studio)、[AWS Lake Formation](../../../services/data-engineering.md#lake-formation)

### 問12 {#q12}

役割と動作の組み合わせとして正しいものはどれですか。（2つ選択）

- A. 所有者が他のプロジェクトのメンバーを個別に削除して公開する
- B. プロデューサーのプロジェクトは公開の後に必ず S3 のデータを削除する
- C. コンシューマーのプロジェクトがカタログを検索して購読を申請する
- D. プロデューサーのプロジェクトがアセットを公開する
- E. コンシューマーのプロジェクトが所有者の代わりに申請を承認する

??? success "答えと解説"
    **正解: C, D**

    プロジェクトの単位で管理します。

    - A: 誤り。公開の手順ではありません。
    - B: 誤り。データは残ります。
    - C: 正しい。申請は所有者が承認します。
    - D: 正しい。説明を付けて公開します。
    - E: 誤り。承認は所有者です。

    **スキル:** [4.5.6](../domain4.md#skill-4-5-6) / **参照:** [DataZone と SageMaker Unified Studio](../../../services/data-engineering.md#datazone-unified-studio)

### 問13 {#q13}

広告主と媒体社が、顧客の生データを互いに見せず、共通の顧客の数だけを集計します。何を選びますか。

- A. AWS Data Exchange
- B. Redshift のデータ共有
- C. AWS Clean Rooms
- D. Lake Formation のクロスアカウント共有

??? success "答えと解説"
    **正解: C**

    分析ルールで許す分析を制限します。

    - A: 誤り。データそのものへのアクセスを渡します。
    - B: 誤り。相手にライブのテーブルを見せます。
    - C: 正しい。
    - D: 誤り。相手にテーブルを見せます。

    **スキル:** [4.5.7](../domain4.md#skill-4-5-7) / **参照:** [データの共有](../../../services/data-engineering.md#choosing-sharing)、[AWS Clean Rooms](../../../services/data-engineering.md#clean-rooms)

### 問14 {#q14}

事業部が 20 あり、中央のデータチームがボトルネックです。各部門がデータを所有して公開し、標準は中央で決めます。どの型ですか。

- A. フェデレーション（データメッシュ）
- B. データのサイロ（部門ごとに標準なしで閉じる）
- C. 中央集権（1 つのチームがデータと権限を管理する）
- D. 単一の EC2 のデータベースへ全データを集める型

??? success "答えと解説"
    **正解: A**

    ドメインごとにデータ製品として公開します。

    - A: 正しい。
    - B: 誤り。標準がなく、ガバナンスになりません。
    - C: 誤り。ボトルネックが残ります。
    - D: 誤り。規模と運用の面で向きません。

    **スキル:** [4.5.7](../domain4.md#skill-4-5-7) / **参照:** [マルチアカウントのパターン](../../../services/governance.md#multi-account-patterns)、[データの共有](../../../services/data-engineering.md#choosing-sharing)

### 問15 {#q15}

ガバナンスの 3 つの要素（発見、アクセス、監視）とサービスの組み合わせで、監視に当たるものはどれですか。（2つ選択）

- A. 申請と承認の流れ
- B. Glue Data Quality
- C. Macie
- D. Glue Data Catalog の検索
- E. SageMaker Catalog の検索

??? success "答えと解説"
    **正解: B, C**

    監視には品質、リネージ、監査、機密データの検出が入ります。

    - A: 誤り。アクセスです。
    - B: 正しい。品質の監視です。
    - C: 正しい。機密データの検出です。
    - D: 誤り。発見です。
    - E: 誤り。発見です。

    **スキル:** [4.5.7](../domain4.md#skill-4-5-7) / **参照:** [データの共有](../../../services/data-engineering.md#choosing-sharing)、[Data Quality](../../../services/data-engineering.md#glue-data-quality)

# Systems Manager と自動化の問題集

対象の解説: [Systems Manager と自動化](../../../services/operations.md#systems-manager)

### 問1 {#q1}

数百台のサーバーで動くアプリの機能フラグの値を、営業時間中に変更します。全サーバーへ段階的に反映し、エラー率のアラームが鳴れば自動で戻します。アプリの再デプロイと再起動はしません。何を使いますか。

- A. AppConfig のデプロイ戦略とアラーム
- B. Secrets Manager の値を更新して、ローテーションのスケジュールで反映する
- C. Parameter Store のパラメータを更新して、全サーバーを Run Command で再起動する
- D. AWS Config の修復で、各サーバーのファイルを書き換える

??? success "答えと解説"
    **正解: A**

    AppConfig はアプリの設定を段階的に配布し、アラームでロールバックします。

    - A: 正しい。
    - B: 誤り。シークレットの管理の機能で、機能フラグの段階的な配布に向かない。
    - C: 誤り。段階的な反映とアラームでのロールバックがない。
    - D: 誤り。AWS リソースの設定の評価の仕組みで、アプリの設定の配布に使わない。

    **スキル:** [構成管理](../domain2.md#t2-1-config-management) / **参照:** [AWS AppConfig](../../../services/secrets.md#appconfig)、[デプロイ戦略](../../../services/secrets.md#deployment-strategies)

### 問2 {#q2}

次の 3 つの要件があります。(1) EC2 の中の NTP の設定を望ましい状態に保つ。(2) S3 バケットの暗号化の設定の履歴を残し、基準を評価する。(3) 既存の Chef のレシピを、終了したサービスの代わりに動かす。適切な組み合わせはどれですか。

- A. (1) State Manager、(2) CloudTrail、(3) Elastic Beanstalk の設定ファイルで実行
- B. (1) AppConfig、(2) AWS Config、(3) OpsWorks for Chef Automate
- C. (1) State Manager、(2) AWS Config、(3) State Manager で Chef のレシピを実行
- D. (1) AWS Config、(2) Systems Manager、(3) OpsWorks Stacks

??? success "答えと解説"
    **正解: C**

    サーバーの中は Systems Manager、AWS リソースの設定は AWS Config です。OpsWorks の役割は State Manager で置き換えられます。

    - A: 誤り。CloudTrail は API の記録で基準を評価せず、Beanstalk はレシピの実行基盤ではない。
    - B: 誤り。AppConfig はアプリの設定の配布で、OpsWorks も終了している。
    - C: 正しい。
    - D: 誤り。(1) と (2) の対象が逆で、OpsWorks Stacks はすでに終了している。

    **スキル:** [構成管理](../domain2.md#t2-1-config-management) / **参照:** [State Manager](../../../services/operations.md#state-manager)、[AWS Config](../../../services/governance.md#config)、[AWS OpsWorks の状況](../../../services/operations.md#opsworks)

### 問3 {#q3}

チーム内で「構成管理はどのサービスか」で議論になりました。担当者の発言のうち正しいものはどれですか。

- A. 「AWS リソースの設定の記録と評価は AWS Config、サーバーの中の適用は Systems Manager」
- B. 「EC2 の OS のパッケージの更新は AWS Config が適用する」
- C. 「AppConfig を使うとセキュリティグループの設定を基準どおりに直せる」
- D. 「Systems Manager の Parameter Store を使えば、OS の設定を自動で適用して修復できる」

??? success "答えと解説"
    **正解: A**

    名前が似ていても、対象が違います。AWS リソースか、サーバーの中か、アプリの設定かで分けます。

    - A: 正しい。
    - B: 誤り。AWS Config はサーバーの中のパッケージを適用しない。
    - C: 誤り。AppConfig はアプリの設定と機能フラグの配布に使う。
    - D: 誤り。Parameter Store は値の保管で、適用も修復もしない。

    **スキル:** [構成管理](../domain2.md#t2-1-config-management) / **参照:** [AWS Config](../../../services/governance.md#config)、[AWS AppConfig](../../../services/secrets.md#appconfig)、[AWS Systems Manager](../../../services/operations.md#systems-manager)

### 問4 {#q4}

全リージョンと全アカウントの未使用の EBS を週 1 回調べて、スナップショットを取ってから削除します。処理はほとんど AWS API の呼び出しで、独自のコードを最小にし、影響を抑えるためにレート制御を使います。何を使いますか。

- A. 各リージョンの EC2 に cron を設定して、AWS CLI を実行するスクリプトを毎週動かす
- B. Lambda を 1 つ作り、全アカウントのループを 15 分の中で実行する
- C. Run Command を全インスタンスへ実行し、インスタンスの中から EBS を調べる
- D. Systems Manager Automation の複数アカウント、複数リージョンの実行

??? success "答えと解説"
    **正解: D**

    AWS API と手順を組み合わせる定型作業には Automation が向きます。レート制御で同時実行とエラーのしきい値を指定できます。

    - A: 誤り。サーバーの運用が必要になり、全アカウントの管理も難しい。
    - B: 誤り。上限の 15 分を超えるおそれがあり、レート制御も自作になる。
    - C: 誤り。サーバーの中の処理の仕組みで、API の定型作業に向かない。
    - D: 正しい。

    **スキル:** [自動化に使うサービス](../domain2.md#t2-3-automation-services) / **参照:** [Automation](../../../services/operations.md#automation)、[複数アカウント、複数リージョンの実行](../../../services/operations.md#automation-multi-account)

### 問5 {#q5}

次の作業の手段を選びます。(1) 毎月第 2 日曜の深夜 2 時間の間に限り、本番サーバーでパッチのスクリプトを実行する。(2) 毎朝 8 時に Lambda で費用のレポートを送る。(3) 今すぐ全サーバーのログレベルを変える。適切な組み合わせはどれですか。

- A. (1) State Manager、(2) Run Command、(3) Maintenance Windows
- B. (1) EventBridge のスケジュール、(2) Maintenance Windows、(3) Automation の承認
- C. (1) Run Command、(2) Maintenance Windows、(3) State Manager
- D. (1) Maintenance Windows、(2) EventBridge のスケジュール、(3) Run Command

??? success "答えと解説"
    **正解: D**

    決まった時間帯なら Maintenance Windows、定期の呼び出しなら EventBridge のスケジュール、一度だけの実行なら Run Command です。

    - A: 誤り。時間帯と一度だけの実行の役割が入れ違っている。
    - B: 誤り。(2) の Lambda の定期実行に Maintenance Windows は過剰で、(3) に承認の条件はない。
    - C: 誤り。(1) は時間帯の制御がなく、(3) は一度だけの実行に合わない。
    - D: 正しい。

    **スキル:** [自動化に使うサービス](../domain2.md#t2-3-automation-services) / **参照:** [Maintenance Windows](../../../services/operations.md#maintenance-windows)、[スケジュール](../../../services/messaging.md#eventbridge-schedule)、[Run Command](../../../services/operations.md#run-command)

### 問6 {#q6}

EC2 の AMI の更新の手順があります。インスタンスの停止、AMI の作成、タグの付与の 3 工程を、そのまま再利用できる AWS 提供の手順に近い形で書きます。別の案件は、複数のサービスの並列処理と人の承認、1 週間の待機を含みます。それぞれの手段の組み合わせはどれですか。

- A. 前者は Systems Manager Automation、後者は Step Functions の Standard
- B. どちらも Maintenance Windows のタスクで、毎週同じ時間に実行する
- C. どちらも Lambda の関数で、ループと `time.sleep` を使って定期的に実行し直して実装する
- D. 前者は Step Functions、後者は Run Command

??? success "答えと解説"
    **正解: A**

    AWS API の定型の手順は Automation、分岐、並列、人の承認を含む長い処理は Step Functions です。

    - A: 正しい。
    - B: 誤り。時間帯の制御の仕組みで、分岐や待機を設計できない。
    - C: 誤り。15 分を超えられず、承認や待機にも向かない。
    - D: 誤り。後者の並列や承認を Run Command では書けない。

    **スキル:** [自動化に使うサービス](../domain2.md#t2-3-automation-services) / **参照:** [Automation](../../../services/operations.md#automation)、[人の承認](../../../services/step-functions.md#human-approval)

### 問7 {#q7}

監査の要件で、SSH のポートを閉じ、踏み台を廃止します。操作の記録も残します。担当者はノート PC に CLI を入れられないので、ブラウザからも AWS の API を呼びます。適切な組み合わせはどれですか。

- A. EC2 Instance Connect で 22 番を開き、ブラウザの SSH で接続し、操作の記録は OS のログに残す
- B. 担当者の PC に長期のアクセスキーを配布し、CloudTrail で全操作を記録する
- C. サーバーへは Session Manager で入り、セッションログを保存する。API の操作は CloudShell を使う
- D. 踏み台を Fargate のタスクにして、担当者の PC から Client VPN で接続する

??? success "答えと解説"
    **正解: C**

    Session Manager は SSH と踏み台が要りません。CloudShell はブラウザから CLI を使えます。

    - A: 誤り。22 番を閉じるという要件に反する。
    - B: 誤り。CLI を入れられない条件に合わず、キーの配布も適切でない。
    - C: 正しい。
    - D: 誤り。踏み台の廃止にならず、部品も増える。

    **スキル:** [AWS を操作する方法](../domain2.md#t2-3-interfaces) / **参照:** [CloudShell](../../../services/iac.md#cloudshell)、[Session Manager](../../../services/operations.md#session-manager)

### 問8 {#q8}

AWS CLI のスクリプトを見直します。条件は次のとおりです。(1) 応答から必要な値だけを取り出す、(2) EC2 の起動を実行せず権限だけを確認する、(3) 大量の結果で `--page-size` を小さくしてタイムアウトを避ける。正しい理解はどれですか。

- A. (1) は `grep`、(2) は `--debug`、(3) は `--region`
- B. (1) は `--query`、(2) は `--dry-run`、(3) は `--page-size` で 1 回の API の取得数を減らす
- C. (1) は `--filters`、(2) は `--generate-cli-skeleton`、(3) は `--no-paginate`
- D. (1) は `--output table`、(2) は `--no-cli-pager`、(3) は `--max-items` で一覧が速くなる

??? success "答えと解説"
    **正解: B**

    `--query` は JMESPath で値を取り出し、`--dry-run` は権限を確認します。`--page-size` は全件を取得したまま、呼び出しごとの件数を減らします。

    - A: 誤り。構造を使わず、`--debug` では実行を止められず、リージョンは結果の分割に関係ない。
    - B: 正しい。
    - C: 誤り。`--filters` はサーバー側の絞り込みで、スケルトンは入力の雛形。
    - D: 誤り。出力の形式、ページャの抑止、表示数の制限で、それぞれ目的が違う。

    **スキル:** [AWS を操作する方法](../domain2.md#t2-3-interfaces) / **参照:** [--query で絞り込む](../../../services/iac.md#cli-query)、[ドライランで権限を確かめる](../../../services/iac.md#cli-dry-run)、[ページネーション](../../../services/iac.md#cli-pagination)

### 問9 {#q9}

Lambda で組織の全アカウントのリソースの一覧を集める処理を作ります。`Throttling` でときどき失敗し、結果が途中で切れることもあります。AWS を操作する方法として適切な修正はどれですか。

- A. CLI の `--no-paginate` をサブプロセスで呼び、応答を文字列として解析する
- B. SDK のページネーターを使い、再試行の設定を `adaptive` か `standard` で増やす
- C. 全アカウントの CloudFormation スタックとして定義し、一覧を `Outputs` に書き出して読む
- D. 手作業で CloudShell から毎日スクリプトを実行し、失敗の分は翌日に再実行する

??? success "答えと解説"
    **正解: B**

    切り捨てはページネーションで、スロットリングは SDK の再試行の設定で解決します。

    - A: 誤り。全件を取得できず、再試行も解決しない。
    - B: 正しい。
    - C: 誤り。IaC はリソースの一覧の取得の手段にならない。
    - D: 誤り。自動化にならず、スロットリングの原因も残る。

    **スキル:** [AWS を操作する方法](../domain2.md#t2-3-interfaces) / **参照:** [リトライ](../../../services/sdk-resilience.md#retries)、[どれを使うか](../../../services/iac.md#choosing)、[AWS SDK の基本](../../../services/sdk-resilience.md#sdk-basics)

### 問10 {#q10}

10 リージョン、200 アカウントのインスタンスに、スキャンと適用を別の日程でパッチを当てます。新しいアカウントも自動で対象にし、パッチグループのタグの運用はなくします。何を使いますか。

- A. 各リージョンの Maintenance Windows でタスクを登録して、アカウントごとに展開する
- B. Quick Setup のパッチポリシー
- C. 各インスタンスの cron で `yum update` を実行して、結果を CloudWatch Logs へ送る
- D. Run Command の `AWS-RunPatchBaseline` を毎週手で実行し、結果はメールで報告する

??? success "答えと解説"
    **正解: B**

    パッチポリシーは組織の複数アカウント、複数リージョンを対象にでき、スキャンと適用の日程を分けられます。

    - A: 誤り。1 アカウント、1 リージョンが範囲で、展開の手間が増える。
    - B: 正しい。
    - C: 誤り。準拠の報告が揃わず、ベースラインの承認も効かない。
    - D: 誤り。手作業で、複数アカウントの統制にならない。

    **スキル:** [インベントリとパッチ](../domain2.md#t2-3-inventory-patch) / **参照:** [実行の設定方法](../../../services/operations.md#patch-methods)、[Patch Manager](../../../services/operations.md#patch-manager)

### 問11 {#q11}

監査で、全アカウントの全ノードで `openssl` の特定のバージョンが入っているものの一覧を求められました。同じ質問が今後も定期的に来ます。一覧を SQL で問い合わせられるようにし、ノードへの負荷は最小にします。どの構成が適切ですか。

- A. Inspector の検出結果から `openssl` の行だけを取り出して、一覧の代わりにする
- B. AWS Config のアグリゲーターに問い合わせて、`openssl` のパッケージの情報を SQL で検索する
- C. Inventory とリソースデータ同期で S3 に集約し、Athena で問い合わせる
- D. 全ノードで `rpm -qa` を Run Command で実行し、S3 の出力をスクリプトで毎回結合する

??? success "答えと解説"
    **正解: C**

    Inventory がノードの情報を集めます。リソースデータ同期で S3 に集め、Athena で検索します。

    - A: 誤り。検出結果は脆弱性があるものだけで、全インストールの一覧にならない。
    - B: 誤り。Inventory の連携がなければ、Config 単体でノード内のパッケージは分からない。
    - C: 正しい。
    - D: 誤り。ノードで都度実行が必要で、手間もかかる。

    **スキル:** [インベントリとパッチ](../domain2.md#t2-3-inventory-patch) / **参照:** [Inventory](../../../services/operations.md#inventory)、[パッチベースライン](../../../services/operations.md#patch-baselines)

### 問12 {#q12}

パッチの報告で、プライベートサブネットの 30 台だけが「未管理」です。OS には SSM Agent が入っています。ベースラインは正しく、他のサブネットのノードは準拠と表示されます。確認すべき項目はどれですか。（2つ選択）

- A. インスタンスのロールに `AmazonSSMManagedInstanceCore` があるか
- B. セキュリティグループの受信で、Systems Manager からの 22 番を許可しているか
- C. パッチベースラインの自動承認の日数が 7 日以上か
- D. `AWS-RunPatchBaseline` の `Operation` が `Install` か
- E. `ssm`、`ssmmessages`、`ec2messages` の VPC エンドポイントか NAT への経路があるか

??? success "答えと解説"
    **正解: A, E**

    マネージドノードの条件は、SSM Agent、インスタンスのロール、Systems Manager への経路の 3 つです。

    - A: 正しい。
    - B: 誤り。SSM Agent は外向きの通信を使い、受信は要らない。
    - C: 誤り。準拠の判定に関わるが、未管理の原因にならない。
    - D: 誤り。未管理の原因ではなく、パッチの適用の方法の話。
    - E: 正しい。

    **スキル:** [インベントリとパッチ](../domain2.md#t2-3-inventory-patch) / **参照:** [マネージドノードの条件](../../../services/operations.md#managed-nodes)、[パッチベースライン](../../../services/operations.md#patch-baselines)

### 問13 {#q13}

全サーバーで、社内の EDR の設定ファイルとサービスの起動を保ちます。担当者が手で変更しても、1 日以内に元に戻します。新しく起動するサーバーにも、タグが一致すれば適用します。何を使いますか。

- A. Maintenance Windows の毎週のタスクで、設定ファイルを上書きする
- B. State Manager の関連付けを、タグで対象にして毎日実行する
- C. Run Command で全サーバーに一度だけ実行し、結果を S3 へ保存する
- D. CloudFormation のドリフト検出を毎日実行して、差分を担当者に通知する

??? success "答えと解説"
    **正解: B**

    State Manager の関連付けは状態を保ち続けます。新しいノードにも適用され、次の実行で変更を元に戻せます。

    - A: 誤り。週次で間隔が長く、新しいサーバーへの適用も遅い。
    - B: 正しい。
    - C: 誤り。一度だけで、変更があっても元に戻らない。
    - D: 誤り。サーバーの中の設定の差を検出せず、修復もしない。

    **スキル:** [望ましい状態](../domain2.md#t2-3-desired-state) / **参照:** [State Manager](../../../services/operations.md#state-manager)、[State Manager と Maintenance Windows の違い](../../../services/operations.md#state-vs-maintenance)

### 問14 {#q14}

OpsWorks Stacks で運用していた Chef のクックブックを捨てずに、同じ構成の管理を続けます。新しいサーバーの追加のたびに自動で適用します。追加のサーバーは立てません。どう移行しますか。

- A. クックブックを捨てて、CloudFormation の `UserData` にすべてのコマンドを書き直す
- B. State Manager の関連付けで `AWS-ApplyChefRecipes` を実行する
- C. OpsWorks for Chef Automate の新しいサーバーを作って、そこへクックブックを移す
- D. Chef Infra Server を EC2 に立て、各サーバーへクライアントを手で導入する

??? success "答えと解説"
    **正解: B**

    State Manager は Chef レシピや Ansible プレイブックも実行できます。

    - A: 誤り。既存の資産を捨てることになり、起動後の状態も保てない。
    - B: 正しい。
    - C: 誤り。OpsWorks はすでに完全に終了している。
    - D: 誤り。追加のサーバーと手作業が必要になる。

    **スキル:** [望ましい状態](../domain2.md#t2-3-desired-state) / **参照:** [State Manager](../../../services/operations.md#state-manager)、[AWS OpsWorks の状況](../../../services/operations.md#opsworks)

### 問15 {#q15}

夜間だけ止められるサーバーがあります。セキュリティエージェントの導入状態は常に確認したいのですが、再起動を伴うカーネルの更新は月 1 回の決まった時間帯だけに実行します。組み合わせとして適切なものはどれですか。

- A. エージェントは Maintenance Windows、カーネルの更新は State Manager の毎時の関連付け
- B. エージェントは State Manager、カーネルの更新は Maintenance Windows
- C. どちらも Run Command で、担当者が必要なときに実行する
- D. どちらも EC2 の起動テンプレートの `UserData` で実行する

??? success "答えと解説"
    **正解: B**

    状態を保つのは State Manager、時間帯を決めて実行するのは Maintenance Windows です。

    - A: 誤り。再起動が時間帯の外で起きるおそれがあり、役割が逆。
    - B: 正しい。
    - C: 誤り。状態の維持も時間帯の制御もできない。
    - D: 誤り。起動の時にしか動かず、稼働中の状態を保てない。

    **スキル:** [望ましい状態](../domain2.md#t2-3-desired-state) / **参照:** [State Manager と Maintenance Windows の違い](../../../services/operations.md#state-vs-maintenance)、[State Manager](../../../services/operations.md#state-manager)

### 問16 {#q16}

ある企業は商用データベースのライセンスを 500 コアだけ持っています。契約を超えるインスタンスの起動を技術的に止め、不足のパッチの一覧も経営会議に報告します。適切な組み合わせはどれですか。

- A. ライセンスは Trusted Advisor のチェックで、パッチは GuardDuty の検出結果で確認する
- B. ライセンスは License Manager のハードリミット、パッチは Patch Manager の `Scan` と Compliance
- C. ライセンスは SCP で EC2 の起動を全面的に拒否し、パッチは Inspector の Classic で報告する
- D. ライセンスは AWS Config のカスタムルールで検出だけ行い、パッチは CloudTrail で確認する

??? success "答えと解説"
    **正解: B**

    License Manager はライセンス設定の上限で超過を止められます。パッチの不足は `Scan` で報告します。

    - A: 誤り。どちらも目的が違う。
    - B: 正しい。
    - C: 誤り。起動の全面的な禁止は過剰で、Classic も終了している。
    - D: 誤り。起動を止められず、CloudTrail はパッチの状況を示さない。

    **スキル:** [準拠の維持](../domain2.md#t2-3-compliance) / **参照:** [パッチベースライン](../../../services/operations.md#patch-baselines)、[AWS License Manager](../../../services/governance.md#license-manager)

### 問17 {#q17}

組織の方針で、禁止のソフトウェアが入ったノードを検出し、全社の準拠の状況を一か所で確認します。組織のアカウントは 150 です。何を組み合わせますか。

- A. Patch Manager のパッチベースラインで、禁止のパッケージを拒否のリストに入れて全社に配るだけにする
- B. GuardDuty の検出結果を全アカウントから委任管理者へ集約する
- C. Trusted Advisor の組織のビューで、全アカウントのソフトウェアの一覧を見る
- D. Inventory の情報を Config で評価し、アグリゲーターとリソースデータ同期で全社を集約する

??? success "答えと解説"
    **正解: D**

    禁止のソフトウェアの検出は Inventory と AWS Config の組み合わせです。全社は集約の仕組みで確認します。

    - A: 誤り。パッチの適用の制御で、全社の準拠の集約にならない。
    - B: 誤り。脅威の検出で、禁止のソフトウェアの一覧にならない。
    - C: 誤り。Trusted Advisor はサーバーの中のソフトウェアを調べない。
    - D: 正しい。

    **スキル:** [準拠の維持](../domain2.md#t2-3-compliance) / **参照:** [Inventory](../../../services/operations.md#inventory)、[アグリゲーター](../../../services/governance.md#config-aggregators)

### 問18 {#q18}

パッチの報告が必要な本番と、変更の凍結中のサーバーがあります。凍結の間は適用せずに報告だけを続けます。必須のサービスが動いているかも同じ画面で確かめます。適切な設定はどれですか。

- A. パッチベースラインを削除して、適用の対象をなくす
- B. `AWS-RunPatchBaseline` の `Operation` を `Scan` にし、サービスの確認は State Manager の関連付けの準拠で見る
- C. SSM Agent を凍結の間だけ停止して、自動のパッチが動かないようにする
- D. `AWS-RunPatchBaseline` の `Operation` を `Install` にし、`RebootOption` を `NoReboot` にする

??? success "答えと解説"
    **正解: B**

    `Scan` は報告だけです。Compliance はパッチと関連付けの準拠状況を集めます。

    - A: 誤り。スキャンの基準がなくなり、報告も意味を失う。
    - B: 正しい。
    - C: 誤り。報告も止まる。
    - D: 誤り。適用が実行されるので、凍結の条件に反する。

    **スキル:** [準拠の維持](../domain2.md#t2-3-compliance) / **参照:** [Patch Manager](../../../services/operations.md#patch-manager)、[State Manager](../../../services/operations.md#state-manager)

### 問19 {#q19}

Auto Scaling のインスタンスが終了するときに、ログを S3 へ退避します。処理は最大 5 分かかります。追加のワーカーは増やしません。適切な機能はどれですか。

- A. EventBridge の `EC2 Instance-terminate Successful` で Lambda を動かし、インスタンスの中のログを取得する
- B. ALB の登録解除の遅延を 5 分にして、その間にインスタンスの中でログを送る
- C. 終了のライフサイクルフックで待機させ、退避の処理の完了を通知して終了を続ける
- D. `UserData` でシャットダウン時の処理を登録し、OS の停止を 5 分待たせる

??? success "答えと解説"
    **正解: C**

    ライフサイクルフックは、起動や終了の途中でインスタンスを待機させます。

    - A: 誤り。終了の後のイベントで、インスタンスの中のログをもう取得できない。
    - B: 誤り。接続の完了を待つ設定で、ログの退避を実行も保証もしない。
    - C: 正しい。
    - D: 誤り。Auto Scaling の終了を待たせる仕組みではなく、完了を保証できない。

    **スキル:** [フリート管理](../domain5.md#t5-2-fleet) / **参照:** [ライフサイクルフック](../../../services/operations.md#lifecycle-hooks)

### 問20 {#q20}

300 台のマネージドノードを運用します。担当者が、SSH なしでコンソールからプロセスとファイルを確認します。別の依頼で、全台のログレベルを今すぐ変えます。適切な組み合わせはどれですか。

- A. Session Manager で全台へ順に入って確認し、変更は Maintenance Windows の次回の実行で行う
- B. Run Command で確認し、変更は State Manager の関連付けの次回の実行で行う
- C. EC2 のシリアルコンソールで確認し、変更は Run Command で行う
- D. Fleet Manager のコンソールで確認し、変更は Run Command で今すぐ行う

??? success "答えと解説"
    **正解: D**

    Fleet Manager はノードの確認と操作、Run Command は一斉の実行です。

    - A: 誤り。300 台を 1 台ずつ確認することになり、次回の実行では今すぐの条件に合わない。
    - B: 誤り。コマンドの結果を読む形で画面の確認にならず、次回の実行では今すぐの条件に合わない。
    - C: 誤り。シリアルコンソールは OS の起動の失敗などの調査の接続で、日常の確認に向かない。
    - D: 正しい。

    **スキル:** [フリート管理](../domain5.md#t5-2-fleet) / **参照:** [Fleet Manager](../../../services/operations.md#fleet-manager)、[Run Command](../../../services/operations.md#run-command)

### 問21 {#q21}

ゴールデン AMI を更新した後、稼働中のインスタンスを順に入れ替えます。全体の 90% は常に動かし、問題があれば前の起動テンプレートへ戻します。適切な機能はどれですか。

- A. 起動テンプレートの既定のバージョンを変え、インスタンスの自然な入れ替わりを待つ
- B. インスタンスの更新で `MinHealthyPercentage` 90 と `AutoRollback`
- C. ALB の登録解除の遅延を延ばし、Run Command で OS のパッケージを全台へ更新する
- D. 新しい Auto Scaling グループを手で作り、Route 53 の重み付けのレコードを順に変更して切り替える

??? success "答えと解説"
    **正解: B**

    インスタンスの更新は入れ替えの割合と、自動のロールバックを指定できます。

    - A: 誤り。稼働中のインスタンスは入れ替わらず、自動で戻す仕組みもない。
    - B: 正しい。
    - C: 誤り。AMI での入れ替えにならず、前の状態へ戻せない。
    - D: 誤り。標準の機能で足りるのに手作業が増える。

    **スキル:** [フリート管理](../domain5.md#t5-2-fleet) / **参照:** [インスタンスの更新](../../../services/operations.md#instance-refresh)、[Run Command](../../../services/operations.md#run-command)

### 問22 {#q22}

1,000 台へ OS の設定変更を行います。最初は小さく適用し、失敗が増えたら自動で止めます。対象は `Env=Prod` のタグのノードです。適切な指定はどれですか。

- A. インスタンス ID の一覧と、`MaxConcurrency` を 100%、`MaxErrors` を 100%
- B. インスタンス ID の一覧と、`MaxConcurrency` を 5%、`MaxErrors` を 100%
- C. タグの対象と、`MaxConcurrency` を 5%、`MaxErrors` を 1%
- D. タグの対象と、`MaxConcurrency` を 100%、`MaxErrors` を 0

??? success "答えと解説"
    **正解: C**

    最初は小さく適用し、`MaxErrors` を超えたら止めます。

    - A: 誤り。全台が一度に変更され、失敗でも止まらない。
    - B: 誤り。`MaxErrors` が 100% では失敗が増えても止まらず、対象もタグで指定していない。
    - C: 正しい。
    - D: 誤り。全台へ一度に実行される。

    **スキル:** [構成変更の適用](../domain5.md#t5-2-apply-changes) / **参照:** [Run Command](../../../services/operations.md#run-command)、[レート制御](../../../services/operations.md#automation-rate-control)

### 問23 {#q23}

本番のレート制限の値を、アプリの再デプロイなしで 20% ずつ 10 分ごとに広げ、アラームで戻します。誤った形式の値は配布の前に止めます。適切な機能の組み合わせはどれですか。（2つ選択）

- A. CloudFormation の変更セットと手動の承認
- B. CodeDeploy のカナリアのデプロイ設定
- C. AppConfig のデプロイ戦略とアラームのモニター
- D. Parameter Store のパラメータの階層と履歴
- E. AppConfig のバリデーター

??? success "答えと解説"
    **正解: C, E**

    AppConfig は段階的な配布、アラームでの戻し、値の検証を提供します。

    - A: 誤り。配布の段階の制御やアラームでの戻しにならない。
    - B: 誤り。コードのデプロイの仕組みで、再デプロイが必要になる。
    - C: 正しい。
    - D: 誤り。段階的な配布も検証もできない。
    - E: 正しい。

    **スキル:** [構成変更の適用](../domain5.md#t5-2-apply-changes) / **参照:** [デプロイ戦略](../../../services/secrets.md#deployment-strategies)、[AWS AppConfig](../../../services/secrets.md#appconfig)

### 問24 {#q24}

本番の VPC のルートテーブルを変更します。他の担当者の確認の後に実行し、影響を事前に確認します。別件で、Automation の手順を複数のアカウントへ順に適用し、エラーが増えたら止めます。適切な組み合わせはどれですか。

- A. ルートテーブルは Run Command の中の CLI で変更し、Automation は Maintenance Windows で一度に全アカウントへ適用する
- B. ルートテーブルはスタックポリシーで確認して更新し、Automation は `MaxErrors` を 100% にする
- C. ルートテーブルは変更セットで確認して実行し、Automation はレート制御を指定する
- D. ルートテーブルは変更セットで確認して実行し、Automation はレート制御なしで全アカウントへ実行する

??? success "答えと解説"
    **正解: C**

    インフラの変更には変更セット、Automation にはレート制御を使います。

    - A: 誤り。事前の影響の確認がなく、一度に適用するのでエラーでも止まらない。
    - B: 誤り。スタックポリシーは影響の確認の手段ではなく、100% ではエラーが増えても止まらない。
    - C: 正しい。
    - D: 誤り。ルートテーブルの進め方はよいが、レート制御がないとエラーが増えても止まらない。

    **スキル:** [構成変更の適用](../domain5.md#t5-2-apply-changes) / **参照:** [変更セット](../../../services/iac.md#change-sets)、[レート制御](../../../services/operations.md#automation-rate-control)

### 問25 {#q25}

本番の VPC で SSH を `0.0.0.0/0` に開ける規則が追加されたら、数分以内に自動で消し、結果を通知します。Lambda の開発は最小にします。適切な構成はどれですか。

- A. Config の `restricted-ssh` を定期のトリガーで評価し、非準拠を SNS で通知して担当者が削除する
- B. GuardDuty の検出結果を EventBridge で受け、Automation のランブックで規則を削除する
- C. VPC フローログのメトリクスフィルターで 22 番の受信を検知し、アラームから Automation を動かす
- D. EventBridge で CloudTrail の `AuthorizeSecurityGroupIngress` を受け、Automation のランブックで削除する

??? success "答えと解説"
    **正解: D**

    EventBridge のターゲットに Automation を直接指定できます。Lambda を書かなくて済みます。

    - A: 誤り。人の削除に頼り、定期の評価では数分以内の条件にも合わない。
    - B: 誤り。GuardDuty は脅威の検出で、規則の追加そのものを検知する手段ではない。
    - C: 誤り。通信があるまで検知できず、規則の追加を捉えない。
    - D: 正しい。

    **スキル:** [インフラの変更](../domain5.md#t5-2-respond) / **参照:** [EventBridge による修復パターン](../../../services/operations.md#eventbridge-remediation)、[EventBridge による自動化](../../../services/threat-detection.md#ir-eventbridge)

### 問26 {#q26}

スポットインスタンスで動くバッチの処理があります。中断の 2 分前の警告を受けたら、途中の結果を S3 へ退避して、ジョブをキューへ戻します。インスタンスのメタデータのポーリングはアプリに組み込みません。何を使いますか。

- A. Auto Scaling の Capacity Rebalancing を有効にして、結果の退避は新しいインスタンスに任せる
- B. EventBridge の `EC2 Instance State-change Notification` の `shutting-down` で Lambda を動かす
- C. EventBridge の `EC2 Spot Instance Interruption Warning` で Lambda や Run Command を動かす
- D. CloudWatch の `StatusCheckFailed_System` のアラームで Lambda を動かす

??? success "答えと解説"
    **正解: C**

    スポットの中断の警告は EventBridge で受けられます。

    - A: 誤り。代わりのインスタンスを起動する機能で、中断するインスタンスの結果を退避しない。
    - B: 誤り。状態の変化は中断が始まった後のイベントで、2 分前の警告ではない。
    - C: 正しい。
    - D: 誤り。中断の警告の仕組みではない。

    **スキル:** [インフラの変更](../domain5.md#t5-2-respond) / **参照:** [スポットの中断への対応](../../../services/operations.md#spot-interruptions)、[ステータスチェック](../../../services/operations.md#status-checks)

### 問27 {#q27}

GuardDuty が EC2 の検出結果を出したら、(1) インスタンスを隔離用のセキュリティグループへ移す、(2) スナップショットを取る、(3) 担当者の判断の後に終了する、を順に実行します。適切な構成はどれですか。

- A. EventBridge から Step Functions を起動し、隔離、スナップショット、`waitForTaskToken` で進める
- B. CloudWatch アラームの EC2 アクションで、検出結果の件数が増えたらインスタンスを停止する
- C. Security Hub CSPM の自動化ルールで 3 つの処理を順に実行し、担当者の判断もルールの中で待つ
- D. Config の自動修復で検出結果を受け、インスタンスの隔離と終了のランブックを実行する

??? success "答えと解説"
    **正解: A**

    複数の工程と人の判断を含むので Step Functions で構成します。

    - A: 正しい。
    - B: 誤り。アラームのアクションでは隔離、スナップショット、判断の順序を組めない。
    - C: 誤り。自動化ルールは検出結果の項目を更新する機能で、処理を実行しない。
    - D: 誤り。Config の修復はルールの非準拠に対するもので、GuardDuty の検出結果を受けず、人の判断も入らない。

    **スキル:** [インフラの変更](../domain5.md#t5-2-respond) / **参照:** [EC2 の隔離](../../../services/threat-detection.md#ir-ec2-isolation)、[イベント連携とエクスポート](../../../services/threat-detection.md#guardduty-events)

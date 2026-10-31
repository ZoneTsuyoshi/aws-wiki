# Systems Manager と修復の問題集

対象の解説: [AWS Systems Manager](../../../services/operations.md#systems-manager)、[Automation](../../../services/operations.md#automation)、[EventBridge による修復パターン](../../../services/operations.md#eventbridge-remediation)

### 問1 {#q1}

ハードウェアの障害で EC2 のシステムステータスチェックが失敗したら、自動で別のホストへ移したいと考えています。インスタンスは EBS を使う対応タイプで、Auto Scaling は使いません。最も単純な方法はどれですか。

- A. `StatusCheckFailed_Instance` のアラームで OS を再起動する Lambda を実行する
- B. インスタンスを手で終了し、同じ AMI から起動し直す手順書を用意する
- C. `StatusCheckFailed_System` のアラームで EC2 の復旧アクションを実行する
- D. `CPUUtilization` のアラームで EC2 の再起動アクションを実行する

??? success "答えと解説"
    **正解: C**

    AWS 側の基盤の障害は `StatusCheckFailed_System` で分かり、復旧アクションで別のホストへ移せます。対応インスタンスでは簡易自動復旧も既定で有効です。

    - A: 誤り。インスタンスのチェックは OS 側の問題で、ハードウェア障害には効かない。
    - B: 誤り。自動ではなく、手順の負担が残る。
    - C: 正しい。
    - D: 誤り。CPU はハードウェア障害の指標にならず、再起動では別のホストに移らない。

    **スキル:** [1.2.1](../domain1.md#skill-1-2-1) / **参照:** [ステータスチェック](../../../services/operations.md#status-checks)、[アラームのアクション](../../../services/observability.md#alarm-actions)

### 問2 {#q2}

S3 バケットの公開設定が AWS Config のルールで非準拠と判定されたら、自動で公開を止めたいと考えています。作り込みを最小にしたいです。どれを選びますか。

- A. Trusted Advisor の S3 バケットの権限のチェックを全リージョンで有効にし、指摘されたバケットが自動で修復されるのを確認する
- B. Lambda を毎時実行して全バケットの設定を読み、差分をメールで報告する
- C. Config のルールに SCP を関連付けて、非準拠のバケットを自動で削除する
- D. ルールの自動修復に Automation の `AWS-DisableS3BucketPublicReadWrite` を関連付ける

??? success "答えと解説"
    **正解: D**

    Config ルールの修復には、Automation のランブックを関連付けられます。

    - A: 誤り。Trusted Advisor は助言だけで、自動では直さない。
    - B: 誤り。修復されず、作り込みも多い。
    - C: 誤り。SCP は修復のアクションではなく、バケットを削除するのも要件に合わない。
    - D: 正しい。

    **スキル:** [1.2.1](../domain1.md#skill-1-2-1) / **参照:** [修復](../../../services/governance.md#config-remediation)、[Automation](../../../services/operations.md#automation)

### 問3 {#q3}

AWS Health に EC2 のメンテナンスの予定が出たら、事前に自動でインスタンスを別のホストへ移したいと考えています。どの構成にしますか。

- A. `AWS/EC2` のアラームでメンテナンスの予定を検知し、アラームのアクションで EC2 の復旧を実行するように全インスタンスへ設定する
- B. `aws.health` のイベントを EventBridge で受け、Automation のランブックを実行する
- C. CloudTrail のデータイベントで Health の通知を探し、Lambda で処理する
- D. Config ルールの定期評価で、Health のイベントがないかを 1 時間ごとに判定する

??? success "答えと解説"
    **正解: B**

    Health のイベントは EventBridge で受け、Automation で対処できます。

    - A: 誤り。メトリクスからは予定が分からない。
    - B: 正しい。
    - C: 誤り。Health のイベントは EventBridge で受ける。
    - D: 誤り。Config は設定の準拠の評価で、Health のイベントは見ない。

    **スキル:** [1.2.1](../domain1.md#skill-1-2-1) / **参照:** [AWS Health イベントの自動化](../../../services/operations.md#health-events)、[EventBridge による修復パターン](../../../services/operations.md#eventbridge-remediation)

### 問4 {#q4}

セキュリティグループを修復する Automation を作りました。修復自体がセキュリティグループの変更イベントを生み、同じルールが何度も動いてしまいます。適切な対策はどれですか。

- A. ルールのパターンで修復用ロールの操作を除くなど、修復が自分を起動しないようにする
- B. CloudWatch の複合アラームで、ルールが動いた回数を数えて止める
- C. ランブックのロールに管理者権限を付けて、1 回で確実に修復できるようにする
- D. EventBridge の再試行の回数を 0 にして、ターゲットの修復が 2 回以上は動かないように制限する

??? success "答えと解説"
    **正解: A**

    修復が別のイベントを起こして、また修復が動く構成にしないようにします。

    - A: 正しい。
    - B: 誤り。アラームではルールの起動は止められない。
    - C: 誤り。権限を増やしてもループは止まらず、最小権限にも反する。
    - D: 誤り。再試行は配信の失敗の話で、新しいイベントの発生は止まらない。

    **スキル:** [1.2.1](../domain1.md#skill-1-2-1) / **参照:** [EventBridge による修復パターン](../../../services/operations.md#eventbridge-remediation)

### 問5 {#q5}

2026 年 10 月時点で新しくインシデントの調査の自動化を始めるアカウントで、AWS の運用系サービスを選びます。提供状況を踏まえた説明として正しいものはどれですか。

- A. AWS DevOps Agent のインシデント調査は一般提供で、新規に検討できる
- B. Incident Manager を新規に有効にし、調査のすべてを任せる
- C. Amazon DevOps Guru を新規に有効にして、調査のすべてを任せる
- D. AWS DevOps Agent のインシデント調査はプレビューなので、本番では評価できない

??? success "答えと解説"
    **正解: A**

    運用系のサービスは提供状況が変わっています。

    - A: 正しい。
    - B: 誤り。Incident Manager は 2025 年 11 月 7 日に新規受付を終了している。
    - C: 誤り。DevOps Guru は 2026 年 10 月 29 日で新規受付を終了している。
    - D: 誤り。プレビューなのはリリース管理で、インシデント調査は一般提供である。

    **スキル:** [1.2.1](../domain1.md#skill-1-2-1) / **参照:** [Amazon DevOps Guru](../../../services/operations.md#devops-guru)、[AWS DevOps Agent](../../../services/operations.md#devops-agent)、[2026 年 10 月時点の提供状況](../../../services/operations.md#status)

### 問6 {#q6}

EC2 を停止し、AMI を作成し、再開するという一連の処理を定期的に行います。AWS API の呼び出しを含み、手順ごとの成否も追いたいです。どの機能が適切ですか。

- A. Session Manager で接続して、手順書どおりに CLI を実行する
- B. Inventory を有効にして、結果に応じた処理を手で実行する
- C. Automation のランブックを実行する
- D. Run Command で `AWS-RunShellScript` を 1 回実行する

??? success "答えと解説"
    **正解: C**

    Automation は AWS API も呼べて、複数の手順を実行できます。

    - A: 誤り。手動の操作で、自動化にならない。
    - B: 誤り。ソフトウェアの一覧を集める機能である。
    - C: 正しい。
    - D: 誤り。ノードの中で動く機能で、インスタンスを停止すると処理が続けられない。

    **スキル:** [1.2.3](../domain1.md#skill-1-2-3) / **参照:** [Automation](../../../services/operations.md#automation)、[選び方の比較](../../../services/operations.md#choosing)

### 問7 {#q7}

カスタムランブックの途中で、本番の変更の前に責任者の承認を入れたいと考えています。どのアクションを使いますか。

- A. `aws:branch`
- B. `aws:approve`
- C. `aws:executeScript`
- D. `aws:executeAwsApi`

??? success "答えと解説"
    **正解: B**

    `aws:approve` は人の承認を待ちます。指定した承認者が承認か拒否をするまで止まります。

    - A: 誤り。条件で分岐するだけで、人の承認は待たない。
    - B: 正しい。
    - C: 誤り。スクリプトを実行するアクションで、承認の機能は持たない。
    - D: 誤り。AWS API を呼ぶアクションで、承認は待たない。

    **スキル:** [1.2.3](../domain1.md#skill-1-2-3) / **参照:** [Automation](../../../services/operations.md#automation)

### 問8 {#q8}

ランブックのアクションと用途の組み合わせとして正しいものを選んでください。（2つ選択）

- A. `aws:branch` で別のアカウントのランブックを共有する
- B. `aws:runCommand` でノードの中のコマンドを実行する
- C. `aws:executeScript` で Python のスクリプトを実行する
- D. `aws:approve` で AWS API を呼び出して結果を受け取る
- E. `aws:executeAwsApi` でノードのシェルを開く

??? success "答えと解説"
    **正解: B, C**

    アクションの役割を組み合わせて、ランブックを作ります。

    - A: 誤り。`aws:branch` は条件で分岐するアクションである。
    - B: 正しい。
    - C: 正しい。
    - D: 誤り。`aws:approve` は人の承認を待つアクションである。
    - E: 誤り。`aws:executeAwsApi` は AWS API を呼ぶアクションである。

    **スキル:** [1.2.3](../domain1.md#skill-1-2-3) / **参照:** [Automation](../../../services/operations.md#automation)

### 問9 {#q9}

別のアカウントで、カスタムランブックを使った複数アカウントの Automation が失敗します。管理アカウントでは動きます。何を確認しますか。（2つ選択）

- A. 各アカウントに `AWS-SystemsManager-AutomationExecutionRole` があるか
- B. 対象のアカウントの CloudWatch エージェントが最新のバージョンか
- C. 各アカウントで `aws:approve` のステップが実行できるようになっているか
- D. ランブックの中の手順が 1 個に収まっているか
- E. カスタムランブックを対象のアカウントに共有しているか

??? success "答えと解説"
    **正解: A, E**

    実行先にランブックが見えることと、実行用のロールがあることが条件です。

    - A: 正しい。
    - B: 誤り。エージェントは Automation の実行の前提ではない。
    - C: 誤り。複数アカウントの実行で `aws:approve` は使えない。
    - D: 誤り。手順の数は複数アカウントの実行の条件ではない。
    - E: 正しい。

    **スキル:** [1.2.3](../domain1.md#skill-1-2-3) / **参照:** [複数アカウント、複数リージョンの実行](../../../services/operations.md#automation-multi-account)

### 問10 {#q10}

本番の 500 台に Automation を実行します。一度に全台へ広がらないようにし、失敗が増えたら止めたいと考えています。どの設定を使いますか。

- A. `AutomationAssumeRole` の権限を最小に絞って、対象の一部で権限エラーを起こして失敗したら全体を止める
- B. ランブックの手順を 500 個に増やして、1 台ずつの処理に分割する
- C. EventBridge の再試行の回数を 0 にして、失敗を止める
- D. 同時実行数（`MaxConcurrency`）とエラーのしきい値（`MaxErrors`）を設定する

??? success "答えと解説"
    **正解: D**

    多数のリソースへの実行は、同時実行数とエラーのしきい値でレートを制御します。

    - A: 誤り。権限でレートは制御できない。
    - B: 誤り。管理の手間が増えるだけで、レート制御にならない。
    - C: 誤り。実行するターゲットの失敗率で止める設定ではない。
    - D: 正しい。

    **スキル:** [1.2.3](../domain1.md#skill-1-2-3) / **参照:** [レート制御](../../../services/operations.md#automation-rate-control)

### 問11 {#q11}

`AutomationAssumeRole` を指定せずにランブックを実行しました。正しい説明はどれですか。

- A. 実行できずに、ロールの指定を求めるエラーで失敗する
- B. ルートユーザーの権限に切り替わり、すべての操作が許可される
- C. 実行を始めた人の権限で動き、実行時間は最大 12 時間になる
- D. Systems Manager のサービスリンクロールが必要な権限をすべて補う

??? success "答えと解説"
    **正解: C**

    指定しないと実行者の権限で動きます。長い処理や委任にはロールを指定します。

    - A: 誤り。ロールなしでも実行できる。
    - B: 誤り。そのような動作はない。
    - C: 正しい。
    - D: 誤り。実行者の権限で動く。

    **スキル:** [1.2.3](../domain1.md#skill-1-2-3) / **参照:** [Automation](../../../services/operations.md#automation)

### 問12 {#q12}

プライベートサブネットの EC2 が Fleet Manager に表示されません。SSM Agent は動いており、NAT も VPC エンドポイントもありません。ロールは正しく付いています。何が足りませんか。

- A. `ssm`、`ssmmessages`、`ec2messages` のインターフェイスエンドポイント、または NAT への経路
- B. セキュリティグループの受信で、Systems Manager の IP の範囲に対してポート 22 と 443 を開ける設定と、インスタンスの再起動
- C. インスタンスのパブリック IP に Elastic IP を割り当てる操作
- D. CloudWatch エージェントの導入と `fetch-config` の実行

??? success "答えと解説"
    **正解: A**

    マネージドノードの条件は、SSM Agent、ロール、SSM のエンドポイントへの経路の 3 つです。

    - A: 正しい。
    - B: 誤り。SSM Agent は外向きに接続するので、受信のポートは不要である。
    - C: 誤り。プライベートサブネットのままでは Elastic IP を付けても経路ができない。
    - D: 誤り。エージェントはマネージドノードの条件ではない。

    **スキル:** [3.2.1](../domain3.md#skill-3-2-1) / **参照:** [マネージドノードの条件](../../../services/operations.md#managed-nodes)

### 問13 {#q13}

踏み台サーバーをなくし、ポート 22 を閉じたまま、Linux のインスタンスにログインして操作を記録したいと考えています。何を使いますか。

- A. EC2 Instance Connect でパブリック IP に SSH し、操作の記録をインスタンスのログから CloudWatch Logs へ送る
- B. Client VPN を作り、ポート 22 を VPN のクライアントに開ける
- C. Run Command を対話的に実行し、キーペアで認証する
- D. Session Manager でセッションを開始し、ログを CloudWatch Logs か S3 に送る

??? success "答えと解説"
    **正解: D**

    Session Manager なら受信のポートも踏み台も不要で、セッションを記録できます。

    - A: 誤り。SSH のポートを開ける必要があり、要件に合わない。
    - B: 誤り。ポート 22 を開くことになり、要件に合わない。
    - C: 誤り。Run Command は対話的なログインの機能ではない。
    - D: 正しい。

    **スキル:** [3.2.1](../domain3.md#skill-3-2-1) / **参照:** [Session Manager](../../../services/operations.md#session-manager)、[選び方の比較](../../../services/operations.md#choosing)

### 問14 {#q14}

Session Manager のログの設定を有効にしましたが、データベースへのポート転送のセッションの内容が記録されません。正しい説明はどれですか。

- A. CloudWatch エージェントが入っていないと、ポート転送だけが記録されないため
- B. ポート転送のセッションの内容はログに残せないため
- C. ログの送信先の S3 バケットが暗号化されていないと、ポート転送だけが記録されないため
- D. ポート転送のセッションの内容は OpsCenter に記録されるので、そちらを確認すればよいため

??? success "答えと解説"
    **正解: B**

    ポート転送のセッションの内容は、ログに残せません。

    - A: 誤り。エージェントの有無の問題ではない。
    - B: 正しい。
    - C: 誤り。暗号化の問題ではない。
    - D: 誤り。OpsCenter はセッションのログの送信先ではない。

    **スキル:** [3.2.1](../domain3.md#skill-3-2-1) / **参照:** [Session Manager](../../../services/operations.md#session-manager)

### 問15 {#q15}

定義済みのパッチベースラインで運用しています。リリース直後のパッチを、7 日より早く適用するよう求められました。何をしますか。

- A. 自動承認の待ち時間を短くしたカスタムのパッチベースラインを作る
- B. 定義済みのパッチベースラインの設定を、直接編集して待ち時間を短くする
- C. `AWS-RunPatchBaseline` の代わりに Inventory を実行する
- D. Maintenance Windows の間隔を短くするだけで対応する

??? success "答えと解説"
    **正解: A**

    定義済みのベースラインは、多くの OS でリリースから 7 日待ちます。

    - A: 正しい。
    - B: 誤り。定義済みのベースラインは変更できない。
    - C: 誤り。Inventory は一覧を集める機能で、パッチを当てない。
    - D: 誤り。承認の待ち時間が変わらないので、新しいパッチは対象にならない。

    **スキル:** [3.2.1](../domain3.md#skill-3-2-1) / **参照:** [パッチベースライン](../../../services/operations.md#patch-baselines)、[Patch Manager](../../../services/operations.md#patch-manager)

### 問16 {#q16}

新しく起動したインスタンスにも自動で CloudWatch エージェントの設定を当て、望ましい状態を保ち続けたいと考えています。作業の時間帯の制限はありません。どれを使いますか。

- A. OpsCenter
- B. Maintenance Windows の定期タスク
- C. Inventory
- D. State Manager の関連付け

??? success "答えと解説"
    **正解: D**

    新しいノードにも自動で構成を当てるなら State Manager です。

    - A: 誤り。運用の課題を管理する機能で、設定は当てない。
    - B: 誤り。決まった時間帯に作業を実行する機能で、望ましい状態の維持には State Manager が向く。
    - C: 誤り。ソフトウェアの一覧を集める機能で、設定は当てない。
    - D: 正しい。

    **スキル:** [3.2.1](../domain3.md#skill-3-2-1) / **参照:** [State Manager と Maintenance Windows の違い](../../../services/operations.md#state-vs-maintenance)

### 問17 {#q17}

本番のパッチの適用を、毎週土曜の深夜 2 時間だけに限りたいと考えています。どれが適切ですか。

- A. OpsCenter の OpsItem として作り、担当者に週末の深夜の実行を依頼して、完了を手で記録する運用
- B. State Manager の関連付けだけを作り、時間帯の指定は行わない
- C. Maintenance Windows のタスクとして Patch Manager の実行を登録する
- D. CloudWatch の複合アラームで土曜の深夜を判定して、パッチを当てる

??? success "答えと解説"
    **正解: C**

    業務時間外に限って実行するなら Maintenance Windows です。

    - A: 誤り。手作業に頼る方法で、自動の実行にはならない。
    - B: 誤り。時間帯を限るという要件に合わない。
    - C: 正しい。
    - D: 誤り。アラームは時間帯の指定の機能を持たない。

    **スキル:** [3.2.1](../domain3.md#skill-3-2-1) / **参照:** [Maintenance Windows](../../../services/operations.md#maintenance-windows)、[State Manager と Maintenance Windows の違い](../../../services/operations.md#state-vs-maintenance)

### 問18 {#q18}

組織の複数のアカウントとリージョンのパッチ適用を、1 か所で設定したいと考えています。最も運用負荷の小さい方法はどれですか。

- A. 各アカウントでカスタムのベースラインを作り、担当者が毎月 Run Command を手で実行する
- B. Quick Setup のパッチポリシーを使う
- C. 各リージョンで Session Manager のセッションを開いて、OS の更新のコマンドを順に実行する
- D. インスタンスのユーザーデータに OS の更新の処理を書き、再起動を待つ

??? success "答えと解説"
    **正解: B**

    組織全体を 1 か所で設定するなら、Quick Setup のパッチポリシーです。

    - A: 誤り。手作業が多く、1 か所の設定にならない。
    - B: 正しい。
    - C: 誤り。自動化にならず、台数に対応できない。
    - D: 誤り。起動時にしか動かず、1 か所の設定にもならない。

    **スキル:** [3.2.1](../domain3.md#skill-3-2-1) / **参照:** [実行の設定方法](../../../services/operations.md#patch-methods)、[Patch Manager](../../../services/operations.md#patch-manager)

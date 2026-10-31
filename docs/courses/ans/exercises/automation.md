# ネットワークの自動化の問題集

対象の解説: [CloudFormation テンプレート](../../../services/iac.md#cloudformation-template), [ネストされたスタックと StackSets](../../../services/iac.md#nested-stacks-stacksets), [カスタムリソース](../../../services/iac.md#custom-resources), [EventBridge による修復パターン](../../../services/operations.md#eventbridge-remediation)

### 問1 {#q1}

ハイブリッド接続を全部 CloudFormation で展開する計画です。VIF、DX ゲートウェイ、VPN 接続、ルートテーブルをコードにしました。レビューで「コードだけでは完結しないもの」を指摘します。正しいものはどれですか。

- A. 物理のクロスコネクトの手配とパートナー側の設定
- B. Transit Gateway のルートテーブルとその静的ルートの作成
- C. CGW のリソースと Site-to-Site VPN 接続の作成
- D. Resolver エンドポイントと Forward ルールの作成と関連付け

??? success "答えと解説"
    **正解: A**

    物理の配線やオンプレミス側は別の手段です。

    - A: 正しい。
    - B: 誤り。テンプレートで作成できる。
    - C: 誤り。テンプレートで作成できる。
    - D: 誤り。テンプレートで作成できる。

    **スキル:** [自動化](../domain2.md#t2-1-automation) / **参照:** [CloudFormation テンプレート](../../../services/iac.md#cloudformation-template)

### 問2 {#q2}

20 の拠点の CGW と VPN 接続を、同じ形で作成します。拠点の IP と ASN は違います。1 拠点の変更が他の拠点へ影響しないようにします。最も適切な IaC の作り方はどれですか。

- A. 拠点ごとにコンソールで作成して、ドリフト検出で差を確認する
- B. 1 つのスタックに 20 拠点分を書いて、`Mappings` で値を切り替える
- C. 拠点の数だけテンプレートをコピーして、値を直接書く
- D. 共通のテンプレートをパラメータで変えて、拠点ごとのスタックにする

??? success "答えと解説"
    **正解: D**

    環境差はパラメータで吸収します。

    - A: 誤り。繰り返せる構成にならない。
    - B: 誤り。1 拠点の変更で全拠点のスタックが更新の対象になる。
    - C: 誤り。共通の変更をすべてのコピーへ繰り返すことになる。
    - D: 正しい。

    **スキル:** [自動化](../domain2.md#t2-1-automation) / **参照:** [パラメータ](../../../services/iac.md#parameters), [ネストされたスタックと StackSets](../../../services/iac.md#nested-stacks-stacksets)

### 問3 {#q3}

VPN のトンネルの事前共有キーを CloudFormation で指定します。リポジトリは社内で共有され、スタックのイベントも多くの担当者が読めます。最も適切な方法はどれですか。

- A. テンプレートに平文で書き、リポジトリの権限で読める人を絞る
- B. パラメータの既定値に書いて、変更セットで確認できるようにする
- C. Secrets Manager に保存し、動的参照で渡す
- D. `Metadata` に Base64 で書いて、起動時に復号する

??? success "答えと解説"
    **正解: C**

    シークレットはテンプレートに書きません。

    - A: 誤り。テンプレートに残る。
    - B: 誤り。既定値はテンプレートに残る。
    - C: 正しい。
    - D: 誤り。Base64 は暗号化ではない。

    **スキル:** [自動化](../domain2.md#t2-1-automation) / **参照:** [CloudFormation テンプレート](../../../services/iac.md#cloudformation-template), [Site-to-Site VPN](../../../services/network-connectivity.md#site-to-site-vpn)

### 問4 {#q4}

組織の全 VPC を Transit Gateway へ接続するテンプレートを展開します。新しいアカウントが増えたら自動で展開し、OU から外れたら削除します。IAM ロールの事前作成は避けます。最も適切な方法はどれですか。

- A. サービスマネージドの StackSets で OU へ自動デプロイする
- B. 各アカウントで Service Catalog の製品を担当者が起動する
- C. セルフマネージドの StackSets で、新しいアカウントを手で追加する
- D. EventBridge で毎週スクリプトを実行し、全アカウントへ CLI で展開する

??? success "答えと解説"
    **正解: A**

    OU を対象にします。

    - A: 正しい。
    - B: 誤り。自動にならない。
    - C: 誤り。手動で、IAM ロールの事前作成も必要。
    - D: 誤り。標準の自動デプロイで足りる。

    **スキル:** [自動化](../domain2.md#t2-2-automation) / **参照:** [StackSets の運用](../../../services/operations.md#stacksets-operations), [ネストされたスタックと StackSets](../../../services/iac.md#nested-stacks-stacksets)

### 問5 {#q5}

共有された Transit Gateway へのアタッチメントと VPC のルートを 1 つのスタックで作ると、ルートの作成が先に動いて失敗することがあります。担当者は順序を制御したいと考えています。最も適切なものはどれですか。

- A. スタックのロールバックを無効にして、失敗後に再実行する
- B. `DeletionPolicy` を `Retain` にして、失敗しても残す
- C. ルートの `Condition` を `true` に固定して、先に作らせる
- D. `DependsOn` やスタックの分割で、ルートを後に作る

??? success "答えと解説"
    **正解: D**

    依存の順序を明示します。

    - A: 誤り。順序の問題が残り、状態の管理も難しくなる。
    - B: 誤り。削除の動作で、作成の順序は変わらない。
    - C: 誤り。条件は作成の有無を決めるだけ。
    - D: 正しい。

    **スキル:** [自動化](../domain2.md#t2-2-automation) / **参照:** [ネストされたスタックと StackSets](../../../services/iac.md#nested-stacks-stacksets), [アタッチメント](../../../services/network-connectivity.md#tgw-attachments)

### 問6 {#q6}

StackSets で VPC アタッチメントを各アカウントに展開します。Transit Gateway の所有者の手作業の承認があると、ルートの作成まで進みません。承認を減らしつつ、誤接続は別の仕組みで防ぎます。最も適切な設定はどれですか。

- A. 既定のルートテーブルへの関連付けを有効にする
- B. RAM の共有をアカウントごとに毎回作り直す
- C. 共有先のアカウントのスタックに、承認のリソースを追加する
- D. `AutoAcceptSharedAttachments` を有効にする

??? success "答えと解説"
    **正解: D**

    順序と権限を考えます。

    - A: 誤り。分離が崩れ、承認の問題も解決しない。
    - B: 誤り。承認の待ちは解決しない。
    - C: 誤り。承認は所有者の操作で、共有先ではできない。
    - D: 正しい。

    **スキル:** [自動化](../domain2.md#t2-2-automation) / **参照:** [アタッチメント](../../../services/network-connectivity.md#tgw-attachments), [ネストされたスタックと StackSets](../../../services/iac.md#nested-stacks-stacksets)

### 問7 {#q7}

ネットワークチームは 40 個の VPC と多数のサブネットを、TypeScript のループと共通の部品で生成したいと考えています。結果は宣言的に管理し、差分も確認します。最も適切な道具はどれですか。

- A. SDK と Lambda。VPC の作成を順に呼ぶ関数を書く
- B. CloudFormation の JSON を手で書き、サブネットを全部列挙する
- C. AWS CLI のシェルスクリプト。VPC ごとに `create-vpc` を実行する
- D. AWS CDK。TypeScript で部品を書き、テンプレートを生成する

??? success "答えと解説"
    **正解: D**

    CDK は CloudFormation を生成します。

    - A: 誤り。状態の管理と差分を自分で作ることになる。
    - B: 誤り。動くが、ループと部品の要件に合わない。
    - C: 誤り。宣言的な管理にならず、差分も確認できない。
    - D: 正しい。

    **スキル:** [IaC](../domain2.md#t2-4-iac) / **参照:** [CDK](../../../services/iac.md#cdk), [CloudFormation テンプレート](../../../services/iac.md#cloudformation-template)

### 問8 {#q8}

本番の VPC のスタックのサブネットの属性を変更します。停止につながる置き換えが起きないかを実行前に確認します。最も適切な機能はどれですか。

- A. スタックポリシー。置き換えの有無を一覧で表示する
- B. ドリフト検出。テンプレートの変更が置き換えになるかを確認する
- C. ロールバックトリガー。実行前に影響を報告する
- D. 変更セット。更新の内容と置き換えの要否を実行前に表示する

??? success "答えと解説"
    **正解: D**

    置き換えの有無を確認します。

    - A: 誤り。保護の機能で、確認の一覧ではない。
    - B: 誤り。手動の変更の検出で、更新の影響を示さない。
    - C: 誤り。実行中の監視の機能。
    - D: 正しい。

    **スキル:** [IaC](../domain2.md#t2-4-iac) / **参照:** [変更セット](../../../services/iac.md#change-sets), [ドリフト検出](../../../services/iac.md#drift)

### 問9 {#q9}

ネットワークチームは CloudFormation で作ったルートテーブルが手動で変更されていないか定期的に確認します。変更があれば、テンプレートとの差を知りたいと考えています。最も適切な機能はどれですか。

- A. Reachability Analyzer。ルートの手動変更を見つける
- B. 変更セット。現在の設定とテンプレートの差を常に示す
- C. ドリフト検出。実際の設定とテンプレートの差を表示する
- D. CloudTrail の `CreateRoute`。テンプレートとの差を表示する

??? success "答えと解説"
    **正解: C**

    ドリフト検出で手動変更を見つけます。

    - A: 誤り。到達性の解析で、テンプレートとの差ではない。
    - B: 誤り。テンプレートの変更の影響を示す機能。
    - C: 正しい。
    - D: 誤り。変更の記録で、テンプレートとの差ではない。

    **スキル:** [IaC](../domain2.md#t2-4-iac) / **参照:** [ドリフト検出](../../../services/iac.md#drift), [AWS Config](../../../services/governance.md#config)

### 問10 {#q10}

SG に `0.0.0.0/0` の SSH が追加されたら、数分以内に自動で削除して通知します。組織の方針で、変更者の情報も通知に含めます。最も適切な構成はどれですか。

- A. Firewall Manager の使用状況の監査で、未使用の SG を毎週整理する
- B. Trusted Advisor の週次のレポートから開放された SG を見つけ、手で削除する
- C. フローログのメトリクスフィルターで SSH の通信を検知し、SNS で通知する
- D. CloudTrail の API の記録を EventBridge で受けて Lambda で削除する

??? success "答えと解説"
    **正解: D**

    変更イベントで修復を起動します。

    - A: 誤り。開放の検知の用途と時間に合わない。
    - B: 誤り。数分以内の要件に合わない。
    - C: 誤り。通信の記録で、ルールの変更や変更者が分からない。
    - D: 正しい。

    **スキル:** [イベント駆動](../domain2.md#t2-4-event) / **参照:** [EventBridge による修復パターン](../../../services/operations.md#eventbridge-remediation)

### 問11 {#q11}

全 VPC でフローログを必ず有効にします。作り忘れた VPC を継続的に評価し、自動で作成して、準拠の履歴も残します。最も適切なものはどれですか。

- A. CloudTrail の `CreateVpc` を EventBridge で受けて Lambda で作る
- B. GuardDuty の検出でフローログのない VPC を見つける
- C. Config の `vpc-flow-logs-enabled` と修復の Automation
- D. CloudWatch のアラームでフローログの数を監視して通知する

??? success "答えと解説"
    **正解: C**

    Config のルールと修復です。

    - A: 誤り。作成時しか評価できず、準拠の履歴が残らない。
    - B: 誤り。GuardDuty の用途ではない。
    - C: 正しい。
    - D: 誤り。自動で作成しない。

    **スキル:** [イベント駆動](../domain2.md#t2-4-event) / **参照:** [修復](../../../services/governance.md#config-remediation)

### 問12 {#q12}

EventBridge と Lambda で SG を修復しています。修復の変更がまた同じルールを起動し、Lambda が失敗したときのイベントも失われています。最も適切な改善はどれですか。

- A. Lambda のタイムアウトを 15 分にして、修復を完了させる
- B. ルールのパターンを広げて、全部の SG の変更を受ける
- C. Lambda の同時実行を 1 にして、失敗のイベントを減らす
- D. パターンで修復の実行者を除外し、DLQ と再試行も設定する

??? success "答えと解説"
    **正解: D**

    ループと失敗時の処理を決めます。

    - A: 誤り。ループとイベントの喪失は解決しない。
    - B: 誤り。ループが増える。
    - C: 誤り。ループは止まらず、失敗の保管にもならない。
    - D: 正しい。

    **スキル:** [イベント駆動](../domain2.md#t2-4-event) / **参照:** [EventBridge による修復パターン](../../../services/operations.md#eventbridge-remediation), [ターゲットの再試行と DLQ](../../../services/messaging.md#target-retry-dlq)

### 問13 {#q13}

テンプレートにサブネットの AZ 名 `ap-northeast-1a` と `ap-northeast-1c` が書かれています。別のリージョンへの展開が失敗しました。リージョンの追加はこれからも続きます。最も適切な修正はどれですか。

- A. `AWS::Region` を AZ 名としてそのまま指定する
- B. `Mappings` にリージョンごとの AZ 名を全部書き続ける
- C. スタックの作成を東京に限定して、他のリージョンは手で作る
- D. `Fn::GetAZs` かパラメータで AZ 名を渡す

??? success "答えと解説"
    **正解: D**

    AZ 名を書きません。

    - A: 誤り。リージョン名は AZ 名ではない。
    - B: 誤り。動くがハードコードが増え、追加のたびに更新が要る。
    - C: 誤り。要件に反する。
    - D: 正しい。

    **スキル:** [ハードコード](../domain2.md#t2-4-hardcoding) / **参照:** [パラメータ](../../../services/iac.md#parameters), [擬似パラメータ](../../../services/iac.md#pseudo-parameters)

### 問14 {#q14}

テンプレートに `10.0.0.0/16` を書いて複数のアカウントへ展開したところ、Transit Gateway の経路が重複しました。CIDR を毎回人が決めることも避けたいと考えています。最も適切な修正はどれですか。

- A. パラメータにして、展開のたびに担当者が空きを探して入力する
- B. `Mappings` にアカウントごとの CIDR を書く
- C. 重複する VPC にプライベート NAT を置いて、経路の重複を回避する
- D. IPAM のプールから CIDR を自動で割り当てて、重複を防ぐ

??? success "答えと解説"
    **正解: D**

    IPAM で重複を防ぎます。

    - A: 誤り。人が決める作業が残る。
    - B: 誤り。手動の管理とハードコードが残る。
    - C: 誤り。根本の対処にならず、構成も複雑になる。
    - D: 正しい。

    **スキル:** [ハードコード](../domain2.md#t2-4-hardcoding) / **参照:** [IPAM](../../../services/network-connectivity.md#ipam), [パラメータ](../../../services/iac.md#parameters)

### 問15 {#q15}

ネットワークのテンプレートのハードコードを減らします。置き換えとして正しいものを選んでください。（2つ選択）

- A. リソース名: 環境ごとに固定の名前
- B. アカウント ID: `AWS::AccountId`
- C. AMI ID: Parameter Store の公開パラメータ
- D. VPC の ID: テンプレートの文字列
- E. BGP の MD5 キー: `Mappings` の値

??? success "答えと解説"
    **正解: B, C**

    ハードコードの代わりの手段です。

    - A: 誤り。名前を指定しないほうが再作成や別リージョンで衝突しない。
    - B: 正しい。
    - C: 正しい。
    - D: 誤り。パラメータかエクスポートを使う。
    - E: 誤り。シークレットは Secrets Manager の動的参照。

    **スキル:** [ハードコード](../domain2.md#t2-4-hardcoding) / **参照:** [擬似パラメータ](../../../services/iac.md#pseudo-parameters), [CloudFormation テンプレート](../../../services/iac.md#cloudformation-template)

### 問16 {#q16}

CloudFormation で VPN を作成するとき、オンプレミスのルーターの管理 API も呼び、削除のときは設定を戻します。スタックのライフサイクルに連動させます。最も適切なものはどれですか。

- A. カスタムリソースで Lambda を呼んで連動させる
- B. `UserData` でルーターの API を呼ぶ
- C. Parameter Store の値をルーターが定期的に読む
- D. `Outputs` にルーターの設定を出力して、担当者が適用する

??? success "答えと解説"
    **正解: A**

    カスタムリソースで外部の仕組みを操作します。

    - A: 正しい。
    - B: 誤り。EC2 の起動の機能で、スタックの削除に連動しない。
    - C: 誤り。作成と削除に連動しない。
    - D: 誤り。手動で、連動しない。

    **スキル:** [ハイブリッドの自動化](../domain2.md#t2-4-hybrid) / **参照:** [カスタムリソース](../../../services/iac.md#custom-resources)

### 問17 {#q17}

データセンターの管理サーバーでスクリプトを実行し、ネットワーク機器へ設定を流します。SSM Agent は導入でき、受信のポートは開けません。AWS から実行を制御します。最も適切なものはどれですか。

- A. 管理サーバーに EC2 のインスタンスプロファイルを付ける
- B. CodeDeploy のエージェントなしのデプロイで、機器へ直接送る
- C. Systems Manager のハイブリッドノードと Run Command
- D. Session Manager の代わりに、SSH の受信のポートを公開する

??? success "答えと解説"
    **正解: C**

    オンプレミスのノードも管理できます。

    - A: 誤り。EC2 の仕組みで、オンプレミスには付けられない。
    - B: 誤り。エージェントなしの対象の手段ではない。
    - C: 正しい。
    - D: 誤り。受信のポートを開けない条件に反する。

    **スキル:** [ハイブリッドの自動化](../domain2.md#t2-4-hybrid) / **参照:** [オンプレミスと他クラウド](../../../services/operations.md#hybrid-nodes), [Run Command](../../../services/operations.md#run-command)

### 問18 {#q18}

新しい VPC の作成をきっかけに、オンプレミスのルーターの経路を更新します。また、新しい VPN は設定を取得して構成管理ツールへ渡します。最も適切な組み合わせはどれですか。

- A. EventBridge で検知し、VPN の設定をダウンロードして渡す
- B. Route 53 の Forward ルールで経路の更新を通知する
- C. 変更セットの結果を、オンプレミスのルーターへ直接適用する
- D. CloudTrail のログファイルをルーターへコピーして読み込ませる

??? success "答えと解説"
    **正解: A**

    イベント駆動で連携します。

    - A: 正しい。
    - B: 誤り。DNS の機能で、経路の更新にならない。
    - C: 誤り。変更セットは AWS のリソースの差分。
    - D: 誤り。ルーターの設定にならない。

    **スキル:** [ハイブリッドの自動化](../domain2.md#t2-4-hybrid) / **参照:** [EventBridge による修復パターン](../../../services/operations.md#eventbridge-remediation), [Site-to-Site VPN](../../../services/network-connectivity.md#site-to-site-vpn)

### 問19 {#q19}

本番の Transit Gateway のスタックで、更新時の重要なリソースの置き換えと、スタックの誤った削除を防ぎます。デプロイの速度はできるだけ落としません。適切な組み合わせを選んでください。（2つ選択）

- A. ドリフト検出を毎時実行して置き換えを止める
- B. スタックポリシーで重要なリソースの更新を拒否する
- C. 全リソースの `Outputs` を出力して履歴を残す
- D. ロールバックを無効にして、更新の失敗で止める
- E. `DeletionPolicy` と終了保護を設定する

??? success "答えと解説"
    **正解: B, E**

    変更の失敗と誤削除を防ぎます。

    - A: 誤り。手動の変更の検出で、更新を止めない。
    - B: 正しい。
    - C: 誤り。保護にならない。
    - D: 誤り。保護にならず、状態の回復も難しくなる。
    - E: 正しい。

    **スキル:** [リスクとコスト](../domain2.md#t2-4-risk-cost) / **参照:** [スタックポリシー](../../../services/iac.md#stack-policy), [リソースの属性: DeletionPolicy](../../../services/iac.md#deletion-policy)

### 問20 {#q20}

ネットワークの更新のあと、接続の確認を自動化します。また、更新の間にアラームが発報したら自動で戻します。最も適切な組み合わせはどれですか。

- A. 変更セットの作成とスタックポリシーの更新
- B. デプロイ後の Reachability Analyzer とロールバックトリガー
- C. Trusted Advisor の週次のチェックと手動の復旧の手順
- D. Network Flow Monitor の導入と `DeletionPolicy` の設定

??? success "答えと解説"
    **正解: B**

    接続の確認を自動にします。

    - A: 誤り。実行前の確認と保護で、実行後の確認にならない。
    - B: 正しい。
    - C: 誤り。自動の確認にならない。
    - D: 誤り。確認と戻す仕組みになっていない。

    **スキル:** [リスクとコスト](../domain2.md#t2-4-risk-cost) / **参照:** [ロールバックトリガー](../../../services/iac.md#rollback-triggers), [Reachability Analyzer](../../../services/network-connectivity.md#reachability-analyzer)

### 問21 {#q21}

ネットワークの費用を見直して、使っていない資源の課金を止めます。整理の対象として費用の削減につながるものを選んでください。（2つ選択）

- A. 使っていない SG
- B. 関連付けのないルートテーブル
- C. 調査の終わった Traffic Mirroring のセッション
- D. 未使用の NAT ゲートウェイとインターフェイスエンドポイント
- E. S3 と DynamoDB のゲートウェイエンドポイント

??? success "答えと解説"
    **正解: C, D**

    使わない資源の課金を止めます。

    - A: 誤り。SG 自体に料金はない。
    - B: 誤り。ルートテーブル自体に料金はない。
    - C: 正しい。
    - D: 正しい。
    - E: 誤り。無料で、削除しても費用は減らない。

    **スキル:** [リスクとコスト](../domain2.md#t2-4-risk-cost) / **参照:** [データ転送の費用](../../../services/cost-management.md#data-transfer), [Traffic Mirroring](../../../services/network-connectivity.md#traffic-mirroring)

### 問22 {#q22}

同じテンプレートで本番と開発を作ります。本番は NAT ゲートウェイを AZ ごと、開発は費用を抑えて 1 つにします。テンプレートは 1 つのままにします。最も適切な方法はどれですか。

- A. `Conditions` で環境を判定して NAT の作成を分ける
- B. 本番にスタックポリシーを付けて、開発の NAT の作成を拒否する
- C. `Metadata` に環境名を書いて、NAT の数を読み取らせる
- D. 環境ごとにテンプレートを複製して、差分をレビューで確認する

??? success "答えと解説"
    **正解: A**

    条件分岐で調整します。

    - A: 正しい。
    - B: 誤り。用途が違う。
    - C: 誤り。条件分岐の機能ではない。
    - D: 誤り。同じ変更を繰り返すことになる。

    **スキル:** [最適化](../domain2.md#t2-4-optimize) / **参照:** [マッピングと条件](../../../services/iac.md#mappings-conditions), [NAT ゲートウェイ](../../../services/network-connectivity.md#nat-gateway)

### 問23 {#q23}

全 VPC で S3 への大量の通信が NAT ゲートウェイを通り、処理料金が大きくなっています。VPC は IaC で管理しています。アプリの変更はしません。最も適切な変更はどれですか。

- A. テンプレートに S3 のゲートウェイエンドポイントを追加する
- B. テンプレートで S3 のインターフェイスエンドポイントを AZ ごとに追加する
- C. テンプレートで NAT のサブネットを AZ ごとに分ける
- D. テンプレートで NAT の Elastic IP を増やす

??? success "答えと解説"
    **正解: A**

    ゲートウェイエンドポイントは無料です。

    - A: 正しい。
    - B: 誤り。時間料金と処理料金がかかり、ゲートウェイ型より高い。
    - C: 誤り。S3 への処理料金は残る。
    - D: 誤り。処理料金は減らない。

    **スキル:** [最適化](../domain2.md#t2-4-optimize) / **参照:** [VPC エンドポイントと PrivateLink](../../../services/networking.md#vpc-endpoints), [CloudFormation テンプレート](../../../services/iac.md#cloudformation-template)

### 問24 {#q24}

全 VPC に同じ種類のインターフェイスエンドポイントが重複して作られています。VPC は Transit Gateway で接続済みです。費用を下げ、構成はコードで維持します。最も適切な方針はどれですか。

- A. 共有 VPC に集約し、PHZ で各 VPC へ解決を配る
- B. VPC ごとにエンドポイントの AZ を増やして、処理料金を分散する
- C. プライベート DNS を無効にし、各アプリの URL にエンドポイント ID を書く
- D. 全 VPC にゲートウェイエンドポイントを作り、全サービスの通信を置き換える

??? success "答えと解説"
    **正解: A**

    Transit Gateway の処理料金と比較したうえで集約します。

    - A: 正しい。
    - B: 誤り。時間料金が増える。
    - C: 誤り。費用は減らず、ハードコードも増える。
    - D: 誤り。ゲートウェイエンドポイントは S3 と DynamoDB のみ。

    **スキル:** [最適化](../domain2.md#t2-4-optimize) / **参照:** [VPC エンドポイントと PrivateLink](../../../services/networking.md#vpc-endpoints), [Transit Gateway](../../../services/network-connectivity.md#transit-gateway)

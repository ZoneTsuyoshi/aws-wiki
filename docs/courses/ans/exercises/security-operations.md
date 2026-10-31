# 監査と通知の自動化の問題集

対象の解説: [Firewall Manager](../../../services/threat-detection.md#firewall-manager), [AWS Config](../../../services/governance.md#config), [Security Hub](../../../services/threat-detection.md#security-hub), [EventBridge による自動化](../../../services/threat-detection.md#ir-eventbridge), [アラーム](../../../services/observability.md#alarms)

### 問1 {#q1}

災害復旧の要件で、DX の切り替えと、サブネットの通信の断をテストします。本番のルーターの設定は変えず、結果を証跡に残します。適切な方法を選んでください。（2つ選択）

- A. AWS FIS の `aws:network:disrupt-connectivity` を使う
- B. オンプレミスのルーターの電源を担当者が切る
- C. Reachability Analyzer で切り替えの時間を測る
- D. CloudWatch アラームを `ALARM` に手で変更する
- E. DX のフェイルオーバーテストで BGP を止める

??? success "答えと解説"
    **正解: A, E**

    テストの方法です。

    - A: 正しい。
    - B: 誤り。ルーターの設定を変えない条件には合うが、制御と証跡に欠け、手順として危険。
    - C: 誤り。パケットを送らない解析で、切り替えの時間を測れない。
    - D: 誤り。BGP や通信の断は起きない。
    - E: 正しい。

    **スキル:** [テスト](../domain4.md#t4-1-testing) / **参照:** [回復性のモデル](../../../services/network-connectivity.md#dx-resiliency), [AWS Fault Injection Service(FIS)](../../../services/resilience.md#fis)

### 問2 {#q2}

監査のため、IGW から届くリソースの一覧を四半期ごとに作り、結果を証跡に残します。パケットは送りません。特定の 2 点ではなく環境全体を確認します。最も適切なものはどれですか。

- A. Network Access Analyzer
- B. 外部のポートスキャンを四半期ごとに実行する
- C. Reachability Analyzer の分析を全 ENI の組み合わせで実行する
- D. Traffic Mirroring で IGW の通信をコピーする

??? success "答えと解説"
    **正解: A**

    望まない経路を環境全体で調べます。

    - A: 正しい。
    - B: 誤り。パケットを送る。
    - C: 誤り。特定の 2 点の解析で、組み合わせが多すぎる。
    - D: 誤り。実際の通信のコピーで、到達の可能性の一覧にならない。

    **スキル:** [テスト](../domain4.md#t4-1-testing) / **参照:** [Network Access Analyzer](../../../services/network-connectivity.md#network-access-analyzer)

### 問3 {#q3}

AZ の障害を想定して ALB のトラフィックを切り離すテストを行い、ネットワークの設定の準拠は継続的に評価します。組み合わせとして最も適切なものはどれですか。

- A. Global Accelerator のダイヤルと GuardDuty
- B. CloudFront のオリジンフェイルオーバーと Trusted Advisor
- C. Route 53 の TTL の短縮と CloudTrail Lake
- D. ARC のゾーンシフトで AZ を切り離し、Config の適合パックで評価する

??? success "答えと解説"
    **正解: D**

    テストの結果を証跡に残します。

    - A: 誤り。リージョンの切り離しで、準拠の評価でもない。
    - B: 誤り。AZ の切り離しのテストにならず、継続の評価でもない。
    - C: 誤り。AZ の切り離しの機能にならず、準拠の評価でもない。
    - D: 正しい。

    **スキル:** [テスト](../domain4.md#t4-1-testing) / **参照:** [ゾーンシフトとオートシフト](../../../services/resilience.md#arc-zonal), [適合パック](../../../services/governance.md#config-conformance-packs)

### 問4 {#q4}

GuardDuty が EC2 の C2 への通信を検出したら、数分以内にインスタンスを隔離して、セキュリティチームへ通知します。夜間も人手なしで動かします。最も適切な構成はどれですか。

- A. EventBridge で受け、Lambda で隔離し SNS で通知する
- B. CloudTrail のログを毎日 Athena で調べ、担当者が隔離する
- C. Security Hub のダッシュボードを 24 時間体制で監視する
- D. Shield Advanced の SRT に通知して隔離を依頼する

??? success "答えと解説"
    **正解: A**

    イベント駆動の構成です。

    - A: 正しい。
    - B: 誤り。数分以内にならず、人手が必要。
    - C: 誤り。人手なしの条件に反する。
    - D: 誤り。SRT は DDoS の支援で、隔離の依頼先ではない。

    **スキル:** [通知の自動化](../domain4.md#t4-1-automation) / **参照:** [EventBridge による自動化](../../../services/threat-detection.md#ir-eventbridge), [EC2 の隔離](../../../services/threat-detection.md#ir-ec2-isolation)

### 問5 {#q5}

開放された SG を継続的に検出して修正します。準拠の履歴も残し、アカウントごとの修復のコードを最小にします。最も適切なものはどれですか。

- A. Trusted Advisor の結果を毎週メールで確認して修正する
- B. フローログの `ACCEPT` を数えて SG を修正する
- C. 各アカウントに SG の確認スクリプトの EC2 を常駐させる
- D. Config のルールと Automation の修復を組み合わせる

??? success "答えと解説"
    **正解: D**

    非準拠を修復します。

    - A: 誤り。継続の修復にならない。
    - B: 誤り。通信の記録で、設定の評価ではない。
    - C: 誤り。コードと運用が増える。
    - D: 正しい。

    **スキル:** [通知の自動化](../domain4.md#t4-1-automation) / **参照:** [修復](../../../services/governance.md#config-remediation), [EventBridge による修復パターン](../../../services/operations.md#eventbridge-remediation)

### 問6 {#q6}

GuardDuty の DNS ベースの検出が出ていません。この VPC は独自の DNS サーバーを使い、外部のリゾルバーへ再帰問い合わせをしています。正しい説明はどれですか。

- A. DNS ベースの検出は AWS のリゾルバーを使う場合だけ働く
- B. Resolver クエリログを無効にすると、検出の処理が優先される
- C. Security Hub を有効にすれば、検出の範囲が DNS まで広がる
- D. GuardDuty は独自の DNS サーバーの問い合わせも分析するので、別の原因を調べる

??? success "答えと解説"
    **正解: A**

    検出の前提を確認します。

    - A: 正しい。
    - B: 誤り。検出の条件ではない。
    - C: 誤り。集約のサービスで、検出の条件は変わらない。
    - D: 誤り。AWS のリゾルバーを使っている場合に働く。

    **スキル:** [通知の自動化](../domain4.md#t4-1-automation) / **参照:** [GuardDuty](../../../services/threat-detection.md#guardduty), [Security Hub](../../../services/threat-detection.md#security-hub)

### 問7 {#q7}

監査で 2 つの質問を受けました。質問 1: SG を誰がいつ変更したか。質問 2: どの IP からの通信が拒否されたか。それぞれの確認先の組み合わせとして正しいものはどれですか。

- A. 1 はフローログ、2 は CloudTrail
- B. 1 は Config のアグリゲーター、2 は Traffic Mirroring
- C. 1 は Network Manager、2 は Route Analyzer
- D. 1 は CloudTrail、2 はフローログ

??? success "答えと解説"
    **正解: D**

    サービスの違いです。

    - A: 誤り。逆。
    - B: 誤り。Config は誰が変えたかを直接示さず、ミラーは拒否の記録ではない。
    - C: 誤り。どちらも質問の記録を持たない。
    - D: 正しい。

    **スキル:** [サービス](../domain4.md#t4-2-services) / **参照:** [CloudTrail の設定](../../../services/observability.md#cloudtrail), [フローログの分析](../../../services/network-connectivity.md#flow-log-analysis)

### 問8 {#q8}

ルートテーブルの設定を時系列で確認し、3 か月前の状態と比べます。API の呼び出しの一覧ではなく、設定そのものの履歴が必要です。最も適切なものはどれですか。

- A. VPC フローログのカスタム形式
- B. CloudTrail のイベント履歴
- C. Network Synthetic Monitor のプローブ
- D. AWS Config の設定の履歴

??? success "答えと解説"
    **正解: D**

    設定の変更履歴は Config です。

    - A: 誤り。通信の記録。
    - B: 誤り。API の呼び出しの記録で、設定の状態ではない。
    - C: 誤り。遅延と損失の測定。
    - D: 正しい。

    **スキル:** [サービス](../domain4.md#t4-2-services) / **参照:** [Config と CloudTrail の違い](../../../services/governance.md#config-vs-cloudtrail), [接続の調査](../../../services/network-connectivity.md#network-analysis)

### 問9 {#q9}

ネットワークの監査で、ツールの限界を説明します。ツールと「分からないこと」の組み合わせで正しいものを選んでください。（2つ選択）

- A. CloudTrail: 誰が API を呼んだか
- B. CloudWatch: 指標の集約とアラーム
- C. フローログ: パケットの中身と DNS の問い合わせ
- D. Network Manager: 個々のフロー
- E. Traffic Mirroring: パケットの中身

??? success "答えと解説"
    **正解: C, D**

    分からないことも覚えます。

    - A: 誤り。分かる。
    - B: 誤り。できる。
    - C: 正しい。
    - D: 正しい。
    - E: 誤り。分かる。

    **スキル:** [サービス](../domain4.md#t4-2-services) / **参照:** [CloudWatch と CloudTrail の違い](../../../services/observability.md#cloudtrail-vs-cloudwatch), [Traffic Mirroring](../../../services/network-connectivity.md#traffic-mirroring)

### 問10 {#q10}

組織の全アカウントで SG を監査し、Network Firewall のポリシーも配ります。Firewall Manager の前提として正しいものを選んでください。（2つ選択）

- A. 全アカウントの CloudTrail Lake の有効化
- B. 全アカウントに Shield Advanced の契約
- C. Network Firewall のポリシーには RAM の組織共有
- D. Organizations のすべての機能と対象での AWS Config
- E. 全 VPC の Traffic Mirroring の有効化

??? success "答えと解説"
    **正解: C, D**

    前提を確認します。

    - A: 誤り。前提ではない。
    - B: 誤り。SG のポリシーの前提ではない。
    - C: 正しい。
    - D: 正しい。
    - E: 誤り。前提ではない。

    **スキル:** [設定の監査](../domain4.md#t4-2-audit) / **参照:** [Firewall Manager](../../../services/threat-detection.md#firewall-manager)

### 問11 {#q11}

200 のアカウントの準拠を 1 か所で確認し、標準に沿ったコントロールの結果も集約します。非準拠の通知もまとめます。最も適切なものはどれですか。

- A. Network Access Analyzer の結果を CloudTrail へ送る
- B. 各アカウントの Trusted Advisor を担当者が順に確認する
- C. Config のアグリゲーターと Security Hub CSPM
- D. 全アカウントのフローログを 1 つのバケットへ集める

??? success "答えと解説"
    **正解: C**

    戦略の組み立てです。

    - A: 誤り。準拠の集約にならない。
    - B: 誤り。手動で、標準の集約にならない。
    - C: 正しい。
    - D: 誤り。通信の記録で、設定の準拠の評価にならない。

    **スキル:** [設定の監査](../domain4.md#t4-2-audit) / **参照:** [アグリゲーター](../../../services/governance.md#config-aggregators), [Security Hub CSPM の標準とコントロール](../../../services/threat-detection.md#security-hub-cspm)

### 問12 {#q12}

複数のアカウントの監査で、担当者ごとに使うツールを割り当てています。仕組みと監査の対象の組み合わせで正しいものはどれですか。

- A. Firewall Manager: DNS の問い合わせの全文の記録
- B. Network Access Analyzer: API の呼び出しの履歴
- C. IAM Access Analyzer: 外部へ公開されたリソースの検出
- D. Trusted Advisor: 組織の SG の基準の強制と修復

??? success "答えと解説"
    **正解: C**

    仕組みの違いです。

    - A: 誤り。ポリシーの適用の機能。
    - B: 誤り。望まない経路の分析。
    - C: 正しい。
    - D: 誤り。手軽な点検で、強制はしない。

    **スキル:** [設定の監査](../domain4.md#t4-2-audit) / **参照:** [Trusted Advisor](../../../services/cloud-foundations.md#trusted-advisor), [IAM Access Analyzer](../../../services/identity-directory.md#access-analyzer)

### 問13 {#q13}

VPN の片方のトンネルの保守の通知が多く、運用者が疲れています。両方のトンネルが同時に落ちたときだけ通知します。既存のトンネルごとのアラームはあります。最も適切なものはどれですか。

- A. 片方の `TunnelState` のしきい値を 0.5 にする
- B. 複合アラームで 2 つのアラームを AND で評価する
- C. 異常検知のアラームを `TunnelDataIn` に設定する
- D. CloudTrail の `ModifyVpnTunnelOptions` を EventBridge で受ける

??? success "答えと解説"
    **正解: B**

    複数の条件で誤報を減らします。

    - A: 誤り。片方でも通知する。
    - B: 正しい。
    - C: 誤り。両方の断の条件ではない。
    - D: 誤り。状態の評価ではない。

    **スキル:** [通知の仕組み](../domain4.md#t4-2-alerts) / **参照:** [複合アラーム](../../../services/observability.md#composite-alarms)

### 問14 {#q14}

フローログを CloudWatch Logs へ送っています。拒否が毎分 100 件を超えたら通知します。アプリの変更はしません。最も適切な手順はどれですか。

- A. Athena のクエリを Lambda で毎分実行して通知する
- B. `PutMetricData` を呼ぶプログラムを各 EC2 で実行する
- C. Trusted Advisor の確認を毎分 API で更新する
- D. メトリクスフィルターで `REJECT` を数えてアラームを付ける

??? success "答えと解説"
    **正解: D**

    カスタムメトリクスの典型です。

    - A: 誤り。動くが、メトリクスフィルターより費用と手間が大きい。
    - B: 誤り。アプリの追加が要り、フローログの数を扱わない。
    - C: 誤り。用途が違う。
    - D: 正しい。

    **スキル:** [通知の仕組み](../domain4.md#t4-2-alerts) / **参照:** [メトリクスフィルター](../../../services/observability.md#metric-filters)

### 問15 {#q15}

自前のプローブが測った遅延と、EC2 の OS の `ethtool` の統計をカスタムメトリクスにします。組み合わせとして最も適切なものはどれですか。

- A. プローブは Route 53 のヘルスチェック、統計は Config のルール
- B. プローブは EMF、統計は CloudTrail の管理イベント
- C. プローブはフローログのカスタム形式、統計は `tcp-flags` の集計
- D. プローブは `PutMetricData`、統計は CloudWatch エージェント

??? success "答えと解説"
    **正解: D**

    作り方の違いです。

    - A: 誤り。目的のメトリクスにならない。
    - B: 誤り。CloudTrail に OS の統計はない。
    - C: 誤り。これらの値は記録されない。
    - D: 正しい。

    **スキル:** [通知の仕組み](../domain4.md#t4-2-alerts) / **参照:** [PutMetricData でカスタムメトリクスを送る](../../../services/observability.md#put-metric-data), [CloudWatch エージェント](../../../services/operations.md#cloudwatch-agent)

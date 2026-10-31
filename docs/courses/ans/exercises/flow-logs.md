# フローログと Traffic Mirroringの問題集

対象の解説: [フローログの分析](../../../services/network-connectivity.md#flow-log-analysis), [Traffic Mirroring](../../../services/network-connectivity.md#traffic-mirroring), [VPC フローログの調査](../../../services/threat-detection.md#investigate-flow-logs), [ログの調査](../../../services/threat-detection.md#log-investigation)

### 問1 {#q1}

全 VPC の通信の有無を常に記録し、特定の ENI のパケットだけは IDS へ送ります。ログの費用は抑えます。設計として最も適切なものはどれですか。

- A. 全 VPC でフローログ、必要な ENI だけ Traffic Mirroring
- B. 必要な ENI だけフローログ、全 VPC で Traffic Mirroring
- C. 全 VPC でフローログ、IDS にはフローログをそのまま送ってシグネチャを照合する
- D. 全 ENI で Traffic Mirroring、フローログは不要として削除する

??? success "答えと解説"
    **正解: A**

    メタデータとパケットの使い分けです。

    - A: 正しい。
    - B: 誤り。範囲が逆で費用も大きい。
    - C: 誤り。フローログに中身はない。
    - D: 誤り。量と費用が大きく、記録の目的に合わない。

    **スキル:** [フローログと Traffic Mirroring](../domain1.md#t1-4-flow-mirror) / **参照:** [フローログの分析](../../../services/network-connectivity.md#flow-log-analysis), [Traffic Mirroring](../../../services/network-connectivity.md#traffic-mirroring)

### 問2 {#q2}

既定の形式のフローログを作成済みです。NAT の裏の元の IP を見るため `pkt-srcaddr` が必要になりました。正しい対応はどれですか。

- A. カスタム形式のフローログを新しく作成し、古いものを削除する
- B. 既存のフローログの形式を編集して、`pkt-srcaddr` を追加する
- C. 既存のフローログの IAM ロールを変更して、`pkt-srcaddr` を出力させる
- D. S3 の Parquet 形式へ変えるだけで、自動で項目が増える

??? success "答えと解説"
    **正解: A**

    作成後は変更できないので作り直します。

    - A: 正しい。
    - B: 誤り。作成後は変更できない。
    - C: 誤り。作成後は変更できず、形式の問題でもある。
    - D: 誤り。形式の変換で項目は増えない。

    **スキル:** [フローログと Traffic Mirroring](../domain1.md#t1-4-flow-mirror) / **参照:** [フローログの分析](../../../services/network-connectivity.md#flow-log-analysis)

### 問3 {#q3}

不審なホストの通信を調査します。通信先と時刻は既に分かり、次にペイロードを確認します。TLS ではない通信です。最も適切なものはどれですか。

- A. CloudTrail のデータイベントでペイロードを記録する
- B. Traffic Mirroring でパケットをコピーして解析する
- C. Reachability Analyzer で当該の ENI のパケットを取得する
- D. フローログの集約間隔を 1 分にして、ペイロードを記録する

??? success "答えと解説"
    **正解: B**

    中身の確認は Traffic Mirroring です。

    - A: 誤り。API の記録。
    - B: 正しい。
    - C: 誤り。パケットを送らず、取得もしない。
    - D: 誤り。間隔を変えても中身は記録されない。

    **スキル:** [フローログと Traffic Mirroring](../domain1.md#t1-4-flow-mirror) / **参照:** [Traffic Mirroring](../../../services/network-connectivity.md#traffic-mirroring), [フローログの分析](../../../services/network-connectivity.md#flow-log-analysis)

### 問4 {#q4}

フローログで、EC2 の受信の記録が `ACCEPT`、対応する送信の記録が `REJECT` です。SG は戻りの通信を自動で許可します。最も可能性の高い原因はどれですか。

- A. ルートテーブルに戻りの経路がないので `REJECT` と記録される
- B. NACL の送信でエフェメラルポートが拒否されている
- C. SG の送信のルールで戻りの通信が拒否されている
- D. インスタンスの OS のファイアウォールが戻りを拒否している

??? success "答えと解説"
    **正解: B**

    片方だけ `REJECT` なら NACL を疑います。

    - A: 誤り。経路の不足は `REJECT` の記録にならない。
    - B: 正しい。
    - C: 誤り。SG はステートフルで戻りを許可する。
    - D: 誤り。OS のドロップはフローログの `REJECT` にならない。

    **スキル:** [収集と分析](../domain3.md#t3-2-tools) / **参照:** [フローログの分析](../../../services/network-connectivity.md#flow-log-analysis)

### 問5 {#q5}

フローログで `tcp-flags=2` の記録が続き、相手からの応答の記録がありません。`action` は `ACCEPT` です。解釈として最も適切なものはどれですか。

- A. RST を受け取ったので、相手のアプリが接続を切断している
- B. SG が SYN を拒否している。`action` は無視してよい
- C. 接続は確立していて、データの転送の記録が省略されている
- D. SYN を送ったが応答が返らず、経路か相手側の問題を疑う

??? success "答えと解説"
    **正解: D**

    `tcp-flags` の値で判断します。

    - A: 誤り。RST は `4`。
    - B: 誤り。拒否なら `REJECT` になる。
    - C: 誤り。SYN だけで確立していない。
    - D: 正しい。

    **スキル:** [収集と分析](../domain3.md#t3-2-tools) / **参照:** [フローログの分析](../../../services/network-connectivity.md#flow-log-analysis)

### 問6 {#q6}

フローログのレコードに `log-status=SKIPDATA` があります。同時に Amazon DNS への問い合わせが見当たらないという報告もあります。正しい説明を選んでください。（2つ選択）

- A. DHCP とメタデータの通信はすべて `ACCEPT` で記録される
- B. Amazon DNS への問い合わせは記録の対象外である
- C. `SKIPDATA` はその通信が拒否されたことを示す
- D. ARP の通信は `REJECT` で記録される
- E. `SKIPDATA` は集約期間の記録が欠けたことを示す

??? success "答えと解説"
    **正解: B, E**

    記録されないものもあります。

    - A: 誤り。記録の対象外。
    - B: 正しい。
    - C: 誤り。`action` で示す。
    - D: 誤り。記録の対象外。
    - E: 正しい。

    **スキル:** [収集と分析](../domain3.md#t3-2-tools) / **参照:** [フローログの分析](../../../services/network-connectivity.md#flow-log-analysis)

### 問7 {#q7}

アプリで再送が増えています。ウィンドウの縮小や断片化の有無を調べるため、Wireshark でパケットを読みます。Traffic Mirroring を設定しましたが、ターゲットに何も届きません。VXLAN の受信の準備はできています。原因として可能性が高いものはどれですか。

- A. ミラーのセッション番号を 1 にしている
- B. フィルターにルールがなく、コピーの対象がない
- C. ターゲットの SG で TCP 4789 を拒否している
- D. 送信元の ENI に Elastic IP がない

??? success "答えと解説"
    **正解: B**

    ルールがなければ何もコピーしません。

    - A: 誤り。番号は順序で、1 でも動作する。
    - B: 正しい。
    - C: 誤り。UDP 4789 が必要で、TCP の話ではない。
    - D: 誤り。条件ではない。

    **スキル:** [パケットの分析](../domain3.md#t3-2-packets) / **参照:** [Traffic Mirroring](../../../services/network-connectivity.md#traffic-mirroring)

### 問8 {#q8}

Traffic Mirroring で 2 つのセッションを同じ ENI に設定し、片方は IDS へ、片方は分析用へ送るつもりでした。同じパケットは片方にしか届きません。正しい説明はどれですか。

- A. 番号の小さいセッションから評価され、パケットは 1 回しかコピーされない
- B. 2 つのターゲットが同じ AZ のときだけ、両方にコピーされる
- C. 番号の大きいセッションだけが有効で、小さいほうは常に無視される
- D. ターゲットの数だけ同じパケットがコピーされるが、VNI が同じだと重複として破棄される

??? success "答えと解説"
    **正解: A**

    2 か所へ送るならターゲットの先で分けます。

    - A: 正しい。
    - B: 誤り。AZ の条件ではない。
    - C: 誤り。小さい順に評価される。
    - D: 誤り。1 回しかコピーされない。

    **スキル:** [パケットの分析](../domain3.md#t3-2-packets) / **参照:** [Traffic Mirroring](../../../services/network-connectivity.md#traffic-mirroring)

### 問9 {#q9}

インスタンスの帯域の上限に当たると、キューイングや破棄が起こるとされています。Traffic Mirroring で再送の増加を確認しました。上限に当たっているかの裏付けとして、最も適切な確認はどれですか。

- A. CloudTrail で `RunInstances` のイベントを確認する
- B. Route 53 のクエリログで `SERVFAIL` の件数を確認する
- C. `ethtool -S` の `allowance_exceeded` の統計を確認する
- D. `TunnelState` のメトリクスで 0 の回数を確認する

??? success "答えと解説"
    **正解: C**

    統計と合わせて確認します。

    - A: 誤り。インスタンスの起動の記録。
    - B: 誤り。DNS の記録。
    - C: 正しい。
    - D: 誤り。VPN のトンネルの状態。

    **スキル:** [パケットの分析](../domain3.md#t3-2-packets) / **参照:** [MTU とジャンボフレーム](../../../services/network-connectivity.md#mtu), [Traffic Mirroring](../../../services/network-connectivity.md#traffic-mirroring)

### 問10 {#q10}

NAT ゲートウェイの ENI のフローログで不審な通信を調べます。`srcaddr` は NAT の IP です。送信元の EC2 のプライベート IP を特定するフィールドはどれですか。

- A. `pkt-srcaddr`。パケットの元の送信元 IP が入る
- B. `traffic-path`。外へ出る経路の情報に元の IP が入る
- C. `pkt-dst-aws-service`。AWS サービスの名前に元の IP が入る
- D. `instance-id`。NAT の ENI の記録に元の EC2 が入る

??? success "答えと解説"
    **正解: A**

    既定の形式にはないのでカスタム形式で作ります。

    - A: 正しい。
    - B: 誤り。経路の種類の値。
    - C: 誤り。サービスの名前の値。
    - D: 誤り。NAT の ENI の記録では EC2 の ID にならない。

    **スキル:** [フローログ](../domain4.md#t4-2-flow-logs) / **参照:** [VPC フローログの調査](../../../services/threat-detection.md#investigate-flow-logs)

### 問11 {#q11}

フローログの `reject-reason` が `BPA` です。ルートも SG も許可しているのに、インターネットへの通信が止まります。最も適切な判断はどれですか。

- A. BGP の経路の上限を超えたので、経路を集約する
- B. SG の最大のルール数を超えているので、ルールを削除する
- C. VPC Block Public Access で止まっているので、除外の設定を確認する
- D. NACL の番号が小さいルールで拒否されているので、順序を変える

??? success "答えと解説"
    **正解: C**

    `BPA` は VPC Block Public Access です。

    - A: 誤り。別の話。
    - B: 誤り。別の話。
    - C: 正しい。
    - D: 誤り。`BPA` の値の意味とは異なる。

    **スキル:** [フローログ](../domain4.md#t4-2-flow-logs) / **参照:** [フローログの分析](../../../services/network-connectivity.md#flow-log-analysis)

### 問12 {#q12}

フローログのカスタム形式について、値の読み方として正しいものを選んでください。（2つ選択）

- A. `tcp-flags=4` は SYN を示す
- B. `flow-direction` はバージョン 2 の既定の項目に含まれる
- C. `tcp-flags=19` は、集約期間で SYN-ACK と FIN が OR されている
- D. `flow-direction=egress` かつ `traffic-path=8` は IGW 経由の外向き
- E. `traffic-path=3` は同じリージョンのピアリング

??? success "答えと解説"
    **正解: C, D**

    値の意味を覚えます。

    - A: 誤り。4 は RST。
    - B: 誤り。バージョン 5 の項目。
    - C: 正しい。
    - D: 正しい。
    - E: 誤り。3 は VGW。

    **スキル:** [フローログ](../domain4.md#t4-2-flow-logs) / **参照:** [フローログの分析](../../../services/network-connectivity.md#flow-log-analysis), [VPC フローログの調査](../../../services/threat-detection.md#investigate-flow-logs)

### 問13 {#q13}

Traffic Mirroring のターゲットを設計します。IDS のアプライアンスを複数の AZ に置き、負荷分散します。最も適切なターゲットはどれですか。

- A. 1 台の IDS の ENI を各 AZ の送信元で共有し、ALB で複製する
- B. ALB の HTTP リスナーと、IDS の Web インターフェイス
- C. UDP の NLB か GWLB エンドポイントをターゲットにする
- D. CloudFront のカスタムオリジンで IDS へ渡す

??? success "答えと解説"
    **正解: C**

    UDP の NLB か GWLB を使います。

    - A: 誤り。負荷分散にならない。
    - B: 誤り。ALB は VXLAN を受けない。
    - C: 正しい。
    - D: 誤り。CloudFront の用途ではない。

    **スキル:** [Traffic Mirroring](../domain4.md#t4-2-mirroring) / **参照:** [Traffic Mirroring](../../../services/network-connectivity.md#traffic-mirroring)

### 問14 {#q14}

監査用の Traffic Mirroring のセッションを設計しています。複数のチームの送信元を、同じターゲットへ送ります。設計の説明として正しいものはどれですか。

- A. 複数の送信元のセッションが同じターゲットを使える
- B. ターゲットの ENI をそのまま送信元にできる
- C. 入力は SG で拒否された受信のパケットもコピーされる
- D. カプセル化は GENEVE の UDP 6081 で固定されている

??? success "答えと解説"
    **正解: A**

    1 つのターゲットで複数の送信元の通信を受けられます。

    - A: 正しい。
    - B: 誤り。ターゲットとして使っている ENI は送信元にできない。
    - C: 誤り。受信で拒否されたパケットはミラーされない。
    - D: 誤り。VXLAN の UDP 4789。

    **スキル:** [Traffic Mirroring](../domain4.md#t4-2-mirroring) / **参照:** [Traffic Mirroring](../../../services/network-connectivity.md#traffic-mirroring)

### 問15 {#q15}

通信量の多い ENI をミラーしたところ、IDS が追いつかず費用も増えました。検査に必要なのは特定のポートの最初のヘッダーだけです。最も適切な対応を選んでください。（2つ選択）

- A. ターゲットの SG を開放する
- B. フィルターで対象のポートに絞る
- C. VXLAN のポートを TCP に変更する
- D. パケットの長さを指定して切り詰める
- E. 送信元の ENI をすべての VPC に広げる

??? success "答えと解説"
    **正解: B, D**

    量を減らします。

    - A: 誤り。量は減らない。
    - B: 正しい。
    - C: 誤り。変更できない。
    - D: 正しい。
    - E: 誤り。量が増える。

    **スキル:** [Traffic Mirroring](../domain4.md#t4-2-mirroring) / **参照:** [Traffic Mirroring](../../../services/network-connectivity.md#traffic-mirroring)

### 問16 {#q16}

ALB のアクセスログの有効化が権限のエラーで失敗しました。また WAF と Route 53 のログも整理しています。有効にする場所の組み合わせとして正しいものはどれですか。

- A. ALB は属性とバケットポリシー、WAF は Web ACL
- B. ALB は CloudTrail の証跡、WAF はホストゾーン
- C. ALB は IAM ユーザーのアクセスキー、WAF は ALB の属性
- D. ALB は VPC の属性、WAF は CloudFront のビヘイビア

??? success "答えと解説"
    **正解: A**

    ログごとに有効にする場所が違います。

    - A: 正しい。
    - B: 誤り。それぞれ異なる。
    - C: 誤り。それぞれ異なる。
    - D: 誤り。それぞれ異なる。

    **スキル:** [ログの作成](../domain4.md#t4-2-log-creation) / **参照:** [ログ](../../../services/networking.md#cloudfront-logs), [ログ](../../../services/certificates.md#waf-logging)

### 問17 {#q17}

Network Firewall の判定の監査のため、ログを作成します。ルールの一致、通信の記録、TLS インスペクションの状況を分けて保管します。ログの種類として正しいものはどれですか。

- A. Access、Error、Slow の 3 種類
- B. Allow、Deny、Audit のログの 3 種類
- C. Alert、Flow、TLS の 3 種類
- D. CloudTrail、Config、GuardDuty の 3 種類

??? success "答えと解説"
    **正解: C**

    ログの設定で種類ごとに送信先を選べます。

    - A: 誤り。別のサービスの種類。
    - B: 誤り。名前が違う。
    - C: 正しい。
    - D: 誤り。別のサービス。

    **スキル:** [ログの作成](../domain4.md#t4-2-log-creation) / **参照:** [フローログの分析](../../../services/network-connectivity.md#flow-log-analysis)

### 問18 {#q18}

フローログを作成する範囲を決めます。サブネットの一部の ENI だけで足りますが、将来の ENI の記録も欲しいと考えています。正しい説明はどれですか。

- A. ENI に作ると、同じサブネットの将来の ENI も対象になる
- B. VPC に作ると、ピアリング先の VPC の ENI も対象になる
- C. サブネットに作ると、そのサブネットの ENI が対象になる
- D. サブネットのフローログは作成後に別のサブネットへ変更できる

??? success "答えと解説"
    **正解: C**

    VPC、サブネット、ENI の単位で作ります。

    - A: 誤り。その ENI だけが対象。
    - B: 誤り。対象は自分の VPC。
    - C: 正しい。
    - D: 誤り。作成後は変更できない。

    **スキル:** [ログの作成](../domain4.md#t4-2-log-creation) / **参照:** [フローログの分析](../../../services/network-connectivity.md#flow-log-analysis), [接続できないときの切り分け](../../../services/networking.md#vpc-troubleshooting)

### 問19 {#q19}

要件は 2 つです。(1) フローログを長期に低コストで保存して Athena で分析する。(2) 外部の SIEM へ送る。送信先の組み合わせとして最も適切なものはどれですか。

- A. 1 は Firehose（保存なし）、2 は CloudTrail Lake
- B. 1 は Route 53 のクエリログ、2 は S3
- C. 1 は S3（Parquet）、2 は Firehose
- D. 1 は CloudWatch Logs（無期限）、2 は Kinesis Data Streams へ直接

??? success "答えと解説"
    **正解: C**

    要件で送信先を選びます。

    - A: 誤り。保存の要件に合わない。
    - B: 誤り。別のログで、要件にも合わない。
    - C: 正しい。
    - D: 誤り。費用が大きく、フローログの送信先にデータストリームはない。

    **スキル:** [ログの配信](../domain4.md#t4-2-delivery) / **参照:** [サブスクリプションフィルター](../../../services/observability.md#subscription-filters), [Amazon Athena](../../../services/streaming.md#athena)

### 問20 {#q20}

セキュリティチームがログの配信先の表を作っています。保持は別に設計します。ログの種類と送信先の組み合わせとして正しいものを選んでください。（2つ選択）

- A. VPC フローログ: S3 は使えない
- B. CloudFront のリアルタイムログ: Kinesis Data Streams
- C. Resolver クエリログ: Kinesis Data Streams のみ
- D. CloudFront 標準ログ v2: CloudWatch Logs のみ
- E. Route 53 の公開クエリログ: CloudWatch Logs のみ

??? success "答えと解説"
    **正解: B, E**

    送信先の表を覚えます。

    - A: 誤り。S3 も使える。
    - B: 正しい。
    - C: 誤り。CloudWatch Logs、S3、Firehose。
    - D: 誤り。S3 と Firehose も。
    - E: 正しい。

    **スキル:** [ログの配信](../domain4.md#t4-2-delivery) / **参照:** [ログ](../../../services/networking.md#cloudfront-logs)

### 問21 {#q21}

各アカウントの CloudWatch Logs のログを、数分以内にログ用アカウントへ集めます。S3 へのエクスポートは使いません。最も適切なものはどれですか。

- A. ログのエクスポートを毎週手動で行う
- B. CloudWatch ダッシュボードの共有で、ログを転送する
- C. メトリクスフィルターの値を別のアカウントへ送る
- D. サブスクリプションフィルターでログ用アカウントへ配信する

??? success "答えと解説"
    **正解: D**

    集中管理の方法です。

    - A: 誤り。数分以内の要件に合わない。
    - B: 誤り。表示の共有で、転送にならない。
    - C: 誤り。ログの本文は送られない。
    - D: 正しい。

    **スキル:** [ログの配信](../domain4.md#t4-2-delivery) / **参照:** [サブスクリプションフィルター](../../../services/observability.md#subscription-filters)

### 問22 {#q22}

不審な通信の直前に何があったかを調べます。SG の変更が疑われます。ログの組み合わせとして最も適切なものはどれですか。

- A. フローログと、SG の変更を記録した CloudTrail
- B. WAF のログと ALB のアクセスログ
- C. Resolver クエリログと Route 53 のヘルスチェック
- D. CloudFront の標準ログと Trusted Advisor

??? success "答えと解説"
    **正解: A**

    通信と変更の相関です。

    - A: 正しい。
    - B: 誤り。Web の攻撃の分析の組み合わせ。
    - C: 誤り。変更の記録がない。
    - D: 誤り。変更の記録がない。

    **スキル:** [相関分析](../domain4.md#t4-2-correlation) / **参照:** [ログの調査](../../../services/threat-detection.md#log-investigation), [フローログの分析](../../../services/network-connectivity.md#flow-log-analysis)

### 問23 {#q23}

EC2 からどのドメインへ接続したかを調べます。フローログには IP しかありません。最も適切な相関はどれですか。

- A. Trusted Advisor と GuardDuty の抑制ルールを照合する
- B. Resolver クエリログとフローログの IP を照合する
- C. CloudTrail と Route Analyzer の結果を照合する
- D. VPC フローログだけで集約間隔を短くする

??? success "答えと解説"
    **正解: B**

    ドメインと IP を対応させます。

    - A: 誤り。ドメインの情報の相関にならない。
    - B: 正しい。
    - C: 誤り。ドメインの情報がない。
    - D: 誤り。ドメインは記録されない。

    **スキル:** [相関分析](../domain4.md#t4-2-correlation) / **参照:** [どのログを見るか](../../../services/threat-detection.md#log-sources), [VPC Resolver](../../../services/network-connectivity.md#vpc-resolver)

### 問24 {#q24}

複数のアカウントのログをまとめて調査します。また、GuardDuty の検出を起点に影響範囲を調べます。組み合わせとして最も適切なものはどれですか。

- A. Security Lake と Athena、Detective
- B. Firewall Manager のポリシーだけで調査する
- C. 各アカウントの CloudWatch コンソールを順に開く
- D. Config のアグリゲーターだけで通信も調査する

??? success "答えと解説"
    **正解: A**

    調査の起点と影響範囲です。

    - A: 正しい。
    - B: 誤り。調査の機能ではない。
    - C: 誤り。まとめて調査できない。
    - D: 誤り。通信の記録ではない。

    **スキル:** [相関分析](../domain4.md#t4-2-correlation) / **参照:** [Security Lake](../../../services/threat-detection.md#security-lake), [Detective](../../../services/threat-detection.md#detective)

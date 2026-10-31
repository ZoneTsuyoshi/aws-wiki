# ネットワークの保護、ログ、監視の問題集

対象の解説: [AWS WAF](../../../services/certificates.md#waf)、[Network Firewall](../../../services/network-connectivity.md#network-firewall)、[DNS Firewall](../../../services/network-connectivity.md#dns-firewall)、[VPC フローログ](../../../services/networking.md#flow-logs)、[接続の調査](../../../services/network-connectivity.md#network-analysis)

### 問1 {#q1}

ALB へのリクエストについて、SQL インジェクションと IP ごとのレート制限を設定します。どれを選びますか。

- A. AWS Network Firewall
- B. Shield Standard
- C. AWS WAF のウェブ ACL
- D. DNS Firewall

??? success "答えと解説"
    **正解: C**

    HTTP の内容の検査とレート制限は WAF です。

    - A: 誤り。レート制限や SQL インジェクションのルールは WAF が向く。
    - B: 誤り。ネットワーク層の DDoS の保護である。
    - C: 正しい。
    - D: 誤り。HTTP のリクエストの内容は見ない。

    **スキル:** [5.1.3](../domain5.md#skill-5-1-3) / **参照:** [AWS WAF](../../../services/certificates.md#waf)、[Shield](../../../services/threat-detection.md#shield)

### 問2 {#q2}

WAF のログの送信先に、作成した S3 バケットを選べません。バケット名は `waf-logs-prod` です。どう直しますか。

- A. 名前を `aws-waf-logs-` で始める
- B. ウェブ ACL のルールをすべて無効にしてから作り直す
- C. ログの送信先を SNS に変える
- D. バケットのバージョニングを有効にする

??? success "答えと解説"
    **正解: A**

    ログの送信先の名前は `aws-waf-logs-` で始めます。

    - A: 正しい。
    - B: 誤り。ログの設定と関係がない。
    - C: 誤り。SNS はログの送信先に使えない。
    - D: 誤り。名前の問題である。

    **スキル:** [5.1.3](../domain5.md#skill-5-1-3) / **参照:** [ログ](../../../services/certificates.md#waf-logging)

### 問3 {#q3}

VPC のインスタンスからマルウェアのドメインへの問い合わせを止めるルールを入れた後、許可したドメインにアクセスできなくなりました。CNAME の先のドメインに問題がありそうです。正しい説明はどれですか。

- A. DNS Firewall は既定でフェイルオープンなので、影響はない
- B. CNAME の連鎖の先のドメインも許可が必要である
- C. 通信は DNS Firewall を必ず通るので、IP の直接の通信も止まる
- D. 独自の DNS サーバーでもルールが効く

??? success "答えと解説"
    **正解: B**

    CNAME の連鎖の先のドメインも評価されます。

    - A: 誤り。既定はフェイルクローズである。
    - B: 正しい。
    - C: 誤り。IP の直接の通信はすり抜ける。
    - D: 誤り。独自の DNS サーバーはすり抜ける。

    **スキル:** [5.1.3](../domain5.md#skill-5-1-3) / **参照:** [DNS Firewall](../../../services/network-connectivity.md#dns-firewall)

### 問4 {#q4}

Network Firewall を配置しましたが、通信が検査されません。ファイアウォールのルールは正しいです。何を確認しますか。

- A. WAF のウェブ ACL の関連付け
- B. Shield Advanced の保護の対象
- C. DNS Firewall のルールグループの関連付けと優先順位の設定
- D. ルートテーブルでファイアウォールのエンドポイントへ通信を通しているか

??? success "答えと解説"
    **正解: D**

    経路が通らないと検査されません。

    - A: 誤り。別のサービスである。
    - B: 誤り。別のサービスである。
    - C: 誤り。別のサービスである。
    - D: 正しい。

    **スキル:** [5.1.3](../domain5.md#skill-5-1-3) / **参照:** [ルーティング](../../../services/network-connectivity.md#nfw-routing)、[Network Firewall](../../../services/network-connectivity.md#network-firewall)

### 問5 {#q5}

単一のアカウントの監査で、各サービスで何を見るかの組み合わせとして正しいものを選んでください。（2つ選択）

- A. Network Firewall: アラートログ、フローログ、TLS ログ
- B. Shield Standard: 設定したルールのブロックの件数
- C. WAF: VPC フローログ
- D. DNS Firewall: ALB のアクセスログ
- E. DNS Firewall: Resolver クエリログ、ルールグループの関連付け

??? success "答えと解説"
    **正解: A, E**

    サービスごとに監査の入口が違います。

    - A: 正しい。
    - B: 誤り。自動で有効で、ルールの設定はない。
    - C: 誤り。WAF のログ、サンプルリクエスト、ルールのメトリクスを見る。
    - D: 誤り。DNS の問い合わせは見えない。
    - E: 正しい。

    **スキル:** [5.1.3](../domain5.md#skill-5-1-3) / **参照:** [ログと TLS](../../../services/threat-detection.md#nfw-logging)、[DNS Firewall](../../../services/network-connectivity.md#dns-firewall)

### 問6 {#q6}

次の要件に合うものはどれですか。IP 宛の通信と DNS 以外のプロトコルも VPC の境界で止めたいです。

- A. DNS Firewall
- B. WAF
- C. Network Firewall
- D. Shield Advanced の保護

??? success "答えと解説"
    **正解: C**

    VPC の出入りの IP、ドメイン、IPS は Network Firewall です。

    - A: 誤り。ドメイン名の問い合わせだけが対象である。
    - B: 誤り。HTTP の層が対象である。
    - C: 正しい。
    - D: 誤り。DDoS の保護である。

    **スキル:** [5.1.3](../domain5.md#skill-5-1-3) / **参照:** [Shield](../../../services/threat-detection.md#shield)、[Network Firewall](../../../services/network-connectivity.md#network-firewall)

### 問7 {#q7}

VPC フローログの次のレコードを読みます。`2 111122223333 eni-EXAMPLE 10.0.1.5 203.0.113.10 49152 443 6 12 3400 1760000000 1760000060 REJECT OK`。正しい説明はどれですか。

- A. `10.0.1.5` から `203.0.113.10` の 443 番への TCP が拒否された
- B. `10.0.1.5` の 443 番ポートへの通信が許可された
- C. HTTP の応答コードが 443 だった
- D. `203.0.113.10` から `10.0.1.5` の 49152 番への UDP がセキュリティグループで拒否された

??? success "答えと解説"
    **正解: A**

    順序は version、account-id、interface-id、srcaddr、dstaddr、srcport、dstport、protocol、packets、bytes、start、end、action、log-status です。

    - A: 正しい。
    - B: 誤り。宛先のポートは 443 で、宛先は `203.0.113.10` である。結果も拒否である。
    - C: 誤り。フローログに HTTP の中身はない。
    - D: 誤り。プロトコルの 6 は TCP で、送信元も違う。

    **スキル:** [5.3.2](../domain5.md#skill-5-3-2) / **参照:** [VPC フローログ](../../../services/networking.md#flow-logs)

### 問8 {#q8}

VPC フローログの説明として正しいものを選んでください。（2つ選択）

- A. Amazon DNS サーバーへの問い合わせは記録されない
- B. 配信の遅れがなく、記録は常に 1 秒以内に届く
- C. インスタンスメタデータへの通信も記録される
- D. 作成後に形式を変更できないので、作り直す
- E. HTTP のパスや応答コードも記録される

??? success "答えと解説"
    **正解: A, D**

    記録の対象外を押さえます。

    - A: 正しい。
    - B: 誤り。CloudWatch Logs で約 5 分、S3 で約 10 分の遅れがある。
    - C: 誤り。記録の対象外である。
    - D: 正しい。
    - E: 誤り。HTTP の中身はない。

    **スキル:** [5.3.2](../domain5.md#skill-5-3-2) / **参照:** [VPC フローログ](../../../services/networking.md#flow-logs)、[フローログの分析](../../../services/network-connectivity.md#flow-log-analysis)

### 問9 {#q9}

ALB の 5xx が増えました。`HTTPCode_ELB_5XX_Count` は 0 で、`HTTPCode_Target_5XX_Count` が増えています。どう判断しますか。

- A. CloudFront のエラーのキャッシュが原因と判断する
- B. ALB 自身の問題なので、AWS のサポートへの連絡だけを行う
- C. セキュリティグループの拒否が原因と判断する
- D. ターゲットが返したエラーなので、アプリを調べる

??? success "答えと解説"
    **正解: D**

    `HTTPCode_ELB_5XX_Count` は ALB が返したエラー、`HTTPCode_Target_5XX_Count` はターゲットが返したエラーです。

    - A: 誤り。ターゲットが返したエラーである。
    - B: 誤り。ターゲットのカウントが増えている。
    - C: 誤り。拒否なら応答は返らない。
    - D: 正しい。

    **スキル:** [5.3.2](../domain5.md#skill-5-3-2) / **参照:** [ALB のエラーコード](../../../services/networking.md#alb-errors)

### 問10 {#q10}

ALB のリクエストごとの応答コードと処理時間を分析したいです。どの設定で、どう分析しますか。

- A. CloudTrail の管理イベントで、全リクエストの応答コードを検索する
- B. アクセスログを有効にして、S3 のログを Athena で検索する
- C. アクセスログは既定で有効なので、CloudWatch Logs のロググループを開く
- D. VPC フローログを有効にして、CloudWatch Logs で HTTP のパスを検索する

??? success "答えと解説"
    **正解: B**

    ALB のアクセスログは既定で無効で、送信先は S3 です。

    - A: 誤り。ALB の API の操作の記録である。
    - B: 正しい。
    - C: 誤り。既定で無効で、送信先は S3 である。
    - D: 誤り。HTTP の中身は記録されない。

    **スキル:** [5.3.2](../domain5.md#skill-5-3-2) / **参照:** [Elastic Load Balancing](../../../services/networking.md#elb)

### 問11 {#q11}

S3 に保存した CloudFront のログを Athena で検索します。スキャンの費用を減らす方法はどれですか。

- A. 日付でパーティションを切る
- B. S3 のバージョニングを有効にする
- C. 全列を `SELECT *` で常に検索する
- D. ログの形式を毎日変更する

??? success "答えと解説"
    **正解: A**

    パーティションを切ると、スキャンの量を減らせます。

    - A: 正しい。
    - B: 誤り。費用は増える。
    - C: 誤り。費用は増える。
    - D: 誤り。検索が難しくなるだけである。

    **スキル:** [5.3.2](../domain5.md#skill-5-3-2) / **参照:** [S3 上のログを問い合わせる](../../../services/streaming.md#athena-logs)、[ログ](../../../services/networking.md#cloudfront-logs)

### 問12 {#q12}

ECS と EKS のコンテナのログの収集の説明で正しいものはどれですか。

- A. EKS では `awslogs` のログドライバーだけが使える
- B. コンテナの標準出力は自動で S3 に保存される
- C. ECS は `awslogs` か FireLens、EKS は Fluent Bit を使う
- D. ECS ではログの収集に必ず EC2 に SSH し、ファイルをコピーする必要がある

??? success "答えと解説"
    **正解: C**

    コンテナのログは、環境ごとに方法が違います。

    - A: 誤り。Fluent Bit などを使う。
    - B: 誤り。ログの設定が必要である。
    - C: 正しい。
    - D: 誤り。`awslogs` や FireLens で収集する。

    **スキル:** [5.3.2](../domain5.md#skill-5-3-2) / **参照:** [コンテナ定義のパラメータ](../../../services/containers.md#container-definition)

### 問13 {#q13}

Direct Connect の先の工場との通信が遅くなることがあります。原因が AWS 側かを判断するため、継続的に遅延を測ります。工場にエージェントは入れられません。何を使いますか。

- A. Network Flow Monitor
- B. Reachability Analyzer
- C. Internet Monitor
- D. Network Synthetic Monitor

??? success "答えと解説"
    **正解: D**

    VPC のサブネットからオンプレミスの宛先へプローブを送ります。[公式](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/what-is-network-monitor.html)

    - A: 誤り。インスタンスにエージェントを入れて VPC の通信を見る機能である。
    - B: 誤り。設定の解析で、遅延は測れない。
    - C: 誤り。AWS のアプリと利用者の間のインターネットを見る機能である。
    - D: 正しい。

    **スキル:** [5.3.5](../domain5.md#skill-5-3-5) / **参照:** [接続の調査](../../../services/network-connectivity.md#network-analysis)、[ダッシュボードとインサイト](../../../services/observability.md#dashboards)

### 問14 {#q14}

VPC の中のマイクロサービスの間の通信と、S3 への通信で、TCP の性能の劣化がどこで起きているかを調べたいです。インスタンスに軽量なエージェントを入れてかまいません。何を使いますか。

- A. Network Synthetic Monitor
- B. Network Flow Monitor
- C. Traffic Mirroring
- D. Internet Monitor

??? success "答えと解説"
    **正解: B**

    エージェントが TCP 接続の統計を集めます。[公式](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch-NetworkFlowMonitor.html)

    - A: 誤り。オンプレミスの宛先へのプローブの機能である。
    - B: 正しい。
    - C: 誤り。パケットのコピーの機能で、性能の監視の機能ではない。
    - D: 誤り。インターネットの経路の監視である。

    **スキル:** [5.3.5](../domain5.md#skill-5-3-5) / **参照:** [接続の調査](../../../services/network-connectivity.md#network-analysis)、[ダッシュボードとインサイト](../../../services/observability.md#dashboards)

### 問15 {#q15}

特定の国の利用者だけアプリが遅いという報告が増えました。どの場所と ISP が影響を受けているかを、エージェントなしで調べたいです。何を使いますか。

- A. Internet Monitor
- B. Reachability Analyzer
- C. Network Flow Monitor
- D. Network Synthetic Monitor

??? success "答えと解説"
    **正解: A**

    影響を受ける場所と ISP（ASN）を特定できます。[公式](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch-InternetMonitor.html)

    - A: 正しい。
    - B: 誤り。設定の解析である。
    - C: 誤り。エージェントが必要で、VPC の内外の通信を見る。
    - D: 誤り。オンプレミスの宛先への監視である。

    **スキル:** [5.3.5](../domain5.md#skill-5-3-5) / **参照:** [接続の調査](../../../services/network-connectivity.md#network-analysis)、[ダッシュボードとインサイト](../../../services/observability.md#dashboards)

### 問16 {#q16}

Network Synthetic Monitor の説明として正しいものを選んでください。（2つ選択）

- A. オンプレミスの宛先にエージェントが必要である
- B. メトリクスは CloudWatch に届くので、ダッシュボードとアラームを作れる
- C. ネットワークヘルス指標で、劣化の原因が AWS のネットワーク側かを判断できる
- D. 劣化を検知すると自動でフェイルオーバーする
- E. モニターのサブネットは別のアカウントのものを指定できる

??? success "答えと解説"
    **正解: B, C**

    ネットワークヘルス指標（NHI）で切り分けます。

    - A: 誤り。エージェントは不要である。
    - B: 正しい。
    - C: 正しい。
    - D: 誤り。自動のフェイルオーバーはしない。
    - E: 誤り。同じアカウントのものを使う。

    **スキル:** [5.3.5](../domain5.md#skill-5-3-5) / **参照:** [接続の調査](../../../services/network-connectivity.md#network-analysis)、[ダッシュボードとインサイト](../../../services/observability.md#dashboards)

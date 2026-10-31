# CloudWatch とログの要件の問題集

対象の解説: [CloudWatch メトリクス](../../../services/observability.md#cloudwatch-metrics), [アラーム](../../../services/observability.md#alarms), [Logs Insights でログを検索する](../../../services/observability.md#logs-insights), [ログ](../../../services/networking.md#cloudfront-logs), [フローログの分析](../../../services/network-connectivity.md#flow-log-analysis)

### 問1 {#q1}

世界の 30 拠点の VPN と DX を 1 つのチームが監視します。拠点ごとの通信量を 1 画面で比較し、トンネルが落ちたら通知します。フローログも検索したいと考えています。追加のサーバーは運用したくありません。CloudWatch の機能の組み合わせとして最も適切なものはどれですか。

- A. CloudWatch エージェントを各拠点のルーターに導入し、`Logs Insights` だけで全部を監視する
- B. Contributor Insights だけで通信量を比較し、通知は CloudTrail の Lake に任せて集計する
- C. ダッシュボード、`TunnelState` のアラーム、Logs Insights を組み合わせる
- D. メトリクスストリームを S3 へ送り、EC2 で Grafana を運用して全部の通知も行う

??? success "答えと解説"
    **正解: C**

    標準のメトリクス、アラーム、ダッシュボード、Logs Insights で足ります。

    - A: 誤り。ネットワーク機器へのエージェントの導入を前提にしており、アラームもない。
    - B: 誤り。CloudTrail は API の記録で、トンネルの状態の通知に使わない。
    - C: 正しい。
    - D: 誤り。追加のサーバーを運用しない条件に反する。

    **スキル:** [CloudWatch](../domain1.md#t1-4-cloudwatch) / **参照:** [ダッシュボードとインサイト](../../../services/observability.md#dashboards), [アラーム](../../../services/observability.md#alarms)

### 問2 {#q2}

EC2 のプロキシで、同時接続数と `ethtool -S` の統計を時系列で見たいと考えています。ハイパーバイザーから見える標準のメトリクスにはこれらの値がありません。最も少ない開発で収集する方法はどれですか。

- A. Network Flow Monitor のスコアから、OS の接続数を逆算してメトリクスにする
- B. VPC フローログのカスタム形式に、接続数と統計の項目を追加して集計する
- C. CloudWatch エージェントで、OS の統計をカスタムメトリクスとして収集する
- D. 詳細モニタリングを有効にして、1 分間隔の標準メトリクスから取り出す

??? success "答えと解説"
    **正解: C**

    OS の値やログはエージェントで集めます。

    - A: 誤り。特定の統計の値を取り出す手段ではない。
    - B: 誤り。フローログにインスタンスの統計の項目はない。
    - C: 正しい。
    - D: 誤り。間隔が短くなるだけで、OS の値は増えない。

    **スキル:** [CloudWatch](../domain1.md#t1-4-cloudwatch) / **参照:** [CloudWatch エージェント](../../../services/operations.md#cloudwatch-agent)

### 問3 {#q3}

フローログを CloudWatch Logs へ送っています。障害の調査中に、過去 1 時間で拒否の多い送信元と宛先ポートの組み合わせをすぐに知りたいと考えています。ログのエクスポートはしません。最も適切な方法はどれですか。

- A. ログを S3 へエクスポートしてから Athena のテーブルを定義して集計する
- B. メトリクスフィルターを新しく作って、過去 1 時間の値が埋まるのを待つ
- C. Logs Insights で `REJECT` を絞り、`stats` で集計する
- D. ロググループごとに Live Tail で表示し続け、手作業で件数を数えて記録する

??? success "答えと解説"
    **正解: C**

    調査の集計は Logs Insights です。

    - A: 誤り。エクスポートしない条件に反する。
    - B: 誤り。メトリクスフィルターは作成後のログにしか効かない。
    - C: 正しい。
    - D: 誤り。過去の集計に向かない。

    **スキル:** [CloudWatch](../domain1.md#t1-4-cloudwatch) / **参照:** [Logs Insights でログを検索する](../../../services/observability.md#logs-insights), [フローログの分析](../../../services/network-connectivity.md#flow-log-analysis)

### 問4 {#q4}

NAT ゲートウェイの背後のアプリで、外部 API への接続がときどき失敗します。CPU と帯域には余裕があり、同じ宛先へ多数の接続を開いています。最初に確認するメトリクスとして最も適切なものはどれですか。

- A. `TunnelDataOut` で NAT の送信量が VPN の上限を超えていないかを確認する
- B. `ErrorPortAllocation` で送信元ポートの割り当ての失敗を確認する
- C. `ConnectionErrorCount` で物理ポートのエラーを確認する
- D. `PacketDropCountBlackhole` で Transit Gateway の破棄を確認する

??? success "答えと解説"
    **正解: B**

    送信元ポートの割り当ての失敗を示します。

    - A: 誤り。VPN のメトリクス。
    - B: 正しい。
    - C: 誤り。Direct Connect のメトリクス。
    - D: 誤り。Transit Gateway のメトリクス。

    **スキル:** [メトリクスとベースライン](../domain1.md#t1-4-metrics) / **参照:** [NAT ゲートウェイ](../../../services/network-connectivity.md#nat-gateway), [フローログの分析](../../../services/network-connectivity.md#flow-log-analysis)

### 問5 {#q5}

EC2 間の通信でパケットの損失が増えています。CloudWatch の `NetworkIn` はインスタンスの仕様の範囲に見えます。ハイパーバイザーでの帯域の制限の超過かを確かめる方法はどれですか。

- A. Route 53 の `HealthCheckPercentageHealthy` の低下を確認する
- B. `CPUCreditBalance` を確認して、帯域のクレジットとして読み替える
- C. `ethtool -S` の `bw_in_allowance_exceeded` の増加を確認する
- D. CloudTrail で `ModifyInstanceAttribute` の呼び出し件数を確認する

??? success "答えと解説"
    **正解: C**

    CloudWatch の 5 分の平均では、短い超過が見えないことがあります。

    - A: 誤り。インスタンスの帯域の統計ではない。
    - B: 誤り。CPU のクレジットで、ネットワークの超過の統計ではない。
    - C: 正しい。
    - D: 誤り。API の記録で、パケットの破棄の統計ではない。

    **スキル:** [メトリクスとベースライン](../domain1.md#t1-4-metrics) / **参照:** [MTU とジャンボフレーム](../../../services/network-connectivity.md#mtu)

### 問6 {#q6}

オンプレミスと VPC の間のハイブリッド接続について、正常時の遅延と損失を測ってベースラインを持ちます。VPC にもオンプレミスにも新しいエージェントを入れたくありません。最も適切なツールはどれですか。

- A. CloudWatch Internet Monitor。インターネットの利用者の影響を測る
- B. Traffic Mirroring を全 ENI で常時有効にして遅延を計算する
- C. Network Synthetic Monitor。AWS のプローブで測定する
- D. CloudWatch Network Flow Monitor。各 EC2 にエージェントを導入する

??? success "答えと解説"
    **正解: C**

    エージェント不要で、遅延と損失を測れます。

    - A: 誤り。利用者とアプリの間のインターネットの測定。
    - B: 誤り。費用が大きく、遅延の測定の機能でもない。
    - C: 正しい。
    - D: 誤り。エージェントの導入が必要。

    **スキル:** [メトリクスとベースライン](../domain1.md#t1-4-metrics) / **参照:** [Direct Connect](../../../services/network-connectivity.md#direct-connect)

### 問7 {#q7}

次の 2 つの要件があります。(1) 誰がどこへ通信したかを 1 年保持し、費用を抑える。(2) 拒否された通信をすぐ知る。フローログの出力の設計として最も適切なものはどれですか。

- A. Traffic Mirroring を 1 年間有効にし、パケットを S3 へ送って拒否を判定する
- B. CloudWatch Logs だけへ送り、保持を無期限にしてメトリクスフィルターで通知する
- C. S3 だけへ送り、1 日 1 回 Athena の結果を確認して拒否を通知する
- D. S3 へ長期保存し、CloudWatch Logs へも送ってフィルターとアラームを付ける

??? success "答えと解説"
    **正解: D**

    要件ごとに送信先を決めます。

    - A: 誤り。パケットの複製は費用が大きく、拒否の判定にも使えない。
    - B: 誤り。動くが、1 年分の保持は S3 より費用が大きい。
    - C: 誤り。すぐ知る要件に合わない。
    - D: 正しい。

    **スキル:** [要件の特定](../domain1.md#t1-4-requirements) / **参照:** [フローログの分析](../../../services/network-connectivity.md#flow-log-analysis), [メトリクスフィルター](../../../services/observability.md#metric-filters)

### 問8 {#q8}

監査チームから 3 つの要件が出ました。(A) IDS でパケットの中身を検査する。(B) VPC から問い合わせたドメインを記録する。(C) ルートテーブルの変更者を追跡する。それぞれに合うものの組み合わせはどれですか。

- A. A は Traffic Mirroring、B はフローログ、C は CloudWatch Logs Insights
- B. A は Traffic Mirroring、B は Resolver クエリログ、C は CloudTrail
- C. A はフローログ、B は公開 DNS クエリログ、C は Config のルール
- D. A は Network Firewall のフローログ、B は Resolver クエリログ、C は Route Analyzer

??? success "答えと解説"
    **正解: B**

    要件から逆算して選びます。

    - A: 誤り。フローログにドメインはない。Logs Insights は変更者の記録ではない。
    - B: 正しい。
    - C: 誤り。フローログに中身はなく、公開クエリログは VPC の問い合わせを記録しない。
    - D: 誤り。フローログに中身はなく、Route Analyzer は変更者を示さない。

    **スキル:** [要件の特定](../domain1.md#t1-4-requirements) / **参照:** [Config と CloudTrail の違い](../../../services/governance.md#config-vs-cloudtrail), [Traffic Mirroring](../../../services/network-connectivity.md#traffic-mirroring)

### 問9 {#q9}

ある会社は、VPC の外向きのドメインごとの接続の傾向を把握したいと考えています。一部の通信は Network Firewall を通りますが、DNS は既定の VPC Resolver です。通信の中身の検査の要件はありません。追加の費用を抑える選択はどれですか。

- A. CloudTrail の管理イベントから、VPC の外向きのドメインを集計する
- B. Resolver クエリログを有効にして、問い合わせ先のドメインごとに集計する
- C. Traffic Mirroring で TLS の SNI を全 ENI から収集して集計する
- D. ALB のアクセスログから、VPC の外向きのドメインを集計する

??? success "答えと解説"
    **正解: B**

    問い合わせたドメインの記録は Resolver クエリログです。

    - A: 誤り。通信の記録ではない。
    - B: 正しい。
    - C: 誤り。全 ENI のミラーは費用が大きい。
    - D: 誤り。外向きの通信は ALB のログに残らない。

    **スキル:** [要件の特定](../domain1.md#t1-4-requirements) / **参照:** [Network Firewall](../../../services/network-connectivity.md#network-firewall), [VPC Resolver](../../../services/network-connectivity.md#vpc-resolver)

### 問10 {#q10}

CloudFront のログを数秒以内に処理して、地域ごとのエラーの急増を検知したいと考えています。全件は不要で、サンプリングで構いません。最も適切なログの設計はどれですか。

- A. サンプリング率を指定したリアルタイムログを Kinesis Data Streams へ送る
- B. ALB のアクセスログを S3 へ送り、エッジのエラーを推定して処理する
- C. 標準ログ v2 を S3 へ送り、日次で Athena の集計を実行する
- D. 標準ログ v2 を CloudWatch Logs へ送り、会計用の精度を確保して処理する

??? success "答えと解説"
    **正解: A**

    リアルタイムログはサンプリング率を指定できます。

    - A: 正しい。
    - B: 誤り。エッジで完結するリクエストが記録されない。
    - C: 誤り。数秒以内の要件に合わない。
    - D: 誤り。ベストエフォートで、数秒以内の保証もない。

    **スキル:** [アクセスログ](../domain1.md#t1-4-access-logs) / **参照:** [ログ](../../../services/networking.md#cloudfront-logs)

### 問11 {#q11}

経理チームが CloudFront の標準ログから、顧客への請求額を確定しようとしています。ログの性質について指摘すべきことはどれですか。

- A. 標準ログは TLS の情報を持たないので、HTTPS のリクエストが記録されない
- B. 標準ログは 1 時間ごとに S3 にのみ出力され、他の送信先を指定できない
- C. 標準ログを有効にすると、ディストリビューションの料金が 2 倍になる
- D. ベストエフォートの記録で欠落もありうるので、会計用途には向かない

??? success "答えと解説"
    **正解: D**

    請求は別の記録で確定します。

    - A: 誤り。HTTPS のリクエストも記録される。
    - B: 誤り。v2 では CloudWatch Logs や Firehose にも送れる。
    - C: 誤り。そのような料金の仕組みではない。
    - D: 正しい。

    **スキル:** [アクセスログ](../domain1.md#t1-4-access-logs) / **参照:** [ログ](../../../services/networking.md#cloudfront-logs)

### 問12 {#q12}

監査のため、HTTP の Web の ALB と TLS の NLB の両方でアクセスログを有効にします。担当者の理解のうち、正しいものを選んでください。（2つ選択）

- A. NLB のアクセスログには TLS 接続の情報が残る
- B. ALB のアクセスログはリクエストごとの詳細を S3 へ記録する
- C. ALB のログのバケットは、ELB の権限を設定しなくても書き込める
- D. NLB のアクセスログには HTTP のパスとステータスが残る
- E. ALB のアクセスログは既定で有効になっている

??? success "答えと解説"
    **正解: A, B**

    ログごとの内容を押さえます。

    - A: 正しい。
    - B: 正しい。
    - C: 誤り。バケットポリシーで書き込みを許可する。
    - D: 誤り。NLB は L4 で HTTP を解釈しない。
    - E: 誤り。属性で有効にする。

    **スキル:** [アクセスログ](../domain1.md#t1-4-access-logs) / **参照:** [NLB の設定](../../../services/networking.md#nlb-settings), [リスナーとルール](../../../services/networking.md#alb-listeners)

### 問13 {#q13}

VPN のトンネルが不安定で、IKE の交渉と DPD の動きを詳しく調べたいと考えています。CGW の担当はオンプレミスのログを別に持っています。AWS 側で有効にするものはどれですか。

- A. VPC フローログを VGW に付けて DPD の失敗の理由を確認する
- B. VPN のトンネルログを CloudWatch Logs へ送って確認する
- C. CloudTrail のデータイベントで IKE のパケットを記録する
- D. Transit Gateway フローログで IKE の交渉の内容を確認する

??? success "答えと解説"
    **正解: B**

    トンネルログで IKE と DPD を調べます。

    - A: 誤り。VGW には付けられず、理由も記録しない。
    - B: 正しい。
    - C: 誤り。IKE の交渉の記録ではない。
    - D: 誤り。通信のメタデータで、交渉の内容はない。

    **スキル:** [監視とログ](../domain2.md#t2-1-monitoring) / **参照:** [Site-to-Site VPN](../../../services/network-connectivity.md#site-to-site-vpn), [CloudWatch Logs](../../../services/observability.md#cloudwatch-logs)

### 問14 {#q14}

在宅の利用者と本社の DX の両方を監視します。VPN の接続の履歴と物理の接続の状態を確認します。監視の設定の組み合わせとして正しいものを選んでください。（2つ選択）

- A. Client VPN: 接続ログを CloudWatch Logs へ送る
- B. Direct Connect: フローログを VIF に直接付けて S3 へ送る
- C. Site-to-Site VPN: トンネルログを Kinesis Data Streams へ直接送る
- D. Direct Connect: `ConnectionState` にアラームを設定する
- E. Transit Gateway: 通信の記録は VPC フローログの設定に自動で含まれる

??? success "答えと解説"
    **正解: A, D**

    対象ごとの設定を覚えます。

    - A: 正しい。
    - B: 誤り。VIF のフローログの設定はない。
    - C: 誤り。トンネルログの送信先は CloudWatch Logs。
    - D: 正しい。
    - E: 誤り。Transit Gateway フローログを別に設定する。

    **スキル:** [監視とログ](../domain2.md#t2-1-monitoring) / **参照:** [Client VPN](../../../services/network-connectivity.md#client-vpn), [Direct Connect](../../../services/network-connectivity.md#direct-connect)

### 問15 {#q15}

オンプレミスと VPC の間の通信で、どのアタッチメントを通ったかを記録します。VPC の中のログを増やしたくありません。最も適切な設定はどれですか。

- A. Route Analyzer を毎分実行して、結果を保存する
- B. 各 VPC の全 ENI でフローログを有効にして、送信元から推定する
- C. 公開 VIF のメトリクスをアタッチメントごとに集計する
- D. Transit Gateway フローログを有効にして記録する

??? success "答えと解説"
    **正解: D**

    アタッチメント間の通信を記録します。

    - A: 誤り。実際の通信を記録しない。
    - B: 誤り。VPC の中のログが増え、アタッチメントの判定も推定になる。
    - C: 誤り。公開 VIF の話で、アタッチメントの記録ではない。
    - D: 正しい。

    **スキル:** [監視とログ](../domain2.md#t2-1-monitoring) / **参照:** [Transit Gateway](../../../services/network-connectivity.md#transit-gateway), [フローログの分析](../../../services/network-connectivity.md#flow-log-analysis)

### 問16 {#q16}

300 のアカウントのフローログをログ用アカウントへ集め、長期保存します。各アカウントの管理者には変更させたくありません。設計として最も適切なものはどれですか。

- A. 各アカウントの CloudWatch Logs に無期限で保持し、ダッシュボードで表示する
- B. 各アカウントの S3 へ配信し、担当者が月末にログ用アカウントへコピーする
- C. ログ用アカウントの VPC へピアリングして、Traffic Mirroring で複製する
- D. ログ用アカウントの S3 へ配信し、バケットポリシーで書き込みだけを許可する

??? success "答えと解説"
    **正解: D**

    全アカウントのフローログをログ用アカウントの S3 へ配信します。

    - A: 誤り。集約にならず費用も大きい。
    - B: 誤り。手動で、変更を防げない。
    - C: 誤り。フローログの集約の手段ではない。
    - D: 正しい。

    **スキル:** [監視とログ](../domain2.md#t2-2-monitoring) / **参照:** [フローログの分析](../../../services/network-connectivity.md#flow-log-analysis), [CloudWatch Logs](../../../services/observability.md#cloudwatch-logs)

### 問17 {#q17}

Network Firewall でドメインの拒否を設定しました。通信は止まっていますが、どのルールで止まったのかがどこにも記録されていません。最も適切な対応はどれですか。

- A. ファイアウォールのログ設定で Alert ログを有効にする
- B. ステートレスのルールを `Pass` にして、通信を通して確認する
- C. CloudTrail のデータイベントでルールの一致を記録する
- D. VPC フローログのカスタム形式に `sid` のフィールドを追加する

??? success "答えと解説"
    **正解: A**

    設定しないとアラートは見えません。

    - A: 正しい。
    - B: 誤り。通信を止める要件に反する。
    - C: 誤り。ルールの一致は CloudTrail に出ない。
    - D: 誤り。フローログにそのフィールドはない。

    **スキル:** [監視とログ](../domain2.md#t2-2-monitoring) / **参照:** [ルーティング](../../../services/network-connectivity.md#nfw-routing)

### 問18 {#q18}

マルチリージョンの Transit Gateway で、トポロジーとルートの変更をネットワークチームが追跡します。個別の通信の中身は不要です。最も適切なものはどれですか。

- A. Traffic Mirroring で BGP の更新のパケットをコピーする
- B. CloudFront の標準ログで、リージョンごとの変化を確認する
- C. Global Networks for Transit Gateways
- D. VPC フローログの `traffic-path` を集計して、経路の変更を推定する

??? success "答えと解説"
    **正解: C**

    トポロジーとルートの変更を追えます。

    - A: 誤り。Transit Gateway の変更の追跡の仕組みではない。
    - B: 誤り。ネットワークのトポロジーの情報を持たない。
    - C: 正しい。
    - D: 誤り。実際の変更の通知にならない。

    **スキル:** [監視とログ](../domain2.md#t2-2-monitoring) / **参照:** [Route Analyzer](../../../services/network-connectivity.md#route-analyzer)

### 問19 {#q19}

同じ VPC の 2 台の間で iperf を実行すると、1 フローでは 5 Gbps で止まり、10 フローでは 25 Gbps 出ます。インスタンスの帯域は 25 Gbps です。遅延や損失はありません。正しい解釈はどれですか。

- A. ジッターが大きいので、複数のフローにすると遅延の差が平均される
- B. SG の接続追跡の上限で、1 フローにだけ制限がかかっている
- C. MTU の不一致で、大きなパケットが断片化している。MTU を 1500 に下げる
- D. シングルフローの上限で、インスタンスの帯域の上限ではない

??? success "答えと解説"
    **正解: D**

    異なるプレイスメントのインスタンスでは 1 フローが 5 Gbps までです。

    - A: 誤り。問題文に遅延の問題はない。
    - B: 誤り。接続追跡の上限はフロー数の制限で、1 フローの帯域の制限ではない。
    - C: 誤り。複数フローでは出ているので MTU の問題ではない。
    - D: 正しい。

    **スキル:** [指標と制約](../domain3.md#t3-2-metrics) / **参照:** [MTU とジャンボフレーム](../../../services/network-connectivity.md#mtu)

### 問20 {#q20}

ある経路で、小さな ping は通りますが、ファイル転送だけタイムアウトします。ルート、SG、NACL の TCP の許可は問題ありません。到達性の制約として次に疑うものはどれですか。

- A. NAT ゲートウェイのポートの枯渇で、大きな通信だけ止まっている
- B. シングルフローの帯域の上限で、接続が確立できなくなっている
- C. 経路の MTU と、PMTUD に必要な ICMP が遮断されていないか
- D. DNS の TTL が長いので、大きなファイルの名前だけ解決できない

??? success "答えと解説"
    **正解: C**

    大きなパケットだけの失敗は MTU を確認します。

    - A: 誤り。接続の開始に影響し、サイズによらない。
    - B: 誤り。帯域の上限はタイムアウトの原因になりにくく、小さな通信が通る症状に合わない。
    - C: 正しい。
    - D: 誤り。サイズと DNS は関係しない。

    **スキル:** [指標と制約](../domain3.md#t3-2-metrics) / **参照:** [PMTUD とトラブルシューティング](../../../services/network-connectivity.md#pmtud)

### 問21 {#q21}

VPN の経路で帯域が 1 Gbps を少し超えると損失が増えます。トンネルの状態は UP で、BGP も安定しています。指標の解釈として最も適切なものはどれですか。

- A. BGP のタイマーが長いので、パケットが遅れて損失になっている
- B. トンネルの MTU が 9001 になっており、大きなパケットが破棄されている
- C. トンネルの帯域の上限に近く、ECMP などで増やす必要がある
- D. AWS の保守の通知なので、次の保守で自然に解消される

??? success "答えと解説"
    **正解: C**

    標準トンネルは 1.25 Gbps です。

    - A: 誤り。BGP は安定している。
    - B: 誤り。VPN の MTU は 9001 にはならない。
    - C: 正しい。
    - D: 誤り。帯域の問題は保守では解消しない。

    **スキル:** [指標と制約](../domain3.md#t3-2-metrics) / **参照:** [トンネル](../../../services/network-connectivity.md#vpn-tunnels), [ルーティング](../../../services/network-connectivity.md#vpn-routing)

### 問22 {#q22}

Transit Gateway を通る通信が一部失敗します。アタッチメントの宛先によって動きが違います。パケットの破棄の理由を区別するため、確認するメトリクスの組み合わせはどれですか。

- A. `TunnelState` と `TunnelDataIn`
- B. `PacketDropCountNoRoute` と `PacketDropCountBlackhole`
- C. `HTTPCode_ELB_5XX_Count` と `ActiveFlowCount`
- D. `ConnectionBpsEgress` と `ConnectionErrorCount`

??? success "答えと解説"
    **正解: B**

    経路なしとブラックホールを区別します。

    - A: 誤り。Site-to-Site VPN のメトリクス。
    - B: 正しい。
    - C: 誤り。ロードバランサーのメトリクス。
    - D: 誤り。Direct Connect のメトリクス。

    **スキル:** [ログとメトリクス](../domain3.md#t3-2-logs) / **参照:** [ルートテーブル](../../../services/network-connectivity.md#tgw-route-tables)

### 問23 {#q23}

DX の接続でパケットの損失があります。トンネルや BGP に異常はなく、物理の問題を疑っています。最初に確認するメトリクスはどれですか。

- A. `PacketDropCountBlackhole`。DX の物理のエラーを示す値である
- B. `TunnelState`。DX の物理の状態を示す値である
- C. `ErrorPortAllocation`。DX のポートの割り当てエラーを示す値である
- D. `ConnectionErrorCount`。DX の物理ポートのエラーを示す値である

??? success "答えと解説"
    **正解: D**

    DX のエラーのメトリクスです。

    - A: 誤り。Transit Gateway のメトリクス。
    - B: 誤り。VPN のメトリクス。
    - C: 誤り。NAT のメトリクス。
    - D: 正しい。

    **スキル:** [ログとメトリクス](../domain3.md#t3-2-logs) / **参照:** [Direct Connect](../../../services/network-connectivity.md#direct-connect)

### 問24 {#q24}

ALB の 5xx が増えています。ALB 自身の 5xx か、ターゲットの 5xx かを区別したうえで、どのリクエストかを調べます。組み合わせとして最も適切なものはどれですか。

- A. `HTTPCode_ELB_5XX_Count` と `HTTPCode_Target_5XX_Count`、アクセスログ
- B. CloudTrail の `RegisterTargets` を確認し、エラーの URL を特定する
- C. `UnHealthyHostCount` だけを確認し、VPC フローログの `action` で判定する
- D. Route 53 のクエリログを確認し、5xx を応答コードから判定する

??? success "答えと解説"
    **正解: A**

    メトリクスで切り分け、ログで詳しく見ます。

    - A: 正しい。
    - B: 誤り。API の記録で、リクエストの情報はない。
    - C: 誤り。フローログに HTTP の情報はない。
    - D: 誤り。DNS の応答コードで、HTTP ではない。

    **スキル:** [ログとメトリクス](../domain3.md#t3-2-logs) / **参照:** [ALB のエラーコード](../../../services/networking.md#alb-errors), [フローログの分析](../../../services/network-connectivity.md#flow-log-analysis)

# ロードバランサーの問題集

対象の解説: [Elastic Load Balancing](../../../services/networking.md#elb), [ALB と NLB の違い](../../../services/networking.md#alb-vs-nlb), [GWLB](../../../services/networking.md#gwlb), [NLB の設定](../../../services/networking.md#nlb-settings)

### 問1 {#q1}

次の 3 つの要件に対するロードバランサーの組み合わせとして正しいものはどれですか。要件 1: URL のパスで振り分け、Cognito で認証する。要件 2: UDP の独自プロトコルで固定 IP を使う。要件 3: 第三者の仮想ファイアウォールを全ポートで透過的に挟む。

- A. 1 は ALB、2 は GWLB、3 は NLB。UDP は GENEVE で運ぶ
- B. 1 は GWLB、2 は NLB、3 は ALB。ALB でパケットを透過する
- C. 1 は ALB、2 は NLB、3 は GWLB。UDP の固定 IP は NLB で受ける
- D. 1 は NLB、2 は ALB、3 は GWLB。TLS の終端は NLB に任せる

??? success "答えと解説"
    **正解: C**

    層と機能で選びます。

    - A: 誤り。GWLB は固定 IP の UDP サービスの公開に使わない。
    - B: 誤り。ALB は全ポートの透過に使えない。
    - C: 正しい。
    - D: 誤り。要件 1 の L7 の機能は ALB、要件 2 の UDP は NLB。

    **スキル:** [L3、L4、L7 と選択](../domain1.md#t1-3-choose) / **参照:** [ALB と NLB の違い](../../../services/networking.md#alb-vs-nlb), [GWLB](../../../services/networking.md#gwlb)

### 問2 {#q2}

既存の Web アプリは ALB のパスベースのルーティングに依存しています。新しい取引先は IP の許可リストの登録を求めており、固定 IP が必要です。L7 の機能を残したまま要件を満たす方法を選んでください。（2つ選択）

- A. CloudFront のエッジの IP の範囲を、取引先に登録してもらう
- B. NLB のターゲットに ALB を登録して、NLB の IP を固定する
- C. Global Accelerator の固定 IP の先に ALB を置く
- D. ALB を GWLB の背後に置いて、GENEVE の外部 IP を固定する
- E. ALB に Elastic IP を割り当てて、DNS を固定する

??? success "答えと解説"
    **正解: B, C**

    固定 IP と L7 の両方を満たす 2 つの構成です。

    - A: 誤り。範囲が広く頻繁に変わるので、固定 IP にならない。
    - B: 正しい。
    - C: 正しい。
    - D: 誤り。GWLB に固定の公開 IP はない。
    - E: 誤り。ALB に Elastic IP は付けられない。

    **スキル:** [L3、L4、L7 と選択](../domain1.md#t1-3-choose) / **参照:** [ALB と NLB の違い](../../../services/networking.md#alb-vs-nlb), [Global Accelerator](../../../services/network-connectivity.md#global-accelerator)

### 問3 {#q3}

gRPC のマイクロサービスを、ヘッダーで振り分けます。また、ログのためにクライアント IP を `X-Forwarded-For` で受け取ります。最も適切なロードバランサーはどれですか。

- A. NLB の TLS リスナー。L7 のルールを TLS の終端で評価する
- B. ALB。gRPC のターゲットグループとヘッダーのルールで振り分ける
- C. NLB。TCP リスナーのプロキシプロトコルでヘッダーの振り分けを行う
- D. GWLB。GENEVE に gRPC のヘッダーをカプセル化する

??? success "答えと解説"
    **正解: B**

    gRPC とヘッダーの振り分けは ALB です。

    - A: 誤り。NLB に L7 のルールはない。
    - B: 正しい。
    - C: 誤り。L4 でヘッダーの判定はできない。
    - D: 誤り。L3 で透過するので、ヘッダーで振り分けない。

    **スキル:** [L3、L4、L7 と選択](../domain1.md#t1-3-choose) / **参照:** [ALB と NLB の違い](../../../services/networking.md#alb-vs-nlb)

### 問4 {#q4}

データセンターの古いサーバーから VPC へアプリを段階的に移します。移行の間、同じ ALB から新旧の両方へ振り分けます。オンプレミスとは DX で接続済みです。ターゲットグループの設定はどれですか。

- A. ターゲットタイプを `lambda` にして、Lambda からオンプレミスへ中継する
- B. ターゲットタイプを `ip` にして、オンプレミスの IP と EC2 の IP を登録する
- C. ターゲットタイプを `instance` にして、オンプレミスのサーバーの ID を登録する
- D. ALB を内部へ変更し、オンプレミスのルーターでターゲットを別途登録する

??? success "答えと解説"
    **正解: B**

    `ip` ならピアリング先やオンプレミスの IP も登録できます。

    - A: 誤り。問題文の振り分けとして不要な変更。
    - B: 正しい。
    - C: 誤り。オンプレミスのサーバーにインスタンス ID はない。
    - D: 誤り。スキームは作成後に変更できず、登録の場所も違う。

    **スキル:** [内部と外部](../domain1.md#t1-3-patterns) / **参照:** [ターゲットタイプ](../../../services/networking.md#target-types)

### 問5 {#q5}

3 層の Web アプリで、Web 層から App 層へのロードバランサーを設計します。App 層はインターネットから到達できず、オンプレミスのクライアントも DX で利用します。正しい構成はどれですか。

- A. 内部スキームをパブリックサブネットに置き、IGW 経由でオンプレミスから接続する
- B. インターネット向けのスキームをパブリックサブネットに置き、SG で Web 層の範囲だけ許可する
- C. インターネット向けのスキームで作成し、後から内部スキームに変更する
- D. 内部スキームのロードバランサーをプライベートサブネットに置き、DX から接続する

??? success "答えと解説"
    **正解: D**

    内部スキームはプライベート IP で解決されます。

    - A: 誤り。IGW 経由ではオンプレミスから接続できない。
    - B: 誤り。インターネットに公開する必要はなく、オンプレミスのプライベートの要件にも合わない。
    - C: 誤り。スキームは作成後に変更できない。
    - D: 正しい。

    **スキル:** [内部と外部](../domain1.md#t1-3-patterns) / **参照:** [Elastic Load Balancing](../../../services/networking.md#elb)

### 問6 {#q6}

インターネット向け ALB を AZ A と AZ B のパブリックサブネットに置きました。ターゲットは AZ C のプライベートサブネットにも登録しましたが、AZ C のターゲットが `unused` で通信が来ません。対処はどれですか。

- A. ALB をインターネット向けから内部へ変更する
- B. ターゲットを AZ C の NAT ゲートウェイの IP に登録し直す
- C. AZ C のサブネットを ALB に追加して、その AZ を有効にする
- D. AZ C のターゲットの SG に、インターネット全体からの HTTP を許可する

??? success "答えと解説"
    **正解: C**

    ターゲットの AZ にロードバランサーのサブネットがないと、そのターゲットへ送れません。

    - A: 誤り。スキームは作成後に変更できない。
    - B: 誤り。NAT はターゲットの入口にならない。
    - C: 正しい。
    - D: 誤り。AZ が有効でない問題で、SG の問題ではない。

    **スキル:** [内部と外部](../domain1.md#t1-3-patterns) / **参照:** [Elastic Load Balancing](../../../services/networking.md#elb), [ターゲットタイプ](../../../services/networking.md#target-types)

### 問7 {#q7}

ALB を `/28` のサブネットに置いており、大きなセールの最中に一部の AZ で 5xx が出ました。ターゲットには余裕があります。VPC の CIDR に余裕はあります。ALB のスケーリングの観点で適切な対応を選んでください。（2つ選択）

- A. 急な増加を見込むときは LCU の予約で最小の容量を確保する
- B. ALB に Elastic IP を AZ ごとに固定して IP の消費を抑える
- C. サブネットに十分な空き IP を確保する。`/27` 以上で空き 8 個以上
- D. ALB の AZ を 1 つに減らして、IP の消費を抑える
- E. ALB のインスタンスタイプを手動で大きなものに変更する

??? success "答えと解説"
    **正解: A, C**

    容量の確保はサブネットの空きと予約で行います。

    - A: 正しい。
    - B: 誤り。ALB に Elastic IP は付けられない。
    - C: 正しい。
    - D: 誤り。可用性が下がり、容量も減る。
    - E: 誤り。ALB にインスタンスタイプの設定はない。

    **スキル:** [スケーリング](../domain1.md#t1-3-scaling) / **参照:** [Elastic Load Balancing](../../../services/networking.md#elb)

### 問8 {#q8}

Auto Scaling グループのインスタンスがアプリの異常で HTTP 500 を返し続けています。EC2 のステータスチェックは正常なので、置き換わりません。ALB のターゲットグループは関連付け済みです。必要な設定はどれですか。

- A. 起動テンプレートでインスタンスの自動復旧を有効にする
- B. Auto Scaling グループで ELB のヘルスチェックを有効にする
- C. ターゲットグループの登録解除の待ちを 0 秒にする
- D. ALB の属性でクロスゾーンを無効にする

??? success "答えと解説"
    **正解: B**

    ELB のヘルスチェックを使うと、アプリの異常でも置き換わります。

    - A: 誤り。ハードウェアの障害などの復旧で、アプリの異常の判定ではない。
    - B: 正しい。
    - C: 誤り。解除の待ちは異常の判定ではない。
    - D: 誤り。異常なインスタンスの置き換えと関係がない。

    **スキル:** [スケーリング](../domain1.md#t1-3-scaling) / **参照:** [EC2 Auto Scaling](../../../services/ec2-beanstalk.md#auto-scaling), [ヘルスチェック](../../../services/ec2-beanstalk.md#asg-health-checks)

### 問9 {#q9}

NLB の TCP ターゲットグループでクライアント IP の保持を無効にしました。1 台のターゲットの 1 つのポートへ、多数のクライアントから接続します。接続数が増えるとエラーが増えました。原因と対策はどれですか。

- A. NLB の SG の接続追跡の上限で、SG を外せば無制限になる
- B. NLB の AZ あたりの接続の上限が 1,000 で、Elastic IP を追加する
- C. ターゲット（IP とポート）あたり約 55,000 接続の上限で、ターゲットやポートを増やす
- D. クライアント IP の保持を無効にすると UDP に切り替わるので、TCP に設定し直す

??? success "答えと解説"
    **正解: C**

    ソース NAT のポートの上限です。

    - A: 誤り。問題文の上限の説明にならない。
    - B: 誤り。問題文の条件の上限はこの値ではない。
    - C: 正しい。
    - D: 誤り。保持の設定はプロトコルを変えない。

    **スキル:** [スケーリング](../domain1.md#t1-3-scaling) / **参照:** [NLB の設定](../../../services/networking.md#nlb-settings)

### 問10 {#q10}

既存の VM 上のアプリに ALB を入れます。ダウンタイムを避け、問題があればすぐ戻せるようにします。最も適切な移行の手順はどれですか。

- A. ALB を古い VM の前に置く前に、VM のアプリを HTTPS から HTTP へ変更してから DNS を切り替える
- B. 既存の DNS レコードの値を、ALB の作成の直後に一度で切り替えて古いサーバーを停止する
- C. ALB のスキームを内部で作り、切り替えの直前にインターネット向けに変更して公開する
- D. ALB を作ってターゲットの正常を確認し、DNS の TTL を下げてから加重レコードで少しずつ移す

??? success "答えと解説"
    **正解: D**

    段階的に切り替えます。

    - A: 誤り。問題文の手順の論点ではない。
    - B: 誤り。問題が起きたときに戻せない。
    - C: 誤り。スキームは作成後に変更できない。
    - D: 正しい。

    **スキル:** [他のサービスとの統合](../domain1.md#t1-3-integrations) / **参照:** [レコード](../../../services/networking.md#route53-records), [NLB の設定](../../../services/networking.md#nlb-settings)

### 問11 {#q11}

非 HTTP の NLB の前に Global Accelerator を置き、ALB の前には CloudFront を置く構成を検討しています。統合の説明として誤りのないものはどれですか。

- A. Global Accelerator の前には必ず CloudFront を置く必要があり、単独では使えない
- B. AWS WAF は ALB に付けられるが、NLB には付けられないので別の対策が要る
- C. Route 53 では NLB を指すエイリアスは作れず、`CNAME` しか使えない
- D. ACM の証明書は NLB のどのリージョンからでも共用でき、リージョンの指定は不要である

??? success "答えと解説"
    **正解: B**

    WAF の関連付け先に NLB は含まれません。

    - A: 誤り。単独で使える。
    - B: 正しい。
    - C: 誤り。エイリアスで指せる。
    - D: 誤り。証明書はロードバランサーと同じリージョン。

    **スキル:** [他のサービスとの統合](../domain1.md#t1-3-integrations) / **参照:** [ウェブ ACL の関連付け](../../../services/certificates.md#waf-association), [NLB の設定](../../../services/networking.md#nlb-settings)

### 問12 {#q12}

ALB をオリジンにした構成で、Route 53 のレコードが ALB の異常時に自動で別のリージョンへ切り替わるようにします。追加のヘルスチェックは作らず、既存のターゲットグループの状態を使います。正しい設定はどれですか。

- A. ターゲットグループの `HealthyHostCount` を読む Lambda でレコードを更新する
- B. ALB に Route 53 の計算ヘルスチェックを直接関連付ける
- C. エイリアスをやめて、ALB の DNS 名を `CNAME` で指定して TTL を 60 秒にする
- D. フェイルオーバーのエイリアスで `Evaluate Target Health` を `Yes` にする

??? success "答えと解説"
    **正解: D**

    エイリアスのターゲットの正常性を使えます。

    - A: 誤り。運用の手間が増え、API に依存する。
    - B: 誤り。ヘルスチェックはレコードに関連付けるもので、追加もしない要件。
    - C: 誤り。ターゲットの状態を反映できない。
    - D: 正しい。

    **スキル:** [他のサービスとの統合](../domain1.md#t1-3-integrations) / **参照:** [レコード](../../../services/networking.md#route53-records)

### 問13 {#q13}

NLB の `ip` ターゲットで、ターゲットは Transit Gateway の先のオンプレミスにあります。TCP のアプリがクライアントの IP をログに残す必要がありますが、クライアント IP の保持は使えません。アプリはプロキシプロトコル v2 を解釈できます。正しい対応はどれですか。

- A. ターゲットの SG で NLB のサブネットを拒否し、クライアントから直接の接続だけを許可する
- B. ターゲットグループでプロキシプロトコル v2 を有効にして、アプリでヘッダーを読む
- C. NLB のリスナーを ALB に変更せず、`X-Forwarded-For` を追加するルールをリスナーに設定する
- D. クロスゾーンを無効にして、クライアントの AZ を保持させて元の IP を取得する

??? success "答えと解説"
    **正解: B**

    プロキシプロトコル v2 はヘッダーで接続情報を渡します。

    - A: 誤り。問題文の経路が壊れる。
    - B: 正しい。
    - C: 誤り。NLB に HTTP ヘッダーを足す機能はない。
    - D: 誤り。クロスゾーンと IP の保持は別の話。

    **スキル:** [ロードバランサーの設定](../domain1.md#t1-3-config) / **参照:** [ターゲットグループの属性](../../../services/networking.md#target-group-attributes), [NLB の設定](../../../services/networking.md#nlb-settings)

### 問14 {#q14}

NLB のターゲットグループでプロキシプロトコル v2 を有効にしました。アプリを未対応のまま有効にしたところ、全ターゲットが異常になりました。原因として最も適切なものはどれですか。

- A. ヘルスチェックの接続にもヘッダーが付き、ターゲットが解釈できず失敗している
- B. プロキシプロトコルを有効にすると、NLB の TCP リスナーが自動で TLS に変わるので接続できない
- C. NLB の SG の既定のルールがヘッダーの付いた通信を破棄しているので、SG の変更で直る
- D. プロキシプロトコル v2 は NLB の `instance` ターゲットで常に禁止されているので、登録が消えている

??? success "答えと解説"
    **正解: A**

    先にアプリを対応させてから有効にします。

    - A: 正しい。
    - B: 誤り。リスナーのプロトコルは変わらない。
    - C: 誤り。SG はヘッダーの有無を判定しない。
    - D: 誤り。`instance` でも使える設定。

    **スキル:** [ロードバランサーの設定](../domain1.md#t1-3-config) / **参照:** [ターゲットグループの属性](../../../services/networking.md#target-group-attributes)

### 問15 {#q15}

ショッピングサイトの ALB の設定を見直します。カートの情報をサーバーに持つアプリがあり、新しいターゲットの準備時間も必要です。ALB の設定の説明として正しいものを選んでください。（2つ選択）

- A. `weighted_random` ではスティッキーセッションを併用できる
- B. スティッキーセッションは Cookie で行い、同じターゲットへ送り続ける
- C. `least_outstanding_requests` でもスロースタートを使える
- D. `round_robin` ではスロースタートを使える
- E. プロキシプロトコル v2 はターゲットグループで ALB ごとに有効にできる

??? success "答えと解説"
    **正解: B, D**

    アルゴリズムと併用できる機能に制限があります。

    - A: 誤り。併用できない。
    - B: 正しい。
    - C: 誤り。併用できない。
    - D: 正しい。
    - E: 誤り。ALB の場合は `X-Forwarded-For` で渡す。プロキシプロトコルは NLB の設定。

    **スキル:** [ロードバランサーの設定](../domain1.md#t1-3-config) / **参照:** [スティッキーセッション](../../../services/networking.md#stickiness), [クロスゾーン負荷分散](../../../services/networking.md#cross-zone)

### 問16 {#q16}

GWLB のターゲットグループを作成します。仮想ファイアウォールの通信を受けるプロトコルとポートで正しいものはどれですか。

- A. TCP_UDP、ポート 443。通常の NLB と同じ設定で受ける
- B. VXLAN、ポート 4789。ミラーと共通の形式で受ける
- C. GENEVE、ポート 6081。この形式でカプセル化して受ける
- D. GRE、ポート番号なし。Connect と同じカプセル化で受ける

??? success "答えと解説"
    **正解: C**

    GWLB は GENEVE の 6081 です。

    - A: 誤り。GWLB の形式ではない。
    - B: 誤り。VXLAN は Traffic Mirroring の形式。
    - C: 正しい。
    - D: 誤り。GRE は Connect の形式。

    **スキル:** [ターゲットグループの設定](../domain1.md#t1-3-target-groups) / **参照:** [GWLB](../../../services/networking.md#gwlb), [Gateway Load Balancer による検査](../../../services/network-connectivity.md#gwlb-inspection)

### 問17 {#q17}

GWLB の検査を入れてから、大きなパケットだけが消えるようになりました。インターフェイスの MTU は 8500 です。フラグメントも ICMP のエラーも返りません。アプライアンスの MTU はどうしますか。

- A. 8500 のままで、GWLB の属性でフラグメントを有効にする
- B. 1500 に下げて、アプライアンスの側でパケットを分割する
- C. 8568 以上に対応させる。GENEVE の分を足した値にする
- D. 9001 より大きな値にできないので、VPC の MTU を GWLB の前で 1500 に固定する

??? success "答えと解説"
    **正解: C**

    GENEVE が 68 バイト足します。

    - A: 誤り。GWLB はフラグメントしない。
    - B: 誤り。大きなパケットの問題を解決しない。
    - C: 正しい。
    - D: 誤り。対処として過剰で、問題文の根本の値でもない。

    **スキル:** [ターゲットグループの設定](../domain1.md#t1-3-target-groups) / **参照:** [Gateway Load Balancer による検査](../../../services/network-connectivity.md#gwlb-inspection), [MTU とジャンボフレーム](../../../services/network-connectivity.md#mtu)

### 問18 {#q18}

NLB の背後のアプリがクライアント IP をログに残します。ターゲットを EC2 と Fargate の両方で検討しています。ターゲットの種類と送信元 IP の既定について、正しい組み合わせはどれですか。

- A. `instance` のターゲットはピアリング先のインスタンスも ID で登録できる
- B. `alb` のターゲットは TCP と UDP の両方に対応し、ALB に UDP の通信を渡せる
- C. `instance` の TCP は既定でクライアント IP を保持し、`ip` の TCP は既定で NLB の IP になる
- D. `ip` の UDP は既定で NLB の IP になり、`instance` の TCP は既定でプロキシプロトコルが有効になる

??? success "答えと解説"
    **正解: C**

    ターゲットの種類とプロトコルで、送信元の IP の既定が変わります。

    - A: 誤り。VPC の外のターゲットは `ip` で登録する。
    - B: 誤り。ALB は UDP を受けない。
    - C: 正しい。
    - D: 誤り。UDP は保持され、プロキシプロトコルの既定は無効。

    **スキル:** [ターゲットグループの設定](../domain1.md#t1-3-target-groups) / **参照:** [ターゲットタイプ](../../../services/networking.md#target-types), [NLB の設定](../../../services/networking.md#nlb-settings)

### 問19 {#q19}

EKS で Kubernetes の `Service`（`type: LoadBalancer`）を AWS Load Balancer Controller で公開します。Pod は Fargate で動きます。NLB のターゲットの種類はどれにしますか。

- A. `lambda`。Pod へのプロキシ関数を登録する
- B. `alb`。Fargate の Pod を ALB 経由で登録する
- C. `ip`。Pod の IP をターゲットとして直接登録する
- D. `instance`。Fargate のノードポートへ送る

??? success "答えと解説"
    **正解: C**

    Fargate の Pod にはノードがないので `ip` を使います。

    - A: 誤り。NLB のターゲットの種類にない。
    - B: 誤り。問題文の NLB の直接のターゲットとして適切でない。
    - C: 正しい。
    - D: 誤り。Fargate の Pod にノードはない。

    **スキル:** [AWS Load Balancer Controller](../domain1.md#t1-3-lbc) / **参照:** [EKS](../../../services/containers.md#eks)

### 問20 {#q20}

AWS Load Balancer Controller を導入しましたが、`Ingress` を作っても ALB ができません。コントローラーのログに `AccessDenied` があります。正しい対応はどれですか。

- A. コントローラーを削除して、`Ingress` を in-tree のクラウドプロバイダーに任せて ALB を作る
- B. `Ingress` を `Service` に変更して NLB を作り、権限の問題を避ける
- C. コントローラーのサービスアカウントに、ELB などの AWS API を呼ぶ IAM 権限を与える
- D. VPC CNI を Calico に置き換えて、コントローラーの API を内部で処理する

??? success "答えと解説"
    **正解: C**

    コントローラーには AWS の API を呼ぶ権限が必要です。

    - A: 誤り。in-tree は ALB を作成しない。
    - B: 誤り。権限の問題は解消しない。
    - C: 正しい。
    - D: 誤り。AWS API の権限の問題が解決しない。

    **スキル:** [AWS Load Balancer Controller](../domain1.md#t1-3-lbc) / **参照:** [EKS](../../../services/containers.md#eks), [Pod に IAM 権限を与える](../../../services/containers.md#pod-identity)

### 問21 {#q21}

Kubernetes のリソースと、AWS Load Balancer Controller が作るものの組み合わせとして正しいものを選んでください。（2つ選択）

- A. `Service`（`type: LoadBalancer`）は ALB を作る
- B. `Ingress` は ALB を作る
- C. `Ingress` は GWLB を作る
- D. `NetworkPolicy` は NLB のターゲットグループを作る
- E. `Service`（`type: LoadBalancer`）は NLB を作る

??? success "答えと解説"
    **正解: B, E**

    `Gateway` API はバージョン 2.14.0 以降で ALB を作ることもできます。

    - A: 誤り。ALB ではなく NLB。
    - B: 正しい。
    - C: 誤り。GWLB は作られない。
    - D: 誤り。`NetworkPolicy` はロードバランサーを作らない。
    - E: 正しい。

    **スキル:** [AWS Load Balancer Controller](../domain1.md#t1-3-lbc) / **参照:** [EKS](../../../services/containers.md#eks)

### 問22 {#q22}

規制で「ロードバランサーで復号してはならない」とされ、ターゲットが証明書と TLS の終端を持ちます。HTTP のパスの振り分けは不要です。最も適切な構成はどれですか。

- A. ALB の HTTPS リスナーで終端してターゲットへ再暗号化する
- B. CloudFront でビューワー側を終端し、オリジンにも HTTPS で接続する
- C. NLB の TCP リスナーでパススルーし、ターゲットで TLS を終端する
- D. NLB の TLS リスナーで ACM の証明書を使い、ターゲットへ TCP で送る

??? success "答えと解説"
    **正解: C**

    ターゲットで終端するなら TCP のパススルーです。

    - A: 誤り。ALB で復号している。
    - B: 誤り。CloudFront で復号している。
    - C: 正しい。
    - D: 誤り。NLB で復号している。

    **スキル:** [暗号化と認証](../domain1.md#t1-3-tls) / **参照:** [NLB の設定](../../../services/networking.md#nlb-settings), [転送時の TLS](../../../services/certificates.md#tls-in-transit)

### 問23 {#q23}

ALB の HTTPS リスナーで終端したあと、ターゲットとの区間も暗号化します。ターゲットの証明書の管理の手間を減らしたいと考えています。ALB の動作として正しいものはどれですか。

- A. 区間の暗号化には ALB の TCP リスナーが必要で、HTTPS リスナーとは併用できない
- B. ターゲットには自己署名の証明書も使える。ALB は検証しない
- C. ALB はターゲットへの通信を自動でトンネルするので、ターゲット側の TLS の設定は不要になる
- D. ターゲットの証明書は ACM の公開証明書に限られ、ALB が発行元を検証する

??? success "答えと解説"
    **正解: B**

    ターゲットグループのプロトコルを HTTPS にします。

    - A: 誤り。ALB に TCP リスナーはない。
    - B: 正しい。
    - C: 誤り。暗号化するにはターゲットで TLS を設定する。
    - D: 誤り。ALB はターゲットの証明書を検証しない。

    **スキル:** [暗号化と認証](../domain1.md#t1-3-tls) / **参照:** [転送時の TLS](../../../services/certificates.md#tls-in-transit), [リスナーとルール](../../../services/networking.md#alb-listeners)

### 問24 {#q24}

ALB のリスナーで、社内の OIDC プロバイダーを使って利用者を認証します。アプリは認証済みのリクエストだけを受けます。アプリの認証コードは増やさないことが条件です。設定はどれですか。

- A. NLB を前に置いて、TCP の中で OIDC のトークンを確認する
- B. HTTP リスナーの認証アクションに OIDC を設定して TLS は使わない
- C. HTTPS リスナーの認証アクションに OIDC を設定し、社内の IdP の情報を登録する
- D. WAF の Web ACL のルールで、OIDC のログイン画面へリダイレクトする

??? success "答えと解説"
    **正解: C**

    ALB のリスナーは Cognito や OIDC で認証できます。

    - A: 誤り。NLB は L7 のトークンの確認を行わない。
    - B: 誤り。認証アクションは HTTPS リスナーで使う。
    - C: 正しい。
    - D: 誤り。利用者の認証は WAF の機能ではない。

    **スキル:** [暗号化と認証](../domain1.md#t1-3-tls) / **参照:** [リスナーとルール](../../../services/networking.md#alb-listeners)

### 問25 {#q25}

ALB のターゲットの異常を 20 秒程度で検知したいと考えています。既定は間隔 30 秒、`UnhealthyThresholdCount` が 2 です。ヘルスチェックの設定はどれですか。

- A. タイムアウトを 2 秒にする。間隔としきい値は変更しない
- B. 間隔を 10 秒、`UnhealthyThresholdCount` を 2 にする
- C. 間隔を 30 秒、`UnhealthyThresholdCount` を 1 にする
- D. `HealthyThresholdCount` を 10 に増やして、間隔は変更しない

??? success "答えと解説"
    **正解: B**

    間隔 × しきい値で計算します。

    - A: 誤り。検知は 60 秒のまま。
    - B: 正しい。
    - C: 誤り。最小は 2 で、1 にはできない。
    - D: 誤り。正常に戻る判定で、異常の検知は速くならない。

    **スキル:** [負荷分散](../domain2.md#t2-1-load-balancing) / **参照:** [ヘルスチェックの計算](../../../services/networking.md#health-check-calc)

### 問26 {#q26}

ALB でときどき HTTP 502 が出ます。ターゲットのログに異常はなく、負荷も低いです。ターゲットは Web サーバーのキープアライブのタイムアウトが 5 秒で、ALB のアイドルタイムアウトは 60 秒です。最も適切な対応はどれですか。

- A. ALB の AZ を増やして、ターゲットへの接続の分散を改善する
- B. ALB のアイドルタイムアウトを 600 秒に延ばして、ターゲットの切断を減らす
- C. ターゲットのキープアライブを ALB のアイドルタイムアウトより長くする
- D. ターゲットの SG で ALB の範囲を許可して、接続の切断を防ぐ

??? success "答えと解説"
    **正解: C**

    ターゲットが先に切断すると 502 になります。

    - A: 誤り。根本の原因が解決しない。
    - B: 誤り。差が広がり、悪化する。
    - C: 正しい。
    - D: 誤り。接続はできており、SG の問題ではない。

    **スキル:** [負荷分散](../domain2.md#t2-1-load-balancing) / **参照:** [ALB のエラーの原因一覧](../../../services/networking.md#alb-error-detail), [アイドルタイムアウトとキープアライブ](../../../services/networking.md#alb-idle-timeout)

### 問27 {#q27}

ALB から HTTP 504 が返ります。ターゲットは別のサブネットにあり、最近 NACL を変更しました。遅い処理はありません。ALB のターゲットの SG は問題ありません。確認の順序として最も適切なものはどれですか。

- A. 登録されたターゲットが 0 台でないかを確認し、それから ACM の証明書の期限を確認する
- B. ターゲットの応答が 200 でないことを確認し、ヘルスチェックのパスを変更する
- C. ALB のログを無効にして ALB の負荷を減らしてから、アプリのログを確認する
- D. サブネットの NACL で戻りのエフェメラルポートが許可されているかを確認する

??? success "答えと解説"
    **正解: D**

    504 はアイドルタイムアウトや NACL の戻りの通信を疑います。

    - A: 誤り。0 台なら 503 で、証明書は 504 の原因にならない。
    - B: 誤り。504 は応答が来ないときの症状。
    - C: 誤り。ログの無効化は対策にならない。
    - D: 正しい。

    **スキル:** [負荷分散](../domain2.md#t2-1-load-balancing) / **参照:** [ALB のエラーの原因一覧](../../../services/networking.md#alb-error-detail)

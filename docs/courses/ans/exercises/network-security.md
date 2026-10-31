# ネットワークのセキュリティの問題集

対象の解説: [Network Firewall](../../../services/network-connectivity.md#network-firewall), [Gateway Load Balancer による検査](../../../services/network-connectivity.md#gwlb-inspection), [DNS Firewall](../../../services/network-connectivity.md#dns-firewall), [Shield](../../../services/threat-detection.md#shield), [AWS WAF](../../../services/certificates.md#waf)

### 問1 {#q1}

スポーク VPC の通信を、Transit Gateway の検査 VPC の Network Firewall へ送っています。同じ AZ の通信は通るのに、AZ をまたぐ通信が一部失敗します。ファイアウォールのログで戻りの通信が破棄されています。最も適切な対応はどれですか。

- A. 検査 VPC のファイアウォールのエンドポイントを 1 つの AZ に集約する
- B. 検査 VPC のアタッチメントでアプライアンスモードを有効にする
- C. スポーク VPC のアタッチメントでアプライアンスモードを有効にする
- D. ファイアウォールのステートレスの既定を `Pass` にして、戻りの通信を許可する

??? success "答えと解説"
    **正解: B**

    行きと戻りが別の AZ の機器を通ると、ステートフルな機器が破棄します。

    - A: 誤り。AZ の障害に耐えられなくなる。
    - B: 正しい。
    - C: 誤り。設定する場所は検査 VPC のアタッチメント。
    - D: 誤り。ステートフルのルールが評価されなくなる。

    **スキル:** [アプライアンス](../domain2.md#t2-1-appliances) / **参照:** [アプライアンスモード](../../../services/network-connectivity.md#tgw-appliance-mode)

### 問2 {#q2}

Transit Gateway の VPC 間の通信を Network Firewall で検査します。検査用の VPC のサブネットとルートの管理をなくし、対称の経路も自動で確保します。最も適切な方法はどれですか。

- A. 検査 VPC の VPC アタッチメント。アプライアンスモードを有効にする
- B. 分散型のファイアウォールエンドポイント。各 VPC に作る
- C. ネットワーク機能アタッチメント
- D. Connect のアタッチメント。ファイアウォールと GRE でつなぐ

??? success "答えと解説"
    **正解: C**

    アプライアンスモードは自動で有効です。

    - A: 誤り。検査 VPC の管理が残る。
    - B: 誤り。各 VPC のサブネットとルートの管理が増える。
    - C: 正しい。
    - D: 誤り。SD-WAN の接続で、Network Firewall を付ける方法ではない。

    **スキル:** [アプライアンス](../domain2.md#t2-1-appliances) / **参照:** [ネットワーク機能アタッチメント](../../../services/network-connectivity.md#tgw-network-function)

### 問3 {#q3}

第三者の仮想ファイアウォールで VPC の全ポートの通信を透過的に検査します。ファイアウォールは冗長で、台数も増減します。通信は VPC のルートテーブルで検査へ向けます。最も適切なものはどれですか。

- A. ALB の HTTP リスナーで、ファイアウォールをターゲットにする
- B. NLB の TCP リスナーで、ファイアウォールをターゲットにする
- C. GWLB とエンドポイント。第三者の機器をターゲットにし、ルートで向ける
- D. VPC Route Server で、ファイアウォールの ENI へ経路を切り替える

??? success "答えと解説"
    **正解: C**

    第三者のアプライアンスは GWLB です。

    - A: 誤り。L7 の処理で、透過にならない。
    - B: 誤り。全ポートの透過の用途に向かず、ルートで向ける先にもならない。
    - C: 正しい。
    - D: 誤り。冗長な機器の台数の増減と負荷分散を担わない。

    **スキル:** [アプライアンス](../domain2.md#t2-1-appliances) / **参照:** [Gateway Load Balancer による検査](../../../services/network-connectivity.md#gwlb-inspection)

### 問4 {#q4}

集中型の Network Firewall で、スポーク VPC の通信がステートフルのルールに一致しません。ステートレスの既定は `Forward to stateful` です。`HOME_NET` は既定のままで、検査 VPC の CIDR だけが対象です。最も適切な修正はどれですか。

- A. 作成済みのポリシーの `RuleOrder` を変更する
- B. `HOME_NET` をスポークの CIDR を含むように上書きする
- C. ファイアウォールのサブネットにスポークの ENI を追加する
- D. ステートレスの既定を `Pass` に変更する

??? success "答えと解説"
    **正解: B**

    スポークの CIDR が含まれないと、ルールが一致しません。

    - A: 誤り。ポリシーの作成時にしか指定できない。
    - B: 正しい。
    - C: 誤り。サブネットは専用にする。
    - D: 誤り。ステートフルのルールが評価されなくなる。

    **スキル:** [境界のセキュリティ](../domain2.md#t2-2-security) / **参照:** [ステートフルのルール順序](../../../services/network-connectivity.md#nfw-rule-order), [Network Firewall](../../../services/network-connectivity.md#network-firewall)

### 問5 {#q5}

Network Firewall の Strict のルール順序で、特定のドメインへの HTTPS だけを許可します。他の TLS の通信はすべて止めます。ルールで SNI を確認します。既定アクションとして最も適切なものはどれですか。

- A. `Drop established`
- B. `Drop all`。SNI を確認する前の TCP も含めて止める
- C. `Alert established` のみ。通信を通して記録する
- D. 既定アクションを指定せず、Strict の暗黙の拒否に任せる

??? success "答えと解説"
    **正解: A**

    TCP のハンドシェイクを通してから、確立した接続を判定します。

    - A: 正しい。
    - B: 誤り。SNI を確認する前に止まる。
    - C: 誤り。通信は止まらない。
    - D: 誤り。既定では拒否されないので、指定する。

    **スキル:** [境界のセキュリティ](../domain2.md#t2-2-security) / **参照:** [ステートフルのルール順序](../../../services/network-connectivity.md#nfw-rule-order)

### 問6 {#q6}

3 層のアプリと複数の VPC の間の境界を設計します。戻りの通信で過去に障害がありました。手段の説明として正しいものを選んでください。（2つ選択）

- A. エンドポイントポリシーは L3 のパケットを検査する
- B. SG はステートフルで、ENI に付ける
- C. NACL は ENI に付け、番号の順に関係なく全部のルールを評価する
- D. NACL はステートレスで、戻りのエフェメラルポートの許可が要る
- E. SG は拒否のルールを指定でき、特定の IP を拒否できる

??? success "答えと解説"
    **正解: B, D**

    層と付ける場所を覚えます。

    - A: 誤り。API の権限の上限。
    - B: 正しい。
    - C: 誤り。サブネットに付け、番号の順に評価する。
    - D: 正しい。
    - E: 誤り。SG は許可のみ。

    **スキル:** [境界のセキュリティ](../domain2.md#t2-2-security) / **参照:** [セキュリティグループとネットワーク ACL](../../../services/networking.md#security-groups-nacls), [Network Firewall](../../../services/network-connectivity.md#network-firewall)

### 問7 {#q7}

非 HTTP の公開サービスを NLB で提供しています。大規模な DDoS の費用を保護し、攻撃時に AWS の支援を受けます。NLB には Elastic IP が付いています。最も適切な選択はどれですか。

- A. NLB に AWS WAF を付けて、レートベースのルールを使う
- B. Shield Advanced で Elastic IP を保護対象に指定する
- C. Network Firewall の Strict のルールで攻撃を止める
- D. Shield Standard の有効化を確認して SRT へ連絡する

??? success "答えと解説"
    **正解: B**

    Elastic IP として保護します。

    - A: 誤り。WAF は NLB に付けられない。
    - B: 正しい。
    - C: 誤り。費用の保護と AWS の支援にならない。
    - D: 誤り。コスト保護と SRT は Advanced の機能。

    **スキル:** [受信](../domain4.md#t4-1-inbound) / **参照:** [Shield Advanced](../../../services/threat-detection.md#shield-advanced)

### 問8 {#q8}

ALB の Web アプリで、SQL インジェクションと特定の IP の過剰なリクエストを止めます。ルールの運用はできるだけ減らします。最も適切なものはどれですか。

- A. Network Firewall の Suricata のルールを自作して VPC の入口で止める
- B. Shield Advanced の自動緩和だけで SQL インジェクションを止める
- C. AWS WAF のマネージドルールとレートベースルールを ALB に適用する
- D. NACL の拒否ルールを、攻撃の IP ごとに手で追加する

??? success "答えと解説"
    **正解: C**

    L7 の攻撃は WAF です。

    - A: 誤り。運用が増え、暗号化された L7 の判定も難しい。
    - B: 誤り。DDoS の対策で、SQL インジェクションの判定ではない。
    - C: 正しい。
    - D: 誤り。L7 を判定できず、運用も増える。

    **スキル:** [受信](../domain4.md#t4-1-inbound) / **参照:** [AWS WAF](../../../services/certificates.md#waf), [似た機能との比較](../../../services/certificates.md#waf-comparison)

### 問9 {#q9}

Shield Advanced を契約して CloudFront と ALB を保護します。誤検知を減らすことも求められています。正しい説明を選んでください。（2つ選択）

- A. 契約すると組織の全リソースが自動で保護対象になる
- B. ヘルスベース検出で誤検知が減り、検出が早くなる
- C. リソースは自動では保護されないので指定する
- D. 攻撃の検出には Network Firewall が前提になる
- E. NLB にも AWS WAF を直接付けられるようになる

??? success "答えと解説"
    **正解: B, C**

    Advanced の特徴です。

    - A: 誤り。指定する。
    - B: 正しい。
    - C: 正しい。
    - D: 誤り。前提ではない。
    - E: 誤り。WAF は NLB に付かない。

    **スキル:** [受信](../domain4.md#t4-1-inbound) / **参照:** [Shield Advanced](../../../services/threat-detection.md#shield-advanced)

### 問10 {#q10}

プライベートサブネットの EC2 から、許可したドメインだけに HTTPS で出します。IP 直接の通信も止めます。集中型の検査 VPC があります。最も適切な構成はどれですか。

- A. SG の送信のルールに許可のドメインを書く
- B. NAT ゲートウェイを許可の IP の経路にだけ通す
- C. Network Firewall の Strict で SNI を許可する
- D. DNS Firewall で許可したドメインだけを解決する

??? success "答えと解説"
    **正解: C**

    ドメインと IP の両方で制限します。

    - A: 誤り。SG にドメインのルールはない。
    - B: 誤り。ドメインで判定できず、IP の変化にも追従できない。
    - C: 正しい。
    - D: 誤り。IP 直接の通信や独自の DNS はすり抜ける。

    **スキル:** [送信](../domain4.md#t4-1-outbound) / **参照:** [DNS Firewall](../../../services/network-connectivity.md#dns-firewall), [Network Firewall](../../../services/network-connectivity.md#network-firewall)

### 問11 {#q11}

EC2 のマルウェアが、悪意のあるドメインを VPC Resolver で解決することを止めます。DNS トンネリングの検出も行います。ドメインの一覧は AWS の管理のものを使います。最も適切なものはどれですか。

- A. GuardDuty の検出で解決を止める
- B. Network Firewall のステートレスのルールで UDP 53 を全部止める
- C. AWS WAF の IP レピュテーションのルールを VPC に付ける
- D. DNS Firewall の管理ドメインリストと Advanced ルール

??? success "答えと解説"
    **正解: D**

    ドメインの解決を止めます。

    - A: 誤り。検出のサービスで、解決を止めない。
    - B: 誤り。既定の DNS の解決も止まるおそれがあり、ドメインの判定もできない。
    - C: 誤り。WAF は VPC の DNS に付けられない。
    - D: 正しい。

    **スキル:** [送信](../domain4.md#t4-1-outbound) / **参照:** [DNS Firewall](../../../services/network-connectivity.md#dns-firewall)

### 問12 {#q12}

スポーク VPC からインターネットへの通信を集中して検査します。NAT の変換の前に元の IP でルールを評価します。経路の順序として正しいものはどれですか。

- A. Transit Gateway、NAT、Network Firewall、IGW の順
- B. Transit Gateway、Network Firewall、NAT、IGW の順
- C. Network Firewall、IGW、Transit Gateway、NAT の順
- D. NAT、Transit Gateway、Network Firewall、IGW の順

??? success "答えと解説"
    **正解: B**

    集中型の出口です。

    - A: 誤り。NAT の後ではスポークの IP でルールを評価できない。
    - B: 正しい。
    - C: 誤り。検査と変換の前にインターネットへ出てしまう。
    - D: 誤り。スポークの NAT の後では元の IP が分からない。

    **スキル:** [送信](../domain4.md#t4-1-outbound) / **参照:** [ルーティング](../../../services/network-connectivity.md#nfw-routing), [NAT ゲートウェイ](../../../services/network-connectivity.md#nat-gateway)

### 問13 {#q13}

別のアカウントのバケットへの持ち出しを防ぐため、VPC エンドポイントのポリシーで S3 の宛先を絞ります。担当者は「このポリシーで EC2 にも権限が付く」と考えています。正しい説明はどれですか。

- A. エンドポイントのポリシーが許可すれば、IAM の許可がなくてもアクセスできる
- B. エンドポイントのポリシーは、NAT ゲートウェイ経由の通信にも適用される
- C. エンドポイント経由のアクセスの上限を決めるだけで、権限は与えない
- D. エンドポイントのポリシーは、パケットを L3 で検査して宛先を判定する

??? success "答えと解説"
    **正解: C**

    権限の上限です。

    - A: 誤り。権限を与えない。
    - B: 誤り。エンドポイントを通る通信にのみ適用される。
    - C: 正しい。
    - D: 誤り。API の権限の話。

    **スキル:** [VPC 間](../domain4.md#t4-1-inter-vpc) / **参照:** [エンドポイントポリシー](../../../services/networking.md#endpoint-policies)

### 問14 {#q14}

Transit Gateway で本番と開発を分離します。誤設定に強い設計にします。アタッチメント用サブネットの NACL は変更しません。最も適切なものはどれですか。

- A. 既定のルートテーブルのまま、各 SG で開発の CIDR を許可しない
- B. 開発 VPC に別の Transit Gateway をピアリングする
- C. 本番と開発でルートテーブルを分け、関連付けと伝播で経路を分ける
- D. 本番 VPC の NACL で開発の CIDR を拒否して、経路は共通にする

??? success "答えと解説"
    **正解: C**

    経路で分離します。

    - A: 誤り。経路が残り、誤設定で通信できる。
    - B: 誤り。静的ルートが増え、この要件に対して過剰。
    - C: 正しい。
    - D: 誤り。経路が残り、運用も増える。

    **スキル:** [VPC 間](../domain4.md#t4-1-inter-vpc) / **参照:** [ルートテーブル](../../../services/network-connectivity.md#tgw-route-tables), [セキュリティグループとネットワーク ACL](../../../services/networking.md#security-groups-nacls)

### 問15 {#q15}

組織全体で VPC 間の SG と NACL の基準を強制します。新しいアカウントにも適用し、違反は修復します。最も適切なものはどれですか。

- A. Config のアグリゲーターで非準拠を一覧にする
- B. StackSets で SG を配るだけで、以後の変更は確認しない
- C. 各アカウントの Trusted Advisor の推奨を担当者が確認する
- D. Firewall Manager の SG と NACL のポリシーを組織へ適用する

??? success "答えと解説"
    **正解: D**

    組織全体の基準を強制します。

    - A: 誤り。集約で、強制や修復はしない。
    - B: 誤り。変更後の違反を修復しない。
    - C: 誤り。手軽な点検で強制しない。
    - D: 正しい。

    **スキル:** [VPC 間](../domain4.md#t4-1-inter-vpc) / **参照:** [Firewall Manager](../../../services/threat-detection.md#firewall-manager), [セキュリティグループとネットワーク ACL](../../../services/networking.md#security-groups-nacls)

### 問16 {#q16}

規制データの VPC からインターネットへの経路を一切なくします。AWS サービスへはプライベートで接続し、オンプレミスとは DX で接続します。最も適切な構成はどれですか。

- A. パブリックサブネットと SG の最小の許可
- B. IGW のない分離された VPC とエンドポイント
- C. プライベートサブネットと NAT ゲートウェイの送信先の制限
- D. Egress-only IGW と IPv6 のみのサブネット

??? success "答えと解説"
    **正解: B**

    分離された VPC です。

    - A: 誤り。インターネットへの経路が残る。
    - B: 正しい。
    - C: 誤り。インターネットへの経路が残る。
    - D: 誤り。外向きの経路が残る。

    **スキル:** [ネットワーク構成](../domain4.md#t4-1-architecture) / **参照:** [サブネットとルートテーブル](../../../services/networking.md#subnets-route-tables)

### 問17 {#q17}

複数のパートナーから VPN で接続を受け、検査してから内部へ通します。パートナーの CIDR は信頼できません。内部の VPC は Transit Gateway で接続しています。最も適切な構成はどれですか。

- A. DMZ の VPC で受け、検査してから Transit Gateway へ渡す
- B. パートナーへ内部の VPC のサブネットを RAM で共有する
- C. パートナーの VPN を Transit Gateway へ直接アタッチし、内部の VPC と同じルートテーブルにする
- D. 内部の VPC の VGW に VPN を接続し、SG で絞る

??? success "答えと解説"
    **正解: A**

    信頼できないネットワークのパターンです。

    - A: 正しい。
    - B: 誤り。同じ信頼の境界向きの方法。
    - C: 誤り。検査なしで内部へ入る。
    - D: 誤り。検査がなく、内部へ直接入る。

    **スキル:** [ネットワーク構成](../domain4.md#t4-1-architecture) / **参照:** [サブネットとルートテーブル](../../../services/networking.md#subnets-route-tables), [検査の配置](../../../services/network-connectivity.md#choosing-inspection)

### 問18 {#q18}

アカウントのリージョン単位で、インターネットからの受信を一括で止めます。NAT の外向きは残し、特定の VPC だけ例外にします。ルートや SG の変更に左右されません。最も適切なものはどれですか。

- A. S3 の Block Public Access のアカウントの設定
- B. Firewall Manager の NACL のポリシーで全サブネットを拒否する
- C. SCP で `ec2:AttachInternetGateway` を拒否する
- D. VPC Block Public Access の受信のみのモードと除外

??? success "答えと解説"
    **正解: D**

    ルートや SG の設定より優先されます。

    - A: 誤り。S3 の設定。
    - B: 誤り。NAT の戻りも影響を受け、ルートの優先の仕組みでもない。
    - C: 誤り。既存の IGW の通信を止めない。
    - D: 正しい。

    **スキル:** [ネットワーク構成](../domain4.md#t4-1-architecture) / **参照:** [サブネットとルートテーブル](../../../services/networking.md#subnets-route-tables)

### 問19 {#q19}

別の VPC のサービスへの通信を、呼び出す側の IAM ロールで制御します。CIDR は重複しており、アプリは HTTP です。最も適切なものはどれですか。

- A. PrivateLink のエンドポイントポリシーと NLB
- B. VPC ピアリングと SG の参照
- C. Transit Gateway の 1:1 NAT とルートテーブルの分離
- D. VPC Lattice の認証ポリシー

??? success "答えと解説"
    **正解: D**

    サービス単位の認可です。

    - A: 誤り。カスタムのサービスの認可の機能として不十分。
    - B: 誤り。CIDR が重複すると作れず、IAM の認可でもない。
    - C: 誤り。経路の制御で、IAM の認可でもない。
    - D: 正しい。

    **スキル:** [通信を守る仕組み](../domain4.md#t4-1-flows) / **参照:** [VPC Lattice](../../../services/network-connectivity.md#vpc-lattice), [VPC エンドポイントと PrivateLink](../../../services/networking.md#vpc-endpoints)

### 問20 {#q20}

社員の端末から社内の Web アプリへ、VPN なしで接続します。ID とデバイスの状態を評価して、アプリごとに許可します。最も適切なものはどれですか。

- A. Site-to-Site VPN を社員の端末から接続する
- B. インターネット向け ALB の OIDC 認証のみで許可する
- C. Client VPN の認可ルールで CIDR ごとに許可する
- D. Verified Access で ID とデバイスの状態をアプリごとに評価する

??? success "答えと解説"
    **正解: D**

    端末からの接続の選択肢です。

    - A: 誤り。拠点の接続の仕組み。
    - B: 誤り。デバイスの状態を評価しない。
    - C: 誤り。VPN を使い、デバイスの状態もアプリ単位で評価しない。
    - D: 正しい。

    **スキル:** [通信を守る仕組み](../domain4.md#t4-1-flows) / **参照:** [Verified Access](../../../services/identity-directory.md#verified-access), [Client VPN](../../../services/network-connectivity.md#client-vpn)

### 問21 {#q21}

3 層のアプリで、Web から App へ、App から DB へのみ通します。Auto Scaling で IP が変わっても設定を変えずに済ませます。最も適切なものはどれですか。

- A. NACL で層のサブネットの CIDR を許可して、戻りも開ける
- B. Lambda で新しい IP を SG に追加し続ける
- C. SG の参照で必要な層だけ許可し、IP に依存しないようにする
- D. Network Firewall を層の間に挟み、全部の IP をルールに書く

??? success "答えと解説"
    **正解: C**

    層の間は SG の参照です。

    - A: 誤り。サブネット単位で、同じ層の細かな制御ができない。
    - B: 誤り。運用が増える。
    - C: 正しい。
    - D: 誤り。過剰で、IP の変化にも追従しにくい。

    **スキル:** [通信を守る仕組み](../domain4.md#t4-1-flows) / **参照:** [セキュリティグループとネットワーク ACL](../../../services/networking.md#security-groups-nacls)

### 問22 {#q22}

公開の非 HTTP サービスと、VPC エンドポイント経由の S3 の両方について脅威モデルを作っています。脅威と緩和策の組み合わせとして適切なものを選んでください。（2つ選択）

- A. DNS トンネリング: SG のポート 53 の許可
- B. 別アカウントのバケットへの持ち出し: エンドポイントポリシー
- C. L4 の DDoS: Shield Advanced と Elastic IP の保護
- D. SQL インジェクション: NLB のプロキシプロトコル
- E. 平文の専用線: Traffic Mirroring で複製

??? success "答えと解説"
    **正解: B, C**

    構成ごとに脅威を整理します。

    - A: 誤り。DNS Firewall を使う。
    - B: 正しい。
    - C: 正しい。
    - D: 誤り。L7 の攻撃は WAF。
    - E: 誤り。暗号化ではない。

    **スキル:** [脅威モデル](../domain4.md#t4-1-threat-models) / **参照:** [Shield](../../../services/threat-detection.md#shield), [エンドポイントポリシー](../../../services/networking.md#endpoint-policies)

### 問23 {#q23}

内部の多層のシステムで、1 台のホストが侵害された場合の被害の拡大を抑えます。外部への通信は既に検査しています。緩和策として最も適切なものはどれですか。

- A. CloudFront と AWS WAF を内部の通信の前に追加する
- B. SG の最小化と、サブネットや Transit Gateway の分離
- C. Shield Advanced を全 EC2 の Elastic IP に適用する
- D. MACsec で DX の通信を暗号化する

??? success "答えと解説"
    **正解: B**

    横移動の対策です。

    - A: 誤り。外部からの攻撃の緩和策。
    - B: 正しい。
    - C: 誤り。DDoS の対策。
    - D: 誤り。内部の横移動の対策にならない。

    **スキル:** [脅威モデル](../domain4.md#t4-1-threat-models) / **参照:** [Network Firewall](../../../services/network-connectivity.md#network-firewall), [セキュリティグループとネットワーク ACL](../../../services/networking.md#security-groups-nacls)

### 問24 {#q24}

新しいハイブリッド構成の脅威モデルを作ります。チームはまず対策の製品を決めようとしています。手順として最も適切なものはどれですか。

- A. 先にアプライアンスを購入し、機能に合わせて脅威を選ぶ
- B. データの流れから境界を見つけ、脅威と緩和策を割り当て、テストする
- C. 全リソースに AWS WAF と Shield Advanced を付けて脅威の列挙を省く
- D. 責任共有モデルにより AWS に任せて、お客様の分析は省く

??? success "答えと解説"
    **正解: B**

    境界ごとに整理します。

    - A: 誤り。脅威の整理の前に対策を決めている。
    - B: 正しい。
    - C: 誤り。整理にならず、付けられないリソースもある。
    - D: 誤り。お客様の責任の範囲がある。

    **スキル:** [脅威モデル](../domain4.md#t4-1-threat-models) / **参照:** [GuardDuty](../../../services/threat-detection.md#guardduty)

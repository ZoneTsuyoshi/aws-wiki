# Direct Connectの問題集

対象の解説: [Direct Connect](../../../services/network-connectivity.md#direct-connect), [接続の種類](../../../services/network-connectivity.md#dx-connections), [VIF の種類](../../../services/network-connectivity.md#dx-vif-types), [Direct Connect ゲートウェイ](../../../services/network-connectivity.md#dx-gateway), [回復性のモデル](../../../services/network-connectivity.md#dx-resiliency)

### 問1 {#q1}

10 Gbps の専用接続を 4 本束ねた LAG で、通常は 25 Gbps を流しています。2 本が故障して残り 20 Gbps では輻輳するので、そのまま使い続けるより別のロケーションの経路へ切り替えたいと考えています。設定として最も適切なものはどれですか。

- A. `minimumLinks` を 1 にして、LAG が動く限り輻輳したまま使い続ける
- B. `minimumLinks` を 3 にして、LAG を止めて切り替える
- C. LAG の本数を 8 本に増やして、輻輳が起きない余裕を確保する
- D. LAG の LACP を無効にして、4 本を別々の VIF で分散する

??? success "答えと解説"
    **正解: B**

    最小リンク数を下回ると LAG 全体が止まり、BGP が別の経路へ切り替えます。

    - A: 誤り。要件と逆の動作。
    - B: 正しい。
    - C: 誤り。100 Gbps 未満は 4 本までで、増やせない。
    - D: 誤り。LAG の前提の LACP を無効にはできない。

    **スキル:** [物理接続](../domain1.md#t1-5-physical) / **参照:** [LAG](../../../services/network-connectivity.md#dx-lag)

### 問2 {#q2}

10 Gbps の DX を同じロケーションで 2 本束ねた LAG があります。監査で「ロケーション障害でも接続を続けること」を求められました。正しい判断はどれですか。

- A. LAG の本数を 4 本に増やして、1 本の障害に耐える構成を強化する
- B. 別のロケーションに接続を追加して、ロケーションの障害に備える
- C. LAG の `minimumLinks` を 1 にして、残りのリンクで動かし続ける
- D. MACsec を有効にして、ロケーションを越えて冗長化する

??? success "答えと解説"
    **正解: B**

    LAG は冗長化の手段ではありません。

    - A: 誤り。同じエンドポイントで終端するので、ロケーションの障害には耐えない。
    - B: 正しい。
    - C: 誤り。ロケーション全体の障害には効かない。
    - D: 誤り。暗号化の機能で冗長化にならない。

    **スキル:** [物理接続](../domain1.md#t1-5-physical) / **参照:** [LAG](../../../services/network-connectivity.md#dx-lag), [回復性のモデル](../../../services/network-connectivity.md#dx-resiliency)

### 問3 {#q3}

新しく 100 Gbps の DX の専用接続を発注します。ルーターの光モジュールの選定と、VIF の設計を確認しています。正しい組み合わせはどれですか。

- A. 銅線の 100GBASE-CR4 と 802.1Q の VLAN
- B. シングルモードファイバーの 100GBASE-LR4 と 802.1Q の VLAN
- C. シングルモードファイバーの 100GBASE-LR4 と QinQ の二重タグ
- D. マルチモードファイバーの 100GBASE-SR4 と 802.1Q の VLAN

??? success "答えと解説"
    **正解: B**

    光の規格と 802.1Q を確認します。

    - A: 誤り。DX に銅線の接続はない。
    - B: 正しい。
    - C: 誤り。VIF の VLAN は 802.1Q。
    - D: 誤り。DX の接続はシングルモードファイバー。

    **スキル:** [物理接続](../domain1.md#t1-5-physical) / **参照:** [接続の種類](../../../services/network-connectivity.md#dx-connections), [MTU とジャンボフレーム](../../../services/network-connectivity.md#mtu)

### 問4 {#q4}

新しい専用接続で、ポートの状態は down です。LOA-CFA をコロケーション事業者に渡してクロスコネクトも終わりました。最初に確認すべき層はどれですか。

- A. L1。ファイバーの種類、光モジュール、オートネゴシエーション
- B. L2。VLAN のタグと VIF の一致を確認する
- C. L3。BGP の ASN と MD5 のキーの一致を確認する
- D. アプリ。EC2 の SG と NACL の許可を確認する

??? success "答えと解説"
    **正解: A**

    接続が down は物理層の症状です。

    - A: 正しい。
    - B: 誤り。接続が up のあとで確認する項目。
    - C: 誤り。接続が down なら BGP の前の段階。
    - D: 誤り。物理の次の次の段階。

    **スキル:** [物理接続](../domain2.md#t2-1-physical) / **参照:** [接続の種類](../../../services/network-connectivity.md#dx-connections)

### 問5 {#q5}

新しい DX で、接続は up なのにプライベート VIF が down のままです。BGP はまだ確立していません。ルーターの設定を確認します。最初に疑うのはどれですか。

- A. VPC のルートテーブルで伝播を有効にしていない
- B. VIF の MTU を 9001 にしていない
- C. ルーターの VLAN が VIF の VLAN と一致していない
- D. ルーターの光モジュールが 1000BASE-LX ではなく 10GBASE-LR である

??? success "答えと解説"
    **正解: C**

    L2 の設定を確認します。ASN や MD5 はその次です。

    - A: 誤り。VIF の状態には関係しない。
    - B: 誤り。既定の 1500 でも VIF は up になる。
    - C: 正しい。
    - D: 誤り。接続が up なので物理は通っている。

    **スキル:** [物理接続](../domain2.md#t2-1-physical) / **参照:** [VIF の種類](../../../services/network-connectivity.md#dx-vif-types)

### 問6 {#q6}

データセンターの移転で DX の専用接続を発注しましたが、配線の工事は 4 か月後です。その間の費用も見積もっています。開通の手順と課金について、正しいものはどれですか。

- A. 接続の要求の承認は常に 1 時間以内に完了し、当日中に VIF を作成できる
- B. LOA の発行から 90 日で、ポートが有効でなくても課金が始まる
- C. クロスコネクトはコンソールから CloudFormation で発注でき、事業者への連絡は不要である
- D. ポートの課金は VIF を最初に作成したときから始まり、VIF がない間は無料である

??? success "答えと解説"
    **正解: B**

    発注から開通までの時間も計画します。

    - A: 誤り。審査とポート割り当てに最大 72 営業時間かかる。
    - B: 正しい。
    - C: 誤り。クロスコネクトは事業者に発注する。
    - D: 誤り。ポートが有効になる、または LOA の発行から 90 日で始まる。

    **スキル:** [物理接続](../domain2.md#t2-1-physical) / **参照:** [接続の種類](../../../services/network-connectivity.md#dx-connections)

### 問7 {#q7}

重要な業務で 99.99% の可用性が必要です。コストより可用性を優先します。DX の接続の構成として公式のモデルに合うものはどれですか。

- A. 1 つのロケーションに 2 接続を別のデバイスで終端する
- B. 2 つのロケーションに各 1 接続を置き、VPN は使わない
- C. 1 つのロケーションに 4 接続を LAG で束ね、同じデバイスで終端する
- D. 2 つのロケーションに各 2 接続を、別々のデバイスで終端する

??? success "答えと解説"
    **正解: D**

    Maximum の構成です。

    - A: 誤り。開発やテスト向けのモデル。
    - B: 誤り。99.9% のモデル。
    - C: 誤り。ロケーションとデバイスの障害に耐えられない。
    - D: 正しい。

    **スキル:** [冗長な接続](../domain1.md#t1-5-redundancy) / **参照:** [回復性のモデル](../../../services/network-connectivity.md#dx-resiliency)

### 問8 {#q8}

10 Gbps の DX の従の経路として VPN を入れます。切り替えたあと、大きなファイルの転送が止まりました。また平常時も一部の経路が VPN へ流れていました。設計の見直しとして正しいものを選んでください。（2つ選択）

- A. DX の VIF の MTU を 1500 より小さくして、VPN と合わせる
- B. VPN のトンネルを 1 本だけ設定して、平常時の誤った経路を避ける
- C. VPN の経路の MTU が小さくなることを前提に MSS を調整する
- D. Transit Gateway の VPN を静的ルートにして、DX を優先する
- E. VPN の広告を DX より具体的にしない

??? success "答えと解説"
    **正解: C, E**

    プレフィックス長は最も強く、VPN の実効 MTU は小さくなります。

    - A: 誤り。VIF の MTU は 1500 か 8500 か 9001 で、その値にはできない。
    - B: 誤り。両方を設定する。冗長性も下がる。
    - C: 正しい。
    - D: 誤り。静的ルートは DX の伝播に勝ってしまう。
    - E: 正しい。

    **スキル:** [冗長な接続](../domain1.md#t1-5-redundancy) / **参照:** [例 4: DX を主、VPN を従にする](../../../services/network-connectivity.md#bgp-dx-vpn), [トンネル](../../../services/network-connectivity.md#vpn-tunnels)

### 問9 {#q9}

監査のため、VIF の BGP を止めたときの切り替えを確かめます。本番のルーターの設定は変更せず、テストの時間も指定して自動で戻します。AWS の機能として最も適切なものはどれですか。

- A. Traffic Mirroring で BGP のパケットを複製して別のピアへ送る
- B. Reachability Analyzer で VIF を除外して分析する
- C. CloudWatch のアラームを `ALARM` に手で変更する
- D. Direct Connect のフェイルオーバーテストで BGP を止める

??? success "答えと解説"
    **正解: D**

    指定した時間だけ BGP を止めます。

    - A: 誤り。BGP を止めるテストにならない。
    - B: 誤り。パケットを送らない解析で、BGP も止まらない。
    - C: 誤り。BGP のセッションは変わらない。
    - D: 正しい。

    **スキル:** [冗長な接続](../domain1.md#t1-5-redundancy) / **参照:** [回復性のモデル](../../../services/network-connectivity.md#dx-resiliency)

### 問10 {#q10}

Transit Gateway と DX ゲートウェイをトランジット VIF で接続しています。新しい VPC を Transit Gateway に追加しましたが、その CIDR がオンプレミスのルーターに届きません。VPC からオンプレミスへの経路は問題ありません。最も可能性の高い原因はどれですか。

- A. VIF の VLAN が変わり、BGP のセッションが再確立されていない
- B. 新しい VPC の SG が BGP の TCP 179 を拒否している
- C. VPC のルートテーブルに DX ゲートウェイへのルートがない
- D. DX ゲートウェイの許可プレフィックスに、新しい CIDR が含まれていない

??? success "答えと解説"
    **正解: D**

    Transit Gateway の場合、許可プレフィックスの値だけがオンプレミスへ広告されます。

    - A: 誤り。VPC の追加で VLAN は変わらない。
    - B: 誤り。BGP は VPC の SG を通らない。
    - C: 誤り。オンプレミスへの広告の問題で、VPC のルートではない。
    - D: 正しい。

    **スキル:** [接続方式の運用](../domain3.md#t3-1-connectivity) / **参照:** [Direct Connect ゲートウェイ](../../../services/network-connectivity.md#dx-gateway), [DX の VIF](../../../services/network-connectivity.md#choosing-vif)

### 問11 {#q11}

DX ゲートウェイに VGW と Transit Gateway の両方を関連付けようとしています。運用の説明として正しいものはどれですか。

- A. DX ゲートウェイはリージョンのリソースで、リージョンごとに 1 つ必要になる
- B. 1 つの DX ゲートウェイに両方を関連付け、許可プレフィックスで振り分ける
- C. VGW 系と Transit Gateway 系ではゲートウェイを分ける
- D. VGW を DX ゲートウェイに関連付けると、VGW の VPC 同士が通信できるようになる

??? success "答えと解説"
    **正解: C**

    DX ゲートウェイの種類に合わせて分けて運用します。

    - A: 誤り。DX ゲートウェイはグローバル。
    - B: 誤り。VGW が関連付いた DX ゲートウェイは Transit Gateway へ接続できない。
    - C: 正しい。
    - D: 誤り。関連付け同士は原則として通信しない。

    **スキル:** [接続方式の運用](../domain3.md#t3-1-connectivity) / **参照:** [Direct Connect ゲートウェイ](../../../services/network-connectivity.md#dx-gateway)

### 問12 {#q12}

DX ゲートウェイに関連付けた 2 つの VGW の VPC が、互いに通信できるようになってしまいました。設計では通信できないはずです。オンプレミスのルーターの広告を確認したところ、`10.0.0.0/8` のスーパーネットを同じ VIF で広告していました。原因はどれですか。

- A. VPC ピアリングが自動で作成された。ピアリングを削除すれば通信は止まる
- B. VIF の種類が公開 VIF で、すべての経路が AWS 内に広がっている
- C. DX ゲートウェイの既定で VGW 同士が常に通信できるので、関連付けを解除する必要がある
- D. VPC を含むスーパーネットを広告し、VPC 間で経路ができた

??? success "答えと解説"
    **正解: D**

    関連付け同士は原則として通信しませんが、このようなスーパーネットは例外になります。

    - A: 誤り。ピアリングは作られない。
    - B: 誤り。公開 VIF は VPC に接続しない。
    - C: 誤り。原則として通信しない。
    - D: 正しい。

    **スキル:** [接続方式の運用](../domain3.md#t3-1-connectivity) / **参照:** [Direct Connect ゲートウェイ](../../../services/network-connectivity.md#dx-gateway), [VIF の種類](../../../services/network-connectivity.md#dx-vif-types)

### 問13 {#q13}

小規模な拠点が 40 か所あり、各拠点の帯域は 50 Mbps 程度です。VPN の接続の費用を抑えたいと考えています。AWS 側は Transit Gateway です。最も適切な選択はどれですか。

- A. Client VPN を拠点のルーターに設定して接続する
- B. VPN Concentrator で多数の拠点を 1 つにまとめる
- C. 拠点ごとに Large Bandwidth Tunnel の VPN を使う
- D. 拠点ごとに DX の専用接続を発注する

??? success "答えと解説"
    **正解: B**

    25 拠点以上で各 100 Mbps 未満の条件に合います。

    - A: 誤り。利用者の端末向けの仕組み。
    - B: 正しい。
    - C: 誤り。帯域が過剰で費用も増える。
    - D: 誤り。費用が大きく、小規模な拠点に合わない。

    **スキル:** [要件の特定](../domain1.md#t1-5-requirements) / **参照:** [オンプレミスとの接続](../../../services/network-connectivity.md#choosing-hybrid)

### 問14 {#q14}

日本と米国の DX ロケーションにそれぞれ拠点があり、拠点間の通信もリージョンを経由せず AWS のネットワークで結びたいと考えています。最も適切な機能はどれですか。

- A. Global Accelerator のカスタムルーティング
- B. 公開 VIF と S3 Transfer Acceleration
- C. Transit Gateway ピアリング
- D. DX の SiteLink を VIF で有効にする

??? success "答えと解説"
    **正解: D**

    SiteLink は DX ロケーションの間を結びます。

    - A: 誤り。拠点間の DX の通信の機能ではない。
    - B: 誤り。拠点間の通信の機能ではない。
    - C: 誤り。リージョンを経由する構成になる。
    - D: 正しい。

    **スキル:** [要件の特定](../domain1.md#t1-5-requirements) / **参照:** [オンプレミスとの接続](../../../services/network-connectivity.md#choosing-hybrid), [SiteLink](../../../services/network-connectivity.md#dx-sitelink)

### 問15 {#q15}

1 つの DX で次の要件があります。(1) 東京の 150 個の VPC へ接続する。(2) S3 の公開エンドポイントに公開 IP で接続する。VIF の組み合わせとして最も適切なものはどれですか。

- A. トランジット VIF で多数の VPC へ、公開 VIF で S3 へ接続する
- B. 公開 VIF のみ。VPC へも公開 VIF で接続する
- C. トランジット VIF のみ。S3 の公開 IP もトランジット VIF で広告される
- D. プライベート VIF 150 本と公開 VIF

??? success "答えと解説"
    **正解: A**

    多数の VPC はトランジット VIF、公開エンドポイントは公開 VIF です。

    - A: 正しい。
    - B: 誤り。公開 VIF は VPC に接続しない。
    - C: 誤り。トランジット VIF では S3 の公開 IP へ届かない。
    - D: 誤り。VIF の数が過大で、運用が困難。

    **スキル:** [要件の特定](../domain1.md#t1-5-requirements) / **参照:** [DX の VIF](../../../services/network-connectivity.md#choosing-vif)

### 問16 {#q16}

オンプレミスの `10.1.0.0/24` から `10.1.255.0/24` までを 1 つずつ VPN の BGP で VGW へ広告する計画です。経路の上限に注意しています。最も適切な対応はどれですか。

- A. VGW の代わりに Client VPN を使って経路を減らす
- B. 経路ごとに別の VPN 接続を作成して上限を分散する
- C. `10.1.0.0/16` にまとめて広告して経路を減らす
- D. 全経路の広告を維持して、VGW の上限の引き上げを申請する

??? success "答えと解説"
    **正解: C**

    256 経路を 1 経路に集約します。

    - A: 誤り。拠点の接続の仕組みではない。
    - B: 誤り。管理が困難で、費用も大きくなる。
    - C: 正しい。
    - D: 誤り。上限は 100 で、この規模の前提にならない。

    **スキル:** [既存のネットワーク](../domain2.md#t2-1-onprem) / **参照:** [経路数の上限に当たったとき](../../../services/network-connectivity.md#bgp-route-limits)

### 問17 {#q17}

既存の企業ネットワークに Site-to-Site VPN を追加します。ファイアウォールで許可すべき通信を決めます。CGW は NAT の背後にあります。BGP を使います。正しい組み合わせはどれですか。

- A. IKE の UDP 53、ESP の UDP 443、トンネル内の BGP の TCP 80
- B. IKE の UDP 500、NAT-T の UDP 4500、トンネル内の BGP の TCP 179
- C. IKE の TCP 500、NAT-T の TCP 4500、トンネル内の BGP の UDP 179
- D. GRE の IP 47、VXLAN の UDP 4789、トンネル内の BGP の TCP 179

??? success "答えと解説"
    **正解: B**

    CGW のファイアウォールで開ける通信です。

    - A: 誤り。ポートが異なる。
    - B: 正しい。
    - C: 誤り。プロトコルが異なる。
    - D: 誤り。AWS の VPN は GRE と VXLAN を使わない。

    **スキル:** [既存のネットワーク](../domain2.md#t2-1-onprem) / **参照:** [MTU と MSS](../../../services/network-connectivity.md#vpn-mtu), [トンネル](../../../services/network-connectivity.md#vpn-tunnels)

### 問18 {#q18}

既存のオンプレミスの `192.168.0.0/16` と AWS の VPC を接続します。接続の前の確認項目として不要なものはどれですか。

- A. 既存の CIDR が VPC の CIDR と重複しないこと
- B. CGW で MSS を調整できること
- C. CGW の機器のシリアル番号を VGW に事前登録すること
- D. 経路の数が上限の 100 に収まること

??? success "答えと解説"
    **正解: C**

    既存のネットワークとの接続では、CIDR、経路の数、MTU を確認します。

    - A: 誤り。重複は通信できない原因になるので必要。
    - B: 誤り。VPN では MTU が小さくなるので必要。
    - C: 正しい。登録する情報に含まれないので、不要。
    - D: 誤り。超えるとセッションに影響するので必要。

    **スキル:** [既存のネットワーク](../domain2.md#t2-1-onprem) / **参照:** [MTU と MSS](../../../services/network-connectivity.md#vpn-mtu), [VPC の CIDR](../../../services/network-connectivity.md#vpc-cidr)

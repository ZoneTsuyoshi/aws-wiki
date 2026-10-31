# ネットワークの問題集

対象の解説: [ネットワークと配信](../../../services/networking.md)、[ネットワーク接続](../../../services/network-connectivity.md)

### 問1 {#q1}

ゲームの UDP の通信を、世界中の利用者から AWS のネットワークに早く乗せます。キャッシュはしません。どれを選びますか。

- A. S3 Transfer Acceleration を使う
- B. CloudFront
- C. Global Accelerator
- D. API Gateway のエッジ最適化を使う

??? success "答えと解説"
    **正解: C**

    TCP と UDP を固定 IP で運びます。

    - A: 誤り。S3 へのアップロードの機能。
    - B: 誤り。HTTP のキャッシュの機能で、UDP を扱えない。
    - C: 正しい。
    - D: 誤り。HTTP の API が対象。

    **スキル:** [エッジネットワーキング](../domain3.md#t3-4-edge) / **参照:** [Global Accelerator](../../../services/network-connectivity.md#global-accelerator)

### 問2 {#q2}

静的コンテンツと API を同じドメインで高速化します。キャッシュでオリジンの負荷も減らします。どれを選びますか。

- A. Route 53
- B. CloudFront
- C. Global Accelerator の TCP リスナー
- D. NLB のクロスゾーンの有効化

??? success "答えと解説"
    **正解: B**

    CloudFront はビヘイビアでパスごとにキャッシュを分けられます。

    - A: 誤り。名前解決で、高速化しない。
    - B: 正しい。
    - C: 誤り。キャッシュしない。
    - D: 誤り。エッジのキャッシュではない。

    **スキル:** [エッジネットワーキング](../domain3.md#t3-4-edge) / **参照:** [CloudFront](../../../services/networking.md#cloudfront)

### 問3 {#q3}

キャッシュのヒット率が低いです。CloudFront のキャッシュキーに全ヘッダーと全 Cookie を含めています。どう改善しますか。

- A. キャッシュキーを必要なものだけにする
- B. オリジンを増やして、リクエストを分散させる
- C. TTL を 0 に設定して、常に最新を取得する
- D. 署名付き URL を全リクエストに必須にする

??? success "答えと解説"
    **正解: A**

    キーを増やすほどキャッシュが分散します。オリジンへ渡すだけならオリジンリクエストポリシーを使います。

    - A: 正しい。
    - B: 誤り。ヒット率は変わらない。
    - C: 誤り。ヒット率がさらに下がる。
    - D: 誤り。キャッシュキーの問題を解決しない。

    **スキル:** [エッジネットワーキング](../domain3.md#t3-4-edge) / **参照:** [キャッシュキーとポリシー](../../../services/networking.md#cache-keys)

### 問4 {#q4}

CloudFront と Global Accelerator の違いで正しいものを選んでください。（2つ選択）

- A. Global Accelerator はエッジで動画を変換して配信する
- B. CloudFront はコンテンツをキャッシュし、Global Accelerator はキャッシュしない
- C. どちらも VPC の中にしか配置できない
- D. Global Accelerator は固定の IPv4 を 2 個提供する
- E. CloudFront は UDP のゲームの通信に使える

??? success "答えと解説"
    **正解: B, D**

    プロトコルとキャッシュと IP で見分けます。

    - A: 誤り。変換もキャッシュもしない。
    - B: 正しい。
    - C: 誤り。どちらもエッジのサービス。
    - D: 正しい。
    - E: 誤り。HTTP と HTTPS が対象。

    **スキル:** [エッジネットワーキング](../domain3.md#t3-4-edge) / **参照:** [Global Accelerator](../../../services/network-connectivity.md#global-accelerator)

### 問5 {#q5}

`10.0.0.0/24` のサブネットで使える IP はいくつですか。

- A. 256 個（全アドレス）
- B. 64 個
- C. 254 個（ネットワークとブロードキャスト以外）
- D. 251 個

??? success "答えと解説"
    **正解: D**

    `.0`、`.1`、`.2`、`.3`、`.255` は使えません。

    - A: 誤り。AWS が 5 個を予約する。
    - B: 誤り。計算が合わない。
    - C: 誤り。一般的なネットワークの計算で、AWS の予約とは違う。
    - D: 正しい。

    **スキル:** [ネットワークの設計](../domain3.md#t3-4-design) / **参照:** [VPC の基本](../../../services/networking.md#vpc)

### 問6 {#q6}

既存の VPC で IP が足りなくなりました。サブネットを追加するため、最小の変更で範囲を増やします。どうしますか。

- A. VPC を削除して大きな CIDR で作り直す
- B. NAT ゲートウェイを増やす
- C. VPC にセカンダリ CIDR を追加する
- D. Elastic IP を追加する

??? success "答えと解説"
    **正解: C**

    セカンダリ CIDR を足して新しいサブネットを作ります。

    - A: 誤り。影響が大きく、不要。
    - B: 誤り。VPC の IP の範囲は増えない。
    - C: 正しい。
    - D: 誤り。パブリック IP で、VPC の範囲は増えない。

    **スキル:** [ネットワークの設計](../domain3.md#t3-4-design) / **参照:** [VPC の CIDR](../../../services/network-connectivity.md#vpc-cidr)

### 問7 {#q7}

将来、オンプレミスや他の VPC とつなぐ可能性があります。CIDR を選ぶときの注意はどれですか。

- A. パブリック IP の範囲を VPC に割り当てる
- B. オンプレミスや他の VPC と重複しない範囲を選ぶ
- C. すべての VPC を `10.0.0.0/16` に揃えて管理を簡単にする
- D. サブネットは最小の `/28` だけで作る

??? success "答えと解説"
    **正解: B**

    ピアリングは一部でも重複すると作れません。組織の IP の管理には IPAM を使います。

    - A: 誤り。重複しない内部の範囲を選ぶのが基本。
    - B: 正しい。
    - C: 誤り。重複すると接続できない。
    - D: 誤り。Lambda や ALB の増加を見込めない。

    **スキル:** [ネットワークの設計](../domain3.md#t3-4-design) / **参照:** [VPC の CIDR](../../../services/network-connectivity.md#vpc-cidr)、[IPAM](../../../services/network-connectivity.md#ipam)

### 問8 {#q8}

IPv6 のインスタンスから外への通信だけを許可し、外からの接続は受けません。何を使いますか。

- A. インターネットゲートウェイに拒否のルールを追加
- B. NAT ゲートウェイをそのまま IPv6 に使う
- C. VPC ピアリングの IPv6 の有効化
- D. Egress-only インターネットゲートウェイ

??? success "答えと解説"
    **正解: D**

    Egress-only は IPv6 の外向きだけを通します。

    - A: 誤り。インターネットゲートウェイにルールはない。
    - B: 誤り。IPv6 の外向きの専用の部品がある。
    - C: 誤り。別の VPC との接続。
    - D: 正しい。

    **スキル:** [ネットワークの設計](../domain3.md#t3-4-design) / **参照:** [IPv6 と Egress-only インターネットゲートウェイ](../../../services/network-connectivity.md#ipv6)

### 問9 {#q9}

50 の VPC とオンプレミスの Direct Connect をつなぎ、さらに増えます。どのトポロジーですか。

- A. Transit Gateway のハブアンドスポーク
- B. すべての VPC を VPC ピアリングで網目につなぐ
- C. 各 VPC に Site-to-Site VPN を別々に設定する
- D. 1 つの VPC に全アカウントのリソースを詰め込む

??? success "答えと解説"
    **正解: A**

    Transit Gateway は多数の VPC と VPN、Direct Connect を集約します。

    - A: 正しい。
    - B: 誤り。管理できず、推移的なルーティングもない。
    - C: 誤り。管理が増える。
    - D: 誤り。分離の利点を失う。

    **スキル:** [ネットワークトポロジー](../domain3.md#t3-4-topology) / **参照:** [Transit Gateway](../../../services/network-connectivity.md#transit-gateway)

### 問10 {#q10}

東京と大阪の Transit Gateway をつないで、リージョンをまたぐ通信を流します。どの機能ですか。

- A. Transit Gateway のピアリング
- B. Route 53 のフェイルオーバー
- C. VPC ピアリングを Transit Gateway に設定する
- D. PrivateLink のサービスを作って公開する

??? success "答えと解説"
    **正解: A**

    ピアリングアタッチメントで複数のリージョンをつなぎます。

    - A: 正しい。
    - B: 誤り。DNS の切り替え。
    - C: 誤り。同じ機能ではない。
    - D: 誤り。1 つのサービスの公開。

    **スキル:** [ネットワークトポロジー](../domain3.md#t3-4-topology) / **参照:** [ピアリング](../../../services/network-connectivity.md#tgw-peering)

### 問11 {#q11}

オンプレミスの DNS で VPC のプライベートホストゾーンの名前を解決します。VPC からもオンプレミスの名前を解決します。どう構成しますか。（2つ選択）

- A. Route 53 Resolver のインバウンドエンドポイント
- B. パブリックホストゾーンに内部の名前をすべて登録する
- C. CloudFront の代替ドメイン名で内部の名前を解決する
- D. DHCP オプションセットを VPC ごとに外部 DNS だけに変更する
- E. Route 53 Resolver のアウトバウンドエンドポイント

??? success "答えと解説"
    **正解: A, E**

    インバウンドはオンプレミスから VPC へ、アウトバウンドは VPC からオンプレミスへの問い合わせです。

    - A: 正しい。
    - B: 誤り。内部の名前を公開することになる。
    - C: 誤り。配信の機能。
    - D: 誤り。VPC の名前の解決ができなくなる。
    - E: 正しい。

    **スキル:** [ネットワークトポロジー](../domain3.md#t3-4-topology) / **参照:** [エンドポイント](../../../services/network-connectivity.md#resolver-endpoints)、[ハイブリッド DNS](../../../services/network-connectivity.md#hybrid-dns)

### 問12 {#q12}

既存の Direct Connect を使い、1 Gbps を安定して確保します。パートナーの提供する 500 Mbps は足りません。どの接続を選びますか。

- A. Direct Connect のホスト接続の 50 Mbps
- B. PrivateLink のエンドポイント
- C. Direct Connect の 1 Gbps の専用接続
- D. Site-to-Site VPN 1 本

??? success "答えと解説"
    **正解: C**

    専用接続は 1、10、100、400 Gbps です。開通に時間がかかります。

    - A: 誤り。足りない。
    - B: 誤り。サービスの公開で、拠点の接続ではない。
    - C: 正しい。
    - D: 誤り。インターネット経由で安定しない。

    **スキル:** [ネットワーク接続の選択肢](../domain3.md#t3-4-connections) / **参照:** [接続の種類](../../../services/network-connectivity.md#dx-connections)

### 問13 {#q13}

取引先の VPC に、自社の 1 つのサービスだけを公開します。お互いの CIDR は重複しています。どれを選びますか。

- A. Transit Gateway のアタッチメント
- B. PrivateLink
- C. Site-to-Site VPN
- D. VPC ピアリング

??? success "答えと解説"
    **正解: B**

    PrivateLink は 1 つのサービスだけを公開します。CIDR が重複してもかまいません。

    - A: 誤り。重複したルーティングの問題が残る。
    - B: 正しい。
    - C: 誤り。CIDR の重複の問題が残る。
    - D: 誤り。CIDR が重複すると作れない。

    **スキル:** [ネットワーク接続の選択肢](../domain3.md#t3-4-connections) / **参照:** [VPC エンドポイントと PrivateLink](../../../services/networking.md#vpc-endpoints)

### 問14 {#q14}

標準の Site-to-Site VPN のトンネル 1 本の帯域の目安はどれですか。

- A. 100 Mbps
- B. 100 Gbps
- C. 10 Gbps
- D. 1.25 Gbps

??? success "答えと解説"
    **正解: D**

    足りなければ Transit Gateway の ECMP で束ねます。

    - A: 誤り。目安より小さい。
    - B: 誤り。専用接続の値。
    - C: 誤り。大きすぎる。Large Bandwidth Tunnel は 5 Gbps。
    - D: 正しい。

    **スキル:** [ネットワーク接続の選択肢](../domain3.md#t3-4-connections) / **参照:** [トンネル](../../../services/network-connectivity.md#vpn-tunnels)

### 問15 {#q15}

インターネットから受ける Web アプリのリソースの配置として適切なものはどれですか。

- A. ALB、アプリ、DB をパブリックに配置
- B. ALB をプライベート、アプリをパブリックに配置
- C. ALB をパブリック、アプリをプライベート、DB を閉域に配置
- D. CloudFront の中に DB を配置

??? success "答えと解説"
    **正解: C**

    DB はパブリックサブネットに置きません。

    - A: 誤り。DB を公開側に置くことになる。
    - B: 誤り。逆。
    - C: 正しい。
    - D: 誤り。CloudFront は DB を置く場所ではない。

    **スキル:** [リソースの配置](../domain3.md#t3-4-placement) / **参照:** [サブネットとルートテーブル](../../../services/networking.md#subnets-route-tables)

### 問16 {#q16}

複数のノードで低遅延の通信を行い、AZ の障害には別の方法で備えます。配置はどれですか。

- A. 同じ AZ のクラスタープレイスメントグループ
- B. 別の AZ に 1 台ずつ配置する構成
- C. Local Zones の各都市に 1 台ずつ配置する構成
- D. 別のリージョンのスプレッドプレイスメントグループ

??? success "答えと解説"
    **正解: A**

    ノード間の性能と可用性はトレードオフです。

    - A: 正しい。
    - B: 誤り。AZ 間の遅延が増える。
    - C: 誤り。ノード間の遅延が増える。
    - D: 誤り。遅延が増える。

    **スキル:** [リソースの配置](../domain3.md#t3-4-placement) / **参照:** [プレイスメントグループ](../../../services/operations.md#placement-groups)

### 問17 {#q17}

規制でデータを自社の施設に置きますが、AWS の API と同じ運用を使います。どこに配置しますか。

- A. CloudFront のエッジロケーション
- B. 東京リージョンの 2 つの AZ
- C. Wavelength
- D. Outposts のラック

??? success "答えと解説"
    **正解: D**

    Outposts は AWS のインフラを自社の施設に置きます。

    - A: 誤り。配信の拠点。
    - B: 誤り。自社の施設ではない。
    - C: 誤り。5G の通信事業者の拠点。
    - D: 正しい。

    **スキル:** [リソースの配置](../domain3.md#t3-4-placement) / **参照:** [Outposts、Local Zones、Wavelength のネットワーク](../../../services/network-connectivity.md#edge-infrastructure)

### 問18 {#q18}

HTTP のパスとホストで振り分け、Lambda と EC2 をターゲットにします。認証も連携します。どれを選びますか。

- A. Global Accelerator
- B. ALB
- C. NLB
- D. GWLB

??? success "答えと解説"
    **正解: B**

    ALB は HTTP の情報で振り分けます。

    - A: 誤り。パスを見ず、ターゲットの振り分けの機能が違う。
    - B: 正しい。
    - C: 誤り。パスを見ない。
    - D: 誤り。ファイアウォール向け。

    **スキル:** [負荷分散の戦略](../domain3.md#t3-4-lb) / **参照:** [ALB と NLB の違い](../../../services/networking.md#alb-vs-nlb)、[ターゲットタイプ](../../../services/networking.md#target-types)

### 問19 {#q19}

第三者の次世代ファイアウォールの仮想アプライアンスを、全通信に透過的に挟みます。どれを選びますか。

- A. Global Accelerator のカスタムルーティング
- B. GWLB
- C. NLB の TCP リスナー
- D. ALB の HTTP のルール

??? success "答えと解説"
    **正解: B**

    GWLB はレイヤー 3 で、GENEVE でアプライアンスに送ります。

    - A: 誤り。用途が違う。
    - B: 正しい。
    - C: 誤り。アプライアンスの透過的な挿入の機能ではない。
    - D: 誤り。HTTP だけで、透過的でない。

    **スキル:** [負荷分散の戦略](../domain3.md#t3-4-lb) / **参照:** [GWLB](../../../services/networking.md#gwlb)

### 問20 {#q20}

NLB でクロスゾーン負荷分散について正しいものはどれですか。

- A. 有効にすると、固定 IP が使えなくなる
- B. ALB と同様に、NLB の既定は常に有効で無効にできない
- C. 既定で無効で、有効にすると AZ 間の通信が発生する
- D. NLB には設定そのものがない

??? success "答えと解説"
    **正解: C**

    ALB ではロードバランサーのレベルで常に有効です。

    - A: 誤り。関係しない。
    - B: 誤り。NLB は既定で無効。
    - C: 正しい。
    - D: 誤り。設定がある。

    **スキル:** [負荷分散の戦略](../domain3.md#t3-4-lb) / **参照:** [クロスゾーン負荷分散](../../../services/networking.md#cross-zone)

### 問21 {#q21}

ALB の後ろのサーバーで、利用者の送信元 IP を記録します。どこから取得しますか。

- A. `X-Forwarded-For` ヘッダー
- B. NLB に変更するしかない
- C. パケットの送信元アドレスをそのまま使う
- D. VPC フローログのリアルタイム API から取得する

??? success "答えと解説"
    **正解: A**

    ALB は `X-Forwarded-For` に送信元の IP を付けます。

    - A: 正しい。
    - B: 誤り。変更の必要はない。
    - C: 誤り。ALB の IP になる。
    - D: 誤り。アプリの中で使う方法ではない。

    **スキル:** [負荷分散の戦略](../domain3.md#t3-4-lb) / **参照:** [ALB と NLB の違い](../../../services/networking.md#alb-vs-nlb)

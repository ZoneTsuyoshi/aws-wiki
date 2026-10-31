# Transit Gateway と SD-WANの問題集

対象の解説: [Transit Gateway](../../../services/network-connectivity.md#transit-gateway), [ルートテーブル](../../../services/network-connectivity.md#tgw-route-tables), [Connect](../../../services/network-connectivity.md#tgw-connect), [マルチキャスト](../../../services/network-connectivity.md#tgw-multicast), [VPC 同士の接続](../../../services/network-connectivity.md#choosing-multi-vpc)

### 問1 {#q1}

SD-WAN の仮想アプライアンスを VPC に置き、Transit Gateway と接続します。VPN より大きな帯域で、BGP に統一します。暗号化はオーバーレイ側で行っています。最も適切な接続はどれですか。

- A. Connect アタッチメント。GRE と BGP でアプライアンスとつなぐ
- B. Accelerated Site-to-Site VPN を 4 本張り、ECMP で束ねる構成
- C. VPC Route Server でアプライアンスの経路を VPC へ反映する構成
- D. VPC ピアリングと静的ルートでアプライアンスへ送る構成

??? success "答えと解説"
    **正解: A**

    Connect は GRE と BGP で SD-WAN のアプライアンスをつなぎます。

    - A: 正しい。
    - B: 誤り。帯域が小さく、IPsec のオーバーヘッドも増える。
    - C: 誤り。Transit Gateway への広告には使わない。
    - D: 誤り。Transit Gateway と BGP でつなぐ構成ではない。

    **スキル:** [SD-WAN とオーバーレイ](../domain1.md#t1-5-sdwan) / **参照:** [Connect](../../../services/network-connectivity.md#tgw-connect)

### 問2 {#q2}

Connect のピア 4 つで最大の帯域を得る計画です。アプライアンスは同じプレフィックスを広告しています。ピアの間で ECMP を使うための条件と、合計帯域の組み合わせはどれですか。

- A. ピアごとに別のプレフィックスを広告する。合計は最大 40 Gbps
- B. 同じ AS_PATH と ASN で広告する。合計は最大 20 Gbps
- C. 異なる ASN を使うと分散が改善する。合計は最大 100 Gbps
- D. MED を異なる値にして重みを付ける。合計は最大 5 Gbps

??? success "答えと解説"
    **正解: B**

    ピアあたり最大 5 Gbps、アタッチメントあたり 4 ピアです。

    - A: 誤り。同じプレフィックスが必要で、帯域の値も違う。
    - B: 正しい。
    - C: 誤り。同じ ASN が必要で、帯域の値も違う。
    - D: 誤り。属性をそろえる必要があり、帯域の値も違う。

    **スキル:** [SD-WAN とオーバーレイ](../domain1.md#t1-5-sdwan) / **参照:** [Connect](../../../services/network-connectivity.md#tgw-connect)

### 問3 {#q3}

SD-WAN のオーバーレイの土台（アンダーレイ）を設計します。データセンターのルーターから直接 Transit Gateway へ Connect を張ります。VPC にアプライアンスは置きません。正しい構成はどれですか。

- A. 公開 VIF の上で GRE を張って土台にする
- B. DX ゲートウェイのアタッチメントを土台にする
- C. ピアリングのアタッチメントを土台にする
- D. VPN のアタッチメントを土台にする

??? success "答えと解説"
    **正解: B**

    土台は VPC か Direct Connect のアタッチメントです。

    - A: 誤り。問題文の構成の土台の種類ではない。
    - B: 正しい。
    - C: 誤り。Connect の土台の種類ではない。
    - D: 誤り。Connect の土台は VPC か DX のアタッチメント。

    **スキル:** [SD-WAN とオーバーレイ](../domain1.md#t1-5-sdwan) / **参照:** [Connect](../../../services/network-connectivity.md#tgw-connect), [アタッチメント](../../../services/network-connectivity.md#tgw-attachments)

### 問4 {#q4}

Connect の実装で、アプライアンスと Transit Gateway の GRE トンネルが上がりません。Transit Gateway の CIDR は `192.0.2.0/24` です。アプライアンスの VPC からの経路を確認しています。必要なものはどれですか。

- A. アプライアンスのサブネットのルートで `192.0.2.0/24` を NAT ゲートウェイへ向ける
- B. Transit Gateway のルートテーブルに `192.0.2.0/24` の静的ルートを追加する
- C. `192.0.2.0/24` を VPC のセカンダリ CIDR に追加する
- D. アプライアンスの VPC のルートテーブルに `192.0.2.0/24 → tgw-` を入れる

??? success "答えと解説"
    **正解: D**

    GRE の外側の宛先は Transit Gateway の CIDR です。

    - A: 誤り。GRE の外側は VPC アタッチメントを通って届く。
    - B: 誤り。必要なのは VPC 側の経路。
    - C: 誤り。Transit Gateway の CIDR は VPC の CIDR とは別のもの。
    - D: 正しい。

    **スキル:** [SD-WAN](../domain2.md#t2-1-sdwan) / **参照:** [Connect](../../../services/network-connectivity.md#tgw-connect)

### 問5 {#q5}

Connect のピアの内部 CIDR を `169.254.6.0/29` にしました。アプライアンスの BGP が確立しません。アプライアンスのアドレスとして正しいものと、eBGP の設定はどれですか。

- A. `169.254.6.0` で、`ebgp-multihop` は使わない
- B. `169.254.6.7` で、BFD を有効にする
- C. `169.254.6.1` で、`ebgp-multihop`（TTL 2）にする
- D. `169.254.6.2` で、`ebgp-multihop`（TTL 2）にする

??? success "答えと解説"
    **正解: C**

    `/29` の最初の使える値がアプライアンスです。

    - A: 誤り。ネットワークアドレスで、TTL 2 も必要。
    - B: 誤り。ブロードキャストの値で、Connect は BFD に対応しない。
    - C: 正しい。
    - D: 誤り。アプライアンスに設定するのは範囲の最初のアドレス。

    **スキル:** [SD-WAN](../domain2.md#t2-1-sdwan) / **参照:** [Connect](../../../services/network-connectivity.md#tgw-connect)

### 問6 {#q6}

SD-WAN のベンダーと Connect の設計を確認しています。ベンダーは静的ルートと BFD を前提にした資料を出してきました。Connect の説明として正しいものを選んでください。（2つ選択）

- A. BFD を使える
- B. Transit Gateway の CIDR の設定は不要である
- C. GRE には暗号化がない
- D. 静的ルートは使えない
- E. ピアあたり最大 100 Gbps である

??? success "答えと解説"
    **正解: C, D**

    Connect の制約です。

    - A: 誤り。非対応。
    - B: 誤り。Transit Gateway の CIDR を設定する。
    - C: 正しい。
    - D: 正しい。
    - E: 誤り。5 Gbps。

    **スキル:** [SD-WAN](../domain2.md#t2-1-sdwan) / **参照:** [Connect](../../../services/network-connectivity.md#tgw-connect), [トンネル](../../../services/network-connectivity.md#vpn-tunnels)

### 問7 {#q7}

新規に 100 個の VPC を接続するハブアンドスポークを設計します。ハブの運用はできるだけ減らします。第三者のルーティング機能の要件はありません。最も適切な構成はどれですか。

- A. EC2 の仮想ルーターをハブの VPC に置くトランジット VPC
- B. VGW に全 VPC を接続して、VPN でハブにする
- C. 全 VPC の間の VPC ピアリングでメッシュを作る
- D. Transit Gateway。マネージドのハブに各 VPC をアタッチする

??? success "答えと解説"
    **正解: D**

    新規の構成は Transit Gateway を優先します。

    - A: 誤り。仮想ルーターの更新と冗長化が必要。
    - B: 誤り。VGW は 1 つの VPC に付く。
    - C: 誤り。本数が多く、推移もできない。
    - D: 正しい。

    **スキル:** [ハブアンドスポーク](../domain2.md#t2-2-hub-spoke) / **参照:** [Transit Gateway](../../../services/network-connectivity.md#transit-gateway)

### 問8 {#q8}

トランジット VPC の既存の構成が残っており、第三者のルーターの機能に依存しています。Transit Gateway へ移行する案との比較で正しいものはどれですか。

- A. Transit Gateway はスポークの VGW から VPN を張る必要がある
- B. トランジット VPC は AWS が仮想ルーターの更新を代行する
- C. Transit Gateway の VPC アタッチメントは AZ あたり最大 1.25 Gbps である
- D. トランジット VPC は帯域が VPN のトンネルとインスタンスに依存する

??? success "答えと解説"
    **正解: D**

    比較の表を確認します。

    - A: 誤り。スポークはアタッチメント。
    - B: 誤り。自分で行う。
    - C: 誤り。最大 100 Gbps。
    - D: 正しい。

    **スキル:** [ハブアンドスポーク](../domain2.md#t2-2-hub-spoke) / **参照:** [Transit Gateway](../../../services/network-connectivity.md#transit-gateway), [アタッチメント](../../../services/network-connectivity.md#tgw-attachments)

### 問9 {#q9}

Transit Gateway の VPC アタッチメントのサブネットを設計します。ベストプラクティスとして最も適切なものはどれですか。

- A. AZ ごとに `/28` の専用サブネットを作る
- B. NACL を最小の許可にして、アタッチメント用のサブネットで制御する
- C. AZ を 1 つだけ指定して経路を単純にする
- D. ワークロードと同じサブネットを共用して IP を節約する

??? success "答えと解説"
    **正解: A**

    AZ ごとに専用の小さなサブネットを使います。

    - A: 正しい。
    - B: 誤り。NACL は開けておき、ワークロード側で制御する。
    - C: 誤り。指定のない AZ のリソースに届かない問題が出る。
    - D: 誤り。専用のサブネットが推奨。

    **スキル:** [ハブアンドスポーク](../domain2.md#t2-2-hub-spoke) / **参照:** [アタッチメント](../../../services/network-connectivity.md#tgw-attachments)

### 問10 {#q10}

第三者のファイアウォールを CGW として Site-to-Site VPN へ接続します。機器はポリシーベースの VPN のみに対応し、複数のトラフィックセレクターを使っています。トンネルが不安定です。正しい理解はどれですか。

- A. CGW の型を VPN Concentrator に指定すると、ポリシーベースも受け付ける
- B. GRE に切り替えると、トラフィックセレクターは自動で統合される
- C. AWS はルートベースなので、トラフィックセレクターの扱いに注意する
- D. AWS はポリシーベースのみに対応するので、機器をルートベースへ変更してはならない

??? success "答えと解説"
    **正解: C**

    第三者の機器との相性を確認します。

    - A: 誤り。別の用途の機能。
    - B: 誤り。別の話。
    - C: 正しい。
    - D: 誤り。AWS はルートベース。

    **スキル:** [第三者製品](../domain2.md#t2-2-third-party) / **参照:** [Site-to-Site VPN](../../../services/network-connectivity.md#site-to-site-vpn)

### 問11 {#q11}

買収した会社の VPN 機器と仮想ファイアウォールを、AWS のネットワークへつなぎます。製品は当面使い続けます。接続の組み合わせとして適切なものを選んでください。（2つ選択）

- A. 第三者の VPN 機器: Site-to-Site VPN の CGW にする
- B. ポリシーベースの VPN 機器: 公開 VIF の上の GRE で接続する
- C. 第三者のファイアウォール: Traffic Mirroring の送信先に置いて遮断する
- D. SD-WAN の仮想アプライアンス: Transit Gateway ピアリングで接続する
- E. 第三者のファイアウォール: GWLB とエンドポイントで挟む

??? success "答えと解説"
    **正解: A, E**

    製品ごとにつなぎ方を選びます。

    - A: 正しい。
    - B: 誤り。AWS の VPN はルートベース。
    - C: 誤り。ミラーはコピーで、遮断はできない。
    - D: 誤り。ピアリングは Transit Gateway 同士の接続で、Connect で GRE と BGP を使う。
    - E: 正しい。

    **スキル:** [第三者製品](../domain2.md#t2-2-third-party) / **参照:** [Site-to-Site VPN](../../../services/network-connectivity.md#site-to-site-vpn), [Firewall Manager](../../../services/threat-detection.md#firewall-manager)

### 問12 {#q12}

第三者のルーターで VPN を初めて設定します。設定の間違いを減らしたいと考えています。AWS の機能として最も適切なものはどれですか。

- A. トンネルログで IKE の失敗を見ながら、値を順に合わせていく
- B. Reachability Analyzer で CGW までの経路を事前に分析する
- C. 機器の種類に合う VPN 接続の設定ファイルをダウンロードする
- D. CGW を作成すると、AWS が機器へ設定を自動で配布する

??? success "答えと解説"
    **正解: C**

    ベンダーごとの設定をダウンロードできます。

    - A: 誤り。調査の手段で、設定の間違いを事前に減らす機能ではない。
    - B: 誤り。オンプレミスの機器の設定は解析の対象外。
    - C: 正しい。
    - D: 誤り。機器へ設定を配布する仕組みはない。

    **スキル:** [第三者製品](../domain2.md#t2-2-third-party) / **参照:** [Site-to-Site VPN](../../../services/network-connectivity.md#site-to-site-vpn)

### 問13 {#q13}

Transit Gateway で本番 VPC と開発 VPC を分け、両方とも共有 VPC と DX へ接続します。本番同士、および開発から本番へは通信させません。ルートテーブルの設計として正しいものはどれですか。

- A. `rt-prod` に本番を関連付け、本番 VPC と開発 VPC を伝播する
- B. `rt-prod` に本番を関連付け、共有 VPC と DX を伝播する
- C. すべてを既定のルートテーブルに関連付け、NACL で止める
- D. `rt-shared` に本番を関連付け、DX だけを伝播する

??? success "答えと解説"
    **正解: B**

    関連付けと伝播を分けます。

    - A: 誤り。本番同士と開発が通信できてしまう。
    - B: 正しい。
    - C: 誤り。既定のままだと全 VPC が通信できる。
    - D: 誤り。共有 VPC へ届かなくなり、分離の表にも合わない。

    **スキル:** [VPC 間の接続](../domain2.md#t2-2-multi-vpc) / **参照:** [ルートテーブル](../../../services/network-connectivity.md#tgw-route-tables)

### 問14 {#q14}

VPC A と B の間でピアリングを作成して承認しました。しかし通信できません。SG は相手の範囲を許可しています。原因として最も可能性の高いものはどれですか。

- A. 両方のルートテーブルに経路がない
- B. ピアリングの推移のルートが必要である
- C. ピアリングは承認から 7 日で失効するので、再作成が必要である
- D. VPC に IGW がない

??? success "答えと解説"
    **正解: A**

    両方に経路を入れます。

    - A: 正しい。
    - B: 誤り。問題文は直接の接続で、推移はできない。
    - C: 誤り。承認されたピアリングは失効しない。7 日は要求の期限。
    - D: 誤り。ピアリングの通信に IGW は不要。

    **スキル:** [VPC 間の接続](../domain2.md#t2-2-multi-vpc) / **参照:** [VPC ピアリング](../../../services/network-connectivity.md#vpc-peering)

### 問15 {#q15}

東京と大阪の Transit Gateway をピアリングで接続しました。BGP を使うつもりでしたが経路が交換されません。正しい設定はどれですか。

- A. 両側で同じ ASN を設定して BGP を有効にする
- B. 両側に、ピアリングのアタッチメントへの静的ルートを追加する
- C. ピアリングのアタッチメントでアプライアンスモードを有効にする
- D. 片側だけに静的ルートを追加して、もう片側は伝播させる

??? success "答えと解説"
    **正解: B**

    ピアリングは静的ルートのみです。

    - A: 誤り。静的のみで、ASN は別々にする。
    - B: 正しい。
    - C: 誤り。経路の交換にならない。
    - D: 誤り。両側に必要。

    **スキル:** [VPC 間の接続](../domain2.md#t2-2-multi-vpc) / **参照:** [ピアリング](../../../services/network-connectivity.md#tgw-peering)

### 問16 {#q16}

NAT ゲートウェイの `ErrorPortAllocation` が増えています。同じ宛先（IP とポート）へ 20 万の同時接続があります。IP は 1 個です。必要な IP の数はどれですか。

- A. 2 個。IP あたりの上限は約 100,000 接続である
- B. 4 個。IP あたりの上限は約 55,000 接続である
- C. 3 個。IP あたりの上限は約 70,000 接続である
- D. 1 個のまま。帯域を増やせば上限も増える

??? success "答えと解説"
    **正解: B**

    `200,000 / 55,000 = 3.6` で 4 個です。

    - A: 誤り。上限は約 55,000 で、2 個では `110,000` 接続まで。
    - B: 正しい。
    - C: 誤り。上限は約 55,000 で、3 個では `165,000` 接続まで。
    - D: 誤り。IP あたりの接続の上限が原因。

    **スキル:** [上限とクォータ](../domain3.md#t3-1-quotas) / **参照:** [既定値と上限のまとめ](../../../services/network-connectivity.md#numbers), [NAT ゲートウェイ](../../../services/network-connectivity.md#nat-gateway)

### 問17 {#q17}

オンプレミスから VIF へ広告する経路が上限を超える場合の動作と、VPC の伝播の上限について正しいものを選んでください。（2つ選択）

- A. VPC の伝播ルートは 100 で変更できない
- B. VIF の受信経路が上限を超えると BGP が `idle` になり全経路が消える
- C. 公開 VIF の受信経路の上限は 100 である
- D. VIF の上限を超えた経路だけが捨てられ、残りは通常どおり動く
- E. Transit Gateway からトランジット VIF への広告は無制限である

??? success "答えと解説"
    **正解: A, B**

    上限の超過の影響は大きいです。

    - A: 正しい。
    - B: 正しい。
    - C: 誤り。公開 VIF は 1,000。
    - D: 誤り。全経路が消える。
    - E: 誤り。合計 200。

    **スキル:** [上限とクォータ](../domain3.md#t3-1-quotas) / **参照:** [経路数の上限に当たったとき](../../../services/network-connectivity.md#bgp-route-limits)

### 問18 {#q18}

設計書で各接続の帯域の上限を確認しています。VPN は標準のトンネルです。VPN、Connect、VPC アタッチメントの値の組み合わせで正しいものはどれですか。

- A. VPN トンネル 1.25 Gbps、Connect ピア 1.25 Gbps、VPC アタッチメント AZ あたり 1.25 Gbps
- B. VPN トンネル 10 Gbps、Connect ピア 1.25 Gbps、VPC アタッチメント AZ あたり 5 Gbps
- C. VPN トンネル 1.25 Gbps、Connect ピア 5 Gbps、VPC アタッチメント AZ あたり 100 Gbps
- D. VPN トンネル 5 Gbps（標準）、Connect ピア 20 Gbps、VPC アタッチメント AZ あたり 50 Gbps

??? success "答えと解説"
    **正解: C**

    上限の値を覚えます。

    - A: 誤り。Connect と VPC の値が違う。
    - B: 誤り。値が異なる。
    - C: 正しい。
    - D: 誤り。標準は 1.25 Gbps で、ピアの値も違う。

    **スキル:** [上限とクォータ](../domain3.md#t3-1-quotas) / **参照:** [トンネル](../../../services/network-connectivity.md#vpn-tunnels), [Connect](../../../services/network-connectivity.md#tgw-connect)

### 問19 {#q19}

10 リージョンの VPC を、動的な経路と 1 つのポリシーで統一して接続します。リージョン間の経路を自動で扱いたいと考えています。最も適切な構成はどれですか。

- A. リージョン間の VPC ピアリングのフルメッシュ
- B. AWS Cloud WAN のコアネットワークと 1 つのポリシー
- C. 各リージョンの Transit Gateway を VPN の BGP でメッシュにする
- D. Transit Gateway ピアリングのメッシュと手動の静的ルート

??? success "答えと解説"
    **正解: B**

    Cloud WAN はポリシーでネットワークを統一します。

    - A: 誤り。本数が多く、推移もできない。
    - B: 正しい。
    - C: 誤り。動作はするが、VPN の帯域と運用が増え、1 つのポリシーにもならない。
    - D: 誤り。静的ルートの運用の手間が大きい。

    **スキル:** [通信パターン](../domain3.md#t3-1-patterns) / **参照:** [ピアリング](../../../services/network-connectivity.md#tgw-peering), [Cloud WAN](../../../services/network-connectivity.md#cloud-wan)

### 問20 {#q20}

大きなフレームを使うアプリを、東京の VPC と大阪の VPC に分けて配置します。リージョン内とリージョン間の接続の MTU と暗号化についての説明で正しいものはどれですか。

- A. 同じリージョンの Transit Gateway は 9001 MTU である
- B. リージョン間の VPC ピアリングは 8500 MTU で、暗号化もされる
- C. 同じリージョンの VPC ピアリングは 8500 MTU である
- D. Transit Gateway ピアリングは暗号化されないので、必ず VPN を重ねる

??? success "答えと解説"
    **正解: B**

    値の違いを覚えます。

    - A: 誤り。8500。
    - B: 正しい。
    - C: 誤り。9001。
    - D: 誤り。AES-256 で暗号化される。

    **スキル:** [通信パターン](../domain3.md#t3-1-patterns) / **参照:** [VPC ピアリング](../../../services/network-connectivity.md#vpc-peering), [ピアリング](../../../services/network-connectivity.md#tgw-peering)

### 問21 {#q21}

本社と支社の DX ロケーションの間の通信が、今はリージョンを経由していて遅延が大きいです。AWS のネットワークの最短経路へ変えます。最も適切な方法はどれですか。

- A. VIF で SiteLink を有効にする
- B. Transit Gateway のピアリングを追加する
- C. VPN のアクセラレーションを有効にする
- D. Global Accelerator を拠点間に置く

??? success "答えと解説"
    **正解: A**

    SiteLink はリージョンを経由しません。

    - A: 正しい。
    - B: 誤り。リージョンを経由する。
    - C: 誤り。インターネットからの VPN の改善で、拠点間の最短経路ではない。
    - D: 誤り。拠点間の DX の機能ではない。

    **スキル:** [通信パターン](../domain3.md#t3-1-patterns) / **参照:** [SiteLink](../../../services/network-connectivity.md#dx-sitelink)

### 問22 {#q22}

同じリージョンの 2 つの VPC の間で大量のデータを転送し、費用と MTU を優先します。他の VPC との接続の要件はありません。最も適切なものはどれですか。

- A. PrivateLink。NLB の背後のサービス単位で接続する
- B. VPC ピアリング。処理料金がなく、MTU も 9001 まで使える
- C. Cloud WAN。コアネットワークの 1 つのセグメントで接続する
- D. Transit Gateway。ルートテーブルで 2 つの VPC を接続する

??? success "答えと解説"
    **正解: B**

    少数の VPC で大量の転送にはピアリングです。

    - A: 誤り。特定のサービスのみ。
    - B: 正しい。
    - C: 誤り。この規模には過剰。
    - D: 誤り。時間と処理の料金がかかり、MTU も 8500。

    **スキル:** [ピアリング、プロキシ、Transit Gateway](../domain3.md#t3-3-peer-vs-tgw) / **参照:** [VPC 同士の接続](../../../services/network-connectivity.md#choosing-multi-vpc)

### 問23 {#q23}

VPC ピアリングから Transit Gateway へ移行します。移行中に大きなパケットだけが消えました。片方の VPC だけ Transit Gateway へ切り替えた状態です。原因はどれですか。

- A. ピアリングの先の SG の参照が残り、大きなパケットだけが拒否される
- B. ピアリングのルートが残っていると、Transit Gateway の暗号化が失敗する
- C. MTU が 9001 から 8500 に下がり、非対称な経路で大きなパケットが落ちる
- D. Transit Gateway は MTU が 1500 に固定されている

??? success "答えと解説"
    **正解: C**

    両方の VPC を同時に切り替えます。

    - A: 誤り。SG はパケットのサイズで判定しない。
    - B: 誤り。同じリージョンの Transit Gateway の暗号化の話ではない。
    - C: 正しい。
    - D: 誤り。8500。

    **スキル:** [ピアリング、プロキシ、Transit Gateway](../domain3.md#t3-3-peer-vs-tgw) / **参照:** [VPC ピアリング](../../../services/network-connectivity.md#vpc-peering), [MTU とジャンボフレーム](../../../services/network-connectivity.md#mtu)

### 問24 {#q24}

外向きの HTTP を中央で検査します。要件は「URL で許可し、利用者を認証する」ことです。EC2 の運用は許容します。最も適切なパターンはどれですか。

- A. NLB の背後の EC2 に Squid のプロキシを置き、URL と利用者を判定する
- B. Network Firewall のステートフルルールだけで URL の認証も行う
- C. 各 VPC の NAT ゲートウェイに、送信先の許可リストを設定する
- D. DNS Firewall の許可リストで、利用者ごとに URL を判定する

??? success "答えと解説"
    **正解: A**

    URL と認証はプロキシの要件です。透過的な検査は Network Firewall です。

    - A: 正しい。
    - B: 誤り。利用者の認証はできない。
    - C: 誤り。NAT ゲートウェイに URL の判定や認証の機能はない。
    - D: 誤り。判定はドメインのみで、利用者の認証もない。

    **スキル:** [ピアリング、プロキシ、Transit Gateway](../domain3.md#t3-3-peer-vs-tgw) / **参照:** [Network Firewall](../../../services/network-connectivity.md#network-firewall), [VPC 同士の接続](../../../services/network-connectivity.md#choosing-multi-vpc)

### 問25 {#q25}

VPC 内で市場データをマルチキャストで配信します。既存の Transit Gateway はマルチキャストを有効にしていません。実装として正しいものはどれですか。

- A. 既存の Transit Gateway を更新してマルチキャストを有効にする
- B. ピアリングの設定でマルチキャストを有効にする
- C. `MulticastSupport=enable` で新しい Transit Gateway を作る
- D. VPC の属性で `enableMulticast` を有効にする

??? success "答えと解説"
    **正解: C**

    有効化は新規作成時のみです。

    - A: 誤り。新規作成時のみ。
    - B: 誤り。ピアリングは非対応。
    - C: 正しい。
    - D: 誤り。VPC 自体は対応しない。

    **スキル:** [マルチキャスト](../domain3.md#t3-3-multicast) / **参照:** [マルチキャスト](../../../services/network-connectivity.md#tgw-multicast)

### 問26 {#q26}

金融のデータ配信で、VPC 内の送信元から複数の受信者へマルチキャストします。古い世代のインスタンスも残っています。Transit Gateway のマルチキャストの構成について正しいものを選んでください。（2つ選択）

- A. 送信元は Nitro のインスタンスのみである
- B. ドメインは VPC 単位で参加し、サブネットは指定しない
- C. Direct Connect と VPN で同じグループをオンプレミスへ届けられる
- D. フラグメントされたパケットも配信される
- E. メンバーは IGMPv2 か API で管理する

??? success "答えと解説"
    **正解: A, E**

    マルチキャストの制約です。

    - A: 正しい。
    - B: 誤り。サブネット単位。
    - C: 誤り。非対応。
    - D: 誤り。破棄する。
    - E: 正しい。

    **スキル:** [マルチキャスト](../domain3.md#t3-3-multicast) / **参照:** [マルチキャスト](../../../services/network-connectivity.md#tgw-multicast)

### 問27 {#q27}

オンプレミスの受信者へ、VPC 内の送信元のマルチキャストのデータを届けます。Direct Connect は既にあります。最も適切な方法はどれですか。

- A. Connect のアタッチメントを関連付けて、自動でマルチキャストを中継する
- B. ルーターと VPC 内の機器の間に、GRE などのトンネルを自分で作る
- C. Transit Gateway のマルチキャストドメインに DX のアタッチメントを関連付ける
- D. VPN のトンネルで IGMP を有効にして、Transit Gateway へ参加する

??? success "答えと解説"
    **正解: B**

    Transit Gateway のマルチキャストだけでは実現できません。

    - A: 誤り。非対応。
    - B: 正しい。
    - C: 誤り。非対応。
    - D: 誤り。非対応。

    **スキル:** [マルチキャスト](../domain3.md#t3-3-multicast) / **参照:** [マルチキャスト](../../../services/network-connectivity.md#tgw-multicast), [Connect](../../../services/network-connectivity.md#tgw-connect)

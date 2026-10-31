# ルーティングと BGPの問題集

対象の解説: [ルートの優先順位](../../../services/network-connectivity.md#route-priority), [BGP と経路制御](../../../services/network-connectivity.md#bgp), [属性の一覧](../../../services/network-connectivity.md#bgp-attributes), [計算例](../../../services/network-connectivity.md#route-priority-examples)

### 問1 {#q1}

VGW に同じプレフィックス `10.1.0.0/16` が、DX の BGP、VPN の静的、VPN の BGP の 3 つで届いています。VPC からこのプレフィックスへの通信はどの経路を通りますか。

- A. 3 つの ECMP
- B. DX の BGP
- C. VPN の BGP
- D. VPN の静的

??? success "答えと解説"
    **正解: B**

    VGW の順序は DX の BGP、VPN の静的、VPN の BGP です。

    - A: 誤り。VGW は ECMP に対応しない。
    - B: 正しい。
    - C: 誤り。VPN の BGP は最後。
    - D: 誤り。DX の BGP のほうが優先される。

    **スキル:** [ルーティングの基礎](../domain1.md#t1-5-routing) / **参照:** [VGW の経路選択](../../../services/network-connectivity.md#vgw-route-priority)

### 問2 {#q2}

Transit Gateway のルートテーブルで、VPN は静的ルート、DX は DX ゲートウェイからの伝播で同じプレフィックス `10.2.0.0/16` が登録されています。平常時は DX を使いたいのに、VPN へ流れています。最も適切な対応はどれですか。

- A. VPN の静的ルートの MED を大きくする
- B. VPN のアタッチメントの既定のルートテーブルの関連付けを無効にする
- C. VPN を BGP に変える
- D. DX ゲートウェイの許可プレフィックスから `10.2.0.0/16` を削除する

??? success "答えと解説"
    **正解: C**

    Transit Gateway では、静的ルートは伝播に勝ちます。

    - A: 誤り。静的ルートに MED はない。
    - B: 誤り。優先順位の問題が解決しない。
    - C: 正しい。
    - D: 誤り。DX の経路がなくなる。

    **スキル:** [ルーティングの基礎](../domain1.md#t1-5-routing) / **参照:** [Transit Gateway ルートテーブル](../../../services/network-connectivity.md#tgw-route-priority)

### 問3 {#q3}

VPC のルートテーブルに `10.1.0.0/16`（ピアリングの静的）と `10.1.0.0/16`（VGW の伝播）と `10.1.5.0/24`（VGW の伝播）があります。`10.1.5.10` への通信はどれを通りますか。

- A. `10.1.5.0/24` の VGW の伝播
- B. `10.1.0.0/16` のピアリング。静的は常に伝播より優先される
- C. `10.1.5.10` は破棄される。同じ範囲の経路が重複している
- D. `10.1.0.0/16` の VGW。2 つの伝播をまとめて判定する

??? success "答えと解説"
    **正解: A**

    最長一致が常に最初です。

    - A: 正しい。
    - B: 誤り。最長一致が先に適用される。
    - C: 誤り。破棄はされない。
    - D: 誤り。最長一致で判定する。

    **スキル:** [ルーティングの基礎](../domain1.md#t1-5-routing) / **参照:** [VPC ルートテーブル](../../../services/network-connectivity.md#vpc-route-priority)

### 問4 {#q4}

東京の VPC と 2 つの DX があります。関連付いたロケーションの接続 A を従、遠いロケーションの接続 B を主にします。A の広告に AS_PATH を付加しましたが、戻りの通信は A を通ります。最も適切な対応はどれですか。

- A. A の MED を B より大きくする
- B. A のルーターの受信ポリシーで Local preference を下げる
- C. A の AS_PATH の付加を増やして、10 回まで繰り返す
- D. B に `7224:7300`、A に `7224:7100` を付ける

??? success "答えと解説"
    **正解: D**

    リージョンは関連付いたロケーションに高い Local preference を与えます。

    - A: 誤り。AS_PATH の後に評価されるので効かない。
    - B: 誤り。オンプレミスから出る通信の制御で、戻りには効かない。
    - C: 誤り。Local preference が先に評価されるので効かない。
    - D: 正しい。

    **スキル:** [BGP 属性](../domain1.md#t1-5-bgp) / **参照:** [例 1: 2 本の DX で active/passive](../../../services/network-connectivity.md#bgp-active-passive), [例 3: AS_PATH が効かないとき](../../../services/network-connectivity.md#bgp-associated-region)

### 問5 {#q5}

2 本の DX を active/passive にしています。AWS からオンプレミスへの戻りはコミュニティで A に寄せましたが、オンプレミスから AWS への通信が B を通り、ステートフルなファイアウォールで切断されます。正しい対応はどれですか。

- A. A の広告に `7224:7300` をもう一度付けて、両方向を A に揃える
- B. B の広告のプレフィックスを細かくして、オンプレミスから出る通信を制御する
- C. VPN を追加して、非対称な経路を暗号化する
- D. ルーターの受信ポリシーで A の Local preference を高くする

??? success "答えと解説"
    **正解: D**

    行きは自分のルーターの Local preference で動かします。

    - A: 誤り。同じく戻りの制御で、行きには効かない。
    - B: 誤り。広告はAWS からオンプレミスへの通信を動かす。
    - C: 誤り。非対称の問題は解決しない。
    - D: 正しい。

    **スキル:** [BGP 属性](../domain1.md#t1-5-bgp) / **参照:** [例 1: 2 本の DX で active/passive](../../../services/network-connectivity.md#bgp-active-passive)

### 問6 {#q6}

同じ速度の 2 本の DX に active/active で分散させます。AWS からオンプレミスの方向で ECMP が働くための条件はどれですか。

- A. 2 本で別の ASN を使って、AS_PATH の長さをそろえない
- B. 同じプレフィックス、コミュニティ、AS_PATH 長、MED で広告する
- C. 2 本で異なる長さのプレフィックスを広告する
- D. 片方にだけ `7224:7300` を付けて広告する

??? success "答えと解説"
    **正解: B**

    属性をそろえると ECMP になります。

    - A: 誤り。AS_PATH の長さをそろえる必要がある。
    - B: 正しい。
    - C: 誤り。長いほうへ寄る。
    - D: 誤り。片方に寄る。

    **スキル:** [BGP 属性](../domain1.md#t1-5-bgp) / **参照:** [例 2: 2 本の DX で active/active](../../../services/network-connectivity.md#bgp-active-active)

### 問7 {#q7}

公開 VIF でオンプレミスの公開プレフィックスを広告しています。AWS 内での広がりを同じ大陸のリージョンに限定したいと考えています。コミュニティの指定として正しいものはどれですか。

- A. `7224:8100`
- B. `7224:9200`
- C. `7224:9100`
- D. `7224:7100`

??? success "答えと解説"
    **正解: B**

    公開 VIF の広がりは `7224:9100`（リージョン）と `7224:9200`（大陸）です。

    - A: 誤り。AWS から受信する経路の範囲を示す値。
    - B: 正しい。
    - C: 誤り。リージョンに限定する値。
    - D: 誤り。Local preference を下げる値で、広がりの指定ではない。

    **スキル:** [BGP 属性](../domain1.md#t1-5-bgp) / **参照:** [公開 VIF の経路制御](../../../services/network-connectivity.md#bgp-public-vif)

### 問8 {#q8}

複数のリージョンと拠点を結ぶ設計で、BGP に統一する案をレビューしています。接続ごとのルーティングの方式のうち、公式の制約に合うものを選んでください。（2つ選択）

- A. Transit Gateway ピアリングは静的ルートのみ
- B. Transit Gateway Connect は BGP のみ
- C. DX の VIF は静的ルートでも設定できる
- D. VGW の VPN は BGP を使えば ECMP を使える
- E. Transit Gateway の VPN の ECMP は静的ルートでも使える

??? success "答えと解説"
    **正解: A, B**

    接続の種類ごとに使える方式が決まっています。

    - A: 正しい。
    - B: 正しい。
    - C: 誤り。VIF は BGP。
    - D: 誤り。VGW は ECMP に対応しない。
    - E: 誤り。動的のみ。

    **スキル:** [ルーティングプロトコル](../domain2.md#t2-1-routing) / **参照:** [ルーティング](../../../services/network-connectivity.md#vpn-routing), [ピアリング](../../../services/network-connectivity.md#tgw-peering)

### 問9 {#q9}

VGW の経路が BGP で届いているのに、サブネットの EC2 からオンプレミスへ通信できません。VPC のルートテーブルに経路が見えません。SG と NACL は問題ありません。最も適切な対応はどれですか。

- A. `0.0.0.0/0` を IGW へ向けて、オンプレミスへの経路の代わりにする
- B. VPN 接続のトンネルオプションで `DPDTimeoutAction` を `Restart` にする
- C. サブネットのルートテーブルで VGW の伝播を有効にする
- D. VGW の ASN を変更して、BGP を再確立する

??? success "答えと解説"
    **正解: C**

    伝播を有効にしないとサブネットの表に反映されません。

    - A: 誤り。オンプレミスへは届かない。
    - B: 誤り。トンネルの再起動で、ルートには関係しない。
    - C: 正しい。
    - D: 誤り。経路はすでに届いている。

    **スキル:** [ルーティングプロトコル](../domain2.md#t2-1-routing) / **参照:** [ルートテーブル](../../../services/network-connectivity.md#tgw-route-tables), [ルーティング](../../../services/network-connectivity.md#vpn-routing)

### 問10 {#q10}

VPC を Transit Gateway にアタッチし、Transit Gateway のルートテーブルにも経路があります。しかし VPC の EC2 から他の VPC へ通信できません。不足している可能性が高いのはどれですか。

- A. VPC のルートテーブルに宛先と `tgw-` のルートを追加する
- B. VPC に IGW を追加する
- C. Transit Gateway のルートテーブルで VPC の伝播を削除する
- D. アタッチメントの DNS サポートを無効にする

??? success "答えと解説"
    **正解: A**

    Transit Gateway は VPC のルートテーブルを自動では変えません。

    - A: 正しい。
    - B: 誤り。Transit Gateway の経路に不要。
    - C: 誤り。戻りの経路がなくなる。
    - D: 誤り。通信の経路に関係しない。

    **スキル:** [ルーティングプロトコル](../domain2.md#t2-1-routing) / **参照:** [ルートテーブル](../../../services/network-connectivity.md#tgw-route-tables), [アタッチメント](../../../services/network-connectivity.md#tgw-attachments)

### 問11 {#q11}

VPN の 2 本のトンネルのうち、AWS の保守のときに片方へ切り替わるようにしています。CGW の設定で、両トンネルの Weight を別々の値にしていました。AWS が付ける MED に従って切り替えるには、どうしますか。

- A. 両トンネルの AS_PATH と Weight をそろえる
- B. 片方のトンネルを `Disable` にして、保守のたびに手で切り替える
- C. CGW の Local preference を片方だけ高くしておく
- D. 両トンネルの MED をルーターで 0 に上書きする

??? success "答えと解説"
    **正解: A**

    Weight や Local preference は MED より先に評価されます。

    - A: 正しい。
    - B: 誤り。手動で、保守の通知の仕組みに合わない。
    - C: 誤り。MED より先に評価されて、AWS の MED が無視される。
    - D: 誤り。AWS の MED が無視される。

    **スキル:** [BGP の管理](../domain3.md#t3-1-bgp) / **参照:** [VPN の 2 本のトンネル](../../../services/network-connectivity.md#bgp-vpn-tunnels)

### 問12 {#q12}

DX の BGP の障害検出が遅く、切り替えまで 90 秒かかっています。プライベート VIF です。切り替えを速くする方法として、正しい理解はどれですか。

- A. BFD を AWS のサポートに申請して、VIF で有効にしてもらう
- B. Connect を挟んで BFD を使えるようにする
- C. BFD は VIF で自動で有効なので、ルーター側で設定する
- D. BGP のタイマーを 1 秒に下げるだけで BFD と同じ効果がある

??? success "答えと解説"
    **正解: C**

    ルーター側で設定するまで BFD は効きません。

    - A: 誤り。VIF で自動で有効。
    - B: 誤り。Connect は BFD に対応しない。
    - C: 正しい。
    - D: 誤り。効果が異なり、推奨の方法ではない。

    **スキル:** [BGP の管理](../domain3.md#t3-1-bgp) / **参照:** [VIF の種類](../../../services/network-connectivity.md#dx-vif-types)

### 問13 {#q13}

SD-WAN のアプライアンスが Transit Gateway Connect の BGP を使っています。切り替えを速くするための BFD を設定できるか、タイマーを変更できるかを確認しています。正しい説明はどれですか。

- A. ホールドタイマーを 3 秒まで短くできるので、アプライアンスで変更すれば足りる
- B. グレースフルリスタートを有効にすれば、BFD がなくても 1 秒で検出できる
- C. BFD は VIF と同じように自動で有効になり、ルーターで設定するだけで使える
- D. BFD とグレースフルリスタートは使えず、タイマーはキープアライブ 10 秒、ホールド 30 秒である

??? success "答えと解説"
    **正解: D**

    Connect の BGP の制約です。

    - A: 誤り。タイマーの値は決まっている。
    - B: 誤り。Connect では使えない。
    - C: 誤り。Connect では使えない。
    - D: 正しい。

    **スキル:** [BGP の管理](../domain3.md#t3-1-bgp) / **参照:** [Connect](../../../services/network-connectivity.md#tgw-connect)

### 問14 {#q14}

Transit Gateway で開発 VPC の通信を、特定の宛先 `10.9.0.0/16` だけ止めます。他の宛先は既存の伝播のままにします。最も適切な方法はどれですか。

- A. 開発 VPC のアタッチメントの関連付けを解除する
- B. 宛先の VPC の SG で開発 VPC を拒否するルールを追加する
- C. 全伝播を無効にして、残りを静的ルートで書き直す
- D. 開発 VPC のルートテーブルに `10.9.0.0/16` のブラックホールルートを追加する

??? success "答えと解説"
    **正解: D**

    ブラックホールは指定の宛先を破棄します。

    - A: 誤り。全通信が止まる。
    - B: 誤り。SG に拒否ルールはない。
    - C: 誤り。変更の範囲が大きい。
    - D: 正しい。

    **スキル:** [ルートテーブル](../domain3.md#t3-1-route-tables) / **参照:** [Transit Gateway ルートテーブル](../../../services/network-connectivity.md#tgw-route-priority)

### 問15 {#q15}

VPC のルートテーブルで DX と VPN が同じ経路を広告しています。表には DX の経路しか表示されず、VPN の経路が見えません。担当者が VPN の障害を疑っています。正しい判断はどれですか。

- A. 表に出るのは優先経路だけで、異常ではない
- B. VPN のルートが消えたので、すぐに VPN を作り直す
- C. 伝播が無効で、VPN の経路が反映されなくなった
- D. `PacketDropCountNoRoute` が増えて、VPN が拒否されている

??? success "答えと解説"
    **正解: A**

    DX が落ちれば VPN の経路が現れます。

    - A: 正しい。
    - B: 誤り。作り直す根拠にならない。
    - C: 誤り。伝播が無効なら DX も表示されない。
    - D: 誤り。Transit Gateway のメトリクスで、この判断には使えない。

    **スキル:** [ルートテーブル](../domain3.md#t3-1-route-tables) / **参照:** [VPC ルートテーブル](../../../services/network-connectivity.md#vpc-route-priority), [計算例](../../../services/network-connectivity.md#route-priority-examples)

### 問16 {#q16}

VPC の中のアプライアンス（BGP に対応）の経路を、サブネットのルートテーブルへ動的に反映したいと考えています。アプライアンスの障害時にルートも自動で切り替えます。最も適切な機能はどれですか。

- A. Transit Gateway Connect
- B. Lambda でルートテーブルを定期的に書き換える処理
- C. VGW のルート伝播
- D. VPC Route Server

??? success "答えと解説"
    **正解: D**

    Route Server は BGP で受けた経路を VPC のルートテーブルへ反映します。

    - A: 誤り。アプライアンスと Transit Gateway の BGP で、VPC の表の更新ではない。
    - B: 誤り。運用の手間が大きく、切り替えも遅い。
    - C: 誤り。VGW の経路の反映で、VPC の中の機器は対象外。
    - D: 正しい。

    **スキル:** [ルートテーブル](../domain3.md#t3-1-route-tables) / **参照:** [VPC Route Server](../../../services/network-connectivity.md#route-server)

### 問17 {#q17}

VPC に新しい CIDR `10.2.0.0/16` を追加しようとしましたが、失敗しました。ルートテーブルには `10.2.0.0/16` の静的ルートがピアリングへ向いています。正しい説明はどれですか。

- A. セカンダリ CIDR は `100.64.0.0/10` にしか追加できない
- B. 追加する CIDR は、既存のルートの宛先と同じか大きくできない
- C. VPC の CIDR の追加には IGW のデタッチが必要である
- D. ピアリングのある VPC には CIDR を追加できない

??? success "答えと解説"
    **正解: B**

    既存のルートと競合しない CIDR を選ぶか、ルートを整理します。

    - A: 誤り。他の範囲も追加できる。
    - B: 正しい。
    - C: 誤り。IGW の条件はない。
    - D: 誤り。重複がなければ追加できる。

    **スキル:** [経路の最適化](../domain3.md#t3-1-route-optimization) / **参照:** [経路数の上限に当たったとき](../../../services/network-connectivity.md#bgp-route-limits), [VPC の CIDR](../../../services/network-connectivity.md#vpc-cidr)

### 問18 {#q18}

DX を主の経路として広告する `10.0.0.0/8` と、VPN で従の経路として広告する `10.1.0.0/16` があります。平常時に `10.1.0.0/16` の通信が VPN を通っています。修正はどれですか。

- A. VPN の AS_PATH を長くする
- B. VPN の MED を大きくする
- C. VPN のプレフィックスを DX より細かくしない
- D. DX の VIF のコミュニティを `7224:7300` にする

??? success "答えと解説"
    **正解: C**

    最長一致は常に最初です。

    - A: 誤り。プレフィックス長が先。
    - B: 誤り。プレフィックス長が先。
    - C: 正しい。
    - D: 誤り。プレフィックスの長さが先に評価される。

    **スキル:** [経路の最適化](../domain3.md#t3-1-route-optimization) / **参照:** [計算例](../../../services/network-connectivity.md#route-priority-examples)

### 問19 {#q19}

プライベート VIF へ 90 経路を広告していますが、新しい拠点で 15 経路増えます。経路が増えると BGP が落ちる恐れがあります。最も適切な対応はどれですか。

- A. 広告したうえで、BGP が落ちてから自動の回復に任せる
- B. VPC のルートテーブルの静的ルートに追加して、VIF の上限を回避する
- C. 経路をプライベート VIF ではなく公開 VIF で広告して上限を回避する
- D. 拠点の経路を集約して、広告の数を上限より少なくする

??? success "答えと解説"
    **正解: D**

    集約が基本です。既定の上限は 100 で、プレフィックス制御で 1,000 まで上げることもできます。

    - A: 誤り。全経路が消える。
    - B: 誤り。VPC 側の静的ルートではオンプレミスからの広告の数は変わらない。
    - C: 誤り。公開 VIF は VPC に接続しない。
    - D: 正しい。

    **スキル:** [経路の最適化](../domain3.md#t3-1-route-optimization) / **参照:** [経路数の上限に当たったとき](../../../services/network-connectivity.md#bgp-route-limits)

### 問20 {#q20}

Transit Gateway に接続した VPC のプレフィックスを、トランジット VIF でオンプレミスへ広告しています。上限（合計 200）に近づいています。経路を最適化する方法はどれですか。

- A. VPC の数を減らすまで新しい VPC を作らない
- B. オンプレミスのルーターで受信の上限を上げる
- C. VIF を公開 VIF に作り直す
- D. 許可プレフィックスを集約して広告する

??? success "答えと解説"
    **正解: D**

    許可プレフィックスで集約して広告します。

    - A: 誤り。集約で解決でき、過剰な制約。
    - B: 誤り。AWS 側の広告の上限は変わらない。
    - C: 誤り。公開 VIF は Transit Gateway に接続しない。
    - D: 正しい。

    **スキル:** [経路の最適化](../domain3.md#t3-1-route-optimization) / **参照:** [経路数の上限に当たったとき](../../../services/network-connectivity.md#bgp-route-limits), [ルートテーブル](../../../services/network-connectivity.md#tgw-route-tables)

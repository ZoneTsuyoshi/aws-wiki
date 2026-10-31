# プライベート接続とハイブリッド接続の問題集

対象の解説: [VPC エンドポイントと PrivateLink](../../../services/networking.md#vpc-endpoints)、[VPC ピアリング](../../../services/network-connectivity.md#vpc-peering)、[Transit Gateway](../../../services/network-connectivity.md#transit-gateway)、[Site-to-Site VPN](../../../services/network-connectivity.md#site-to-site-vpn)、[Direct Connect](../../../services/network-connectivity.md#direct-connect)

### 問1 {#q1}

40 個の VPC を相互に接続します。オンプレミスとの接続も共有します。どれが適切ですか。

- A. VPC ピアリングを総当たりで作成する構成
- B. インターフェイスエンドポイントを全 VPC に置く構成
- C. Transit Gateway
- D. NAT ゲートウェイを VPC ごとに置く構成

??? success "答えと解説"
    **正解: C**

    多数の VPC の接続には Transit Gateway が向きます。

    - A: 誤り。推移せず、多数の接続の管理が大変である。
    - B: 誤り。特定のサービスへの接続で、VPC の相互接続ではない。
    - C: 正しい。
    - D: 誤り。VPC の間の接続ではない。

    **スキル:** [5.1.2](../domain5.md#skill-5-1-2) / **参照:** [VPC 同士の接続](../../../services/network-connectivity.md#choosing-multi-vpc)、[Transit Gateway](../../../services/network-connectivity.md#transit-gateway)

### 問2 {#q2}

VPC ピアリングの A-B、B-C があります。A から C へ通信できません。CIDR の重複はありません。どう直しますか。

- A. A-C のピアリングを作り、両方のルートテーブルに経路を足す
- B. C のセキュリティグループで B の CIDR を許可する
- C. B のルートテーブルに、A から C への転送の経路を足す
- D. A のルートテーブルの宛先を B のインターネットゲートウェイにする

??? success "答えと解説"
    **正解: A**

    ピアリングは推移しません。

    - A: 正しい。
    - B: 誤り。A-C の経路の問題が残る。
    - C: 誤り。ピアリングは推移しない。
    - D: 誤り。相手の IGW は使えない。

    **スキル:** [5.1.2](../domain5.md#skill-5-1-2) / **参照:** [VPC ピアリング](../../../services/network-connectivity.md#vpc-peering)

### 問3 {#q3}

自社のサービスを、CIDR が重複する他の VPC へ公開します。どの構成が適切ですか。

- A. VPC ピアリングで接続し、両方のルートテーブルに経路を足す
- B. NLB の裏に置いて PrivateLink で公開する
- C. Transit Gateway でつなぎ、両方の VPC に同じ経路を足す
- D. S3 のゲートウェイエンドポイントを使い、ルートテーブルに経路を足す

??? success "答えと解説"
    **正解: B**

    PrivateLink は CIDR の重複があっても使えます。

    - A: 誤り。CIDR が重複すると作れない。
    - B: 正しい。
    - C: 誤り。CIDR の重複で経路が衝突する。
    - D: 誤り。S3 と DynamoDB 向けの機能である。

    **スキル:** [5.1.2](../domain5.md#skill-5-1-2) / **参照:** [VPC エンドポイントと PrivateLink](../../../services/networking.md#vpc-endpoints)、[エンドポイントの選び方と制約](../../../services/networking.md#endpoint-settings)

### 問4 {#q4}

オンプレミスと VPC を今日から接続します。専用線の契約はありません。BGP が使える機器があります。どれを選びますか。

- A. VPC ピアリングでオンプレミスのルーターへ接続する構成
- B. Direct Connect の専用接続
- C. Client VPN のエンドポイント
- D. 動的ルーティングの Site-to-Site VPN

??? success "答えと解説"
    **正解: D**

    Site-to-Site VPN はすぐに始められ、BGP が使えるなら動的ルーティングを選びます。

    - A: 誤り。オンプレミスとは接続できない。
    - B: 誤り。開通までに時間がかかる。
    - C: 誤り。利用者の端末の接続に使う。
    - D: 正しい。

    **スキル:** [5.1.2](../domain5.md#skill-5-1-2) / **参照:** [オンプレミスとの接続](../../../services/network-connectivity.md#choosing-hybrid)、[Site-to-Site VPN](../../../services/network-connectivity.md#site-to-site-vpn)

### 問5 {#q5}

リモートの社員のノート PC から VPC のサーバーへ接続します。どれを設定しますか。

- A. Site-to-Site VPN と CGW を全員の自宅に置く構成
- B. Client VPN のルートと認可ルール
- C. ゲートウェイエンドポイントの全員分の追加
- D. Direct Connect の仮想インターフェイスを全員に割り当てる構成

??? success "答えと解説"
    **正解: B**

    Client VPN はルートと認可ルールの両方を設定します。

    - A: 誤り。拠点の接続である。
    - B: 正しい。
    - C: 誤り。AWS サービスへの経路の機能である。
    - D: 誤り。利用者の端末の接続ではない。

    **スキル:** [5.1.2](../domain5.md#skill-5-1-2) / **参照:** [Client VPN](../../../services/network-connectivity.md#client-vpn)

### 問6 {#q6}

VPC エンドポイントの説明として正しいものを選んでください。（2つ選択）

- A. インターフェイス型はサブネットに ENI を作る
- B. インターフェイス型は追加料金がない
- C. ゲートウェイ型はオンプレミスからも使える
- D. ゲートウェイ型にはセキュリティグループを付ける
- E. ゲートウェイ型はルートテーブルにルートを追加する

??? success "答えと解説"
    **正解: A, E**

    仕組みと料金が違います。

    - A: 正しい。
    - B: 誤り。時間とデータ量の料金がある。
    - C: 誤り。オンプレミスから使うならインターフェイス型である。
    - D: 誤り。ゲートウェイ型はエンドポイントポリシーで制御する。
    - E: 正しい。

    **スキル:** [5.1.2](../domain5.md#skill-5-1-2) / **参照:** [エンドポイントの選び方と制約](../../../services/networking.md#endpoint-settings)、[エンドポイントポリシー](../../../services/networking.md#endpoint-policies)

### 問7 {#q7}

Site-to-Site VPN の `TunnelState` が 0 です。確認するものはどれですか。

- A. セキュリティグループの送信ルールの 500 番ポート
- B. VPC のルートテーブルのプレフィックスリストと伝播の設定
- C. Transit Gateway のアプライアンスモードの設定
- D. CGW の設定、PSK、IKE のバージョンとトンネルログ

??? success "答えと解説"
    **正解: D**

    トンネルが上がらないときは、IKE の交渉の条件を確認します。

    - A: 誤り。トンネルの確立にセキュリティグループは使わない。
    - B: 誤り。トンネルが上がった後の経路の話である。
    - C: 誤り。検査機器向けの設定で、トンネルの確立とは関係がない。
    - D: 正しい。

    **スキル:** [5.3.4](../domain5.md#skill-5-3-4) / **参照:** [トンネル](../../../services/network-connectivity.md#vpn-tunnels)、[トンネルオプション](../../../services/network-connectivity.md#vpn-tunnel-options)

### 問8 {#q8}

VPN のトンネルが通信なしの時間に落ちます。CGW はイニシエーターにしたくありません。どの設定と対策が適切ですか。

- A. `StartupAction=start`、`DPDTimeoutAction=restart` にする
- B. `Mtu` を 9001 にする
- C. `TunnelState` のアラームの期間を短くし、切れたらコンソールから人が再接続する手順を定めて運用する
- D. 動的ルーティングを静的へ変える

??? success "答えと解説"
    **正解: A**

    AWS の側から接続を始められ、切れたときに再起動できます。

    - A: 正しい。
    - B: 誤り。VPN のトンネルが落ちる原因の対処ではない。
    - C: 誤り。監視の設定で、落ちる問題は直らない。
    - D: 誤り。トンネルが落ちる問題の対処ではない。

    **スキル:** [5.3.4](../domain5.md#skill-5-3-4) / **参照:** [トンネルオプション](../../../services/network-connectivity.md#vpn-tunnel-options)

### 問9 {#q9}

VPN のトンネルは上がっていますが、VPC とオンプレミスの間が通りません。確認するものを選んでください。（2つ選択）

- A. トンネルログの IKE の交渉の結果
- B. ACM の証明書の有効期限
- C. CGW の経路
- D. VPC のルートテーブルのルート伝播か静的ルート
- E. `TunnelState` の値が 0 になっているか

??? success "答えと解説"
    **正解: C, D**

    トンネルが上がっているなら、両側の経路を確認します。

    - A: 誤り。トンネルは上がっているので、まず経路を確認する。
    - B: 誤り。PSK の VPN では、この症状の確認の対象ではない。
    - C: 正しい。
    - D: 正しい。
    - E: 誤り。トンネルは上がっている。

    **スキル:** [5.3.4](../domain5.md#skill-5-3-4) / **参照:** [ルーティング](../../../services/network-connectivity.md#vpn-routing)

### 問10 {#q10}

VPN 経由で小さな通信は通るのに、大きなファイルの転送だけが止まります。どの説明が正しいですか。

- A. ルートの伝播が有効になっているため
- B. CloudFront のエラーのキャッシュが残っているため
- C. VPN は PMTUD に非対応なので、MTU と MSS を調整する
- D. `ConnectionState` が 0 になっているため

??? success "答えと解説"
    **正解: C**

    大きな転送だけ止まるときは、MTU と MSS を疑います。

    - A: 誤り。大きなパケットだけの問題の説明ではない。
    - B: 誤り。VPN と関係がない。
    - C: 正しい。
    - D: 誤り。Direct Connect の指標である。

    **スキル:** [5.3.4](../domain5.md#skill-5-3-4) / **参照:** [MTU と MSS](../../../services/network-connectivity.md#vpn-mtu)、[PMTUD とトラブルシューティング](../../../services/network-connectivity.md#pmtud)

### 問11 {#q11}

Direct Connect の BGP が `idle` になり、全経路が消えました。物理の接続は正常です。広告する経路を増やした直後です。どう直しますか。

- A. `ConnectionErrorCount` を 0 にリセットする
- B. VPN の静的ルートに変える
- C. 広告する経路を上限以下に集約する
- D. 新しい接続を発注する

??? success "答えと解説"
    **正解: C**

    広告の経路が上限を超えると、BGP のセッションが落ちます。

    - A: 誤り。物理のエラーの指標である。
    - B: 誤り。広告の経路の問題は直らない。
    - C: 正しい。
    - D: 誤り。物理の接続は正常である。

    **スキル:** [5.3.4](../domain5.md#skill-5-3-4) / **参照:** [経路数の上限に当たったとき](../../../services/network-connectivity.md#bgp-route-limits)、[Direct Connect](../../../services/network-connectivity.md#direct-connect)

### 問12 {#q12}

Direct Connect と VPN が同じ VGW にあります。DX が正常なのに、一部の通信が VPN を通ります。どの説明が正しいですか。

- A. VPN により具体的な経路があり、最長一致が優先されている
- B. `TunnelState` が 1 だと、必ず VPN が優先される
- C. VGW では VPN が常に優先される
- D. DX は BGP を使わないので、優先されない

??? success "答えと解説"
    **正解: A**

    まず最長一致です。同じ長さなら DX の BGP、VPN の静的、VPN の BGP の順です。

    - A: 正しい。
    - B: 誤り。トンネルが正常というだけで VPN が優先されることはない。逆に、トンネルの異常は他の条件より先に経路の選択に影響する。
    - C: 誤り。同じ長さなら DX の BGP が優先される。
    - D: 誤り。DX は BGP を使う。

    **スキル:** [5.3.4](../domain5.md#skill-5-3-4) / **参照:** [VGW の経路選択](../../../services/network-connectivity.md#vgw-route-priority)、[ルートの優先順位](../../../services/network-connectivity.md#route-priority)

### 問13 {#q13}

インターフェイスエンドポイントを作りましたが、サービスの通常の名前が公開 IP に解決されます。何を確認しますか。

- A. S3 のバケットポリシー
- B. プライベート DNS と VPC の DNS 属性
- C. ピアリングの承認の期限
- D. ゲートウェイエンドポイントのルート

??? success "答えと解説"
    **正解: B**

    プライベート DNS が有効なら、通常の名前がプライベート IP に解決されます。

    - A: 誤り。名前解決の問題ではない。
    - B: 正しい。
    - C: 誤り。名前解決の問題ではない。
    - D: 誤り。インターフェイス型の名前解決の確認ではない。

    **スキル:** [5.3.4](../domain5.md#skill-5-3-4) / **参照:** [エンドポイントの選び方と制約](../../../services/networking.md#endpoint-settings)、[VPC の DNS 属性](../../../services/networking.md#vpc-dns-attributes)

### 問14 {#q14}

接続の問題の説明として正しいものを選んでください。（2つ選択）

- A. オンプレミスからゲートウェイエンドポイントは使えない
- B. ピアリングは片方のルートテーブルに経路があればよい
- C. Client VPN はルートがあれば認可ルールは不要である
- D. インターフェイスエンドポイントのセキュリティグループでは 443 を閉じる
- E. ピアリングの未承認の要求は 7 日で失効する

??? success "答えと解説"
    **正解: A, E**

    接続の種類ごとに、確認する点が違います。

    - A: 正しい。
    - B: 誤り。両方に必要である。
    - C: 誤り。両方が必要である。
    - D: 誤り。サービスの通信を許可する必要がある。
    - E: 正しい。

    **スキル:** [5.3.4](../domain5.md#skill-5-3-4) / **参照:** [VPC ピアリング](../../../services/network-connectivity.md#vpc-peering)、[エンドポイントの選び方と制約](../../../services/networking.md#endpoint-settings)

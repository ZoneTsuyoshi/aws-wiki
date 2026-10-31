# VPN とカプセル化の問題集

対象の解説: [Site-to-Site VPN](../../../services/network-connectivity.md#site-to-site-vpn), [トンネル](../../../services/network-connectivity.md#vpn-tunnels), [トンネルオプション](../../../services/network-connectivity.md#vpn-tunnel-options), [プライベート IP VPN](../../../services/network-connectivity.md#vpn-private-ip), [Client VPN](../../../services/network-connectivity.md#client-vpn)

### 問1 {#q1}

既存の Transit Gateway の VPN 接続で、遠隔地からの通信の品質を上げるためアクセラレーションを使います。現在は標準のトンネルです。正しい手順はどれですか。

- A. アクセラレーションを有効にした VPN 接続を新しく作り、切り替える
- B. 既存の接続のトンネルオプションでアクセラレーションを有効に変更する
- C. VGW に移してから、既存の接続のアクセラレーションを有効にする
- D. Large Bandwidth Tunnel へ変更して、アクセラレーションと併用する

??? success "答えと解説"
    **正解: A**

    アクセラレーションは作成時のみです。

    - A: 正しい。
    - B: 誤り。作成時にしか有効にできない。
    - C: 誤り。Transit Gateway のみ。
    - D: 誤り。併用できない。

    **スキル:** [VPN](../domain2.md#t2-1-vpn) / **参照:** [トンネル](../../../services/network-connectivity.md#vpn-tunnels), [アクセラレーション](../../../services/network-connectivity.md#vpn-accelerated)

### 問2 {#q2}

通信がしばらくないと VPN のトンネルが落ち、次に通信を始めると遅れます。CGW からは定期的な通信がありません。AWS 側の設定で改善する方法はどれですか。

- A. `StartupAction` を `Add`、`DPDTimeoutAction` を `Clear` にする
- B. フェーズ 2 のライフタイムを 28,800 秒に変更する
- C. `StartupAction` を `Start`、`DPDTimeoutAction` を `Restart` にする
- D. トンネルの内部 CIDR を別の値に変更する

??? success "答えと解説"
    **正解: C**

    トンネルの維持を AWS 側から開始します。

    - A: 誤り。既定で、問題文の状況。
    - B: 誤り。上限を超え、問題の解決にならない。
    - C: 正しい。
    - D: 誤り。DPD とは関係がない。

    **スキル:** [VPN](../domain2.md#t2-1-vpn) / **参照:** [トンネルオプション](../../../services/network-connectivity.md#vpn-tunnel-options)

### 問3 {#q3}

Site-to-Site VPN を 1 接続だけ作り、CGW にはトンネル 1 だけを設定しました。動作確認は成功しています。監査の指摘として最も適切なものはどれですか。

- A. 両方のトンネルを設定しないと、保守などで片方が落ちたときに切断される
- B. 2 本目は待機専用なので、CGW に設定すると経路が非対称になる
- C. 冗長化には別の CGW が必須で、同じ CGW にトンネル 2 は設定できない
- D. 標準のトンネル 1 本で帯域が足りるので、指摘の必要はない

??? success "答えと解説"
    **正解: A**

    1 接続に 2 本のトンネルがあり、別々の AZ にあります。

    - A: 正しい。
    - B: 誤り。両方を設定することが推奨。
    - C: 誤り。同じ CGW に両方を設定できる。
    - D: 誤り。帯域とは別に、冗長のため両方が必要。

    **スキル:** [VPN](../domain2.md#t2-1-vpn) / **参照:** [トンネル](../../../services/network-connectivity.md#vpn-tunnels)

### 問4 {#q4}

新しい担当者が、AWS のカプセル化の技術を整理しています。規制で暗号化の有無を報告します。カプセル化と暗号化の組み合わせのうち、正しいものを選んでください。（2つ選択）

- A. Traffic Mirroring は VXLAN の UDP 4789 で運ぶ
- B. Site-to-Site VPN は GRE で、暗号化はない
- C. MACsec は L3 のトンネルで、VPC まで暗号化する
- D. GWLB は MACsec で、暗号化がある
- E. Transit Gateway Connect は GRE で、暗号化はない

??? success "答えと解説"
    **正解: A, E**

    技術と使いどころを対応させます。

    - A: 正しい。
    - B: 誤り。IPsec で暗号化する。
    - C: 誤り。L2 で、区間のみ。
    - D: 誤り。GENEVE で暗号化はない。
    - E: 正しい。

    **スキル:** [カプセル化と暗号化](../domain1.md#t1-5-encapsulation) / **参照:** [MTU と MSS](../../../services/network-connectivity.md#vpn-mtu), [Connect](../../../services/network-connectivity.md#tgw-connect)

### 問5 {#q5}

Connect の GRE のアプライアンスで、外部の MTU が 1500 です。内側のインターフェイスの MTU をいくつにしますか。

- A. 1476
- B. 1446
- C. 1472
- D. 1500

??? success "答えと解説"
    **正解: A**

    GRE のヘッダーの 24 バイトを引きます。

    - A: 正しい。
    - B: 誤り。VPN の最大の実効 MTU。
    - C: 誤り。28 バイトは IP と ICMP の分で、GRE の値ではない。
    - D: 誤り。GRE のヘッダーの分を引く必要がある。

    **スキル:** [カプセル化と暗号化](../domain1.md#t1-5-encapsulation) / **参照:** [Connect](../../../services/network-connectivity.md#tgw-connect), [MTU と MSS](../../../services/network-connectivity.md#vpn-mtu)

### 問6 {#q6}

平常時は DX のトランジット VIF（MTU 8500）を使い、障害時は VPN へ切り替わります。切り替わると大きなパケットだけが消えます。原因として正しいものはどれですか。

- A. DX の BGP が切れたので、VPC のルートテーブルの伝播が止まる
- B. VPN の暗号化で大きなパケットは必ず破棄される
- C. カプセル化で実効 MTU が 1446 以下に下がる
- D. DX の MTU 8500 が VPN にも引き継がれ、CGW で断片化できなくなる

??? success "答えと解説"
    **正解: C**

    DX から VPN へ切り替わると急に小さくなります。

    - A: 誤り。問題文の症状の説明にならない。
    - B: 誤り。MTU に収まれば通る。
    - C: 正しい。
    - D: 誤り。VPN はジャンボに対応せず、8500 は適用されない。

    **スキル:** [カプセル化と暗号化](../domain1.md#t1-5-encapsulation) / **参照:** [MTU とジャンボフレーム](../../../services/network-connectivity.md#mtu), [MTU と MSS](../../../services/network-connectivity.md#vpn-mtu)

### 問7 {#q7}

規制により DX の上の通信も暗号化します。公開 IP は使えません。AWS 側は Transit Gateway です。最も適切な構成はどれですか。

- A. トランジット VIF の上の Accelerated VPN
- B. 公開 VIF の上の Site-to-Site VPN
- C. トランジット VIF の上のプライベート IP VPN
- D. プライベート VIF の上の標準の VPN

??? success "答えと解説"
    **正解: C**

    プライベート IP VPN は公開 IP を使いません。

    - A: 誤り。アクセラレーションと併用できない。
    - B: 誤り。公開 IP が必要。
    - C: 正しい。
    - D: 誤り。公開エンドポイントへの経路にならない。

    **スキル:** [DX の上の VPN](../domain4.md#t4-3-vpn-dx) / **参照:** [プライベート IP VPN](../../../services/network-connectivity.md#vpn-private-ip)

### 問8 {#q8}

10 Gbps の DX の上に標準のトンネルでプライベート IP VPN を張りました。すると実効の帯域が大幅に下がりました。アプリは同時に多くのフローを使います。原因と最も適切な対応はどれですか。

- A. プライベート IP VPN は処理の都合で DX の帯域の半分に制限される
- B. DX の VIF の MTU が 9001 で固定されるので、値を 1500 に下げる
- C. MACsec を有効にすれば、VPN の帯域の上限が解除される
- D. トンネルの帯域が上限になるので、Transit Gateway で ECMP にする

??? success "答えと解説"
    **正解: D**

    VPN を重ねるとトンネルの帯域が上限になります。

    - A: 誤り。制限は DX の半分ではなく、トンネルの帯域。
    - B: 誤り。実効帯域の主因ではない。
    - C: 誤り。別の機能で上限は解除されない。
    - D: 正しい。

    **スキル:** [DX の上の VPN](../domain4.md#t4-3-vpn-dx) / **参照:** [プライベート IP VPN](../../../services/network-connectivity.md#vpn-private-ip), [トンネル](../../../services/network-connectivity.md#vpn-tunnels)

### 問9 {#q9}

1 本の DX で、機密データは暗号化し、大容量のバックアップは暗号化なしで DX の全帯域を使いたいと考えています。最も適切な構成はどれですか。

- A. ルートテーブルを分け、機密だけプライベート IP VPN の経路へ流す
- B. MACsec で片方の通信だけを暗号化する
- C. 全通信に VPN を適用して、バックアップの帯域の不足は受け入れることにする
- D. バックアップだけ公開 VIF の上の VPN へ流して、帯域を確保する

??? success "答えと解説"
    **正解: A**

    併用できます。

    - A: 正しい。
    - B: 誤り。通信の種類で暗号化を分けられない。
    - C: 誤り。要件に合わない。
    - D: 誤り。トンネルの帯域が上限になり、全帯域の要件に合わない。

    **スキル:** [DX の上の VPN](../domain4.md#t4-3-vpn-dx) / **参照:** [プライベート IP VPN](../../../services/network-connectivity.md#vpn-private-ip), [ルートテーブル](../../../services/network-connectivity.md#tgw-route-tables)

### 問10 {#q10}

VPN のトンネルを、新しい方式へ揃えます。AWS 側から接続を開始する要件もあります。IKE のバージョンとして正しいものはどれですか。

- A. IKEv1 と IKEv2 の両方を許可する。AWS からの開始は版を問わない
- B. IKEv1。AWS から開始するには IKEv1 を使う
- C. IKEv2。AWS からの開始にも対応する
- D. IKEv1 のみ。CGW との互換性を優先する

??? success "答えと解説"
    **正解: C**

    IKEv2 を推奨します。

    - A: 誤り。AWS から開始できるのは IKEv2 のみ。
    - B: 誤り。AWS から開始できるのは IKEv2 のみ。
    - C: 正しい。
    - D: 誤り。新しい方式の要件に合わず、AWS からも開始できない。

    **スキル:** [暗号化の方式](../domain4.md#t4-3-ipsec) / **参照:** [トンネルオプション](../../../services/network-connectivity.md#vpn-tunnel-options)

### 問11 {#q11}

VPN の実効 MTU を最大にする暗号方式を選びます。CGW は NAT の背後にありません。正しいものはどれですか。

- A. AES-GCM。NAT-T なしで最大の 1446 まで使える
- B. AES-CBC。ヘッダーが小さいので 1500 まで使える
- C. AES-CBC と SHA2-384。認証の値が長いので 1446 より大きくできる
- D. AES-GCM。DF ビットを立てると 8500 まで使える

??? success "答えと解説"
    **正解: A**

    AES-GCM は MTU の効率がよいです。

    - A: 正しい。
    - B: 誤り。AES-CBC は SHA1 や SHA2-256 でも 1438 で、1500 にはならない。
    - C: 誤り。AES-CBC と SHA2-384 は 1422 で、AES-GCM より小さい。
    - D: 誤り。VPN はジャンボに対応しない。

    **スキル:** [暗号化の方式](../domain4.md#t4-3-ipsec) / **参照:** [トンネルオプション](../../../services/network-connectivity.md#vpn-tunnel-options), [MTU と MSS](../../../services/network-connectivity.md#vpn-mtu)

### 問12 {#q12}

DX の区間に MACsec、インターネットの区間に Site-to-Site VPN を使う設計をレビューします。鍵の管理の手順も確認します。正しいものを選んでください。（2つ選択）

- A. AWS の VPN はトランスポートモードのポリシーベースである
- B. MACsec の SAK は手動でのみローテーションできる
- C. IPsec は IKE で鍵を交換し、ESP で暗号化する
- D. MACsec は L2 のフレームを暗号化し、CKN/CAK は手動で設定する
- E. 事前共有キーの長さは 256 文字まで指定できる

??? success "答えと解説"
    **正解: C, D**

    方式と運用の違いを覚えます。

    - A: 誤り。トンネルモードのルートベース。
    - B: 誤り。SAK は自動でローテーションする。
    - C: 正しい。
    - D: 正しい。
    - E: 誤り。8〜64 文字。

    **スキル:** [暗号化の方式](../domain4.md#t4-3-ipsec) / **参照:** [MACsec](../../../services/network-connectivity.md#dx-macsec), [トンネルオプション](../../../services/network-connectivity.md#vpn-tunnel-options)

### 問13 {#q13}

Client VPN に接続できる利用者が、VPC の DB サーバーへ届きません。Active Directory の認証は成功しています。必要な確認項目として適切なものはどれですか。（2つ選択）

- A. AD の認証を SAML に変更すること
- B. サーバー証明書を無効にすること
- C. 既定の認可ルールで全部が許可されていること
- D. エンドポイントの SG と宛先の SG
- E. エンドポイントのルートと認可ルール

??? success "答えと解説"
    **正解: D, E**

    ルート、認可ルール、SG の 3 つが必要です。

    - A: 誤り。認証は成功している。
    - B: 誤り。サーバー証明書は認証方式に関係なく ACM に必要。
    - C: 誤り。既定では何もなく全部拒否。
    - D: 正しい。
    - E: 正しい。

    **スキル:** [認証と認可](../domain2.md#t2-2-auth) / **参照:** [Client VPN](../../../services/network-connectivity.md#client-vpn), [ID ソース](../../../services/identity-directory.md#idc-identity-sources)

### 問14 {#q14}

Client VPN で、社内の SAML の IdP と連携して利用者を認証します。証明書の配布は最小にしたいと考えています。認証方式の選択として正しいものはどれですか。

- A. SAML のフェデレーション認証を使う
- B. 相互証明書を全端末へ配布する
- C. Active Directory 認証を選び、SAML の IdP を AD として登録する
- D. IAM ロールで端末を認証し、認可ルールで宛先を絞る

??? success "答えと解説"
    **正解: A**

    Client VPN の認証は AD、相互証明書、SAML です。

    - A: 正しい。
    - B: 誤り。証明書の配布が増える。
    - C: 誤り。AD 認証に SAML の IdP は登録できない。
    - D: 誤り。Client VPN の認証は AD、相互証明書、SAML で、IAM ロールの認証はない。

    **スキル:** [認証と認可](../domain2.md#t2-2-auth) / **参照:** [Client VPN](../../../services/network-connectivity.md#client-vpn), [ID ソース](../../../services/identity-directory.md#idc-identity-sources)

### 問15 {#q15}

社内の AD の管理者に、複数の AWS アカウントのネットワークの管理を許可します。AD のアカウントでそのまま認証します。最も適切なサービスの組み合わせはどれですか。

- A. AD のパスワードを IAM ユーザーへ同期して、アカウントごとに作成する
- B. IAM Identity Center と AD を連携し、許可セットを割り当てる
- C. Client VPN の認可ルールで AWS のマネジメントコンソールを許可する
- D. VPC Lattice の認証ポリシーに AD のグループを直接指定する

??? success "答えと解説"
    **正解: B**

    管理操作は Identity Center で統合します。

    - A: 誤り。管理の手間が大きく、長期の認証情報が増える。
    - B: 正しい。
    - C: 誤り。AWS の管理操作の認可にならない。
    - D: 誤り。VPC Lattice はサービスの認可の仕組みで、管理者の認証ではない。

    **スキル:** [認証と認可](../domain2.md#t2-2-auth) / **参照:** [ID ソース](../../../services/identity-directory.md#idc-identity-sources), [VPC Lattice](../../../services/network-connectivity.md#vpc-lattice)

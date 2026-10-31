# ネットワークのセキュリティの問題集

対象の解説: [ネットワーク](../../../services/networking.md)、[Network Firewall](../../../services/threat-detection.md#network-firewall)、[ネットワークの接続](../../../services/network-connectivity.md)

すべてオリジナルの問題で、実際の試験問題ではありません。基準は SCS-C03 です。

### 問1 {#q1}

プライベートサブネットの EC2 が、NAT ゲートウェイ経由で外部へ HTTPS の通信をしています。監査では次を求められました。承認した数個のドメインだけに接続できること。IP アドレスを直接指定した通信や、独自の DNS サーバーを使った接続も止めること。運用の手間も抑えます。最も適切なものはどれですか。

- A. Route 53 Resolver DNS Firewall で承認ドメインだけを許可し、他を `BLOCK` にする
- B. Network Firewall を経路に挟み、ステートフルなドメインリストの許可ルールで他を拒否する
- C. セキュリティグループの送信ルールに、承認ドメインの現在の IP アドレスを列挙する
- D. サブネットのネットワーク ACL で、宛先の 443 番ポートの通信を承認済みの IP アドレスにだけ許可する

??? success "答えと解説"
    **正解: B**

    Network Firewall のドメインリストは TLS の SNI や HTTP の Host で判定し、既定のアクションの順序では一致しない通信を拒否します。DNS を使わない通信も経路上で止められます。

    - A: 誤り。DNS Firewall は VPC Resolver を通る問い合わせだけを見るので、IP の直接指定と独自の DNS サーバーはすり抜ける。
    - B: 正しい。
    - C: 誤り。セキュリティグループはドメインを扱えず、IP の変更に追従する運用の手間もかかる。
    - D: 誤り。NACL も IP 単位で、数の上限があり、ドメインでの制御はできない。

    **スキル:** [3.3.1](../domain3.md#skill-3-3-1) / **参照:** [ルールの評価](../../../services/threat-detection.md#nfw-rules)、[DNS Firewall](../../../services/network-connectivity.md#dns-firewall)

### 問2 {#q2}

Network Firewall を導入し、ステートフルルールグループで不審な宛先を `DROP` にしました。ルールの構文に問題はありませんが、通信は止まらず、アラートログにも何も出ません。ルートテーブルでファイアウォールのエンドポイントは経由しています。原因と修正の組み合わせとして正しいものはどれですか。

- A. ログの配信先が S3 なので遅れている。CloudWatch Logs に変更して確認する
- B. ファイアウォールのサブネットが小さい。CIDR を拡張してエンドポイントを作り直す
- C. ステートレスの既定アクションが `pass` になっている。ステートフルエンジンへ転送する設定にする
- D. ルールグループの容量が不足している。容量の値を変更して上書きする

??? success "答えと解説"
    **正解: C**

    ステートレスの既定アクションが `pass` だと、通信はステートフルエンジンに渡りません。ログもステートフルエンジンに転送された通信だけが対象です。

    - A: 誤り。配信先を変えても、検査されていない通信は記録されない。
    - B: 誤り。サブネットの大きさはこの症状の原因にならない。
    - C: 正しい。
    - D: 誤り。容量の不足ならルールグループの作成でエラーになる。

    **スキル:** [3.3.1](../domain3.md#skill-3-3-1) / **参照:** [ルールの評価](../../../services/threat-detection.md#nfw-rules)、[Network Firewall のログ](../../../services/threat-detection.md#nfw-logging)

### 問3 {#q3}

中央の検査 VPC（10.100.0.0/16）に Network Firewall を置き、Transit Gateway で各 VPC（10.0.0.0/8 の範囲）を接続しました。`$HOME_NET` を送信元にした Suricata のルールが、スポーク VPC の通信に一致しません。ルールを 1 つずつ書き換えたくありません。どう修正しますか。

- A. ポリシーの変数で `HOME_NET` を各 VPC の CIDR を含むように上書きする
- B. ファイアウォールを各スポーク VPC に作り、それぞれの `HOME_NET` を既定のまま使う
- C. `EXTERNAL_NET` にスポークの CIDR を追加し、`HOME_NET` はそのままにする
- D. Transit Gateway の VPC アタッチメントのアプライアンスモードを有効にする

??? success "答えと解説"
    **正解: A**

    ポリシーの `HOME_NET` の既定は検査用 VPC の CIDR です。集中型の構成では、ポリシーの変数で範囲を広げます。

    - A: 正しい。
    - B: 誤り。集中型の検査の構成をやめることになり、費用と運用が増える。
    - C: 誤り。ポリシーの `EXTERNAL_NET` は `HOME_NET` の否定で決まる。
    - D: 誤り。アプライアンスモードは AZ の対称性の設定で、ルールの一致には関係がない。

    **スキル:** [3.3.1](../domain3.md#skill-3-3-1) / **参照:** [Network Firewall の構成](../../../services/threat-detection.md#nfw-architecture)、[ルールの評価](../../../services/threat-detection.md#nfw-rules)

### 問4 {#q4}

既定のアクション順序で運用しているファイアウォールポリシーがあります。チームは、`pass` が他のルールより先に評価されることで検査から漏れる通信を避けるため、厳密な順序にしたいと考えています。稼働中のポリシーの設定画面で変更しようとしましたが、変更できません。正しい対応はどれですか。

- A. Suricata のルールの `priority` キーワードを全ルールに付けると、順序がポリシー全体で厳密になる
- B. 厳密な順序を指定した新しいポリシーを作り、ルールグループを移行してファイアウォールに関連付ける
- C. ファイアウォールを停止するとポリシーの設定を編集できるようになるので、メンテナンス時間に変更する
- D. Firewall Manager の管理者アカウントからだけ変更できるので、管理者に依頼する

??? success "答えと解説"
    **正解: B**

    `RuleOrder` はポリシーの作成時にだけ設定でき、後から編集できません。

    - A: 誤り。アクションの順序の中で優先度を決めるだけで、`pass` が先に評価される仕組みは変わらない。
    - B: 正しい。
    - C: 誤り。そのような編集の手順はない。
    - D: 誤り。誰が操作しても後から変更できない。

    **スキル:** [3.3.1](../domain3.md#skill-3-3-1) / **参照:** [ルールの評価](../../../services/threat-detection.md#nfw-rules)、[ルールの順序](../../../services/network-connectivity.md#nfw-rule-order)

### 問5 {#q5}

重要な決済システムの VPC に DNS Firewall を導入します。可用性の要件が厳しく、DNS Firewall 自体が応答しない場合でも名前解決を続けます。リスクは別の統制で補います。正しい説明と設定はどれですか。

- A. 既定は fail open なので設定は不要で、応答がなければクエリは通過する
- B. 既定は fail closed なので、この VPC の設定で fail open を有効にする
- C. 既定は fail closed なので、ルールのアクションを `ALERT` に変えて検査を外す
- D. 障害時の動作は変更できないので、DNS Firewall の導入を見送り、Network Firewall だけを使う

??? success "答えと解説"
    **正解: B**

    既定は fail closed で、応答がないクエリは `SERVFAIL` で止まります。可用性を優先するなら VPC の設定（`FirewallFailOpen`）を有効にします。

    - A: 誤り。既定は fail closed。
    - B: 正しい。
    - C: 誤り。平常時の検査の効果までなくなり、障害時の動作も変わらない。
    - D: 誤り。fail open は設定で選べる。

    **スキル:** [3.3.1](../domain3.md#skill-3-3-1) / **参照:** [DNS Firewall](../../../services/network-connectivity.md#dns-firewall)

### 問6 {#q6}

パブリックサブネットの NACL に、インバウンドで 443 番の許可と、アウトバウンドで 443 番の許可だけを設定しました。外部の利用者からの HTTPS が失敗します。インスタンスのセキュリティグループは 443 番のインバウンドを許可しています。原因と修正はどれですか。

- A. セキュリティグループに戻り通信の許可がない。アウトバウンドにエフェメラルポートを追加する
- B. NACL はステートフルなので、インバウンドの許可に矛盾する 443 番のアウトバウンドの設定を削除する
- C. NACL の規則番号が小さすぎる。番号を 32767 より大きくすると評価される順序が直る
- D. NACL はステートレスなので、応答用にアウトバウンドのエフェメラルポートを許可する

??? success "答えと解説"
    **正解: D**

    NACL は戻り通信を自動で許可しません。応答はクライアントのエフェメラルポート宛なので、たとえば 1024-65535 をアウトバウンドで許可します。

    - A: 誤り。セキュリティグループはステートフルで、戻りは自動で許可される。
    - B: 誤り。NACL はステートレス。
    - C: 誤り。番号の大小は評価の順番を決めるだけで、原因ではない。
    - D: 正しい。

    **スキル:** [3.3.1](../domain3.md#skill-3-3-1) / **参照:** [NACL のルール](../../../services/networking.md#nacl-rules)、[SG と NACL](../../../services/networking.md#security-groups-nacls)

### 問7 {#q7}

Direct Connect のトランジット VIF で Transit Gateway に接続しています。規制により、オンプレミスと AWS の間を IP 層で暗号化します。公開 IP アドレスは使わず、他社の VPN 機器も増やしません。最も適切なものはどれですか。

- A. Direct Connect の公開 VIF の上に、公開 IP の Site-to-Site VPN を張る
- B. 接続を MACsec に切り替え、ルーターと Direct Connect ロケーションの間を暗号化する
- C. インターネット経由の Site-to-Site VPN を Transit Gateway に張り、Direct Connect は使わない
- D. トランジット VIF の上にプライベート IP の Site-to-Site VPN を張る

??? success "答えと解説"
    **正解: D**

    プライベート IP VPN は Direct Connect の上に IPsec を張り、公開 IP も他社の VPN 機器も使いません。

    - A: 誤り。公開 IP が必要になる。
    - B: 誤り。MACsec はレイヤー 2 の区間の暗号化で、IP 層での暗号化の要件を満たさない。
    - C: 誤り。Direct Connect の経路を使わなくなる。
    - D: 正しい。

    **スキル:** [3.3.2](../domain3.md#skill-3-3-2) / **参照:** [プライベート IP VPN](../../../services/network-connectivity.md#vpn-private-ip)、[オンプレミスとの接続の選び方](../../../services/network-connectivity.md#choosing-hybrid)

### 問8 {#q8}

100 Gbps の Direct Connect 専用接続に MACsec を設定しました。監査は、暗号化されていない通信が流れないことを求めています。ただし、切り替えの当日に接続を止めるリスクは最小限にします。正しい手順はどれですか。

- A. 最初から `must_encrypt` だけで作成して、ルーターの設定を後から合わせる
- B. `no_encrypt` のまま開通し、暗号化は VPN に任せて、MACsec の鍵は関連付けない
- C. 既定の `should_encrypt` で開通し、MACsec のセッションの確立を確認してから `must_encrypt` に変更する
- D. `should_encrypt` のまま運用する。このモードは確立に失敗すると通信を止めるので要件を満たす

??? success "答えと解説"
    **正解: C**

    既定の `should_encrypt` は確立に失敗しても暗号化なしで通信を続けます。確認してから `must_encrypt` にすれば、開通の失敗を避けて要件を満たせます。

    - A: 誤り。確立に失敗すると通信が止まり、当日のリスクが大きい。
    - B: 誤り。100 Gbps の帯域と要件に合わない。
    - C: 正しい。
    - D: 誤り。`should_encrypt` の動作の説明が逆。

    **スキル:** [3.3.2](../domain3.md#skill-3-3-2) / **参照:** [MACsec](../../../services/network-connectivity.md#dx-macsec)

### 問9 {#q9}

ある拠点は 1 Gbps のホスト接続で Direct Connect を使っています。通信を暗号化するため、担当者は MACsec を有効にしようとしましたが、できません。他の拠点は 10 Gbps の専用接続で MACsec を使っています。この拠点の対応として最も適切なものはどれですか。

- A. MACsec は 10、100、400 Gbps の専用接続が対象なので、Direct Connect の上で IPsec VPN を使う
- B. MACsec の鍵を 3 組まで事前に関連付けると、1 Gbps のホスト接続でも有効にできる
- C. MACsec の暗号スイートを `GCM-AES-XPN-256` に変更すると、ホスト接続でも有効にできる
- D. 他の拠点の 10 Gbps の接続を LAG にまとめて、この拠点から MACsec を共有して利用する

??? success "答えと解説"
    **正解: A**

    MACsec の対象は対応する拠点の 10、100、400 Gbps の専用接続です。他の暗号化の手段として IPsec VPN を組み合わせます。

    - A: 正しい。
    - B: 誤り。鍵の数は対象の接続を変えない。
    - C: 誤り。暗号スイートも対象の接続を変えない。
    - D: 誤り。LAG は別の拠点の接続を共有する仕組みではなく、MACsec はリンクの区間の暗号化。

    **スキル:** [3.3.2](../domain3.md#skill-3-3-2) / **参照:** [MACsec](../../../services/network-connectivity.md#dx-macsec)、[オンプレミスとの接続の選び方](../../../services/network-connectivity.md#choosing-hybrid)

### 問10 {#q10}

他社のクラウドと AWS を IPsec でつなぎます。1 トンネルで 3 Gbps を出すことが要件です。現在は VPC に付けた仮想プライベートゲートウェイを使う案が出ています。正しい判断はどれですか。

- A. 既定のトンネルの上限は 5 Gbps なので、仮想プライベートゲートウェイのまま設定を変えずに使える
- B. Large Bandwidth Tunnel は Transit Gateway か Cloud WAN に接続する VPN で使えるので、そちらに接続する
- C. VPN Concentrator を使うと 1 トンネルあたりの帯域を増やせるので、仮想プライベートゲートウェイの前に追加する
- D. VPN のトンネルの上限は変えられないので、IPsec をやめて暗号化なしの接続に変える

??? success "答えと解説"
    **正解: B**

    標準のトンネルは 1.25 Gbps です。Large Bandwidth Tunnel は最大 5 Gbps で、Transit Gateway か Cloud WAN に接続した VPN で使えます。

    - A: 誤り。既定は 1.25 Gbps で、仮想プライベートゲートウェイでは使えない。
    - B: 正しい。
    - C: 誤り。VPN Concentrator のトンネルの帯域は最大 100 Mbps で、小規模の拠点向け。
    - D: 誤り。暗号化の要件を外すことになる。

    **スキル:** [3.3.2](../domain3.md#skill-3-3-2) / **参照:** [トンネルオプション](../../../services/network-connectivity.md#vpn-tunnel-options)、[VPN Concentrator](../../../services/network-connectivity.md#vpn-concentrator)

### 問11 {#q11}

従業員は Client VPN で VPC に入り、社内の Web アプリを使っています。監査で、接続すると VPC の他のシステムへの経路まで持つことを指摘されました。要件は次のとおりです。アプリ単位で許可すること。リクエストごとに利用者と端末の状態を評価すること。利用者に VPN クライアントを求めないこと。何を選びますか。

- A. Client VPN の認可ルールを各アプリのサブネットに絞り、セキュリティグループでアプリのポートだけを許可する
- B. Site-to-Site VPN で本社と VPC をつなぎ、本社の社内ネットワークからだけアプリを使えるようにする
- C. AWS Verified Access を置き、ID と端末の信頼プロバイダーと Cedar のポリシーで評価する
- D. CloudFront の署名付き Cookie をログイン時に発行して、社内のアプリへのアクセスを期限付きで許可する

??? success "答えと解説"
    **正解: C**

    Verified Access は VPN なしで、アプリへのリクエストごとに信頼データを評価します。

    - A: 誤り。VPN クライアントが残り、評価もリクエストごとではない。
    - B: 誤り。拠点のネットワーク全体の接続で、端末や利用者を評価しない。
    - C: 正しい。
    - D: 誤り。署名付き Cookie はコンテンツの配信の許可で、端末の状態を評価しない。

    **スキル:** [3.3.3](../domain3.md#skill-3-3-3) / **参照:** [Verified Access](../../../services/identity-directory.md#verified-access)、[Client VPN](../../../services/network-connectivity.md#client-vpn)

### 問12 {#q12}

AWS Verified Access のインスタンス、信頼プロバイダー、グループ、エンドポイントを作成しました。利用者はログインできますが、すべてのアクセスがブロックされます。アプリは正常に動いていて、エンドポイントのアクセスログには拒否が記録されています。最初に確認すべき点はどれですか。

- A. アクセスログの配信先のバケットで、OCSF の形式を選択しているか
- B. CloudFront の地理的制限でアクセス元の国が拒否されていないか
- C. Client VPN の認可ルールに、利用者のグループが追加されているか
- D. グループかエンドポイントにポリシーが定義されているか

??? success "答えと解説"
    **正解: D**

    グループとエンドポイントはポリシーなしでも作成できますが、ポリシーを定義するまですべてのリクエストがブロックされます。

    - A: 誤り。ログの形式はアクセスの許可に影響しない。
    - B: 誤り。この構成に関わる設定ではない。
    - C: 誤り。Verified Access は Client VPN を使わない。
    - D: 正しい。

    **スキル:** [3.3.3](../domain3.md#skill-3-3-3) / **参照:** [Verified Access](../../../services/identity-directory.md#verified-access)

### 問13 {#q13}

運用者が AWS Verified Access で社内の管理画面に接続します。ID プロバイダーは組織の IAM Identity Center にします。さらに、Web でない PostgreSQL の接続も同じ仕組みに載せます。正しい説明を選んでください。（2つ選択）

- A. 信頼プロバイダーに使う IAM Identity Center は組織インスタンスである必要がある
- B. 信頼プロバイダーに使う IAM Identity Center は、アカウントインスタンスだけが使える
- C. HTTP 以外のアプリには、利用者の端末に Connectivity Client が必要である
- D. HTTP 以外のアプリには対応しないので、PostgreSQL は別途 Client VPN で接続する
- E. 端末の信頼プロバイダーを設定すると、ユーザーの ID の信頼プロバイダーは不要になる

??? success "答えと解説"
    **正解: A, C**

    Identity Center を使うなら組織インスタンスが必要です。HTTP 以外のアプリには Connectivity Client を使います。

    - A: 正しい。
    - B: 誤り。アカウントインスタンスは使えない。
    - C: 正しい。
    - D: 誤り。Connectivity Client で HTTP 以外にも対応する。
    - E: 誤り。端末の情報とユーザーの ID は別の種類の信頼データで、端末だけでは利用者を特定できない。

    **スキル:** [3.3.3](../domain3.md#skill-3-3-3) / **参照:** [Verified Access](../../../services/identity-directory.md#verified-access)

### 問14 {#q14}

Client VPN で VPC A のサブネットに関連付けたエンドポイントがあります。利用者は接続でき、VPC A の一部のサーバーには届きます。ピアリングした VPC B のサーバーには届きません。認可ルールを見ると、VPC A の CIDR だけが許可されています。エンドポイントは分割トンネルです。必要な設定を選んでください。（2つ選択）

- A. Client VPN のルートテーブルに、関連付けたサブネットを経由する VPC B の CIDR のルートを追加する
- B. Client VPN の認可ルールに、VPC B の CIDR を許可するルールを追加する
- C. VPC A の仮想プライベートゲートウェイを Direct Connect に接続し、VPC B へ通信を折り返す
- D. Client VPN の認可ルールで VPC A を拒否して、すべての通信を VPC B に向ける
- E. 利用者の端末に Session Manager のプラグインを追加して、VPC B へのポート転送を行う

??? success "答えと解説"
    **正解: A, B**

    追加のネットワークに届くには、ルートと認可ルールの両方が必要です。VPC のルートは関連付けで自動で追加されますが、ピアリング先は手動です。認可ルールは既定で拒否です。

    - A: 正しい。
    - B: 正しい。
    - C: 誤り。Direct Connect は関係がない。
    - D: 誤り。認可ルールは制限のためのルールではなく、許可だけを書く。
    - E: 誤り。Client VPN の経路の問題の解決にならない。

    **スキル:** [3.3.3](../domain3.md#skill-3-3-3) / **参照:** [Client VPN](../../../services/network-connectivity.md#client-vpn)

### 問15 {#q15}

中央の検査 VPC に他社のステートフルなアプライアンスを置き、Transit Gateway で VPC 間の通信を通しています。AZ が異なる VPC の間の通信だけが断続的に切れます。アプライアンスのログには、戻りの通信が別の AZ の機器に届いて破棄された記録があります。どう修正しますか。

- A. 検査 VPC の Transit Gateway アタッチメントのアプライアンスモードを有効にする
- B. Transit Gateway のルートテーブルの伝播を無効にして、ルートを静的にする
- C. スポーク VPC のセキュリティグループで、戻りのエフェメラルポートを許可する
- D. 各スポーク VPC のサブネットを 1 つの AZ に統一して、全通信を同じ AZ で処理する

??? success "答えと解説"
    **正解: A**

    Transit Gateway は既定で送信元の AZ に留まります。アプライアンスモードを有効にすると、同じフローの行きと戻りで同じ AZ のアタッチメントを使います。

    - A: 正しい。
    - B: 誤り。ルートの作り方で、AZ の対称性は変わらない。
    - C: 誤り。セキュリティグループはステートフルで、アプライアンスでの破棄の説明にならない。
    - D: 誤り。可用性を損ない、根本の解決にもならない。

    **スキル:** [3.3.4](../domain3.md#skill-3-3-4) / **参照:** [アプライアンスモード](../../../services/network-connectivity.md#tgw-appliance-mode)、[検査の配置](../../../services/network-connectivity.md#choosing-inspection)

### 問16 {#q16}

Transit Gateway に本番の VPC 群、開発の VPC 群、共有サービスの VPC がつながっています。要件は、本番と開発がそれぞれ共有サービスと通信でき、本番と開発の間は通信できないことです。既定のルートテーブルで全部を関連付けて伝播している現状を、どう変えますか。

- A. 本番と開発の VPC のセキュリティグループに、相手の CIDR を拒否するルールを追加する
- B. 全部を 1 つの Transit Gateway ルートテーブルに残したまま、ブラックホールのルートを本番の CIDR にだけ追加する
- C. 本番用、開発用、共有サービス用のルートテーブルに分け、共有サービスのルートだけを本番と開発に伝播する
- D. VPC ごとに別の Transit Gateway を作成して、共有サービスだけをピアリングで接続する

??? success "答えと解説"
    **正解: C**

    Transit Gateway のルートテーブルを分け、関連付けと伝播で到達性を決めます。共有サービス用のテーブルには本番と開発の両方を伝播します。

    - A: 誤り。セキュリティグループに拒否のルールはない。
    - B: 誤り。1 つのテーブルでは全 VPC が同じ経路を見て、共有サービスから本番にも届かなくなる。
    - C: 正しい。
    - D: 誤り。分けられるが、費用と運用の負担が過大。

    **スキル:** [3.3.4](../domain3.md#skill-3-3-4) / **参照:** [Transit Gateway のルートテーブル](../../../services/network-connectivity.md#tgw-route-tables)

### 問17 {#q17}

データベースの階層を分離サブネットに置きます。インターネットへの経路は作りません。この階層のバッチは S3 と Secrets Manager を呼びます。もっとも少ない変更で要件を満たす組み合わせはどれですか。

- A. NAT ゲートウェイをパブリックサブネットに置き、ネットワーク ACL で送信先を AWS の IP 範囲に絞る
- B. S3 はゲートウェイエンドポイント、Secrets Manager はインターフェイスエンドポイントを使う
- C. どちらもゲートウェイエンドポイントを使い、ルートテーブルにそれぞれのプレフィックスリストを追加する
- D. インターネットゲートウェイをサブネットのルートに追加して、ポリシーでアクセス先を絞る

??? success "答えと解説"
    **正解: B**

    分離サブネットのままプライベートに接続します。S3 と DynamoDB はゲートウェイ型があり、Secrets Manager はインターフェイス型です。

    - A: 誤り。インターネットへの経路ができる。
    - B: 正しい。
    - C: 誤り。Secrets Manager にゲートウェイエンドポイントはない。
    - D: 誤り。分離の要件に反する。

    **スキル:** [3.3.4](../domain3.md#skill-3-3-4) / **参照:** [エンドポイントの選び方](../../../services/networking.md#endpoint-settings)、[サブネットとルートテーブル](../../../services/networking.md#subnets-route-tables)

### 問18 {#q18}

東西の通信を検査します。既存の他社のファイアウォールのルールと運用を維持し、その製品を AWS でそのまま使います。検査の前後で IP パケットを変更させず、アプライアンスを複数の AZ でスケールさせます。どの方式が合いますか。

- A. Network Firewall のステートフルルールに製品のルールを手で書き直す
- B. WAF のウェブ ACL を Transit Gateway に関連付けて、HTTP の検査で代用する
- C. ALB の背後にファイアウォールを登録して、L7 の通信を順に流す
- D. GWLB と GWLB エンドポイントを使い、他社のアプライアンスをターゲットにする

??? success "答えと解説"
    **正解: D**

    GWLB は他社のアプライアンスを透過的に挟み、スケールと可用性を提供します。マネージドで済ませるなら Network Firewall です。

    - A: 誤り。既存の製品と運用を維持できない。
    - B: 誤り。ウェブ ACL は Transit Gateway に関連付けられない。
    - C: 誤り。ALB は L7 のプロキシで、透過的な検査の方式ではない。
    - D: 正しい。

    **スキル:** [3.3.4](../domain3.md#skill-3-3-4) / **参照:** [GWLB による検査](../../../services/network-connectivity.md#gwlb-inspection)、[検査の配置](../../../services/network-connectivity.md#choosing-inspection)

### 問19 {#q19}

3 層の Web アプリの東西の通信を絞ります。Web 層と AP 層、AP 層と DB 層のサブネットは同じ VPC にあり、インスタンスは Auto Scaling で IP が変わります。IP の管理を増やさずに、必要な通信だけを許可します。最も適切なものはどれですか。

- A. AP 層のセキュリティグループで、Web 層のセキュリティグループを送信元に参照する
- B. 各層のサブネットの NACL に、起動中のインスタンスの IP を自動で追記する Lambda を置く
- C. 各層を別の VPC に分け、VPC ピアリングで全ポートを接続する
- D. WAF のウェブ ACL を各層のインスタンスに直接関連付ける

??? success "答えと解説"
    **正解: A**

    セキュリティグループは他のセキュリティグループを送信元に指定できるので、IP が変わっても維持できます。

    - A: 正しい。
    - B: 誤り。動くが管理する部品が増え、要件に反する。
    - C: 誤り。全ポートの接続では通信を絞れない。
    - D: 誤り。ウェブ ACL は EC2 に直接関連付けられない。

    **スキル:** [3.3.4](../domain3.md#skill-3-3-4) / **参照:** [セキュリティグループのルール](../../../services/networking.md#security-group-rules)、[SG と NACL](../../../services/networking.md#security-groups-nacls)

### 問20 {#q20}

監査で、次の要件の実証を求められました。本番の VPC と開発の VPC の間にネットワークの経路がないこと。インターネットゲートウェイへの全経路に必ず Network Firewall が含まれること。全経路を自分たちの要件として定義し、違反だけを見つけます。何を使いますか。

- A. Inspector のネットワーク到達性を全アカウントで有効にする
- B. Reachability Analyzer で、全インスタンスの組み合わせをそれぞれ 1 組ずつ分析する
- C. Network Access Analyzer のスコープで違反の経路を定義する
- D. IAM Access Analyzer の外部アクセスの分析ツールを組織全体で作成する

??? success "答えと解説"
    **正解: C**

    Network Access Analyzer は、要件を Network Access Scope として定義し、ネットワークの分離や信頼された経路に反する経路を見つけます。

    - A: 誤り。開いた経路を自動で報告するが、自分の要件を定義しない。
    - B: 誤り。1 組ずつの確認で、全経路の要件の検証に向かない。
    - C: 正しい。
    - D: 誤り。IAM ポリシーの分析で、ネットワークの経路は見ない。

    **スキル:** [3.3.5](../domain3.md#skill-3-3-5) / **参照:** [Network Access Analyzer](../../../services/network-connectivity.md#network-access-analyzer)

### 問21 {#q21}

Network Access Analyzer のスコープを作ります。「インターネットゲートウェイから EC2 への経路を検出するが、Network Firewall を通る経路は正当なので結果から外す」という要件です。正しい定義はどれですか。

- A. `ExcludePaths` にインターネットゲートウェイを送信元に書き、`MatchPaths` に Network Firewall を通過点として書く
- B. `MatchPaths` と `ExcludePaths` に同じ内容を書き、片方の結果を手で除外して判断する
- C. `MatchPaths` は使わず、`ExcludePaths` に Network Firewall を書いて他の全経路を結果にする
- D. `MatchPaths` にインターネットゲートウェイから EC2 への経路を書き、`ExcludePaths` に Network Firewall を通る経路を書く

??? success "答えと解説"
    **正解: D**

    検出結果は、`MatchPaths` のいずれかに一致し、`ExcludePaths` のどれにも一致しない経路です。

    - A: 誤り。意味が逆で、違反の経路を除外してしまう。
    - B: 誤り。同じ内容では結果が残らない。
    - C: 誤り。`MatchPaths` が検出の対象を決めるので、省けない。
    - D: 正しい。

    **スキル:** [3.3.5](../domain3.md#skill-3-3-5) / **参照:** [Network Access Analyzer](../../../services/network-connectivity.md#network-access-analyzer)

### 問22 {#q22}

セキュリティチームは、VPC の端から EC2 のポートに届く経路を、スコープを作らずに継続的に見つけて、脆弱性の情報と一緒に確認したいと考えています。対象は EC2 だけです。Lambda と RDS は別の方法で扱います。最も合うものはどれですか。

- A. VPC フローログの `ACCEPT` の行を集計し、開いているポートの一覧を作る
- B. Inspector のネットワーク到達性の検出結果を、脆弱性の検出結果と一緒に確認する
- C. Trusted Advisor のセキュリティのチェックの結果を週に 1 回エクスポートする
- D. Security Lake のカスタムソースに EC2 の設定を取り込み、到達性を問い合わせる

??? success "答えと解説"
    **正解: B**

    Inspector は 12 時間ごとに EC2 のネットワーク到達性を評価し、インターネットゲートウェイなどの VPC の端から届く TCP と UDP のポートを報告します。

    - A: 誤り。実際の通信の記録で、開いている経路をすべて示さない。
    - B: 正しい。
    - C: 誤り。継続的な検出ではなく、同じ観点の結果も得られない。
    - D: 誤り。Security Lake はログの保管で、到達性の評価はしない。

    **スキル:** [3.3.5](../domain3.md#skill-3-3-5) / **参照:** [ネットワーク到達性](../../../services/threat-detection.md#inspector-network)

### 問23 {#q23}

組織の全アカウントで、使われていないセキュリティグループと冗長なセキュリティグループを減らします。自動で修復する前に影響を確認し、組織で一元管理します。どの方法が最も適切ですか。

- A. 各アカウントで Config の `required-tags` ルールを作り、タグのないセキュリティグループを手動で削除する
- B. IAM Access Analyzer の未使用アクセスの分析ツールを作り、未使用のロールとともに削除する
- C. Firewall Manager の使用状況の監査ポリシーを、自動修復を無効にして開始する
- D. VPC フローログに通信のないセキュリティグループを Athena で探し、Lambda で自動で一括削除する

??? success "答えと解説"
    **正解: C**

    Firewall Manager のセキュリティグループのポリシーには、未使用と冗長の整理のための使用状況の監査があります。公式ドキュメントは、自動修復を無効にして影響を確認してから進めるよう案内しています。

    - A: 誤り。タグの有無は未使用を示さず、一元管理にもならない。
    - B: 誤り。IAM の分析で、セキュリティグループは対象外。
    - C: 正しい。
    - D: 誤り。フローログはセキュリティグループの単位ではなく、影響を確認せずに一括で削除してしまう。

    **スキル:** [3.3.5](../domain3.md#skill-3-3-5) / **参照:** [Firewall Manager](../../../services/threat-detection.md#firewall-manager)

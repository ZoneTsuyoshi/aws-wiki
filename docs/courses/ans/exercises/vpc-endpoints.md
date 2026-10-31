# VPC の構成とエンドポイントの問題集

対象の解説: [VPC の基本](../../../services/networking.md#vpc), [VPC エンドポイントと PrivateLink](../../../services/networking.md#vpc-endpoints), [エンドポイントの選び方と制約](../../../services/networking.md#endpoint-settings), [エンドポイントポリシー](../../../services/networking.md#endpoint-policies)

### 問1 {#q1}

アカウント A の API を、NLB の背後からアカウント B の VPC へ PrivateLink で公開します。B はインターフェイスエンドポイントを作りましたが、状態が `pendingAcceptance` のままで通信できません。エンドポイントサービスの許可プリンシパルには B を登録済みです。次に行うことはどれですか。

- A. 利用者のアカウント B でエンドポイントのプライベート DNS を無効にする
- B. 提供者のアカウント A でエンドポイントの接続要求を承認する
- C. A と B の VPC の間に VPC ピアリングを作成して、ピアリング経由で許可する
- D. 利用者のアカウント B のルートテーブルに、A の VPC の CIDR を追加する

??? success "答えと解説"
    **正解: B**

    承認を必須にしたサービスでは、提供者が承認するまで使えません。

    - A: 誤り。接続の承認の状態に影響しない。
    - B: 正しい。
    - C: 誤り。PrivateLink はピアリングを必要としない。
    - D: 誤り。PrivateLink はルートを追加しない。

    **スキル:** [PrivateLink](../domain2.md#t2-2-privatelink) / **参照:** [VPC エンドポイントと PrivateLink](../../../services/networking.md#vpc-endpoints)

### 問2 {#q2}

PrivateLink のエンドポイントサービスを `ap-northeast-1a` と `1c` の NLB で提供しています。利用者の VPC は `1d` のサブネットだけにエンドポイントを作ろうとして、失敗しました。利用者は AZ を増やせません。正しい判断はどれですか。

- A. 利用者の VPC と提供者の VPC の CIDR が重複しているので、CIDR を変更する
- B. 提供者の NLB に `1d` のサブネットを追加し、利用者の AZ と重ねる
- C. 利用者の SG で提供者の NLB の IP を許可する
- D. エンドポイントのプライベート DNS を有効にすれば、別の AZ の NLB へ自動で届く

??? success "答えと解説"
    **正解: B**

    両側の AZ が重なる必要があります。AZ の名前と ID の対応にも注意します。

    - A: 誤り。PrivateLink は CIDR の重複を問題にしない。
    - B: 正しい。
    - C: 誤り。AZ の不一致を解決しない。
    - D: 誤り。DNS の設定で AZ の制約は解決しない。

    **スキル:** [PrivateLink](../domain2.md#t2-2-privatelink) / **参照:** [VPC エンドポイントと PrivateLink](../../../services/networking.md#vpc-endpoints)

### 問3 {#q3}

オンプレミスから DX 経由で、VPC のインターフェイスエンドポイントを使って AWS サービスの API を呼びます。経路は通っていますが、API の名前が公開 IP に解決され、公開の経路を通ってしまいます。VPC ではプライベート DNS を有効にしています。最も適切な対応はどれですか。

- A. オンプレミスの DNS で、サービスの名前をインバウンドエンドポイントへ転送する
- B. オンプレミスの DNS で、VPC の `10.0.0.2` へ転送する
- C. エンドポイントの SG を削除して、名前の解決の制限を解除する
- D. エンドポイントのプライベート DNS を無効にして、公開 DNS に PHZ の値を登録する

??? success "答えと解説"
    **正解: A**

    プライベート DNS は AWS が管理する隠れた PHZ で動きます。オンプレミスからはインバウンドエンドポイント経由で引きます。

    - A: 正しい。
    - B: 誤り。オンプレミスから VPC+2 への転送は非対応。
    - C: 誤り。SG は解決に関係しない。
    - D: 誤り。公開 DNS にプライベート IP を登録する案で、管理も困難。

    **スキル:** [PrivateLink](../domain2.md#t2-2-privatelink) / **参照:** [VPC エンドポイントと PrivateLink](../../../services/networking.md#vpc-endpoints), [ハイブリッド DNS](../../../services/network-connectivity.md#hybrid-dns)

### 問4 {#q4}

提供者の VPC と利用者の VPC は CIDR が重複しています。提供者の 1 つの TCP サービスを、利用者だけに公開し、提供者から利用者へは通信を開始させません。他のリソースは見せません。最も適切なものはどれですか。

- A. Transit Gateway の既定のルートテーブルと 1:1 NAT
- B. 公開 NLB と SG の許可リストでインターネット経由で公開
- C. VPC ピアリングとルートテーブルの絞り込み
- D. NLB とエンドポイントサービスの PrivateLink

??? success "答えと解説"
    **正解: D**

    PrivateLink は公開の範囲が NLB の裏のサービスだけです。

    - A: 誤り。ネットワーク全体の接続で、公開の範囲が広い。
    - B: 誤り。プライベートのアクセスにならない。
    - C: 誤り。CIDR が重複していると作れない。
    - D: 正しい。

    **スキル:** [プライベートアクセス](../domain3.md#t3-1-private-access) / **参照:** [VPC エンドポイントと PrivateLink](../../../services/networking.md#vpc-endpoints), [VPC ピアリング](../../../services/network-connectivity.md#vpc-peering)

### 問5 {#q5}

運用中の PrivateLink で、利用者の一部の接続がタイムアウトします。提供者の NLB のターゲットは 1 台を除いて正常です。利用者側の DNS は正しくプライベート IP を返しています。切り分けとして適切な確認を選んでください。（2つ選択）

- A. 提供者から利用者への通信を許可しているか
- B. NLB のターゲットの正常性とターゲットの SG を確認する
- C. エンドポイントの SG がクライアントからの通信を許可しているか
- D. 利用者の VPC で IGW がアタッチされているか
- E. 利用者のルートテーブルに提供者の VPC の CIDR があるか

??? success "答えと解説"
    **正解: B, C**

    タイムアウトでは SG とターゲットを確認します。

    - A: 誤り。利用者から提供者への方向のみ。
    - B: 正しい。
    - C: 正しい。
    - D: 誤り。PrivateLink に IGW は要らない。
    - E: 誤り。PrivateLink に経路は要らない。

    **スキル:** [プライベートアクセス](../domain3.md#t3-1-private-access) / **参照:** [VPC エンドポイントと PrivateLink](../../../services/networking.md#vpc-endpoints)

### 問6 {#q6}

VPC ピアリングで共有サービスへ接続しています。VPC A が B とピアリングし、B が C とピアリングしています。A から C のサービスへ接続する要件が新しく出ました。最も適切なものはどれですか。

- A. B のルートテーブルに A と C の経路を追加して、B を中継させる
- B. A の SG で C の SG を参照して、経路を不要にする
- C. A と C の間に新しいピアリングを作り、両方のルートテーブルに経路を追加する
- D. B に NAT ゲートウェイを置いて、A から C へ中継させる

??? success "答えと解説"
    **正解: C**

    推移的な通信はできません。

    - A: 誤り。推移的な通信はできない。
    - B: 誤り。経路がないと通信できない。
    - C: 正しい。
    - D: 誤り。ピアリングの推移は NAT でもできない。

    **スキル:** [プライベートアクセス](../domain3.md#t3-1-private-access) / **参照:** [VPC ピアリング](../../../services/network-connectivity.md#vpc-peering)

### 問7 {#q7}

オンプレミスから DX 経由で、S3 へプライベートの IP で接続します。公開 VIF は作れず、VPC にはトランジット VIF で接続しています。最も適切なものはどれですか。

- A. 公開 VIF の代わりに、トランジット VIF で S3 の公開プレフィックスを受信する
- B. S3 のゲートウェイエンドポイントのプレフィックスリストをオンプレミスへ広告する
- C. NAT ゲートウェイを経由して S3 へ接続する
- D. S3 のインターフェイスエンドポイントへ、トランジット VIF の経路で接続する

??? success "答えと解説"
    **正解: D**

    オンプレミスからならインターフェイスエンドポイントです。

    - A: 誤り。トランジット VIF は公開プレフィックスを受信しない。
    - B: 誤り。ゲートウェイエンドポイントは VPC の外から使えない。
    - C: 誤り。公開 IP を経由する。VGW からは通らない。
    - D: 正しい。

    **スキル:** [AWS サービスへのアクセス](../domain3.md#t3-1-access-aws) / **参照:** [エンドポイントの選び方と制約](../../../services/networking.md#endpoint-settings)

### 問8 {#q8}

公開 VIF で S3 へ大量に転送します。受信した経路に、すべてのリージョンの公開プレフィックスが含まれているので、同じリージョンだけに絞ります。ルーターでの対応はどれですか。

- A. AWS のサポートに、経路の広告の削除を依頼する
- B. `7224:7300` の経路だけを受け入れる
- C. オンプレミスから `7224:9100` を AWS から受信する経路に付ける
- D. `7224:8100` の経路だけを受け入れて、同じリージョンに絞る

??? success "答えと解説"
    **正解: D**

    受信した経路のコミュニティで絞ります。

    - A: 誤り。ルーターで絞る。
    - B: 誤り。優先度のコミュニティで、範囲の指定ではない。
    - C: 誤り。オンプレミスからの広告の広がりを制御する値。
    - D: 正しい。

    **スキル:** [AWS サービスへのアクセス](../domain3.md#t3-1-access-aws) / **参照:** [公開 VIF の経路制御](../../../services/network-connectivity.md#bgp-public-vif)

### 問9 {#q9}

規制で「公開 IP を使わず、経路も暗号化する」ことを求められています。オンプレミスから KMS の API を呼びます。DX と Transit Gateway があります。最も適切な構成はどれですか。

- A. インターネットの Site-to-Site VPN と NAT ゲートウェイ
- B. プライベート IP VPN とインターフェイスエンドポイント
- C. 公開 VIF と TLS。API が TLS なので要件をすべて満たす
- D. 公開 VIF の上の VPN

??? success "答えと解説"
    **正解: B**

    経路と公開 IP の両方の要件を確認します。

    - A: 誤り。公開 IP を使い、VGW から NAT へも出られない。
    - B: 正しい。
    - C: 誤り。公開 IP を使う。
    - D: 誤り。公開 IP を使う。

    **スキル:** [AWS サービスへのアクセス](../domain3.md#t3-1-access-aws) / **参照:** [エンドポイントの選び方と制約](../../../services/networking.md#endpoint-settings), [プライベート IP VPN](../../../services/network-connectivity.md#vpn-private-ip)

### 問10 {#q10}

オンプレミスから VPC の NAT ゲートウェイを通ってインターネットへ出す構成を検討しています。今は VGW で VPC に接続しています。正しい説明はどれですか。

- A. VGW 経由では NAT へ出られず、Transit Gateway 経由なら集中型の出口にできる
- B. オンプレミスのルーターで `0.0.0.0/0` を広告すれば NAT へ流れる
- C. VGW 経由で NAT ゲートウェイの ENI へルートを向ければ、どの構成でも出られる
- D. NAT ゲートウェイを公開 VIF に接続すれば、オンプレミスの全通信が NAT で変換される

??? success "答えと解説"
    **正解: A**

    経路の制約です。

    - A: 正しい。
    - B: 誤り。経路の向きが違う。
    - C: 誤り。VGW からは NAT へ出られない。
    - D: 誤り。公開 VIF はそのような接続をしない。

    **スキル:** [VPC のサービス](../domain2.md#t2-1-vpc-services) / **参照:** [NAT ゲートウェイ](../../../services/network-connectivity.md#nat-gateway), [Transit Gateway](../../../services/network-connectivity.md#transit-gateway)

### 問11 {#q11}

IPv6 のみのプライベートサブネットの EC2 からインターネットへ接続します。インターネットからの接続は受けません。最も適切なゲートウェイはどれですか。

- A. インターフェイスエンドポイント。IPv6 の通信をインターネットへ転送する
- B. NAT ゲートウェイ。IPv6 の送信元を変換して受信も止める
- C. VGW。IPv6 の経路をインターネットへ広告する
- D. Egress-only IGW。IPv6 の外向きだけを通す

??? success "答えと解説"
    **正解: D**

    Egress-only IGW は内から外の IPv6 です。

    - A: 誤り。AWS サービスへの接続。
    - B: 誤り。IPv6 の外向きには Egress-only IGW を使う。
    - C: 誤り。VPN と DX の VPC 側の終端。
    - D: 正しい。

    **スキル:** [VPC のサービス](../domain2.md#t2-1-vpc-services) / **参照:** [IPv6 と Egress-only インターネットゲートウェイ](../../../services/network-connectivity.md#ipv6), [VPC の基本](../../../services/networking.md#vpc)

### 問12 {#q12}

プライベートサブネットのバッチが、同じ外部 API へ多数の接続を開いています。接続のエラーが増え、NAT ゲートウェイの設計を見直します。説明として正しいものを選んでください。（2つ選択）

- A. インバウンドの接続を受け付けて、ターゲットへ転送する
- B. `ErrorPortAllocation` が増えたら IP の追加を検討する
- C. 同じ宛先へ IP あたり 55,000 接続が上限である
- D. SG を付けて通信を制限する
- E. 公開 NAT ゲートウェイは IGW のない VPC で使う

??? success "答えと解説"
    **正解: B, C**

    NAT の接続の上限です。

    - A: 誤り。内から外へ。内向きには使えない。
    - B: 正しい。
    - C: 正しい。
    - D: 誤り。NAT ゲートウェイに SG は付かない。
    - E: 誤り。公開 NAT ゲートウェイには IGW が必要。

    **スキル:** [VPC のサービス](../domain2.md#t2-1-vpc-services) / **参照:** [NAT ゲートウェイ](../../../services/network-connectivity.md#nat-gateway)

### 問13 {#q13}

新しい VPC を DHCP オプションセットと一緒に設計します。VPC には既定の DHCP オプションセットがあり、PHZ の名前を引く必要があります。独自の DNS サーバーの要件はありません。設定として最も適切なものはどれですか。

- A. VPC ごとに 2 つの DHCP オプションセットを関連付けて、冗長化する
- B. ドメインネームサーバーを `8.8.8.8` にして、外部の公開 DNS を使う
- C. `AmazonProvidedDNS` のままにして、VPC Resolver で PHZ を解決する
- D. ドメインネームサーバーに、オンプレミスの DNS を設定する

??? success "答えと解説"
    **正解: C**

    独自の DNS サーバーは PHZ の転送の設計が必要です。

    - A: 誤り。VPC に関連付けられるのは 1 つ。
    - B: 誤り。PHZ の名前が引けない。
    - C: 正しい。
    - D: 誤り。PHZ が引けなくなる。

    **スキル:** [単一と複数の VPC](../domain2.md#t2-2-single-multi-vpc) / **参照:** [サブネットとルートテーブル](../../../services/networking.md#subnets-route-tables), [アタッチメント](../../../services/network-connectivity.md#tgw-attachments)

### 問14 {#q14}

同じリージョンの VPC ピアリングで、Web 層の VPC の SG から App 層の VPC の SG を参照したいと考えています。正しい説明はどれですか。

- A. Transit Gateway を使っても常に SG の参照の設定なしで可能になる
- B. 同じリージョンならピアリング先の SG を参照できる
- C. ピアリングでは SG の参照は使えず、NACL のみ使う
- D. 別のリージョンでも相手の SG を参照できる

??? success "答えと解説"
    **正解: B**

    SG の参照の条件です。

    - A: 誤り。既定の動作ではない。
    - B: 正しい。
    - C: 誤り。同じリージョンなら参照できる。
    - D: 誤り。同じリージョンのみ。

    **スキル:** [単一と複数の VPC](../domain2.md#t2-2-single-multi-vpc) / **参照:** [セキュリティグループのルール](../../../services/networking.md#security-group-rules), [セキュリティグループとネットワーク ACL](../../../services/networking.md#security-groups-nacls)

### 問15 {#q15}

Windows のサーバーが多い VPC で、DHCP オプションセットを変更します。IPv6 のみのサブネットの NAT64 と DNS Firewall も併用します。正しいものを選んでください。（2つ選択）

- A. NTP サーバーの既定はオンプレミスのサーバーである
- B. 独自の DNS サーバーを指定しても DNS Firewall は常に効く
- C. 1 つのセットを複数の VPC に関連付けられる
- D. VPC に複数のセットを関連付けられる
- E. NAT64 の DNS64 は VPC Resolver を通るときだけ効く

??? success "答えと解説"
    **正解: C, E**

    DHCP オプションの動作です。

    - A: 誤り。既定は Amazon Time Sync。
    - B: 誤り。VPC Resolver を通るときだけ効く。
    - C: 正しい。
    - D: 誤り。VPC に 1 つ。
    - E: 正しい。

    **スキル:** [単一と複数の VPC](../domain2.md#t2-2-single-multi-vpc) / **参照:** [VPC の DNS 属性](../../../services/networking.md#vpc-dns-attributes), [サブネットとルートテーブル](../../../services/networking.md#subnets-route-tables)

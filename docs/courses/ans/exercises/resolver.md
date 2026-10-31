# VPC Resolver とハイブリッド DNSの問題集

対象の解説: [VPC Resolver](../../../services/network-connectivity.md#vpc-resolver), [エンドポイント](../../../services/network-connectivity.md#resolver-endpoints), [転送ルール](../../../services/network-connectivity.md#resolver-rules), [ハイブリッド DNS](../../../services/network-connectivity.md#hybrid-dns)

### 問1 {#q1}

200 個の VPC を複数のアカウントで運用しています。各 VPC は Transit Gateway で共有サービス VPC とオンプレミスへ接続しています。オンプレミスの `corp.example.com` を全 VPC で解決し、DNS の ENI の費用を最小にします。最も適切な構成はどれですか。

- A. DHCP オプションセットで全 VPC の DNS をオンプレミスのサーバーへ向ける
- B. 共有サービス VPC のアウトバウンドエンドポイントと、RAM で共有した Forward ルール
- C. 全 VPC にアウトバウンドエンドポイントを作り、各アカウントで Forward ルールを個別に作成する
- D. 共有サービス VPC にインバウンドエンドポイントを置き、各 VPC から条件付き転送を設定する

??? success "答えと解説"
    **正解: B**

    エンドポイントは集約し、ルールは RAM で共有します。

    - A: 誤り。PHZ や AWS の名前の解決も壊れ、遅延が増える。
    - B: 正しい。
    - C: 誤り。費用と運用の手間が VPC の数だけ増える。
    - D: 誤り。インバウンドはオンプレミスから AWS への方向で、VPC に条件付き転送の設定はない。

    **スキル:** [ハイブリッドとマルチアカウント](../domain1.md#t1-2-hybrid) / **参照:** [ハイブリッド DNS](../../../services/network-connectivity.md#hybrid-dns), [エンドポイント](../../../services/network-connectivity.md#resolver-endpoints)

### 問2 {#q2}

VPC Resolver のインバウンドエンドポイントの容量を設計します。オンプレミスから UDP で 20,000 QPS の問い合わせがあり、1 つの AZ が停止しても処理を続ける必要があります。IP あたりの上限は 10,000 QPS です。SG の接続追跡が働かない構成とします。最小の IP の数はどれですか。

- A. 2 つの AZ に各 1 個で、合計 2 個
- B. 1 つの AZ に 2 個で、合計 2 個
- C. 2 つの AZ に各 2 個で、合計 4 個
- D. 3 つの AZ に各 3 個で、合計 9 個

??? success "答えと解説"
    **正解: C**

    1 つの AZ が落ちても残りの AZ で 20,000 QPS を処理できる必要があります。

    - A: 誤り。AZ の障害時に 10,000 QPS しか残らない。
    - B: 誤り。AZ の障害に耐えられない。
    - C: 正しい。
    - D: 誤り。必要以上に多い。

    **スキル:** [ハイブリッドとマルチアカウント](../domain1.md#t1-2-hybrid) / **参照:** [エンドポイント](../../../services/network-connectivity.md#resolver-endpoints), [ハイブリッド DNS](../../../services/network-connectivity.md#hybrid-dns)

### 問3 {#q3}

PHZ `aws.example.com` はワークロード VPC にのみ関連付いています。インバウンドエンドポイントは共有サービス VPC にあり、オンプレミスからの条件付き転送も設定済みです。オンプレミスから引くと NXDOMAIN が返ります。経路と SG に問題はありません。対処はどれですか。

- A. インバウンドエンドポイントをアウトバウンドエンドポイントへ変更する
- B. オンプレミスの条件付き転送の先を、ワークロード VPC の VPC+2 へ変更する
- C. PHZ をインバウンドエンドポイントのある共有サービス VPC にも関連付ける
- D. ワークロード VPC とオンプレミスの間に Forward ルールを追加して、PHZ の名前を転送する

??? success "答えと解説"
    **正解: C**

    インバウンドエンドポイントは、自分の VPC の視点で解決します。

    - A: 誤り。向きが逆になる。
    - B: 誤り。オンプレミスから VPC+2 への転送は非対応。
    - C: 正しい。
    - D: 誤り。ルールは VPC から外へ転送する設定で、この問題は解決しない。

    **スキル:** [ハイブリッドとマルチアカウント](../domain1.md#t1-2-hybrid) / **参照:** [ハイブリッド DNS](../../../services/network-connectivity.md#hybrid-dns), [プライベートホストゾーン](../../../services/network-connectivity.md#private-hosted-zones)

### 問4 {#q4}

東京と大阪の VPC を Transit Gateway ピアリングで接続しています。大阪の EC2 が、東京の VPC に関連付けた PHZ の名前を解決できません。大阪のチームは「ピアリングで DNS も届く」と考えていました。最も適切な対応はどれですか。

- A. 東京の VPC の VPC+2 を大阪の DHCP オプションセットに指定する
- B. ピアリングの静的ルートに `169.254.169.253/32` を追加する
- C. Transit Gateway ピアリングのアタッチメントで `DnsSupport` を有効にする
- D. PHZ を大阪の VPC にも関連付けて、大阪の VPC Resolver で解決する

??? success "答えと解説"
    **正解: D**

    Transit Gateway は PHZ の名前を解決しません。PHZ は使う VPC に関連付けます。

    - A: 誤り。別の VPC の VPC+2 を DNS サーバーに使うことはできない。
    - B: 誤り。リンクローカルの範囲で、ルーティングできない。
    - C: 誤り。ピアリングはこの解決に対応しない。
    - D: 正しい。

    **スキル:** [ハイブリッドとマルチアカウント](../domain1.md#t1-2-hybrid) / **参照:** [VPC Resolver](../../../services/network-connectivity.md#vpc-resolver), [ピアリング](../../../services/network-connectivity.md#tgw-peering)

### 問5 {#q5}

公開サイト `example.com` について、権威 DNS への問い合わせの件数と問い合わせ元のリゾルバーの情報を記録して分析します。ログの送信先の設定で正しいものはどれですか。

- A. VPC フローログを有効にし、宛先ポート 53 のレコードを抽出する
- B. Resolver クエリログを有効にし、Firehose で S3 へ送る
- C. 公開 DNS クエリログを有効にし、ゾーンと同じリージョンの S3 バケットへ直接送る
- D. 公開 DNS クエリログを `us-east-1` の CloudWatch Logs へ送る

??? success "答えと解説"
    **正解: D**

    公開 DNS クエリログは `us-east-1` の CloudWatch Logs に送ります。

    - A: 誤り。権威 DNS は自分の VPC の外で、Amazon DNS への通信はフローログに出ない。
    - B: 誤り。Resolver クエリログは VPC の問い合わせのログで、権威 DNS の記録ではない。
    - C: 誤り。公開クエリログの送信先は CloudWatch Logs のみ。
    - D: 正しい。

    **スキル:** [DNS のログと監視](../domain1.md#t1-2-logging) / **参照:** [フローログの分析](../../../services/network-connectivity.md#flow-log-analysis)

### 問6 {#q6}

EC2 が不審なドメインへ問い合わせた疑いがあります。VPC は既定の DNS を使っています。フローログに宛先ポート 53 の記録がほとんどなく、調査が進みません。正しい判断はどれですか。

- A. Traffic Mirroring で対象の ENI の全パケットをコピーし、DNS を抜き出す
- B. フローログが欠落しているので、集約間隔を 1 分へ変更すれば 53 番の記録が出る
- C. 公開 DNS クエリログを有効にして、不審なドメインへの問い合わせを探す
- D. Amazon DNS への問い合わせは記録されないので、Resolver クエリログを使う

??? success "答えと解説"
    **正解: D**

    VPC からの名前解決の調査は Resolver クエリログです。

    - A: 誤り。全 ENI の常時のミラーは費用が大きく、名前の記録なら Resolver クエリログで足りる。
    - B: 誤り。記録の対象外であり、間隔の問題ではない。
    - C: 誤り。自分のゾーンへの問い合わせだけが対象で、他のドメインは記録されない。
    - D: 正しい。

    **スキル:** [DNS のログと監視](../domain1.md#t1-2-logging) / **参照:** [フローログの分析](../../../services/network-connectivity.md#flow-log-analysis)

### 問7 {#q7}

Resolver クエリログを全 VPC で有効にしましたが、同じ EC2 が同じドメインを何度も問い合わせても、ログの件数が想定より少ないです。アプリのログでは毎秒問い合わせています。説明として正しいものはどれですか。

- A. VPC Resolver がキャッシュから答えた問い合わせは、クエリログに記録されない
- B. クエリログの送信先が CloudWatch Logs のとき、同じ名前は 1 分に 1 件へまとめられる
- C. SG で 53 番を許可していない EC2 の問い合わせは記録の対象外になる
- D. クエリログはサンプリング率が 10% に固定されており、変更もできない

??? success "答えと解説"
    **正解: A**

    どちらのクエリログも全件の記録ではありません。キャッシュから答えたものは出ません。

    - A: 正しい。
    - B: 誤り。送信先によるまとめは行われない。
    - C: 誤り。VPC Resolver への問い合わせは SG に影響されず、記録の条件でもない。
    - D: 誤り。そのようなサンプリングの固定はない。

    **スキル:** [DNS のログと監視](../domain1.md#t1-2-logging) / **参照:** [VPC Resolver](../../../services/network-connectivity.md#vpc-resolver)

### 問8 {#q8}

オンプレミスの DNS で `aws.example.com` を AWS へ転送しています。現在は VPC の `10.0.0.2` を転送先にしていますが、解決が不安定です。公式に対応した構成へ改める手順はどれですか。

- A. 公開ホストゾーンに同じ名前を作り、オンプレミスの DNS からインターネット経由で解決する
- B. アウトバウンドエンドポイントを作り、オンプレミスのルールで `aws.example.com` の転送先をその IP に変更する
- C. `10.0.0.2` の SG に、オンプレミスの DNS サーバーからの UDP 53 を許可する
- D. インバウンドエンドポイントを 2 つの AZ に作り、条件付き転送の先をエンドポイントの IP に変更する

??? success "答えと解説"
    **正解: D**

    オンプレミスから VPC+2 への転送は非対応です。

    - A: 誤り。プライベートの名前を公開することになる。
    - B: 誤り。アウトバウンドは VPC からオンプレミスへの方向。
    - C: 誤り。VPC+2 に SG は付けられず、公式に非対応。
    - D: 正しい。

    **スキル:** [名前解決](../domain2.md#t2-1-dns) / **参照:** [ハイブリッド DNS](../../../services/network-connectivity.md#hybrid-dns), [エンドポイント](../../../services/network-connectivity.md#resolver-endpoints)

### 問9 {#q9}

Forward ルールのターゲットとしてオンプレミスの DNS を 3 台指定しました。解決はできますが、ときどき数秒の遅延があります。1 台は保守のためネットワークから切り離されています。最も可能性が高い原因と対処はどれですか。

- A. ルールが PHZ より低い優先度で評価されている。ルールを System に変更して解決する
- B. VPC の `enableDnsHostnames` が `false` で、公開名の解決にフォールバックしている
- C. 到達できないターゲットへの試行で解決が延びている。到達できないターゲットを外すか、経路と SG を確認する
- D. Forward ルールは 2 台までしか使えないので、3 台目が拒否されている。1 台を別のルールへ分ける

??? success "答えと解説"
    **正解: C**

    ターゲットの IP のどれかに届かないと解決が延びます。

    - A: 誤り。System にするとオンプレミスへ転送されなくなる。
    - B: 誤り。問題文の症状とは関係がない。
    - C: 正しい。
    - D: 誤り。問題文の症状の原因にならない。

    **スキル:** [名前解決](../domain2.md#t2-1-dns) / **参照:** [転送ルール](../../../services/network-connectivity.md#resolver-rules)

### 問10 {#q10}

VPC からオンプレミスの `corp.example.com` を引くために、アウトバウンドエンドポイントと Forward ルールを作りました。EC2 から引くと SERVFAIL になります。DX の経路と、オンプレミス側のファイアウォールの許可は確認済みです。確認すべき項目はどれですか。（2つ選択）

- A. VPC に IGW がアタッチされているか
- B. アウトバウンドエンドポイントの SG で、送信の TCP と UDP の 53 を許可しているか
- C. ルールが EC2 の VPC に関連付いているか
- D. インバウンドエンドポイントの SG で受信の 53 を許可しているか
- E. `corp.example.com` の PHZ を VPC に関連付けているか

??? success "答えと解説"
    **正解: B, C**

    アウトバウンド側の SG と、ルールの VPC への関連付けが必要です。

    - A: 誤り。オンプレミスへは DX で転送する。
    - B: 正しい。
    - C: 正しい。
    - D: 誤り。VPC からオンプレミスへの方向では使わない。
    - E: 誤り。オンプレミスの名前なので PHZ は不要。

    **スキル:** [名前解決](../domain2.md#t2-1-dns) / **参照:** [転送ルール](../../../services/network-connectivity.md#resolver-rules), [エンドポイント](../../../services/network-connectivity.md#resolver-endpoints)

### 問11 {#q11}

ECS のタスクが頻繁に増減するマイクロサービスで、呼び出し側は API で正常なインスタンスを取得したいと考えています。カスタム属性（バージョンや環境）で絞り込みも行います。最も適切なサービスはどれですか。

- A. PHZ の加重レコードを更新する Lambda
- B. VPC Resolver の Forward ルールと DHCP オプションセット
- C. AWS Cloud Map の API のみの名前空間と `DiscoverInstances`
- D. 公開ホストゾーンの複数値回答と短い TTL

??? success "答えと解説"
    **正解: C**

    インスタンスの登録、属性、API の発見は Cloud Map の機能です。

    - A: 誤り。運用の手間が大きく、属性の絞り込みもない。
    - B: 誤り。サービスの発見の機能ではない。
    - C: 正しい。
    - D: 誤り。属性で絞り込めず、内部の情報を公開する。

    **スキル:** [名前解決](../domain2.md#t2-2-name-resolution) / **参照:** [プライベートホストゾーン](../../../services/network-connectivity.md#private-hosted-zones)

### 問12 {#q12}

2 つの VPC を接続しています。VPC A の EC2 から VPC B の EC2 の公開 DNS 名を引いたとき、公開 IP でなくプライベート IP を得たいと考えています。接続方法ごとの設定として正しいものはどれですか。（2つ選択）

- A. VPC ピアリングの場合は、ピアリング接続の DNS オプションを有効にする
- B. Transit Gateway の場合は、`DnsSupport` を有効にする
- C. VPC ピアリングの場合は、相手の VPC+2 を DNS サーバーに指定する
- D. どちらの場合も、VPC の `enableDnsSupport` を `false` にする
- E. Transit Gateway の場合は、PHZ を自動で作成するアプライアンスモードを有効にする

??? success "答えと解説"
    **正解: A, B**

    接続方法ごとに、公開 DNS 名をプライベート IP へ解決するオプションがあります。

    - A: 正しい。
    - B: 正しい。
    - C: 誤り。別の VPC の VPC+2 は使わない。
    - D: 誤り。この属性を無効にすると解決が止まる。
    - E: 誤り。アプライアンスモードは流れの対称性の設定。

    **スキル:** [名前解決](../domain2.md#t2-2-name-resolution) / **参照:** [VPC ピアリング](../../../services/network-connectivity.md#vpc-peering), [作成時の設定](../../../services/network-connectivity.md#tgw-options)

### 問13 {#q13}

固定の名前 `db.internal.example.com` を、複数の VPC の EC2 から解決します。名前の変更は月に 1 回で、担当者が手で管理します。ECS のタスクの登録のような自動の登録はありません。最も適切な方式はどれですか。

- A. 各 EC2 の `/etc/hosts` に CloudFormation で書き込む
- B. AWS Cloud Map の HTTP 名前空間に `RegisterInstance` で登録する
- C. PHZ にレコードを作り、使う VPC に関連付ける
- D. Forward ルールで、オンプレミスの DNS に同じ名前のレコードを登録する

??? success "答えと解説"
    **正解: C**

    固定の名前を人が管理するなら Route 53 です。

    - A: 誤り。変更時の配布の手間が大きい。
    - B: 誤り。動的なサービスの発見に向く仕組みで、API を呼ぶ変更もアプリに必要。
    - C: 正しい。
    - D: 誤り。オンプレミスの名前の解決に使う方法。

    **スキル:** [名前解決](../domain2.md#t2-2-name-resolution) / **参照:** [プライベートホストゾーン](../../../services/network-connectivity.md#private-hosted-zones)

### 問14 {#q14}

複数のアカウントの VPC からオンプレミスの名前を解決でき、オンプレミスから各 VPC の PHZ も解決できる構成にします。共有サービス VPC にインバウンドとアウトバウンドのエンドポイントを置きます。次のうち、オンプレミスから各 PHZ を解決するために追加で必要なものはどれですか。

- A. 各 PHZ を共有サービス VPC に関連付け、オンプレミスの DNS で条件付き転送を設定する
- B. 各 VPC のインバウンドエンドポイントの IP を、オンプレミスの DNS のフォワーダーに個別に登録する
- C. 各 VPC に Forward ルールを作成し、オンプレミスの DNS のルートヒントを AWS へ向ける
- D. 各 PHZ の NS をオンプレミスの親のゾーンに登録し、インターネット経由で委任する

??? success "答えと解説"
    **正解: A**

    インバウンドエンドポイントの VPC の視点で解決されるので、PHZ の関連付けが必要です。

    - A: 正しい。
    - B: 誤り。エンドポイントは集約できるので、問題文の構成と合わない。
    - C: 誤り。Forward は外向きのルールで、この方向の解決に使わない。
    - D: 誤り。PHZ はインターネットから解決できない。

    **スキル:** [名前解決でハイブリッド接続](../domain2.md#t2-2-dns-hybrid) / **参照:** [ハイブリッド DNS](../../../services/network-connectivity.md#hybrid-dns)

### 問15 {#q15}

Forward ルールを RAM で組織へ共有しました。新しいアカウントの EC2 からオンプレミスの名前が解決できません。RAM の共有は受け入れ済みです。不足している手順はどれですか。

- A. 共有先のアカウントで、ルールを自分の VPC に関連付けて有効にする
- B. 管理アカウントで、共有先のアカウントの VPC の DHCP オプションセットを変更する
- C. 共有先のアカウントで、ルールのターゲットの IP を編集する
- D. 共有先のアカウントにアウトバウンドエンドポイントを作成する

??? success "答えと解説"
    **正解: A**

    共有されたルールは、共有先で VPC に関連付けて初めて効きます。

    - A: 正しい。
    - B: 誤り。DHCP の変更は不要。
    - C: 誤り。共有されたルールのターゲットは共有先が編集しない。
    - D: 誤り。エンドポイントは共有元の VPC のものが使われる。

    **スキル:** [名前解決でハイブリッド接続](../domain2.md#t2-2-dns-hybrid) / **参照:** [ハイブリッド DNS](../../../services/network-connectivity.md#hybrid-dns)

### 問16 {#q16}

ある VPC が独自の DNS サーバー（EC2）を DHCP オプションセットで使っています。この VPC に関連付けた PHZ の名前を EC2 から引けません。DNS サーバーの再帰問い合わせ先はインターネットです。この VPC の DNS 設計を変えずに解決する方法はどれですか。

- A. DHCP オプションセットを既定に戻し、独自の DNS サーバーを廃止する
- B. DNS サーバーで、プライベートの問い合わせを VPC+2 へ転送する
- C. PHZ のレコードを公開ホストゾーンにも登録して、インターネットから解決する
- D. VPC の `enableDnsSupport` を無効にして、独自の DNS サーバーの再帰を優先させる

??? success "答えと解説"
    **正解: B**

    独自の DNS サーバーを使う VPC は、プライベートの問い合わせを VPC+2 へ転送します。

    - A: 誤り。DNS の設計を変更することになる。
    - B: 正しい。
    - C: 誤り。プライベートの名前を公開してしまう。
    - D: 誤り。VPC Resolver が使えなくなり、PHZ を解決できない。

    **スキル:** [名前解決でハイブリッド接続](../domain2.md#t2-2-dns-hybrid) / **参照:** [ハイブリッド DNS](../../../services/network-connectivity.md#hybrid-dns)

### 問17 {#q17}

オンプレミスからインバウンドエンドポイントを使って PHZ の名前を解決します。ネットワークの経路は通っていますが、問い合わせがタイムアウトします。VPC は自社の所有で、PHZ の関連付けも済んでいます。最も可能性の高い原因はどれですか。

- A. エンドポイントの SG が TCP と UDP の 53 の受信を許可していない
- B. VPC の DHCP オプションセットがオンプレミスの DNS を指していない
- C. エンドポイントの SG が、インターネットへの送信の 53 を許可していない
- D. エンドポイントにアウトバウンドの Forward ルールを関連付けていない

??? success "答えと解説"
    **正解: A**

    インバウンドは受信の 53、アウトバウンドは送信の 53 です。

    - A: 正しい。
    - B: 誤り。インバウンドの解決に DHCP の変更は不要。
    - C: 誤り。インバウンドの要件は受信の 53。
    - D: 誤り。Forward ルールは外向きの解決に使う。

    **スキル:** [エンドポイント](../domain2.md#t2-3-endpoints) / **参照:** [エンドポイント](../../../services/network-connectivity.md#resolver-endpoints)

### 問18 {#q18}

アウトバウンドエンドポイントを作成します。自社で所有する VPC に、既定のテナンシーのものと専有テナンシーのものがあります。高可用性も必要です。最も適切な設計はどれですか。

- A. 専有テナンシーの VPC に、1 つの AZ の IP でエンドポイントを作り、費用を抑える
- B. 共有された VPC のサブネットに、参加者のアカウントからエンドポイントを作る
- C. 既定のテナンシーの自社の VPC に、2 つの AZ の IP でエンドポイントを作る
- D. パブリックサブネットに Elastic IP を付けて作り、オンプレミスへの転送をインターネットのみにする

??? success "答えと解説"
    **正解: C**

    API では IP を最低 2 個、2 つの AZ を推奨します。

    - A: 誤り。専有テナンシーの VPC では使えない。
    - B: 誤り。エンドポイントは自分が所有する VPC に作る。
    - C: 正しい。
    - D: 誤り。Elastic IP は付けない。問題文の要件にも合わない。

    **スキル:** [エンドポイント](../domain2.md#t2-3-endpoints) / **参照:** [エンドポイント](../../../services/network-connectivity.md#resolver-endpoints)

### 問19 {#q19}

VPC からオンプレミスの `example.com` を解決する Forward ルールを使っています。`dev.example.com` だけ NXDOMAIN になります。この VPC には開発チームが作った PHZ `dev.example.com` が関連付いており、`app.dev.example.com` のレコードはありません。原因はどれですか。

- A. DNSSEC 検証で `dev` の署名が失敗して NXDOMAIN に変換された
- B. インバウンドエンドポイントが `dev` の名前を受けていない
- C. Forward ルールのターゲットが `dev` のサブドメインを拒否している
- D. より具体的な PHZ に一致し、その PHZ にレコードがない

??? success "答えと解説"
    **正解: D**

    最も具体的な名前で解決先が決まります。

    - A: 誤り。検証の失敗は SERVFAIL になり、PHZ にも署名がない。
    - B: 誤り。インバウンドはこの方向に関係しない。
    - C: 誤り。問い合わせはオンプレミスに届いていない。
    - D: 正しい。

    **スキル:** [エンドポイント](../domain2.md#t2-3-endpoints) / **参照:** [エンドポイント](../../../services/network-connectivity.md#resolver-endpoints), [プライベートホストゾーン](../../../services/network-connectivity.md#private-hosted-zones)

### 問20 {#q20}

アカウント A の PHZ を、アカウント B の VPC に関連付けます。コンソールの VPC の一覧にアカウント B の VPC は表示されません。正しい手順はどれですか。

- A. A で B の VPC の ID をコンソールに入力して、ゾーンの関連付けを追加する
- B. B で `associate-vpc-with-hosted-zone` を実行するだけで、A の承認は不要である
- C. A が許可を作り、B が `associate-vpc-with-hosted-zone` を実行し、許可を削除する
- D. PHZ を RAM で組織に共有し、B のコンソールで受け入れてから VPC を選択する

??? success "答えと解説"
    **正解: C**

    別のアカウントの VPC との関連付けは CLI か API です。

    - A: 誤り。別アカウントの VPC はコンソールで関連付けられない。
    - B: 誤り。A の許可が必要。
    - C: 正しい。
    - D: 誤り。PHZ の共有は RAM ではない。

    **スキル:** [共有と構成](../domain2.md#t2-3-sharing) / **参照:** [プライベートホストゾーン](../../../services/network-connectivity.md#private-hosted-zones)

### 問21 {#q21}

1,000 個の VPC に、PHZ、Resolver ルール、DNS Firewall のルールグループをまとめて適用したいと考えています。個別の関連付けでは運用が追いつかず、PHZ のゾーンあたりの関連付けの上限も超えます。最も適切なサービスはどれですか。

- A. Route 53 Profiles を RAM で共有し、各 VPC に関連付ける
- B. Firewall Manager の DNS Firewall のポリシーだけで、PHZ も配布する
- C. 共有サービス VPC に PHZ を集め、各 VPC はインバウンドエンドポイントへ DHCP で向ける
- D. CloudFormation StackSets で PHZ と VPC の関連付けをすべて作成する

??? success "答えと解説"
    **正解: A**

    Profiles は PHZ、ルール、DNS Firewall をまとめて多数の VPC へ適用します。

    - A: 正しい。
    - B: 誤り。PHZ やルールは配布できない。
    - C: 誤り。非常に大きな集約点になり、DNS Firewall も適用されない。
    - D: 誤り。上限の問題が解決しない。

    **スキル:** [共有と構成](../domain2.md#t2-3-sharing) / **参照:** [ハイブリッド DNS](../../../services/network-connectivity.md#hybrid-dns)

### 問22 {#q22}

DNS エンドポイントを共有サービス VPC に集約する案と、VPC ごとに置く案を比較しています。集約型の説明として正しいものはどれですか。（2つ選択）

- A. VPC ごとに異なるルールの適用はできなくなる
- B. 各アカウントの DNS Firewall が不要になる
- C. 分離の要件が強いアカウントに最も向いている
- D. 集約点の QPS の容量を見積もる必要がある
- E. ENI の数が減るので費用を抑えられる

??? success "答えと解説"
    **正解: D, E**

    集約型は費用が少なく、集中点の容量に注意します。

    - A: 誤り。ルールの関連付けは VPC ごとに行える。
    - B: 誤り。集約はフィルタリングを置き換えない。
    - C: 誤り。分離の要件が強いなら分散型が向く。
    - D: 正しい。
    - E: 正しい。

    **スキル:** [共有と構成](../domain2.md#t2-3-sharing) / **参照:** [ハイブリッド DNS](../../../services/network-connectivity.md#hybrid-dns), [エンドポイント](../../../services/network-connectivity.md#resolver-endpoints)

### 問23 {#q23}

公開ホストゾーンのクエリログを有効にしようとしたところ、権限のエラーで失敗しました。ロググループは `us-east-1` にあります。正しい対応はどれですか。

- A. クエリログの送信先を S3 にして、バケットポリシーで Route 53 を許可する
- B. ロググループのリソースポリシーで、Route 53 に書き込みを許可する
- C. IAM ロールを Route 53 にアタッチして、CloudWatch Logs への権限を付ける
- D. ロググループの KMS 暗号化を無効にして、ゾーンのリージョンへ移動する

??? success "答えと解説"
    **正解: B**

    リソースポリシーで Route 53 に許可を与えます。

    - A: 誤り。公開クエリログの送信先は CloudWatch Logs のみ。
    - B: 正しい。
    - C: 誤り。Route 53 のクエリログはリソースポリシーで許可する。
    - D: 誤り。公開クエリログのロググループは `us-east-1` のまま。

    **スキル:** [監視とログ](../domain2.md#t2-3-logging) / **参照:** [フローログの分析](../../../services/network-connectivity.md#flow-log-analysis), [Logs Insights でログを検索する](../../../services/observability.md#logs-insights)

### 問24 {#q24}

組織の VPC の DNS の異常を調べます。応答コード `NXDOMAIN` や `SERVFAIL` の多い名前を見つけ、長期のログは費用を抑えて保管します。設計として最も適切なものはどれですか。

- A. CloudTrail のデータイベントで、VPC Resolver の問い合わせをすべて記録する
- B. 公開 DNS クエリログを全ゾーンで有効にして、VPC の問い合わせを記録する
- C. Resolver クエリログを CloudWatch Logs へ送り、Logs Insights で集計する
- D. フローログのカスタム形式に、DNS の応答コードのフィールドを追加して集計する

??? success "答えと解説"
    **正解: C**

    Resolver クエリログ設定を作って VPC に関連付けます。送信先は CloudWatch Logs、S3、Firehose です。

    - A: 誤り。DNS の問い合わせは CloudTrail のイベントではない。
    - B: 誤り。VPC の問い合わせは記録されない。
    - C: 正しい。
    - D: 誤り。フローログにそのフィールドはない。

    **スキル:** [監視とログ](../domain2.md#t2-3-logging) / **参照:** [VPC Resolver](../../../services/network-connectivity.md#vpc-resolver), [Logs Insights でログを検索する](../../../services/observability.md#logs-insights)

### 問25 {#q25}

Route 53 のヘルスチェックの異常を、運用チームへ自動で通知したいと考えています。追加のツールは使いません。最も適切な方法はどれですか。

- A. CloudTrail で `GetHealthCheckStatus` を監視して、EventBridge で通知する
- B. 公開クエリログのメトリクスフィルターで `HEALTHCHECK` を数え、SNS で通知する
- C. `HealthCheckStatus` メトリクスに CloudWatch アラームを設定し、SNS で通知する
- D. Resolver クエリログを Firehose へ送り、Lambda でヘルスチェックの状態を判定する

??? success "答えと解説"
    **正解: C**

    `HealthCheckStatus` のアラームで通知します。CloudWatch のメトリクスは `us-east-1` にあります。

    - A: 誤り。状態の変化は API の呼び出しとして記録されない。
    - B: 誤り。クエリログはヘルスチェックの状態を記録しない。
    - C: 正しい。
    - D: 誤り。VPC の問い合わせのログで状態の情報を持たない。

    **スキル:** [監視とログ](../domain2.md#t2-3-logging) / **参照:** [Route 53 ヘルスチェック](../../../services/networking.md#route53-health-checks), [アラーム](../../../services/observability.md#alarms)

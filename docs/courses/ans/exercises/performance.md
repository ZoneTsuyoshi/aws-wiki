# MTU と性能の最適化の問題集

対象の解説: [MTU とジャンボフレーム](../../../services/network-connectivity.md#mtu), [PMTUD とトラブルシューティング](../../../services/network-connectivity.md#pmtud), [プレイスメントグループ](../../../services/operations.md#placement-groups), [VPC の CIDR](../../../services/network-connectivity.md#vpc-cidr)

### 問1 {#q1}

EC2 から Transit Gateway と Site-to-Site VPN を経由してオンプレミスへ接続しています。SSH は問題ないのに、大きなファイルの転送だけ止まります。EC2 の MTU は 9001 です。最も適切な対応はどれですか。

- A. Transit Gateway の VPC アタッチメントのアプライアンスモードを有効にする
- B. EC2 の SG で ICMP を拒否して、不要なエラーを止める
- C. CGW で TCP の MSS を調整して、経路の実効 MTU に合わせる
- D. VPN のトンネルを増やして帯域を広げ、パケットの損失を減らす

??? success "答えと解説"
    **正解: C**

    VPN は PMTUD に対応しません。実効は最大 1446 です。

    - A: 誤り。経路の対称性の設定で、MTU と関係しない。
    - B: 誤り。ICMP の拒否で状況が悪化する。
    - C: 正しい。
    - D: 誤り。サイズの問題で、帯域の問題ではない。

    **スキル:** [パケットサイズ](../domain3.md#t3-2-mtu) / **参照:** [PMTUD とトラブルシューティング](../../../services/network-connectivity.md#pmtud), [MTU と MSS](../../../services/network-connectivity.md#vpn-mtu)

### 問2 {#q2}

VPC 内の EC2 とインターネットの間で、大きな応答だけが返ってきません。ICMP の Type 3 Code 4 がアプリに返っていないようです。PMTUD が働くようにする修正はどれですか。

- A. NAT ゲートウェイを追加して、ICMP のエラーを変換させる
- B. MTU を 9001 より大きくして、断片の発生を避ける
- C. SG の TCP の受信を全開放して、ICMP のエラーの代わりに使わせる
- D. SG と NACL で ICMP の Type 3 Code 4 を許可する

??? success "答えと解説"
    **正解: D**

    IPv4 は Type 3 Code 4、IPv6 は Packet Too Big を許可します。

    - A: 誤り。NAT の追加は解決にならない。
    - B: 誤り。値を大きくしても解決しない。
    - C: 誤り。ICMP を許可しないと PMTUD は働かない。
    - D: 正しい。

    **スキル:** [パケットサイズ](../domain3.md#t3-2-mtu) / **参照:** [PMTUD とトラブルシューティング](../../../services/network-connectivity.md#pmtud)

### 問3 {#q3}

EC2 が VPC 内の通信で 9001 を使いつつ、DX 経由のオンプレミスへの通信だけで問題が出ています。ICMP は使えず、UDP のアプリも使っています。アプリの変更はできません。最も適切な対応はどれですか。

- A. その宛先の経路だけ MTU を下げる。例: `ip route add ... mtu 1400`
- B. CGW で MSS クランプを設定して、UDP のパケットも小さくする
- C. 全インターフェイスの MTU を 1500 に下げて、VPC 内の性能の低下は受け入れる
- D. `ethtool` で `bw_in_allowance_exceeded` のカウンターを 0 に戻す

??? success "答えと解説"
    **正解: A**

    経路ごとに MTU を指定できます。

    - A: 正しい。
    - B: 誤り。MSS クランプは TCP だけ。
    - C: 誤り。VPC 内の性能が下がる。
    - D: 誤り。帯域の統計で、MTU の対処ではない。

    **スキル:** [パケットサイズ](../domain3.md#t3-2-mtu) / **参照:** [MTU とジャンボフレーム](../../../services/network-connectivity.md#mtu), [PMTUD とトラブルシューティング](../../../services/network-connectivity.md#pmtud)

### 問4 {#q4}

DF を立てて ping で確認します。経路は Transit Gateway の VPC アタッチメント間です。8500 バイトの IP パケットが通るか確かめる `ping -M do -s` の値はどれですか。

- A. `8528`
- B. `8472`
- C. `8492`
- D. `8500`

??? success "答えと解説"
    **正解: B**

    `8500 - IP 20 - ICMP 8 = 8472` です。

    - A: 誤り。ヘッダーを足した値で、指定する値ではない。
    - B: 正しい。
    - C: 誤り。ICMP の 8 バイトしか引いていない。
    - D: 誤り。ヘッダーを含めると 8528 になる。

    **スキル:** [パケットサイズ](../domain3.md#t3-2-mtu) / **参照:** [MTU とジャンボフレーム](../../../services/network-connectivity.md#mtu)

### 問5 {#q5}

トランジット VIF のジャンボフレームを有効にします。既存の接続はまだジャンボに対応していません。本番の通信への影響を見積もっています。正しい説明はどれですか。

- A. MTU を 9001 に更新すると、VIF の通信を中断せずに切り替わる
- B. MTU の変更は BGP のセッションの再確立の次の更新まで適用されない
- C. MTU を 8500 に更新すると、その接続の全 VIF が最大 30 秒中断する
- D. MTU の変更は公開 VIF にも同時に適用され、中断は発生しない

??? success "答えと解説"
    **正解: C**

    変更の時間を計画します。

    - A: 誤り。トランジット VIF は 8500 で、中断もある。
    - B: 誤り。問題文の影響の説明にならない。
    - C: 正しい。
    - D: 誤り。公開 VIF はジャンボに対応しない。

    **スキル:** [フレームサイズ](../domain3.md#t3-3-frames) / **参照:** [MTU とジャンボフレーム](../../../services/network-connectivity.md#mtu)

### 問6 {#q6}

DX のプライベート VIF の MTU を 9001 にしましたが、VPC の EC2 からの `tracepath` は 1500 です。経路は 2 つあり、DX に加えて同じ経路を VPN でも広告しています。VPC の EC2 の MTU は 9001 です。最も可能性の高い原因はどれですか。

- A. `tracepath` は ICMP を使うので、DX では常に 1500 と表示される
- B. プライベート VIF は 1500 固定で、ジャンボにはトランジット VIF が必要になる
- C. 同じ経路を別の MTU の経路でも広告しているので、1500 に下がっている
- D. VPC の EC2 の MTU は 9001 ではジャンボにならず、8500 に下げる必要がある

??? success "答えと解説"
    **正解: C**

    同じ経路を別の MTU の VIF や VPN でも広告していると、1500 に落ちることがあります。

    - A: 誤り。常に 1500 と表示される動作ではない。
    - B: 誤り。プライベート VIF も 9001 に対応する。
    - C: 正しい。
    - D: 誤り。プライベート VIF は 9001 で使える。

    **スキル:** [フレームサイズ](../domain3.md#t3-3-frames) / **参照:** [MTU とジャンボフレーム](../../../services/network-connectivity.md#mtu), [MTU と MSS](../../../services/network-connectivity.md#vpn-mtu)

### 問7 {#q7}

ハイブリッドと VPC 間の経路で、ジャンボフレームの適用範囲を見直しています。接続の種類と MTU の組み合わせのうち、正しいものを選んでください。（2つ選択）

- A. リージョン間の VPC ピアリングは 9001 まで使える
- B. 同じリージョンの VPC ピアリングは 9001 まで使える
- C. DX のトランジット VIF は 8500 に設定できる
- D. DX の公開 VIF は 9001 に設定できる
- E. Site-to-Site VPN は 8500 に設定できる

??? success "答えと解説"
    **正解: B, C**

    公開 VIF と VPN はジャンボに対応しません。

    - A: 誤り。リージョン間は 8500。
    - B: 正しい。
    - C: 正しい。
    - D: 誤り。公開 VIF はジャンボに対応しない。
    - E: 誤り。VPN はジャンボに対応しない。

    **スキル:** [フレームサイズ](../domain3.md#t3-3-frames) / **参照:** [MTU とジャンボフレーム](../../../services/network-connectivity.md#mtu)

### 問8 {#q8}

同じ AZ の 2 台の EC2 の間で、アプリの 1 つの TCP 接続が 5 Gbps で頭打ちです。インスタンスの帯域はずっと大きいです。クラスタープレイスメントグループへの移動はできません。アプリの変更も避けます。最も適切な対応はどれですか。

- A. 対応インスタンスで ENA Express を有効にし、1 フローの上限を上げる
- B. NLB を間に入れて、1 つの TCP 接続を複数のターゲットへ分ける
- C. MTU を 1500 に下げて、CPU の負荷を軽くする
- D. インスタンスのタイプを大きくすることだけで、シングルフローの上限を解除する

??? success "答えと解説"
    **正解: A**

    ENA Express はシングルフローを最大 25 Gbps にします。

    - A: 正しい。
    - B: 誤り。1 つの接続は 1 つのターゲットへ送られる。
    - C: 誤り。シングルフローの上限は解決しない。
    - D: 誤り。インスタンスを大きくしても 5 Gbps の上限は残る。

    **スキル:** [スループット](../domain3.md#t3-3-throughput) / **参照:** [トンネル](../../../services/network-connectivity.md#vpn-tunnels)

### 問9 {#q9}

VPC とオンプレミスの間で 8 Gbps のスループットが必要です。DX はなく、VPN を使います。標準のトンネルで設計します。正しい構成はどれですか。

- A. Transit Gateway に VPN 接続を 7 本つなぎ、静的ルートで ECMP を行う
- B. Transit Gateway に VPN 接続を 4 本つなぎ、BGP と ECMP で束ねる
- C. VGW に VPN 接続を 4 本つなぎ、BGP と ECMP で束ねる
- D. Transit Gateway に VPN 接続を 1 本つなぎ、両トンネルを ECMP で束ねる

??? success "答えと解説"
    **正解: B**

    `8 / 1.25 = 6.4` で 7 本以上のトンネルが要ります。

    - A: 誤り。静的ルートで ECMP はできない。
    - B: 正しい。
    - C: 誤り。VGW は ECMP に対応しない。
    - D: 誤り。2.5 Gbps にしかならない。

    **スキル:** [スループット](../domain3.md#t3-3-throughput) / **参照:** [トンネル](../../../services/network-connectivity.md#vpn-tunnels), [MTU と MSS](../../../services/network-connectivity.md#vpn-mtu)

### 問10 {#q10}

16 vCPU の EC2 で、短時間は高い帯域が出ますが、数分で下がります。インスタンスの仕様は「最大 12.5 Gbps」と書かれています。常時 10 Gbps が必要です。正しい判断はどれですか。

- A. MTU を 9001 から上げて、クレジットの消費を止めて値を維持する
- B. NAT ゲートウェイを通して、インスタンスの上限の代わりに NAT の上限を使う
- C. 「最大」の値は常時保証されるので、OS のチューニングを疑う
- D. ベースラインの帯域が 10 Gbps 以上のインスタンスタイプへ選び直す

??? success "答えと解説"
    **正解: D**

    16 vCPU 以下の「最大」の帯域はクレジット次第です。

    - A: 誤り。MTU を上げてもクレジットは解決しない。
    - B: 誤り。インスタンスの上限は残る。
    - C: 誤り。「最大」はクレジットによるバーストの値。
    - D: 正しい。

    **スキル:** [スループット](../domain3.md#t3-3-throughput) / **参照:** [MTU とジャンボフレーム](../../../services/network-connectivity.md#mtu)

### 問11 {#q11}

緊密に結合した MPI の HPC ジョブを実行します。ノード間の遅延が最大の課題です。すべて 1 つの AZ で動きます。最も適切な構成はどれですか。

- A. Global Accelerator をノード間に挟み、最短の経路を選ぶ
- B. ENA Express と分散プレイスメントグループ。ノードを別々のラックに置いて MPI を高速にする
- C. ENI を複数追加したうえで別の AZ にノードを分散する
- D. EFA とクラスタープレイスメントグループで、OS をバイパスして遅延を下げる

??? success "答えと解説"
    **正解: D**

    OS バイパスの EFA をクラスター配置で使います。

    - A: 誤り。ノード間の通信の用途ではない。
    - B: 誤り。分散は遅延に不利で、MPI の OS バイパスもない。
    - C: 誤り。遅延が大きくなり、MPI の性能が上がらない。
    - D: 正しい。

    **スキル:** [インターフェイス](../domain3.md#t3-3-interfaces) / **参照:** [プレイスメントグループ](../../../services/operations.md#placement-groups)

### 問12 {#q12}

EFA を使う ML のトレーニングで、一部のノードを別の AZ に置いて高可用性を確保する提案があります。EFA の通信についての説明として正しいものはどれですか。

- A. EFA の通信は同じリージョンならルーティングでき、Transit Gateway も経由できる
- B. EFA の通信はピアリングの先の VPC でも使えるが、IP の重複は不可である
- C. EFA の通信はルーティングできず、AZ も VPC も越えられない
- D. EFA with ENA のインターフェイスでは IP 通信もできないので、管理の通信に別の NIC が必要である

??? success "答えと解説"
    **正解: C**

    EFA with ENA なら通常の IP 通信は ENA で通ります。

    - A: 誤り。EFA の通信はルーティングできない。
    - B: 誤り。VPC を越えられない。
    - C: 正しい。
    - D: 誤り。ENA のデバイスで通常の IP 通信はできる。

    **スキル:** [インターフェイス](../domain3.md#t3-3-interfaces) / **参照:** [プレイスメントグループ](../../../services/operations.md#placement-groups)

### 問13 {#q13}

EC2 に別のサブネットへの足を持たせて、管理ネットワークの通信を分離します。性能の要件は特にありません。同じ AZ に管理用のサブネットがあります。選択として正しいものはどれですか。

- A. EFA を追加して OS をバイパスし、管理通信を暗号化する
- B. インスタンスを ENA Express に対応した型に変更すれば足が増える
- C. 同じ AZ の管理サブネットの ENI を追加し、SG も分ける
- D. 別の AZ の管理サブネットの ENI を追加して可用性を高める

??? success "答えと解説"
    **正解: C**

    ENI は SG、IP、MAC を持ち、同じ AZ のインスタンスに付けられます。

    - A: 誤り。EFA の用途ではない。
    - B: 誤り。サブネットの足は増えない。
    - C: 正しい。
    - D: 誤り。ENI は同じ AZ のインスタンスにしか付けられない。

    **スキル:** [インターフェイス](../domain3.md#t3-3-interfaces) / **参照:** [プレイスメントグループ](../../../services/operations.md#placement-groups)

### 問14 {#q14}

インスタンスのネットワークの上限に当たっているか調べます。`ethtool -S` の統計で、接続追跡の上限に当たったときに増えるカウンターはどれですか。

- A. `conntrack_allowance_exceeded`
- B. `bw_in_allowance_exceeded`
- C. `linklocal_allowance_exceeded`
- D. `pps_allowance_exceeded`

??? success "答えと解説"
    **正解: A**

    各カウンターで、どの上限に当たったかを区別します。

    - A: 正しい。
    - B: 誤り。受信の帯域の超過。
    - C: 誤り。リンクローカルの PPS の超過。
    - D: 誤り。PPS の超過。

    **スキル:** [インターフェイス](../domain3.md#t3-3-interfaces) / **参照:** [MTU とジャンボフレーム](../../../services/network-connectivity.md#mtu)

### 問15 {#q15}

VPC の CIDR が `10.0.0.0/16` で、サブネットの IP が枯渇してきました。VPC を止めずに IP を増やします。選択肢のうち正しいものはどれですか。

- A. セカンダリ CIDR `192.168.0.0/16` を追加する
- B. VPC のプライマリ CIDR を `/8` に広げる
- C. `100.64.0.0/16` を追加し、新しいサブネットを作る
- D. 既存のサブネットの CIDR を `/20` に広げる

??? success "答えと解説"
    **正解: C**

    既存のサブネットは変更できないので、追加で対応します。

    - A: 誤り。既存の CIDR が `10.0.0.0/8` の範囲なら、他の RFC 1918 の範囲は追加できない。
    - B: 誤り。既存の CIDR の大きさは変更できない。
    - C: 正しい。
    - D: 誤り。サブネットの CIDR は作成後に変更できない。

    **スキル:** [サブネット](../domain3.md#t3-3-subnets) / **参照:** [VPC の CIDR](../../../services/network-connectivity.md#vpc-cidr)

### 問16 {#q16}

Auto Scaling グループが `/24` のサブネットを 2 つ使っています。最大で AZ あたり 260 台に増やす計画です。ローリング更新もあります。正しい判断はどれですか。

- A. `/24` の利用可能な 251 個では足りないので、より大きなサブネットを AZ ごとに追加する
- B. `/24` は 256 個が全部使えるので、260 台の分に足りないのは 4 台だけで問題は小さい
- C. Auto Scaling グループのサブネットは 1 つだけにしたほうが、IP の消費が減って足りる
- D. サブネットの CIDR を `/23` に変更すれば、既存のインスタンスを止めずに足りる

??? success "答えと解説"
    **正解: A**

    予約を引いた数で計画します。

    - A: 正しい。
    - B: 誤り。予約の 5 個を引くと 251 個。
    - C: 誤り。消費は減らず、可用性が下がる。
    - D: 誤り。サブネットの CIDR は変更できない。

    **スキル:** [サブネット](../domain3.md#t3-3-subnets) / **参照:** [容量の設定](../../../services/ec2-beanstalk.md#asg-capacity), [VPC の CIDR](../../../services/network-connectivity.md#vpc-cidr)

### 問17 {#q17}

複数のアカウントで、IP の枯渇を事前に見つけ、重複しない CIDR を配りたいと考えています。最も適切な方法はどれですか。

- A. Trusted Advisor の VPC のチェックに全部の割り当てを任せる
- B. Network Access Analyzer で望まない経路を探して割り当てを判断する
- C. IPAM で使用状況を監視し、プールから重複しない CIDR を割り当てる
- D. Config のルールで VPC の CIDR の重複を検出して、手動で表計算に記録する

??? success "答えと解説"
    **正解: C**

    IPAM は監視と割り当ての両方を担います。

    - A: 誤り。CIDR の割り当ての機能ではない。
    - B: 誤り。IP の割り当ての機能ではない。
    - C: 正しい。
    - D: 誤り。手動の管理で、枯渇の監視にならない。

    **スキル:** [サブネット](../domain3.md#t3-3-subnets) / **参照:** [IPAM](../../../services/network-connectivity.md#ipam), [VPC の CIDR](../../../services/network-connectivity.md#vpc-cidr)

### 問18 {#q18}

毎月 50 TB の送信があるオンプレミスとの接続を選びます。帯域は安定していて、今後も継続します。受信はほとんどありません。費用の判断として最も適切なものはどれですか。

- A. インターネットの送信は DX より常に安いので、VPN も DX も使わない
- B. DX の受信の料金が大きいので、受信が少ないなら比較するまでもなく VPN を選ぶ
- C. VPN は接続の時間料金だけで送信データの料金がないので、VPN が常に安い
- D. 送信料金の差額がポート料金を上回るかを試算し、回収できるなら DX を選ぶ

??? success "答えと解説"
    **正解: D**

    少量で短期なら VPN、送信が多く安定しているなら DX です。

    - A: 誤り。大量の送信では DX が安くなることが多い。
    - B: 誤り。DX の受信は無料。
    - C: 誤り。VPN にも送信データの料金がある。
    - D: 正しい。

    **スキル:** [費用の低い接続](../domain3.md#t3-3-cost) / **参照:** [データ転送の費用](../../../services/cost-management.md#data-transfer), [オンプレミスとの接続](../../../services/network-connectivity.md#choosing-hybrid)

### 問19 {#q19}

同じリージョンの 2 つの VPC の間で、大量のデータを定常的に転送しています。今は Transit Gateway で接続しており、データ処理料金が大きな割合です。他の VPC との接続は引き続き Transit Gateway を使います。費用を最も下げる方法はどれですか。

- A. 2 つの VPC の間に VPN を張って、Transit Gateway の処理料金を避ける
- B. Transit Gateway ピアリングを同じリージョンで作成して、料金を無料にする
- C. 転送の多い 2 つの VPC の間だけ VPC ピアリングを併用して、処理料金を避ける
- D. Transit Gateway のアタッチメントのサブネットを 1 AZ に減らす

??? success "答えと解説"
    **正解: C**

    ピアリングはデータ転送の料金のみで、時間料金も処理料金もありません。

    - A: 誤り。VPN の料金と帯域の制約が増える。
    - B: 誤り。ピアリングでも処理料金は無料にならない。
    - C: 正しい。
    - D: 誤り。処理料金は通信量で決まる。

    **スキル:** [費用の低い接続](../domain3.md#t3-3-cost) / **参照:** [データ転送の費用](../../../services/cost-management.md#data-transfer), [VPC ピアリング](../../../services/network-connectivity.md#vpc-peering)

### 問20 {#q20}

AWS のネットワーク費用が想定より大きいので、原因を調べます。データ転送、NAT、Transit Gateway の費用の内訳を確認します。最も適切なツールはどれですか。

- A. Network Access Analyzer で望まない経路を探して費用を見積もる
- B. Cost Explorer で使用タイプごとに分解し、費用の大きい項目を見つける
- C. CloudWatch の `TunnelDataOut` を見て請求額を計算する
- D. VPC Reachability Analyzer で経路ごとの料金を表示する

??? success "答えと解説"
    **正解: B**

    使用タイプやリソースで分解できます。

    - A: 誤り。費用の分析の機能ではない。
    - B: 正しい。
    - C: 誤り。特定の VPN の通信量で、費用の全体の内訳ではない。
    - D: 誤り。到達性の解析で、料金は表示しない。

    **スキル:** [費用の低い接続](../domain3.md#t3-3-cost) / **参照:** [Cost Explorer](../../../services/cost-management.md#cost-explorer), [データ転送の費用](../../../services/cost-management.md#data-transfer)

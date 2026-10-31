# VPC の設定と調査の問題集

対象の解説: [VPC の基本](../../../services/networking.md#vpc)、[セキュリティグループとネットワーク ACL](../../../services/networking.md#security-groups-nacls)、[NAT ゲートウェイ](../../../services/network-connectivity.md#nat-gateway)、[接続できないときの切り分け](../../../services/networking.md#vpc-troubleshooting)

### 問1 {#q1}

プライベートサブネットの EC2 からインターネットへ出られません。NAT ゲートウェイはあります。確認する内容として正しいものを選んでください。（2つ選択）

- A. NAT ゲートウェイのセキュリティグループの送信ルール
- B. VPC のサブネットのルートテーブルの `::/0` が Egress-only か
- C. EC2 の Elastic IP の関連付け
- D. プライベートサブネットのルートテーブルの `0.0.0.0/0` が NAT ゲートウェイか
- E. NAT ゲートウェイがパブリックサブネットにあり、そのサブネットの経路が IGW か

??? success "答えと解説"
    **正解: D, E**

    2 つのルートテーブルをそれぞれ確認します。

    - A: 誤り。NAT ゲートウェイにセキュリティグループは付けられない。
    - B: 誤り。IPv6 の設定で、この IPv4 の問題の確認ではない。
    - C: 誤り。プライベートの EC2 に Elastic IP は不要である。
    - D: 正しい。
    - E: 正しい。

    **スキル:** [5.1.1](../domain5.md#skill-5-1-1) / **参照:** [サブネットとルートテーブル](../../../services/networking.md#subnets-route-tables)、[NAT ゲートウェイ](../../../services/network-connectivity.md#nat-gateway)

### 問2 {#q2}

IPv6 の EC2 から外へだけ通信させ、インターネットからの接続は受けたくありません。どれを使いますか。

- A. インターネットゲートウェイ。`::/0` を向ける
- B. VPC ピアリング。相手の VPC の NAT を使う
- C. NAT ゲートウェイを作り、`0.0.0.0/0` と `::/0` の両方を NAT ゲートウェイへ向ける
- D. `::/0` を Egress-only インターネットゲートウェイへ向ける

??? success "答えと解説"
    **正解: D**

    Egress-only インターネットゲートウェイは IPv6 の外向きのみです。

    - A: 誤り。双方向の通信になる。
    - B: 誤り。相手の NAT は使えない。
    - C: 誤り。IPv4 向けの設定である。
    - D: 正しい。

    **スキル:** [5.1.1](../domain5.md#skill-5-1-1) / **参照:** [IPv6 と Egress-only インターネットゲートウェイ](../../../services/network-connectivity.md#ipv6)

### 問3 {#q3}

特定の IP アドレスからの通信だけをサブネットの単位で拒否したいです。どこで設定しますか。

- A. ネットワーク ACL。番号の小さい拒否のルールを追加する
- B. ルートテーブル。その IP への経路を削除する
- C. セキュリティグループ。拒否のルールを追加する
- D. インターネットゲートウェイに拒否のリストを設定して、特定の IP を止める

??? success "答えと解説"
    **正解: A**

    ネットワーク ACL は許可と拒否を持ち、番号の小さい順に評価します。

    - A: 正しい。
    - B: 誤り。通信の拒否の機能ではない。
    - C: 誤り。セキュリティグループは許可のみである。
    - D: 誤り。そのような設定はない。

    **スキル:** [5.1.1](../domain5.md#skill-5-1-1) / **参照:** [ネットワーク ACL のルール](../../../services/networking.md#nacl-rules)、[セキュリティグループのルール](../../../services/networking.md#security-group-rules)

### 問4 {#q4}

インターフェイスエンドポイントのプライベート DNS を使うために、VPC で有効にする属性の組み合わせはどれですか。

- A. DNS 解決のみ
- B. DNS ホスト名のみ
- C. DNS 解決と DNS ホスト名の両方
- D. どちらも無効で、Route 53 のパブリックホストゾーンを使う

??? success "答えと解説"
    **正解: C**

    プライベート DNS には、両方を有効にします。

    - A: 誤り。両方を有効にする。
    - B: 誤り。両方を有効にする。
    - C: 正しい。
    - D: 誤り。プライベート DNS には両方の属性が必要である。

    **スキル:** [5.1.1](../domain5.md#skill-5-1-1) / **参照:** [VPC の DNS 属性](../../../services/networking.md#vpc-dns-attributes)

### 問5 {#q5}

パブリックサブネットの EC2 にインターネットから届きません。IGW と SG は正しいです。確認することはどれですか。

- A. S3 のゲートウェイエンドポイント
- B. EC2 のパブリック IP と NACL のエフェメラルポート
- C. プライベートホストゾーンの関連付け
- D. NAT ゲートウェイの Elastic IP と、プライベートサブネットのルートテーブル

??? success "答えと解説"
    **正解: B**

    インターネットゲートウェイを使うには、パブリック IP も必要です。

    - A: 誤り。インターネットからの受信とは関係がない。
    - B: 正しい。
    - C: 誤り。DNS の設定で、この症状の確認の優先度は低い。
    - D: 誤り。受信の経路に NAT は使わない。

    **スキル:** [5.1.1](../domain5.md#skill-5-1-1) / **参照:** [サブネットとルートテーブル](../../../services/networking.md#subnets-route-tables)

### 問6 {#q6}

プライベートサブネットから S3 へ毎日数 TB を転送し、NAT ゲートウェイの費用が高くなっています。同じリージョンです。どう変えますか。

- A. S3 のインターフェイスエンドポイントを全 AZ に作り、時間とデータ量の料金を払う
- B. NAT ゲートウェイを 2 つに増やし、それぞれのスループットを分ける
- C. Transfer Acceleration を有効にして、エッジ経由で S3 へ送る
- D. S3 のゲートウェイエンドポイントを作り、ルートテーブルに関連付ける

??? success "答えと解説"
    **正解: D**

    ゲートウェイエンドポイントは追加料金がありません。

    - A: 誤り。ゲートウェイ型なら追加料金がない。
    - B: 誤り。処理料金は減らない。
    - C: 誤り。費用は減らず、この要件に合わない。
    - D: 正しい。

    **スキル:** [5.1.4](../domain5.md#skill-5-1-4) / **参照:** [データ転送の費用](../../../services/cost-management.md#data-transfer)、[VPC エンドポイントと PrivateLink](../../../services/networking.md#vpc-endpoints)

### 問7 {#q7}

AZ 間のデータ転送の費用が高いです。a の AZ の NAT ゲートウェイを、b と c の AZ のインスタンスも使っています。可用性も高くしたいです。どう変えますか。

- A. 各 AZ に NAT ゲートウェイを置き、同じ AZ の経路へ変える
- B. b と c の AZ のインスタンスをすべて a の AZ に移す
- C. VPC ピアリングで同じ VPC の AZ 同士を接続する
- D. NAT ゲートウェイを削除し、全インスタンスにパブリック IP を付ける

??? success "答えと解説"
    **正解: A**

    リソースと同じ AZ に NAT を置くと AZ 間の料金を減らせます。

    - A: 正しい。
    - B: 誤り。可用性が下がる。
    - C: 誤り。同じ VPC の中はピアリングの対象ではない。
    - D: 誤り。外部に公開される。

    **スキル:** [5.1.4](../domain5.md#skill-5-1-4) / **参照:** [データ転送の費用](../../../services/cost-management.md#data-transfer)、[NAT ゲートウェイ](../../../services/network-connectivity.md#nat-gateway)

### 問8 {#q8}

パブリック IPv4 の費用が増えています。使用状況を確認して減らしたいです。正しいものを選んでください。（2つ選択）

- A. IPAM で公開 IP の使用状況を確認する
- B. Global Accelerator の固定 IP に置き換えると料金がなくなる
- C. パブリック IPv4 は使用中なら無料なので、未使用だけを確認する
- D. 使っていない Elastic IP を解放し、IPv6 を検討する
- E. NAT ゲートウェイの Elastic IP を増やすと、料金が下がる

??? success "答えと解説"
    **正解: A, D**

    パブリック IPv4 は 1 個あたり 0.005 USD/時です。

    - A: 正しい。
    - B: 誤り。Global Accelerator にも料金がかかる。
    - C: 誤り。使用中も料金がかかる。
    - D: 正しい。
    - E: 誤り。下がらない。

    **スキル:** [5.1.4](../domain5.md#skill-5-1-4) / **参照:** [Elastic IP](../../../services/network-connectivity.md#elastic-ip)、[IPAM](../../../services/network-connectivity.md#ipam)

### 問9 {#q9}

データ転送の料金の説明として正しいものを選んでください。（2つ選択）

- A. AWS からインターネットへの転送は無制限に無料である
- B. AZ 間の転送は送受信の両方で有料である
- C. リージョン間の転送は無料である
- D. インターネットから AWS への受信は無料である
- E. 同じ AZ の中の転送は常に有料である

??? success "答えと解説"
    **正解: B, D**

    経路ごとの料金です。

    - A: 誤り。月 100 GB を超えると有料である。
    - B: 正しい。
    - C: 誤り。送信元で有料である。
    - D: 正しい。
    - E: 誤り。無料である。

    **スキル:** [5.1.4](../domain5.md#skill-5-1-4) / **参照:** [データ転送の費用](../../../services/cost-management.md#data-transfer)

### 問10 {#q10}

プライベートサブネットで NAT 経由の DynamoDB の通信が大半を占めています。インターフェイスエンドポイントではなく何を選びますか。

- A. 別のリージョンの DynamoDB へ接続を変える構成
- B. DynamoDB のゲートウェイエンドポイント
- C. CloudFront のディストリビューションを前に置く構成
- D. Global Accelerator の 2 個の固定 IP を使う構成

??? success "答えと解説"
    **正解: B**

    S3 と DynamoDB にはゲートウェイ型があります。

    - A: 誤り。転送料金が増える。
    - B: 正しい。
    - C: 誤り。API の通信の費用の削減の方法ではない。
    - D: 誤り。NAT の処理料金は減らせない。

    **スキル:** [5.1.4](../domain5.md#skill-5-1-4) / **参照:** [NAT ゲートウェイ](../../../services/network-connectivity.md#nat-gateway)、[VPC エンドポイントと PrivateLink](../../../services/networking.md#vpc-endpoints)

### 問11 {#q11}

VPC フローログに、受信の `ACCEPT` と送信の `REJECT` が並んでいます。セキュリティグループは正しいです。何を直しますか。

- A. ルートテーブルに相手の CIDR のプレフィックスリストを追加して経路を足す
- B. セキュリティグループの送信ルールを追加する
- C. ネットワーク ACL の送信でエフェメラルポートを許可する
- D. NAT ゲートウェイを同じ AZ に移す

??? success "答えと解説"
    **正解: C**

    ネットワーク ACL はステートレスで、戻りの通信を自動で許可しません。

    - A: 誤り。受信は届いているので、経路の問題ではない。
    - B: 誤り。セキュリティグループはステートフルで、戻りは自動で許可される。
    - C: 正しい。
    - D: 誤り。拒否の原因ではない。

    **スキル:** [5.3.1](../domain5.md#skill-5-3-1) / **参照:** [接続できないときの切り分け](../../../services/networking.md#vpc-troubleshooting)

### 問12 {#q12}

本番に影響なく、EC2 からデータベースまでの経路が設定上通るかを確認し、どの設定が止めているかを知りたいです。どれを使いますか。

- A. Reachability Analyzer
- B. VPC フローログで過去の通信を探す機能
- C. Traffic Mirroring で通信のコピーを全量取得して解析する機能
- D. ping を定期的に実行するスクリプトを本番で動かす方法

??? success "答えと解説"
    **正解: A**

    設定を解析するのでパケットを送らず、本番に影響しません。

    - A: 正しい。
    - B: 誤り。実際に流れた通信の記録で、原因の設定は特定できない。
    - C: 誤り。実際の通信のコピーで、設定の解析ではない。
    - D: 誤り。本番で通信を送ることになり、原因の設定も分からない。

    **スキル:** [5.3.1](../domain5.md#skill-5-3-1) / **参照:** [Reachability Analyzer](../../../services/network-connectivity.md#reachability-analyzer)

### 問13 {#q13}

デプロイの直後から、ALB が 503 を返すようになりました。ターゲットのアプリのプロセスは動いています。最も考えられる原因はどれですか。

- A. WAF のルールでブロックされているため
- B. クライアントの TLS のバージョンが古いため
- C. ターゲットの応答が遅く、タイムアウトしているため
- D. 登録済みのターゲットがないか、すべて `unused` のため

??? success "答えと解説"
    **正解: D**

    登録済みのターゲットがないと 503 になります。

    - A: 誤り。WAF のブロックなら 403 である。
    - B: 誤り。503 の説明ではない。
    - C: 誤り。それは 504 の説明である。
    - D: 正しい。

    **スキル:** [5.3.1](../domain5.md#skill-5-3-1) / **参照:** [ALB のエラーコード](../../../services/networking.md#alb-errors)

### 問14 {#q14}

Transit Gateway でつないだ 2 つの VPC の間が通りません。アタッチメントは両方 `available` です。確認するものを選んでください。（2つ選択）

- A. Transit Gateway のセキュリティグループのルール
- B. Transit Gateway のルートテーブルの関連付けと伝播
- C. インターネットゲートウェイの有無
- D. 両方の VPC のルートテーブルの Transit Gateway への経路
- E. 両方の VPC の CIDR が重複しているか。重複しているほうが望ましい

??? success "答えと解説"
    **正解: B, D**

    関連付け、伝播、両方の VPC の経路を確認します。

    - A: 誤り。Transit Gateway にセキュリティグループはない。
    - B: 正しい。
    - C: 誤り。VPC の間の通信には不要である。
    - D: 正しい。
    - E: 誤り。重複すると経路が問題になる。

    **スキル:** [5.3.1](../domain5.md#skill-5-3-1) / **参照:** [ルートテーブル](../../../services/network-connectivity.md#tgw-route-tables)、[アタッチメント](../../../services/network-connectivity.md#tgw-attachments)

### 問15 {#q15}

Transit Gateway の AZ の問題です。検査用の機器を置いた VPC を通ると、一部の通信が切れます。戻りの通信が別の AZ の機器へ行っています。どの設定を変えますか。

- A. `DefaultRouteTableAssociation` を無効にする
- B. アプライアンスモードを有効にする
- C. 検査機器のセキュリティグループを追加する
- D. Route Analyzer を有効にする

??? success "答えと解説"
    **正解: B**

    アプライアンスモードは、通信の往復を同じ AZ に保ちます。

    - A: 誤り。ルートの既定の関連付けの設定である。
    - B: 正しい。
    - C: 誤り。非対称な経路の問題は解決しない。
    - D: 誤り。経路の確認の機能で、通信は変わらない。

    **スキル:** [5.3.1](../domain5.md#skill-5-3-1) / **参照:** [アタッチメント](../../../services/network-connectivity.md#tgw-attachments)、[アプライアンスモード](../../../services/network-connectivity.md#tgw-appliance-mode)

### 問16 {#q16}

NAT ゲートウェイの `ErrorPortAllocation` が増え、同じ宛先への接続に失敗します。どの説明が正しいですか。

- A. セキュリティグループの送信ルールが不足している
- B. NAT ゲートウェイの AZ が障害を起こしている
- C. 同じ宛先への接続が IP あたり 55,000 の上限に達している
- D. VPC のサブネットの CIDR が重複している

??? success "答えと解説"
    **正解: C**

    同じ宛先への同時接続の上限です。

    - A: 誤り。NAT ゲートウェイにセキュリティグループはない。
    - B: 誤り。接続数の上限の問題の説明ではない。
    - C: 正しい。
    - D: 誤り。接続の上限の説明ではない。

    **スキル:** [5.3.1](../domain5.md#skill-5-3-1) / **参照:** [NAT ゲートウェイ](../../../services/network-connectivity.md#nat-gateway)、[接続できないときの切り分け](../../../services/networking.md#vpc-troubleshooting)

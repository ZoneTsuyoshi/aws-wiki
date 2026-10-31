# ネットワーク の問題集

対象の解説: [ネットワーク](../../../services/networking.md)、[ネットワーク接続](../../../services/network-connectivity.md)、[API Gateway](../../../services/api-gateway.md)

### 問1 {#q1}

CloudFront と Global Accelerator の違いの説明として正しいものはどれですか。

- A. CloudFront は VPC を接続し、Global Accelerator はサブネットを作る
- B. CloudFront は DNS の名前解決を行い、Global Accelerator はドメインを登録する
- C. CloudFront はキャッシュで配信し、Global Accelerator は経路を速くする
- D. 両方とも静的なコンテンツをキャッシュする同じサービスである

??? success "答えと解説"
    **正解: C**

    Global Accelerator は固定 IP と AWS 網の経路を提供します。

    - A: 誤り。VPC の接続は Transit Gateway など。
    - B: 誤り。それは Route 53 の役割。
    - C: 正しい。
    - D: 誤り。Global Accelerator はキャッシュしない。

    **スキル:** [ネットワークの全体像](../domain3.md#t3-5-overview) / **参照:** [CloudFront](../../../services/networking.md#cloudfront)、[Global Accelerator](../../../services/network-connectivity.md#global-accelerator)

### 問2 {#q2}

多数の VPC とオンプレミスの VPN を 1 か所で接続したいと考えています。最も適切なサービスはどれですか。

- A. Amazon API Gateway
- B. AWS Transit Gateway
- C. Amazon CloudFront
- D. Amazon Route 53

??? success "答えと解説"
    **正解: B**

    Transit Gateway は VPC や VPN を 1 か所で接続します。

    - A: 誤り。API の作成と公開のサービス。
    - B: 正しい。
    - C: 誤り。コンテンツ配信のサービス。
    - D: 誤り。DNS のサービス。

    **スキル:** [ネットワークの全体像](../domain3.md#t3-5-overview) / **参照:** [Transit Gateway](../../../services/network-connectivity.md#transit-gateway)

### 問3 {#q3}

要件とサービスの組み合わせとして正しいものはどれですか。（2つ選択）

- A. サーバーレスの API の入口を作る: Amazon API Gateway
- B. 論理的に分離された仮想ネットワークを作る: AWS Global Accelerator
- C. 世界共通の固定 IP で高速に届ける: AWS PrivateLink
- D. 世界中に静的コンテンツを速く配信する: Amazon VPC
- E. インターネットを通らずに VPC からサービスへ接続する: AWS PrivateLink

??? success "答えと解説"
    **正解: A, E**

    問題文の要件から、ネットワークのサービスを選びます。

    - A: 正しい。
    - B: 誤り。仮想ネットワークは Amazon VPC。
    - C: 誤り。これは AWS Global Accelerator。
    - D: 誤り。配信は Amazon CloudFront。
    - E: 正しい。

    **スキル:** [ネットワークの全体像](../domain3.md#t3-5-overview) / **参照:** [VPC エンドポイントと PrivateLink](../../../services/networking.md#vpc-endpoints)、[API の種類](../../../services/api-gateway.md#api-types)

### 問4 {#q4}

プライベートサブネットのインスタンスから外へ通信し、外からの接続は受けないようにしたいと考えています。使うものはどれですか。

- A. NAT ゲートウェイ
- B. ネットワーク ACL
- C. Route 53 のホストゾーン
- D. インターネットゲートウェイを直接ルートに指定する

??? success "答えと解説"
    **正解: A**

    NAT ゲートウェイは外へ出るためのもので、外からの接続は受けません。

    - A: 正しい。
    - B: 誤り。通信を制御するもので、外へ出る経路は作らない。
    - C: 誤り。DNS のレコードを管理するもの。
    - D: 誤り。外からも接続できるパブリックサブネットの構成になる。

    **スキル:** [VPC の構成要素](../domain3.md#t3-5-vpc) / **参照:** [サブネットとルートテーブル](../../../services/networking.md#subnets-route-tables)

### 問5 {#q5}

パブリックサブネットの説明として正しいものはどれですか。

- A. 複数のリージョンにまたがって作るサブネット
- B. Multi-AZ の RDS を必ず置くサブネット
- C. NAT ゲートウェイだけを置くことができる特別なサブネット
- D. インターネットゲートウェイへのルートを持つサブネット

??? success "答えと解説"
    **正解: D**

    インターネットゲートウェイへのルートがあれば、パブリックサブネットです。

    - A: 誤り。サブネットは AZ ごとに分ける。
    - B: 誤り。そのような定義ではない。
    - C: 誤り。定義は、インターネットゲートウェイへのルートの有無。
    - D: 正しい。

    **スキル:** [VPC の構成要素](../domain3.md#t3-5-vpc) / **参照:** [サブネットとルートテーブル](../../../services/networking.md#subnets-route-tables)

### 問6 {#q6}

VPC の構成要素と役割の組み合わせとして正しいものはどれですか。（2つ選択）

- A. NAT ゲートウェイ: 外部からの接続を受ける入口
- B. インターネットゲートウェイ: 通信の中身を検査して止める
- C. ルートテーブル: 利用者の ID を管理する
- D. サブネット: VPC を AZ ごとに分けた IP の範囲
- E. ルートテーブル: 宛先ごとの転送先を決める

??? success "答えと解説"
    **正解: D, E**

    構成要素ごとの役割を区別します。

    - A: 誤り。外からの接続は受けない。
    - B: 誤り。VPC とインターネットをつなぐもの。
    - C: 誤り。ID の管理の機能はない。
    - D: 正しい。
    - E: 正しい。

    **スキル:** [VPC の構成要素](../domain3.md#t3-5-vpc) / **参照:** [サブネットとルートテーブル](../../../services/networking.md#subnets-route-tables)

### 問7 {#q7}

特定の攻撃元の IP アドレスをサブネットの単位で拒否したいと考えています。最も適切なものはどれですか。

- A. NAT ゲートウェイ
- B. セキュリティグループ
- C. ルートテーブル
- D. ネットワーク ACL

??? success "答えと解説"
    **正解: D**

    ネットワーク ACL はサブネット単位で、許可と拒否を指定できます。

    - A: 誤り。外へ出るためのもので、拒否のルールはない。
    - B: 誤り。許可のルールだけで、拒否のルールがない。
    - C: 誤り。転送先を決めるもので、拒否のルールはない。
    - D: 正しい。

    **スキル:** [VPC のセキュリティ](../domain3.md#t3-5-vpc-security) / **参照:** [セキュリティグループとネットワーク ACL](../../../services/networking.md#security-groups-nacls)

### 問8 {#q8}

セキュリティグループの説明として正しいものはどれですか。

- A. インスタンス単位で適用され、戻りの通信は自動で許可される
- B. 許可と拒否の両方のルールを書ける
- C. リージョン全体の通信を一括で拒否する機能である
- D. サブネット単位で適用され、戻りの通信の許可が別に必要である

??? success "答えと解説"
    **正解: A**

    セキュリティグループはステートフルです。

    - A: 正しい。
    - B: 誤り。セキュリティグループは許可のみ。
    - C: 誤り。そのような機能ではない。
    - D: 誤り。それはネットワーク ACL の説明。

    **スキル:** [VPC のセキュリティ](../domain3.md#t3-5-vpc-security) / **参照:** [セキュリティグループとネットワーク ACL](../../../services/networking.md#security-groups-nacls)

### 問9 {#q9}

インターネットから EC2 のポートに届く経路があるかを報告してほしいと考えています。最も適切なサービスはどれですか。

- A. ネットワーク ACL
- B. Amazon Inspector
- C. Amazon Macie
- D. AWS Firewall Manager

??? success "答えと解説"
    **正解: B**

    Inspector は問題を見つけるサービスで、通信を止めるものではありません。

    - A: 誤り。通信を制御するもので、経路を報告しない。
    - B: 正しい。
    - C: 誤り。S3 の機密データを検出するサービス。
    - D: 誤り。保護の設定を展開するサービスで、経路の報告は行わない。

    **スキル:** [VPC のセキュリティ](../domain3.md#t3-5-vpc-security) / **参照:** [ネットワーク到達性](../../../services/threat-detection.md#inspector-network)

### 問10 {#q10}

ネットワーク ACL の説明として正しいものはどれですか。（2つ選択）

- A. 戻りの通信にも明示的な許可が必要である
- B. インスタンス単位で適用される
- C. 通信の経路を報告するサービスである
- D. 許可のルールだけを書ける
- E. サブネット単位で適用される

??? success "答えと解説"
    **正解: A, E**

    ネットワーク ACL はステートレスです。

    - A: 正しい。
    - B: 誤り。それはセキュリティグループの説明。
    - C: 誤り。それは Amazon Inspector の説明。
    - D: 誤り。許可と拒否を書ける。
    - E: 正しい。

    **スキル:** [VPC のセキュリティ](../domain3.md#t3-5-vpc-security) / **参照:** [セキュリティグループとネットワーク ACL](../../../services/networking.md#security-groups-nacls)

### 問11 {#q11}

ドメイン名を IP アドレスなどに変換する DNS のサービスはどれですか。

- A. AWS Direct Connect
- B. Amazon VPC
- C. Amazon Route 53
- D. Amazon CloudFront

??? success "答えと解説"
    **正解: C**

    Route 53 は DNS のサービスです。

    - A: 誤り。専用接続のサービス。
    - B: 誤り。仮想ネットワークのサービス。
    - C: 正しい。
    - D: 誤り。コンテンツ配信のサービス。

    **スキル:** [Route 53 の目的](../domain3.md#t3-5-route53) / **参照:** [Route 53](../../../services/networking.md#route53)

### 問12 {#q12}

Amazon Route 53 でできることはどれですか。（2つ選択）

- A. コンテナイメージの保管
- B. S3 オブジェクトのストレージクラスの変更
- C. ドメインの登録
- D. EC2 インスタンスへのパッチの適用
- E. ヘルスチェックに基づいた振り分け

??? success "答えと解説"
    **正解: C, E**

    利用者に近いリージョンや正常なリージョンへの振り分けにも使います。

    - A: 誤り。それは Amazon ECR の役割。
    - B: 誤り。それは S3 のライフサイクルの役割。
    - C: 正しい。
    - D: 誤り。それは Systems Manager の役割。
    - E: 正しい。

    **スキル:** [Route 53 の目的](../domain3.md#t3-5-route53) / **参照:** [Route 53](../../../services/networking.md#route53)、[ルーティングポリシー](../../../services/networking.md#routing-policies)

### 問13 {#q13}

障害の起きたリージョンを避けて、正常なリージョンへ利用者を向けたいと考えています。DNS の段階で行うサービスはどれですか。

- A. AWS Global Accelerator
- B. AWS Direct Connect
- C. Amazon Route 53
- D. Amazon CloudFront

??? success "答えと解説"
    **正解: C**

    Route 53 はヘルスチェックをもとに、正常なリージョンへ振り分けられます。

    - A: 誤り。固定 IP と AWS 網の経路で切り替えるサービスで、DNS の段階ではない。
    - B: 誤り。自社と AWS の専用接続のサービス。
    - C: 正しい。
    - D: 誤り。コンテンツ配信のサービスで、DNS のサービスではない。

    **スキル:** [Route 53 の目的](../domain3.md#t3-5-route53) / **参照:** [ルーティングポリシー](../../../services/networking.md#routing-policies)

### 問14 {#q14}

本社と AWS を今週中に、なるべく費用をかけずに暗号化して接続したいと考えています。最も適切なものはどれですか。

- A. AWS Site-to-Site VPN
- B. AWS Direct Connect
- C. Amazon CloudFront
- D. AWS Client VPN

??? success "答えと解説"
    **正解: A**

    「すぐ接続したい」は VPN です。

    - A: 正しい。
    - B: 誤り。準備に時間がかかる。
    - C: 誤り。コンテンツ配信のサービス。
    - D: 誤り。個々の端末からの接続で、拠点の接続ではない。

    **スキル:** [AWS への接続方法](../domain3.md#t3-5-connectivity) / **参照:** [Site-to-Site VPN](../../../services/network-connectivity.md#site-to-site-vpn)

### 問15 {#q15}

大量のデータを送るので、安定した帯域と遅延がほしいと考えています。最も適切なものはどれですか。

- A. AWS Site-to-Site VPN
- B. AWS Direct Connect
- C. AWS Client VPN
- D. インターネットゲートウェイ

??? success "答えと解説"
    **正解: B**

    Direct Connect は専用の接続です。

    - A: 誤り。インターネット上のトンネルなので、帯域と遅延が安定しにくい。
    - B: 正しい。
    - C: 誤り。個々の端末からの接続のサービス。
    - D: 誤り。VPC とインターネットをつなぐもの。

    **スキル:** [AWS への接続方法](../domain3.md#t3-5-connectivity) / **参照:** [Direct Connect](../../../services/network-connectivity.md#direct-connect)

### 問16 {#q16}

在宅勤務の社員の端末を VPC に接続したいと考えています。最も適切なものはどれですか。

- A. AWS Transit Gateway
- B. AWS Site-to-Site VPN
- C. AWS Direct Connect
- D. AWS Client VPN

??? success "答えと解説"
    **正解: D**

    Client VPN は利用者の端末からの VPN です。

    - A: 誤り。VPC や VPN を 1 か所で接続するサービスで、端末からの接続の手段ではない。
    - B: 誤り。拠点と AWS の接続のサービス。
    - C: 誤り。拠点と AWS の専用接続のサービス。
    - D: 正しい。

    **スキル:** [AWS への接続方法](../domain3.md#t3-5-connectivity) / **参照:** [Client VPN](../../../services/network-connectivity.md#client-vpn)

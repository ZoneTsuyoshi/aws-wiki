# マルチ VPC とマルチアカウントの問題集

対象の解説: [VPC 同士の接続](../../../services/network-connectivity.md#choosing-multi-vpc), [AWS Resource Access Manager](../../../services/governance.md#ram), [VPC サブネットの共有](../../../services/governance.md#ram-vpc-sharing), [1:1 NAT](../../../services/network-connectivity.md#tgw-nat)

### 問1 {#q1}

SaaS の事業者が API を多数の顧客の VPC へ公開します。顧客の CIDR は事業者と重複することがあり、通信の開始は常に顧客側です。事業者は顧客の VPC に通信を開始してはなりません。最も適切な接続はどれですか。

- A. 顧客を共有の Transit Gateway にアタッチし、1:1 NAT で重複を変換して接続する
- B. Global Accelerator の固定 IP を公開し、顧客の NAT からインターネット経由で受ける
- C. 顧客ごとに VPC ピアリングを作り、ルートテーブルで API のサブネットだけを許可する
- D. NLB の背後のサービスをエンドポイントサービスにして PrivateLink で公開する

??? success "答えと解説"
    **正解: D**

    PrivateLink は利用者から提供者へのみで、CIDR の重複も問題になりません。

    - A: 誤り。動作はするが事業者から顧客への経路もでき、設定も大きい。
    - B: 誤り。プライベートの接続にならない。
    - C: 誤り。CIDR が重複すると作成できず、通信は両方向に可能になる。
    - D: 正しい。

    **スキル:** [接続パターン](../domain1.md#t1-6-patterns) / **参照:** [VPC 同士の接続](../../../services/network-connectivity.md#choosing-multi-vpc)

### 問2 {#q2}

20 の VPC にまたがるマイクロサービスで、サービス単位の接続と IAM の認可を使います。一部の VPC は CIDR が重複します。ネットワーク全体の接続は不要で、ネットワークチームの作業も減らしたいと考えています。最も適切なものはどれですか。

- A. VPC ピアリングのメッシュと SG の参照でサービスごとに制御する
- B. PrivateLink のエンドポイントサービスをサービスと利用者の全組み合わせで作る
- C. VPC Lattice のサービスネットワークと認証ポリシーでサービス単位に接続する
- D. Transit Gateway のルートテーブルを VPC ごとに分けて、SG で認可する

??? success "答えと解説"
    **正解: C**

    Lattice はサービス単位で接続し、CIDR の重複も問題ありません。

    - A: 誤り。重複すると作れず、本数も増える。
    - B: 誤り。動作はするが、組み合わせの数だけ作業が増え IAM の認可もない。
    - C: 正しい。
    - D: 誤り。CIDR の重複が問題になり、サービス単位の IAM の認可もない。

    **スキル:** [接続パターン](../domain1.md#t1-6-patterns) / **参照:** [VPC 同士の接続](../../../services/network-connectivity.md#choosing-multi-vpc), [VPC Lattice](../../../services/network-connectivity.md#vpc-lattice)

### 問3 {#q3}

10 個の VPC が相互に通信し、今後も増える見込みです。ネットワークチームはオンプレミスの接続も集約したいと考えています。メッシュのピアリングの本数と、適切な判断の組み合わせはどれですか。

- A. 90 本。ピアリングは VPC ごとに要求と承認で別々に数えるので、Transit Gateway へ集約する
- B. 10 本。隣の VPC を経由して推移で届くので、リング状に接続すれば足りる
- C. 45 本。増える前提でオンプレミスも集約するなら、Transit Gateway を使う
- D. 45 本。ピアリングの先のオンプレミスにも推移で届くので、メッシュのままでよい

??? success "答えと解説"
    **正解: C**

    `n(n-1)/2` です。

    - A: 誤り。1 本は 2 つの VPC で共有するので `10 × 9 / 2 = 45`。
    - B: 誤り。推移はできない。
    - C: 正しい。
    - D: 誤り。推移はできない。

    **スキル:** [接続パターン](../domain1.md#t1-6-patterns) / **参照:** [VPC ピアリング](../../../services/network-connectivity.md#vpc-peering), [Transit Gateway](../../../services/network-connectivity.md#transit-gateway)

### 問4 {#q4}

5 つのアプリチームをアカウントで分け、請求も分けます。ネットワークは中央のチームが管理し、アプリ同士は同じ信頼の境界で密に通信します。VPC の数と AZ 間以外のデータ処理料金も増やしたくありません。最も適切な設計はどれですか。

- A. アカウントごとに VPC を作り Transit Gateway へアタッチして、中央のアカウントがルートを管理する
- B. 中央のアカウントの VPC のサブネットを RAM で共有し、各チームが自分のアカウントで使う
- C. 中央のアカウントに全アプリを置いて、コスト配分タグで請求を分ける
- D. アカウントごとに VPC を作りピアリングのメッシュで接続して、中央のアカウントが承認する

??? success "答えと解説"
    **正解: B**

    同じ VPC の中の通信で、請求とアクセス権限だけをアカウントで分けます。

    - A: 誤り。VPC が増え、データ処理料金もかかる。
    - B: 正しい。
    - C: 誤り。アカウントを分ける要件に合わない。
    - D: 誤り。VPC が増え、管理も分散する。

    **スキル:** [VPC 共有](../domain1.md#t1-6-vpc-sharing) / **参照:** [VPC サブネットの共有](../../../services/governance.md#ram-vpc-sharing)

### 問5 {#q5}

VPC 共有の参加者のアプリチームが、共有サブネットで作業します。参加者のアカウントでできることを選んでください。（2つ選択）

- A. 共有サブネットのルートテーブルに、ピアリング先の経路を追加する
- B. 共有サブネットの NACL に、アプリのポートの許可を追加する
- C. 共有 VPC に NAT ゲートウェイを作成して、自分の費用で使う
- D. 共有サブネットに EC2 を作り、自分の SG を付ける
- E. 自分の ENI のフローログを作成する

??? success "答えと解説"
    **正解: D, E**

    権限の分担を覚えます。

    - A: 誤り。オーナーが管理する。参加者は参照のみ。
    - B: 誤り。オーナーが管理する。参加者は参照のみ。
    - C: 誤り。参加者は NAT を作成も参照もできない。
    - D: 正しい。
    - E: 正しい。

    **スキル:** [VPC 共有](../domain1.md#t1-6-vpc-sharing) / **参照:** [VPC サブネットの共有](../../../services/governance.md#ram-vpc-sharing)

### 問6 {#q6}

オーナーのアカウントが RAM でサブネットを共有しようとしましたが、組織を共有先に選べません。オーナーと参加者は同じ組織にあります。Organizations のすべての機能は有効です。次に確認するものはどれですか。

- A. オーナーのアカウントで Transit Gateway の自動承認が有効か
- B. 管理アカウントで RAM の組織の共有が有効になっているか
- C. 参加者のアカウントで VPC のピアリングが承認済みか
- D. 参加者のアカウントで AWS Config が有効か

??? success "答えと解説"
    **正解: B**

    組織の共有は管理アカウントで有効にします。

    - A: 誤り。Transit Gateway の設定で、サブネットの共有の前提ではない。
    - B: 正しい。
    - C: 誤り。VPC 共有にピアリングは使わない。
    - D: 誤り。Firewall Manager の前提で、RAM の共有の前提ではない。

    **スキル:** [VPC 共有](../domain1.md#t1-6-vpc-sharing) / **参照:** [VPC サブネットの共有](../../../services/governance.md#ram-vpc-sharing), [AWS Resource Access Manager](../../../services/governance.md#ram)

### 問7 {#q7}

VPC（`10.0.0.0/16`）がオンプレミスと重複しています。VPC からオンプレミスのサーバーへの接続が必要で、逆方向の接続はありません。VPC の作り直しはできず、Transit Gateway はあります。最も適切な方法はどれですか。

- A. パブリック NAT ゲートウェイと IGW で、オンプレミスの公開 IP を経由させる
- B. 重複しないセカンダリ CIDR にプライベート NAT を置き、その IP で接続する
- C. オンプレミスの経路を `10.0.0.0/8` に集約して、VPC のルートで最長一致に任せる
- D. インターフェイスエンドポイントを作成し、オンプレミスのサーバーの名前を指定する

??? success "答えと解説"
    **正解: B**

    相手には NAT の IP が見えます。

    - A: 誤り。プライベートの経路にならず、公開 IP も必要になる。
    - B: 正しい。
    - C: 誤り。`local` が優先され、重複は解決しない。
    - D: 誤り。AWS サービスやエンドポイントサービスへの接続で、問題文の方向に使えない。

    **スキル:** [IP の重複](../domain1.md#t1-6-overlap) / **参照:** [NAT ゲートウェイ](../../../services/network-connectivity.md#nat-gateway), [VPC の CIDR](../../../services/network-connectivity.md#vpc-cidr)

### 問8 {#q8}

買収した会社の VPC と CIDR が重複しています。ネットワーク全体で両方向に通信する必要があり、アドレスの付け替えは 1 年後です。Transit Gateway の 1:1 NAT を検討しています。制約として正しいものはどれですか。

- A. 設定がなくても重複を Transit Gateway が検出して自動で変換する
- B. 変換前より短いプレフィックスへ集約でき、IPv6 にも使える
- C. 片方向の接続のみで、戻りの接続は受けられない
- D. 変換前後でプレフィックス長が同じで、IPv4 のみ

??? success "答えと解説"
    **正解: D**

    片方向で足りるならプライベート NAT も候補です。

    - A: 誤り。設定が必要。
    - B: 誤り。同じ長さで、IPv4 のみ。
    - C: 誤り。両方向に対応する。
    - D: 正しい。

    **スキル:** [IP の重複](../domain1.md#t1-6-overlap) / **参照:** [1:1 NAT](../../../services/network-connectivity.md#tgw-nat)

### 問9 {#q9}

組織の各アカウントが VPC を自由に作っており、重複の問題が繰り返されています。今後の VPC の重複を防ぎ、使用状況も把握します。各アカウントは IaC で VPC を作ります。最も適切な方法はどれですか。

- A. Config のルールで重複を検出し、重複した VPC を削除する
- B. 重複したらプライベート NAT で回避すると方針を決め、全 VPC に置く
- C. Network Access Analyzer のスコープで CIDR の重複を確認して通知する
- D. IPAM のプールを RAM で共有して、各アカウントの IaC はそこから割り当てる

??? success "答えと解説"
    **正解: D**

    予防は IPAM です。

    - A: 誤り。事後の対処で、作成時に防げない。
    - B: 誤り。重複を前提にした対処で、予防にならない。
    - C: 誤り。経路の分析の機能で、割り当ての機能ではない。
    - D: 正しい。

    **スキル:** [IP の重複](../domain1.md#t1-6-overlap) / **参照:** [IPAM](../../../services/network-connectivity.md#ipam), [AWS Resource Access Manager](../../../services/governance.md#ram)

### 問10 {#q10}

ネットワークアカウントが Transit Gateway とそのルートテーブルを管理し、各アプリのアカウントは VPC の接続だけを行います。組織には 100 のアカウントがあります。最も適切な共有の設計はどれですか。

- A. 各アカウントの IAM ロールでネットワークアカウントへ入り、中央で全部の VPC を作る
- B. 各アカウントが Transit Gateway を作り、ネットワークアカウントとピアリングする
- C. DX ゲートウェイの関連付けの提案で各アカウントの VPC を受け入れる
- D. RAM で組織へ共有し、各アカウントが自分の VPC のアタッチメントを作る

??? success "答えと解説"
    **正解: D**

    各アカウントはアタッチするだけで済みます。

    - A: 誤り。アプリのアカウントの VPC にならない。
    - B: 誤り。ルートの管理が分散し、静的ルートも増える。
    - C: 誤り。Transit Gateway の共有の方法ではない。
    - D: 正しい。

    **スキル:** [リソース共有](../domain1.md#t1-5-sharing) / **参照:** [AWS Resource Access Manager](../../../services/governance.md#ram), [アタッチメント](../../../services/network-connectivity.md#tgw-attachments)

### 問11 {#q11}

アカウント X の Transit Gateway を、ネットワークアカウントの DX ゲートウェイに関連付けます。DX ゲートウェイの所有者は、広告するプレフィックスの確認も行います。正しい方法はどれですか。

- A. 所有者が DX ゲートウェイを RAM で X に共有し、X が関連付ける
- B. 所有者が DX ゲートウェイを X へ移管し、関連付けのあとで戻す
- C. X がホスト VIF を作成して Transit Gateway に直接関連付ける
- D. X が関連付けを提案し、所有者が承認時に許可プレフィックスを確認する

??? success "答えと解説"
    **正解: D**

    関連付けの提案と承認です。

    - A: 誤り。DX ゲートウェイは RAM ではなく提案と承認。
    - B: 誤り。そのような移管はしない。
    - C: 誤り。ホスト VIF は DX ゲートウェイに接続するもので、問題文の手順ではない。
    - D: 正しい。

    **スキル:** [リソース共有](../domain1.md#t1-5-sharing) / **参照:** [Direct Connect ゲートウェイ](../../../services/network-connectivity.md#dx-gateway)

### 問12 {#q12}

ネットワークアカウントが物理の DX を持ち、別のアカウントが所有する DX ゲートウェイを使うチームが、VIF を自分で管理したいと言っています。ポートの料金はネットワークアカウントが払います。最も適切な方法はどれですか。

- A. ホスト VIF を作成して別のアカウントへ提供し、そのアカウントが承認する
- B. RAM で VIF を共有して、別のアカウントが受け入れる
- C. 別のアカウントがコンソールで同じ VLAN の VIF を作成する
- D. 物理の接続を別のアカウントへ移管して、ポートの料金も移す

??? success "答えと解説"
    **正解: A**

    ホスト VIF として別のアカウントへ渡します。

    - A: 正しい。
    - B: 誤り。VIF は RAM で共有しない。
    - C: 誤り。接続の所有者でないと VIF を作れない。
    - D: 誤り。料金の条件に反する。

    **スキル:** [リソース共有](../domain1.md#t1-5-sharing) / **参照:** [VIF の種類](../../../services/network-connectivity.md#dx-vif-types), [AWS Resource Access Manager](../../../services/governance.md#ram)

### 問13 {#q13}

RAM で Transit Gateway を共有しました。共有先のアカウントがアタッチメントを作りましたが、`pendingAcceptance` のままで、ルートの設定に進めません。`AutoAcceptSharedAttachments` は既定のままです。最も適切な対応はどれですか。

- A. 共有先のアカウントで RAM の招待を再度受け入れる
- B. 共有先のアカウントで同じアタッチメントの所有者を自分に変更する
- C. Transit Gateway の所有者がアタッチメントを承認する
- D. 組織の SCP で `ec2:AcceptTransitGatewayVpcAttachment` を拒否から除外する

??? success "答えと解説"
    **正解: C**

    既定では無効なので、所有者の承認が必要です。

    - A: 誤り。共有はすでに受け入れ済みで、状態の原因が違う。
    - B: 誤り。所有者の変更の操作はない。
    - C: 正しい。
    - D: 誤り。問題文に SCP の拒否はない。承認は所有者の操作。

    **スキル:** [Organizations と RAM](../domain2.md#t2-1-org-ram) / **参照:** [アタッチメント](../../../services/network-connectivity.md#tgw-attachments), [AWS Resource Access Manager](../../../services/governance.md#ram)

### 問14 {#q14}

RAM で Resolver ルールを OU へ共有したいと考えています。OU を指定できず、アカウントへ招待を送る形になります。組織のすべての機能は有効です。最も適切な対応はどれですか。

- A. 各アカウントで RAM のサービスリンクロールを削除して作り直す
- B. 共有先の OU に SCP を付けて RAM の操作を許可する
- C. ルールの種類を Forward から System に変更する
- D. 管理アカウントで RAM の組織の共有を有効にしてから、OU を指定する

??? success "答えと解説"
    **正解: D**

    `enable-sharing-with-aws-organization` です。

    - A: 誤り。招待の問題の原因ではない。
    - B: 誤り。組織共有の有効化が前提。
    - C: 誤り。共有の方法と関係がない。
    - D: 正しい。

    **スキル:** [Organizations と RAM](../domain2.md#t2-1-org-ram) / **参照:** [AWS Resource Access Manager](../../../services/governance.md#ram)

### 問15 {#q15}

ネットワークチームが、共有の仕組みを一覧にしています。リソースと仕組みの組み合わせで正しいものを選んでください。（2つ選択）

- A. DX ゲートウェイ: RAM で共有し、共有先が関連付ける
- B. PHZ と別アカウントの VPC: 関連付けの許可を CLI か API で行う
- C. PHZ: RAM で共有し、共有先が受け入れる
- D. Resolver ルール: RAM で共有し、共有先が VPC に関連付ける
- E. Transit Gateway: 関連付けの許可を CLI で行い、ルートも共有する

??? success "答えと解説"
    **正解: B, D**

    仕組みが異なるので分けて覚えます。

    - A: 誤り。関連付けの提案と承認を使う。
    - B: 正しい。
    - C: 誤り。PHZ は関連付けの許可を使う。
    - D: 正しい。
    - E: 誤り。RAM で共有する。

    **スキル:** [Organizations と RAM](../domain2.md#t2-1-org-ram) / **参照:** [プライベートホストゾーン](../../../services/network-connectivity.md#private-hosted-zones), [AWS Resource Access Manager](../../../services/governance.md#ram)

### 問16 {#q16}

Cloud WAN でタグによる接続を運用しています。新しい VPC に `segment=prod` のタグを付けましたが、ポリシーのセグメント名は `production` です。作成したアタッチメントが `production` のセグメントに関連付きません。最も適切な対処はどれですか。

- A. 既定のセグメントを新しく作り、ポリシーで全アタッチメントを割り当てる
- B. タグの値をポリシーのルールの条件に合わせる
- C. VPC のルートテーブルにコアネットワークへのルートを追加する
- D. `prod` という名前の VPC を作り直して、再度アタッチする

??? success "答えと解説"
    **正解: B**

    アタッチメントポリシーのルールは、タグの値でセグメントを決めます。

    - A: 誤り。分離の設計が崩れ、タグの不一致も解決しない。
    - B: 正しい。
    - C: 誤り。セグメントへの関連付けの問題で、VPC のルートでは解決しない。
    - D: 誤り。ルールが見るのはタグで、VPC の名前ではない。

    **スキル:** [接続を広げる](../domain2.md#t2-2-expansion) / **参照:** [Cloud WAN](../../../services/network-connectivity.md#cloud-wan)

### 問17 {#q17}

Control Tower で新しいアカウントを作るたびに、VPC を Transit Gateway へ接続します。担当者の作業は増やしません。Transit Gateway は共有済みです。最も適切な方法はどれですか。

- A. ネットワークアカウントで全 OU の VPC を代理で作り、RAM で共有する
- B. OU を対象にしたサービスマネージドの StackSets で自動デプロイする
- C. 新しいアカウントの作成を EventBridge で受け、担当者へメールで手順を送る
- D. SCP で新しいアカウントの VPC の作成を禁止して、Transit Gateway の接続を待つ

??? success "答えと解説"
    **正解: B**

    組織の OU を対象にすれば自動で展開できます。

    - A: 誤り。問題文の VPC の接続の要件から離れ、設計も大きく変わる。
    - B: 正しい。
    - C: 誤り。担当者の作業になる。
    - D: 誤り。接続は自動にならない。

    **スキル:** [接続を広げる](../domain2.md#t2-2-expansion) / **参照:** [ネストされたスタックと StackSets](../../../services/iac.md#nested-stacks-stacksets), [AWS Control Tower](../../../services/governance.md#control-tower)

### 問18 {#q18}

6 リージョンで VPC を接続しています。Transit Gateway の共有を続けるか、Cloud WAN へ移るかを比較します。比較として正しいものはどれですか。

- A. Transit Gateway のピアリングはリージョン間で BGP を交換する
- B. Cloud WAN では新しい VPC のアタッチメントをタグで割り当てられない
- C. Cloud WAN はリージョン間を自動のフルメッシュにする。経路も動的に扱う
- D. Transit Gateway を共有すれば、共有先のルート操作は常に不要である

??? success "答えと解説"
    **正解: C**

    比較の表を確認します。

    - A: 誤り。ピアリングは静的ルートのみ。
    - B: 誤り。タグで自動で割り当てられる。
    - C: 正しい。
    - D: 誤り。所有者がルートを管理する。作業自体はなくならない。

    **スキル:** [接続を広げる](../domain2.md#t2-2-expansion) / **参照:** [Cloud WAN](../../../services/network-connectivity.md#cloud-wan), [Transit Gateway](../../../services/network-connectivity.md#transit-gateway)

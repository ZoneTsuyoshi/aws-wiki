# 到達性の検証とトポロジーの問題集

対象の解説: [接続の調査](../../../services/network-connectivity.md#network-analysis), [Reachability Analyzer](../../../services/network-connectivity.md#reachability-analyzer), [Network Access Analyzer](../../../services/network-connectivity.md#network-access-analyzer), [Route Analyzer](../../../services/network-connectivity.md#route-analyzer)

### 問1 {#q1}

世界に 40 の拠点と 5 リージョンの Transit Gateway があります。複数のアカウントにまたがる構成を 1 つの画面で地図として表示し、ルートの変更を監視します。パケットの中身は不要です。最も適切なものはどれですか。

- A. Network Manager のグローバルネットワークでトポロジーを表示する
- B. 全 VPC のフローログを表示する CloudWatch ダッシュボード
- C. 全 ENI の Traffic Mirroring と Wireshark の分析
- D. リージョンごとの Reachability Analyzer の定期実行

??? success "答えと解説"
    **正解: A**

    トポロジーを表示し、ルートの変更やイベントを監視します。

    - A: 正しい。
    - B: 誤り。構成とルートの変更の監視にならない。
    - C: 誤り。パケットの中身の解析で、地図にならない。
    - D: 誤り。2 点間の解析で、全体の地図にならない。

    **スキル:** [Network Manager](../domain1.md#t1-4-network-manager) / **参照:** [Route Analyzer](../../../services/network-connectivity.md#route-analyzer)

### 問2 {#q2}

Network Manager を導入したチームが、特定の 2 台の間の通信の量と拒否の有無を知りたいと言っています。導入済みの機能で足りるかを判断します。正しい助言はどれですか。

- A. Network Manager のトポロジーに、SG の拒否の理由が表示される
- B. Route Analyzer を実行すると、実際に流れたバイト数が表示される
- C. 個々のフローはフローログや Traffic Mirroring で確認する
- D. Network Manager のイベントに、個々のフローの送信元と宛先が記録される

??? success "答えと解説"
    **正解: C**

    用途を分けます。

    - A: 誤り。SG の拒否は表示しない。
    - B: 誤り。経路の解析で、通信量は表示しない。
    - C: 正しい。
    - D: 誤り。個々のフローは見えない。

    **スキル:** [Network Manager](../domain1.md#t1-4-network-manager) / **参照:** [Route Analyzer](../../../services/network-connectivity.md#route-analyzer), [フローログの分析](../../../services/network-connectivity.md#flow-log-analysis)

### 問3 {#q3}

複数のリージョンの Transit Gateway を運用するチームが、Global Networks の導入を検討しています。説明として正しいものはどれですか。

- A. 登録できる Transit Gateway は同じリージョンのものに限られる
- B. 登録すると、Transit Gateway のルートテーブルが自動で最適化される
- C. 登録すると、VPC の SG のルールが全部地図に表示される
- D. Transit Gateway と拠点を登録し、ルートの変更や状態の変化を追える

??? success "答えと解説"
    **正解: D**

    拠点の多い環境に向きます。

    - A: 誤り。複数のリージョンを登録できる。
    - B: 誤り。表示と監視の機能で、ルートを変更しない。
    - C: 誤り。SG の表示の機能ではない。
    - D: 正しい。

    **スキル:** [Network Manager](../domain1.md#t1-4-network-manager) / **参照:** [Route Analyzer](../../../services/network-connectivity.md#route-analyzer)

### 問4 {#q4}

新しい VPC の設計で「変更のたびに本番の DB への到達性を確認する」と決めます。本番へ通信を流さず、SG、NACL、ルートをまとめて評価します。最も適切なツールはどれですか。

- A. Traffic Mirroring のセッションの定期的な確認
- B. `ping` を毎分実行するスクリプトと CloudWatch のアラーム
- C. Reachability Analyzer で設定を解析する
- D. Route Analyzer。SG と NACL も含めて評価する

??? success "答えと解説"
    **正解: C**

    設定のモデルを解析し、パケットを送りません。

    - A: 誤り。実際の通信のコピーで、到達性の判定にならない。
    - B: 誤り。実パケットを送り、ICMP を止めていると使えない。
    - C: 正しい。
    - D: 誤り。SG と NACL は評価しない。

    **スキル:** [Reachability Analyzer](../domain1.md#t1-4-reachability) / **参照:** [Reachability Analyzer](../../../services/network-connectivity.md#reachability-analyzer)

### 問5 {#q5}

VPC 内の 2 台の EC2 について、Reachability Analyzer が「到達可能」と判定しました。しかしアプリは接続できません。フローログでも `REJECT` はありません。次に確認するものとして最も適切なものはどれですか。

- A. 判定は誤りとみなして、SG をすべて開ける
- B. ルートテーブルの伝播を無効にして再度分析する
- C. OS のファイアウォールと、アプリの待ち受けの状態
- D. Network Access Analyzer で同じ 2 点を指定して上書きする

??? success "答えと解説"
    **正解: C**

    ネットワークの設定には問題がありません。

    - A: 誤り。根拠のない変更で、リスクが増える。
    - B: 誤り。切り分けにならない。
    - C: 正しい。
    - D: 誤り。目的の異なるツールで、結果の上書きにならない。

    **スキル:** [Reachability Analyzer](../domain1.md#t1-4-reachability) / **参照:** [Reachability Analyzer](../../../services/network-connectivity.md#reachability-analyzer)

### 問6 {#q6}

Reachability Analyzer の設計の段階での制約を確認しています。正しいものを選んでください。（2つ選択）

- A. OS のファイアウォールは見えない
- B. Connect の先は解析しない
- C. 解析のたびに実パケットを送るので、本番に影響する
- D. リージョンを越えた経路を常に解析できる
- E. IPv6 の経路も IPv4 と同じように解析できる

??? success "答えと解説"
    **正解: A, B**

    解析の範囲です。

    - A: 正しい。
    - B: 正しい。
    - C: 誤り。パケットを送らない。
    - D: 誤り。同じリージョン。
    - E: 誤り。IPv4 のみ。

    **スキル:** [Reachability Analyzer](../domain1.md#t1-4-reachability) / **参照:** [Reachability Analyzer](../../../services/network-connectivity.md#reachability-analyzer)

### 問7 {#q7}

Transit Gateway の VPC と VPN の間で、Transit Gateway のルートテーブルの経路だけを確認します。SG や NACL は別のチームが確認済みです。パケットは流しません。最も適切なツールはどれですか。

- A. Route Analyzer。Transit Gateway の表の経路だけを確認する
- B. DX のフェイルオーバーテスト。表を検証する
- C. Reachability Analyzer。Transit Gateway の表だけに絞れる
- D. `tracepath`。Transit Gateway の表を表示する

??? success "答えと解説"
    **正解: A**

    ルートテーブルの経路を調べます。

    - A: 正しい。
    - B: 誤り。BGP を止めるテスト。
    - C: 誤り。SG と NACL を含む解析で、問題文の範囲より広い。
    - D: 誤り。実パケットで MTU を調べるツール。

    **スキル:** [テストと検証](../domain2.md#t2-1-testing) / **参照:** [Route Analyzer](../../../services/network-connectivity.md#route-analyzer)

### 問8 {#q8}

オンプレミスから VPC の EC2 への通信が失敗します。DX の接続、VIF、BGP、VPC と SG、アプリのどれが原因か不明です。環境間の検証の順序として最も適切なものはどれですか。

- A. アプリ、SG と NACL、AWS のルートテーブル、BGP、物理の順
- B. BGP、アプリ、物理、SG と NACL、AWS のルートテーブルの順
- C. AWS のルートテーブル、物理、アプリ、BGP、SG と NACL の順
- D. 物理、BGP、AWS のルートテーブル、SG と NACL、アプリの順

??? success "答えと解説"
    **正解: D**

    下の層から順に確かめます。

    - A: 誤り。上の層から始めると、下の層の問題の切り分けが遅れる。
    - B: 誤り。物理が通らないと BGP も確立しない。
    - C: 誤り。順序に一貫性がない。
    - D: 正しい。

    **スキル:** [テストと検証](../domain2.md#t2-1-testing) / **参照:** [接続の調査](../../../services/network-connectivity.md#network-analysis)

### 問9 {#q9}

EC2 からオンプレミスのサーバーへ、DX と VPN の経路ごとに経路の MTU を確認します。ICMP は通っています。実パケットで確かめます。最も適切なコマンドはどれですか。

- A. `dig`。名前の解決の結果から MTU を読み取る
- B. `nslookup`。応答のサイズから MTU を読み取る
- C. `aws ec2 describe-route-tables`。ルートの MTU を読み取る
- D. `tracepath`。実パケットで経路の MTU を確認する

??? success "答えと解説"
    **正解: D**

    経路の MTU を調べます。

    - A: 誤り。名前解決の確認。
    - B: 誤り。名前解決の確認。
    - C: 誤り。経路の表示で MTU を示さない。
    - D: 正しい。

    **スキル:** [テストと検証](../domain2.md#t2-1-testing) / **参照:** [接続の調査](../../../services/network-connectivity.md#network-analysis), [PMTUD とトラブルシューティング](../../../services/network-connectivity.md#pmtud)

### 問10 {#q10}

組織の全 VPC で「本番から開発へ到達する経路がない」ことを定期的に確認します。特定の 2 点を列挙せず、環境全体の条件で評価します。最も適切なツールはどれですか。

- A. Reachability Analyzer。本番と開発の全部の組み合わせを登録する
- B. Route Analyzer。Transit Gateway の表で全 VPC を確認する
- C. Traffic Mirroring。本番の全 ENI の通信をコピーする
- D. Network Access Analyzer。環境全体の条件で経路を調べる

??? success "答えと解説"
    **正解: D**

    望まない経路を環境全体で調べます。

    - A: 誤り。特定の 2 点の解析で、列挙が必要。
    - B: 誤り。SG などを評価せず、表の経路のみの解析。
    - C: 誤り。実際の通信のコピーで、経路の有無の確認にならない。
    - D: 正しい。

    **スキル:** [接続のテスト](../domain2.md#t2-2-testing) / **参照:** [Network Access Analyzer](../../../services/network-connectivity.md#network-access-analyzer)

### 問11 {#q11}

別のアカウントのリソースへの経路を Reachability Analyzer で解析します。両方のアカウントは同じ組織にあります。解析の担当者に各アカウントの長期の認証情報は渡しません。必要な設定はどれですか。

- A. 相手の VPC と自分の VPC の間にピアリングを作成する
- B. 相手のアカウントの IAM ユーザーのアクセスキーを発行する
- C. RAM で相手のサブネットを共有する
- D. Organizations で信頼されたアクセスを有効にする

??? success "答えと解説"
    **正解: D**

    委任管理者も登録できます。

    - A: 誤り。解析の条件ではない。
    - B: 誤り。長期の認証情報は不要。
    - C: 誤り。解析の条件ではない。
    - D: 正しい。

    **スキル:** [接続のテスト](../domain2.md#t2-2-testing) / **参照:** [Reachability Analyzer](../../../services/network-connectivity.md#reachability-analyzer)

### 問12 {#q12}

同じリージョンの 2 つの Transit Gateway をピアリングしています。Route Analyzer でこの経路を調べようとしましたが、期待どおりに解析できません。リージョン間のピアリングでは解析できました。正しい理解はどれですか。

- A. Route Analyzer の解析は最初に Reachability Analyzer の分析を必要とする
- B. VPC のフローログを有効にしないと解析の結果が出ない
- C. Route Analyzer は同じリージョンのピアリングに対応しない
- D. 同じリージョンのピアリングには動的ルーティングの有効化が必要である

??? success "答えと解説"
    **正解: C**

    制約を確認します。

    - A: 誤り。依存はない。
    - B: 誤り。解析はルートテーブルを見るので不要。
    - C: 正しい。
    - D: 誤り。ピアリングは静的ルートのみで、解析の条件でもない。

    **スキル:** [接続のテスト](../domain2.md#t2-2-testing) / **参照:** [Route Analyzer](../../../services/network-connectivity.md#route-analyzer), [ピアリング](../../../services/network-connectivity.md#tgw-peering)

### 問13 {#q13}

運用チームが次の 3 つの質問に答えます。質問 1: A から B へ届くか、何が止めているか。質問 2: Transit Gateway の経路は正しいか。質問 3: 望まない経路がないか。ツールの組み合わせとして正しいものはどれですか。

- A. 1 は Route Analyzer、2 は Network Access Analyzer、3 は Reachability Analyzer
- B. 1 は Traffic Mirroring、2 は Reachability Analyzer、3 は Route Analyzer
- C. 1 は Reachability Analyzer、2 は Route Analyzer、3 は Network Access Analyzer
- D. 1 は Network Access Analyzer、2 は Reachability Analyzer、3 は Route Analyzer

??? success "答えと解説"
    **正解: C**

    ツールごとの質問を覚えます。

    - A: 誤り。質問とツールの対応が違う。
    - B: 誤り。Traffic Mirroring は到達性の判定にならない。
    - C: 正しい。
    - D: 誤り。質問とツールの対応が違う。

    **スキル:** [経路の分析](../domain3.md#t3-2-routing-tools) / **参照:** [接続の調査](../../../services/network-connectivity.md#network-analysis)

### 問14 {#q14}

オンプレミスの一部の拠点へ通信できなくなりました。BGP の経路が消えたのか、Transit Gateway のルートテーブルの関連付けの問題かを、パケットを流さずに確認します。最も適切な手順はどれですか。

- A. Route Analyzer で送信元と宛先のアタッチメントを指定する
- B. 実トラフィックを増やして、`PacketDropCountNoRoute` の変化を見る
- C. BGP の MD5 キーを一度変更して、セッションを再確立する
- D. CloudTrail で `DeleteVpc` のイベントを検索する

??? success "答えと解説"
    **正解: A**

    Route Analyzer は経路を解析します。

    - A: 正しい。
    - B: 誤り。パケットを流している。
    - C: 誤り。本番に影響が大きい。
    - D: 誤り。経路の状態の確認にならない。

    **スキル:** [経路の分析](../domain3.md#t3-2-routing-tools) / **参照:** [Route Analyzer](../../../services/network-connectivity.md#route-analyzer)

### 問15 {#q15}

VPC A から VPC B へ Transit Gateway を経由する TCP の通信で、Reachability Analyzer の分析は成功しました。しかし実際には接続できません。VPC B の戻りのルートが足りないことが疑われます。正しい説明はどれですか。

- A. 戻りのルートの不足は必ず到達不能と表示される
- B. Transit Gateway の TCP は行きだけ解析する
- C. Transit Gateway の経路は解析の対象外なので、結果は信用できない
- D. 行きと戻りの両方を解析するので、戻りのルートの問題はない

??? success "答えと解説"
    **正解: B**

    戻りの経路は別に確認します。

    - A: 誤り。戻りは解析しない。
    - B: 正しい。
    - C: 誤り。行きは対象。
    - D: 誤り。行きだけ解析する。

    **スキル:** [経路の分析](../domain3.md#t3-2-routing-tools) / **参照:** [Reachability Analyzer](../../../services/network-connectivity.md#reachability-analyzer), [ルートテーブル](../../../services/network-connectivity.md#tgw-route-tables)

### 問16 {#q16}

大規模な障害で、影響を受けた拠点を素早く把握します。拠点は数十か所あり、Transit Gateway も複数あります。各担当者の調査の前に全体を把握します。最も適切なものはどれですか。

- A. Network Manager のトポロジーと状態を確認する
- B. CloudTrail のログを時系列で読み、変更を探す
- C. `ping` のスクリプトを全拠点へ実行して結果を比べる
- D. Trusted Advisor の VPN のチェックを更新する

??? success "答えと解説"
    **正解: A**

    障害の影響範囲をすぐ把握できます。

    - A: 正しい。
    - B: 誤り。API の記録で、影響範囲の把握に向かない。
    - C: 誤り。ICMP の可否に左右され、構成の把握にもならない。
    - D: 誤り。全体のトポロジーの把握にならない。

    **スキル:** [トポロジー](../domain3.md#t3-2-topology) / **参照:** [Route Analyzer](../../../services/network-connectivity.md#route-analyzer)

### 問17 {#q17}

ネットワークチームは、トポロジーの把握と Transit Gateway の経路の解析を 1 か所で行いたいと考えています。ツールの場所の説明として正しいものはどれですか。

- A. Route Analyzer も Network Manager のコンソールにある
- B. トポロジーの図は Route 53 のコンソールで確認する
- C. Route Analyzer は VPC のフローログの画面にある
- D. トポロジーの図は CloudWatch Logs Insights で作る

??? success "答えと解説"
    **正解: A**

    同じコンソールで使えます。

    - A: 正しい。
    - B: 誤り。場所が違う。
    - C: 誤り。場所が違う。
    - D: 誤り。場所が違う。

    **スキル:** [トポロジー](../domain3.md#t3-2-topology) / **参照:** [Route Analyzer](../../../services/network-connectivity.md#route-analyzer), [ルートテーブル](../../../services/network-connectivity.md#tgw-route-tables)

### 問18 {#q18}

オンプレミスの拠点とリンクをトポロジーに追加し、Transit Gateway との関係を図で見ます。SD-WAN の機器の情報も含めます。最も適切な作業はどれですか。

- A. Route 53 の PHZ に拠点のレコードを登録する
- B. グローバルネットワークにサイト、リンク、デバイスを登録する
- C. 拠点ごとに CGW を作成するだけで、リンクの情報を自動で取り込む
- D. VPC のタグに拠点の名前を書いて地図を自動で作る

??? success "答えと解説"
    **正解: B**

    オンプレミスの拠点も登録します。

    - A: 誤り。別の用途。
    - B: 正しい。
    - C: 誤り。サイトやリンクの情報の登録が別に必要。
    - D: 誤り。図に現れない。

    **スキル:** [トポロジー](../domain3.md#t3-2-topology) / **参照:** [Route Analyzer](../../../services/network-connectivity.md#route-analyzer)

### 問19 {#q19}

Reachability Analyzer で到達不能と表示され、止めている部品として NACL が示されました。担当者は SG の確認から始めようとしています。正しい対応はどれですか。

- A. SG をすべて開放して再度分析し、結果を比べる
- B. ルートテーブルを削除して再作成する
- C. 結果を無視して OS のファイアウォールを調べる
- D. 表示された NACL の該当のルールを修正する

??? success "答えと解説"
    **正解: D**

    示された部品を直します。

    - A: 誤り。不要な開放で、表示の部品を先に直す。
    - B: 誤り。根拠のない変更で影響が大きい。
    - C: 誤り。到達不能のときの手順ではない。
    - D: 正しい。

    **スキル:** [設定の誤り](../domain3.md#t3-2-misconfig) / **参照:** [接続できないときの切り分け](../../../services/networking.md#vpc-troubleshooting)

### 問20 {#q20}

Reachability Analyzer は到達可能で、フローログにも `REJECT` はありません。ssh や小さな HTTP の要求は通りますが、大きな応答だけ止まります。次に確認すべきものはどれですか。

- A. 経路の MTU と、PMTUD に必要な ICMP の許可
- B. `enableDnsSupport` と DHCP オプションセット
- C. BGP の MD5 キーとピアの ASN
- D. IGW のアタッチの有無とデフォルトルート

??? success "答えと解説"
    **正解: A**

    大きなパケットだけの失敗は MTU です。

    - A: 正しい。
    - B: 誤り。名前解決の問題の症状ではない。
    - C: 誤り。BGP が確立しないときの確認。
    - D: 誤り。小さな通信が通るので経路はある。

    **スキル:** [設定の誤り](../domain3.md#t3-2-misconfig) / **参照:** [接続できないときの切り分け](../../../services/networking.md#vpc-troubleshooting), [PMTUD とトラブルシューティング](../../../services/network-connectivity.md#pmtud)

### 問21 {#q21}

ピアリングした 2 つの VPC の間で、片方向の通信だけが失敗します。ピアリングは `active` です。設定の誤りの切り分けとして、まず確認すべきものを選んでください。（2つ選択）

- A. ピアリング先の VPC の IGW の有無
- B. 両方のルートテーブルの経路
- C. 両方の VPC の DHCP オプションセットの NTP サーバー
- D. 両方の VPC の CIDR を一度削除して追加し直すこと
- E. 両方の SG と NACL

??? success "答えと解説"
    **正解: B, E**

    片方だけの設定の誤りが多い症状です。

    - A: 誤り。ピアリングの通信に関係しない。
    - B: 正しい。
    - C: 誤り。通信の経路に関係しない。
    - D: 誤り。根拠のない変更で影響が大きい。
    - E: 正しい。

    **スキル:** [設定の誤り](../domain3.md#t3-2-misconfig) / **参照:** [接続できないときの切り分け](../../../services/networking.md#vpc-troubleshooting), [VPC ピアリング](../../../services/network-connectivity.md#vpc-peering)

### 問22 {#q22}

ネットワークの変更のたびに、接続の意図を自動で確認します。確認する経路はコードで管理します。パケットは流しません。最も適切な手順はどれですか。

- A. `AWS::EC2::FlowLog` を定義して、変更のたびに `REJECT` の増加を待つ
- B. 変更のたびに担当者が `ping` を実行して結果を記録する
- C. Trusted Advisor のチェックを変更のたびに更新する
- D. `AWS::EC2::NetworkInsightsPath` を定義して、変更を EventBridge で受けて分析する

??? success "答えと解説"
    **正解: D**

    検証を自動にします。

    - A: 誤り。実際の通信が必要で、変更の直後に判定できない。
    - B: 誤り。自動にならない。
    - C: 誤り。接続の意図の確認にならない。
    - D: 正しい。

    **スキル:** [検証と自動化](../domain3.md#t3-2-verify) / **参照:** [Reachability Analyzer](../../../services/network-connectivity.md#reachability-analyzer), [CloudFormation テンプレート](../../../services/iac.md#cloudformation-template)

### 問23 {#q23}

設計要件は「IGW への経路には必ずファイアウォールがある」ことです。全 VPC について要件を満たさない経路を見つけます。特定の 2 点は指定しません。最も適切なものはどれですか。

- A. Network Access Analyzer のスコープで経路を調べる
- B. CloudTrail で `CreateFirewall` の呼び出しを確認する
- C. Reachability Analyzer で全 ENI と IGW の組を分析する
- D. Config の `vpc-flow-logs-enabled` のルールを確認する

??? success "答えと解説"
    **正解: A**

    要件の検証です。

    - A: 正しい。
    - B: 誤り。経路の確認にならない。
    - C: 誤り。組み合わせの列挙が必要で、中間の部品の条件を扱いにくい。
    - D: 誤り。ログの有無の確認で、経路の確認にならない。

    **スキル:** [検証と自動化](../domain3.md#t3-2-verify) / **参照:** [Network Access Analyzer](../../../services/network-connectivity.md#network-access-analyzer)

### 問24 {#q24}

自動の分析の結果が期待と違ったときの動作を組みます。結果を運用チームへ伝え、必要なら変更を戻します。パイプラインは既にあり、CI/CD に組み込みます。最も適切な構成はどれですか。

- A. 分析の結果を手で確認して、毎週メールで報告する
- B. Lambda で分析し、期待と違えば SNS で通知して変更を戻す
- C. 変更セットで分析の結果を確認して通知する
- D. ドリフト検出で分析の結果を確認して変更を戻す

??? success "答えと解説"
    **正解: B**

    CI/CD に組み込むこともできます。

    - A: 誤り。自動にならない。
    - B: 正しい。
    - C: 誤り。実行前の差分で、到達性の結果ではない。
    - D: 誤り。分析の結果の確認の機能ではない。

    **スキル:** [検証と自動化](../domain3.md#t3-2-verify) / **参照:** [Reachability Analyzer](../../../services/network-connectivity.md#reachability-analyzer), [EventBridge による修復パターン](../../../services/operations.md#eventbridge-remediation)

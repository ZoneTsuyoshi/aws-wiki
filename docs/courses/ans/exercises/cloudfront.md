# CloudFront と配信設計の問題集

対象の解説: [CloudFront](../../../services/networking.md#cloudfront), [キャッシュキーとポリシー](../../../services/networking.md#cache-keys), [オリジンフェイルオーバー](../../../services/networking.md#origin-failover), [S3 オリジンの保護: OAC](../../../services/networking.md#oac)

### 問1 {#q1}

静的ファイルを S3 に置き、世界へ配信します。監査の要件で、S3 への直接のアクセスは禁止し、配信は CloudFront だけを通します。バケットは SSE-KMS で暗号化しています。最も適切な構成はどれですか。

- A. OAC を使い、バケットポリシーと KMS キーポリシーで CloudFront を許可する
- B. S3 のプリサインド URL を 1 年の期限で発行してオリジンのパスに固定し、KMS は無効にする
- C. S3 の Web サイトエンドポイントをオリジンにして、IP でバケットポリシーを制限する
- D. バケットを公開にして、`Referer` ヘッダーが CloudFront の場合だけバケットポリシーで許可し、KMS は既定のままにする

??? success "答えと解説"
    **正解: A**

    OAC は SSE-KMS のオブジェクトにも対応します。キーポリシーの許可も必要です。

    - A: 正しい。
    - B: 誤り。長期の URL の管理が必要で、暗号化の要件にも合わない。
    - C: 誤り。Web サイトエンドポイントは OAC に対応せず、CloudFront の IP の管理も難しい。
    - D: 誤り。直接アクセスを防げず、ヘッダーは偽装もできる。

    **スキル:** [CDN の設計パターン](../domain1.md#t1-1-cdn) / **参照:** [S3 オリジンの保護: OAC](../../../services/networking.md#oac), [CloudFront](../../../services/networking.md#cloudfront)

### 問2 {#q2}

EC サイトでキャッシュのヒット率が 20% しかありません。ビヘイビアのキャッシュポリシーで、全クエリ文字列と `User-Agent` ヘッダーをキャッシュキーに入れています。オリジンはログの分析のため `User-Agent` を必要としますが、応答は変わりません。最も適切な変更はどれですか。

- A. `User-Agent` をオリジンリクエストポリシーへ移し、キャッシュキーを絞る
- B. TTL を長くして、ヒット率の低下をキャッシュの保持時間で補い、ポリシーはそのままにする
- C. Origin Shield を有効にするだけで、キャッシュキーの種類を問わずヒット率を改善する
- D. Lambda@Edge でオリジンの応答に `Vary: User-Agent` を追加して、キャッシュを細かく分ける

??? success "答えと解説"
    **正解: A**

    オリジンへ渡すだけの値はキャッシュキーに入れません。

    - A: 正しい。
    - B: 誤り。キーがばらつくとオブジェクトが増え続け、効果が小さい。
    - C: 誤り。キーのばらつきそのものは解決しない。
    - D: 誤り。キャッシュをさらに分割してヒット率が下がる。

    **スキル:** [CDN の設計パターン](../domain1.md#t1-1-cdn) / **参照:** [キャッシュキーとポリシー](../../../services/networking.md#cache-keys), [ビヘイビアの全設定](../../../services/networking.md#behavior-settings)

### 問3 {#q3}

2 リージョンの S3 バケットをオリジングループに設定しました。プライマリの障害時に、利用者の GET の応答が返るまで 30 秒かかります。切り替えの時間を短くしたいと考えています。最も適切な変更はどれですか。

- A. プライマリとセカンダリを入れ替えて、セカンダリを先に評価させてから障害を判定する
- B. オリジングループをやめて、Route 53 のレイテンシーレコードでバケットを切り替えて高速にする
- C. オリジンへの接続の試行回数とタイムアウトを短くして、待ち時間を減らす
- D. CloudFront のキャッシュの TTL を 0 にして、毎回プライマリの状態を確認させる

??? success "答えと解説"
    **正解: C**

    接続の失敗は既定で最大 30 秒（10 秒 × 3 回）かかります。

    - A: 誤り。障害時の待ち時間は同じで、平常時の宛先が変わるだけ。
    - B: 誤り。DNS のキャッシュと S3 のバケット名の問題があり、改善にならない。
    - C: 正しい。
    - D: 誤り。オリジンの負荷が増え、切り替えの時間は短くならない。

    **スキル:** [CDN の設計パターン](../domain1.md#t1-1-cdn) / **参照:** [オリジンフェイルオーバー](../../../services/networking.md#origin-failover)

### 問4 {#q4}

ライブ配信で、世界の複数のリージョナルエッジキャッシュから、1 つのオリジンへ同時に多くのリクエストが届きます。オリジンの負荷をさらに下げたいと考えています。既存のビヘイビアとキャッシュキーは最適化済みです。最も適切な機能はどれですか。

- A. Origin Shield。オリジンの手前に集約のキャッシュ層を追加する
- B. CloudFront Functions でリクエストのヘッダーを削除する機能
- C. 署名付き Cookie によるコンテンツの制限
- D. フィールドレベル暗号化の有効化と公開鍵の登録

??? success "答えと解説"
    **正解: A**

    Origin Shield はオリジンの手前のキャッシュ層で、リクエストを集約します。

    - A: 正しい。
    - B: 誤り。キャッシュ層を増やす機能ではない。
    - C: 誤り。アクセス制御の機能で、負荷の集約にならない。
    - D: 誤り。データ保護の機能で、オリジンの負荷は減らない。

    **スキル:** [CDN の設計パターン](../domain1.md#t1-1-cdn) / **参照:** [オリジンの設定](../../../services/networking.md#origin-settings)

### 問5 {#q5}

大阪リージョンの ALB をオリジンとする CloudFront に、独自ドメインの HTTPS を設定します。ALB にも同じ名前の証明書を使います。ACM の証明書の発行先として正しい組み合わせはどれですか。

- A. CloudFront も ALB も大阪リージョンに 1 つ発行して、両方で共用する
- B. CloudFront も ALB も `us-east-1` に 1 つ発行して、ALB へコピーする
- C. CloudFront は `us-east-1`、ALB は大阪リージョンにそれぞれ発行する
- D. CloudFront は大阪リージョン、ALB は `us-east-1` に分けて発行する

??? success "答えと解説"
    **正解: C**

    証明書はリージョンの規則に従います。

    - A: 誤り。CloudFront の証明書は `us-east-1` に必要。
    - B: 誤り。ALB の証明書は ALB と同じリージョンに必要。
    - C: 正しい。
    - D: 誤り。リージョンの組み合わせが逆。

    **スキル:** [他のサービスとの統合](../domain1.md#t1-1-integration) / **参照:** [リージョンのルール](../../../services/certificates.md#region-rules), [API の種類](../../../services/api-gateway.md#api-types)

### 問6 {#q6}

API Gateway の API の前に、自社で管理する CloudFront を置きます。キャッシュ、WAF、カスタムヘッダーを自社の CloudFront で制御します。不要なレイヤーを避けるには、API のエンドポイントの種類をどれにしますか。

- A. リージョナル API。自社の CloudFront だけを前に置ける構成にする
- B. エッジ最適化 API。内部の CloudFront と自社の CloudFront を二重に使う
- C. プライベート API。インターネットに公開せず CloudFront のオリジンとして VPC エンドポイントで直接つなぐ
- D. ローカルの API。エッジロケーションに API を複製してオリジンを不要にする

??? success "答えと解説"
    **正解: A**

    自前の CloudFront を前に置くならリージョナルです。

    - A: 正しい。
    - B: 誤り。AWS 管理の CloudFront が内部で使われ、二重になる。
    - C: 誤り。問題文の不要なレイヤーの論点の答えにならず、接続の前提も異なる。
    - D: 誤り。そのようなエンドポイントの種類はない。

    **スキル:** [他のサービスとの統合](../domain1.md#t1-1-integration) / **参照:** [API の種類](../../../services/api-gateway.md#api-types)

### 問7 {#q7}

CloudFront に AWS WAF の Web ACL を付けます。ディストリビューションと ALB は東京リージョンを使う構成です。Web ACL を作るスコープとリージョンで正しいものはどれですか。

- A. `CLOUDFRONT` スコープの Web ACL を `us-east-1` に作成して関連付ける
- B. `REGIONAL` スコープで東京に作成し、ALB の属性で CloudFront にも伝える
- C. `CLOUDFRONT` スコープで東京に作成し、エッジへ同期されるのを待つ
- D. `GLOBAL` スコープで Firewall Manager の管理者アカウントに作成して関連付ける

??? success "答えと解説"
    **正解: A**

    CloudFront の Web ACL はグローバルスコープで `us-east-1` に作ります。

    - A: 正しい。
    - B: 誤り。CloudFront に付ける Web ACL のスコープではない。
    - C: 誤り。CloudFront の Web ACL は `us-east-1`。
    - D: 誤り。そのようなスコープはない。

    **スキル:** [他のサービスとの統合](../domain1.md#t1-1-integration) / **参照:** [アタッチできる場所](../../../services/certificates.md#waf-resources), [S3 オリジンの保護: OAC](../../../services/networking.md#oac)

### 問8 {#q8}

インターネット向け ALB が CloudFront の背後にあります。利用者が ALB の DNS 名で直接アクセスして WAF を迂回することを防ぎます。運用の手間を増やさずに実現する組み合わせを選んでください。（2つ選択）

- A. ALB の SG で、CloudFront のエッジ IP を手で全件登録して毎日更新する
- B. CloudFront でカスタムヘッダーを追加し、ALB のリスナールールで確認する
- C. ALB に Elastic IP を付けて、その IP だけを CloudFront のオリジンに指定する
- D. ALB の SG でオリジン向けの CloudFront のマネージドプレフィックスリストだけを許可する
- E. ALB のスキームを作成後に内部へ変更し、CloudFront から VPC 経由でつなぐ

??? success "答えと解説"
    **正解: B, D**

    カスタムヘッダーは公式の推奨の方法の 1 つで、プレフィックスリストと組み合わせられます。

    - A: 誤り。手動の更新は運用の負担になる。
    - B: 正しい。
    - C: 誤り。ALB に Elastic IP は付けられない。
    - D: 正しい。
    - E: 誤り。スキームは作成後に変更できない。

    **スキル:** [他のサービスとの統合](../domain1.md#t1-1-integration) / **参照:** [オリジンの設定](../../../services/networking.md#origin-settings), [リスナーとルール](../../../services/networking.md#alb-listeners)

### 問9 {#q9}

世界中の工場が、数 GB のログファイルを東京の S3 バケットへ毎日アップロードします。遅延が大きく、転送が失敗します。アプリの変更は最小限にしたいと考えています。最も適切な選択はどれですか。

- A. S3 Transfer Acceleration を有効にし、専用のエンドポイントへ送る
- B. CloudFront のキャッシュ TTL を伸ばして、アップロードをエッジに保持する
- C. Route 53 のレイテンシーレコードで最寄りのリージョンの別のバケットを返す
- D. Global Accelerator の標準アクセラレーターで S3 のバケットをエンドポイントに指定する

??? success "答えと解説"
    **正解: A**

    大きなファイルの世界からの S3 へのアップロードは Transfer Acceleration です。

    - A: 正しい。
    - B: 誤り。キャッシュはアップロードの高速化にならない。
    - C: 誤り。東京のバケットへの転送にならず、レプリケーションも必要になる。
    - D: 誤り。S3 は Global Accelerator のエンドポイントではない。

    **スキル:** [要件から配信方式を選ぶ](../domain1.md#t1-1-requirements) / **参照:** [Global Accelerator](../../../services/network-connectivity.md#global-accelerator), [Transfer Acceleration](../../../services/s3.md#transfer-acceleration)

### 問10 {#q10}

動的な HTTP API を世界へ提供します。応答はキャッシュできません。SQL インジェクション対策で WAF を使い、既存の ALB に手を入れたくありません。遅延は下げたいです。固定 IP の要件はありません。最も適切な構成はどれですか。

- A. Route 53 のレイテンシーレコードを追加し、ALB の前には何も置かずに WAF を付ける
- B. CloudFront をキャッシュなしで ALB の前に置き、WAF を CloudFront に付ける
- C. S3 にキャッシュした API の応答を CloudFront で配信し、更新のたびに無効化する
- D. Global Accelerator のみを ALB の前に置き、WAF は ALB から外してアプリで検査する

??? success "答えと解説"
    **正解: B**

    キャッシュしない動的な通信でも CloudFront は AWS のネットワークを通せます。

    - A: 誤り。利用者から ALB までの遅延が改善しない。
    - B: 正しい。
    - C: 誤り。動的な応答はキャッシュできないという要件に反する。
    - D: 誤り。アプリの変更になり、要件に合わない。

    **スキル:** [要件から配信方式を選ぶ](../domain1.md#t1-1-requirements) / **参照:** [CloudFront](../../../services/networking.md#cloudfront), [Global Accelerator](../../../services/network-connectivity.md#global-accelerator)

### 問11 {#q11}

50 個の VPC がそれぞれ NAT ゲートウェイを持ち、費用と出口の管理が問題になっています。全 VPC は Transit Gateway に接続済みです。インターネットへの送信の出口をまとめる場合の説明として正しいものはどれですか。

- A. 集約すると Transit Gateway の処理料金が無料になり、総費用は必ず小さくなる
- B. CloudFront を送信の出口に指定して NAT を不要にし、送信先のインターネットへ透過的につなぐ
- C. NAT ゲートウェイはリージョンに 1 つしか作成できないので、集約の代わりに全 VPC で IGW を使う
- D. 出口用 VPC に NAT を集約する。集約で NAT の時間料金は減るが、Transit Gateway の処理料金は増える

??? success "答えと解説"
    **正解: D**

    時間料金と処理料金の両方で比較します。

    - A: 誤り。処理料金は無料にならず、通信量次第で総額は比較が必要。
    - B: 誤り。CloudFront は外向きの出口の仕組みではない。
    - C: 誤り。NAT は複数作成でき、プライベートの要件にも反する。
    - D: 正しい。

    **スキル:** [要件から配信方式を選ぶ](../domain1.md#t1-1-requirements) / **参照:** [NAT ゲートウェイ](../../../services/network-connectivity.md#nat-gateway), [データ転送の費用](../../../services/cost-management.md#data-transfer)

### 問12 {#q12}

EC2 のオリジンから直接 JSON を配信しており、データ転送の費用が大きくなっています。同じ応答は多くの利用者に共通です。アプリの変更は避けます。帯域の使用量を最も効果的に減らす組み合わせを選んでください。（2つ選択）

- A. CloudFront を前に置いてキャッシュする
- B. オリジンの EC2 を大きなインスタンスに変更する
- C. CloudFront の自動圧縮を有効にする
- D. NLB を前に置いてターゲットを増やす
- E. ALB の HTTP/2 を無効にしてフレームを減らす

??? success "答えと解説"
    **正解: A, C**

    キャッシュと圧縮の両方で、オリジンから送るデータを減らせます。

    - A: 正しい。
    - B: 誤り。帯域の上限は上がるが、使用量は減らない。
    - C: 正しい。
    - D: 誤り。同じ量のデータが流れるので減らない。
    - E: 誤り。使用量を減らす手段にならない。

    **スキル:** [帯域の使用量](../domain3.md#t3-3-bandwidth) / **参照:** [圧縮](../../../services/networking.md#cloudfront-compression), [データ転送の費用](../../../services/cost-management.md#data-transfer)

### 問13 {#q13}

VPC 内の 1 台のサーバーから、同じ市場データを 80 台の受信者へ UDP で送っています。ユニキャストでは送信元の帯域が 80 倍必要で、上限に近づいています。受信者は全員 VPC の中にあります。最も適切な方法はどれですか。

- A. 送信元に複数の ENI を付けて、受信者ごとに ENI を分ける
- B. 受信者を Global Accelerator のエンドポイントに登録して、エッジから配る
- C. VPC の DHCP オプションセットでブロードキャストアドレスを指定して全員に送る
- D. Transit Gateway のマルチキャストで、送信元から 1 回だけ送る

??? success "答えと解説"
    **正解: D**

    マルチキャストでは送信元は 1 回だけ送ります。

    - A: 誤り。帯域の総量は減らない。
    - B: 誤り。同じ VPC の内部の配信の仕組みではない。
    - C: 誤り。VPC はブロードキャストに対応しない。
    - D: 正しい。

    **スキル:** [帯域の使用量](../domain3.md#t3-3-bandwidth) / **参照:** [マルチキャスト](../../../services/network-connectivity.md#tgw-multicast)

### 問14 {#q14}

プライベートサブネットの EC2 が、同じリージョンの S3 へ月に数百 TB を転送しています。Cost Explorer で NAT ゲートウェイのデータ処理料金が大半を占めています。最も費用を下げる対応はどれですか。

- A. CloudFront を S3 の前に置き、EC2 からは CloudFront の URL で取得する
- B. S3 のゲートウェイエンドポイントを作り、ルートテーブルに関連付ける
- C. S3 のインターフェイスエンドポイントを AZ ごとに作る
- D. NAT ゲートウェイを各 AZ に増やし、AZ 間のデータ転送の料金を減らす

??? success "答えと解説"
    **正解: B**

    ゲートウェイエンドポイントは無料で、NAT を通らなくなります。

    - A: 誤り。書き込みやキャッシュされない通信では効果が小さく、変更も大きい。
    - B: 正しい。
    - C: 誤り。機能するが時間料金と処理料金がかかり、費用はゲートウェイ型より高い。
    - D: 誤り。S3 へのデータ処理料金は残る。

    **スキル:** [帯域の使用量](../domain3.md#t3-3-bandwidth) / **参照:** [VPC エンドポイントと PrivateLink](../../../services/networking.md#vpc-endpoints), [データ転送の費用](../../../services/cost-management.md#data-transfer)

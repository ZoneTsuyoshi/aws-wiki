# 暗号化と証明書の問題集

対象の解説: [転送時の TLS](../../../services/certificates.md#tls-in-transit), [AWS Certificate Manager](../../../services/certificates.md#acm), [MACsec](../../../services/network-connectivity.md#dx-macsec), [責任共有モデル](../../../services/cloud-foundations.md#shared-responsibility)

### 問1 {#q1}

金融の監査で「100 Gbps の DX で全通信を暗号化し、暗号化できないなら通信を止めること」を求められています。ルーターと DX ロケーションの区間の暗号化で足ります。ルーターは MACsec に対応します。最も適切なものはどれですか。

- A. MACsec を `should_encrypt` で有効にして、暗号化を試みる
- B. トランジット VIF の上のプライベート IP VPN を 1 本使う
- C. MACsec を `must_encrypt` で有効にする
- D. 公開 VIF の上の VPN を標準トンネルで束ねる

??? success "答えと解説"
    **正解: C**

    `must_encrypt` なら暗号化できないと通信しません。

    - A: 誤り。暗号化できなくても通信が続く。
    - B: 誤り。トンネルの帯域が上限で、100 Gbps に足りない。
    - C: 正しい。
    - D: 誤り。帯域が足りず、MACsec より遅い。

    **スキル:** [暗号化の選択肢](../domain4.md#t4-3-options) / **参照:** [MACsec](../../../services/network-connectivity.md#dx-macsec)

### 問2 {#q2}

追加の監査で、DX ロケーションから VPC までの暗号化と、アプリの間の相互認証が必要になりました。MACsec は既に使っています。公開 IP は使いません。適切なものを選んでください。（2つ選択）

- A. 同じリージョンの VPC ピアリングの暗号化に任せる
- B. プライベート IP VPN で VPC までの区間を暗号化する
- C. アプリの間に mTLS を使う
- D. MACsec の範囲を VPC の中まで延長する
- E. 公開 VIF の上の VPN で VPC までの区間を暗号化する

??? success "答えと解説"
    **正解: B, C**

    範囲ごとに方法を選びます。

    - A: 誤り。DX の区間の話ではなく、相互認証にもならない。
    - B: 正しい。
    - C: 正しい。
    - D: 誤り。MACsec はルーターと DX ロケーションの間のみ。
    - E: 誤り。公開 IP を使う。

    **スキル:** [暗号化の選択肢](../domain4.md#t4-3-options) / **参照:** [プライベート IP VPN](../../../services/network-connectivity.md#vpn-private-ip), [相互 TLS（mTLS）](../../../services/certificates.md#mtls)

### 問3 {#q3}

暗号化の方法の表をレビューしています。方法と範囲の組み合わせで正しいものはどれですか。

- A. TLS: ルーターと DX ロケーションの L2 の間
- B. Site-to-Site VPN: アプリとアプリの間
- C. MACsec: CGW と Transit Gateway の間
- D. Client VPN: 利用者の端末と VPC の間

??? success "答えと解説"
    **正解: D**

    範囲を覚えます。

    - A: 誤り。アプリの間。
    - B: 誤り。CGW と VGW、Transit Gateway の間。
    - C: 誤り。ルーターと DX ロケーションの間。
    - D: 正しい。

    **スキル:** [暗号化の選択肢](../domain4.md#t4-3-options) / **参照:** [Client VPN](../../../services/network-connectivity.md#client-vpn), [転送時の TLS](../../../services/certificates.md#tls-in-transit)

### 問4 {#q4}

CloudFront でビューワーとの通信を HTTPS に限定し、HTTP のアクセスは自動で誘導します。オリジンの ALB までの区間も暗号化します。設定の組み合わせとして正しいものはどれですか。

- A. ビューワーは `HTTP and HTTPS`、オリジンは `HTTPS Only`
- B. ビューワーは `Redirect HTTP to HTTPS`、オリジンは `HTTPS Only`
- C. ビューワーは `HTTPS Only`、オリジンは `Match Viewer`
- D. ビューワーは `Redirect HTTP to HTTPS`、オリジンは `HTTP Only`

??? success "答えと解説"
    **正解: B**

    両方の区間を設定します。

    - A: 誤り。HTTP を誘導しない。
    - B: 正しい。
    - C: 誤り。HTTP を誘導せず、拒否する。
    - D: 誤り。オリジンの区間が暗号化されない。

    **スキル:** [サービスごとの暗号化](../domain4.md#t4-3-in-transit) / **参照:** [HTTPS](../../../services/networking.md#cloudfront-https), [転送時の TLS](../../../services/certificates.md#tls-in-transit)

### 問5 {#q5}

S3 のバケットへ HTTP でアクセスするクライアントが残っていることが監査で分かりました。今後は HTTP の要求を拒否します。保存時の暗号化は別の要件で設定済みです。最も適切な設定はどれですか。

- A. バケットポリシーで `aws:SecureTransport` の `false` を拒否する
- B. デフォルト暗号化を SSE-KMS に変更して、HTTP の要求も暗号化して受ける
- C. VPC エンドポイントのポリシーで全部の S3 の操作を明示的に許可する
- D. Block Public Access を有効にして、公開の要求として HTTP の要求を拒否する

??? success "答えと解説"
    **正解: A**

    転送時の暗号化を強制します。

    - A: 正しい。
    - B: 誤り。保存時の暗号化で、転送の強制にならない。
    - C: 誤り。エンドポイントを通らない要求は制御できず、強制にならない。
    - D: 誤り。公開の制御で、プロトコルの制御ではない。

    **スキル:** [サービスごとの暗号化](../domain4.md#t4-3-in-transit) / **参照:** [基本と整合性](../../../services/s3.md#basics), [転送時の TLS](../../../services/certificates.md#tls-in-transit)

### 問6 {#q6}

東京の VPC 間は Transit Gateway、東京と大阪の間は Transit Gateway ピアリングです。規制で「VPC 間の全区間の暗号化を、お客様が確認できる形で実施する」ことが必要です。最も適切な対応はどれですか。

- A. ピアリングの AES-256 が同じリージョンの区間にも適用されると説明する
- B. DX の MACsec を有効にして、Transit Gateway の中も暗号化する
- C. アタッチメントのアプライアンスモードで全区間を暗号化する
- D. アプリの TLS か VPN を、同じリージョンの区間にも適用する

??? success "答えと解説"
    **正解: D**

    区間ごとの暗号化を確認します。

    - A: 誤り。リージョン間の暗号化で、同じリージョンの区間には当てはまらない。
    - B: 誤り。別の区間の暗号化。
    - C: 誤り。流れの対称性の設定。
    - D: 正しい。

    **スキル:** [サービスごとの暗号化](../domain4.md#t4-3-in-transit) / **参照:** [ピアリング](../../../services/network-connectivity.md#tgw-peering), [転送時の TLS](../../../services/certificates.md#tls-in-transit)

### 問7 {#q7}

ElastiCache（Redis）へのアプリの通信と、RDS への通信を暗号化します。アプリは接続文字列を変更できます。正しい組み合わせはどれですか。

- A. ElastiCache は保存時の KMS 暗号化、RDS は SG の最小限の許可と監査ログ
- B. どちらも NLB の TLS リスナーを間に入れて暗号化する
- C. どちらも VPC ピアリングで接続して、リージョン内の暗号化に任せる
- D. ElastiCache は `TransitEncryptionEnabled`、RDS は TLS で接続

??? success "答えと解説"
    **正解: D**

    マネージド DB の設定です。

    - A: 誤り。どちらも転送時の暗号化の設定ではない。
    - B: 誤り。マネージド DB の標準の方法ではない。
    - C: 誤り。同じリージョンのピアリングの標準の説明ではなく、DB の設定でもない。
    - D: 正しい。

    **スキル:** [サービスごとの暗号化](../domain4.md#t4-3-in-transit) / **参照:** [統合サービス](../../../services/certificates.md#integrated-services)

### 問8 {#q8}

東京の ALB と CloudFront で同じドメインの ACM の証明書を使います。CloudFront の設定画面で、東京で発行した証明書が選べません。自動更新は維持します。正しい対応はどれですか。

- A. `us-east-1` で別の証明書を発行して設定する
- B. 証明書をエクスポートして、CloudFront へインポートする
- C. 東京の証明書を `us-east-1` へコピーして更新は東京で行う
- D. CloudFront のエッジのリージョンを東京に固定する

??? success "答えと解説"
    **正解: A**

    リージョンの規則です。

    - A: 正しい。
    - B: 誤り。インポートすると自動更新の対象にならない。
    - C: 誤り。証明書はコピーできない。
    - D: 誤り。CloudFront にその設定はない。

    **スキル:** [証明書の管理](../domain4.md#t4-3-certificates) / **参照:** [リージョンのルール](../../../services/certificates.md#region-rules)

### 問9 {#q9}

社内のマイクロサービスの mTLS に使う証明書を発行します。ブラウザーの信頼は不要で、信頼のルートは社内で配布します。証明書の自動更新も使います。最も適切なものはどれですか。

- A. AWS Private CA と ACM の連携
- B. ACM の公開証明書を全部のサービスで使う
- C. Private CA の API で直接発行し、ACM の自動更新を使う
- D. 自己署名の証明書を EC2 で作って手動で配る

??? success "答えと解説"
    **正解: A**

    ACM から発行するなら管理されます。

    - A: 正しい。
    - B: 誤り。社内の名前には使えず、用途も合わない。
    - C: 誤り。API 直接は ACM の更新の対象外。
    - D: 誤り。更新と配布の手間が大きい。

    **スキル:** [証明書の管理](../domain4.md#t4-3-certificates) / **参照:** [AWS Private CA](../../../services/certificates.md#private-ca), [自動更新](../../../services/certificates.md#auto-renewal)

### 問10 {#q10}

ACM の DNS 検証の証明書が更新に失敗しました。担当者が検証の CNAME を消していたことが分かりました。今後の再発の検知も含めて正しい対応はどれですか。

- A. メール検証に切り替えて、担当者の承認なしで更新させる
- B. 証明書を削除して、ACM が自動で再発行するのを待って設定する
- C. CNAME を戻し、期限を EventBridge で監視する
- D. ALB のリスナーを作り直して、新しい証明書を自動で発行させる

??? success "答えと解説"
    **正解: C**

    更新の監視も設定します。

    - A: 誤り。メール検証は承認が要る。
    - B: 誤り。自動の再発行はない。
    - C: 正しい。
    - D: 誤り。更新の手順ではない。

    **スキル:** [証明書の管理](../domain4.md#t4-3-certificates) / **参照:** [自動更新](../../../services/certificates.md#auto-renewal), [更新の監視](../../../services/certificates.md#renewal-monitoring)

### 問11 {#q11}

監査で「DX は専用線だから暗号化は不要」という社内文書が指摘されました。データは規制の対象です。責任共有モデルに照らして正しい説明はどれですか。

- A. 専用線は物理的に分離されるので、規制の対象外になる
- B. DX の区間は AWS が既定で IPsec により暗号化している
- C. DX は既定で暗号化されないので、設定はお客様の責任
- D. AWS のサポートに依頼すると、MACsec が標準で設定される

??? success "答えと解説"
    **正解: C**

    既定で暗号化されません。

    - A: 誤り。平文で通るので、規制があるなら暗号化する。
    - B: 誤り。既定では暗号化されない。
    - C: 正しい。
    - D: 誤り。お客様が選んで設定する。

    **スキル:** [責任共有モデル](../domain4.md#t4-3-shared-responsibility) / **参照:** [責任共有モデル](../../../services/cloud-foundations.md#shared-responsibility)

### 問12 {#q12}

暗号化の責任の分担の表をレビューしています。組み合わせで正しいものを選んでください。（2つ選択）

- A. AWS: Transit Gateway ピアリングのリージョン間の暗号化
- B. AWS: お客様のアプリの TLS のバージョンの設定
- C. AWS: S3 のバケットポリシーでの TLS の強制
- D. お客様: 証明書の管理と TLS の強制
- E. お客様: リージョン間のバックボーンの物理の保護

??? success "答えと解説"
    **正解: A, D**

    分担を整理します。

    - A: 正しい。
    - B: 誤り。お客様の責任。
    - C: 誤り。お客様の設定。
    - D: 正しい。
    - E: 誤り。AWS の責任。

    **スキル:** [責任共有モデル](../domain4.md#t4-3-shared-responsibility) / **参照:** [サービスごとの違い](../../../services/cloud-foundations.md#responsibility-by-service), [ピアリング](../../../services/network-connectivity.md#tgw-peering)

### 問13 {#q13}

EC2 で動く独自の TCP サービスの通信を暗号化します。ACM の証明書を EC2 に置きたいと考えています。前段に ALB や CloudFront は置きません。最も適切な選択はどれですか。

- A. エクスポート可能な公開証明書か ACME の証明書を置く
- B. Nitro の暗号化があるので、責任はお客様から AWS に移る
- C. ACM に EC2 のインスタンス ID を関連付けて自動で配布する
- D. 通常の ACM の公開証明書の秘密鍵をダウンロードして置く

??? success "答えと解説"
    **正解: A**

    通常は前に ALB や CloudFront を置くほうが簡単です。

    - A: 正しい。
    - B: 誤り。アプリの暗号化の責任はお客様。
    - C: 誤り。そのような統合はない。
    - D: 誤り。通常の証明書の秘密鍵は取り出せない。

    **スキル:** [責任共有モデル](../domain4.md#t4-3-shared-responsibility) / **参照:** [統合サービス](../../../services/certificates.md#integrated-services)

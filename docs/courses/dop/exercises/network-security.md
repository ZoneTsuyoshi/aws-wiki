# ネットワークセキュリティと証明書の問題集

対象の解説: [ネットワークセキュリティと証明書](../../../services/networking.md#security-groups-nacls)

### 問1 {#q1}

攻撃の IP を遮断するため、サブネットのネットワーク ACL に拒否のルールを追加しました。同時に、Web サーバーのセキュリティグループで特定の IP を拒否しようとして設定ができませんでした。また、ACL の変更で一部の応答が返らなくなりました。正しい理解はどれですか。（2つ選択）

- A. セキュリティグループには拒否のルールがない
- B. セキュリティグループはステートレスで、戻りの通信の許可が必要
- C. ネットワーク ACL はインスタンスごとに適用される
- D. ネットワーク ACL のルールは番号の大きいものから評価される
- E. ネットワーク ACL はステートレスなので、エフェメラルポートの許可が必要

??? success "答えと解説"
    **正解: A, E**

    特定の IP の遮断はネットワーク ACL です。戻りのためにエフェメラルポートも許可します。

    - A: 正しい。
    - B: 誤り。ステートフルで、戻りの許可は要らない。
    - C: 誤り。サブネットごとに適用される。
    - D: 誤り。小さい番号から評価される。
    - E: 正しい。

    **スキル:** [ネットワーク](../domain6.md#t6-2-network) / **参照:** [セキュリティグループとネットワーク ACL](../../../services/networking.md#security-groups-nacls)、[ネットワーク ACL のルール](../../../services/networking.md#nacl-rules)

### 問2 {#q2}

次の脅威の対策を選びます。(1) VPC から特定のドメインへの通信だけを許可する。(2) API への SQL インジェクションとレートの超過を止める。(3) 大規模な DDoS で SRT の支援を受ける。適切な組み合わせはどれですか。

- A. (1) セキュリティグループ、(2) GuardDuty、(3) Shield Standard
- B. (1) セキュリティグループ、(2) ネットワーク ACL、(3) Shield Standard
- C. (1) Network Firewall、(2) WAF、(3) Shield Advanced
- D. (1) WAF、(2) Network Firewall、(3) Macie

??? success "答えと解説"
    **正解: C**

    層ごとの役割で選びます。

    - A: 誤り。セキュリティグループはドメインを扱わず、GuardDuty は止めない。
    - B: 誤り。いずれも目的に合わない。
    - C: 正しい。
    - D: 誤り。層が入れ違い、Macie は目的が違う。

    **スキル:** [ネットワーク](../domain6.md#t6-2-network) / **参照:** [Network Firewall](../../../services/threat-detection.md#network-firewall)、[AWS WAF](../../../services/certificates.md#waf)、[Shield](../../../services/threat-detection.md#shield)

### 問3 {#q3}

プライベートなデータ処理のサブネットで、インターネットへの経路を完全になくしつつ S3 と DynamoDB を使います。ルートとエンドポイントの組み合わせはどれですか。

- A. NAT ゲートウェイへのルートと、S3 のバケットポリシー
- B. `0.0.0.0/0` のルートを持たず、S3 と DynamoDB のゲートウェイエンドポイントを使う
- C. インターネットゲートウェイへのルートを残し、セキュリティグループの外向きのルールをすべて削除して禁止する
- D. Transit Gateway へのルートと、CloudFront

??? success "答えと解説"
    **正解: B**

    ゲートウェイエンドポイントはルートテーブルに追加し、インターネットを経由しません。

    - A: 誤り。インターネットへの経路が残る。
    - B: 正しい。
    - C: 誤り。経路を残すことになる。
    - D: 誤り。目的のサービスへの閉じた経路にならない。

    **スキル:** [ネットワーク](../domain6.md#t6-2-network) / **参照:** [サブネットとルートテーブル](../../../services/networking.md#subnets-route-tables)、[VPC エンドポイントと PrivateLink](../../../services/networking.md#vpc-endpoints)

### 問4 {#q4}

東京の ALB の前に CloudFront を置き、利用者から CloudFront、CloudFront から ALB の両方を HTTPS にします。証明書は ACM のパブリック証明書を使い、更新は自動にします。適切なリージョンの組み合わせはどれですか。

- A. どちらも東京に作る
- B. CloudFront 用はオリジンと同じ東京、ALB 用はバージニア北部
- C. CloudFront 用は米国東部（バージニア北部）、ALB 用は東京
- D. どちらもバージニア北部に作る

??? success "答えと解説"
    **正解: C**

    CloudFront はバージニア北部、ALB は同じリージョンの ACM の証明書を使います。

    - A: 誤り。CloudFront はバージニア北部の証明書を使う。
    - B: 誤り。逆になっている。
    - C: 正しい。
    - D: 誤り。ALB の証明書は ALB と同じリージョンに作る。

    **スキル:** [証明書](../domain6.md#t6-2-certificates) / **参照:** [リージョンのルール](../../../services/certificates.md#region-rules)、[統合サービス](../../../services/certificates.md#integrated-services)

### 問5 {#q5}

ACM にインポートした証明書の期限切れで障害が起きました。パブリック証明書には切り替えられません。再発を防ぐ組み合わせはどれですか。（2つ選択）

- A. DNS 検証を追加すれば、インポートした証明書も自動更新される
- B. EventBridge や SNS で通知して更新の作業を自動化する
- C. CloudFront のセキュリティポリシーを更新して、証明書の期限を延ばす
- D. ACM のインポートした証明書の自動更新を有効にする
- E. `DaysToExpiry` か Config の `acm-certificate-expiration-check` で期限を監視する

??? success "答えと解説"
    **正解: B, E**

    インポートした証明書は自動更新されません。期限を監視します。

    - A: 誤り。ACM が発行した証明書の話。
    - B: 正しい。
    - C: 誤り。期限は発行元が決めるもので、この設定では変わらない。
    - D: 誤り。インポートした証明書は自動更新されない。
    - E: 正しい。

    **スキル:** [証明書](../domain6.md#t6-2-certificates) / **参照:** [更新の監視](../../../services/certificates.md#renewal-monitoring)、[証明書のインポート](../../../services/certificates.md#import)

### 問6 {#q6}

社内のマイクロサービスの間の mTLS の証明書を発行します。公開の CA からの証明書は使いません。証明書の配布と更新はマネージドに行い、ALB でのクライアント認証も使います。適切な手段はどれですか。

- A. 自己署名の証明書を手で作り、各サーバーへ毎年配布する
- B. IAM Roles Anywhere のトラストアンカーで社内の証明書を発行する
- C. AWS Private CA と ACM の統合
- D. ACM のパブリック証明書を内部のドメインで発行して配布する

??? success "答えと解説"
    **正解: C**

    社内の mTLS には Private CA を使います。ACM 経由で更新できます。

    - A: 誤り。マネージドでなく、更新の手間が大きい。
    - B: 誤り。証明書で AWS の一時的な認証情報を得る仕組みで、証明書を発行しない。
    - C: 正しい。
    - D: 誤り。公開の CA で、社内の要件に合わない。

    **スキル:** [証明書](../domain6.md#t6-2-certificates) / **参照:** [AWS Private CA](../../../services/certificates.md#private-ca)、[相互 TLS（mTLS）](../../../services/certificates.md#mtls)

### 問7 {#q7}

次の問いに答えるサービスを選びます。(1) 怪しい動きがあるか。(2) ソフトウェアの脆弱性があるか。(3) なぜ起きて影響はどこまでか。適切な組み合わせはどれですか。

- A. (1) Security Hub CSPM、(2) Detective、(3) Macie
- B. (1) Config、(2) Security Hub CSPM の標準、(3) Inspector
- C. (1) GuardDuty、(2) Inspector、(3) Detective
- D. (1) Inspector、(2) GuardDuty、(3) Config

??? success "答えと解説"
    **正解: C**

    サービスごとの問いを区別します。

    - A: 誤り。いずれも問いに合わない。
    - B: 誤り。いずれも問いに合わない。
    - C: 正しい。
    - D: 誤り。(1) と (2) が逆で、Config は影響範囲の調査の道具ではない。

    **スキル:** [多層防御](../domain6.md#t6-2-defense-in-depth) / **参照:** [選び方の比較](../../../services/threat-detection.md#choosing)

### 問8 {#q8}

公開の Web アプリに多層防御を入れます。すでに ALB の HTTPS とセキュリティグループがあります。アプリの層と VPC の境界の検査を追加し、設定の準拠も確認します。適切な組み合わせはどれですか。（2つ選択）

- A. GuardDuty の Runtime Monitoring を追加して、アプリの層の検査の代わりにする
- B. CloudFront のカスタムヘッダーで ALB への直接のアクセスを閉じ、VPC の境界の検査の代わりにする
- C. Network Firewall で VPC の境界を検査し、Config のルールで設定を評価する
- D. ALB に WAF のウェブ ACL を関連付ける
- E. ネットワーク ACL で送信元の IP を絞り、アプリの層の検査の代わりにする

??? success "答えと解説"
    **正解: C, D**

    1 つの防御が破られても次で止まるように重ねます。

    - A: 誤り。脅威の検出で、リクエストを検査して止めない。
    - B: 誤り。入口の制限で、VPC の境界の通信の検査にならない。
    - C: 正しい。
    - D: 正しい。
    - E: 誤り。IP とポートの制御で、アプリの層の内容を検査できない。

    **スキル:** [多層防御](../domain6.md#t6-2-defense-in-depth) / **参照:** [AWS WAF](../../../services/certificates.md#waf)、[Network Firewall](../../../services/threat-detection.md#network-firewall)、[セキュリティグループとネットワーク ACL](../../../services/networking.md#security-groups-nacls)

### 問9 {#q9}

GuardDuty、Inspector、Config、Macie の結果を一か所で優先付けし、1 つの検出結果の原因は別の画面で深く調べます。適切な組み合わせはどれですか。

- A. 集約に CloudTrail、調査に Trusted Advisor
- B. 集約に Security Hub、調査に Detective
- C. 集約に Detective、調査に Security Hub
- D. 集約に Config、調査に Inspector

??? success "答えと解説"
    **正解: B**

    集約と優先付けは Security Hub、原因の調査は Detective です。

    - A: 誤り。どちらも役割に合わない。
    - B: 正しい。
    - C: 誤り。役割が逆。
    - D: 誤り。Config は他の検出結果の集約の役割ではない。

    **スキル:** [多層防御](../domain6.md#t6-2-defense-in-depth) / **参照:** [Security Hub](../../../services/threat-detection.md#security-hub)、[GuardDuty](../../../services/threat-detection.md#guardduty)

### 問10 {#q10}

3 層の Web アプリの通信を見直します。DB のセキュリティグループで、アプリ層の IP 範囲を毎回更新しており、Auto Scaling で IP が変わるとエラーになります。また、許可されない通信の送信元を確認したいと考えています。適切な組み合わせはどれですか。（2つ選択）

- A. CloudTrail の管理イベントを Athena で検索して、拒否された通信の送信元を調べる
- B. VPC フローログを `REJECT` で確認する
- C. アプリ層のインスタンスに Elastic IP を割り当てて、IP を固定してから許可する
- D. DB のサブネットのネットワーク ACL に、アプリ層の全インスタンスの IP を自動で追記する Lambda を作る
- E. DB のセキュリティグループのソースにアプリ層のセキュリティグループを指定する

??? success "答えと解説"
    **正解: B, E**

    セキュリティグループはソースに別のセキュリティグループを指定できます。通信の拒否はフローログで確認します。

    - A: 誤り。API の記録で、通信の記録ではない。
    - B: 正しい。
    - C: 誤り。台数の増減に合わず、データベース接続に公開の IP を使う設計も不適切。
    - D: 誤り。同じ運用の問題を自作の処理で抱えることになる。
    - E: 正しい。

    **スキル:** [ネットワーク](../domain6.md#t6-2-network) / **参照:** [VPC フローログ](../../../services/networking.md#flow-logs)、[セキュリティグループのルール](../../../services/networking.md#security-group-rules)

# 監査とログの問題集

対象の解説: [監査とログ](../../../services/observability.md#cloudtrail)

### 問1 {#q1}

組織のログは、ログ保管アカウントの S3 に集めています。規制で、7 年間は誰にも削除や上書きができないようにします。管理者が権限を奪われた場合も同じです。何を使いますか。

- A. バージョニングと MFA Delete を有効にしたバケット
- B. ライフサイクルで Glacier へ移し、バケットポリシーで削除を拒否する
- C. Object Lock のコンプライアンスモードで 7 年の保持期間を指定する
- D. ガバナンスモードの Object Lock と、管理者だけのバイパスの権限

??? success "答えと解説"
    **正解: C**

    コンプライアンスモードは保持期間の間、root ユーザーでも削除できません。

    - A: 誤り。権限と MFA を奪われると防げない。
    - B: 誤り。管理者がポリシーを変更できる。
    - C: 正しい。
    - D: 誤り。権限があれば解除できる。

    **スキル:** [安全な保管](../domain4.md#t4-1-secure-storage) / **参照:** [Object Lock](../../../services/s3.md#object-lock)、[マルチアカウントのパターン](../../../services/governance.md#multi-account-patterns)

### 問2 {#q2}

監査人は、CloudTrail のログファイルが配信の後に変更されていないことを確かめたいと考えています。また、組織の全アカウントの証跡を一か所に集め、メンバーアカウントから証跡を止められないようにします。適切な組み合わせはどれですか。（2つ選択）

- A. 管理アカウントか委任管理者で組織の証跡を作る
- B. S3 のサーバーアクセスログを有効にすれば、ログの改ざんを検知できる
- C. メンバーアカウントごとに別の証跡を作り、それぞれのバケットに置く
- D. CloudTrail の代わりに Config のレコーダーで API の履歴を残す
- E. ログファイルの検証を有効にする

??? success "答えと解説"
    **正解: A, E**

    検証で改ざんを検知できます。組織の証跡はメンバーアカウントから変更できません。

    - A: 正しい。
    - B: 誤り。アクセスの記録で、内容の検証ではない。
    - C: 誤り。集約にならず、メンバーが止められる。
    - D: 誤り。Config は API の記録の代わりにならない。
    - E: 正しい。

    **スキル:** [安全な保管](../domain4.md#t4-1-secure-storage) / **参照:** [証跡とイベント履歴](../../../services/observability.md#cloudtrail-trails)、[CloudTrail の設定](../../../services/observability.md#cloudtrail)

### 問3 {#q3}

中央のログバケットの読み取りを、監査ロールだけに限ります。S3 の管理者であっても、KMS の復号の権限がなければログの中身を読めないようにします。適切な組み合わせはどれですか。

- A. S3 のアクセスポイントを監査ロール専用にして、バケットへの直接のアクセスを閉じる
- B. SSE-S3 の暗号化と、バケットの ACL で監査ロールだけを許可する
- C. SSE-KMS の AWS 管理キー `aws/s3` を使い、バケットポリシーで監査ロールを許可する
- D. SSE-KMS のカスタマー管理キーと、バケットポリシーとキーポリシーで監査ロールを許可する

??? success "答えと解説"
    **正解: D**

    カスタマー管理キーのキーポリシーで、データの読み取りを分離できます。

    - A: 誤り。アクセスの経路の制御で、S3 の管理者とキーの権限を分けられない。
    - B: 誤り。SSE-S3 にはキーの権限を分ける仕組みがない。
    - C: 誤り。`aws/s3` のキーポリシーは変更できず、読み取りをキーの権限で分けられない。
    - D: 正しい。

    **スキル:** [安全な保管](../domain4.md#t4-1-secure-storage) / **参照:** [ブロックパブリックアクセス](../../../services/s3.md#block-public-access)、[キーポリシー、IAM、グラント](../../../services/kms.md#access-control)

### 問4 {#q4}

S3 の特定のバケットで、誰がどのオブジェクトをダウンロードしたかが必要になりました。既定の証跡には記録されていません。Lambda の呼び出しも同様です。費用は対象を絞って抑えます。設定はどれですか。

- A. CloudTrail Insights を有効にして、呼び出しの量の変化を確認する
- B. 管理イベントの読み取りを有効にして、全リージョンで記録する
- C. 対象のバケットと関数に絞って、証跡のデータイベントを有効にする
- D. Config のレコーダーで S3 のオブジェクトの変更履歴を記録する

??? success "答えと解説"
    **正解: C**

    S3 のオブジェクト操作や Lambda の呼び出しはデータイベントで、有効化が必要です。

    - A: 誤り。量の異常の検知で、個別の操作の記録ではない。
    - B: 誤り。S3 のオブジェクト操作は管理イベントに含まれない。
    - C: 正しい。
    - D: 誤り。Config はオブジェクトの操作の履歴を記録しない。

    **スキル:** [CloudTrail](../domain4.md#t4-2-cloudtrail) / **参照:** [イベントの種類](../../../services/observability.md#cloudtrail-events)

### 問5 {#q5}

次の要件に合う CloudTrail の機能の組み合わせはどれですか。(1) 通常と違う量の `RunInstances` を自動で検知する。(2) 半年前の API の履歴を残す。イベント履歴だけでは足りません。

- A. (1) GuardDuty の抑制ルール、(2) CloudWatch のメトリクスの保持の延長
- B. (1) 管理イベントの履歴の手動の確認、(2) イベント履歴の 90 日を延ばす設定
- C. (1) CloudTrail Insights、(2) 証跡を作成してログを S3 に配信する
- D. (1) データイベント、(2) CloudTrail Lake を新規に有効化する

??? success "答えと解説"
    **正解: C**

    Insights は通常と違う呼び出しの量を検知します。90 日より長く残すには証跡を作ります。

    - A: 誤り。目的が違う。
    - B: 誤り。自動ではなく、イベント履歴の期間は延ばせない。
    - C: 正しい。
    - D: 誤り。量の異常を検知せず、Lake は新規受付を終了している。

    **スキル:** [CloudTrail](../domain4.md#t4-2-cloudtrail) / **参照:** [CloudTrail Insights](../../../services/observability.md#cloudtrail-insights)、[証跡とイベント履歴](../../../services/observability.md#cloudtrail-trails)

### 問6 {#q6}

本番のセキュリティグループが昨夜変更され、接続の障害が起きました。(1) 誰が変更したか。(2) 変更の前の規則はどうだったか。それぞれ何で確認しますか。

- A. (1) VPC フローログ、(2) CloudTrail の管理イベント
- B. (1) AWS Config、(2) VPC フローログ
- C. (1) AWS Config、(2) CloudTrail のデータイベント
- D. (1) CloudTrail、(2) AWS Config

??? success "答えと解説"
    **正解: D**

    誰が変更したかは CloudTrail、設定がどうだったかは Config です。

    - A: 誤り。フローログは通信の記録で変更者を示さず、管理イベントは変更の呼び出しで前の規則の全体を示さない。
    - B: 誤り。変更の主体は CloudTrail で確かめ、フローログは規則を示さない。
    - C: 誤り。データイベントは設定の履歴ではなく、(1) の主体の確認にも CloudTrail が向く。
    - D: 正しい。

    **スキル:** [CloudTrail](../domain4.md#t4-2-cloudtrail) / **参照:** [Config と CloudTrail の違い](../../../services/governance.md#config-vs-cloudtrail)、[イベントの種類](../../../services/observability.md#cloudtrail-events)

### 問7 {#q7}

監査で次の問いが出ました。(1) 誰がいつこの操作をしたか。(2) この EC2 への通信は許可されたか。(3) IaC の外で変更されたか。適切な組み合わせはどれですか。

- A. (1) AWS Config、(2) Network Firewall のログ、(3) Detective
- B. (1) AWS Config の設定履歴、(2) CloudTrail の管理イベント、(3) X-Ray
- C. (1) CloudTrail、(2) VPC フローログ、(3) ドリフト検出
- D. (1) VPC フローログ、(2) ドリフト検出、(3) CloudTrail

??? success "答えと解説"
    **正解: C**

    サービスごとに記録するものが違います。

    - A: 誤り。いずれも問いに合わない。
    - B: 誤り。(2) と (3) の手がかりが合わない。
    - C: 正しい。
    - D: 誤り。手がかりが入れ違っている。

    **スキル:** [監査](../domain6.md#t6-3-audit-services) / **参照:** [CloudTrail の設定](../../../services/observability.md#cloudtrail)、[VPC フローログ](../../../services/networking.md#flow-logs)、[ドリフト検出](../../../services/iac.md#drift)

### 問8 {#q8}

管理者が誤って CloudTrail を止め、監査の空白が生まれました。全アカウントで再発を防ぎ、改ざんも検知します。適切な組み合わせはどれですか。（2つ選択）

- A. 組織の証跡と、`cloudtrail:StopLogging` と `DeleteTrail` を拒否する SCP
- B. ログファイルの検証と、ログ保管アカウントの S3 の Object Lock
- C. CloudTrail のログを各アカウントの S3 にも残し、バケットのバージョニングを有効にする
- D. CloudWatch のアラームで `StopLogging` を検知し、当番へ通知するだけにする
- E. Config の `cloudtrail-enabled` で検出して、各アカウントの管理者が手で再開する

??? success "答えと解説"
    **正解: A, B**

    監査の仕組みそのものを守ります。

    - A: 正しい。
    - B: 正しい。
    - C: 誤り。各アカウントの管理者が止められる状態は変わらず、再発を防げない。
    - D: 誤り。検知だけで、止める操作を防げない。
    - E: 誤り。空白が生まれた後の検出で、再発を防げない。

    **スキル:** [監査](../domain6.md#t6-3-audit-services) / **参照:** [マルチアカウントのパターン](../../../services/governance.md#multi-account-patterns)、[証跡とイベント履歴](../../../services/observability.md#cloudtrail-trails)

### 問9 {#q9}

監査人の依頼で、EBS の暗号化の基準の準拠を過去 1 年で示します。全アカウントの結果を 1 か所から確認します。適切な手段はどれですか。

- A. CloudTrail のイベント履歴で全 API を読む
- B. Inspector の検出結果の履歴を確認する
- C. Trusted Advisor の週次のレポートを毎週 S3 へ保存して、監査人へ渡す
- D. AWS Config の設定と準拠の履歴をアグリゲーターで確認する

??? success "答えと解説"
    **正解: D**

    Config は設定と準拠の履歴を残します。

    - A: 誤り。90 日までで、準拠の状態を示さない。
    - B: 誤り。脆弱性の結果で、設定の基準の評価ではない。
    - C: 誤り。基準の評価の履歴にならない。
    - D: 正しい。

    **スキル:** [監査](../domain6.md#t6-3-audit-services) / **参照:** [Config と CloudTrail の違い](../../../services/governance.md#config-vs-cloudtrail)、[設定レコーダー](../../../services/governance.md#config-recorder)

### 問10 {#q10}

S3 の機密バケットの `GetObject` を監査します。全バケットで有効にすると費用が高くなります。また、CloudTrail の特定のイベントでリアルタイムに検索とアラームを設定します。適切な組み合わせはどれですか。（2つ選択）

- A. 証跡の CloudWatch Logs への送信
- B. 全バケットのデータイベントと、ログの S3 からの毎週のダウンロード
- C. 機密バケットに絞ったデータイベントの有効化
- D. CloudTrail Lake の新しいイベントデータストア
- E. Macie の検出結果を監査ログの代わりにする

??? success "答えと解説"
    **正解: A, C**

    データイベントは対象を絞ります。検索やアラームは CloudWatch Logs へ送ります。

    - A: 正しい。
    - B: 誤り。費用の条件に反し、リアルタイムでない。
    - C: 正しい。
    - D: 誤り。新規受付を終了している。
    - E: 誤り。オブジェクト操作の記録にならない。

    **スキル:** [ログの設定](../domain6.md#t6-3-logging) / **参照:** [イベントの種類](../../../services/observability.md#cloudtrail-events)

### 問11 {#q11}

インシデントの調査に備えて、ALB、CloudFront、WAF のログを有効にします。WAF が判定した内容は残しますが、認証ヘッダーの値はログに残さないようにします。適切な組み合わせはどれですか。

- A. それぞれのログを有効にし、認証ヘッダーは ALB のアクセスログの設定でマスクする
- B. それぞれのログを有効にし、WAF のログのフィールドの編集で機密の項目を隠す
- C. 費用を抑えるため WAF のログをやめて、ALB のアクセスログだけで WAF の判定を確認する
- D. それぞれのログを有効にし、WAF のルールで認証ヘッダーを削除してからログへ送る

??? success "答えと解説"
    **正解: B**

    それぞれのアクセスログを有効にします。WAF はログのフィールドを編集できます。

    - A: 誤り。WAF のログのヘッダーは ALB の設定では隠せず、そのようなマスクの設定もない。
    - B: 正しい。
    - C: 誤り。WAF の判定の詳細を失う。
    - D: 誤り。WAF のルールはヘッダーを削除する仕組みではなく、バックエンドの認証も壊す。

    **スキル:** [ログの設定](../domain6.md#t6-3-logging) / **参照:** [ログ](../../../services/certificates.md#waf-logging)、[ログ](../../../services/networking.md#cloudfront-logs)

### 問12 {#q12}

EC2 のアプリのログに顧客のメールアドレスが含まれます。組織の基準はアプリのログの集約、機密情報のマスク、一定期間の保持です。適切な組み合わせはどれですか。

- A. CloudWatch エージェントで集約し、データ保護ポリシーと保持期間を設定する
- B. ログの保持を無期限にして、KMS のキーでマスクする
- C. CloudWatch エージェントで集約し、メトリクスフィルターで機密情報を隠して保持を設定する
- D. アプリのログを Firehose で S3 へ送り、Macie の検出でマスクして保持を設定する

??? success "答えと解説"
    **正解: A**

    ログをエージェントで集約し、データ保護ポリシーでマスクし、保持期間を設定します。

    - A: 正しい。
    - B: 誤り。KMS はマスクの機能ではない。
    - C: 誤り。メトリクスフィルターは数えるだけで、ログを隠さない。
    - D: 誤り。Macie は検出で、ログをマスクしない。

    **スキル:** [ログの設定](../domain6.md#t6-3-logging) / **参照:** [ロギング戦略](../../../services/observability.md#logging-strategy)、[データ保護ポリシー](../../../services/observability.md#logs-data-protection)

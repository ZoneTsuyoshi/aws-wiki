# 脅威の検出の問題集

対象の解説: [脅威の検出](../../../services/threat-detection.md#choosing)

### 問1 {#q1}

組織の EC2、ECR のイメージ、Lambda の脆弱性を継続的に確認します。担当者は過去の資料を見て、評価テンプレートを作りエージェントを導入する計画を立てています。2026 年の時点の正しい手順はどれですか。

- A. Config のカスタムルールで CVE の有無を判定する処理を自作する
- B. Inspector Classic の評価テンプレートとルールパッケージを作り、週次で実行する
- C. 委任管理者で Amazon Inspector を有効にする。テンプレートは作らない
- D. GuardDuty の検出結果から CVE の一覧を手で作る

??? success "答えと解説"
    **正解: C**

    現在の Inspector はテンプレートを作らず、有効にすれば自動でスキャンします。

    - A: 誤り。標準のスキャンを自作することになる。
    - B: 誤り。Inspector Classic はサポートが終了した。
    - C: 正しい。
    - D: 誤り。GuardDuty は脅威の検出で、ソフトウェアの脆弱性のスキャンではない。

    **スキル:** [Inspector](../domain4.md#t4-2-inspector) / **参照:** [Inspector](../../../services/threat-detection.md#inspector)、[スキャンの種類](../../../services/threat-detection.md#inspector-scan-types)

### 問2 {#q2}

EC2 の Inspector で一部のインスタンスがスキャンされません。修正のパッチを適用した後、検出結果はどうなりますか。適切な組み合わせはどれですか。（2つ選択）

- A. パッチの適用の後、検出結果を担当者が必ず手で閉じる
- B. 古い評価テンプレートの実行スケジュールを確認する
- C. 修正が確認されると、検出結果は自動で閉じられる
- D. パッチベースラインが Inspector を呼ぶ設定を確認する
- E. SSM のマネージドノードか、エージェントレスのスキャンの条件を確認する

??? success "答えと解説"
    **正解: C, E**

    スキャンの前提を確認します。修正が確認されると、検出結果は自動で閉じられます。

    - A: 誤り。自動で閉じられる。
    - B: 誤り。現在の Inspector にテンプレートはない。
    - C: 正しい。
    - D: 誤り。パッチベースラインは Inspector を呼ばない。
    - E: 正しい。

    **スキル:** [Inspector](../domain4.md#t4-2-inspector) / **参照:** [EC2 のスキャン](../../../services/threat-detection.md#inspector-ec2)、[検出結果と管理](../../../services/threat-detection.md#inspector-findings)

### 問3 {#q3}

次の検査のうち、Inspector の範囲に含まれないものはどれですか。パイプラインとコンテナの検査の担当を決めるときに確認します。

- A. EC2 のネットワーク到達性の確認
- B. ECR のイメージの CVE のスキャン
- C. S3 オブジェクトの個人情報の検出
- D. Lambda の依存関係と独自のコードの確認

??? success "答えと解説"
    **正解: C**

    S3 の機密データの検出は Macie の役割です。

    - A: 誤り。Inspector の範囲に含まれる。
    - B: 誤り。Inspector の範囲に含まれる。
    - C: 正しい。
    - D: 誤り。Inspector の範囲に含まれる。

    **スキル:** [Inspector](../domain4.md#t4-2-inspector) / **参照:** [Lambda とコードのスキャン](../../../services/threat-detection.md#inspector-code)、[ECR のスキャン](../../../services/threat-detection.md#inspector-ecr)、[ネットワーク到達性](../../../services/threat-detection.md#inspector-network)

### 問4 {#q4}

全アカウント、全リージョンの Security Hub CSPM の標準を統一します。例外の OU には別の標準を適用し、新しいアカウントへも自動で適用します。適切な機能はどれですか。

- A. Config の修復で標準を有効にする
- B. SCP で標準の無効化を拒否し、有効化は担当者に任せる
- C. 各アカウントで標準を手で有効にする
- D. 中央設定の設定ポリシー

??? success "答えと解説"
    **正解: D**

    中央設定で、アカウント、OU、リージョンをまたいで管理します。

    - A: 誤り。標準の管理の仕組みではない。
    - B: 誤り。有効化の統一にならない。
    - C: 誤り。手間が増え、自動にならない。
    - D: 正しい。

    **スキル:** [自動適用](../domain6.md#t6-2-automation) / **参照:** [組織と集約](../../../services/threat-detection.md#security-hub-org)

### 問5 {#q5}

組織の全アカウントの ALB に同じ WAF のルールを適用します。新しい ALB にも自動で適用します。全 VPC のセキュリティグループの基準も配ります。適切なサービスはどれですか。

- A. Firewall Manager
- B. Service Catalog のポートフォリオで WAF の製品を配布する
- C. WAF のウェブ ACL を各アカウントで手で作り、ALB ごとに関連付ける
- D. Network Firewall の組織のルールグループを ALB へ関連付ける

??? success "答えと解説"
    **正解: A**

    WAF やセキュリティグループを組織に配るなら Firewall Manager です。

    - A: 正しい。
    - B: 誤り。新しい ALB への自動の適用にならない。
    - C: 誤り。手間が増え、自動にならない。
    - D: 誤り。ALB の WAF の配布の手段にならない。

    **スキル:** [自動適用](../domain6.md#t6-2-automation) / **参照:** [Firewall Manager](../../../services/threat-detection.md#firewall-manager)

### 問6 {#q6}

Security Hub CSPM の検出結果のうち、開発用アカウントの一部は重要度を下げて通知しません。本番の特定の S3 の公開の検出結果は、自動で修復します。適切な組み合わせはどれですか。（2つ選択）

- A. Security Hub の自動化ルールで重要度を調整する
- B. GuardDuty の抑制ルールで Security Hub CSPM の全検出結果を止める
- C. Security Hub CSPM を開発用アカウントで無効にして基準を外す
- D. CloudTrail の証跡を止めて検出の件数を減らす
- E. `Security Hub Findings - Imported` のイベントで Automation を動かす

??? success "答えと解説"
    **正解: A, E**

    重要度の調整は自動化ルール、修復は EventBridge と Automation です。

    - A: 正しい。
    - B: 誤り。GuardDuty の検出結果にしか効かない。
    - C: 誤り。監視を失う。
    - D: 誤り。監査の仕組みを失う。
    - E: 正しい。

    **スキル:** [自動適用](../domain6.md#t6-2-automation) / **参照:** [自動化](../../../services/threat-detection.md#security-hub-automation)、[EventBridge による自動化](../../../services/threat-detection.md#ir-eventbridge)

### 問7 {#q7}

担当者が GuardDuty を使い始めるために、VPC フローログと CloudTrail の証跡、DNS ログを全アカウントで有効にする作業を計画しています。正しい指摘はどれですか。

- A. 基本のデータとは別に、CloudTrail の S3 データイベントを全バケットで有効にしておく必要がある
- B. 全部を有効にしたうえで、ログを GuardDuty へ送るサブスクリプションを作る必要がある
- C. GuardDuty は基本のデータを独立して取得して分析するので、ログを自分で有効にする必要はない
- D. VPC フローログだけは自分で有効にしておけば、残りは GuardDuty が自動で分析する

??? success "答えと解説"
    **正解: C**

    GuardDuty は CloudTrail、VPC フローログ、DNS ログを独立して分析します。

    - A: 誤り。GuardDuty を使い始める前提ではなく、S3 の保護も独立して動く。
    - B: 誤り。独立して分析するので不要。
    - C: 正しい。
    - D: 誤り。VPC フローログも GuardDuty が独立して取得する。

    **スキル:** [検出のサービス](../domain6.md#t6-3-vulnerability-services) / **参照:** [データソース](../../../services/threat-detection.md#guardduty-data-sources)

### 問8 {#q8}

次の検出の対象とサービスの組み合わせとして、適切なものはどれですか。(1) 組織の外へ共有された S3 と KMS キー。(2) コンテナイメージの CVE。(3) 暗号化なしの EBS。

- A. (1) Config、(2) GuardDuty、(3) Access Analyzer
- B. (1) Inspector のネットワーク到達性、(2) Access Analyzer、(3) GuardDuty の EBS の検査
- C. (1) IAM Access Analyzer、(2) Inspector、(3) AWS Config
- D. (1) GuardDuty、(2) Macie、(3) Inspector

??? success "答えと解説"
    **正解: C**

    外部へ公開されたリソースは Access Analyzer、脆弱性は Inspector、設定は Config です。

    - A: 誤り。対象が入れ違っている。
    - B: 誤り。対象が入れ違っている。
    - C: 正しい。
    - D: 誤り。いずれも対象が違う。

    **スキル:** [検出のサービス](../domain6.md#t6-3-vulnerability-services) / **参照:** [外部アクセスの検出](../../../services/identity-directory.md#aa-external)、[Inspector](../../../services/threat-detection.md#inspector)

### 問9 {#q9}

EC2 の暗号通貨のマイニングや、不審な IP からの認証情報の利用を検出します。S3 の不審なデータアクセスと、EKS の監査ログの脅威も見ます。適切な組み合わせはどれですか。（2つ選択）

- A. GuardDuty を有効にする
- B. GuardDuty の S3 保護と EKS 保護を有効にする
- C. Macie で不審な IP の接続を検出する
- D. Config のルールで暗号通貨のマイニングを見つける
- E. Inspector のスキャンで脅威の行動を見る

??? success "答えと解説"
    **正解: A, B**

    不審な動きは GuardDuty です。保護プランで対象を広げます。

    - A: 正しい。
    - B: 正しい。
    - C: 誤り。Macie は機密データの検出。
    - D: 誤り。設定の評価で、行動の検出ではない。
    - E: 誤り。脆弱性のスキャンで、行動の分析ではない。

    **スキル:** [検出のサービス](../domain6.md#t6-3-vulnerability-services) / **参照:** [保護プラン](../../../services/threat-detection.md#guardduty-protection-plans)、[検出結果](../../../services/threat-detection.md#guardduty-findings)

### 問10 {#q10}

開発者の誤りで、公開リポジトリに本番の IAM ユーザーのアクセスキーが 3 時間前から載っていました。漏えいの被害を止め、影響を調べ、後片付けをします。正しい順序はどれですか。

- A. 作られたリソースを先にすべて削除し、次にキーを無効化してから CloudTrail で調べる
- B. 公開リポジトリの履歴からコミットを消してキーは有効のまま残し、CloudTrail で不審な操作がないかを先に調べる
- C. CloudTrail で使われた操作を調べ終えてから、作られたリソースを消してキーを無効化する
- D. キーを無効化し、CloudTrail で使われた操作を調べ、作られたリソースと追加の認証情報を消す

??? success "答えと解説"
    **正解: D**

    キーを無効化して被害を止め、CloudTrail で調べて、リソースを消します。

    - A: 誤り。キーが有効な間は、消した後も作られ続ける。
    - B: 誤り。既にコピーされたおそれがあり、キーが有効なまま。
    - C: 誤り。調べている間もキーを使われ続ける。
    - D: 正しい。

    **スキル:** [脅威](../domain6.md#t6-3-threats) / **参照:** [認証情報の漏えい](../../../services/threat-detection.md#ir-credentials)、[アクセスキーの扱い](../../../services/iam.md#access-key-handling)

### 問11 {#q11}

組織の全 S3 バケットの公開を防ぎ、基準を変更できないようにします。公開済みのものも検出します。適切な組み合わせはどれですか。（2つ選択）

- A. 全バケットのポリシーで `aws:SecureTransport` が false のアクセスを拒否する
- B. バケットごとの ACL を毎週手で確認する
- C. Config の `s3-bucket-public-read-prohibited` と Access Analyzer の検出
- D. Macie の検出ジョブを週 1 回実行するだけ
- E. アカウントのブロックパブリックアクセスと、その変更を拒否する SCP

??? success "答えと解説"
    **正解: C, E**

    予防はブロックパブリックアクセスと SCP、検出は Config と Access Analyzer です。

    - A: 誤り。通信の暗号化の強制で、公開の防止にならない。
    - B: 誤り。手作業で、規模に合わない。
    - C: 正しい。
    - D: 誤り。公開設定の検出と防止の手段にならない。
    - E: 正しい。

    **スキル:** [脅威](../domain6.md#t6-3-threats) / **参照:** [ブロックパブリックアクセス](../../../services/s3.md#block-public-access)、[SCP](../../../services/governance.md#scp)

### 問12 {#q12}

複数のアカウントの公開の Web アプリに HTTP のアクセスが残っています。監査では、安全でない通信の継続的な検出と修復を求められています。ALB と CloudFront を使っています。適切な組み合わせはどれですか。

- A. 検出は Config の `alb-http-to-https-redirection-check`、修復は ALB と CloudFront の HTTPS へのリダイレクト
- B. 検出は Security Hub CSPM の標準、修復は WAF のレートベースのルールで HTTP のリクエストを制限する
- C. 検出は Inspector のネットワーク到達性、修復はセキュリティグループで 443 番だけを開く
- D. 検出は VPC フローログの 80 番の週次の集計、修復はネットワーク ACL で 80 番を全面拒否する

??? success "答えと解説"
    **正解: A**

    HTTP の通信は Config で検出し、ALB や CloudFront でリダイレクトします。

    - A: 正しい。
    - B: 誤り。WAF のレート制限は HTTP を HTTPS へ変えない。
    - C: 誤り。リダイレクトの設定の評価にならず、80 番を閉じると利用者の接続が失敗する。
    - D: 誤り。継続的な設定の評価にならず、全面拒否では HTTPS へのリダイレクトも届かなくなる。

    **スキル:** [脅威](../domain6.md#t6-3-threats) / **参照:** [HTTPS](../../../services/networking.md#cloudfront-https)、[リスナーとルール](../../../services/networking.md#alb-listeners)

### 問13 {#q13}

GuardDuty の結果を通知します。重要度の高いものは当番へ、それ以外は Slack へ送ります。承認済みのスキャナーからの検出結果は通知しないで、記録だけ残します。適切な組み合わせはどれですか。

- A. EventBridge で重要度ごとのルールと、GuardDuty の抑制ルール
- B. SNS の購読のフィルターポリシーで、スキャナーの検出結果を当番の宛先から除く
- C. Security Hub CSPM の自動化ルールでスキャナーの結果を `SUPPRESSED` にし、通知は 1 つの SNS トピックへ送る
- D. CloudWatch アラームで全検出結果の件数を数え、1 件でも増えたら当番へ通知する

??? success "答えと解説"
    **正解: A**

    EventBridge で重要度に応じて通知します。想定内のものは抑制ルールで除きます。

    - A: 正しい。
    - B: 誤り。検出結果の抑制の仕組みにならない。
    - C: 誤り。重要度で宛先を分けられず、GuardDuty の結果の扱いとしても遠回りになる。
    - D: 誤り。重要度で分けられない。

    **スキル:** [通知](../domain6.md#t6-3-alerting) / **参照:** [イベント連携とエクスポート](../../../services/threat-detection.md#guardduty-events)、[抑制ルールとリスト](../../../services/threat-detection.md#guardduty-suppression)

### 問14 {#q14}

ルートユーザーは緊急時しか使わない方針です。ログインがあれば、数分以内にセキュリティ担当へ通知します。全リージョンの証跡はあります。追加のサーバーは使いません。適切な方法はどれですか。

- A. Trusted Advisor のセキュリティのチェックを毎週確認し、ルートの MFA の状況とあわせて報告する
- B. CloudTrail の `ConsoleLogin` を EventBridge かメトリクスフィルターで受ける
- C. IAM Access Analyzer の外部アクセスの検出で、ルートユーザーのサインインの結果を確認して通知する
- D. IAM の認証情報レポートを 1 時間ごとに Lambda で取得し、ルートの最終利用の時刻を前回と比べて通知する

??? success "答えと解説"
    **正解: B**

    CloudTrail を EventBridge で受けるか、メトリクスフィルターとアラームを使います。

    - A: 誤り。遅く、目的が違う。
    - B: 正しい。
    - C: 誤り。外部アクセスの検出で、サインインの検知の手段ではない。
    - D: 誤り。レポートの生成には間隔の制限があり、数分以内の要件に合わない。

    **スキル:** [通知](../domain6.md#t6-3-alerting) / **参照:** [メトリクスフィルター](../../../services/observability.md#metric-filters)、[ルールとイベントパターン](../../../services/messaging.md#eventbridge-rules)

### 問15 {#q15}

次の検知を設定します。(1) `RunInstances` の呼び出しの量が平常から急に増えた。(2) S3 の暗号化の設定が基準に合わなくなった。適切な組み合わせはどれですか。

- A. (1) CloudTrail Insights、(2) `Config Rules Compliance Change`
- B. (1) CloudWatch の API メトリクスの固定のしきい値、(2) Trusted Advisor のセキュリティのチェック
- C. (1) Config のルール、(2) CloudTrail Insights
- D. (1) GuardDuty の検出結果、(2) Security Hub CSPM の手動の週次レポート

??? success "答えと解説"
    **正解: A**

    量の急増は CloudTrail Insights、準拠の変化は Config のイベントです。

    - A: 正しい。
    - B: 誤り。固定のしきい値では平常の変化に合わせられず、Trusted Advisor は準拠の変化のイベントではない。
    - C: 誤り。役割が逆。
    - D: 誤り。どちらも目的が違う。

    **スキル:** [通知](../domain6.md#t6-3-alerting) / **参照:** [CloudTrail Insights](../../../services/observability.md#cloudtrail-insights)、[Config ルール](../../../services/governance.md#config-rules)

### 問16 {#q16}

インシデントの調査です。(1) 特定の EC2 への拒否された通信の送信元の一覧。(2) 漏れたキーが呼んだ API の一覧。適切な組み合わせはどれですか。

- A. (1) CloudTrail の管理イベント、(2) VPC フローログ
- B. (1) Config の設定履歴でセキュリティグループを調べる、(2) Inspector の検出結果でキーの利用を確認する
- C. (1) VPC フローログを `REJECT` で絞る、(2) Athena で CloudTrail を問い合わせる
- D. (1) X-Ray のサービスマップで失敗の接続を調べる、(2) GuardDuty の検出結果の一覧で API を確認する

??? success "答えと解説"
    **正解: C**

    通信はフローログ、API は CloudTrail です。

    - A: 誤り。手がかりが逆。
    - B: 誤り。どちらも目的が違う。
    - C: 正しい。
    - D: 誤り。どちらも目的が違う。

    **スキル:** [分析](../domain6.md#t6-3-analysis) / **参照:** [VPC フローログの調査](../../../services/threat-detection.md#investigate-flow-logs)、[CloudTrail の調査](../../../services/threat-detection.md#investigate-cloudtrail)

### 問17 {#q17}

GuardDuty の検出結果の影響範囲を、関連する IP とロールのつながりから調べます。別に、複数のソースのログを正規化して社内の SIEM へ流します。適切な組み合わせはどれですか。（2つ選択）

- A. 影響範囲の調査は Security Hub CSPM の検出結果の集約
- B. ログの正規化は Data Firehose の配信と S3 のパーティション
- C. 影響範囲の調査は CloudTrail Insights
- D. 影響範囲の調査は Detective
- E. ログの正規化は Security Lake

??? success "答えと解説"
    **正解: D, E**

    検出結果の調査は Detective、正規化は Security Lake です。

    - A: 誤り。結果の集約と優先付けで、つながりの調査ではない。
    - B: 誤り。配信と形式の変換はできても、複数のソースを共通の形式へ正規化する機能ではない。
    - C: 誤り。呼び出しの量の異常の検知で、つながりの調査ではない。
    - D: 正しい。
    - E: 正しい。

    **スキル:** [分析](../domain6.md#t6-3-analysis) / **参照:** [Detective](../../../services/threat-detection.md#detective)、[Security Lake](../../../services/threat-detection.md#security-lake)

### 問18 {#q18}

GuardDuty、Inspector、Config から毎週数百件の検出結果があり、3 人の担当者では全件を確認できません。本番の重要なものを先に扱います。担当者が優先順位を決める流れとして、適切なものはどれですか。

- A. 本番の検出結果だけを別の SNS トピックへ流し、開発用のアカウントのサービスは無効にする
- B. 件数が多いので全部を抑制ルールで止めて、毎月のレポートの集計の結果だけを見る運用にする
- C. 各サービスのコンソールで重要度の高いものを順に確認し、表計算で突き合わせる
- D. Security Hub で集約し、本番や重要度などで優先付けしてから、関連するログで調べる

??? success "答えと解説"
    **正解: D**

    複数の検出結果の優先付けは Security Hub です。

    - A: 誤り。開発用の監視を失い、複数のサービスの優先付けにならない。
    - B: 誤り。重要な検出結果を見逃す。
    - C: 誤り。手作業で、一か所の優先付けにならない。
    - D: 正しい。

    **スキル:** [分析](../domain6.md#t6-3-analysis) / **参照:** [Security Hub](../../../services/threat-detection.md#security-hub)、[どのログを見るか](../../../services/threat-detection.md#log-sources)

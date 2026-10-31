# 分野2: コンプライアンスとガバナンス

監査レポートの入手先、暗号化の選択肢、どのログで何が分かるかを問います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [コンプライアンスとガバナンスの考え方](../../domain2.md#t2-2-concepts) | 統制のサービスと考え方 |
| [暗号化の利点と選択肢](../../domain2.md#t2-2-encryption) | 保存時と転送時、鍵と証明書 |
| [セキュリティのログを取る場所](../../domain2.md#t2-2-logs) | 知りたいことからログを選ぶ |
| [コンプライアンス情報の入手先](../../domain2.md#t2-2-compliance-info) | AWS Artifact |
| [地域や業界で異なる要件](../../domain2.md#t2-2-regions-industries) | 国や業種で異なる基準 |
| [リソースを守るサービス](../../domain2.md#t2-2-securing) | 脅威、脆弱性、機密データ |
| [ガバナンスとコンプライアンスを助けるサービス](../../domain2.md#t2-2-governance-services) | 監視、監査、アクセスレポート |
| [サービスで異なる準拠の範囲](../../domain2.md#t2-2-service-variance) | サービスごとの確認 |

## 学習の順番 {#study-order}

1. [AWS Artifact](../../../../services/cloud-foundations.md#artifact): Artifact で手に入るものと、自社で用意するものを分けます。
2. [保存時と転送時の暗号化](../../../../services/kms.md#at-rest-in-transit)と[KMS との比較](../../../../services/identity-directory.md#cloudhsm-vs-kms): 暗号化と鍵のサービスを確認します。
3. [どのログを見るか](../../../../services/threat-detection.md#log-sources)と[証跡とイベント履歴](../../../../services/observability.md#cloudtrail-trails): ログの使い分けを覚えます。
4. [Config と CloudTrail の違い](../../../../services/governance.md#config-vs-cloudtrail)と[CloudWatch と CloudTrail の違い](../../../../services/observability.md#cloudtrail-vs-cloudwatch): 似たサービスの違いを確認します。
5. [GuardDuty](../../../../services/threat-detection.md#guardduty)、[Inspector](../../../../services/threat-detection.md#inspector)、[Macie](../../../../services/threat-detection.md#macie): 見るものの違いを覚えます。
6. [AWS Organizations](../../../../services/governance.md#organizations)、[AWS Control Tower](../../../../services/governance.md#control-tower)、[AWS Service Catalog](../../../../services/governance.md#service-catalog): 統制のサービスの役割を確認します。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| CloudTrail のイベント履歴 | 過去 90 日 | 長く残すなら証跡を作って S3 へ |
| 認証情報レポート | 4 時間に 1 回まで | 全ユーザーの状態の CSV |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| AWS の SOC レポートがほしい | AWS Artifact |
| 誰が API を呼んだか | CloudTrail |
| IP 通信の許可と拒否 | VPC フローログ |
| 設定がどう変わり、基準に合うか | AWS Config |
| 性能や動作を見る | CloudWatch |
| 不審な動きを見つける | GuardDuty |
| CVE を見つける | Inspector |
| S3 の個人情報を見つける | Macie |
| TLS 証明書の発行と更新 | ACM |
| 専用のハードウェアで鍵を守る | CloudHSM |
| データを国内に置く規制 | その国のリージョン |

## 引っかかりやすい点 {#traps}

- Artifact のレポートは AWS のインフラについてのものです。自社のシステムの準拠は自社で示します。
- ある基準の対象でも、すべてのサービスが含まれるわけではありません。公式のページで確認します。
- 新しい Security Hub はリスクの優先付けを行います。古い教材の Security Hub は、現在 Security Hub CSPM と呼ばれています。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [compliance 問1](../../exercises/compliance.md#q1) | コンプライアンスとガバナンスの考え方 | 複数のアカウントで使える操作を組織全体で制限したいと考えています。SCP を使うサービスはどれですか… |
| [compliance 問2](../../exercises/compliance.md#q2) | コンプライアンスとガバナンスの考え方 | マルチアカウントの基盤をベストプラクティスに沿った標準の形で用意したいと考えています。最も適切なサー… |
| [compliance 問3](../../exercises/compliance.md#q3) | コンプライアンスとガバナンスの考え方 | 社内の利用者に、承認済みの構成だけを選んで作らせたいと考えています。最も適切なサービスはどれですか。 |
| [compliance 問4](../../exercises/compliance.md#q4) | コンプライアンスとガバナンスの考え方 | コンプライアンスとガバナンスの説明として正しいものはどれですか。（2つ選択） |
| [compliance 問5](../../exercises/compliance.md#q5) | 暗号化の利点と選択肢 | 保存時の暗号化で防げるものはどれですか。 |
| [compliance 問6](../../exercises/compliance.md#q6) | 暗号化の利点と選択肢 | ブラウザーと ALB の間を流れるデータの盗聴を防ぎたいと考えています。使う仕組みとして最も適切なも… |
| [compliance 問7](../../exercises/compliance.md#q7) | 暗号化の利点と選択肢 | Web サイトの TLS 証明書を発行して、更新を任せたいと考えています。最も適切なサービスはどれで… |
| [compliance 問8](../../exercises/compliance.md#q8) | 暗号化の利点と選択肢 | 規制の要件で、専用のハードウェアで暗号鍵を保護する必要があります。最も適切なサービスはどれですか。 |
| [compliance 問9](../../exercises/compliance.md#q9) | セキュリティのログを取る場所 | 誰がいつどの API を呼んだかを調べたいと考えています。確認するものはどれですか。 |
| [compliance 問10](../../exercises/compliance.md#q10) | セキュリティのログを取る場所 | ある IP アドレスから EC2 への通信が許可されたか拒否されたかを調べたいと考えています。確認す… |
| [compliance 問11](../../exercises/compliance.md#q11) | セキュリティのログを取る場所 | CloudTrail のイベント履歴で管理イベントを確認できる期間と、長く残す方法の組み合わせはどれ… |
| [compliance 問12](../../exercises/compliance.md#q12) | セキュリティのログを取る場所 | 調べたい内容と、確認するログの組み合わせとして正しいものはどれですか。（2つ選択） |
| [compliance 問13](../../exercises/compliance.md#q13) | コンプライアンス情報の入手先 | 監査人が、AWS の SOC レポートの提出を求めています。入手先として最も適切なものはどれですか。 |
| [compliance 問14](../../exercises/compliance.md#q14) | コンプライアンス情報の入手先 | AWS Artifact で入手や確認ができるものはどれですか。（2つ選択） |
| [compliance 問15](../../exercises/compliance.md#q15) | コンプライアンス情報の入手先 | 自社のシステムが PCI DSS に準拠していることを取引先に示す必要があります。正しい考え方はどれ… |
| [compliance 問16](../../exercises/compliance.md#q16) | 地域や業界で異なる要件 | ある国の規制で、個人データを国内に保管する必要があります。AWS で最初に検討することはどれですか。 |
| [compliance 問17](../../exercises/compliance.md#q17) | 地域や業界で異なる要件 | クレジットカードのデータを扱う会社が、AWS で業界の基準に対応します。正しい進め方はどれですか。 |
| [compliance 問18](../../exercises/compliance.md#q18) | 地域や業界で異なる要件 | コンプライアンスの要件についての説明として正しいものはどれですか。 |
| [compliance 問19](../../exercises/compliance.md#q19) | リソースを守るサービス | 不審な API 呼び出しや、不審な通信を継続的に検出したいと考えています。最も適切なサービスはどれで… |
| [compliance 問20](../../exercises/compliance.md#q20) | リソースを守るサービス | EC2 インスタンスとコンテナイメージの既知の脆弱性（CVE）を見つけたいと考えています。最も適切な… |
| [compliance 問21](../../exercises/compliance.md#q21) | リソースを守るサービス | 複数のセキュリティサービスの検出結果を 1 か所にまとめて、リスクの優先付けをしたいと考えています。… |
| [compliance 問22](../../exercises/compliance.md#q22) | リソースを守るサービス | 目的とサービスの組み合わせとして正しいものはどれですか。（2つ選択） |
| [compliance 問23](../../exercises/compliance.md#q23) | ガバナンスとコンプライアンスを助けるサービス | セキュリティグループの設定がどう変わり、社内の基準に合っているかを評価したいと考えています。最も適切… |
| [compliance 問24](../../exercises/compliance.md#q24) | ガバナンスとコンプライアンスを助けるサービス | 目的とサービスの組み合わせとして正しいものはどれですか。 |
| [compliance 問25](../../exercises/compliance.md#q25) | ガバナンスとコンプライアンスを助けるサービス | 全 IAM ユーザーのパスワード、アクセスキー、MFA の状態を CSV で一覧にしたいと考えていま… |
| [compliance 問26](../../exercises/compliance.md#q26) | ガバナンスとコンプライアンスを助けるサービス | 許可したのに使われていないサービスの権限を見つけて削りたいと考えています。役立つ IAM の機能はど… |
| [compliance 問27](../../exercises/compliance.md#q27) | サービスで異なる準拠の範囲 | ある基準について、使う予定の AWS のサービスが対象に含まれるかを確認したいと考えています。正しい… |
| [compliance 問28](../../exercises/compliance.md#q28) | サービスで異なる準拠の範囲 | 「AWS はある基準の認証を取得している」と聞いた担当者の理解として正しいものはどれですか。 |
| [compliance 問29](../../exercises/compliance.md#q29) | サービスで異なる準拠の範囲 | 医療データを扱う新しいアプリの設計で、候補の 3 つのサービスのうち 1 つが必要な基準の対象か不明… |

<!-- questions:end -->

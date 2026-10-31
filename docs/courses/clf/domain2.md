# 分野2: セキュリティとコンプライアンス

配点は **30%** です。責任共有モデル、コンプライアンスの情報、IAM、セキュリティサービスの役割を扱います。

ポリシーを書く力は問われません。誰の責任か、どのサービスが何を見つけるかを区別できるようにします。

## タスク 2.1: 責任共有モデルを理解する {#task-2-1}

### モデルの全体像 {#t2-1-model}

セキュリティとコンプライアンスは、AWS と利用者で分担します。

- AWS は「クラウドのセキュリティ」を担当します。
- 利用者は「クラウドの中のセキュリティ」を担当します。

問題では、具体的な作業を挙げて担当を問います。

詳細: [責任共有モデル](../../services/cloud-foundations.md#shared-responsibility)

### 利用者の責任 {#t2-1-customer}

データ、IAM の権限、暗号化の設定、ネットワークのアクセス制御、アプリケーションです。

たとえば、S3 バケットを公開設定にして情報が漏れた場合、責任は利用者にあります。AWS が設定を代わりに判断することはありません。

詳細: [責任共有モデル](../../services/cloud-foundations.md#shared-responsibility)

### AWS の責任 {#t2-1-aws}

物理施設、ハードウェア、ネットワーク、仮想化層、マネージドサービスの基盤です。

データセンターの入退室の管理や、ディスクの廃棄は AWS の担当です。

詳細: [責任共有モデル](../../services/cloud-foundations.md#shared-responsibility)

### 共有する責任 {#t2-1-shared}

同じ項目を、それぞれが自分の層で担当します。

| 項目 | AWS | 利用者 |
|---|---|---|
| パッチ管理 | インフラ | ゲスト OS、アプリ |
| 構成管理 | インフラの機器 | OS、データベース、アプリの設定 |
| 教育 | AWS の従業員 | 自社の従業員 |

詳細: [責任共有モデル](../../services/cloud-foundations.md#shared-responsibility)

### サービスによる責任の変化 {#t2-1-by-service}

抽象度が高いサービスほど、利用者の担当は減ります。

| 項目 | EC2 | RDS | Lambda |
|---|---|---|---|
| 物理とホスト | AWS | AWS | AWS |
| ゲスト OS のパッチ | 利用者 | AWS | AWS |
| DB エンジン、ランタイムの管理 | 利用者 | AWS | AWS |
| データと権限 | 利用者 | 利用者 | 利用者 |
| アプリのコード | 利用者 | 利用者（SQL、スキーマ） | 利用者 |

データと権限は、どのサービスでも利用者の担当です。

詳細: [サービスごとの違い](../../services/cloud-foundations.md#responsibility-by-service)

## タスク 2.2: セキュリティ、ガバナンス、コンプライアンスの概念を理解する {#task-2-2}

### コンプライアンスとガバナンスの考え方 {#t2-2-concepts}

コンプライアンスは、法律や業界の基準を満たしていることです。ガバナンスは、組織のルールどおりに使われるようにする仕組みです。

AWS は自社のインフラについて監査を受け、レポートを提供します。利用者のシステムが基準を満たすことは、利用者が示します。

複数のアカウントを統制するサービスは次のとおりです。

| サービス | 役割 |
|---|---|
| AWS Organizations | アカウントをまとめ、SCP で使える操作を制限する |
| AWS Control Tower | マルチアカウントの基盤を標準の形で用意する |
| AWS Service Catalog | 承認済みの構成を利用者に提供する |
| AWS Resource Access Manager | リソースをアカウント間で共有する |

詳細: [Organizations](../../services/governance.md#organizations)、[Control Tower](../../services/governance.md#control-tower)、[Service Catalog](../../services/governance.md#service-catalog)、[RAM](../../services/governance.md#ram)

### 暗号化の利点と選択肢 {#t2-2-encryption}

暗号化すると、媒体の盗難や通信の盗聴があっても中身を読まれません。これがクラウドのセキュリティの利点の代表です。

| 観点 | 保存時の暗号化 | 転送時の暗号化 |
|---|---|---|
| 守る対象 | ディスクやストレージ上のデータ | ネットワークを流れるデータ |
| 主な仕組み | KMS、S3、EBS、RDS の暗号化 | TLS（HTTPS） |
| 防ぐもの | 媒体やバックアップからの漏えい | 盗聴、改ざん |

鍵と証明書のサービスは次のように分けます。

| 要件 | サービス |
|---|---|
| 暗号鍵を管理する | AWS KMS |
| 専用のハードウェアで鍵を保護する | AWS CloudHSM |
| TLS 証明書を発行して更新する | AWS Certificate Manager（ACM） |

詳細: [保存時と転送時の暗号化](../../services/kms.md#at-rest-in-transit)、[CloudHSM と KMS の比較](../../services/identity-directory.md#cloudhsm-vs-kms)、[ACM](../../services/certificates.md#acm)

### セキュリティのログを取る場所 {#t2-2-logs}

| 知りたいこと | ログ |
|---|---|
| 誰がどの API を呼んだか | CloudTrail |
| IP 通信の有無と許可、拒否 | VPC フローログ |
| HTTP リクエストの中身 | ALB、CloudFront、WAF のログ |
| 設定がいつ変わったか | AWS Config |
| アプリケーションのログ | CloudWatch Logs |

CloudTrail のイベント履歴では、管理イベントを 90 日間確認できます。長く残すなら、証跡を作って S3 に保存します。

詳細: [どのログを見るか](../../services/threat-detection.md#log-sources)、[CloudTrail の証跡](../../services/observability.md#cloudtrail-trails)、[CloudWatch Logs](../../services/observability.md#cloudwatch-logs)

### コンプライアンス情報の入手先 {#t2-2-compliance-info}

AWS の監査レポートや認証は、AWS Artifact からダウンロードします。ISO、PCI、SOC などのレポートと、AWS との契約を扱います。

「監査人に SOC レポートを渡したい」なら Artifact です。自社のシステムの準拠を示す文書は、利用者が別に用意します。

詳細: [AWS Artifact](../../services/cloud-foundations.md#artifact)

### 地域や業界で異なる要件 {#t2-2-regions-industries}

必要な基準は、国や業種で異なります。データを国内に置く規制があるなら、該当する国のリージョンを選びます。

業界の基準の例は、クレジットカードの PCI です。自社に必要な基準を確認して、AWS の該当する準拠資料を Artifact で確認します。

詳細: [AWS Artifact](../../services/cloud-foundations.md#artifact)、[リージョン](../../services/cloud-foundations.md#regions)

### サービスで異なる準拠の範囲 {#t2-2-service-variance}

ある基準の対象でも、すべてのサービスが含まれるわけではありません。公式の「コンプライアンスプログラム対象のサービス」のページで、使うサービスが対象かを確認します。

詳細: [AWS Artifact](../../services/cloud-foundations.md#artifact)

### リソースを守るサービス {#t2-2-securing}

名前が似ているので、見るものと役割で区別します。

| サービス | 役割 | 問題文での表れ方 |
|---|---|---|
| Amazon GuardDuty | 脅威の検出 | 不審な API 呼び出しや通信を見つけたい |
| Amazon Inspector | 脆弱性の検出 | EC2 やコンテナの CVE を見つけたい |
| AWS Security Hub | 検出結果の集約とリスクの優先付け | 1 か所でまとめて見たい |
| Amazon Macie | 機密データの検出 | S3 の個人情報を見つけたい |
| Amazon Detective | 根本原因の調査 | 検出結果の原因を調べたい |
| AWS Shield | DDoS 攻撃の防御 | DDoS から守りたい |

!!! note "Security Hub の名称（2026年10月時点）"
    2025年12月に、リスクの優先付けを行う新しい AWS Security Hub が一般提供になりました。古い教材の Security Hub にあたる設定チェックの製品は、現在 AWS Security Hub CSPM と呼ばれています。

詳細: [GuardDuty](../../services/threat-detection.md#guardduty)、[Inspector](../../services/threat-detection.md#inspector)、[Security Hub](../../services/threat-detection.md#security-hub-products)、[Macie](../../services/threat-detection.md#macie)、[Detective](../../services/threat-detection.md#detective)、[Shield](../../services/threat-detection.md#shield)

### ガバナンスとコンプライアンスを助けるサービス {#t2-2-governance-services}

| 目的 | サービス | 答える問い |
|---|---|---|
| 監視 | Amazon CloudWatch | 性能や動作はどうか |
| 監査 | AWS CloudTrail | 誰がいつどの API を呼んだか |
| 監査 | AWS Config | 設定はどう変わり、基準に合っているか |
| レポート | アクセスレポート | 誰の認証情報がどの状態で、権限が使われているか |

ガイドのアクセスレポートにあたるのは、次の IAM の機能です。

| レポート | 内容 |
|---|---|
| 認証情報レポート | 全ユーザーのパスワード、アクセスキー、MFA の状態を CSV で一覧にする。4 時間に 1 回まで生成できる |
| 最終アクセス情報 | 許可されたサービスにいつアクセスしたかを示す。未使用の権限を見つけて削るのに使う |
| Organizations のアクセスレポート | 管理アカウントから、OU やアカウントごとのサービスの最終アクセスを確認する |

詳細: [Config と CloudTrail の違い](../../services/governance.md#config-vs-cloudtrail)、[CloudWatch と CloudTrail の違い](../../services/observability.md#cloudtrail-vs-cloudwatch)

アクセスレポートの参考: [認証情報レポート](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_getting-report.html)、[最終アクセス情報](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_last-accessed.html)

## タスク 2.3: アクセス管理の機能を理解する {#task-2-3}

### IAM の要素 {#t2-3-iam}

| 要素 | 内容 |
|---|---|
| ユーザー | 長期の認証情報を持つ主体。例外的な利用にとどめる |
| グループ | ユーザーの集まり。まとめて権限を与える |
| ロール | 一時的な認証情報を受け取る。アプリ、AWS サービス、外部の利用者が使う |
| ポリシー | 権限を JSON で定義する |

「EC2 上のアプリから S3 を読みたい」ならロールです。アクセスキーをサーバーに置くのは誤りです。

詳細: [プリンシパルと権限の定義](../../services/iam.md#principals)

### 最小権限とポリシーの種類 {#t2-3-least-privilege}

最小権限は、作業に必要な権限だけを与える原則です。権限は人ごとに付けず、グループで付けます。

| ポリシー | 作成者 | 特徴 |
|---|---|---|
| AWS 管理ポリシー | AWS | すぐ使えるが、広めの権限になりやすい |
| カスタマー管理ポリシー | 利用者 | 必要な権限に絞れる。複数に付けられる |
| インラインポリシー | 利用者 | 1 つのユーザーやロールに直接埋め込む |

最小権限を守るには、カスタム（カスタマー管理）ポリシーで操作と対象を具体的に書きます。

詳細: [最小権限](../../services/iam.md#least-privilege)、[管理ポリシーとインラインポリシー](../../services/iam.md#managed-vs-inline)

### ルートユーザーの保護 {#t2-3-root}

ルートユーザーは、アカウントの作成時にできる、すべての権限を持つ ID です。IAM のポリシーで権限を減らすことは基本的にできないので、使わないことが最大の防御です。

| 方法 | 内容 |
|---|---|
| 日常の作業に使わない | 管理者を別に用意する。IAM Identity Center の管理ユーザーが推奨 |
| MFA を設定する | すべての種類のアカウントで必須。初回サインインの試行から 14 日以内に登録する。最大 8 台まで登録できる |
| アクセスキーを作らない | 作ってしまったら削除する |
| 強いパスワードを使う | 共有しない |
| 共有のメールアドレスを使う | 個人の退職や不在で連絡が止まらないように、グループのアドレスにする |
| 使用を監視する | CloudTrail と EventBridge などで通知する |
| 組織で一元管理する | Organizations のメンバーアカウントからルートの認証情報を削除できる |

詳細: [アクセス方法](../../services/cloud-foundations.md#access-methods)

参考: [ルートユーザーのベストプラクティス](https://docs.aws.amazon.com/IAM/latest/UserGuide/root-user-best-practices.html)

### ルートユーザーだけができる作業 {#t2-3-root-tasks}

| 分類 | 作業 |
|---|---|
| アカウント | 組織に属さないアカウントのメールアドレス、ルートのパスワード、ルートのアクセスキーの変更 |
| アカウント | 組織に属さないアカウントの閉鎖と再開 |
| アカウント | 唯一の管理者が自分の権限を消してしまったときの復旧 |
| 請求 | IAM ユーザーやロールに請求コンソールへのアクセスを有効にする。一部の税の請求書の表示 |
| EC2 | リザーブドインスタンスマーケットプレイスの販売者登録 |
| S3 | MFA Delete の設定、すべての主体を拒否するバケットポリシーの修正 |
| SQS | すべての主体を拒否するキューのポリシーの修正 |
| GovCloud | AWS GovCloud (US) へのサインアップ |

アカウント名や連絡先、利用するリージョンの変更には、ルートは不要です。古い教材の一覧とは異なる部分があるので、公式の一覧で確認してください。

参考: [ルートユーザーの認証情報が必要なタスク](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_root-user.html#root-user-tasks)

### IAM Identity Center {#t2-3-identity-center}

従業員の ID を 1 か所にまとめ、複数の AWS アカウントとアプリへのシングルサインオンを提供します。

「多数のアカウントに、社員を 1 つの ID でサインインさせたい」なら IAM Identity Center です。一般の利用者のサインインなら、Amazon Cognito です。

詳細: [IAM Identity Center](../../services/identity-directory.md#identity-center)、[Cognito](../../services/cognito.md#user-vs-identity-pools)

### アクセスキー、パスワードポリシー、認証情報の保管 {#t2-3-credentials}

**アクセスキー**は、CLI や SDK で使う長期の認証情報です。1 ユーザーにつき 2 つまで持てます。漏えいに備えて定期的に更新し、可能ならロールの一時認証情報を使います。

**パスワードポリシー**は、IAM ユーザーのパスワードの条件をアカウントで決める設定です。

| 項目 | 内容 |
|---|---|
| 既定 | 8〜128 文字、3 種類以上の文字、期限なし |
| カスタムの長さ | 最小 6〜128 文字 |
| 有効期限 | 1〜1,095 日 |
| 再利用の禁止 | 過去 1〜24 個 |
| 対象外 | ルートユーザーのパスワード、アクセスキー |

**認証情報の保管**は、コードに書かず、専用のサービスに置きます。

| サービス | 向くもの |
|---|---|
| AWS Secrets Manager | データベースの資格情報、API キー。自動ローテーションができる |
| Systems Manager Parameter Store | 設定値や低リスクの秘密情報。スタンダードは無料 |

詳細: [アクセスキーの扱い](../../services/iam.md#access-key-handling)、[3 つのサービスの比較](../../services/secrets.md#comparison)

参考: [アカウントのパスワードポリシー](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_passwords_account-policy.html)

### 認証の方法 {#t2-3-authentication}

| 方法 | 内容 | 向く場面 |
|---|---|---|
| MFA | パスワードに加えて別の要素で確認する | ルートユーザーや管理者の保護 |
| IAM Identity Center | 1 つの ID で複数のアカウントへ | 社員の複数アカウント利用 |
| クロスアカウント IAM ロール | 別のアカウントのロールを引き受ける | 他のアカウントのリソースを一時的に操作する |

クロスアカウントでは、相手のアカウントにユーザーを作りません。ロールと信頼ポリシーを使います。

詳細: [MFA](../../services/iam.md#mfa)、[IAM Identity Center](../../services/iam.md#identity-center)、[クロスアカウントアクセス](../../services/iam.md#cross-account)

### ID 管理の種類 {#t2-3-federation}

| 種類 | 内容 | 例 |
|---|---|---|
| IAM の ID | AWS の中で作るユーザー | 少数の例外的な利用 |
| フェデレーション | 外部の ID 基盤で認証して、一時認証情報を受け取る | 社内ディレクトリの ID で AWS にサインイン |
| アプリの利用者の ID | アプリの利用者を管理する | Amazon Cognito |
| ディレクトリ | Active Directory を AWS で動かす、接続する | AWS Directory Service |

フェデレーションでは、IAM ユーザーを作る必要がありません。

詳細: [フェデレーション](../../services/iam.md#federation)、[Directory Service](../../services/identity-directory.md#directory-service)

## タスク 2.4: セキュリティの機能と情報源を理解する {#task-2-4}

### AWS のセキュリティ機能とサービス {#t2-4-capabilities}

| サービス | 役割 | 問題文での表れ方 |
|---|---|---|
| AWS WAF | Web アプリ（L7）の防御 | SQL インジェクションや特定の IP を止めたい |
| AWS Shield | DDoS の防御 | Standard は全利用者に追加料金なしで適用される。Advanced は有料の追加の保護 |
| AWS Firewall Manager | 保護の設定を組織全体に展開する | 全アカウントに同じ WAF ルールを強制したい |
| Amazon GuardDuty | 脅威の検出 | 不審な動きを見つけたい |

Firewall Manager は展開と統制のサービスです。検査そのものは WAF などが行います。

詳細: [WAF](../../services/certificates.md#waf)、[Shield](../../services/threat-detection.md#shield)、[Firewall Manager](../../services/threat-detection.md#firewall-manager)、[GuardDuty](../../services/threat-detection.md#guardduty)

### Marketplace のセキュリティ製品 {#t2-4-marketplace}

サードパーティのセキュリティ製品は、AWS Marketplace で探して購入できます。料金は AWS の請求書にまとまります。

AWS のサービスにない機能が必要なときや、社内で使っている他社製品を AWS でも使いたいときに選びます。

詳細: [AWS Marketplace](../../services/cloud-foundations.md#marketplace)

### セキュリティの情報源 {#t2-4-docs}

| 情報源 | 使いどころ |
|---|---|
| AWS Security Center | セキュリティの総合的な情報 |
| AWS Security Blog | 新機能や手法の解説 |
| AWS Knowledge Center | よくある質問と解決方法 |
| AWS Artifact | 監査レポートと契約 |

詳細: [サポートの情報源](../../services/cloud-foundations.md#support-resources)

### 問題を見つけるサービス {#t2-4-trusted-advisor}

AWS Trusted Advisor は環境を点検し、ルートの MFA の未設定、公開スナップショット、S3 バケットの権限、開放されたポートなどを指摘します。

助言するサービスで、自動では修正しません。使えるチェックはサポートプランで変わります。

| 迷うもの | 使い分け |
|---|---|
| Trusted Advisor / GuardDuty | 設定の弱点なら Trusted Advisor、実際の不審な動きなら GuardDuty |
| Trusted Advisor / Inspector | 環境全体の設定の点検なら Trusted Advisor、ソフトウェアの脆弱性なら Inspector |

詳細: [Trusted Advisor](../../services/cloud-foundations.md#trusted-advisor)

## 確認問題 {#self-check}

??? question "問1: EC2 上のデータベースと RDS を比べています。RDS にすると、OS のパッチの担当はどう変わりますか？"
    EC2 では利用者の担当ですが、RDS では AWS の担当になります。一方、データとアクセス権限は、どちらでも利用者の担当です。

??? question "問2: 監査人が、AWS のデータセンターに関する SOC レポートを求めています。どこで入手しますか？"
    AWS Artifact です。AWS の監査レポートをオンデマンドでダウンロードできます。AWS Config は自分のリソースの設定を監査するもので、AWS 自身のレポートは得られません。

??? question "問3: セキュリティグループが誰によって変更されたかを調べたいです。どのサービスを使いますか？"
    AWS CloudTrail です。誰がいつどの API を呼んだかを記録します。設定がどう変わったかを時系列で見るなら Config、性能を見るなら CloudWatch です。

??? question "問4: 新しい AWS アカウントを作りました。ルートユーザーについて最初にすべきことは何ですか？"
    MFA を設定し、アクセスキーを作らず、日常の作業用に別の管理者を用意します。ルートユーザーは、それが必要な作業のときだけ使います。

??? question "問5: S3 に保存したファイルに個人情報が含まれていないか、自動で調べたいです。どのサービスを使いますか？"
    Amazon Macie です。S3 の機密データを検出します。GuardDuty は脅威の検出、Inspector はソフトウェアの脆弱性の検出で、データの中身は調べません。

??? question "問6: 50 個のアカウントがある組織で、すべての ALB に同じ WAF ルールを適用し、新しいアカウントにも自動で広げたいです。どのサービスを使いますか？"
    AWS Firewall Manager です。保護の設定を組織全体に展開します。WAF はルールを実行する側で、WAF だけではアカウントごとの設定が必要です。

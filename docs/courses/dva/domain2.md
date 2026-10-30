# 分野2: セキュリティ

C03 の配点は **26%** です。認証と認可、暗号化と機密データ、AI サービスのリスク対策の3つを扱います。AI のタスクは C03 で新しく追加されました。

## タスク 2.1: 認証と認可を実装する {#task-2-1}

[![Cognito のユーザープールと ID プール](../../assets/diagrams/cognito-pools.png)](../../assets/diagrams/cognito-pools.png)

### 2.1.1 ID フェデレーション {#skill-2-1-1}

外部の ID を使って AWS にアクセスさせます。アプリのログインには Cognito ユーザープール、AWS の一時的な認証情報の発行には ID プールを使います。

詳細: [IAM のフェデレーション](../../services/iam.md#federation)、[Cognito のフェデレーション](../../services/cognito.md#federation)、[ID プール](../../services/cognito.md#identity-pools)

### 2.1.2 アクセス制御 {#skill-2-1-2}

きめ細かい権限、セキュリティトークン、MFA を組み合わせます。API の呼び出し側は、Cognito が発行した JWT をベアラートークンとして送ります。

詳細: [条件](../../services/iam.md#conditions)、[MFA](../../services/iam.md#mfa)、[トークン](../../services/cognito.md#tokens)、[アプリの認可](../../services/cognito.md#app-authorization)

### 2.1.3 AWS へのプログラムによるアクセス {#skill-2-1-3}

アクセスキーを埋め込まず、インスタンスプロファイルや実行ロールを使います。SDK が認証情報を探す順番（プロバイダーチェーン）も押さえます。

詳細: [プログラムによるアクセス](../../services/iam.md#programmatic-access)

### 2.1.4 署名付き URL {#skill-2-1-4}

S3 の署名付き URL は、認証情報のない相手に期限付きでオブジェクトへのアクセスを許可します。CloudFront を経由して配信するなら、CloudFront の署名付き URL か署名付き Cookie を使います。複数のファイルをまとめて許可するときは Cookie が向いています。

詳細: [S3 の署名付き URL](../../services/s3.md#presigned-urls)、[CloudFront の署名付き URL と Cookie](../../services/networking.md#signed-urls-cookies)

### 2.1.5 認証された API 呼び出し {#skill-2-1-5}

AWS API は SigV4 で署名します。SDK や CLI を使えば自動で署名されます。

詳細: [SigV4](../../services/iam.md#sigv4)

### 2.1.6 IAM プリンシパルの権限 {#skill-2-1-6}

明示的な拒否が常に優先され、どこにも許可がなければ暗黙的に拒否されます。アイデンティティベースのポリシーとリソースベースのポリシーの違いも問われます。

詳細: [プリンシパル](../../services/iam.md#principals)、[2種類のポリシー](../../services/iam.md#identity-vs-resource)、[ポリシーの評価](../../services/iam.md#policy-evaluation)

### 2.1.7 IAM ロールの引き受け {#skill-2-1-7}

STS の AssumeRole で一時的な認証情報を取得します。呼び出し側の権限と、ロール側の信頼ポリシーの両方が必要です。

詳細: [AssumeRole](../../services/iam.md#assume-role)、[クロスアカウント](../../services/iam.md#cross-account)

## タスク 2.2: 暗号化と機密データの管理 {#task-2-2}

### 2.2.1 保存時と転送時の暗号化 {#skill-2-2-1}

保存時は KMS と各サービスの暗号化設定、転送時は TLS を使います。S3 では、バケットポリシーで HTTPS を強制できます。

詳細: [保存時と転送時](../../services/kms.md#at-rest-in-transit)、[S3 の暗号化](../../services/s3.md#encryption)、[暗号化の強制](../../services/s3.md#enforcing-encryption)、[TLS](../../services/certificates.md#tls-in-transit)

### 2.2.2 証明書の管理 {#skill-2-2-2}

公開証明書は ACM、組織内の証明書は AWS Private CA で管理します。CloudFront で使う ACM 証明書は、米国東部（バージニア北部）リージョンで発行します。

詳細: [ACM](../../services/certificates.md#acm)、[Private CA](../../services/certificates.md#private-ca)

### 2.2.3 クライアント側とサーバー側の暗号化 {#skill-2-2-3}

AWS にも平文を渡したくないならクライアント側で暗号化します。運用の手間を抑えるならサーバー側の暗号化を使います。

詳細: [比較](../../services/kms.md#client-vs-server-side)、[S3 のクライアント側暗号化](../../services/s3.md#client-side-encryption)

### 2.2.4 暗号化キーの利用 {#skill-2-2-4}

KMS の Encrypt で直接扱えるのは小さなデータだけです。大きなデータは GenerateDataKey で作ったデータキーで暗号化します（エンベロープ暗号化）。

詳細: [キーの使い方](../../services/kms.md#use-keys)、[エンベロープ暗号化](../../services/kms.md#envelope-encryption)

### 2.2.5 開発用の証明書と SSH キー {#skill-2-2-5}

`openssl` で自己署名証明書を、`ssh-keygen` で SSH キーを作ります。

詳細: [開発用の証明書と SSH キー](../../services/certificates.md#dev-certs-ssh)

### 2.2.6 機密データの特定、マスキング、アクセス制限 {#skill-2-2-6}

PII や PHI を分類し、ログに出す前にマスクします。CloudWatch Logs のデータ保護も使えます。

詳細: [データの分類](../../services/secrets.md#data-classification)、[サニタイズとマスキング](../../services/secrets.md#sanitization-masking)、[CloudWatch Logs のデータ保護](../../services/secrets.md#cloudwatch-data-protection)

### 2.2.7 シークレット管理サービス {#skill-2-2-7}

| 要件 | 選択肢 |
|---|---|
| 自動ローテーションが必要なシークレット | Secrets Manager |
| 設定値や、ローテーション不要の値 | Parameter Store |

詳細: [Secrets Manager](../../services/secrets.md#secrets-manager)、[Parameter Store](../../services/secrets.md#parameter-store)、[比較](../../services/secrets.md#comparison)

## タスク 2.3: AI サービスのリスク対策（C03 で追加） {#task-2-3}

[![Bedrock への閉域アクセス](../../assets/diagrams/ai-bedrock-private-access.png)](../../assets/diagrams/ai-bedrock-private-access.png)

### 2.3.1 AI サービスへのアクセス管理 {#skill-2-3-1}

Bedrock のモデルアクセスの仕組みと、IAM でモデル単位に権限を絞る方法を押さえます。

詳細: [アクセス管理](../../services/ai.md#access)、[モデルアクセス](../../services/ai.md#model-access)、[IAM による制限](../../services/ai.md#iam-scope)

### 2.3.2 データプライバシーの制御 {#skill-2-3-2}

VPC エンドポイント（PrivateLink）でインターネットを経由せずに接続します。入力と出力がモデルの学習に使われるかどうかも確認します。

詳細: [データプライバシー](../../services/ai.md#data-privacy)、[PrivateLink](../../services/ai.md#privatelink)、[学習への利用](../../services/ai.md#training-use)

### 2.3.3 モデルの入出力の制御 {#skill-2-3-3}

Bedrock Guardrails で、コンテンツフィルター、拒否トピック、機密情報のマスキング、プロンプト攻撃の防御を適用します。

詳細: [Guardrails](../../services/ai.md#guardrails)、[フィルター](../../services/ai.md#guardrail-filters)、[処理の流れ](../../services/ai.md#guardrail-flow)、[ApplyGuardrail](../../services/ai.md#apply-guardrail)

### 2.3.4 AI エージェントの保護 {#skill-2-3-4}

ツール呼び出しの認可、セッションの分離、重要な操作への人による承認を組み合わせます。

詳細: [エージェントの保護](../../services/ai.md#agent-security)、[ツールの認可](../../services/ai.md#tool-authorization)、[セッションの分離](../../services/ai.md#session-isolation)、[人による承認](../../services/ai.md#human-in-the-loop)

### 2.3.5 ログ内の機密情報の保護 {#skill-2-3-5}

モデル呼び出しログには、入力や出力がそのまま残ることがあります。出力先のアクセス制限と、CloudWatch Logs のデータ保護を組み合わせます。

詳細: [呼び出しログ](../../services/ai.md#invocation-logging)、[データ保護](../../services/ai.md#cloudwatch-data-protection)

## 確認問題 {#self-check}

??? question "問1: スマホアプリの利用者をログインさせ、その利用者に S3 への一時的なアクセスを許可します。何を組み合わせますか？"
    Cognito ユーザープールでログインさせ、ID プールで AWS の一時的な認証情報に交換します。

??? question "問2: 別アカウントのロールを AssumeRole できません。両方のアカウントで何を確認しますか？"
    呼び出し側に `sts:AssumeRole` の許可があること、ロール側の信頼ポリシーが呼び出し側を許可していることを確認します。

??? question "問3: KMS で大きなファイルを暗号化するにはどうしますか？"
    GenerateDataKey でデータキーを取得し、平文のデータキーでファイルを暗号化します。暗号化されたデータキーをファイルと一緒に保存し、平文のデータキーはメモリから消します。

??? question "問4: データベースのパスワードを自動でローテーションしたいです。何を使いますか？"
    Secrets Manager です。

??? question "問5: CloudFront に独自ドメインの ACM 証明書を設定します。どのリージョンで発行しますか？"
    米国東部（バージニア北部、us-east-1）です。

??? question "問6: Bedrock の呼び出しをインターネット経由にせず、モデルの応答に含まれる個人情報もマスクしたいです。何を使いますか？"
    Bedrock のインターフェイス型 VPC エンドポイントと、機密情報フィルターを設定した Guardrails です。呼び出しログに生の入力が残る可能性があるので、ログも別に保護します。

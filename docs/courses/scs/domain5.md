# 分野5: データ保護

配点は **18%** です。転送時と保存時の暗号化、データの完全性と保持、シークレットと鍵素材の管理を問います。

暗号そのものの設計は範囲外です。鍵をどのサービスで、誰の責任で持つかという選択が中心で、費用と運用の負担のトレードオフがよく問われます。

## タスク 5.1: 転送時のデータの統制 {#task-5-1}

### 5.1.1 暗号化の強制 {#skill-5-1-1}

「暗号化できる」と「暗号化しないと接続できない」は別です。強制する設定を押さえます。

| 対象 | 強制の方法 |
|---|---|
| S3 | バケットポリシーで `aws:SecureTransport` が `false` を拒否 |
| 組織全体 | RCP で HTTPS 以外を拒否 |
| ALB、NLB | HTTPS や TLS のリスナーとセキュリティポリシー。ALB は HTTP を HTTPS へリダイレクト |
| CloudFront | ビューワープロトコルポリシー、オリジンプロトコルポリシー |
| RDS | `rds.force_ssl=1`（PostgreSQL）、`require_secure_transport=ON`（MySQL） |
| ElastiCache | `TransitEncryptionEnabled`。AUTH トークンの前提 |
| EFS | マウントオプション `tls` |
| API Gateway | カスタムドメインのセキュリティポリシー、相互 TLS |

**ELB のセキュリティポリシー:** プロトコルと暗号の組み合わせです。作り方で既定が違うことに注意します。

| 作成方法 | 既定のポリシー |
|---|---|
| コンソール | `ELBSecurityPolicy-TLS13-1-2-Res-PQ-2025-09` |
| CLI、CloudFormation、CDK など | `ELBSecurityPolicy-2016-08`（TLS 1.0 と 1.1 も許可し、1.3 には非対応） |

IaC で作った ALB が古い TLS を受け入れているなら、これが原因です。ポリシーを明示します。AWS の推奨は `ELBSecurityPolicy-TLS13-1-2-Res-PQ-2025-09`、FIPS が要件なら `ELBSecurityPolicy-TLS13-1-2-Res-FIPS-PQ-2025-09` です。接続ログで実際の TLS のバージョンを確認できます。

**TLS の終端:** ALB で終端すると、その先は別の区間です。エンドツーエンドの要件なら、ターゲットグループも HTTPS にします。ALB から先の証明書は自己署名でも可能です。

詳細: [転送時の TLS](../../services/certificates.md#tls-in-transit)、[相互 TLS](../../services/certificates.md#mtls)、[CloudFront の HTTPS](../../services/networking.md#cloudfront-https)、[RDS の SSL/TLS](../../services/databases.md#rds-ssl)、[EFS の暗号化](../../services/storage.md#efs-encryption)、[保存時と転送時](../../services/kms.md#at-rest-in-transit)

### 5.1.2 安全でプライベートなアクセス {#skill-5-1-2}

| 要件 | 手段 | 注意点 |
|---|---|---|
| VPC から S3、DynamoDB へ | ゲートウェイエンドポイント | VPC の外（VPN、DX の先）からは使えない |
| VPC から多くの AWS サービスへ | インターフェイスエンドポイント（PrivateLink） | SG で 443 を許可。プライベート DNS の属性を確認 |
| オンプレミスから S3 へプライベートに | S3 のインターフェイスエンドポイント | ゲートウェイでは届かない |
| 別の VPC のサービスを公開 | PrivateLink のエンドポイントサービス | VPC 全体をつながずに済む |
| 端末から VPC へ | Client VPN | ネットワーク単位 |
| 端末から社内アプリへ | Verified Access | アプリ単位でリクエストごとに判定 |

**経路を強制する:** バケットポリシーで `aws:SourceVpce` や `aws:SourceVpc` を条件にして、エンドポイント以外からのアクセスを拒否します。エンドポイントポリシーで「このエンドポイントから届くバケット」も絞ります。両方を組み合わせると、持ち出しの経路が減ります。

詳細: [VPC エンドポイント](../../services/networking.md#vpc-endpoints)、[エンドポイントの選び方](../../services/networking.md#endpoint-settings)、[エンドポイントポリシー](../../services/networking.md#endpoint-policies)、[Client VPN](../../services/network-connectivity.md#client-vpn)、[Verified Access](../../services/identity-directory.md#verified-access)

### 5.1.3 リソース間の転送時暗号化 {#skill-5-1-3}

C03 で追加されたスキルです。クラスターの内部の通信は、設定しないと暗号化されないことがあります。

| 対象 | 既定の状態 | 有効にする方法 |
|---|---|---|
| Nitro のインスタンス間 | 対応するインスタンスタイプなら自動で暗号化 | 条件を満たす構成にする |
| EMR | 明示が必要 | セキュリティ設定で転送時の暗号化を有効にし、証明書を指定 |
| SageMaker AI の分散学習、処理ジョブ | ノード間は暗号化されない部分がある | コンテナ間の通信の暗号化を有効にする |
| EKS | ノード間は上の Nitro の条件に従う | 必要に応じアプリの TLS。ストレージは EFS の `tls` など |

**Nitro の暗号化の条件:** 256 ビットの AEAD で自動的に暗号化され、性能への影響はありません。

- 対応するインスタンスタイプであること（`encryption-in-transit-supported` で確認できます）
- 同じリージョンであること
- 同じ VPC かピアリングした VPC で、ロードバランサーや Transit Gateway などを**通らない**こと

「NLB を挟むと、この暗号化の対象外」というのが落とし穴です。また、これとは別に、AZ 間やリージョン間の通信は AWS のネットワークで物理層で暗号化されます。

**EMR のセキュリティ設定:** 保存時と転送時の暗号化の設定を、クラスターとは別に保存して再利用します。転送時の証明書は、EMR が作成して管理する方法、S3 の zip で渡す方法、独自の Java クラスで渡す方法があります。一部のエンドポイントは Kerberos 認証も必要です。

**SageMaker AI:** API や成果物の通信は暗号化されますが、分散学習や処理ジョブのノード間の通信は、既定では一部暗号化されません。医療などの要件なら有効にします。学習時間と費用が増えることがあります。

**EKS:** ノード間は Nitro の条件を確認します。Pod の通信に TLS を求める場合は、アプリ側で対応します。Kubernetes のシークレットは KMS のエンベロープ暗号化で保護します。これは保存時の話で、転送時とは別です。

詳細: [SageMaker の IAM と暗号化](../../services/sagemaker.md#iam-encryption)、[EMR](../../services/data-engineering.md#emr)、[EKS](../../services/containers.md#eks)

## タスク 5.2: 保存時のデータの統制 {#task-5-2}

### 5.2.1 保存時の暗号化の設計 {#skill-5-2-1}

**鍵のサービスの選択:**

| 観点 | KMS | KMS + CloudHSM キーストア | KMS + 外部キーストア | CloudHSM |
|---|---|---|---|---|
| 鍵素材の場所 | KMS の HSM | 自分の CloudHSM | AWS の外 | 自分の CloudHSM |
| AWS サービスとの統合 | 多数 | あり | あり（対称キーを使えるサービス） | 直接はなし |
| 認可 | IAM とキーポリシー | 同左 | 同左と外部の認可 | HSM のユーザー |
| 可用性の責任 | AWS | 利用者の設計（2台以上） | **すべて利用者** | 利用者の設計 |
| 向いている場面 | ほとんどの場合 | 単一テナントの HSM が必須 | 鍵を AWS の外に置く規制 | TDE、SSL オフロード、PKCS#11 |

AWS は、カスタムキーストアは規制で明確に必要な場合にだけ選ぶよう案内しています。

**暗号化の方式の選択:**

| 要件 | 方式 |
|---|---|
| 特別な要件がない | SSE-S3 |
| 権限の分離、CloudTrail で鍵の利用を監査 | SSE-KMS |
| 2層の暗号化が求められる | DSSE-KMS |
| 鍵を AWS に保存したくない | SSE-C。自分で鍵を管理する |
| AWS に平文を渡したくない | クライアント側の暗号化（AWS Encryption SDK） |

!!! note "SSE-C の状況"
    SSE-C は 2026年4月から、新しい汎用バケットなどで既定で無効です。必要ならバケットの設定で有効にします。

**費用のトレードオフ:** SSE-KMS はリクエストごとに KMS を呼びます。S3 バケットキーで KMS の呼び出しを減らせますが、暗号化コンテキストがオブジェクトの ARN からバケットの ARN に変わるので、それに依存するポリシーを確認します。

**カスタマー管理キーが必要な場面:** クロスアカウントでの共有、キーポリシーの管理、ローテーションの管理。AWS 管理キーはクロスアカウントで使えません。

詳細: [KMS キーの種類](../../services/kms.md#key-types)、[KMS との比較](../../services/identity-directory.md#cloudhsm-vs-kms)、[CloudHSM キーストア](../../services/identity-directory.md#cloudhsm-key-store)、[クライアント側とサーバー側](../../services/kms.md#client-vs-server-side)、[S3 の暗号化オプション](../../services/kms.md#s3-encryption)、[SSE-C の注意点](../../services/s3.md#sse-c)、[S3 バケットキー](../../services/s3.md#bucket-key)

### 5.2.2 データの完全性の保護 {#skill-5-2-2}

| 手段 | 守るもの | 要点 |
|---|---|---|
| S3 Object Lock | オブジェクトのバージョン | WORM。バージョニングが必須 |
| S3 のバージョニング | 誤削除と上書き | 消しても削除マーカーで戻せる。WORM ではない |
| Glacier の Vault Lock | Glacier のボールト | ロック後はポリシーを変更も削除もできない |
| AWS Backup の Vault Lock | 復旧ポイント | ガバナンスとコンプライアンス |
| Lambda のコード署名 | デプロイするコード | AWS Signer の署名だけを許可 |
| CloudTrail のログファイルの検証 | ログ | SHA-256 のハッシュと署名で改ざんを検出 |
| DataSync のデータの検証 | 転送したファイル | 転送先との一致を確認 |

| Object Lock のモード | 削除できる人 | 選ぶ場面 |
|---|---|---|
| ガバナンス | `s3:BypassGovernanceRetention` と専用ヘッダーを持つ人 | 社内の統制、誤削除の防止 |
| コンプライアンス | **ルートユーザーでも不可**。期間の短縮もできない | 規制の要件 |
| リーガルホールド | `s3:PutObjectLegalHold` を持つ人が外すまで | 期限のない訴訟対応 |

!!! note "Glacier の Vault Lock の状況"
    Vault Lock は別サービスの Amazon Glacier（ボールトの API）の機能で、このサービスは新規受付を終了しています。新しい環境では S3 Glacier ストレージクラスと S3 Object Lock を使います。

**Vault Lock の手順:** ポリシーをボールトに付けてロックを開始すると進行中の状態になり、ロック ID が返ります。**24時間以内**に検証して完了します。完了しなければポリシーは消えます。完了後は変更できません。

**Lambda のコード署名:** `UntrustedArtifactOnDeployment` を `Enforce` にすると、検証に失敗したデプロイをブロックします。既定の `Warn` は記録だけです。すでに動いている未署名のコードは止まらず、次のデプロイから検証されます。

詳細: [Object Lock](../../services/s3.md#object-lock)、[バージョニング](../../services/s3.md#versioning)、[Lambda のコード署名](../../services/lambda.md#code-signing)、[CloudTrail の調査](../../services/threat-detection.md#investigate-cloudtrail)、[DataSync のタスク設定](../../services/migration.md#datasync-task-settings)

### 5.2.3 ライフサイクルと保持 {#skill-5-2-3}

| 対象 | 手段 | 要点 |
|---|---|---|
| S3 | ライフサイクルルール | 移行と失効 |
| S3 | Object Lock | 保持期間中は消せない |
| EFS | ライフサイクルポリシー | 既定で30日アクセスなしで IA へ、90日で Archive へ |
| FSx for Lustre | バックアップの保持 | Persistent で S3 にリンクなしのみ。既定 0 日、最大 90 日 |
| CloudWatch Logs | 保持期間 | 既定は無期限 |
| EBS スナップショット | Data Lifecycle Manager | 作成、保持、削除を自動化 |

**FSx for Lustre の落とし穴:** Scratch や S3 にリンクした構成では、自動バックアップを使えません。S3 のバージョニングなど別の手段を使います。

**組み合わせの注意:** ロックされたバージョンは、ライフサイクルのルールでも削除されません。保持期間はライフサイクルの失効より長く保護されるので、費用を見積もるときに考慮します。

詳細: [S3 のライフサイクル](../../services/s3.md#lifecycle)、[EFS のライフサイクル](../../services/storage.md#efs-lifecycle)、[FSx のバックアップ](../../services/storage-advanced.md#fsx-protection)、[データの保持](../../services/storage.md#retention)

### 5.2.4 レプリケーションとバックアップの安全な設計 {#skill-5-2-4}

| サービス | 対象 | 向いている場面 |
|---|---|---|
| Data Lifecycle Manager | EBS スナップショットと EBS-backed AMI | EBS だけを自動化する |
| AWS Backup | 多数のサービス | サービスをまたぐ一元管理、組織での統制 |
| DataSync | ファイルとオブジェクトの転送 | オンプレミスや他のストレージとの同期 |

Data Lifecycle Manager 自体に追加費用はかからず、別のリージョンやアカウントへのバックアップにも使えます。ただし、他の方法で作ったスナップショットや AMI は管理できません。

**ランサムウェアへの備え:**

| 脅威 | 対策 |
|---|---|
| バックアップの削除 | AWS Backup の Vault Lock（コンプライアンスモードは猶予期間の後に解除不可） |
| アカウントごとの乗っ取り | 論理的にエアギャップされたボールトと別アカウントからの復元 |
| スナップショットの削除 | EBS スナップショットロック、Recycle Bin |
| S3 の暗号化や上書き | Object Lock、バージョニング |
| 鍵の削除 | キーのアクセス制御。削除の待機期間（7〜30日） |
| バックアップの感染 | GuardDuty の Malware Protection for AWS Backup |

**暗号化の扱い:** 別アカウントへのコピーには、カスタマー管理キーの共有が必要です。Vault Lock の最小、最大の保持期間はロック後の新しいジョブに適用され、既存の復旧ポイントには適用されません。

詳細: [AWS Backup](../../services/resilience.md#backup)、[Vault Lock](../../services/resilience.md#vault-lock)、[エアギャップのボールト](../../services/resilience.md#logically-air-gapped)、[ランサムウェアと誤削除の防止](../../services/resilience.md#immutable-compare)、[アカウント間コピー](../../services/resilience.md#backup-cross-account)、[DataSync](../../services/migration.md#datasync)、[EBS スナップショット](../../services/storage.md#ebs-snapshots)

## タスク 5.3: 機密データ、認証情報、シークレット、鍵素材の統制 {#task-5-3}

### 5.3.1 認証情報とシークレットの管理とローテーション {#skill-5-3-1}

| 観点 | Secrets Manager | Parameter Store（SecureString） |
|---|---|---|
| 自動ローテーション | あり | なし |
| 費用 | シークレットごとに課金 | 標準は無料 |
| 他リージョンへの複製 | あり | なし |
| クロスアカウント | リソースポリシー | 共有パラメータ |
| 選ぶ場面 | DB の認証情報などローテーションが必要 | 設定値と簡単な秘密 |

**ローテーションの方式:**

| 方式 | 対象 | Lambda |
|---|---|---|
| マネージドローテーション | 他のサービスが管理するシークレット（RDS など） | 不要 |
| Lambda 関数 | その他 | 必要。`createSecret`、`setSecret`、`testSecret`、`finishSecret` の4段階 |

| 戦略 | 動作 | 向いている場面 |
|---|---|---|
| シングルユーザー | 1ユーザーのパスワードを更新。一瞬拒否される可能性あり | ほとんどの場合 |
| 交代ユーザー | 2ユーザーを交互に更新 | 高い可用性。別途 `superuser` のシークレットが必要 |

スケジュールは最短 4 時間ごとです。ローテーションの Lambda が VPC 内なら、Secrets Manager への経路（VPC エンドポイントなど）が必要です。

**クロスアカウントで読む3条件:** シークレットのリソースポリシー、相手の IAM ポリシー、カスタマー管理キーのキーポリシー。既定の `aws/secretsmanager` は使えません。

詳細: [3 つのサービスの比較](../../services/secrets.md#comparison)、[ローテーション](../../services/secrets.md#rotation)、[クロスアカウント](../../services/secrets.md#secrets-cross-account)、[Lambda ローテーションの動き](../../services/secrets.md#lambda-rotation-steps)

### 5.3.2 インポートした鍵素材と外部キーストア {#skill-5-3-2}

**インポートの手順:**

1. `CreateKey --origin EXTERNAL` で鍵素材なしのキーを作ります。
2. `GetParametersForImport` でラッピング用の公開鍵とインポートトークンを取得します。
3. 鍵素材を暗号化し、`ImportKeyMaterial` でアップロードします。

**ローテーション:** 自動ローテーションはできません。対称キーならオンデマンドで、新しい鍵素材を先にインポートしてローテーションできます。期限（`ValidTo`）を設定したときは、期限切れの通知を CloudWatch アラームで作れます。

**外部キーストア（XKS）:** 鍵素材を AWS の外の鍵管理システムに置いたまま、KMS の API と AWS サービスの統合を使います（Hold Your Own Key）。

| 要素 | 内容 |
|---|---|
| 外部キーマネージャー | 自分が所有する HSM など。AES 256 ビットの鍵で暗号化と復号を行う |
| XKS プロキシ | KMS とキーマネージャーを仲介するソフトウェア。**自分で用意して運用する** |
| 接続方法 | パブリックエンドポイントか、VPC エンドポイントサービス |
| プロキシの認証 | KMS は SigV4 の専用の認証情報で署名。IAM の認証情報を流用しない |
| 二重暗号化 | KMS の鍵素材と外部の鍵で暗号化。どちらか一方だけでは復号できない |

**トレードオフ:** 可用性、耐久性、遅延がすべて利用者の責任になり、責任共有モデルが大きく変わります。外部の鍵を失うと暗号文は復元できません。逆に、アクセスを止めるとデータを使えなくできるのが利点です。AWS は往復の遅延を 35 ミリ秒以下にできるリージョンを勧めています。

**カスタムキーストアでできないこと:** 非対称キー、HMAC キー、インポートした鍵素材、自動ローテーション、マルチリージョンキー。外部キーストアの外部の鍵は、キーマネージャー側でローテーションします。

詳細: [鍵素材のインポート](../../services/kms.md#imported-key-material)、[ローテーションの設定](../../services/kms.md#rotation-settings)、[CloudHSM キーストア](../../services/identity-directory.md#cloudhsm-key-store)

### 5.3.3 インポートした鍵素材と AWS 生成の違い {#skill-5-3-3}

| 観点 | AWS 生成 | インポート |
|---|---|---|
| `Origin` | `AWS_KMS` | `EXTERNAL`。作成後に変更不可 |
| 耐久性の責任 | AWS | **利用者**。元のコピーを自分で保管する |
| 自動ローテーション | 可（90〜2,560日、既定365日） | 不可 |
| オンデマンドローテーション | 可（25回まで） | 対称キーは可 |
| 有効期限 | なし | `ValidTo` で設定可 |
| 鍵素材の即時削除 | 不可。キーの削除に7〜30日の待機 | `DeleteImportedKeyMaterial` ですぐ削除。再インポートで戻せる |
| 期限切れや削除の後 | | キーの状態が `PendingImport` になり使えない |
| 対象 | すべての種類 | 対称、非対称（ML-DSA と ML-KEM を除く）、HMAC、マルチリージョンキー |
| カスタムキーストア | | インポートできない |

**選ぶ理由:** 鍵素材の生成元（エントロピー）を証明したい、すぐに消して後で戻したい、AWS の外にも元のコピーを持ちたい、既存の署名鍵を使いたい、という要件です。

**誤解しやすい点:** インポートしても、対称キーの KMS の暗号文を KMS の外で復号することはできません。暗号文の形式は公開されていません。非対称キーと HMAC キーは KMS の外でも互換性があります。

詳細: [鍵素材のインポート](../../services/kms.md#imported-key-material)、[キーの無効化と削除](../../services/kms.md#disable-delete)

### 5.3.4 機密データのマスキング {#skill-5-3-4}

C03 で追加されたスキルです。

| 対象 | 手段 | 動き |
|---|---|---|
| CloudWatch Logs | データ保護ポリシー | 取り込み時に検出してマスク |
| SNS | メッセージデータ保護ポリシー | 受信時と配信時に検査 |
| CloudFront の特定のフィールド | フィールドレベル暗号化 | エッジで公開鍵により暗号化 |
| 生成 AI の入出力 | Bedrock Guardrails の機密情報フィルター | `ANONYMIZE` で置き換え |
| WAF のログ | フィールドの編集（redaction） | 指定の項目を隠す |
| S3 の中の機密データ | Macie | マスクではなく検出 |

**CloudWatch Logs のデータ保護:**

- アカウント全体か、ロググループごとに設定できます。両方あれば両方が適用されます。
- マスクは取り込み時に行います。**ポリシーの設定前のログはマスクされません。**
- Logs Insights やサブスクリプションフィルターなどの出口でもマスクされます。
- マスクされていないデータを見られるのは `logs:Unmask` を持つ主体だけです。
- 検知の数は `LogEventsWithFindings` メトリクスで確認できます。

!!! note "SNS のメッセージデータ保護の状況"
    2026年4月30日で新規顧客の受付を終了しました。既存の顧客は使い続けられます。公式の代替案は、Lambda と Bedrock Guardrails を組み合わせる構成です。

**SNS のデータ保護ポリシー:** トピックごとに 1 つです。文に方向とマネージドデータ識別子、操作を指定します。

| 項目 | 内容 |
|---|---|
| `DataDirection` | `Inbound`（Publish）、`Outbound`（配信） |
| Audit | 中断せず、メトリクスと検出のログを残す。1 ポリシーに 1 文のみ |
| De-identify | マスクまたは削除して続行 |
| Deny | 発行や配信を止める |

詳細: [CloudWatch Logs のデータ保護](../../services/secrets.md#cloudwatch-data-protection)、[データ保護ポリシー](../../services/observability.md#logs-data-protection)、[データ分類](../../services/secrets.md#data-classification)、[サニタイズとマスキング](../../services/secrets.md#sanitization-masking)、[フィールドレベル暗号化](../../services/networking.md#field-level-encryption)、[WAF のログ](../../services/certificates.md#waf-logging)

### 5.3.5 単一または複数リージョンの鍵と証明書 {#skill-5-3-5}

C03 で追加されたスキルです。KMS も ACM も Private CA も、**リージョンのリソース**です。

**カスタマー管理キー:** 

| 設定 | 内容 |
|---|---|
| キーポリシー | すべてのキーに必須。アクセスの基本 |
| グラント | 一時的な権限の委任 |
| `kms:ViaService` | 特定のサービス経由に限定 |
| 暗号化コンテキスト | 追加の認証データ。CloudTrail に残る |
| 削除 | 7〜30日の待機。使用中か CloudTrail で確認する |

**マルチリージョンキー:**

| 項目 | 内容 |
|---|---|
| 共通 | キー ID、鍵素材、キーの仕様、自動ローテーションの設定 |
| 別々 | キーポリシー、グラント、別名、タグ、有効と無効 |
| 変換 | 既存のキーを変換できない |
| 向いている場面 | クライアント側の暗号化で、別のリージョンでも再暗号化なしで復号したい |

別々のものがあるので、**各リージョンのキーポリシーをそれぞれ管理します**。鍵素材が共有されるので、鍵をリージョン内に閉じる要件には向きません。多くの場合は単一リージョンのキーが基本です。

**証明書:**

| 発行の方法 | 使える場所 | 自動更新 |
|---|---|---|
| ACM のパブリック証明書 | ACM の統合サービス | あり（DNS 検証が確実） |
| ACM で Private CA から要求 | ACM の統合サービス | あり |
| Private CA の `IssueCertificate` | どこでも | なし。自分で管理 |
| ACM へのインポート | ACM の統合サービス | なし |

| サービス | 証明書を置くリージョン |
|---|---|
| CloudFront | `us-east-1` のみ |
| API Gateway のエッジ最適化 | `us-east-1` |
| ALB、NLB、リージョナルの API Gateway | リソースと同じリージョン |

**Private CA:** ルート CA と下位 CA の階層を運用します。リージョン間でコピーできないので、必要なリージョンごとに計画します。証明書の有効期間が短い用途には、短期証明書モード（最大7日、費用が低い）があります。短いので失効の仕組みを省略できる場合があります。

詳細: [キーポリシーの詳細](../../services/kms.md#key-policy-details)、[マルチリージョンキー](../../services/kms.md#multi-region-keys)、[グラントの設定](../../services/kms.md#grant-settings)、[暗号化コンテキスト](../../services/kms.md#encryption-context)、[リージョンのルール](../../services/certificates.md#region-rules)、[自動更新](../../services/certificates.md#auto-renewal)、[Private CA](../../services/certificates.md#private-ca)、[Private CA の設定](../../services/certificates.md#private-ca-settings)

## 確認問題 {#self-check}

??? question "問1: 規制で、鍵素材を AWS の外に置き、いつでもアクセスを止められる必要があります。S3 と EBS は通常の AWS サービスとして使いたいです。何を選びますか？トレードオフは？"
    KMS の外部キーストアです。外部の鍵が AWS を離れず、接続を切ればデータを使えなくできます。代わりに可用性、耐久性、遅延がすべて利用者の責任で、XKS プロキシの運用も必要です。外部の鍵を失うとデータも失います。インポートした鍵素材では、コピーが KMS に渡るので要件を満たしません。CloudHSM は AWS の中にあります。

??? question "問2: すぐに鍵素材を削除し、必要になったら元に戻せるようにしたいです。キーの削除では7日待つ必要があります。何を使いますか？注意点は？"
    インポートした鍵素材です。`DeleteImportedKeyMaterial` ですぐ削除でき、同じ鍵素材を再度インポートすれば戻せます。耐久性は利用者の責任なので、元のコピーを失うと暗号文を復号できません。自動ローテーションもできず、カスタムキーストアでは使えません。

??? question "問3: 同じ VPC 内の Nitro の対応インスタンス間で通信が自動で暗号化されると聞きました。間に NLB を置いた通信も対象ですか？"
    対象外です。自動の暗号化の条件は、同じリージョンで、同じ VPC かピアリングした VPC にあり、ロードバランサーや Transit Gateway を通らないことです。経路を問わず暗号化が必要なら、アプリの TLS を使います。

??? question "問4: 監査で、S3 の記録を5年間、ルートユーザーを含む誰にも消されないようにすることを求められました。さらに社内のテストでは、担当者が消せる設定も試したいです。どう設定しますか？"
    本番はバージョニングと Object Lock のコンプライアンスモードで5年の保持を設定します。ルートユーザーでも消せず、短縮もできません。テストはガバナンスモードで行い、`s3:BypassGovernanceRetention` と専用ヘッダーで消せるようにします。コンプライアンスモードを試しに使うと、期限まで消せないので注意します。

??? question "問5: ランサムウェアで本番アカウントごと乗っ取られても復旧できるようにしたいです。AWS Backup を使っています。どう構成しますか？"
    論理的にエアギャップされたボールトにコピーし、AWS RAM などで別のアカウントと共有して、そこから復元できるようにします。このボールトには Vault Lock のコンプライアンスモードが自動で適用されます。同じアカウントの通常のボールトでは、権限を奪われると守りきれません。定期的に復元テストも行います。

??? question "問6: アプリのログに誤ってメールアドレスが出力されました。CloudWatch Logs のデータ保護ポリシーを設定しましたが、過去のログにはメールアドレスが見えます。なぜですか？また、特定の担当者だけ元の値を見たいです。"
    マスクは取り込み時に行うので、ポリシーの設定前のログには効きません。過去のログは保持期間の短縮などで別に対処します。元の値は `logs:Unmask` の権限を持つ主体だけが、Logs Insights の `unmask(@message)` などで見られます。

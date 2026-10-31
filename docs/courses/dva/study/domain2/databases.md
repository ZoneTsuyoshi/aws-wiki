# 分野2: データベース

データベースへの接続をどう認証し、通信とデータをどう守るかを問います。データストアとキャッシュの選択は[分野1](../domain1/databases.md)、接続プーリングや性能の調査は[分野4](../domain4/databases.md)で扱います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [2.1.5](../../domain2.md#skill-2-1-5) | IAM データベース認証 |
| [2.2.1](../../domain2.md#skill-2-2-1) | SSL/TLS の強制、ElastiCache の暗号化 |
| [2.2.6](../../domain2.md#skill-2-2-6) | テナントごとのデータの分離 |
| [2.2.7](../../domain2.md#skill-2-2-7) | Secrets Manager との統合 |

## 学習の順番 {#study-order}

1. [IAM データベース認証](../../../../services/databases.md#rds-iam-auth): トークンの寿命と、`rds-db:connect` の権限を覚えます。
2. [Secrets Manager との統合](../../../../services/databases.md#rds-secrets-manager): RDS にパスワードを管理させる方法を確認します。
3. [SSL/TLS](../../../../services/databases.md#rds-ssl): エンジンごとの強制の設定を見ます。
4. [RDS Proxy の設定](../../../../services/databases.md#rds-proxy-settings): `RequireTLS`、`DefaultAuthScheme` と、プロキシのロールの権限を押さえます。
5. [ElastiCache の認証と暗号化](../../../../services/databases.md#elasticache-security): AUTH、RBAC と、作成後に変えられない設定を確認します。
6. [マルチテナントのデータアクセス](../../../../services/databases.md#multi-tenant): 3 つのモデルと、データストアごとの強制の方法を整理します。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| IAM 認証トークンの寿命 | 15 分 | 接続の確立にだけ使い、既存の接続は切れない |
| マスターユーザーのシークレット | 既定で 7 日ごとにローテーション | スケジュールは変更できる |
| `rds.force_ssl` | PostgreSQL 15 以降は既定 1。それより前は 0 | MySQL は `require_secure_transport=ON` |
| AUTH トークン | 16〜128 文字 | 転送中の暗号化が必須 |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| DB のパスワードをアプリに持たせたくない | IAM データベース認証か Secrets Manager |
| IAM 認証のアプリに付ける権限 | `rds-db:connect`。リソースは `dbuser` の ARN |
| マスターパスワードを自動で変更する | `--manage-master-user-password` |
| PostgreSQL 14 で SSL を強制する | カスタムのパラメータグループで `rds.force_ssl=1` |
| サーバー証明書とホスト名の両方を検証する | `sslmode=verify-full` と `global-bundle.pem` |
| RDS Proxy のクライアント接続に TLS を強制する | `RequireTLS` |
| ElastiCache の AUTH トークンを無停止で変える | `ROTATE` の後に `SET` |
| 規制があり、テナントを強く分離する | サイロモデル |
| 共有テーブルでテナントを分離する | プールモデルと `dynamodb:LeadingKeys`。RDB は PostgreSQL の行レベルセキュリティ |

## 引っかかりやすい点 {#traps}

- PostgreSQL で `rds_iam` を付けたユーザーは、パスワードで入れなくなります。
- Route 53 のカスタム DNS 名では認証トークンを作れません。DB のエンドポイントを使います。
- シークレットを長時間キャッシュすると、ローテーションの後に認証エラーになります。
- RDS Proxy の IAM ロールがシークレットを読めないと、プロキシは DB に接続できません。
- ノードベースの Valkey と Redis OSS の保存時の暗号化は作成時のみです。後から有効にするならバックアップから作り直します。
- RDS の KMS キーは[作成後に変更できません](../../../../services/kms.md#service-integration)。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [databases 問2](../../exercises/databases.md#q2) | 2.1.5 | Lambda 関数がパスワードを使わずに RDS for PostgreSQL に接続できるように、… |
| [databases 問3](../../exercises/databases.md#q3) | 2.2.7 | マスターユーザーのパスワードをコードに書かず、定期的に自動で変更したいと考えています。運用負荷が最も… |
| [databases 問4](../../exercises/databases.md#q4) | 2.2.1 | RDS for PostgreSQL 14 のインスタンスで、すべてのクライアント接続に SSL を… |
| [databases 問13](../../exercises/databases.md#q13) | 2.2.1 | ノードベースの Redis OSS のクラスターに AUTH を有効にしようとしましたが、設定できま… |

<!-- questions:end -->

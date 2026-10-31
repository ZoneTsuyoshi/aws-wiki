# 分野2: Secrets Manager と Parameter Store

シークレットをどのサービスで守るか、PII や PHI をログにどう残さないかを問います。環境ごとの設定や AppConfig でのデプロイは[分野3](../domain3/secrets.md)で扱います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [2.2.6](../../domain2.md#skill-2-2-6) | 機密データの分類、マスキング、アクセス制限 |
| [2.2.7](../../domain2.md#skill-2-2-7) | シークレット管理サービスの選択と利用 |

## 学習の順番 {#study-order}

1. [3 つのサービスの比較](../../../../services/secrets.md#comparison): 自動ローテーションと料金の違いで選び方を決めます。
2. [Secrets Manager](../../../../services/secrets.md#secrets-manager)と[ステージングラベル](../../../../services/secrets.md#version-labels): API と 3 つのラベルの意味を覚えます。
3. [ローテーション](../../../../services/secrets.md#rotation): 方式と 4 ステップ、シングルユーザーと交代ユーザーの違いを理解します。
4. [取得とキャッシュ](../../../../services/secrets.md#retrieval-caching)と [Lambda 拡張](../../../../services/secrets.md#lambda-extension): 既定の更新間隔と、古い値が返る場面を確認します。
5. [クロスアカウントでの利用](../../../../services/secrets.md#secrets-cross-account): 必要な 3 つの許可を覚えます。
6. [ティア](../../../../services/secrets.md#parameter-tiers)と [SecureString](../../../../services/secrets.md#securestring): サイズ、ポリシー、`WithDecryption` の条件を押さえます。
7. [データ分類](../../../../services/secrets.md#data-classification)と[サニタイズとマスキング](../../../../services/secrets.md#sanitization-masking): 手法ごとに元の値に戻せるかを整理します。
8. [CloudWatch Logs のデータ保護](../../../../services/secrets.md#cloudwatch-data-protection): マスキングの時点と `logs:Unmask` を確認します。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| シークレットの値 | 65,536 バイト | パラメータは Standard 4 KB、Advanced 8 KB |
| ローテーションの最短間隔 | 4 時間 | ウィンドウは最短 1 時間。cron は UTC |
| 復旧期間 | 既定 30 日。7〜30 日 | 待機中は `GetSecretValue` が失敗する |
| キャッシュライブラリの更新 | 既定 1 時間 | 無効化の機能はない |
| Lambda 拡張 | ポート 2773、TTL 既定 300 秒 | `X-Aws-Parameters-Secrets-Token` が必須 |
| Parameter Store の取得 | 既定で合計 40 TPS | 超えるならキャッシュか高スループット |
| データ保護ポリシー | ロググループごとに 1 つ | アカウント全体のものと両方が適用される |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| データベースのパスワードを自動でローテーションする | Secrets Manager |
| ローテーションが不要な値を低コストで保存する | Parameter Store の `SecureString` |
| 切り替えの瞬間も常に接続できるようにする | 交代ユーザー戦略。別途 `superuser` のシークレットが必要 |
| Lambda でシークレットの取得が遅く、費用も高い | Parameters and Secrets Lambda Extension でキャッシュする |
| 別アカウントからシークレットを読む | リソースポリシー、IAM、カスタマー管理キーのキーポリシーの3つ |
| ローテーションの後に前の値へ戻す | `UpdateSecretVersionStage` で `AWSCURRENT` を移す |
| `SecureString` が暗号文のまま返る | `WithDecryption=True` と、カスタマー管理キーなら `kms:Decrypt` |
| ログのメールアドレスを自動でマスクする | CloudWatch Logs のデータ保護ポリシー |
| マスクされていないログを見る | `logs:Unmask` を持つ主体だけが見られる |
| 共有テーブルでテナントのデータを分ける | `dynamodb:LeadingKeys` とセッションタグ。テナント ID は検証済みのトークンから取る |

## 引っかかりやすい点 {#traps}

- データ保護ポリシーは取り込み時に動きます。設定前のログはマスクされません。
- `testSecret` が失敗すると `AWSCURRENT` は動きません。シングルユーザーで `setSecret` まで進むと、データベースのパスワードだけが変わり接続エラーになります。
- ローテーション直後にキャッシュの古い値で接続できなくなります。接続エラー時に取り直すか、TTL を短くします。
- 既定の `aws/secretsmanager` は AWS 管理キーなので、クロスアカウントには使えません。
- `GetParametersByPath` では、`/a` へのアクセスを持つ主体は、`/a/b` を明示的に拒否していても `Recursive=true` で取得できます。
- ステージ変数や Lambda 環境変数の平文に資格情報を入れません。環境変数にはシークレットの名前だけを渡します。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [secrets 問1](../../exercises/secrets.md#q1) | 2.2.7 | データベースのパスワードを、毎週日曜の日本時間 2:00 から 2 時間以内に自動でローテーションし… |
| [secrets 問2](../../exercises/secrets.md#q2) | 2.2.7 | Lambda によるローテーションで、testSecret のステップが失敗しました。アプリの Ge… |
| [secrets 問3](../../exercises/secrets.md#q3) | 2.2.7 | Secrets Manager のバージョンの説明として正しいものを選んでください。（2つ選択） |
| [secrets 問4](../../exercises/secrets.md#q4) | 2.2.7 | テストの後、同じ名前のシークレットをすぐに作り直したいと考えています。DeleteSecret の指… |
| [secrets 問5](../../exercises/secrets.md#q5) | 2.2.7 | 東京のシークレットをオレゴンに複製しています。プライマリのシークレットを削除しようとすると失敗します… |
| [secrets 問6](../../exercises/secrets.md#q6) | 2.2.7 | Lambda に Parameters and Secrets Lambda Extension を… |
| [secrets 問7](../../exercises/secrets.md#q7) | 2.2.7 | CloudFormation で RDS のパスワードに {{resolve:secretsmana… |
| [secrets 問8](../../exercises/secrets.md#q8) | 2.2.7 | EC2 の UserData に {{resolve:ssm-secure:/prod/token:… |
| [secrets 問16](../../exercises/secrets.md#q16) | 2.2.6 | ロググループに CloudWatch Logs のデータ保護ポリシーを設定し、メールアドレスをマスク… |
| [secrets 問17](../../exercises/secrets.md#q17) | 2.2.6 | サポート担当者のロールに、Customers テーブルの name と plan だけを読ませます。… |
| [secrets 問18](../../exercises/secrets.md#q18) | 2.2.6 | 多数の S3 バケットにデータが保管されていますが、どこに個人情報があるのかわかりません。機械学習と… |

<!-- questions:end -->

# 分野4: Redshift の権限とデータ共有

データベースの権限の管理とデータ共有を問います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [4.2.3](../../domain4.md#skill-4-2-3) | データベースのユーザー、グループ、ロールの権限 |
| [4.5.1](../../domain4.md#skill-4-5-1) | データ共有の権限の付与 |

## 学習の順番 {#study-order}

1. [暗号化とセキュリティ](../../../../services/data-engineering.md#redshift-security): ロール、RLS、マスキングを確認します。
2. [IAM データベース認証](../../../../services/databases.md#rds-iam-auth): RDS の認証を確認します。
3. [データ共有](../../../../services/data-engineering.md#redshift-data-sharing): プロデューサーとコンシューマーの手順を覚えます。

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 権限をまとめて付与する | `CREATE ROLE` と `GRANT ROLE` |
| 見える行を制限する | 行レベルセキュリティ |
| 列の値を隠す | 動的データマスキング |
| コピーせずライブで渡す | データ共有 |

## 引っかかりやすい点 {#traps}

- データ共有はアカウントやリージョンをまたげます。
- コンシューマーは `CREATE DATABASE ... FROM DATASHARE` を実行します。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [redshift 問16](../../exercises/redshift.md#q16) | 4.2.3 | アナリストが 50 人います。Redshift で同じ権限を、人ごとの GRANT なしでまとめて付… |
| [redshift 問17](../../exercises/redshift.md#q17) | 4.2.3 | 販売担当者には自分の地域の行だけを見せ、支払いの担当者以外にはカード番号を隠します。Redshift… |
| [redshift 問18](../../exercises/redshift.md#q18) | 4.2.3 | RDS のデータベースに、パスワードを保存せず IAM の認証でユーザーを接続させます。何を使います… |
| [redshift 問19](../../exercises/redshift.md#q19) | 4.5.1 | ETL のクラスターのデータを、BI のワークグループへコピーせずライブで渡します。プロデューサーの… |
| [redshift 問20](../../exercises/redshift.md#q20) | 4.5.1 | Redshift のデータ共有の説明として正しいものはどれですか。（2つ選択） |
| [redshift 問21](../../exercises/redshift.md#q21) | 4.5.1 | 共有の要件と選択の組み合わせで正しいものはどれですか。 |

<!-- questions:end -->

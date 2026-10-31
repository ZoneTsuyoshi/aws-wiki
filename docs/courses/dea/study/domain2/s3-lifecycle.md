# 分野2: S3 のライフサイクルとオープンテーブル形式

ライフサイクル、失効、バージョニング、削除の要件、データの保護と Iceberg を問います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [2.1.7](../../domain2.md#skill-2-1-7) | オープンテーブル形式 |
| [2.3.2](../../domain2.md#skill-2-3-2) | ライフサイクルによるストレージ階層の変更 |
| [2.3.3](../../domain2.md#skill-2-3-3) | 期限が来たデータの失効 |
| [2.3.4](../../domain2.md#skill-2-3-4) | S3 バージョニングと DynamoDB TTL |
| [2.3.5](../../domain2.md#skill-2-3-5) | 業務と法律の要件に合わせたデータの削除 |
| [2.3.6](../../domain2.md#skill-2-3-6) | 回復性と可用性によるデータの保護 |

## 学習の順番 {#study-order}

1. [ライフサイクル](../../../../services/s3.md#lifecycle): 移行の一方向性と 128 KB を確認します。
2. [ライフサイクルのルール要素](../../../../services/s3.md#lifecycle-elements): 4 つの要素を区別します。
3. [バージョニング](../../../../services/s3.md#versioning): 削除マーカーの動きを理解します。
4. [TTL](../../../../services/dynamodb.md#ttl): 属性の型と削除の時期を覚えます。
5. [Object Lock](../../../../services/s3.md#object-lock): モードとリーガルホールドを区別します。
6. [Iceberg](../../../../services/data-engineering.md#iceberg): 機能と保守を確認します。
7. [AWS Backup](../../../../services/resilience.md#backup): 一元管理を確認します。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| 移行しないサイズ | 128 KB 未満（既定） | フィルターで変更できる |
| 最小保存期間 | Glacier Instant Retrieval と Flexible Retrieval は 90 日、Deep Archive は 180 日 | 前に移すと残り分が課金 |
| DynamoDB PITR | 1〜35 日 |  |
| S3 Tables の圧縮の目標 | 既定 512 MB |  |
| S3 Tables のスナップショット | 既定は最小 1 個、最大 120 時間 |  |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 誰にも消させない | コンプライアンスモード |
| 調査が終わるまで残す | リーガルホールド |
| バージョンのあるバケットで実データを消す | `NoncurrentVersionExpiration` |
| 誤って削除した | 削除マーカーのバージョン ID を指定して `DELETE` |
| 保守を任せた Iceberg | S3 Tables |
| リージョンの障害に備える | CRR |

## 引っかかりやすい点 {#traps}

- `Expiration` だけではバージョニングのあるバケットの費用は下がりません。
- DynamoDB の TTL は秒単位の Number です。
- グローバルテーブルは誤操作も複製します。
- S3 Tables の権限は `s3tables` で、`s3` とは別です。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [s3-lifecycle 問1](../../exercises/s3-lifecycle.md#q1) | 2.1.7 | S3 のデータレイクで、同時の読み書き、行単位の MERGE、過去の時点の参照が要ります。どの形式を… |
| [s3-lifecycle 問2](../../exercises/s3-lifecycle.md#q2) | 2.1.7 | Iceberg の小さなファイルと古いスナップショットの保守を、自分で設定せず任せたいです。何を選び… |
| [s3-lifecycle 問3](../../exercises/s3-lifecycle.md#q3) | 2.1.7 | Iceberg と S3 Tables の説明として正しいものはどれですか。（2つ選択） |
| [s3-lifecycle 問4](../../exercises/s3-lifecycle.md#q4) | 2.3.2 | ログを 30 日後に Standard-IA、120 日後に Glacier へ移します。正しい要素… |
| [s3-lifecycle 問5](../../exercises/s3-lifecycle.md#q5) | 2.3.2 | ライフサイクルで Deep Archive へ移したのに、64 KB のログファイルが移行されません… |
| [s3-lifecycle 問6](../../exercises/s3-lifecycle.md#q6) | 2.3.2 | アクセスの頻度が読めないデータの費用を下げます。また、Deep Archive にあるオブジェクトを… |
| [s3-lifecycle 問7](../../exercises/s3-lifecycle.md#q7) | 2.3.3 | バージョニングが有効なバケットに Expiration だけ設定しました。1 年後も費用が下がりませ… |
| [s3-lifecycle 問8](../../exercises/s3-lifecycle.md#q8) | 2.3.3 | バケットの費用に、中断したマルチパートアップロードの断片が含まれています。何で片付けますか。 |
| [s3-lifecycle 問9](../../exercises/s3-lifecycle.md#q9) | 2.3.3 | バージョニングのあるバケットで、期限切れのデータを完全に消し、残骸も残さない設定の組み合わせはどれで… |
| [s3-lifecycle 問10](../../exercises/s3-lifecycle.md#q10) | 2.3.4 | バージョニングのあるバケットで、誤ってオブジェクトを削除しました。バージョン ID は指定していませ… |
| [s3-lifecycle 問11](../../exercises/s3-lifecycle.md#q11) | 2.3.4 | DynamoDB の TTL を設定しましたが、項目が削除されません。属性は ISO 8601 の文… |
| [s3-lifecycle 問12](../../exercises/s3-lifecycle.md#q12) | 2.3.4 | TTL で項目が消える前後に、次の要件があります。正しい対応はどれですか。（2つ選択） |
| [s3-lifecycle 問13](../../exercises/s3-lifecycle.md#q13) | 2.3.4 | バージョニングを有効にした分析バケットの費用が増えています。日次で同じキーを上書きしています。説明と… |
| [s3-lifecycle 問14](../../exercises/s3-lifecycle.md#q14) | 2.3.4 | 別のリージョンのバケットへレプリケーションしたいのに、設定できません。前提として確認するものはどれで… |
| [s3-lifecycle 問15](../../exercises/s3-lifecycle.md#q15) | 2.3.5 | 規制で、7 年間はルートユーザーを含めて誰もログを消せないようにします。どの設定ですか。 |
| [s3-lifecycle 問16](../../exercises/s3-lifecycle.md#q16) | 2.3.5 | 訴訟の調査中のデータを、期限を決めずに残し、調査が終わったら解除します。どの機能ですか。 |
| [s3-lifecycle 問17](../../exercises/s3-lifecycle.md#q17) | 2.3.5 | GDPR の削除要求で、特定の人の行を消します。データは Iceberg とそのバックアップにありま… |
| [s3-lifecycle 問18](../../exercises/s3-lifecycle.md#q18) | 2.3.6 | リージョンの障害に備え、S3 のデータを別のリージョンにも置きます。RPO は短くしたいです。どの機… |
| [s3-lifecycle 問19](../../exercises/s3-lifecycle.md#q19) | 2.3.6 | RDS、DynamoDB、EFS のバックアップをまとめて管理し、別のリージョンへもコピーします。ど… |
| [s3-lifecycle 問20](../../exercises/s3-lifecycle.md#q20) | 2.3.6 | 誤操作で DynamoDB の項目を消しました。2 日前の時点へ戻します。何を有効にしておくべきでし… |

<!-- questions:end -->

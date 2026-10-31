# 分野2: Redshift

データへの遠隔アクセス、ロック、ロードとアンロード、スキーマの設計を問います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [2.1.5](../../domain2.md#skill-2-1-5) | データの移行と遠隔アクセス |
| [2.1.6](../../domain2.md#skill-2-1-6) | ロックの管理 |
| [2.3.1](../../domain2.md#skill-2-3-1) | S3 と Redshift の間のロードとアンロード |
| [2.4.1](../../domain2.md#skill-2-4-1) | Redshift、DynamoDB、Lake Formation のスキーマ設計 |

## 学習の順番 {#study-order}

1. [分散スタイル](../../../../services/data-engineering.md#redshift-distribution): 結合列と `ALL` の使いどころを覚えます。
2. [ソートキー](../../../../services/data-engineering.md#redshift-sort-keys): `COMPOUND` の先頭の列を確認します。
3. [COPY と UNLOAD](../../../../services/data-engineering.md#redshift-copy): オプションと暗号化の現状を確認します。
4. [Spectrum](../../../../services/data-engineering.md#redshift-spectrum): 外部テーブルの制限を押さえます。
5. [マテリアライズドビュー](../../../../services/data-engineering.md#redshift-materialized-views): 更新と自動書き換えを理解します。
6. [ロックと同時実行](../../../../services/data-engineering.md#redshift-locks): 確認の方法と切り方を覚えます。

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| RDS を最新のまま直接読む | フェデレーテッドクエリ |
| めったに読まない S3 のデータと結合する | Spectrum |
| 同じ集計を繰り返す | マテリアライズドビュー |
| `COPY` と `UNLOAD` の通信を VPC に通す | Enhanced VPC Routing |
| 小さなディメンションを結合する | `DISTSTYLE ALL` |
| アクセスパターンから設計する | DynamoDB。Redshift は分析のクエリから |

## 引っかかりやすい点 {#traps}

- `TRUNCATE` と `DROP TABLE` は排他ロックで読み取りも止めます。
- 新規顧客はクライアント側暗号化の `COPY` と `UNLOAD` を使えません。
- 日付の `DISTKEY` は狭い期間で偏ります。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [redshift 問1](../../exercises/redshift.md#q1) | 2.1.5 | Redshift のダッシュボードで、RDS for PostgreSQL の在庫を最新の状態で表示… |
| [redshift 問2](../../exercises/redshift.md#q2) | 2.1.5 | 同じ結合と集計を繰り返すダッシュボードが遅いです。結果を事前に計算して保存します。ベーステーブルは夜… |
| [redshift 問3](../../exercises/redshift.md#q3) | 2.1.5 | データの扱いの説明として正しいものはどれですか。（2つ選択） |
| [redshift 問4](../../exercises/redshift.md#q4) | 2.1.6 | 夜間のロード中も、BI のクエリは読み続けられています。ところが TRUNCATE を実行した時だけ… |
| [redshift 問5](../../exercises/redshift.md#q5) | 2.1.6 | Redshift で長時間止まっているセッションがテーブルをロックしています。確認して解消する手順は… |
| [redshift 問6](../../exercises/redshift.md#q6) | 2.1.6 | RDS for MySQL 8.0 のロックを調べ、問題のスレッドを切ります。正しいものはどれですか… |
| [redshift 問7](../../exercises/redshift.md#q7) | 2.3.1 | S3 の Parquet を Redshift へロードします。長期の認証情報は使いません。正しい文… |
| [redshift 問8](../../exercises/redshift.md#q8) | 2.3.1 | レポートを S3 へ出し、Athena で読みます。1 ファイルを 256 MB 以下にし、地域で区… |
| [redshift 問9](../../exercises/redshift.md#q9) | 2.3.1 | COPY と UNLOAD の通信を、インターネットではなく VPC の中に通し、VPC フローログ… |
| [redshift 問10](../../exercises/redshift.md#q10) | 2.3.1 | 新規の顧客が、UNLOAD の結果を S3 で暗号化します。現在の選択肢として正しいものはどれですか… |
| [redshift 問11](../../exercises/redshift.md#q11) | 2.4.1 | 大きな売上ファクトを顧客で結合し、日付の範囲で絞ります。小さな店舗ディメンションも結合します。設計と… |
| [redshift 問12](../../exercises/redshift.md#q12) | 2.4.1 | 次のうち、Redshift のスキーマとして不適切なものはどれですか。 |
| [redshift 問22](../../exercises/redshift.md#q22) | 2.4.1 | DynamoDB で注文を設計します。「顧客の注文を新しい順に読む」と「注文 ID で 1 件読む」… |
| [redshift 問23](../../exercises/redshift.md#q23) | 2.4.1 | データレイクのスキーマを設計します。部門とセンシティビティごとの権限を、後から増えるテーブルにも適用… |

<!-- questions:end -->

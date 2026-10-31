# 分野3: Athena と SQL

Athena の使い方、ビュー、Spark、集計の SQL を問います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [3.1.7](../../domain3.md#skill-3-1-7) | データのクエリ（Athena） |
| [3.2.3](../../domain3.md#skill-3-2-3) | Redshift と Athena の SQL とビュー |
| [3.2.4](../../domain3.md#skill-3-2-4) | Athena の Spark ノートブック |
| [3.2.6](../../domain3.md#skill-3-2-6) | 集計、移動平均、グループ化、ピボット |

## 学習の順番 {#study-order}

1. [Athena](../../../../services/streaming.md#athena): 基本の仕組みを確認します。
2. [速く、安くするコツ](../../../../services/streaming.md#athena-performance): 形式とパーティションを覚えます。
3. [ワークグループ](../../../../services/streaming.md#athena-workgroups): 2 種類の制限と上書きを区別します。
4. [マテリアライズドビュー](../../../../services/data-engineering.md#redshift-materialized-views): ビューとの違いを確認します。
5. [S3 上のログを問い合わせる](../../../../services/streaming.md#athena-logs): SQL の例を読みます。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| クエリ結果の再利用の既定の経過時間 | 60 分 | 分、時間、日で指定 |
| Spark（コンソール） | PySpark エンジン バージョン 3 | コンソールのノートブック |
| Spark（Unified Studio など） | Apache Spark バージョン 3.5 | Spark Connect |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 1 クエリのスキャンを止める | クエリごとの制限 |
| 期間の合計を通知する | ワークグループ全体の制限と SNS |
| 結果の場所を強制する | クライアント側の設定を上書き |
| 結果を保存する | CTAS |
| Python で対話的に探索する | Athena の Spark |
| 集計の後に絞る | `HAVING` |

## 引っかかりやすい点 {#traps}

- ビューは結果を保存しません。
- 当日を含む 7 日は `6 PRECEDING` です。
- 結果の再利用は古い結果を返すことがあります。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [athena 問1](../../exercises/athena.md#q1) | 3.1.7 | Athena の費用と時間を減らす効果が最も大きいものはどれですか。 |
| [athena 問2](../../exercises/athena.md#q2) | 3.1.7 | チームのアナリストが巨大なクエリを誤って実行します。1 クエリが 1 TB を超えたら止めます。何を… |
| [athena 問3](../../exercises/athena.md#q3) | 3.1.7 | 全アナリストのクエリ結果を、決められた暗号化済みのバケットへ強制します。どの設定ですか。 |
| [athena 問4](../../exercises/athena.md#q4) | 3.1.7 | 同じダッシュボードのクエリが 10 分おきに実行されます。データの更新は 1 時間に 1 回です。ス… |
| [athena 問5](../../exercises/athena.md#q5) | 3.2.3 | Athena の CREATE VIEW で複雑な SQL をまとめました。クエリが速くなりません。… |
| [athena 問6](../../exercises/athena.md#q6) | 3.2.3 | Athena の集計の結果を、S3 に Parquet で保存し、後のクエリで読みます。どの文ですか… |
| [athena 問7](../../exercises/athena.md#q7) | 3.2.3 | Redshift で、集計の結果を保存して速くし、S3 のテーブルとも結合します。正しい組み合わせは… |
| [athena 問8](../../exercises/athena.md#q8) | 3.2.4 | データサイエンティストが、クラスターを作らずに Python で対話的に S3 のデータを探索します… |
| [athena 問9](../../exercises/athena.md#q9) | 3.2.4 | Athena の Spark のエンジンと実行の場所の組み合わせで正しいものはどれですか。 |
| [athena 問10](../../exercises/athena.md#q10) | 3.2.4 | 要件と選択の組み合わせで正しいものはどれですか。 |
| [athena 問11](../../exercises/athena.md#q11) | 3.2.6 | 日次の売上から、直近 7 日の移動平均を求めます。正しいウィンドウの指定はどれですか。 |
| [athena 問12](../../exercises/athena.md#q12) | 3.2.6 | 地域ごとの売上の合計が 100 万を超える地域だけを求めます。正しい SQL はどれですか。 |
| [athena 問13](../../exercises/athena.md#q13) | 3.2.6 | Redshift で四半期の行を列にします。方法として正しいものはどれですか。（2つ選択） |

<!-- questions:end -->

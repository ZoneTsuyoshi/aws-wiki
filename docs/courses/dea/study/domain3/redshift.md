# 分野3: Redshift の機能

Redshift の機能を使った処理と、ワークロードの分離を問います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [3.1.4](../../domain3.md#skill-3-1-4) | サービスの機能を使ったデータ処理 |

## 学習の順番 {#study-order}

1. [ワークロード管理](../../../../services/data-engineering.md#redshift-wlm): キュー、SQA、同時実行スケーリングを確認します。
2. [データを取り込む他の方法](../../../../services/data-engineering.md#redshift-ingestion): ストリーミング取り込みを確認します。
3. [マテリアライズドビュー](../../../../services/data-engineering.md#redshift-materialized-views): 増分の更新を理解します。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| 手動 WLM | 合計 15 スロット以下を推奨 | キューあたり最大 50 |
| 自動 WLM のキュー | 最大 8 個 | 優先度を設定できる |
| SQA の最大実行時間 | 動的または 1〜20 秒 | 既定で有効 |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| ETL と BI を分ける | キューを分け、優先度と同時実行スケーリング |
| 短いクエリを優先する | SQA |
| DWH の中で繰り返しの計算をする | マテリアライズドビュー |

## 引っかかりやすい点 {#traps}

- インターリーブドソートキーのテーブルは同時実行スケーリングの対象外です。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [redshift 問13](../../exercises/redshift.md#q13) | 3.1.4 | ETL の負荷が高い時間に、BI のダッシュボードが待たされます。ノードは増やしません。Redshi… |
| [redshift 問14](../../exercises/redshift.md#q14) | 3.1.4 | 短いダッシュボードのクエリが、長いレポートの後ろで待たされます。短いクエリを優先する機能はどれですか… |
| [redshift 問15](../../exercises/redshift.md#q15) | 3.1.4 | Redshift の機能でパイプラインを減らします。正しい組み合わせはどれですか。（2つ選択） |

<!-- questions:end -->

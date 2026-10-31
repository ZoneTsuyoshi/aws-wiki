# 分野1: データ変換と特徴量

変換ツールを利用者とコードの有無で選び、Feature Store で学習と推論のずれを防ぎます。特徴量の計算は値で問われます。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [1.1.9](../../domain1.md#skill-1-1-9) | Feature Store への取り込み |
| [1.2.1](../../domain1.md#skill-1-2-1) | AWS ツールによるデータ変換 |
| [1.2.2](../../domain1.md#skill-1-2-2) | 特徴量の作成と管理 |
| [1.2.4](../../domain1.md#skill-1-2-4) | 特徴量エンジニアリング |
| [1.3.7](../../domain1.md#skill-1-3-7) | データのクリーニング |

## 学習の順番 {#study-order}

1. [Data Wrangler](../../../../services/sagemaker.md#data-wrangler)、[DataBrew](../../../../services/data-engineering.md#databrew)、[EMR](../../../../services/data-engineering.md#emr): 誰が使うか、コードがあるかで選びます。
2. [Feature Store](../../../../services/sagemaker.md#feature-store): オンラインとオフラインの違い、必須の項目、取り込みの方法を覚えます。
3. [特徴量エンジニアリング](../../../../services/ai-fundamentals.md#feature-engineering): 標準化、対数変換、データ漏えいを確認します。
4. [データ品質](../../../../services/ai-fundamentals.md#data-quality): 欠損、外れ値、重複の扱いを押さえます。
5. [組み込みアルゴリズム](../../../../services/sagemaker.md#built-in-algorithms): 異常なレコードの検出に Random Cut Forest を使えることを確認します。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| 最小最大の正規化 | 範囲 0〜100 で 25 → 0.25 | 0〜1 に揃える |
| 標準化 | 平均 50、標準偏差 10 で 70 → 2.0 | 線形モデルや k-means の前 |
| フィーチャーグループの必須項目 | `RecordIdentifierFeatureName`、`EventTimeFeatureName` | `TtlDuration` は任意 |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 分析担当がコードなしで整形する | DataBrew |
| ML の前処理を画面で試して Pipelines へ渡す | Data Wrangler |
| 既存の Spark コードと細かい制御 | EMR |
| 推論は最新の値、学習は履歴 | オンラインとオフラインの両方を有効にする |
| 大量のバッチの取り込み | Spark コネクタ |
| 共通の ID がない顧客の照合 | FindMatches |

## 引っかかりやすい点 {#traps}

- オンラインストアだけの設定では履歴が残りません。
- 全データで標準化してから分割すると、データ漏えいになります。
- 外れ値がある列の補完には、平均より中央値が向きます。
- XGBoost などの木モデルは尺度を揃えなくても動きますが、k-means や k-NN は揃えます。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [data-prep 問1](../../exercises/data-prep.md#q1) | 1.2.1 | 分析担当者がコードを書かずに、売上データの整形手順を画面で作り、毎月同じ手順を再利用します。ML の… |
| [data-prep 問2](../../exercises/data-prep.md#q2) | 1.2.1 | データサイエンティストが画面で ML の前処理を試し、結果を Feature Store と Pip… |
| [data-prep 問3](../../exercises/data-prep.md#q3) | 1.2.1 | 既に Spark の独自コードがあり、クラスターの構成や Spark の設定を細かく調整します。大規… |
| [data-prep 問4](../../exercises/data-prep.md#q4) | 1.2.2 | 不正検知で、推論時に顧客の最新の特徴量を低遅延で読み、再学習には過去の値を使います。Feature … |
| [data-prep 問5](../../exercises/data-prep.md#q5) | 1.2.2 | 推論では最新の値を読み、学習では特徴量の履歴を検索します。それぞれの方法の組み合わせとして正しいもの… |
| [data-prep 問6](../../exercises/data-prep.md#q6) | 1.2.2 | 学習のノートブックと推論のコードで計算方法が別々になり、本番の精度が検証より大きく落ちました。この問… |
| [data-prep 問7](../../exercises/data-prep.md#q7) | 1.1.9 | フィーチャーグループを作成します。スキーマの中で定義が必須の特徴はどれですか。（2つ選択） |
| [data-prep 問8](../../exercises/data-prep.md#q8) | 1.1.9 | Kinesis のイベントを Lambda で集計し、結果を 1 件ずつ Feature Store… |
| [data-prep 問9](../../exercises/data-prep.md#q9) | 1.1.9 | 数億件の過去データを、まとめてフィーチャーグループへ取り込みます。最も適した方法はどれですか。 |
| [data-prep 問10](../../exercises/data-prep.md#q10) | 1.2.4 | 年収の列は右に長い分布で、10 万から 1 億まで広がります。線形モデルの前に行う変換として最も適切… |
| [data-prep 問11](../../exercises/data-prep.md#q11) | 1.2.4 | 平均 50、標準偏差 10 の列を標準化します。値が 70 のとき、結果はどれですか。 |
| [data-prep 問12](../../exercises/data-prep.md#q12) | 1.2.4 | 全データの平均と標準偏差で標準化したあとに学習用とテスト用へ分割した結果、テストの指標が本番よりよく… |
| [data-prep 問13](../../exercises/data-prep.md#q13) | 1.3.7 | 年収の列に欠損があり、極端に高い外れ値も少数あります。分布を大きく歪めずに補完する方法はどれですか。 |
| [data-prep 問14](../../exercises/data-prep.md#q14) | 1.3.7 | 2 つの顧客データベースを統合します。共通の ID がなく、氏名や住所の表記も少しずつ違います。同じ… |
| [data-prep 問15](../../exercises/data-prep.md#q15) | 1.3.7 | ラベルのないセンサーデータの中から、異常なレコードを見つけて前処理で確認したいです。SageMake… |

<!-- questions:end -->

# 分野3: データ品質とデータ準備

データの準備、可視化、検証、品質ルール、一貫性、サンプリング、偏りを問います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [3.1.6](../../domain3.md#skill-3-1-6) | 変換の前のデータの準備 |
| [3.2.1](../../domain3.md#skill-3-2-1) | データの可視化 |
| [3.2.2](../../domain3.md#skill-3-2-2) | データの検証とクリーニング |
| [3.4.1](../../domain3.md#skill-3-4-1) | 処理中のデータ品質チェック |
| [3.4.2](../../domain3.md#skill-3-4-2) | データ品質ルールの定義 |
| [3.4.3](../../domain3.md#skill-3-4-3) | データの一貫性の調査 |
| [3.4.4](../../domain3.md#skill-3-4-4) | データのサンプリング手法 |
| [3.4.5](../../domain3.md#skill-3-4-5) | データの偏りへの対応 |

## 学習の順番 {#study-order}

1. [DataBrew](../../../../services/data-engineering.md#databrew): プロジェクト、レシピ、プロファイルを区別します。
2. [Data Quality](../../../../services/data-engineering.md#glue-data-quality): 入口と DQDL を覚えます。
3. [Quick Sight](../../../../services/data-engineering.md#quick-sight): SPICE と直接クエリを比べます。
4. [Data Wrangler](../../../../services/sagemaker.md#data-wrangler): 現在の形を確認します。
5. [分散スタイル](../../../../services/data-engineering.md#redshift-distribution): `skew_rows` と対処を確認します。
6. [読み取りの整合性](../../../../services/dynamodb.md#read-consistency): GSI の制限を押さえます。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| DataBrew のプロジェクトのサンプル | `FIRST_N`、`LAST_N`、`RANDOM` | 画面の確認用 |
| プロファイルの既定のサンプル | `CUSTOM_ROWS` の 20,000 行 | 全件は `FULL_DATASET` |
| `TABLESAMPLE BERNOULLI` | 全ブロックをスキャン | 行単位 |
| `TABLESAMPLE SYSTEM` | セグメント単位 | 独立性は保証されない |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| ロードの前に不良を隔離する | ETL ジョブの Data Quality |
| アナリストが画面でルールを作る | DataBrew のルールセット |
| 欠損の数を調べる | `COUNT(*) - COUNT(col)` |
| 少数のグループを抜かさない | 層化サンプリング |
| 一部のタスクだけ遅い | データの偏り。ソルティングやブロードキャスト |

## 引っかかりやすい点 {#traps}

- ワーカーを増やしても、同じキーは同じタスクに集まります。
- 複合型の列には DataBrew の列レベルのルールを定義できません。
- SPICE は容量が足りないと取り込みが失敗します。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [data-quality 問1](../../exercises/data-quality.md#q1) | 3.1.6 | アナリストが、列の分割や欠損の補完を画面で試し、確定した手順を全データへ適用します。DataBrew… |
| [data-quality 問2](../../exercises/data-quality.md#q2) | 3.1.6 | データの準備から分析、ML までを、チームで 1 つのプロジェクトの中で進めます。何を選びますか。 |
| [data-quality 問3](../../exercises/data-quality.md#q3) | 3.1.6 | データ準備の担当とツールの組み合わせで正しいものはどれですか。 |
| [data-quality 問4](../../exercises/data-quality.md#q4) | 3.2.1 | Quick Sight のダッシュボードを速くし、Athena のスキャン費用を抑えます。データは日… |
| [data-quality 問5](../../exercises/data-quality.md#q5) | 3.2.1 | 見るものとツールの組み合わせで正しいものはどれですか。（2つ選択） |
| [data-quality 問6](../../exercises/data-quality.md#q6) | 3.2.1 | Quick Sight で更新したのにダッシュボードが古いままです。取り込みの失敗も出ています。何を… |
| [data-quality 問7](../../exercises/data-quality.md#q7) | 3.2.2 | S3 のテーブルで、email 列の欠損の数を SQL で調べます。正しいものはどれですか。 |
| [data-quality 問8](../../exercises/data-quality.md#q8) | 3.2.2 | ML の前処理のデータを、画面で検証して整え、自然言語でも変換します。どれを使いますか。 |
| [data-quality 問9](../../exercises/data-quality.md#q9) | 3.2.2 | 届いたファイルの列数が正しいかを、到着時に検証して、不正なら別のプレフィックスへ移します。処理は数秒… |
| [data-quality 問10](../../exercises/data-quality.md#q10) | 3.4.1 | Glue の ETL の途中で不良レコードを隔離し、正常なデータだけを Redshift へ書き込み… |
| [data-quality 問11](../../exercises/data-quality.md#q11) | 3.4.1 | 注文 ID が空でないことを確かめる DQDL のルールはどれですか。 |
| [data-quality 問12](../../exercises/data-quality.md#q12) | 3.4.1 | Data Quality の 2 つの入口の説明で正しいものはどれですか。（2つ選択） |
| [data-quality 問13](../../exercises/data-quality.md#q13) | 3.4.2 | アナリストが画面で「列 APY は 0〜100」「欠損は 5% 以下」のルールを作り、検証レポートを… |
| [data-quality 問14](../../exercises/data-quality.md#q14) | 3.4.2 | ステータスの列の値を許可された値に限定するルールはどれですか。 |
| [data-quality 問15](../../exercises/data-quality.md#q15) | 3.4.2 | DataBrew でルールを定義できない列はどれですか。 |
| [data-quality 問16](../../exercises/data-quality.md#q16) | 3.4.3 | データの分布の変化を週次で確かめ、列の間の関係も確認します。どの機能ですか。 |
| [data-quality 問17](../../exercises/data-quality.md#q17) | 3.4.3 | ETL の後に、ソースの S3 とターゲットの Redshift の件数が一致するかを確かめ、長期の… |
| [data-quality 問18](../../exercises/data-quality.md#q18) | 3.4.3 | DynamoDB の GSI を読むと、書いた直後の値が古いことがあります。正しい説明はどれですか。 |
| [data-quality 問19](../../exercises/data-quality.md#q19) | 3.4.4 | Athena の TABLESAMPLE で、行単位の独立した抽出を行います。全ブロックのスキャンは… |
| [data-quality 問20](../../exercises/data-quality.md#q20) | 3.4.4 | DataBrew のプロファイルでは問題なかった列に、本番で 0.1% の不正な値が見つかりました。… |
| [data-quality 問21](../../exercises/data-quality.md#q21) | 3.4.4 | 少数の地域のデータが抜けないよう、地域ごとの比率を保ってサンプリングします。どの手法ですか。 |
| [data-quality 問22](../../exercises/data-quality.md#q22) | 3.4.5 | Redshift のテーブルの行の偏りを調べます。DISTSTYLE KEY の列の値が偏っています… |
| [data-quality 問23](../../exercises/data-quality.md#q23) | 3.4.5 | Spark の結合で 1 つのタスクだけ長く、そのエグゼキューターが OOM になります。ワーカーを… |
| [data-quality 問24](../../exercises/data-quality.md#q24) | 3.4.5 | データの偏りと対処の組み合わせで正しいものはどれですか。 |

<!-- questions:end -->

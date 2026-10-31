# 分野2: モデルの選択と基本の調整

業務の要件を問題の種類に置き換えて、アルゴリズムを選びます。過学習と過少適合の症状から対策を答えます。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [2.1.3](../../domain2.md#skill-2-1-3) | モデル、アルゴリズム、テンプレートの比較 |
| [2.2.1](../../domain2.md#skill-2-2-1) | 組み込みアルゴリズムと一般的なライブラリ |
| [2.2.5](../../domain2.md#skill-2-2-5) | 過学習、過少適合、破滅的忘却の防止 |
| [2.2.6](../../domain2.md#skill-2-2-6) | 複数モデルの組み合わせ |
| [2.2.7](../../domain2.md#skill-2-2-7) | 基本のハイパーパラメータの調整 |

## 学習の順番 {#study-order}

1. [組み込みアルゴリズム](../../../../services/sagemaker.md#built-in-algorithms): 用途と入力形式を対応させます。
2. [説明可能性](../../../../services/ai-fundamentals.md#explainability): 説明が必須の場面の選択を確認します。
3. [過学習](../../../../services/ai-fundamentals.md#overfitting)と[正則化](../../../../services/ai-fundamentals.md#regularization): 症状と対策、エポックとバッチサイズの関係を覚えます。
4. [アンサンブル](../../../../services/ai-fundamentals.md#ensembles): バギング、ブースティング、スタッキングを区別します。

## 覚える値 {#values}

| 項目 | 例 | 判断のポイント |
|---|---|---|
| 過少適合 | 学習 65%、検証 64% | 複雑にする、正則化を弱める |
| 過学習 | 学習 99%、検証 70% | 正則化、早期停止、データの追加 |
| ステップ数 | 10,000 件、バッチ 100、10 エポックで 1,000 | 1 エポックは 100 ステップ |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 表データの分類の第一候補 | XGBoost |
| 似た系列の需要予測 | DeepAR |
| 高次元の疎データ | Factorization Machines |
| ラベルなしの異常検知 | Random Cut Forest |
| 過学習している | バギング |
| 過少適合している | ブースティング |
| 損失が発散する | 学習率を下げる |
| 新しいデータの追加学習で以前を忘れる | 新旧のデータを混ぜる |

## 引っかかりやすい点 {#traps}

- Linear Learner は CSV と recordIO-protobuf を受け付けます。
- K-Means は CPU が推奨です。
- L1 は不要な重みを 0 にし、L2 は重みを全体に小さくします。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [ml-modeling 問1](../../exercises/ml-modeling.md#q1) | 2.1.3 | 数千の店舗の日次の売上を予測します。店舗ごとの系列は似ていて、全体をまとめて学習したいです。どの組み… |
| [ml-modeling 問2](../../exercises/ml-modeling.md#q2) | 2.1.3 | 広告のクリックを予測します。ユーザー ID と広告 ID の組み合わせによる、高次元で疎なデータです… |
| [ml-modeling 問3](../../exercises/ml-modeling.md#q3) | 2.1.3 | 融資の審査で、規制により否決の理由の説明が必須です。深層学習モデルの精度は 1 ポイントだけ高い状況… |
| [ml-modeling 問4](../../exercises/ml-modeling.md#q4) | 2.2.1 | Linear Learner に学習データを渡します。受け付ける入力形式の組み合わせはどれですか。 |
| [ml-modeling 問5](../../exercises/ml-modeling.md#q5) | 2.2.1 | K-Means の学習ジョブのインスタンスを選びます。コストを無駄にしない選択はどれですか。 |
| [ml-modeling 問6](../../exercises/ml-modeling.md#q6) | 2.2.1 | scikit-learn の独自の前処理とモデルのコードがあります。独自のコンテナは作りたくありませ… |
| [ml-modeling 問7](../../exercises/ml-modeling.md#q7) | 2.2.5 | 学習の精度が 99%、検証の精度が 70% です。正しい診断と対策の組み合わせはどれですか。 |
| [ml-modeling 問8](../../exercises/ml-modeling.md#q8) | 2.2.5 | 学習の精度が 65%、検証の精度が 64% です。対策として適切なものはどれですか。（2つ選択） |
| [ml-modeling 問9](../../exercises/ml-modeling.md#q9) | 2.2.5 | 新しい商品のデータだけで追加学習すると、以前の商品の分類が大きく悪化しました。現象と対策の組み合わせ… |
| [ml-modeling 問10](../../exercises/ml-modeling.md#q10) | 2.2.6 | 1 つの決定木が過学習しています。データを復元抽出で分け、複数の木を並列に学習して多数決をとります。… |
| [ml-modeling 問11](../../exercises/ml-modeling.md#q11) | 2.2.6 | 単純なモデルが過少適合しています。前のモデルの誤りを次のモデルが補う方法を使います。どれを選びますか… |
| [ml-modeling 問12](../../exercises/ml-modeling.md#q12) | 2.2.6 | 複数の種類のモデルの出力を別のモデルに入力して予測します。AutoGluon-Tabular も使う… |
| [ml-modeling 問13](../../exercises/ml-modeling.md#q13) | 2.2.7 | データ 10,000 件、バッチサイズ 100 で、10 エポック学習します。全体のステップ数はどれ… |
| [ml-modeling 問14](../../exercises/ml-modeling.md#q14) | 2.2.7 | 学習を始めるとすぐに損失が上下に大きく振れ、下がらなくなりました。データは正しいです。まず調整するハ… |
| [ml-modeling 問15](../../exercises/ml-modeling.md#q15) | 2.2.7 | GPU のメモリ不足で学習がすぐ失敗します。モデルは変えません。最初に調整する項目と方向はどれですか… |

<!-- questions:end -->

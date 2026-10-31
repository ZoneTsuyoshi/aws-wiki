# 分野4: モデルの監視

本番のモデルと FM の性能を監視します。正解が遅れて届く業務の考え方と、A/B テストの設定を問います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [4.1.1](../../domain4.md#skill-4-1-1) | 本番のモデルの性能の監視 |
| [4.1.3](../../domain4.md#skill-4-1-3) | データ分布の変化の検出 |
| [4.1.4](../../domain4.md#skill-4-1-4) | A/B テスト |

## 学習の順番 {#study-order}

1. [生成 AI オブザーバビリティ](../../../../services/genai-apps.md#genai-observability)と[見るべき指標](../../../../services/genai-apps.md#genai-metrics): FM のアプリの監視を確認します。
2. [Model Monitor](../../../../services/sagemaker.md#model-monitor)と[ドリフトの種類](../../../../services/sagemaker.md#drift): 監視の種類と必要なものを覚えます。
3. [サーバーレス](../../../../services/sagemaker.md#serverless): データキャプチャに対応しないことを押さえます。
4. [デプロイとテストの戦略](../../../../services/sagemaker.md#deployment-strategies): A/B の設定を確認します。

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| アプリ全体をプロンプト単位で追う | CloudWatch の生成 AI オブザーバビリティ |
| 品質をダッシュボードに出す | 評価の結果をカスタムメトリクスで送る |
| 正解がすぐ届かない | まず入力の分布を見る |
| 精度を見る | 届いた正解と予測を結合する |
| 配分を変える | `UpdateEndpointWeightsAndCapacities` |
| 特定のバリアントを呼ぶ | `TargetVariant` |

## 引っかかりやすい点 {#traps}

- サーバーレス推論はデータキャプチャに対応しません。
- コンセプトドリフトは入力の分布の監視では検出できません。
- A/B では遅延だけでなく、コンバージョン率などの業務指標を比べます。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [model-monitoring 問7](../../exercises/model-monitoring.md#q7) | 4.1.1 | Bedrock のアプリ全体を、モデルの呼び出し、ナレッジベース、ガードレール、ツールまで通して監視… |
| [model-monitoring 問8](../../exercises/model-monitoring.md#q8) | 4.1.1 | FM の回答の品質を本番のダッシュボードに出します。AWS/Bedrock の運用の指標に品質の指標… |
| [model-monitoring 問9](../../exercises/model-monitoring.md#q9) | 4.1.1, 4.1.3 | 不正検知の本番のモデルで、精度を監視します。正解は数週間後に届きます。監視の組み合わせとして適切なも… |
| [model-monitoring 問10](../../exercises/model-monitoring.md#q10) | 4.1.3 | データキャプチャで、本番のリクエストの 20% を S3 に保存します。設定する項目はどれですか。 |
| [model-monitoring 問11](../../exercises/model-monitoring.md#q11) | 4.1.3 | サーバーレス推論のエンドポイントでドリフトを監視するため、データキャプチャを有効にしようとしています… |
| [model-monitoring 問12](../../exercises/model-monitoring.md#q12) | 4.1.3 | 既に Model Monitor を使っています。特徴量の重要度の順位が学習時から変わったかを監視し… |
| [model-monitoring 問13](../../exercises/model-monitoring.md#q13) | 4.1.4 | エンドポイントに 2 つの本番バリアントがあります。作り直さずに、新しいモデルへの配分を 10% か… |
| [model-monitoring 問14](../../exercises/model-monitoring.md#q14) | 4.1.4 | A/B テストの一部の呼び出しで、新しいモデルを指定して検証します。呼び出しの設定はどれですか。 |
| [model-monitoring 問15](../../exercises/model-monitoring.md#q15) | 4.1.4 | 新しいレコメンドのモデルが遅延では勝ちました。導入の判断の進め方として適切なものはどれですか。 |

<!-- questions:end -->

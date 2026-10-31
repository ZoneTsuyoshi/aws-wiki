# 分野1: ML ライフサイクルと MLOps

開発の段階の順番と、段階ごとのサービス、モデルの指標とビジネス指標の違いを問います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [1.3.1](../../domain1.md#obj-1-3-1) | AI/ML パイプラインの構成要素 |
| [1.3.4](../../domain1.md#obj-1-3-4) | パイプラインの各段階の AWS サービス |
| [1.3.5](../../domain1.md#obj-1-3-5) | MLOps の基本概念 |
| [1.3.6](../../domain1.md#obj-1-3-6) | モデルの性能指標とビジネス指標 |

## 学習の順番 {#study-order}

1. [ML ライフサイクルと MLOps](../../../../services/ai-fundamentals.md#ml-lifecycle): 段階の順番とデータの分割を覚えます。
2. [特徴量エンジニアリング](../../../../services/ai-fundamentals.md#feature-engineering): 特徴量エンジニアリングが何をするかだけ押さえます。
3. [SageMaker Pipelines](../../../../services/sagemaker.md#pipelines)と[Model Registry](../../../../services/sagemaker.md#model-registry): 自動化とモデルの承認の役割を確認します。
4. [MLflow on SageMaker AI](../../../../services/sagemaker.md#mlflow)と[ドリフトの種類](../../../../services/sagemaker.md#drift): 実験の記録と、データドリフトとコンセプトドリフトの違いを押さえます。
5. [分類の指標](../../../../services/ai-fundamentals.md#classification-metrics): 適合率と再現率を、損失の種類で使い分けます。
6. [ビジネス指標](../../../../services/ai-fundamentals.md#business-metrics): モデルの指標と事業の成果を区別します。
7. [Amazon Quick](../../../../services/ai.md#quick)と[Kiro](../../../../services/ai.md#kiro): 業務ユーザー向けと開発者向けを区別します。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| 精度 | 全体のうち正解した割合 | クラスが均衡しているとき |
| 適合率 | 陽性と予測したうち本当に陽性の割合 | 誤検知の損失が大きいとき |
| 再現率 | 本当の陽性のうち見つけた割合 | 見逃しの損失が大きいとき |
| F1 スコア | 適合率と再現率の調和平均 | 両方を見たいとき |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 検証用データの役割 | ハイパーパラメータの調整 |
| テスト用データの役割 | 最後の評価 |
| 手作業の手順を毎回同じように実行する | SageMaker Pipelines |
| パラメータと結果を記録する | MLflow |
| モデルの版と承認を管理する | Model Registry |
| 不正の手口が変わって精度が落ちる | コンセプトドリフト |
| 利用者の年齢層が変わる | データドリフト |
| 病気の見逃しを減らす | 再現率 |
| 事業として続ける価値があるか | ROI、ユーザーあたりコスト |

## 引っかかりやすい点 {#traps}

- 陽性がごく少ないと、全部を陰性と答えても精度は高くなります。
- Model Monitor、Ground Truth、Clarify、Debugger は新規顧客を受け付けていません。役割は押さえますが、新規の設計では公式の案内を確認します。
- モデルの指標がよくても、事業の成果になるとは限りません。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [ml-lifecycle 問1](../../exercises/ml-lifecycle.md#q1) | 1.3.1 | ML プロジェクトの進め方として正しい順番はどれですか。 |
| [ml-lifecycle 問2](../../exercises/ml-lifecycle.md#q2) | 1.3.1 | データを学習用、検証用、テスト用に分けます。テスト用データの役割はどれですか。 |
| [ml-lifecycle 問3](../../exercises/ml-lifecycle.md#q3) | 1.3.1 | 購入日時の列から「曜日」と「時間帯」の列を新しく作って、モデルの入力にしました。この作業はパイプライ… |
| [ml-lifecycle 問4](../../exercises/ml-lifecycle.md#q4) | 1.3.1 | 評価の結果、モデルが基準を満たしませんでした。次の行動として適切なものはどれですか。 |
| [ml-lifecycle 問5](../../exercises/ml-lifecycle.md#q5) | 1.3.4 | 業務部門の担当者が、コードを書かずに社内データへの質問、分析、定型作業の自動化を行いたいと考えていま… |
| [ml-lifecycle 問6](../../exercises/ml-lifecycle.md#q6) | 1.3.4 | 開発者が、要件、設計、タスクを先に文書にしてから AI に実装させる流れで開発したいと考えています。… |
| [ml-lifecycle 問7](../../exercises/ml-lifecycle.md#q7) | 1.3.4 | パイプラインの段階と AWS のサービスの組み合わせとして正しいものを選んでください。（2つ選択） |
| [ml-lifecycle 問8](../../exercises/ml-lifecycle.md#q8) | 1.3.4 | 複数の FM を API で使い、インスタンスを管理せずに生成 AI の機能を作りたいと考えています… |
| [ml-lifecycle 問9](../../exercises/ml-lifecycle.md#q9) | 1.3.5 | データの準備、学習、評価、登録という手作業の手順を、毎回同じように実行できるようにしたいと考えていま… |
| [ml-lifecycle 問10](../../exercises/ml-lifecycle.md#q10) | 1.3.5 | 実験ごとのパラメータと結果を記録し、同じ結果を再現できるようにしたいと考えています。MLOps のど… |
| [ml-lifecycle 問11](../../exercises/ml-lifecycle.md#q11) | 1.3.5 | 不正検知のモデルの精度が、不正の手口が変わったことで落ちました。入力の分布は大きく変わっていません。… |
| [ml-lifecycle 問12](../../exercises/ml-lifecycle.md#q12) | 1.3.5 | モデルのバージョンを管理し、承認されたものだけを本番に出したいと考えています。適切な機能はどれですか… |
| [ml-lifecycle 問13](../../exercises/ml-lifecycle.md#q13) | 1.3.5 | MLOps の考え方として正しいものを選んでください。（2つ選択） |
| [ml-lifecycle 問14](../../exercises/ml-lifecycle.md#q14) | 1.3.6 | がんの検診を補助するモデルを作ります。陽性の見逃しを最も減らしたいとき、重視する指標はどれですか。 |
| [ml-lifecycle 問15](../../exercises/ml-lifecycle.md#q15) | 1.3.6 | 取引の 0.5% だけが不正のデータで、モデルの精度は 99.5% でした。このモデルの評価として正… |
| [ml-lifecycle 問16](../../exercises/ml-lifecycle.md#q16) | 1.3.6 | 重要なメールを誤って迷惑メールに振り分けると、大きな損失が出ます。この誤検知を減らしたいときに重視す… |
| [ml-lifecycle 問17](../../exercises/ml-lifecycle.md#q17) | 1.3.6 | モデルの F1 スコアは高いのですが、経営層は事業として続ける価値があるかを知りたがっています。適切… |

<!-- questions:end -->

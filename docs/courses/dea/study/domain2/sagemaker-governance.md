# 分野2: ビジネスカタログとリネージ

ビジネスカタログの作成と管理、データリネージを問います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [2.2.6](../../domain2.md#skill-2-2-6) | ビジネスカタログの作成と管理 |
| [2.4.4](../../domain2.md#skill-2-4-4) | データリネージの確立 |

## 学習の順番 {#study-order}

1. [DataZone と Unified Studio](../../../../services/data-engineering.md#datazone-unified-studio): 公開、申請、承認の流れを覚えます。
2. [SageMaker Pipelines](../../../../services/sagemaker.md#pipelines): ML のワークフローの追跡との関係を確認します。

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| データを検索し申請する | SageMaker Catalog |
| 説明の項目を揃える | 用語集とメタデータフォーム |
| パイプライン全体のデータの由来 | SageMaker Catalog のリネージ |
| モデルと学習データの関係 | ML Lineage Tracking |

## 引っかかりやすい点 {#traps}

- Glue Data Catalog はエンジン向けで、申請の流れはありません。
- リネージは OpenLineage 互換で、カタログの外の処理も API で記録できます。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [sagemaker-governance 問1](../../exercises/sagemaker-governance.md#q1) | 2.2.6 | 社内のアナリストが、データを意味で検索し、利用を申請し、承認を受けて使えるようにします。どのサービス… |
| [sagemaker-governance 問2](../../exercises/sagemaker-governance.md#q2) | 2.2.6 | SageMaker Catalog でデータを使えるようになるまでの順序はどれですか。 |
| [sagemaker-governance 問3](../../exercises/sagemaker-governance.md#q3) | 2.2.6 | 部門ごとに説明の項目がばらばらです。項目と用語を揃えます。SageMaker Catalog のどの… |
| [sagemaker-governance 問4](../../exercises/sagemaker-governance.md#q4) | 2.4.4 | データの品質の問題が見つかりました。どのダッシュボードが影響を受けるか、パイプライン全体でたどります… |
| [sagemaker-governance 問5](../../exercises/sagemaker-governance.md#q5) | 2.4.4 | 本番のモデルがどのデータセットと学習ジョブから作られたかを、監査で示します。何を使いますか。 |
| [sagemaker-governance 問6](../../exercises/sagemaker-governance.md#q6) | 2.4.4 | データリネージの目的として正しいものはどれですか。（2つ選択） |

<!-- questions:end -->

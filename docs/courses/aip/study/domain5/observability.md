# 分野5: 関係者への報告

相手ごとに指標を変えて、報告を自動化します。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [5.1.8](../../domain5.md#skill-5-1-8) | 関係者への報告 |

## 学習の順番 {#study-order}

1. [KPI と ROI](../../../../services/ai-fundamentals.md#kpi-roi): 経営層に見せる指標を確認します。
2. [ダッシュボード](../../../../services/observability.md#dashboards)と [Quick Sight](../../../../services/data-engineering.md#quick-sight): 手段の違いを押さえます。

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 経営層 | 解決率、削減した工数 |
| 運用担当 | 遅延、エラー |
| 定期の報告 | EventBridge、Lambda、SNS |
| モデルの比較 | S3 の評価の結果を可視化 |

## 引っかかりやすい点 {#traps}

- 技術の指標をそのまま経営層に見せても判断につながりません。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [observability 問17](../../exercises/observability.md#q17) | 5.1.8 | 生成 AI のチャットの効果を月次で報告します。経営層向けのレポートと運用担当向けのダッシュボードで… |
| [observability 問18](../../exercises/observability.md#q18) | 5.1.8 | 3 つのモデルの評価ジョブの結果を、品質、遅延、費用で並べて、関係者が見られるようにします。結果は … |
| [observability 問19](../../exercises/observability.md#q19) | 5.1.8 | 毎週月曜に、先週の評価のスコアと解決率を集計して関係者にメールで配信します。手作業の報告をなくしたい… |

<!-- questions:end -->

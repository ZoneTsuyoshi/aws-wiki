# 分野3: ファインチューニングの自動化

ジョブの開始から評価、配置、切り替えまでを自動化します。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [3.3.10](../../domain3.md#skill-3-3-10) | ファインチューニングしたモデルの自動化 |

## 学習の順番 {#study-order}

1. [カスタムモデルの実行](../../../../services/genai-apps.md#custom-model-deploy): 配置の方法を確認します。
2. [動的なモデル切り替え](../../../../services/genai-apps.md#dynamic-model-selection): AppConfig での切り替えを押さえます。
3. [モデルのライフサイクル](../../../../services/genai-apps.md#model-lifecycle): Legacy の制約を覚えます。

## こう問われたらこう考える {#decisions}

| 段階 | 実装 |
|---|---|
| 調整 | データを検証して、カスタマイズのジョブを開始する |
| 待機と順序 | Step Functions |
| 評価 | Bedrock Evaluations で基準と比べる |
| 配置 | Provisioned Throughput かカスタムモデルのデプロイ |
| 切り替え | AppConfig |

## 引っかかりやすい点 {#traps}

- Legacy になった基盤モデルでは、新しいファインチューニングと Provisioned Throughput を作れません。既存のものは条件付きで使い続けられます。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [fm-customization 問8](../../exercises/fm-customization.md#q8) | 3.3.10 | ファインチューニングの工程を自動化します。カスタマイズのジョブは長時間かかります。ジョブの完了を待っ… |
| [fm-customization 問9](../../exercises/fm-customization.md#q9) | 3.3.10 | 調整したモデルをアプリに切り替えるとき、コードをデプロイしたくありません。使うモデルの設定を外に持ち… |
| [fm-customization 問10](../../exercises/fm-customization.md#q10) | 3.3.10 | ファインチューニングの元の基盤モデルが Legacy になりました。正しい説明はどれですか。 |

<!-- questions:end -->

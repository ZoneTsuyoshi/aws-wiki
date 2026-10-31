# 分野1: FM の選定と耐障害

要件を制約に翻訳し、PoC で確かめてモデルを選びます。切り替えと障害の備えも、最初の設計で問われます。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [1.1.1](../../domain1.md#skill-1-1-1) | 業務要件と技術的制約に合う設計 |
| [1.1.2](../../domain1.md#skill-1-1-2) | PoC で実現性と価値を検証 |
| [1.1.3](../../domain1.md#skill-1-1-3) | 標準化された部品 |
| [1.2.1](../../domain1.md#skill-1-2-1) | FM の評価と選定 |
| [1.2.2](../../domain1.md#skill-1-2-2) | コードを変えずにモデルを切り替える |
| [1.2.3](../../domain1.md#skill-1-2-3) | 障害時も動き続ける設計 |

## 学習の順番 {#study-order}

1. [選定の観点](../../../../services/genai-apps.md#fm-criteria): モダリティ、言語、機能、ライフサイクルで先に候補を落とす順序を覚えます。
2. [Nova と Titan](../../../../services/genai-apps.md#nova-titan)と[モデルのライフサイクル](../../../../services/genai-apps.md#model-lifecycle): モダリティの違いと、Legacy と EOL の動作を確認します。
3. [Bedrock Evaluations](../../../../services/genai-apps.md#bedrock-evaluations)と [KPI と ROI](../../../../services/ai-fundamentals.md#kpi-roi): PoC で品質と事業価値を測る方法を押さえます。
4. [動的なモデル切り替え](../../../../services/genai-apps.md#dynamic-model-selection)と [AppConfig](../../../../services/secrets.md#appconfig): デプロイなしで切り替え、自動で戻す構成を理解します。
5. [クロスリージョン推論](../../../../services/ai.md#model-identifiers): 地理的とグローバルの違い、SCP と IAM の注意点を覚えます。
6. [耐障害の設計](../../../../services/genai-apps.md#fm-resilience)と[サーキットブレーカー](../../../../services/sdk-resilience.md#circuit-breaker): 障害の範囲ごとの対策を表で整理します。
7. [Well-Architected Tool](../../../../services/cloud-foundations.md#wa-tool)と [Service Catalog](../../../../services/governance.md#service-catalog): 標準化の手段の役割の違いを確認します。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| Legacy 期間（2026-09-07 以降のモデル） | 6 か月または 45 日 | EOL の日付を追って移行する |
| Titan Text Embeddings V2 の次元 | 1,024（既定）、512、256 | マルチモーダルではない |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| データを国外に出せず、容量も要る | 地理的な推論プロファイル。`global` は不可 |
| 情報が頻繁に変わる | RAG。ファインチューニングは再学習が要る |
| 提供者をまたいで切り替え、自動で戻す | AppConfig と `Converse`。Intelligent Prompt Routing は同じ系統だけ |
| 承認済みの構成を起動だけさせる | Service Catalog |
| 設計レビューの観点を揃える | Well-Architected Tool の Generative AI Lens |
| 障害中に無駄な呼び出しを避ける | サーキットブレーカー |
| リージョン全体の障害に備える | S3 の複製、別リージョンのナレッジベース、Route 53 のフェイルオーバー |

## 引っかかりやすい点 {#traps}

- Lens はレビューの枠組みで、実行時に何も強制しません。
- EOL に自動移行はなく、リクエストが失敗します。
- 推論プロファイルは Provisioned Throughput に対応しません。
- クロスリージョン推論が振り分けるのは推論だけで、文書やベクトルストアは複製されません。
- PoC の合格基準は結果を見る前に決めます。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [fm-selection 問1](../../exercises/fm-selection.md#q1) | 1.1.1 | ある保険会社は、社内規定に答えるアプリを作ります。規定は月に数回改定され、改定の当日から新しい内容で… |
| [fm-selection 問2](../../exercises/fm-selection.md#q2) | 1.1.1 | ある物流会社は、配送伝票の要約機能を基幹システムに追加します。処理は平日の夕方に数万件が集中し、利用… |
| [fm-selection 問3](../../exercises/fm-selection.md#q3) | 1.1.1 | ある製造業の研究部門は、外部で学習した独自の重みを持つ特殊なアーキテクチャのモデルを使いたいと考えて… |
| [fm-selection 問4](../../exercises/fm-selection.md#q4) | 1.1.2 | ある小売企業は、商品説明文の生成に使うモデルを 3 候補から選ぶ PoC を始めます。経営層は、4 … |
| [fm-selection 問5](../../exercises/fm-selection.md#q5) | 1.1.2 | 問い合わせ要約の PoC で、候補モデル X は品質スコアが基準を満たしました。経営層は「全社展開で… |
| [fm-selection 問6](../../exercises/fm-selection.md#q6) | 1.1.2 | チャット機能の PoC の性能を測ります。要件は「質問してから 2 秒以内に表示が始まること」「ピー… |
| [fm-selection 問7](../../exercises/fm-selection.md#q7) | 1.1.3 | ある金融グループでは、20 のチームが生成 AI のアプリを作っています。設計レビューの観点がチーム… |
| [fm-selection 問8](../../exercises/fm-selection.md#q8) | 1.1.3 | ある企業の基盤チームは、承認済みの RAG 構成（Knowledge Bases、ガードレール、ログ… |
| [fm-selection 問9](../../exercises/fm-selection.md#q9) | 1.1.3 | 複数のチームが同じ実装をそれぞれ書いており、認証、呼び出しの記録、モデル選択の実装がばらばらです。ア… |
| [fm-selection 問10](../../exercises/fm-selection.md#q10) | 1.2.1 | ある企業は、日本語の契約書と図表を読み、5 年間運用するシステムのモデルを選びます。契約書は長く、ツ… |
| [fm-selection 問11](../../exercises/fm-selection.md#q11) | 1.2.1 | 動画、音声、画像、文書を同じ検索基盤で探せるようにします。アップロードされた素材を埋め込みにして、自… |
| [fm-selection 問12](../../exercises/fm-selection.md#q12) | 1.2.1 | 本番で使っている基盤モデルが Legacy になり、EOL の日付が通知されました。このモデルからフ… |
| [fm-selection 問13](../../exercises/fm-selection.md#q13) | 1.2.2 | あるチームは、複数の提供者のモデルを本番で切り替えながら評価します。切り替えは数分で行い、エラーが増… |
| [fm-selection 問14](../../exercises/fm-selection.md#q14) | 1.2.2 | AppConfig でモデル ID を配布しています。新しいモデルへの切り替えで品質が落ちたときに自… |
| [fm-selection 問15](../../exercises/fm-selection.md#q15) | 1.2.2 | 既存のアプリは Lambda から InvokeModel で特定の提供者のモデルを呼び、本文を提供… |
| [fm-selection 問16](../../exercises/fm-selection.md#q16) | 1.2.3 | EU の顧客データを扱う RAG アプリで、ピーク時に特定リージョンの容量不足で ServiceUn… |
| [fm-selection 問17](../../exercises/fm-selection.md#q17) | 1.2.3 | Step Functions で FM を呼ぶ処理があります。第一候補のモデルが長時間の障害を起こす… |
| [fm-selection 問18](../../exercises/fm-selection.md#q18) | 1.2.3 | 東京リージョンで動く Knowledge Bases の RAG アプリに、大阪リージョンへの DR… |
| [fm-selection 問19](../../exercises/fm-selection.md#q19) | 1.2.3 | 製品 FAQ のチャットで、第一候補と代替のどちらの FM も失敗する全面障害を想定します。FAQ … |

<!-- questions:end -->

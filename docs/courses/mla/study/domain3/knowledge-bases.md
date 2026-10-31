# 分野3: Knowledge Bases

ナレッジベースの作成と同期、検索の設定、検索パイプラインの実装を問います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [3.1.8](../../domain3.md#skill-3-1-8) | RAG システムの設定 |
| [3.2.7](../../domain3.md#skill-3-2-7) | Knowledge Bases の作成と管理 |
| [3.2.8](../../domain3.md#skill-3-2-8) | 検索パイプラインの実装 |
| [3.3.11](../../domain3.md#skill-3-3-11) | RAG の更新とナレッジベースの更新サイクル |

## 学習の順番 {#study-order}

1. [Managed と Customer-managed](../../../../services/genai-apps.md#managed-kb): データソースと解析の違いを確認します。
2. [Knowledge Bases のパラメータ](../../../../services/ai.md#kb-params): 検索の設定の値を覚えます。
3. [検索の改善](../../../../services/genai-apps.md#retrieval-optimization): 手法と設定を対応させます。
4. [Knowledge Bases を呼ぶ](../../../../services/ai.md#knowledge-bases)と [ApplyGuardrail](../../../../services/ai.md#apply-guardrail): パイプラインの部品を押さえます。
5. [同期と鮮度](../../../../services/genai-apps.md#kb-sync)と[キャッシュの種類](../../../../services/genai-apps.md#caching): 更新の方法とキャッシュを確認します。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| `numberOfResults` | 1〜100、既定 5 | 最大数。少なく返ることがある |
| `overrideSearchType` | `HYBRID`、`SEMANTIC` | 省略時は Bedrock が選ぶ |
| `dataDeletionPolicy` | `RETAIN`、`DELETE` | データソースを消したときの扱い |
| リランク | Amazon Rerank 1.0、Cohere Rerank 3.5 | テキストのみ |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 部署ごとに見える文書を分ける | `filter` |
| 質問から条件を自動で作る | `implicitFilterConfiguration` |
| 言い換えの質問でモデルを呼ばない | セマンティックキャッシュ |
| 文書を更新して数分で反映する | S3 イベント、EventBridge、Lambda、`StartIngestionJob` |
| 確認してから反映する | Step Functions で同期、評価、切り替え |
| 埋め込みモデルを変える | 新しいインデックスとナレッジベースへ全データを同期 |

## 引っかかりやすい点 {#traps}

- ファイルを変えても、同期は自動では動きません。同期は差分だけを処理します。
- 既存のナレッジベースの埋め込みモデルは変更できません。
- S3 Vectors ではハイブリッド検索を使えません。
- Customer-managed で Confluence、SharePoint、Salesforce、Web Crawler のコネクタを新しく作ることは、2026 年 9 月 30 日に終了しました。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [knowledge-bases 問10](../../exercises/knowledge-bases.md#q10) | 3.1.8 | RetrieveAndGenerate で最大 10 件を取得したいです。設定する項目はどれですか。 |
| [knowledge-bases 問11](../../exercises/knowledge-bases.md#q11) | 3.1.8 | S3 Vectors をベクトルストアにしたナレッジベースで、overrideSearchType … |
| [knowledge-bases 問12](../../exercises/knowledge-bases.md#q12) | 3.1.8 | 階層チャンクのナレッジベースで numberOfResults を 10 にしたのに、返るのは 6 … |
| [knowledge-bases 問13](../../exercises/knowledge-bases.md#q13) | 3.2.7 | 2026 年 10 月に新しく作る Customer-managed のナレッジベースで、データソー… |
| [knowledge-bases 問14](../../exercises/knowledge-bases.md#q14) | 3.2.7 | データソースを削除するとき、ベクトルストアのデータも一緒に消します。どの設定ですか。 |
| [knowledge-bases 問15](../../exercises/knowledge-bases.md#q15) | 3.2.7 | 既存のナレッジベースの埋め込みモデルを新しいものへ変更します。適切な手順はどれですか。 |
| [knowledge-bases 問16](../../exercises/knowledge-bases.md#q16) | 3.2.8 | 検索の前に入力を検査し、検索と生成を別に制御します。部署ごとに文書を絞ります。正しい組み合わせはどれ… |
| [knowledge-bases 問17](../../exercises/knowledge-bases.md#q17) | 3.2.8 | 言い換えの質問が多く、同じ回答を何度も生成しています。検索パイプラインに加えて、FM の呼び出しを減… |
| [knowledge-bases 問18](../../exercises/knowledge-bases.md#q18) | 3.2.8 | 質問の文に「2025 年の人事規定」と書かれていたら、自動で年と部署のフィルターを付けて検索します。… |
| [knowledge-bases 問19](../../exercises/knowledge-bases.md#q19) | 3.3.11 | S3 の文書を更新してから、数分以内に回答へ反映させます。同期の仕組みとして適切なものはどれですか。 |
| [knowledge-bases 問20](../../exercises/knowledge-bases.md#q20) | 3.3.11 | 夜間に 1 回同期する運用で、S3 の 100 万件のうち更新は 500 件です。同期ジョブの処理の… |
| [knowledge-bases 問21](../../exercises/knowledge-bases.md#q21) | 3.3.11 | 規定の文書の更新を、品質を確認してから本番の RAG に反映します。評価に合格しなければ切り替えませ… |

<!-- questions:end -->

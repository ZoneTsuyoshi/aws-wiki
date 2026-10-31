# 分野2: Knowledge Bases と RAG

要件に合う RAG のパターンを選び、検索精度を評価します。誤答の原因を切り分ける問題が出ます。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [2.1.5](../../domain2.md#skill-2-1-5) | RAG のアーキテクチャパターン |
| [2.3.10](../../domain2.md#skill-2-3-10) | RAG の監視と検索精度の評価 |

## 学習の順番 {#study-order}

1. [Managed と Customer-managed](../../../../services/genai-apps.md#managed-kb): 違いと API の制約を覚えます。
2. [Knowledge Bases を呼ぶ](../../../../services/ai.md#knowledge-bases): `Retrieve` と `RetrieveAndGenerate` を区別します。
3. [選び方の比較](../../../../services/genai-apps.md#choosing): パターンを要件で選びます。
4. [Bedrock Evaluations](../../../../services/genai-apps.md#bedrock-evaluations): 取得のみと、取得と生成のジョブの指標を確認します。
5. [トラブルシューティング](../../../../services/genai-apps.md#troubleshooting)と[ベクトルストアの運用](../../../../services/genai-apps.md#vector-operations): 切り分けと監視を押さえます。

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 素早く作り、管理を減らす | Managed Knowledge Base |
| データウェアハウスへの質問 | 構造化データストア |
| 関係をたどる質問 | Neptune Analytics の GraphRAG |
| ContextRelevance が低い | チャンク、埋め込み、検索を見直す |
| ContextCoverage が低い | 取得件数、文書の不足 |
| 取得はよいが Faithfulness が低い | プロンプトやモデルを変える |

## 引っかかりやすい点 {#traps}

- Managed では `RetrieveAndGenerate` を使えません。`Retrieve` のあとに生成を呼びます。
- 誤答の調査は、取得、文書、生成の順に分けます。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [knowledge-bases 問4](../../exercises/knowledge-bases.md#q4) | 2.1.5 | 社内ポータルの RAG を早く作り、運用の管理を減らします。組み込みの検索とリランクを使います。生成… |
| [knowledge-bases 問5](../../exercises/knowledge-bases.md#q5) | 2.1.5 | Redshift のデータウェアハウスに、自然文で「先月の地域別の売上は?」と質問させます。文書の検… |
| [knowledge-bases 問6](../../exercises/knowledge-bases.md#q6) | 2.1.5 | 製品、部品、供給元の関係をたどる質問に答える RAG です。「この部品を使う製品の供給元はどこですか… |
| [knowledge-bases 問7](../../exercises/knowledge-bases.md#q7) | 2.3.10 | RAG の取得のみの評価で ContextRelevance は高いのですが、ContextCove… |
| [knowledge-bases 問8](../../exercises/knowledge-bases.md#q8) | 2.3.10 | 検索の精度を、応答の生成と切り離して定期的に評価します。Bedrock Evaluations の設… |
| [knowledge-bases 問9](../../exercises/knowledge-bases.md#q9) | 2.3.10 | RAG の誤答を調査します。切り分けの順序として適切なものはどれですか。 |

<!-- questions:end -->

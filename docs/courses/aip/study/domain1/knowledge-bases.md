# 分野1: Knowledge Bases と検索

取り込み、チャンク、埋め込み、検索の改善までの判断を扱います。症状から手法を選べるようにします。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [1.4.4](../../domain1.md#skill-1-4-4) | データソースとの統合 |
| [1.4.5](../../domain1.md#skill-1-4-5) | ベクトルストアの鮮度を保つ |
| [1.5.1](../../domain1.md#skill-1-5-1) | 文書の分割 |
| [1.5.2](../../domain1.md#skill-1-5-2) | 埋め込みの選択と設定 |
| [1.5.4](../../domain1.md#skill-1-5-4) | 関連性を高める検索の構成 |
| [1.5.5](../../domain1.md#skill-1-5-5) | 問い合わせの処理 |
| [1.5.6](../../domain1.md#skill-1-5-6) | 一貫したアクセスの仕組み |

## 学習の順番 {#study-order}

1. [Managed と Customer-managed](../../../../services/genai-apps.md#managed-kb): コネクタの違いと、接続先ごとの手段を確認します。
2. [同期と鮮度](../../../../services/genai-apps.md#kb-sync): `StartIngestionJob` と、更新の方式の違いを覚えます。
3. [チャンク化の戦略](../../../../services/genai-apps.md#chunking): 文書と症状から戦略を選びます。設定の範囲も確認します。
4. [埋め込みの選び方](../../../../services/genai-apps.md#embedding-selection)と[クォータ](../../../../services/ai.md#quotas-detail): RPM の制限と大量生成の方法を押さえます。
5. [検索の改善](../../../../services/genai-apps.md#retrieval-optimization)と[パラメータ](../../../../services/ai.md#kb-params): ハイブリッド、リランク、クエリ分解、暗黙のフィルターを整理します。
6. [MCP](../../../../services/genai-apps.md#mcp)と[ツール利用の流れ](../../../../services/ai.md#tool-use-flow): 検索をツールにするときの利点と注意を理解します。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| 既定のチャンク | 約 300 トークン | まず試す |
| 固定サイズの重なり | 1〜99% | 例は 20 |
| `numberOfResults` | 1〜100、既定 5 | 上限で、少なく返ることがある |
| Titan Text Embeddings V2 の入力 | 8,192 トークン、50,000 文字 | クォータは RPM |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| Customer-managed で SaaS のデータを使う | AppFlow で S3 へ転送 |
| オンプレミスのファイル、SFTP | DataSync、Transfer Family |
| 文脈が足りないが細かく一致させたい | 階層チャンク |
| FAQ を組で分ける | チャンクなしとカスタム変換の Lambda |
| 製品番号で外れる | ハイブリッド検索 |
| 候補はあるが順位が悪い | リランク |
| 比較の質問で片方しか返らない | クエリ分解 |
| 必ず根拠が要る | アプリ側で先に検索する |

## 引っかかりやすい点 {#traps}

- Customer-managed は自動で同期しません。Managed のスケジュール同期も日次、週次、月次です。
- S3 Vectors ではハイブリッド検索を使えず、階層チャンクも非推奨です。
- リランクは候補に入らない文書を救えません。
- 検索をツールにすると、モデルが呼び忘れることがあります。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [knowledge-bases 問1](../../exercises/knowledge-bases.md#q1) | 1.4.4 | ある企業は、Customer-managed のナレッジベースと OpenSearch を運用してい… |
| [knowledge-bases 問2](../../exercises/knowledge-bases.md#q2) | 1.4.4 | 工場のオンプレミスのファイルサーバーにある手順書を RAG の対象にします。更新されたファイルを毎日… |
| [knowledge-bases 問3](../../exercises/knowledge-bases.md#q3) | 1.4.4 | 独自の社内 wiki に文書があり、更新は専用の API からしか取得できません。更新を検知したらす… |
| [knowledge-bases 問4](../../exercises/knowledge-bases.md#q4) | 1.4.5 | S3 の文書を更新してもナレッジベースに反映されません。文書は平日に数回更新され、更新から数分以内に… |
| [knowledge-bases 問5](../../exercises/knowledge-bases.md#q5) | 1.4.5 | 医療情報の RAG では、更新で品質が下がると大きな問題になります。文書を更新したら、同期のあとで取… |
| [knowledge-bases 問6](../../exercises/knowledge-bases.md#q6) | 1.4.5 | 1 時間に数百件の文書が更新されるデータソースで、更新のたびに StartIngestionJob … |
| [knowledge-bases 問7](../../exercises/knowledge-bases.md#q7) | 1.5.1 | 製品マニュアルの RAG で、検索の一致は細かい単位で行いたいものの、回答には前後の文脈が必要です。… |
| [knowledge-bases 問8](../../exercises/knowledge-bases.md#q8) | 1.5.1 | S3 Vectors をベクトルストアにしたナレッジベースで、親 8,000 トークン、子 300 … |
| [knowledge-bases 問9](../../exercises/knowledge-bases.md#q9) | 1.5.1 | FAQ の文書を「質問と回答の組」で 1 チャンクにしたいと考えています。組の長さはまちまちで、既定… |
| [knowledge-bases 問10](../../exercises/knowledge-bases.md#q10) | 1.5.2 | 500 万チャンクの初回の埋め込みを Titan Text Embeddings V2 で行います。… |
| [knowledge-bases 問11](../../exercises/knowledge-bases.md#q11) | 1.5.2 | 1,000 万チャンクの FAQ を検索する基盤で、ストレージの費用が課題です。チームは 1,024… |
| [knowledge-bases 問12](../../exercises/knowledge-bases.md#q12) | 1.5.2 | 製品の写真と説明文を同じ検索基盤で探せるようにします。利用者は文章でも写真でも質問します。Titan… |
| [knowledge-bases 問13](../../exercises/knowledge-bases.md#q13) | 1.5.4 | 部品番号「AB-123」で検索すると無関係な文書が上位に来ます。ベクトルストアは OpenSearc… |
| [knowledge-bases 問14](../../exercises/knowledge-bases.md#q14) | 1.5.4 | RAG で、関連する文書は候補に入っていますが、順位が低く、モデルに渡す 5 件に入りません。回答の… |
| [knowledge-bases 問15](../../exercises/knowledge-bases.md#q15) | 1.5.4 | 大量の古い文書を S3 Vectors に置いたナレッジベースに、キーワードの一致が重要な新しい質問… |
| [knowledge-bases 問16](../../exercises/knowledge-bases.md#q16) | 1.5.5 | 「A 社と B 社で、昨年の売上が高いのはどちらか」という質問で、片方の会社の文書だけが返ります。文… |
| [knowledge-bases 問17](../../exercises/knowledge-bases.md#q17) | 1.5.5 | 利用者は「去年の日本向けの規定」のように自然文で条件を書きます。文書には year と region… |
| [knowledge-bases 問18](../../exercises/knowledge-bases.md#q18) | 1.5.5 | すべての質問にクエリ拡張とクエリ分解を適用したところ、簡単な質問の遅延と費用が増えました。複雑な質問… |
| [knowledge-bases 問19](../../exercises/knowledge-bases.md#q19) | 1.5.6 | 社内検索を、チャットアプリ、3 つのエージェント、別チームの開発支援ツールで共通に使わせたいと考えて… |
| [knowledge-bases 問20](../../exercises/knowledge-bases.md#q20) | 1.5.6 | 規定の質問に答えるアプリで、検索を Converse のツールとして定義しました。雑談では検索されず… |
| [knowledge-bases 問21](../../exercises/knowledge-bases.md#q21) | 1.5.6 | 社内の複数のシステムが検索結果を使います。モデルを介さないバッチ処理も、同じ検索結果の形で使う必要が… |

<!-- questions:end -->

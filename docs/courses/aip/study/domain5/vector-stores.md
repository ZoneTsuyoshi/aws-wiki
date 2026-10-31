# 分野5: 検索システムの問題

症状から検索の原因を切り分けます。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [5.2.4](../../domain5.md#skill-5-2-4) | 検索システムの問題 |

## 学習の順番 {#study-order}

1. [トラブルシューティング](../../../../services/genai-apps.md#troubleshooting): 調査の順序を確認します。
2. [チャンク化の戦略](../../../../services/genai-apps.md#chunking)と[解析の選択肢](../../../../services/genai-apps.md#kb-ingestion): 表が崩れるときの対応を押さえます。
3. [埋め込みの選び方](../../../../services/genai-apps.md#embedding-selection): モデルの変更の影響を理解します。
4. [キャッシュの種類](../../../../services/genai-apps.md#caching): 古い回答の原因を確認します。

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 検索か生成か分からない | `Retrieve` の単体テスト |
| 急に精度が落ちた | 質問と文書の埋め込みモデルを確かめる |
| 表の数値を誤る | BDA か FM のパーサー |
| `Retrieve` は新しいのに回答が古い | セマンティックキャッシュ |

## 引っかかりやすい点 {#traps}

- 差分の同期では、変更のない文書は埋め込み直されません。
- 解析の時点で崩れた表は、チャンクやリランクでは直りません。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [vector-stores 問20](../../exercises/vector-stores.md#q20) | 5.2.4 | ある週から RAG の精度が急に落ちました。文書の更新はなく、遅延やエラーも変わっていません。調べる… |
| [vector-stores 問21](../../exercises/vector-stores.md#q21) | 5.2.4 | RAG の回答が誤っていると報告されました。チームは、検索が悪いのか、生成が悪いのかで意見が分かれて… |
| [vector-stores 問22](../../exercises/vector-stores.md#q22) | 5.2.4 | 財務レポートの PDF を Knowledge Bases に取り込みました。文章の質問には答えられ… |
| [vector-stores 問23](../../exercises/vector-stores.md#q23) | 5.2.4 | 文書を更新して同期ジョブは成功しましたが、新しい内容が回答に出ません。Retrieve を単体で呼ぶ… |

<!-- questions:end -->

# 分野1: 生成 AI の技法

プロンプト、トークンとコンテキストウィンドウ、RAG とファインチューニングを、業務の症状と結びつけて判断します。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [1.3.1](../../domain1.md#skill-1-3-1) | プロンプトの基本 |
| [1.3.2](../../domain1.md#skill-1-3-2) | トークンとコンテキストウィンドウ |
| [1.3.3](../../domain1.md#skill-1-3-3) | RAG、ファインチューニング |

## 学習の順番 {#study-order}

1. [プロンプトエンジニアリング](../../../../services/ai-fundamentals.md#prompt-engineering): 指示、文脈、入力データ、出力形式と、4 つの手法を確認します。
2. [トークンとコンテキストウィンドウ](../../../../services/ai-fundamentals.md#tokens): 症状と原因の対応を表で覚えます。
3. [モデルを業務に合わせる方法](../../../../services/ai-fundamentals.md#customization-options): 手軽で安い順の並びを覚えます。
4. [RAG](../../../../services/ai-fundamentals.md#rag)と [Knowledge Bases](../../../../services/genai-apps.md#knowledge-bases): 文書を更新すれば再学習が不要なことと、引用を示せることを押さえます。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| 検討の順序 | プロンプト、RAG、ファインチューニング、独自の学習 | 手軽で安いものから |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 出力の形が毎回違う | 役割、目的、出力形式を指定する |
| 分類の基準が伝わらない | フューショット |
| 計算や推論の考え方を誤る | Chain-of-thought |
| 回答が途中で切れる | 最大出力トークンを確認する |
| 会話の後半で最初の指示を忘れる | 履歴を要約し、指示を入れ直す |
| 文書が上限を超える | 分割、要約、RAG |
| 最新の情報に答えさせたい | RAG |
| 自社の文体で書かせたい | ファインチューニング |

## 引っかかりやすい点 {#traps}

- 大きなコンテキストウィンドウのモデルに変えても、入力が減るわけではないので費用は下がりません。
- temperature は長さの上限ではありません。
- RAG でもハルシネーションはゼロになりません。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [genai-techniques 問1](../../exercises/genai-techniques.md#q1) | 1.3.1 | 営業担当者が「この議事録をまとめて」と入力すると、毎回違う形で返ってきて使いにくいと困っています。最… |
| [genai-techniques 問2](../../exercises/genai-techniques.md#q2) | 1.3.1 | 問い合わせを社内独自の 5 つの分類に分けさせています。分類の基準がうまく伝わらず、結果がぶれます。… |
| [genai-techniques 問3](../../exercises/genai-techniques.md#q3) | 1.3.1 | 見積もりの合計を生成 AI に確認させると、途中の計算の考え方を誤ることがあります。段階を追って考え… |
| [genai-techniques 問4](../../exercises/genai-techniques.md#q4) | 1.3.1 | 部署の全員が同じ品質で報告書の要約を作れるようにしたいと考えています。最も手軽で適切な方法はどれです… |
| [genai-techniques 問5](../../exercises/genai-techniques.md#q5) | 1.3.2 | コンテキストウィンドウの説明として正しいものはどれですか。 |
| [genai-techniques 問6](../../exercises/genai-techniques.md#q6) | 1.3.2 | 長く続けた会話の後半で、チャットの AI が最初に指定した条件を守らなくなりました。最も可能性の高い… |
| [genai-techniques 問7](../../exercises/genai-techniques.md#q7) | 1.3.2 | 生成 AI の回答が毎回、文の途中で切れます。入力の文書は短く、エラーも出ていません。まず確認すべき… |
| [genai-techniques 問8](../../exercises/genai-techniques.md#q8) | 1.3.2 | 800 ページの製品マニュアルについて質問に答えさせたいのですが、毎回全文を渡すと上限を超えます。最… |
| [genai-techniques 問9](../../exercises/genai-techniques.md#q9) | 1.3.2 | チャットの費用が想定の 3 倍になりました。調べると、毎回の呼び出しに長い会話履歴と数十ページの資料… |
| [genai-techniques 問10](../../exercises/genai-techniques.md#q10) | 1.3.3 | 価格表が毎週更新されます。営業向けの AI に常に最新の価格を答えさせたいと考えています。最も適切な… |
| [genai-techniques 問11](../../exercises/genai-techniques.md#q11) | 1.3.3 | 広報部門は、生成 AI に自社独特の文体と書式で文章を書かせたいと考えています。プロンプトでは十分に… |
| [genai-techniques 問12](../../exercises/genai-techniques.md#q12) | 1.3.3 | モデルを業務に合わせる技法を、一般に手軽で費用の少ないものから順に並べたものはどれですか。 |
| [genai-techniques 問13](../../exercises/genai-techniques.md#q13) | 1.3.3 | 社内文書を根拠に、引用付きで回答する機能をマネージドで実現したいと考えています。該当する AWS の… |
| [genai-techniques 問14](../../exercises/genai-techniques.md#q14) | 1.3.3 | RAG の説明として正しいものはどれですか。（2つ選択） |
| [genai-techniques 問15](../../exercises/genai-techniques.md#q15) | 1.3.3 | 法律事務所は、毎週更新される判例を根拠にしつつ、事務所の書面の文体で回答を作りたいと考えています。最… |

<!-- questions:end -->

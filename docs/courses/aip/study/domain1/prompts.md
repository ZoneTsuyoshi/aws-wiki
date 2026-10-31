# 分野1: プロンプトと Flows

プロンプトの指示の枠組み、対話の文脈、ガバナンス、品質保証、流れの構築を扱います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [1.6.1](../../domain1.md#skill-1-6-1) | モデルへの指示の枠組み |
| [1.6.2](../../domain1.md#skill-1-6-2) | 文脈を保つ対話システム |
| [1.6.3](../../domain1.md#skill-1-6-3) | プロンプトの管理とガバナンス |
| [1.6.4](../../domain1.md#skill-1-6-4) | プロンプトの品質保証 |
| [1.6.5](../../domain1.md#skill-1-6-5) | プロンプトの反復的な改善 |
| [1.6.6](../../domain1.md#skill-1-6-6) | 複雑なプロンプトシステム |

## 学習の順番 {#study-order}

1. [プロンプトの管理](../../../../services/genai-apps.md#prompt-management): テンプレート、バリアント、バージョンの違いを確認します。
2. [Guardrails の実践](../../../../services/genai-apps.md#guardrails-depth)と[構造化出力](../../../../services/genai-apps.md#structured-output): プロンプトでは保証できないものの置き場所を押さえます。
3. [TTL](../../../../services/dynamodb.md#ttl)と [Memory の設計](../../../../services/genai-apps.md#agentcore-memory): 履歴と記憶の保存先を選べるようにします。
4. [モデル呼び出しログ](../../../../services/ai.md#invocation-logging)と [CloudTrail との違い](../../../../services/observability.md#cloudtrail-vs-cloudwatch): どちらが何を記録するかを覚えます。
5. [テスト](../../../../services/genai-apps.md#testing)と [Map の設定](../../../../services/step-functions.md#map-settings): 回帰と境界条件の確かめ方を理解します。
6. [プロンプトエンジニアリング](../../../../services/ai-fundamentals.md#prompt-engineering): 入力の構造化と Chain-of-thought の使いどころを確認します。
7. [Bedrock Flows](../../../../services/genai-apps.md#flows): ノードの役割と、バージョンとエイリアスの動きを押さえます。

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 役割を揃える | Prompt Management のテンプレート |
| 確実に守らせる | Guardrails やアプリの検証 |
| 応答を JSON に合わせる | 構造化出力 |
| 人の入力を数日待つ | Step Functions の Standard と `.waitForTaskToken` |
| 誰が変更したか | CloudTrail |
| 何を送ったか | モデル呼び出しログ |
| プロンプト中心の分岐を画面で作る | Flows の Prompt と Condition |
| 配列を順に処理してまとめる | Iterator と Collector |

## 引っかかりやすい点 {#traps}

- `Converse` に `sessionId` のような保持の仕組みはありません。
- 出力は毎回変わるので、完全一致のテストは使えません。
- `TSTALIASID` は `DRAFT` を指します。本番に使うと編集がそのまま流れます。
- Chain-of-thought は単純な分類では費用だけが増えることがあります。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [prompts 問1](../../exercises/prompts.md#q1) | 1.6.1 | 銀行の問い合わせチャットでは、投資助言を絶対に出してはならず、回答の文体は全チームで揃えます。今はシ… |
| [prompts 問2](../../exercises/prompts.md#q2) | 1.6.1 | FM の応答を下流の受注システムに渡します。項目の名前と型が決まっており、プロンプトで「JSON で… |
| [prompts 問3](../../exercises/prompts.md#q3) | 1.6.1 | 10 のチームが FM を使ったアプリを作っており、役割の定義と責任ある AI の方針の適用がばらば… |
| [prompts 問4](../../exercises/prompts.md#q4) | 1.6.2 | チャットの会話履歴を保存します。要件は、セッションごとに低遅延で読み書きすること、30 日で自動削除… |
| [prompts 問5](../../exercises/prompts.md#q5) | 1.6.2 | 申請の受付の対話で、必要な情報が足りないときは利用者に聞き返し、回答を数時間から数日待ちます。今は … |
| [prompts 問6](../../exercises/prompts.md#q6) | 1.6.2 | 英語のサポートチャットで、問い合わせの意図（解約、請求、技術）によって処理を分けます。意図のラベルは… |
| [prompts 問7](../../exercises/prompts.md#q7) | 1.6.3 | 監査チームから 2 つの要求がありました。「誰がプロンプトのテンプレートを変更したか」と「ある回答の… |
| [prompts 問8](../../exercises/prompts.md#q8) | 1.6.3 | 本番アプリが Prompt Management のプロンプトを使っています。担当者が編集した内容が… |
| [prompts 問9](../../exercises/prompts.md#q9) | 1.6.3 | コンプライアンスの要件で、プロンプトのテンプレートは承認なしで変更できないようにし、誰の変更かも追え… |
| [prompts 問10](../../exercises/prompts.md#q10) | 1.6.4 | 要約のプロンプトの回帰テストを作ります。担当者は、期待する文と完全一致するかを判定する案を出しました… |
| [prompts 問11](../../exercises/prompts.md#q11) | 1.6.4 | プロンプトの変更のたびに、空の入力、非常に長い入力、記号だけの入力などの境界条件を 200 件流し、… |
| [prompts 問12](../../exercises/prompts.md#q12) | 1.6.4 | 本番のプロンプトの合格率が徐々に下がっていないかを継続して監視し、下がったら担当者に知らせたいと考え… |
| [prompts 問13](../../exercises/prompts.md#q13) | 1.6.5 | 契約書の条項の分析で、モデルが指示と契約書の本文を取り違え、本文の中の文を指示として扱うことがありま… |
| [prompts 問14](../../exercises/prompts.md#q14) | 1.6.5 | 毎日数百万件の短い感情分類に使っているプロンプトに、精度を上げようと Chain-of-though… |
| [prompts 問15](../../exercises/prompts.md#q15) | 1.6.5 | 利用者の低評価が多いプロンプトを改善します。評価は DynamoDB に応答の ID と共に保存して… |
| [prompts 問16](../../exercises/prompts.md#q16) | 1.6.6 | カテゴリを判定するプロンプトの結果で、別のプロンプトへ分岐し、結果を整形して返す流れを作ります。コー… |
| [prompts 問17](../../exercises/prompts.md#q17) | 1.6.6 | Flows の新しい版をリリースします。アプリのコードの変更は避け、問題があればすぐに戻したいと考え… |
| [prompts 問18](../../exercises/prompts.md#q18) | 1.6.6 | 複数の章を持つ文書を章ごとに要約し、結果をまとめて全体の要約を作ります。人の承認は要らず、失敗時の複… |

<!-- questions:end -->

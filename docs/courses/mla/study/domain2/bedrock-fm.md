# 分野2: Bedrock の FM

要件からモデルを絞り、同じ評価データで比べます。ライフサイクルと、遅延とコストの手段も問います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [2.1.1](../../domain2.md#skill-2-1-1) | Bedrock の FM の評価と選択 |
| [2.1.7](../../domain2.md#skill-2-1-7) | AI モデルの性能、遅延、コストのトレードオフ |

## 学習の順番 {#study-order}

1. [FM の選定の観点](../../../../services/genai-apps.md#fm-criteria): モダリティ、コンテキスト長、遅延、コストを確認します。
2. [モデルのライフサイクル](../../../../services/genai-apps.md#model-lifecycle): Active、Legacy、EOL の動作を覚えます。
3. [動的なモデル切り替え](../../../../services/genai-apps.md#dynamic-model-selection)と[遅延の短縮](../../../../services/genai-apps.md#latency): 手段の違いを押さえます。
4. [Bedrock の料金](../../../../services/cost-management.md#bedrock-pricing): 層ごとの価格を確認します。

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 図表を読む | マルチモーダルのモデル |
| 対話の待ち時間を短くする | 小さなモデル、ストリーミング |
| 同じ系統で振り分けを任せる | Intelligent Prompt Routing |
| 急がない大量の処理 | バッチ、Flex |
| 応答速度を最優先 | Priority |

## 引っかかりやすい点 {#traps}

- EOL に達するとリクエストは失敗し、自動の移行はありません。
- ストリーミングは全体の時間を変えません。
- Intelligent Prompt Routing は同じ系統の中だけです。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [bedrock-fm 問1](../../exercises/bedrock-fm.md#q1) | 2.1.1 | 図表を含む提案書を読ませて、要点をすぐ返す対話アプリです。FM を絞り込むときに見る観点の組み合わせ… |
| [bedrock-fm 問2](../../exercises/bedrock-fm.md#q2) | 2.1.1 | 使っているモデルが End-of-Life（EOL）に達すると、どうなりますか。 |
| [bedrock-fm 問3](../../exercises/bedrock-fm.md#q3) | 2.1.1 | 長期運用するアプリで FM の状態を定期的に確認します。正しい運用はどれですか。（2つ選択） |
| [bedrock-fm 問4](../../exercises/bedrock-fm.md#q4) | 2.1.7 | 問い合わせの 8 割は定型で、残りは難しい質問です。品質を保ちつつ FM のコストを下げます。Nov… |
| [bedrock-fm 問5](../../exercises/bedrock-fm.md#q5) | 2.1.7 | 対話アプリで、全体の処理時間は変えずに体感の待ち時間を減らします。適切な変更はどれですか。 |
| [bedrock-fm 問6](../../exercises/bedrock-fm.md#q6) | 2.1.7 | 毎晩の 100 万件の文書の要約です。翌朝に終わればよく、できるだけ安くします。どれを選びますか。 |

<!-- questions:end -->

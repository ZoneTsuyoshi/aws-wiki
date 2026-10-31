# 分野4: コストの最適化とキャッシュ

トークン、モデルの選択、容量、キャッシュの 4 つの面で費用を下げます。何を犠牲にするかを押さえます。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [4.1.1](../../domain4.md#skill-4-1-1) | トークンの効率化 |
| [4.1.2](../../domain4.md#skill-4-1-2) | 費用対効果の高いモデル選択 |
| [4.1.3](../../domain4.md#skill-4-1-3) | 高い処理能力と資源の活用 |
| [4.1.4](../../domain4.md#skill-4-1-4) | 賢いキャッシュ |

## 学習の順番 {#study-order}

1. [トークンの削減](../../../../services/genai-apps.md#token-efficiency)と[推論の容量とプロファイル](../../../../services/genai-apps.md#inference-profiles): 削減の手法と費用の追跡を確認します。
2. [Bedrock の料金](../../../../services/cost-management.md#bedrock-pricing)と[スループットの選択肢](../../../../services/ai.md#throughput-options): 層とバッチの価格の違いを覚えます。
3. [CloudWatch のメトリクス](../../../../services/ai.md#bedrock-metrics): クォータの指標を確認します。
4. [キャッシュの種類](../../../../services/genai-apps.md#caching)と [Amazon MemoryDB](../../../../services/databases-specialized.md#memorydb): 種類ごとの効く場面を比べます。
5. [クォータとプロンプトキャッシュ](../../../../services/ai.md#quotas-detail): `cachePoint` と結果の確かめ方を押さえます。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| バッチ | 対象のモデルで 50% 引き | プロビジョンドモデルでは使えない |
| プロンプトキャッシュの TTL | 多くのモデルで 5 分 | ヒットごとに延びる |
| `global` のプロファイル | 地理的プロファイルより約 10% 安い | データの所在の要件がないとき |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 固定の長い指示、質問は毎回違う | プロンプトキャッシュ |
| 言い換えの質問が多い | セマンティックキャッシュ |
| 同じ文書の再処理 | 内容とモデルの版をキーにしたフィンガープリント |
| アプリごとの費用 | アプリケーション推論プロファイルのタグ |
| 時間に余裕がある同期の処理 | Flex |
| 価格性能比 | 1 件の成功あたりの費用 |

## 引っかかりやすい点 {#traps}

- プロンプトキャッシュは FM を呼びます。他のキャッシュは呼び出しを省きます。
- 順番が変わるとプロンプトキャッシュは一致しません。
- 権限や個人情報を含む回答は、キャッシュしないかキーを分けます。
- コミットメントの期間中は Provisioned Throughput を削除できません。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [cost-optimization 問1](../../exercises/cost-optimization.md#q1) | 4.1.1 | 同じアカウントで 5 つのアプリが同じモデルを呼んでいます。月額が増え、どのアプリの費用かが分かりま… |
| [cost-optimization 問2](../../exercises/cost-optimization.md#q2) | 4.1.1 | RAG の入力トークンの大半が、検索で取得した 20 件のチャンクです。回答に使われているのは多くて… |
| [cost-optimization 問3](../../exercises/cost-optimization.md#q3) | 4.1.1 | 長文の分析を受け付ける API で、上限を超える入力が FM まで届き、エラーと費用の無駄が発生して… |
| [cost-optimization 問4](../../exercises/cost-optimization.md#q4) | 4.1.2 | 次の 3 つの処理の費用と応答を最適化します。(a) 画面で待つ質問応答。(b) 数時間かかってもよ… |
| [cost-optimization 問5](../../exercises/cost-optimization.md#q5) | 4.1.2 | 安いモデル X は上位のモデル Y の 10 分の 1 の単価ですが、X の回答は正解率が低く、再試… |
| [cost-optimization 問6](../../exercises/cost-optimization.md#q6) | 4.1.2 | 英語の問い合わせの多くは簡単ですが、一部に難しいものがあります。同じ提供者の 2 つのモデルで、複雑… |
| [cost-optimization 問7](../../exercises/cost-optimization.md#q7) | 4.1.3 | Provisioned Throughput を 1 か月のコミットメントで購入しましたが、夜間の使… |
| [cost-optimization 問8](../../exercises/cost-optimization.md#q8) | 4.1.3 | オンデマンドの TPM クォータにいつ近づくかを、スロットリングが起きる前に知りたいと考えています。… |
| [cost-optimization 問9](../../exercises/cost-optimization.md#q9) | 4.1.3 | 100 万件の要約をプロビジョンドモデルのカスタムモデルでバッチ推論しようとしたところ、ジョブが作れ… |
| [cost-optimization 問10](../../exercises/cost-optimization.md#q10) | 4.1.4 | 50 ページの製品マニュアルを毎回システムプロンプトに入れており、質問は毎回違います。入力の費用と遅… |
| [cost-optimization 問11](../../exercises/cost-optimization.md#q11) | 4.1.4 | FAQ のチャットで、同じ意味の言い換えの質問が多く、FM の費用を減らしたいと考えています。回答に… |
| [cost-optimization 問12](../../exercises/cost-optimization.md#q12) | 4.1.4 | プロンプトキャッシュを入れましたが、費用が下がりません。呼び出しの間隔は 20 分に 1 回程度で、… |
| [cost-optimization 問13](../../exercises/cost-optimization.md#q13) | 4.1.4 | 同じ文書を何度も処理するパイプラインで、モデルの版やプロンプトの版が変わると結果が変わります。同じ文… |
| [cost-optimization 問14](../../exercises/cost-optimization.md#q14) | 4.1.1, 4.1.4 | 長い会話を続けるサポートのチャットで、入力トークンが費用の大半を占めています。システムプロンプトは長… |

<!-- questions:end -->

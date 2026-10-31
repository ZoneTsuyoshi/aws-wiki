# 分野2: 生成 AI の料金とコスト

トークン課金の考え方と、容量の選択肢のトレードオフを問います。単純な計算が出ることがあります。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [2.1.4](../../domain2.md#obj-2-1-4) | トークン単位の料金 |
| [2.3.4](../../domain2.md#obj-2-3-4) | AWS の生成 AI サービスのコストのトレードオフ |

## 学習の順番 {#study-order}

1. [トークンとコンテキストウィンドウ](../../../../services/ai-fundamentals.md#tokens): 計算例を自分で計算します。
2. [料金の形とコスト管理](../../../../services/ai-fundamentals.md#ai-pricing): 消費量、インスタンス、シートの 3 つの料金の形を区別します。
3. [トークンの削減](../../../../services/genai-apps.md#token-efficiency)と[キャッシュの種類](../../../../services/genai-apps.md#caching): 入力と出力を減らす方法を確認します。
4. [スループットの選択肢](../../../../services/ai.md#throughput-options): オンデマンド、Provisioned Throughput、バッチ、Priority と Flex の向き不向きを覚えます。
5. [推論の容量とプロファイル](../../../../services/genai-apps.md#inference-profiles)と[モデル ID と推論プロファイル](../../../../services/ai.md#model-identifiers): クロスリージョン推論とデータの所在の関係を理解します。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| Provisioned Throughput のコミットメント | なし、1 か月、6 か月 | 期間中は削除できない |
| グローバル推論プロファイル | 地理的クロスリージョン推論より約 10% 安い | データの所在の要件があると使えない |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 長い固定の入力が毎回ある | プロンプトキャッシュ |
| 夜間に大量に要約する | バッチ推論 |
| 固定の高い負荷、カスタムモデル | Provisioned Throughput |
| 負荷が読めない | オンデマンド |
| データを EU の外で処理しない | `eu` の推論プロファイル |
| 割増で最速にする | Priority |
| 割引で、時間がかかってもよい | Flex |

## 引っかかりやすい点 {#traps}

- 最大出力トークンが小さすぎると、応答が途中で切れます。
- Provisioned Throughput は使わなくても課金され、削除するまで続きます。
- `global` は安いのですが、処理先が世界に広がります。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [genai-cost 問1](../../exercises/genai-cost.md#q1) | 2.1.4 | Bedrock のオンデマンド推論の料金の基本的な考え方はどれですか。 |
| [genai-cost 問2](../../exercises/genai-cost.md#q2) | 2.1.4 | 仮の単価を、入力 100 万トークンあたり $3、出力 100 万トークンあたり $15 とします。… |
| [genai-cost 問3](../../exercises/genai-cost.md#q3) | 2.1.4 | チャットアプリの毎回の入力に、同じ長い規定文が含まれています。品質を保って入力の費用を減らす方法とし… |
| [genai-cost 問4](../../exercises/genai-cost.md#q4) | 2.1.4 | 最大出力トークンを極端に小さくして費用を削りました。起こりやすい症状はどれですか。 |
| [genai-cost 問5](../../exercises/genai-cost.md#q5) | 2.1.4 | トークンの費用を減らす方法として適切なものを選んでください。（2つ選択） |
| [genai-cost 問6](../../exercises/genai-cost.md#q6) | 2.3.4 | 夜間に 10 万件の通話を要約します。結果は翌朝までに出ればよく、すぐには要りません。適切な選択肢は… |
| [genai-cost 問7](../../exercises/genai-cost.md#q7) | 2.3.4 | カスタムモデルを使い、一日中ほぼ一定の高い負荷が続きます。適切な容量の選択肢と注意点はどれですか。 |
| [genai-cost 問8](../../exercises/genai-cost.md#q8) | 2.3.4 | Provisioned Throughput を 6 か月のコミットメントで購入しました。2 か月目… |
| [genai-cost 問9](../../exercises/genai-cost.md#q9) | 2.3.4 | 負荷が読めない新規のアプリで、まず Bedrock を試します。費用の面で適切な選択肢はどれですか。 |
| [genai-cost 問10](../../exercises/genai-cost.md#q10) | 2.3.4 | データを EU の外で処理してはいけません。推論プロファイルの選択として適切なものはどれですか。 |
| [genai-cost 問11](../../exercises/genai-cost.md#q11) | 2.3.4 | 可用性を上げるためにクロスリージョン推論を使います。あわせて確認すべき代償はどれですか。 |
| [genai-cost 問12](../../exercises/genai-cost.md#q12) | 2.3.4 | 応答を速くするために Priority 層を使います。トレードオフとして正しいものはどれですか。 |

<!-- questions:end -->

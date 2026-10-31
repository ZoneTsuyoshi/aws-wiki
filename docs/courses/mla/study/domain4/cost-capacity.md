# 分野4: コストと容量

容量の最適化の順序、コスト管理ツール、購入オプション、FM のトークンのコストを問います。計算問題も出ます。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [4.2.4](../../domain4.md#skill-4-2-4) | 容量の最適化 |
| [4.2.5](../../domain4.md#skill-4-2-5) | コスト管理ツールとコストのクォータ |
| [4.2.6](../../domain4.md#skill-4-2-6) | 購入オプションの選択 |
| [4.2.7](../../domain4.md#skill-4-2-7) | FM の推論のコスト評価 |
| [4.2.9](../../domain4.md#skill-4-2-9) | 使い方の最適化による FM のコスト管理 |
| [4.2.10](../../domain4.md#skill-4-2-10) | AI 固有のコストの監視 |

## 学習の順番 {#study-order}

1. [推論の最適化](../../../../services/sagemaker.md#inference-optimization)と[耐障害の設計](../../../../services/genai-apps.md#fm-resilience): 手順と容量の確保を確認します。
2. [予算の種類](../../../../services/cost-management.md#budget-types)、[予算アクション](../../../../services/cost-management.md#budget-actions)、[コスト配分タグ](../../../../services/cost-management.md#cost-allocation-tags): 通知と統制を覚えます。
3. [購入の選び方](../../../../services/cost-management.md#purchase-choice): 割引の値を押さえます。
4. [Bedrock の料金](../../../../services/cost-management.md#bedrock-pricing)と[トークン](../../../../services/ai-fundamentals.md#tokens): 計算できるようにします。
5. [トークンの削減](../../../../services/genai-apps.md#token-efficiency)と[キャッシュの種類](../../../../services/genai-apps.md#caching): 手段を比べます。
6. [ベクトルストア](../../../../services/genai-apps.md#vector-stores)と [Cost Anomaly Detection](../../../../services/cost-management.md#cost-anomaly-detection): AI 固有の項目を確認します。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| Managed Spot | 最大 90% 割引 | 中断できる学習 |
| SageMaker AI Savings Plans | 最大 64% 割引。1 年か 3 年 | 継続する利用 |
| Priority | 多くのプロバイダーで Standard の 75% 増し | 速さを優先 |
| Flex | 多くのプロバイダーで Standard の 50% 引き | 遅くても安く |
| バッチ | 対象のモデルでオンデマンドの 50% 引き | 急がない大量処理 |
| プロンプトキャッシュの TTL | 多くのモデルで 5 分 | 固定の内容を先に置く |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 超過に早く気付く | `FORECASTED` と低めのしきい値 |
| 超過時に新しいリソースを止める | 予算アクションと IAM ポリシー |
| チームごとの集計 | コスト配分タグの有効化 |
| 定常のエンドポイント | Savings Plans |
| GPU の容量を計画的に確保する | トレーニングプラン |
| 言い換えの質問でモデルを呼ばない | セマンティックキャッシュ |
| コストの急増に気付く | Cost Anomaly Detection |

## 引っかかりやすい点 {#traps}

- タグは付けるだけでは請求データに出ません。
- `maxTokens` が大きすぎると、クォータの予約も増えてスロットリングの原因になります。
- Savings Plans は、使用量を最適化してから買います。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [cost-capacity 問1](../../exercises/cost-capacity.md#q1) | 4.2.4 | 本番のエンドポイントの信頼性を上げます。AZ の障害に備える最も基本の設定はどれですか。 |
| [cost-capacity 問2](../../exercises/cost-capacity.md#q2) | 4.2.4 | Bedrock のオンデマンドで、ピーク時に容量不足のエラーが出ます。容量を確保する選択肢を選んでく… |
| [cost-capacity 問3](../../exercises/cost-capacity.md#q3) | 4.2.4 | 使用率の低いエンドポイントが 20 個あり、それぞれ別のインスタンスで動いています。容量を最適化する… |
| [cost-capacity 問4](../../exercises/cost-capacity.md#q4) | 4.2.5 | 月の予算の超過に早く気付き、超えそうなら新しいリソースの作成を止めます。AWS Budgets の設… |
| [cost-capacity 問5](../../exercises/cost-capacity.md#q5) | 4.2.5 | チームごとの ML のコストを Cost Explorer で見たいです。リソースに team タグ… |
| [cost-capacity 問6](../../exercises/cost-capacity.md#q6) | 4.2.5 | 次の目的とツールの組み合わせとして正しいものはどれですか。 |
| [cost-capacity 問7](../../exercises/cost-capacity.md#q7) | 4.2.6 | 24 時間一定の負荷の GPU のエンドポイントを 3 年運用します。購入方法はどれですか。 |
| [cost-capacity 問8](../../exercises/cost-capacity.md#q8) | 4.2.6 | 夜間の学習ジョブは中断されても問題なく、コストを最大に下げます。割引の最大の値も含めて正しいものはど… |
| [cost-capacity 問9](../../exercises/cost-capacity.md#q9) | 4.2.6 | 大規模な FM の学習を来月行います。GPU の容量を計画的に確保します。どれですか。 |
| [cost-capacity 問10](../../exercises/cost-capacity.md#q10) | 4.2.7 | 入力 100 万トークンあたり $3、出力 100 万トークンあたり $15 の仮のモデルです。1 … |
| [cost-capacity 問11](../../exercises/cost-capacity.md#q11) | 4.2.7 | FM のコストを見積もります。トークンのほかに含める項目を選んでください。（2つ選択） |
| [cost-capacity 問12](../../exercises/cost-capacity.md#q12) | 4.2.7 | Bedrock のサービス層の特徴の組み合わせとして正しいものはどれですか。 |
| [cost-capacity 問13](../../exercises/cost-capacity.md#q13) | 4.2.9 | 長いシステムプロンプトと固定の社内規定を毎回送っています。後半の質問だけが毎回変わります。コストを下… |
| [cost-capacity 問14](../../exercises/cost-capacity.md#q14) | 4.2.9 | maxTokens を実態より大きく設定すると、コスト以外に何が起きますか。 |
| [cost-capacity 問15](../../exercises/cost-capacity.md#q15) | 4.2.9 | 会話の履歴が長くなり、トークンが増えています。アプリごとのコストも追跡します。適切な手段を選んでくだ… |
| [cost-capacity 問16](../../exercises/cost-capacity.md#q16) | 4.2.10 | プロンプトキャッシュの効果を確認します。CloudWatch で見る Bedrock の指標はどれで… |
| [cost-capacity 問17](../../exercises/cost-capacity.md#q17) | 4.2.10 | ベクトルの保存のコストが急増しました。文書は 1 億チャンクで、古い文書の検索はまれです。対策として… |
| [cost-capacity 問18](../../exercises/cost-capacity.md#q18) | 4.2.10 | Bedrock の日次のコストが突然 3 倍になったことに、自動で気付きたいです。どの機能が適切です… |

<!-- questions:end -->

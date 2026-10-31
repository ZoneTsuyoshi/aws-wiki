# 分野2: AI のコスト管理

料金の形を見分け、見積もり、実績の分析、最適化の手段を選びます。金額より単位と使う時点を覚えます。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [2.2.5](../../domain2.md#skill-2-2-5) | コスト管理 |

## 学習の順番 {#study-order}

1. [料金の形とコスト管理](../../../../services/ai-fundamentals.md#ai-pricing): 消費量、インスタンス、シートの 3 つの形を覚えます。
2. [AI サービスの料金の構造](../../../../services/cost-management.md#ai-pricing)と [Amazon Bedrock](../../../../services/cost-management.md#bedrock-pricing): ティアの違いと、費用を下げる方法を確認します。
3. [Pricing Calculator](../../../../services/cost-management.md#pricing-calculator)と [Cost Explorer](../../../../services/cost-management.md#cost-explorer): 導入の前と後で使い分けます。
4. [AWS Budgets](../../../../services/cost-management.md#budgets)と[コスト配分タグ](../../../../services/cost-management.md#cost-allocation-tags): 超過に気づく仕組みと、責任の配分を確認します。
5. [Savings Plans](../../../../services/cost-management.md#savings-plans): 確約と割引の関係、SageMaker AI 向けのプランを押さえます。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| Bedrock のティア | Reserved、Priority、Standard、Flex | 既定は Standard |
| Reserved の最小容量 | 入力 100,000 TPM、出力 10,000 TPM | アカウントチームに連絡する |
| バッチ | 対象のモデルでオンデマンドより 50% 安い | 急がない大量の処理 |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 需要が読めず変動が大きい | 消費量ベース |
| 未使用でも費用がかかる | インスタンスベース |
| 利用者数が読める業務アプリ | シートベース |
| 作る前に費用を示す | AWS Pricing Calculator |
| 導入後の実績を分析する | AWS Cost Explorer |
| 超過に早く気づく | AWS Budgets のアラート |
| 夜間の大量処理で即時の応答は不要 | バッチ |
| 応答の速さを優先し、容量の予約は不要 | Priority |
| ダウンタイムを許容できない | Reserved |
| 同じ長い指示を繰り返し送る | プロンプトキャッシュ |
| SageMaker AI を継続して使う | SageMaker AI Savings Plans |

## 引っかかりやすい点 {#traps}

- Cost Explorer はまだ使っていないものを見積もれません。
- Savings Plans は確約した額を使わなくても支払います。購入後に確約の条件は変更できません。
- RAG の費用はトークンだけではありません。ベクトルストアや Guardrails の費用も見積もります。
- Priority は応答を優先しますが、容量は確保しません。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [ai-costs 問1](../../exercises/ai-costs.md#q1) | 2.2.5 | 新しい顧客向け機能の需要が読めず、利用量の変動も大きいと予想されます。最初に合う料金の形はどれですか… |
| [ai-costs 問2](../../exercises/ai-costs.md#q2) | 2.2.5 | Amazon SageMaker AI のエンドポイントを常時起動しています。夜間はほとんど利用があ… |
| [ai-costs 問3](../../exercises/ai-costs.md#q3) | 2.2.5 | 全社の 3,000 人が使う業務向けの AI アシスタントを、利用者ごとの月額で契約します。これはど… |
| [ai-costs 問4](../../exercises/ai-costs.md#q4) | 2.2.5 | 構築を始める前に、生成 AI のアプリの費用を経営層に見積もりで示したいと考えています。どのツールを… |
| [ai-costs 問5](../../exercises/ai-costs.md#q5) | 2.2.5 | AI の本番の導入から 3 か月がたちました。費用の実績をサービス別、タグ別に分析したいと考えていま… |
| [ai-costs 問6](../../exercises/ai-costs.md#q6) | 2.2.5 | 生成 AI の費用が月の予算を超えそうになったら、担当者が早く気づけるようにしたいと考えています。最… |
| [ai-costs 問7](../../exercises/ai-costs.md#q7) | 2.2.5 | 毎晩、大量の文書を生成 AI で要約します。結果は翌朝までに揃えばよく、即時の応答は要りません。Am… |
| [ai-costs 問8](../../exercises/ai-costs.md#q8) | 2.2.5 | 顧客向けの重要な画面で、応答の速さを優先したいと考えています。24 時間の容量の確保までは不要で、割… |
| [ai-costs 問9](../../exercises/ai-costs.md#q9) | 2.2.5 | ダウンタイムを許容できない基幹の業務で、Amazon Bedrock の容量を事前に確保したいと考え… |
| [ai-costs 問10](../../exercises/ai-costs.md#q10) | 2.2.5 | Amazon SageMaker AI のインスタンスを今後も継続して使う見込みで、確約と引き換えに… |
| [ai-costs 問11](../../exercises/ai-costs.md#q11) | 2.2.5 | Savings Plans の購入を検討している経営層に、伝えるべきリスクはどれですか。 |
| [ai-costs 問12](../../exercises/ai-costs.md#q12) | 2.2.5 | 同じ長いシステムプロンプトと参照資料を、毎回の呼び出しで繰り返し送っています。費用を下げる機能として… |
| [ai-costs 問13](../../exercises/ai-costs.md#q13) | 2.2.5 | 問い合わせを 3 つに分類するだけの単純な処理に、最も高性能で高価なモデルを使っています。評価では、… |
| [ai-costs 問14](../../exercises/ai-costs.md#q14) | 2.2.5 | 部門ごとの AI の費用の責任を明確にし、超過に早く気づける仕組みはどれですか。（2つ選択） |
| [ai-costs 問15](../../exercises/ai-costs.md#q15) | 2.2.5 | RAG のチャットボットの費用を、モデルのトークン料金だけで見積もりました。見積もりの見直しとして最… |
| [ai-costs 問16](../../exercises/ai-costs.md#q16) | 2.2.5 | 回答が長く、月の費用の多くを生成の部分が占めています。モデルの変更なしで費用を下げる一歩として、最も… |

<!-- questions:end -->

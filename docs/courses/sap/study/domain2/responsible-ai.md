# 分野2: 責任ある AI の統制

生成 AI とエージェントの統制を、内容のフィルター、アクセス制御、人の承認の 3 つの層で問います。モデルの判断を信用せず、コードの外で制限することが基本です。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [2.5.1](../../domain2.md#skill-2-5-1) | 生成 AI のコンテンツフィルタリング |
| [2.5.2](../../domain2.md#skill-2-5-2) | 生成 AI とエージェントのアクセス制御 |
| [2.5.3](../../domain2.md#skill-2-5-3) | 人による監督と承認のワークフロー |

## 学習の順番 {#study-order}

1. [Guardrails](../../../../services/ai.md#guardrails)と[フィルターの種類](../../../../services/ai.md#guardrail-filters): 脅威と機能の対応を表で覚えます。
2. [適用の強制と限界](../../../../services/ai.md#guardrail-enforcement)と[組織での強制](../../../../services/genai-apps.md#guardrail-org-enforcement): IAM の条件キーと Bedrock ポリシーの違い、評価されない内容を確認します。
3. [コンテキストグラウンディング](../../../../services/genai-apps.md#contextual-grounding)と[多層防御](../../../../services/genai-apps.md#defense-in-depth): 根拠の確認と、他の対策との組み合わせをつかみます。
4. [ツール利用の認可](../../../../services/ai.md#tool-authorization)と [Policy](../../../../services/genai-apps.md#agentcore-policy): コードの外で制限する方法と、迂回の防ぎ方を理解します。
5. [AgentCore の構成要素と設定](../../../../services/ai.md#agentcore-components)と [IAM のスコープ](../../../../services/ai.md#iam-scope): Identity の 2LO と 3LO、モデルの制限を押さえます。
6. [人の承認](../../../../services/step-functions.md#human-approval)、[コールバック](../../../../services/step-functions.md#wait-for-callback)、[人による確認](../../../../services/genai-apps.md#human-in-the-loop): 待機の仕組みとタイムアウトを確認します。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| Standard の最大実行時間 | 1 年 | 長い承認の待ち |
| Express の最大実行時間 | 5 分 | `waitForTaskToken` は使えない |
| 3 日のタイムアウト | `TimeoutSeconds` 259,200 | `States.Timeout` を `Catch` で捕らえる |
| Lambda durable functions | 最大 1 年 | 待機中のコンピューティング料金なし |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 業務に無関係な話題を止める | 拒否トピック |
| 個人情報の一部を伏せて返す | 機密情報フィルターのマスク |
| 回答が参照文書に基づくかを確認する | コンテキストグラウンディング |
| 回答が論理の規則に沿うかを検証する | Automated Reasoning |
| アプリを変えず、組織で必ず適用する | Organizations の Bedrock ポリシー |
| ガードレールなしの呼び出しを拒否する | `bedrock:GuardrailIdentifier` の条件キー。アプリの変更が必要 |
| ツール結果に仕込まれた指示を止める | アプリで `ApplyGuardrail` を通す |
| ツールの入力値で決定的に制限する | Policy in AgentCore |
| Gateway の迂回を防ぐ | Runtime のリソースベースポリシーで Gateway の実行ロールだけを許可 |
| 利用者の同意で外部 API を呼ぶ | AgentCore Identity の 3LO |
| サービスの権限で外部 API を呼ぶ | AgentCore Identity の 2LO |
| 使えるモデルを組織で制限する | SCP |
| AWS サービスを統合する承認の流れ | Step Functions Standard と `waitForTaskToken` |
| Lambda のコードの中で承認を待つ | Lambda durable functions |

## 引っかかりやすい点 {#traps}

- `guardrailConfig` は `toolResult`、`toolSpec`、`toolUse.input` を評価しません。
- 単語フィルターは完全一致です。言い換えには拒否トピックを使います。
- 金額の制限をプロンプトや拒否トピックに書いても、決定的になりません。
- Policy は Gateway を通る呼び出しにしか効きません。
- `LOG_ONLY` は記録だけです。ブロックするのは `ENFORCE` です。
- すべてに承認を求めると、形だけの承認になります。基準を決めて絞ります。
- SageMaker A2I は新規顧客を受け付けていません。
- コールバックのタスクに期限を付けないと、応答が来るまで待ち続けます。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [responsible-ai 問1](../../exercises/responsible-ai.md#q1) | 2.5.1 | ある銀行は Bedrock で問い合わせ用のチャットを作ります。「投資の助言はしない」という規定があ… |
| [responsible-ai 問2](../../exercises/responsible-ai.md#q2) | 2.5.1 | ある組織の 30 のアカウントで、開発者が各自で Bedrock を呼んでいます。組織のガードレール… |
| [responsible-ai 問3](../../exercises/responsible-ai.md#q3) | 2.5.1 | ある保険会社のチャットは、加入の条件を答えます。条件は「年齢は 18 歳以上かつ 70 歳以下、かつ… |
| [responsible-ai 問4](../../exercises/responsible-ai.md#q4) | 2.5.1 | ある社内エージェントは Converse のツール利用で外部のウェブページを取得し、その内容をツール… |
| [responsible-ai 問5](../../exercises/responsible-ai.md#q5) | 2.5.2 | ある会社のサポートエージェントは、AgentCore Gateway 経由で返金ツールを呼びます。「… |
| [responsible-ai 問6](../../exercises/responsible-ai.md#q6) | 2.5.2 | ある設計では、AgentCore Gateway に Policy を関連付けて、ツール呼び出しの制… |
| [responsible-ai 問7](../../exercises/responsible-ai.md#q7) | 2.5.2 | ある社内エージェントは、外部の SaaS のカレンダーを利用者の代わりに読み書きします。各利用者の同… |
| [responsible-ai 問8](../../exercises/responsible-ai.md#q8) | 2.5.2 | ある組織は、開発の OU で承認済みの基盤モデルだけを Bedrock で呼べるようにします。各アカ… |
| [responsible-ai 問9](../../exercises/responsible-ai.md#q9) | 2.5.3 | ある AI エージェントが本番環境の変更を提案します。実行の前に、運用責任者の承認を待ちます。承認に… |
| [responsible-ai 問10](../../exercises/responsible-ai.md#q10) | 2.5.3 | ある承認のワークフローでは、担当者が 3 日以内に応答しなければ、その要求を却下して記録します。現在… |
| [responsible-ai 問11](../../exercises/responsible-ai.md#q11) | 2.5.3 | ある会社の AI エージェントは 1 日に数万件の返金の要求を処理します。すべてに人の承認を求めた結… |
| [responsible-ai 問12](../../exercises/responsible-ai.md#q12) | 2.5.3 | あるチームのビジネスロジックはすべて Python の Lambda で書かれています。この処理の途… |

<!-- questions:end -->

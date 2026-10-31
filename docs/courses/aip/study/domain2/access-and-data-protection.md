# 分野2: 安全なアクセス

利用者の認証、モデルの権限、ガードレールの強制を組み合わせます。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [2.3.3](../../domain2.md#skill-2-3-3) | 安全なアクセスの枠組み |

## 学習の順番 {#study-order}

1. [IAM のスコープ](../../../../services/ai.md#iam-scope): モデルの ARN とプロファイルの権限を確認します。
2. [適用の強制と限界](../../../../services/ai.md#guardrail-enforcement): 条件キーの動きと限界を押さえます。
3. [Cognito のフェデレーション](../../../../services/cognito.md#federation)と [Bedrock API キー](../../../../services/ai.md#api-keys): 認証の方式を選べるようにします。
4. [ツール利用の認可](../../../../services/ai.md#tool-authorization): AgentCore Identity の 2LO と 3LO の違いを理解します。

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 使えるモデルを絞る | `bedrock:InvokeModel` をモデルの ARN に |
| ガードレールを必須にする | `bedrock:GuardrailIdentifier` |
| 利用者の代わりに外部の API を呼ぶ | AgentCore Identity の 3LO |
| 過剰な権限を探す | IAM Access Analyzer |

## 引っかかりやすい点 {#traps}

- `bedrock:Converse` というアクションはありません。
- クロスリージョン推論では、宛先の各リージョンの基盤モデルの権限も要ります。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [access-and-data-protection 問1](../../exercises/access-and-data-protection.md#q1) | 2.3.3 | あるチームのロールに、承認済みの 2 つのモデルだけを使わせ、呼び出しのたびに指定のガードレールを必… |
| [access-and-data-protection 問2](../../exercises/access-and-data-protection.md#q2) | 2.3.3 | 社内の IdP に登録された従業員が、Web アプリの生成 AI のチャットを使います。ブラウザに … |
| [access-and-data-protection 問3](../../exercises/access-and-data-protection.md#q3) | 2.3.3 | エージェントが利用者の代わりに、社外の SaaS の予定表を読み書きします。利用者ごとの同意が必要で… |
| [access-and-data-protection 問4](../../exercises/access-and-data-protection.md#q4) | 2.3.3 | 本番の Bedrock のロールに bedrock:* が付いたままになっている疑いがあります。実際… |

<!-- questions:end -->

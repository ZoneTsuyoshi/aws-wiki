# 分野5: 内容の処理と FM の統合の問題

`stopReason` と例外から原因を切り分けます。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [5.2.1](../../domain5.md#skill-5-2-1) | 内容の処理の問題 |
| [5.2.2](../../domain5.md#skill-5-2-2) | FM の統合の問題 |

## 学習の順番 {#study-order}

1. [Converse の例](../../../../services/ai.md#converse): `stopReason` の値と対応を覚えます。
2. [エラー処理とスロットリング](../../../../services/ai.md#errors-throttling): 例外ごとの原因を確認します。
3. [CloudWatch のメトリクス](../../../../services/ai.md#bedrock-metrics)と[ストリーミング](../../../../services/ai.md#streaming): 見るところと途中のエラーを押さえます。
4. [アクセスの要求と管理](../../../../services/ai.md#access)と [IAM のスコープ](../../../../services/ai.md#iam-scope): `AccessDeniedException` の切り分けを理解します。

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 応答が途中で切れる | `max_tokens` なら `maxTokens` を増やす |
| 文脈の超過 | `CountTokens` で判定し、履歴を要約 |
| 長い文書の後半が無視される | 構造に合わせて分割 |
| 第三者モデルの初回の 403 | Marketplace の権限 |
| プロファイル経由の 403 | 宛先の基盤モデルの権限 |

## 引っかかりやすい点 {#traps}

- スロットリングは `Invocations` に含まれません。`InvocationThrottles` を見ます。
- ストリームの開始後の失敗はループの中の例外で受けます。
- `ResourceNotFoundException` は ID の誤りです。権限の問題ではありません。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [bedrock-api 問15](../../exercises/bedrock-api.md#q15) | 5.2.1 | 長い議事録の要約で、結論の部分が欠けていると報告されました。エラーはありません。応答のログを見ると … |
| [bedrock-api 問16](../../exercises/bedrock-api.md#q16) | 5.2.1 | 長い会話を続けるチャットで、数十ターンを超えると stopReason に model_contex… |
| [bedrock-api 問17](../../exercises/bedrock-api.md#q17) | 5.2.1 | 数百ページの契約書を 1 回の呼び出しで分析すると、後半の条項が無視されます。文書は長さも構成もまち… |
| [bedrock-api 問18](../../exercises/bedrock-api.md#q18) | 5.2.2 | ある第三者モデルを、新しいアカウントで初めて呼ぶと AccessDeniedException にな… |
| [bedrock-api 問19](../../exercises/bedrock-api.md#q19) | 5.2.2 | 利用者から「たまにエラーになる」と報告があります。ダッシュボードの Invocations は増えて… |
| [bedrock-api 問20](../../exercises/bedrock-api.md#q20) | 5.2.2 | ConverseStream を呼ぶコードは、呼び出しを try で囲んでいますが、ストリームの読み… |
| [bedrock-api 問21](../../exercises/bedrock-api.md#q21) | 5.2.2 | eu の地理的な推論プロファイルで呼び出すと、AccessDeniedException になる場合… |

<!-- questions:end -->

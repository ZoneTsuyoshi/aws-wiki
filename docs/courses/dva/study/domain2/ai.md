# 分野2: AI サービス

C03 で追加されたタスク 2.3 のページです。AI サービスへのアクセス、データの扱い、入出力の制御、エージェント、ログの保護を問います。呼び出し方は[分野1](../domain1/ai.md)、テストや CI/CD の支援は[分野3](../domain3/ai.md)、エラー分析は[分野4](../domain4/ai.md)で扱います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [2.3.1](../../domain2.md#skill-2-3-1) | モデルアクセスと IAM |
| [2.3.2](../../domain2.md#skill-2-3-2) | PrivateLink と学習への利用 |
| [2.3.3](../../domain2.md#skill-2-3-3) | Guardrails |
| [2.3.4](../../domain2.md#skill-2-3-4) | ツールの認可、セッションの分離、人による承認 |
| [2.3.5](../../domain2.md#skill-2-3-5) | 呼び出しログの保護 |

## 学習の順番 {#study-order}

1. [試験範囲と全体像](../../../../services/ai.md#overview): ガードレールの設計などは範囲外で、適用方法が問われることを確認します。
2. [モデルアクセスの現在の動き](../../../../services/ai.md#model-access)と[使わせない方法](../../../../services/ai.md#block-access): 初回呼び出しで有効になる流れと、止め方を覚えます。
3. [IAM のスコープ](../../../../services/ai.md#iam-scope)と [IAM のアクションと条件キー](../../../../services/ai.md#iam-actions): API とアクションの対応、ARN の書き方を押さえます。
4. [VPC エンドポイントでの接続](../../../../services/ai.md#privatelink)と[入出力は学習に使われるか](../../../../services/ai.md#training-use): 経路の保護とデータの利用が別の話であることを理解します。
5. [フィルターの種類](../../../../services/ai.md#guardrail-filters)と[適用の流れ](../../../../services/ai.md#guardrail-flow): フィルターごとのアクションと課金の違いを確認します。
6. [Converse で適用する](../../../../services/ai.md#guardrail-converse)、[ApplyGuardrail](../../../../services/ai.md#apply-guardrail)、[適用の強制と限界](../../../../services/ai.md#guardrail-enforcement): 評価される内容とされない内容を見分けます。
7. [ツール利用の認可](../../../../services/ai.md#tool-authorization)、[セッションの分離](../../../../services/ai.md#session-isolation)、[人による承認](../../../../services/ai.md#human-in-the-loop): 実行の時点で制御する方法を学びます。
8. [モデル呼び出しログ](../../../../services/ai.md#invocation-logging)と [CloudWatch Logs のデータ保護](../../../../services/ai.md#cloudwatch-data-protection): Guardrails のマスクがログに効かないことを押さえます。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| 初回の自動有効化 | 最大 15 分 | `PENDING` の間は `AccessDeniedException` |
| Bedrock の短期 API キー | 最大 12 時間 | 長期キーは検証のみ |
| 不正利用検知の保持 | 一部のモデルで最大 30 日 | 学習には使わない |
| エンドポイントのアイドルタイムアウト | 350 秒（固定） | 長い呼び出しは TCP キープアライブ |
| 拒否トピック | 1 ガードレールに 30 個 | |
| 正規表現 | パターン 500 文字 | 先読みと後読みは不可 |
| Runtime のセッション | 既定でアイドル 15 分、最大 8 時間 | セッション ID は 33 文字以上 |
| 呼び出しログ | 既定は無効。本文は 100 KB まで | 大きい本文は S3 へ |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 特定のモデルを組織全体で禁止する | SCP や IAM で `bedrock:InvokeModel` と `bedrock:InvokeModelWithResponseStream` を拒否する |
| `Converse` を呼ぶロールの権限 | `bedrock:InvokeModel`。ストリームは `bedrock:InvokeModelWithResponseStream` |
| インターネットを通さず Bedrock を呼ぶ | `bedrock-runtime` のインターフェイス VPC エンドポイント |
| 入出力が学習に使われないか確認する | Bedrock は使わない。Q Developer の Free Tier（新規作成は 2026-05-15 に停止）や Kiro の個人向けは使われる場合があり、オプトアウトできる |
| PII を隠して処理を続ける | 機密情報フィルターの `ANONYMIZE` |
| ジェイルブレイクを防ぐ | コンテンツフィルターのプロンプト攻撃。`InvokeModel` では入力タグが必須 |
| ガードレールの使用を強制する | `bedrock:GuardrailIdentifier` 条件キー |
| Bedrock 以外のモデルやツール結果を検査する | `ApplyGuardrail` |
| ツール呼び出しをコードの外で制御する | AgentCore Gateway と Policy。既定は拒否で `forbid` が優先 |
| 重要な操作の前に人が承認する | 新規は AgentCore のインライン関数ツールと時間的ポリシー。Agents Classic（2026-07-30 から新規顧客を受け付けていない）はユーザー確認か制御の返却 |
| 呼び出しログの PII を隠す | CloudWatch Logs のデータ保護ポリシー。S3 はバケットポリシーと SSE-KMS で保護する |
| 呼び出しログに本文を残したくない | `textDataDeliveryEnabled` などを `false` にする |

## 引っかかりやすい点 {#traps}

- `aws-marketplace:Subscribe` の拒否では初回呼び出しを止められません。自動で有効化されるためです。
- `bedrock:Converse` というアクションはありません。書いても効きません。
- 呼び出しログの `input` は、ガードレールが介入しても元のまま残ります。トレースにも元の値が入るので、通常のアプリログに書きません。
- `guardrailConfig` は `toolResult`、`toolSpec`、`toolUse.input` を評価しません。ツール結果のインジェクションは `ApplyGuardrail` やアプリ側で確認します。
- 本番で `DRAFT` を指定すると、編集がそのまま本番に反映されます。番号付きの版を使います。
- AgentCore はユーザーとセッション ID の対応を強制しません。バックエンドで管理し、Memory の `actorId` も利用者ごとに分けます。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [ai 問6](../../exercises/ai.md#q6) | 2.3.2 | アプリは EU のお客様のデータを扱い、処理を EU 域内に留める要件があります。一方で、単一リージ… |
| [ai 問7](../../exercises/ai.md#q7) | 2.3.1 | 推論プロファイル経由で呼ぶロールに、プロファイルの ARN だけを許可したところ、AccessDen… |
| [ai 問11](../../exercises/ai.md#q11) | 2.3.5 | bedrock-runtime の呼び出しログを有効にします。監査の要件で、本文は S3 に残さず、… |
| [ai 問12](../../exercises/ai.md#q12) | 2.3.3 | ガードレールの設定について、正しい説明はどれですか。（2つ選択） |
| [ai 問13](../../exercises/ai.md#q13) | 2.3.3 | 検索結果を根拠に回答するアプリで、根拠にない情報を含む応答をブロックしたいと考えています。ガードレー… |
| [ai 問14](../../exercises/ai.md#q14) | 2.3.3 | 本番のアプリの guardrailConfig に guardrailVersion: "DRAFT… |
| [ai 問16](../../exercises/ai.md#q16) | 2.3.2 | プライベートサブネットのアプリから、インターネットを経由せず Converse を呼びます。セキュリ… |
| [ai 問17](../../exercises/ai.md#q17) | 2.3.4 | AgentCore Runtime で動くエージェントで、利用者が 30 分おきに質問するたびに、メ… |
| [ai 問18](../../exercises/ai.md#q18) | 2.3.4 | AgentCore Gateway に AWS の IAM 認証で接続するクライアントのポリシーに、… |
| [ai 問22](../../exercises/ai.md#q22) | 2.3.1 | アカウントで Anthropic のモデルを初めて使います。bedrock-runtime の Co… |
| [ai 問23](../../exercises/ai.md#q23) | 2.3.1 | セキュリティ担当者は、特定の基盤モデルを組織のどのアカウントでも使わせないようにしたいと考えています… |
| [ai 問24](../../exercises/ai.md#q24) | 2.3.4 | Bedrock Agents のアクショングループに注文を取り消す関数 cancelOrder があ… |
| [ai 問25](../../exercises/ai.md#q25) | 2.3.5 | Bedrock のガードレールで応答のメールアドレスをマスクし、モデル呼び出しログを CloudWa… |
| [ai 問26](../../exercises/ai.md#q26) | 2.3.5 | モデル呼び出しログを S3 に送っています。機密情報を守るためにバケットの既定の暗号化を SSE-K… |
| [ai 問39](../../exercises/ai.md#q39) | 2.3.2 | 法務部門から、Bedrock に送るプロンプトと応答の扱いについて質問がありました。アプリは bed… |

<!-- questions:end -->

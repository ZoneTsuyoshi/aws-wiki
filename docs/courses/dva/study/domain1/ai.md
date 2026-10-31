# 分野1: AI

分野1では、Kiro を使った開発と、アプリから Bedrock を呼ぶコードを問われます。アクセス制御や Guardrails は[分野2](../domain2/ai.md)、テストと CI/CD での活用は[分野3](../domain3/ai.md)、調査と最適化は[分野4](../domain4/ai.md)で扱います。モデルの選定、プロンプトの設計、RAG の設計は試験の範囲外です。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [1.1.9](../../domain1.md#skill-1-1-9) | AI による開発支援ツール |
| [1.1.10](../../domain1.md#skill-1-1-10) | マネージド AI サービスの組み込み |

## 学習の順番 {#study-order}

1. [試験範囲と全体像](../../../../services/ai.md#overview): 対象のサービスと、対象外のサービスを確認します。
2. [Kiro](../../../../services/ai.md#kiro)、[Steering の読み込みモード](../../../../services/ai.md#steering-modes)、[Hooks の設定](../../../../services/ai.md#hooks-settings): Specs、Steering、Hooks、MCP の役割を区別します。
3. [Amazon Q Developer の現状と Kiro との関係](../../../../services/ai.md#q-developer)、[スキル例ごとの対応](../../../../services/ai.md#kiro-vs-q): 公式スキルの例と機能の対応を確認します。
4. [API の選び方](../../../../services/ai.md#invoke-apis)、[Converse の全パラメータ](../../../../services/ai.md#converse-params): API と IAM アクションの対応と、パラメータの置き場所を覚えます。
5. [ツール利用の流れ](../../../../services/ai.md#tool-use-flow): `toolUse` と `toolResult` のやり取りを理解します。
6. [ストリーミング](../../../../services/ai.md#streaming)、[ストリームのイベント](../../../../services/ai.md#stream-events): イベントの順番と途中のエラーの扱いを学びます。
7. [エラー処理とスロットリング](../../../../services/ai.md#errors-throttling)、[クォータとトークンの数え方](../../../../services/ai.md#quotas-detail): 再試行してよいエラーと、`max_tokens` の影響を計算できるようにします。
8. [スループットの選択肢](../../../../services/ai.md#throughput-options)、[Knowledge Bases を呼ぶ](../../../../services/ai.md#knowledge-bases): 処理量に応じた選び方と、検索の呼び方を確認します。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| `maxTokens` の既定 | モデルの最大値 | 省略するとクォータを多く押さえます |
| `temperature`、`topP` | 0〜1 | |
| `toolChoice` の既定 | `auto` | 必ず使わせるなら `any` か `tool` です |
| `ModelNotReadyException` | SDK が最大 5 回再試行 | |
| `numberOfResults` | 既定 5、1〜100 | Knowledge Bases の検索件数です |
| バッチの `timeoutDurationInHours` | 24〜168 | |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 仕様を先に作ってから実装させる | Kiro の Specs を使います |
| プロジェクトの規約を AI に常に伝える | Kiro の Steering を使います。特定のファイルを扱うときだけなら `inclusion: fileMatch` にします |
| エージェントのファイル保存を契機にテストやリントを動かす | Kiro の Hooks を使います |
| モデルを差し替えやすくしたい | `Converse` を使います |
| `top_k` を `Converse` で渡す | `additionalModelRequestFields` に入れます |
| 使用トークン数を `ConverseStream` で記録する | `metadata` イベントの `usage` を読みます |
| `ThrottlingException`（429）が出る | 指数バックオフとジッターで再試行し、`max_tokens` を見直し、クォータの引き上げを検討します |
| `ServiceUnavailableException`（503）が出る | クォータの問題ではありません。再試行し、クロスリージョン推論も検討します |
| 入力 1,000、`max_tokens` 8,000 のリクエスト | 開始時に 9,000 がクォータから差し引かれ、未使用分は完了時に戻ります |
| 夜間の大量処理を安く行う | バッチを使います。完了は EventBridge で受けます |

## 引っかかりやすい点 {#traps}

- `ConverseStream` に必要なのは `bedrock:InvokeModelWithResponseStream` です。`Converse` は `bedrock:InvokeModel` です。
- ストリームの途中のエラーは、HTTP 200 の後にイベントで届きます。ループの中で例外を処理します。
- 短い入力でもすぐスロットリングするなら、`maxTokens` の省略や過大な値を疑います。
- Kiro の File Save の Hook は、エージェントによる変更が対象で、手動編集では動きません。
- DVA-C03 の対象一覧に Q Developer はなく、Kiro が載っています。Quick Sight、SageMaker AI、Polly、Rekognition も対象外です。
- 推論プロファイルと Provisioned Throughput は併用できません。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [ai 問1](../../exercises/ai.md#q1) | 1.1.10 | アプリは Converse で複数のモデルを呼びます。特定のモデルだけが持つパラメータ top_k … |
| [ai 問2](../../exercises/ai.md#q2) | 1.1.10 | Converse で inferenceConfig を省略し、入力は短いにもかかわらず、呼び出しが… |
| [ai 問3](../../exercises/ai.md#q3) | 1.1.10 | 出力トークンの消費率が 5 倍のモデルで、入力 1,000 トークン、max_tokens 8,00… |
| [ai 問4](../../exercises/ai.md#q4) | 1.1.10 | Converse のツール利用について、正しい説明はどれですか。（2つ選択） |
| [ai 問5](../../exercises/ai.md#q5) | 1.1.10 | ConverseStream を使うチャットで、請求の集計のために使用トークン数を記録したいと考えて… |
| [ai 問8](../../exercises/ai.md#q8) | 1.1.10 | 数十万件の文書を夜間に要約します。応答はすぐに必要ありません。Bedrock の機能のうち、最も適切… |
| [ai 問9](../../exercises/ai.md#q9) | 1.1.10 | Bedrock のサービスティアの説明として、正しいものはどれですか。（2つ選択） |
| [ai 問15](../../exercises/ai.md#q15) | 1.1.10 | Knowledge Bases の Retrieve で、最大 10 件を、メタデータの dept … |
| [ai 問19](../../exercises/ai.md#q19) | 1.1.9 | Kiro のワークスペースで、テストのファイルを扱うときだけ読み込まれる規約を Steering で… |
| [ai 問20](../../exercises/ai.md#q20) | 1.1.9 | 開発チームは Kiro の Hook で、エージェントがファイルを保存したときに npx eslin… |
| [ai 問21](../../exercises/ai.md#q21) | 1.1.9 | チームは Kiro で新機能を作ります。コードを生成させる前に要件と設計をレビューして合意し、その後… |

<!-- questions:end -->

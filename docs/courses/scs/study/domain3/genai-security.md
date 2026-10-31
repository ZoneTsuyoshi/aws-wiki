# 分野3: 生成 AI アプリの保護

C03 で追加された範囲です。OWASP Top 10 for LLM のリスクを AWS の統制に対応させ、モデルの判断に頼らない方法を選ぶ力を問います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [3.2.7](../../domain3.md#skill-3-2-7) | 生成 AI アプリの保護 |

## 学習の順番 {#study-order}

1. [スキル 3.2.7](../../domain3.md#skill-3-2-7): OWASP の 10 項目と AWS の対策の表を確認します。
2. [Guardrails のフィルター](../../../../services/ai.md#guardrail-filters): 各フィルターが何を見るかを覚えます。
3. [適用の強制と限界](../../../../services/ai.md#guardrail-enforcement): IAM の条件キーの限界と、評価されないフィールドを押さえます。
4. [組織での強制](../../../../services/genai-apps.md#guardrail-org-enforcement): Bedrock ポリシーと IAM の違いを比べます。
5. [コンテキストグラウンディング](../../../../services/genai-apps.md#contextual-grounding)と [Automated Reasoning](../../../../services/genai-apps.md#automated-reasoning): 誤情報への対策を使い分けます。
6. [エージェントの保護](../../../../services/ai.md#agent-security)と [Policy](../../../../services/genai-apps.md#agentcore-policy): 実行の時点での統制を確認します。
7. [多層防御](../../../../services/genai-apps.md#defense-in-depth): 入口から応答までの統制の位置をつかみます。

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| ツール結果に仕込まれた指示（LLM01） | `toolResult` は評価されない。`ApplyGuardrail` に通す |
| 応答の個人情報を隠す（LLM02） | 機密情報フィルターの `ANONYMIZE` |
| 許可していないモデルを使わせない（LLM03） | IAM で許可するモデルを限定 |
| 文書の改ざん（LLM04） | データソースの権限とバージョニング |
| 出力をそのまま後段に渡している（LLM05） | JSON Schema と業務ルールで検証。パラメータ化したクエリ |
| エージェントの権限が大きい（LLM06） | 最小権限のロール、AgentCore Policy、人の承認 |
| プロンプトの秘密が漏れた（LLM07） | 秘密をプロンプトから外す。検出は補助 |
| 別テナントの文書が混ざる（LLM08） | アクセス制御とメタデータの絞り込みをサーバー側で強制 |
| 文書にない内容を答える（LLM09） | コンテキストグラウンディング |
| 規則に論理的に反する回答を防ぐ（LLM09） | Automated Reasoning |
| 費用の搾取（LLM10） | レート制限と GuardDuty の AI Protection |
| 指定し忘れても必ず適用する | Organizations の Bedrock ポリシー |
| 入力タグで評価を狭められたくない | 選択的コンテンツガードの制御を `comprehensive` にする |

## 引っかかりやすい点 {#traps}

- `bedrock:GuardrailIdentifier` の条件付きのロールで `RetrieveAndGenerate` や `InvokeAgent` を呼ぶと、内部の呼び出しのために拒否されることがあります。
- IAM の条件で強制しても、入力タグで入力の評価を避けられます。応答には常に適用されます。
- `toolUse.input` の個人情報はマスクされません。呼び出しログの `input` にも元の内容が残ります。
- Bedrock ポリシーは宣言型です。SCP のように付けたものがそれぞれ効くのではなく、1 つの有効なポリシーに解決されます。`DescribeEffectivePolicy` で確認します。
- Automated Reasoning は組織の強制には含められません。
- AgentCore Policy は Gateway を通る呼び出しにしか効きません。Runtime への直接の呼び出しを禁止します。
- Prompt Leakage の検出は Standard の階層だけです。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [genai-security 問1](../../exercises/genai-security.md#q1) | 3.2.7 | 社内の問い合わせエージェントは、Converse API のツール利用で外部のチケットを読みます。g… |
| [genai-security 問2](../../exercises/genai-security.md#q2) | 3.2.7 | セキュリティチームは、アプリのロールに次のポリシーを付けました。bedrock:InvokeMode… |
| [genai-security 問3](../../exercises/genai-security.md#q3) | 3.2.7 | 組織の全アカウントで、Bedrock のモデル呼び出しにガードレールを適用します。呼び出し側の開発者… |
| [genai-security 問4](../../exercises/genai-security.md#q4) | 3.2.7 | ルートに汎用のガードレール、金融部門の OU に厳しいガードレールを Organizations の… |
| [genai-security 問5](../../exercises/genai-security.md#q5) | 3.2.7 | 返金エージェントが、指示の注入によって高額の返金ツールを呼ぶリスクが指摘されました。OWASP の過… |
| [genai-security 問6](../../exercises/genai-security.md#q6) | 3.2.7 | AgentCore Gateway に Policy を関連付けて、ツール呼び出しを制御しました。し… |
| [genai-security 問7](../../exercises/genai-security.md#q7) | 3.2.7 | サポート要約アプリで、Guardrails の機密情報フィルターの ANONYMIZE を使い、応答… |
| [genai-security 問8](../../exercises/genai-security.md#q8) | 3.2.7 | Bedrock の公開チャットで、高額な入力を大量に送られて費用が急増するリスク（LLM10）を検討… |
| [genai-security 問9](../../exercises/genai-security.md#q9) | 3.2.7 | 人事の規程に関する回答を生成するアプリがあります。回答が規程の条件（勤続年数と休暇の日数の規則）に論… |
| [genai-security 問10](../../exercises/genai-security.md#q10) | 3.2.7 | あるアプリのシステムプロンプトに、社内 API のキーと内部の処理手順が書かれています。ペネトレーシ… |
| [genai-security 問11](../../exercises/genai-security.md#q11) | 3.2.7 | マルチテナントの RAG アプリのベクトル検索で、別のテナントの文書の断片が応答に混ざりました。LL… |
| [genai-security 問12](../../exercises/genai-security.md#q12) | 3.2.7 | モデルの出力をそのまま SQL に組み立ててデータベースで実行する社内ツールがあります。監査で不適切… |
| [genai-security 問13](../../exercises/genai-security.md#q13) | 3.2.7 | ナレッジベース用の S3 バケットに、誰かが虚偽の手順書を上書きした痕跡が見つかりました。今後の汚染… |

<!-- questions:end -->

# 分野3: アクセス制御とデータの保護

閉域の接続、機密情報の扱い、組織全体の統制を扱います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [3.2.1](../../domain3.md#skill-3-2-1) | 保護された AI 環境 |
| [3.2.2](../../domain3.md#skill-3-2-2) | 機密情報を守る仕組み |
| [3.3.3](../../domain3.md#skill-3-3-3) | 組織のガバナンス |

## 学習の順番 {#study-order}

1. [VPC エンドポイントでの接続](../../../../services/ai.md#privatelink)と[エンドポイントポリシー](../../../../services/networking.md#endpoint-policies): API ごとのエンドポイントと `aws:SourceVpce` を確認します。
2. [Lake Formation](../../../../services/data-engineering.md#lake-formation): 列と行の権限を理解します。
3. [Macie](../../../../services/threat-detection.md#macie)と[機密情報フィルター](../../../../services/ai.md#guardrail-policy-settings): 段階ごとの手段を区別します。
4. [入出力は学習に使われるか](../../../../services/ai.md#training-use): 学習と保持の違いを押さえます。
5. [モデル呼び出しログ](../../../../services/ai.md#invocation-logging)と [CloudWatch Logs のデータ保護](../../../../services/ai.md#cloudwatch-data-protection): ログの保護の限界を確認します。
6. [組織での強制](../../../../services/genai-apps.md#guardrail-org-enforcement)と[使わせない方法](../../../../services/ai.md#block-access): 組織の統制の手段を整理します。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| 不正利用検知の保持 | 最大 30 日（一部のモデル） | 提供者とは共有しない |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| `Retrieve` と `Converse` を閉域で | `bedrock-agent-runtime` と `bedrock-runtime` |
| エンドポイント経由に限定する | `aws:SourceVpce` |
| S3 の個人情報を探す | Macie |
| ログのマスク | CloudWatch Logs のデータ保護 |
| 呼び出し側の指定なしで全社に適用 | Organizations の Bedrock ポリシー |
| 特定のモデルを止める | SCP で `bedrock:InvokeModel` 系を拒否 |

## 引っかかりやすい点 {#traps}

- Guardrails の `ANONYMIZE` は呼び出しログの `input` を守りません。
- データ保護ポリシーは S3 に送ったログに効かず、適用前のログもマスクしません。
- `aws-marketplace:Subscribe` の拒否では初回の呼び出しを止められません。
- 組織とアプリのガードレールは両方適用され、厳しい方が優先されます。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [access-and-data-protection 問5](../../exercises/access-and-data-protection.md#q5) | 3.2.1 | インターネットへの経路がないプライベートサブネットの ECS から、Knowledge Bases … |
| [access-and-data-protection 問6](../../exercises/access-and-data-protection.md#q6) | 3.2.1 | VPC エンドポイント経由で Bedrock を呼ぶように変更したところ、aws:SourceIp … |
| [access-and-data-protection 問7](../../exercises/access-and-data-protection.md#q7) | 3.2.1 | FM の学習の外で、Athena からの分析と、要約に渡すデータの取得で、部署ごとに見える列と行を分… |
| [access-and-data-protection 問8](../../exercises/access-and-data-protection.md#q8) | 3.2.2 | RAG に取り込む S3 の文書に個人情報が混ざっていないかを、取り込みの前に大量に調べます。さらに… |
| [access-and-data-protection 問9](../../exercises/access-and-data-protection.md#q9) | 3.2.2 | 法務部門から、Bedrock の入出力の扱いについて質問がありました。「モデルの学習に使われないなら… |
| [access-and-data-protection 問10](../../exercises/access-and-data-protection.md#q10) | 3.2.2 | 監査で、Bedrock の呼び出しログに顧客のメールアドレスが残っていると指摘されました。Guard… |
| [access-and-data-protection 問11](../../exercises/access-and-data-protection.md#q11) | 3.2.2 | 呼び出しログを CloudWatch Logs と S3 の両方に送っています。CloudWatch… |
| [access-and-data-protection 問12](../../exercises/access-and-data-protection.md#q12) | 3.3.3 | 全社の Bedrock の呼び出しに同じ安全策を適用します。アプリの多くは既存のコードで、guard… |
| [access-and-data-protection 問13](../../exercises/access-and-data-protection.md#q13) | 3.3.3 | 組織のガードレールでは投資助言を HIGH で止めています。アプリのガードレールでは同じ項目を LO… |
| [access-and-data-protection 問14](../../exercises/access-and-data-protection.md#q14) | 3.3.3 | 全社で、特定の第三者モデルの利用を止め、推論を EU の中に限定します。Marketplace の … |
| [access-and-data-protection 問15](../../exercises/access-and-data-protection.md#q15) | 3.3.3 | 全社の生成 AI のガバナンス方針を作りました。しかし、「誰が最終責任を持つのか」「どの用途がどの統… |

<!-- questions:end -->

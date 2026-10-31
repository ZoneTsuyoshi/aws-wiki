# 分野5: AI システムのセキュリティ

要件に合うサービスを選びます。ログの区別とデータの保護の技術が要点です。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [5.1.1](../../domain5.md#obj-5-1-1) | AI システムを保護するサービスと機能 |
| [5.1.3](../../domain5.md#obj-5-1-3) | 安全なデータエンジニアリングのベストプラクティス |
| [5.1.4](../../domain5.md#obj-5-1-4) | AI システムのセキュリティとプライバシーの考慮点 |

## 学習の順番 {#study-order}

1. [AI システムを守るサービス](../../../../services/ai-fundamentals.md#security-services): 目的とサービスの表を覚えます。
2. [責任共有モデル](../../../../services/ai-fundamentals.md#shared-responsibility): AWS と利用者の担当を確認します。
3. [VPC エンドポイントでの接続](../../../../services/ai.md#privatelink)と[入出力は学習に使われるか](../../../../services/ai.md#training-use): 通信経路の保護と、データの利用を区別します。
4. [AgentCore の構成要素と設定](../../../../services/ai.md#agentcore-components)と[Policy](../../../../services/genai-apps.md#agentcore-policy): エージェントの ID と認可の役割を確認します。
5. [Data Quality](../../../../services/data-engineering.md#glue-data-quality)と[AWS Lake Formation](../../../../services/data-engineering.md#lake-formation)と[Object Lock](../../../../services/s3.md#object-lock): 品質、アクセス、完全性の手段を押さえます。
6. [サニタイズとマスキング](../../../../services/secrets.md#sanitization-masking): マスキングの考え方を確認します。
7. [モデル呼び出しログ](../../../../services/ai.md#invocation-logging)と[イベントの種類](../../../../services/observability.md#cloudtrail-events): 2 つのログの違いを覚えます。
8. [Inspector](../../../../services/threat-detection.md#inspector)と[多層防御](../../../../services/genai-apps.md#defense-in-depth): 脆弱性の管理と多層防御を確認します。

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| S3 の PII を見つける | Macie |
| インターネットを経由しない | PrivateLink |
| 保存時の暗号化を自社の鍵で | KMS |
| エージェントの資格情報 | AgentCore Identity |
| ツール呼び出しの認可 | Policy in AgentCore |
| 一部を隠す | マスキング |
| 別の値に置き換える | トークン化 |
| ノイズを加える | 差分プライバシー |
| 列単位のアクセス制御 | Lake Formation |
| 誰が操作したか | CloudTrail |
| プロンプトの本文 | モデル呼び出しログ（既定は無効） |
| コンテナイメージの脆弱性 | Inspector |

## 引っかかりやすい点 {#traps}

- Guardrails でブロックした内容も、モデル呼び出しログには平文で残ります。ログ自体を保護します。
- 文書やツールの結果に指示が仕込まれる間接プロンプトインジェクションもあります。
- GuardDuty、WAF、Shield、Security Hub は範囲外の一覧に載っています。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [ai-security 問1](../../exercises/ai-security.md#q1) | 5.1.1 | FM の学習データを入れる S3 バケットに、顧客の個人情報が含まれていないかを確認します。適切なサ… |
| [ai-security 問2](../../exercises/ai-security.md#q2) | 5.1.1 | VPC 内のアプリから、インターネットを経由せずに Bedrock を呼びたいと考えています。適切な… |
| [ai-security 問3](../../exercises/ai-security.md#q3) | 5.1.1 | 特定のチームだけが特定のモデルを呼べるようにしたいと考えています。適切な手段はどれですか。 |
| [ai-security 問4](../../exercises/ai-security.md#q4) | 5.1.1 | エージェントが外部の API を呼ぶときの ID と資格情報を、安全に管理したいと考えています。適切… |
| [ai-security 問5](../../exercises/ai-security.md#q5) | 5.1.1 | エージェントの返金ツールを「金額が 10,000 円以下のときだけ許可」にしたいと考えています。プロ… |
| [ai-security 問6](../../exercises/ai-security.md#q6) | 5.1.1 | 自社で鍵を管理して、保存時のデータを暗号化したいと考えています。適切なサービスはどれですか。 |
| [ai-security 問7](../../exercises/ai-security.md#q7) | 5.1.3 | 学習データの欠損、重複、誤りをルールで測りたいと考えています。適切なサービスを選んでください。（2つ… |
| [ai-security 問8](../../exercises/ai-security.md#q8) | 5.1.3 | クレジットカード番号を ****-1234 と表示します。このプライバシー強化技術はどれですか。 |
| [ai-security 問9](../../exercises/ai-security.md#q9) | 5.1.3 | 集計結果に調整したノイズを加えて、個人の情報を推定しにくくします。この技術はどれですか。 |
| [ai-security 問10](../../exercises/ai-security.md#q10) | 5.1.3 | データレイクの学習データに、列単位の細かいアクセス権を設定します。適切なサービスはどれですか。 |
| [ai-security 問11](../../exercises/ai-security.md#q11) | 5.1.3 | 学習データが改ざんされないよう、一定期間は上書きも削除もできないようにしたいと考えています。適切な機… |
| [ai-security 問12](../../exercises/ai-security.md#q12) | 5.1.4 | セキュリティ部門が、誰が Bedrock のガードレールを変更したかと、モデルに送られたプロンプトの… |
| [ai-security 問13](../../exercises/ai-security.md#q13) | 5.1.4 | Bedrock のモデル呼び出しログの説明として正しいものを選んでください。（2つ選択） |
| [ai-security 問14](../../exercises/ai-security.md#q14) | 5.1.4 | エージェントが動くコンテナイメージの既知の脆弱性を見つけます。適切なサービスはどれですか。 |
| [ai-security 問15](../../exercises/ai-security.md#q15) | 5.1.4 | 利用者が普通の質問をしただけなのに、RAG で取得した文書の中に仕込まれた指示にモデルが従いました。… |
| [ai-security 問16](../../exercises/ai-security.md#q16) | 5.1.4 | AI アプリのネットワークを分離して、基盤を保護します。適切な組み合わせはどれですか。 |
| [ai-security 問17](../../exercises/ai-security.md#q17) | 5.1.4 | 応答に含まれる機密情報の漏えいを防ぎ、攻撃的な内容も止めたいと考えています。適切な対策はどれですか。 |

<!-- questions:end -->

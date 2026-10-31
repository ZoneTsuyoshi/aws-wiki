# 分野5: ガバナンスとコンプライアンス

サービスの役割の区別と、Scoping Matrix のスコープの判定が中心です。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [5.1.2](../../domain5.md#obj-5-1-2) | 出典の明示とデータの出所の記録 |
| [5.2.1](../../domain5.md#obj-5-2-1) | ガバナンスと規制への準拠を支えるサービス |
| [5.2.2](../../domain5.md#obj-5-2-2) | データガバナンスの戦略 |
| [5.2.3](../../domain5.md#obj-5-2-3) | ガバナンスの手順 |

## 学習の順番 {#study-order}

1. [統治の仕組み](../../../../services/genai-apps.md#governance-controls): 出典の明示とデータ系譜の手段を確認します。
2. [Data Catalog](../../../../services/data-engineering.md#glue-data-catalog)と[Model Cards](../../../../services/sagemaker.md#model-cards): カタログとモデルの文書化を押さえます。
3. [Config と CloudTrail の違い](../../../../services/governance.md#config-vs-cloudtrail): 「設定」と「操作」の違いを覚えます。
4. [AWS Artifact](../../../../services/cloud-foundations.md#artifact)と[Trusted Advisor](../../../../services/cloud-foundations.md#trusted-advisor)と[Inspector](../../../../services/threat-detection.md#inspector): それぞれの役割を区別します。
5. [ライフサイクル](../../../../services/s3.md#lifecycle)と[データの保持](../../../../services/storage.md#retention)と[CloudWatch の生成 AI オブザーバビリティ](../../../../services/genai-apps.md#genai-observability): 保持、削除、観察の手段を確認します。
6. [Generative AI Security Scoping Matrix](../../../../services/ai-fundamentals.md#scoping-matrix): 5 つのスコープを例で覚えます。
7. [シャドー AI](../../../../services/ai-fundamentals.md#shadow-ai)と[役割と責任](../../../../services/ai-fundamentals.md#governance-roles): 方針と体制の考え方を確認します。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| スコープ 1 | 消費者向けアプリ | 公開のチャットサービス |
| スコープ 2 | 企業向けアプリ | 第三者の SaaS に組み込まれた AI |
| スコープ 3 | 事前学習済みモデル | Bedrock の FM で自社のアプリ |
| スコープ 4 | ファインチューニング | FM を自社のデータで調整 |
| スコープ 5 | 自社で学習 | ゼロから学習 |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| AWS の SOC レポートを入手する | Artifact |
| 設定が基準に合っているか | Config |
| 誰がいつ操作したか | CloudTrail |
| 環境を点検して推奨を受ける | Trusted Advisor |
| 回答の根拠を示す | Knowledge Bases の引用 |
| データの出所と加工の履歴 | データ系譜 |
| データを EU の外で処理しない | `eu` の推論プロファイル |
| 期限後のデータを自動で消す | S3 ライフサイクル |
| 把握していない AI ツールの利用 | シャドー AI。分類を公開し代替を用意する |

## 引っかかりやすい点 {#traps}

- Artifact の文書は AWS 側のものです。自社のシステムの準拠は別に示します。
- Object Lock は削除を防ぐ機能で、自動で消す機能ではありません。
- 番号が大きいほど、自社の制御と責任が大きくなります。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [governance 問1](../../exercises/governance.md#q1) | 5.1.2 | 監査で「この回答の根拠はどの文書か」と問われました。すぐ示せるようにする仕組みはどれですか。 |
| [governance 問2](../../exercises/governance.md#q2) | 5.1.2 | データの出所と加工の履歴を記録する考え方はどれですか。 |
| [governance 問3](../../exercises/governance.md#q3) | 5.1.2 | 社内のどのデータがどこにあるかを登録して、探せるようにしたいと考えています。適切な機能はどれですか。 |
| [governance 問4](../../exercises/governance.md#q4) | 5.1.2 | 「このモデルはどのデータで学習したか」という監査の質問に答えられるようにします。適切な組み合わせを選… |
| [governance 問5](../../exercises/governance.md#q5) | 5.2.1 | 監査人から、AWS のデータセンターの SOC レポートを求められました。入手先はどれですか。 |
| [governance 問6](../../exercises/governance.md#q6) | 5.2.1 | 学習データの S3 バケットが暗号化されているかを、ルールで継続的に評価します。適切なサービスはどれ… |
| [governance 問7](../../exercises/governance.md#q7) | 5.2.1 | 誰がいつ Bedrock のカスタムモデルを削除したかを調べます。適切なサービスはどれですか。 |
| [governance 問8](../../exercises/governance.md#q8) | 5.2.1 | コスト、セキュリティ、耐障害性の観点で環境を点検し、推奨を受けたいと考えています。適切なサービスはど… |
| [governance 問9](../../exercises/governance.md#q9) | 5.2.1 | AWS Artifact の文書の説明として正しいものはどれですか。 |
| [governance 問10](../../exercises/governance.md#q10) | 5.2.2 | 学習データの保持の要件に合わせて、一定期間が過ぎた S3 のデータを自動で削除します。適切な機能はど… |
| [governance 問11](../../exercises/governance.md#q11) | 5.2.2 | データを日本の外で処理してはいけない規定があります。どのデータガバナンスの戦略に関わりますか。 |
| [governance 問12](../../exercises/governance.md#q12) | 5.2.2 | 生成 AI アプリの呼び出し、エージェント、ナレッジベースの利用状況と品質の傾向を見続けます。適切な… |
| [governance 問13](../../exercises/governance.md#q13) | 5.2.2 | データガバナンスの戦略として適切なものを選んでください。（2つ選択） |
| [governance 問14](../../exercises/governance.md#q14) | 5.2.3 | 企業が Bedrock の FM を自社の過去の問い合わせでファインチューニングして使います。Gen… |
| [governance 問15](../../exercises/governance.md#q15) | 5.2.3 | 第三者の業務 SaaS に組み込まれた AI 機能を使います。Scoping Matrix のどのス… |
| [governance 問16](../../exercises/governance.md#q16) | 5.2.3 | Scoping Matrix の番号が大きくなると、どう変わりますか。 |
| [governance 問17](../../exercises/governance.md#q17) | 5.2.3 | 社員が会社の把握していない AI ツールを使っています。ガバナンスの手順として適切なものはどれですか… |
| [governance 問18](../../exercises/governance.md#q18) | 5.2.3 | AI の用途の見直しの頻度を決めます。適切な考え方はどれですか。 |
| [governance 問19](../../exercises/governance.md#q19) | 5.2.3 | ガバナンスの手順として適切なものを選んでください。（2つ選択） |

<!-- questions:end -->

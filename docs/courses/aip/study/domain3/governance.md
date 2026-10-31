# 分野3: ガバナンスと責任ある AI

文書化、データの追跡、継続的な監視、透明性と公平性を扱います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [3.3.1](../../domain3.md#skill-3-3-1) | 規制に対応する枠組み |
| [3.3.2](../../domain3.md#skill-3-3-2) | データソースの追跡 |
| [3.3.4](../../domain3.md#skill-3-3-4) | 継続的な監視と高度な統制 |
| [3.4.1](../../domain3.md#skill-3-4-1) | 透明性 |
| [3.4.2](../../domain3.md#skill-3-4-2) | 公平性の評価 |
| [3.4.3](../../domain3.md#skill-3-4-3) | ポリシーに準拠したシステム |

## 学習の順番 {#study-order}

1. [統治の仕組み](../../../../services/genai-apps.md#governance-controls)と [Model Cards](../../../../services/sagemaker.md#model-cards): 要件と実装の対応を確認します。
2. [Data Catalog](../../../../services/data-engineering.md#glue-data-catalog)と [Knowledge Bases を呼ぶ](../../../../services/ai.md#knowledge-bases): データソースと引用の追跡を押さえます。
3. [異常検知](../../../../services/observability.md#anomaly-detection)と [Model Monitor](../../../../services/sagemaker.md#model-monitor): 継続的な監視の方法と提供状況を理解します。
4. [透明性と公平性](../../../../services/genai-apps.md#transparency-fairness)と[バイアスと公平性](../../../../services/ai-fundamentals.md#fairness): 手段を整理します。
5. [責任ある AI の 8 つの観点](../../../../services/ai-fundamentals.md#rai-dimensions): 方針の観点を確認します。

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| モデルの文書化 | SageMaker Model Cards |
| データの系譜 | Glue 5.0 以降の Spark で「Generate lineage events」 |
| 回答の根拠を追う | `citations` とチャンクのメタデータ |
| 処理したリージョンを追う | CloudTrail の `inferenceRegion` |
| 周期のある指標の急増 | CloudWatch の異常検知 |
| 応答のドリフト | ゴールデンデータセットの定期評価 |
| 属性による差を確かめる | 反事実のテスト、`Stereotyping` |
| 方針を実行時に適用 | Guardrails のトピックとフィルター |

## 引っかかりやすい点 {#traps}

- Guardrails のトレースには元の値が入ります。通常のログに書きません。
- トレースは開発者向けで、利用者には加工して見せます。
- Clarify と Model Monitor は新規顧客を受け付けていません。
- Bedrock Evaluations は表データのバイアス検出の代わりになりません。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [governance 問1](../../exercises/governance.md#q1) | 3.3.1 | 規制当局への説明のために、社内で運用する複数のモデルの目的、学習データ、限界を統一の形式で文書化しま… |
| [governance 問2](../../exercises/governance.md#q2) | 3.3.1 | 規制の要件で、FM の入力データがどこから来て、どのジョブで加工されたかを示す必要があります。加工は… |
| [governance 問3](../../exercises/governance.md#q3) | 3.3.1 | 金融の規制で、AI が出した判断について、入力と出力、使ったモデルを後から説明できる必要があります。… |
| [governance 問4](../../exercises/governance.md#q4) | 3.3.2 | Customer-managed のナレッジベースで、回答の根拠となった文書を後から監査できるように… |
| [governance 問5](../../exercises/governance.md#q5) | 3.3.2 | 地理的な推論プロファイルで呼んでいます。監査で、ある呼び出しが実際に処理されたリージョンの提示を求め… |
| [governance 問6](../../exercises/governance.md#q6) | 3.3.2 | 全社で FM に渡すデータソースが増え、どのデータソースがどこにあるのかを管理できなくなっています。… |
| [governance 問7](../../exercises/governance.md#q7) | 3.3.4 | ある API キーからの呼び出しで、深夜にガードレールの介入率とトークンが急に増えました。今後は不正… |
| [governance 問8](../../exercises/governance.md#q8) | 3.3.4 | Bedrock の FM を使った問い合わせ応答で、モデルを変えていないのに応答の傾向が徐々に変わる… |
| [governance 問9](../../exercises/governance.md#q9) | 3.3.4 | ポリシー違反の傾向を分析するため、チームは Guardrails のトレースをアプリのログに出力しま… |
| [governance 問10](../../exercises/governance.md#q10) | 3.4.1 | 与信の相談チャットで、利用者が「なぜその回答なのか」を確かめられるようにします。一方、エージェントの… |
| [governance 問11](../../exercises/governance.md#q11) | 3.4.1 | 新規のエージェントで、モデルがどの手順でどのツールを選んだかを開発者が後から確かめられるようにします… |
| [governance 問12](../../exercises/governance.md#q12) | 3.4.1 | 回答の不確実さを定量化して、運用チームが傾向を追えるようにしたいと考えています。回答ごとのスコアが低… |
| [governance 問13](../../exercises/governance.md#q13) | 3.4.2 | 採用の要約を生成するアプリで、候補者の属性による差が出ていないかを確かめます。実際の候補者のデータは… |
| [governance 問14](../../exercises/governance.md#q14) | 3.4.2 | 2 つのプロンプトの案で、固定観念に基づく表現の傾向を比べます。人による採点は費用が合いません。また… |
| [governance 問15](../../exercises/governance.md#q15) | 3.4.2 | 公平性を改善するプロンプトの案を本番で検証します。属性ごとの結果を集計して、案ごとに継続的に比べ、差… |
| [governance 問16](../../exercises/governance.md#q16) | 3.4.3 | 全社の責任ある AI の方針に「医療の診断はしない」「差別的な表現を出さない」があります。今は文書だ… |
| [governance 問17](../../exercises/governance.md#q17) | 3.4.3 | 新しいアプリが本番に出るときに、ガードレールの設定とログの設定を必ず確認したいと考えています。人のレ… |
| [governance 問18](../../exercises/governance.md#q18) | 3.4.3 | 社内で調整したモデルは、医療の用途に使わないことが条件で承認されました。この制限を、利用部門とモデル… |

<!-- questions:end -->

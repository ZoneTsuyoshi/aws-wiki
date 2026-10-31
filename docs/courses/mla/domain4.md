# 分野4: ML と AI のソリューションの運用、監視、保護

MLA-C02 の配点は **24%** です。モデルとエージェントの監視、コストと性能の最適化、セキュリティの3つのタスクがあります。FM のトークンコストやエージェントの監視は C02 で加わった範囲です。

## タスク 4.1: 推論と性能を監視する {#task-4-1}

### 4.1.1 本番のモデルの性能の監視 {#skill-4-1-1}

| 手段 | 見るもの |
|---|---|
| CloudWatch の生成 AI オブザーバビリティ | モデルの呼び出し、エージェント、ナレッジベース、ガードレール、ツール。プロンプトをエンドツーエンドで追う |
| Bedrock Evaluations | 品質と安全の指標を定期的に採点する |
| ドリフト検知のパイプライン | Processing で Evidently AI を動かし、EventBridge Scheduler で定期実行する |

Bedrock の運用の指標は `AWS/Bedrock` にあります。品質はこの指標には出ないので、評価の結果をカスタムメトリクスとして送ります。

詳細: [生成 AI オブザーバビリティ](../../services/genai-apps.md#genai-observability)、[見るべき指標](../../services/genai-apps.md#genai-metrics)、[Bedrock のメトリクス](../../services/ai.md#bedrock-metrics)、[Model Monitor](../../services/sagemaker.md#model-monitor)

### 4.1.2 ワークフローの異常とエラーの検出 {#skill-4-1-2}

!!! note "DevOps Guru の提供状況"
    Amazon DevOps Guru は 2026-10-29 で新規顧客の受付を終了し、2027-09-30 にサポートを終了します。AWS は CloudWatch と AWS DevOps Agent への移行を案内しています。

| 対象 | 手段 |
|---|---|
| 前処理のジョブ | Glue、Pipelines の状態変更を EventBridge で受ける |
| データの品質 | Glue Data Quality のスコア |
| 推論のエラー | `Invocation4XXErrors`、`Invocation5XXErrors` |
| 季節性のある指標 | CloudWatch の異常検知 |
| ログのパターン | Logs Insights、メトリクスフィルター |
| ML による運用の異常検知 | DevOps Guru |

**切り分け:** `ModelLatency` が大きければモデルやインスタンス、`OverheadLatency` が大きければコールドスタートなどの基盤側です。

詳細: [SageMaker の CloudWatch メトリクス](../../services/sagemaker.md#cloudwatch-metrics)、[異常検知](../../services/observability.md#anomaly-detection)、[Logs Insights](../../services/observability.md#logs-insights)、[Glue Data Quality](../../services/data-engineering.md#glue-data-quality)、[DevOps Guru](../../services/operations.md#devops-guru)

### 4.1.3 データ分布の変化の検出 {#skill-4-1-3}

データキャプチャで本番の入力と出力を S3 に保存します。`InitialSamplingPercentage` で割合を決めます。サーバーレス推論はデータキャプチャに対応しません。

| 監視の種類 | 必要なもの |
|---|---|
| データ品質 | データキャプチャとベースライン |
| モデル品質 | ＋ 後から届く正解ラベル |
| バイアスドリフト | 集団別の指標 |
| 特徴量の寄与のドリフト | SHAP の順位の比較 |

正解がすぐ届かない業務では、まず入力の分布を見ます。分布の変化は、精度の低下より先に分かる兆候です。

詳細: [Model Monitor](../../services/sagemaker.md#model-monitor)、[ドリフトの種類](../../services/sagemaker.md#drift)、[サーバーレス](../../services/sagemaker.md#serverless)

### 4.1.4 A/B テスト {#skill-4-1-4}

1 つのエンドポイントに複数の本番バリアントを置き、トラフィックを分けます。

| 設定 | 内容 |
|---|---|
| `InitialVariantWeight` | 配分の重み |
| `UpdateEndpointWeightsAndCapacities` | エンドポイントを作り直さずに配分を変える |
| `TargetVariant` | 呼び出しで特定のバリアントを指定する |

CloudWatch の指標はバリアントごとに見ます。比べるのは遅延だけでなく、コンバージョン率などの業務指標です。先にシャドウテストで安定性を確かめ、その後 10% だけ流して、結果を見て増やします。

FM では、Prompt Management のバリアント、Flows、AppConfig で分けます。

詳細: [デプロイとテストの戦略](../../services/sagemaker.md#deployment-strategies)、[テスト](../../services/genai-apps.md#testing)

### 4.1.5 エージェントの性能と連携の監視 {#skill-4-1-5}

| 症状 | 調べるもの | 自動の対応 |
|---|---|---|
| 応答が途中で切れる | `stopReason` が `max_tokens` | `maxTokens` を増やす、続きを要求する |
| ストリームが途中で止まる | `modelStreamErrorException` などのイベント | ループ内で例外を処理して再試行する |
| ツールの失敗 | ツールごとの失敗率と遅延 | 再試行、サーキットブレーカー |
| ツールが呼ばれない | ツールの説明、`toolChoice` | 説明を具体的にする |
| 同じ操作を繰り返す | トレース、繰り返し回数 | 上限と停止条件 |
| エージェント間の連携の失敗 | トレースのつながり、タスク完了率 | アラームから代替の処理へ |

ストリーミングは HTTP 200 を受け取った後でも失敗します。トークン数は最後の `metadata` にしか来ないので、途中で切れると使用量を取得できません。

自動化は、CloudWatch アラーム、EventBridge、Lambda か Step Functions の組み合わせで行います。

詳細: [ストリーミング](../../services/ai.md#streaming)、[トラブルシューティング](../../services/genai-apps.md#troubleshooting)、[安全な自律動作](../../services/genai-apps.md#agent-safeguards)、[エージェントの評価](../../services/genai-apps.md#agent-evaluation)

### 4.1.6 FM の性能の監視 {#skill-4-1-6}

| 指標 | 意味 |
|---|---|
| `TimeToFirstToken` | 最初のトークンまで。体感の待ち時間 |
| `InvocationLatency` | 最後のトークンまで |
| `InvocationThrottles` | スロットリングされた数 |
| `EstimatedTPMQuotaUsage` | TPM クォータの推定消費 |
| `InputTokenCount`、`OutputTokenCount` | トークン数 |

`Invocations` にスロットリングされた分は含まれません。品質は Bedrock Evaluations で定期的に採点します。

呼び出しログは既定で無効です。有効にすると、CloudWatch Logs Insights で大きなプロンプトを探せます。

詳細: [Bedrock のメトリクス](../../services/ai.md#bedrock-metrics)、[Bedrock Evaluations](../../services/genai-apps.md#bedrock-evaluations)、[モデル呼び出しログ](../../services/ai.md#invocation-logging)

## タスク 4.2: コストと性能を最適化する {#task-4-2}

### 4.2.1 推論のインスタンスファミリーの選択 {#skill-4-2-1}

| 区分 | ファミリーの例 | 用途 |
|---|---|---|
| 汎用、CPU | `ml.m5`、`ml.c5` | 表データの推論 |
| GPU | `ml.g5`、`ml.p4d`、`ml.p5` | 深層学習、LLM |
| Inferentia | `ml.inf1`、`ml.inf2` | 推論のコストと性能 |

Inferentia は CUDA 向けのコードがそのまま動きません。AWS Neuron でコンパイルします。

適切なサイズを負荷試験で決めるなら、Inference Recommender です。

詳細: [インスタンスの選び方](../../services/sagemaker.md#instance-selection)、[Inference Recommender](../../services/sagemaker.md#inference-optimization)

### 4.2.2 調査と分析のツール {#skill-4-2-2}

| ツール | 使いどころ |
|---|---|
| CloudWatch | メトリクス、ログ、アラーム |
| AgentCore Observability | エージェントのスパンとログ。CloudWatch に保存し、OpenTelemetry に対応 |
| X-Ray | サービス間の呼び出しをつなげて遅い箇所を探す |
| Logs Insights | ログの集計と検索 |
| CloudTrail | 誰が API を呼んだか |

「どこで遅いか」は X-Ray、「誰が変更したか」は CloudTrail です。

詳細: [監視とオブザーバビリティ](../../services/genai-apps.md#observability)、[X-Ray](../../services/observability.md#xray)、[CloudTrail と CloudWatch](../../services/observability.md#cloudtrail-vs-cloudwatch)

### 4.2.3 ダッシュボードの設定 {#skill-4-2-3}

CloudWatch のダッシュボードは、複数のリージョンのリソースを 1 つに載せられます。クロスアカウントオブザーバビリティで複数のアカウントも扱えます。

事業の指標を経営層に見せるなら Amazon Quick です。Managed Grafana はこの試験の対象外です。

Logs Insights のウィジェットは更新のたびにクエリが走り、料金がかかります。自動更新の間隔を短くしすぎないようにします。

詳細: [ダッシュボード](../../services/observability.md#dashboards)、[ダッシュボードの設定](../../services/observability.md#dashboard-settings)、[Amazon Quick](../../services/ai.md#quick)

### 4.2.4 容量の最適化 {#skill-4-2-4}

| 目的 | 手段 |
|---|---|
| 信頼性 | インスタンス 2 台以上で複数の AZ に分散する |
| 急増への対応 | 高解像度の指標、早めのスケールアウト |
| 過剰な容量の削減 | ターゲット追跡、マルチモデルや推論コンポーネントで統合する |
| Bedrock の容量不足 | クロスリージョン推論、Provisioned Throughput |
| アイドルの削減 | サーバーレス、非同期の 0 台への縮小 |

手順は、推論の種類を選ぶ、Inference Recommender でサイズを決める、複数のエンドポイントを統合する、自動スケーリング、Savings Plans の順です。

詳細: [推論の最適化](../../services/sagemaker.md#inference-optimization)、[自動スケーリング](../../services/sagemaker.md#autoscaling)、[耐障害の設計](../../services/genai-apps.md#fm-resilience)

### 4.2.5 コスト管理ツールとコストのクォータ {#skill-4-2-5}

| ツール | 使いどころ |
|---|---|
| AWS Budgets | しきい値で通知、自動の処理 |
| Cost Explorer | 実績の分析と推奨 |
| コスト配分タグ | チームやプロジェクトごとの集計 |
| Compute Optimizer | リソースの適正サイズ |
| Trusted Advisor | 幅広い点検 |
| Service Quotas | クォータの確認と引き上げ |

Budgets の通知は遅れることがあるので、`FORECASTED` を使い、しきい値を低めにします。予算アクションで IAM ポリシーを適用すると、超過時に新しいリソースの作成を止められます。

タグは付けるだけでは請求データに出ません。コスト配分タグとして有効化します。

詳細: [予算の種類](../../services/cost-management.md#budget-types)、[予算アクション](../../services/cost-management.md#budget-actions)、[Cost Explorer](../../services/cost-management.md#cost-explorer)、[コスト配分タグ](../../services/cost-management.md#cost-allocation-tags)、[推奨を出すサービス](../../services/cost-management.md#recommendation-tools)

### 4.2.6 購入オプションの選択 {#skill-4-2-6}

| 選択肢 | 効果 | 使いどころ |
|---|---|---|
| オンデマンド | 基準 | 変動する負荷 |
| Managed Spot | 最大 90% 割引 | 中断できる学習 |
| SageMaker AI Savings Plans | 最大 64% 割引。1 年か 3 年 | 継続する利用 |
| トレーニングプラン | GPU 容量の予約 | 大規模な学習 |

定常の部分は Savings Plans、変動の部分はオンデマンド、中断できる学習はスポットと組み合わせます。

詳細: [インスタンスの選び方](../../services/sagemaker.md#instance-selection)、[購入の選び方](../../services/cost-management.md#purchase-choice)

### 4.2.7 FM の推論のコスト評価 {#skill-4-2-7}

トークン単価が入力 100 万あたり $3、出力 100 万あたり $15 の仮の例です。1 日 1,000 回、1 回あたり入力 2,000、出力 500 トークンとします。

- 入力: 200 万トークンで $6
- 出力: 50 万トークンで $7.5
- 合計: 1 日 $13.5

| 方式 | 課金 |
|---|---|
| オンデマンド | トークン |
| Priority | 多くのプロバイダーで Standard の 75% 増し |
| Flex | 多くのプロバイダーで Standard の 50% 引き |
| バッチ | 対象のモデルでオンデマンドの 50% 引き |
| Provisioned Throughput | モデルユニットの時間課金 |

Guardrails、Knowledge Bases のベクトルストア、カスタムモデルの保存の費用も含めて見積もります。

詳細: [Bedrock の料金](../../services/cost-management.md#bedrock-pricing)、[トークン](../../services/ai-fundamentals.md#tokens)

### 4.2.8 エージェントのリソース消費の監視 {#skill-4-2-8}

エージェントは 1 つの依頼で何度もモデルとツールを呼ぶので、依頼あたりの消費を見ます。

| 指標 | 手段 |
|---|---|
| 繰り返し回数、ステップ数 | AgentCore Observability のトレース |
| 依頼あたりのトークン | 累計を記録し、予算を超えたら止める |
| ツールの呼び出し回数と遅延 | カスタムメトリクス |
| セッションの資源 | Runtime の 1 セッションは 2 vCPU、8 GB |

詳細: [見るべき指標](../../services/genai-apps.md#genai-metrics)、[安全な自律動作](../../services/genai-apps.md#agent-safeguards)、[AgentCore の構成要素と設定](../../services/ai.md#agentcore-components)

### 4.2.9 使い方の最適化による FM のコスト管理 {#skill-4-2-9}

| 手法 | 具体例 |
|---|---|
| 文脈の削減 | 履歴を要約する |
| 応答の制限 | `maxTokens` を実態に合わせる |
| RAG の絞り込み | リランクで 5 件に |
| プロンプトキャッシュ | 固定の指示を先に置く。TTL は多くのモデルで 5 分 |
| セマンティックキャッシュ | 言い換えの質問でモデルを呼ばない |
| モデルカスケード | 分類は小さなモデル、難しい質問は上位へ |
| バッチ | 夜間の要約 |

`maxTokens` が大きすぎると、クォータの予約も増えてスロットリングの原因になります。アプリごとのコストは、アプリケーション推論プロファイルのタグで追跡します。

詳細: [トークンの削減](../../services/genai-apps.md#token-efficiency)、[キャッシュの種類](../../services/genai-apps.md#caching)、[推論の容量とプロファイル](../../services/genai-apps.md#inference-profiles)、[エラーとスロットリング](../../services/ai.md#errors-throttling)

### 4.2.10 AI 固有のコストの監視 {#skill-4-2-10}

| 項目 | 見るもの | 対策 |
|---|---|---|
| トークン | `InputTokenCount`、`CacheReadInputTokenCount` | キャッシュの利用率を上げる |
| 埋め込みの計算 | 再埋め込みの頻度と件数 | 差分の同期、バッチ推論 |
| ベクトルの保存 | 次元と件数 | 次元の削減、低頻度のデータは S3 Vectors |
| OpenSearch Serverless | OCU | 利用に合うストアを選ぶ |

急増の検知には Cost Anomaly Detection を使います。100 万チャンクで次元を 1,024 から 256 に下げると、生データは約 4.1 GB から約 1.0 GB になります。精度を評価で確かめてから変えます。

詳細: [埋め込みの選び方](../../services/genai-apps.md#embedding-selection)、[ベクトルストア](../../services/genai-apps.md#vector-stores)、[Cost Anomaly Detection](../../services/cost-management.md#cost-anomaly-detection)、[見るべき指標](../../services/genai-apps.md#genai-metrics)

## タスク 4.3: ワークロードとエンドポイントを保護する {#task-4-3}

### 4.3.1 CI/CD でのコードとイメージの脆弱性の検査 {#skill-4-3-1}

!!! note "CodeGuru の提供状況"
    CodeGuru Security は 2025-11-20 にサポートを終了しました。CodeGuru Reviewer は新しいリポジトリを関連付けられません。現在のコードのスキャンは Inspector の Code Security が担います。試験で CodeGuru が出たら、パイプラインでの静的スキャンの役割として読みます。

| 対象 | サービス |
|---|---|
| コンテナイメージ | Inspector（ECR の拡張スキャン） |
| CI/CD でのイメージの検査 | Inspector の Scan API と SBOM Generator |
| コード | Inspector の Code Security、CodeGuru |
| Lambda | Inspector の Lambda スキャン |

重大な検出結果が出たら、CodeBuild のステップを失敗させてデプロイを止めます。拡張スキャンの結果は EventBridge に送られます。

詳細: [Inspector](../../services/threat-detection.md#inspector)、[ECR のスキャン](../../services/threat-detection.md#inspector-ecr)、[コードのスキャン](../../services/threat-detection.md#inspector-code)、[CodeGuru](../../services/other-services.md#codeguru)、[CodeGuru Security](../../services/threat-detection.md#codeguru-security)

### 4.3.2 成果物への最小権限 {#skill-4-3-2}

| 成果物 | 絞り方 |
|---|---|
| S3 の学習データとモデル | バケットとプレフィックスに限定する |
| KMS キー | キーポリシーとロールの許可の両方を確認する |
| ECR イメージ | リポジトリに限定する |
| Model Registry | 承認の操作を担当者に限定する |
| Bedrock のモデル | ワイルドカードではなくモデルの ARN に絞る |
| データレイク | Lake Formation で列や行に絞る |

推論プロファイルを使うなら、プロファイルと、経路上の各リージョンの基盤モデルの両方を許可します。

詳細: [最小権限](../../services/iam.md#least-privilege)、[Bedrock の IAM のスコープ](../../services/ai.md#iam-scope)、[IAM と暗号化](../../services/sagemaker.md#iam-encryption)、[Lake Formation の権限](../../services/data-engineering.md#lake-formation-permissions)

### 4.3.3 利用者とアプリの IAM ポリシーとロール {#skill-4-3-3}

| 主体 | 必要な権限の例 |
|---|---|
| データサイエンティスト | `sagemaker:CreateTrainingJob` と `iam:PassRole`。本番のデプロイは与えない |
| ジョブやエンドポイントの実行ロール | S3、ECR、KMS へのアクセス |
| アプリ | `sagemaker:InvokeEndpoint` か `bedrock:InvokeModel` |

ロールを渡す `iam:PassRole` は、`Resource` を `*` にすると権限の昇格につながります。ロールの名前で絞り、`iam:PassedToService` の条件も付けます。

詳細: [IAM と暗号化](../../services/sagemaker.md#iam-encryption)、[iam:PassRole](../../services/iam.md#passrole)、[ポリシーの評価](../../services/iam.md#policy-evaluation)

### 4.3.4 監視、監査、コンプライアンス、ログ {#skill-4-3-4}

| サービス | 記録するもの |
|---|---|
| CloudTrail | API の呼び出し。誰がいつ何をしたか |
| Config | リソースの設定とルールへの準拠 |
| CloudWatch Logs | ジョブとアプリのログ |
| Bedrock の呼び出しログ | プロンプトと応答。既定は無効 |
| Macie | S3 の機密データ |

呼び出しログの `input` は、ガードレールが介入しても元のリクエストのままです。ブロックされた内容も平文で残るので、ログを別途保護します。

詳細: [CloudTrail](../../services/observability.md#cloudtrail)、[Config](../../services/governance.md#config)、[CloudTrail との違い](../../services/governance.md#config-vs-cloudtrail)、[モデル呼び出しログ](../../services/ai.md#invocation-logging)、[統治の仕組み](../../services/genai-apps.md#governance-controls)

### 4.3.5 セキュリティの問題の調査 {#skill-4-3-5}

| 症状 | 原因の候補 |
|---|---|
| 学習ジョブで S3 の `AccessDenied` | 実行ロールの権限、KMS キーの権限 |
| ジョブの作成が拒否される | `iam:PassRole` がない |
| VPC 内の学習で S3 に接続できない | S3 エンドポイントも NAT もない |
| 分離モードでスクリプトが S3 を読めない | 仕様。入力チャネル経由で受け取る |
| Bedrock の `AccessDeniedException` | モデルの利用条件、IAM の権限 |
| 暗号化メッセージつきの拒否 | `DecodeAuthorizationMessage` で読む |

調査には CloudTrail のイベント、IAM ポリシーシミュレーター、IAM Access Analyzer を使います。

詳細: [VPC とネットワーク分離](../../services/sagemaker.md#vpc-isolation)、[アクセス拒否メッセージ](../../services/iam.md#access-denied-messages)、[DecodeAuthorizationMessage](../../services/iam.md#decode-authorization)、[ポリシーシミュレーター](../../services/iam.md#policy-simulator)、[アクセスの要求と管理](../../services/ai.md#access)

### 4.3.6 VPC、サブネット、セキュリティグループによる分離 {#skill-4-3-6}

| 要件 | 設定 |
|---|---|
| インターネットを経由しない | プライベートサブネットと VPC エンドポイント |
| S3 と DynamoDB へ閉域で | ゲートウェイエンドポイント。追加料金なし |
| SageMaker API、Bedrock へ閉域で | インターフェイスエンドポイント（PrivateLink） |
| コンテナの外向き通信を完全に遮断 | `EnableNetworkIsolation` |
| 分散学習のノード間の暗号化 | コンテナ間の通信の暗号化。時間は延びる |
| 通信の許可 | セキュリティグループで必要なポートだけ |

サーバーレス推論は VPC の設定に対応しません。VPC が必須ならリアルタイムです。

詳細: [VPC とネットワーク分離](../../services/sagemaker.md#vpc-isolation)、[サブネットとルートテーブル](../../services/networking.md#subnets-route-tables)、[セキュリティグループと NACL](../../services/networking.md#security-groups-nacls)、[VPC エンドポイント](../../services/networking.md#vpc-endpoints)、[Bedrock の VPC エンドポイント](../../services/ai.md#privatelink)

### 4.3.7 セキュリティリスクと脆弱性の特定と緩和 {#skill-4-3-7}

| リスク | 対策 |
|---|---|
| プロンプトインジェクション | プロンプト攻撃フィルター、入力の無害化、ツールの権限制限 |
| 間接インジェクション（文書内の指示） | データソースの管理、外部の内容をデータとして区切る |
| データポイズニング | データの出所の管理と検査 |
| データ漏えい | 機密情報フィルター、最小権限 |
| ツールの悪用 | AgentCore Policy、人の承認 |
| イメージの脆弱性 | Inspector |
| 認証情報の漏えい | Secrets Manager、ロールの一時認証情報 |

既知の攻撃プロンプトを定期的に流し、遮断率を CloudWatch に記録します。

詳細: [多層防御](../../services/genai-apps.md#defense-in-depth)、[プロンプトのリスク](../../services/ai-fundamentals.md#prompt-engineering)、[エージェントの保護](../../services/ai.md#agent-security)、[Secrets Manager](../../services/secrets.md#secrets-manager)

### 4.3.8 FM にアクセスする認証情報の選択 {#skill-4-3-8}

| 認証情報 | 有効期間 | 使いどころ |
|---|---|---|
| IAM ロール | 一時 | アプリの基本。Lambda、ECS、EC2 |
| Bedrock の短期 API キー | 最大 12 時間。生成元の権限を継承 | SigV4 を使いにくいクライアントの本番 |
| Bedrock の長期 API キー | 設定した期限まで。IAM ユーザーに紐づく | 検証のみ |

API キーの環境変数は `AWS_BEARER_TOKEN_BEDROCK` です。使用の可否は `bedrock:CallWithBearerToken`、長期キーの生成は `iam:CreateServiceSpecificCredential` で制御します。

AWS 上で動くアプリに長期キーを配る案は誤りです。ロールを使います。

詳細: [Bedrock API キー](../../services/ai.md#api-keys)、[IAM のスコープ](../../services/ai.md#iam-scope)

### 4.3.9 安全策と機密データの保護 {#skill-4-3-9}

| 要件 | Guardrails の機能 |
|---|---|
| 有害な内容を止める | コンテンツフィルター |
| 話題を禁止する（例: 投資助言） | 拒否トピック |
| PII をマスクする | 機密情報フィルターの `ANONYMIZE` |
| 攻撃を防ぐ | プロンプト攻撃フィルター |
| 参照元に基づかない応答を止める | コンテキストグラウンディング |
| 規定と論理的に矛盾しないか検証する | Automated Reasoning |
| モデルを呼ばずに検査する | `ApplyGuardrail` |

日本語を扱うなら Standard 層です。PII のマスクが必要なら、ストリーミングの非同期モードは避けます。マスク前の内容が届く可能性があるためです。

本番では番号付きのバージョンを指定します。全アカウントに強制するなら Organizations の Bedrock ポリシーです。

詳細: [Guardrails のフィルター](../../services/ai.md#guardrail-filters)、[層の選び方](../../services/genai-apps.md#guardrail-tiers)、[ストリーミングでの動作](../../services/genai-apps.md#guardrail-streaming)、[コンテキストグラウンディング](../../services/genai-apps.md#contextual-grounding)、[組織での強制](../../services/genai-apps.md#guardrail-org-enforcement)、[責任ある AI](../../services/ai-fundamentals.md#responsible-ai)

## 確認問題 {#self-check}

??? question "問1: リアルタイム推論の遅延が増えました。CloudWatch では `ModelLatency` は変わらず、`OverheadLatency` が大きく増えています。エンドポイントはサーバーレスです。原因と対策は？"
    コールドスタートです。モデルの処理時間は変わっていないので、基盤側の問題です。Provisioned Concurrency を設定します。インスタンスの種類を変える案は、サーバーレスには当てはまりません。

??? question "問2: 不正検知の精度が半年で低下しましたが、入力の分布はほとんど変わっていません。正解ラベルは数週間後に届きます。何が起きていて、どう検出しますか？"
    コンセプトドリフトです。入力と正解の関係が変わっています。分布の監視では検出できないので、届いた正解ラベルと予測を結合して精度を監視します。基準を下回ったら、アラームから再学習を起動します。

??? question "問3: 対話型の FM アプリで、「応答が遅い」という声と、スロットリングの増加が出ています。入力は短いのに `maxTokens` は最大値にしています。何を見て、何を変えますか？"
    体感の遅さは `TimeToFirstToken`、スロットリングは `InvocationThrottles` と `EstimatedTPMQuotaUsage` で見ます。`maxTokens` を実態に合わせて下げます。リクエストの開始時に入力と `maxTokens` の合計がクォータから差し引かれるので、過大だと実際の消費より早く上限に達します。

??? question "問4: GPU のエンドポイントが 24 時間一定の負荷で動いています。今後 3 年は同じ利用が続きます。夜間のバッチ学習は中断されても問題ありません。それぞれの購入方法は？"
    エンドポイントは SageMaker AI Savings Plans で最大 64% 下げます。バッチ学習は Managed Spot とチェックポイントで最大 90% 下げます。

??? question "問5: データサイエンティストが学習ジョブを作れません。`sagemaker:CreateTrainingJob` は許可されています。エラーはロールに関するものです。何が足りず、どう安全に許可しますか？"
    `iam:PassRole` です。`Resource` を学習用の実行ロールに限定し、`iam:PassedToService` の条件を付けます。`*` にすると、より強いロールを渡して権限を昇格できてしまいます。

??? question "問6: 顧客対応の生成 AI で、回答の中の氏名とメールアドレスをマスクし、ストリーミングで返します。さらに監査のために呼び出しログも有効にします。設定で注意する点を 2 つ答えてください。"
    1 つ目は、機密情報フィルターを `ANONYMIZE` にし、ストリーミングは同期モードにすることです。非同期ではマスク前の内容が届く可能性があります。2 つ目は、呼び出しログにはマスク前の内容が残ることです。ログの保存先へのアクセスを絞り、暗号化します。

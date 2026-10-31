# 分野4: 生成 AI アプリの運用効率と最適化

配点は **12%** です。コストの最適化、性能の最適化、監視の3タスクがあります。

コスト、遅延、品質は同時には改善しにくいものです。どの手法が何を犠牲にするかを押さえます。

## タスク 4.1: コストの最適化と資源の効率化を実装する {#task-4-1}

### 4.1.1 トークンの効率化 {#skill-4-1-1}

| 手法 | 具体例 | 犠牲になるもの |
|---|---|---|
| 見積もりと追跡 | `CountTokens`、`InputTokenCount`、`OutputTokenCount` | 特になし |
| 文脈の最適化 | リランクで 5 件に絞る | 網羅性 |
| 応答の制限 | `maxTokens` を実態に合わせる | 長い回答が切れる |
| プロンプトの圧縮 | 共通の説明を削る | 指示の明確さ |
| 文脈の刈り込み | 古い履歴を要約する | 細かな文脈 |

**出力の単価は入力より高いのが一般的です。** 長い回答を避ける効果は大きくなります。アプリケーション推論プロファイルのタグで、アプリごとの費用を追跡します。

詳細: [トークンの削減](../../services/genai-apps.md#token-efficiency)、[クォータとトークンの数え方](../../services/ai.md#quotas-detail)、[Bedrock の料金](../../services/cost-management.md#bedrock-pricing)、[推論プロファイル](../../services/genai-apps.md#inference-profiles)

### 4.1.2 費用対効果の高いモデル選択 {#skill-4-1-2}

| 手法 | 内容 |
|---|---|
| 費用と能力の評価 | 必要な品質を満たす中で最も安いモデルを選ぶ |
| 複雑さで分ける | カスケード、Intelligent Prompt Routing |
| 価格性能比の測定 | 1 件の成功あたりの費用で比べる |
| 効率のよい推論方式 | バッチ、Flex で安く |

| 方式 | 価格の目安 | 向いている処理 |
|---|---|---|
| Standard | 基準 | 日常の処理 |
| Priority | Standard より割高 | 応答速度が重要 |
| Flex | Standard より割安 | 評価、要約など時間に余裕がある |
| バッチ | 対象のモデルで 50% 引き | 非同期の大量処理 |

**単価だけで比べない:** 安いモデルで再試行や人の修正が増えるなら、高くつきます。

詳細: [動的なモデル切り替え](../../services/genai-apps.md#dynamic-model-selection)、[スループットの選択肢](../../services/ai.md#throughput-options)、[Bedrock の料金](../../services/cost-management.md#bedrock-pricing)

### 4.1.3 高い処理能力と資源の活用 {#skill-4-1-3}

| 手段 | 内容 | 注意 |
|---|---|---|
| バッチ | `CreateModelInvocationJob` | プロビジョンドモデルでは使えない |
| 容量の計画 | 入力 + `maxTokens` のピークで見積もる | 実際の出力より大きく予約される |
| 使用率の監視 | `EstimatedTPMQuotaUsage` にアラーム | |
| 自動スケーリング | SageMaker AI のエンドポイント | Bedrock のオンデマンドには不要 |
| Provisioned Throughput | モデルユニットを購入 | 使用率が低いと無駄。コミット中は削除できない |

モデルユニットが処理できる量はアカウントマネージャーに確認します。

詳細: [推論の容量とプロファイル](../../services/genai-apps.md#inference-profiles)、[スループット](../../services/genai-apps.md#throughput)、[CloudWatch のメトリクス](../../services/ai.md#bedrock-metrics)、[自動スケーリング](../../services/sagemaker.md#autoscaling)

### 4.1.4 賢いキャッシュ {#skill-4-1-4}

| 種類 | 仕組み | 効く場面 | 実装 | リスク |
|---|---|---|---|---|
| プロンプトキャッシュ | 入力の前半を再利用 | 長い固定の指示や文書 | Bedrock の `cachePoint` | 順番が変わると一致しない |
| 決定的なハッシュ | リクエストのハッシュで検索 | 同じ質問 | DynamoDB、ElastiCache | 言い換えには効かない |
| 結果のフィンガープリント | 入力の内容から指紋を作り再利用 | 同じ文書の再処理 | DynamoDB | モデルや版もキーに入れる |
| セマンティック | 埋め込みが近ければ過去の回答 | 言い換えの質問 | MemoryDB、OpenSearch | しきい値が低いと別の質問に古い答え |
| エッジ | 配信ネットワークで返す | 公開の固定の回答 | CloudFront | 利用者ごとの回答には不向き |

**プロンプトキャッシュは FM を呼びます。** 他のキャッシュは呼び出しそのものを省きます。固定の内容を前に、変わる内容を後に置きます。TTL は多くのモデルで 5 分で、ヒットごとに延びます。

**権限に注意:** 利用者ごとの権限や個人情報を含む回答は、キャッシュしないかキーを分けます。

詳細: [キャッシュの種類](../../services/genai-apps.md#caching)、[クォータとプロンプトキャッシュ](../../services/ai.md#quotas-detail)、[Amazon MemoryDB](../../services/databases-specialized.md#memorydb)

## タスク 4.2: アプリの性能を最適化する {#task-4-2}

### 4.2.1 応答性の高い AI システム {#skill-4-2-1}

| 手法 | 効果 | 犠牲になるもの |
|---|---|---|
| 事前計算 | 予測できる質問でモデルを呼ばない | 鮮度 |
| 遅延に最適化したモデル | 処理が速い | 費用や対応モデル |
| 並列リクエスト | 独立した処理を同時に | 同時に消費するクォータ |
| ストリーミング | 体感の待ち時間を減らす | 全体の時間は短くならない |
| ベンチマーク | 改善を測る | 測定の手間 |

**ストリーミングで改善するのは `TimeToFirstToken` で、`InvocationLatency` は変わりません。** どちらの問題かを先に切り分けます。

!!! note "Latency Optimized Inference の状況"
    `performanceConfig` の `latency: optimized` は、2026 年 10 月時点でプレビューです。

詳細: [遅延の短縮](../../services/genai-apps.md#latency)、[キャッシュの種類](../../services/genai-apps.md#caching)、[CloudWatch のメトリクス](../../services/ai.md#bedrock-metrics)

### 4.2.2 検索の性能を高める {#skill-4-2-2}

| 手法 | 内容 |
|---|---|
| インデックスの最適化 | HNSW のパラメータ、シャードの設計、次元の削減 |
| 問い合わせの前処理 | 書き換え、フィルターで候補を絞る |
| 独自のスコアでのハイブリッド検索 | キーワードとベクトルの重みを調整する |

**OpenSearch のハイブリッド検索:** キーワードとベクトルのスコアは尺度が違うので、そのまま足せません。検索パイプラインの正規化プロセッサで、スコアを揃えてから合成します。正規化は `min_max` や `l2`、合成は `arithmetic_mean` などで、重みも指定できます。

詳細: [検索の改善](../../services/genai-apps.md#retrieval-optimization)、[OpenSearch](../../services/genai-apps.md#opensearch-vectors)、[ベクトルインデックス](../../services/databases-specialized.md#vector-indexes)

### 4.2.3 FM のスループットの最適化 {#skill-4-2-3}

| 課題 | 手法 |
|---|---|
| トークンの消費が多い | `maxTokens` を実態に近づける。未使用分は完了時に戻るが、その間は枠を占める |
| 急がない大量の処理 | バッチ推論。夜間に実行 |
| スパイク | SQS でならす |
| 同時実行の管理 | Lambda の予約済み同時実行、Step Functions の Map の並列度 |

一部のモデルは出力 1 トークンをクォータ上で複数トークンとして数えます。**例:** 消費率 5 倍なら、入力 1,000、出力 100 の消費は 1,500 です。ただし課金は実際の 1,100 トークンです。

詳細: [スループット](../../services/genai-apps.md#throughput)、[クォータの計算例](../../services/ai.md#quotas-detail)、[予約済み同時実行](../../services/lambda.md#reserved-concurrency)、[Map の設定](../../services/step-functions.md#map-settings)

### 4.2.4 用途に合わせた FM の調整 {#skill-4-2-4}

| 用途 | temperature | 備考 |
|---|---|---|
| 抽出、分類、SQL | 0〜0.2 | 再現性を優先 |
| 一般の質問応答 | 0.2〜0.5 | |
| 文案、アイデア | 0.7 以上 | 多様性 |

- **top-p:** 累積確率がこの値に届くまでの候補から選びます。
- **top-k:** 上位 k 個の候補から選びます。対応はモデルごとに違います。
- **停止シーケンスや `maxTokens`:** 不要な出力を止めます。

temperature を 0 にしても、誤りがなくなるわけではありません。変更の効果は A/B テストで確かめます。

詳細: [パラメータの調整](../../services/genai-apps.md#parameter-tuning)、[推論パラメータ](../../services/ai-fundamentals.md#inference-parameters)、[inferenceConfig](../../services/ai.md#inference-config)、[テスト](../../services/genai-apps.md#testing)

### 4.2.5 FM に合わせた資源の割り当て {#skill-4-2-5}

| 観点 | 従来のアプリ | FM のワークロード |
|---|---|---|
| 容量の単位 | リクエスト数 | トークン数 |
| 負荷の指標 | CPU 使用率 | 同時実行数、トークンの消費 |
| スケールの速度 | 比較的速い | モデルの読み込みで遅い |

- **容量の計画:** プロンプトと応答の長さの分布を、呼び出しログから取ります。平均ではなくピークで考えます。
- **利用パターンの監視:** 入出力の比率の変化は、プロンプトの変更や不正利用の兆候です。
- **自動スケーリング:** `ConcurrentRequestsPerModel` を使い、早めにスケールアウトします。

詳細: [スループット](../../services/genai-apps.md#throughput)、[デプロイ戦略](../../services/genai-apps.md#deployment)、[自動スケーリング](../../services/sagemaker.md#autoscaling)

### 4.2.6 ワークフロー全体の性能 {#skill-4-2-6}

| 対象 | 手法 |
|---|---|
| API 呼び出しの分析 | 呼び出しログから、プロンプトと応答の長さと遅延の関係を見る |
| ベクトル検索 | p95、p99 を追う。フィルターで候補を絞る |
| LLM の推論 | プロンプトキャッシュ、小さなモデル、短い入力 |
| サービス間の通信 | X-Ray で遅い箇所を探す。接続を再利用する |

RAG で遅いときは、検索、リランク、生成のどこが遅いかを分けます。多くの場合は生成が支配的ですが、測ってから判断します。

詳細: [遅延の短縮](../../services/genai-apps.md#latency)、[運用](../../services/genai-apps.md#vector-operations)、[X-Ray](../../services/observability.md#xray)、[接続の再利用](../../services/sdk-resilience.md#connection-reuse)

## タスク 4.3: 生成 AI アプリの監視を実装する {#task-4-3}

### 4.3.1 全体を見渡す観測 {#skill-4-3-1}

| 種類 | 例 | 手段 |
|---|---|---|
| 運用の指標 | 遅延、エラー、スロットリング | `AWS/Bedrock` |
| 性能のトレース | サービス間の呼び出し | X-Ray、Application Signals |
| FM のやり取り | プロンプトから応答まで | CloudWatch の生成 AI オブザーバビリティ |
| 事業の指標 | 解決率、満足度 | カスタムメトリクスとダッシュボード |

ダッシュボードは CloudWatch、Managed Grafana、Quick Sight から選びます。運用担当と事業の担当で、見る指標を分けます。

詳細: [監視とオブザーバビリティ](../../services/genai-apps.md#observability)、[見るべき指標](../../services/genai-apps.md#genai-metrics)、[Application Signals](../../services/observability.md#application-signals)、[Managed Grafana](../../services/operations.md#managed-grafana)、[Quick Sight](../../services/data-engineering.md#quick-sight)

### 4.3.2 生成 AI に特有の監視 {#skill-4-3-2}

| 指標 | 取り方 |
|---|---|
| トークンの使用量 | `InputTokenCount`、`OutputTokenCount` |
| プロンプトの効果 | 版ごとの評価スコア |
| ハルシネーション率、応答の品質 | 定期の評価をカスタムメトリクスで送る |
| トークンの急増、応答のドリフト | CloudWatch の異常検知 |
| リクエストと応答の詳細 | モデル呼び出しログ |
| 費用の急増 | Cost Anomaly Detection |

**既定のメトリクスでは品質は分かりません。** `AWS/Bedrock` が分かるのは遅延や量です。品質は評価の結果を送って初めて見えます。

**呼び出しログの対象:** `bedrock-runtime` 経由の呼び出しです。`bedrock-mantle` の呼び出しは記録されません。

詳細: [見るべき指標](../../services/genai-apps.md#genai-metrics)、[モデル呼び出しログ](../../services/ai.md#invocation-logging)、[異常検知](../../services/observability.md#anomaly-detection)、[Cost Anomaly Detection](../../services/cost-management.md#cost-anomaly-detection)

### 4.3.3 実行につながる統合的な観測 {#skill-4-3-3}

| 目的 | 手段 |
|---|---|
| 運用のダッシュボード | CloudWatch |
| 事業への影響の可視化 | Quick Sight、Managed Grafana |
| コンプライアンスの監視 | ガードレールの介入率、ログの設定の検査 |
| フォレンジックと監査 | CloudTrail、呼び出しログを S3 に長期保存 |
| 利用者の行動の追跡 | `requestMetadata` でテナントや利用者を付与 |
| モデルの振る舞いの追跡 | 応答の長さ、拒否の割合の変化 |

通知は Q Developer in chat applications で Slack や Teams に流せます。指標には、次に何をするかの手順を結びつけます。

詳細: [監視とオブザーバビリティ](../../services/genai-apps.md#observability)、[モデル呼び出しログ](../../services/ai.md#invocation-logging)、[チャットアプリへの通知](../../services/operations.md#q-chat)、[CloudTrail](../../services/observability.md#cloudtrail)

### 4.3.4 ツールの性能の枠組み {#skill-4-3-4}

| 項目 | 指標 |
|---|---|
| 呼び出しのパターン | ツールごとの回数、順序 |
| 性能 | 遅延、失敗率 |
| マルチエージェントの協調 | 引き継ぎの回数、スパンの親子関係 |
| 異常の検知 | 平常時の基準との差 |

AgentCore Observability はメトリクス、スパン、ログを CloudWatch に保存し、OpenTelemetry に対応します。Lambda のツールでは、Embedded Metric Format でカスタムメトリクスを送れます。

**シナリオ:** 同じツールの呼び出しが急に増えたら、エージェントのループかもしれません。トレースで確認し、繰り返しの上限を見直します。

詳細: [見るべき指標](../../services/genai-apps.md#genai-metrics)、[CloudWatch の生成 AI オブザーバビリティ](../../services/genai-apps.md#genai-observability)、[EMF](../../services/observability.md#emf)、[安全な自律動作](../../services/genai-apps.md#agent-safeguards)

### 4.3.5 ベクトルストアの運用管理 {#skill-4-3-5}

| 項目 | 内容 |
|---|---|
| 性能の監視 | 検索の遅延（p95、p99）、メモリとディスク |
| インデックスの最適化 | 定期的な再構築。HNSW は削除や上書きが多いと精度が落ちることがある |
| データ品質の検証 | 取得の評価を定期実行、最終同期の時刻の確認 |
| 取り込みの監視 | 同期ジョブの統計と失敗の理由 |

詳細: [運用](../../services/genai-apps.md#vector-operations)、[ベクトルインデックス](../../services/databases-specialized.md#vector-indexes)、[同期と鮮度](../../services/genai-apps.md#kb-sync)

### 4.3.6 生成 AI に特有の障害の調査 {#skill-4-3-6}

従来の ML と違い、エラーなく誤った回答を返します。HTTP 200 でも失敗していることがあります。

| 障害 | 調べ方 |
|---|---|
| ハルシネーション | ゴールデンデータセットで定期的に評価する |
| 応答の一貫性の低下 | 同じ入力の出力の差分を、意味的類似度で比べる |
| 論理の誤り | エージェントの推論の過程をたどる |
| 原因の特定 | 検索、生成、ツールを分けて記録する観測の仕組み |

**ハルシネーションの調査の順序:** 取得は正しいか、取得した文書に答えがあるか、生成が文書に従っているか、の順に確かめます。

詳細: [テスト](../../services/genai-apps.md#testing)、[トラブルシューティング](../../services/genai-apps.md#troubleshooting)、[エージェントの評価](../../services/genai-apps.md#agent-evaluation)

## 確認問題 {#self-check}

??? question "問1: 50 ページの製品マニュアルを毎回システムプロンプトに入れており、質問は毎回違います。入力の費用を減らすには、どのキャッシュを選びますか？"
    プロンプトキャッシュです。固定のマニュアルを前に置き、質問を後ろに置いて `cachePoint` で区切ります。質問が毎回違うので、回答を再利用するキャッシュは効きません。TTL は多くのモデルで 5 分なので、呼び出しの間隔が長いと効果が落ちます。`cacheReadInputTokens` で効果を確かめます。

??? question "問2: FAQ のチャットで、同じ意味の言い換えの質問が多く、FM の費用を減らしたいです。回答には顧客ごとの契約情報が含まれることがあります。どう設計しますか？"
    セマンティックキャッシュです。MemoryDB や OpenSearch で埋め込みの近さを検索します。契約情報を含む回答は、キャッシュしないか、キーを顧客ごとに分けます。しきい値が低いと別の質問に誤った回答を返すので、評価して決めます。一般的な回答だけをキャッシュする分類を前に置く方法もあります。

??? question "問3: 利用者から「最初の文字が出るまで遅い」と苦情があります。`InvocationLatency` は許容範囲です。何を見て、どう対応しますか？"
    `TimeToFirstToken` を見ます。ストリーミングが有効か、Guardrails の同期モードでのバッファ、モデルの大きさ、入力の長さを確認します。小さなモデルや短い文脈に変えると改善します。プロンプトキャッシュも遅延を下げます。Latency Optimized Inference はプレビューなので、本番の前提にするかは慎重に判断します。

??? question "問4: Provisioned Throughput を 1 か月のコミットで購入しましたが、夜間の使用率が 5% です。費用を減らすにはどうしますか？"
    負荷が安定していないので、オンデマンドや Reserved ティアを検討します。Provisioned Throughput はコミットメントの期間中は削除できないので、期間の終了後に切り替えます。急がない処理を夜間のバッチや Flex に回す設計も考えます。カスタムモデルなら、カスタムモデルのデプロイのオンデマンド推論も候補です。

??? question "問5: エラー率は 0% なのに、顧客満足度が下がっています。プロンプトは先週更新しました。何を確認しますか？"
    品質の問題なので、既定のメトリクスでは分かりません。ゴールデンデータセットで新旧のプロンプトのバージョンを比較し、呼び出しログで応答の変化を見ます。悪化が確認できたらプロンプトのバージョンを戻します。今後は評価スコアをカスタムメトリクスで送り、CI/CD に品質ゲートを入れます。

??? question "問6: エージェントの月額が急に 3 倍になりました。呼び出しの数はほぼ同じです。どこから調べますか？"
    Cost Anomaly Detection で発見し、`InputTokenCount` と `OutputTokenCount`、アプリケーション推論プロファイルのタグでアプリを特定します。呼び出しログと Logs Insights でトークンの多い呼び出しを探します。履歴が要約されず増えている、ツールの結果が長い、取得するチャンクが増えた、などが候補です。上限と刈り込みを入れます。

# 分野2: ML モデルと FM の開発

MLA-C02 の配点は **24%** です。手法の選択、学習と調整、評価の3つのタスクがあります。従来の ML と FM の両方が問われ、どちらを使うかの判断も範囲です。

## タスク 2.1: 適切なモデリング手法を選ぶ {#task-2-1}

### 2.1.1 Bedrock の FM の評価と選択 {#skill-2-1-1}

要件からモデルを絞り込み、同じプロンプトと評価データで数個を比べます。

| 観点 | 確認すること | 例 |
|---|---|---|
| モダリティ | テキスト、画像、動画、音声 | 図表を読むならマルチモーダル |
| コンテキスト長 | 入出力の長さ | 長い契約書なら長いモデル |
| 遅延 | `TimeToFirstToken` | 対話なら小さなモデルとストリーミング |
| コスト | トークン単価 | 大量の分類なら安いモデル |
| カスタマイズ | 調整の可否 | ファインチューニングできるモデルは限られる |
| ライフサイクル | Active、Legacy、EOL | 長期運用なら EOL の日付を確認 |

EOL に達するとリクエストは失敗し、自動の移行はありません。`ListFoundationModels` で状態を確認し、モデル ID は設定で変えられるようにします。

詳細: [FM の選定の観点](../../services/genai-apps.md#fm-criteria)、[モデルのライフサイクル](../../services/genai-apps.md#model-lifecycle)、[Nova と Titan](../../services/genai-apps.md#nova-titan)

### 2.1.2 事前学習済み FM のファインチューニング戦略 {#skill-2-1-2}

上から順に検討します。手軽な方法で足りるなら、重みは調整しません。

| 要件 | 戦略 |
|---|---|
| 指示の工夫で足りる | プロンプト設計 |
| 情報が頻繁に変わる、引用が必要 | RAG |
| 文体や形式を学ばせたい、正解の例がある | 教師ありファインチューニング |
| 正解は決めにくいが採点はできる | 強化ファインチューニング |
| 精度を保ち、推論のコストを下げたい | 蒸留 |
| 少ない GPU で用途別のモデルを提供したい | SageMaker AI の LoRA アダプター |

「最新の社内規定に答えさせる」はファインチューニングではなく RAG です。規定を更新しても再学習が要りません。

詳細: [モデルカスタマイズ](../../services/genai-apps.md#customization)、[方法の比較](../../services/ai-fundamentals.md#customization-options)、[SageMaker AI での FM](../../services/genai-apps.md#sagemaker-fm)

### 2.1.3 モデル、アルゴリズム、テンプレートの比較 {#skill-2-1-3}

業務の要件を、問題の種類とデータに置き換えます。

| 要件 | 選択 |
|---|---|
| 表データの分類、回帰の第一候補 | XGBoost |
| 解釈可能性が必須 | Linear Learner、決定木系と SHAP |
| 似た系列が多い需要予測 | DeepAR |
| ラベルなしの異常検知 | Random Cut Forest |
| グループ分け | K-Means |
| 文章の話題を教師なしで | LDA、NTM |
| 高次元の疎データ、クリック予測 | Factorization Machines |
| 文章の生成、要約 | Bedrock の FM |
| よくある用途のインフラをまとめて作る | JumpStart のソリューションテンプレート |

遅延が厳しいなら小さなモデル、ドメイン固有の性能が必要なら、ドメインのデータで評価して決めます。

詳細: [組み込みアルゴリズム](../../services/sagemaker.md#built-in-algorithms)、[JumpStart](../../services/sagemaker.md#jumpstart)、[従来の ML と FM](../../services/ai-fundamentals.md#ml-vs-fm)、[説明可能性](../../services/ai-fundamentals.md#explainability)

### 2.1.4 独自開発、マネージド、事前学習済み、FM のトレードオフ {#skill-2-1-4}

| 選択肢 | 制御 | 手間 | 向いている場面 |
|---|---|---|---|
| マネージド AI サービス | 小 | 最小 | OCR、文字起こしなど決まった作業 |
| Bedrock の FM | 中 | 小 | 生成、要約。トークン課金 |
| JumpStart の事前学習済みモデル | 大 | 中 | FM を自分のインスタンスで制御する |
| SageMaker AI で独自に学習 | 最大 | 最大 | 独自の表データ、独自のアルゴリズム |

決まった作業を大量に確実に行うなら、FM より専用の AI サービスを選びます。出力の形式が決まっていて再現性も高いからです。

詳細: [マネージド AI サービスと Bedrock](../../services/ai-managed-services.md#vs-bedrock)、[AI の 3 階層](../../services/ai-managed-services.md#three-layers)、[選び方の比較](../../services/sagemaker.md#choosing)

### 2.1.5 RAG のアーキテクチャパターン {#skill-2-1-5}

| 要件 | パターン |
|---|---|
| 素早く作り、管理を減らす | Managed Knowledge Base |
| ベクトル DB を自分で制御する | Customer-managed と OpenSearch など |
| データウェアハウスへの質問 | 構造化データストア（自然文を SQL に変換） |
| 関係をたどる質問 | Neptune Analytics の GraphRAG |
| モデルが必要なときだけ検索する | 検索をツールや MCP サーバーとして公開する |

Managed では `RetrieveAndGenerate` を使えません。`Retrieve` で検索し、生成は別に呼びます。

詳細: [Managed と Customer-managed](../../services/genai-apps.md#managed-kb)、[Knowledge Bases を呼ぶ](../../services/ai.md#knowledge-bases)、[RAG](../../services/ai-fundamentals.md#rag)、[選び方の比較](../../services/genai-apps.md#choosing)

### 2.1.6 ML の性能、学習時間、コストのトレードオフ {#skill-2-1-6}

| 手段 | 効果 | 代償 |
|---|---|---|
| インスタンスを増やす | 時間が減る | 通信のため比例しては減らない |
| Managed Spot | 最大 90% 安い | 中断がある。オンデマンドに切り替わらない |
| 複雑なモデル | 精度が上がることがある | 時間、コスト、解釈のしやすさ |
| 早期停止 | 時間と過学習を抑える | 指標を出すアルゴリズムが必要 |
| AMT の試行を増やす | 精度が上がることがある | ジョブの数だけコストが増える |

安く済むのは、スポット、チェックポイント、適切なサイズの組み合わせです。課金時間 100 秒、学習時間 500 秒なら節約率は 80% です。

詳細: [分散学習と時間短縮](../../services/sagemaker.md#distributed-training)、[マネージドスポット学習](../../services/sagemaker.md#spot-training)、[インスタンスの選び方](../../services/sagemaker.md#instance-selection)

### 2.1.7 AI モデルの性能、遅延、コストのトレードオフ {#skill-2-1-7}

| 手段 | 効果 | 注意 |
|---|---|---|
| 小さなモデル | 速くて安い | 品質を評価して確かめる |
| モデルカスケード | 難しい質問だけ上位へ | 判定の処理が要る |
| Intelligent Prompt Routing | Bedrock が同じ系統のモデルから選ぶ | 同じ系統の中だけ |
| プロンプトキャッシュ | 固定の前半を再利用 | 固定の内容を先に置く |
| ストリーミング | 体感の待ち時間が減る | 全体の時間は変わらない |
| バッチ、Flex | 安くなる | 遅い。対話には向かない |
| Priority | 速くなる | 割増 |

詳細: [動的なモデル切り替え](../../services/genai-apps.md#dynamic-model-selection)、[トークンの削減](../../services/genai-apps.md#token-efficiency)、[遅延の短縮](../../services/genai-apps.md#latency)、[Bedrock の料金](../../services/cost-management.md#bedrock-pricing)

### 2.1.8 AWS の AI サービスの適用 {#skill-2-1-8}

| 業務 | サービス |
|---|---|
| 請求書やフォームから項目を抽出 | Textract |
| 不適切な画像の検出、顔の照合 | Rekognition |
| 感情、固有表現、テキストの PII | Comprehend |
| 医療のテキスト | Comprehend Medical |
| 通話の文字起こし | Transcribe |
| 翻訳 | Translate |
| 文字を音声に | Polly |
| チャットボット | Lex |
| レコメンド | Personalize |
| FHIR での医療データ | HealthLake |

紛らわしい組み合わせに注意します。Comprehend は文の意味を、Textract は文書の文字を扱います。Rekognition は写真や動画、Textract は文書です。

詳細: [選び方](../../services/ai-managed-services.md#choosing)、[紛らわしい組み合わせ](../../services/ai-managed-services.md#confusing-pairs)

## タスク 2.2: モデルを学習、調整、カスタマイズする {#task-2-2}

### 2.2.1 組み込みアルゴリズムと一般的なライブラリ {#skill-2-2-1}

組み込みアルゴリズムは、コンテナを用意せずに使えます。入力形式とインスタンスの種類を確認します。Linear Learner は CSV と recordIO-protobuf を受け付けます。K-Means は CPU が推奨です。

一般的なライブラリとして、scikit-learn、PyTorch、TensorFlow はフレームワークのコンテナで動かします。組み込みに合わなければ、スクリプトモードに進みます。

詳細: [組み込みアルゴリズム](../../services/sagemaker.md#built-in-algorithms)、[学習ジョブの設定](../../services/sagemaker.md#training-job)

### 2.2.2 スクリプトモードの設定 {#skill-2-2-2}

AWS が用意したフレームワークのコンテナで、自分のスクリプトを動かします。独自のコンテナを作らずに済むので、まず検討します。

| コンテナ内のパス | 内容 | 環境変数 |
|---|---|---|
| `/opt/ml/input/data/<チャネル名>` | 入力データ | `SM_CHANNEL_<チャネル名>` |
| `/opt/ml/model` | 保存したモデルが `model.tar.gz` で S3 へ | `SM_MODEL_DIR` |
| `/opt/ml/output/data` | その他の成果物 | `SM_OUTPUT_DATA_DIR` |

`/opt/ml/model` の外に保存したモデルは失われます。追加のパッケージは `source_dir` の `requirements.txt` に書きます。

大きなデータで開始までが長いなら、File モードのダウンロードが原因です。FastFile に変えます。

詳細: [スクリプトモード](../../services/sagemaker.md#script-mode)、[入力モード](../../services/sagemaker.md#input-modes)

### 2.2.3 ハイパーパラメータの最適化 {#skill-2-2-3}

| 戦略 | 向いている場面 | 注意 |
|---|---|---|
| Bayesian | 既定の選択。試行数を減らす | 並列数を増やしすぎると学習効果が減る |
| Random | 並列で一気に試す | 前の結果を使わない |
| Grid | カテゴリ値を網羅する | カテゴリのパラメータのみ |
| Hyperband | エポックごとに指標を出す反復型 | `TrainingJobEarlyStoppingType` は `Off` |

学習率のように桁が変わる範囲は、`ScalingType` を `Logarithmic` にします。前回の結果を活かすならウォームスタートで、親は最大 5 個です。同じデータなら `IDENTICAL_DATA_AND_ALGORITHM`、データを変えるなら `TRANSFER_LEARNING` です。

詳細: [自動モデルチューニング](../../services/sagemaker.md#amt)

### 2.2.4 学習時間の短縮 {#skill-2-2-4}

| 手法 | 使いどころ |
|---|---|
| 早期停止（AMT の `Auto`） | 改善しないジョブを止める |
| データ並列（SMDDP） | データが大きい |
| モデル並列（SMP） | モデルが 1 枚の GPU に載らない |
| FastFile | データのダウンロードが遅い |
| HyperPod | 長時間の大規模な FM の学習。ノード障害から回復する |

詳細: [分散学習と時間短縮](../../services/sagemaker.md#distributed-training)、[入力モード](../../services/sagemaker.md#input-modes)

### 2.2.5 過学習、過少適合、破滅的忘却の防止 {#skill-2-2-5}

| 状態 | 学習の精度 | 検証の精度 | 対策 |
|---|---|---|---|
| 過少適合 | 65% | 64% | 特徴量を増やす、複雑なモデル、長く学習、正則化を弱める |
| 過学習 | 99% | 70% | データを増やす、正則化、ドロップアウト、早期停止、特徴量を減らす |

正則化では、L1 は不要な重みを 0 にし、L2 は重みを全体に小さくします。

**破滅的忘却**は、新しいデータだけで追加学習すると、以前学んだ内容を忘れる現象です。新旧のデータを混ぜる、学習率を下げる、一部の層を固定する、といった対策があります。

詳細: [過学習](../../services/ai-fundamentals.md#overfitting)、[正則化](../../services/ai-fundamentals.md#regularization)

### 2.2.6 複数モデルの組み合わせ {#skill-2-2-6}

| 手法 | 仕組み | 主な効果 | 例 |
|---|---|---|---|
| バギング | 復元抽出で並列に学習し、平均や多数決 | バリアンスを下げる | ランダムフォレスト |
| ブースティング | 前のモデルの誤りを次が補う | バイアスを下げる | XGBoost |
| スタッキング | 複数の出力を別のモデルに入れる | 精度を上げる | AutoGluon-Tabular |

過学習しているならバギング、過少適合ならブースティングです。コストを下げる組み合わせには、小さなモデルで処理して難しいものだけ大きなモデルに渡すカスケードがあります。

詳細: [アンサンブル](../../services/ai-fundamentals.md#ensembles)、[動的なモデル切り替え](../../services/genai-apps.md#dynamic-model-selection)

### 2.2.7 基本のハイパーパラメータの調整 {#skill-2-2-7}

| 項目 | 誤ったときの症状 |
|---|---|
| エポック | 少ないと過少適合、多いと過学習 |
| バッチサイズ | 大きいとメモリ不足や汎化の低下、小さいと損失がぶれる |
| 学習率 | 大きいと損失が発散、小さいと収束が遅い |

データ 10,000 件、バッチサイズ 100 なら、1 エポックは 100 ステップです。10 エポックで 1,000 ステップになります。

詳細: [正則化と学習の設定](../../services/ai-fundamentals.md#regularization)

### 2.2.8 AI ソリューションのカスタマイズ {#skill-2-2-8}

| 手法 | 例 |
|---|---|
| 指示を具体的に | 役割と出力の形式を定める |
| フューショット | 分類の基準を例で示す |
| Chain-of-thought | 計算や推論を段階的に考えさせる |
| 構造化出力 | JSON Schema に合わせて返させる |
| パラメータ | 抽出や分類は temperature を 0〜0.2、文案は 0.7 以上 |
| ファインチューニング | プロンプトで足りないときに重みを調整する |

まずプロンプトを調整し、Bedrock Prompt Management でバージョンとバリアントを比べます。

詳細: [プロンプトエンジニアリング](../../services/ai-fundamentals.md#prompt-engineering)、[パラメータの調整](../../services/genai-apps.md#parameter-tuning)、[構造化出力](../../services/genai-apps.md#structured-output)、[プロンプトの管理](../../services/genai-apps.md#prompt-management)

### 2.2.9 検索コンポーネントと埋め込みモデルの最適化 {#skill-2-2-9}

| 症状 | 調整 |
|---|---|
| 製品番号など固有の語で外れる | ハイブリッド検索 |
| 上位に関係のない文書が混ざる | リランク、メタデータフィルター |
| 複雑な質問で文書が足りない | クエリ分解 |
| 同義語で見つからない | クエリ拡張 |
| 意味の似た文書を区別できない | 次元の大きい埋め込み、別のモデル |
| 保存と検索のコストが高い | 次元を下げる。精度を評価で確かめる |

上位 20 件を取ってリランクで 5 件に絞ると、精度とトークンコストの両方が改善します。

詳細: [検索の改善](../../services/genai-apps.md#retrieval-optimization)、[埋め込みの選び方](../../services/genai-apps.md#embedding-selection)

## タスク 2.3: ML と AI システムの性能を分析し評価する {#task-2-3}

### 2.3.1 再現可能な実験 {#skill-2-3-1}

| ツール | 記録するもの | 用途 |
|---|---|---|
| MLflow on SageMaker AI | パラメータ、指標、成果物 | 従来の ML と FM の実験 |
| Bedrock Evaluations | モデルとプロンプトの評価結果 | FM の比較 |
| Bedrock Prompt Management | プロンプトのバージョンとバリアント | プロンプトの比較 |

再現するには、データのバージョン、コードのコミット、ハイパーパラメータを記録します。

詳細: [MLflow](../../services/sagemaker.md#mlflow)、[Bedrock Evaluations](../../services/genai-apps.md#bedrock-evaluations)、[プロンプトの管理](../../services/genai-apps.md#prompt-management)

### 2.3.2 ベースラインの作成とドリフト検知 {#skill-2-3-2}

!!! note "Model Monitor の提供状況"
    SageMaker Model Monitor は新規顧客の受付を終了しています。公式の移行先は、公開の監視ソリューション（MLflow Apps と Evidently AI）、QuickSight、CloudWatch です。

学習時のデータと性能をベースラインにして、本番と比べます。

| 種類 | 意味 | 検出 |
|---|---|---|
| データドリフト | 入力の分布が変わる | 分布の距離 |
| コンセプトドリフト | 入力と正解の関係が変わる | 正解ラベルとの比較 |
| 予測ドリフト | 出力の分布が変わる | 出力の統計 |
| バイアスドリフト | 集団間の差が変わる | 集団別の指標 |

Model Monitor の流れは、ベースラインの統計と制約を作る、データキャプチャで本番のデータを取る、スケジュールで比較する、結果を CloudWatch に出す、です。モデル品質の監視には正解ラベルが必要です。

移行後の構成では、Processing で Evidently AI を動かし、EventBridge Scheduler で定期実行し、SNS で通知します。

詳細: [Model Monitor](../../services/sagemaker.md#model-monitor)、[ドリフトの種類](../../services/sagemaker.md#drift)

### 2.3.3 シャドウバリアントと本番バリアントの比較 {#skill-2-3-3}

シャドウテストは、本番のリクエストのコピーを新しいバリアントに送ります。応答は利用者に返さないので、影響がありません。

比べるのは、`ModelLatency`、エラー率、インスタンスの使用率です。正解は後から届くので、精度を見るならログを保存して結合します。

| 方式 | 利用者への影響 | 使いどころ |
|---|---|---|
| シャドウ | なし | 遅延と安定性を安全に確かめる |
| A/B | あり | 業務指標を比べる |

詳細: [デプロイとテストの戦略](../../services/sagemaker.md#deployment-strategies)、[CloudWatch のメトリクス](../../services/sagemaker.md#cloudwatch-metrics)

### 2.3.4 モデルの出力の説明 {#skill-2-3-4}

| 手法 | 内容 |
|---|---|
| SHAP | 特徴量ごとの予測への寄与。Clarify の説明の中心 |
| 部分依存プロット | 特徴量の変化と予測の関係 |
| Model Cards | 用途、学習、評価、リスクの記録 |
| 解釈しやすいモデル | 線形回帰、決定木 |
| 引用 | RAG の根拠を示す |
| エージェントのトレース | 推論の過程を示す |

「融資の否決理由を示す」なら SHAP です。Clarify を新規に使えないなら、SHAP ライブラリを直接使います。

詳細: [Clarify](../../services/sagemaker.md#clarify)、[説明可能性と透明性](../../services/ai-fundamentals.md#explainability)、[Model Cards](../../services/sagemaker.md#model-cards)

### 2.3.5 収束の問題のデバッグ {#skill-2-3-5}

!!! note "Debugger の提供状況"
    SageMaker Debugger は新規顧客の受付を終了しています。公式の移行先は、学習の指標に MLflow と TensorBoard、プロファイルに CloudWatch です。

| 症状 | 原因の候補 | 対応 |
|---|---|---|
| 損失が発散、`NaN` | 学習率が高い、勾配爆発、欠損 | 学習率を下げる、勾配クリッピング |
| 損失が下がらない | 学習率が低い、バグ | 少量のデータで過学習できるか試す |
| 勾配消失 | 深すぎる、活性化関数 | ReLU、残差接続、正規化 |
| 検証の損失だけ上がる | 過学習 | 正則化、早期停止 |
| GPU の使用率が低い | データ読み込みが遅い | FastFile、ローダーの並列化 |

詳細: [収束の問題](../../services/sagemaker.md#convergence)、[Debugger](../../services/sagemaker.md#debugger)

### 2.3.6 従来の ML と生成 AI の評価手法 {#skill-2-3-6}

**分類:** スパム 100 通、通常 900 通で、TP 80、FN 20、FP 30、TN 870 とします。

| 指標 | 計算 | 重視する場面 |
|---|---|---|
| 精度 | 950 / 1000 = 0.95 | クラスが均衡している |
| 適合率 | 80 / 110 = 0.727 | 誤検知の損失が大きい |
| 再現率 | 80 / 100 = 0.80 | 見逃しの損失が大きい |
| F1 | 160 / 210 = 0.762 | 両方を見る |
| AUC | しきい値によらず比較する | 0.5 がランダム、1.0 が完全 |

**回帰:** MAE は外れ値に強く、RMSE は大きな誤差を強く罰します。R² は 1 に近いほどよいです。

**生成 AI:** 正解が 1 つに決まらないので、自動の指標、人の評価、LLM の採点を組み合わせます。

詳細: [評価指標](../../services/ai-fundamentals.md#metrics)、[AUC](../../services/ai-fundamentals.md#auc)、[回帰の指標](../../services/ai-fundamentals.md#regression-metrics)、[評価](../../services/genai-apps.md#evaluation)

### 2.3.7 人による評価の組み込み {#skill-2-3-7}

!!! note "Augmented AI の提供状況"
    Amazon Augmented AI（A2I）は新規顧客の受付を終了しています。新規の代替の例は、Step Functions の人の承認と Bedrock の人による評価です。

| 目的 | 手段 |
|---|---|
| 文章の品質を人が評価する | Bedrock Evaluations の人のジョブ |
| 信頼度が低い予測を人に回す | A2I、または Step Functions の `waitForTaskToken` |
| 利用者の評価を集める | API Gateway、Lambda、DynamoDB |

A2I の起動条件は、信頼度のしきい値（例: 80% 未満）やランダムサンプリング（例: 5%）です。低評価の例はレビューして、ゴールデンデータセットやプロンプトの改善に使います。

詳細: [Bedrock Evaluations](../../services/genai-apps.md#bedrock-evaluations)、[Augmented AI](../../services/ai-managed-services.md#a2i)、[人による確認](../../services/genai-apps.md#human-in-the-loop)、[利用者からの評価](../../services/genai-apps.md#user-feedback)

### 2.3.8 NLP の評価指標 {#skill-2-3-8}

| 指標 | 用途 | 見るもの |
|---|---|---|
| BLEU | 機械翻訳 | 正解文との n-gram の一致。適合率寄り。短い文には罰 |
| ROUGE | 要約 | 正解要約の語をどれだけ含むか。再現率寄り |
| BERTScore | 翻訳、要約 | BERT 埋め込みで意味の近さを比べる |
| 意味的類似度 | 回答の比較 | 埋め込みのコサイン類似度。1 に近いほど似ている |

BLEU と ROUGE は語の一致を見るので、意味が同じ言い換えを低く評価します。言い換えも正しく評価したいなら BERTScore です。

a = (1, 0)、b = (1, 1) のコサイン類似度は 1 / 1.414 = 0.707 です。

詳細: [NLP の指標](../../services/ai-fundamentals.md#nlp-metrics)

### 2.3.9 AI の評価 {#skill-2-3-9}

LLM-as-a-judge は、別の LLM が出力を採点して説明を付ける方法です。Bedrock Evaluations の判定モデルで実行します。

| 区分 | 指標 |
|---|---|
| 品質 | Correctness、Completeness、Faithfulness、Helpfulness、Relevance |
| 安全 | Harmfulness、Stereotyping、Refusal |

バイアスの検出には、Stereotyping の指標や、属性だけを変えたプロンプトの比較を使います。エージェントは AgentCore Evaluations でトレースを採点します。

詳細: [Bedrock Evaluations](../../services/genai-apps.md#bedrock-evaluations)、[エージェントの評価](../../services/genai-apps.md#agent-evaluation)、[透明性と公平性](../../services/genai-apps.md#transparency-fairness)

### 2.3.10 RAG の監視と検索精度の評価 {#skill-2-3-10}

| ジョブ | 指標 |
|---|---|
| 取得のみ | ContextRelevance、ContextCoverage |
| 取得と生成 | Correctness、Faithfulness、CitationPrecision、CitationCoverage など |

| 結果 | 原因の候補 |
|---|---|
| ContextRelevance が低い | チャンク、埋め込み、検索 |
| ContextCoverage が低い | 取得件数が少ない、文書がない |
| 取得はよいが Faithfulness が低い | 生成。プロンプトやモデルを変える |

運用では、検索の遅延（p95、p99）、最終同期の時刻、評価の定期実行を見ます。誤答の調査は、取得が正しいか、文書に答えがあるか、生成が文書に従っているか、の順に分けます。

詳細: [Bedrock Evaluations](../../services/genai-apps.md#bedrock-evaluations)、[ベクトルストアの運用](../../services/genai-apps.md#vector-operations)、[トラブルシューティング](../../services/genai-apps.md#troubleshooting)

## 確認問題 {#self-check}

??? question "問1: 融資の審査モデルで、規制により否決の理由を説明する必要があります。深層学習モデルは精度が 1 ポイント高いだけです。どう選びますか？"
    説明しやすいモデルを選びます。XGBoost などの決定木系と SHAP、または Linear Learner です。説明が必須の場面では、わずかな精度より説明しやすさを優先します。

??? question "問2: 社内の 2,000 件の規定に答えるチャットボットを作ります。規定は毎週更新され、回答には根拠の文書も示します。ファインチューニングと RAG のどちらにしますか？"
    RAG です。更新のたびに同期すればよく、再学習は要りません。引用で根拠も示せます。ファインチューニングは文体や形式を学ばせる場面に向きます。

??? question "問3: GPU の学習ジョブの費用を最大限に下げたいです。ジョブは中断されても構いません。設定で必要なものを挙げ、容量がないときの動作も答えてください。"
    `EnableManagedSpotTraining` を有効にし、`MaxWaitTimeInSeconds` を `MaxRuntimeInSeconds` より大きくし、チェックポイントを S3 に保存します。容量がないときは上限まで待って終了し、オンデマンドには切り替わりません。

??? question "問4: 学習の精度が 99%、検証の精度が 72% です。学習を続けても検証の損失が上がっていきます。何が起きていて、どう対応しますか？"
    過学習です。早期停止、L1 や L2 の正則化、ドロップアウト、データの追加、特徴量の削減で対応します。エポックを増やすと悪化します。

??? question "問5: 要約モデルの評価で ROUGE は低いのに、担当者が読むと内容は正確です。言い換えが多いモデルです。どの指標を足しますか？"
    BERTScore か意味的類似度です。ROUGE は語の一致を見るので言い換えを低く評価します。埋め込みで比べる指標なら意味の近さを評価できます。品質全般には LLM-as-a-judge も使えます。

??? question "問6: RAG の回答が誤っています。評価の結果、ContextRelevance は高く、Faithfulness は低いです。チャンクと埋め込みを変える案は適切ですか？"
    適切ではありません。正しい文書は取得できているので、問題は生成の側です。プロンプトで文書に基づいて答えるよう指示する、モデルを変える、コンテキストグラウンディングで参照元に基づかない応答を止める、といった対応をします。

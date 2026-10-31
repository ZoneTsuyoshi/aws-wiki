# 分野1: AI と ML の組み込み

モデルを作る話ではなく、アーキテクトとして組み込み方を判断します。統制の置き場所、エージェントの部品、推論の方式、RAG の構成が中心です。モデルの学習とファインチューニングは範囲外です。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [1.2.1](../../domain1.md#skill-1-2-1) | 生成 AI の統合とマルチアカウント |
| [1.2.2](../../domain1.md#skill-1-2-2) | ツールと連携する AI エージェント |
| [1.2.3](../../domain1.md#skill-1-2-3) | ML の推論アーキテクチャ |
| [1.2.4](../../domain1.md#skill-1-2-4) | RAG のアーキテクチャ |

## 学習の順番 {#study-order}

1. [推論の容量とプロファイル](../../../../services/genai-apps.md#inference-profiles): アプリケーション推論プロファイルとクロスリージョン推論を区別します。
2. [組織での強制](../../../../services/genai-apps.md#guardrail-org-enforcement)と [GenAI ゲートウェイ](../../../../services/genai-apps.md#genai-gateway): コードを変えずに強制する方法と、中央に集める方法を比べます。
3. [VPC エンドポイントでの接続](../../../../services/ai.md#privatelink)と[耐障害の設計](../../../../services/genai-apps.md#fm-resilience): 閉域とスロットリングへの備えを確認します。
4. [AgentCore のアーキテクチャ](../../../../services/genai-apps.md#agentcore)、[AgentCore の構成要素](../../../../services/ai.md#agentcore-components)、[Policy](../../../../services/genai-apps.md#agentcore-policy): 要件と部品の対応を覚えます。
5. [エンドポイントと推論](../../../../services/sagemaker.md#endpoints)と[マルチモデル](../../../../services/sagemaker.md#multi-model): 入力の大きさと頻度で方式を選びます。
6. [Knowledge Bases](../../../../services/genai-apps.md#knowledge-bases)、[チャンク化の戦略](../../../../services/genai-apps.md#chunking)、[ベクトルストア](../../../../services/genai-apps.md#vector-stores)、[検索の改善](../../../../services/genai-apps.md#retrieval-optimization): RAG の各段階の判断を整理します。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| リアルタイム推論 | 入力 25 MB（FAQ。API リファレンスは 6 MB）、処理 60 秒（ストリーミングの応答は 8 分） | 常に低遅延 |
| 非同期推論 | 入力 1 GB、処理 1 時間 | 0 台まで縮小できる |
| 推論パイプライン | 2〜15 コンテナ | 前処理、推論、後処理を順に |
| 既定のチャンク化 | 約 300 トークン | 文の境界を保つ |
| Agents Classic の新規受付の終了 | 2026 年 7 月 30 日 | 新しい構成は AgentCore |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 共有のアカウントで、アプリごとに費用を配分 | タグ付きのアプリケーション推論プロファイル |
| コードを変えずに全アカウントへガードレールを強制 | Organizations の Bedrock ポリシー |
| データを EU にとどめてスロットリングを避ける | EU の地理的なプロファイル |
| 利用の制限、記録、モデルの隠蔽を集約 | 中央の GenAI ゲートウェイ |
| ツール呼び出しの金額の制限を確実に | AgentCore の Policy |
| API や Lambda を MCP ツールに、外部の OAuth | Gateway と Identity |
| セッションをまたぐ好みの保持 | Memory の長期記憶 |
| 大きな入力、長い処理、不定期 | 非同期推論 |
| 同じフレームワークの多数の小さなモデル | マルチモデルエンドポイント |
| データセット全体を定期的に | バッチ変換 |
| 既存の PostgreSQL と SQL で結合 | pgvector |
| 大量で低頻度、保管費用を最小に | S3 Vectors |
| 番号や固有名詞が検索に外れる | ハイブリッド検索とリランキング |
| 細かく検索して広い文脈を返す | 階層チャンク化 |

## 引っかかりやすい点 {#traps}

- 推論プロファイルは Provisioned Throughput に対応していません。
- グローバルのプロファイルは地域の外へ送られることがあります。データの地域の要件があれば、地理的なプロファイルです。
- `bedrock:GuardrailIdentifier` の条件は、呼び出しに指定がないと拒否するので、コードの変更が必要です。
- プロンプトの規則や Guardrails は、ツールの入力値による認可の代わりになりません。
- ハイブリッド検索に対応するのは RDS、OpenSearch Serverless、MongoDB です。
- 埋め込みモデルを変えると全件の再取り込みが必要です。データの追加や更新の同期は増分です。
- Bedrock Agents Classic は新規顧客を受け付けていません。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [ai-ml 問1](../../exercises/ai-ml.md#q1) | 1.2.1 | 共有のアカウントで、5 つのアプリが同じ Bedrock の基盤モデルを呼んでいます。経理は、アプリ… |
| [ai-ml 問2](../../exercises/ai-ml.md#q2) | 1.2.1 | 組織の 100 以上のアカウントで、各チームが独自に Bedrock を呼んでいます。セキュリティ部… |
| [ai-ml 問3](../../exercises/ai-ml.md#q3) | 1.2.1 | EU の金融機関が、プライベートサブネットのアプリから Bedrock を呼びます。通信はインターネ… |
| [ai-ml 問4](../../exercises/ai-ml.md#q4) | 1.2.1 | 40 のチームが複数のモデルを使います。プラットフォームチームは、チームごとの利用の制限と全呼び出し… |
| [ai-ml 問5](../../exercises/ai-ml.md#q5) | 1.2.2 | カスタマーサポートの AI エージェントが、30 個の既存の社内 API をツールとして呼びます。「… |
| [ai-ml 問6](../../exercises/ai-ml.md#q6) | 1.2.2 | 新しいエージェントから、社内の Lambda 関数と REST API を MCP のツールとして使… |
| [ai-ml 問7](../../exercises/ai-ml.md#q7) | 1.2.2 | 旅行の相談エージェントを本番に公開します。利用者のセッションは互いに分離します。前回までの好みや予約… |
| [ai-ml 問8](../../exercises/ai-ml.md#q8) | 1.2.3 | 医療画像の解析モデルを SageMaker AI で動かします。入力は 1 件あたり最大 800 M… |
| [ai-ml 問9](../../exercises/ai-ml.md#q9) | 1.2.3 | 需要予測の SaaS は、3,000 の顧客それぞれに小さなモデルを持ちます。モデルのフレームワーク… |
| [ai-ml 問10](../../exercises/ai-ml.md#q10) | 1.2.3 | 通信会社は、月に 1 回、全 5,000 万件の契約データで解約の可能性を推定します。自社で学習した… |
| [ai-ml 問11](../../exercises/ai-ml.md#q11) | 1.2.4 | 社内ヘルプデスクの RAG を、Bedrock Knowledge Bases で作ります。製品の情… |
| [ai-ml 問12](../../exercises/ai-ml.md#q12) | 1.2.4 | 法律事務所が、過去 20 年の 数億チャンク規模の判例を RAG で検索します。アクセスは 1 日に… |
| [ai-ml 問13](../../exercises/ai-ml.md#q13) | 1.2.4 | 製品マニュアルの RAG で、問いに合う小さな手順は見つかりますが、回答に必要な前後の文脈が足りませ… |
| [ai-ml 問14](../../exercises/ai-ml.md#q14) | 1.2.4 | 保守の手順書の RAG で、XJ-4102 のような部品番号の検索が外れます。意味の近い文書は返りま… |
| [ai-ml 問15](../../exercises/ai-ml.md#q15) | 1.2.4 | SaaS に RAG の機能を追加します。大半のテナントは共有で構いませんが、数社の規制対象のテナン… |

<!-- questions:end -->

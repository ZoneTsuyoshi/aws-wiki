# 分野2: Bedrock の API 統合

呼び方の選択、ストリーミング、再試行、タイムアウトを扱います。設定値の違いがそのまま問われます。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [2.4.1](../../domain2.md#skill-2-4-1) | 柔軟なモデル呼び出し |
| [2.4.2](../../domain2.md#skill-2-4-2) | リアルタイムの応答 |
| [2.4.3](../../domain2.md#skill-2-4-3) | 信頼性の高い FM システム |
| [2.5.1](../../domain2.md#skill-2-5-1) | 生成 AI 向けの API |

## 学習の順番 {#study-order}

1. [API の選び方](../../../../services/ai.md#invoke-apis)と[スループットの選択肢](../../../../services/ai.md#throughput-options): 同期、非同期、バッチの選択を整理します。
2. [SQS と Lambda の設定](../../../../services/messaging.md#sqs-lambda-settings)と[リクエストの検証](../../../../services/api-gateway.md#request-validation): 非同期の入口を確認します。
3. [レスポンスストリーミング](../../../../services/api-gateway.md#response-streaming)と [WebSocket API](../../../../services/api-gateway.md#websocket): 片方向と双方向の違いと制約を覚えます。
4. [ストリームのイベント](../../../../services/ai.md#stream-events): `usage` の届く位置を押さえます。
5. [エラー処理とスロットリング](../../../../services/ai.md#errors-throttling)と [SDK の再試行モード](../../../../services/sdk-resilience.md#retry-modes): 再試行の対象と多重の再試行を理解します。
6. [クォータとトークンの数え方](../../../../services/ai.md#quotas-detail)と [VPC エンドポイントでの接続](../../../../services/ai.md#privatelink): 予約の計算と 350 秒の切断を確認します。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| REST API のストリーミング | 最大 15 分 | `HTTP_PROXY`、`AWS_PROXY` のみ |
| ストリーミングのアイドル | リージョン 5 分、エッジ最適化 30 秒 |  |
| ストリーミングの帯域 | 10 MB 超で 2 MB/秒 | 切断はされない |
| WebSocket | 接続 2 時間、アイドル 10 分 |  |
| REST API の統合タイムアウト | 既定 29 秒 | リージョンとプライベートは引き上げ可 |
| インターフェイスエンドポイントのアイドル | 350 秒で固定 | TCP キープアライブ |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 待てない、急増する | SQS と Lambda |
| 大量で翌朝まで | バッチ推論 |
| 途中の指示を同じ接続で送る | WebSocket API |
| 集中的なスロットリング | `adaptive` モード |
| チームごとの量を抑える | 使用量プラン |

## 引っかかりやすい点 {#traps}

- ストリーミングでは VTL の応答変換とエンドポイントのキャッシュを使えません。
- 可視性タイムアウトは Lambda のタイムアウト以上にします。公式の推奨は 6 倍以上です。
- SDK、Lambda、Step Functions の再試行は掛け算で増えます。
- `maxTokens` が大きいと、実際の出力が少なくてもスロットリングが起きます。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [bedrock-api 問1](../../exercises/bedrock-api.md#q1) | 2.4.1 | 問い合わせの要約を、API で受けて SQS 経由で Lambda から FM に送っています。応答… |
| [bedrock-api 問2](../../exercises/bedrock-api.md#q2) | 2.4.1 | FM を呼ぶ API に、必須項目のない不正なリクエストが多く届き、Lambda と FM の費用が… |
| [bedrock-api 問3](../../exercises/bedrock-api.md#q3) | 2.4.1 | Lambda と ECS で動くアプリから Bedrock を呼びます。担当者はアクセスキーを環境変… |
| [bedrock-api 問4](../../exercises/bedrock-api.md#q4) | 2.4.1 | 1 つのアプリに 3 種類の処理があります。(a) 画面で待つ質問応答、(b) 不定期に急増するアッ… |
| [bedrock-api 問5](../../exercises/bedrock-api.md#q5) | 2.4.2 | チャットを REST API と Lambda の非プロキシ統合で提供しています。回答に 1 分近く… |
| [bedrock-api 問6](../../exercises/bedrock-api.md#q6) | 2.4.2 | 生成 AI のエディタで、モデルの応答を順に表示します。利用者は生成の途中で「止める」「別の方向で続… |
| [bedrock-api 問7](../../exercises/bedrock-api.md#q7) | 2.4.2 | ConverseStream でチャットを実装しました。利用者が途中で画面を閉じたとき、ループを抜け… |
| [bedrock-api 問8](../../exercises/bedrock-api.md#q8) | 2.4.2 | エッジ最適化の REST API でレスポンスストリーミングを有効にしました。モデルが長く考えて最初… |
| [bedrock-api 問9](../../exercises/bedrock-api.md#q9) | 2.4.3 | Bedrock の呼び出しに再試行を実装します。ThrottlingException、Valida… |
| [bedrock-api 問10](../../exercises/bedrock-api.md#q10) | 2.4.3 | SDK、Lambda の非同期呼び出し、Step Functions の Retry のそれぞれで再… |
| [bedrock-api 問11](../../exercises/bedrock-api.md#q11) | 2.4.3 | FM を呼ぶ API を複数の社内チームに公開しています。1 つのチームの大量の呼び出しで、他のチー… |
| [bedrock-api 問12](../../exercises/bedrock-api.md#q12) | 2.5.1 | あるアプリは maxTokens を指定せず呼んでいます。実際の応答は平均 300 トークンですが、… |
| [bedrock-api 問13](../../exercises/bedrock-api.md#q13) | 2.5.1 | REST API の Lambda 統合で FM を呼びます。回答に 40 秒かかる場合があり、AP… |
| [bedrock-api 問14](../../exercises/bedrock-api.md#q14) | 2.5.1 | インターフェイスエンドポイント経由で Bedrock を呼ぶ ECS のアプリで、非ストリーミングの… |

<!-- questions:end -->

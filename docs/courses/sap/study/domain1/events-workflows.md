# 分野1: イベントとワークフロー

配信の保証と順序を要件から読み取り、状態をどこに置くか、処理の途中で失敗したらどう再開するかを判断します。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [1.1.1](../../domain1.md#skill-1-1-1) | イベント駆動とメッセージングのパターン |
| [1.1.2](../../domain1.md#skill-1-1-2) | ステートレスな設計と状態の外部化 |
| [1.1.3](../../domain1.md#skill-1-1-3) | サーバーレスのデータ処理と分析 |
| [1.1.4](../../domain1.md#skill-1-1-4) | 永続的な実行パターンのワークフロー |
| [1.1.5](../../domain1.md#skill-1-1-5) | アカウントとリージョンをまたぐイベントルーティング |

## 学習の順番 {#study-order}

1. [選び方](../../../../services/messaging.md#how-to-choose)と[標準と FIFO](../../../../services/messaging.md#standard-fifo): 配信の保証と順序の違いを表で覚えます。
2. [パーティションキー](../../../../services/streaming.md#partition-key)と[冪等性](../../../../services/sdk-resilience.md#idempotency): 順序の単位の決め方と、重複への備えを確認します。
3. [ファンアウト](../../../../services/messaging.md#fanout): 宛先ごとにキューを分ける理由を押さえます。
4. [ステートフルとステートレス](../../../../services/sdk-resilience.md#stateful-stateless): 状態の種類ごとの置き場所を判断できるようにします。
5. [Athena](../../../../services/streaming.md#athena)、[Firehose](../../../../services/streaming.md#firehose)、[Glue の ETL ジョブ](../../../../services/data-engineering.md#glue-jobs): 処理の大きさで選びます。
6. [Standard と Express](../../../../services/step-functions.md#standard-express)と[サービス統合パターン](../../../../services/step-functions.md#integration-patterns): 実行の保証と承認待ちの作り方を理解します。
7. [イベントバス](../../../../services/messaging.md#event-buses)と[ルールとイベントパターン](../../../../services/messaging.md#eventbridge-rules): 転送の段数、権限、グローバルエンドポイントを確認します。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| FIFO の重複排除の時間枠 | 5 分 | 長い間隔の再送には処理側の冪等性が必要 |
| Step Functions Standard の最大実行時間 | 1 年 | 実行は正確に 1 回 |
| Step Functions Express の最大実行時間 | 5 分 | 非同期は少なくとも 1 回、同期は最大 1 回 |
| Lambda durable functions の最大実行時間 | 1 年 | 待機中のコンピューティング料金はかからない |
| Lambda の通常の実行 | 最大 15 分 | 長い処理は分けるかワークフローへ |
| EventBridge の転送 | 1 段 | 第 3 のバスへは届かない |
| グローバルエンドポイントの RTO、RPO | 360 秒、最大 420 秒 | 公式の推奨のアラームを使う場合 |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 再送の間隔が 5 分より長い | 冪等キーを DynamoDB へ条件付きで書き込む |
| 顧客ごとの順序と読み直し | Kinesis Data Streams で、キーを顧客 ID に |
| 順序が必要で FIFO が詰まる | `MessageGroupId` を順序の単位にする |
| 宛先ごとに自分のペースで処理 | SNS から SQS へのファンアウト |
| 消えると損失になるセッション | DynamoDB か MemoryDB |
| 消えても再ログインで済むセッション | ElastiCache |
| 承認を数週間待つ、監査の履歴が必要 | Standard とコールバックパターン |
| 大量で短い、結果を待たない | Express の非同期。処理を冪等に |
| Lambda のコードとしてワークフローを書く | Lambda durable functions |
| データベースをまたぐ取り消し | サーガパターン |
| 新しいアカウントが増えても設定を変えない | `aws:PrincipalOrgID` でバスを許可 |

## 引っかかりやすい点 {#traps}

- 同じパーティションキーや同じグループ ID を全件に付けると、並列度が 1 になります。
- 受信側のルールで第 3 のアカウントへ転送しても届きません。送信元のルールに宛先をすべて設定します。
- `account` を指定しないルールは、許可した他のアカウントのイベントにも一致します。
- グローバルエンドポイントでイベントのレプリケーションを無効にすると、復旧後にヘルスチェックを手動で戻す必要があります。カスタムバスは同じ名前で用意します。
- スティッキーセッションは可用性の対策になりません。インスタンスが消えれば状態も消えます。
- Athena の費用は保管ではなくスキャンの量で決まります。Parquet とパーティションで減らします。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [events-workflows 問1](../../exercises/events-workflows.md#q1) | 1.1.1 | 決済会社が、SQS 標準キューと Lambda で入金通知を処理しています。入金元のゲートウェイは、… |
| [events-workflows 問2](../../exercises/events-workflows.md#q2) | 1.1.1 | 小売の注文イベントを、請求、分析、不正検知の 3 チームが別々に読みます。同じ顧客の注文は発生順に処… |
| [events-workflows 問3](../../exercises/events-workflows.md#q3) | 1.1.1 | SQS FIFO キューで、全メッセージに同じ MessageGroupId を付けて送っています。… |
| [events-workflows 問4](../../exercises/events-workflows.md#q4) | 1.1.1 | 受注イベントを在庫、配送、不正検知の 3 システムへ配ります。各システムは自分のペースで処理し、1 … |
| [events-workflows 問5](../../exercises/events-workflows.md#q5) | 1.1.2 | EC 事業者の Web 層は、Auto Scaling グループの EC2 上で動いています。カート… |
| [events-workflows 問6](../../exercises/events-workflows.md#q6) | 1.1.2 | 動画の変換サービスが Fargate のタスクで動いています。利用者がアップロードした最大 5 GB… |
| [events-workflows 問7](../../exercises/events-workflows.md#q7) | 1.1.2 | オンラインゲームのマッチング前の待機情報を、複数のコンテナから読み書きします。1 ミリ秒未満で読み取… |
| [events-workflows 問8](../../exercises/events-workflows.md#q8) | 1.1.3 | Web のクリックログを、Kinesis Data Streams と Lambda で S3 に … |
| [events-workflows 問9](../../exercises/events-workflows.md#q9) | 1.1.3 | Kinesis Data Streams に複数のコンシューマーが既にいます。新たにすべてのレコード… |
| [events-workflows 問10](../../exercises/events-workflows.md#q10) | 1.1.3 | 金融の事業者が、毎晩 2 TB の CSV を複数の参照テーブルと結合し、S3 のキュレーション層に… |
| [events-workflows 問11](../../exercises/events-workflows.md#q11) | 1.1.4 | 保険金の請求処理は、複数の AWS サービスの呼び出しと、担当者の承認からなります。承認には最長 3… |
| [events-workflows 問12](../../exercises/events-workflows.md#q12) | 1.1.4 | センサーのデータを変換するワークフローを、毎秒数千回起動します。1 回は 30 秒以内に終わり、起動… |
| [events-workflows 問13](../../exercises/events-workflows.md#q13) | 1.1.4 | 開発チームは Python に習熟し、業務ロジックのほとんどを Lambda に書いています。注文の… |
| [events-workflows 問14](../../exercises/events-workflows.md#q14) | 1.1.4 | 注文、決済、配送はマイクロサービスに分かれ、データベースも Aurora と DynamoDB で別… |
| [events-workflows 問15](../../exercises/events-workflows.md#q15) | 1.1.5 | 30 個のメンバーアカウントのイベントを、監査アカウントの EventBridge バスへ送っていま… |
| [events-workflows 問16](../../exercises/events-workflows.md#q16) | 1.1.5 | 組織には 200 のアカウントがあり、毎月増えています。各アカウントのイベントを、中央アカウントの … |
| [events-workflows 問17](../../exercises/events-workflows.md#q17) | 1.1.5 | 受注システムは、カスタムイベントバスへ PutEvents します。リージョン障害でもイベントの受け… |
| [events-workflows 問18](../../exercises/events-workflows.md#q18) | 1.1.5 | 本番アカウントのイベントバスのポリシーで組織全体からの受信を許可したところ、既存のルール（sourc… |

<!-- questions:end -->

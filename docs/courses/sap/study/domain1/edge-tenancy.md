# 分野1: エッジとマルチテナント

エッジで何を実行するか、WebSocket の上限をどう設計で吸収するか、テナントをどの層でどう分離するかを判断します。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [1.1.11](../../domain1.md#skill-1-1-11) | エッジのアーキテクチャ |
| [1.1.12](../../domain1.md#skill-1-1-12) | WebSocket と発行購読によるリアルタイム処理 |
| [1.1.13](../../domain1.md#skill-1-1-13) | マルチテナントのアーキテクチャ |

## 学習の順番 {#study-order}

1. [Lambda@Edge と CloudFront Functions](../../../../services/networking.md#edge-functions)と[エッジ関数の制限](../../../../services/networking.md#edge-function-limits): 使えるイベントと機能の差を表で覚えます。
2. [WebSocket API](../../../../services/api-gateway.md#websocket): 接続の流れと、変更できない上限を確認します。
3. [マルチテナントのデータアクセス](../../../../services/secrets.md#multi-tenant)と[パターンの比較](../../../../services/secrets.md#tenant-patterns): サイロ、プール、ブリッジの違いを整理します。
4. [動的なセッション](../../../../services/secrets.md#tenant-sessions)と[グループとカスタム属性](../../../../services/cognito.md#groups-attributes): テナントの文脈を認証から伝える方法を理解します。
5. [使用量プラン](../../../../services/api-gateway.md#usage-plans): 騒がしい隣人への対策を確認します。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| CloudFront Functions の実行時間 | 1 ミリ秒未満 | ビューワーのイベントだけ |
| Lambda@Edge の実行時間 | 最大 30 秒 | オリジンのイベントも使える |
| WebSocket の接続時間 | 2 時間（変更不可） | 再接続を実装 |
| WebSocket のアイドルタイムアウト | 10 分（変更不可） | 定期的にメッセージを送る |
| WebSocket のフレーム、メッセージ | 32 KB、128 KB（変更不可） | 大きなデータは S3 の URL で |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| ヘッダーの追加、URL の正規化、大量のリクエスト | CloudFront Functions |
| 外部の参照や SDK、キャッシュミスのときだけ | オリジンリクエストの Lambda@Edge |
| キャッシュする前にレスポンスを修正 | オリジンレスポンスの Lambda@Edge |
| 解約した利用者の配信を止める | `@connections` の `DELETE` で切断 |
| 別の処理から接続へ配信 | 接続 ID を DynamoDB に置き、イベントで配信 |
| 共有のテーブルで他のテナントに触れさせない | セッションタグと `dynamodb:LeadingKeys` |
| 共有の RDB で行を強制的に分離 | PostgreSQL の行レベルセキュリティ |
| 大口だけ分離とキーの失効 | ブリッジ。専用の DB と KMS キー |
| プランごとの呼び出しの制限 | 使用量プランと API キー |

## 引っかかりやすい点 {#traps}

- CloudFront Functions は外部へ通信できず、本文にもアクセスできません。オリジンのイベントでも動きません。
- WebSocket の認可は `$connect` だけで判定されます。接続後は再評価されません。
- Lambda の実行環境のメモリは共有されないので、接続 ID を置けません。
- テナント ID をリクエストのヘッダーから取ると、利用者が書き換えられます。検証済みの JWT から取ります。
- IAM データベース認証や RDS Proxy は、行の分離の手段ではありません。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [edge-tenancy 問1](../../exercises/edge-tenancy.md#q1) | 1.1.11 | 世界向けのニュースサイトは、毎秒数十万のリクエストを CloudFront で受けています。すべての… |
| [edge-tenancy 問2](../../exercises/edge-tenancy.md#q2) | 1.1.11 | 多国展開の EC サイトは、利用者ごとの契約先を DynamoDB で調べ、その結果に応じて Clo… |
| [edge-tenancy 問3](../../exercises/edge-tenancy.md#q3) | 1.1.11 | オリジンは古いシステムで、Cache-Control を正しく返しません。オリジンのコードは変更でき… |
| [edge-tenancy 問4](../../exercises/edge-tenancy.md#q4) | 1.1.12 | 共同編集のサービスは、API Gateway の WebSocket API を使っています。利用者… |
| [edge-tenancy 問5](../../exercises/edge-tenancy.md#q5) | 1.1.12 | 金融情報の配信で、WebSocket API を通じて最大 500 KB のレポートをクライアントへ… |
| [edge-tenancy 問6](../../exercises/edge-tenancy.md#q6) | 1.1.12 | 配送の状況をリアルタイムに通知します。$connect の Lambda は、接続 ID を実行環境… |
| [edge-tenancy 問7](../../exercises/edge-tenancy.md#q7) | 1.1.12 | WebSocket API で、$connect ルートに Lambda オーソライザーを設定してい… |
| [edge-tenancy 問8](../../exercises/edge-tenancy.md#q8) | 1.1.13 | B2B の SaaS は、Lambda、DynamoDB、S3 をテナントで共有しています。現在は … |
| [edge-tenancy 問9](../../exercises/edge-tenancy.md#q9) | 1.1.13 | SaaS の利用者には、多数の小規模なテナントと、規制を受ける数社の大口があります。大口はデータベー… |
| [edge-tenancy 問10](../../exercises/edge-tenancy.md#q10) | 1.1.13 | 共有の Aurora PostgreSQL の同じテーブルに、3,000 のテナントのデータがありま… |
| [edge-tenancy 問11](../../exercises/edge-tenancy.md#q11) | 1.1.13 | 共有の API で、一部のテナントが大量に呼び出し、他のテナントの応答が遅くなっています。契約プラン… |
| [edge-tenancy 問12](../../exercises/edge-tenancy.md#q12) | 1.1.13 | Cognito で認証する SaaS の API が、リクエストの X-Tenant-Id ヘッダー… |

<!-- questions:end -->

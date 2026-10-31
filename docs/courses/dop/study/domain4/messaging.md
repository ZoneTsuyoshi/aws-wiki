# 分野4: イベントの通知

イベントの経路の選択と、通知が届かない原因を問います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [イベントパターン](../../domain4.md#t4-3-event-patterns) | イベント駆動の非同期パターン |
| [EventBridge](../../domain4.md#t4-3-eventbridge) | EventBridge の通知 |

## 学習の順番 {#study-order}

1. [S3 イベント通知](../../../../services/messaging.md#s3-events): S3 イベント通知と EventBridge の違いを確認します。
2. [ルールとイベントパターン](../../../../services/messaging.md#eventbridge-rules): パターンの項目を覚えます。
3. [入力トランスフォーマー](../../../../services/messaging.md#input-transformer): 通知の文を整える方法を確認します。
4. [ターゲットの再試行と DLQ](../../../../services/messaging.md#target-retry-dlq): 失敗の受け皿を押さえます。
5. [アーカイブとリプレイ](../../../../services/messaging.md#archive-replay): 再処理の方法を確認します。

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| サイズなど内容で絞る | EventBridge のパターン |
| `FailedInvocations` が増える | ターゲットのアクセスポリシー |
| 届かなかったイベントを残す | 再試行ポリシーと DLQ |

## 引っかかりやすい点 {#traps}

- パターンを広くすると、すべての状態の変化が通知されます。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [messaging 問1](../../exercises/messaging.md#q1) | イベントパターン | S3 に PDF が届いたときの処理です。条件は、(1) オブジェクトのサイズが 1 MB より大き… |
| [messaging 問2](../../exercises/messaging.md#q2) | イベントパターン | EC2 の状態の変化イベントで Lambda を動かし、Lambda の中で SNS へ通知していま… |
| [messaging 問3](../../exercises/messaging.md#q3) | イベントパターン | 画像のアップロードの完了を、サムネイル、タグ付け、監査の 3 つのチームが非同期に処理します。S3 … |
| [messaging 問4](../../exercises/messaging.md#q4) | EventBridge | 組織には 40 本の CodePipeline があり、成功の通知が多すぎてチームが読まなくなりまし… |
| [messaging 問5](../../exercises/messaging.md#q5) | EventBridge | EventBridge のルールは一致しており、CloudWatch の Invocations も… |
| [messaging 問6](../../exercises/messaging.md#q6) | EventBridge | デプロイの結果をチャットの Lambda へ送るルールがあります。関数のリソースベースポリシーの更新… |

<!-- questions:end -->

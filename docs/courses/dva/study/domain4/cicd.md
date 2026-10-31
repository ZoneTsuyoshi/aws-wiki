# 分野4: CI/CD

デプロイが失敗したときに、どのログを読み、どう原因を絞るかが問われます。パイプラインの作り方やデプロイ戦略は[分野3](../domain3/cicd.md)で扱います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [4.1.4](../../domain4.md#skill-4-1-4) | デプロイの失敗の調査 |
| [4.2.3](../../domain4.md#skill-4-2-3) | デプロイの完了の通知 |

## 学習の順番 {#study-order}

1. [デプロイ失敗の診断](../../../../services/cicd.md#troubleshooting-deployments): 症状、確認先、原因の一覧を覚えます。この節が中心です。
2. [CodeBuild のログ](../../../../services/cicd.md#build-logs): 失敗したフェーズのログの探し方を確認します。
3. [CodeDeploy エージェント](../../../../services/cicd.md#codedeploy-agent): ログの置き場所と、エージェントの前提条件を覚えます。
4. [CodeDeploy のロールバック](../../../../services/cicd.md#codedeploy-rollback): アラームで止まることと、戻ることの違いを理解します。
5. [よくある失敗と対処](../../../../services/iac.md#common-failures): スタックイベントの読み方と、代表的なエラーを学びます。
6. [ロールバックの既定動作](../../../../services/iac.md#stack-rollback): 失敗後の状態と次の操作、調査用のオプションを確認します。
7. [デプロイの通知](../../../../services/observability.md#deployment-alerts): EventBridge のイベントパターンを押さえます。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| フックスクリプトの出力 | `/opt/codedeploy-agent/deployment-root/<グループID>/<デプロイID>/logs/scripts.log` | フックの失敗はここを読みます |
| エージェントのログ | `/var/log/aws/codedeploy-agent/codedeploy-agent.log` | エージェント自体の動作の記録です |
| エージェントの通信 | HTTPS（443 番）で外向き | EC2 とオンプレミスだけに必要です |
| ロールバックトリガー | 最大 5 個、監視時間は 0〜180 分 | 既定の監視時間は 0 です |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| EC2 へのデプロイで全イベントが Skipped になる | エージェントの起動、インスタンスプロファイル、外向き通信を確認します |
| `DownloadBundle` で失敗する | S3 の権限とリビジョンの場所を、エージェントログで確認します |
| `ApplicationStop` で失敗する | 前回の版のスクリプトが不正です。`scripts.log` を読みます |
| フックがタイムアウトする | スクリプトがバックグラウンド処理を待ち続けていないか、`scripts.log` で確認します |
| `AllowTraffic` で失敗し、ログに原因がない | ターゲットグループのヘルスチェック設定を確認します |
| CodeBuild の `docker` の実行で失敗する | 特権モードを有効にします |
| VPC 内のビルドで依存関係を取得できない | NAT ゲートウェイや VPC エンドポイントを確認します |
| Lambda のカナリアが戻された | CloudWatch アラーム、関数のログ、フック関数の `Failed` 報告を確認します |
| ECS のタスクが起動しない | サービスイベントとタスクの停止理由を読みます |
| スタックの作成の失敗を、リソースを残して調べたい | `--on-failure DO_NOTHING` で作成し、スタックイベントで最初の失敗を確認します |

## 引っかかりやすい点 {#traps}

- **スタックイベントの最後のエラーを読んでしまう:** 後続の失敗は連鎖であることが多いので、最初の `CREATE_FAILED` か `UPDATE_FAILED` を読みます。
- **アラームで止まったのに元に戻らない:** 発火で `Stopped` になるだけです。`DEPLOYMENT_STOP_ON_ALARM` の自動ロールバックを別に有効にします。
- **Lambda や ECS で `scripts.log` を探す:** CodeDeploy のこの種のログは EC2 とオンプレミスだけです。関数やタスク自体のログとデプロイのイベントを確認します。
- **`ROLLBACK_COMPLETE` のスタックを更新しようとする:** 初回作成の失敗では更新できません。削除して作り直します。
- **`UPDATE_ROLLBACK_FAILED` から抜けられない:** 原因を直して `continue-update-rollback` を実行します。難しければ `--resources-to-skip` を指定します。
- **ロールバックトリガーが `INSUFFICIENT_DATA` で動かない:** 戻すには、アラームで欠落データを `breaching` として扱います。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [cicd 問7](../../exercises/cicd.md#q7) | 4.1.4 | VPC の RDS に接続する統合テストのために vpcConfig を設定したところ、pip in… |
| [cicd 問10](../../exercises/cicd.md#q10) | 4.1.4 | CodeDeploy の新しいリビジョンでスクリプトを直したのに、ApplicationStop で… |

<!-- questions:end -->

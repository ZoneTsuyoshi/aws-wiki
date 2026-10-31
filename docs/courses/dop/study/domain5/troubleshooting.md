# 分野5: 障害の調査

手がかりをたどる順番と、最初に見る場所を問います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [メトリクスとログ](../../domain5.md#t5-3-observability) | メトリクスとログのサービス |
| [サービスの状態](../../domain5.md#t5-3-service-health) | サービスの状態を見るサービス |
| [根本原因](../../domain5.md#t5-3-root-cause) | 根本原因の分析 |
| [失敗したデプロイ](../../domain5.md#t5-3-failed-deployments) | 失敗したデプロイの分析 |
| [プロセスの障害](../../domain5.md#t5-3-failed-processes) | 失敗したプロセスのインシデントの分析 |

## 学習の順番 {#study-order}

1. [メトリクス、ログ、トレースの読み解き](../../../../services/observability.md#interpret-signals): メトリクス、ログ、トレースの役割を確認します。
2. [AWS Health Dashboard](../../../../services/cloud-foundations.md#health): AWS 側の障害の確認を押さえます。
3. [OpsCenter](../../../../services/operations.md#opscenter): 運用の課題の集約を確認します。
4. [デバッグとエラー診断](../../../../services/observability.md#debugging): 調査の進め方を確認します。
5. [スタックのロールバックと失敗](../../../../services/iac.md#stack-failures): 最初の失敗の読み方を確認します。
6. [デプロイ失敗の診断](../../../../services/cicd.md#troubleshooting-deployments): サービスごとの最初の確認先を覚えます。
7. [スケーリングの失敗の調査](../../../../services/operations.md#asg-troubleshooting): 起動の失敗の原因を確認します。

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| いつから、どれくらい | CloudWatch メトリクス |
| どの区間で | X-Ray |
| 誰が変更したか | CloudTrail |
| AWS 側の障害か | AWS Health |
| `UPDATE_ROLLBACK_FAILED` | `continue-update-rollback` |
| デプロイの後の異常で自動で戻す | Synthetics のアラームと CodeDeploy |

## 引っかかりやすい点 {#traps}

- スタックイベントは最初の失敗を読みます。後の失敗は結果であることが多いです。
- Incident Manager、DevOps Guru、CloudTrail Lake は新規受付を終了しました。
- 暗号化された EBS で起動できないときは、サービスリンクロールのキーの権限を確認します。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [troubleshooting 問4](../../exercises/troubleshooting.md#q4) | メトリクスとログ | 午後から API が遅くなりました。次の問いに答える手段を選びます。(1) いつからどれくらい悪いか… |
| [troubleshooting 問5](../../exercises/troubleshooting.md#q5) | メトリクスとログ | マイクロサービスの呼び出しで、エラーの発生元が分かりません。サービスマップで見ると、サービス A か… |
| [troubleshooting 問6](../../exercises/troubleshooting.md#q6) | メトリクスとログ | Lambda の呼び出しの一部が遅いことが分かりました。Duration の平均は正常ですが、p99… |
| [troubleshooting 問7](../../exercises/troubleshooting.md#q7) | サービスの状態 | 本番のアプリのエラーが 10 時から増えました。当日の変更はありません。AWS 側の障害の影響かを最… |
| [troubleshooting 問8](../../exercises/troubleshooting.md#q8) | サービスの状態 | 運用チームが、アラームと Config の変更、Trusted Advisor の警告を別々の画面で… |
| [troubleshooting 問9](../../exercises/troubleshooting.md#q9) | サービスの状態 | 次の説明のうち、正しいものを選んでください。（2つ選択） |
| [troubleshooting 問10](../../exercises/troubleshooting.md#q10) | 根本原因 | 14 時から本番の API で 5xx が増えました。午前中にデプロイが 2 回あり、同じ時間帯に別… |
| [troubleshooting 問11](../../exercises/troubleshooting.md#q11) | 根本原因 | 14 時 02 分に HTTPCode_Target_5XX_Count が増えました。CodeDe… |
| [troubleshooting 問12](../../exercises/troubleshooting.md#q12) | 根本原因 | 夜間のバッチで RDS の接続エラーが毎週木曜に起きます。都度の再実行で直っており、担当者は再実行の… |
| [troubleshooting 問13](../../exercises/troubleshooting.md#q13) | 失敗したデプロイ | CloudFormation の更新が失敗し、多数のイベントが UPDATE_FAILED と Re… |
| [troubleshooting 問14](../../exercises/troubleshooting.md#q14) | 失敗したデプロイ | 次の失敗の最初の確認先を選びます。(1) CodeBuild が BUILD フェーズで失敗した。(… |
| [troubleshooting 問15](../../exercises/troubleshooting.md#q15) | 失敗したデプロイ | デプロイは正常に完了しますが、ログインの画面が壊れていることに利用者の報告で気づきました。デプロイの… |
| [troubleshooting 問16](../../exercises/troubleshooting.md#q16) | プロセスの障害 | Auto Scaling グループで新しいインスタンスが起動しません。describe-scalin… |

<!-- questions:end -->

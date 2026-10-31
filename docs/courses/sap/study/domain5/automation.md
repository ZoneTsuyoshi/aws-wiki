# 分野5: 運用の自動化

自動で直す仕組みと、それが暴走しないための制約を問います。スケーリングとヘルスチェックの設定値も判断の材料になります。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [5.4.1](../../domain5.md#skill-5-4-1) | ヘルス監視、容量計画、運用の対応 |
| [5.4.2](../../domain5.md#skill-5-4-2) | 安全制約を備えた修復 |
| [5.4.3](../../domain5.md#skill-5-4-3) | メトリクスとスケジュールのスケーリング |
| [5.4.4](../../domain5.md#skill-5-4-4) | ヘルスチェックと置き換えによる自動復旧 |
| [5.4.5](../../domain5.md#skill-5-4-5) | 自動のランブックとインシデント対応 |

## 学習の順番 {#study-order}

1. [クォータの上限に近づいたとき](../../../../services/observability.md#quota-alerts)と [AWS Health イベントの自動化](../../../../services/operations.md#health-events): 通知の作り方と、組織での見方を確認します。
2. [レート制御](../../../../services/operations.md#automation-rate-control)、[予約済み同時実行](../../../../services/lambda.md#reserved-concurrency)、[サーキットブレーカー](../../../../services/sdk-resilience.md#circuit-breaker)、[指数バックオフとジッター](../../../../services/sdk-resilience.md#backoff-jitter): 障害を広げない制約を整理します。
3. [EC2 Auto Scaling](../../../../services/ec2-beanstalk.md#auto-scaling)、[予測スケーリング](../../../../services/operations.md#predictive-scaling)、[ウォームプール](../../../../services/operations.md#warm-pools): ポリシーの選び方を押さえます。
4. [ヘルスチェック](../../../../services/ec2-beanstalk.md#asg-health-checks)、[プローブ](../../../../services/containers.md#probes)、[ストリームのエラー処理](../../../../services/lambda.md#esm-stream-errors): 検出と置き換えの設定を確認します。
5. [Automation](../../../../services/operations.md#automation)、[複数アカウントの実行](../../../../services/operations.md#automation-multi-account)、[State Manager と Maintenance Windows の違い](../../../../services/operations.md#state-vs-maintenance)、[OpsCenter](../../../../services/operations.md#opscenter): ランブックの運用を理解します。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| `MaxErrors` が 3 | 4 件目で止まる | 実行中の分は続くので超えることがある |
| `MaxErrors` が 0 | 最初のエラーで止まる | 厳密には同時実行も 1 にする |
| ヘルスチェックの猶予期間 | コンソールは既定 300 秒、CLI は既定 0 秒 | 起動の時間に合わせる |
| 予測スケーリングの履歴 | 最低 24 時間、2 週間で効果が高い | 周期のない負荷には向かない |
| Lambda の非同期の再試行 | 既定で 2 回 | 送信先や DLQ を設定 |
| `aws:approve` のタイムアウト | 既定 7 日、最大 30 日 | 複数アカウントの実行では使えない |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| DR で起動がクォータで失敗する | DR のリージョンの値を事前に引き上げ |
| 上限に追随するアラーム | `AWS/Usage` と `SERVICE_QUOTA()` |
| 全アカウントの Health を 1 か所で | 組織ビューと委任管理者 |
| 全台を壊さず修復する | 同時実行とエラーしきい値 |
| 顧客の障害の範囲を限定する | セルベースのアーキテクチャ |
| 他の関数に枠を奪われない | 予約済み同時実行 |
| 再試行の集中を防ぐ | 指数バックオフとジッター |
| SQS の処理のスケーリング | インスタンスあたりのバックログでターゲット追跡 |
| 毎朝の周期と遅い初期化 | 予測スケーリング |
| 1 回限りの日時が分かる負荷 | スケジュールとターゲット追跡 |
| 不規則な急増と遅い初期化 | ウォームプール |
| アプリが落ちても置き換わらない | ELB のヘルスチェックを有効に |
| 状態を保ち、準拠を報告する | State Manager |
| 決まった時間帯に順に作業する | Maintenance Windows |

## 引っかかりやすい点 {#traps}

- 深いヘルスチェックは、依存先の障害で全台を置き換えることがあります。
- ライブネスプローブに依存先を入れません。依存先はレディネスで確認します。
- ウォームプールに入る前の停止は、ユーザーデータの完了を待ちません。ライフサイクルフックを使います。
- カスタムランブックは対象のアカウントすべてに共有します。
- EventBridge のルールで受ける Health のイベントは、自分のアカウントの分だけです。
- 修復が別のイベントを発生させて、ループにならないようにします。
- DevOps Guru は新規受付を終了しました。新しい構成は CloudWatch と AWS DevOps Agent で考えます。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [automation 問1](../../exercises/automation.md#q1) | 5.4.1 | ある企業は、主系を東京、DR を大阪としたパイロットライトの構成です。DR の訓練でスケールアウトを… |
| [automation 問2](../../exercises/automation.md#q2) | 5.4.1 | Lambda の同時実行や EC2 の vCPU の使用率が、上限に近づいた時点で運用チームに通知さ… |
| [automation 問3](../../exercises/automation.md#q3) | 5.4.1 | 組織には 100 のアカウントがあります。セキュリティのアカウントに EventBridge のルー… |
| [automation 問4](../../exercises/automation.md#q4) | 5.4.1 | EC2 のインスタンスのリタイアの予定が、不規則に通知されます。担当者が気づくのが遅れ、予定の時刻に… |
| [automation 問5](../../exercises/automation.md#q5) | 5.4.2 | Automation のランブックで 1,000 台のインスタンスの設定を修復します。MaxConc… |
| [automation 問6](../../exercises/automation.md#q6) | 5.4.2 | 共有の SaaS の API で、ある大口顧客の異常なリクエストが全顧客の障害につながりました。アー… |
| [automation 問7](../../exercises/automation.md#q7) | 5.4.2 | 同じアカウントに、決済の Lambda と夜間のバッチの Lambda があります。夜間のバッチが急… |
| [automation 問8](../../exercises/automation.md#q8) | 5.4.2 | あるマイクロサービスが依存先の障害で失敗すると、全インスタンスが同じ間隔ですぐに再試行し、回復しかけ… |
| [automation 問9](../../exercises/automation.md#q9) | 5.4.2 | Config ルールの自動修復で、許可しないセキュリティグループのルールを削除しています。あるチーム… |
| [automation 問10](../../exercises/automation.md#q10) | 5.4.3 | SQS のキューを処理する EC2 の Auto Scaling グループがあります。CPU を基準… |
| [automation 問11](../../exercises/automation.md#q11) | 5.4.3 | 社内の業務アプリは、毎週の平日の朝に急増し、夜と週末は少なくなります。インスタンスの初期化に 8 分… |
| [automation 問12](../../exercises/automation.md#q12) | 5.4.3 | EBS をルートとするアプリのインスタンスは、起動スクリプトの完了まで 10 分かかります。負荷の急… |
| [automation 問13](../../exercises/automation.md#q13) | 5.4.3 | 来月の特定の日に、テレビ番組と連動した初めてのキャンペーンを行います。放送の開始時刻に負荷が 10 … |
| [automation 問14](../../exercises/automation.md#q14) | 5.4.4 | ALB の裏の Auto Scaling グループは、CLI で作成されました。アプリが 500 を… |
| [automation 問15](../../exercises/automation.md#q15) | 5.4.4 | Web 層のターゲットグループのヘルスチェックは /health を呼び、このパスは DB への接続… |
| [automation 問16](../../exercises/automation.md#q16) | 5.4.4 | EKS のアプリには、DB への接続を確認するライブネスプローブがあります。DB のフェイルオーバー… |
| [automation 問17](../../exercises/automation.md#q17) | 5.4.4 | Kinesis Data Streams を Lambda で処理しています。処理できないレコードが… |
| [automation 問18](../../exercises/automation.md#q18) | 5.4.5 | 運用チームには 2 つの作業があります。(1) Auto Scaling で増える新しいインスタンス… |
| [automation 問19](../../exercises/automation.md#q19) | 5.4.5 | 影響の大きい修復のランブックを、組織の 40 のアカウントへ Automation で実行します。実… |
| [automation 問20](../../exercises/automation.md#q20) | 5.4.5 | 委任管理者のアカウントから、OU を対象に自作のランブックを実行しました。AWS-SystemsMa… |
| [automation 問21](../../exercises/automation.md#q21) | 5.4.5 | 新しい事業のアカウントで、インシデント対応の流れを新規に整えます。検出から記録、ランブックの実行、調… |

<!-- questions:end -->

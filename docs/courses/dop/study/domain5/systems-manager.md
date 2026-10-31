# 分野5: フリートと構成の変更

動いているものを安全に変える方法と、イベントで変える方法を問います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [フリート管理](../../domain5.md#t5-2-fleet) | フリート管理のサービス |
| [構成変更の適用](../../domain5.md#t5-2-apply-changes) | システムへの構成変更の適用 |
| [インフラの変更](../../domain5.md#t5-2-respond) | イベントに応じたインフラの変更 |

## 学習の順番 {#study-order}

1. [ライフサイクルフック](../../../../services/operations.md#lifecycle-hooks): 待機の使い方を確認します。
2. [インスタンスの更新](../../../../services/operations.md#instance-refresh): 割合とロールバックを押さえます。
3. [Run Command](../../../../services/operations.md#run-command): 対象と安全策を確認します。
4. [レート制御](../../../../services/operations.md#automation-rate-control): レート制御を理解します。
5. [EventBridge による修復パターン](../../../../services/operations.md#eventbridge-remediation): ターゲットの指定を確認します。
6. [スポットの中断への対応](../../../../services/operations.md#spot-interruptions): 中断の警告を覚えます。

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 終了の前にログを退避する | 終了のライフサイクルフック |
| 最初は小さく適用する | `MaxConcurrency` と `MaxErrors` |
| 規則の追加をすぐに消す | EventBridge と Automation |
| 多工程で人の判断も入る | Step Functions |

## 引っかかりやすい点 {#traps}

- Lambda を書かなくて済むなら、ターゲットに Automation を直接指定します。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [systems-manager 問19](../../exercises/systems-manager.md#q19) | フリート管理 | Auto Scaling のインスタンスが終了するときに、ログを S3 へ退避します。処理は最大 5… |
| [systems-manager 問20](../../exercises/systems-manager.md#q20) | フリート管理 | 300 台のマネージドノードを運用します。担当者が、SSH なしでコンソールからプロセスとファイルを… |
| [systems-manager 問21](../../exercises/systems-manager.md#q21) | フリート管理 | ゴールデン AMI を更新した後、稼働中のインスタンスを順に入れ替えます。全体の 90% は常に動か… |
| [systems-manager 問22](../../exercises/systems-manager.md#q22) | 構成変更の適用 | 1,000 台へ OS の設定変更を行います。最初は小さく適用し、失敗が増えたら自動で止めます。対象… |
| [systems-manager 問23](../../exercises/systems-manager.md#q23) | 構成変更の適用 | 本番のレート制限の値を、アプリの再デプロイなしで 20% ずつ 10 分ごとに広げ、アラームで戻しま… |
| [systems-manager 問24](../../exercises/systems-manager.md#q24) | 構成変更の適用 | 本番の VPC のルートテーブルを変更します。他の担当者の確認の後に実行し、影響を事前に確認します。… |
| [systems-manager 問25](../../exercises/systems-manager.md#q25) | インフラの変更 | 本番の VPC で SSH を 0.0.0.0/0 に開ける規則が追加されたら、数分以内に自動で消し… |
| [systems-manager 問26](../../exercises/systems-manager.md#q26) | インフラの変更 | スポットインスタンスで動くバッチの処理があります。中断の 2 分前の警告を受けたら、途中の結果を S… |
| [systems-manager 問27](../../exercises/systems-manager.md#q27) | インフラの変更 | GuardDuty が EC2 の検出結果を出したら、(1) インスタンスを隔離用のセキュリティグル… |

<!-- questions:end -->

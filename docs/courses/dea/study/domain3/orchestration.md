# 分野3: MWAA、Step Functions、EventBridge の運用

マネージドワークフローの設定とトラブルシューティング、イベントとスケジューラーの管理を問います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [3.1.1](../../domain3.md#skill-3-1-1) | パイプラインの連結（MWAA、Step Functions） |
| [3.1.2](../../domain3.md#skill-3-1-2) | マネージドワークフローのトラブルシューティング |
| [3.1.9](../../domain3.md#skill-3-1-9) | イベントとスケジューラーの管理 |

## 学習の順番 {#study-order}

1. [MWAA](../../../../services/data-engineering.md#mwaa): ファイルの置き場と環境クラスを覚えます。
2. [再実行とログ](../../../../services/step-functions.md#redrive-logging): Standard と Express の違いを確認します。
3. [ターゲットの再試行と DLQ](../../../../services/messaging.md#target-retry-dlq): 配信失敗の扱いを理解します。
4. [アーカイブとリプレイ](../../../../services/messaging.md#archive-replay): 順序の注意を確認します。
5. [Pipes](../../../../services/messaging.md#eventbridge-pipes): ルールとの違いを押さえます。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| `mw1.micro` | DAG 25、同時タスク 3 | 自動スケーリングなし |
| `mw1.small` | DAG 50、同時タスク 5 | 小規模の本番 |
| `mw1.medium` | DAG 250、同時タスク 10 |  |
| `mw1.large` | DAG 1,000、同時タスク 20 |  |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| PyPI に届かない VPC の依存 | `plugins.zip` に同梱 |
| タスクがキューにたまる | 環境クラスと最大ワーカー数 |
| Express の失敗を調べる | CloudWatch Logs |
| 失敗したイベントを残す | ターゲットの DLQ |
| 1 回のみの予約 | Scheduler の `at()` |

## 引っかかりやすい点 {#traps}

- `GetExecutionHistory` は Standard の機能です。
- リプレイの順序は保証されません。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [orchestration 問20](../../exercises/orchestration.md#q20) | 3.1.1 | MWAA で DAG を更新します。ファイルを置く場所はどこですか。 |
| [orchestration 問21](../../exercises/orchestration.md#q21) | 3.1.1 | MWAA の環境で、DAG 40 個を動かします。同時タスクの既定は 5 個で足ります。費用を抑えた… |
| [orchestration 問22](../../exercises/orchestration.md#q22) | 3.1.1 | パイプラインの定義方法の説明として正しいものはどれですか。（2つ選択） |
| [orchestration 問23](../../exercises/orchestration.md#q23) | 3.1.2 | インターネットへの経路のない VPC の MWAA で、requirements.txt のインスト… |
| [orchestration 問24](../../exercises/orchestration.md#q24) | 3.1.2 | MWAA の DAG でタスクがキューに長くたまり、スケジュールが遅れます。CPU の使用率は高い状… |
| [orchestration 問25](../../exercises/orchestration.md#q25) | 3.1.2 | Express の状態機械が失敗しますが、コンソールの実行履歴から原因を追えません。どうしますか。 |
| [orchestration 問26](../../exercises/orchestration.md#q26) | 3.1.9 | EventBridge のルールのターゲットの Lambda に権限がなく、配信が失敗しています。失… |
| [orchestration 問27](../../exercises/orchestration.md#q27) | 3.1.9 | 下流のバグで 2 日前からのイベントを取りこぼしました。イベントを再送して処理し直します。事前に設定… |
| [orchestration 問28](../../exercises/orchestration.md#q28) | 3.1.9 | 要件と機能の組み合わせとして正しいものはどれですか。 |

<!-- questions:end -->

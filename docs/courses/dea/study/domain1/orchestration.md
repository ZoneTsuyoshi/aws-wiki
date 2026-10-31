# 分野1: オーケストレーションとイベント

スケジューラー、イベントトリガー、ワークフローの種類、失敗からの回復、通知を問います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [1.1.5](../../domain1.md#skill-1-1-5) | スケジューラーの設定 |
| [1.1.6](../../domain1.md#skill-1-1-6) | イベントトリガーの設定 |
| [1.3.1](../../domain1.md#skill-1-3-1) | オーケストレーションサービスの利用 |
| [1.3.2](../../domain1.md#skill-1-3-2) | 性能、可用性、耐障害性のあるパイプライン |
| [1.3.3](../../domain1.md#skill-1-3-3) | サーバーレスワークフローの実装と保守 |
| [1.3.4](../../domain1.md#skill-1-3-4) | 通知サービスによるアラート |

## 学習の順番 {#study-order}

1. [オーケストレーションの比較](../../../../services/data-engineering.md#orchestration): Glue、Step Functions、MWAA の選び方を覚えます。
2. [スケジュール](../../../../services/messaging.md#eventbridge-schedule): cron の項目数の違いを確認します。
3. [ワークフローとトリガー](../../../../services/data-engineering.md#glue-workflows): 条件トリガーとバッチを理解します。
4. [サービス統合パターン](../../../../services/step-functions.md#integration-patterns): `.sync` の意味を押さえます。
5. [Standard と Express](../../../../services/step-functions.md#standard-express): 時間と保証の違いを覚えます。
6. [エラー処理](../../../../services/step-functions.md#error-handling): `Retry` と `Catch` を確認します。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| Standard の最大実行時間 | 1 年 | `.sync` を使える |
| Express の最大実行時間 | 5 分 | `.sync` を使えない |
| redrive の期限 | 完了から 14 日 | Standard のみ |
| Glue のバッチのウィンドウ | 件数だけなら 15 分 | 最大 900 秒 |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| Glue だけで完結する | Glue ワークフロー |
| 既存の Airflow、AWS の外の処理 | MWAA |
| AWS で完結する混在処理 | Step Functions |
| ファイルの到着で複数のターゲットへ振り分ける | EventBridge |
| ジョブの完了を待つ | `.sync` |
| ジョブの失敗をメールで通知する | EventBridge のルールと SNS |

## 引っかかりやすい点 {#traps}

- 入力と同じプレフィックスに書くとイベントがループします。
- EventBridge の cron は 6 項目、Airflow の cron は通常 5 項目です。
- EMR のプライマリを 3 台にしても、クラスターは 1 つの AZ です。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [orchestration 問1](../../exercises/orchestration.md#q1) | 1.1.5 | 毎朝 9 時（東京時間）に Lambda を起動します。新規の構築です。AWS が勧めている方法と書… |
| [orchestration 問2](../../exercises/orchestration.md#q2) | 1.1.5 | Airflow の DAG を毎日 2 時に実行します。DAG の schedule の書き方として… |
| [orchestration 問3](../../exercises/orchestration.md#q3) | 1.1.5 | 毎晩のクローラーの後に Glue ジョブを実行します。Glue の中だけで完結させ、クローラーの完了… |
| [orchestration 問4](../../exercises/orchestration.md#q4) | 1.1.6 | Lambda が S3 の raw/ に届いたファイルを変換し、同じ raw/ に結果を書いたところ… |
| [orchestration 問5](../../exercises/orchestration.md#q5) | 1.1.6 | S3 にファイルが届くと、Step Functions の起動、別の関数の呼び出し、SNS の通知の… |
| [orchestration 問6](../../exercises/orchestration.md#q6) | 1.1.6 | 小さなファイルが連続して届きます。Glue ワークフローを、100 個たまるか 10 分たつかの先に… |
| [orchestration 問7](../../exercises/orchestration.md#q7) | 1.3.1 | パイプラインは Glue、Lambda、Redshift の Data API、SNS で構成されま… |
| [orchestration 問8](../../exercises/orchestration.md#q8) | 1.3.1 | 既存の Airflow の DAG が 200 個あり、オンプレミスの処理や他社クラウドのデータも扱… |
| [orchestration 問9](../../exercises/orchestration.md#q9) | 1.3.1 | Step Functions で Glue ジョブの後に COPY を実行します。Glue の出力が… |
| [orchestration 問10](../../exercises/orchestration.md#q10) | 1.3.1 | 次の要件のうち、Glue ワークフローで十分なものはどれですか。 |
| [orchestration 問11](../../exercises/orchestration.md#q11) | 1.3.2 | Glue のタスクが一時的な失敗で止まることがあります。3 回まで間隔を空けて再試行し、それでも失敗… |
| [orchestration 問12](../../exercises/orchestration.md#q12) | 1.3.2 | EMR on EC2 の長期クラスターの可用性を高めます。正しい説明はどれですか。（2つ選択） |
| [orchestration 問13](../../exercises/orchestration.md#q13) | 1.3.2 | Step Functions が失敗した Glue のロードを再試行すると、S3 のテーブルに同じ行… |
| [orchestration 問14](../../exercises/orchestration.md#q14) | 1.3.3 | Glue ジョブの完了を待ち、数時間かかることもある ETL です。人の承認の手順も入ります。どのワ… |
| [orchestration 問15](../../exercises/orchestration.md#q15) | 1.3.3 | S3 の 1 万個のファイルをそれぞれ小さな Lambda で並列に処理します。Step Funct… |
| [orchestration 問16](../../exercises/orchestration.md#q16) | 1.3.3 | Standard の実行が 10 段目で失敗しました。原因を直したので、9 段目までをやり直さず再開… |
| [orchestration 問17](../../exercises/orchestration.md#q17) | 1.3.4 | Glue ジョブが失敗したら、担当者にメールを送ります。コードは書きません。どの構成ですか。 |
| [orchestration 問18](../../exercises/orchestration.md#q18) | 1.3.4 | ジョブ失敗の通知を、運用担当のメールと自動修復の処理の 2 つへ送ります。修復の処理は止まっていても… |
| [orchestration 問19](../../exercises/orchestration.md#q19) | 1.3.4 | Athena のワークグループで、1 日のスキャン量が 10 TB を超えたら管理者へ通知します。ク… |

<!-- questions:end -->

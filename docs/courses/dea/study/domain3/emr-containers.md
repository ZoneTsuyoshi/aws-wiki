# 分野3: プロビジョンドとサーバーレス、Glue と EMR の保守

プロビジョンドとサーバーレスのトレードオフと、Glue と EMR のトラブルシューティングを問います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [3.2.5](../../domain3.md#skill-3-2-5) | プロビジョンドとサーバーレスのトレードオフ |
| [3.3.6](../../domain3.md#skill-3-3-6) | パイプラインのトラブルシューティングと保守 |

## 学習の順番 {#study-order}

1. [Redshift Serverless](../../../../services/data-engineering.md#redshift-serverless): 最大 RPU の設定を確認します。
2. [EMR Serverless](../../../../services/data-engineering.md#emr-serverless): EMR on EC2 との違いを理解します。
3. [ワークフローとトリガー](../../../../services/data-engineering.md#glue-workflows): 同時実行の上限の動作を確認します。
4. [クラスターのノード](../../../../services/data-engineering.md#emr-nodes): Application Master の配置を押さえます。
5. [スケーリングと終了](../../../../services/data-engineering.md#emr-scaling): 上限と自動終了を確認します。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| Glue のタイムアウト | 5.0 以降は既定 480 分 | タイムアウトは再実行されない |
| Glue のリトライ | 0〜10 | タイムアウトには効かない |
| Serverless の課金 | 秒単位、最小 60 秒 | Redshift の場合 |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 断続的で読めない負荷 | サーバーレス。上限も設定する |
| 常に負荷があり予約で安くする | プロビジョンド |
| Spot の中断でジョブごと失敗する | Application Master を `CORE` か `ON_DEMAND` に限定 |
| 終了後のクラスターを調べる | S3 のログ |
| EventBridge の起動が一部始まらない | ワークフローの同時実行の上限 |

## 引っかかりやすい点 {#traps}

- MSK Serverless は IAM 認証のみです。
- Glue はワークフローの上限を超えたイベントを再試行しません。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [emr-containers 問10](../../exercises/emr-containers.md#q10) | 3.2.5 | 分析は平日の朝にだけ集中し、負荷は読めません。夜間と週末の費用は減らします。Redshift で適切… |
| [emr-containers 問11](../../exercises/emr-containers.md#q11) | 3.2.5 | プロビジョンドとサーバーレスの判断で、正しいものはどれですか。 |
| [emr-containers 問12](../../exercises/emr-containers.md#q12) | 3.2.5 | 次の要件のうち、プロビジョンドよりサーバーレスやオンデマンドを選ぶ根拠になるものはどれですか。（2つ… |
| [emr-containers 問13](../../exercises/emr-containers.md#q13) | 3.3.6 | Glue 5.0 のジョブが、データ増の後に毎回 8 時間で止まります。エラーはタイムアウトです。適… |
| [emr-containers 問14](../../exercises/emr-containers.md#q14) | 3.3.6 | EMR で Spot のタスクノードが中断されると、ジョブごと失敗することがあります。タスクが再試行… |
| [emr-containers 問15](../../exercises/emr-containers.md#q15) | 3.3.6 | EMR のログを調べたいのに、クラスターが終了して SSH できません。今後に備える設定と、ジョブが… |
| [emr-containers 問16](../../exercises/emr-containers.md#q16) | 3.3.6 | EventBridge で起動する Glue ワークフローで、イベントが集中した時に一部の実行が始ま… |

<!-- questions:end -->

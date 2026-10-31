# 分野4: オブザーバビリティ

CloudWatch、X-Ray、CloudTrail で原因を調べ、ログ、メトリクス、トレース、通知を実装する力が問われます。分野4の土台になるページで、各サービスに固有の症状は [Lambda](lambda.md) や [API Gateway](api-gateway.md) などのページで扱います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [4.1.1](../../domain4.md#skill-4-1-1) | コードとサービス連携のデバッグ |
| [4.1.2](../../domain4.md#skill-4-1-2) | メトリクス、ログ、トレースの読み取り |
| [4.1.3](../../domain4.md#skill-4-1-3) | ログのクエリ |
| [4.2.1](../../domain4.md#skill-4-2-1) | ログ戦略 |
| [4.2.2](../../domain4.md#skill-4-2-2) | カスタムメトリクス |
| [4.2.3](../../domain4.md#skill-4-2-3) | 通知 |
| [4.2.4](../../domain4.md#skill-4-2-4) | トレース |
| [4.2.5](../../domain4.md#skill-4-2-5) | ワークロードの状態監視 |
| [4.3.5](../../domain4.md#skill-4-3-5) | ボトルネックの検出 |

## 学習の順番 {#study-order}

1. [メトリクス、ログ、トレースの読み解き](../../../../services/observability.md#interpret-signals): どの順に見ると、何が分かるかをつかみます。
2. [代表的なエラーコード](../../../../services/observability.md#error-codes)と[サービス統合の問題](../../../../services/observability.md#debug-integration): 症状から確認先を選べるようにします。
3. [Logs Insights](../../../../services/observability.md#logs-insights): `filter`、`stats`、`parse` のクエリを読めるようにします。
4. [ロギング戦略](../../../../services/observability.md#logging-strategy)と[構造化ログ](../../../../services/observability.md#structured-events): JSON で出す理由と、入れる項目を確認します。
5. [PutMetricData](../../../../services/observability.md#put-metric-data)、[EMF](../../../../services/observability.md#emf)、[統計](../../../../services/observability.md#statistics): 送り方の使い分けと、`p99` の意味を押さえます。
6. [アラームの評価](../../../../services/observability.md#alarm-evaluation)、[欠落データ](../../../../services/observability.md#treat-missing-data)、[通知アラート](../../../../services/observability.md#alerts): M out of N、`TreatMissingData`、クォータとデプロイの通知を学びます。
7. [アノテーションとメタデータ](../../../../services/observability.md#annotations-metadata)、[サンプリング](../../../../services/observability.md#xray-sampling)、[OpenTelemetry](../../../../services/observability.md#xray-opentelemetry): 検索できる値と、現在の推奨を確認します。
8. [ヘルスチェックとプローブ](../../../../services/observability.md#health-checks)と[代表的なメトリクス](../../../../services/observability.md#bottleneck-metrics): 正常性の確認方法と、遅さの原因を示すメトリクスを結びつけます。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| `StorageResolution` | 既定 60、高解像度は 1 | 1 秒単位のカスタムメトリクスには 1 を指定します |
| データの利用期間 | 60 秒未満は 3 時間、60 秒は 15 日、300 秒は 63 日、3,600 秒は 455 日 | 古い障害は細かい粒度で調べられません |
| `PutMetricData` | 1 MB、1,000 メトリクス、1 メトリクス 150 値 | `Values` と `Counts` でまとめて送れます |
| EMF | 1 イベント 1 MB、メトリクス定義は合計 100 個 | 超えるとそのイベントからは何も抽出されません |
| `TreatMissingData` | 既定は `missing` | エラー時だけ出るメトリクスには合いません |
| ログの保持期間 | 既定は無期限 | 費用を抑えるには保持期間を設定します |
| Logs Insights | 60 分、同時 100 クエリ、50 ロググループ | 料金はスキャン量で決まるので、時間範囲を絞ります |
| X-Ray のサンプリング | 毎秒 1 件と、以降の 5% | Lambda ではこの率を変更できません |
| アノテーション | トレースあたり 50 個がインデックス対象 | 値は文字列、数値、真偽値です |
| X-Ray デーモン | UDP 2000 | Lambda では導入が不要です。SDK とデーモンは 2026 年 2 月 25 日からメンテナンスモードです |
| CloudTrail | イベント履歴 90 日、配信は平均 約 5 分 | データイベントは既定で記録されません |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| Lambda から遅延を増やさずにメトリクスを大量に出したい | EMF を使います。ログの 1 メッセージ全体を JSON にして、標準出力へ書きます |
| コードを変えずに、既存ログの特定のパターンでアラームを鳴らしたい | メトリクスフィルターを作ります。効くのは作成後のログだけです |
| エラー時だけ出るメトリクスのアラームが `INSUFFICIENT_DATA` のまま | `TreatMissingData=notBreaching` にします |
| 単発のスパイクでは鳴らさず、断続的な障害では鳴らしたい | `Period=60`、`EvaluationPeriods=5`、`DatapointsToAlarm=3` のように M out of N にします |
| ユーザーや顧客の値でトレースを検索したい | アノテーションに記録し、`annotation.tier = "gold"` のように検索します |
| 問題のあるパスだけ一時的に全件トレースしたい | 入口のサービスに `Priority=1`、`ReservoirSize=1`、`FixedRate=1`、`URLPath` を指定したルールを追加します。コードの修正は不要です |
| クォータの 80% で通知したい | `m1 / SERVICE_QUOTA(m1) * 100` でアラームを作り、SNS へ通知します |
| デプロイの成功と失敗を通知したい | EventBridge ルールで `aws.codedeploy` の `SUCCESS` と `FAILURE` を受け、SNS へ送ります |
| 遅い API の原因を絞り込みたい | メトリクスの `p99` で時期を特定し、トレースで遅い区間を見つけ、ログや Insights で原因を確認します |
| 新しくトレースの計装を始める | X-Ray SDK ではなく、OpenTelemetry（ADOT）を使います |

## 引っかかりやすい点 {#traps}

- **`p99` が取得できない:** `StatisticValues`（統計セット）で送ると、原則としてパーセンタイルを取れません。生の値か `Values` と `Counts` で送ります。
- **EMF のメトリクスが出ない:** `[INFO] {...}` のように前に文字が付いていると抽出されません。Essentials クラスのロググループでも使えません。
- **ログから数えられない:** Essentials クラスではメトリクスフィルターを使えず、ログクラスは後から変更できません。
- **サンプリングルールが効かない:** 判定は親が決めるので、下流に作ったルールは無視されます。
- **呼び出し回数は平らなのにエラーの報告がある:** スロットリングは `Invocations` に数えません。`Throttles` を見ます。
- **データベース障害で全コンテナが再起動する:** Liveness に依存先の確認を入れた結果です。依存先は Readiness で確認します。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [observability 問1](../../exercises/observability.md#q1) | 4.2.3 | ある開発者は、1 日に数回だけ動くバッチの Lambda 関数の Errors メトリクスにアラーム… |
| [observability 問2](../../exercises/observability.md#q2) | 4.2.3 | ある API の遅延を監視するアラームを作ります。単発のスパイクでは通知せず、直近 5 分のうち 3… |
| [observability 問3](../../exercises/observability.md#q3) | 4.2.2 | 開発者は、注文処理の遅延を PutMetricData の StatisticValues で 1 … |
| [observability 問4](../../exercises/observability.md#q4) | 4.2.2 | Lambda 関数からカスタムメトリクスを出すために、EMF で次の 1 行を標準出力へ出しています… |
| [observability 問5](../../exercises/observability.md#q5) | 4.2.2 | EC2 インスタンスがメモリ不足で停止する疑いがあります。運用担当者は詳細モニタリングを有効にしまし… |
| [observability 問6](../../exercises/observability.md#q6) | 4.3.5 | REST API の応答が遅いと報告がありました。CloudWatch で Latency の p9… |
| [observability 問7](../../exercises/observability.md#q7) | 4.1.2 | Lambda 関数の利用者から「ときどきエラーになる」と報告がありますが、Errors は 0 で、… |
| [observability 問8](../../exercises/observability.md#q8) | 4.2.1 | 開発チームは、アプリのログを取り込み料金の安いクラスで作ったロググループに送っています。その後、特定… |
| [observability 問12](../../exercises/observability.md#q12) | 4.2.2 | メトリクスフィルターの設定について、正しい説明はどれですか。（2つ選択） |
| [observability 問14](../../exercises/observability.md#q14) | 4.1.3 | Logs Insights で、各サーバーの最新のログを 1 件ずつ表示したいと考えています。最も適… |
| [observability 問15](../../exercises/observability.md#q15) | 4.2.4 | A、B の順に呼び出すマイクロサービスを X-Ray でトレースしています。開発者は、サービス B … |
| [observability 問16](../../exercises/observability.md#q16) | 4.2.4 | 毎秒 100 リクエストを受ける API で、X-Ray のルールを ReservoirSize=1… |
| [observability 問17](../../exercises/observability.md#q17) | 4.2.4 | X-Ray のアノテーションとメタデータの説明として正しいものはどれですか。（2つ選択） |
| [observability 問18](../../exercises/observability.md#q18) | 4.2.4 | ECS でアプリと X-Ray デーモンを別のコンテナで動かしています。アプリはバックグラウンドのス… |
| [observability 問19](../../exercises/observability.md#q19) | 4.2.4 | 長時間かかる処理のセグメントが 64 KB を超え、X-Ray に届かないことがあります。また、処理… |
| [observability 問20](../../exercises/observability.md#q20) | 4.1.2 | 監査担当者から「先月、この S3 オブジェクトを削除した人を調べてほしい」と依頼されました。組織には… |
| [observability 問21](../../exercises/observability.md#q21) | 4.1.3 | Lambda 関数のロググループで、ERROR を含むログの件数を 5 分ごとに集計したいと考えてい… |
| [observability 問22](../../exercises/observability.md#q22) | 4.2.1 | Python の Lambda 関数は標準の logging でテキストのログを出しています。Log… |

<!-- questions:end -->

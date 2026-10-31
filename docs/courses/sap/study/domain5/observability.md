# 分野5: オブザーバビリティ

シグナルの標準化、複数アカウントの集約、通知の質、AI の監視、利用者の体験、SLO までを問います。値の計算も出ます。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [5.3.1](../../domain5.md#skill-5-3-1) | メトリクス、ログ、分散トレースの標準化 |
| [5.3.2](../../domain5.md#skill-5-3-2) | コンテナの監視 |
| [5.3.3](../../domain5.md#skill-5-3-3) | マルチアカウントのログ集約 |
| [5.3.4](../../domain5.md#skill-5-3-4) | アラートの設計 |
| [5.3.5](../../domain5.md#skill-5-3-5) | AI と ML のワークロードの監視 |
| [5.3.6](../../domain5.md#skill-5-3-6) | 利用者の体験の監視 |
| [5.3.7](../../domain5.md#skill-5-3-7) | サービスレベル目標 |

## 学習の順番 {#study-order}

1. [ロギング、モニタリング、オブザーバビリティの違い](../../../../services/observability.md#logging-monitoring-observability)、[SDK と OpenTelemetry](../../../../services/observability.md#xray-opentelemetry)、[構造化ログ](../../../../services/observability.md#structured-logging): 3 つのシグナルの役割と、新規の計装の標準を確認します。
2. [logConfiguration](../../../../services/containers.md#log-configuration)と [Application Signals](../../../../services/observability.md#application-signals): コンテナのログと、アプリの標準メトリクスを押さえます。
3. [サブスクリプションフィルター](../../../../services/observability.md#subscription-filters)、[設定](../../../../services/observability.md#subscription-settings)、[ログクラス](../../../../services/observability.md#log-classes): 集約の構成と制限を覚えます。
4. [評価の仕組み](../../../../services/observability.md#alarm-evaluation)、[欠落データの扱い](../../../../services/observability.md#treat-missing-data)、[複合アラーム](../../../../services/observability.md#composite-alarms)、[異常検知](../../../../services/observability.md#anomaly-detection): 誤報と見逃しを減らす手段を選べるようにします。
5. [Bedrock のメトリクス](../../../../services/ai.md#bedrock-metrics)、[見るべき指標](../../../../services/genai-apps.md#genai-metrics)、[ドリフトの種類](../../../../services/sagemaker.md#drift): 運用、トークン、品質、ドリフトを分けて考えます。
6. [CloudWatch Synthetics](../../../../services/operations.md#synthetics)と [CloudWatch RUM](../../../../services/operations.md#rum): データの元の違いを理解します。
7. [統計とパーセンタイル](../../../../services/observability.md#statistics)と[パーセンタイルのアラーム](../../../../services/observability.md#percentile-alarms): 平均で隠れる問題と SLO の指標を確認します。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| 配信の再試行 | 最大 24 時間 | その後は破棄 |
| RUM のデータの保持 | 30 日 | 長く残すなら CloudWatch Logs へコピー |
| 30 日のエラーバジェット | 99.9% で 43.2 分、99.95% で 21.6 分 | 43,200 分 × 許容の割合 |
| バーンレートのしきい値 | 消費の割合 × SLO の時間 ÷ 窓の時間 | 5% を 1 時間で、30 日の SLO なら 36 |
| 複合アラーム | 子は同じアカウントとリージョン | EC2 や Auto Scaling のアクションは不可 |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| ベンダーに依存せず計装する | ADOT と OpenTelemetry |
| 1 つのリージョンの多数のアカウントを横断で見る | クロスアカウントオブザーバビリティと Organizations |
| 短命なタスクの CPU とメモリ | Container Insights |
| 呼び出し数、可用性、遅延、依存関係、SLO | Application Signals |
| 別のリージョンのストリームへ集約する | ロググループと同じリージョンに宛先を置く |
| 一部のシャードだけ混む | `distribution` を `Random` |
| 複数の症状のときだけ呼ぶ | 複合アラームにだけ通知を付ける |
| 周期のある指標の急減 | 異常検知の下側 |
| データが来ないこと自体が障害 | `breaching` |
| 入力も出力も安定なのに正解率が下がる | コンセプトドリフト |
| 利用者がいない時間の故障 | Synthetics |
| 実際の国やブラウザの差 | RUM |
| 計画メンテナンスを SLO から外す | 時間枠の除外 |

## 引っかかりやすい点 {#traps}

- X-Ray SDK とデーモンはメンテナンスモードです。トレースの保存先としての X-Ray は引き続き使えます。
- Essentials クラスではサブスクリプションフィルターを使えません。クラスは後から変更できません。
- アラームのアクションにランブックは直接指定できません。EventBridge で状態変化を受けます。
- 子のアラームに通知を残すと、複合アラームを作っても通知は減りません。
- Incident Manager、Change Manager、Model Monitor は新規受付を終了しました。
- ハートビートのアラームに `notBreaching` を選ぶと、止まっても `OK` のままです。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [observability 問1](../../exercises/observability.md#q1) | 5.3.1 | ある企業は、ECS と Lambda で動く 50 の新しいサービスの計装を標準化します。将来、トレ… |
| [observability 問2](../../exercises/observability.md#q2) | 5.3.1 | 組織には 1 つのリージョンで動く 60 のアカウントがあり、毎月アカウントが増えます。運用チームは… |
| [observability 問3](../../exercises/observability.md#q3) | 5.3.1 | 障害の調査に時間がかかっています。アラームで遅延の増加に気づいても、どのサービスが遅いのかが分からず… |
| [observability 問4](../../exercises/observability.md#q4) | 5.3.2 | ECS on Fargate で 80 のサービスを動かしています。タスクは頻繁に入れ替わり、タスク… |
| [observability 問5](../../exercises/observability.md#q5) | 5.3.2 | ECS のアプリは標準出力へログを書きます。アプリのコードは変更せずに、ログを Firehose と… |
| [observability 問6](../../exercises/observability.md#q6) | 5.3.2 | EKS と ECS で動くアプリの運用チームは、サービスごとの呼び出し数、可用性、遅延を統一の形式で… |
| [observability 問7](../../exercises/observability.md#q7) | 5.3.3 | ある企業は、東京と大阪の多数のアカウントのアプリログを、ログ用のアカウントにある東京の Kinesi… |
| [observability 問8](../../exercises/observability.md#q8) | 5.3.3 | 費用の削減のため、昨年作成したアプリのロググループはすべて Essentials クラスです。今回、… |
| [observability 問9](../../exercises/observability.md#q9) | 5.3.3 | ログストリームの少ない大量のログを、プロビジョンドの Kinesis Data Streams へサ… |
| [observability 問10](../../exercises/observability.md#q10) | 5.3.3 | 全アカウントのログについて、2 つの要件があります。セキュリティチームは、認証のログを準リアルタイム… |
| [observability 問11](../../exercises/observability.md#q11) | 5.3.4 | 当番の担当者は、CPU、遅延、エラー率の 3 つのアラームから別々に呼び出され、夜間の呼び出しが多す… |
| [observability 問12](../../exercises/observability.md#q12) | 5.3.4 | EC の受注数は、平日の昼に多く、深夜に少ないパターンです。深夜に受注が急に止まる障害があっても、深… |
| [observability 問13](../../exercises/observability.md#q13) | 5.3.4 | 常駐の処理は、動いている間だけ 1 分ごとにカスタムメトリクスのハートビートを送ります。アラームは … |
| [observability 問14](../../exercises/observability.md#q14) | 5.3.4 | ディスクの使用率のアラームが鳴ったら、定型の手順としてログを退避するランブックを実行します。一方、複… |
| [observability 問15](../../exercises/observability.md#q15) | 5.3.5 | Bedrock を使うチャットアプリで、利用者から「最初の文字が出るまで遅い」という声があります。ま… |
| [observability 問16](../../exercises/observability.md#q16) | 5.3.5 | AgentCore で動く手続き支援のエージェントで、ツールの呼び出しを何度も繰り返して、回答までの… |
| [observability 問17](../../exercises/observability.md#q17) | 5.3.5 | 不正検知のモデルを SageMaker AI のエンドポイントで運用しています。入力の分布も、予測の… |
| [observability 問18](../../exercises/observability.md#q18) | 5.3.5 | 利用が断続的な社内の推論 API に、SageMaker AI のサーバーレス推論を使っています。朝… |
| [observability 問19](../../exercises/observability.md#q19) | 5.3.6 | インターネットに公開していない社内の API を、VPC の中から Synthetics のカナリア… |
| [observability 問20](../../exercises/observability.md#q20) | 5.3.6 | ある動画配信の企業は CloudWatch RUM を導入しました。読み込み時間の傾向を前年の同じ時… |
| [observability 問21](../../exercises/observability.md#q21) | 5.3.6 | オンライン予約のサイトで、2 つの課題があります。(1) 利用者がいない早朝のデプロイで予約の手順が… |
| [observability 問22](../../exercises/observability.md#q22) | 5.3.7 | 期間ベースの SLO を、30 日間、1 分の期間、達成目標 99.95% で設定しました。今月は、… |
| [observability 問23](../../exercises/observability.md#q23) | 5.3.7 | 30 日間の SLO に、バーンレートのアラームを設定します。「6 時間で 30 日分のエラーバジェ… |
| [observability 問24](../../exercises/observability.md#q24) | 5.3.7 | 毎週日曜日の深夜に計画メンテナンスがあり、その間はサービスが意図的に止まります。契約上、この時間は可… |
| [observability 問25](../../exercises/observability.md#q25) | 5.3.7 | 経営層から「購入の体験を速くする」という要望がありました。現在のダッシュボードは、購入 API の平… |
| [observability 問26](../../exercises/observability.md#q26) | 5.3.7 | SaaS 企業は、顧客との契約で「各暦月の可用性 99.9%」を約束しています。同時に、リリースの判… |

<!-- questions:end -->

# 分野4: 監査ログ

監査のための CloudTrail と CloudWatch Logs、ログの分析と組み合わせを問います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [4.4.1](../../domain4.md#skill-4-4-1) | CloudTrail による API の追跡 |
| [4.4.2](../../domain4.md#skill-4-4-2) | CloudWatch Logs によるアプリケーションログの保存 |
| [4.4.3](../../domain4.md#skill-4-4-3) | CloudTrail Lake による一元的なログのクエリ |
| [4.4.4](../../domain4.md#skill-4-4-4) | AWS サービスによるログの分析 |
| [4.4.5](../../domain4.md#skill-4-4-5) | サービスを組み合わせたロギング |

## 学習の順番 {#study-order}

1. [証跡とイベント履歴](../../../../services/observability.md#cloudtrail-trails): 組織の証跡と検証を確認します。
2. [ロググループと保持期間](../../../../services/observability.md#log-groups): 保存の期間を設定します。
3. [データ保護ポリシー](../../../../services/observability.md#logs-data-protection): 取り込み時のマスクを覚えます。
4. [CloudTrail Lake](../../../../services/observability.md#cloudtrail-lake): 現在の状況を確認します。
5. [サブスクリプションフィルター](../../../../services/observability.md#subscription-filters): 送信先を確認します。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| CloudTrail Lake の新規受付 | 2026 年 5 月 31 日で終了 | 新規は証跡と Athena、または CloudWatch |
| サブスクリプションフィルターの送信先 | Kinesis、Lambda、Firehose、OpenSearch | S3 は Firehose 経由 |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 90 日より長く残す | 証跡で S3 へ |
| 権限の変更者を調べる | 管理イベント |
| ログの機密データを隠す | データ保護ポリシー |
| S3 の CloudTrail を調べる | Athena |
| 直近のアプリのエラーの傾向 | Logs Insights |
| 大量のログの複雑な処理 | EMR |

## 引っかかりやすい点 {#traps}

- KMS の暗号化はマスクではありません。
- 新規の環境で CloudTrail Lake は選べません。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [audit-logging 問1](../../exercises/audit-logging.md#q1) | 4.4.1 | 監査の要件で、全アカウントと全リージョンの API の記録を 7 年残します。どの設定ですか。 |
| [audit-logging 問2](../../exercises/audit-logging.md#q2) | 4.4.1 | 「誰が Lake Formation の権限を変えたか」を調べます。どのイベントですか。 |
| [audit-logging 問3](../../exercises/audit-logging.md#q3) | 4.4.1 | 監査の要件と CloudTrail の設定の組み合わせで正しいものはどれですか。（2つ選択） |
| [audit-logging 問4](../../exercises/audit-logging.md#q4) | 4.4.2 | アプリのログを監査のため 3 年残し、1 か月より古いものは安く保存します。最も適切なものはどれです… |
| [audit-logging 問5](../../exercises/audit-logging.md#q5) | 4.4.2 | ログに個人のメールアドレスが入ることがあります。コードの変更なしに、取り込み時に隠します。何を設定し… |
| [audit-logging 問6](../../exercises/audit-logging.md#q6) | 4.4.2 | ログの要件と設定の組み合わせで正しいものはどれですか。 |
| [audit-logging 問7](../../exercises/audit-logging.md#q7) | 4.4.3 | 2026 年 5 月より前から CloudTrail Lake を使っている組織です。複数のアカウン… |
| [audit-logging 問8](../../exercises/audit-logging.md#q8) | 4.4.3 | 2026 年 10 月に新しく AWS を使い始めた顧客が、複数のアカウントの CloudTrail… |
| [audit-logging 問9](../../exercises/audit-logging.md#q9) | 4.4.3 | CloudTrail Lake と「証跡と Athena」の違いとして正しいものはどれですか。 |
| [audit-logging 問10](../../exercises/audit-logging.md#q10) | 4.4.4 | 「過去 90 日に、このバケットのポリシーを変えた人は誰か」を、S3 にある CloudTrail … |
| [audit-logging 問11](../../exercises/audit-logging.md#q11) | 4.4.4 | Lambda の直近 1 時間のエラーの傾向を、その場で調べます。構築はしません。何を使いますか。 |
| [audit-logging 問12](../../exercises/audit-logging.md#q12) | 4.4.4 | セキュリティチームが、ログの全文検索とダッシュボードを常時使います。何を選びますか。 |
| [audit-logging 問13](../../exercises/audit-logging.md#q13) | 4.4.5 | CloudWatch Logs のログを Parquet で S3 に集め、Athena で調べます… |
| [audit-logging 問14](../../exercises/audit-logging.md#q14) | 4.4.5 | 毎日数十 TB のログを結合し、複雑な処理を Spark で行います。どれが適切ですか。 |
| [audit-logging 問15](../../exercises/audit-logging.md#q15) | 4.4.5 | ログの使い方と選択の組み合わせで正しいものはどれですか。（2つ選択） |

<!-- questions:end -->

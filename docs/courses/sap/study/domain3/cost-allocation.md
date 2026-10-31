# 分野3: コストの配分と可視化

誰の費用かを正しく分け、見える形にし、想定を超える前に気づく仕組みを問います。予防、標準化、検出、修復の手段を区別するのが要点です。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [3.3.1](../../domain3.md#skill-3-3-1) | コスト配分のタグ戦略 |
| [3.3.2](../../domain3.md#skill-3-3-2) | 詳細な請求データの報告と分析 |
| [3.3.3](../../domain3.md#skill-3-3-3) | ポリシーによるタグの強制 |
| [3.3.4](../../domain3.md#skill-3-3-4) | チャージバックとショーバック |
| [3.3.5](../../domain3.md#skill-3-3-5) | コストの監視とアラート |

## 学習の順番 {#study-order}

1. [コスト配分タグ](../../../../services/cost-management.md#cost-allocation-tags): 有効化の場所、反映の時間、バックフィルを覚えます。
2. [タグ戦略](../../../../services/governance.md#tagging-strategy): キーと値の標準を、IaC で付ける流れをつかみます。
3. [タグポリシー](../../../../services/governance.md#tag-policies)、[SCP](../../../../services/governance.md#scp)、[Config ルール](../../../../services/governance.md#config-rules): それぞれが止めるものと、止めないものを区別します。
4. [Cost Explorer](../../../../services/cost-management.md#cost-explorer)と [Data Exports と CUR](../../../../services/cost-management.md#data-exports): 画面での分析と行単位の分析を使い分けます。
5. [Quick Sight](../../../../services/data-engineering.md#quick-sight)と [S3 上のログを問い合わせる](../../../../services/streaming.md#athena-logs): 報告の流れを確認します。
6. [Cost Categories](../../../../services/cost-management.md#cost-categories): 分類のルールと、共有費用の分割方式を覚えます。
7. [分割コスト配分データ（公式）](https://docs.aws.amazon.com/cur/latest/userguide/split-cost-allocation-data.html): コンテナの費用を分ける方法と、見られる場所を押さえます。
8. [モデル ID と推論プロファイル](../../../../services/ai.md#model-identifiers): Bedrock の費用をタグで追う方法を確認します。
9. [AWS Budgets](../../../../services/cost-management.md#budgets)、[予算アクション](../../../../services/cost-management.md#budget-actions)、[Cost Anomaly Detection](../../../../services/cost-management.md#cost-anomaly-detection)、[請求アラーム](../../../../services/cost-management.md#billing-alarms): 検出と対応の違いを整理します。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| タグの表示、有効化 | それぞれ最大 24 時間 | 設定の直後には見えない |
| タグのバックフィル | 最大 12 か月 | 管理アカウントから依頼 |
| コストカテゴリの反映 | 最大 24 時間 | Cost Explorer、Budgets、Data Exports で使う |
| `required-tags` | 一度に最大 6 タグ | 検出で、作成は止めない |
| 請求メトリクスのリージョン | `us-east-1` | 他のリージョンでは見つからない |
| Budgets の更新 | 1 日最大 3 回 | しきい値は低めに |
| Anomaly Detection の実行 | 1 日に約 3 回 | 請求データの処理の後 |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| タグのない作成を止める | `Null` 条件で拒否する SCP。作成の操作に絞る |
| タグの値を標準化する | タグポリシーの `enforced_for` |
| 既存のタグのないリソースを補う | Config の `required-tags` と独自の自動化ドキュメント |
| タグが揃う前に事業部で報告する | コストカテゴリでアカウントとタグを組み合わせる |
| 明細を SQL で分析する | CUR 2.0 を S3 へ出力し、Athena |
| 経営層の共有のダッシュボード | Athena と Quick Sight |
| 共有の EKS クラスターをチームへ請求する | 分割コスト配分データ。`aws:eks:namespace` で集計 |
| 実際の使用量も反映して請求する | Prometheus の方式（リクエストと使用量の高い方） |
| 合意した比率で共有費用を配る | 分割ルールの Fixed |
| しきい値を決めにくい急増を見つける | Cost Anomaly Detection |
| 予測で超過しそうなら新規の作成を止める | 予算アクションで SCP を適用 |
| Savings Plans の使い残しに気づきたい | Savings Plans の使用率の予算 |

## 引っかかりやすい点 {#traps}

- タグを付けるだけでは請求データに出ません。管理アカウントで有効にします。
- タグのキーと値は大文字小文字を区別します。
- タグポリシーの基本のルールは、タグのない作成を止めません。
- `AWS-SetRequiredTags` は `required-tags` の修復として動作しません。独自のドキュメントを作ります。
- 分割コスト配分データは Cost Explorer で使えません。オプトインも必要です。
- 予算アクションから、他のアカウントの EC2 や RDS は指定できません。他のアカウントへ適用できるのは SCP です。
- 連結アカウント、タグ、カテゴリのモニターは管理アカウントでだけ作れます。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [cost-allocation 問1](../../exercises/cost-allocation.md#q1) | 3.3.1 | ある会社の組織では、8 か月前から CostCenter タグを各リソースに付けています。昨日、管理… |
| [cost-allocation 問2](../../exercises/cost-allocation.md#q2) | 3.3.1 | ある会社の費用レポートには、Env と env、prod と Prod が別々に集計されています。リ… |
| [cost-allocation 問3](../../exercises/cost-allocation.md#q3) | 3.3.1 | ある会社は事業部ごとに費用を報告したいと考えています。ところが、古いアカウントにはタグのないリソース… |
| [cost-allocation 問4](../../exercises/cost-allocation.md#q4) | 3.3.2 | ある会社の FinOps チームは、組織全体の明細を行単位で SQL により分析したいと考えています… |
| [cost-allocation 問5](../../exercises/cost-allocation.md#q5) | 3.3.2 | あるグローバル企業の経営層は、事業部とプロダクトごとの費用を、毎週見られる共有のダッシュボードで確認… |
| [cost-allocation 問6](../../exercises/cost-allocation.md#q6) | 3.3.2 | あるデータ基盤チームは、従来の CUR を取り込む ETL を運用しています。タグの追加などで列が変… |
| [cost-allocation 問7](../../exercises/cost-allocation.md#q7) | 3.3.3 | ある会社は、全アカウントでタグ CostCenter のない EC2 インスタンスを作成できないよう… |
| [cost-allocation 問8](../../exercises/cost-allocation.md#q8) | 3.3.3 | ある会社は、タグの統制を設計しています。要件は 2 つあります。EC2 の作成時に Project … |
| [cost-allocation 問9](../../exercises/cost-allocation.md#q9) | 3.3.3 | ある会社には、タグのない既存のリソースが多数あります。作成を止めるのではなく、タグのないリソースを継… |
| [cost-allocation 問10](../../exercises/cost-allocation.md#q10) | 3.3.3 | あるプラットフォームチームは、全リソースのタグ付けを強制するため、Action: "*" で aws… |
| [cost-allocation 問11](../../exercises/cost-allocation.md#q11) | 3.3.4 | ある会社は 1 つの EKS クラスターを 5 チームで共有し、チームごとに名前空間を分けています。… |
| [cost-allocation 問12](../../exercises/cost-allocation.md#q12) | 3.3.4 | ある会社は、EKS の分割コスト配分データでチームへ請求しています。Pod のリクエストより実際の使… |
| [cost-allocation 問13](../../exercises/cost-allocation.md#q13) | 3.3.4 | ある会社は、共有のネットワーク基盤の費用を 3 つの事業部へ配分します。社内の合意で、比率は 60%… |
| [cost-allocation 問14](../../exercises/cost-allocation.md#q14) | 3.3.4 | ある会社は、1 つのアカウントで複数のチームが同じ Bedrock のモデルを呼んでいます。チームご… |
| [cost-allocation 問15](../../exercises/cost-allocation.md#q15) | 3.3.5 | ある会社は、Organizations の配下に検証用のアカウントを多数持っています。各検証アカウン… |
| [cost-allocation 問16](../../exercises/cost-allocation.md#q16) | 3.3.5 | ある会社には、季節性のある事業を持つ 100 のアカウントがあります。アカウントごとに適切な額を決め… |
| [cost-allocation 問17](../../exercises/cost-allocation.md#q17) | 3.3.5 | ある会社は、Compute Savings Plans を大量に購入しました。適正化やワークロードの… |
| [cost-allocation 問18](../../exercises/cost-allocation.md#q18) | 3.3.5 | ある運用担当者は、東京リージョンの CloudWatch で EstimatedCharges のア… |

<!-- questions:end -->

# 分野1: クラウドの導入と移行

AWS CAF の見方、移行の 7 つの R、誰に何を頼るかを問います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [クラウド導入の戦略](../../domain1.md#t1-3-adoption-strategies) | 4 つのフェーズとハイブリッド |
| [移行を支える情報源とプログラム](../../domain1.md#t1-3-resources) | 情報源とプログラムの選択 |
| [AWS CAF の成果とパースペクティブ](../../domain1.md#t1-3-caf) | 成果と 6 つのパースペクティブ |
| [移行の戦略](../../domain1.md#t1-3-migration-strategies) | 7 つの R とデータベースのレプリケーション |

## 学習の順番 {#study-order}

1. [Cloud Adoption Framework](../../../../services/cloud-foundations.md#caf): 4 つのフェーズと 6 つのパースペクティブを覚えます。
2. [移行の 7 つの R](../../../../services/migration.md#seven-rs): 問題文の表現と戦略を対応させます。
3. [移行タイプ](../../../../services/migration.md#dms-migration-types): 動かしたまま移す仕組みを確認します。
4. [Migration Evaluator](../../../../services/migration.md#migration-evaluator)、[Application Discovery Service](../../../../services/migration.md#application-discovery)、[AWS Migration Hub](../../../../services/migration.md#migration-hub): 目的で区別します。
5. [サポートの情報源](../../../../services/cloud-foundations.md#support-resources): Prescriptive Guidance と Professional Services を確認します。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| CAF のパースペクティブ | 6 つ | 事業寄りはビジネス、人材、ガバナンス。技術寄りはプラットフォーム、セキュリティ、オペレーション |
| CAF のフェーズ | 4 つ | Envision、Align、Launch、Scale |
| 移行の戦略 | 7 つ | Retire、Retain、Rehost、Relocate、Repurchase、Replatform、Refactor |
| MAP の段階 | 3 つ | Assess、Mobilize、Migrate & Modernize |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 期限が短く、手を加えずに移す | Rehost |
| 自社開発の CRM を SaaS にする | Repurchase |
| 自前の DB を RDS にする | Replatform |
| サーバーレスで作り直す | Refactor |
| 規制の都合で今は移さない | Retain |
| 使われていない | Retire |
| 社員のスキルや文化を整える | CAF の人材 |
| 費用対効果を試算する | Migration Evaluator |
| 移行の具体的な手順を調べる | AWS Prescriptive Guidance |

## 引っかかりやすい点 {#traps}

- Migration Hub と Application Discovery Service は新規受付を終了しています。試験対策としては役割を覚えます。
- Application Migration Service は、現在 AWS Transform MGN と呼ばれています。
- データの移行は DMS で、スキーマの変換は SCT です。
- CAF は組織の準備の枠組みで、システムを評価するものではありません。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [migration 問1](../../exercises/migration.md#q1) | クラウド導入の戦略 | AWS CAF が示す、クラウドによる変革の 4 つのフェーズを順に並べたものはどれですか。 |
| [migration 問2](../../exercises/migration.md#q2) | クラウド導入の戦略 | AWS CAF のフェーズのうち、小規模な試験導入を行って成果を確かめる段階はどれですか。 |
| [migration 問3](../../exercises/migration.md#q3) | クラウド導入の戦略 | 基幹システムはしばらく自社のデータセンターに残し、新しい Web サービスだけを AWS に置く方針… |
| [migration 問4](../../exercises/migration.md#q4) | 移行を支える情報源とプログラム | 経営層が移行の判断のために、現状の環境をもとに費用対効果の試算を求めています。最も適切なものはどれで… |
| [migration 問5](../../exercises/migration.md#q5) | 移行を支える情報源とプログラム | 移行の計画のために、オンプレミスのサーバーの一覧と依存関係を把握したいと考えています。試験ガイドの対… |
| [migration 問6](../../exercises/migration.md#q6) | 移行を支える情報源とプログラム | チームが移行の具体的な手順とパターンを文書で調べたいと考えています。最初に見るものとして最も適切なも… |
| [migration 問7](../../exercises/migration.md#q7) | 移行を支える情報源とプログラム | AWS Migration Acceleration Program（MAP）の説明として正しいもの… |
| [migration 問8](../../exercises/migration.md#q8) | AWS CAF の成果とパースペクティブ | 試験ガイドが挙げる、AWS CAF を使って得られる成果の例はどれですか。（2つ選択） |
| [migration 問9](../../exercises/migration.md#q9) | AWS CAF の成果とパースペクティブ | クラウド移行に向けて、社員のスキルと組織の文化を整える計画を立てたいと考えています。AWS CAF … |
| [migration 問10](../../exercises/migration.md#q10) | AWS CAF の成果とパースペクティブ | データとワークロードの機密性、完全性、可用性を確保することに焦点を当てた AWS CAF のパースペ… |
| [migration 問11](../../exercises/migration.md#q11) | AWS CAF の成果とパースペクティブ | AWS CAF のパースペクティブのうち、事業寄りのものはどれですか。（3つ選択） |
| [migration 問12](../../exercises/migration.md#q12) | 移行の戦略 | 期限まで時間がないので、数百台のサーバーをコードの変更なしで EC2 に移します。どの移行戦略ですか… |
| [migration 問13](../../exercises/migration.md#q13) | 移行の戦略 | 自社で開発した顧客管理システムをやめて、SaaS の製品に切り替えます。どの移行戦略ですか。 |
| [migration 問14](../../exercises/migration.md#q14) | 移行の戦略 | EC2 上で自前で運用する構成ではなく、アプリは変えずにデータベースだけ Amazon RDS に移… |
| [migration 問15](../../exercises/migration.md#q15) | 移行の戦略 | 規制の都合で、ある専用機器のシステムは当面オンプレミスに残すことにしました。どの移行戦略ですか。 |
| [migration 問16](../../exercises/migration.md#q16) | 移行の戦略 | 本番のデータベースを動かしたままクラウドへ移し、切り替えの停止を短くしたいと考えています。最も適切な… |

<!-- questions:end -->

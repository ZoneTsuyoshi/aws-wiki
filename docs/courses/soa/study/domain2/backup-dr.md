# 分野2: バックアップと災害復旧

サービスの選択、保持の条件、DR 戦略の見分け方を問います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [2.3.1](../../domain2.md#skill-2-3-1) | スナップショットとバックアップの自動化 |
| [2.3.4](../../domain2.md#skill-2-3-4) | 災害復旧の手順 |

## 学習の順番 {#study-order}

1. [AWS Backup](../../../../services/resilience.md#backup)と[バックアッププランとルール](../../../../services/resilience.md#backup-plans): プランとルールの設定を確認します。
2. [リソースの割り当て](../../../../services/resilience.md#backup-assignment)と[Vault Lock](../../../../services/resilience.md#vault-lock): タグの割り当てと削除の防止を覚えます。
3. [RTO と RPO](../../../../services/resilience.md#rto-rpo)と[4 つの DR 戦略](../../../../services/resilience.md#dr-strategies): 指標と戦略を結びます。
4. [パイロットライト](../../../../services/resilience.md#pilot-light)と[ウォームスタンバイ](../../../../services/resilience.md#warm-standby): 2 つの違いを見分けます。
5. [復元テストと監査](../../../../services/resilience.md#backup-testing)と[AWS Fault Injection Service(FIS)](../../../../services/resilience.md#fis): 復元テストと障害の演習を確認します。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| RDS の保持期間 | 0〜35 日 | 0 との間の変更で停止 |
| AWS Backup の頻度 | 最短 1 時間 | 毎日では RPO 1 時間を満たせない |
| コールドへの移行 | 最低 90 日 | 保持は移行日数 + 90 日以上 |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 複数のサービスを一元管理 | AWS Backup |
| EBS と AMI だけを追加料金なしで | Data Lifecycle Manager |
| 削除や短縮を防ぐ | Vault Lock |
| 待機側に少ない台数が稼働 | ウォームスタンバイ |
| データだけ複製し、アプリは 0 台 | パイロットライト |
| 費用を最小に、RTO は時間単位 | バックアップと復元 |

## 引っかかりやすい点 {#traps}

- レプリケーションは破損も複製します。
- 試していないバックアップは当てにできません。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [backup-dr 問1](../../exercises/backup-dr.md#q1) | 2.3.1 | 本番の EBS、RDS、DynamoDB、EFS のバックアップをタグで指定し、別のリージョンにもコ… |
| [backup-dr 問2](../../exercises/backup-dr.md#q2) | 2.3.1 | EBS のスナップショットだけを追加料金なしで、毎日自動で作って 7 日で消したいです。どれが最も適… |
| [backup-dr 問3](../../exercises/backup-dr.md#q3) | 2.3.1 | AWS Backup のプランで、RPO を 1 時間にしたいです。現在のルールは毎日 1 回です。… |
| [backup-dr 問4](../../exercises/backup-dr.md#q4) | 2.3.1 | AWS Backup のルールで、コールドストレージへの移行を 30 日後、保持の期間を 60 日に… |
| [backup-dr 問5](../../exercises/backup-dr.md#q5) | 2.3.1 | 監査の要件で、バックアップの削除や保持期間の短縮を管理者でもできないようにしたいです。どの機能を使い… |
| [backup-dr 問6](../../exercises/backup-dr.md#q6) | 2.3.1 | RDS の自動バックアップの保持期間の設定について正しいものを選んでください。（2つ選択） |
| [backup-dr 問7](../../exercises/backup-dr.md#q7) | 2.3.4 | 本番 12 台、DR に 2 台が常時稼働し、データは複製されています。どの DR 戦略ですか。 |
| [backup-dr 問8](../../exercises/backup-dr.md#q8) | 2.3.4 | Aurora のセカンダリだけが動き、Auto Scaling グループは希望 0 台です。RTO … |
| [backup-dr 問9](../../exercises/backup-dr.md#q9) | 2.3.4 | RTO は 24 時間、RPO は数時間です。費用を最小にしたいです。どの DR 戦略を選びますか。 |
| [backup-dr 問10](../../exercises/backup-dr.md#q10) | 2.3.4 | 災害復旧の手順についてのベストプラクティスとして正しいものを選んでください。（2つ選択） |
| [backup-dr 問11](../../exercises/backup-dr.md#q11) | 2.3.4 | DR の手順の演習で、AZ の障害や API のエラーを制御された形で起こしたいと考えています。どの… |
| [backup-dr 問12](../../exercises/backup-dr.md#q12) | 2.3.4 | RTO と RPO の説明として正しいものはどれですか。 |

<!-- questions:end -->

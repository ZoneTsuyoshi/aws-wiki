# 分野3: 災害対策

目標を満たす最も安い戦略の選択と、手順の自動化を問います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [RTO と RPO](../../domain3.md#t3-3-rto-rpo) | DR の概念（RTO、RPO） |
| [DR 戦略](../../domain3.md#t3-3-dr-strategies) | AWS Backup と復旧の戦略 |
| [復旧の手順](../../domain3.md#t3-3-recovery-procedures) | 復旧の手順 |
| [フェイルオーバーのテスト](../../domain3.md#t3-3-failover-testing) | フェイルオーバーのテスト |
| [バックアップと復旧](../../domain3.md#t3-3-backup) | リージョンをまたぐバックアップと復旧 |

## 学習の順番 {#study-order}

1. [達成できるかの計算](../../../../services/resilience.md#rto-rpo-budget): 検知、判断、昇格、DNS の合計で見積もります。
2. [4 つの DR 戦略](../../../../services/resilience.md#dr-strategies): 4 つの戦略の待機系の状態と費用を覚えます。
3. [AWS Elastic Disaster Recovery(DRS)](../../../../services/resilience.md#drs): サーバーの複製による DR を確認します。
4. [Region switch](../../../../services/resilience.md#arc-region-switch): 切り替えの工程の実行を理解します。
5. [実験テンプレート](../../../../services/resilience.md#fis-template): 対象、アクション、停止条件を確認します。
6. [バックアッププランとルール](../../../../services/resilience.md#backup-plans): プラン、タグの割り当て、コピーを押さえます。
7. [Vault Lock](../../../../services/resilience.md#vault-lock): コンプライアンスモードの意味を覚えます。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| バックアップと復元 | 時間単位 | 費用は低 |
| パイロットライト | 数十分 | データは複製、コンピュートは止める |
| ウォームスタンバイ | 数分 | 小さい規模で常時稼働 |
| マルチサイト | ほぼゼロ | 全規模で常時稼働 |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| サーバーの起動が RTO を超える | パイロットライトからウォームスタンバイへ |
| オンプレミスのサーバーをそのまま守る | Elastic Disaster Recovery |
| 管理者が奪われてもバックアップを守る | コンプライアンスモードの Vault Lock と別アカウント |
| 本番の障害なしで切り替えを試す | `Inverted`、FIS と停止条件 |

## 引っかかりやすい点 {#traps}

- 人の承認の時間も RTO に足します。
- コピーは宛先のボールトのキーで再暗号化されます。
- 復旧の後の切り戻しとデータの再同期も決めておきます。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [disaster-recovery 問1](../../exercises/disaster-recovery.md#q1) | RTO と RPO | Route 53 のフェイルオーバーで 30 秒ごとに 3 回のチェック（90 秒）、DB の昇格に… |
| [disaster-recovery 問2](../../exercises/disaster-recovery.md#q2) | RTO と RPO | データベースの RPO を 5 分と決めました。バックアップは毎晩 1 回で、4 時間ごとにトランザ… |
| [disaster-recovery 問3](../../exercises/disaster-recovery.md#q3) | RTO と RPO | 次の説明のうち、ビジネスの言葉を RTO と RPO に正しく対応付けているものはどれですか。（2つ… |
| [disaster-recovery 問4](../../exercises/disaster-recovery.md#q4) | DR 戦略 | RTO 15 分、RPO 1 分のシステムを別のリージョンで守ります。全規模で常時動かす費用は避けま… |
| [disaster-recovery 問5](../../exercises/disaster-recovery.md#q5) | DR 戦略 | オンプレミスの 80 台の Windows と Linux のサーバーを、アプリの変更なしで AWS… |
| [disaster-recovery 問6](../../exercises/disaster-recovery.md#q6) | DR 戦略 | 3 つのシステムの DR を選びます。費用の順番も考えて、最も安く要件を満たす組み合わせはどれですか… |
| [disaster-recovery 問7](../../exercises/disaster-recovery.md#q7) | 復旧の手順 | リージョン切り替えの手順は 12 段階あり、担当者の記憶と Wiki に頼っています。データベースの… |
| [disaster-recovery 問8](../../exercises/disaster-recovery.md#q8) | 復旧の手順 | RDS の昇格は Systems Manager Automation、切り替えは Route 53… |
| [disaster-recovery 問9](../../exercises/disaster-recovery.md#q9) | 復旧の手順 | DR の演習で次の問題が分かりました。別のリージョンの VPC と IAM ロールの構成が本番と違っ… |
| [disaster-recovery 問10](../../exercises/disaster-recovery.md#q10) | フェイルオーバーのテスト | RDS Multi-AZ と Aurora のフェイルオーバーの動きを定期的に確かめ、アプリの再接続… |
| [disaster-recovery 問11](../../exercises/disaster-recovery.md#q11) | フェイルオーバーのテスト | 本番の障害を起こさずに、次の切り替えの確認をします。(1) Route 53 のフェイルオーバーで、… |
| [disaster-recovery 問12](../../exercises/disaster-recovery.md#q12) | フェイルオーバーのテスト | 本番で AZ の障害を模擬する実験を行います。条件は次のとおりです。影響する対象をタグで絞る。応答時… |
| [disaster-recovery 問13](../../exercises/disaster-recovery.md#q13) | バックアップと復旧 | EBS、RDS、DynamoDB、EFS のバックアップを別々のスクリプトで管理しています。これを一… |
| [disaster-recovery 問14](../../exercises/disaster-recovery.md#q14) | バックアップと復旧 | ランサムウェアで管理者の権限が奪われても、バックアップを消されないようにします。保持の設定も短くさせ… |
| [disaster-recovery 問15](../../exercises/disaster-recovery.md#q15) | バックアップと復旧 | AWS Backup の運用で、(1) 別のリージョンへのコピーの暗号化は何で行うか、(2) バック… |

<!-- questions:end -->

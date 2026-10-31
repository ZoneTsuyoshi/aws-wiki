# 分野4: DR

RTO と RPO から戦略を選び、切り替えが障害時にも動く設計を問います。要件を満たす中で最も安いものを選ぶのが基本です。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [4.2.1](../../domain4.md#skill-4-2-1) | ビジネス要件に合う DR |
| [4.2.2](../../domain4.md#skill-4-2-2) | 継続的なレプリケーション |
| [4.2.3](../../domain4.md#skill-4-2-3) | DR の評価と復旧手順 |
| [4.2.4](../../domain4.md#skill-4-2-4) | マルチリージョンの DR |
| [4.2.5](../../domain4.md#skill-4-2-5) | DR のテストと検証 |
| [4.2.6](../../domain4.md#skill-4-2-6) | マルチクラスターのコンテナ戦略 |

## 学習の順番 {#study-order}

1. [RTO と RPO](../../../../services/resilience.md#rto-rpo)と[達成できるかの計算](../../../../services/resilience.md#rto-rpo-budget): 段階ごとの時間を足せるようにします。
2. [4 つの DR 戦略](../../../../services/resilience.md#dr-strategies): パイロットライトとウォームスタンバイの違いを説明できるようにします。
3. [AWS Elastic Disaster Recovery](../../../../services/resilience.md#drs): RPO を守る帯域の条件と、PIT スナップショットの使いどころを確認します。
4. [サービスごとの Multi-AZ と Multi-Region](../../../../services/resilience.md#patterns-by-service): マネージドサービスは各サービスの機能で複製します。
5. [AWS Resilience Hub](../../../../services/resilience.md#resilience-hub): ポリシー、評価の結果、推奨の流れを押さえます。
6. [Automation](../../../../services/operations.md#automation)と[複数アカウント、複数リージョンの実行](../../../../services/operations.md#automation-multi-account): 手順をコードにする方法を確認します。
7. [フェイルオーバーはデータプレーンで](../../../../services/resilience.md#failover-data-plane)と[静的安定性](../../../../services/resilience.md#static-stability): 障害時に頼れない操作を見分けます。
8. [ルーティングコントロール](../../../../services/resilience.md#arc-routing-control)、[Region switch](../../../../services/resilience.md#arc-region-switch)、[Global Accelerator との比較](../../../../services/resilience.md#global-accelerator): 切り替えの手段を使い分けます。
9. [グローバルデータベースの切り替え](../../../../services/databases-specialized.md#aurora-global-switchover): スイッチオーバーとフェイルオーバーの違いを確認します。
10. [復元テストと監査](../../../../services/resilience.md#backup-testing)と[コンテナのマルチクラスター戦略](../../../../services/resilience.md#multi-cluster): 検証の方法と、層ごとの設計を押さえます。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| バックアップと復元 | 時間単位 | 費用は最小 |
| パイロットライト | 数十分 | データは同期、アプリは停止 |
| ウォームスタンバイ | 分単位 | 縮小版がすぐに処理できる |
| アクティブ/アクティブ | ほぼゼロ | 費用は最大 |
| DRS | RPO は秒単位、RTO は通常 5〜20 分 | 平常時はステージング領域の費用 |
| AWS Backup の最短の頻度 | 1 時間 | 短い RPO には継続的バックアップ |
| Aurora グローバルデータベース | 最大 10 のセカンダリ、RPO は通常秒単位 | スイッチオーバーなら RPO 0 |
| Route 53 のコントロールプレーン | us-east-1 | データプレーンは世界に分散 |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 要件を満たす中で最も安くする | 許容できる最も遅い戦略を選ぶ |
| 直後から少ない容量でも処理する | ウォームスタンバイ |
| 破損や誤削除からも戻す | レプリケーションに加えて時点復旧のバックアップ |
| オンプレミスのサーバーの DR で、RPO が秒単位 | DRS |
| ランサムウェアの前の状態へ戻す | DRS の PIT スナップショットを選ぶ |
| Resilience Hub の結果が Policy breached | 推奨を反映して再評価する。ポリシーを緩めない |
| Route 53 のレコードを編集する手順がある | ヘルスチェックか ARC に置き換える |
| 誤った自動切り替えを避け、人が判断する | ARC のルーティングコントロール。全停止はアサーションルールで防ぐ |
| 複数アカウントの手順を順に実行する | ARC の Region switch |
| 固定 IP、TCP、DNS のキャッシュを避ける | Global Accelerator |
| 計画された Aurora のリージョン移動 | スイッチオーバー |
| DR を本番に影響なく試す | DRS のドリル |
| 実際に復元できるかを自動で確かめる | AWS Backup の復元テスト |
| 変更のたびに回復性の低下を見つける | パイプラインで Resilience Hub を評価する |

## 引っかかりやすい点 {#traps}

- レプリケーションは破損も複製します。Aurora グローバルデータベースだけでは誤削除から戻せません。
- DRS の RPO は、回線が書き込みを受け取れる場合の値です。帯域が足りないと伸びます。
- DRS はサーバーのブロックを複製します。マネージドサービスのデータには使えません。
- Resilience Hub の RTO、RPO に 0 を入れると、評価の最小がほぼ 0 のため Policy breached になります。
- ウォームスタンバイでも、障害時のスケールはコントロールプレーンに依存します。DR 側のクォータと容量も確認します。
- ゾーンオートシフトは AZ の機能です。リージョンの切り替えには使いません。
- ECR のレプリケーションは、既定では設定の後にプッシュしたイメージだけが対象です。既存のものにはバックフィルが必要です。
- ECS と EKS のクラスターはリージョン単位です。1 つのクラスターでリージョンをまたげません。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [dr 問1](../../exercises/dr.md#q1) | 4.2.1 | 社内の在庫レポートのシステムは、RTO 4 時間、RPO 1 時間を求められています。データは RD… |
| [dr 問2](../../exercises/dr.md#q2) | 4.2.1 | 会員サイトは ECS と DynamoDB で動いています。要件は RTO 30 分、RPO 1 分… |
| [dr 問3](../../exercises/dr.md#q3) | 4.2.1 | 決済のシステムは RTO 3 分、RPO は秒単位を求められています。障害の直後から、容量は少なくて… |
| [dr 問4](../../exercises/dr.md#q4) | 4.2.1 | 受注システムは Aurora グローバルデータベースで DR に備えています。ある日、アプリの不具合… |
| [dr 問5](../../exercises/dr.md#q5) | 4.2.1 | あるシステムの RTO は 20 分です。ウォームスタンバイの切り替えの実測は次のとおりでした。検知… |
| [dr 問6](../../exercises/dr.md#q6) | 4.2.2 | オンプレミスの 80 台の Windows と Linux のサーバーに、業務アプリと自前のデータベ… |
| [dr 問7](../../exercises/dr.md#q7) | 4.2.2 | DRS で保護しているオンプレミスのファイルサーバーが、3 時間前にランサムウェアで暗号化されたと分… |
| [dr 問8](../../exercises/dr.md#q8) | 4.2.2 | DRS で 10 台のサーバーを保護しています。各サーバーは平均 10 MB/s で書き込みます。A… |
| [dr 問9](../../exercises/dr.md#q9) | 4.2.2 | EC2 のアプリ（OS に独自の設定がある）、Aurora MySQL、DynamoDB でできたシ… |
| [dr 問10](../../exercises/dr.md#q10) | 4.2.3 | Resilience Hub で、アプリを Terraform の状態ファイルから定義しました。回復… |
| [dr 問11](../../exercises/dr.md#q11) | 4.2.3 | Mission critical のアプリに、Resilience Hub の回復性ポリシーで RT… |
| [dr 問12](../../exercises/dr.md#q12) | 4.2.3 | DR の手順は 60 ページの文書で、担当者がコンソールを操作しています。訓練のたびに順序を間違えま… |
| [dr 問13](../../exercises/dr.md#q13) | 4.2.4 | ある企業の DR の手順では、障害時に担当者が Route 53 のレコードを編集して、DR リージ… |
| [dr 問14](../../exercises/dr.md#q14) | 4.2.4 | Aurora グローバルデータベースを使う 2 リージョンのシステムです。一時的なネットワークの不調… |
| [dr 問15](../../exercises/dr.md#q15) | 4.2.4 | あるアプリの復旧には、5 つのアカウントにまたがる手順が必要です。データベースの切り替え、DR の容… |
| [dr 問16](../../exercises/dr.md#q16) | 4.2.4 | 工場の機器が独自プロトコルの TCP で AWS 上のサービスへ接続します。機器は DNS の結果を… |
| [dr 問17](../../exercises/dr.md#q17) | 4.2.4 | Aurora グローバルデータベースのプライマリを、四半期に一度、保守と訓練のために別のリージョンへ… |
| [dr 問18](../../exercises/dr.md#q18) | 4.2.4 | ウォームスタンバイの DR で、障害時に DR リージョンの Auto Scaling グループの希… |
| [dr 問19](../../exercises/dr.md#q19) | 4.2.5 | アプリの構成は毎週のように変わります。過去に、ある変更で RDS のクロスリージョンのレプリカが外れ… |
| [dr 問20](../../exercises/dr.md#q20) | 4.2.5 | DRS で保護するオンプレミスの基幹サーバーを、四半期ごとに検証します。業務を止めず、元のサーバーに… |
| [dr 問21](../../exercises/dr.md#q21) | 4.2.5 | 監査人から、AWS Backup の復旧ポイントが実際に復元できる証拠と、復元にかかる時間の実績を求… |
| [dr 問22](../../exercises/dr.md#q22) | 4.2.5 | Direct Connect を 2 つのロケーションで冗長にし、片方の障害でもう片方へ切り替わる設… |
| [dr 問23](../../exercises/dr.md#q23) | 4.2.6 | ECR のレジストリに、別リージョンへのレプリケーションを今週設定しました。DR リージョンの EK… |
| [dr 問24](../../exercises/dr.md#q24) | 4.2.6 | ECS と DynamoDB のアプリで、リージョンの障害に備えます。タスクは東京の 3 つの AZ… |
| [dr 問25](../../exercises/dr.md#q25) | 4.2.6 | EKS を東京と大阪で動かしています。大阪は平常時にほとんど処理せず、Karpenter で障害時に… |
| [dr 問26](../../exercises/dr.md#q26) | 4.2.6 | 本番の EKS クラスターは 1 つで、Kubernetes のバージョンアップのたびに全サービスへ… |

<!-- questions:end -->

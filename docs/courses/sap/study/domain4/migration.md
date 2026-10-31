# 分野4: 移行戦略

移行のどの段階で、どの戦略とサービスを選ぶかを問います。期限と回線の数字から答えを絞る問題が多く出ます。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [4.1.1](../../domain4.md#skill-4-1-1) | 発見、ポートフォリオ評価、移行ウェーブ |
| [4.1.2](../../domain4.md#skill-4-1-2) | リホスト戦略 |
| [4.1.3](../../domain4.md#skill-4-1-3) | データベースとデータの移行 |
| [4.1.4](../../domain4.md#skill-4-1-4) | リプラットフォーム戦略 |
| [4.1.5](../../domain4.md#skill-4-1-5) | リファクタ戦略 |
| [4.1.6](../../domain4.md#skill-4-1-6) | レガシーワークロードのモダナイズ |

## 学習の順番 {#study-order}

1. [移行の 7 つの R](../../../../services/migration.md#seven-rs): 戦略ごとの向く場面を表で覚えます。大規模な移行で最初に Refactor を選ばない理由も確認します。
2. [AWS Transform](../../../../services/migration.md#transform)と [Migration Evaluator](../../../../services/migration.md#migration-evaluator): 依存関係とウェーブは Transform、費用対効果は Migration Evaluator と分けて覚えます。
3. [AWS Transform MGN](../../../../services/migration.md#mgn): ライフサイクル、[通信の要件](../../../../services/migration.md#mgn-network)、[テンプレート](../../../../services/migration.md#mgn-templates)の適用範囲を押さえます。
4. [VMware の移行](../../../../services/migration.md#vmware): VMware をそのまま使うか、やめるかで分けます。
5. [AWS DMS](../../../../services/migration.md#dms)と [SCT](../../../../services/migration.md#sct): データとスキーマの役割の違い、[CDC の前提](../../../../services/migration.md#dms-cdc)、[タスクの設定](../../../../services/migration.md#dms-task-settings)を確認します。
6. [DataSync](../../../../services/migration.md#datasync)と[転送方法の選び方](../../../../services/migration.md#choosing-transfer): 計算式を手で解けるようにします。変更の量も含めます。
7. [Aurora](../../../../services/databases.md#aurora)と [Fargate と EC2](../../../../services/containers.md#fargate-vs-ec2): リプラットフォームで減る作業と、合わない条件を確認します。
8. [アーキテクチャパターン](../../../../services/sdk-resilience.md#architectural-patterns)と[密結合と疎結合](../../../../services/messaging.md#coupling): 機能を切り出すときのデータの分離を考えます。
9. [Amazon MQ](../../../../services/other-services.md#mq): プロトコルを保つか、書き換えるかで SQS、SNS と分けます。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| 転送の目安 | 1 Gbps、利用率 80% で 100 TB が約 12 日 | 他は比例で計算する |
| 回線で 1 日に送れる量 | 100 Mbps、利用率 80% で 864 GB | 変更の量が下回らないと追いつかない |
| MGN の通信 | TCP 443、TCP 1500 | 登録は 443、複製は 1500 |
| MGN のレプリケーションサーバーの既定 | `t3.small` | 書き込みが多いサーバーだけ個別に大きくする |
| DataSync のスケジュール | 最短 1 時間 | 短い間隔にはできない |
| DataSync のタスクあたりの上限 | エージェントあり 10 Gbps、なし 5 Gbps | 超えるならタスクを分ける |
| Lambda の実行時間 | 最大 15 分 | 超える処理は Fargate のタスクにする |
| Retire の目安 | 90 日間接続がない、CPU とメモリの平均が 5% 未満 | 移さずに止める |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 期限が短い、多数のサーバーを変更せずに移す | Rehost（AWS Transform MGN） |
| 依存関係を調べて移行ウェーブを作る | AWS Transform（既存のお客様は Application Discovery Service） |
| 移行後の費用を取締役会に説明する | Migration Evaluator |
| VMware の IP と運用手順を変えたくない | Relocate（Amazon EVS） |
| 異なるエンジンへ、停止を最小に | SCT か DMS Schema Conversion と、DMS の `full-load-and-cdc` |
| ターゲットがまだないが変換の難しさを知りたい | 評価レポートと仮想ターゲット |
| MySQL のソースで CDC が動かない | 行形式のバイナリログ。RDS なら自動バックアップも有効にする |
| 回線の余力があるのに DataSync が遅い | データセットを分けて複数のタスクにする |
| 回線が足りず、データは稼働中の NAS にある | 期間限定の Direct Connect と DataSync |
| 機能ごとに切り替え、切り戻す | ストラングラーフィグパターン |
| 呼び出し元を変えずに新しいモデルのサービスを呼ぶ | 腐敗防止層 |
| JMS のコードを変更できない | Amazon MQ |
| メインフレーム、.NET Framework のモダナイズ | AWS Transform |

## 引っかかりやすい点 {#traps}

- 古い教材の Migration Hub、Application Discovery Service、App2Container、Mainframe Modernization は新規受付を終了しています。新しいお客様の答えにはなりません。
- MGN のテンプレートを変えても、追加済みのサーバーには適用されません。サーバーごとに上書きします。
- MGN の vCenter のエージェントレス複製は、新規のデプロイでは使えません。
- MGN は移行、DRS は備え続けるためのサービスです。複製の仕組みが似ているので、設問の目的で分けます。
- DMS はテーブルと主キーなどの基本しか作りません。ストアドプロシージャやセカンダリインデックスは移りません。
- Limited LOB mode は、上限を超えた部分を切り詰めます。エラーにならないので、後で気づきます。
- Data Transfer Terminal は、データが可搬の機器にあることが前提です。
- VMware Cloud on AWS は、AWS が再販していません。
- Refactor の切り出しで、データベースを共有したままだと密結合が残ります。同期は移行の間だけの手段です。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [migration 問1](../../exercises/migration.md#q1) | 4.1.1 | 製造業の企業が、5 か月後に契約が切れるデータセンターから AWS へ移行します。調査の結果、320… |
| [migration 問2](../../exercises/migration.md#q2) | 4.1.1 | これまで AWS の移行サービスを使ったことがない企業が、900 台の VMware と物理サーバー… |
| [migration 問3](../../exercises/migration.md#q3) | 4.1.1 | ある企業の CFO は、800 台の x86 サーバーを AWS に移した場合の費用を、取締役会で説… |
| [migration 問4](../../exercises/migration.md#q4) | 4.1.1 | 移行ウェーブを計画しています。勤怠システムは他のシステムに依存せず、止まっても影響は小さいです。受注… |
| [migration 問5](../../exercises/migration.md#q5) | 4.1.2 | AWS Transform MGN で移行を始めました。元のサーバーにエージェントを入れると、コンソ… |
| [migration 問6](../../exercises/migration.md#q6) | 4.1.2 | 小売企業が、物理サーバーと VMware 上の 180 台の Windows と Linux を A… |
| [migration 問7](../../exercises/migration.md#q7) | 4.1.2 | 金融系の企業が 600 台の VM を AWS へ移します。VMware Cloud Foundat… |
| [migration 問8](../../exercises/migration.md#q8) | 4.1.2 | MGN で 200 台を移行中です。すでに登録した 3 台は書き込みが多く、複製が遅れています。担当… |
| [migration 問9](../../exercises/migration.md#q9) | 4.1.3 | オンプレミスの Oracle Database を、ライセンス費用を減らすために Aurora Po… |
| [migration 問10](../../exercises/migration.md#q10) | 4.1.3 | RDS for MySQL をソースに、DMS の full-load-and-cdc タスクで移行… |
| [migration 問11](../../exercises/migration.md#q11) | 4.1.3 | 稼働中の NAS にある 400 TB のファイルを、30 日以内に S3 へ移します。回線は 1 … |
| [migration 問12](../../exercises/migration.md#q12) | 4.1.3 | Direct Connect の 10 Gbps を確保し、DataSync で 2 PB のファイ… |
| [migration 問13](../../exercises/migration.md#q13) | 4.1.3 | DMS で文書管理のデータベースを移行しました。表には最大 2 MB の LOB 列があります。タス… |
| [migration 問14](../../exercises/migration.md#q14) | 4.1.4 | EC2 上で PostgreSQL を 2 つ運用しています。パッチ、バックアップ、フェイルオーバー… |
| [migration 問15](../../exercises/migration.md#q15) | 4.1.4 | EC2 に Docker を直接入れて 12 のコンテナを動かしています。ホストのパッチと台数の調整… |
| [migration 問16](../../exercises/migration.md#q16) | 4.1.4 | 1 台の EC2 で 30 個の定期実行スクリプトを動かしています。常時起動の費用と、OS の管理を… |
| [migration 問17](../../exercises/migration.md#q17) | 4.1.5 | EC サイトのモノリスをマイクロサービスへ移します。機能は 40 以上あり、売上を止めるわけにはいき… |
| [migration 問18](../../exercises/migration.md#q18) | 4.1.5 | モノリスから「ユーザー」の機能をマイクロサービスへ切り出しました。新しいサービスの項目名と形式は、モ… |
| [migration 問19](../../exercises/migration.md#q19) | 4.1.5 | 「カート」の機能をマイクロサービスへ切り出しましたが、モノリスと同じリレーショナルデータベースを使っ… |
| [migration 問20](../../exercises/migration.md#q20) | 4.1.5 | モノリスから最初に切り出す機能を 2 つ決めます。チームの経験は多くありません。候補は次のとおりです… |
| [migration 問21](../../exercises/migration.md#q21) | 4.1.6 | 日本の保険会社が、富士通 GS21 のメインフレームで動く COBOL のアプリを AWS でモダナ… |
| [migration 問22](../../exercises/migration.md#q22) | 4.1.6 | .NET Framework で作った業務アプリが 60 本あり、Windows Server のラ… |
| [migration 問23](../../exercises/migration.md#q23) | 4.1.6 | 商用データベースからオープンソース系への移行を検討しています。データベースは 150 個あり、ストア… |
| [migration 問24](../../exercises/migration.md#q24) | 4.1.6 | 古いオンプレミスのメッセージブローカーを廃止します。受注アプリ（Java）は JMS で Activ… |

<!-- questions:end -->

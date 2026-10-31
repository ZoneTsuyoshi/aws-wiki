# 分野3: ストレージとデータベースの費用

アクセスの頻度と保持の要件から、階層、ボリュームタイプ、キャパシティ、バックアップ、ログの扱いを決める判断を問います。最低保存期間のような制約が決め手になります。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [3.4.1](../../domain3.md#skill-3-4-1) | ストレージの階層化とライフサイクル |
| [3.4.2](../../domain3.md#skill-3-4-2) | ブロックストレージの費用 |
| [3.4.3](../../domain3.md#skill-3-4-3) | データベースのキャパシティモードと予約 |
| [3.4.4](../../domain3.md#skill-3-4-4) | 保持期間を最適化したバックアップと DR |
| [3.4.5](../../domain3.md#skill-3-4-5) | コストを抑えたオブザーバビリティ |

## 学習の順番 {#study-order}

1. [S3 のストレージ費用](../../../../services/cost-management.md#s3-cost)と[ストレージクラス](../../../../services/s3.md#storage-classes): 最低保存期間、最低課金サイズ、取り出し料を表で覚えます。
2. [ライフサイクル](../../../../services/s3.md#lifecycle): 移行の順序、古いバージョン、未完了のマルチパートを確認します。
3. [ライフサイクルとストレージクラス](../../../../services/storage.md#efs-lifecycle): EFS の既定と、Standard へ戻す設定を押さえます。
4. [EBS のボリュームタイプ](../../../../services/storage.md#ebs-volume-types)と[ボリュームの変更と AZ の制約](../../../../services/storage.md#ebs-modify): タイプの選択と、縮小できないことを確認します。
5. [キャパシティモードと RCU/WCU](../../../../services/dynamodb.md#capacity)と[テーブルクラス](../../../../services/dynamodb.md#table-classes): 負荷の形とストレージの割合で選びます。
6. [Aurora Serverless v2](../../../../services/databases.md#aurora-serverless-v2)と [Savings Plans](../../../../services/cost-management.md#savings-plans): 変動する負荷と、移行を見込む確約を確認します。
7. [バックアッププランとルール](../../../../services/resilience.md#backup-plans)、[スナップショット](../../../../services/storage.md#ebs-snapshots)、[4 つの DR 戦略](../../../../services/resilience.md#dr-strategies): 要件に合う保持と戦略を選びます。
8. [ログクラス](../../../../services/observability.md#log-classes)、[保持期間の設定](../../../../services/observability.md#log-retention)、[サンプリング](../../../../services/observability.md#xray-sampling): 監視の費用の原因ごとに対策を覚えます。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| Standard-IA、One Zone-IA の最低保存期間 | 30 日 | 早く消しても残りが課金される |
| Glacier Instant、Flexible の最低保存期間 | 90 日 | 次の移行の日にも影響 |
| Glacier Deep Archive の最低保存期間 | 180 日 | 最も安いが取り出しに時間がかかる |
| ライフサイクルの移行の既定 | 128 KB 未満は対象外 | Intelligent-Tiering も自動階層化しない |
| EFS の既定の移行 | 30 日で IA、90 日で Archive | 既定では Standard に戻らない |
| `gp3` の最大 IOPS | 80,000 | サイズと独立に設定 |
| `io2` Block Express の最大 IOPS | 256,000 | 重要なデータベース |
| Aurora I/O-Optimized の目安 | I/O が費用の 25% 以上 | Standard への変更はいつでも、逆は 30 日に 1 回 |
| DynamoDB Standard-IA の目安 | ストレージが処理費用の 50% 超 | リザーブドは使えない |
| AWS Backup のコールド | 最低 90 日 | 削除はコールドへ移す日 + 90 日以降 |
| EBS Snapshots Archive | 最大 75% 削減 | 90 日以上保存するもの |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| アクセスパターンが読めない | Intelligent-Tiering |
| 小さなオブジェクトが大量にある | まとめてから階層を下げる |
| 最新の量は一定なのに請求が増える | 古いバージョンと未完了のマルチパートを疑う |
| IOPS のために `gp2` を大きくしている | 小さい `gp3` に IOPS を設定し、データを移す |
| `io2` の性能が使われていない | `gp3` へ変更 |
| 順次の読み書きで、スループット重視 | `st1`。ルートには使えない |
| 24 時間一定の DynamoDB を長く使う | プロビジョンドとリザーブドキャパシティ |
| 複数のエンジンへの移行を見込む確約 | Database Savings Plans |
| 夜間にほぼ使わない検証用の Aurora | Serverless v2 の 0 ACU と自動一時停止 |
| EBS だけを単純に自動化 | Data Lifecycle Manager。追加料金なし |
| 長期の監査ログ | 保持は短く。サブスクリプションで S3 へ送り、Glacier へ |
| トレースの費用が高い | X-Ray のサンプリングルール |

## 引っかかりやすい点 {#traps}

- 1 つのライフサイクルのルールでは、最低保存期間より前の次の移行を指定できません。
- EBS の容量は縮小できません。新しいボリュームへ移します。
- Savings Plans は EBS に適用されません。
- リザーブドキャパシティは、オンデマンドと Standard-IA のテーブルでは使えません。
- ログクラスは作成後に変更できません。
- Essentials ではメトリクスフィルター、サブスクリプションフィルター、EMF が使えません。
- ログクラスの料金の差は取り込みだけです。保管の単価は同じです。
- ディメンションに `RequestId` のような値を入れると、カスタムメトリクスの数が大きく増えます。
- EBS スナップショットをアーカイブすると、完全なスナップショットに変換されます。使う前に復元が必要です。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [storage-db-cost 問1](../../exercises/storage-db-cost.md#q1) | 3.4.1 | ある会社は、利用者がアップロードした資料を S3 に保管しています。オブジェクトは 1 MB 以上で… |
| [storage-db-cost 問2](../../exercises/storage-db-cost.md#q2) | 3.4.1 | あるサービスは、1 件 40 KB のログを S3 に毎日大量に保存しています。総数は 200 億件… |
| [storage-db-cost 問3](../../exercises/storage-db-cost.md#q3) | 3.4.1 | ある病院は、画像を 30 日間は S3 Standard に置き、その後 Glacier Insta… |
| [storage-db-cost 問4](../../exercises/storage-db-cost.md#q4) | 3.4.1 | ある会社の S3 バケットは、最新のオブジェクトの量が安定しているのに、請求額が増え続けています。バ… |
| [storage-db-cost 問5](../../exercises/storage-db-cost.md#q5) | 3.4.1 | あるチームは、多数の小さなファイルを持つ EFS を使っています。多くのファイルは 1 か月以上読ま… |
| [storage-db-cost 問6](../../exercises/storage-db-cost.md#q6) | 3.4.2 | あるデータベースサーバーは、9,000 IOPS を得るために 3 TiB の gp2 ボリュームを… |
| [storage-db-cost 問7](../../exercises/storage-db-cost.md#q7) | 3.4.2 | ある会社では、多くの業務システムに io2 Block Express を 30,000 IOPS … |
| [storage-db-cost 問8](../../exercises/storage-db-cost.md#q8) | 3.4.2 | ある分析基盤は、ログの大きなファイルを毎日順に読み書きしています。データは 12 TiB で、IOP… |
| [storage-db-cost 問9](../../exercises/storage-db-cost.md#q9) | 3.4.3 | ある Aurora PostgreSQL のクラスターは I/O が多く、請求の内訳では I/O が… |
| [storage-db-cost 問10](../../exercises/storage-db-cost.md#q10) | 3.4.3 | ある会社は、RDS for PostgreSQL を今後 1 年で段階的に Aurora へ移し、一… |
| [storage-db-cost 問11](../../exercises/storage-db-cost.md#q11) | 3.4.3 | ある DynamoDB のテーブルは、24 時間ほぼ一定のトラフィックで、今後も 2 年以上続く見込… |
| [storage-db-cost 問12](../../exercises/storage-db-cost.md#q12) | 3.4.3 | ある EC サイトは、DynamoDB に過去 10 年の注文履歴を保存しています。読み書きは少なく… |
| [storage-db-cost 問13](../../exercises/storage-db-cost.md#q13) | 3.4.3 | ある会社の検証環境の Aurora は、平日の日中だけ使われ、夜間と週末はほぼ接続がありません。日中… |
| [storage-db-cost 問14](../../exercises/storage-db-cost.md#q14) | 3.4.4 | ある会社は、AWS Backup で EFS のバックアップを取っています。コンプライアンスの要件は… |
| [storage-db-cost 問15](../../exercises/storage-db-cost.md#q15) | 3.4.4 | ある小さなチームは、EBS ボリュームのスナップショットを 1 つのアカウントで定期的に取り、14 … |
| [storage-db-cost 問16](../../exercises/storage-db-cost.md#q16) | 3.4.4 | ある会社は、月次の EBS スナップショットを監査のために 7 年保持しています。読むことはほとんど… |
| [storage-db-cost 問17](../../exercises/storage-db-cost.md#q17) | 3.4.4 | ある業務システムの DR は、別のリージョンでウォームスタンバイを常時稼働させています。事業部門と見… |
| [storage-db-cost 問18](../../exercises/storage-db-cost.md#q18) | 3.4.5 | ある会社のアプリは、調査のときにだけ読むデバッグログを大量に CloudWatch Logs へ送っ… |
| [storage-db-cost 問19](../../exercises/storage-db-cost.md#q19) | 3.4.5 | ある金融機関は、アプリのログを継続的に長期保存する必要があります。調査で使うのは直近の 30 日だけ… |
| [storage-db-cost 問20](../../exercises/storage-db-cost.md#q20) | 3.4.5 | あるチームは、リクエスト単位の遅延をカスタムメトリクスで送っており、ディメンションに Request… |
| [storage-db-cost 問21](../../exercises/storage-db-cost.md#q21) | 3.4.5 | ある高トラフィックの API は、ADOT で X-Ray へトレースを送っており、費用が想定を超え… |

<!-- questions:end -->

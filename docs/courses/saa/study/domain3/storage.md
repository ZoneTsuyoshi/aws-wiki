# 分野3: ストレージの性能と拡張

EBS のタイプと S3 の性能の設定、容量の増やし方を扱います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [ストレージの種類とサービス](../../domain3.md#t3-1-types) | ストレージサービスの適切な用途、ストレージの種類と特徴 |
| [性能の要求に合う設定](../../domain3.md#t3-1-performance) | 性能の要求を満たすストレージサービスと設定の判断 |
| [将来の増加に対応できるストレージ](../../domain3.md#t3-1-scale) | 将来の需要に対応してスケールできるストレージサービスの判断 |

## 学習の順番 {#study-order}

1. [FSx の選び方](../../../../services/storage-advanced.md#fsx-selection)と[インスタンスストア](../../../../services/storage-advanced.md#instance-store): ファイルの要件ごとのサービスと、最小の遅延の選択を確認します。
2. [EBS のボリュームタイプ](../../../../services/storage.md#ebs-volume-types)と[IOPS とスループットの設定](../../../../services/storage.md#ebs-performance-settings): `gp3` と `io2` の値を覚えます。
3. [リクエストレートとプレフィックス](../../../../services/s3.md#request-rate)と[マルチパートアップロード](../../../../services/s3.md#multipart-upload): プレフィックスとマルチパートの効果を押さえます。
4. [Transfer Acceleration](../../../../services/s3.md#transfer-acceleration)と[スループットモード](../../../../services/storage.md#efs-throughput-mode): 遠距離のアップロードと EFS のモードを確認します。
5. [ボリュームの変更と AZ の制約](../../../../services/storage.md#ebs-modify)と[基本と整合性](../../../../services/s3.md#basics): 容量の増やし方の違いを比べます。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| `gp3` | 基準 3,000 IOPS、125 MiB/s。最大 80,000 IOPS、2,000 MiB/s | 容量と性能を別に設定できる |
| `io2` Block Express | 最大 256,000 IOPS、4,000 MiB/s | 重要な DB |
| `st1`、`sc1` | 最大 500、250 IOPS | ブート不可 |
| S3 のプレフィックス | 書き込み毎秒 3,500、読み取り毎秒 5,500 以上 | 分けて並列にする |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 容量はそのまま IOPS だけ増やす | `gp3` に変更 |
| Windows の共有と NTFS の ACL | FSx for Windows File Server |
| iSCSI と複数のプロトコル | FSx for NetApp ONTAP |
| S3 のデータを高速に並列処理 | FSx for Lustre |
| S3 への遠距離のアップロード | Transfer Acceleration とマルチパート |
| 容量の増加が読めない共有 | EFS |

## 引っかかりやすい点 {#traps}

- EBS は増やせますが減らせません。OS 側のファイルシステムの拡張も必要です。
- `gp2` は容量に比例して IOPS が増えます。容量を買う必要はありません。
- HDD は DB のランダムアクセスに向きません。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [storage 問7](../../exercises/storage.md#q7) | ストレージの種類 | Windows のアプリのファイル共有を移します。SMB と NTFS の ACL、AD の連携が必… |
| [storage 問8](../../exercises/storage.md#q8) | ストレージの種類 | iSCSI のブロックと NFS、SMB を同じストレージで提供し、スナップショットやデータの階層化… |
| [storage 問9](../../exercises/storage.md#q9) | ストレージの種類 | 最小の遅延のディスクが必要な一時ファイルの処理です。データは消えても再作成できます。どれを選びますか… |
| [storage 問10](../../exercises/storage.md#q10) | 性能の要求に合う設定 | EC2 の DB が 100 GiB の gp2 で動いていて、IOPS が 6,000 必要です。… |
| [storage 問11](../../exercises/storage.md#q11) | 性能の要求に合う設定 | gp3 の性能について正しいものはどれですか。 |
| [storage 問12](../../exercises/storage.md#q12) | 性能の要求に合う設定 | 重要なトランザクションの DB に 100,000 IOPS を超える性能と、サブミリ秒の遅延が要り… |
| [storage 問13](../../exercises/storage.md#q13) | 性能の要求に合う設定 | 1 つのプレフィックスに書き込みが集中し、S3 が 503 を返します。性能を上げる方法はどれですか… |
| [storage 問14](../../exercises/storage.md#q14) | 性能の要求に合う設定 | 世界中の拠点から 1 つの東京のバケットへ大きなファイルをアップロードします。遠距離で遅く、失敗も多… |
| [storage 問15](../../exercises/storage.md#q15) | 将来の増加 | ログの容量の増え方が読めず、複数の Linux サーバーで共有します。容量の管理はしたくありません。… |
| [storage 問16](../../exercises/storage.md#q16) | 将来の増加 | 使用中の EBS ボリュームの容量が足りません。ダウンタイムなしで増やします。手順はどれですか。 |
| [storage 問17](../../exercises/storage.md#q17) | 将来の増加 | データ量が 10 倍になる見込みです。追加の作業なしで増えるストレージを選んでください。（2つ選択） |

<!-- questions:end -->

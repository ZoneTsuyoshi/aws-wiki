# 分野1: EBS と共有ストレージ

EBS のメトリクスとボリュームタイプ、共有ストレージの選択を問います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [1.3.2](../../domain1.md#skill-1-3-2) | EBS の性能とボリュームタイプ |
| [1.3.4](../../domain1.md#skill-1-3-4) | 共有ストレージの選択と最適化 |

## 学習の順番 {#study-order}

1. [EBS のボリュームタイプ](../../../../services/storage.md#ebs-volume-types)と[IOPS とスループットの設定](../../../../services/storage.md#ebs-performance-settings): タイプと IOPS の決まり方を確認します。
2. [ボリュームの変更と AZ の制約](../../../../services/storage.md#ebs-modify)と[スナップショット](../../../../services/storage.md#ebs-snapshots): 変更の制限と AZ の移動を覚えます。
3. [比較](../../../../services/storage.md#comparison)と[FSx の選び方](../../../../services/storage-advanced.md#fsx-selection): 要件からストレージを選びます。
4. [スループットモード](../../../../services/storage.md#efs-throughput-mode)と[ライフサイクルとストレージクラス](../../../../services/storage.md#efs-lifecycle): Elastic と Bursting、ライフサイクルの既定を確認します。
5. [ストレージ階層と階層化ポリシー](../../../../services/storage-advanced.md#fsx-ontap-tiering)と[S3 Files](../../../../services/storage-advanced.md#s3-files): 費用を下げる設定を確認します。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| `gp3` の基準 | 3,000 IOPS、125 MiB/s | サイズと独立に決める |
| `gp2` | 3 IOPS/GiB | `BurstBalance` が尽きると落ちる |
| `io2` Block Express | 最大 256,000 IOPS | 高い IOPS と低遅延 |
| Elastic Volumes | 24 時間で 4 回 | サイズは増やすだけ |
| EFS のライフサイクルの既定 | 30 日で IA、90 日で Archive | 「初回アクセス時」で Standard へ戻る |
| S3 Files | しきい値 128 KiB 未満、期限 30 日 | いずれも既定値。1 MiB 以上の読み取りは S3 から直接読む |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| `BurstBalance` が 0 に近い | `gp3` へ変更して IOPS を指定 |
| `InstanceEBSIOPSExceededCheck` が `1` | 大きいインスタンスタイプへ |
| サイズを増やしたのに容量が同じ | OS でファイルシステムを拡張 |
| スナップショットからの初回の読み取りが遅い | Fast Snapshot Restore |
| Windows の共有、NTFS の ACL、AD | FSx for Windows File Server |
| S3 のデータを高速に並列処理 | FSx for Lustre |
| NFS、SMB、iSCSI を同時に使う | FSx for NetApp ONTAP |

## 引っかかりやすい点 {#traps}

- `st1` と `sc1` はブートに使えません。
- FSx for OpenZFS はこのコースの対象外です。
- FSx File Gateway は新規受付を終了しています。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [storage 問1](../../exercises/storage.md#q1) | 1.3.2 | 100 GiB の gp2 のデータベースのボリュームが昼だけ遅くなります。BurstBalance… |
| [storage 問2](../../exercises/storage.md#q2) | 1.3.2 | gp3 のボリュームで VolumeIOPSExceededCheck は 0 のままですが、Ins… |
| [storage 問3](../../exercises/storage.md#q3) | 1.3.2 | EBS のボリュームのサイズを増やす変更が完了しましたが、OS から見える容量が変わりません。何をし… |
| [storage 問4](../../exercises/storage.md#q4) | 1.3.2 | EBS の Elastic Volumes について正しいものを選んでください。（2つ選択） |
| [storage 問5](../../exercises/storage.md#q5) | 1.3.2 | スナップショットから作ったボリュームで、最初の読み取りが遅くなります。本番の切り替えの直後から性能を… |
| [storage 問6](../../exercises/storage.md#q6) | 1.3.2 | 次の要件に合う EBS を選びます。ログの順次読み取りが中心の大きなデータを扱い、最小の費用ではなく… |
| [storage 問7](../../exercises/storage.md#q7) | 1.3.4 | Windows のアプリケーションで、SMB の共有フォルダと NTFS の ACL が必要です。A… |
| [storage 問8](../../exercises/storage.md#q8) | 1.3.4 | S3 にある数百 TB のデータを、ML の学習で多数のノードから高速に並列で読みたいと考えています… |
| [storage 問9](../../exercises/storage.md#q9) | 1.3.4 | オンプレミスの NetApp から移行します。NFS、SMB、iSCSI を同時に使い、アクセスの少… |
| [storage 問10](../../exercises/storage.md#q10) | 1.3.4 | Linux の複数台で共有する EFS で、負荷の予測がしにくいアプリケーションを動かします。スルー… |
| [storage 問11](../../exercises/storage.md#q11) | 1.3.4 | Bursting モードの EFS で、夕方から遅くなります。BurstCreditBalance … |
| [storage 問12](../../exercises/storage.md#q12) | 1.3.4 | EFS のライフサイクルを設定しました。ほとんど読まれないファイルの費用を下げつつ、アクセスがあった… |
| [storage 問13](../../exercises/storage.md#q13) | 1.3.4 | 正本は S3 に置いたまま、ファイルシステムとして共有したいと考えています。読まれないデータの高性能… |

<!-- questions:end -->

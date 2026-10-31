# 分野3: ハイブリッドストレージとデータ転送

使い続けるなら Storage Gateway、移すなら DataSync という区別が中心です。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [ハイブリッドストレージ](../../domain3.md#t3-1-hybrid) | 業務要件を満たすハイブリッドストレージ |
| [データ転送](../../domain3.md#t3-5-transfer) | データ転送サービスの適切な用途、データ転送ソリューションの設計 |

## 学習の順番 {#study-order}

1. [AWS Storage Gateway](../../../../services/migration.md#storage-gateway): 3 つのタイプとプロトコルを表で覚えます。
2. [AWS DataSync](../../../../services/migration.md#datasync)と[サービスの比較](../../../../services/migration.md#transfer-comparison): 転送のサービスの違いを比べます。
3. [AWS Transfer Family](../../../../services/migration.md#transfer-family)と[AWS Data Exchange](../../../../services/data-engineering.md#data-exchange): 取引先の受け渡しと、第三者のデータを確認します。

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| NFS で書き、S3 で分析する | S3 File Gateway |
| 頻繁に使う部分だけローカルに | Volume Gateway のキャッシュ型 |
| 全データに低遅延でアクセスする | Volume Gateway の保管型 |
| バックアップソフトを変えずにテープをやめる | Tape Gateway |
| NAS を移し、差分を同期する | DataSync |
| 取引先の SFTP を変えない | Transfer Family |

## 引っかかりやすい点 {#traps}

- FSx File Gateway は新規受付を終了しました。
- 1 回の移行に Storage Gateway を選ぶ選択肢は誤りです。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [migration 問1](../../exercises/migration.md#q1) | ハイブリッドストレージ | オンプレミスのアプリが NFS でファイルを書き、クラウド側ではそのファイルを S3 のオブジェクト… |
| [migration 問2](../../exercises/migration.md#q2) | ハイブリッドストレージ | オンプレミスのストレージの容量は増やさず、頻繁に使うデータだけをローカルに置いて iSCSI で使い… |
| [migration 問3](../../exercises/migration.md#q3) | ハイブリッドストレージ | 既存のバックアップソフトをそのまま使い、物理テープをやめます。どれを選びますか。 |
| [migration 問4](../../exercises/migration.md#q4) | データ転送 | NAS の 50 TB を S3 に移し、切り替えまで毎週差分を同期します。帯域の制限やスケジュール… |
| [migration 問5](../../exercises/migration.md#q5) | データ転送 | 取引先が今の SFTP の手順を変えずにファイルを送り、S3 に保存します。どれを選びますか。 |
| [migration 問6](../../exercises/migration.md#q6) | データ転送 | 第三者の市場データのセットを購読し、更新を AWS で受け取ります。どれを使いますか。 |

<!-- questions:end -->

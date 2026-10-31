# 分野4: データとスキーマの移行

転送の日数を計算してから、最も安い方法を選びます。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [データの移行とハイブリッド](../../domain4.md#t4-1-transfer) | ハイブリッドストレージの選択肢、ワークロードのデータを AWS ストレージへ転送する最も安い方法の判断、ストレージサービスへのデータ移行に適したサービスの選択 |
| [スキーマとデータの移行](../../domain4.md#t4-3-migration) | 別の場所や別のエンジンへのスキーマとデータの移行 |

## 学習の順番 {#study-order}

1. [計算式](../../../../services/migration.md#transfer-formula)と[転送方法の選び方と時間の計算](../../../../services/migration.md#choosing-transfer): 計算式と選び方を確認します。
2. [AWS DataSync](../../../../services/migration.md#datasync)と[AWS Transform MGN(旧 Application Migration Service)](../../../../services/migration.md#mgn): ファイルとサーバーの移行を区別します。
3. [AWS Data Transfer Terminal](../../../../services/migration.md#data-transfer-terminal)と[Snow Family の現在の状況](../../../../services/migration.md#snow-family): 回線に乗らないときの現在の選択肢を確認します。
4. [AWS SCT と DMS Schema Conversion](../../../../services/migration.md#sct)と[移行タイプ](../../../../services/migration.md#dms-migration-types): スキーマとデータの役割を分けます。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| 1 Gbps、利用率 80%、24 時間 | 100 TB が約 12 日 | 比例で計算する |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 既存の回線で間に合う | DataSync |
| 1 回だけ、回線が足りない | 期間限定の Direct Connect と DataSync |
| サーバーを EC2 へ移す | Application Migration Service |
| 異種間の DB | SCT か DMS Schema Conversion と DMS |
| 停止を最小にする DB の移行 | `full-load-and-cdc` |

## 引っかかりやすい点 {#traps}

- Snow Family は新規のお客様に提供されません。試験では「回線が細く、オフラインで転送する」という役割で覚えます。
- DMS だけではストアドプロシージャを変換できません。
- インターネットからの受信の転送料はかかりません。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [migration 問7](../../exercises/migration.md#q7) | データの移行 | 1 Gbps の回線を利用率 80% で 24 時間使うとき、100 TB の転送にかかる日数はおよ… |
| [migration 問8](../../exercises/migration.md#q8) | データの移行 | 既存の回線で期限内に転送できることを計算で確かめました。ファイルサーバーを最も安く EFS に移しま… |
| [migration 問9](../../exercises/migration.md#q9) | データの移行 | 期限に間に合わず、回線の増強はできます。データは 1 回だけ移します。最も費用を抑える選択はどれです… |
| [migration 問10](../../exercises/migration.md#q10) | データの移行 | 新規の顧客が、回線に乗らない数百 TB を移します。Snow Family は新規のお客様に提供され… |
| [migration 問11](../../exercises/migration.md#q11) | データの移行 | オンプレミスのサーバーをブロック単位で継続して複製し、短い停止で EC2 に移します。どれを選びます… |
| [migration 問12](../../exercises/migration.md#q12) | スキーマの移行 | Oracle から Aurora PostgreSQL へ移します。ストアドプロシージャも変換します… |
| [migration 問13](../../exercises/migration.md#q13) | スキーマの移行 | オンプレミスの MySQL を Aurora MySQL へ、停止を最小にして移します。どの設定です… |
| [migration 問14](../../exercises/migration.md#q14) | スキーマの移行 | RDS の DB を別のリージョンへ移します。スナップショットを使う以外の方法として適切なものはどれ… |

<!-- questions:end -->

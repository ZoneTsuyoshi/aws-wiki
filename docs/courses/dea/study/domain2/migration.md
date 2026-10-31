# 分野2: 移行とスキーマ変換

移行のツールの選択と、スキーマの変換を問います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [2.1.4](../../domain2.md#skill-2-1-4) | 移行ツールの組み込み |
| [2.4.3](../../domain2.md#skill-2-4-3) | スキーマの変換 |

## 学習の順番 {#study-order}

1. [転送方法の比較](../../../../services/migration.md#transfer-comparison): 対象とプロトコルで選びます。
2. [Transfer Family](../../../../services/migration.md#transfer-family): 公開エンドポイントの制限を確認します。
3. [DataSync](../../../../services/migration.md#datasync): 定期的な転送を確認します。
4. [DMS](../../../../services/migration.md#dms): 全件と CDC を確認します。
5. [SCT と DMS Schema Conversion](../../../../services/migration.md#sct): 違いと評価レポートを覚えます。

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 取引先の SFTP をそのまま受ける | Transfer Family |
| NFS、SMB から S3 へ定期的に転送する | DataSync |
| データベースの全件と変更を複製する | DMS |
| Oracle から Aurora PostgreSQL へ | スキーマ変換の後に DMS |
| Netezza から Redshift へ | SCT とデータ抽出エージェント |
| ターゲットがない段階で評価する | DMS Schema Conversion の仮想ターゲット |

## 引っかかりやすい点 {#traps}

- 変換ツールはスキーマとコードだけを扱い、データは移しません。
- Snow Family は新規のお客様に提供されません。
- 同種の移行にスキーマの変換は要りません。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [migration 問1](../../exercises/migration.md#q1) | 2.1.4 | 取引先は今の SFTP クライアントを変えられません。受け取ったファイルは S3 に保存し、到着で … |
| [migration 問2](../../exercises/migration.md#q2) | 2.1.4 | オンプレミスの NFS の 50 TB を S3 へ移し、その後も毎晩差分を転送します。回線の帯域は… |
| [migration 問3](../../exercises/migration.md#q3) | 2.1.4 | 回線に乗らない規模のデータをオフラインで運びます。転送サービスの現在の状況として正しいものはどれです… |
| [migration 問4](../../exercises/migration.md#q4) | 2.1.4 | 移行のツールの選択で正しいものはどれですか。（2つ選択） |
| [migration 問5](../../exercises/migration.md#q5) | 2.1.4 | Transfer Family の公開エンドポイントについて正しいものはどれですか。 |
| [migration 問6](../../exercises/migration.md#q6) | 2.4.3 | Oracle から Aurora PostgreSQL へ移ります。スキーマとコードの変換は誰が担い… |
| [migration 問7](../../exercises/migration.md#q7) | 2.4.3 | MySQL から Aurora MySQL へ移ります。スキーマの変換のツールはどう扱いますか。 |
| [migration 問8](../../exercises/migration.md#q8) | 2.4.3 | Netezza の DWH を Redshift へ移します。データの抽出も含め、分散キーの提案も受… |
| [migration 問9](../../exercises/migration.md#q9) | 2.4.3 | 変換のターゲットのデータベースがまだない段階で、移行の難しさを評価します。DMS Schema Co… |
| [migration 問10](../../exercises/migration.md#q10) | 2.4.3 | AWS SCT と DMS Schema Conversion の違いとして正しいものはどれですか。… |

<!-- questions:end -->

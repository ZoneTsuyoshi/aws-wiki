# 分野1: バッチ取り込みと接続

バッチのソースの読み方、取り込みの設定値、接続元の制限と Glue の接続を問います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [1.1.2](../../domain1.md#skill-1-1-2) | バッチソースの読み取り |
| [1.1.3](../../domain1.md#skill-1-1-3) | バッチ取り込みの設定 |
| [1.1.8](../../domain1.md#skill-1-1-8) | 接続元 IP アドレスの許可リスト |
| [1.2.2](../../domain1.md#skill-1-2-2) | データソースへの接続（JDBC、ODBC） |

## 学習の順番 {#study-order}

1. [ジョブのブックマーク](../../../../services/data-engineering.md#glue-bookmarks): 新しいデータだけ読む仕組みと症状を確認します。
2. [DPU とワーカータイプ](../../../../services/data-engineering.md#glue-dpu): `groupFiles` と OOM の関係を押さえます。
3. [COPY と UNLOAD](../../../../services/data-engineering.md#redshift-copy): マニフェスト、`MAXERROR`、ファイル分割を覚えます。
4. [DMS の移行タイプ](../../../../services/migration.md#dms-migration-types): 全件ロードと CDC を区別します。
5. [NAT と Elastic IP](../../../../services/network-connectivity.md#nat-eip): 固定の出口の作り方を確認します。
6. [セキュリティグループのルール](../../../../services/networking.md#security-group-rules): 自己参照のルールを理解します。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| ブックマークの既定 | 無効 | `job-bookmark-enable` で有効 |
| `groupFiles` の自動有効 | ファイル 50,000 個超 | 小さなファイルが多いとき |
| `MAXERROR` | 既定 0、上限 100,000 | 1 行の不良で失敗 |
| マニフェストの `mandatory` | 既定 `false` | 欠けても失敗しない |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| SaaS をコードなしで定期的に取り込む | AppFlow |
| 短い停止でデータベースを移す | DMS の全件ロードと CDC |
| Redshift の結果を S3 へ出す | `UNLOAD` |
| VPC 内の Glue から社外の API へ接続する | NAT ゲートウェイの Elastic IP を許可リストへ |
| VPC エンドポイント経由のバケット制限 | `aws:SourceVpce` |
| Glue から VPC 内の RDS へ接続する | 自己参照ルール、S3 への経路、データベースのポート |

## 引っかかりやすい点 {#traps}

- 1 回の `COPY` で複数ファイルを読みます。同時に複数の `COPY` を実行すると直列になります。
- Transfer Family の公開エンドポイントはセキュリティグループで制限できません。
- ブックマークは同時実行に対応していません。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [ingestion 問1](../../exercises/ingestion.md#q1) | 1.1.2 | 営業部門は Salesforce のデータを毎晩 S3 へ増分で取り込みたいです。開発者はおらず、コ… |
| [ingestion 問2](../../exercises/ingestion.md#q2) | 1.1.2 | オンプレミスの PostgreSQL 10 TB を Aurora へ移します。切り替えまでの間に発… |
| [ingestion 問3](../../exercises/ingestion.md#q3) | 1.1.2 | Redshift の集計結果を、SaaS の連携先が読む S3 へ毎日 CSV 以外の列指向形式で渡… |
| [ingestion 問4](../../exercises/ingestion.md#q4) | 1.1.3 | 毎日実行する Glue ジョブが、S3 の全ファイルを読み直しています。新しく届いたファイルだけを処… |
| [ingestion 問5](../../exercises/ingestion.md#q5) | 1.1.3 | Glue ジョブが 1 KB 程度のファイル数十万個を読むとき、ドライバーが OOM で失敗します。… |
| [ingestion 問6](../../exercises/ingestion.md#q6) | 1.1.3 | 夜間の COPY で、前日のファイルのうち 1 つが欠けていても成功してしまいました。指定したファイ… |
| [ingestion 問7](../../exercises/ingestion.md#q7) | 1.1.3 | 16 スライスのクラスターへ 1 つの大きな gzip ファイルを COPY すると遅いです。ロード… |
| [ingestion 問8](../../exercises/ingestion.md#q8) | 1.1.8 | VPC 内の Glue ジョブから取引先の API を呼びます。取引先は接続元 IP の許可リストを… |
| [ingestion 問9](../../exercises/ingestion.md#q9) | 1.1.8 | SFTP で S3 へ納品する取引先を、接続元 IP で制限します。Transfer Family … |
| [ingestion 問10](../../exercises/ingestion.md#q10) | 1.1.8 | バケットポリシーの aws:SourceIp で社内の CIDR だけ許可しました。VPC の S3… |
| [ingestion 問11](../../exercises/ingestion.md#q11) | 1.2.2 | VPC 内の RDS を読む Glue ジョブが、接続テストで失敗します。ジョブのセキュリティグルー… |
| [ingestion 問12](../../exercises/ingestion.md#q12) | 1.2.2 | JDBC の Glue ジョブを、インターネットへの経路のないプライベートサブネットで動かします。ス… |
| [ingestion 問13](../../exercises/ingestion.md#q13) | 1.2.2 | BI ツールと Java のレポートアプリから、Athena と Redshift へ接続します。ど… |

<!-- questions:end -->

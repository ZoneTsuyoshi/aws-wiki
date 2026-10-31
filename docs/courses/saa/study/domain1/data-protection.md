# 分野1: データの保護

公開の防止、保持、分類、復旧を組み合わせて考えます。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [データアクセスとガバナンス](../../domain1.md#t1-3-governance) | データアクセスとガバナンス、データのアクセス、ライフサイクル、保護のポリシーの実装 |
| [データの保持と分類](../../domain1.md#t1-3-classification) | データの保持と分類 |
| [データの復旧、バックアップ、レプリケーション](../../domain1.md#t1-3-backup) | データの復旧、データのバックアップとレプリケーションの実装 |

## 学習の順番 {#study-order}

1. [ブロックパブリックアクセス](../../../../services/s3.md#block-public-access)と[イベントの種類](../../../../services/observability.md#cloudtrail-events): 公開の防止と、オブジェクトの操作の記録を確認します。
2. [AWS Lake Formation](../../../../services/data-engineering.md#lake-formation): 列と行の権限の置き場所を押さえます。
3. [バージョニング](../../../../services/s3.md#versioning)と[Object Lock](../../../../services/s3.md#object-lock): 誤削除からの復旧と、削除の禁止を区別します。
4. [Vault Lock](../../../../services/resilience.md#vault-lock)と[タグ戦略](../../../../services/governance.md#tagging-strategy): バックアップの保護と、タグによる分類を確認します。
5. [レプリケーション](../../../../services/s3.md#replication)と[AWS Backup](../../../../services/resilience.md#backup): 複製とバックアップの違いを理解します。
6. [バックアップと復元](../../../../services/dynamodb.md#backup)と[アカウント間コピーと組織での管理](../../../../services/resilience.md#backup-cross-account): 時点復旧と、アカウント間コピーを確認します。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| RDS の自動バックアップ | 0〜35 日 | 長期には手動スナップショットか AWS Backup |
| DynamoDB の PITR | 1〜35 日 | 期間内の任意の時点に戻せる |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 組織で S3 の公開を防ぐ | ブロックパブリックアクセス |
| 誰がオブジェクトを読んだかを記録する | CloudTrail のデータイベント |
| ルートユーザーも含めて削除させない | Object Lock のコンプライアンスモード |
| 管理者だけは例外を残す | Object Lock のガバナンスモード |
| バックアップを誰にも消させない | AWS Backup の Vault Lock |
| 複数サービスのバックアップを一元管理する | AWS Backup |

## 引っかかりやすい点 {#traps}

- レプリケーションは破損や誤った上書きも複製します。
- CloudTrail のデータイベントは既定で記録されません。
- S3 のレプリケーションは両方のバケットでバージョニングが必須です。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [data-protection 問1](../../exercises/data-protection.md#q1) | データガバナンス | 組織の全アカウントで、S3 バケットが誤って公開されることを防ぎます。最も適切なものはどれですか。 |
| [data-protection 問2](../../exercises/data-protection.md#q2) | データガバナンス | 監査で「S3 のオブジェクトを誰が読んだか」を示せませんでした。CloudTrail の証跡はありま… |
| [data-protection 問3](../../exercises/data-protection.md#q3) | データガバナンス | データレイクの S3 のテーブルで、人事の列は一部の分析者だけに見せます。列と行の単位の権限を 1 … |
| [data-protection 問4](../../exercises/data-protection.md#q4) | データガバナンス | S3 バケットの次の要件を満たす組み合わせを選んでください。誤った削除から戻せること、古いバージョン… |
| [data-protection 問5](../../exercises/data-protection.md#q5) | 保持と分類 | 監査ログを 7 年間、ルートユーザーを含めて誰にも削除させません。正しい設定はどれですか。 |
| [data-protection 問6](../../exercises/data-protection.md#q6) | 保持と分類 | 機密度に応じて S3 のオブジェクトへのアクセスを制御します。ロールとオブジェクトの属性の一致で許可… |
| [data-protection 問7](../../exercises/data-protection.md#q7) | 保持と分類 | AWS Backup のバックアップを、ランサムウェアや管理者の誤操作でも保持期間の間は削除させませ… |
| [data-protection 問8](../../exercises/data-protection.md#q8) | データの復旧 | S3 のレプリケーションで別のリージョンに複製しています。破損したファイルの上書きからも復旧できるよ… |
| [data-protection 問9](../../exercises/data-protection.md#q9) | データの復旧 | 複数のサービス（EBS、RDS、DynamoDB、EFS）のバックアップを一元管理し、別のアカウント… |
| [data-protection 問10](../../exercises/data-protection.md#q10) | データの復旧 | DynamoDB のテーブルを、35 日以内の任意の秒の時点に戻せるようにします。何を有効にしますか… |
| [data-protection 問11](../../exercises/data-protection.md#q11) | データの復旧 | RDS の自動バックアップの説明として正しいものはどれですか。 |

<!-- questions:end -->

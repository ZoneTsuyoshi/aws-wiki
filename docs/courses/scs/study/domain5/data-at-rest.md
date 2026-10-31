# 分野5: 保存時のデータ

暗号化の方式と鍵のサービスの選択、改ざんの防止、保持、バックアップの保護を問います。費用と責任のトレードオフが判断の軸です。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [5.2.1](../../domain5.md#skill-5-2-1) | 保存時の暗号化の設計 |
| [5.2.2](../../domain5.md#skill-5-2-2) | データの完全性の保護 |
| [5.2.3](../../domain5.md#skill-5-2-3) | ライフサイクルと保持 |
| [5.2.4](../../domain5.md#skill-5-2-4) | レプリケーションとバックアップの安全な設計 |

## 学習の順番 {#study-order}

1. [S3 の暗号化オプション](../../../../services/kms.md#s3-encryption)と[クライアント側とサーバー側](../../../../services/kms.md#client-vs-server-side): 要件から方式を選びます。
2. [S3 バケットキー](../../../../services/s3.md#bucket-key)と [SSE-C の注意点](../../../../services/s3.md#sse-c): 暗号化コンテキストの変化と、2026 年の既定の変更を押さえます。
3. [KMS との比較](../../../../services/identity-directory.md#cloudhsm-vs-kms): CloudHSM を選ぶ条件を確認します。
4. [Object Lock](../../../../services/s3.md#object-lock): 2 つのモードとリーガルホールドを覚えます。
5. [Lambda のコード署名](../../../../services/lambda.md#code-signing)と[DataSync のタスク設定](../../../../services/migration.md#datasync-task-settings): コードと転送の完全性を確認します。
6. [S3 のライフサイクル](../../../../services/s3.md#lifecycle)、[EFS のライフサイクル](../../../../services/storage.md#efs-lifecycle)、[FSx のバックアップ](../../../../services/storage-advanced.md#fsx-protection): 保持の設定を確認します。
7. [EBS スナップショット](../../../../services/storage.md#ebs-snapshots)と [AWS Backup](../../../../services/resilience.md#backup): 自動化の範囲で使い分けます。
8. [Vault Lock](../../../../services/resilience.md#vault-lock)、[エアギャップのボールト](../../../../services/resilience.md#logically-air-gapped)、[アカウント間コピー](../../../../services/resilience.md#backup-cross-account): ランサムウェアへの備えを理解します。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| EFS のライフサイクルの既定 | 30 日で IA、90 日で Archive | 最終アクセスからの日数 |
| FSx for Lustre の自動バックアップ | 0〜90 日、既定 0 日 | S3 にリンクなしの Persistent だけ |
| AWS Backup の Vault Lock の猶予期間 | 3 日（72 時間）以上 | コンプライアンスモードは後で誰も解除できない |
| Glacier の Vault Lock の検証期間 | 24 時間 | 完了後は変更できない |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 2 層の暗号化 | DSSE-KMS。バケットキーは使えない |
| バケットキーの有効化の後に拒否が出る | 暗号化コンテキストがバケットの ARN に変わった |
| PKCS#11 と単一テナントの HSM | CloudHSM を 2 台以上 |
| AWS に平文を渡さない | クライアント側の暗号化 |
| ルートでも消せない保持 | Object Lock のコンプライアンスモード |
| 期限のない保全 | リーガルホールド |
| 未署名のコードのデプロイを止める | `UntrustedArtifactOnDeployment` を `Enforce` |
| ログの改ざんの証明 | CloudTrail のログファイルの検証 |
| 転送したファイルだけを照合 | `VerifyMode` を `ONLY_FILES_TRANSFERRED` |
| EBS だけを自動化 | Data Lifecycle Manager |
| アカウントごと奪われても復元 | 論理的にエアギャップされたボールトと RAM |

## 引っかかりやすい点 {#traps}

- ロックされたバージョンは、ライフサイクルの失効でも削除されません。費用もかかり続けます。
- コード署名は新しいデプロイを制御します。動いている未署名のコードは止まりません。
- Vault Lock の最小と最大の保持期間は、既存の復旧ポイントには適用されません。
- ガバナンスモードは権限があれば解除できます。
- AWS 管理キーで暗号化されたリソースのバックアップは、キーを共有できないのでアカウント間のコピーで問題になります。AWS Backup が完全に管理するリソースは例外です。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [data-at-rest 問1](../../exercises/data-at-rest.md#q1) | 5.2.1 | 規制の要件で、S3 のオブジェクトに 2 層の暗号化を適用し、鍵の利用を CloudTrail で監… |
| [data-at-rest 問2](../../exercises/data-at-rest.md#q2) | 5.2.1 | S3 の SSE-KMS の暗号化コンテキストをオブジェクトの ARN に限定する IAM 条件を、… |
| [data-at-rest 問3](../../exercises/data-at-rest.md#q3) | 5.2.1 | データベースベンダーの製品で TDE を使います。ベンダーの製品は PKCS#11 で鍵を扱う必要が… |
| [data-at-rest 問4](../../exercises/data-at-rest.md#q4) | 5.2.1 | ある会社は、S3 に保存する医療データを AWS に平文で渡さないことを求められています。処理は社内… |
| [data-at-rest 問5](../../exercises/data-at-rest.md#q5) | 5.2.2 | 金融の規制で、取引記録を 7 年間、ルートユーザーを含めて誰も削除できないようにします。また、別の訴… |
| [data-at-rest 問6](../../exercises/data-at-rest.md#q6) | 5.2.2 | Lambda 関数に AWS Signer の署名を必須にしました。コード署名の設定を関数に追加しま… |
| [data-at-rest 問7](../../exercises/data-at-rest.md#q7) | 5.2.2 | 監査人が「CloudTrail のログが配信後に変更または削除されていないこと」の証明を求めています… |
| [data-at-rest 問8](../../exercises/data-at-rest.md#q8) | 5.2.2 | オンプレミスの NAS から EFS へ DataSync で規制データを移行します。監査は「転送し… |
| [data-at-rest 問9](../../exercises/data-at-rest.md#q9) | 5.2.3 | ログのバケットにライフサイクルで「365 日後に削除」を設定しています。同じオブジェクトには Obj… |
| [data-at-rest 問10](../../exercises/data-at-rest.md#q10) | 5.2.3 | FSx for Lustre の Persistent ファイルシステムを S3 にリンクして使って… |
| [data-at-rest 問11](../../exercises/data-at-rest.md#q11) | 5.2.3 | 調査で EFS の費用が想定を超えていることが分かりました。アクセスの少ないファイルを安い階層に移し… |
| [data-at-rest 問12](../../exercises/data-at-rest.md#q12) | 5.2.4 | EBS スナップショットの作成、保持、削除だけを自動化します。別のリージョンへのコピーも必要です。E… |
| [data-at-rest 問13](../../exercises/data-at-rest.md#q13) | 5.2.4 | ランサムウェアで本番アカウントの管理者権限が奪われた場合でも、別のアカウントから復元できるようにしま… |
| [data-at-rest 問14](../../exercises/data-at-rest.md#q14) | 5.2.4 | AWS Backup の通常のボールトに Vault Lock を設定します。監査の要件で、猶予期間… |
| [data-at-rest 問15](../../exercises/data-at-rest.md#q15) | 5.2.4 | EBS ボリュームのバックアップを AWS Backup で別のアカウントへコピーしたところ、失敗し… |

<!-- questions:end -->

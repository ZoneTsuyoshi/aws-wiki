# 分野2: KMS

どの場所で、どのキーで暗号化するかの判断と、キーを実際に使うときの API と権限を問います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [2.2.1](../../domain2.md#skill-2-2-1) | 保存時と転送時の暗号化 |
| [2.2.3](../../domain2.md#skill-2-2-3) | クライアント側とサーバー側の選択 |
| [2.2.4](../../domain2.md#skill-2-2-4) | データキーと API の使い分け |

## 学習の順番 {#study-order}

1. [保存時と転送時の暗号化](../../../../services/kms.md#at-rest-in-transit): 別の対策であることと、サービスごとの既定を確認します。
2. [KMS キーの種類](../../../../services/kms.md#key-types): カスタマー管理キー、AWS 管理キー、AWS 所有キーの違いを表で覚えます。
3. [キーポリシー、IAM、グラント](../../../../services/kms.md#access-control): IAM だけでは使えない理由と、既定のキーポリシーの意味を理解します。
4. [主な API](../../../../services/kms.md#api-operations)と[エンベロープ暗号化](../../../../services/kms.md#envelope-encryption): 4 KB の上限と、データキーの流れをつかみます。
5. [暗号化コンテキスト](../../../../services/kms.md#encryption-context): 復号時の完全一致と、CloudTrail に平文で残ることを押さえます。
6. [クライアント側とサーバー側](../../../../services/kms.md#client-vs-server-side)と [AWS Encryption SDK](../../../../services/kms.md#encryption-sdk): 選ぶ基準と、SDK が代わりにしてくれることを確認します。
7. [アカウントをまたぐ暗号化](../../../../services/kms.md#cross-account)と[キーのローテーション](../../../../services/kms.md#key-rotation): 両側の許可、再暗号化されないことを覚えます。
8. [ThrottlingException とキャッシュ](../../../../services/kms.md#throttling)と[主なエラー](../../../../services/kms.md#kms-errors): 対処の順序とエラーの見分け方を確認します。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| `Encrypt` の平文（対称） | 4,096 バイト | 超えるならエンベロープ暗号化 |
| `Encrypt`（`RSA_2048` と `SHA_256`） | 190 バイト | 非対称はさらに小さい |
| `GenerateRandom` | 1〜1,024 バイト | キー不要 |
| 自動ローテーション | 既定 365 日。90〜2,560 日 | 対称のカスタマー管理キーが対象 |
| オンデマンドローテーション | キーあたり 25 回 | 自動の予定は変わらない |
| 削除の待機期間 | 既定 30 日。7〜30 日 | 待機中は `CancelKeyDeletion` |
| 対称キーの暗号操作 | 秒間 10,000 / 20,000 / 100,000 | 東京は 20,000。呼び出し側のアカウントに計上 |
| S3 バケットキー | KMS のコストを最大 99% 削減 | 既存のオブジェクトは対象外 |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 4 KB を超えるデータを暗号化する | `GenerateDataKey` でエンベロープ暗号化。AWS Encryption SDK を推奨 |
| 別のワーカーが後で使うデータキーを準備する | `GenerateDataKeyWithoutPlaintext` |
| 平文を見せずに別のキーへ切り替える | `ReEncrypt` |
| AWS にも平文を見せたくない | クライアント側暗号化（AWS Encryption SDK） |
| 誰がいつキーを使ったかを監査する | CloudTrail。AWS 管理キーの利用も記録される。キーポリシーまで自分で管理するならカスタマー管理キー |
| IAM で許可したのにキーを使えない | キーポリシーに IAM を有効にする文か主体の許可がない |
| 別アカウントのキーを使う | キーポリシーと IAM の両方で許可し、キー ARN か別名 ARN を指定する |
| 特定のサービス経由でだけキーを使わせる | `kms:ViaService`。値にリージョンを含める |
| `GenerateDataKey` で `ThrottlingException` | バックオフ、S3 バケットキー、データキーキャッシュ、上限の引き上げの順 |
| 外部システムに公開鍵だけを渡して暗号化させる | 非対称の RSA キー |

## 引っかかりやすい点 {#traps}

- 復号で `InvalidCiphertextException` が出ます。暗号化コンテキストが大文字小文字まで一致していないか、暗号文の破損です。
- ローテーションは既存のデータを再暗号化しません。古い鍵素材が保持されるので、古い暗号文はそのまま復号できます。
- 別アカウントのキーを `alias/app-key` で指定すると、自分のアカウントの別名を探して `NotFoundException` になります。
- AWS 管理キーのポリシーは変更できず、共有できません。RDS のスナップショットの共有などにはカスタマー管理キーが必要です。
- キーの管理者は、キーを管理できても暗号操作はできません。
- 暗号化コンテキストは CloudTrail に平文で記録されるので、機密情報を入れません。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [kms 問1](../../exercises/kms.md#q1) | 2.2.4 | ある開発者は引数なしで CreateKey を呼びました。作成されるキーの説明として正しいものはどれ… |
| [kms 問2](../../exercises/kms.md#q2) | 2.2.4 | AWS の認証情報を持たない取引先のシステムが、データを暗号化して送ってきます。復号は社内で行います… |
| [kms 問3](../../exercises/kms.md#q3) | 2.2.4 | RSA_2048 のキーで RSAES_OAEP_SHA_256 を使い、Encrypt を呼びます… |
| [kms 問4](../../exercises/kms.md#q4) | 2.2.4 | アプリが 10 MB のファイルを暗号化する予定ですが、処理は数日後に別のワーカーが行います。今は暗… |
| [kms 問5](../../exercises/kms.md#q5) | 2.2.4 | GenerateRandom について正しいものはどれですか。 |
| [kms 問6](../../exercises/kms.md#q6) | 2.2.4 | カスタマー管理キーのキーポリシーから arn:aws:iam::111122223333:root … |
| [kms 問7](../../exercises/kms.md#q7) | 2.2.4 | API で作成したキーと、コンソールで作成したキーの既定のキーポリシーの違いとして正しいものを選んで… |
| [kms 問8](../../exercises/kms.md#q8) | 2.2.4 | カスタマー管理キーを、S3 経由でだけ使わせ、アプリからの直接の Decrypt は拒否したいと考え… |
| [kms 問9](../../exercises/kms.md#q9) | 2.2.4 | ワーカーのロールに一時的に復号の権限を渡します。作成直後から確実に使いたいので、キーポリシーの変更は… |
| [kms 問10](../../exercises/kms.md#q10) | 2.2.4 | CreateGrant の Operations に指定できないものはどれですか。 |
| [kms 問11](../../exercises/kms.md#q11) | 2.2.1 | クライアント側で暗号化したデータを、東京とオレゴンで再暗号化なしで復号できるようにしたいと考えていま… |
| [kms 問12](../../exercises/kms.md#q12) | 2.2.1 | マルチリージョンキーの説明として正しいものを選んでください。（2つ選択） |
| [kms 問13](../../exercises/kms.md#q13) | 2.2.4 | カスタマー管理キーの自動ローテーションを 30 日ごとにしたいと考えています。結果として正しいものは… |
| [kms 問14](../../exercises/kms.md#q14) | 2.2.4 | 本番のキーを誤って ScheduleKeyDeletion しました。今は待機期間中です。データを失… |
| [kms 問15](../../exercises/kms.md#q15) | 2.2.4 | データを暗号学的に使えなくする処理を、待機期間なしで実行したいと考えています。また、必要になったら元… |
| [kms 問16](../../exercises/kms.md#q16) | 2.2.4 | インポートした鍵素材を持つ対称キーのローテーションとして正しいものはどれですか。 |
| [kms 問17](../../exercises/kms.md#q17) | 2.2.4 | 別のアカウントのキーを使うアプリが、KeyId="alias/shared-key" で呼ぶと No… |
| [kms 問18](../../exercises/kms.md#q18) | 2.2.1 | 東京リージョンの SSE-KMS のバケットに大量のアップロードがあり、ThrottlingExce… |
| [kms 問19](../../exercises/kms.md#q19) | 2.2.3 | AWS Encryption SDK のデータキーキャッシュを使います。しきい値の説明として正しいも… |
| [kms 問20](../../exercises/kms.md#q20) | 2.2.4 | KMS の操作を CloudTrail で監査するときの説明として正しいものはどれですか。 |
| [kms 問21](../../exercises/kms.md#q21) | 2.2.3 | 医療データを S3 に保存します。要件は、平文のデータが AWS に届かないことで、S3 は暗号化さ… |

<!-- questions:end -->

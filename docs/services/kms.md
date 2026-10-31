# AWS KMS

[:material-sprout: CLF](../courses/clf/services.md){ .exam-badge .exam-foundational } [:material-sprout: AIF](../courses/aif/services.md){ .exam-badge .exam-foundational } [:material-certificate: SAA](../courses/saa/services.md){ .exam-badge .exam-associate } [:material-certificate: DVA](../courses/dva/services.md){ .exam-badge .exam-associate } [:material-certificate: SOA](../courses/soa/services.md){ .exam-badge .exam-associate } [:material-certificate: DEA](../courses/dea/services.md){ .exam-badge .exam-associate } [:material-certificate: MLA](../courses/mla/services.md){ .exam-badge .exam-associate } [:material-star-circle: SAP](../courses/sap/services.md){ .exam-badge .exam-professional } [:material-star-circle: DOP](../courses/dop/services.md){ .exam-badge .exam-professional } [:material-star-circle: AIP](../courses/aip/services.md){ .exam-badge .exam-professional } [:material-target: SCS](../courses/scs/services.md){ .exam-badge .exam-specialty }

暗号鍵を作成、管理し、データの暗号化と復号に使うためのサービスです。AWS サービスのデータを保存時に暗号化するときも、アプリで独自に暗号化するときも、鍵の管理を任せられます。

**提供単位:** KMS キーはリージョンのリソースで、VPC の外にあります（[提供単位の一覧](resource-scope.md#scope-regional-outside)）。マルチリージョンキーも、各リージョンの別々のキーとして存在します。VPC から呼ぶときは、インターフェイスエンドポイントか NAT を通します。

[![KMS を使う主なサービス](../assets/diagrams/kms-services.png)](../assets/diagrams/kms-services.png)

## 保存時と転送時の暗号化 {#at-rest-in-transit}

| 観点 | 保存時の暗号化 | 転送時の暗号化 |
| --- | --- | --- |
| 守る対象 | ディスクやストレージ上のデータ | ネットワークを流れるデータ |
| 主な仕組み | KMS、S3 の SSE、EBS、RDS の暗号化 | TLS（HTTPS） |
| 防ぐもの | 媒体やバックアップからの漏えい | 盗聴、改ざん |
| 開発者の作業 | キーの選択、権限の設定 | HTTPS の強制、証明書の管理 |

保存時と転送時は別の対策なので、両方必要です。

- **例:** SSE-KMS の S3 バケットでも、`http://` で取得すれば、復号された本文がネットワークを平文で流れる。`aws:SecureTransport` の拒否を足して、初めて転送時も守れる。
- **例:** TLS で RDS に接続しても、ストレージが未暗号化ならスナップショットから読める。作成時にキーを指定する。

| サービス | 保存時 | 転送時の強制の例 |
| --- | --- | --- |
| S3 | 新規オブジェクトは既定で SSE-S3 | バケットポリシーで `aws:SecureTransport` が `false` のリクエストを拒否 |
| DynamoDB | 常に暗号化。既定は AWS 所有キー | SDK は HTTPS を使用 |
| RDS | 作成時に KMS キーを指定 | クライアントから TLS で接続 |
| Lambda | 環境変数は常に暗号化 | 暗号化ヘルパーで追加の保護 |

- **誤ると:** 次のバケットポリシーがないと、`http://` での取得も通る。止めるには、Allow の条件ではなく `Deny` で書く。

```json
{
  "Effect": "Deny",
  "Principal": "*",
  "Action": "s3:*",
  "Resource": ["arn:aws:s3:::my-bucket", "arn:aws:s3:::my-bucket/*"],
  "Condition": {"Bool": {"aws:SecureTransport": "false"}}
}
```

TLS の証明書については [証明書と WAF](certificates.md) を参照してください。

## KMS キーの種類 {#key-types}

管理主体で 3 種類に分かれます。

| 観点 | カスタマー管理キー | AWS 管理キー | AWS 所有キー |
| --- | --- | --- | --- |
| 作成先 | 自分のアカウント | 自分のアカウント | AWS のサービスアカウント |
| キーポリシー | 自分で管理 | サービスが管理（閲覧は可） | 見えない |
| CloudTrail での監査 | 可 | 可 | 不可 |
| 自動ローテーション | 任意 | 必須（約 1 年ごと） | サービスが決定 |
| 暗号 API の直接呼び出し | 可 | 不可（サービス経由のみ） | 不可 |
| クロスアカウント共有 | 可 | 不可 | サービスによる |
| 料金 | 月額と利用料 | 月額なし。利用料はサービスによる | なし |
| 見分け方 | `DescribeKey` の `KeyManager` が `CUSTOMER` | `KeyManager` が `AWS`、別名が `aws/サービス名` | 一覧に出ない |

キーポリシーやローテーションを自分で管理したいとき、暗号 API を直接呼びたいとき、クロスアカウントで共有したいときは、カスタマー管理キーを選びます。CloudTrail での監査は AWS 管理キーでもできます。

- **カスタマー管理キーの例:** `alias/orders` を作り、`OrdersRole` にだけ `kms:Decrypt` を許可する。監査人にキーの使用履歴を CloudTrail で示せる。
- **AWS 管理キーの例:** S3 で `aws/s3` を選ぶ。キーポリシーは AWS が管理するので、別のアカウントに許可できない。
- **AWS 所有キーの例:** DynamoDB の既定。料金はかからず何も設定しないが、CloudTrail にも一覧にも出ない。
- **誤ると:** AWS 管理キーの ARN を `Encrypt` に直接渡すと、サービス経由に限るキーなので `AccessDeniedException` になる。

用途では次のように分かれます。

| 種類 | 用途 | 主な操作 |
| --- | --- | --- |
| 対称（`SYMMETRIC_DEFAULT`） | 暗号化と復号の標準 | `Encrypt`, `Decrypt`, `GenerateDataKey` |
| 非対称（RSA） | KMS の外で公開鍵を使って暗号化、署名 | `Encrypt`, `Decrypt`, `Sign`, `Verify` |
| 非対称（楕円曲線） | 署名、鍵共有 | `Sign`, `Verify`, `DeriveSharedSecret` |
| HMAC | メッセージ認証コード | `GenerateMac`, `VerifyMac` |

キーの仕様は作成後に変更できません。データキーの生成には対称キーが必要です。また、複数リージョンで同じ鍵を使う場合は、マルチリージョンキー（ID が `mrk-` で始まる）があります。

- **対称の例:** S3 や RDS の暗号化、`GenerateDataKey`。
- **RSA の例:** 取引先に公開鍵を渡し、AWS アカウントがなくても `RSAES_OAEP_SHA_256` で暗号化してもらう。復号は `kms:Decrypt` を持つ人だけ。
- **楕円曲線の例:** `ECC_NIST_P256` と `ECDSA_SHA_256` で、ファームウェアに署名する。公開鍵を持つ端末が KMS を呼ばずに検証する。
- **HMAC の例:** `HMAC_256` で Webhook の本文に `GenerateMac` し、受け側が `VerifyMac` で確認する。
- **誤ると:** 非対称キーで `GenerateDataKey` を呼ぶと、`InvalidKeyUsageException` になる。

## キーポリシー、IAM、グラント {#access-control}

KMS キーの権限は、キーポリシーが中心です。他の多くのリソースと違い、キーポリシーで許可しない限り、同じアカウントの主体でも使えません。

| 仕組み | 特徴 | 使いどころ |
| --- | --- | --- |
| キーポリシー | すべてのキーに必須。主たる権限の定義 | 基本の管理者、利用者の定義 |
| IAM ポリシー | キーポリシーで許可されたときだけ有効 | アカウント内での権限の委譲 |
| グラント | 特定の主体に一時的に権限を委譲。条件も付けられる | AWS サービスの代理利用、動的な委譲 |

既定のキーポリシーの中心は次の文です。これはアカウントのルートユーザーだけに許可するものではなく、「IAM ポリシーでこのキーの権限を与えられるようにする」という意味を持ちます。

```json
{
  "Sid": "Enable IAM User Permissions",
  "Effect": "Allow",
  "Principal": {"AWS": "arn:aws:iam::111122223333:root"},
  "Action": "kms:*",
  "Resource": "*"
}
```

この文がないと、IAM ポリシーで許可しても効きません（IAM の拒否は効きます）。

- API で作成して指定しない場合、既定のポリシーはこの文だけ。
- コンソールで作成すると、キー管理者とキー利用者の文も追加される。
- キー管理者はキーを管理できるが、暗号操作はできない。
- `kms:ViaService` で、特定の AWS サービス経由の利用に限定できる。
- `kms:GrantIsForAWSResource` で、AWS サービス向けのグラントだけを許可できる。

グラントは、`CreateGrant` で作り、`RetireGrant` や `RevokeGrant` で削除します。作成直後は結果整合性の影響で反映に時間がかかることがあり、グラントトークンを使うとすぐに利用できます。

- **例:** alice に `kms:Decrypt` を渡す方法は 3 つある。キーポリシーに alice を書く、ルートの文を残して IAM ポリシーで許可する、グラントで渡す。
- **例:** EBS の暗号化ボリュームを付けると、EC2 がそのキーのグラントを作り、ボリュームを使う間だけ復号に使う。利用者には `kms:CreateGrant` が要る。
- **誤ると:** 利用者が `kms:ViaService` で `s3.ap-northeast-1.amazonaws.com` に絞られていると、同じキーを Secrets Manager 経由で使えない。

## 主な API {#api-operations}

| API | 動作 | 必要な権限 | 注意点 |
| --- | --- | --- | --- |
| `Encrypt` | 平文を暗号化 | `kms:Encrypt` | 対称キーで最大 4,096 バイト |
| `Decrypt` | 暗号文を復号 | `kms:Decrypt` | 対称キーは `KeyId` を省略可 |
| `GenerateDataKey` | データキーを生成。平文と暗号化済みを返す | `kms:GenerateDataKey` | `KeySpec` または `NumberOfBytes` が必須 |
| `GenerateDataKeyWithoutPlaintext` | 暗号化済みのデータキーだけを返す | `kms:GenerateDataKeyWithoutPlaintext` | 後で使うときに `Decrypt` |
| `ReEncrypt` | 平文を見せずに別のキーで再暗号化 | `kms:ReEncryptFrom`, `kms:ReEncryptTo` | キーの切り替えに使う |
| `DescribeKey` | キーの情報を取得 | `kms:DescribeKey` | |

非対称キーでの `Encrypt` は、さらに上限が小さくなります。たとえば `RSA_2048` と `RSAES_OAEP_SHA_256` の組み合わせでは 190 バイトです。

- **例:** 3 KB の API キーは `Encrypt` で暗号化できる。5 KB の設定ファイルは 4,096 バイトを超えるので、`ValidationException` になる。エンベロープ暗号化に変える。
- **例:** `GenerateDataKeyWithoutPlaintext` は、100 台のワーカーへ配る暗号化済みのキーの準備に使う。各ワーカーは使うときに `Decrypt` する。
- **例:** `ReEncrypt` は、`alias/old` の暗号文を `alias/new` に移すのに使う。呼び出し元には `kms:ReEncryptFrom`（元のキー）と `kms:ReEncryptTo`（先のキー）の両方が要る。

```python
import boto3

kms = boto3.client("kms")
KEY = "alias/app-key"
CONTEXT = {"app": "billing"}

encrypted = kms.encrypt(
    KeyId=KEY,
    Plaintext=b"small secret",
    EncryptionContext=CONTEXT,
)["CiphertextBlob"]

plain = kms.decrypt(
    CiphertextBlob=encrypted,
    EncryptionContext=CONTEXT,
)["Plaintext"]
```

## エンベロープ暗号化 {#envelope-encryption}

`Encrypt` は最大 4 KB までしか扱えません。大きなデータは、データキーで暗号化し、そのデータキーを KMS キーで暗号化します。これがエンベロープ暗号化です。KMS を呼ぶ回数が減り、暗号鍵自体は KMS の外に出ません。

```mermaid
sequenceDiagram
    participant A as アプリ
    participant K as KMS
    participant S as ストレージ
    A->>K: GenerateDataKey
    K-->>A: 平文のデータキーと暗号化済みのデータキー
    A->>A: 平文のキーでデータを暗号化し、キーを消去
    A->>S: 暗号文と暗号化済みのキーを保存
    A->>S: 取得
    S-->>A: 暗号文と暗号化済みのキー
    A->>K: Decrypt (暗号化済みのキー)
    K-->>A: 平文のデータキー
    A->>A: データを復号
```

次の例は、仕組みを説明するためのコードです（`cryptography` ライブラリを使用）。実際には AWS Encryption SDK を使うほうが安全です。

```python
import os
import boto3
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

kms = boto3.client("kms")
CONTEXT = {"purpose": "invoice"}


def encrypt(data: bytes) -> dict:
    key = kms.generate_data_key(
        KeyId="alias/app-key",
        KeySpec="AES_256",
        EncryptionContext=CONTEXT,
    )
    nonce = os.urandom(12)
    ciphertext = AESGCM(key["Plaintext"]).encrypt(nonce, data, None)
    return {
        "ciphertext": ciphertext,
        "nonce": nonce,
        "encrypted_key": key["CiphertextBlob"],  # データと一緒に保存する
    }


def decrypt(item: dict) -> bytes:
    plain_key = kms.decrypt(
        CiphertextBlob=item["encrypted_key"],
        EncryptionContext=CONTEXT,
    )["Plaintext"]
    return AESGCM(plain_key).decrypt(item["nonce"], item["ciphertext"], None)
```

| 確認事項 | 内容 |
| --- | --- |
| 保存するもの | 暗号文と暗号化済みのデータキー |
| 保存しないもの | 平文のデータキー。使い終えたらメモリから消す |
| 同じ暗号化済みキーの復号 | KMS の権限がある人だけ |
| キーの `KeySpec` | `AES_128` か `AES_256` |

**呼び出し回数の計算**です。100 万個の 1 MB のファイルを暗号化するとします。

- `Encrypt` なら、そもそも 4,096 バイトを超えるので使えない。
- ファイルごとに `GenerateDataKey` を呼ぶと、書き込みで 100 万回。
- データキーをキャッシュし、1 つのキーを 1,000 ファイルで再利用すると、1,000,000 ÷ 1,000 = 1,000 回で済む。その代わり、1 つのキーが漏れると 1,000 ファイルが読まれる。
- **誤ると:** 平文のデータキーを暗号文の隣に保存すると、暗号化の意味がなくなる。保存するのは `CiphertextBlob` のほう。

## 暗号化コンテキスト {#encryption-context}

暗号化コンテキストは、暗号化のときに渡す秘密でないキーと値の組で、追加認証データとして暗号文に結び付けられます。対称キーでのみ使えます。

- 復号では、暗号化のときと完全に一致（大文字と小文字も区別）する値を渡す。違うと `InvalidCiphertextException` になる。
- CloudTrail に平文で記録されるので、監査に役立つが、機密情報は入れない。
- ポリシーの条件 `kms:EncryptionContext:キー名` で、利用を制限できる。

```json
{
  "Effect": "Allow",
  "Principal": {"AWS": "arn:aws:iam::111122223333:role/BillingApp"},
  "Action": "kms:Decrypt",
  "Resource": "*",
  "Condition": {
    "StringEquals": {"kms:EncryptionContext:app": "billing"}
  }
}
```

S3 や Secrets Manager など、多くの AWS サービスも独自の暗号化コンテキストを使います。

- **例:** `{"app": "billing"}` で暗号化した暗号文を、`{"app": "Billing"}` で復号すると `InvalidCiphertextException` になる。大文字と小文字も区別する。キーの順序は関係ない。
- **例:** テナントごとに `{"tenant": "a"}` を付けると、テナント B の処理がテナント A の暗号文を渡しても復号に失敗する。CloudTrail で誰がどのテナントのデータを読んだかも分かる。
- **例:** S3 の SSE-KMS は `{"aws:s3:arn": "arn:aws:s3:::my-bucket/a.csv"}` を使う。バケットキーを有効にすると、値はバケットの ARN になる。
- **誤ると:** `{"user_email": "alice@example.com"}` のように個人情報を入れると、CloudTrail に平文で残る。

## ThrottlingException とキャッシュ {#throttling}

リクエストが上限を超えると、KMS は `ThrottlingException` を返します（HTTP 400）。

暗号操作の上限は対称キーで共有され、アカウントとリージョンごとに計算されます。AWS サービスが代理で呼ぶ分も含みます。

| リージョン | 対称キーの暗号操作の既定の上限（秒間） |
| --- | --- |
| us-east-1, us-west-2, eu-west-1 | 100,000 |
| ap-northeast-1 など一部 | 20,000 |
| その他 | 10,000 |

RSA と楕円曲線のキーは、それぞれ別枠で 1,000 です。クロスアカウントで使うと、キーの所有者ではなく呼び出し側のアカウントが計上されます。AWS 所有キーの利用は計上されません。

対処の順序は次のとおりです。

1. エクスポネンシャルバックオフで再試行する。SDK の再試行設定は [SDK と耐障害性](sdk-resilience.md) を参照。
2. S3 なら S3 バケットキーで KMS 呼び出しを減らす。
3. データキーをキャッシュする。AWS Encryption SDK のデータキーキャッシュや Hierarchical keyring を使う。
4. Service Quotas で上限の引き上げを申請する。

**計算の例**です。東京リージョンの上限は秒間 20,000 回です。

| 処理 | KMS の呼び出し（秒間） |
| --- | --- |
| S3 の SSE-KMS の `GetObject` | 12,000 |
| DynamoDB のカスタマー管理キー | 3,000 |
| アプリの `GenerateDataKey` | 7,000 |
| 合計 | 22,000 |

22,000 は 20,000 を超えるので、2,000 回分が `ThrottlingException` になる可能性があります。S3 バケットキーで `GetObject` の分が大きく減れば、合計は上限に収まります。

- **例:** 別のアカウントのキーを `444455556666` のロールが使う場合、この回数は `444455556666` の枠に数える。キーを持つアカウントの枠は減らない。
- **誤ると:** S3 への `PutObject` の失敗を S3 の性能の問題と考えても解決しない。SSE-KMS では KMS の呼び出しも同じ処理に含まれるので、KMS のメトリクスも確認する。

### データキーキャッシュ {#data-key-caching}

AWS Encryption SDK は、既定では暗号化のたびに新しいデータキーを作ります。キャッシュすると再利用できますが、同じ鍵で暗号化するデータが増えるトレードオフがあります。

| 向いている条件 | 設定すべきしきい値 |
| --- | --- |
| データキーを再利用できる | キャッシュの最大有効期間 |
| 大量のデータキーを生成する | 1 つのキーで暗号化する最大バイト数 |
| KMS の呼び出しが遅い、高い、上限に近い | 1 つのキーで暗号化する最大メッセージ数 |

- **例:** 最大有効期間 300 秒、最大メッセージ数 100 にすると、5 分経つか 100 回使うと新しいデータキーを取得する。秒間 10 メッセージなら、100 ÷ 10 = 10 秒ごとに `GenerateDataKey` を 1 回呼ぶ。キャッシュがなければ 10 秒で 100 回なので、呼び出しは 100 分の 1 になる。

## クライアント側とサーバー側の暗号化 {#client-vs-server-side}

| 観点 | サーバー側暗号化 | クライアント側暗号化 |
| --- | --- | --- |
| 暗号化する場所 | AWS サービスの中 | データを送る前のアプリの中 |
| サービスから見えるもの | 処理中は平文 | 暗号文のみ |
| 実装の負担 | 小さい。設定のみ | 大きい。鍵と形式の管理が必要 |
| 検索や集計 | そのまま使える | サービス側で中身を扱えない |
| 向いている場面 | 多くの場合の標準 | AWS にも平文を見せたくない要件 |
| 例 | SSE-S3、SSE-KMS、DynamoDB、EBS | AWS Encryption SDK、S3 Encryption Client |

- **サーバー側の例:** RDS の暗号化は、SQL で `WHERE` を使ったまま保存時だけ暗号化できる。
- **クライアント側の例:** クレジットカード番号をアプリで暗号化してから DynamoDB に入れる。DynamoDB の管理者にも読めないが、その属性では検索できない。

### S3 の暗号化オプション {#s3-encryption}

| 方式 | 鍵の管理 | 使う場面 |
| --- | --- | --- |
| SSE-S3 | S3 が管理 | 既定。特別な要件がないとき |
| SSE-KMS | KMS キー | 権限の分離、CloudTrail での監査 |
| DSSE-KMS | KMS キーで 2 層 | 2 層の暗号化が求められるとき |
| SSE-C | リクエストごとに自分の鍵を渡す | 鍵を AWS に保存したくないとき |
| クライアント側 | アプリが管理 | S3 に平文を渡したくないとき |

ヘッダーでの指定の例です。

```bash
# SSE-KMS でアップロード
aws s3 cp a.csv s3://my-bucket/ --sse aws:kms --sse-kms-key-id alias/orders
```

- **SSE-S3 の例:** `x-amz-server-side-encryption: AES256`。何も指定しなくても新しいオブジェクトはこの形になる。
- **SSE-KMS の例:** `x-amz-server-side-encryption: aws:kms`。キーを読めない人は、`s3:GetObject` があっても読めない。
- **DSSE-KMS の例:** `x-amz-server-side-encryption: aws:kms:dsse`。
- **SSE-C の例:** アップロードもダウンロードも、`x-amz-server-side-encryption-customer-key` で同じ鍵を渡す。鍵をなくすと読めない。

### AWS Encryption SDK {#encryption-sdk}

[:material-star-circle: AIP](../courses/aip/services.md){ .exam-badge .exam-professional }

クライアント側の暗号化ライブラリで、エンベロープ暗号化を代わりに行います。暗号文と暗号化済みのデータキーを 1 つのメッセージ形式にまとめるので、データキーを別に管理する必要がありません。

```python
import aws_encryption_sdk
from aws_encryption_sdk import CommitmentPolicy

client = aws_encryption_sdk.EncryptionSDKClient(
    commitment_policy=CommitmentPolicy.REQUIRE_ENCRYPT_REQUIRE_DECRYPT
)
provider = aws_encryption_sdk.StrictAwsKmsMasterKeyProvider(
    key_ids=["arn:aws:kms:ap-northeast-1:111122223333:key/1234abcd-12ab-34cd-56ef-1234567890ab"]
)

ciphertext, _ = client.encrypt(source=b"large data", key_provider=provider)
plaintext, _ = client.decrypt(source=ciphertext, key_provider=provider)
```

新しい版では、キーリングを使う方法も選べます。Encryption SDK は他のライブラリと形式の互換性がなく、DynamoDB Encryption Client や S3 のクライアント側暗号化で作った暗号文は復号できません。

- **例:** `key_ids` に東京と大阪のキーを並べると、データキーが両方で暗号化され、どちらのリージョンの権限でも復号できる。
- **例:** `CommitmentPolicy.REQUIRE_ENCRYPT_REQUIRE_DECRYPT` は既定かつ最も厳しい設定で、古い形式のメッセージの復号は失敗する。移行中だけ `REQUIRE_ENCRYPT_ALLOW_DECRYPT` を使う。
- **誤ると:** `StrictAwsKmsMasterKeyProvider` の `key_ids` に別のキーしかないと、暗号文に含まれるキーを使わず、`DecryptKeyError` になる。

## 暗号鍵でのデータの暗号化と復号 {#use-keys}

用途ごとの選び方です。

| 目的 | 方法 |
| --- | --- |
| 4 KB 以下の少量データ | `Encrypt` と `Decrypt` |
| 大きなデータ | エンベロープ暗号化。AWS Encryption SDK を推奨 |
| 今は使わないデータキーを準備 | `GenerateDataKeyWithoutPlaintext` |
| 別のキーへの切り替え | `ReEncrypt` |
| 署名と検証 | 非対称キーで `Sign` と `Verify` |
| AWS サービス上のデータ | サービスの暗号化設定でキーを指定 |

- **例:** 2 KB の API トークンは `Encrypt`、500 MB のログは Encryption SDK、ライセンスの署名は `RSA_2048` の `Sign` を選ぶ。

## Lambda 環境変数の暗号化 {#lambda-env-encryption}

Lambda の環境変数は、常にサーバー側で KMS により保存時に暗号化されます。既定は AWS 管理キーで、設定は不要です。

| 方法 | 動作 | 必要な権限 |
| --- | --- | --- |
| 既定（AWS 管理キー） | デプロイ時に暗号化、実行環境では平文で参照 | 追加なし |
| カスタマー管理キー | キーのローテーションや権限を自分で管理 | 設定する人に `kms:CreateGrant`, `kms:Encrypt`、閲覧する人に `kms:Decrypt` |
| 転送時の暗号化ヘルパー | コンソールでクライアント側でも暗号化。値は暗号文のまま関数に届く | 実行ロールに `kms:Decrypt` |

ヘルパーを使うと、コードで復号が必要になります。

```python
import base64
import os
import boto3

kms = boto3.client("kms")
ENCRYPTED = os.environ["DB_PASSWORD"]

# コールドスタート時に 1 回だけ復号する
DB_PASSWORD = kms.decrypt(
    CiphertextBlob=base64.b64decode(ENCRYPTED),
    EncryptionContext={
        "LambdaFunctionName": os.environ["AWS_LAMBDA_FUNCTION_NAME"]
    },
)["Plaintext"].decode()
```

カスタマー管理キーへの `kms:Decrypt` がないユーザーは、関数を管理できても環境変数を閲覧できません。特定のユーザーに見せたくないときは、この性質を使います。

データベースの認証情報は、環境変数ではなく [Secrets Manager](secrets.md) に置くのが AWS の推奨です。

- **例:** 関数の設定で `KMSKeyArn` に `arn:aws:kms:ap-northeast-1:111122223333:key/1234abcd-12ab-34cd-56ef-1234567890ab` を指定する。監査人は誰が復号したかを CloudTrail で追える。
- **誤ると:** カスタマー管理キーを無効にすると、関数の起動時に `KMSDisabledException` で失敗する。
- **誤ると:** ヘルパーを使っているのに実行ロールに `kms:Decrypt` がないと、コードの `decrypt` が `AccessDeniedException` になる。`EncryptionContext` を省いても `InvalidCiphertextException` になる。

## アカウントをまたぐ暗号化 {#cross-account}

別のアカウントのキーを使うには、次の両方が必要です。

1. キーを所有するアカウントで、キーポリシーに相手のアカウントまたはロールを許可する。
2. 利用するアカウントで、IAM ポリシーで主体に許可する。

```json
{
  "Sid": "AllowExternalAccount",
  "Effect": "Allow",
  "Principal": {"AWS": "arn:aws:iam::444455556666:root"},
  "Action": ["kms:Decrypt", "kms:GenerateDataKey*", "kms:DescribeKey"],
  "Resource": "*"
}
```

```json
{
  "Effect": "Allow",
  "Action": ["kms:Decrypt", "kms:GenerateDataKey*", "kms:DescribeKey"],
  "Resource": "arn:aws:kms:ap-northeast-1:111122223333:key/1234abcd-12ab-34cd-56ef-1234567890ab"
}
```

- 呼び出しでは、キー ARN または別名 ARN を指定する。キー ID や別名だけだと、自分のアカウントのキーと解釈される。
- 使えるのは暗号操作と `CreateGrant`、`DescribeKey`、`GetKeyRotationStatus`、`GetPublicKey`、`ListGrants`、`RetireGrant`、`RevokeGrant` などに限られる。`ScheduleKeyDeletion` のような管理操作を許可しても効かない。
- AWS 管理キーのポリシーは変更できないので、共有できない。共有するならカスタマー管理キーで暗号化する。
- たとえば RDS のスナップショットを共有するなら、AWS 管理キーではなくカスタマー管理キーが必要。
- **誤ると:** `aws/rds` で暗号化したスナップショットは、別のアカウントに共有できない。カスタマー管理キーで暗号化し直すコピーを作ってから共有する。
- **誤ると:** キーポリシーで `444455556666:root` に許可しただけだと、そのアカウントのロールは使えない。ロールの IAM ポリシーでも許可する。

## キーのローテーション {#key-rotation}

ローテーションは、キーの ID や ARN を変えずに、中の鍵素材を新しくします。古い素材は保持されるので、以前の暗号文も復号でき、コードの変更は不要です。

```python
import boto3

kms = boto3.client("kms")
key_id = "1234abcd-12ab-34cd-56ef-1234567890ab"

kms.enable_key_rotation(KeyId=key_id, RotationPeriodInDays=180)  # 有効化
kms.get_key_rotation_status(KeyId=key_id)                        # 確認
kms.rotate_key_on_demand(KeyId=key_id)                           # 今すぐ実行
kms.list_key_rotations(KeyId=key_id)                             # 履歴
kms.disable_key_rotation(KeyId=key_id)                           # 無効化
```

| 方式 | 対象 | 仕様 |
| --- | --- | --- |
| 自動 | 対称のカスタマー管理キー（KMS 生成の鍵素材） | 既定 365 日。90〜2560 日で指定 |
| オンデマンド | 対称キー（KMS 生成またはインポート） | キーごとに最大 25 回。自動の予定は変えない |
| 手動 | 非対称、HMAC、カスタムキーストアのキー | 新しいキーを作り、別名を切り替える |
| AWS 管理キー | 変更不可 | 約 1 年ごとに自動 |

- 無効化すると、その時点の鍵素材を使い続ける。古い素材は削除されない。
- 再度有効化すると、有効化した日を基準にローテーションする。
- 無効化されたキーや削除待ちのキーはローテーションされない。
- ローテーションは既存のデータを再暗号化しない。流出したデータキーの影響も消えない。
- 実行すると EventBridge に `KMS CMK Rotation` イベントが、CloudTrail に `RotateKey` イベントが記録される。
- 料金は、最初の 2 回のローテーションで増え、それ以降は増えない。
- **例:** 2026 年 1 月に有効化すると、365 日の設定なら 2027 年 1 月に新しい鍵素材になる。アプリの `Decrypt` はそのままで動き、KMS が暗号文のメタデータから古い鍵素材を選ぶ。
- **例:** 監査の前に確認のために 1 回だけ回すなら、`rotate_key_on_demand` を使う。上限 25 回のうち 1 回を消費し、年次の予定は動かない。
- **誤ると:** データキーが漏えいしたときに KMS キーをローテーションしても、そのデータキーで作った暗号文は読まれたまま。データを新しいデータキーで暗号化し直す。

## 別名とキーの削除 {#aliases}

別名（エイリアス）は KMS キーの覚えやすい名前で、`alias/` で始まります。

- 別名はキーのプロパティではなく別のリソース。`UpdateAlias` で指し先を切り替えられる。
- 手動ローテーションでは、コードを変えずに別名の指し先を新しいキーに変える。
- 別名はアカウントとリージョンごと。同じ名前を各リージョンで作れば、コードを共通化できる。
- `alias/aws/` は AWS 管理キー用に予約されている。
- 別のアカウントのキーは、別名 ARN で指定する。

キーの削除はすぐには実行されません。`ScheduleKeyDeletion` で 7〜30 日（既定 30 日）の待機期間を置き、その間は `CancelKeyDeletion` で取り消せます。削除すると、そのキーの暗号文は復号できなくなります。迷ったら `DisableKey` で無効化します。

- **別名の例:** アプリは `alias/orders` を使う。新しいキーを作ったら `aws kms update-alias --alias-name alias/orders --target-key-id <新しいキー ID>` だけで、以後の暗号化が新しいキーになる。
- **誤ると:** 別名を切り替えたあとに古いキーを削除すると、古いキーで作った暗号文は読めなくなる。暗号文の中身は古いキーを指しているからだ。別名を切り替えても、古いキーは残す。
- **誤ると:** IAM ポリシーの `Resource` に別名の ARN を書いても、暗号操作の対象はキーなので効かない。`kms:RequestAlias` を使う。

## サービスでの KMS の利用 {#service-integration}

| サービス | 既定 | KMS の使い方 | 注意点 |
| --- | --- | --- | --- |
| S3（SSE-KMS） | SSE-S3 | アップロードで `GenerateDataKey`、ダウンロードで `Decrypt` | 上限に達しやすい。S3 バケットキーで KMS リクエストのコストを最大 99% 削減 |
| DynamoDB | AWS 所有キー | テーブルごとにキーの種類を選択 | 常に暗号化され、無効にできない |
| RDS | 作成時に選択 | ストレージ、ログ、バックアップ、スナップショットを暗号化 | 作成後にキーを変更できない |
| EBS | 設定による | グラントを作ってデータキーを利用 | キーの利用者に `kms:CreateGrant` が必要 |
| Lambda | AWS 管理キー | 環境変数を暗号化 | 上記のとおり |
| Secrets Manager | `aws/secretsmanager` | シークレットを暗号化 | カスタマー管理キーなら `kms:Decrypt` も必要 |
| Parameter Store | `aws/ssm` | スタンダードは直接暗号化、アドバンストはエンベロープ暗号化 | `WithDecryption=True` で復号 |
| SQS | 設定による | データキーでメッセージを暗号化 | AWS 管理キーで暗号化したキューは別アカウントの Lambda を呼べない |

S3 バケットキーを有効にすると、暗号化コンテキストはオブジェクト ARN ではなくバケット ARN になります。ポリシーでオブジェクト ARN を条件にしているなら修正します。

SSE-KMS のオブジェクトを読むには、`s3:GetObject` に加えて KMS キーの `kms:Decrypt` も必要です。権限エラーの原因としてよく問われます。

- **例:** 表の値の使い方です。DynamoDB のテーブルを `AWS_OWNED_KMS_KEY` からカスタマー管理キーに切り替えられる。RDS は作成時のキーのまま変更できないので、スナップショットを別のキーでコピーして復元する。
- **例:** Parameter Store の `SecureString` をスタンダードの 4 KB で `aws/ssm` に入れると、`Encrypt` で直接暗号化される。
- **誤ると:** `s3:GetObject` だけのロールで SSE-KMS のオブジェクトを読むと、`kms:Decrypt` の `AccessDenied` になる。S3 のエラーでも、メッセージは KMS の操作を示している。

## キーの作成時の設定 {#key-creation-settings}

`CreateKey` は引数なしでも動き、対称の暗号化キーができます。

| パラメータ | 既定 | 値と効果 |
| --- | --- | --- |
| `KeySpec` | `SYMMETRIC_DEFAULT` | 下の表。作成後は変更できない |
| `KeyUsage` | `ENCRYPT_DECRYPT` | `SIGN_VERIFY`, `GENERATE_VERIFY_MAC`, `KEY_AGREEMENT` |
| `Origin` | `AWS_KMS` | `EXTERNAL`（インポート）, `AWS_CLOUDHSM`, `EXTERNAL_KEY_STORE` |
| `MultiRegion` | `false` | `true` でマルチリージョンのプライマリキー。後から変換できない |
| `Policy` | 既定のキーポリシー | 未指定なら「IAM を有効にする文」のみ |
| `BypassPolicyLockoutSafetyCheck` | `false` | 自分が管理できなくなるポリシーの拒否を飛ばす。通常は使わない |

パラメータごとの例です。

```bash
aws kms create-key --description "orders" --key-spec RSA_2048 --key-usage SIGN_VERIFY
```

- **`KeySpec` と `KeyUsage` の例:** `RSA_2048` なら `ENCRYPT_DECRYPT` か `SIGN_VERIFY` を選ぶ。`ENCRYPT_DECRYPT` で作ったキーで `Sign` を呼ぶと `InvalidKeyUsageException` になり、後から用途は変えられない。
- **`Origin` の例:** `EXTERNAL` は自分の鍵素材を入れるとき。`AWS_CLOUDHSM` は専用の HSM に鍵を置くとき。
- **`MultiRegion` の例:** `true` にすると ID が `mrk-` で始まる。後から `true` にはできないので、必要なら作り直して暗号文を移す。
- **`Policy` の例:** 指定しないと IAM を有効にする文だけになる。自分の許可を書かないポリシーを渡すと、安全チェックで `MalformedPolicyDocumentException` になる。
- **`BypassPolicyLockoutSafetyCheck` の例:** `true` で上のチェックを飛ばせるが、誰も管理できないキーができる恐れがある。回復には AWS サポートへの相談が必要になる。

### キーの仕様 {#key-specs}

| 仕様 | 用途 | 備考 |
| --- | --- | --- |
| `SYMMETRIC_DEFAULT` | 暗号化と復号 | 暗号文は KMS でのみ復号できる。データキーの生成はこれだけ |
| `RSA_2048`, `RSA_3072`, `RSA_4096` | 暗号化と復号、または署名と検証 | どちらか一方を作成時に選ぶ |
| `ECC_NIST_P256`, `ECC_NIST_P384`, `ECC_NIST_P521`, `ECC_SECG_P256K1` | 署名と検証、または鍵共有 | |
| `ECC_NIST_EDWARDS25519` | 署名と検証 | |
| `HMAC_224`, `HMAC_256`, `HMAC_384`, `HMAC_512` | `GenerateMac`, `VerifyMac` | `KeyUsage` の指定が必須 |

- **選び方の例:** 署名の検証を社外の端末で行うなら `ECC_NIST_P256`、古い端末で RSA しか扱えないなら `RSA_2048`、ビットコイン系の署名なら `ECC_SECG_P256K1`、Webhook の認証なら `HMAC_256`。
- **誤ると:** `HMAC_256` を作るときに `--key-usage GENERATE_VERIFY_MAC` を省くと、エラーになる。

### 対称と非対称の違い {#symmetric-vs-asymmetric}

| 観点 | 対称 | 非対称 |
| --- | --- | --- |
| 鍵素材 | KMS の外に出ない | 公開鍵は `GetPublicKey` で取得できる |
| 暗号文の作成場所 | KMS 内 | KMS の外で公開鍵を使える |
| 暗号化コンテキスト | 使える | 使えない |
| `Decrypt` の `KeyId` | 省略できる | 必須 |
| 自動ローテーション | 対象 | 対象外 |

外部のシステムが AWS の認証情報を持てず、データを暗号化して送ってくる場合は、RSA キーの公開鍵を渡します。AWS の認証情報があるなら、対称キーが標準です。

- **例:** 非対称キーの `Decrypt` で `KeyId` と `EncryptionAlgorithm` を省くと失敗する。対称キーは暗号文のメタデータから分かるので、`KeyId` なしで通る。

## キーポリシーの詳細 {#key-policy-details}

### 既定のキーポリシー {#default-key-policy-details}

| 作成の方法 | 既定で入る文 |
| --- | --- |
| API、CLI、SDK、CloudFormation | IAM を有効にする文のみ |
| コンソール | IAM を有効にする文、キー管理者、キー利用者、AWS サービスとの統合のための文 |

| 文 | 主な権限 |
| --- | --- |
| キー管理者 | `kms:Create*`, `kms:Describe*`, `kms:Enable*`, `kms:Put*`, `kms:Update*`, `kms:Revoke*`, `kms:Disable*`, `kms:Get*`, `kms:Delete*`, `kms:ScheduleKeyDeletion`, `kms:CancelKeyDeletion` など |
| キー利用者 | `kms:Encrypt`, `kms:Decrypt`, `kms:ReEncrypt*`, `kms:GenerateDataKey*`, `kms:DescribeKey` |
| AWS サービスとの統合 | `kms:CreateGrant`, `kms:ListGrants`, `kms:RevokeGrant`（`kms:GrantIsForAWSResource` が真のとき） |

`arn:aws:iam::アカウント:root` を指定すると、そのアカウントの主体すべてに直接許可されるわけではありません。アカウントが IAM ポリシーで委譲できるようになるだけです。

この文を消してから IAM だけで許可しても、キーを使えません。利用者には `AccessDeniedException` が返ります。誰も管理できないポリシーを `PutKeyPolicy` で設定すると、キーが管理不能になります。

キーポリシーの `Principal` を `*` にして条件を付けないと、全アカウントの全員に許可するので避けます。

- **キー管理者の例:** `KmsAdmin` に管理の文を許可する。`kms:ScheduleKeyDeletion` はできるが、`kms:Decrypt` はないので、データは読めない。
- **キー利用者の例:** `OrdersRole` に利用者の文を許可する。`kms:DisableKey` はできない。
- **統合の文の例:** 利用者が EBS でこのキーを使うと、EBS がグラントを作る。この文がないと、EBS の暗号化ボリュームのアタッチが失敗する。

### kms:ViaService {#via-service}

特定のサービス経由に限定します。AWS サービスが利用者の代理で呼ぶとき（フォワードアクセスセッション）に効きます。

```json
{
  "Effect": "Allow",
  "Principal": {"AWS": "arn:aws:iam::111122223333:role/App"},
  "Action": ["kms:Decrypt", "kms:GenerateDataKey*"],
  "Resource": "*",
  "Condition": {
    "StringEquals": {
      "kms:ViaService": "s3.ap-northeast-1.amazonaws.com",
      "kms:CallerAccount": "111122223333"
    }
  }
}
```

このロールは S3 を通してならキーを使えますが、アプリから直接 `kms:Decrypt` を呼ぶと拒否されます。値には `<サービス>.<リージョン>.amazonaws.com` の形で、リージョンを含めます。

- **誤ると:** 値を `s3.amazonaws.com` と書くと、リージョンが入っていないので一致せず、S3 経由でも拒否される。
- **誤ると:** 値のリージョンを `ap-northeast-1` にしたままマルチリージョンキーのレプリカのポリシーをコピーすると、`us-west-2` の S3 から使えない。

### 主な条件キー {#kms-condition-keys}

| キー | 用途 |
| --- | --- |
| `kms:ViaService` | 特定のサービス経由に限定 |
| `kms:CallerAccount` | 呼び出し元のアカウント |
| `kms:EncryptionContext:キー`, `kms:EncryptionContextKeys` | 暗号化コンテキストの値、キーで絞る |
| `kms:GrantIsForAWSResource` | AWS サービスと統合されたグラントだけ許可 |
| `kms:RequestAlias`, `kms:ResourceAliases` | 別名に基づく制御。IAM の `Resource` に別名は書けない |

- **`kms:CallerAccount` の例:** `111122223333` と `kms:ViaService` を組み合わせると、AWS 管理キーと同じ「アカウントのサービス経由だけ」の形になる。
- **`kms:EncryptionContext:` の例:** `kms:EncryptionContext:department` を `finance` にすると、`{"department": "finance"}` を渡した呼び出しだけが通る。
- **`kms:EncryptionContextKeys` の例:** `ForAllValues:StringEquals` で `["department"]` にすると、他のキーを含むコンテキストを拒否する。
- **`kms:GrantIsForAWSResource` の例:** 真のときだけ `kms:CreateGrant` を許可すると、EBS などの統合サービスには渡せるが、人が自分でグラントを作れない。
- **`kms:ResourceAliases` の例:** `ForAnyValue:StringLike` で `alias/finance-*` のキーだけを使わせる。キーに別名を足すだけで権限を与えられる。
- **`kms:RequestAlias` の例:** `alias/finance` という別名を指定した呼び出しだけを許可する。キー ID で呼ぶと一致しない。

### グラントの設定 {#grant-settings}

```bash
aws kms create-grant \
  --key-id 1234abcd-12ab-34cd-56ef-1234567890ab \
  --grantee-principal arn:aws:iam::111122223333:role/Worker \
  --operations Decrypt GenerateDataKey \
  --retiring-principal arn:aws:iam::111122223333:role/Admin \
  --constraints EncryptionContextEquals={Purpose=Test}
```

| 項目 | 内容 |
| --- | --- |
| `GranteePrincipal` | 権限を受ける主体。別アカウントでも可 |
| `Operations` | 暗号操作、`DescribeKey`, `CreateGrant`, `RetireGrant` などに限る。`ScheduleKeyDeletion` は不可で、`ValidationError` になる |
| `Constraints` | `EncryptionContextEquals` か `EncryptionContextSubset` |
| `RetiringPrincipal` | グラントを退役できる主体 |
| `Name` | 再試行の重複を防ぐ名前 |
| 上限 | キーあたり 50,000 |

- **`Operations` の例:** `Decrypt` だけを渡す。`GenerateDataKey` を呼ぶと拒否される。`ScheduleKeyDeletion` は指定できる操作にないので、検証エラーになる。
- **`Constraints` の例:** `EncryptionContextEquals={Purpose=Test}` は、コンテキストが `{"Purpose": "Test"}` と完全一致のときだけ通る。`EncryptionContextSubset` なら、`{"Purpose": "Test", "Team": "a"}` も通る。
- **`Name` の例:** `--name batch-20261031` を付けて再試行すると、同じグラントが 2 つできない。
- **`RetiringPrincipal` の例:** `Admin` を指定すると、`Admin` は `RetireGrant` で削除できる。受け手の `Worker` も、`RetireGrant` を操作に含めていなければ削除できない。

**結果整合性**: 反映は通常数秒以内ですが、すぐに使うならレスポンスの `GrantToken` をリクエストの `GrantTokens` に渡します。トークンは秘密ではありません。

| 削除の API | 主な使い手 |
| --- | --- |
| `RetireGrant` | 作業が終わったグラントの受け手や退役の主体 |
| `RevokeGrant` | 権限を取り消す管理者。付与を意図的に否定する |

## マルチリージョンキー {#multi-region-keys}

| 項目 | 内容 |
| --- | --- |
| 共通するもの | キー ID、鍵素材、キーの仕様、自動ローテーションの設定 |
| 別々のもの | キーポリシー、グラント、別名、タグ、キーの有効、無効 |
| 作成 | `CreateKey` の `MultiRegion=true` のあと `ReplicateKey` |
| ローテーション | プライマリで実施 |
| 既存のキーの変換 | できない |
| 料金と上限 | 関連キーはそれぞれ 1 つのキーとして数える |

```bash
aws kms replicate-key --key-id mrk-1234abcd12ab34cd56ef1234567890ab \
  --replica-region us-west-2
```

東京で暗号化した DynamoDB グローバルテーブルのフィールドを、オレゴンでも再暗号化なしで復号したい場合に使います。クライアント側で暗号化するとき以外は、単一リージョンのキーが基本です。多くの AWS サービスは、これを単一リージョンのキーと同様に扱います。

プライマリキーを削除するには、先にレプリカを削除します。その間の状態は `PendingReplicaDeletion` です。プライマリの待機期間は、最後のレプリカが削除されたときから始まります。

- **例:** `mrk-1234...` のレプリカを `us-west-2` に作ると、キーポリシーはレプリカごとに別なので、オレゴンのロールへの許可をレプリカ側に書く必要がある。
- **誤ると:** 東京のキーのポリシーだけ直しても、レプリカの権限は変わらない。オレゴンで `AccessDeniedException` になる。
- **誤ると:** レプリカを無効にしてもプライマリは動く。状態は同期しないので、片方を無効にしても全体は止まらない。

## ローテーションの設定 {#rotation-settings}

```bash
aws kms enable-key-rotation --key-id <id> --rotation-period-in-days 180
```

| 設定 | 値 |
| --- | --- |
| `RotationPeriodInDays` | 90〜2,560 日。既定 365 日 |
| オンデマンド | キーあたり 25 回まで。引き上げ不可 |

180 日に設定して 3 年運用すると、自動ローテーションは約 6 回です。ID や ARN は変わらず、新しい暗号文は新しい鍵素材で作られ、古い暗号文は古い鍵素材で復号されます。

既存の暗号文やデータキーは再暗号化されません。データキーを再度暗号化したいなら、`ReEncrypt` を使います。

- **`RotationPeriodInDays` の例:** `30` は 90 未満なので拒否される。`90` なら年に約 4 回、365 ÷ 90 ≒ 4.06 回。
- **オンデマンドの例:** 26 回目の `RotateKeyOnDemand` はエラーになる。引き上げられないので、頻繁に回す用途には使わない。

## キーの無効化と削除 {#disable-delete}

| 操作 | 効果 | 戻せるか | 暗号操作でのエラー |
| --- | --- | --- | --- |
| `DisableKey` | 使えなくなる。ローテーションも止まる | `EnableKey` | `DisabledException` |
| `ScheduleKeyDeletion` | 7〜30 日後に削除（既定 30 日） | 待機中は `CancelKeyDeletion`。戻すと `Disabled` になる | `KMSInvalidStateException` |
| 削除の完了 | 鍵素材、メタデータ、別名を削除 | 不可 | |

実際の削除は、指定より最大 24 時間ほど遅れることがあります。正確な日時は `DescribeKey` で確認します。

待機中に誰かがキーを使おうとしたことを検知するには、CloudTrail のイベントから CloudWatch アラームを作ります。

- **例:** `aws kms schedule-key-deletion --key-id <id> --pending-window-in-days 7` なら、7 日後に消える。待機中にアプリの `Decrypt` が失敗してアラームが鳴れば、`cancel-key-deletion` と `enable-key` で元に戻せる。
- **例:** 使っていないと思うキーは、まず `DisableKey` で 1 か月様子を見る。`DisabledException` が出なければ、削除の予約に進む。
- **誤ると:** `--pending-window-in-days 3` は範囲外でエラーになる。`CancelKeyDeletion` の後は `Disabled` のままなので、`EnableKey` を忘れると `DisabledException` が続く。
- **誤ると:** 待機期間の 30 日が過ぎてからは戻せない。S3 のオブジェクトも EBS のスナップショットも読めなくなる。

## 鍵素材のインポート {#imported-key-material}

自分で作った鍵素材を使う方法で、`Origin=EXTERNAL` のキーを作ります。

1. `CreateKey --origin EXTERNAL` で鍵素材なしのキーを作る。
2. `GetParametersForImport` でラッピング用の公開鍵とインポートトークンを取得する。
3. 鍵素材を暗号化し、`ImportKeyMaterial` でアップロードする。

| 観点 | 内容 |
| --- | --- |
| 対象 | 対称、非対称（ML-DSA, ML-KEM を除く）、HMAC、マルチリージョンキー |
| 有効期限 | `ValidTo` で任意に設定できる |
| 鍵素材の削除 | `DeleteImportedKeyMaterial` ですぐ削除できる。再度インポートで戻せる |
| 自動ローテーション | 不可 |
| オンデマンドローテーション | 対称キーは可。新しい鍵素材を先にインポートする |

鍵素材が期限切れや削除になると、キーの状態が `PendingImport` になり、使えなくなります。

待機期間なしで鍵素材を消せるのが、インポートを選ぶ主な理由です。

- **例:** `ImportKeyMaterial` で `ValidTo` を `2027-06-30T00:00:00Z` にすると、その時点で `PendingImport` になり、暗号化も復号もできない。同じ鍵素材を再度インポートすれば戻る。
- **誤ると:** 違う鍵素材をインポートすると拒否される（ローテーションの追加を除く）。元の鍵素材を手元でなくすと、既存の暗号文は読めない。

## API の詳細 {#api-details}

| API | 入力 | 出力 | 上限 |
| --- | --- | --- | --- |
| `Encrypt` | 平文 | 暗号文 | 下の表 |
| `Decrypt` | 暗号文 | 平文 | 暗号文は 6,144 バイトまで |
| `ReEncrypt` | 暗号文、宛先キー | 新しい暗号文 | 平文をアプリに見せない |
| `GenerateDataKey` | `KeySpec` または `NumberOfBytes` | 平文のキー、暗号化されたキー | `NumberOfBytes` は 1〜1,024 |
| `GenerateDataKeyWithoutPlaintext` | 同上 | 暗号化されたキーのみ | |
| `GenerateDataKeyPair` | `KeyPairSpec` | 公開鍵、平文の秘密鍵、暗号化された秘密鍵 | |
| `GenerateRandom` | `NumberOfBytes` | ランダムなバイト列 | 1〜1,024 バイト。キー不要 |

| 暗号化のアルゴリズム、キー | `Encrypt` の平文の上限 |
| --- | --- |
| `SYMMETRIC_DEFAULT` | 4,096 バイト |
| `RSA_2048` + `RSAES_OAEP_SHA_1` / `SHA_256` | 214 / 190 バイト |
| `RSA_3072` + `RSAES_OAEP_SHA_1` / `SHA_256` | 342 / 318 バイト |
| `RSA_4096` + `RSAES_OAEP_SHA_1` / `SHA_256` | 470 / 446 バイト |

`GenerateDataKey` は `KeySpec` と `NumberOfBytes` を同時に指定できません。128 ビットや 256 ビットなら `KeySpec` を使います。

KMS はデータキーを保存も追跡もしません。またデータキーで暗号化もしません。使うのはアプリ側で、暗号化されたキーの保管もアプリの責任です。

**用途別の例**です。

| 場面 | API |
| --- | --- |
| 今すぐ 10 MB のファイルを暗号化 | `GenerateDataKey` |
| 別のワーカーが後で暗号化するキーを、準備だけする | `GenerateDataKeyWithoutPlaintext` |
| KMS キーを新しいものに切り替え、データキーを包み直す | `ReEncrypt` |
| 暗号学的に強い 32 バイトのトークンが欲しい | `GenerateRandom` |

- **`GenerateDataKey` の例:** `KeySpec=AES_256` は 32 バイト（256 ビット）。512 ビットなら `NumberOfBytes=64`。両方は指定できない。
- **`GenerateDataKeyPair` の例:** 端末ごとの RSA キーペアを作り、暗号化された秘密鍵を保存し、公開鍵を配る。
- **`GenerateRandom` の例:** `NumberOfBytes=32` で 32 バイトのランダム値を得る。KMS キーは要らないが、対称キーの暗号操作の枠に数える。
- **`Decrypt` の例:** 暗号文が 6,144 バイトを超えるなら、KMS で作った暗号文ではない。エンベロープ暗号化のデータ本体を誤って渡していることが多い。

### 主なエラー {#kms-errors}

| エラー | 原因 |
| --- | --- |
| `AccessDeniedException` | キーポリシー、IAM、グラントのいずれにも許可がない |
| `InvalidCiphertextException` | 暗号文の破損、暗号化コンテキストの不一致 |
| `IncorrectKeyException` | `KeyId` が暗号化に使ったキーと違う |
| `DisabledException` | キーが無効 |
| `KMSInvalidStateException` | 削除待ちなど、操作に合わない状態 |
| `ThrottlingException` | リクエストの上限超過（HTTP 400） |
| `KeyUnavailableException` | キーを一時的に使えない。再試行する |
| `NotFoundException` | 指定のキーがない。別のリージョンや、別アカウントのキーを ID で指定している場合など |

- **`IncorrectKeyException` の例:** `alias/a` で暗号化した暗号文を、`KeyId=alias/b` で `Decrypt` すると起きる。対称キーなら `KeyId` を省けば、暗号文の中のキーが使われる。
- **`InvalidCiphertextException` の例:** Base64 のままの文字列を `CiphertextBlob` に渡すと起きる。先にデコードする。
- **`NotFoundException` の例:** 東京のキー ID を `us-west-2` のクライアントで使うと起きる。マルチリージョンキーでなければ、リージョンごとにキーが別。
- **`KMSInvalidStateException` の例:** 削除待ちのキーで `Encrypt` すると起きる。`CancelKeyDeletion` と `EnableKey` で戻す。

## リクエストの計算 {#request-quota-calc}

| 項目 | 既定の上限（秒間、共有） |
| --- | --- |
| 対称キーの暗号操作 | 10,000。`ap-northeast-1` などは 20,000。`us-east-1`, `us-west-2`, `eu-west-1` は 100,000 |
| RSA キーの暗号操作 | 1,000 |
| 楕円曲線、SM2 キーの暗号操作 | 1,000 |
| `CreateGrant` | 50 |
| `DescribeKey` | 2,000 |
| `CreateKey` | 5 |

**計算の例**: 東京リージョンで、SSE-KMS の S3 バケットに秒間 500 回 `PutObject` し、秒間 800 回 `GetObject` するとします。S3 バケットキーがないと、KMS へのリクエストは秒間 1,300 回です。

同じアカウントとリージョンの他の処理と合わせて 20,000 を超えなければ、スロットリングされません。バケットキーを有効にすると、S3 が短期間バケット単位のキーを再利用するので、KMS へのリクエストはさらに減ります。

- **例:** 同じ処理を東京以外の既定 10,000 のリージョンに置いても、1,300 ÷ 10,000 = 13% で収まる。秒間 15,000 まで増えれば、そのリージョンでは上限を超える。
- **例:** `DescribeKey` を呼ぶ検証を毎リクエストに入れると、秒間 2,000 の別枠に当たる。結果をキャッシュする。
- **例:** `CreateGrant` は秒間 50 回。起動時に大量の暗号化ボリュームを作る処理で当たりやすい。

### S3 バケットキー {#s3-bucket-key-settings}

| 項目 | 内容 |
| --- | --- |
| 効果 | KMS へのリクエストのコストを最大 99% 削減 |
| 既存のオブジェクト | 対象外。`CopyObject` でコピーすると適用される |
| 暗号化コンテキスト | バケット ARN になる。オブジェクト ARN を条件にしたポリシーは効かなくなる |
| CloudTrail | KMS のイベントがオブジェクト単位でなくバケット単位になる |

- **例:** バケットキーを有効にしたあと、既存の 1 億オブジェクトを読んでも KMS の呼び出しは減らない。`CopyObject` で同じ場所にコピーし直すか、S3 バッチオペレーションを使う。
- **誤ると:** ポリシーが `kms:EncryptionContext:aws:s3:arn` を `arn:aws:s3:::my-bucket/*` に絞っていると、有効にした途端に拒否される。値をバケットの ARN に直す。

### データキーキャッシュの設定 {#data-key-cache-settings}

| しきい値 | 既定、範囲 | 必須か |
| --- | --- | --- |
| 最大有効期間 | 0 より大きい値。多くの言語は秒、JavaScript はミリ秒 | 必須 |
| 暗号化の最大メッセージ数 | 1〜2^32。既定 2^32 | 任意 |
| 暗号化の最大バイト数 | 既定 2^63 - 1 | 任意 |

- **例:** 最大有効期間 60 秒、最大バイト数 1 GB にすると、1 分経つか 1 GB 暗号化した時点でキーを捨てる。100 MB のメッセージなら 10 個で上限になる。
- **誤ると:** JavaScript 版で `300` を秒のつもりで指定すると、300 ミリ秒になり、キャッシュがほとんど効かない。

## CloudTrail での監査 {#kms-cloudtrail}

KMS のすべての操作は CloudTrail に記録されます。読み取り専用の `ListAliases` や、管理操作の `CreateKey`、暗号操作の `Decrypt` も含みます。

- `Encrypt` の `Plaintext` のような機密フィールドは記録されない。
- 暗号化コンテキストは記録される。
- 証跡からは、KMS のイベントだけをまとめて除外できる（個別には選べない）。大量のイベントでコストが増えるときの選択肢。
- `RotateKey` イベントでローテーションを確認できる。
- AWS 所有キーの使用は記録されない。
- **例:** イベント名 `Decrypt` の `requestParameters.encryptionContext` を見ると、どのテナントのデータかが分かる。`userIdentity` で読んだ主体が分かる。
- **例:** S3 のバケットキーを有効にすると、`Decrypt` のイベントが大きく減る。「イベントが減った」はバケットキーの効果として正常。

## アカウントをまたぐ手順 {#cross-account-steps}

Account A のキーを Account B のロールで使う順序です。

1. A のキーポリシーで、B のアカウントかロールに `kms:Decrypt` などを許可する。
2. B の IAM ポリシーで、ロールにキー ARN への同じ権限を許可する。
3. B のロールは呼び出しでキー ARN か別名 ARN を指定する。
4. スロットリングは B（呼び出し側）に計上される。

別名を使う場合は別名 ARN にします。`alias/app-key` のように書くと、B のアカウントの別名を探して `NotFoundException` になります。

片方だけだと `AccessDeniedException` です。

- **例:** A = `111122223333`、B = `444455556666`。B のロールが S3 にある A の SSE-KMS オブジェクトを読むなら、バケットポリシーと B の IAM の `s3:GetObject` に加えて、A のキーポリシーと B の IAM の `kms:Decrypt` の、合計 4 か所が要る。

## 既定値と上限のまとめ {#numbers}

| 項目 | 値 |
| --- | --- |
| `Encrypt` の平文（対称） | 4,096 バイト |
| `Decrypt` の暗号文 | 6,144 バイト |
| `GenerateDataKey` の `NumberOfBytes` | 1〜1,024 |
| `GenerateRandom` | 1〜1,024 バイト |
| 自動ローテーションの期間 | 既定 365 日。90〜2,560 日 |
| オンデマンドローテーション | キーあたり 25 回 |
| AWS 管理キーのローテーション | 約 1 年ごと |
| 削除の待機期間 | 既定 30 日。7〜30 日 |
| カスタマー管理キー | リージョンあたり 100,000 |
| 別名 | キーあたり 50 |
| グラント | キーあたり 50,000 |
| 対称キーの暗号操作 | 秒間 10,000 / 20,000 / 100,000（リージョンによる） |
| RSA、楕円曲線の暗号操作 | 秒間 1,000 |
| S3 バケットキーの削減効果 | 最大 99% |

## 試験のポイント {#exam-points}

| こう問われたら | 答え |
| --- | --- |
| 4 KB を超えるデータを KMS で暗号化 | `GenerateDataKey` によるエンベロープ暗号化 |
| 大量の `GenerateDataKey` で `ThrottlingException` | データキーキャッシュ、バックオフ、上限の引き上げ |
| S3 の SSE-KMS でコストや呼び出し回数を減らす | S3 バケットキー |
| 誰がいつ鍵を使ったか監査したい | カスタマー管理キーと CloudTrail |
| AWS にも平文を見せたくない | クライアント側暗号化（AWS Encryption SDK） |
| IAM で許可したのにキーを使えない | キーポリシーに、IAM を有効にする文や主体の許可がない |
| 別アカウントのキーを使う | キーポリシーと IAM の両方の許可、キー ARN の指定 |
| AWS 管理キーのデータを他アカウントと共有 | できない。カスタマー管理キーで再暗号化する |
| 自動ローテーションの期間 | 既定 365 日。90〜2560 日で指定できる |
| ローテーション後に古いデータは | 古い鍵素材は保持され、そのまま復号できる |
| 非対称キーのローテーション | 自動は不可。新しいキーと別名の切り替え |
| 復号で `InvalidCiphertextException` | 暗号化コンテキストの不一致など |
| AWS サービスに一時的に権限を委譲 | グラント |
| 特定サービス経由でのみ鍵を使わせる | `kms:ViaService` |
| 環境変数の暗号化ヘルパーを使う Lambda の権限 | 実行ロールに `kms:Decrypt` |
| キーの削除の待機期間 | 7〜30 日。既定は 30 日 |
| ランダムなバイト列を KMS で作る | `GenerateRandom`（1〜1,024 バイト） |
| 今は平文のキーが要らない | `GenerateDataKeyWithoutPlaintext` |
| KMS の外の相手に公開鍵だけ渡して暗号化させる | 非対称の RSA キー |
| 別リージョンで再暗号化なしに復号したい | マルチリージョンキー |
| 待機期間なしで鍵素材を消したい | インポートした鍵素材と `DeleteImportedKeyMaterial` |
| グラントをすぐに使う | `GrantToken` を渡す |

## 関連ページ {#related}

- [IAM と STS](iam.md): ポリシー評価とクロスアカウント
- [Secrets Manager と Parameter Store](secrets.md): シークレットの暗号化
- [証明書と WAF](certificates.md): 転送時の暗号化
- [S3](s3.md): サーバー側暗号化の詳細
- [Lambda](lambda.md): 環境変数
- [DynamoDB](dynamodb.md): 保存時の暗号化

## 参考 {#references}

- [AWS KMS keys](https://docs.aws.amazon.com/kms/latest/developerguide/concepts.html)
- [Default key policy](https://docs.aws.amazon.com/kms/latest/developerguide/key-policy-default.html)
- [Grants in AWS KMS](https://docs.aws.amazon.com/kms/latest/developerguide/grants.html)
- [Encrypt API](https://docs.aws.amazon.com/kms/latest/APIReference/API_Encrypt.html)
- [GenerateDataKey API](https://docs.aws.amazon.com/kms/latest/APIReference/API_GenerateDataKey.html)
- [Encryption context](https://docs.aws.amazon.com/kms/latest/developerguide/encrypt_context.html)
- [Request quotas](https://docs.aws.amazon.com/kms/latest/developerguide/requests-per-second.html)
- [Throttling AWS KMS requests](https://docs.aws.amazon.com/kms/latest/developerguide/throttling.html)
- [Rotate AWS KMS keys](https://docs.aws.amazon.com/kms/latest/developerguide/rotate-keys.html)
- [EnableKeyRotation API](https://docs.aws.amazon.com/kms/latest/APIReference/API_EnableKeyRotation.html)
- [Perform on-demand key rotation](https://docs.aws.amazon.com/kms/latest/developerguide/rotating-keys-on-demand.html)
- [Allowing users in other accounts to use a KMS key](https://docs.aws.amazon.com/kms/latest/developerguide/key-policy-modifying-external-accounts.html)
- [Aliases in AWS KMS](https://docs.aws.amazon.com/kms/latest/developerguide/kms-alias.html)
- [ScheduleKeyDeletion API](https://docs.aws.amazon.com/kms/latest/APIReference/API_ScheduleKeyDeletion.html)
- [AWS Encryption SDK](https://docs.aws.amazon.com/encryption-sdk/latest/developer-guide/introduction.html)
- [Data key caching](https://docs.aws.amazon.com/encryption-sdk/latest/developer-guide/data-key-caching.html)
- [Securing Lambda environment variables](https://docs.aws.amazon.com/lambda/latest/dg/configuration-envvars-encryption.html)
- [Protecting data with encryption in Amazon S3](https://docs.aws.amazon.com/AmazonS3/latest/userguide/UsingEncryption.html)
- [Reducing the cost of SSE-KMS with S3 Bucket Keys](https://docs.aws.amazon.com/AmazonS3/latest/userguide/bucket-key.html)
- [DynamoDB encryption at rest](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/EncryptionAtRest.html)
- [Encrypting Amazon RDS resources](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Overview.Encryption.html)
- [Parameter Store SecureString and KMS](https://docs.aws.amazon.com/systems-manager/latest/userguide/secure-string-parameter-kms-encryption.html)
- [Amazon SQS server-side encryption](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-server-side-encryption.html)

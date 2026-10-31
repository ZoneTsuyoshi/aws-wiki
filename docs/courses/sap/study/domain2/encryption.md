# 分野2: 暗号化と鍵管理

鍵をどこに置き、誰が管理するのかの判断を問います。KMS、インポート、CloudHSM、外部キーストアの違いと、耐量子暗号の優先順位を押さえます。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [2.2.1](../../domain2.md#skill-2-2-1) | カスタマー管理キーと自動ローテーション |
| [2.2.2](../../domain2.md#skill-2-2-2) | 証明書管理と転送時の暗号化 |
| [2.2.3](../../domain2.md#skill-2-2-3) | 専用のハードウェアセキュリティモジュール |
| [2.2.4](../../domain2.md#skill-2-2-4) | 耐量子暗号の戦略 |

## 学習の順番 {#study-order}

1. [KMS キーの種類](../../../../services/kms.md#key-types)と[アカウントをまたぐ暗号化](../../../../services/kms.md#cross-account): AWS 管理キーを共有できない理由を確認します。
2. [キーのローテーション](../../../../services/kms.md#key-rotation)と[ローテーションの設定](../../../../services/kms.md#rotation-settings): 自動とオンデマンドの対象を表で覚えます。
3. [マルチリージョンキー](../../../../services/kms.md#multi-region-keys)と[鍵素材のインポート](../../../../services/kms.md#imported-key-material): 選ぶ理由と制約をつかみます。
4. [S3 Bucket Key](../../../../services/s3.md#bucket-key): 費用を減らす仕組みと、既存のオブジェクトの扱いを確認します。
5. [リージョンのルール](../../../../services/certificates.md#region-rules)、[証明書のインポート](../../../../services/certificates.md#import)、[転送時の TLS](../../../../services/certificates.md#tls-in-transit)、[mTLS](../../../../services/certificates.md#mtls): 終端の場所と更新の責任を整理します。
6. [KMS との比較](../../../../services/identity-directory.md#cloudhsm-vs-kms)、[クラスター](../../../../services/identity-directory.md#cloudhsm-clusters)、[KMS の CloudHSM キーストア](../../../../services/identity-directory.md#cloudhsm-key-store): CloudHSM を選ぶ条件と、可用性の責任を覚えます。
7. [キーの仕様](../../../../services/kms.md#key-specs)と[主な条件キー](../../../../services/kms.md#kms-condition-keys): ML-DSA と ML-KEM の用途と、作成の制限を確認します。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| 自動ローテーションの周期 | 既定 365 日。90〜2,560 日 | 対称で KMS が生成した鍵素材 |
| オンデマンドローテーション | 最大 25 回 | 計画外のとき。インポートした対称キーも可 |
| キーの削除の待機期間 | 7〜30 日 | インポートした鍵素材は待機なしで消せる |
| CloudHSM キーストアの HSM | 異なる AZ に 2 台以上 | 満たさないと接続できない |
| ML-DSA のキー仕様 | `ML_DSA_44`、`ML_DSA_65`、`ML_DSA_87` | 署名と検証 |
| ML-KEM のキー仕様 | `ML_KEM_512`、`ML_KEM_768`、`ML_KEM_1024` | カプセル化と非カプセル化 |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| RDS のスナップショットを別アカウントへ共有する | カスタマー管理キーでコピーし、キーポリシーで相手を許可する |
| 周期を指定してアプリの変更なしで鍵素材を更新する | 自動ローテーションの周期を設定する |
| 別のリージョンの暗号文を、リージョン間の呼び出しなしで復号する | マルチリージョンキー |
| 自社で作った鍵素材を、待機なしで消したい | 鍵素材のインポートと `DeleteImportedKeyMaterial` |
| SSE-KMS の費用とスロットリングを減らす | S3 バケットキー。既存のオブジェクトはコピーする |
| ロードバランサーでも復号してはいけない | NLB の TCP リスナーで通過させる |
| ALB でクライアント証明書を検証する | mTLS の検証モードとトラストストア |
| インポートした証明書の期限切れを防ぐ | 期限のイベントで通知し、同じ ARN へ再インポートする |
| PKCS#11 と単一テナントの HSM | CloudHSM を複数の AZ に |
| AWS サービスの統合のまま、鍵を単一テナントの HSM に | KMS の CloudHSM キーストア |
| 鍵を AWS の外に置いて使う規制 | KMS の外部キーストア |
| 長期の秘匿と量子計算機への備え | 鍵交換を先に。AES-256-GCM は変更不要 |
| 長期間検証する署名 | ML-DSA |

## 引っかかりやすい点 {#traps}

- ローテーションは既存のデータを再暗号化しません。キーの ID も変わりません。
- 非対称、HMAC、カスタムキーストアのキーはローテーションに対応しません。新しいキーを作り、別名を切り替えます。
- CloudFront の証明書は `us-east-1` です。ALB の証明書は ALB と同じリージョンです。
- NLB の TLS リスナーはロードバランサーで終端します。通過させるのは TCP リスナーです。
- インポートした鍵素材は KMS の中に入ります。「AWS の外で鍵を使う」要件は外部キーストアです。
- RSA の鍵長を上げても、量子計算機への根本的な対策になりません。
- ML-KEM は鍵の確立の方式で、署名には使えません。キー仕様は作成後に変更できません。
- ALB の `TLS13-1-3` のポリシーは TLS 1.3 だけです。TLS 1.2 のクライアントを残すなら `TLS13-1-2` の PQ を選びます。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [encryption 問1](../../exercises/encryption.md#q1) | 2.2.1 | ある会社は RDS の本番データベースを AWS 管理キー（aws/rds）で暗号化しています。規制… |
| [encryption 問2](../../exercises/encryption.md#q2) | 2.2.1 | ある会社の規定では、暗号鍵の鍵素材を 180 日ごとに更新する必要があります。対象は KMS が生成… |
| [encryption 問3](../../exercises/encryption.md#q3) | 2.2.1 | ある決済サービスは、2 つのリージョンでアクティブ/アクティブに動いています。アプリはクライアント側… |
| [encryption 問4](../../exercises/encryption.md#q4) | 2.2.1 | ある銀行の規定では、S3 と EBS の暗号化の鍵素材を社内の HSM で生成する必要があります。ま… |
| [encryption 問5](../../exercises/encryption.md#q5) | 2.2.1 | あるデータレイクでは、数十億のオブジェクトを 1 つのカスタマー管理キーによる SSE-KMS で保… |
| [encryption 問6](../../exercises/encryption.md#q6) | 2.2.2 | ある EC サイトは、CloudFront を東京リージョンの ALB の前に置いています。独自ドメ… |
| [encryption 問7](../../exercises/encryption.md#q7) | 2.2.2 | ある工場の機器は、第三者の CA が発行したクライアント証明書を持ち、ALB の背後の HTTP サ… |
| [encryption 問8](../../exercises/encryption.md#q8) | 2.2.2 | あるカード決済のサービスでは、利用者の端末からコンテナのアプリまで、途中で平文にならないことが監査の… |
| [encryption 問9](../../exercises/encryption.md#q9) | 2.2.2 | ある会社は契約の都合で、外部の CA が発行した証明書を ACM にインポートして ALB で使って… |
| [encryption 問10](../../exercises/encryption.md#q10) | 2.2.3 | ある決済アプリは、PKCS#11 で HSM を呼び、独自のアルゴリズムの指定で鍵を操作します。監査… |
| [encryption 問11](../../exercises/encryption.md#q11) | 2.2.3 | ある保険会社は、S3、EBS、RDS の暗号化を標準の AWS サービスの統合のまま使いたいと考えて… |
| [encryption 問12](../../exercises/encryption.md#q12) | 2.2.3 | ある設計者は KMS の CloudHSM キーストアを使う案をレビューしています。この案で必ず考慮… |
| [encryption 問13](../../exercises/encryption.md#q13) | 2.2.4 | ある医療機関は、記録を 30 年間秘匿する必要があります。データは S3 の SSE-KMS（AES… |
| [encryption 問14](../../exercises/encryption.md#q14) | 2.2.4 | ある機器メーカーは、15 年間使われる機器のファームウェアに署名します。機器は出荷後も公開鍵で署名を… |
| [encryption 問15](../../exercises/encryption.md#q15) | 2.2.4 | ある組織は耐量子への移行を進めています。ある OU では、新しく作る非対称の署名キーを ML-DSA… |
| [encryption 問16](../../exercises/encryption.md#q16) | 2.2.4 | ある会社は公開 API を ALB で提供しています。新しいクライアントには ML-KEM を含むハ… |

<!-- questions:end -->

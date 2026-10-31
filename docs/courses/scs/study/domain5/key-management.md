# 分野5: 鍵と証明書の管理

鍵素材の出どころと場所の選択、責任の変化、複数リージョンでの鍵と証明書の扱いを問います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [5.3.2](../../domain5.md#skill-5-3-2) | インポートした鍵素材と外部キーストア |
| [5.3.3](../../domain5.md#skill-5-3-3) | インポートした鍵素材と AWS 生成の違い |
| [5.3.5](../../domain5.md#skill-5-3-5) | 単一または複数リージョンの鍵と証明書 |

## 学習の順番 {#study-order}

1. [鍵素材のインポート](../../../../services/kms.md#imported-key-material): 手順と、AWS 生成との違いを覚えます。
2. [キーの無効化と削除](../../../../services/kms.md#disable-delete)と[ローテーションの設定](../../../../services/kms.md#rotation-settings): 待機期間と自動ローテーションの可否を確認します。
3. [CloudHSM キーストア](../../../../services/identity-directory.md#cloudhsm-key-store): カスタムキーストアでできないことを押さえます。
4. [マルチリージョンキー](../../../../services/kms.md#multi-region-keys)と[キーポリシーの詳細](../../../../services/kms.md#key-policy-details): 共有されるものと別々のものを分けます。
5. [リージョンのルール](../../../../services/certificates.md#region-rules)と[自動更新](../../../../services/certificates.md#auto-renewal): 証明書の置き場所と更新の条件を覚えます。
6. [Private CA](../../../../services/certificates.md#private-ca)と [Private CA の設定](../../../../services/certificates.md#private-ca-settings): 短期証明書モードとリージョンの制約を確認します。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| キーの削除の待機 | 7〜30 日、既定 30 日 | 0 日にはできない |
| 自動ローテーション | 90〜2,560 日、既定 365 日 | インポートのキーは不可 |
| 短期証明書モード | 最大 7 日 | 失効の仕組みを省ける場合がある |
| 標準キーストアの SLA | 99.999% | 外部キーストアに SLA はない |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 鍵を AWS の外に置き、接続を切ると使えなくする | 外部キーストア |
| 待機なしで鍵素材を消し、後で戻す | インポートと `DeleteImportedKeyMaterial` |
| 鍵素材の生成元を証明する | インポート |
| 期限切れでキーが使えない | `PendingImport`。同じ鍵素材を再度インポート |
| 非対称、HMAC、マルチリージョンのキーが必要 | 標準キーストア |
| 別のリージョンでも再暗号化なしで復号 | マルチリージョンキー。既存のキーは変換できない |
| CloudFront に証明書を付ける | `us-east-1` の ACM |
| 短期間の内部証明書を大量に発行 | Private CA の短期証明書モード |
| 統合サービスで自動更新を使う | ACM から要求する |

## 引っかかりやすい点 {#traps}

- 鍵素材をインポートしても、対称の KMS の暗号文を KMS の外で復号できません。
- インポートのキーの耐久性は利用者の責任です。元のコピーを失うと復号できません。
- XKS プロキシは利用者が用意して運用します。
- キーポリシーはレプリカと同期されません。リージョンごとに管理します。
- Private CA と ACM の証明書は、リージョン間でコピーできません。
- `IssueCertificate` で発行した証明書とインポートした証明書は、自動更新されません。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [key-management 問1](../../exercises/key-management.md#q1) | 5.3.2 | 規制により、鍵を AWS の外に置き、外部の鍵マネージャーへの接続を切ることでデータを即座に使えなく… |
| [key-management 問2](../../exercises/key-management.md#q2) | 5.3.2 | 既存の HSM で生成した鍵素材を KMS にインポートします。正しい手順の順序はどれですか。 |
| [key-management 問3](../../exercises/key-management.md#q3) | 5.3.2 | 外部キーストアの導入を検討しています。経営層に、責任の変化を説明します。正しい説明を選んでください。… |
| [key-management 問4](../../exercises/key-management.md#q4) | 5.3.2 | カスタムキーストアの利用を検討している 3 つの要望が出ました。「非対称キーで署名する」「HMAC … |
| [key-management 問5](../../exercises/key-management.md#q5) | 5.3.3 | 重要なデータを暗号化しているキーについて、インシデントの発生時に待機期間なしで鍵素材を消し、後で元に… |
| [key-management 問6](../../exercises/key-management.md#q6) | 5.3.3 | インポートした鍵素材に ValidTo を設定したキーで、期限が過ぎるとアプリが暗号化も復号もできな… |
| [key-management 問7](../../exercises/key-management.md#q7) | 5.3.3 | 担当者は「鍵素材をインポートすれば、KMS で暗号化した対称の暗号文を社内の HSM でも復号できる… |
| [key-management 問8](../../exercises/key-management.md#q8) | 5.3.3 | インポートする鍵素材を検討するときの、次の 4 つの要望があります。この中で、AWS 生成の鍵素材で… |
| [key-management 問9](../../exercises/key-management.md#q9) | 5.3.5 | マルチリージョンキーのプライマリを東京に作り、大阪にレプリカを作りました。セキュリティチームは東京の… |
| [key-management 問10](../../exercises/key-management.md#q10) | 5.3.5 | 既存の単一リージョンのカスタマー管理キーで暗号化したデータを、別のリージョンでも再暗号化なしで復号で… |
| [key-management 問11](../../exercises/key-management.md#q11) | 5.3.5 | 東京の ALB と、グローバルな CloudFront に同じドメインのパブリック証明書を付けます。… |
| [key-management 問12](../../exercises/key-management.md#q12) | 5.3.5 | 社内のマイクロサービスの mTLS に数千の証明書が必要で、毎日発行します。有効期間は 3 日で十分… |
| [key-management 問13](../../exercises/key-management.md#q13) | 5.3.5 | 東京の Private CA で発行した証明書を、シンガポールのサービスでも使いたいと考えています。… |

<!-- questions:end -->

# 分野6: データ保護

データの分類から暗号化、認証情報の更新までの自動化を問います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [ローテーション](../../domain6.md#t6-1-rotation) | 認証情報のローテーションの自動化 |
| [データ管理](../../domain6.md#t6-2-data-management) | データ管理 |
| [Macie](../../domain6.md#t6-2-macie) | 機密データの検出の自動化 |
| [暗号化](../../domain6.md#t6-2-encryption) | 転送時と保存時の暗号化 |

## 学習の順番 {#study-order}

1. [ローテーション](../../../../services/secrets.md#rotation): 関数と経路を確認します。
2. [取得とクライアント側キャッシュ](../../../../services/secrets.md#retrieval-caching): キャッシュの注意を押さえます。
3. [キーのローテーション](../../../../services/kms.md#key-rotation): 既存のデータの扱いを覚えます。
4. [検出の方法](../../../../services/threat-detection.md#macie-discovery): 自動の検出とジョブの違いを確認します。
5. [識別子と許可リスト](../../../../services/threat-detection.md#macie-identifiers): 識別子と許可リストを確認します。
6. [KMS との比較](../../../../services/identity-directory.md#cloudhsm-vs-kms): 選ぶ基準を押さえます。
7. [バケットのデフォルト暗号化とポリシーによる強制](../../../../services/s3.md#enforcing-encryption): ポリシーでの強制を確認します。

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 独自の API キーのローテーション | Lambda のローテーション関数 |
| 特定のバケットを確実に調べる | Macie の検出ジョブ |
| 独自の形式を検出する | カスタムの識別子 |
| 専有の HSM が必須 | CloudHSM |
| HTTPS に限定する | `aws:SecureTransport` |
| EBS を必ず暗号化する | アカウントのデフォルト暗号化 |

## 引っかかりやすい点 {#traps}

- Parameter Store には自動ローテーションがありません。
- 自動ローテーションは既存のデータを再暗号化しません。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [data-protection 問1](../../exercises/data-protection.md#q1) | ローテーション | RDS のパスワードを 30 日ごとに自動で変更します。ローテーションの Lambda は VPC … |
| [data-protection 問2](../../exercises/data-protection.md#q2) | ローテーション | ローテーションの後、一部のアプリがしばらくデータベースの認証エラーになります。Secrets Man… |
| [data-protection 問3](../../exercises/data-protection.md#q3) | ローテーション | 次の機械の ID の認証情報を整理します。自動ローテーションの方法の組み合わせはどれですか。(1) … |
| [data-protection 問4](../../exercises/data-protection.md#q4) | データ管理 | 組織のデータ保護の方針を実装します。次の工程と手段の組み合わせとして正しいものはどれですか。(1) … |
| [data-protection 問5](../../exercises/data-protection.md#q5) | データ管理 | キーの管理の方針の見直しです。担当者の理解のうち、正しいものを選んでください。（2つ選択） |
| [data-protection 問6](../../exercises/data-protection.md#q6) | データ管理 | S3 のデータレイクを Athena で分析します。列のレベルで部署ごとにアクセスを制御します。1 … |
| [data-protection 問7](../../exercises/data-protection.md#q7) | Macie | 500 個の S3 バケットを持つ組織で、機密データの傾向を費用を抑えて継続的に把握します。一方、四… |
| [data-protection 問8](../../exercises/data-protection.md#q8) | Macie | 社員番号 EMP- で始まる 8 桁の値を検出したいのですが、Macie のマネージドの識別子で見つ… |
| [data-protection 問9](../../exercises/data-protection.md#q9) | Macie | 委任管理者で Macie を組織に有効にしました。機密データの検出結果が出たら、担当へ通知し、バケッ… |
| [data-protection 問10](../../exercises/data-protection.md#q10) | 暗号化 | 規制で、鍵の管理を自社の担当者だけが行う FIPS の専有の HSM が必須です。ただし S3 や … |
| [data-protection 問11](../../exercises/data-protection.md#q11) | 暗号化 | 組織の基準を強制します。(1) S3 への HTTP のアクセスを拒否する。(2) 新しい EBS … |
| [data-protection 問12](../../exercises/data-protection.md#q12) | 暗号化 | 医療データを扱うチームの要件です。(1) ロードバランサーから利用者まで TLS で通信する。(2)… |

<!-- questions:end -->

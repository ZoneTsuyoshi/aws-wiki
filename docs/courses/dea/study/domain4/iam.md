# 分野4: IAM とネットワークの権限

セキュリティグループ、ロール、ポリシー、責任の分担を問います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [4.1.1](../../domain4.md#skill-4-1-1) | VPC セキュリティグループの更新 |
| [4.1.2](../../domain4.md#skill-4-1-2) | IAM グループ、ロール、エンドポイント、サービス |
| [4.1.4](../../domain4.md#skill-4-1-4) | アクセス用の IAM ロールの設定 |
| [4.1.5](../../domain4.md#skill-4-1-5) | ロール、エンドポイント、サービスへのポリシーの適用 |
| [4.1.6](../../domain4.md#skill-4-1-6) | マネージドサービスとアンマネージドサービスの違い |
| [4.2.1](../../domain4.md#skill-4-2-1) | カスタム IAM ポリシーの作成 |
| [4.2.6](../../domain4.md#skill-4-2-6) | 最小権限のカスタムポリシー |

## 学習の順番 {#study-order}

1. [セキュリティグループのルール](../../../../services/networking.md#security-group-rules): 参照とステートフルを確認します。
2. [信頼ポリシー](../../../../services/iam.md#trust-policy): 権限ポリシーとの違いを覚えます。
3. [iam:PassRole](../../../../services/iam.md#passrole): エラーの原因を確認します。
4. [ポリシーの要素](../../../../services/iam.md#policy-elements): バケットとオブジェクトの ARN を区別します。
5. [エンドポイントポリシー](../../../../services/networking.md#endpoint-policies): 権限を与えないことを理解します。
6. [責任共有モデル](../../../../services/cloud-foundations.md#shared-responsibility): マネージドの線引きを確認します。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| MSK のポート | IAM 9098、SCRAM 9096、TLS 9094、平文 9092 | VPC 内の接続 |
| EFS | 2049 番 | Lambda の SG から許可 |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| サービスに権限を渡す | IAM ロール |
| ロールを渡せない | `iam:PassRole` |
| バケットポリシーを用途で分ける | S3 Access Points |
| Glue がロールを引き受けられない | `Principal` が `glue.amazonaws.com` |
| 権限の上限を決める | 権限境界 |
| 使っていない権限を見つける | Access Analyzer |

## 引っかかりやすい点 {#traps}

- `ListBucket` はバケットの ARN、`GetObject` はオブジェクトの ARN です。
- マネージドでもデータの暗号化と権限は利用者の責任です。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [iam 問1](../../exercises/iam.md#q1) | 4.1.1 | Glue ジョブから RDS へ接続します。接続元の IP は変わります。RDS のセキュリティグル… |
| [iam 問2](../../exercises/iam.md#q2) | 4.1.1 | MSK のクライアントが IAM 認証で接続できません。VPC 内の接続で、セキュリティグループに許… |
| [iam 問3](../../exercises/iam.md#q3) | 4.1.1 | 接続できないときの確認で正しいものはどれですか。（2つ選択） |
| [iam 問4](../../exercises/iam.md#q4) | 4.1.2 | データアナリスト 30 人に同じ権限を付けます。Glue のジョブには S3 の権限を渡します。正し… |
| [iam 問5](../../exercises/iam.md#q5) | 4.1.2 | データエンジニアが Glue のジョブを作成すると、iam:PassRole の権限エラーになります… |
| [iam 問6](../../exercises/iam.md#q6) | 4.1.2 | VPC 内の処理から S3 と KMS へ、インターネットを経由せず接続します。何を使いますか。 |
| [iam 問7](../../exercises/iam.md#q7) | 4.1.4 | Glue のジョブがロールを引き受けられず失敗します。権限ポリシーは正しいです。信頼ポリシーで確認す… |
| [iam 問8](../../exercises/iam.md#q8) | 4.1.4 | Lambda から Kinesis を読み、ログも CloudWatch に出します。どのロールに権… |
| [iam 問9](../../exercises/iam.md#q9) | 4.1.4 | ロールの渡し方の組み合わせで正しいものはどれですか。（2つ選択） |
| [iam 問10](../../exercises/iam.md#q10) | 4.1.5 | 1 つのバケットを使う部署が増え、バケットポリシーが巨大です。部署ごとにプレフィックスとネットワーク… |
| [iam 問11](../../exercises/iam.md#q11) | 4.1.5 | S3 のゲートウェイエンドポイントのポリシーで、許可した操作を絞りました。説明として正しいものはどれ… |
| [iam 問12](../../exercises/iam.md#q12) | 4.1.5 | 分析バケットを、特定の VPC エンドポイントからだけ読ませます。アクセスポイントを使う場合の評価も… |
| [iam 問13](../../exercises/iam.md#q13) | 4.1.6 | 運用の負荷を最小にして Kafka を使います。責任の説明として正しいものはどれですか。 |
| [iam 問14](../../exercises/iam.md#q14) | 4.1.6 | EC2 上で独自の Spark クラスターを動かす場合に、Glue と比べて利用者が新たに担うものは… |
| [iam 問15](../../exercises/iam.md#q15) | 4.1.6 | アンマネージドの構成を選ぶ根拠として適切なものはどれですか。 |
| [iam 問16](../../exercises/iam.md#q16) | 4.2.1 | lake バケットの curated/ だけを一覧して読むポリシーを書きます。s3:ListBuck… |
| [iam 問17](../../exercises/iam.md#q17) | 4.2.1 | lake バケットの s3:ListBucket で、curated/ の下だけを一覧させる条件はど… |
| [iam 問18](../../exercises/iam.md#q18) | 4.2.1 | カスタムポリシーの評価の説明で正しいものはどれですか。 |
| [iam 問19](../../exercises/iam.md#q19) | 4.2.6 | Glue のジョブロールを最小権限にします。適切なものはどれですか。 |
| [iam 問20](../../exercises/iam.md#q20) | 4.2.6 | データエンジニアが自分で Glue 用のロールを作りますが、管理者権限のロールを作れないようにします… |
| [iam 問21](../../exercises/iam.md#q21) | 4.2.6 | 使っていない権限を見つけ、バケットの外部からのアクセスも検出します。何を使いますか。 |

<!-- questions:end -->

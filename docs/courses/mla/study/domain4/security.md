# 分野4: セキュリティ

最小権限、ロールの渡し方、監査の記録先、拒否の調査、ネットワークの分離、Bedrock の認証情報を問います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [4.3.2](../../domain4.md#skill-4-3-2) | 成果物への最小権限 |
| [4.3.3](../../domain4.md#skill-4-3-3) | 利用者とアプリの IAM ポリシーとロール |
| [4.3.4](../../domain4.md#skill-4-3-4) | 監視、監査、コンプライアンス、ログ |
| [4.3.5](../../domain4.md#skill-4-3-5) | セキュリティの問題の調査 |
| [4.3.6](../../domain4.md#skill-4-3-6) | VPC、サブネット、セキュリティグループによる分離 |
| [4.3.8](../../domain4.md#skill-4-3-8) | FM にアクセスする認証情報の選択 |

## 学習の順番 {#study-order}

1. [最小権限](../../../../services/iam.md#least-privilege)と [IAM と暗号化](../../../../services/sagemaker.md#iam-encryption): 主体ごとの権限を確認します。
2. [iam:PassRole](../../../../services/iam.md#passrole)と [Bedrock の IAM のスコープ](../../../../services/ai.md#iam-scope): 安全な書き方を覚えます。
3. [CloudTrail との違い](../../../../services/governance.md#config-vs-cloudtrail)と[モデル呼び出しログ](../../../../services/ai.md#invocation-logging): 監査の記録先を押さえます。
4. [DecodeAuthorizationMessage](../../../../services/iam.md#decode-authorization)と[ポリシーシミュレーター](../../../../services/iam.md#policy-simulator): 調査のツールを確認します。
5. [VPC とネットワーク分離](../../../../services/sagemaker.md#vpc-isolation)と [Bedrock の VPC エンドポイント](../../../../services/ai.md#privatelink): 閉域の設計を覚えます。
6. [Bedrock API キー](../../../../services/ai.md#api-keys): キーの種類と制御を確認します。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| 短期 API キー | 最大 12 時間 | SigV4 を使いにくいクライアントの本番 |
| 長期 API キー | 設定した期限まで | 検証のみ |
| 環境変数 | `AWS_BEARER_TOKEN_BEDROCK` | |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| ジョブの作成が拒否される | `iam:PassRole` |
| S3 の権限があるのに読めない | KMS のキーポリシーとロール |
| 推論プロファイルの権限 | プロファイルと経路上の各リージョンの基盤モデル |
| 誰が API を呼んだか | CloudTrail |
| 設定がルールに準拠しているか | Config |
| S3 と DynamoDB へ閉域で | ゲートウェイエンドポイント |
| Bedrock へ閉域で | インターフェイスエンドポイント |
| AWS 上のアプリの認証 | IAM ロール |

## 引っかかりやすい点 {#traps}

- `iam:PassRole` を `*` にすると権限の昇格につながります。`iam:PassedToService` も付けます。
- 呼び出しログの `input` はガードレールが介入しても元のリクエストのままです。
- 分離モードでスクリプトが S3 を読めないのは仕様です。入力チャネル経由で受け取ります。
- サーバーレス推論は VPC の設定に対応しません。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [security 問4](../../exercises/security.md#q4) | 4.3.2 | 学習ジョブの実行ロールに S3 の権限を付けます。学習データは 1 つのバケットの projects… |
| [security 問5](../../exercises/security.md#q5) | 4.3.2 | カスタマーマネージドキーで暗号化した学習データを読めません。ロールの S3 の権限はあります。確認す… |
| [security 問6](../../exercises/security.md#q6) | 4.3.2 | 推論プロファイルで Bedrock のモデルを呼びます。bedrock:InvokeModel の … |
| [security 問7](../../exercises/security.md#q7) | 4.3.3 | データサイエンティストに学習ジョブの作成を許可します。実行ロールを渡す権限の安全な書き方はどれですか… |
| [security 問8](../../exercises/security.md#q8) | 4.3.3 | 次の主体と権限の組み合わせとして適切なものを選んでください。（2つ選択） |
| [security 問9](../../exercises/security.md#q9) | 4.3.3 | 学習ジョブがコンテナの中から S3 と ECR にアクセスします。この権限はどの主体に付けますか。 |
| [security 問10](../../exercises/security.md#q10) | 4.3.4 | 次の監査の要件と記録先の組み合わせとして正しいものを選んでください。（2つ選択） |
| [security 問11](../../exercises/security.md#q11) | 4.3.4 | 監査のために Bedrock の呼び出しログを有効にします。ガードレールでブロックされた内容はログに… |
| [security 問12](../../exercises/security.md#q12) | 4.3.4 | Bedrock のプロンプトと応答を記録する機能の既定の状態はどれですか。 |
| [security 問13](../../exercises/security.md#q13) | 4.3.5 | EnableNetworkIsolation を有効にした学習ジョブで、スクリプトが S3 を直接読… |
| [security 問14](../../exercises/security.md#q14) | 4.3.5 | 学習ジョブの作成が拒否され、エラーはロールに関するものです。sagemaker:CreateTrai… |
| [security 問15](../../exercises/security.md#q15) | 4.3.5 | AccessDenied のエラーに暗号化されたメッセージが付いていました。内容を読む方法と、調査に… |
| [security 問16](../../exercises/security.md#q16) | 4.3.6 | インターネットを経由せずに、VPC 内から S3 と Bedrock を呼びます。エンドポイントの種… |
| [security 問17](../../exercises/security.md#q17) | 4.3.6 | 分散学習のノード間の通信も暗号化します。規制の要件で、学習時間が少し延びても構いません。どの設定です… |
| [security 問18](../../exercises/security.md#q18) | 4.3.6 | VPC 必須の規制環境で、断続的な推論にサーバーレス推論を選ぼうとしています。判断として正しいものは… |
| [security 問19](../../exercises/security.md#q19) | 4.3.8 | ECS で動くアプリから Bedrock を呼びます。長期の認証情報を持たせない設計はどれですか。 |
| [security 問20](../../exercises/security.md#q20) | 4.3.8 | SigV4 を使いにくい既存のクライアントから Bedrock を呼びます。本番で使う API キー… |
| [security 問21](../../exercises/security.md#q21) | 4.3.8 | Bedrock の API キーの管理を統制します。正しい組み合わせを選んでください。（2つ選択） |

<!-- questions:end -->

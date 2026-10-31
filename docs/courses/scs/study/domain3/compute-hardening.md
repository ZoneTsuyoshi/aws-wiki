# 分野3: コンピューティングの強化

イメージ、ロール、パッチ、管理アクセスの4点で、コンピューティングの攻撃面を減らす方法を問います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [3.2.1](../../domain3.md#skill-3-2-1) | AMI とコンテナイメージの強化 |
| [3.2.2](../../domain3.md#skill-3-2-2) | ロールの適切な適用 |
| [3.2.4](../../domain3.md#skill-3-2-4) | パッチの展開と継続的な検証 |
| [3.2.5](../../domain3.md#skill-3-2-5) | 安全な管理アクセス |

## 学習の順番 {#study-order}

1. [EC2 Image Builder](../../../../services/operations.md#image-builder)と [AMI の管理](../../../../services/operations.md#amis): ビルドから配布、廃棄までの流れを確認します。
2. [タグと不変タグ](../../../../services/containers.md#image-tags): コンテナイメージの上書きを防ぐ設定を押さえます。
3. [インスタンスプロファイル](../../../../services/iam.md#instance-profile)と[タスクロールと実行ロール](../../../../services/containers.md#task-role-vs-execution-role): どのロールを誰が使うかを区別します。
4. [Pod の IAM](../../../../services/containers.md#pod-identity): Pod Identity と IRSA の違い、Fargate の扱いを確認します。
5. [PassRole](../../../../services/iam.md#passrole)と [IMDS](../../../../services/iam.md#imds): 権限の昇格と SSRF を防ぐ設定を覚えます。
6. [Patch Manager](../../../../services/operations.md#patch-manager)と[パッチベースライン](../../../../services/operations.md#patch-baselines): 実行の方法の範囲と、承認の待機を押さえます。
7. [インスタンスの更新](../../../../services/operations.md#instance-refresh)と[検出結果と管理](../../../../services/threat-detection.md#inspector-findings): 入れ替えと継続的な検証を確認します。
8. [Session Manager](../../../../services/operations.md#session-manager)と [EC2 の運用](../../../../services/operations.md#ec2-operations): ログの範囲と、Instance Connect の仕組みを比べます。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| 定義済みベースラインの承認 | 多くの OS でリリースの 7 日後 | 短くするならカスタムベースライン |
| Instance Connect の公開鍵 | メタデータに 60 秒 | その間に接続する |
| `maxTunnelDuration` | 1〜3,600 秒 | Instance Connect Endpoint の時間の上限 |
| Session Manager のアイドルタイムアウト | 既定 20 分。1〜60 分 | 入力があると延びる |
| IMDS のホップ制限 | 1〜64 | コンテナから届かせないなら 1 |
| Image Builder のライフサイクル | 1 日 1 回実行 | 配布先も対象にできる |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| ビルドで作った AMI を Inspector の有効化なしで検査 | `ON_DEMAND_AMI_CVE` と結果の条件 |
| ビルド用インスタンスでコンポーネントが動かない | `EC2InstanceProfileForImageBuilder` と `AmazonSSMManagedInstanceCore` |
| OU に AMI を使わせ、費用は中央で負担 | 起動の権限。OU にはコピーされない |
| 同じタグでの置き換えを防ぐ | ECR のタグを不変にする |
| コンテナのアプリに権限を与える | タスクロール。実行ロールはエージェント用 |
| Fargate の Pod に権限を与える | IRSA。Pod Identity は Fargate に対応しない |
| 起動テンプレートの IMDSv1 も止める | アカウントレベルの IMDSv2 の強制 |
| 複数アカウント、複数リージョンのパッチ | Quick Setup のパッチポリシー |
| ゼロデイの修正を今すぐ適用 | Patch now |
| コマンドの中身まで監査 | Session Manager のシェルのセッションとログ |
| パブリック IP のない Windows に手元の RDP で接続 | EC2 Instance Connect Endpoint |

## 引っかかりやすい点 {#traps}

- Session Manager の SSH とポート転送のセッションは、内容をログに残せません。ドキュメントごとに IAM で制限します。
- Session Manager の KMS 暗号化は、利用者とノードの両方にキーの権限が必要です。
- 起動時に指定した IMDS の値は、アカウントの既定や AMI の設定より優先されます。
- `iam:PassRole` を `ResourceTag` 条件で制御しても確実な結果になりません。ARN と `iam:PassedToService` で絞ります。
- SCP はサービスリンクロールに効きません。
- 承認されていないパッチは、実行の頻度を上げても適用されません。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [compute-hardening 問1](../../exercises/compute-hardening.md#q1) | 3.2.1 | ある会社は EC2 Image Builder で標準 AMI を作ります。次の要件があります。ビル… |
| [compute-hardening 問2](../../exercises/compute-hardening.md#q2) | 3.2.1 | EC2 Image Builder のパイプラインが、ビルドの段階で失敗するようになりました。ビルド… |
| [compute-hardening 問3](../../exercises/compute-hardening.md#q3) | 3.2.1 | ある組織は標準 AMI を毎週ビルドし、複数のアカウントとリージョンへ配布しています。古いバージョン… |
| [compute-hardening 問4](../../exercises/compute-hardening.md#q4) | 3.2.1 | 本番の ECS サービスは ECR の app:release というタグでイメージを取得しています… |
| [compute-hardening 問5](../../exercises/compute-hardening.md#q5) | 3.2.1 | 中央のアカウントで作った強化済み AMI を、組織の Workloads OU の全アカウントに使わ… |
| [compute-hardening 問6](../../exercises/compute-hardening.md#q6) | 3.2.2 | Fargate の ECS タスクを起動すると、イメージの取得とシークレットの注入は成功します。しか… |
| [compute-hardening 問7](../../exercises/compute-hardening.md#q7) | 3.2.2 | 開発者は Lambda 関数をデプロイするときに、チームのロールを渡します。監査で、開発者のポリシー… |
| [compute-hardening 問8](../../exercises/compute-hardening.md#q8) | 3.2.2 | EKS クラスターに、EC2 のマネージドノードの Pod と Fargate の Pod がありま… |
| [compute-hardening 問9](../../exercises/compute-hardening.md#q9) | 3.2.2 | ある Web アプリに SSRF の脆弱性が見つかり、IMDS からロールの認証情報が取られるリスク… |
| [compute-hardening 問10](../../exercises/compute-hardening.md#q10) | 3.2.2 | 組織の SCP で ec2:RunInstances を特定の AMI 以外で拒否しました。ところが… |
| [compute-hardening 問11](../../exercises/compute-hardening.md#q11) | 3.2.4 | 20 のアカウントと 4 つのリージョンで EC2 を運用しています。パッチのスキャンと適用を組織全… |
| [compute-hardening 問12](../../exercises/compute-hardening.md#q12) | 3.2.4 | Amazon Linux 2023 の EC2 を AWS-AmazonLinux2023Defau… |
| [compute-hardening 問13](../../exercises/compute-hardening.md#q13) | 3.2.4 | ゼロデイの脆弱性の修正パッチが公開されました。1 つのアカウントとリージョンの数十台に、次の定期実行… |
| [compute-hardening 問14](../../exercises/compute-hardening.md#q14) | 3.2.4 | Auto Scaling グループの Web サーバーは数日で入れ替わるので、起動時に古い AMI … |
| [compute-hardening 問15](../../exercises/compute-hardening.md#q15) | 3.2.5 | プライベートサブネットの Linux サーバーに管理者がアクセスします。監査の要件は、インバウンドポ… |
| [compute-hardening 問16](../../exercises/compute-hardening.md#q16) | 3.2.5 | Session Manager のログを S3 に残しています。監査で、一部の管理者のセッションの内… |
| [compute-hardening 問17](../../exercises/compute-hardening.md#q17) | 3.2.5 | Session Manager の設定で KMS キーによるセッションデータの暗号化を有効にしたとこ… |
| [compute-hardening 問18](../../exercises/compute-hardening.md#q18) | 3.2.5 | パブリック IP を持たない Windows インスタンスに、運用者が手元の RDP クライアントで… |
| [compute-hardening 問19](../../exercises/compute-hardening.md#q19) | 3.2.5 | Linux の開発環境で EC2 Instance Connect を使っています。SSH クライア… |

<!-- questions:end -->

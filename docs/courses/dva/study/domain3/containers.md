# 分野3: コンテナ

分野3では、イメージの作成と管理、タスク定義、ECS と EKS へのデプロイが問われます。タスクが起動しないときの調査やスケーリングは[分野4のコンテナ](../domain4/containers.md) で扱います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [3.1.1](../../domain3.md#skill-3-1-1) | イメージに含める依存関係と環境変数 |
| [3.1.2](../../domain3.md#skill-3-1-2) | Dockerfile、ECR、タグ、ライフサイクルポリシー |
| [3.2.4](../../domain3.md#skill-3-2-4) | イメージタグによる環境の分離 |
| [3.3.2](../../domain3.md#skill-3-3-2) | タスク定義、マニフェスト、Fargate、ローリング更新 |
| [3.3.6](../../domain3.md#skill-3-3-6) | ECS のブルー/グリーン、線形、カナリア |
| [3.3.7](../../domain3.md#skill-3-3-7) | サーキットブレーカーとアラームによる自動ロールバック |

## 学習の順番 {#study-order}

1. [Dockerfile の基本](../../../../services/containers.md#dockerfile)と[命令の詳細](../../../../services/containers.md#dockerfile-instructions): 命令の順序と `CMD`、`ENTRYPOINT` の違いを理解します。
2. [認証とプッシュ、プル](../../../../services/containers.md#ecr-auth): `docker login` の流れとトークンの期間を覚えます。
3. [タグと不変タグ](../../../../services/containers.md#image-tags)と[環境とイメージタグ](../../../../services/containers.md#environments-image-tags): 不変性の設定と昇格の考え方を押さえます。
4. [ライフサイクルポリシー](../../../../services/containers.md#ecr-lifecycle): ルールを読めるようにします。
5. [タスク定義](../../../../services/containers.md#task-definition)、[タスクロールと実行ロール](../../../../services/containers.md#task-role-vs-execution-role)、[環境変数とシークレットの注入](../../../../services/containers.md#env-and-secrets): 2 つのロールの役割と値の渡し方を区別します。
6. [Fargate と EC2](../../../../services/containers.md#fargate-vs-ec2): 違いと CPU、メモリの組み合わせを確認します。
7. [デプロイの種類](../../../../services/containers.md#ecs-deployments)、[ローリング更新](../../../../services/containers.md#rolling-update)、[サーキットブレーカー](../../../../services/containers.md#circuit-breaker)、[ブルー/グリーン](../../../../services/containers.md#ecs-blue-green): ECS のデプロイと戻し方を整理します。
8. [EKS のマニフェスト](../../../../services/containers.md#eks-manifests)と[AWS Copilot](../../../../services/containers.md#copilot): ローリング更新の設定と、Copilot の現状を確認します。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| ECR の認証トークン | 12 時間 | 長いバッチはプッシュの直前に取り直す |
| ライフサイクルの実行 | 条件を満たしてから 24 時間以内 | すぐには消えない |
| `minimumHealthyPercent` / `maximumPercent` | `REPLICA` は 100 / 200 | 希望数 4 で 50 なら 2 つまで止めてよい |
| サーキットブレーカーのしきい値 | 希望数の 50%、最小 3、最大 200 | ローリング更新でのみ使える |
| `maxSurge` / `maxUnavailable` | 既定 25%。前者は切り上げ、後者は切り捨て | `replicas: 10` なら 3 と 2 |
| Fargate の組み合わせの例 | 256 は 512 MiB〜2 GB、1024 は 2〜8 GB | 範囲外は登録時にエラー |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 既存のタグの上書きを防ぐ | リポジトリを `IMMUTABLE` にする |
| `latest` を毎回プッシュする CI が失敗する | 不変タグのためです。コミットのタグを使うか、`latest` を除外フィルターに入れる（`IMMUTABLE_WITH_EXCLUSION`） |
| イメージの中身を完全に固定 | `my-app@sha256:...` のダイジェストで指定する |
| dev で確かめたイメージを prod へ | 同じイメージにタグを追加して昇格する。ビルドし直さず、差は環境変数と Parameter Store で扱う |
| タグなしを 14 日で消し、`prod` は最新 10 個を残す | `untagged` と `sinceImagePushed`、`tagged` と `imageCountMoreThan` のルール |
| Fargate がイメージをプルできない、`awslogs` が動かない | 実行ロールを確認する |
| コンテナのアプリが S3 を読めない | タスクロールを確認する |
| 起動に失敗するデプロイを自動で戻す | `deploymentCircuitBreaker={enable=true,rollback=true}` |
| 本番の前に新版をテストトラフィックで検証 | `strategy: BLUE_GREEN` とライフサイクルフック。`bakeTimeInMinutes` でベイク時間を決める |
| EKS で前の版へ戻す | `kubectl rollout undo deployment/web` |

## 引っかかりやすい点 {#traps}

- **タグの中身を変えたのにタスクが古いまま**: ECS はデプロイ時にタグをダイジェストに解決します。再デプロイを強制しない限り反映されません。
- **シークレットの更新が届かない**: 値は起動時に注入します。新しいデプロイを強制します。
- **ソースを 1 行変えただけでビルドが遅い**: `RUN pip install` の前に `COPY . .` を書いています。依存関係を先にコピーします。
- **シークレットがイメージに残る**: `ENV` や `ARG` に入れると履歴に残ります。実行時に注入します。
- **タスク定義で起動コマンドが想定と違う**: ECS は `entryPoint`、`command` で、Kubernetes は `command`、`args` で上書きします。`command` の意味が違います。
- **試験ガイドに Copilot がある**: Copilot CLI は 2026 年 6 月 12 日にサポートが終了しました。概念だけ押さえ、新しい構成には使いません。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [containers 問1](../../exercises/containers.md#q1) | 3.1.2 | Dockerfile に ENTRYPOINT ["python", "app.py"] と CMD… |
| [containers 問2](../../exercises/containers.md#q2) | 3.1.2 | CI で夜間にビルドするジョブが、ビルドに 14 時間かかり、最後の docker push が認証… |
| [containers 問3](../../exercises/containers.md#q3) | 3.1.2 | リポジトリに IMMUTABLE を設定したところ、CI の docker push my-app:… |
| [containers 問4](../../exercises/containers.md#q4) | 3.1.2 | 次のライフサイクルルールの適用を検討しています。tagStatus が tagged、tagPatt… |
| [containers 問5](../../exercises/containers.md#q5) | 3.1.2 | プログラミング言語のパッケージの脆弱性も検出し、新しい CVE が公開されたらプッシュ済みのイメージ… |
| [containers 問6](../../exercises/containers.md#q6) | 3.1.2 | アカウント A の ECR から、アカウント B の別リージョンへイメージを複製します。設定について… |
| [containers 問7](../../exercises/containers.md#q7) | 3.3.2 | Fargate のタスクがイメージを取得できず、CannotPullContainerError で… |
| [containers 問10](../../exercises/containers.md#q10) | 3.3.2 | タスク内の migrate コンテナで DB を初期化し、正常終了したら app コンテナを起動しま… |
| [containers 問12](../../exercises/containers.md#q12) | 3.3.2 | ALB の背後にある ECS サービスのタスクは、起動に 90 秒かかります。デプロイのたびに、準備… |
| [containers 問13](../../exercises/containers.md#q13) | 3.3.6 | desiredCount が 4、minimumHealthyPercent が 50、maximu… |
| [containers 問14](../../exercises/containers.md#q14) | 3.3.2 | capacityProviderStrategy を、FARGATE は base: 2、weigh… |
| [containers 問16](../../exercises/containers.md#q16) | 3.3.2 | EC2 の ECS サービスで、AZ に均等に分けた上で、各 AZ ではインスタンス数を減らしたいと… |
| [containers 問18](../../exercises/containers.md#q18) | 3.3.2 | Kubernetes の Deployment を replicas: 10 で、maxSurge … |

<!-- questions:end -->

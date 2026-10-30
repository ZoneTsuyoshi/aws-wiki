# コンテナ(ECR、ECS、EKS)

コンテナイメージを ECR に保存し、ECS か EKS で動かします。AWS のサービスと簡単に連携したいなら ECS、Kubernetes の API やエコシステムが必要なら EKS を選びます。

[![ECSタスクと2つのロールの役割](../assets/diagrams/containers-ecs-flow.png)](../assets/diagrams/containers-ecs-flow.png)

## Dockerfile の基本 {#dockerfile}

```dockerfile
FROM python:3.12-slim

WORKDIR /app

# 依存関係を先にコピーし、レイヤーキャッシュを活かす
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

USER 1000
EXPOSE 8080
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "app:app"]
```

| 命令 | 役割 |
| --- | --- |
| `FROM` | ベースイメージ |
| `WORKDIR` | 作業ディレクトリ |
| `COPY` | ファイルをイメージに入れる |
| `RUN` | ビルド時に実行 |
| `ENV` | 環境変数 |
| `EXPOSE` | 使うポートの宣言(公開はしない) |
| `ENTRYPOINT`、`CMD` | 起動時に実行。`CMD` は上書きしやすい |

良いイメージを作るための要点は次のとおりです。

- 変わりにくい命令を先に書き、ビルドキャッシュを効かせます。
- マルチステージビルドで、ビルドツールを最終イメージから除きます。
- 小さなベースイメージを使うと、起動が速くなり脆弱性も減ります。
- シークレットをイメージに入れません。実行時に注入します。
- `.dockerignore` で不要なファイルを除きます。

## ECR {#ecr}

### 認証とプッシュ、プル {#ecr-auth}

Docker CLI は IAM を直接扱えません。トークンを取得して `docker login` します。

```bash
aws ecr get-login-password --region ap-northeast-1 | \
  docker login --username AWS --password-stdin \
  123456789012.dkr.ecr.ap-northeast-1.amazonaws.com

docker build -t my-app .
docker tag my-app:latest 123456789012.dkr.ecr.ap-northeast-1.amazonaws.com/my-app:1.4.2
docker push 123456789012.dkr.ecr.ap-northeast-1.amazonaws.com/my-app:1.4.2
```

- トークンの有効期間は 12 時間です。ユーザー名は `AWS` です。
- `ecr:GetAuthorizationToken` はリソース `*` に対して許可します。
- プッシュには、`ecr:InitiateLayerUpload`、`ecr:UploadLayerPart`、`ecr:CompleteLayerUpload`、`ecr:BatchCheckLayerAvailability`、`ecr:PutImage`、`ecr:BatchGetImage` が必要です。
- プルには、`ecr:BatchGetImage`、`ecr:GetDownloadUrlForLayer` が必要です。
- ログインのエラーが出たら、AWS CLI の更新と権限を確認します。Docker 認証情報ヘルパーも使えますが、MFA には対応していません。

### タグと不変タグ {#image-tags}

| 指定方法 | 例 | 特徴 |
| --- | --- | --- |
| 可変タグ | `latest` | 指す先が変わる。再現性が低い |
| バージョンやコミットのタグ | `1.4.2`、`git-abc123` | 環境ごとに承認済みの版を指定しやすい |
| ダイジェスト | `my-app@sha256:...` | 内容が完全に固定される |

**タグの不変性**はリポジトリの設定です。

| 設定 | 動作 |
| --- | --- |
| `MUTABLE` | 上書きできる |
| `IMMUTABLE` | 既存のタグへのプッシュは `ImageTagAlreadyExistsException` |
| `IMMUTABLE_WITH_EXCLUSION` | 不変とするが、指定のフィルターに一致するタグだけ上書き可 |
| `MUTABLE_WITH_EXCLUSION` | 可変とするが、指定のフィルターに一致するタグだけ上書き不可 |

本番の環境では不変タグを使うことで、同じタグの中身が変わる事故を防げます。プルスルーキャッシュを使うリポジトリは、更新のために可変にしておきます。

### 環境とイメージタグ {#environments-image-tags}

統合テストに承認済みの版を使う場合は、CI でイメージをタグ付けし、環境ごとの設定でそのタグを指定します。

| 方法 | 内容 |
| --- | --- |
| 昇格 | テスト済みのイメージに `staging`、`prod-2026-10-31` などのタグを追加する |
| 不変な参照 | タスク定義やマニフェストでコミットタグかダイジェストを指定する |
| 環境の分離 | 環境ごとにタスク定義のリビジョンを分ける |

同じイメージを dev から prod に昇格させ、環境の違いは環境変数と Parameter Store で扱います。イメージを環境ごとにビルドし直しません。Lambda のエイリアスに相当するのがこの仕組みです。

ECS はデプロイ時にタグをダイジェストに解決するので、サービス内のタスクは同じイメージで動きます。ただし、後からタグの中身が変わっても、再デプロイを強制しない限り反映されません。

### ライフサイクルポリシー {#ecr-lifecycle}

古いイメージを自動で期限切れにします。適用前にプレビューで確認します。

```json
{
  "rules": [
    {
      "rulePriority": 1,
      "description": "タグなしを 14 日で削除",
      "selection": {
        "tagStatus": "untagged",
        "countType": "sinceImagePushed",
        "countUnit": "days",
        "countNumber": 14
      },
      "action": {"type": "expire"}
    },
    {
      "rulePriority": 2,
      "description": "prod は最新 10 個を残す",
      "selection": {
        "tagStatus": "tagged",
        "tagPrefixList": ["prod"],
        "countType": "imageCountMoreThan",
        "countNumber": 10
      },
      "action": {"type": "expire"}
    }
  ]
}
```

- `rulePriority` の数字が小さいほど優先されます。
- `countType` は主に `imageCountMoreThan`(個数)と `sinceImagePushed`(経過日数)です。
- 条件を満たしてから 24 時間以内に実行されます。

### イメージスキャン {#ecr-scanning}

| 種類 | 対象 | タイミング | 仕組み |
| --- | --- | --- | --- |
| 基本 | OS の脆弱性 | プッシュ時か手動 | ECR |
| 拡張 | OS とプログラミング言語のパッケージ | プッシュ時と継続的 | Amazon Inspector と連携。結果は EventBridge に送られる |

結果は `DescribeImageScanFindings` で取得します。スキャンの設定はプライベートレジストリのレベルで行うのが推奨です。

## ECS {#ecs}

| 用語 | 意味 |
| --- | --- |
| クラスター | タスクを動かす論理的なグループ |
| タスク定義 | イメージ、CPU、メモリ、ロールなどの設計図。バージョン管理される(リビジョン) |
| タスク | タスク定義から起動した実体 |
| サービス | 指定した数のタスクを維持し、ロードバランサーと連携する |

### タスク定義 {#task-definition}

```json
{
  "family": "web",
  "requiresCompatibilities": ["FARGATE"],
  "networkMode": "awsvpc",
  "cpu": "512",
  "memory": "1024",
  "executionRoleArn": "arn:aws:iam::123456789012:role/ecsTaskExecutionRole",
  "taskRoleArn": "arn:aws:iam::123456789012:role/webTaskRole",
  "containerDefinitions": [{
    "name": "app",
    "image": "123456789012.dkr.ecr.ap-northeast-1.amazonaws.com/my-app:1.4.2",
    "portMappings": [{"containerPort": 8080}],
    "environment": [{"name": "LOG_LEVEL", "value": "info"}],
    "secrets": [{
      "name": "DB_PASSWORD",
      "valueFrom": "arn:aws:secretsmanager:ap-northeast-1:123456789012:secret:prod/db-AbCdEf:password::"
    }],
    "healthCheck": {
      "command": ["CMD-SHELL", "curl -f http://localhost:8080/health || exit 1"],
      "interval": 30,
      "timeout": 5,
      "retries": 3,
      "startPeriod": 60
    },
    "logConfiguration": {
      "logDriver": "awslogs",
      "options": {
        "awslogs-group": "/ecs/web",
        "awslogs-region": "ap-northeast-1",
        "awslogs-stream-prefix": "app"
      }
    }
  }]
}
```

### タスクロールと実行ロール {#task-role-vs-execution-role}

試験で最もよく問われる違いです。

| 観点 | タスクロール (`taskRoleArn`) | 実行ロール (`executionRoleArn`) |
| --- | --- | --- |
| 使うのは | コンテナの中のアプリ | ECS エージェント、Fargate エージェント |
| 用途 | S3、DynamoDB などアプリからの呼び出し | ECR からのプル、`awslogs` でのログ送信、`secrets` の取得 |
| 代表的なポリシー | アプリに必要な最小権限 | `AmazonECSTaskExecutionRolePolicy` |
| 信頼するプリンシパル | `ecs-tasks.amazonaws.com` | `ecs-tasks.amazonaws.com` |

判断の基準は、**タスクが起動する前に必要なら実行ロール、アプリのコードが呼ぶならタスクロール**です。Secrets Manager のカスタムキーを使うなら `kms:Decrypt` も実行ロールに付けます。

タスクロールを指定すると、SDK はタスクロールの認証情報だけを使い、EC2 のインスタンスプロファイルの権限は引き継ぎません。EC2 で動かす場合はタスク間の分離がないので、厳しい分離が必要なら Fargate を使います。

### Fargate と EC2 {#fargate-vs-ec2}

| 観点 | Fargate | EC2 |
| --- | --- | --- |
| サーバーの管理 | 不要 | 必要(パッチ、スケール) |
| CPU、メモリの指定 | タスクレベルで必須。組み合わせが決まっている | コンテナレベルでも可 |
| ネットワークモード | `awsvpc` のみ | `awsvpc`、`bridge`、`host` など |
| 分離 | タスクごとに独立 | インスタンスの中で共有 |
| インスタンスプロファイル | コンテナからは使えない | あり |
| 特権コンテナ、GPU | 使えない | 使える |
| 向く場面 | 運用を減らしたい | 特殊な要件、コストの細かい最適化 |

**アプリの要件に合わせて CPU とメモリを決めます**。Fargate の有効な組み合わせの例です。

| CPU | メモリ |
| --- | --- |
| 256 (.25 vCPU) | 512 MiB、1 GB、2 GB |
| 512 (.5 vCPU) | 1〜4 GB |
| 1024 (1 vCPU) | 2〜8 GB |
| 2048 (2 vCPU) | 4〜16 GB(1 GB 単位) |
| 4096 (4 vCPU) | 8〜30 GB(1 GB 単位) |

### 環境変数とシークレットの注入 {#env-and-secrets}

| 方法 | 指定 | 値の扱い |
| --- | --- | --- |
| 直接 | `environment` | タスク定義に平文で残る。機密でない値のみ |
| Secrets Manager | `secrets` の `valueFrom` に ARN | 起動時に環境変数へ注入。実行ロールで取得 |
| Parameter Store | `secrets` の `valueFrom` に ARN | 同上 |

ARN の末尾で、JSON のキーやバージョンを指定できます。

```text
arn:aws:secretsmanager:region:account:secret:name-AbCdEf:json-key:version-stage:version-id
```

!!! warning "ローテーションは自動で反映されない"
    シークレットは起動時に注入します。更新しても動いているコンテナには届きません。新しいタスクを起動するか、サービスの「新しいデプロイを強制」を実行します。

詳しくは [Secrets Manager と Parameter Store](secrets.md) を参照してください。

### デプロイ {#ecs-deployments}

| 種類 | 設定 | 動作 |
| --- | --- | --- |
| ローリング更新 | `deploymentController: ECS`(デフォルト) | タスクを順に置き換える |
| ブルー/グリーン | `deploymentController: ECS`、`strategy: BLUE_GREEN` | 新旧を並行して動かし、トラフィックを切り替える |
| 線形、カナリア | `deploymentController: ECS` と戦略の指定 | トラフィックを段階的に移す |
| CodeDeploy | `deploymentController: CODE_DEPLOY` | CodeDeploy が制御する従来のブルー/グリーン |
| 外部 | `deploymentController: EXTERNAL` | サードパーティのコントローラー |

#### ローリング更新 {#rolling-update}

| パラメータ | 意味 | 例(希望数 4) |
| --- | --- | --- |
| `minimumHealthyPercent` | 動いていなければならない下限(切り上げ) | 50 なら 2 つまで止めてよい |
| `maximumPercent` | 同時に動かせる上限(切り捨て) | 200 なら 8 つまで増やせる |

少なくとも 1 タスクを止めるか起動できる値にしないと、デプロイが進みません。

#### デプロイサーキットブレーカー {#circuit-breaker}

失敗を検知してデプロイを止めます。`rollback` を有効にすると、最後に `COMPLETED` になったデプロイに戻します。**ローリング更新(`ECS` コントローラー)でのみ使えます**。

```bash
aws ecs update-service --cluster prod --service web \
  --deployment-configuration "deploymentCircuitBreaker={enable=true,rollback=true}"
```

| 段階 | 確認内容 | 失敗 |
| --- | --- | --- |
| 1 | タスクが `RUNNING` になるか | なれないと失敗数を加算 |
| 2 | ELB、Cloud Map、コンテナのヘルスチェック | 失敗して置き換えられると加算 |

デフォルトのしきい値は、希望タスク数の 50% です。ただし最小は 3、最大は 200 です。`thresholdConfiguration` と `resetOnHealthyTask` で変更できます。失敗数が達すると `rolloutState` が `FAILED` になります。

CloudWatch アラームでの失敗検知は、アプリのメトリクスで判定したいときに使います。併用でき、どちらかの条件を満たすと失敗となります。

#### ブルー/グリーン {#ecs-blue-green}

現在は ECS 自体のブルー/グリーンが推奨されています。ライフサイクルフック(Lambda かポーズ)で検証を組み込めます。切り替え後のベイク時間中は両方が動き、問題があればすぐに戻せます。

```mermaid
flowchart TD
    A["グリーンを起動"] --> B["テストトラフィックで検証 (ライフサイクルフック)"]
    B --> C["本番トラフィックを移す"]
    C --> D["ベイク時間 (両方が稼働)"]
    D -- "問題なし" --> E["ブルーを削除"]
    D -- "問題あり" --> F["ブルーへ戻す"]
```

- 一時的にリソースが約 2 倍になります。
- ロードバランサー、Service Connect、VPC Lattice を使うサービスでは ECS がトラフィックを切り替えます。
- CodeDeploy の場合は 2 つのターゲットグループが必要です。`CodeDeployDefault.ECSCanary10Percent5Minutes` などの設定を使います。詳しくは [CI/CD](cicd.md) を参照してください。

## EKS {#eks}

マネージドの Kubernetes です。アプリはマニフェストで宣言します。

### マニフェストとローリング更新 {#eks-manifests}

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web
spec:
  replicas: 4
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  selector:
    matchLabels:
      app: web
  template:
    metadata:
      labels:
        app: web
    spec:
      serviceAccountName: web-sa
      containers:
        - name: app
          image: 123456789012.dkr.ecr.ap-northeast-1.amazonaws.com/my-app:1.4.2
          ports:
            - containerPort: 8080
          resources:
            requests:
              cpu: "250m"
              memory: "512Mi"
            limits:
              memory: "1Gi"
          startupProbe:
            httpGet:
              path: /healthz
              port: 8080
            failureThreshold: 30
            periodSeconds: 5
          livenessProbe:
            httpGet:
              path: /healthz
              port: 8080
            periodSeconds: 10
          readinessProbe:
            httpGet:
              path: /ready
              port: 8080
            periodSeconds: 5
```

| コマンド | 用途 |
| --- | --- |
| `kubectl apply -f deployment.yaml` | マニフェストを適用 |
| `kubectl rollout status deployment/web` | 進行状況を確認 |
| `kubectl rollout undo deployment/web` | 前の版に戻す |

| Kubernetes のリソース | 意味 |
| --- | --- |
| Pod | コンテナの最小単位 |
| Deployment | Pod の数と更新を管理 |
| Service | Pod への安定した接続先 |
| ServiceAccount | Pod の ID。IAM ロールと結びつける |

`maxSurge` は増やせる数、`maxUnavailable` は止めてよい数です。ECS の `maximumPercent`、`minimumHealthyPercent` に相当します。

### ヘルスチェックとプローブ {#probes}

| プローブ | 実行時期 | 失敗時の動作 | トラフィックへの影響 |
| --- | --- | --- | --- |
| スタートアップ | 起動時に成功するまで | コンテナを再起動 | 成功するまで他のプローブを止める |
| ライブネス | 稼働中ずっと | しきい値を超えるとコンテナを再起動 | 直接はなし |
| レディネス | 稼働中ずっと | Service の接続先から外す。再起動しない | 受けなくなる |

| 使いどころ | プローブ |
| --- | --- |
| デッドロックなど再起動で直る状態を検知 | ライブネス |
| 起動完了や DB 接続の確立までトラフィックを止める | レディネス |
| 一時的な過負荷の間だけトラフィックを止める | レディネス |
| 起動が遅いアプリ | スタートアップ |

!!! warning "ライブネスに依存先を入れない"
    ライブネスで DB の確認をすると、DB の障害で全 Pod が再起動を繰り返します。依存先の確認はレディネスで行います。

ECS での対応関係は次のとおりです。Kubernetes のようにレディネスとライブネスを分ける仕組みはありません。

| 確認の場所 | 設定 | 失敗時の動作 |
| --- | --- | --- |
| コンテナ | タスク定義の `healthCheck` | タスクが異常になり置き換えられる |
| ロードバランサー | ターゲットグループのヘルスチェック | トラフィックを止め、ECS がタスクを置き換える |
| 起動中の猶予 | サービスの `healthCheckGracePeriodSeconds`、`startPeriod` | 猶予中は失敗を数えない |

### Pod に IAM 権限を与える {#pod-identity}

| 観点 | EKS Pod Identity | IRSA |
| --- | --- | --- |
| 仕組み | EKS Auth サービスが認証情報を発行 | OIDC プロバイダーと `sts:AssumeRoleWithWebIdentity` |
| クラスター側の準備 | Pod Identity Agent(DaemonSet) | クラスターごとに IAM OIDC プロバイダー |
| 結び付け | アソシエーションを EKS API で作る | ServiceAccount に `eks.amazonaws.com/role-arn` の注釈 |
| 信頼ポリシー | `pods.eks.amazonaws.com` を信頼。クラスターごとの変更は不要 | クラスターごとの OIDC 発行者を指定 |
| Fargate の Pod | 使えない | 使える |

```bash
aws eks create-pod-identity-association \
  --cluster-name prod \
  --namespace default \
  --service-account web-sa \
  --role-arn arn:aws:iam::123456789012:role/webPodRole
```

```yaml
# IRSA の場合
apiVersion: v1
kind: ServiceAccount
metadata:
  name: web-sa
  annotations:
    eks.amazonaws.com/role-arn: arn:aws:iam::123456789012:role/webPodRole
```

どちらも Pod ごとに最小権限を実現します。ノードのロールを Pod に使わせないようにします。IMDS へのアクセスを制限しないと、Pod からノードのロールが取得できてしまいます。

## AWS Copilot について {#copilot}

!!! warning "AWS Copilot CLI はサポートが終了しています"
    AWS Copilot CLI は **2026 年 6 月 12 日にサポートが終了** しました。以降は新機能、セキュリティ更新、技術サポートがありません。既存のデプロイは動き続けますが、保守はされません。AWS は移行先として Amazon ECS Express Mode と AWS CDK を挙げています。

C03 のスキル 3.2.4 と C02 のスキル 3.3.3 では、アプリケーション環境の例として Copilot 環境の名前が挙がっているので、概念を押さえておきます。

Copilot は ECS 向けの CLI です。アプリの中に `test`、`prod` などの環境を定義し、環境ごとに同じサービスをデプロイします。

| コマンド | 用途 |
| --- | --- |
| `copilot app init` | アプリの作成 |
| `copilot env init` | 環境の作成 |
| `copilot svc deploy --env test` | 環境へのサービスのデプロイ |

新しい構成には使わず、タスク定義のリビジョンと不変のイメージタグで環境を分ける方法か、[IaC](iac.md) を使います。

## 試験のポイント {#exam-points}

| こう問われたら | 答え |
| --- | --- |
| ECR に `docker push` できない、認証エラー | `aws ecr get-login-password` で `docker login` |
| ECR のトークンの有効期間 | 12 時間 |
| 既存のタグを上書きできないように | タグの不変性 |
| `ImageTagAlreadyExistsException` | 不変タグに同じタグをプッシュした |
| 古いイメージを自動で削除 | ECR ライフサイクルポリシー |
| 言語パッケージの脆弱性も継続的に検査 | 拡張スキャン(Inspector) |
| コンテナのアプリが S3 を読めない | タスクロールを確認 |
| Fargate がイメージをプルできない、`awslogs` が動かない | 実行ロールを確認 |
| `secrets` の取得に失敗 | 実行ロールの `secretsmanager:GetSecretValue`、`kms:Decrypt` |
| シークレットの更新が反映されない | 新しいデプロイを強制 |
| サーバーを管理したくない | Fargate |
| Fargate のネットワークモード | `awsvpc` |
| 起動に失敗するデプロイを自動で戻す | サーキットブレーカーの `rollback` |
| メトリクスの悪化で自動で戻す | CloudWatch アラームの失敗検知 |
| 本番前に新版をテストトラフィックで検証 | ブルー/グリーン |
| デプロイ中に半分まで止めてよい | `minimumHealthyPercent: 50` |
| Pod を再起動せずにトラフィックだけ止める | レディネスプローブ |
| 固まった Pod を自動で再起動 | ライブネスプローブ |
| 起動の遅いアプリが再起動を繰り返す | スタートアッププローブ |
| Pod に IAM ロールを渡す、シンプルに | EKS Pod Identity |
| OIDC と注釈を使う方法 | IRSA |
| Fargate の Pod に IAM ロール | IRSA |
| Copilot を新規に使ってよいか | サポート終了済み。ECS Express Mode や CDK を検討 |

## 関連ページ {#related}

- [CI/CD](cicd.md)
- [IaC](iac.md)
- [IAM](iam.md)
- [Secrets Manager と Parameter Store](secrets.md)
- [ストレージの選び方](storage.md)
- [EC2 と Elastic Beanstalk](ec2-beanstalk.md)
- [監視](observability.md)
- [Lambda](lambda.md)

## 参考 {#references}

- [Private registry authentication in Amazon ECR](https://docs.aws.amazon.com/AmazonECR/latest/userguide/registry_auth.html)
- [IAM permissions for pushing an image](https://docs.aws.amazon.com/AmazonECR/latest/userguide/image-push-iam.html)
- [Preventing image tags from being overwritten](https://docs.aws.amazon.com/AmazonECR/latest/userguide/image-tag-mutability.html)
- [Automate the cleanup of images by using lifecycle policies](https://docs.aws.amazon.com/AmazonECR/latest/userguide/LifecyclePolicies.html)
- [Scan images for software vulnerabilities](https://docs.aws.amazon.com/AmazonECR/latest/userguide/image-scanning.html)
- [Amazon ECS task IAM role](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task-iam-roles.html)
- [Amazon ECS task execution IAM role](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task_execution_IAM_role.html)
- [Amazon ECS task definition differences for Fargate](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/fargate-tasks-services.html)
- [Pass Secrets Manager secrets through Amazon ECS environment variables](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/secrets-envvar-secrets-manager.html)
- [Deploy Amazon ECS services by replacing tasks](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/deployment-type-ecs.html)
- [How the Amazon ECS deployment circuit breaker detects failures](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/deployment-circuit-breaker.html)
- [Amazon ECS service deployment controllers and strategies](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs_service-options.html)
- [Amazon ECS blue/green deployments](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/deployment-type-blue-green.html)
- [CodeDeploy blue/green deployments for Amazon ECS](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/deployment-type-bluegreen.html)
- [Learn how EKS Pod Identity grants pods access to AWS services](https://docs.aws.amazon.com/eks/latest/userguide/pod-identities.html)
- [IAM roles for service accounts](https://docs.aws.amazon.com/eks/latest/userguide/iam-roles-for-service-accounts.html)
- [Kubernetes: Liveness, readiness, and startup probes](https://kubernetes.io/docs/concepts/configuration/liveness-readiness-startup-probes/)
- [AWS Copilot (ECS Developer Guide)](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/AWS_Copilot.html)
- [Announcing the end of support for the AWS Copilot CLI](https://aws.amazon.com/blogs/containers/announcing-the-end-of-support-for-the-aws-copilot-cli/)

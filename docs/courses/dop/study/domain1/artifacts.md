# 分野1: 成果物とリポジトリ

成果物の置き場所と保護、古いものの削除、取得の権限を問います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [リポジトリ](../../domain1.md#t1-1-repositories) | コード、イメージ、成果物のリポジトリの設定 |
| [用途と安全な管理](../../domain1.md#t1-3-security) | 成果物の用途と安全な管理 |
| [成果物の作り方](../../domain1.md#t1-3-create) | 成果物の作成、生成の方法、ビルドツールの設定（CodeBuild、Lambda） |
| [ライフサイクル](../../domain1.md#t1-3-lifecycle) | 成果物のライフサイクル |
| [リポジトリの作成と設定](../../domain1.md#t1-3-repositories) | リポジトリの作成と設定 |
| [自動ビルド](../../domain1.md#t1-3-image-builder) | AMI とコンテナイメージのビルドの自動化 |
| [アクセス権限](../../domain1.md#t1-4-permissions) | リポジトリへのアクセス権限 |

## 学習の順番 {#study-order}

1. [デプロイ環境でコードリポジトリを使う](../../../../services/cicd.md#repositories): 置くものごとのサービスの選択を確認します。
2. [タグと不変タグ](../../../../services/containers.md#image-tags): 不変タグとダイジェストでの参照を理解します。
3. [ライフサイクルポリシー](../../../../services/containers.md#ecr-lifecycle): タグの条件と保持の条件の組み合わせを覚えます。
4. [レプリケーション](../../../../services/containers.md#ecr-replication): リージョンとアカウントをまたぐ配置を確認します。
5. [ドメインとリポジトリの設定](../../../../services/cicd.md#codeartifact-settings): ドメイン、アップストリーム、外部接続、トークンを押さえます。
6. [EC2 Image Builder](../../../../services/operations.md#image-builder): レシピ、配布、ライフサイクルと、ビルド用インスタンスの条件を確認します。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| CodeArtifact のトークン | 既定 12 時間 | 15 分から 12 時間で指定できる |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| タグの上書きを防ぐ | ECR の不変タグとダイジェスト |
| 未承認のコードのデプロイを拒否する | Lambda のコード署名 |
| パッケージの取得元を統制する | CodeArtifact の外部接続を持つアップストリーム |
| 別アカウントからイメージを取得する | リポジトリポリシーと呼び出し側の IAM |
| 閉じた VPC からイメージを取得する | ECR の 2 つのエンドポイントと S3 のゲートウェイエンドポイント |
| 週次で AMI を更新して配布する | Image Builder と Parameter Store、インスタンスの更新 |

## 引っかかりやすい点 {#traps}

- トークンの取得には `sts:GetServiceBearerToken` も必要です。
- ライフサイクルポリシーの対象を広げすぎると、ロールバック先まで消えます。
- Image Builder のビルドが長く待って失敗するなら、ロールと SSM への経路を確認します。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [artifacts 問1](../../exercises/artifacts.md#q1) | リポジトリ | 新規プロジェクトで、コード、コンテナイメージ、社内の Python パッケージの置き場所を決めます。… |
| [artifacts 問2](../../exercises/artifacts.md#q2) | リポジトリ | 東京とフランクフルトの ECS で同じイメージを動かします。フランクフルトのタスクの起動が遅く、リー… |
| [artifacts 問3](../../exercises/artifacts.md#q3) | リポジトリ | 既存の CodeCommit のリポジトリを使うチームから、「新規受付が止まったと聞いたので移行が必… |
| [artifacts 問4](../../exercises/artifacts.md#q4) | 用途と安全な管理 | 本番の ECS タスクが app:latest を参照しています。ある日、誰かが同じタグで別のイメー… |
| [artifacts 問5](../../exercises/artifacts.md#q5) | 用途と安全な管理 | 金融機関の方針で、セキュリティチームが承認していないコードの Lambda へのデプロイを、技術的に… |
| [artifacts 問6](../../exercises/artifacts.md#q6) | 用途と安全な管理 | 社内の npm パッケージと同じ名前の公開パッケージが悪意のある人に登録され、開発者のマシンが誤って… |
| [artifacts 問7](../../exercises/artifacts.md#q7) | 成果物の作り方 | CodeBuild のプロジェクトを Lambda コンピュートへ移すことを検討しています。ビルドの… |
| [artifacts 問8](../../exercises/artifacts.md#q8) | 成果物の作り方 | 社内の複数アカウントで使うサーバーレスアプリを、版を付けて再利用できるように公開します。依存関係の解… |
| [artifacts 問9](../../exercises/artifacts.md#q9) | 成果物の作り方 | 1 つのビルドで Web の静的ファイルと API の ZIP を作り、後続のステージは別々のアクシ… |
| [artifacts 問10](../../exercises/artifacts.md#q10) | ライフサイクル | ECR の費用が増えています。開発用のタグ（dev- で始まる）は最新 20 個だけ残し、タグのない… |
| [artifacts 問11](../../exercises/artifacts.md#q11) | ライフサイクル | パイプラインのアーティファクト用 S3 バケットと Elastic Beanstalk のアプリケー… |
| [artifacts 問12](../../exercises/artifacts.md#q12) | ライフサイクル | Image Builder で毎週 AMI を作っています。古い AMI とスナップショットの費用が… |
| [artifacts 問13](../../exercises/artifacts.md#q13) | リポジトリの作成と設定 | 組織の 30 アカウントで社内の Python パッケージを共有します。パッケージの重複保存を避け、… |
| [artifacts 問14](../../exercises/artifacts.md#q14) | リポジトリの作成と設定 | 本番アカウントの ECS（EC2 起動）が、共有サービス用アカウントの ECR からイメージを取得し… |
| [artifacts 問15](../../exercises/artifacts.md#q15) | リポジトリの作成と設定 | パイプラインのアーティファクト用 S3 バケットを新しく作ります。組織の基準は次のとおりです。公開の… |
| [artifacts 問16](../../exercises/artifacts.md#q16) | 自動ビルド | 毎週 AMI に OS のパッチを焼き込み、脆弱性の検査を通ったものだけを Auto Scaling… |
| [artifacts 問17](../../exercises/artifacts.md#q17) | 自動ビルド | Image Builder のパイプラインが、ビルドの段階で長時間待った後に失敗します。プライベート… |
| [artifacts 問18](../../exercises/artifacts.md#q18) | 自動ビルド | 組織の標準のコンテナベースイメージを毎週更新し、3 つのリージョンの ECR へ配布します。Dock… |
| [artifacts 問19](../../exercises/artifacts.md#q19) | アクセス権限 | CodeBuild で CodeArtifact から npm パッケージを取得します。ビルドの途中… |
| [artifacts 問20](../../exercises/artifacts.md#q20) | アクセス権限 | EC2 の CodeDeploy で、DownloadBundle が AccessDenied で… |

<!-- questions:end -->

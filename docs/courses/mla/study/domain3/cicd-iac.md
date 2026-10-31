# 分野3: CI/CD、コンテナ、IaC

スタック間の連携、ML のコンテナの作り方、Code シリーズのトラブルシューティングを問います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [3.2.2](../../domain3.md#skill-3-2-2) | プロビジョニングの自動化とスタック間の連携 |
| [3.2.3](../../domain3.md#skill-3-2-3) | ML と AI のコンテナの作成と維持 |
| [3.3.2](../../domain3.md#skill-3-3-2) | Code シリーズの設定とトラブルシューティング |

## 学習の順番 {#study-order}

1. [出力とエクスポート](../../../../services/iac.md#outputs-exports)と[ネストとエクスポートの比較](../../../../services/iac.md#nested-vs-exports): 値の渡し方を選びます。
2. [Service Catalog](../../../../services/governance.md#service-catalog): セルフサービスの役割を確認します。
3. [Dockerfile](../../../../services/containers.md#dockerfile)、[ライフサイクル](../../../../services/containers.md#ecr-lifecycle)、[スキャン](../../../../services/containers.md#ecr-scanning): コンテナの作成と維持を押さえます。
4. [CodeBuild](../../../../services/cicd.md#codebuild)、[ソース管理](../../../../services/cicd.md#source-control)、[CodeCommit の現状](../../../../services/cicd.md#codecommit-status): よくある問題を覚えます。

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 別チームの VPC ID を使う | `Export` と `ImportValue` |
| 別のアカウントやリージョンの出力を参照する | `Fn::GetStackOutput` |
| Python のパッケージを足す | `requirements.txt` |
| OS のライブラリを足す | ビルド済みイメージの拡張 |
| 対応しないフレームワーク | 独自のコンテナ |
| Docker のビルドに失敗する | CodeBuild の特権モード |
| GitHub の接続が動かない | CodeConnections の承認 |

## 引っかかりやすい点 {#traps}

- 参照されている `Export` は、値の変更もスタックの削除もできません。先に参照側を変えます。
- ビルド済みのイメージは SageMaker AI のサービス側の認証情報で取得します。ECR を拒否するポリシーでも止まりません。
- CodeCommit は 2025 年 11 月に一般提供へ戻りました。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [cicd-iac 問1](../../exercises/cicd-iac.md#q1) | 3.2.2 | ネットワークのチームが管理するスタックの VPC ID を、ML のチームのスタックで使います。同じ… |
| [cicd-iac 問2](../../exercises/cicd-iac.md#q2) | 3.2.2 | Export している値を別のスタックが参照しています。値を変更しようとすると失敗しました。正しい手… |
| [cicd-iac 問3](../../exercises/cicd-iac.md#q3) | 3.2.2 | データサイエンティストが、承認された構成の学習環境を自分で作れるようにします。IAM の管理者の手間… |
| [cicd-iac 問4](../../exercises/cicd-iac.md#q4) | 3.2.3 | SageMaker AI のビルド済みのイメージに必要なパッケージがそろっていますが、OS のライブ… |
| [cicd-iac 問5](../../exercises/cicd-iac.md#q5) | 3.2.3 | ECR のモデルのイメージを維持します。適切な運用を選んでください。（2つ選択） |
| [cicd-iac 問6](../../exercises/cicd-iac.md#q6) | 3.2.3 | SageMaker AI のビルド済みのイメージを使っています。実行ロールに ECR を拒否する I… |
| [cicd-iac 問7](../../exercises/cicd-iac.md#q7) | 3.3.2 | CodeBuild で推論のコンテナをビルドして ECR にプッシュします。docker build… |
| [cicd-iac 問8](../../exercises/cicd-iac.md#q8) | 3.3.2 | GitHub のリポジトリをパイプラインのソースにしました。接続が「保留中」のままで動きません。原因… |
| [cicd-iac 問9](../../exercises/cicd-iac.md#q9) | 3.3.2 | 2026 年に新しい ML プロジェクトで CodeCommit を検討しています。「新規に使えない… |

<!-- questions:end -->

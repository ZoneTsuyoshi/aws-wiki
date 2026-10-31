# 分野1: CodeBuild とテスト

ビルドの設定と、テストの結果をパイプラインの判定につなぐ方法を問います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [ビルドプロセス](../../domain1.md#t1-1-build) | ビルドプロセスの設定 |
| [シークレット](../../domain1.md#t1-1-secrets) | ビルドとデプロイのシークレットの管理 |
| [テストの種類と配置](../../domain1.md#t1-2-test-types) | テストの種類、各段階でのテストの使い分け |
| [PR とマージでのビルド](../../domain1.md#t1-2-pr-builds) | PR やマージでのビルド、テスト |
| [負荷テスト](../../domain1.md#t1-2-load-testing) | 負荷テスト、性能のベンチマーク |
| [終了コード](../../domain1.md#t1-2-exit-codes) | 終了コードによる健全性の測定 |
| [単体テストとカバレッジ](../../domain1.md#t1-2-unit-coverage) | 単体テストとコードカバレッジの自動化 |

## 学習の順番 {#study-order}

1. [buildspec の構成](../../../../services/cicd.md#buildspec): フェーズと主なセクションの構成を確認します。
2. [プロジェクトの設定](../../../../services/cicd.md#codebuild-project): 特権モード、コンピュートの種類の違いを押さえます。
3. [キャッシュ](../../../../services/cicd.md#build-cache): S3 キャッシュとローカルキャッシュの使い分けを覚えます。
4. [secrets-manager の指定](../../../../services/cicd.md#buildspec-secrets): `env.secrets-manager` と必要な権限を確認します。
5. [Webhook とフィルターグループ](../../../../services/cicd.md#codebuild-webhook): フィルターグループの AND と OR、`BASE_REF` と `HEAD_REF` の違いを理解します。
6. [テストレポート](../../../../services/cicd.md#build-reports): レポートの形式、30 日の期限、判定はしないことを押さえます。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| テストレポートの期限 | 30 日 | 長く残すなら S3 へエクスポート |
| 終了コード | 0 は成功、それ以外は失敗 | パイプで握りつぶさない |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| `docker build` がデーモンに接続できない | 特権モードを有効にする |
| VPC の中のデータベースへ接続できない | プロジェクトの VPC 設定 |
| 自動ローテーションが必要なシークレット | Secrets Manager と `env.secrets-manager` |
| カバレッジが基準未満なら止める | コマンドで計算し、0 以外で終了する |
| `main` への PR でだけビルドする | 1 つのグループに `EVENT` と `BASE_REF` |
| 速いテストと遅いテストの配置 | 速いものを PR やコミット、遅いものをデプロイ後へ |
| 大きな負荷を複数リージョンからかける | Distributed Load Testing on AWS |

## 引っかかりやすい点 {#traps}

- `npm test | tee log` は `tee` の終了コードを返します。
- レポートを設定しても、ビルドの成否は変わりません。
- パターンを `^` と `$` で固定しないと、部分一致で別のブランチでも動きます。
- カスタマー管理キーで暗号化されたシークレットには `kms:Decrypt` も必要です。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [codebuild 問1](../../exercises/codebuild.md#q1) | ビルドプロセス | CodeBuild でコンテナイメージをビルドし、続けて VPC の中の RDS に接続する結合テス… |
| [codebuild 問2](../../exercises/codebuild.md#q2) | ビルドプロセス | Java のビルドで依存関係の取得に毎回 8 分かかります。同じプロジェクトを複数の担当者が 1 日… |
| [codebuild 問3](../../exercises/codebuild.md#q3) | ビルドプロセス | ビルド後のテストで失敗しても、テスト結果のファイルをアップロードして、一時リソースを必ず削除する必要… |
| [codebuild 問4](../../exercises/codebuild.md#q4) | シークレット | ビルドでプライベートレジストリのパスワードを使います。現在はプロジェクトの環境変数に平文で設定してお… |
| [codebuild 問5](../../exercises/codebuild.md#q5) | シークレット | CloudFormation でデプロイする RDS のマスターパスワードと、CodeBuild で… |
| [codebuild 問6](../../exercises/codebuild.md#q6) | シークレット | CodeBuild が env.secrets-manager でシークレットを取得するとき、ビルド… |
| [codebuild 問7](../../exercises/codebuild.md#q7) | テストの種類と配置 | あるパイプラインでは 40 分の UI テストを最初に実行し、その後に 2 分の単体テストと 1 分… |
| [codebuild 問8](../../exercises/codebuild.md#q8) | テストの種類と配置 | パイプラインに次の 3 つの検査を組み込みます。自作コードの脆弱なパターン、ビルド後のコンテナイメー… |
| [codebuild 問9](../../exercises/codebuild.md#q9) | テストの種類と配置 | モバイル向け Web アプリのリリース前に、複数の実機のブラウザでレイアウトの崩れを確認します。リリ… |
| [codebuild 問10](../../exercises/codebuild.md#q10) | PR とマージでのビルド | main へ向けた PR が作られたとき、または更新されたときだけ CodeBuild を動かします… |
| [codebuild 問11](../../exercises/codebuild.md#q11) | PR とマージでのビルド | HEAD_REF のフィルターに release と書いたところ、release-old や pre… |
| [codebuild 問12](../../exercises/codebuild.md#q12) | PR とマージでのビルド | GitHub のブランチ保護で、テストが通らない PR のマージを止めたいと考えています。CodeB… |
| [codebuild 問13](../../exercises/codebuild.md#q13) | 負荷テスト | 決済 API の性能テストをパイプラインへ組み込みます。条件は次のとおりです。複数のリージョンから大… |
| [codebuild 問14](../../exercises/codebuild.md#q14) | 負荷テスト | 検証環境の負荷テストでは問題がありませんでしたが、本番のキャンペーンで Lambda の 429 と… |
| [codebuild 問15](../../exercises/codebuild.md#q15) | 負荷テスト | 新しいサービスのリリース前に、負荷がかかった状態で AZ を 1 つ失っても応答時間の目標を守れるか… |
| [codebuild 問16](../../exercises/codebuild.md#q16) | 終了コード | buildspec の build フェーズで npm test / tee results.log… |
| [codebuild 問17](../../exercises/codebuild.md#q17) | 終了コード | CloudFormation で作る Auto Scaling グループの起動スクリプトで、アプリの… |
| [codebuild 問18](../../exercises/codebuild.md#q18) | 単体テストとカバレッジ | カバレッジが 80% 未満ならビルドを失敗にする方針です。buildspec の reports で… |
| [codebuild 問19](../../exercises/codebuild.md#q19) | 単体テストとカバレッジ | 監査の要件で、単体テストの結果を 1 年間保管します。CodeBuild のレポートグループには J… |
| [codebuild 問20](../../exercises/codebuild.md#q20) | 単体テストとカバレッジ | Python と Java のサービスで、テストと行カバレッジの推移を CodeBuild のコンソ… |

<!-- questions:end -->

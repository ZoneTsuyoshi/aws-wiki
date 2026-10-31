# 分野3: アプリ統合とその他のサービス

通知、業務、開発、端末、IoT のサービスを、要件から選びます。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [メッセージと通知のサービス](../../domain3.md#t3-8-integration) | SQS、SNS、EventBridge、Step Functions |
| [業務アプリケーション](../../domain3.md#t3-8-business) | Connect と SES |
| [顧客支援のサービス](../../domain3.md#t3-8-enablement) | AWS Support |
| [開発ツール](../../domain3.md#t3-8-developer) | CodeBuild、CodePipeline、X-Ray |
| [エンドユーザーコンピューティング](../../domain3.md#t3-8-euc) | WorkSpaces、AppStream 2.0、Secure Browser |
| [フロントエンドとモバイル](../../domain3.md#t3-8-frontend) | Amplify |
| [IoT](../../domain3.md#t3-8-iot) | IoT Core |

## 学習の順番 {#study-order}

1. [選び方](../../../../services/messaging.md#how-to-choose): メッセージのサービスの選び方を覚えます。
2. [Amazon Connect](../../../../services/other-services.md#connect)と[Amazon SES](../../../../services/other-services.md#ses): 業務のサービスを確認します。
3. [AWS Support プラン](../../../../services/cloud-foundations.md#support-plans): プランを選ぶ観点を確認します。
4. [サービスの役割](../../../../services/cicd.md#overview)と[X-Ray によるトレース](../../../../services/observability.md#xray): 開発ツールの役割を区別します。
5. [Amazon WorkSpaces](../../../../services/other-services.md#workspaces)、[Amazon WorkSpaces Applications（旧 AppStream 2.0）](../../../../services/other-services.md#appstream)、[Amazon WorkSpaces Secure Browser](../../../../services/other-services.md#secure-browser): 何を届けるかで区別します。
6. [Amplify Hosting とブランチ](../../../../services/cicd.md#amplify)と[AWS IoT Core](../../../../services/other-services.md#iot-core): 用途を確認します。

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 注文を溜めて順に処理する | SQS |
| アラートをメールで受け取る | SNS |
| 内容で振り分ける、スケジュールで実行する | EventBridge |
| 複数の手順を順番に実行する | Step Functions |
| 自前の設備なしでコールセンターを作る | Connect |
| アプリからメールを大量に送る | SES |
| リリースの流れを自動化する | CodePipeline |
| ボトルネックを調べる | X-Ray |
| 社員に仮想デスクトップを配る | WorkSpaces |
| 特定のアプリをブラウザーへ配信する | AppStream 2.0 |
| フロントエンドをサーバー管理なしで公開する | Amplify |
| 多数のセンサーを接続する | IoT Core |

## 引っかかりやすい点 {#traps}

- 試験ガイドの名前と現在の製品名が異なるものがあります。AppStream 2.0 は現在 WorkSpaces Applications です。
- WorkSpaces Secure Browser は 2026年10月29日にメンテナンスへ移行し、新しい顧客は使えません。
- X-Ray はアプリを調べるもので、API 操作の記録の CloudTrail とは別です。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [other-services 問1](../../exercises/other-services.md#q1) | メッセージと通知のサービス | 注文をいったん溜めて、処理側が自分のペースで順に取り出すようにしたいと考えています。最も適切なサービ… |
| [other-services 問2](../../exercises/other-services.md#q2) | メッセージと通知のサービス | サーバーの異常のアラートを、担当者のメールや SMS に同時に送りたいと考えています。最も適切なサー… |
| [other-services 問3](../../exercises/other-services.md#q3) | メッセージと通知のサービス | イベントの内容によって送り先を振り分け、スケジュールでの実行もしたいと考えています。最も適切なサービ… |
| [other-services 問4](../../exercises/other-services.md#q4) | メッセージと通知のサービス | 受注、在庫の確認、配送の手配の処理を順番に実行し、流れを管理したいと考えています。最も適切なサービス… |
| [other-services 問5](../../exercises/other-services.md#q5) | 業務アプリケーション | 自前の設備なしでコールセンターを作りたいと考えています。最も適切なサービスはどれですか。 |
| [other-services 問6](../../exercises/other-services.md#q6) | 業務アプリケーション | アプリから、案内のメールを本文付きで大量に送りたいと考えています。最も適切なサービスはどれですか。 |
| [other-services 問7](../../exercises/other-services.md#q7) | 業務アプリケーション | SES と SNS の違いの説明として正しいものはどれですか。 |
| [other-services 問8](../../exercises/other-services.md#q8) | 顧客支援のサービス | 本番環境で AWS の技術的な問題が起きたときの相談先として最も適切なものはどれですか。 |
| [other-services 問9](../../exercises/other-services.md#q9) | 顧客支援のサービス | サポートプランを選ぶときに比べるものとして適切なものはどれですか。（2つ選択） |
| [other-services 問10](../../exercises/other-services.md#q10) | 顧客支援のサービス | 専任の担当者（TAM）に継続して支援してほしい会社が選ぶべきプランとして適切なものはどれですか。 |
| [other-services 問11](../../exercises/other-services.md#q11) | 開発ツール | コードのビルドとテストを実行するサービスはどれですか。 |
| [other-services 問12](../../exercises/other-services.md#q12) | 開発ツール | ソースの変更からビルド、デプロイまでの流れ全体を自動化したいと考えています。最も適切なサービスはどれ… |
| [other-services 問13](../../exercises/other-services.md#q13) | 開発ツール | 分散アプリの遅いリクエストについて、どのサービスの間でボトルネックが起きているかを調べたいと考えてい… |
| [other-services 問14](../../exercises/other-services.md#q14) | エンドユーザーコンピューティング | 社員に仮想デスクトップを配り、在宅勤務でも同じ環境を使わせたいと考えています。最も適切なサービスはど… |
| [other-services 問15](../../exercises/other-services.md#q15) | エンドユーザーコンピューティング | CAD などの重いアプリだけを、ブラウザーへ配信したいと考えています。デスクトップ全体は不要です。試… |
| [other-services 問16](../../exercises/other-services.md#q16) | エンドユーザーコンピューティング | 届けるものとサービスの組み合わせとして正しいものはどれですか。（2つ選択） |
| [other-services 問17](../../exercises/other-services.md#q17) | フロントエンドとモバイル | フロントエンドの開発者が、サーバーの管理なしで Web アプリを公開したいと考えています。最も適切な… |
| [other-services 問18](../../exercises/other-services.md#q18) | フロントエンドとモバイル | Git リポジトリに接続して、ブランチごとに Web アプリをビルドしてデプロイしたいと考えています… |
| [other-services 問19](../../exercises/other-services.md#q19) | フロントエンドとモバイル | AWS Amplify の説明として正しいものはどれですか。 |
| [other-services 問20](../../exercises/other-services.md#q20) | IoT | 工場の多数のセンサーを AWS に接続して管理したいと考えています。最も適切なサービスはどれですか。 |
| [other-services 問21](../../exercises/other-services.md#q21) | IoT | AWS IoT Core がデバイスとの通信に使うプロトコルの例はどれですか。 |
| [other-services 問22](../../exercises/other-services.md#q22) | IoT | センサーのデータを受けて、ルールで Lambda や DynamoDB に渡したいと考えています。受… |

<!-- questions:end -->

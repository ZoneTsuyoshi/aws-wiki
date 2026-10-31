# 分野1: デプロイ方式

条件から方式を選ぶ力と、失敗したイベントから原因を絞る力を問います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [デプロイ戦略の判断](../../domain1.md#t1-1-deployment-strategy) | デプロイ戦略の判断 |
| [デプロイ方式](../../domain1.md#t1-4-methods) | 各プラットフォームのデプロイ方式、さまざまなデプロイ方式の使用 |
| [ストレージパターン](../../domain1.md#t1-4-storage) | アプリケーションのストレージパターン |
| [ミュータブルとイミュータブル](../../domain1.md#t1-4-mutable-immutable) | ミュータブルとイミュータブル |
| [配布するツール](../../domain1.md#t1-4-distribution) | コードを配布するツール |
| [エージェント](../../domain1.md#t1-4-agents) | デプロイエージェントの設定 |
| [デプロイの問題の解決](../../domain1.md#t1-4-troubleshooting) | デプロイの問題の解決 |

## 学習の順番 {#study-order}

1. [デプロイ戦略の比較](../../../../services/cicd.md#deployment-strategies): ダウンタイム、戻す速さ、追加コストで方式を比べます。
2. [デプロイ設定](../../../../services/cicd.md#deployment-configs): EC2 と Lambda の設定名を確認します。
3. [デプロイポリシー](../../../../services/ec2-beanstalk.md#deployment-policies): Beanstalk のポリシーの違いを押さえます。
4. [比較](../../../../services/storage.md#comparison): インスタンスの入れ替えとストレージの関係を理解します。
5. [Distributor](../../../../services/operations.md#distributor): パッケージの配布と State Manager の組み合わせを確認します。
6. [CodeDeploy エージェント](../../../../services/cicd.md#codedeploy-agent): エージェントが要る対象と外向きの経路を覚えます。
7. [デプロイ失敗の診断](../../../../services/cicd.md#troubleshooting-deployments): 失敗したイベントごとの原因を表で覚えます。

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 追加費用なしで止めずに更新する | インプレースのローリング |
| 即座に切り戻す、2 環境の費用は許容する | Blue/Green |
| 一部の利用者で確かめてから全体へ | カナリアとアラーム |
| 失敗しても既存のサーバーに影響させない | イミュータブル |
| コードを変えずに複数 AZ でファイルを共有する | EFS |
| オンプレミスにもアプリを配布する | CodeDeploy のオンプレミスインスタンス |
| 全イベントが `Skipped` | エージェント、インスタンスプロファイル、外向きの経路 |

## 引っかかりやすい点 {#traps}

- `ApplicationStop` は前回の版のスクリプトで動くので、今回の修正は効きません。
- `AllowTraffic` の失敗は、ターゲットグループのヘルスチェックが典型です。
- エージェントが要るのは EC2 とオンプレミスだけです。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [deployments 問1](../../exercises/deployments.md#q1) | デプロイ戦略の判断 | EC2 の Web アプリを更新します。条件は次のとおりです。追加の EC2 の費用はかけない、更新… |
| [deployments 問2](../../exercises/deployments.md#q2) | デプロイ戦略の判断 | 決済 API を Lambda で動かしています。新しい版を一部の利用者で実データを使って 10 分… |
| [deployments 問3](../../exercises/deployments.md#q3) | デプロイ戦略の判断 | 開発環境、検証環境、本番環境で方式を決めます。開発は速さが最優先で短い停止を許容します。本番は切り戻… |
| [deployments 問4](../../exercises/deployments.md#q4) | デプロイ方式 | Elastic Beanstalk の本番環境を更新します。条件は次のとおりです。更新の失敗が既存の… |
| [deployments 問5](../../exercises/deployments.md#q5) | デプロイ方式 | SAM で管理する Lambda を、10 分ごとに 10% ずつ切り替えます。切り替え前に検証用の… |
| [deployments 問6](../../exercises/deployments.md#q6) | ストレージパターン | CMS を EC2 の Auto Scaling グループで動かしています。利用者がアップロードした… |
| [deployments 問7](../../exercises/deployments.md#q7) | ストレージパターン | 単一の EC2 で動くデータベースサーバーの更新で、インスタンスの入れ替え方式を採用します。データは… |
| [deployments 問8](../../exercises/deployments.md#q8) | ストレージパターン | 画像の変換の処理を EC2 から Lambda へ移します。元の画像は Web から直接アップロード… |
| [deployments 問9](../../exercises/deployments.md#q9) | ミュータブルとイミュータブル | 毎月の OS 更新を Run Command で稼働中のサーバーへ適用しています。サーバーごとに状態… |
| [deployments 問10](../../exercises/deployments.md#q10) | ミュータブルとイミュータブル | 起動に時間がかかるレガシーのアプリで、更新の所要時間と切り戻しの速さを比較しています。バイナリの置き… |
| [deployments 問11](../../exercises/deployments.md#q11) | 配布するツール | セキュリティチームが、自社製の監視エージェントの新しいバージョンを 5,000 台の EC2 とオン… |
| [deployments 問12](../../exercises/deployments.md#q12) | 配布するツール | データセンターの Windows サーバー 40 台と、AWS の EC2 にアプリのリビジョンを同… |
| [deployments 問13](../../exercises/deployments.md#q13) | 配布するツール | 工場の中のサーバーでコンテナを動かします。規制でデータを外に出せないのでサーバーはそのまま使います。… |
| [deployments 問14](../../exercises/deployments.md#q14) | エージェント | Auto Scaling で増えた EC2 だけ、CodeDeploy のデプロイの全イベントが S… |
| [deployments 問15](../../exercises/deployments.md#q15) | エージェント | プライベートサブネットの EC2 で CodeDeploy のデプロイが始まりません。エージェントは… |
| [deployments 問16](../../exercises/deployments.md#q16) | エージェント | 新しい基盤を設計中です。Lambda、Fargate の ECS、EC2、オンプレミスのサーバーに … |
| [deployments 問17](../../exercises/deployments.md#q17) | デプロイの問題の解決 | EC2 の CodeDeploy で、前回の版のデプロイは成功していましたが、今回は Applica… |
| [deployments 問18](../../exercises/deployments.md#q18) | デプロイの問題の解決 | Blue/Green の EC2 デプロイで、新しいインスタンスへの全イベントは成功するのに、All… |

<!-- questions:end -->

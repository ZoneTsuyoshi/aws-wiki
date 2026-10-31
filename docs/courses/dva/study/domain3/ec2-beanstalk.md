# 分野3: EC2 と Elastic Beanstalk

分野3では、Elastic Beanstalk のデプロイポリシーの選択と、環境の分け方、設定の渡し方が問われます。ログや Auto Scaling の調整は[分野4の EC2 と Elastic Beanstalk](../domain4/ec2-beanstalk.md) で扱います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [3.1.4](../../domain3.md#skill-3-1-4) | 環境プロパティと設定の優先順位 |
| [3.2.4](../../domain3.md#skill-3-2-4) | 環境の分離 |
| [3.3.6](../../domain3.md#skill-3-3-6) | デプロイポリシーとブルー/グリーン |
| [3.3.7](../../domain3.md#skill-3-3-7) | ポリシーごとの戻し方 |

## 学習の順番 {#study-order}

1. [環境](../../../../services/ec2-beanstalk.md#beanstalk-environments): 用語と、環境を分ける意味を確認します。
2. [デプロイポリシー](../../../../services/ec2-beanstalk.md#deployment-policies): 比較表で失敗時の影響と戻し方を覚えます。
3. [バッチと健全性の設定](../../../../services/ec2-beanstalk.md#batch-settings): 既定値と台数の計算を練習します。
4. [選び方](../../../../services/ec2-beanstalk.md#choosing-policy): 要件からポリシーを選べるようにします。
5. [不変デプロイの流れ](../../../../services/ec2-beanstalk.md#immutable)と[トラフィック分割の設定](../../../../services/ec2-beanstalk.md#traffic-splitting): 新しいインスタンスを使う 2 つの方式を比べます。
6. [ブルー/グリーンと CNAME スワップ](../../../../services/ec2-beanstalk.md#blue-green): DNS を変える方式の注意点を押さえます。
7. [環境プロパティ](../../../../services/ec2-beanstalk.md#environment-properties)と[設定の優先順位](../../../../services/ec2-beanstalk.md#option-precedence): どの設定が勝つかを覚えます。
8. [ディレクトリ構成](../../../../services/ec2-beanstalk.md#directory-structure)と[.ebextensions](../../../../services/ec2-beanstalk.md#ebextensions): 設定ファイルの置き場所を確認します。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| `DeploymentPolicy` | 既定 `AllAtOnce` | EB CLI で作ったスケーラブルな環境は `Rolling` |
| `BatchSize` / `BatchSizeType` | 既定 100 / `Percentage` | `Fixed` なら台数で指定 |
| `Timeout` | 既定 600 秒（実効 840 秒）、1〜3600 | 秒で書く |
| `NewVersionPercent` | 既定 10、1〜100 | 新版に流す割合 |
| `EvaluationTime` | 既定 5 分、3〜600 | 正常なら残りも移す |
| 環境プロパティ | 合計 4,096 バイト | パスワードは平文で入れない |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 開発環境で最速に | `AllAtOnce`。ダウンタイムは許容する |
| ダウンタイムなし、追加費用なし、容量は減ってもよい | `Rolling` |
| 容量を落とせない | `RollingWithAdditionalBatch` |
| 失敗時にすぐ戻す、新しいインスタンスで検証する | `Immutable` |
| 一部のトラフィックだけで試す | `TrafficSplitting`（ALB が必要） |
| 環境ごと切り替える、互換性のないプラットフォーム更新 | ブルー/グリーンと CNAME スワップ |
| 8 台で `BatchSize: 25` の `Rolling` | 2 台ずつ更新し、動くのは 6 台 |
| 8 台で `BatchSize: 25` の追加バッチ付き | 先に 2 台増やして 10 台にし、8 台を維持する |
| 15% を流して 10 分見る | `NewVersionPercent: "15"`、`EvaluationTime: "10"` |
| 環境ごとに API の URL を変える | `aws:elasticbeanstalk:application:environment` の環境プロパティ |

## 引っかかりやすい点 {#traps}

- **`.ebextensions` に書いたポリシーが効かない**: コンソールや EB CLI は推奨値を API で直接設定します。直接の設定が優先されるので、消すか、コンソールで変えます。
- **ローリングの失敗で旧版と新版が混ざる**: 完了したバッチは新版のままで、自動では戻りません。正常なバージョンをもう一度デプロイします。
- **単一インスタンス環境でローリングを選ぶ**: ローリング、追加バッチ付き、トラフィック分割は使えません。
- **スワップ直後に古い環境を消す**: DNS のキャッシュがあるので、TTL が切れるまで消しません。
- **不変デプロイでエラーになる**: リソース設定の変更とは同時に実行できません。2 回に分けるか、ブルー/グリーンにします。
- **ブルー/グリーンで DB を共有できない**: 環境の中に作った RDS は環境と結び付きます。DB は環境の外に作ります。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [ec2-beanstalk 問5](../../exercises/ec2-beanstalk.md#q5) | 3.3.6 | Elastic Beanstalk のロードバランス環境は 8 台で動いています。BatchSize… |
| [ec2-beanstalk 問6](../../exercises/ec2-beanstalk.md#q6) | 3.3.7 | ローリングデプロイが 3 バッチ目で失敗しました。Elastic Beanstalk の環境はどのよ… |
| [ec2-beanstalk 問7](../../exercises/ec2-beanstalk.md#q7) | 3.1.4 | 開発者は、コンソールで作成した環境のデプロイポリシーを、ソースバンドルの .ebextensions… |
| [ec2-beanstalk 問8](../../exercises/ec2-beanstalk.md#q8) | 3.1.4 | 環境は最初に MinSize を 5 として作成しました。ソースバンドルの .ebextension… |
| [ec2-beanstalk 問9](../../exercises/ec2-beanstalk.md#q9) | 3.3.6 | DB のマイグレーションを、デプロイごとに 1 台のインスタンスで、アプリの配置前に実行したいと考え… |
| [ec2-beanstalk 問14](../../exercises/ec2-beanstalk.md#q14) | 3.3.6 | ある環境は、作成時に結合した RDS を使っています。本番化にあたり、ブルー/グリーンを行えるように… |

<!-- questions:end -->

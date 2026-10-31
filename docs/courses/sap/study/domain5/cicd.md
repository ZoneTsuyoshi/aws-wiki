# 分野5: CI/CD と DevSecOps

パイプラインの組み立てに加えて、成果物の同一性、脆弱性と発行元の確認、アカウントをまたぐ権限、安全に戻す方法を問います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [5.2.1](../../domain5.md#skill-5-2-1) | 自動のビルドとデプロイのパイプライン |
| [5.2.2](../../domain5.md#skill-5-2-2) | セキュリティスキャンと署名 |
| [5.2.3](../../domain5.md#skill-5-2-3) | マルチアカウント、マルチリージョンのパイプライン |
| [5.2.4](../../domain5.md#skill-5-2-4) | AI と ML のアプリの評価と出力の検証 |
| [5.2.5](../../domain5.md#skill-5-2-5) | ロールバックできるデプロイ戦略 |

## 学習の順番 {#study-order}

1. [サービスの役割](../../../../services/cicd.md#overview)と[パイプラインタイプ](../../../../services/cicd.md#pipeline-types): V2 だけの機能を覚えます。
2. [複数環境への展開](../../../../services/cicd.md#multi-environment)と[ステージ条件](../../../../services/cicd.md#stage-conditions): 同じ成果物を昇格する理由と、条件の 3 つのタイミングを押さえます。
3. [イメージスキャン](../../../../services/containers.md#ecr-scanning)、[スキャンの種類](../../../../services/threat-detection.md#inspector-scan-types)、[コード署名](../../../../services/lambda.md#code-signing): スキャンと署名が答える問いの違いを理解します。
4. [アカウントをまたぐ手順](../../../../services/kms.md#cross-account-steps)と[ロールの引き受け](../../../../services/iam.md#assume-role): カスタマー管理キーが必要な理由と、必要な設定の場所を確認します。
5. [Bedrock Evaluations](../../../../services/genai-apps.md#bedrock-evaluations)、[テスト](../../../../services/genai-apps.md#testing)、[エージェントの評価](../../../../services/genai-apps.md#agent-evaluation): ジョブの種類と、指標の読み方を覚えます。
6. [デプロイ戦略の比較](../../../../services/cicd.md#deployment-strategies)、[ロールバックの方法](../../../../services/cicd.md#rollback)、[ロールバックとアラームの設定](../../../../services/cicd.md#codedeploy-rollback-settings)、[デプロイサーキットブレーカー](../../../../services/containers.md#circuit-breaker): 自動で戻る条件をサービスごとに整理します。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| 実行モード | `SUPERSEDED`（既定）、`QUEUED`、`PARALLEL` | `QUEUED` と `PARALLEL` は V2 |
| Entry の結果 | `Fail`、`Skip` | ステージに入る前 |
| On Failure の結果 | `Rollback` | ステージの失敗時 |
| On Success の結果 | `Rollback`、`Fail` | ステージの成功後 |
| Lambda のコード署名 | `Warn`（既定）、`Enforce` | 検証はデプロイ時 |
| サーキットブレーカーのしきい値 | 希望タスク数の 50%、最小 3、最大 200 | 既定値 |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| テストしたものと本番のものを同じにする | 1 回だけビルドして昇格 |
| ファイルパスで起動を絞る | V2 のトリガーのフィルター |
| すべてのコミットを順に本番へ | `QUEUED` モード |
| クライアントのツールなしでイメージに署名 | ECR マネージド署名 |
| プッシュの前に脆弱性で止める | Inspector の SBOM Generator と Scan API |
| 新しい CVE を継続的に知る | ECR の拡張スキャンと EventBridge |
| 別のアカウントがアーティファクトを読めない | カスタマー管理キー、バケットポリシー、対象のロール |
| 別のリージョンへのアクション | パイプラインのアカウントのそのリージョンにバケットとキー |
| 出力の品質で昇格を止める | 判定モデルの評価ジョブとスコアの基準 |
| 主観的な専門の品質 | 人の評価ジョブ |
| アラームで止まるが戻らない | `DEPLOYMENT_STOP_ON_ALARM` の自動ロールバック |
| 業務エラーでも ECS を戻す | アラームによる失敗検知を追加 |

## 引っかかりやすい点 {#traps}

- 既定の S3 の AWS 管理キーは、他のアカウントと共有できません。
- 本番の EC2 にデプロイするときは、EC2 のインスタンスロールにもバケットとキーの権限が要ります。
- 署名プロファイルはレジストリと同じリージョンに必要です。別のアカウントのものは使えます。
- `PARALLEL` モードでは、ステージのロールバックを使えません。
- サーキットブレーカーは起動とヘルスチェックしか見ません。業務のエラーは別に検知します。
- データベースのスキーマは簡単に戻せません。新旧の両方で動く形で進めます。
- CodeGuru Security はサポートが終了しました。後継は Inspector の Code Security です。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [cicd 問1](../../exercises/cicd.md#q1) | 5.2.1 | ある企業のパイプラインは、開発、ステージング、本番の各ステージでソースからコンテナイメージをビルドし… |
| [cicd 問2](../../exercises/cicd.md#q2) | 5.2.1 | モノレポに 30 のサービスがあり、CodePipeline の V1 タイプのパイプラインがサービ… |
| [cicd 問3](../../exercises/cicd.md#q3) | 5.2.1 | 決済チームのパイプラインは V2 タイプで、1 日に何度もコミットがあります。規制のため、すべてのコ… |
| [cicd 問4](../../exercises/cicd.md#q4) | 5.2.1 | 製造業の企業は、同じ業務アプリを EC2 とオンプレミスのサーバーの両方で動かしています。移行が終わ… |
| [cicd 問5](../../exercises/cicd.md#q5) | 5.2.2 | ある企業は、ECR のイメージへの署名を標準にします。ビルド環境にクライアント側の署名ツールを入れた… |
| [cicd 問6](../../exercises/cicd.md#q6) | 5.2.2 | コンテナのパイプラインに脆弱性の対策を入れます。要件は 2 つです。(1) 重大な脆弱性のあるイメー… |
| [cicd 問7](../../exercises/cicd.md#q7) | 5.2.2 | 本番アカウントの Lambda に、信頼できる発行元のコードだけをデプロイさせます。ただし、現在のパ… |
| [cicd 問8](../../exercises/cicd.md#q8) | 5.2.2 | 監査で、「レジストリに悪意のあるイメージが置かれた場合でも本番へ入らないこと」と「依存パッケージに既… |
| [cicd 問9](../../exercises/cicd.md#q9) | 5.2.3 | ツール用のアカウントにある CodePipeline から、本番のアカウントへデプロイするパイプライ… |
| [cicd 問10](../../exercises/cicd.md#q10) | 5.2.3 | 東京のリージョンにあるパイプラインに、バージニア北部へデプロイするアクションを追加します。パイプライ… |
| [cicd 問11](../../exercises/cicd.md#q11) | 5.2.3 | ツールアカウントのパイプラインが、本番アカウントの CodeDeploy で EC2 へデプロイしま… |
| [cicd 問12](../../exercises/cicd.md#q12) | 5.2.3 | 複数のアカウントへ順に昇格するパイプラインで、次の条件を満たしてから本番のステージへ進めたいです。ス… |
| [cicd 問13](../../exercises/cicd.md#q13) | 5.2.4 | カスタマーサポートの回答を生成するアプリで、プロンプトの変更が頻繁にあります。変更後に回答の品質が下… |
| [cicd 問14](../../exercises/cicd.md#q14) | 5.2.4 | 社内文書を根拠に回答する RAG アプリの評価を実行しました。取得のみのジョブでは ContextR… |
| [cicd 問15](../../exercises/cicd.md#q15) | 5.2.4 | 法律事務所向けの要約機能を、基盤モデルの新しい候補へ切り替えるか検討しています。評価の基準は、自社の… |
| [cicd 問16](../../exercises/cicd.md#q16) | 5.2.4 | AgentCore で動く社内エージェントは、複数のツールを呼び出して手続きを進めます。モデルの回答… |
| [cicd 問17](../../exercises/cicd.md#q17) | 5.2.5 | CodeDeploy で Lambda をカナリアでデプロイしています。デプロイグループに 5XX … |
| [cicd 問18](../../exercises/cicd.md#q18) | 5.2.5 | ECS のローリング更新にデプロイサーキットブレーカーとロールバックを設定しました。あるリリースで、… |
| [cicd 問19](../../exercises/cicd.md#q19) | 5.2.5 | Blue/Green で注文サービスを更新します。今回のリリースでは、customer_name の… |
| [cicd 問20](../../exercises/cicd.md#q20) | 5.2.5 | 複数のサービスを順にデプロイする CodePipeline の V2 タイプのパイプラインがあります… |

<!-- questions:end -->

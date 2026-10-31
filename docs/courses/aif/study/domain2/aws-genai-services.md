# 分野2: AWS の生成 AI サービス

どのサービスを誰が何のために使うかを、階層で整理して問います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [2.3.1](../../domain2.md#obj-2-3-1) | 生成 AI アプリのサービスと機能 |
| [2.3.2](../../domain2.md#obj-2-3-2) | AWS の生成 AI サービスを使う利点 |
| [2.3.3](../../domain2.md#obj-2-3-3) | AWS の基盤の利点 |

## 学習の順番 {#study-order}

1. [AWS の AI の 3 階層](../../../../services/ai-managed-services.md#three-layers): 3 階層と使う人、制御の大きさを覚えます。
2. [アプリから Bedrock を呼ぶ](../../../../services/ai.md#bedrock-runtime)と[JumpStart](../../../../services/sagemaker.md#jumpstart): API で使うか、自分のインスタンスで動かすかを区別します。
3. [AgentCore のアーキテクチャ](../../../../services/genai-apps.md#agentcore)と[マルチエージェント](../../../../services/genai-apps.md#multi-agent): エージェントを動かす基盤と書く道具を区別します。
4. [Amazon Quick](../../../../services/ai.md#quick)と[Kiro](../../../../services/ai.md#kiro): 業務ユーザー向けと開発者向けを区別します。
5. [入出力は学習に使われるか](../../../../services/ai.md#training-use): Bedrock の入出力の扱いを正確に覚えます。
6. [責任共有モデル](../../../../services/ai-fundamentals.md#shared-responsibility)と[AWS Artifact](../../../../services/cloud-foundations.md#artifact): AWS と利用者の担当、監査レポートの入手先を確認します。

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| インスタンスを管理せず複数の FM を試す | Bedrock |
| 事前学習済みモデルを自分のインスタンスに | JumpStart |
| コードなしで業務に使う | Quick |
| 仕様駆動で開発を AI に支援させる | Kiro |
| エージェントを本番で動かす | AgentCore |
| AWS の第三者の監査レポートを入手する | Artifact |
| 入出力がモデルの学習に使われるか | 使われず、提供者とも共有されない |

## 引っかかりやすい点 {#traps}

- PrivateLink が守るのは通信経路です。学習への利用の有無とは別の話です。
- AWS のサービスを使っても、データ、権限、プロンプト、ガードレールの設定は利用者の担当です。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [aws-genai-services 問1](../../exercises/aws-genai-services.md#q1) | 2.3.1 | インスタンスを管理せず、複数の FM を同じ API で試したいと考えています。適切なサービスはどれ… |
| [aws-genai-services 問2](../../exercises/aws-genai-services.md#q2) | 2.3.1 | 事前学習済みモデルのハブから FM を選び、自分のインスタンスにすぐデプロイしたいと考えています。適… |
| [aws-genai-services 問3](../../exercises/aws-genai-services.md#q3) | 2.3.1 | AWS の AI の 3 階層のうち、ML プラットフォームの階層にあり、最も細かく制御できるものは… |
| [aws-genai-services 問4](../../exercises/aws-genai-services.md#q4) | 2.3.1 | 営業部門の担当者が、コードを書かずに、社内の文書とデータをもとに調査レポートを作りたいと考えています… |
| [aws-genai-services 問5](../../exercises/aws-genai-services.md#q5) | 2.3.1 | 生成 AI アプリの部品と役割の組み合わせとして正しいものを選んでください。（2つ選択） |
| [aws-genai-services 問6](../../exercises/aws-genai-services.md#q6) | 2.3.2 | ML の専門家がいない部門でも、Bedrock の API で複数のモデルを試して PoC を作れま… |
| [aws-genai-services 問7](../../exercises/aws-genai-services.md#q7) | 2.3.2 | 基盤の管理が不要で、使った分だけ支払える点は、AWS の生成 AI サービスのどの利点に当たりますか… |
| [aws-genai-services 問8](../../exercises/aws-genai-services.md#q8) | 2.3.2 | 自社のアプリで FM を切り替えながら評価し、用途に最も合うものを選べました。これが示す利点はどれで… |
| [aws-genai-services 問9](../../exercises/aws-genai-services.md#q9) | 2.3.3 | Bedrock に送るプロンプトの扱いについて、セキュリティ部門から質問がありました。正しい説明はど… |
| [aws-genai-services 問10](../../exercises/aws-genai-services.md#q10) | 2.3.3 | 監査人に示すために、AWS の第三者の監査レポートを入手したいと考えています。AWS の基盤のコンプ… |
| [aws-genai-services 問11](../../exercises/aws-genai-services.md#q11) | 2.3.3 | 責任共有モデルで、Bedrock を使う利用者の担当に当たるものを選んでください。（2つ選択） |
| [aws-genai-services 問12](../../exercises/aws-genai-services.md#q12) | 2.3.3 | AWS の基盤を使うときの安全性の利点の例として正しいものはどれですか。 |

<!-- questions:end -->

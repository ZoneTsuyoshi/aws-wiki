# 分野4: AI

AI ツールでエラーを分析する方法と、最適化の機会を見つける方法が問われます。コード生成は[分野1](../domain1/ai.md)、データの保護は[分野2](../domain2/ai.md)、テストと CI/CD の支援は[分野3](../domain3/ai.md)で扱います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [4.1.5](../../domain4.md#skill-4-1-5) | AI によるエラー分析 |
| [4.3.6](../../domain4.md#skill-4-3-6) | AI による最適化 |

## 学習の順番 {#study-order}

1. [AI ツールで開発を支える](../../../../services/ai.md#ai-tools-lifecycle): 試験ガイドが製品を指定していないこと、対象一覧にないツールがあることを確認します。
2. [エラー分析とトラブルシューティング](../../../../services/ai.md#ai-troubleshooting): 場面ごとのツールを比べます。
3. [最適化](../../../../services/ai.md#ai-optimization): 確認できた機能と、一般的な実践を分けて読みます。
4. [Q Developer の現状](../../../../services/ai.md#q-developer): IDE とコンソールで影響が違うことを押さえます。

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| アラームの原因を AI で調べたい | CloudWatch investigations を使います。テレメトリ、デプロイイベント、CloudTrail、X-Ray から根本原因の仮説を示します |
| コンソールで権限や設定のエラーが出た | 「Diagnose with Amazon Q」を使います |
| コードのバグやビルド失敗を AI で直したい | Kiro の Bugfix Spec や、ヘッドレスでのビルド失敗の切り分けを使います |
| コードの効率を改善したい | Kiro なら Steering で性能要件を伝え、チャットで依頼します。Q Developer IDE の Optimize と Refactor も確認できた機能ですが、新規のサブスクリプションは停止済みで、2027-04-30 にサポートが終了します |
| トレースやメトリクスから改善案を得たい | X-Ray のトレースや CloudWatch のメトリクスを根拠として AI に渡します |

## 引っかかりやすい点 {#traps}

- **対象外のツールを前提にする:** AWS DevOps Agent、AWS Security Agent、Amazon CodeGuru Profiler は C03 の対象サービス一覧に載っていません。
- **Q Developer の終了を一律に考える:** IDE プラグインは 2027-04-30 にサポートが終了しますが、コンソールの Q Developer は影響を受けません。
- **AI の提案をそのまま適用する:** 根拠のログやトレースで検証してから適用します。スタックトレースやログを渡すときは、機密情報を含めないようにします。
- **権限の範囲を誤解する:** CloudWatch investigations はサインイン中のユーザーの権限で動き、操作は CloudTrail に残ります。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [ai 問10](../../exercises/ai.md#q10) | 4.3.5 | CloudWatch の AWS/Bedrock で、利用者が感じる待ち時間（最初の文字が表示される… |
| [ai 問33](../../exercises/ai.md#q33) | 4.1.5 | 深夜に API のエラー率のアラームが発火しました。担当者は、関連するメトリクス、ログ、デプロイイベ… |
| [ai 問34](../../exercises/ai.md#q34) | 4.1.5 | 開発者がコンソールで Lambda 関数を作成しようとすると、権限不足のエラーが表示されました。エラ… |
| [ai 問35](../../exercises/ai.md#q35) | 4.1.5 | 障害の調査で、AI ツールにスタックトレースとログを渡して修正案を受け取ります。適切な進め方はどれで… |
| [ai 問36](../../exercises/ai.md#q36) | 4.3.6 | ECS で動く Python のサービスの CPU 使用率が高く、どのコード行が高コストなのかわかり… |
| [ai 問37](../../exercises/ai.md#q37) | 4.3.6 | チームは Kiro にコードを改善させています。しかし、生成されたコードが社内の性能の基準（N+1 … |
| [ai 問38](../../exercises/ai.md#q38) | 4.3.6 | AI ツールが、X-Ray のトレースをもとに、Lambda 関数のメモリを 512 MB から 2… |

<!-- questions:end -->

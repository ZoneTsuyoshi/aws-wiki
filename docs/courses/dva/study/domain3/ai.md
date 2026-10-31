# 分野3: AI サービスと AI 開発ツール

分野3では、テストの生成と自動化、CI/CD の支援に AI ツールを使う方法が問われます。開発の支援と Bedrock の呼び出しは[分野1の AI](../domain1/ai.md)、権限や Guardrails は[分野2の AI](../domain2/ai.md)、エラー分析と最適化は[分野4の AI](../domain4/ai.md) で扱います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [3.2.5](../../domain3.md#skill-3-2-5) | AI ツールによるテストの生成と自動化 |
| [3.3.9](../../domain3.md#skill-3-3-9) | AI ツールによる CI/CD の支援 |

## 学習の順番 {#study-order}

1. [AI ツールで開発を支える](../../../../services/ai.md#ai-tools-lifecycle): 試験ガイドが製品を指定していないことと、対象サービス一覧との関係を確認します。
2. [Kiro](../../../../services/ai.md#kiro)と [Hooks の設定](../../../../services/ai.md#hooks-settings): Specs と Hooks の役割を理解します。
3. [テスト生成と自動化](../../../../services/ai.md#ai-testing): ツールごとの機能と、一般的な実践を区別します。
4. [CI/CD の支援](../../../../services/ai.md#ai-cicd): パイプラインからの実行方法と、組み合わせで実現する項目を確認します。
5. [Amazon Q Developer の現状](../../../../services/ai.md#q-developer): C02 と C03 の違いを押さえます。

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 要件から正しさの性質を抽出して検証 | Kiro の Specs のプロパティベーステスト。ランダム入力で実行し、失敗時は最小の入力まで縮小して示す |
| エージェントの変更に合わせてテストを実行 | Kiro の Hooks。File Save で変更ファイルのテスト |
| Spec のタスク完了後にテストを実行 | Kiro の Hooks。Post Task Execution |
| 回帰を防ぎながらバグを直す | Kiro の Bugfix Spec |
| パイプラインでテストの生成やレビューを実行 | Kiro CLI のヘッドレスモード。認証は `KIRO_API_KEY`、`--no-interactive` で実行し、`--trust-tools` で許可ツールを最小にする |
| ビルド失敗の切り分けを自動化 | Kiro CLI のヘッドレスモード |
| AI の評価でデプロイを承認 | CodePipeline の承認やテストのステージで、AI の評価を人の判断材料にする。本番は人の承認を残す |
| AI で環境を用意 | Kiro などに IaC テンプレートを書かせ、レビュー後に CloudFormation や SAM でデプロイする |
| カバレッジを上げる | CI で計測し、不足箇所のテスト作成を AI に頼む |
| C02 で単体テストを生成 | Q Developer の Generate tests。Java と Python が対象で、1 ファイルずつ処理する。新規の Free Tier とサブスクリプションは 2026-05-15 に停止 |

## 引っかかりやすい点 {#traps}

- **手で保存しても Hook が動かない**: ファイルのトリガーは、エージェントによる変更にだけ反応します。
- **生成したテストをそのまま信じる**: 実装の誤りをそのまま正解にしていることがあります。人が確認します。
- **AWS DevOps Agent を答えに選ぶ**: DVA-C03 の対象サービス一覧に載っていません。リリース管理の機能はプレビューです。Security Agent も同様に一覧にありません。
- **自動承認の専用機能があると考える**: 専用の AWS 製品機能は確認できておらず、CodePipeline などとの組み合わせで実現します。カバレッジの確保を担う機能も同様です。
- **C03 でも Q Developer を選ぶ**: C03 の対象一覧には Kiro が載っており、Q Developer はありません。IDE プラグインのサポートは 2027 年 4 月 30 日に終了します。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [ai 問27](../../exercises/ai.md#q27) | 3.2.5 | Kiro の Spec で決済の端数処理を実装しています。例を手で並べるテストでは、思いつかない入力… |
| [ai 問28](../../exercises/ai.md#q28) | 3.2.5 | Kiro の Spec でタスクを順に実装しています。タスクが 1 つ完了するたびに、回帰テストのス… |
| [ai 問29](../../exercises/ai.md#q29) | 3.2.5 | AI に既存の関数の単体テストを生成させました。カバレッジは 95% に上がり、全テストが成功してい… |
| [ai 問30](../../exercises/ai.md#q30) | 3.3.9 | CodeBuild のステージで Kiro CLI（V3）を動かし、プルリクエストの変更をレビューさ… |
| [ai 問31](../../exercises/ai.md#q31) | 3.3.9 | AI にリリース前の変更をレビューさせ、その結果を CodePipeline に組み込みます。社内の… |
| [ai 問32](../../exercises/ai.md#q32) | 3.3.9 | 検証環境を用意するために、Kiro に CloudFormation テンプレートを書かせます。展開… |

<!-- questions:end -->

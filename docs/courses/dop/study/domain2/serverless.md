# 分野2: Lambda と Step Functions の自動化

Lambda の 15 分の制約を超える自動化の設計を問います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [Lambda と Step Functions](../../domain2.md#t2-3-lambda) | 複雑なシナリオの Lambda の自動化 |

## 学習の順番 {#study-order}

1. [Standard と Express](../../../../services/step-functions.md#standard-express): 実行時間と用途の違いを確認します。
2. [エラー処理](../../../../services/step-functions.md#error-handling): `Retry` と `Catch` を押さえます。
3. [人の承認](../../../../services/step-functions.md#human-approval): `waitForTaskToken` の流れを理解します。
4. [冪等性](../../../../services/sdk-resilience.md#idempotency): 再実行で壊れない処理を確認します。
5. [リトライ](../../../../services/sdk-resilience.md#retries): スロットリングへの備えを覚えます。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| Lambda の実行時間 | 最大 15 分 | 超えるなら Step Functions |
| Express の実行時間 | 最大 5 分 | 長い運用の工程は Standard |
| SQS の可視性タイムアウト | 最大 12 時間 | 承認の待機には使わない |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 全アカウントに同じ操作をする | `Map` で分散して各アカウントのロールを引き受ける |
| 人の承認を数日待つ | `waitForTaskToken` |
| API のスロットリング | SDK の再試行と並行数の制限 |

## 引っかかりやすい点 {#traps}

- Provisioned Concurrency は同時に呼ぶ数を減らす手段ではありません。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [serverless 問1](../../exercises/serverless.md#q1) | Lambda と Step Functions | 全 300 アカウントのセキュリティグループを調べて、許可しないルールを削除します。処理はアカウント… |
| [serverless 問2](../../exercises/serverless.md#q2) | Lambda と Step Functions | 本番の設定を変える自動化で、変更の前に担当者の承認を最大 3 日待ちます。Lambda は再実行され… |
| [serverless 問3](../../exercises/serverless.md#q3) | Lambda と Step Functions | Lambda で複数のアカウントの API を大量に呼ぶ自動化が、ThrottlingExcepti… |

<!-- questions:end -->

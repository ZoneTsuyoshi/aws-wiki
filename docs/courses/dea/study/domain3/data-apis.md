# 分野3: SDK と API の運用

SDK からの呼び出しと、データ API を保守するときの機能を問います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [3.1.3](../../domain3.md#skill-3-1-3) | SDK からの AWS 機能の呼び出し |
| [3.1.5](../../domain3.md#skill-3-1-5) | データ API の利用と保守 |

## 学習の順番 {#study-order}

1. [AWS SDK の基本](../../../../services/sdk-resilience.md#sdk-basics): 認証情報の取得元を確認します。
2. [ウェイター](../../../../services/sdk-resilience.md#waiters): 状態の確認の方法を覚えます。
3. [再試行モード](../../../../services/sdk-resilience.md#retry-modes): 一時的な失敗への備えです。
4. [使用量プランと API キー](../../../../services/api-gateway.md#usage-plans): 取引先ごとの制限を確認します。
5. [エラーコード](../../../../services/api-gateway.md#errors): 429 と 504 を区別します。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| `ClientToken` | 8 時間有効 | 再試行の重複を防ぐ |
| Data API の結果 | 24 時間で消える |  |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| Athena の結果を取る | `get_query_execution` で完了を確認してから |
| 取引先ごとの 1 日の上限 | 使用量プラン |
| 変更を安全に出す | ステージとカナリアリリース |
| 同じ問い合わせの費用を下げる | API Gateway のキャッシュ |

## 引っかかりやすい点 {#traps}

- データ系の API の多くは非同期です。
- Step Functions の再試行で SQL を重複させないよう、`ClientToken` を渡します。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [data-apis 問7](../../exercises/data-apis.md#q7) | 3.1.3 | SDK で Athena のクエリを実行します。start_query_execution の直後に… |
| [data-apis 問8](../../exercises/data-apis.md#q8) | 3.1.3 | SDK のページネーターとウェイターの説明として正しいものはどれですか。（2つ選択） |
| [data-apis 問9](../../exercises/data-apis.md#q9) | 3.1.3 | Lambda から boto3 で Glue ジョブを起動します。一時的な失敗に耐え、認証情報はコー… |
| [data-apis 問10](../../exercises/data-apis.md#q10) | 3.1.5 | データ API を取引先に公開します。取引先ごとに 1 日のリクエスト数を制限します。REST AP… |
| [data-apis 問11](../../exercises/data-apis.md#q11) | 3.1.5 | データ API の呼び出し元に、次のエラーが返りました。対応として正しいものはどれですか。（2つ選択… |
| [data-apis 問12](../../exercises/data-apis.md#q12) | 3.1.5 | Step Functions から Redshift Data API の ExecuteState… |
| [data-apis 問13](../../exercises/data-apis.md#q13) | 3.1.5 | Redshift Data API を使うアプリが、前の日の GetStatementResult … |

<!-- questions:end -->

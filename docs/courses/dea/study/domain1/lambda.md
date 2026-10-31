# 分野1: Lambda

コードの最適化、同時実行の設定、一時的なストレージの選び方を問います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [1.4.1](../../domain1.md#skill-1-4-1) | 実行時間を短くするコードの最適化 |
| [1.4.2](../../domain1.md#skill-1-4-2) | Lambda の同時実行と性能の設定 |
| [1.4.7](../../domain1.md#skill-1-4-7) | Lambda でのストレージボリュームの利用 |

## 学習の順番 {#study-order}

1. [コードの最適化](../../../../services/lambda.md#code-optimization): クライアントの再利用を確認します。
2. [メモリ](../../../../services/lambda.md#memory): CPU との関係を覚えます。
3. [予約済みと Provisioned](../../../../services/lambda.md#reserved-provisioned): 枠と事前初期化を区別します。
4. [エフェメラルストレージ](../../../../services/lambda.md#ephemeral-storage): `/tmp` の範囲を確認します。
5. [EFS と Lambda](../../../../services/storage.md#efs-lambda): VPC とマウントの条件を覚えます。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| メモリ | 128〜10,240 MB | 増やすと CPU も増える |
| タイムアウト | 既定 3 秒、最大 900 秒 | 長い処理は Glue へ |
| `/tmp` | 512〜10,240 MB | 実行環境ごとで共有されない |
| アカウントの同時実行数 | 既定 1,000 | 引き上げ可能 |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 下流のデータベースを守る | 予約済み同時実行 |
| コールドスタートを抑える | Provisioned Concurrency |
| CPU を増やす | メモリを増やす |
| 関数の間でファイルを共有する | EFS |
| 読み込みの前に絞る | `push_down_predicate`、必要な列だけ |

## 引っかかりやすい点 {#traps}

- EFS に接続するには関数を VPC に接続します。接続できなければ 2049 番を確認します。
- Provisioned Concurrency は上限ではありません。超えた分はオンデマンドで動きます。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [lambda 問1](../../exercises/lambda.md#q1) | 1.4.1 | Lambda の処理で、毎回 S3 クライアントを作り直しているため遅いです。コード上の改善はどれで… |
| [lambda 問2](../../exercises/lambda.md#q2) | 1.4.1 | Spark のジョブで全パーティションを読んだ後に日付で絞っており、時間がかかります。コードの最適化… |
| [lambda 問3](../../exercises/lambda.md#q3) | 1.4.1 | 実行時間を短くする書き換えとして正しいものはどれですか。 |
| [lambda 問4](../../exercises/lambda.md#q4) | 1.4.2 | CPU を多く使う変換の関数が遅いです。Lambda で CPU を増やす設定はどれですか。 |
| [lambda 問5](../../exercises/lambda.md#q5) | 1.4.2 | 書き込み先のデータベースが耐えられるのは同時 50 接続です。関数がこれを超えないようにします。最も… |
| [lambda 問6](../../exercises/lambda.md#q6) | 1.4.2 | レイテンシに敏感な API の関数で、コールドスタートを抑えます。費用は許容します。どの設定ですか。 |
| [lambda 問7](../../exercises/lambda.md#q7) | 1.4.7 | 関数が S3 から 3 GB のファイルを取得して変換します。別の関数と共有はしません。最も簡単な置… |
| [lambda 問8](../../exercises/lambda.md#q8) | 1.4.7 | 複数の関数で共有する大きなモデルファイルを置きます。関数の設定で必要なものはどれですか。 |
| [lambda 問9](../../exercises/lambda.md#q9) | 1.4.7 | 関数から EFS へのマウントがタイムアウトします。確認すべきものはどれですか。（2つ選択） |

<!-- questions:end -->

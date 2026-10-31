# 分野3: Lambda

分野3では、デプロイパッケージの選び方、バージョンとエイリアスによる環境の分離、テストイベントが問われます。関数の設定やイベントソースは[分野1の Lambda](../domain1/lambda.md)、メモリや同時実行の調整は[分野4の Lambda](../domain4/lambda.md) で扱います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [3.1.1](../../domain3.md#skill-3-1-1) | レイヤーと環境変数による依存関係の管理 |
| [3.1.4](../../domain3.md#skill-3-1-4) | 環境ごとの設定 |
| [3.2.3](../../domain3.md#skill-3-2-3) | テストイベント |
| [3.2.4](../../domain3.md#skill-3-2-4) | エイリアスによる環境の分離 |
| [3.3.1](../../domain3.md#skill-3-3-1) | デプロイパッケージ |
| [3.3.6](../../domain3.md#skill-3-3-6) | 重み付きエイリアスによるカナリア |
| [3.3.7](../../domain3.md#skill-3-3-7) | エイリアスを戻す手動のロールバック |

## 学習の順番 {#study-order}

1. [デプロイパッケージ](../../../../services/lambda.md#packaging): .zip、レイヤー、コンテナイメージの上限と向いている場面を比べます。
2. [効率を上げるコツ](../../../../services/lambda.md#packaging-tips): パッケージを小さくする方法と、ベースイメージの違いを確認します。
3. [レイヤー](../../../../services/lambda.md#layers): `/opt` への展開とバージョンの指定を覚えます。
4. [環境変数](../../../../services/lambda.md#environment-variables): 値をコードから分ける方法と、バージョンで固定されることを押さえます。
5. [バージョンとエイリアス](../../../../services/lambda.md#versions-aliases): 発行時に固定されるものと、後から変えられるものを区別します。
6. [エイリアスによる環境の分離](../../../../services/lambda.md#alias-environments)と[トラフィックの分割](../../../../services/lambda.md#alias-routing): 環境の分け方と、重みの制約を覚えます。
7. [テストイベントとテスト](../../../../services/lambda.md#testing): コンソール、SAM、CLI の使い分けを確認します。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| .zip | 直接 50 MB、展開後 250 MB | 大きいファイルは S3 経由 |
| コンテナイメージ | 10 GB | 依存関係が 250 MB を超えるときの答え |
| レイヤー | 5 個 | 本体と合わせて展開後 250 MB |
| 環境変数 | 合計 4 KB | 大きな設定は Parameter Store や AppConfig へ |
| エイリアスの重み | 0.0〜1.0、2 バージョンまで | `0.1` が 10% |
| プライベートのテストイベント | 関数ごとに 10 個 | 共有するなら共有イベント |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 3 つの関数で同じライブラリを使う | `python/requests/` を入れたレイヤーにまとめ、各パッケージから外す |
| 依存関係が 250 MB を超える | コンテナイメージにして ECR に置く |
| 呼び出し元を変えずに本番を切り替える | エイリアス経由で呼び、`update-alias` で指す先を変える |
| ステージングで検証済みのバージョン 7 を本番へ | `aws lambda update-alias --function-name orders --name prod --function-version 7` |
| 新バージョンに 10% だけ流す | `RoutingConfig` の `AdditionalVersionWeights` に `{"5": 0.1}`。自動で進めるなら CodeDeploy |
| 本番で問題が出たのですぐ戻す | エイリアスを前のバージョンへ向ける |
| 同じコードで値だけ環境ごとに変える | 環境ごとにバージョンを発行するか、関数を分ける。値を外に置くなら[環境別の設定](../../../../services/secrets.md#environment-config) |
| SQS のイベントでローカルテスト | `sam local generate-event sqs receive-message > event.json`、`sam local invoke MyFunction -e event.json` |
| デプロイ済みの `test` エイリアスを CLI で呼ぶ | `aws lambda invoke --function-name my-function:test --cli-binary-format raw-in-base64-out --payload file://event.json response.json` |
| テストイベントをチームで共有 | コンソールの共有イベント（スキーマレジストリ `lambda-testevent-schemas` に保存） |

## 引っかかりやすい点 {#traps}

- **レイヤーを更新したのに反映されない**: 関数はバージョン番号付きの ARN を指します。新しいバージョンを発行しても自動では切り替わりません。
- **コンテナイメージの関数でレイヤーを使いたい**: 使えません。依存関係はイメージに含めます。
- **重み付きエイリアスを設定できない**: どちらのバージョンも発行済みで、実行ロールと DLQ の設定が同じである必要があります。`$LATEST` は指定できません。
- **発行しても新しいバージョンができない**: `$LATEST` が前のバージョンと同じなら作られません。
- **環境変数を変えても本番が変わらない**: バージョンを発行すると環境変数も固定されます。
- **SQS のテストで本文が辞書にならない**: `body` は文字列です。JSON なら自分で解析します。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [lambda 問14](../../exercises/lambda.md#q14) | 3.1.1 | ネイティブ拡張を使う Python 関数を x86_64 から arm64 に移行します。設定変更の… |
| [lambda 問16](../../exercises/lambda.md#q16) | 3.3.6, 3.2.4 | prod エイリアスで、バージョン 4 に 90%、バージョン 5 に 10% を流す設定をします。… |
| [lambda 問20](../../exercises/lambda.md#q20) | 3.3.1 | 会社は Lambda 関数にコード署名を導入しました。署名されていないコードは本番でデプロイできない… |
| [lambda 問21](../../exercises/lambda.md#q21) | 3.2.3 | API Gateway のプロキシ統合で呼ばれる Python の関数を、コンソールのテストイベント… |
| [lambda 問22](../../exercises/lambda.md#q22) | 3.3.1 | Lambda のデプロイパッケージについて、正しい説明はどれですか。（2つ選択） |
| [lambda 問23](../../exercises/lambda.md#q23) | 3.3.1 | 5 つの関数が、同じ 40 MB の共通ライブラリをそれぞれの .zip に含めています。デプロイを… |

<!-- questions:end -->

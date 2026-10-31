# 分野3: API Gateway

分野3では、ステージによる環境の分離、Mock 統合、テストの方法が問われます。統合や変換の作り方は[分野1の API Gateway](../domain1/api-gateway.md)、認可は[分野2の API Gateway](../domain2/api-gateway.md)、エラーやキャッシュの調整は[分野4の API Gateway](../domain4/api-gateway.md) で扱います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [3.1.4](../../domain3.md#skill-3-1-4) | ステージ変数による環境ごとの設定 |
| [3.1.5](../../domain3.md#skill-3-1-5) | ステージの URL、エンドポイント、カスタムドメイン |
| [3.2.2](../../domain3.md#skill-3-2-2) | Mock 統合 |
| [3.2.3](../../domain3.md#skill-3-2-3) | テストイベント |
| [3.2.4](../../domain3.md#skill-3-2-4) | ステージによる環境の分離 |
| [3.3.6](../../domain3.md#skill-3-3-6) | カナリアリリース |
| [3.3.7](../../domain3.md#skill-3-3-7) | 過去のデプロイへ戻す |

## 学習の順番 {#study-order}

1. [デプロイとステージ](../../../../services/api-gateway.md#stages): デプロイとステージの関係と、再デプロイが必要な変更を理解します。
2. [ステージの設定](../../../../services/api-gateway.md#stage-settings): ステージごとに変えられる項目を確認します。
3. [ステージ変数](../../../../services/api-gateway.md#stage-variables): Lambda エイリアスやバックエンド URL の切り替え方を覚えます。
4. [エンドポイントタイプ](../../../../services/api-gateway.md#endpoint-types)と[カスタムドメイン](../../../../services/api-gateway.md#custom-domains): 利用者の場所から選び、証明書のリージョンを覚えます。
5. [モック統合](../../../../services/api-gateway.md#mock-integration): 設定の 3 つの手順を押さえます。
6. [テスト用エンドポイントとテストイベント](../../../../services/api-gateway.md#test-endpoints): テストの手段と、プロキシ統合のイベントの形を確認します。
7. [カナリアリリース](../../../../services/api-gateway.md#canary): 割合の指定と昇格の流れをつかみます。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| ステージ数 | API あたり 10 | REST API の既定の上限 |
| ステージ変数 | 100 個、キー 64 文字、値 512 文字 | 機密情報は入れない |
| `percentTraffic` | 0.0〜100.0 | カナリアに流す割合 |
| URL の形 | `https://{api-id}.execute-api.{region}.amazonaws.com/{stage}` | ステージごとに変わる |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| REST API を変更したのに反映されない | ステージへデプロイする。ステージの設定だけならデプロイは不要 |
| dev と prod で別の Lambda エイリアスを呼ぶ | 統合の ARN に `${stageVariables.alias}` を入れ、エイリアスごとに `aws lambda add-permission` |
| バックエンドが未完成でも開発を進める | `type` が `MOCK` の統合で固定の応答を返す |
| エラーの動作も Mock で試す | クエリ文字列で 200 と 500 を切り替える |
| 5% だけ新しい Lambda エイリアスへ | カナリアの `percentTraffic: 5` と `stageVariableOverrides` で `alias` を変える。問題なければ昇格する |
| 問題のあるデプロイから戻す | ステージの向き先を過去のデプロイに変える |
| 世界中の利用者向けに自前の CloudFront を使う | リージョン API を選ぶ |
| `api.example.com/orders` を注文 API の prod へ | カスタムドメインを作り、API マッピングでパスとステージを結ぶ |
| プロキシ統合の Lambda 用のテストイベント | `sam local generate-event apigateway aws-proxy` |
| API をローカルで起動して試す | `sam local start-api` |

## 引っかかりやすい点 {#traps}

- **コンソールのテストでデータが変わる**: ログは模擬ですが、バックエンドの呼び出しは本物です。
- **Mock が期待の応答を返さない**: 統合リクエストのテンプレートがないか、`statusCode` を返していません。メソッドレスポンスにも同じステータスを宣言します。
- **HTTP API で Mock を使おうとする**: Mock 統合は REST API の機能です。
- **ステージ変数にした途端 Lambda を呼べない**: 権限は自動で付きません。`add-permission` で関数やエイリアスごとに許可します。
- **ステージ変数で統合タイプを変えようとする**: 変えられるのは接続先の名前や URL です。`HTTP_PROXY` を Lambda に変えることはできません。
- **ステージを別のデプロイに切り替えられない**: カナリアが有効な間はできません。無効にして設定を外してから行います。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [api-gateway 問1](../../exercises/api-gateway.md#q1) | 3.1.5 | REST API の本番ステージで次の変更をしました。変更を反映するために、ステージへの再デプロイが… |
| [api-gateway 問7](../../exercises/api-gateway.md#q7) | 3.2.4 | REST API の統合の URI で ${stageVariables.alias} を使い、ステ… |
| [api-gateway 問8](../../exercises/api-gateway.md#q8) | 3.3.6 | REST API の prod ステージにカナリアリリースを設定しました。開発者はカナリアへのリクエ… |
| [api-gateway 問14](../../exercises/api-gateway.md#q14) | 3.2.2 | 外部の決済 API がまだ利用できない状態で、REST API の開発を進めます。バックエンドなしで… |
| [api-gateway 問19](../../exercises/api-gateway.md#q19) | 3.1.5 | HTTP API で運用中の API に新しい要件が追加されました。REST API に移行しないと… |
| [api-gateway 問21](../../exercises/api-gateway.md#q21) | 3.2.2 | REST API のモック統合で、決まった JSON を 200 で返します。必要な設定はどれですか… |
| [api-gateway 問22](../../exercises/api-gateway.md#q22) | 3.2.2 | 外部 API のモックを REST API で作り、結合テストで成功と失敗の両方を再現します。クエリ… |
| [api-gateway 問23](../../exercises/api-gateway.md#q23) | 3.2.3 | REST API の DELETE /items/{id} を、コンソールのメソッドの Test タ… |

<!-- questions:end -->

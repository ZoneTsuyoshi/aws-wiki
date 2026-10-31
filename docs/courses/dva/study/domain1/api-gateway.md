# 分野1: API Gateway

分野1では、API の作り方、特に統合タイプの選択、リクエストとレスポンスの変換、検証を問われます。認可は[分野2](../domain2/api-gateway.md)、ステージとデプロイは[分野3](../domain3/api-gateway.md)、ログや障害の調査は[分野4](../domain4/api-gateway.md)で扱います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [1.1.2](../../domain1.md#skill-1-1-2) | 同期の API と非同期の処理の使い分け |
| [1.1.4](../../domain1.md#skill-1-1-4) | API の作成と保守、変換、検証 |
| [1.2.4](../../domain1.md#skill-1-2-4) | Lambda との統合 |

## 学習の順番 {#study-order}

1. [API の種類](../../../../services/api-gateway.md#api-types): REST API、HTTP API、WebSocket API の違いをつかみます。
2. [統合タイプ](../../../../services/api-gateway.md#integration-types): `AWS_PROXY`、`AWS`、`HTTP_PROXY`、`HTTP`、`MOCK` を、変換の有無で区別します。
3. [プロキシ統合](../../../../services/api-gateway.md#proxy-integration): 関数が返す形式と、502 になる原因を覚えます。
4. [非プロキシ統合の流れ](../../../../services/api-gateway.md#non-proxy-flow): 4つの段階と、それぞれの設定を覚えます。
5. [マッピングテンプレート](../../../../services/api-gateway.md#mapping-templates)、[テンプレートがないときの動き](../../../../services/api-gateway.md#passthrough): 主な変数と `passthroughBehavior` の3つの値を学びます。
6. [ステータスコードの上書き](../../../../services/api-gateway.md#status-override): `$context.responseOverride` の使い方を確認します。
7. [リクエストの検証](../../../../services/api-gateway.md#request-validation): モデルとバリデーターの関係と、検証できる範囲を押さえます。
8. [Lambda の非同期呼び出し](../../../../services/api-gateway.md#lambda-async)、[モック統合](../../../../services/api-gateway.md#mock-integration)、[エラーコード](../../../../services/api-gateway.md#errors): 長い処理の逃がし方、バックエンドなしの開発、コードごとの原因を確認します。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| 統合タイムアウト（REST） | 既定 29 秒、50 ms〜29 秒 | リージョンとプライベートは引き上げられます。エッジ最適化はできません |
| 統合タイムアウト（HTTP） | 最大 30 秒 | 超える処理は非同期にします |
| ペイロード（REST、HTTP） | 10 MB | 超えるなら S3 の署名付き URL に切り替えます |
| マッピングテンプレート | 300 KB、`#foreach` 1,000 回 | |
| モデル | API あたり合計 400 KB | |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| Lambda を単純に呼びたい | プロキシ統合（`AWS_PROXY`）にします。AWS もこれを勧めています |
| 古い形式のクライアントと新しいバックエンドをつなぐ | 非プロキシ統合とマッピングテンプレートで変換します |
| バックエンドを動かさずに不正なリクエストを弾く | モデルとバリデーターを設定します。失敗すると 400 を返します |
| 統合が 200 を返しても、内容によって 400 で返したい | テンプレートで `$context.responseOverride.status` を設定します |
| Lambda カスタム統合で、エラーメッセージから 404 を返す | 統合レスポンスの `selectionPattern` に `.*NotFound.*` を指定します |
| 2 分かかるレポート作成を受け付ける | Lambda 非プロキシ統合で、統合リクエストのヘッダー `X-Amz-Invocation-Type` を `'Event'` にして非同期で呼びます |
| 数分かかる処理の結果を返したい | SQS に入れて 202 と受付 ID を返し、別の API で状態を確認させます |
| 40 秒かかる処理をリージョン API で同期のまま返す | クォータの引き上げを申請し、`timeoutInMillis` を 45,000 にします。アカウントのスロットリングの枠が減ることがあります |
| バックエンドが未完成でも開発を進めたい | モック統合を使います |
| `application/json` のテンプレートだけで、他の形式を 415 で弾きたい | `passthroughBehavior` を `WHEN_NO_TEMPLATES` か `NEVER` にします |

## 引っかかりやすい点 {#traps}

- プロキシ統合で 502 が返るときは、応答の形式を疑います。`body` に辞書を入れるのがよくある原因で、`json.dumps()` で文字列にします。
- 関数のタイムアウトを 60 秒にしても、統合タイムアウトが 29 秒ならクライアントには 29 秒で 504 が返ります。
- モデルを指定しただけでは検証されません。メソッドにバリデーターも指定します。
- パラメーターの検証は、存在と空でないことしか見ません。`?limit=abc` は通るので、型の確認はバックエンドで行います。
- `WHEN_NO_MATCH` は、想定外の形式をそのままバックエンドに渡します。
- メソッドレスポンスで宣言していないステータスは、統合レスポンスからマッピングできません。プロキシ統合ではこの段階を設定しません。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [api-gateway 問2](../../exercises/api-gateway.md#q2) | 1.1.4 | リージョン API の REST API で、Lambda の処理に約 40 秒かかり、クライアント… |
| [api-gateway 問3](../../exercises/api-gateway.md#q3) | 1.1.4 | ペイロード形式バージョン 2.0 の Lambda 統合を使う HTTP API で、関数が {"m… |
| [api-gateway 問4](../../exercises/api-gateway.md#q4) | 1.1.4 | REST API の非プロキシ統合に、application/json のマッピングテンプレートだけ… |
| [api-gateway 問5](../../exercises/api-gateway.md#q5) | 1.1.4 | Lambda プロキシ統合の REST API で JPEG を返しています。関数は Base64 … |
| [api-gateway 問6](../../exercises/api-gateway.md#q6) | 1.1.4 | REST API のメソッドで limit を必須のクエリパラメーターにし、パラメーターのバリデータ… |
| [api-gateway 問17](../../exercises/api-gateway.md#q17) | 1.1.4 | HTTP API に CORS 設定を追加しています。開発者が Lambda の応答の Access… |
| [api-gateway 問20](../../exercises/api-gateway.md#q20) | 1.1.4 | チャットアプリの WebSocket API で、メッセージのないクライアントの接続が約 10 分で… |

<!-- questions:end -->

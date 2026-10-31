# 分野5: DNS と配信

ハイブリッドの名前解決、ルーティング、キャッシュの問題を問います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [5.2.1](../../domain5.md#skill-5-2-1) | DNS の設定 |
| [5.2.2](../../domain5.md#skill-5-2-2) | Route 53 のルーティングとクエリログ |
| [5.2.3](../../domain5.md#skill-5-2-3) | CloudFront と Global Accelerator |
| [5.3.3](../../domain5.md#skill-5-3-3) | CloudFront のキャッシュの問題 |

## 学習の順番 {#study-order}

1. [VPC Resolver](../../../../services/network-connectivity.md#vpc-resolver)、[エンドポイント](../../../../services/network-connectivity.md#resolver-endpoints)と[ハイブリッド DNS](../../../../services/network-connectivity.md#hybrid-dns): 2 つの方向を確認します。
2. [プライベートホストゾーン](../../../../services/network-connectivity.md#private-hosted-zones)と[VPC の DNS 属性](../../../../services/networking.md#vpc-dns-attributes): 名前が引けないときの確認を押さえます。
3. [ルーティングポリシー](../../../../services/networking.md#routing-policies)と[TTL とエイリアスの違い](../../../../services/networking.md#route53-ttl): ポリシーとエイリアスを確認します。
4. [Global Accelerator](../../../../services/network-connectivity.md#global-accelerator)と[CloudFront](../../../../services/networking.md#cloudfront): 2 つのサービスを比較します。
5. [S3 オリジンの保護: OAC](../../../../services/networking.md#oac)と[オリジンフェイルオーバー](../../../../services/networking.md#origin-failover): オリジンの保護と切り替えを確認します。
6. [キャッシュキーとポリシー](../../../../services/networking.md#cache-keys)、[キャッシュポリシーの項目と TTL の計算](../../../../services/networking.md#ttl-worked)と[キャッシュの無効化](../../../../services/networking.md#invalidation): キャッシュの問題を確認します。
7. [CloudFront のエラー](../../../../services/networking.md#cloudfront-errors)と[エラー応答のキャッシュ](../../../../services/networking.md#error-caching): エラーを見分けます。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| 複数値回答 | 最大 8 個 | 正常なレコードをランダムに返す |
| パブリック DNS のクエリログ | `us-east-1` の CloudWatch Logs | キャッシュの間は記録されない |
| トラフィックダイヤルの既定 | 100% | 保守で 0 に下げる |
| エンドポイントの重みの既定 | 128 | グループの中の割合 |
| 無効化 | 月 1,000 パスまで無料 | `/*` は 1 パス |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| VPC からオンプレミスの名前を引く | アウトバウンドと転送ルール |
| オンプレミスから VPC の名前を引く | インバウンド |
| 法令で国ごとに振り分ける | 位置情報 |
| ゾーンの頂点を ALB へ | エイリアス |
| 固定 IP と TCP の独自プロトコル | Global Accelerator |
| S3 を直接公開しない | OAC とバケットポリシー |
| ヒット率が低い | キャッシュキーを絞り、オリジンリクエストポリシーへ |

## 引っかかりやすい点 {#traps}

- CloudFront のオリジンフェイルオーバーは `GET`、`HEAD`、`OPTIONS` のみです。
- ブラウザのキャッシュは無効化で消えません。
- VPC の既定のリゾルバーはオンプレミスからの転送に対応していません。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [dns-cdn 問1](../../exercises/dns-cdn.md#q1) | 5.2.1 | 東京の VPC のアプリから、オンプレミスの db.corp.example を名前で引きたいです。… |
| [dns-cdn 問2](../../exercises/dns-cdn.md#q2) | 5.2.1 | オンプレミスから VPC のプライベートホストゾーンの名前を引きたいです。条件付きフォワードの先はど… |
| [dns-cdn 問3](../../exercises/dns-cdn.md#q3) | 5.2.1 | プライベートホストゾーンのレコードが VPC から解決できません。確認するものを選んでください。（2… |
| [dns-cdn 問4](../../exercises/dns-cdn.md#q4) | 5.2.1 | 転送ルールを別のアカウントの VPC でも使いたいです。どうしますか。 |
| [dns-cdn 問5](../../exercises/dns-cdn.md#q5) | 5.2.1 | Resolver エンドポイントの設定として正しいものを選んでください。（2つ選択） |
| [dns-cdn 問6](../../exercises/dns-cdn.md#q6) | 5.2.2 | 次の要件に合うルーティングポリシーはどれですか。新しいバージョンに 10% のトラフィックだけを流し… |
| [dns-cdn 問7](../../exercises/dns-cdn.md#q7) | 5.2.2 | 法令の要件で、ドイツの利用者をフランクフルトのリソースへ必ず振り分けます。どのポリシーを使いますか。 |
| [dns-cdn 問8](../../exercises/dns-cdn.md#q8) | 5.2.2 | ゾーンの頂点 example.com を ALB へ向けたいです。何を使いますか。 |
| [dns-cdn 問9](../../exercises/dns-cdn.md#q9) | 5.2.2 | パブリックホストゾーンのクエリログを有効にしましたが、問い合わせの回数が想定より少なく見えます。正し… |
| [dns-cdn 問10](../../exercises/dns-cdn.md#q10) | 5.2.2 | VPC のインスタンスの DNS の問い合わせを調査したいです。VPC フローログには Amazon… |
| [dns-cdn 問11](../../exercises/dns-cdn.md#q11) | 5.2.2 | パブリック DNS のクエリログの設定で正しいものを選んでください。（2つ選択） |
| [dns-cdn 問12](../../exercises/dns-cdn.md#q12) | 5.2.3 | 世界中の企業の利用者が、ファイアウォールの許可リストに固定 IP を登録する必要があります。TCP … |
| [dns-cdn 問13](../../exercises/dns-cdn.md#q13) | 5.2.3 | S3 オリジンを直接公開せず、CloudFront 経由だけで配信したいです。どの設定を使いますか。 |
| [dns-cdn 問14](../../exercises/dns-cdn.md#q14) | 5.2.3 | CloudFront のオリジングループを設定しました。POST のリクエストが、プライマリの障害の… |
| [dns-cdn 問15](../../exercises/dns-cdn.md#q15) | 5.2.3 | Global Accelerator の保守で、リージョンのトラフィックを一時的に 0 にしたいです… |
| [dns-cdn 問16](../../exercises/dns-cdn.md#q16) | 5.2.3 | CloudFront の設定について正しいものを選んでください。（2つ選択） |
| [dns-cdn 問17](../../exercises/dns-cdn.md#q17) | 5.3.3 | CloudFront のヒット率が低いです。キャッシュキーに全 Cookie とクエリ文字列を入れて… |
| [dns-cdn 問18](../../exercises/dns-cdn.md#q18) | 5.3.3 | リリースの更新がすぐ反映されません。無効化をしても、ブラウザに古い内容が残る利用者がいます。リリース… |
| [dns-cdn 問19](../../exercises/dns-cdn.md#q19) | 5.3.3 | キャッシュポリシーは Minimum TTL 60 秒、Default TTL 3,600 秒、Ma… |
| [dns-cdn 問20](../../exercises/dns-cdn.md#q20) | 5.3.3 | 言語別のページで、日本語の利用者に英語のページが返ることがあります。オリジンは Accept-Lan… |
| [dns-cdn 問21](../../exercises/dns-cdn.md#q21) | 5.3.3 | CloudFront のエラーの原因の組み合わせとして正しいものを選んでください。（2つ選択） |
| [dns-cdn 問22](../../exercises/dns-cdn.md#q22) | 5.3.3 | オリジンの一時的な 500 が、復旧後もしばらく利用者へ返り続けます。どの設定を見直しますか。 |
| [dns-cdn 問23](../../exercises/dns-cdn.md#q23) | 5.3.3 | 無効化の費用の説明として正しいものはどれですか。 |
| [dns-cdn 問24](../../exercises/dns-cdn.md#q24) | 5.3.3 | ヒット率の確認の説明として正しいものはどれですか。 |

<!-- questions:end -->

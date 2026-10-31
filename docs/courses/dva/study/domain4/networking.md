# 分野4: ネットワーク

CloudFront のキャッシュ設定と、ALB のヘルスチェック、エラーコードの切り分けが問われます。通信の保護やアクセス制御は[分野2](../domain2/networking.md)で扱います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [4.1.1](../../domain4.md#skill-4-1-1) | エラーコードからの切り分け |
| [4.2.5](../../domain4.md#skill-4-2-5) | ALB のヘルスチェック |
| [4.3.4](../../domain4.md#skill-4-3-4) | CloudFront のキャッシュ |

## 学習の順番 {#study-order}

1. [ALB のヘルスチェック](../../../../services/networking.md#alb-health-checks): 既定値、状態、理由コードを覚えます。
2. [ヘルスチェックの計算](../../../../services/networking.md#health-check-calc): 判定までの時間と `Matcher` の指定を確認します。
3. [ALB のエラーコード](../../../../services/networking.md#alb-errors)と[エラーの原因一覧](../../../../services/networking.md#alb-error-detail): 502、503、504 の違いを言えるようにします。
4. [アイドルタイムアウトとキープアライブ](../../../../services/networking.md#alb-idle-timeout): 断続的な 502 と 504 の直し方を学びます。
5. [接続できないときの切り分け](../../../../services/networking.md#vpc-troubleshooting): 症状と確認先を結びつけます。
6. [キャッシュキーとポリシー](../../../../services/networking.md#cache-keys)と[ヘッダーによるキャッシュ](../../../../services/networking.md#header-caching): 2 種類のポリシーの役割と、ヒット率との関係を理解します。
7. [TTL の計算](../../../../services/networking.md#ttl-worked)と[キャッシュの無効化](../../../../services/networking.md#invalidation): キャッシュ時間の決まり方と消し方を押さえます。
8. [エラー応答のキャッシュ](../../../../services/networking.md#error-caching)と [CloudFront のエラー](../../../../services/networking.md#cloudfront-errors): 復旧後もエラーが返る理由と、原因ごとのコードを確認します。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| ヘルスチェックの間隔とタイムアウト | 30 秒、5 秒 | Lambda ターゲットでは 35 秒、30 秒です |
| 正常と異常のしきい値 | `HealthyThresholdCount` 5、`UnhealthyThresholdCount` 2 | 異常まで約 60 秒、正常に戻るまで約 150 秒です |
| `Matcher` | 既定 200、HTTP は 200〜499 で指定 | `200,202` や `200-299` と書けます |
| ALB のアイドルタイムアウト | 既定 60 秒、1〜4000 秒 | 処理時間より長くします |
| ALB からターゲットへの接続タイムアウト | 10 秒 | 超えると 504 です |
| エラー応答のキャッシュ | 既定 10 秒 | Error Caching Minimum TTL で変更します |
| ポリシーなしの TTL | Min 0、Default 86,400、Max 31,536,000 秒 | Default はオリジンがヘッダーを返さないときの値です |
| `CachingOptimized` | Min 1、Default 86,400、Max 31,536,000 秒 | `CachingDisabled` はすべて 0 です |
| 無効化パス | 月 1,000 個まで無料 | `/*` は 1 パスと数えます |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| ヘルスチェックが `Target.ResponseCodeMismatch` になる | パス、認証の要否、`Matcher` を確認します。`/` が 401 なら、パスを変えるか `Matcher` を `200,401` にします |
| ヘルスチェックが `Target.Timeout` になる | セキュリティグループとアプリの応答速度を確認します |
| 故障を約 20 秒で検出したい | 間隔を 10 秒にし、`UnhealthyThresholdCount` を 2 にします |
| ALB の 5XX の出どころを切り分けたい | `HTTPCode_ELB_5XX_Count` は ALB が返したもの、`HTTPCode_Target_5XX_Count` はターゲットが返したものです |
| ALB が 503 を返す | 登録済みターゲットがないか、すべて `unused` です |
| ALB の 502 が断続的に出る | ターゲットのキープアライブを ALB のアイドルタイムアウトより長くします |
| 処理に 90 秒かかる API が 504 になる | ALB のアイドルタイムアウトを 120 秒に伸ばします |
| 言語や端末ごとに別のキャッシュにしたい | キャッシュポリシーに `Accept-Language` や `CloudFront-Is-Mobile-Viewer` を含めます。`User-Agent` は避けます |
| キャッシュを分けずに値をオリジンへ送りたい | オリジンリクエストポリシーを使います |
| `no-cache` なのにキャッシュされる | Minimum TTL が 0 より大きいと上書きします。0 にします |

## 引っかかりやすい点 {#traps}

- **全ターゲットが異常なのに 503 にならない:** ALB はフェイルオープンで全ターゲットへ転送します。
- **ヒット率が下がる:** キャッシュキーの値を増やしすぎています。応答が実際に変わる値だけを含め、値は CloudFront Functions で正規化できます。
- **別のユーザーの応答が返る:** `Authorization` をキャッシュキーに含めずに転送すると、最初のユーザーの応答が共有されます。
- **オリジンの復旧後も 500 が返る:** 4xx と 5xx は既定で 10 秒キャッシュされます。
- **CloudFront が 502 を返す:** オリジンの証明書のドメインがオリジンドメイン名と一致していないと、TLS で失敗します。
- **圧縮を有効にしても変わらない:** すでにキャッシュされたオブジェクトは圧縮されません。無効化するか、期限切れを待ちます。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [networking 問1](../../exercises/networking.md#q1) | 4.1.1 | ある開発者は、ALB の後ろの EC2 のサブネットに自作のネットワーク ACL を関連付けました。… |
| [networking 問2](../../exercises/networking.md#q2) | 4.1.1 | NACL に 100 ALLOW 0.0.0.0/0 TCP 443 があります。攻撃元の 203.… |
| [networking 問7](../../exercises/networking.md#q7) | 4.2.5 | Route 53 のヘルスチェックについて正しい説明はどれですか。（2つ選択） |
| [networking 問8](../../exercises/networking.md#q8) | 4.1.1 | 国別に別の ALB へ振り分けるため、Route 53 で日本とドイツの位置情報レコードだけを作りま… |
| [networking 問9](../../exercises/networking.md#q9) | 4.2.5 | ALB のターゲットグループは既定の設定です。ターゲットが完全に停止してから、そのターゲットへのリク… |
| [networking 問10](../../exercises/networking.md#q10) | 4.1.1 | 処理に最長 90 秒かかる API を ALB の後ろで運用しています。登録解除の待ちは 30 秒、… |
| [networking 問11](../../exercises/networking.md#q11) | 4.1.1 | ALB のログに断続的な 502 があり、HTTPCode_ELB_502_Count が増えていま… |
| [networking 問12](../../exercises/networking.md#q12) | 4.2.5 | ターゲットがすべて unhealthy のターゲットグループへ、ALB がリクエストを転送しています… |
| [networking 問13](../../exercises/networking.md#q13) | 4.3.4 | キャッシュポリシーの TTL は Minimum 60、Default 3600、Maximum 8… |
| [networking 問14](../../exercises/networking.md#q14) | 4.3.4 | CloudFront の Lambda@Edge の設定について、正しい説明はどれですか。 |

<!-- questions:end -->

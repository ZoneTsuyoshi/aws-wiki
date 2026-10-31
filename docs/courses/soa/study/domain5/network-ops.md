# 分野5: ネットワークの保護、ログ、監視

保護サービスの選択、ログの読み方、監視サービスの選択を問います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [5.1.3](../../domain5.md#skill-5-1-3) | ネットワーク保護サービスの監査 |
| [5.3.2](../../domain5.md#skill-5-3-2) | ネットワークログの収集と解釈 |
| [5.3.5](../../domain5.md#skill-5-3-5) | CloudWatch のネットワーク監視サービス |

## 学習の順番 {#study-order}

1. [AWS WAF](../../../../services/certificates.md#waf)と[ログ](../../../../services/certificates.md#waf-logging): HTTP の保護とログの名前を確認します。
2. [DNS Firewall](../../../../services/network-connectivity.md#dns-firewall)、[Network Firewall](../../../../services/network-connectivity.md#network-firewall)と[ルーティング](../../../../services/network-connectivity.md#nfw-routing): VPC の保護を区別します。
3. [VPC フローログ](../../../../services/networking.md#flow-logs)と[フローログの分析](../../../../services/network-connectivity.md#flow-log-analysis): フローログの項目を読みます。
4. [ログ](../../../../services/networking.md#cloudfront-logs)と[S3 上のログを問い合わせる](../../../../services/streaming.md#athena-logs): ログの分析を確認します。
5. [接続の調査](../../../../services/network-connectivity.md#network-analysis): 解析と監視の違いを確認します。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| フローログの配信 | CloudWatch Logs で約 5 分、S3 で約 10 分 | 目安 |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| SQL インジェクションとレート制限 | WAF |
| マルウェアのドメインを止める | DNS Firewall |
| IP 宛の通信も止める | Network Firewall |
| `HTTPCode_Target_5XX_Count` が増える | アプリを調べる |
| オンプレミスの宛先の遅延を測る | Network Synthetic Monitor |
| VPC の中の TCP の性能を見る | Network Flow Monitor |
| 特定の国の利用者だけ遅い | Internet Monitor |

## 引っかかりやすい点 {#traps}

- WAF のログの送信先は `aws-waf-logs-` で始めます。
- フローログに HTTP の中身はなく、Amazon DNS サーバーへの問い合わせも記録されません。
- ALB のアクセスログは既定で無効です。
- Network Synthetic Monitor は自動でフェイルオーバーしません。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [network-ops 問1](../../exercises/network-ops.md#q1) | 5.1.3 | ALB へのリクエストについて、SQL インジェクションと IP ごとのレート制限を設定します。どれ… |
| [network-ops 問2](../../exercises/network-ops.md#q2) | 5.1.3 | WAF のログの送信先に、作成した S3 バケットを選べません。バケット名は waf-logs-pr… |
| [network-ops 問3](../../exercises/network-ops.md#q3) | 5.1.3 | VPC のインスタンスからマルウェアのドメインへの問い合わせを止めるルールを入れた後、許可したドメイ… |
| [network-ops 問4](../../exercises/network-ops.md#q4) | 5.1.3 | Network Firewall を配置しましたが、通信が検査されません。ファイアウォールのルールは… |
| [network-ops 問5](../../exercises/network-ops.md#q5) | 5.1.3 | 単一のアカウントの監査で、各サービスで何を見るかの組み合わせとして正しいものを選んでください。（2つ… |
| [network-ops 問6](../../exercises/network-ops.md#q6) | 5.1.3 | 次の要件に合うものはどれですか。IP 宛の通信と DNS 以外のプロトコルも VPC の境界で止めた… |
| [network-ops 問7](../../exercises/network-ops.md#q7) | 5.3.2 | VPC フローログの次のレコードを読みます。2 111122223333 eni-EXAMPLE 1… |
| [network-ops 問8](../../exercises/network-ops.md#q8) | 5.3.2 | VPC フローログの説明として正しいものを選んでください。（2つ選択） |
| [network-ops 問9](../../exercises/network-ops.md#q9) | 5.3.2 | ALB の 5xx が増えました。HTTPCode_ELB_5XX_Count は 0 で、HTTP… |
| [network-ops 問10](../../exercises/network-ops.md#q10) | 5.3.2 | ALB のリクエストごとの応答コードと処理時間を分析したいです。どの設定で、どう分析しますか。 |
| [network-ops 問11](../../exercises/network-ops.md#q11) | 5.3.2 | S3 に保存した CloudFront のログを Athena で検索します。スキャンの費用を減らす… |
| [network-ops 問12](../../exercises/network-ops.md#q12) | 5.3.2 | ECS と EKS のコンテナのログの収集の説明で正しいものはどれですか。 |
| [network-ops 問13](../../exercises/network-ops.md#q13) | 5.3.5 | Direct Connect の先の工場との通信が遅くなることがあります。原因が AWS 側かを判断… |
| [network-ops 問14](../../exercises/network-ops.md#q14) | 5.3.5 | VPC の中のマイクロサービスの間の通信と、S3 への通信で、TCP の性能の劣化がどこで起きている… |
| [network-ops 問15](../../exercises/network-ops.md#q15) | 5.3.5 | 特定の国の利用者だけアプリが遅いという報告が増えました。どの場所と ISP が影響を受けているかを、… |
| [network-ops 問16](../../exercises/network-ops.md#q16) | 5.3.5 | Network Synthetic Monitor の説明として正しいものを選んでください。（2つ選… |

<!-- questions:end -->

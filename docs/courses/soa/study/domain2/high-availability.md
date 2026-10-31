# 分野2: ヘルスチェックと高可用性

異常と判定される理由と、AZ の障害への備えを問います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [2.2.1](../../domain2.md#skill-2-2-1) | ELB と Route 53 のヘルスチェック |
| [2.2.2](../../domain2.md#skill-2-2-2) | 耐障害性のある構成 |

## 学習の順番 {#study-order}

1. [ヘルスチェック](../../../../services/networking.md#alb-health-checks)と[ALB のエラーの原因一覧](../../../../services/networking.md#alb-error-detail): 既定値と理由コードを確認します。
2. [Route 53 ヘルスチェック](../../../../services/networking.md#route53-health-checks)と[Route 53 のフェイルオーバー設計](../../../../services/resilience.md#route53-failover): 確認元の違いとアラーム型を覚えます。
3. [ヘルスチェック](../../../../services/ec2-beanstalk.md#asg-health-checks): Auto Scaling との連携を確認します。
4. [サービスごとの Multi-AZ と Multi-Region](../../../../services/resilience.md#patterns-by-service)と[高可用性のための Auto Scaling](../../../../services/resilience.md#auto-scaling-ha): サービスごとの Multi-AZ を確認します。
5. [ゾーンシフトとオートシフト](../../../../services/resilience.md#arc-zonal)と[フェイルオーバーはデータプレーンで](../../../../services/resilience.md#failover-data-plane): 切り替えの手段と考え方を確認します。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| ALB の既定 | 30 秒、異常 2 回、正常 5 回 | 全異常ならフェイルオープン |
| Route 53 の既定 | 30 秒、連続 3 回 | 18% 超が正常なら正常 |
| 文字列の一致 | 先頭 5,120 バイト | Route 53 のヘルスチェック |
| RDS のフェイルオーバー | DB インスタンス 60〜120 秒、クラスター 35 秒未満 | どちらも通常の値 |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| `Target.ResponseCodeMismatch` | パスと `Matcher` |
| `Target.Timeout` | セキュリティグループとアプリの応答 |
| 内部のリソースを確認する | CloudWatch アラーム型 |
| 500 でも置き換えない | ELB ヘルスチェックを有効にする |
| 1 AZ を失っても 6 台 | 3 AZ で AZ あたり 3 台 |
| AZ へのトラフィックを外す | ARC のゾーンシフト |

## 引っかかりやすい点 {#traps}

- NLB のクロスゾーンは既定で無効です。
- NAT ゲートウェイは AZ ごとに作ります。
- 障害のときは作成や更新の API が使えないことがあります。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [high-availability 問1](../../exercises/high-availability.md#q1) | 2.2.1 | ALB のターゲットの状態が異常で、理由コードは Target.ResponseCodeMismat… |
| [high-availability 問2](../../exercises/high-availability.md#q2) | 2.2.1 | ALB のターゲットの理由コードが Target.Timeout です。確認すべきものはどれですか。 |
| [high-availability 問3](../../exercises/high-availability.md#q3) | 2.2.1 | Route 53 のフェイルオーバーで、プライベートサブネットの内部 ALB の正常性を確認したいで… |
| [high-availability 問4](../../exercises/high-availability.md#q4) | 2.2.1 | Route 53 の CloudWatch アラーム型のヘルスチェックに使えるアラームとして、注意す… |
| [high-availability 問5](../../exercises/high-availability.md#q5) | 2.2.1 | Route 53 のエンドポイント型のヘルスチェックが、エンドポイントは正常なのに異常になります。公… |
| [high-availability 問6](../../exercises/high-availability.md#q6) | 2.2.1 | アプリが 500 を返し続けていますが、Auto Scaling がインスタンスを置き換えません。E… |
| [high-availability 問7](../../exercises/high-availability.md#q7) | 2.2.1 | ALB の全ターゲットが異常になりました。ALB の動作の説明として正しいものはどれですか。 |
| [high-availability 問8](../../exercises/high-availability.md#q8) | 2.2.2 | 3 つの AZ で常に 6 台が必要です。1 つの AZ を失っても 6 台を維持したいです。最小の… |
| [high-availability 問9](../../exercises/high-availability.md#q9) | 2.2.2 | 3 AZ のプライベートサブネットが 1 つの NAT ゲートウェイを共有しています。その AZ の… |
| [high-availability 問10](../../exercises/high-availability.md#q10) | 2.2.2 | NLB の裏のターゲットの台数が AZ ごとに違い、一部のターゲットに負荷が偏ります。何を確認します… |
| [high-availability 問11](../../exercises/high-availability.md#q11) | 2.2.2 | ALB の 1 つの AZ で障害があり、その AZ のターゲットはヘルスチェックに成功するものの、… |
| [high-availability 問12](../../exercises/high-availability.md#q12) | 2.2.2 | 障害のときに確実に動く切り替えの手順を作ります。どの考え方が適切ですか。（2つ選択） |
| [high-availability 問13](../../exercises/high-availability.md#q13) | 2.2.2 | JVM のアプリケーションが、RDS Multi-AZ のフェイルオーバーの後も古い接続先へ繋ごうと… |
| [high-availability 問14](../../exercises/high-availability.md#q14) | 2.2.2 | Multi-AZ の構成についての説明で正しいものを選んでください。（2つ選択） |

<!-- questions:end -->

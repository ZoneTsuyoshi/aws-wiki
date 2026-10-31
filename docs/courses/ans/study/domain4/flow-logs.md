# 分野4: フローログと Traffic Mirroring

フローログと Traffic Mirroring の作成、ログの配信、相関分析を問います。タスク 4.2 の中心です。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [フローログ](../../domain4.md#t4-2-flow-logs) | フローログの作成と分析（基本と拡張のフィールド） |
| [Traffic Mirroring](../../domain4.md#t4-2-mirroring) | Traffic Mirroring の作成と分析 |
| [ログの作成](../../domain4.md#t4-2-log-creation) | サービスごとのログの作成 |
| [ログの配信](../../domain4.md#t4-2-delivery) | ログの配信（Kinesis、Route 53、CloudWatch）、ログ配信の実装 |
| [相関分析](../../domain4.md#t4-2-correlation) | 複数のログの相関分析 |

## 学習の順番 {#study-order}

1. [フローログの分析](../../../../services/network-connectivity.md#flow-log-analysis): フィールドと値を確認します。
2. [VPC フローログの調査](../../../../services/threat-detection.md#investigate-flow-logs): 調査の使い方を押さえます。
3. [Traffic Mirroring](../../../../services/network-connectivity.md#traffic-mirroring): 要素と注意を覚えます。
4. [サブスクリプションフィルター](../../../../services/observability.md#subscription-filters): ログの集約を確認します。
5. [どのログを見るか](../../../../services/threat-detection.md#log-sources): どのログを見るかを整理します。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| `pkt-srcaddr` | バージョン 3 | NAT の裏の元の IP |
| `flow-direction`、`traffic-path` | バージョン 5 | 向きと経路 |
| `reject-reason` | バージョン 8 | `BPA`、`EC` |
| カプセル化 | VXLAN、UDP 4789 | ミラーのターゲット |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 長期保存と Athena | S3 |
| 外部の SIEM | Firehose |
| 数秒以内の処理 | Kinesis Data Streams（CloudFront のリアルタイムログ） |
| 通信の前の変更 | フローログと CloudTrail |

## 引っかかりやすい点 {#traps}

- 1 つのターゲットで複数の送信元の通信を受けられます。
- ターゲットとして使う ENI は送信元にできません。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [flow-logs 問10](../../exercises/flow-logs.md#q10) | フローログ | NAT ゲートウェイの ENI のフローログで不審な通信を調べます。srcaddr は NAT の … |
| [flow-logs 問11](../../exercises/flow-logs.md#q11) | フローログ | フローログの reject-reason が BPA です。ルートも SG も許可しているのに、イン… |
| [flow-logs 問12](../../exercises/flow-logs.md#q12) | フローログ | フローログのカスタム形式について、値の読み方として正しいものを選んでください。（2つ選択） |
| [flow-logs 問13](../../exercises/flow-logs.md#q13) | Traffic Mirroring | Traffic Mirroring のターゲットを設計します。IDS のアプライアンスを複数の AZ… |
| [flow-logs 問14](../../exercises/flow-logs.md#q14) | Traffic Mirroring | 監査用の Traffic Mirroring のセッションを設計しています。複数のチームの送信元を、… |
| [flow-logs 問15](../../exercises/flow-logs.md#q15) | Traffic Mirroring | 通信量の多い ENI をミラーしたところ、IDS が追いつかず費用も増えました。検査に必要なのは特定… |
| [flow-logs 問16](../../exercises/flow-logs.md#q16) | ログの作成 | ALB のアクセスログの有効化が権限のエラーで失敗しました。また WAF と Route 53 のロ… |
| [flow-logs 問17](../../exercises/flow-logs.md#q17) | ログの作成 | Network Firewall の判定の監査のため、ログを作成します。ルールの一致、通信の記録、T… |
| [flow-logs 問18](../../exercises/flow-logs.md#q18) | ログの作成 | フローログを作成する範囲を決めます。サブネットの一部の ENI だけで足りますが、将来の ENI の… |
| [flow-logs 問19](../../exercises/flow-logs.md#q19) | ログの配信 | 要件は 2 つです。(1) フローログを長期に低コストで保存して Athena で分析する。(2) … |
| [flow-logs 問20](../../exercises/flow-logs.md#q20) | ログの配信 | セキュリティチームがログの配信先の表を作っています。保持は別に設計します。ログの種類と送信先の組み合… |
| [flow-logs 問21](../../exercises/flow-logs.md#q21) | ログの配信 | 各アカウントの CloudWatch Logs のログを、数分以内にログ用アカウントへ集めます。S3… |
| [flow-logs 問22](../../exercises/flow-logs.md#q22) | 相関分析 | 不審な通信の直前に何があったかを調べます。SG の変更が疑われます。ログの組み合わせとして最も適切な… |
| [flow-logs 問23](../../exercises/flow-logs.md#q23) | 相関分析 | EC2 からどのドメインへ接続したかを調べます。フローログには IP しかありません。最も適切な相関… |
| [flow-logs 問24](../../exercises/flow-logs.md#q24) | 相関分析 | 複数のアカウントのログをまとめて調査します。また、GuardDuty の検出を起点に影響範囲を調べま… |

<!-- questions:end -->

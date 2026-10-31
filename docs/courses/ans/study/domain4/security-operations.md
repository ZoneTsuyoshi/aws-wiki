# 分野4: 監査と通知の自動化

テスト、通知の自動化、監視サービスの区別、監査の戦略を問います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [テスト](../../domain4.md#t4-1-testing) | 要件を満たすかのテスト（フェイルオーバー、回復性） |
| [通知の自動化](../../domain4.md#t4-1-automation) | インシデントの報告と通知の自動化 |
| [サービス](../../domain4.md#t4-2-services) | 監視とログのサービス（CloudWatch、CloudTrail、Traffic Mirroring、フローログ、Network Manager） |
| [設定の監査](../../domain4.md#t4-2-audit) | 設定の監査（SG、Firewall Manager、Trusted Advisor）、複数のサービス、アカウントの監査戦略の実装 |
| [通知の仕組み](../../domain4.md#t4-2-alerts) | 通知の仕組み（CloudWatch アラーム）、CloudWatch の自動アラームの実装、CloudWatch のカスタムメトリクスの実装 |

## 学習の順番 {#study-order}

1. [Network Access Analyzer](../../../../services/network-connectivity.md#network-access-analyzer): 環境全体の確認を押さえます。
2. [AWS Fault Injection Service(FIS)](../../../../services/resilience.md#fis): 障害の注入を確認します。
3. [EventBridge による自動化](../../../../services/threat-detection.md#ir-eventbridge): 自動の流れを理解します。
4. [Firewall Manager](../../../../services/threat-detection.md#firewall-manager): 前提を覚えます。
5. [AWS Config](../../../../services/governance.md#config): ルールと履歴を確認します。
6. [複合アラーム](../../../../services/observability.md#composite-alarms): 誤報を減らす方法を確認します。
7. [メトリクスフィルター](../../../../services/observability.md#metric-filters): カスタムメトリクスを押さえます。

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 誰が SG を変えたか | CloudTrail |
| どの IP が拒否されたか | フローログ |
| 設定の変更履歴 | Config |
| 両方のトンネルが落ちたときだけ | 複合アラーム |
| 全アカウントの基準を強制 | Firewall Manager |

## 引っかかりやすい点 {#traps}

- GuardDuty の DNS ベースの検出は AWS のリゾルバーを使う場合に働きます。
- 複数アカウントの監査はアグリゲーターと Security Hub で集約します。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [security-operations 問1](../../exercises/security-operations.md#q1) | テスト | 災害復旧の要件で、DX の切り替えと、サブネットの通信の断をテストします。本番のルーターの設定は変え… |
| [security-operations 問2](../../exercises/security-operations.md#q2) | テスト | 監査のため、IGW から届くリソースの一覧を四半期ごとに作り、結果を証跡に残します。パケットは送りま… |
| [security-operations 問3](../../exercises/security-operations.md#q3) | テスト | AZ の障害を想定して ALB のトラフィックを切り離すテストを行い、ネットワークの設定の準拠は継続… |
| [security-operations 問4](../../exercises/security-operations.md#q4) | 通知の自動化 | GuardDuty が EC2 の C2 への通信を検出したら、数分以内にインスタンスを隔離して、セ… |
| [security-operations 問5](../../exercises/security-operations.md#q5) | 通知の自動化 | 開放された SG を継続的に検出して修正します。準拠の履歴も残し、アカウントごとの修復のコードを最小… |
| [security-operations 問6](../../exercises/security-operations.md#q6) | 通知の自動化 | GuardDuty の DNS ベースの検出が出ていません。この VPC は独自の DNS サーバー… |
| [security-operations 問7](../../exercises/security-operations.md#q7) | サービス | 監査で 2 つの質問を受けました。質問 1: SG を誰がいつ変更したか。質問 2: どの IP か… |
| [security-operations 問8](../../exercises/security-operations.md#q8) | サービス | ルートテーブルの設定を時系列で確認し、3 か月前の状態と比べます。API の呼び出しの一覧ではなく、… |
| [security-operations 問9](../../exercises/security-operations.md#q9) | サービス | ネットワークの監査で、ツールの限界を説明します。ツールと「分からないこと」の組み合わせで正しいものを… |
| [security-operations 問10](../../exercises/security-operations.md#q10) | 設定の監査 | 組織の全アカウントで SG を監査し、Network Firewall のポリシーも配ります。Fir… |
| [security-operations 問11](../../exercises/security-operations.md#q11) | 設定の監査 | 200 のアカウントの準拠を 1 か所で確認し、標準に沿ったコントロールの結果も集約します。非準拠の… |
| [security-operations 問12](../../exercises/security-operations.md#q12) | 設定の監査 | 複数のアカウントの監査で、担当者ごとに使うツールを割り当てています。仕組みと監査の対象の組み合わせで… |
| [security-operations 問13](../../exercises/security-operations.md#q13) | 通知の仕組み | VPN の片方のトンネルの保守の通知が多く、運用者が疲れています。両方のトンネルが同時に落ちたときだ… |
| [security-operations 問14](../../exercises/security-operations.md#q14) | 通知の仕組み | フローログを CloudWatch Logs へ送っています。拒否が毎分 100 件を超えたら通知し… |
| [security-operations 問15](../../exercises/security-operations.md#q15) | 通知の仕組み | 自前のプローブが測った遅延と、EC2 の OS の ethtool の統計をカスタムメトリクスにしま… |

<!-- questions:end -->

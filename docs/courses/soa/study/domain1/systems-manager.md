# 分野1: 修復と Automation

検知から修復までの手段の選択と、ランブックの運用を問います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [1.2.1](../../domain1.md#skill-1-2-1) | 性能の分析と修復の自動化 |
| [1.2.3](../../domain1.md#skill-1-2-3) | Automation ランブックの作成と実行 |

## 学習の順番 {#study-order}

1. [ステータスチェック](../../../../services/operations.md#status-checks): システムとインスタンスのチェックの違いを確認します。
2. [EventBridge による修復パターン](../../../../services/operations.md#eventbridge-remediation)と[修復](../../../../services/governance.md#config-remediation): きっかけごとの修復の手段を表で覚えます。
3. [Automation](../../../../services/operations.md#automation): アクションと `AutomationAssumeRole` を確認します。
4. [複数アカウント、複数リージョンの実行](../../../../services/operations.md#automation-multi-account)と[レート制御](../../../../services/operations.md#automation-rate-control): 複数アカウントの条件とレート制御を覚えます。
5. [AWS DevOps Agent](../../../../services/operations.md#devops-agent)と[2026 年 10 月時点の提供状況](../../../../services/operations.md#status): AI の支援と、提供状況の変わったサービスを確認します。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| `aws:approve` | 既定 7 日、最大 30 日 | 複数アカウントの実行では使えない |
| ロールなしの実行 | 最大 12 時間 | 実行者の権限で動く |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| ハードウェアの障害で別のホストへ移す | `StatusCheckFailed_System` と EC2 の復旧アクション |
| Config の非準拠を自動で直す | ルールの修復に Automation |
| Health の予定で動かす | `aws.health` を EventBridge で受ける |
| 本番の変更の前に承認を入れる | `aws:approve` |
| 多数のリソースへ順に実行する | 同時実行数とエラーのしきい値 |

## 引っかかりやすい点 {#traps}

- 修復が別のイベントを起こすと、ループになります。
- 複数アカウントの実行には、ランブックの共有と実行用のロールが必要です。
- DevOps Guru は 2026年10月29日で新規受付を終了しました。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [systems-manager 問1](../../exercises/systems-manager.md#q1) | 1.2.1 | ハードウェアの障害で EC2 のシステムステータスチェックが失敗したら、自動で別のホストへ移したいと… |
| [systems-manager 問2](../../exercises/systems-manager.md#q2) | 1.2.1 | S3 バケットの公開設定が AWS Config のルールで非準拠と判定されたら、自動で公開を止めた… |
| [systems-manager 問3](../../exercises/systems-manager.md#q3) | 1.2.1 | AWS Health に EC2 のメンテナンスの予定が出たら、事前に自動でインスタンスを別のホスト… |
| [systems-manager 問4](../../exercises/systems-manager.md#q4) | 1.2.1 | セキュリティグループを修復する Automation を作りました。修復自体がセキュリティグループの… |
| [systems-manager 問5](../../exercises/systems-manager.md#q5) | 1.2.1 | 2026 年 10 月時点で新しくインシデントの調査の自動化を始めるアカウントで、AWS の運用系サ… |
| [systems-manager 問6](../../exercises/systems-manager.md#q6) | 1.2.3 | EC2 を停止し、AMI を作成し、再開するという一連の処理を定期的に行います。AWS API の呼… |
| [systems-manager 問7](../../exercises/systems-manager.md#q7) | 1.2.3 | カスタムランブックの途中で、本番の変更の前に責任者の承認を入れたいと考えています。どのアクションを使… |
| [systems-manager 問8](../../exercises/systems-manager.md#q8) | 1.2.3 | ランブックのアクションと用途の組み合わせとして正しいものを選んでください。（2つ選択） |
| [systems-manager 問9](../../exercises/systems-manager.md#q9) | 1.2.3 | 別のアカウントで、カスタムランブックを使った複数アカウントの Automation が失敗します。管… |
| [systems-manager 問10](../../exercises/systems-manager.md#q10) | 1.2.3 | 本番の 500 台に Automation を実行します。一度に全台へ広がらないようにし、失敗が増え… |
| [systems-manager 問11](../../exercises/systems-manager.md#q11) | 1.2.3 | AutomationAssumeRole を指定せずにランブックを実行しました。正しい説明はどれです… |

<!-- questions:end -->

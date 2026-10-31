# 分野5: 構成管理と状態の修復

対象ごとの修復の手段を問います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [構成管理](../../domain5.md#t5-2-config) | 構成管理のサービス |
| [状態の修復](../../domain5.md#t5-2-remediate) | 望ましくない状態の修復 |

## 学習の順番 {#study-order}

1. [設定レコーダー](../../../../services/governance.md#config-recorder): 記録の前提を確認します。
2. [アグリゲーター](../../../../services/governance.md#config-aggregators): 全社の確認を押さえます。
3. [適合パック](../../../../services/governance.md#config-conformance-packs): ルールの配布を確認します。
4. [修復](../../../../services/governance.md#config-remediation): 自動の修復を確認します。
5. [OpsCenter](../../../../services/operations.md#opscenter): 人の判断が要るものの扱いを確認します。

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 準拠の変化だけを受ける | `Config Rules Compliance Change` |
| AWS リソースの設定を直す | Config の自動修復 |
| サーバーの中の状態を保つ | State Manager |
| 人の調査が要る | OpsItem |

## 引っかかりやすい点 {#traps}

- ドリフト検出は直さないので、テンプレートへの反映か再デプロイが必要です。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [config 問7](../../exercises/config.md#q7) | 構成管理 | Config のルールが非準拠になったら、当番へ通知します。全リソースの全変更を通知するのではなく、… |
| [config 問8](../../exercises/config.md#q8) | 構成管理 | 組織の全アカウントの Config の評価を、1 か所のアカウントから見ます。また、同じ一連のルール… |
| [config 問9](../../exercises/config.md#q9) | 構成管理 | 障害の調査で、3 日前の時点のセキュリティグループの規則と、関連する ENI の関係を確認します。対… |
| [config 問10](../../exercises/config.md#q10) | 状態の修復 | 本番のアカウントで、暗号化が無効の EBS のデフォルトの設定を検出して自動で直します。結果も人に伝… |
| [config 問11](../../exercises/config.md#q11) | 状態の修復 | 次の望ましくない状態を修復します。(1) サーバーの中で必須のセキュリティエージェントのサービスが止… |
| [config 問12](../../exercises/config.md#q12) | 状態の修復 | Auto Scaling の起動の失敗のイベントに対応します。定型の修復が決まっているものは自動で直… |

<!-- questions:end -->

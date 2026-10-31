# 分野4: Organizations、Trusted Advisor、Config

権限の上限、助言と修復、継続的な準拠を問います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [4.1.3](../../domain4.md#skill-4-1-3) | マルチアカウントの戦略 |
| [4.1.4](../../domain4.md#skill-4-1-4) | Trusted Advisor のセキュリティチェックと修復 |
| [4.1.5](../../domain4.md#skill-4-1-5) | コンプライアンスと継続的な監視 |

## 学習の順番 {#study-order}

1. [OU の設計](../../../../services/governance.md#org-ous)、[SCP](../../../../services/governance.md#scp)と[RCP](../../../../services/governance.md#rcp): 上限の考え方を確認します。
2. [権限セット](../../../../services/identity-directory.md#idc-permission-sets)と[コントロール](../../../../services/governance.md#ct-controls): サインインとコントロールを確認します。
3. [Trusted Advisor](../../../../services/cloud-foundations.md#trusted-advisor)と[AWS Health Dashboard](../../../../services/cloud-foundations.md#health): 助言と AWS 側の通知を区別します。
4. [NotAction](../../../../services/iam.md#notaction)と[主なグローバル条件キー](../../../../services/iam.md#condition-keys): リージョンの制限の書き方を確認します。
5. [Config ルール](../../../../services/governance.md#config-rules)と[修復](../../../../services/governance.md#config-remediation): ルールと修復を確認します。
6. [適合パック](../../../../services/governance.md#config-conformance-packs)と[アグリゲーター](../../../../services/governance.md#config-aggregators): 展開と閲覧を区別します。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| SCP | 対象に 10 個、10,240 文字 | 古い教材の 5 個、5,120 文字は古い値 |
| 適合パック | 1 パック 130 ルール、アカウント 50 パック | 展開の単位 |
| `MaximumAutomaticAttempts` | 既定 5 回 | 超えると止まる |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 新しい SCP の影響を確かめる | テスト用の OU に少しずつ移す |
| 作成の前に確認する | プロアクティブコントロール |
| Trusted Advisor の指摘を自動で直す | EventBridge で受けて Automation |
| IAM まで止まった | `NotAction` でグローバルサービスを除く |
| 作成を止める | SCP か Control Tower |

## 引っかかりやすい点 {#traps}

- SCP は権限を与えません。管理アカウントには効きません。
- Trusted Advisor は助言だけです。イベントは `us-east-1` に届きます。
- Config は判定するだけで、止めません。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [governance 問1](../../exercises/governance.md#q1) | 4.1.3 | SCP の説明として正しいものを選んでください。（2つ選択） |
| [governance 問2](../../exercises/governance.md#q2) | 4.1.3 | 本番の全アカウントに新しい拒否の SCP を付けたいですが、影響が読めません。どの進め方が適切ですか… |
| [governance 問3](../../exercises/governance.md#q3) | 4.1.3 | 複数のアカウントへ、1 か所のサインインでアクセスさせたいです。権限は職務ごとにまとめます。どれが適… |
| [governance 問4](../../exercises/governance.md#q4) | 4.1.3 | Control Tower のコントロールの動作と実装の組み合わせとして正しいものはどれですか。 |
| [governance 問5](../../exercises/governance.md#q5) | 4.1.3 | 組織の外のプリンシパルが、組織の S3 バケットへアクセスできないよう、リソース側の上限を一律に決め… |
| [governance 問6](../../exercises/governance.md#q6) | 4.1.4 | Trusted Advisor のセキュリティチェックの指摘について正しいものはどれですか。 |
| [governance 問7](../../exercises/governance.md#q7) | 4.1.4 | Trusted Advisor で S3 バケットの権限の指摘が出ました。公開の必要はありません。修… |
| [governance 問8](../../exercises/governance.md#q8) | 4.1.4 | Trusted Advisor でセキュリティグループの指摘が出ました。SSH が 0.0.0.0/… |
| [governance 問9](../../exercises/governance.md#q9) | 4.1.4 | 次の見分け方として正しいものはどれですか。 |
| [governance 問10](../../exercises/governance.md#q10) | 4.1.5 | ap-northeast-1 以外の操作を止める SCP を作りました。すると、IAM の操作まで止… |
| [governance 問11](../../exercises/governance.md#q11) | 4.1.5 | AWS Config で非準拠のリソースを、人の操作なしに直したいです。正しい設定はどれですか。 |
| [governance 問12](../../exercises/governance.md#q12) | 4.1.5 | Config のルールと修復をまとめて各アカウントへ展開します。また、結果を中央で見ます。組み合わせ… |
| [governance 問13](../../exercises/governance.md#q13) | 4.1.5 | Config の自動修復が途中で止まりました。修復の失敗が続いています。確認すべきものを選んでくださ… |
| [governance 問14](../../exercises/governance.md#q14) | 4.1.5 | 「暗号化なしの EBS ボリュームの作成を禁止する」という要件を、作成の時点で止めたいです。正しい判… |

<!-- questions:end -->

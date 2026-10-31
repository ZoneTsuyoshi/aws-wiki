# 分野6: 準拠の評価

非準拠を見つけて直すことと、監査の証拠をそろえること、ベストプラクティスに照らして評価することを問います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [6.3.1](../../domain6.md#skill-6-3-1) | 非準拠の検出、修復、通知 |
| [6.3.2](../../domain6.md#skill-6-3-2) | 監査の証拠の収集と整理 |
| [6.3.3](../../domain6.md#skill-6-3-3) | ベストプラクティスに対する評価 |

## 学習の順番 {#study-order}

1. [Config](../../../../services/governance.md#config)と [Config ルール](../../../../services/governance.md#config-rules): 評価するだけで止めないことを押さえます。
2. [修復](../../../../services/governance.md#config-remediation): 実行ロールと Automation を確認します。
3. [アグリゲーター](../../../../services/governance.md#config-aggregators)と[適合パック](../../../../services/governance.md#config-conformance-packs): 集約と展開の違いを理解します。
4. [Artifact](../../../../services/threat-detection.md#artifact)と [Audit Manager](../../../../services/threat-detection.md#audit-manager): 誰の資料かと、新規受付の状況を覚えます。
5. [責任共有モデル](../../../../services/cloud-foundations.md#shared-responsibility): 証拠を誰が用意するかを整理します。
6. [Well-Architected Tool](../../../../services/cloud-foundations.md#wa-tool)、[Trusted Advisor](../../../../services/cloud-foundations.md#trusted-advisor)、[CSPM の標準](../../../../services/threat-detection.md#security-hub-cspm): 評価の方法の違いで使い分けます。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| Audit Manager の新規受付の終了 | 2026 年 4 月 30 日 | 代替は Config の適合パック |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 未暗号化の作成を止めたい | Config では止まらない。SCP や既定の暗号化 |
| 修復が権限不足で失敗 | Automation の実行ロール |
| 全アカウントの設定を横断で検索 | アグリゲーターと高度なクエリ |
| ルールと修復を組織へ一括で配る | 適合パック |
| AWS の SOC 2 レポートと BAA | Artifact |
| 新規の環境で自社の証拠を集める | Config の適合パックと履歴 |
| 質問形式で設計をレビュー | Well-Architected Tool とマイルストーン |
| AWS のベストプラクティスを継続的にチェック | Security Hub CSPM の FSBP |
| 環境を幅広く自動で点検 | Trusted Advisor |
| 独自の質問を足す | Well-Architected Tool のカスタムレンズ |

## 引っかかりやすい点 {#traps}

- アグリゲーターは読み取り専用で、展開も修復もできません。
- 組織ルールは API か CLI でのみ作成します。
- サービスリンクルールの修復は管理できません。
- Audit Manager は証拠を集めますが、準拠を判定しません。
- Artifact は AWS 自身の資料で、自社のワークロードの証明ではありません。
- Well-Architected Tool は指摘と記録だけで、リソースを修正しません。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [compliance 問1](../../exercises/compliance.md#q1) | 6.3.1 | 暗号化されていない EBS ボリュームの作成を止めたいと、担当者は Config ルール encry… |
| [compliance 問2](../../exercises/compliance.md#q2) | 6.3.1 | S3 のパブリックアクセスの設定が外れたバケットを、Config で検出したら自動で戻します。修復の… |
| [compliance 問3](../../exercises/compliance.md#q3) | 6.3.1 | 全アカウントと全リージョンの未暗号化の EBS を、アドホックに一覧にします。また、今後も組織の準拠… |
| [compliance 問4](../../exercises/compliance.md#q4) | 6.3.1 | 新規の環境で、PCI DSS に対応する一連の Config ルールと修復を、組織全体へ一括で配りま… |
| [compliance 問5](../../exercises/compliance.md#q5) | 6.3.2 | 監査人から、AWS 自身の SOC 2 レポートの提出を求められました。別途、組織の全アカウントで … |
| [compliance 問6](../../exercises/compliance.md#q6) | 6.3.2 | 新しい会社が 2026 年 10 月に AWS を使い始めました。監査に向けて、自社のワークロードが… |
| [compliance 問7](../../exercises/compliance.md#q7) | 6.3.2 | 既存の Audit Manager の利用者が、PCI DSS のフレームワークで評価を作成しました… |
| [compliance 問8](../../exercises/compliance.md#q8) | 6.3.2 | 責任共有モデルについて、監査の担当者に説明する資料を作ります。EC2 の OS のパッチの適用と、デ… |
| [compliance 問9](../../exercises/compliance.md#q9) | 6.3.3 | アーキテクトが主要なワークロードのセキュリティの設計を見直します。質問に答えてリスクと改善計画を残し… |
| [compliance 問10](../../exercises/compliance.md#q10) | 6.3.3 | 組織の標準として、AWS のベストプラクティスのチェックを全アカウントで継続的に行い、スコアで全体を… |
| [compliance 問11](../../exercises/compliance.md#q11) | 6.3.3 | ツールを選びます。「環境を自動で幅広く点検し、セキュリティ、費用、耐障害性の推奨を見る」「自社独自の… |

<!-- questions:end -->

# 分野4: 請求と費用管理

費用を見積もる、見張る、分析する、分ける道具を区別します。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [請求の情報](../../domain4.md#t4-2-billing-info) | 請求書と問い合わせ |
| [サービスの料金情報](../../domain4.md#t4-2-pricing-info) | 料金の確認先 |
| [Budgets と Cost Explorer](../../domain4.md#t4-2-budgets-explorer) | 通知と分析 |
| [Pricing Calculator](../../domain4.md#t4-2-pricing-calculator) | 作る前の見積もり |
| [Organizations の一括請求](../../domain4.md#t4-2-organizations) | 一括請求の利点 |
| [コスト配分タグとレポート](../../domain4.md#t4-2-tags) | 有効化と CUR |

## 学習の順番 {#study-order}

1. [Billing and Cost Management](../../../../services/cost-management.md#billing): コンソールで確認できるものを確認します。
2. [AWS Budgets](../../../../services/cost-management.md#budgets)と[Cost Explorer](../../../../services/cost-management.md#cost-explorer): 通知か分析かで区別します。
3. [Pricing Calculator](../../../../services/cost-management.md#pricing-calculator): 作る前の見積もりであることを確認します。
4. [一括請求](../../../../services/cost-management.md#consolidated-billing)と[AWS Organizations](../../../../services/governance.md#organizations): 一括請求の利点を覚えます。
5. [コスト配分タグ](../../../../services/cost-management.md#cost-allocation-tags)と[Data Exports と Cost and Usage Reports](../../../../services/cost-management.md#data-exports): 有効化と詳しいデータの場所を確認します。

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 予算の 80% で通知する | AWS Budgets |
| どのサービスの費用が増えたか見る | AWS Cost Explorer |
| 移行前に見積もる | AWS Pricing Calculator |
| 請求書を 1 つにまとめる | Organizations の一括請求 |
| タグが Cost Explorer で選べない | コスト配分タグの有効化 |
| 部門ごとに行単位で分析する | タグを有効化して CUR |

## 引っかかりやすい点 {#traps}

- タグはリソースに付けるだけでは請求データに出ません。有効化が必要です。
- 公開の Pricing Calculator はアカウント不要で無料です。
- 一括請求に追加料金はかかりません。
- 現在の CUR の推奨は、Data Exports で作る CUR 2.0 です。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [billing 問1](../../exercises/billing.md#q1) | 請求の情報 | 請求書、支払い方法、クレジットを確認する場所として最も適切なものはどれですか。 |
| [billing 問2](../../exercises/billing.md#q2) | 請求の情報 | 今月の請求の内容について AWS に問い合わせたいと考えています。契約しているサポートプランは Ba… |
| [billing 問3](../../exercises/billing.md#q3) | 請求の情報 | Billing and Cost Management で確認できるものはどれですか。（2つ選択） |
| [billing 問4](../../exercises/billing.md#q4) | サービスの料金情報 | AWS のサービスの料金についての説明として正しいものはどれですか。 |
| [billing 問5](../../exercises/billing.md#q5) | サービスの料金情報 | ある EC2 インスタンスの東京リージョンの現在の単価を確認したいと考えています。最も適切な情報源は… |
| [billing 問6](../../exercises/billing.md#q6) | サービスの料金情報 | 同じインスタンスタイプを別のリージョンで動かす場合の費用の考え方として正しいものはどれですか。 |
| [billing 問7](../../exercises/billing.md#q7) | Budgets と Cost Explorer | 月の費用が予算の 80% に達しそうなときに通知を受けたいと考えています。最も適切なものはどれですか… |
| [billing 問8](../../exercises/billing.md#q8) | Budgets と Cost Explorer | 先月からどのサービスの費用が増えたかをグラフで分析したいと考えています。最も適切なものはどれですか。 |
| [billing 問9](../../exercises/billing.md#q9) | Budgets と Cost Explorer | AWS Budgets と Cost Explorer の説明として正しいものはどれですか。（2つ選… |
| [billing 問10](../../exercises/billing.md#q10) | Pricing Calculator | AWS を使い始める前に、計画中の構成の月額の費用を見積もりたいと考えています。最も適切なものはどれ… |
| [billing 問11](../../exercises/billing.md#q11) | Pricing Calculator | AWS Pricing Calculator の公開の Web サイトの説明として正しいものはどれで… |
| [billing 問12](../../exercises/billing.md#q12) | Pricing Calculator | 「移行前に見積もる」「作った後の実績を分析する」に合う道具の組み合わせはどれですか。 |
| [billing 問13](../../exercises/billing.md#q13) | Organizations の一括請求 | AWS Organizations の一括請求の説明として正しいものはどれですか。 |
| [billing 問14](../../exercises/billing.md#q14) | Organizations の一括請求 | 一括請求の利点はどれですか。（2つ選択） |
| [billing 問15](../../exercises/billing.md#q15) | Organizations の一括請求 | 各部門が別のアカウントを使っていますが、経理は請求を 1 か所にまとめたいと考えています。最も適切な… |
| [billing 問16](../../exercises/billing.md#q16) | コスト配分タグとレポート | 部門ごとの費用を分けるためにリソースへタグを付けましたが、Cost Explorer で選べません。… |
| [billing 問17](../../exercises/billing.md#q17) | コスト配分タグとレポート | コスト配分タグの種類と例の組み合わせとして正しいものはどれですか。 |
| [billing 問18](../../exercises/billing.md#q18) | コスト配分タグとレポート | 部門ごとの費用を行単位で詳しく分析したいと考えています。最も適切なものはどれですか。 |
| [billing 問19](../../exercises/billing.md#q19) | コスト配分タグとレポート | AWS Cost and Usage Report（CUR）の説明として正しいものはどれですか。 |

<!-- questions:end -->

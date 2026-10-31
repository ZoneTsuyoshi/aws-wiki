# 分野1: クラウドの経済性

費用の見方と、なぜ費用が下がるのかを問います。用語の意味を例で区別します。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [経済性の見方と節約の要素](../../domain1.md#t1-4-economics) | TCO と節約の要素 |
| [固定費と変動費](../../domain1.md#t1-4-fixed-variable) | 固定費と変動費の違い |
| [オンプレミスにかかる費用](../../domain1.md#t1-4-onprem-costs) | 機器代以外の費用 |
| [ライセンスの持ち込みとライセンス込み](../../domain1.md#t1-4-licensing) | BYOL とライセンス込み |
| [適正サイズ](../../domain1.md#t1-4-rightsizing) | 使用率に合わせた見直し |
| [自動化の利点](../../domain1.md#t1-4-automation) | 自動化の効果とサービス |
| [規模の経済](../../domain1.md#t1-4-scale) | 単価が下がる理由 |

## 学習の順番 {#study-order}

1. [クラウドの経済性](../../../../services/cloud-foundations.md#cloud-economics): TCO、適正サイズ、BYOL の意味を確認します。
2. [クラウドの 6 つの利点](../../../../services/cloud-foundations.md#six-advantages): 固定費と変動費、規模の経済の利点を確認します。
3. [Compute Optimizer と適正サイズ](../../../../services/cost-management.md#compute-optimizer): 適正サイズの提案を出すサービスを覚えます。
4. [AWS License Manager](../../../../services/governance.md#license-manager)と[購入オプション](../../../../services/cost-management.md#purchase-options): ライセンスの管理と Dedicated Hosts を確認します。

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| オンプレミスの費用を比べる | 機器、施設、電力、冷却、保守、人員を含めた TCO |
| 手持ちのライセンスを使う | BYOL |
| ソケットやコア単位のライセンスを持ち込む | Dedicated Hosts |
| ライセンスの超過を防ぐ | AWS License Manager |
| CPU 使用率が常に低い | 小さいタイプに変える。提案は Compute Optimizer |
| 同じ環境を手作業なしで作る | CloudFormation |
| パッチの適用を自動化する | Systems Manager |

## 引っかかりやすい点 {#traps}

- 規模の経済は多数の利用者の集約の話です。自社の使用量の合算による割引は、ボリューム割引や一括請求の話です。
- Compute Optimizer を使うにはオプトインが必要です。
- 責任共有モデルの利用者の担当は、移行しても残ります。運用担当者がゼロになるわけではありません。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [cloud-economics 問1](../../exercises/cloud-economics.md#q1) | 経済性の見方と節約の要素 | AWS への移行で費用が下がる主な理由はどれですか。（2つ選択） |
| [cloud-economics 問2](../../exercises/cloud-economics.md#q2) | 経済性の見方と節約の要素 | オンプレミスと AWS の費用を比べるときの考え方として、最も適切なものはどれですか。 |
| [cloud-economics 問3](../../exercises/cloud-economics.md#q3) | 経済性の見方と節約の要素 | 移行後にさらに費用を減らす方法のうち、購入方法の選択に当たるものはどれですか。 |
| [cloud-economics 問4](../../exercises/cloud-economics.md#q4) | 固定費と変動費 | 固定費と変動費の説明のうち、クラウドの変動費の説明はどれですか。 |
| [cloud-economics 問5](../../exercises/cloud-economics.md#q5) | 固定費と変動費 | 新しい事業を試すスタートアップが、失敗したときの損失を抑えたいと考えています。この点でクラウドの変動… |
| [cloud-economics 問6](../../exercises/cloud-economics.md#q6) | 固定費と変動費 | 次のうち、固定費から変動費への移行の例はどれですか。 |
| [cloud-economics 問7](../../exercises/cloud-economics.md#q7) | オンプレミスにかかる費用 | オンプレミスの TCO の見積もりに含めるものはどれですか。（3つ選択） |
| [cloud-economics 問8](../../exercises/cloud-economics.md#q8) | オンプレミスにかかる費用 | 見積もり資料のオンプレミスの費用に、サーバーの購入費だけが載っています。この資料の問題点はどれですか… |
| [cloud-economics 問9](../../exercises/cloud-economics.md#q9) | オンプレミスにかかる費用 | 次のうち、AWS に移行するとデータセンターの費用として不要になるものはどれですか。 |
| [cloud-economics 問10](../../exercises/cloud-economics.md#q10) | ライセンスの持ち込みとライセンス込み | 手持ちの SQL Server のライセンスが有効で、これを AWS で使いたいと考えています。ライ… |
| [cloud-economics 問11](../../exercises/cloud-economics.md#q11) | ライセンスの持ち込みとライセンス込み | 物理的なソケットやコアの単位のライセンスを AWS に持ち込む必要があります。EC2 のどの選択肢が… |
| [cloud-economics 問12](../../exercises/cloud-economics.md#q12) | ライセンスの持ち込みとライセンス込み | 複数のアカウントで使うソフトウェアのライセンスの使用数を管理し、超過を防ぎたいと考えています。最も適… |
| [cloud-economics 問13](../../exercises/cloud-economics.md#q13) | ライセンスの持ち込みとライセンス込み | ライセンスを持っておらず、調達の手間も省きたい会社が、Windows Server の EC2 イン… |
| [cloud-economics 問14](../../exercises/cloud-economics.md#q14) | 適正サイズ | EC2 インスタンスの CPU 使用率が常に低いことが分かりました。適正サイズの考え方に沿った対応は… |
| [cloud-economics 問15](../../exercises/cloud-economics.md#q15) | 適正サイズ | 実際の使用状況をもとに、適切なサイズの EC2 インスタンスの提案を受けたいと考えています。最も適切… |
| [cloud-economics 問16](../../exercises/cloud-economics.md#q16) | 適正サイズ | 適正サイズの説明として正しいものはどれですか。 |
| [cloud-economics 問17](../../exercises/cloud-economics.md#q17) | 自動化の利点 | 開発、検証、本番に同じ構成を手作業なしで作り、手順の誤りを減らしたいと考えています。最も適切なサービ… |
| [cloud-economics 問18](../../exercises/cloud-economics.md#q18) | 自動化の利点 | 多数の EC2 インスタンスへのパッチの適用を自動化して、運用の人件費を減らしたいと考えています。最… |
| [cloud-economics 問19](../../exercises/cloud-economics.md#q19) | 自動化の利点 | 手作業をクラウドの自動化に置き換える利点はどれですか。（2つ選択） |
| [cloud-economics 問20](../../exercises/cloud-economics.md#q20) | 規模の経済 | AWS の「規模の経済」の利点の説明として正しいものはどれですか。 |
| [cloud-economics 問21](../../exercises/cloud-economics.md#q21) | 規模の経済 | 組織の複数のアカウントの使用量を合算してボリューム割引を受けました。これと「規模の経済」の関係として… |
| [cloud-economics 問22](../../exercises/cloud-economics.md#q22) | 規模の経済 | ある会社が、自社のデータセンターで調達するより、AWS の単価のほうが安い理由を尋ねられました。最も… |

<!-- questions:end -->

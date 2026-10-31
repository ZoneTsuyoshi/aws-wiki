# 分野4: サポートと技術リソース

要件に合うサポートプランと、情報や支援の探し先を問います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [AWS の公式サイトの情報](../../domain4.md#t4-3-official-sites) | ドキュメント、ホワイトペーパー、ブログ |
| [技術リソースの探し方](../../domain4.md#t4-3-technical-resources) | Prescriptive Guidance、Knowledge Center、re:Post |
| [サポートプラン](../../domain4.md#t4-3-support-plans) | 4 つのプラン |
| [AWS Support Center](../../domain4.md#t4-3-support-center) | ケースの管理 |
| [Trusted Advisor と Health による管理](../../domain4.md#t4-3-monitoring-role) | Trusted Advisor と Health |
| [AWS Trust & Safety](../../domain4.md#t4-3-trust-safety) | 悪用の報告 |
| [技術支援の選択肢](../../domain4.md#t4-3-technical-assistance) | Professional Services、SA、TAM |

## 学習の順番 {#study-order}

1. [AWS Support プラン](../../../../services/cloud-foundations.md#support-plans): 4 つのプランの違いを表で覚えます。
2. [サポートの情報源](../../../../services/cloud-foundations.md#support-resources): 情報源の使いどころを確認します。
3. [Trusted Advisor](../../../../services/cloud-foundations.md#trusted-advisor)と[AWS Health Dashboard](../../../../services/cloud-foundations.md#health): 自分の設定か AWS 側かで区別します。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| Business Support+ の応答目標 | 30 分未満 | 事業に重大な障害 |
| Enterprise の応答目標 | 15 分未満 | 事業に重大な障害 |
| Unified Operations | インシデント管理エンジニアから 5 分 | |
| 古いプランの終了 | 2027 年 1 月 1 日 | GovCloud では継続 |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| アカウントと請求の相談だけ | Basic |
| 24 時間の技術サポートと全チェックを最小の費用で | Business Support+ |
| 専任の TAM が必要 | Enterprise 以上 |
| AWS 側の障害の影響を見る | AWS Health Dashboard |
| Health の情報を社内システムと連携する | Health API。Business Support+ 以上 |
| AWS のリソースからの攻撃を報告する | AWS Trust & Safety |
| AWS の専門チームの有償の支援 | AWS Professional Services |
| コミュニティで質問する | AWS re:Post |

## 引っかかりやすい点 {#traps}

- 古い教材の Developer、Business、Enterprise On-Ramp は終了予定です。
- Basic に技術サポートのケースはありません。
- AWS Support は悪用の報告を扱いません。
- CloudWatch では AWS 側の障害情報は分かりません。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [support 問1](../../exercises/support.md#q1) | AWS の公式サイトの情報 | 設計の考え方や Well-Architected の解説を読みたいと考えています。最も適切な資料はど… |
| [support 問2](../../exercises/support.md#q2) | AWS の公式サイトの情報 | あるサービスの使い方の説明を、公式の情報で確認したいと考えています。最も適切なものはどれですか。 |
| [support 問3](../../exercises/support.md#q3) | AWS の公式サイトの情報 | 情報と入手先の組み合わせとして正しいものはどれですか。（2つ選択） |
| [support 問4](../../exercises/support.md#q4) | 技術リソースの探し方 | 移行や実装の具体的な手順を調べたいと考えています。最も適切なリソースはどれですか。 |
| [support 問5](../../exercises/support.md#q5) | 技術リソースの探し方 | 他の利用者や専門家に質問して、回答を得られるコミュニティの場はどれですか。 |
| [support 問6](../../exercises/support.md#q6) | 技術リソースの探し方 | よくある質問と解決方法の記事を探したいと考えています。最も適切なリソースはどれですか。 |
| [support 問7](../../exercises/support.md#q7) | サポートプラン | 費用をかけずに、アカウントと請求の相談だけができればよいと考えています。最も適切なプランはどれですか… |
| [support 問8](../../exercises/support.md#q8) | サポートプラン | 専任の担当者はいらないものの、本番の障害のときに 24 時間技術者に相談でき、Trusted Adv… |
| [support 問9](../../exercises/support.md#q9) | サポートプラン | 事業に重大な障害の応答目標として正しい組み合わせはどれですか。 |
| [support 問10](../../exercises/support.md#q10) | サポートプラン | 古い教材にある Developer、Business、Enterprise On-Ramp のプラン… |
| [support 問11](../../exercises/support.md#q11) | サポートプラン | 専任の TAM が付くプランはどれですか。（2つ選択） |
| [support 問12](../../exercises/support.md#q12) | AWS Support Center | サポートのケースを作成して管理する場所はどれですか。 |
| [support 問13](../../exercises/support.md#q13) | AWS Support Center | 請求の内容について AWS の担当者に問い合わせを起票したいと考えています。最も適切なものはどれです… |
| [support 問14](../../exercises/support.md#q14) | AWS Support Center | AWS Support Center の説明として正しいものはどれですか。 |
| [support 問15](../../exercises/support.md#q15) | Trusted Advisor と Health による管理 | AWS 側の障害が自分のどのリソースに影響するかを知りたいと考えています。最も適切なものはどれですか… |
| [support 問16](../../exercises/support.md#q16) | Trusted Advisor と Health による管理 | 使っていないリソースなどの節約の余地を、環境の点検で見つけたいと考えています。最も適切なものはどれで… |
| [support 問17](../../exercises/support.md#q17) | Trusted Advisor と Health による管理 | AWS Health の情報を社内のシステムと API で連携したいと考えています。必要なサポートプ… |
| [support 問18](../../exercises/support.md#q18) | AWS Trust & Safety | AWS の IP アドレスから自社のサーバーへ攻撃らしき通信が来ています。報告先として最も適切なもの… |
| [support 問19](../../exercises/support.md#q19) | AWS Trust & Safety | AWS Trust & Safety へ報告する対象として適切なものはどれですか。（2つ選択） |
| [support 問20](../../exercises/support.md#q20) | AWS Trust & Safety | AWS のリソースの悪用を報告する正しい方法はどれですか。 |
| [support 問21](../../exercises/support.md#q21) | 技術支援の選択肢 | 大規模な移行プロジェクトに、AWS の専門チームの有償の支援を受けたいと考えています。最も適切なもの… |
| [support 問22](../../exercises/support.md#q22) | 技術支援の選択肢 | AWS 上の設計について相談したいと考えています。最も適切な相手はどれですか。 |
| [support 問23](../../exercises/support.md#q23) | 技術支援の選択肢 | 支援と問題文の表現の組み合わせとして正しいものはどれですか。（2つ選択） |

<!-- questions:end -->

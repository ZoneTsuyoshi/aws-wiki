# 分野4: 全社展開

反復する変革の段階、短期の成果から全社への展開、AI CoE、フィードバック、PoC から本番への移行、拡大時の確認を問います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [4.4.1](../../domain4.md#skill-4-4-1) | 段階的な変革の進め方 |
| [4.4.2](../../domain4.md#skill-4-4-2) | 短期の成果から全社展開へ |
| [4.4.3](../../domain4.md#skill-4-4-3) | AI CoE と部門横断の連携 |
| [4.4.4](../../domain4.md#skill-4-4-4) | フィードバックと成功の指標 |
| [4.4.5](../../domain4.md#skill-4-4-5) | 実験から本番の水準へ |
| [4.4.6](../../domain4.md#skill-4-4-6) | 拡大時の継続性と性能 |

## 学習の順番 {#study-order}

1. [AWS Cloud Adoption Framework for AI](../../../../services/ai-fundamentals.md#caf-ai)と [Cloud Adoption Framework](../../../../services/cloud-foundations.md#caf): 4 段階の内容と、Experiment と Align の違いを確認します。
2. [パイロットから全社展開へ](../../../../services/ai-fundamentals.md#scaling): 短期の成果、CoE、フィードバック、本番の要件を確認します。
3. [本番での監視](../../../../services/ai-fundamentals.md#production-monitoring): 本番で新たに必要になることを押さえます。
4. [Cost Explorer](../../../../services/cost-management.md#cost-explorer): 拡大の途中で費用の実績を追う手段を確認します。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| 試験ガイドの例 | envision、experiment、launch、scale | 反復して進める |
| CAF の 4 段階 | Envision、Align、Launch、Scale | 2 番目の名前が違う |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 最初のパイロットを選ぶ | 価値が見えやすく、データがそろい、低リスクで、スポンサーがいる |
| 部門の成果が再利用できない | パイロットの段階から部品と標準を作る |
| CoE に依頼が集中している | CoE が標準を示し、各部門が実行する |
| 効果が時間とともに薄れた | 長期の値を追い、原因を調べて改善する |
| PoC が成功した | 本番の要件を別に確認する |
| 計画に PoC の費用しかない | 本番の要件を満たすまでの費用と期間も入れる |
| 別の国に広げる | データ、規制、業務の違いを確認する |
| 一部の部門で定着しない | 原因を調べ、研修やチャンピオンで支援する |

## 引っかかりやすい点 {#traps}

- 集中型、分散型、ハブアンドスポークの分類はこの wiki の整理で、公式の分類ではありません。
- 短期の成果を繰り返すだけでは、全社の基盤は育ちません。
- 全社平均の数字では、部門ごとの問題が隠れます。
- CAF for AI のホワイトペーパーは、現在「歴史的な参照用」と表示されています。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [scaling 問1](../../exercises/scaling.md#q1) | 4.4.1 | 試験ガイドが例に挙げる、反復する変革の段階の順序として正しいものはどれですか。 |
| [scaling 問2](../../exercises/scaling.md#q2) | 4.4.1 | AWS CAF の変革の 4 段階のうち、部門間の依存と関係者の懸念を明らかにする段階はどれですか。 |
| [scaling 問3](../../exercises/scaling.md#q3) | 4.4.1 | 変革の最初の段階（Envision）で決めるべきことはどれですか。 |
| [scaling 問4](../../exercises/scaling.md#q4) | 4.4.1 | 変革の進め方について、最も適切な考え方はどれですか。 |
| [scaling 問5](../../exercises/scaling.md#q5) | 4.4.2 | 最初のパイロットの選び方として最も適切なものはどれですか。 |
| [scaling 問6](../../exercises/scaling.md#q6) | 4.4.2 | 全社に一斉に展開する案と、小さな成功から広げる案があります。後者の利点として最も適切なものはどれです… |
| [scaling 問7](../../exercises/scaling.md#q7) | 4.4.2 | 部門ごとに短期の成果は出ていますが、それぞれ別のやり方で作られ、再利用できません。全社への展開に向け… |
| [scaling 問8](../../exercises/scaling.md#q8) | 4.4.3 | AI CoE の主な目的として最も適切なものはどれですか。 |
| [scaling 問9](../../exercises/scaling.md#q9) | 4.4.3 | 全案件を集中型の CoE で開発しています。依頼が積み上がり、現場は数か月待っています。最も適切な見… |
| [scaling 問10](../../exercises/scaling.md#q10) | 4.4.3 | 各部門が別々に AI を導入し、同じ機能の開発が重複し、ベンダーの評価基準もばらばらです。部門横断の… |
| [scaling 問11](../../exercises/scaling.md#q11) | 4.4.4 | 社内の AI アシスタントの回答の質について、継続して利用者の評価を集める方法として最も適切なものは… |
| [scaling 問12](../../exercises/scaling.md#q12) | 4.4.4 | AI の取り組みの定期的なレビューの進め方として、最も適切なものはどれですか。 |
| [scaling 問13](../../exercises/scaling.md#q13) | 4.4.4 | 導入の直後は処理時間が大きく短くなりましたが、1 年後には差が小さくなってきました。成功の指標の扱い… |
| [scaling 問14](../../exercises/scaling.md#q14) | 4.4.4 | 全社の AI の進捗を追う指標の組み合わせとして、適切なものはどれですか。（2つ選択） |
| [scaling 問15](../../exercises/scaling.md#q15) | 4.4.5 | 社内 50 人の PoC で評判の良かった AI を本番に移します。担当者は「PoC に成功したので… |
| [scaling 問16](../../exercises/scaling.md#q16) | 4.4.5 | PoC から本番に移るときに、新たに必要になるものはどれですか。（2つ選択） |
| [scaling 問17](../../exercises/scaling.md#q17) | 4.4.5 | AI の案件の計画書で、PoC の費用と期間だけが計上されています。経営層として指摘すべきことはどれ… |
| [scaling 問18](../../exercises/scaling.md#q18) | 4.4.5 | PoC では開発者が目で出力を確認していました。本番の品質の管理として最も適切なものはどれですか。 |
| [scaling 問19](../../exercises/scaling.md#q19) | 4.4.6 | 全社への拡大の途中で、利用の増加に費用が見合っているかを追いたいと考えています。最も適切な対応はどれ… |
| [scaling 問20](../../exercises/scaling.md#q20) | 4.4.6 | 日本で成功した AI を欧州の拠点に広げます。拡大の際の確認として最も適切なものはどれですか。 |
| [scaling 問21](../../exercises/scaling.md#q21) | 4.4.6 | 利用者の増加とともに、顧客向けの AI の応答が遅くなってきました。拡大の継続を判断するうえで、最も… |
| [scaling 問22](../../exercises/scaling.md#q22) | 4.4.6 | 拡大の途中で同時に見るべき要素はどれですか。（2つ選択） |
| [scaling 問23](../../exercises/scaling.md#q23) | 4.4.6 | ある部門への展開で、定着率が他部門より大きく低いことがわかりました。全社の拡大計画の中での対応として… |

<!-- questions:end -->

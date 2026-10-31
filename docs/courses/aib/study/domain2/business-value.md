# 分野2: KPI と ROI

事業の成果を測り、数字で示す力を問います。ROI の計算問題もあります。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [2.2.1](../../domain2.md#skill-2-2-1) | KPI（有形、無形） |
| [2.2.2](../../domain2.md#skill-2-2-2) | ベースライン |
| [2.2.3](../../domain2.md#skill-2-2-3) | ROI の計算 |
| [2.2.4](../../domain2.md#skill-2-2-4) | 先行指標 |

## 学習の順番 {#study-order}

1. [KPI と ROI](../../../../services/ai-fundamentals.md#kpi-roi): 有形と無形、先行と遅行の区別と、ROI の計算例を確認します。
2. [ビジネス指標](../../../../services/ai-fundamentals.md#business-metrics): コスト、収益、効率、満足度の例を覚えます。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| ROI | （効果 − 費用）÷ 費用 | 分母は費用。効果ではない |
| 時間の換算 | 削減分 × 件数 ÷ 60 × 時間単価 | 時間の活用が前提 |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| KPI を選ぶ | 処理時間や費用など事業の成果。モデルの精度ではない |
| 満足度は数字にならないと言われた | CSAT や NPS で測る |
| 測定を始める時期 | 導入を決める前に、同じ定義で |
| 季節変動がある | 前年の同じ月などと比べる |
| 他の施策と同時に実施した | AI を使うグループと使わないグループで比べる |
| 1 年後の利益まで待てない | 利用率や研修の完了率など先行指標を報告する |
| 精度は高いが利用率が低い | 早い段階で原因を調べる |

## 引っかかりやすい点 {#traps}

- （効果 − 費用）を効果で割る誤りが典型です。
- 費用にはデータ整備、研修、監視、人のレビュー、モデルの更新を入れます。
- 浮いた時間の使い道がなければ、金額の効果にはなりません。
- 導入の前後で指標の定義が違うと、比較できません。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [business-value 問1](../../exercises/business-value.md#q1) | 2.2.1 | 問い合わせ対応を支援する AI の KPI として、最も適切なものはどれですか。 |
| [business-value 問2](../../exercises/business-value.md#q2) | 2.2.1 | AI の効果のうち、有形の効果はどれですか。（2つ選択） |
| [business-value 問3](../../exercises/business-value.md#q3) | 2.2.1 | 経営層が「顧客満足度の改善は数字にならないので KPI にしない」と言っています。最も適切な助言はど… |
| [business-value 問4](../../exercises/business-value.md#q4) | 2.2.1 | 「従業員の生産性の向上」という効果を KPI にしたいと考えています。測定できる形として最も適切なも… |
| [business-value 問5](../../exercises/business-value.md#q5) | 2.2.2 | 効果を正しく示すために、KPI の測定はいつ始めるべきですか。 |
| [business-value 問6](../../exercises/business-value.md#q6) | 2.2.2 | 年末に問い合わせが急増する企業が、繁忙の 12 月を導入前の値とし、閑散の 2 月を導入後の値として… |
| [business-value 問7](../../exercises/business-value.md#q7) | 2.2.2 | AI の導入と同時期に、業務の手順の変更と増員も行われました。AI 自体の効果を切り分けるのに最も適… |
| [business-value 問8](../../exercises/business-value.md#q8) | 2.2.2 | 導入前の「処理時間」は受付から完了までで測り、導入後は担当者の作業時間だけで測っていました。この比較… |
| [business-value 問9](../../exercises/business-value.md#q9) | 2.2.3 | AI の年間の効果が 6,000 万円、年間の費用が 4,000 万円です。ROI はいくらですか。 |
| [business-value 問10](../../exercises/business-value.md#q10) | 2.2.3 | 1 件あたりの処理時間が 3 分短くなりました。年間の件数は 200,000 件、人件費は 1 時間… |
| [business-value 問11](../../exercises/business-value.md#q11) | 2.2.3 | ある案件の ROI を、効果 4,500 万円、費用 2,500 万円で 80% と報告しました。そ… |
| [business-value 問12](../../exercises/business-value.md#q12) | 2.2.3 | ROI の費用に入れるべきものはどれですか。（3つ選択） |
| [business-value 問13](../../exercises/business-value.md#q13) | 2.2.3 | AI で事務の作業時間が年間 10,000 時間減り、担当者は 1 時間 3,000 円換算で 3,… |
| [business-value 問14](../../exercises/business-value.md#q14) | 2.2.3 | AI の提案文で成約率が上がり、売上が増えました。ROI の効果の枠組みのうち、どれにあたりますか。 |
| [business-value 問15](../../exercises/business-value.md#q15) | 2.2.4 | AI の取り組みの先行指標はどれですか。 |
| [business-value 問16](../../exercises/business-value.md#q16) | 2.2.4 | 導入から 3 か月、モデルの精度は高いのですが、利用率は 10% のままです。最も適切な解釈と対応は… |
| [business-value 問17](../../exercises/business-value.md#q17) | 2.2.4 | 先行指標の例はどれですか。（2つ選択） |
| [business-value 問18](../../exercises/business-value.md#q18) | 2.2.4 | 経営層は、利益への効果が見える 1 年後まで判断を待てないと言っています。3 か月目の時点で成否の見… |

<!-- questions:end -->

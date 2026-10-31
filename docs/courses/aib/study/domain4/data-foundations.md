# 分野4: データと基盤

データの準備状況、データ戦略と所有者、基盤の要件を評価します。設計そのものではなく、事業の要件から何を問うかを判断します。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [4.2.1](../../domain4.md#skill-4-2-1) | データの準備状況 |
| [4.2.2](../../domain4.md#skill-4-2-2) | データ戦略、所有者、共有 |
| [4.2.3](../../domain4.md#skill-4-2-3) | 技術と基盤の要件 |

## 学習の順番 {#study-order}

1. [成熟度と準備状況](../../../../services/ai-fundamentals.md#maturity): データの基礎と、サイロの影響を確認します。
2. [データ品質と不均衡](../../../../services/ai-fundamentals.md#data-quality): 品質の問題の種類を確認します。
3. [AWS Cloud Adoption Framework for AI](../../../../services/ai-fundamentals.md#caf-ai): データ戦略と AI フライホイールの関係を押さえます。
4. [AWS の AI の 3 階層](../../../../services/ai-managed-services.md#three-layers): 階層ごとの基盤と人材の要件を比べます。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| データの準備の 4 観点 | 品質、アクセス、サイロ、権利 | 問題の例と結びつけて覚える |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 販売とサポートのデータがつながらない | サイロ。精度が制限され、整備も重複する |
| 取り出しに毎回数週間かかる | アクセス |
| 別の目的で得たデータを学習に使う | 権利と同意の範囲 |
| 品質の問題を誰も直さない | データの所有者を決める |
| 共有が滞る、または無秩序に広がる | データの共有の枠組み |
| 案件ごとに場当たりで整備している | データ戦略 |
| 基盤の負担を最小にしたい | Amazon Quick のようなアプリケーション |
| 全社に広げる前に確認する | 利用量、応答速度、費用の予測、データの所在 |

## 引っかかりやすい点 {#traps}

- データが分かれていても、モデルが自動で統合してくれるわけではありません。
- ハイパーパラメータやアルゴリズムの選定は範囲外です。
- パイロットと同じ費用で全社に広がるとは限りません。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [data-foundations 問1](../../exercises/data-foundations.md#q1) | 4.2.1 | 解約予測を作りたいのですが、販売のデータとサポートのデータが部門ごとに別のシステムにあり、つながりま… |
| [data-foundations 問2](../../exercises/data-foundations.md#q2) | 4.2.1 | データ分析の担当者が、必要なデータの取り出しに毎回数週間かかると訴えています。データの準備状況のどの… |
| [data-foundations 問3](../../exercises/data-foundations.md#q3) | 4.2.1 | 顧客が別の目的で提供した情報を、AI の学習に使う案があります。データの準備状況で確認すべき観点はど… |
| [data-foundations 問4](../../exercises/data-foundations.md#q4) | 4.2.1 | 顧客の名寄せができておらず、同じ顧客が複数の番号で登録されています。AI の案件を進める前の評価とし… |
| [data-foundations 問5](../../exercises/data-foundations.md#q5) | 4.2.2 | データの品質の問題が見つかっても、誰も修正の責任を持たず放置されています。最も適切な対応はどれですか… |
| [data-foundations 問6](../../exercises/data-foundations.md#q6) | 4.2.2 | 部門をまたぐデータの利用の承認が案件ごとに滞る一方で、別の部門では無秩序に共有が広がっています。何が… |
| [data-foundations 問7](../../exercises/data-foundations.md#q7) | 4.2.2 | データ戦略がない企業で起きやすいこととして、最も適切なものはどれですか。 |
| [data-foundations 問8](../../exercises/data-foundations.md#q8) | 4.2.2 | データ戦略が競争優位につながる理由として、最も適切なものはどれですか。 |
| [data-foundations 問9](../../exercises/data-foundations.md#q9) | 4.2.2 | データの所有者の責任に含まれるものはどれですか。（2つ選択） |
| [data-foundations 問10](../../exercises/data-foundations.md#q10) | 4.2.3 | 自社で ML の基盤と人材をほとんど持たない企業が、基盤の負担を最小にしたいと考えています。AWS … |
| [data-foundations 問11](../../exercises/data-foundations.md#q11) | 4.2.3 | 全社への展開の前に、事業の責任者が技術チームに確認すべき問いとして、最も適切なものはどれですか。 |
| [data-foundations 問12](../../exercises/data-foundations.md#q12) | 4.2.3 | AI の基盤の要件を評価する観点はどれですか。（2つ選択） |
| [data-foundations 問13](../../exercises/data-foundations.md#q13) | 4.2.3 | 独自のモデルを自社で学習する案と、マネージドのサービスを使う案があります。基盤の要件の説明として正し… |
| [data-foundations 問14](../../exercises/data-foundations.md#q14) | 4.2.3 | パイロットは問題なく動きました。全社に広げたときの基盤の評価で、特に確認すべきものはどれですか。 |

<!-- questions:end -->

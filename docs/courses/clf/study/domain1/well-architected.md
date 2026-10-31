# 分野1: Well-Architected Framework

6 つの柱の名前と、問題文の表現からどの柱かを判断する力を問います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [Well-Architected Framework](../../domain1.md#t1-2-wa-framework) | 枠組みと Well-Architected Tool |
| [6 つの柱](../../domain1.md#t1-2-pillars) | 6 つの柱の問い |
| [柱の違いの見分け方](../../domain1.md#t1-2-pillar-differences) | 設計原則からの判別 |

## 学習の順番 {#study-order}

1. [Well-Architected Framework](../../../../services/cloud-foundations.md#well-architected): 6 つの柱の名前と問いを覚えます。
2. 同じ節の設計原則の例: 動詞や目的から柱を見分けられるようにします。
3. [Well-Architected Tool](../../../../services/cloud-foundations.md#wa-tool): 指摘と記録を行うツールで、自動では修正しないことを確認します。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| 柱 | 6 つ | 運用上の優秀性、セキュリティ、信頼性、パフォーマンス効率、コスト最適化、サステナビリティ |
| Well-Architected Tool の料金 | 追加料金なし | 自動の修正は行わない |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 小さく元に戻せる変更を頻繁に行う | 運用上の優秀性 |
| 人をデータから遠ざける、追跡できるようにする | セキュリティ |
| 復旧手順をテストする、自動で復旧する | 信頼性 |
| サーバーレスを使う、頻繁に実験する | パフォーマンス効率 |
| 使った分だけ払う、費用を配賦する | コスト最適化 |
| 使用率を上げて消費電力を減らす | サステナビリティ |
| ワークロードを質問形式でレビューする | Well-Architected Tool |

## 引っかかりやすい点 {#traps}

- 費用を減らすならコスト最適化、環境負荷を減らすならサステナビリティです。問題文の目的で分けます。
- 障害からの復旧は信頼性、リソースの選び方と使い方はパフォーマンス効率です。
- システムの設計の見直しは Well-Architected、組織の移行準備は AWS CAF です。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [well-architected 問1](../../exercises/well-architected.md#q1) | Well-Architected Framework | AWS Well-Architected Framework の説明として最も適切なものはどれですか… |
| [well-architected 問2](../../exercises/well-architected.md#q2) | Well-Architected Framework | 開発チームが、自分たちのワークロードを質問に答える形で見直し、改善点を記録したいと考えています。最も… |
| [well-architected 問3](../../exercises/well-architected.md#q3) | Well-Architected Framework | AWS Well-Architected Tool の説明として正しいものはどれですか。 |
| [well-architected 問4](../../exercises/well-architected.md#q4) | 6 つの柱 | AWS Well-Architected Framework の柱に含まれるものはどれですか。（2つ… |
| [well-architected 問5](../../exercises/well-architected.md#q5) | 6 つの柱 | Well-Architected の柱のうち、「障害から復旧し、期待どおり動くか」を問うものはどれで… |
| [well-architected 問6](../../exercises/well-architected.md#q6) | 6 つの柱 | Well-Architected の柱のうち、「不要な費用を避けられるか」を問うものはどれですか。 |
| [well-architected 問7](../../exercises/well-architected.md#q7) | 柱の違いの見分け方 | ある会社は、運用手順をコードにして、小さく元に戻せる変更を頻繁に行うようにしました。どの柱の考え方で… |
| [well-architected 問8](../../exercises/well-architected.md#q8) | 柱の違いの見分け方 | ある会社は、担当者が本番データに直接触らなくても済むように、ツールを整備しました。どの柱の考え方です… |
| [well-architected 問9](../../exercises/well-architected.md#q9) | 柱の違いの見分け方 | 新しい世代のインスタンスに替えて使用率を上げ、消費電力を減らす取り組みをしています。目的は環境への影… |
| [well-architected 問10](../../exercises/well-architected.md#q10) | 柱の違いの見分け方 | 本番の障害を想定して復旧手順を定期的にテストし、監視から自動で復旧するようにしました。どの柱の考え方… |
| [well-architected 問11](../../exercises/well-architected.md#q11) | 柱の違いの見分け方 | チームが、サーバーレスの構成を使い、頻繁に実験して最適な構成を選ぶようにしました。どの柱の考え方です… |
| [well-architected 問12](../../exercises/well-architected.md#q12) | 柱の違いの見分け方 | 各部門の費用を分析して配賦し、使った分だけ払う形に切り替えました。どの柱の考え方ですか。 |

<!-- questions:end -->

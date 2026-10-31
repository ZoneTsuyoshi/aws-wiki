# 分野1: AI の基本概念

AI の言葉を、事業の場面で正しく使い分ける力を問います。データの種類と品質、過去データによる学習の限界、国際規格の役割も含みます。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [1.1.1](../../domain1.md#skill-1-1-1) | 事業の文脈での基本概念 |
| [1.1.2](../../domain1.md#skill-1-1-2) | AI、ML、生成 AI の違い |
| [1.1.3](../../domain1.md#skill-1-1-3) | 構造化データと非構造化データ |
| [1.1.4](../../domain1.md#skill-1-1-4) | データ品質の重要性 |
| [1.1.5](../../domain1.md#skill-1-1-5) | 過去データによる学習 |
| [1.1.6](../../domain1.md#skill-1-1-6) | 国際的な枠組みと共通の語彙 |

## 学習の順番 {#study-order}

1. [モデル、アルゴリズム、学習、推論](../../../../services/ai-fundamentals.md#model-training-inference): 学習は作る段階、推論は使う段階で、費用の出方が違うことを押さえます。
2. [AI、ML、深層学習、生成 AI の関係](../../../../services/ai-fundamentals.md#ai-ml-dl): 包含の関係と、ルールベースも広い意味の AI に入ることを確認します。
3. [従来の ML と FM の使い分け](../../../../services/ai-fundamentals.md#ml-vs-fm): 数値や分類を返すのか、新しい内容を作るのかで見分けます。
4. [データの種類](../../../../services/ai-fundamentals.md#data-types): 表は構造化、文書や画像や音声は非構造化です。
5. [データ品質と不均衡](../../../../services/ai-fundamentals.md#data-quality): 欠損、重複、偏り、古さが結果に与える影響を覚えます。
6. [学習の種類](../../../../services/ai-fundamentals.md#learning-types)と[過学習](../../../../services/ai-fundamentals.md#overfitting): ラベルの有無と、学習に使わないデータで評価する理由を確認します。
7. [標準と規制](../../../../services/ai-fundamentals.md#standards): 3 つの ISO/IEC 規格の役割を区別します。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| ISO/IEC 42001 | AI マネジメントシステムの要求事項 | 組織の仕組みの認証 |
| ISO/IEC 23053 | ML を使う AI システムの枠組み | 構成要素の整理 |
| ISO/IEC 22989 | AI の概念と用語 | 語彙をそろえる |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 毎朝、学習済みの仕組みで予測を出す | 推論 |
| 文章や画像を新しく作る | 生成 AI |
| 数値や分類を返す | 従来の ML |
| 予測が悪く、データに重複や欠損がある | モデルの変更より先にデータを直す |
| RAG が廃止された規定を根拠に答える | 古い文書を検索の対象から外す |
| 学習データでは高精度で、新しいデータでは低い | 過学習 |
| 第三者の認証を受けたい | ISO/IEC 42001 |

## 引っかかりやすい点 {#traps}

- 表示された確率の値は予測で、モデルの精度ではありません。
- データの期間が長くても、過去の偏りは消えません。むしろ学習されます。
- AWS が ISO/IEC 42001 の認証を受けていても、自社の AI の統治は自社の責任です。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [ai-concepts 問1](../../exercises/ai-concepts.md#q1) | 1.1.1 | ある小売企業は、過去 3 年の販売データから来店数を予測する仕組みを作りました。今は毎朝、その仕組み… |
| [ai-concepts 問2](../../exercises/ai-concepts.md#q2) | 1.1.1 | 経営会議で「解約予測モデル」という言葉が出ました。出席者に「モデル」を説明するとき、最も適切なものは… |
| [ai-concepts 問3](../../exercises/ai-concepts.md#q3) | 1.1.1 | 予算の担当者が「モデルの学習が終われば、その後の AI の費用はなくなりますか」と質問しました。最も… |
| [ai-concepts 問4](../../exercises/ai-concepts.md#q4) | 1.1.1 | 担当者の画面に「顧客 A の解約確率は 80%」と表示されました。この「80%」の説明として正しいも… |
| [ai-concepts 問5](../../exercises/ai-concepts.md#q5) | 1.1.2 | 次のうち、生成 AI の用途はどれですか。 |
| [ai-concepts 問6](../../exercises/ai-concepts.md#q6) | 1.1.2 | AI、ML（機械学習）、生成 AI の関係を正しく表しているものはどれですか。 |
| [ai-concepts 問7](../../exercises/ai-concepts.md#q7) | 1.1.2 | あるベンダーが「当社の AI は、専門家が書いた if-then の規則で判定します。データからの学… |
| [ai-concepts 問8](../../exercises/ai-concepts.md#q8) | 1.1.2 | 数値や分類を返す、従来の ML の典型的な用途はどれですか。（2つ選択） |
| [ai-concepts 問9](../../exercises/ai-concepts.md#q9) | 1.1.3 | 次のうち、非構造化データはどれですか。 |
| [ai-concepts 問10](../../exercises/ai-concepts.md#q10) | 1.1.3 | 保険会社には、保険金請求の自由記述の文章と、添付の事故写真が大量にあります。このデータの活用について… |
| [ai-concepts 問11](../../exercises/ai-concepts.md#q11) | 1.1.3 | ある企業には、契約者の属性と過去の支払い履歴が表の形で整理されています。支払いの遅れを契約者ごとに予… |
| [ai-concepts 問12](../../exercises/ai-concepts.md#q12) | 1.1.4 | 需要予測の精度が低いままです。調べると、同じ商品が別のコードで重複し、販売日の欠損も多いことがわかり… |
| [ai-concepts 問13](../../exercises/ai-concepts.md#q13) | 1.1.4 | 社内規定に答えるチャットボットが、廃止された規定を根拠に回答しています。検索の対象フォルダには、新旧… |
| [ai-concepts 問14](../../exercises/ai-concepts.md#q14) | 1.1.4 | 融資の審査モデルの学習データの大半は、都市部の顧客でした。導入後、地方の顧客に対する判定の結果が悪い… |
| [ai-concepts 問15](../../exercises/ai-concepts.md#q15) | 1.1.4 | データ品質と AI の成果の関係について、正しい説明はどれですか。（2つ選択） |
| [ai-concepts 問16](../../exercises/ai-concepts.md#q16) | 1.1.5 | ある企業が過去 10 年の採用の記録でモデルを学習し、応募者を採点しようとしています。当時の採用者は… |
| [ai-concepts 問17](../../exercises/ai-concepts.md#q17) | 1.1.5 | 開発チームから「学習データでの精度は非常に高いのですが、新しいデータで試すと大きく下がりました」と報… |
| [ai-concepts 問18](../../exercises/ai-concepts.md#q18) | 1.1.5 | 本番に出す前に、モデルを学習に使わなかったデータで評価する理由として、最も適切なものはどれですか。 |
| [ai-concepts 問19](../../exercises/ai-concepts.md#q19) | 1.1.5 | 過去の顧客について「解約した、しなかった」の記録があります。この記録を正解として、新しい顧客の解約を… |
| [ai-concepts 問20](../../exercises/ai-concepts.md#q20) | 1.1.5 | 5 年分の実店舗の販売データで学習したモデルがあります。今年から始めたネット販売の需要も、このモデル… |
| [ai-concepts 問21](../../exercises/ai-concepts.md#q21) | 1.1.6 | ある企業は、自社の AI の統治の仕組みについて、第三者による認証を受けたいと考えています。どの規格… |
| [ai-concepts 問22](../../exercises/ai-concepts.md#q22) | 1.1.6 | 技術チームと事業部門で、ML を使う AI システムの構成要素を同じ言葉で整理したいと考えています。… |
| [ai-concepts 問23](../../exercises/ai-concepts.md#q23) | 1.1.6 | グループ会社ごとに「AI」「学習」などの言葉の定義が違い、議論がかみ合いません。共通の語彙をそろえる… |
| [ai-concepts 問24](../../exercises/ai-concepts.md#q24) | 1.1.6 | AWS は ISO/IEC 42001 の認証を受けています。この事実を自社の AI の統治にどう位… |

<!-- questions:end -->

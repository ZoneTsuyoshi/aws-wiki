# 分野2: 作る、買う、組むと移行

予算、期限、社内の能力、ベンダーの提案、規制の要件から調達の方法を選びます。AI への移行や基盤間の移行の確認事項も扱います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [2.1.2](../../domain2.md#skill-2-1-2) | 作る、買う、組む |
| [2.1.5](../../domain2.md#skill-2-1-5) | AI への移行、基盤間の移行 |

## 学習の順番 {#study-order}

1. [作る、買う、組む](../../../../services/ai-fundamentals.md#build-buy-partner): 4 つの選択と AWS の例を表で覚えます。
2. [AWS の AI の 3 階層](../../../../services/ai-managed-services.md#three-layers): Quick、Bedrock、SageMaker AI の違いを、制御と必要な人材で見分けます。
3. [Amazon Quick](../../../../services/ai.md#quick)と [AWS Marketplace](../../../../services/cloud-foundations.md#marketplace): 完成品と第三者の製品の入手先を確認します。
4. [モデルのライフサイクル](../../../../services/genai-apps.md#model-lifecycle)と [FM の選択と切り替え](../../../../services/genai-apps.md#fm-selection): 切り替えられる設計が必要な理由を押さえます。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| 移行の 4 観点 | 事業の継続、費用、データの準備、性能への影響 | 基盤間の移行でも同じ |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 差別化にならず、早く始めたい | 買う（Amazon Quick、Marketplace の製品） |
| 自社の業務に合わせたアプリを作る | Amazon Bedrock |
| 独自データが競争力で、専門人材がいる | Amazon SageMaker AI で作る |
| 人材や期間が足りない | パートナーと組む |
| 機能が同等のベンダーを比べる | データの扱いと乗り換えのしやすさ |
| 業務を止めずに切り替える | 並行運用、段階的な切り替え、切り戻しの手順 |
| 料金体系が変わる | 実際の利用量で、移行費を含む総費用を比べる |

## 引っかかりやすい点 {#traps}

- 初期費用だけの比較は誤りです。運用と更新を含めます。
- 機能と価格が優れていても、規制の要件を満たせないなら候補から外します。
- EOL の後に自動の移行はありません。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [build-buy 問1](../../exercises/build-buy.md#q1) | 2.1.2 | 中堅の商社は、社内文書の調査と日常業務の補助を、できるだけ早く社員に提供したいと考えています。差別化… |
| [build-buy 問2](../../exercises/build-buy.md#q2) | 2.1.2 | ある製造業は、独自の設備のセンサーデータが競争力の源泉だと考えています。専門のデータサイエンティスト… |
| [build-buy 問3](../../exercises/build-buy.md#q3) | 2.1.2 | 自社の業務の流れに合わせた、顧客向けの生成 AI アプリを半年以内に出したいと考えています。モデルの… |
| [build-buy 問4](../../exercises/build-buy.md#q4) | 2.1.2 | ある保険会社には独自の要件があり、市販の製品では足りません。期限は 9 か月後で、社内の人材はこの期… |
| [build-buy 問5](../../exercises/build-buy.md#q5) | 2.1.2 | 2 社のベンダーの提案を比べます。機能はどちらも要件を満たしています。次に確認すべきこととして、最も… |
| [build-buy 問6](../../exercises/build-buy.md#q6) | 2.1.2, 2.2.5 | 第三者の AI 製品を探して比べ、購入後の支払いを AWS の請求にまとめたいと考えています。該当す… |
| [build-buy 問7](../../exercises/build-buy.md#q7) | 2.1.2 | 作ると買うの比較で、担当者は初期開発費だけを比べて「作るほうが安い」と結論づけました。この比較の問題… |
| [build-buy 問8](../../exercises/build-buy.md#q8) | 2.1.2 | 候補のベンダーは機能と価格で最も優れていますが、自社の規制が求める地域でのデータ処理を保証できません… |
| [build-buy 問9](../../exercises/build-buy.md#q9) | 2.1.5 | 請求の問い合わせ対応を AI に移行します。業務を止めないために、最も適切な進め方はどれですか。 |
| [build-buy 問10](../../exercises/build-buy.md#q10) | 2.1.5 | シート課金の AI アプリから、トークン課金の基盤へ移ることを検討しています。費用の面で最も適切な確… |
| [build-buy 問11](../../exercises/build-buy.md#q11) | 2.1.5 | 別の AI 基盤へ移ると費用が下がる見込みです。性能への影響を確かめる方法として、最も適切なものはど… |
| [build-buy 問12](../../exercises/build-buy.md#q12) | 2.1.5 | Amazon Bedrock の基盤モデルに提供の終了があることを踏まえて、業務に組み込む前に用意し… |
| [build-buy 問13](../../exercises/build-buy.md#q13) | 2.1.5 | 業務を AI へ移行する準備で確認すべき観点はどれですか。（2つ選択） |

<!-- questions:end -->

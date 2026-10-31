# 分野2: プロンプトの調整

重みを変える前にプロンプトを調整します。パラメータの値と手法の使い分けを問います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [2.2.8](../../domain2.md#skill-2-2-8) | AI ソリューションのカスタマイズ |

## 学習の順番 {#study-order}

1. [プロンプトエンジニアリング](../../../../services/ai-fundamentals.md#prompt-engineering): フューショットと Chain-of-thought を確認します。
2. [パラメータの調整](../../../../services/genai-apps.md#parameter-tuning): temperature の目安を覚えます。
3. [構造化出力](../../../../services/genai-apps.md#structured-output): 形式を揃える方法を押さえます。
4. [プロンプトの管理](../../../../services/genai-apps.md#prompt-management): バリアントの比較を確認します。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| 抽出、分類の temperature | 0〜0.2 | ばらつきを抑える |
| 文案の temperature | 0.7 以上 | 多様性を出す |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 分類の基準を示す | フューショット |
| 計算や推論を段階的に | Chain-of-thought |
| 決まった形式で返させる | JSON Schema の構造化出力 |
| プロンプトで足りない | ファインチューニング |

## 引っかかりやすい点 {#traps}

- 手間の大きいファインチューニングから始める選択は誤りです。まずプロンプトを調整します。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [prompts 問1](../../exercises/prompts.md#q1) | 2.2.8 | 問い合わせを 5 つのカテゴリに分類し、結果を毎回同じ形式で返します。パラメータとプロンプトの設定と… |
| [prompts 問2](../../exercises/prompts.md#q2) | 2.2.8 | 計算の手順を含む問い合わせで、FM の誤りが多いです。モデルは変えません。最初に試す調整はどれですか… |
| [prompts 問3](../../exercises/prompts.md#q3) | 2.2.8 | AI ソリューションのカスタマイズを進める順序として適切なものはどれですか。 |

<!-- questions:end -->

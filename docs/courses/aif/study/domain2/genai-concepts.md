# 分野2: 生成 AI の基本

用語の意味と、生成 AI が得意なこと、苦手なことを問います。分野3 の前提になります。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [2.1.1](../../domain2.md#obj-2-1-1) | 生成 AI の基本用語 |
| [2.1.2](../../domain2.md#obj-2-1-2) | 生成 AI のユースケース |
| [2.1.3](../../domain2.md#obj-2-1-3) | FM のライフサイクル |
| [2.1.5](../../domain2.md#obj-2-1-5) | コンテキストエンジニアリング |
| [2.2.1](../../domain2.md#obj-2-2-1) | 生成 AI の長所 |
| [2.2.2](../../domain2.md#obj-2-2-2) | 生成 AI の短所 |

## 学習の順番 {#study-order}

1. [トークンとコンテキストウィンドウ](../../../../services/ai-fundamentals.md#tokens): トークン、チャンク、コンテキストウィンドウの関係を理解します。
2. [埋め込みとベクトル](../../../../services/ai-fundamentals.md#embeddings)と[モデルの種類](../../../../services/ai-fundamentals.md#model-kinds): 埋め込みとモデルの種類の用途を押さえます。
3. [FM のライフサイクル](../../../../services/ai-fundamentals.md#fm-lifecycle): 段階の順番を覚えます。
4. [プロンプトエンジニアリング](../../../../services/ai-fundamentals.md#prompt-engineering): コンテキストエンジニアリングの段落を読みます。
5. [生成 AI の長所と短所](../../../../services/ai-fundamentals.md#genai-pros-cons)と[ハルシネーションへの対策](../../../../services/ai-fundamentals.md#hallucinations): 長所と短所、ハルシネーションの対策を結びつけます。

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 意味で検索する | 埋め込みとベクトル |
| 文書が大きく検索しにくい | チャンク化 |
| ノイズを除去して画像を作る | 拡散モデル |
| 図表と文章を一緒に扱う | マルチモーダルモデル |
| 存在しない判例を挙げる | ハルシネーション |
| 回答が毎回変わる | 非決定性。temperature を下げる |
| 順位付けと説明文の両方 | Personalize と FM |
| 通話の要約 | Bedrock の LLM |
| 「何を渡すか」を設計する | コンテキストエンジニアリング |

## 引っかかりやすい点 {#traps}

- temperature を下げてもばらつきが減るだけで、誤りはなくなりません。
- 事前学習は通常は提供者が行います。
- コンテキストエンジニアリングは「どう書くか」ではなく「何を渡すか」です。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [genai-concepts 問1](../../exercises/genai-concepts.md#q1) | 2.1.1 | 「犬」と「子犬」のように意味が近い文章を、キーワードが一致しなくても探したいと考えています。文章を数… |
| [genai-concepts 問2](../../exercises/genai-concepts.md#q2) | 2.1.1 | 長いマニュアルを RAG で使うために、検索しやすい単位に分割します。この処理の名前はどれですか。 |
| [genai-concepts 問3](../../exercises/genai-concepts.md#q3) | 2.1.1 | ノイズを少しずつ取り除くことで画像を生成するモデルはどれですか。 |
| [genai-concepts 問4](../../exercises/genai-concepts.md#q4) | 2.1.1 | 図表の画像と質問の文章を一緒に受け取って答えるモデルを探しています。必要なモデルの種類はどれですか。 |
| [genai-concepts 問5](../../exercises/genai-concepts.md#q5) | 2.1.1 | 生成 AI の用語の説明として正しいものを選んでください。（2つ選択） |
| [genai-concepts 問6](../../exercises/genai-concepts.md#q6) | 2.1.2 | 会議の議事録を短くまとめる機能を作りたいと考えています。生成 AI のユースケースとして当てはまるも… |
| [genai-concepts 問7](../../exercises/genai-concepts.md#q7) | 2.1.2 | 利用者の注文を調べ、条件を満たせば返金の手続きまで行うカスタマーサービスを作ります。適切なものはどれ… |
| [genai-concepts 問8](../../exercises/genai-concepts.md#q8) | 2.1.2 | EC サイトで、商品の順位付けとおすすめの理由の文章の両方を作ります。適切な組み合わせはどれですか。 |
| [genai-concepts 問9](../../exercises/genai-concepts.md#q9) | 2.1.2 | 広告の素材用に、文章の指示から画像を作りたいと考えています。適切な選択はどれですか。 |
| [genai-concepts 問10](../../exercises/genai-concepts.md#q10) | 2.1.3 | FM のライフサイクルの正しい順番はどれですか。 |
| [genai-concepts 問11](../../exercises/genai-concepts.md#q11) | 2.1.3 | Bedrock の FM を使う企業にとって、通常はモデルの提供者が担当する段階はどれですか。 |
| [genai-concepts 問12](../../exercises/genai-concepts.md#q12) | 2.1.3 | FM をデプロイした後に、回答ごとの評価ボタンで利用者の声を集め、次の改善に使っています。ライフサイ… |
| [genai-concepts 問13](../../exercises/genai-concepts.md#q13) | 2.1.5 | コンテキストエンジニアリングの説明として最も適切なものはどれですか。 |
| [genai-concepts 問14](../../exercises/genai-concepts.md#q14) | 2.1.5 | チャットの会話が長くなると、費用が増え、最初の指示が失われることがあります。コンテキストエンジニアリ… |
| [genai-concepts 問15](../../exercises/genai-concepts.md#q15) | 2.1.5 | 次のうち、FM に渡すコンテキストに含まれるものを選んでください。（2つ選択） |
| [genai-concepts 問16](../../exercises/genai-concepts.md#q16) | 2.2.1 | 同じモデルを、要約にも分類にも翻訳にも使えました。この生成 AI の長所はどれですか。 |
| [genai-concepts 問17](../../exercises/genai-concepts.md#q17) | 2.2.1 | 利用者が追加の質問を自然文で続けても、チャットボットが文脈を踏まえて答えられます。この長所を表すもの… |
| [genai-concepts 問18](../../exercises/genai-concepts.md#q18) | 2.2.1 | 製品説明の下書きを数秒で作れることが評価されています。当てはまる生成 AI の長所を選んでください。… |
| [genai-concepts 問19](../../exercises/genai-concepts.md#q19) | 2.2.2 | チャットボットが、存在しない判例をもっともらしく挙げました。この短所の名前はどれですか。 |
| [genai-concepts 問20](../../exercises/genai-concepts.md#q20) | 2.2.2 | 同じ質問に、回答が毎回少しずつ変わります。この性質を減らすために、まず調整するものはどれですか。 |
| [genai-concepts 問21](../../exercises/genai-concepts.md#q21) | 2.2.2 | ある FM の判断について、理由を問われても十分に説明できません。この短所はどれですか。また、補う方… |
| [genai-concepts 問22](../../exercises/genai-concepts.md#q22) | 2.2.2 | 「temperature を 0 に近づければ、生成 AI の誤りはなくなる」という意見があります。… |

<!-- questions:end -->

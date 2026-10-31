# 分野1: 解決策の種類

課題に合う解決策の種類を選ぶ力を問います。ルールか AI か、RAG かエージェントか、作った後の監視、ツールの分類までを扱います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [1.2.1](../../domain1.md#skill-1-2-1) | ルールベースか AI か |
| [1.2.2](../../domain1.md#skill-1-2-2) | AI エージェントの能力 |
| [1.2.3](../../domain1.md#skill-1-2-3) | 継続的な監視と更新 |
| [1.2.4](../../domain1.md#skill-1-2-4) | AI ツールの分類とシャドー AI |

## 学習の順番 {#study-order}

1. [AI を使わない判断](../../../../services/ai-fundamentals.md#when-not-ai): 規則を書き切れるかどうかを最初に確認します。
2. [エージェント](../../../../services/ai-fundamentals.md#agents): チャット、RAG、エージェントの違いを、外部を変更するかどうかで見分けます。
3. [マルチエージェント](../../../../services/genai-apps.md#multi-agent)と[安全な自律動作](../../../../services/genai-apps.md#agent-safeguards): 方式の名前と、権限の制限、人の承認を確認します。
4. [本番での監視](../../../../services/ai-fundamentals.md#production-monitoring)と[ドリフトの種類](../../../../services/sagemaker.md#drift): コードを変えなくても精度が落ちる理由を説明できるようにします。
5. [モデルのライフサイクル](../../../../services/genai-apps.md#model-lifecycle): Active、Legacy、EOL の動きを確認します。
6. [シャドー AI](../../../../services/ai-fundamentals.md#shadow-ai): 承認済み、評価中、禁止の 3 分類と、代替の提供を覚えます。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| Bedrock のモデルの状態 | Active、Legacy、EOL | EOL の後はリクエストが失敗する。自動の移行はない |
| ツールの分類 | 承認済み、評価中、禁止 | 入力してよいデータの範囲も示す |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 条件が表で完全に定義されている | ルールベース |
| 手口が変わり、規則を書き切れない | ML |
| 1 つの業務に形の決まらない入力と明確な判定がある | 読み取りは AI、判定は規則と組み合わせる |
| 文書に基づく回答だけでよい | RAG。エージェントは不要 |
| 調べて、登録して、手配まで自分で進める | エージェント。権限の制限と人の承認も要求する |
| 処理の順序を保証したい | 決まった流れで進める方式 |
| エラーがないのに精度が徐々に落ちる | モデルドリフト |
| 個人契約の AI が使われている | 分類の公開と、承認済みの代替の提供 |

## 引っかかりやすい点 {#traps}

- データドリフトは入力の変化、コンセプトドリフトは入力と正解の関係の変化です。
- 導入時の精度が高くても、運用費はゼロになりません。
- 全面禁止は逆効果です。隠れた利用が続き、把握もできなくなります。
- エージェントは最も新しい選択肢ですが、要件を超えるなら選びません。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [solution-types 問1](../../exercises/solution-types.md#q1) | 1.2.1 | 会員ランクと注文額の組み合わせで割引率を決める処理を自動化します。割引率は表で完全に定義され、例外は… |
| [solution-types 問2](../../exercises/solution-types.md#q2) | 1.2.1 | 自由な文章で届く問い合わせメールを 20 の担当窓口に振り分けています。キーワードの規則は数千に増え… |
| [solution-types 問3](../../exercises/solution-types.md#q3) | 1.2.1 | 監査のために、経費の上限チェックは毎回同じ結果を出し、判定の根拠を説明できる必要があります。ルールベ… |
| [solution-types 問4](../../exercises/solution-types.md#q4) | 1.2.1 | クレジットカードの不正の手口は毎月のように変わり、担当者が規則を追加しても追いつきません。最も適切な… |
| [solution-types 問5](../../exercises/solution-types.md#q5) | 1.2.1 | 経費精算の自動化を検討しています。紙の領収書から金額と日付を読み取る部分と、「1 件 5 万円を超え… |
| [solution-types 問6](../../exercises/solution-types.md#q6) | 1.2.2 | 顧客対応の AI で「注文の状況を調べ、返品を登録し、配送を手配する」までを、状況に応じて自分で手順… |
| [solution-types 問7](../../exercises/solution-types.md#q7) | 1.2.2 | 社員の質問に、社内規定を根拠に引用付きで答えられれば十分です。外部のシステムは変更しません。担当者は… |
| [solution-types 問8](../../exercises/solution-types.md#q8) | 1.2.2 | エージェントが在庫の API を呼んで残数を確認し、足りなければ発注の API を呼びます。これはエ… |
| [solution-types 問9](../../exercises/solution-types.md#q9) | 1.2.2 | 別の部門が別の基盤で作った在庫担当のエージェントに、営業担当のエージェントが標準のプロトコルで問い合… |
| [solution-types 問10](../../exercises/solution-types.md#q10) | 1.2.2 | 計画役のエージェントが、調査、執筆、確認の専門エージェントに仕事を分担し、結果をまとめます。この調整… |
| [solution-types 問11](../../exercises/solution-types.md#q11) | 1.2.2 | 監査の要件で、申請の処理は必ず決まった順序で各エージェントを通す必要があります。方式の方向性として最… |
| [solution-types 問12](../../exercises/solution-types.md#q12) | 1.2.2 | 返金まで自動で行うエージェントの導入を承認します。自律性の高さに応じて、要求すべき統制はどれですか。… |
| [solution-types 問13](../../exercises/solution-types.md#q13) | 1.2.3 | 2 年前に導入した売上予測の精度が徐々に落ちています。コードの変更はなく、エラーも出ていません。最も… |
| [solution-types 問14](../../exercises/solution-types.md#q14) | 1.2.3 | 不正検知のモデルで、不正の手口が変わり、同じような取引でも正解が以前と変わってきました。これはどの変… |
| [solution-types 問15](../../exercises/solution-types.md#q15) | 1.2.3 | 利用中の Amazon Bedrock の基盤モデルが Legacy の状態になり、終了の日付が通知… |
| [solution-types 問16](../../exercises/solution-types.md#q16) | 1.2.3 | AI の事業計画の案で、運用費が「導入後はゼロ」となっています。導入時の精度が 95% と高いことが… |
| [solution-types 問17](../../exercises/solution-types.md#q17) | 1.2.3 | 本番の AI の性能低下に備えて、導入前に決めておくべきことはどれですか。（2つ選択） |
| [solution-types 問18](../../exercises/solution-types.md#q18) | 1.2.4 | シャドー AI の説明として正しいものはどれですか。 |
| [solution-types 問19](../../exercises/solution-types.md#q19) | 1.2.4 | 法務の審査が終わるまで、ある AI ツールは申請した部署だけが限定的に使えることにしました。AI ツ… |
| [solution-types 問20](../../exercises/solution-types.md#q20) | 1.2.4 | 社員が個人契約の AI ツールを業務に使っていることがわかりました。業務上の需要は強くあります。経営… |
| [solution-types 問21](../../exercises/solution-types.md#q21) | 1.2.4 | 承認済みの AI ツールの一覧を公開します。ツール名に加えて示すべき情報として、最も重要なものはどれ… |

<!-- questions:end -->

# 分野3: Guardrails と入出力の安全対策

入力と出力の検査、ハルシネーションの抑制、敵対的な入力への対策を重ねます。各層が何を守れないかが問われます。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [3.1.1](../../domain3.md#skill-3-1-1) | 有害な入力への対策 |
| [3.1.2](../../domain3.md#skill-3-1-2) | 有害な出力への対策 |
| [3.1.3](../../domain3.md#skill-3-1-3) | ハルシネーションを減らす |
| [3.1.4](../../domain3.md#skill-3-1-4) | 多層防御 |
| [3.1.5](../../domain3.md#skill-3-1-5) | 敵対的な入力の検出 |
| [3.2.3](../../domain3.md#skill-3-2-3) | 有用性を保ちつつプライバシーを守る |

## 学習の順番 {#study-order}

1. [フィルターの種類](../../../../services/ai.md#guardrail-filters)と[層の選び方](../../../../services/genai-apps.md#guardrail-tiers): Standard と Classic の違いを覚えます。
2. [ポリシーごとの設定](../../../../services/ai.md#guardrail-policy-settings)と [Converse で適用する](../../../../services/ai.md#guardrail-converse): 設定値とタグの注意を確認します。
3. [ApplyGuardrail](../../../../services/ai.md#apply-guardrail): モデルを呼ばない検査を理解します。
4. [ストリーミングでの動作](../../../../services/genai-apps.md#guardrail-streaming): 同期と非同期の違いを押さえます。
5. [コンテキストグラウンディング](../../../../services/genai-apps.md#contextual-grounding)と [Automated Reasoning](../../../../services/genai-apps.md#automated-reasoning): 何を検証するかを区別します。
6. [多層防御](../../../../services/genai-apps.md#defense-in-depth)と[適用の強制と限界](../../../../services/ai.md#guardrail-enforcement): 層の役割と評価されない内容を確認します。
7. [データ分類](../../../../services/secrets.md#data-classification)と[サニタイズとマスキング](../../../../services/secrets.md#sanitization-masking): マスク、仮名化、匿名化の違いを理解します。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| グラウンディングのしきい値 | 0〜0.99 | 1 にはできない |
| 拒否トピックの定義 | Standard 1,000 文字、Classic 200 文字 | 最大 30 件 |
| Classic の言語 | 英語、フランス語、スペイン語 | 日本語は Standard |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 日本語で検査する | Standard 層。クロスリージョン推論が必要 |
| 外部のモデルに同じ基準を適用する | `ApplyGuardrail` |
| 文書に基づかない応答を止める | コンテキストグラウンディング |
| 規定と論理的に矛盾しないか | Automated Reasoning |
| 数値の正しさ | text-to-SQL |
| 文の構造を残して個人情報を隠す | `ANONYMIZE` |
| 応答で氏名を戻す | 仮名化。対応表を保護する |

## 引っかかりやすい点 {#traps}

- `async` ではマスクが使えず、不適切な内容が一時的に届くことがあります。
- `InvokeModel` 系ではタグがないとプロンプト攻撃は検査されません。
- `guardrailConfig` は `toolResult` を評価しません。間接インジェクションは別に防ぎます。
- JSON Schema が保証するのは形式で、内容の正しさではありません。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [guardrails 問1](../../exercises/guardrails.md#q1) | 3.1.1 | 日本語のチャットに、憎悪や暴力の入力を止める仕組みと、業務外の投資相談を止める仕組みを入れます。デー… |
| [guardrails 問2](../../exercises/guardrails.md#q2) | 3.1.1 | SageMaker AI で動かす自社のモデルに、Bedrock のモデルと同じ入力の安全基準を適用… |
| [guardrails 問3](../../exercises/guardrails.md#q3) | 3.1.1 | 掲示板への投稿を FM で要約する前に審査します。Guardrails で明らかな違反を止め、判定の… |
| [guardrails 問4](../../exercises/guardrails.md#q4) | 3.1.1 | ガードレールで入力をブロックしたときと、応答をブロックしたときの費用の違いを、経理担当に説明します。… |
| [guardrails 問5](../../exercises/guardrails.md#q5) | 3.1.2 | 日本語のチャットで、ストリーミングの応答に電話番号が一瞬表示されました。ANONYMIZE を設定し… |
| [guardrails 問6](../../exercises/guardrails.md#q6) | 3.1.2 | 売上の数値を答えるチャットで、もっともらしい誤った数値が返ります。文書の RAG を使っていますが、… |
| [guardrails 問7](../../exercises/guardrails.md#q7) | 3.1.2 | 安全チームが 2 つの要求を出しました。(a) 本番の個別の応答で有害な内容を止める。(b) モデル… |
| [guardrails 問8](../../exercises/guardrails.md#q8) | 3.1.3 | RAG の回答が文書に基づかない内容を含むことがあります。生成の時点で止めたいと考えています。しきい… |
| [guardrails 問9](../../exercises/guardrails.md#q9) | 3.1.3 | Converse にコンテキストグラウンディングを設定しましたが、スコアが評価されません。ガードレー… |
| [guardrails 問10](../../exercises/guardrails.md#q10) | 3.1.3 | 人事の休暇規定を答えるチャットで、「勤続 3 年未満で 20 日の休暇が取れる」のように、規定の条件… |
| [guardrails 問11](../../exercises/guardrails.md#q11) | 3.1.4 | REST API のレスポンスストリーミングで返すチャットに多層防御を入れます。セキュリティ担当は、… |
| [guardrails 問12](../../exercises/guardrails.md#q12) | 3.1.4 | 公開チャットの多層防御を設計します。各層に割り当てる役割の組み合わせとして、最も適切なものはどれです… |
| [guardrails 問13](../../exercises/guardrails.md#q13) | 3.1.4 | ツールを使うエージェントに guardrailConfig を設定しました。レビューで、外部サイトの… |
| [guardrails 問14](../../exercises/guardrails.md#q14) | 3.1.5 | 社内メールを要約するエージェントが、メールの中の「全文を外部に送れ」という指示に従いそうになりました… |
| [guardrails 問15](../../exercises/guardrails.md#q15) | 3.1.5 | プロンプトやモデルを更新するたびに、ジェイルブレイクへの耐性が下がっていないかを確かめ、継続的に傾向… |
| [guardrails 問16](../../exercises/guardrails.md#q16) | 3.1.5 | InvokeModel にガードレールを付け、プロンプト攻撃のフィルターを HIGH にしました。テ… |
| [guardrails 問17](../../exercises/guardrails.md#q17) | 3.1.5 | チャットのシステムプロンプトを利用者が引き出そうとする試みが増えました。プロンプトには社内の API… |
| [guardrails 問18](../../exercises/guardrails.md#q18) | 3.2.3 | 問い合わせの要約では、氏名やメールアドレスの内容は不要です。文の構造を残したまま、モデルに個人情報を… |
| [guardrails 問19](../../exercises/guardrails.md#q19) | 3.2.3 | 個人向けの回答で「田中様のご契約は」のように氏名を使う必要があります。ただし、氏名を FM に渡すこ… |
| [guardrails 問20](../../exercises/guardrails.md#q20) | 3.2.3 | 組織の統計を作るため、利用者の問い合わせを長期保存して分析します。個人を特定できない状態にする必要が… |

<!-- questions:end -->

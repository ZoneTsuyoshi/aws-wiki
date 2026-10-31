# 分野3: ガバナンスと規制

統治の体制、規制のリスク、データの保護で要求すべきこと、リスク分類を問います。実装ではなく、何を要求し、誰に任せるかを判断します。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [3.2.1](../../domain3.md#skill-3-2-1) | 部門横断の統治体制 |
| [3.2.2](../../domain3.md#skill-3-2-2) | 規制上のリスク |
| [3.2.3](../../domain3.md#skill-3-2-3) | アクセス制御とデータセキュリティ |
| [3.2.4](../../domain3.md#skill-3-2-4) | リスク分類の枠組み |

## 学習の順番 {#study-order}

1. [役割と責任](../../../../services/ai-fundamentals.md#governance-roles): 役割の一覧と、1 人の責任者を決める理由を確認します。
2. [標準と規制](../../../../services/ai-fundamentals.md#standards): GDPR、HIPAA、EU AI 法、NIST AI RMF の位置づけを区別します。
3. [AWS Artifact](../../../../services/cloud-foundations.md#artifact): AWS の文書の入手先と、自社の順守との違いを確認します。
4. [責任共有モデル](../../../../services/ai-fundamentals.md#shared-responsibility)と [Scoping Matrix](../../../../services/ai-fundamentals.md#scoping-matrix): 利用の形で責任がどう変わるかを押さえます。
5. [入出力は学習に使われるか](../../../../services/ai.md#training-use): Bedrock のデータの扱いを確認します。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| Scoping Matrix | 1 消費者向け、2 企業向け、3 事前学習済み、4 ファインチューニング、5 自社学習 | 番号が大きいほど自社の責任が大きい |
| EU AI 法 | 許容できない、高、透明性（Transparency risk）、最小 | 用途で義務が変わる |
| NIST AI RMF | Govern、Map、Measure、Manage | 法律ではなく指針 |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 統治の委員会を作る | 事業、法務、コンプライアンス、セキュリティ、データの責任者 |
| 誰も責任を取らない | ユースケースごとに 1 人の責任者 |
| 規制への対応を始める | AI を使っている業務の一覧から |
| ベンダーの AI で問題が起きた | 自社の責任は残る |
| AWS 基盤の SOC レポートが必要 | AWS Artifact |
| RAG で機密文書が見える恐れがある | 元の文書の権限が回答にも反映されること |
| Bedrock を API で使い、RAG を組む | スコープ 3 |
| 採用の履歴書の選別、信用スコアリング | EU AI 法の高リスクの例 |
| 用途が変わった | リスク分類を見直す |

## 引っかかりやすい点 {#traps}

- AWS の監査レポートは、自社の AI の利用の順守を示しません。
- Bedrock の入出力は基盤モデルの改善に使われず、提供者とも共有されません。学習に使わないことと保持しないことは別です。
- 全案件に同じ審査を課すと、低リスクが止まり、高リスクへの目配りが薄くなります。
- 権限の設定そのものは技術チームが行います。要求するのは最小権限と記録です。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [ai-governance 問1](../../exercises/ai-governance.md#q1) | 3.2.1 | 全社の AI の統治の委員会を作ります。構成として最も適切なものはどれですか。 |
| [ai-governance 問2](../../exercises/ai-governance.md#q2) | 3.2.1 | 委員会を作りましたが、問題が起きると「委員会で決めたこと」として誰も責任を取りません。最も適切な改善… |
| [ai-governance 問3](../../exercises/ai-governance.md#q3) | 3.2.1 | 学習データの品質とアクセスの承認について、責任を持つ役割はどれですか。 |
| [ai-governance 問4](../../exercises/ai-governance.md#q4) | 3.2.1 | 役割と責任の組み合わせのうち、正しいものはどれですか。（2つ選択） |
| [ai-governance 問5](../../exercises/ai-governance.md#q5) | 3.2.2 | AI の規制への対応を始めます。最初に行うべきことはどれですか。 |
| [ai-governance 問6](../../exercises/ai-governance.md#q6) | 3.2.2 | 第三者の AI を顧客対応に使っている企業が、差別的な回答で苦情を受けました。社内で「ベンダーの A… |
| [ai-governance 問7](../../exercises/ai-governance.md#q7) | 3.2.2 | 監査人から、利用している AWS の基盤についての ISO や SOC のレポートを求められました。… |
| [ai-governance 問8](../../exercises/ai-governance.md#q8) | 3.2.2 | 枠組みの説明として正しいものはどれですか。（2つ選択） |
| [ai-governance 問9](../../exercises/ai-governance.md#q9) | 3.2.2 | 日本の企業が、社内の AI の採用支援ツールを EU の拠点にも展開します。規制の面で最も適切な対応… |
| [ai-governance 問10](../../exercises/ai-governance.md#q10) | 3.2.3 | 全社の文書を検索する RAG を導入すると、人事の機密文書の内容が一般の社員の回答に出る恐れがありま… |
| [ai-governance 問11](../../exercises/ai-governance.md#q11) | 3.2.3 | Amazon Bedrock のプロンプトと出力の扱いについて、正しい説明はどれですか。 |
| [ai-governance 問12](../../exercises/ai-governance.md#q12) | 3.2.3 | Amazon Bedrock を使う場合の責任共有モデルで、利用者の責任はどれですか。（2つ選択） |
| [ai-governance 問13](../../exercises/ai-governance.md#q13) | 3.2.3 | 自社のアプリから、Amazon Bedrock の基盤モデルを API で呼び、自社の文書で RAG… |
| [ai-governance 問14](../../exercises/ai-governance.md#q14) | 3.2.3 | Scoping Matrix のスコープについて、自社の責任が最も小さい形から大きい形へ正しく並べた… |
| [ai-governance 問15](../../exercises/ai-governance.md#q15) | 3.2.3 | 顧客情報を扱うエージェントの導入にあたり、経営層が要求すべきセキュリティの方針として最も適切なものは… |
| [ai-governance 問16](../../exercises/ai-governance.md#q16) | 3.2.4 | 審査の人員が限られる中で、次の案件の中から最も厳しい審査を行うべきものはどれですか。 |
| [ai-governance 問17](../../exercises/ai-governance.md#q17) | 3.2.4 | すべての AI 案件に同じ重い審査を課しています。この運用の問題点として最も適切なものはどれですか。 |
| [ai-governance 問18](../../exercises/ai-governance.md#q18) | 3.2.4 | EU AI 法のリスク分類で、履歴書を選別して採用に使う AI、融資の審査のための信用スコアリングは… |
| [ai-governance 問19](../../exercises/ai-governance.md#q19) | 3.2.4 | 社内の文書要約として低リスクに分類された AI を、顧客の与信の判断の補助にも使うことになりました。… |

<!-- questions:end -->

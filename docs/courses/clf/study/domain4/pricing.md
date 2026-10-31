# 分野4: 料金モデル

負荷の性質から購入オプションを選び、データ転送とストレージの料金の考え方を問います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [コンピューティングの購入オプション](../../domain4.md#t4-1-compute-options) | オプションの使い分け |
| [リザーブドインスタンスの柔軟性](../../domain4.md#t4-1-ri-flexibility) | スタンダードとコンバーティブル、リージョナルとゾーナル |
| [Organizations での RI の動き](../../domain4.md#t4-1-ri-organizations) | 割引の共有 |
| [データ転送の費用](../../domain4.md#t4-1-data-transfer) | 受信と送信 |
| [ストレージの料金](../../domain4.md#t4-1-storage) | 最低保存期間と取り出し料 |

## 学習の順番 {#study-order}

1. [購入オプション](../../../../services/cost-management.md#purchase-options)と[向いているものの選び方](../../../../services/cost-management.md#purchase-choice): 確約と中断の有無で整理します。
2. [Savings Plans](../../../../services/cost-management.md#savings-plans)と[Reserved Instances](../../../../services/cost-management.md#reserved-instances): 柔軟性の違いを覚えます。
3. [一括請求](../../../../services/cost-management.md#consolidated-billing): 組織での割引の共有を確認します。
4. [データ転送の費用](../../../../services/cost-management.md#data-transfer): 通信の方向と場所で覚えます。
5. [S3 のストレージ費用](../../../../services/cost-management.md#s3-cost)と[比較](../../../../services/storage.md#comparison): 保存料と課金の基準を確認します。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| スポット | 最大 90% | 中断あり |
| EC2 Instance Savings Plans、スタンダード RI | 最大 72% | 構成の確約が必要 |
| Compute Savings Plans | 最大 66% | ファミリーやリージョンを問わない |
| Standard-IA、One Zone-IA の最低保存期間 | 30 日 | |
| Glacier Instant、Flexible の最低保存期間 | 90 日 | |
| Glacier Deep Archive の最低保存期間 | 180 日 | |
| インターネットへの送信の無料枠 | 月 100 GB | 全サービスの合計 |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 中断してよいバッチ | スポット |
| 短期で予測できない | オンデマンド |
| 定常で構成が変わる可能性がある | Savings Plans かコンバーティブル RI |
| 特定の AZ に容量を確保する | Capacity Reservations |
| 物理のコア単位で BYOL | Dedicated Hosts |
| 不要な RI を売る | スタンダード RI |
| NAT ゲートウェイの S3 向けの費用を減らす | ゲートウェイエンドポイント |

## 引っかかりやすい点 {#traps}

- Savings Plans と RI は割引で、容量の確保はしません。ゾーナル RI は例外です。
- コンバーティブル RI はマーケットプレイスで販売できません。
- 最低保存期間より前に削除しても、その期間分の料金がかかります。
- EBS は確保した容量などで課金され、使っていなくても料金がかかります。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [pricing 問1](../../exercises/pricing.md#q1) | コンピューティングの購入オプション | 毎晩のバッチ処理は、途中で止まっても再実行できます。最も安い購入オプションはどれですか。 |
| [pricing 問2](../../exercises/pricing.md#q2) | コンピューティングの購入オプション | 3 年間動き続ける業務システムの費用を減らします。将来インスタンスファミリーやリージョンを変える可能… |
| [pricing 問3](../../exercises/pricing.md#q3) | コンピューティングの購入オプション | 期間が 2 か月で、負荷の予測ができない検証です。中断は避けたいです。最も適切なオプションはどれです… |
| [pricing 問4](../../exercises/pricing.md#q4) | コンピューティングの購入オプション | 特定の AZ で、確実にインスタンスを起動できる容量を確保したいと考えています。1 年の確約は不要で… |
| [pricing 問5](../../exercises/pricing.md#q5) | コンピューティングの購入オプション | EC2 の購入オプションの説明として正しいものはどれですか。（2つ選択） |
| [pricing 問6](../../exercises/pricing.md#q6) | リザーブドインスタンスの柔軟性 | 1 年の RI を購入します。途中でインスタンスファミリーを変更する可能性があります。最も適切な R… |
| [pricing 問7](../../exercises/pricing.md#q7) | リザーブドインスタンスの柔軟性 | 不要になった RI をマーケットプレイスで販売できるものはどれですか。 |
| [pricing 問8](../../exercises/pricing.md#q8) | リザーブドインスタンスの柔軟性 | リージョナル RI とゾーナル RI の説明として正しいものはどれですか。 |
| [pricing 問9](../../exercises/pricing.md#q9) | リザーブドインスタンスの柔軟性 | スタンダード RI とコンバーティブル RI の違いの説明として正しいものはどれですか。（2つ選択） |
| [pricing 問10](../../exercises/pricing.md#q10) | Organizations での RI の動き | 組織のアカウント A が購入した RI のうち、使っていない分があります。アカウント B に条件の合… |
| [pricing 問11](../../exercises/pricing.md#q11) | Organizations での RI の動き | 組織の RI の割引の共有を制御できるのはどれですか。 |
| [pricing 問12](../../exercises/pricing.md#q12) | Organizations での RI の動き | ある部門のアカウントだけ RI の割引を受けないようにしたいと考えています。最も適切な方法はどれです… |
| [pricing 問13](../../exercises/pricing.md#q13) | データ転送の費用 | AWS のデータ転送料金の基本の説明として正しいものはどれですか。 |
| [pricing 問14](../../exercises/pricing.md#q14) | データ転送の費用 | データ転送の料金の説明として正しいものはどれですか。（2つ選択） |
| [pricing 問15](../../exercises/pricing.md#q15) | データ転送の費用 | プライベートサブネットから同じリージョンの S3 へ大量に通信し、NAT ゲートウェイの費用が大きく… |
| [pricing 問16](../../exercises/pricing.md#q16) | ストレージの料金 | S3 Glacier Deep Archive の最低保存期間はどれですか。 |
| [pricing 問17](../../exercises/pricing.md#q17) | ストレージの料金 | 1 週間で削除するデータを S3 Glacier Flexible Retrieval に保存しまし… |
| [pricing 問18](../../exercises/pricing.md#q18) | ストレージの料金 | ストレージの課金の説明として正しいものはどれですか。（2つ選択） |
| [pricing 問19](../../exercises/pricing.md#q19) | ストレージの料金 | アクセスが少ないクラスの料金の特徴として正しいものはどれですか。 |

<!-- questions:end -->

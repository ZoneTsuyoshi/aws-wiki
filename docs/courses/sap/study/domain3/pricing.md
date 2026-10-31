# 分野3: 料金モデル

使い方の形から購入オプションと構成を選び、実績のメトリクスで規模を合わせる判断を問います。割引と容量を分けて考えるのが出発点です。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [3.1.1](../../domain3.md#skill-3-1-1) | 使用パターンに応じた購入オプション |
| [3.1.2](../../domain3.md#skill-3-1-2) | 要件に合うコスト最適化のアーキテクチャ |
| [3.1.3](../../domain3.md#skill-3-1-3) | 性能メトリクスに基づく適正化とスケーリング |
| [3.1.4](../../domain3.md#skill-3-1-4) | AI と ML のワークロードのコスト最適化 |

## 学習の順番 {#study-order}

1. [購入オプション](../../../../services/cost-management.md#purchase-options): 割引の上限、確約、中断、容量の確保を表で比べます。
2. [Savings Plans](../../../../services/cost-management.md#savings-plans)と [Reserved Instances](../../../../services/cost-management.md#reserved-instances): 種類ごとの適用先と、RI、Savings Plans の適用順を覚えます。
3. [スポットインスタンス](../../../../services/cost-management.md#spot): 中断の通知と、複数のタイプを指定する理由を押さえます。
4. [Standard と Express](../../../../services/step-functions.md#standard-express): 課金の違いと、Express で使えないパターンを確認します。
5. [メモリと CPU の最適化](../../../../services/lambda.md#memory-tuning)と[アーキテクチャ](../../../../services/lambda.md#architecture): メモリと時間の関係、`arm64` の条件をつかみます。
6. [Compute Optimizer と適正サイズ](../../../../services/cost-management.md#compute-optimizer)と[推奨を出すサービスの違い](../../../../services/cost-management.md#recommendation-tools): どの推奨をどこで見るかを整理します。
7. [キャパシティプロバイダー](../../../../services/containers.md#capacity-providers): `base` と `weight` の計算を手で解けるようにします。
8. [Amazon Bedrock の料金](../../../../services/cost-management.md#bedrock-pricing)と[キャッシュの種類](../../../../services/genai-apps.md#caching): ティアとキャッシュを、処理の急ぎ方と入力の形で選びます。
9. [SageMaker の最適化](../../../../services/sagemaker.md#optimization): 使われないエンドポイントの費用を減らす方法を確認します。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| Compute Savings Plans | 最大 66% | ファミリー、リージョン、Fargate、Lambda をまたぐ |
| EC2 Instance Savings Plans | 最大 72% | 選んだリージョンとファミリーの EC2 |
| Database Savings Plans | 最大 35% | エンジンとリージョンをまたぐ。1 年、前払いなし |
| SageMaker AI Savings Plans | 最大 64% | ファミリー、リージョン、コンポーネントをまたぐ |
| スポットの割引、通知 | 最大 90%、2 分前 | Fargate Spot も 2 分前の警告 |
| Express の最大実行時間 | 5 分 | Standard は 1 年 |
| Bedrock Reserved の最小 | 入力 100,000 TPM、出力 10,000 TPM | アカウントチームに連絡 |
| グローバル推論の割引 | 約 10% | モデルによる。地理的な制約がないとき |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| リージョンやファミリーが変わる常時稼働 | Compute Savings Plans を最低の利用量に合わせる |
| DR 先で必ず起動できることが要件 | Capacity Reservation。割引は Savings Plans と組み合わせる |
| 確約を急ぐよう求められたが、過剰な構成が残っている | 適正化してから確約する |
| 大量で短く、冪等なワークフロー | Express を新しく作る。タイプは変更できない |
| 24 時間一定の高い負荷の Lambda | Fargate と Compute Savings Plans を比べる |
| 既知の時間帯と読めない変動の両方がある | スケジュールとターゲット追跡を併用する |
| 応答を優先したいが常時の予約は避けたい | Bedrock の Priority ティア |
| 夜間にまとめて処理し、翌朝でよい | バッチ推論か Flex ティア |
| 大きな入力を断続的に処理し、待てる | SageMaker AI の非同期推論。0 台まで縮小 |

## 引っかかりやすい点 {#traps}

- Savings Plans もリージョナル RI も、容量を確保しません。
- 適用の順序は、RI、EC2 Instance Savings Plans、Compute Savings Plans です。
- Savings Plans は購入後に確約を変更できません。
- Express は `.sync` と `.waitForTaskToken` に対応しません。
- Fargate Spot の容量が不足しても、通常の Fargate へ自動で切り替わりません。
- Lambda のメモリを下げると CPU も減ります。実行時間が延びて、費用が増えることもあります。
- プロンプトキャッシュは入力の前半の一致を使います。固定の内容を先に置きます。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [pricing 問1](../../exercises/pricing.md#q1) | 3.1.1 | ある製造業の会社は、東京リージョンの EC2 で基幹の API を動かしています。オンデマンド換算の… |
| [pricing 問2](../../exercises/pricing.md#q2) | 3.1.1 | ある金融機関は、大阪リージョンを DR 先としています。東京の障害時には、大阪の特定の AZ で r… |
| [pricing 問3](../../exercises/pricing.md#q3) | 3.1.1 | ある動画サービスには 2 つのワークロードがあります。1 つは動画の変換で、ジョブは数分で終わり、失… |
| [pricing 問4](../../exercises/pricing.md#q4) | 3.1.1 | ある会社の組織には、EC2 のリージョナル RI、EC2 Instance Savings Plan… |
| [pricing 問5](../../exercises/pricing.md#q5) | 3.1.2 | ある IoT 事業者は、機器のイベントを正規化する Step Functions の Standar… |
| [pricing 問6](../../exercises/pricing.md#q6) | 3.1.2 | あるチームは、数百の Lambda 関数の価格性能を改善したいと考えています。多くは Python … |
| [pricing 問7](../../exercises/pricing.md#q7) | 3.1.2 | ある会社の API は Lambda で動いており、24 時間ほぼ一定の高い同時実行が続いています。… |
| [pricing 問8](../../exercises/pricing.md#q8) | 3.1.3 | ある会社は、オンプレミスから移行した EC2 を半年運用しました。CPU の平均使用率は 12% で… |
| [pricing 問9](../../exercises/pricing.md#q9) | 3.1.3 | ある ECS サービスは、次のキャパシティプロバイダー戦略で動いています。desiredCount … |
| [pricing 問10](../../exercises/pricing.md#q10) | 3.1.3 | ある社内システムの利用は、平日の 8 時から 20 時に集中し、夜間と休日はほとんどありません。始業… |
| [pricing 問11](../../exercises/pricing.md#q11) | 3.1.4 | ある会社は、顧客向けのチャットを Bedrock のオンデマンドで動かしています。キャンペーンの期間… |
| [pricing 問12](../../exercises/pricing.md#q12) | 3.1.4 | ある自治体は、公開情報だけを答える FAQ ボットを Bedrock で運用しています。毎回同じ長い… |
| [pricing 問13](../../exercises/pricing.md#q13) | 3.1.4 | ある研究機関は、自社で作ったモデルを SageMaker AI のリアルタイムエンドポイントで動かし… |
| [pricing 問14](../../exercises/pricing.md#q14) | 3.1.4 | あるコールセンターは、問い合わせの分類と回答の作成を、同じ高性能なモデルで処理しています。分類が件数… |

<!-- questions:end -->

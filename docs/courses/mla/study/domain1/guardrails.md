# 分野1: 機密データと学習データの検査

データがどの段階にあるかでマスクの手段を選びます。FM の学習データの検査も含みます。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [1.2.8](../../domain1.md#skill-1-2-8) | マスキング、秘匿化、匿名化 |
| [1.3.6](../../domain1.md#skill-1-3-6) | AI の学習データの完全性の検証 |

## 学習の順番 {#study-order}

1. [Macie](../../../../services/threat-detection.md#macie): 発見と報告の役割を確認します。
2. [データの保護](../../../../services/genai-apps.md#data-protection)と[サニタイズとマスキング](../../../../services/secrets.md#sanitization-masking): 段階ごとの手段を比べます。
3. [Comprehend](../../../../services/ai-managed-services.md#comprehend)と [Guardrails のフィルター](../../../../services/ai.md#guardrail-filters): 日本語の扱いの違いを覚えます。
4. [データの準備](../../../../services/genai-apps.md#fine-tuning-data)と [ApplyGuardrail](../../../../services/ai.md#apply-guardrail): 学習データの検査の方法を押さえます。

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| S3 のどこに個人情報があるか知りたい | Macie |
| ETL の中で検出して置換する | Glue の Detect PII |
| 元の値に戻す必要がある | 決定的または確率的な暗号化 |
| 結合のキーに使いたいが値を隠す | ハッシュ、決定的な暗号化 |
| 日本語の PII をマスクする | Guardrails の機密情報フィルター、正規表現 |
| FM を呼ばずに学習データを検査する | `ApplyGuardrail` |

## 引っかかりやすい点 {#traps}

- Macie はマスクをしません。
- Comprehend の PII は英語とスペイン語が対象です。日本語には使えません。
- FM は誤りも有害な内容もそのまま学習します。出所の管理と人の確認を組み合わせます。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [guardrails 問1](../../exercises/guardrails.md#q1) | 1.2.8 | S3 のデータレイクのどこに個人情報があるかを発見して報告します。データの変更はしません。どのサービ… |
| [guardrails 問2](../../exercises/guardrails.md#q2) | 1.2.8 | Glue の ETL で氏名の列をハッシュに置き換え、結合のキーとして使います。元の値は復元しません… |
| [guardrails 問3](../../exercises/guardrails.md#q3) | 1.2.8 | DataBrew で個人情報を保護します。後で権限のある担当者が元の値に戻す必要があります。適切な手… |
| [guardrails 問4](../../exercises/guardrails.md#q4) | 1.2.8 | 日本語の問い合わせ履歴から氏名と電話番号をマスクします。Comprehend の PII の非同期ジ… |
| [guardrails 問5](../../exercises/guardrails.md#q5) | 1.3.6 | FM のファインチューニングに使う問い合わせの回答例を、FM を呼ばずに有害な内容で検査します。どの… |
| [guardrails 問6](../../exercises/guardrails.md#q6) | 1.3.6 | 外部の委託先から FM の学習データを受け取ります。悪意のあるデータが混ざるポイズニングを防ぐ対応と… |
| [guardrails 問7](../../exercises/guardrails.md#q7) | 1.3.6 | FM の学習データの代表性を確かめます。何を確認しますか。 |

<!-- questions:end -->

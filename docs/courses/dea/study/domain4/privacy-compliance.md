# 分野4: プライバシーとコンプライアンス

個人情報の特定、リージョンの制限、設定の変更の確認、データ主権を問います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [4.5.2](../../domain4.md#skill-4-5-2) | 個人情報の特定 |
| [4.5.3](../../domain4.md#skill-4-5-3) | 許可しないリージョンへのバックアップと複製の防止 |
| [4.5.4](../../domain4.md#skill-4-5-4) | アカウントの設定変更の確認 |
| [4.5.5](../../domain4.md#skill-4-5-5) | データ主権の維持 |

## 学習の順番 {#study-order}

1. [Macie の検出](../../../../services/threat-detection.md#macie-discovery): 自動検出とジョブを区別します。
2. [SCP](../../../../services/governance.md#scp): 対象外の範囲を覚えます。
3. [Config](../../../../services/governance.md#config): 記録と評価を確認します。
4. [リージョン](../../../../services/cloud-foundations.md#regions): データの置き場を確認します。
5. [AWS Artifact](../../../../services/threat-detection.md#artifact): 準拠の証明を確認します。

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 全体の見通し | Macie の自動検出 |
| 機密データを検出して隠す | Macie、EventBridge、Lambda、LF タグ |
| リージョンの外での作成を防ぐ | SCP の `aws:RequestedRegion` |
| 公開のバケットを直す | Config ルールと修復アクション |
| 監査レポートを入手する | AWS Artifact |

## 引っかかりやすい点 {#traps}

- SCP は管理アカウントとサービスリンクロールの操作を制限できません。
- Bedrock の推論プロファイルは他のリージョンで処理することがあります。
- Config は検出の仕組みで、事前の拒否はしません。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [privacy-compliance 問1](../../exercises/privacy-compliance.md#q1) | 4.5.2 | S3 のデータレイク全体で、どこに個人情報がありそうかを毎日の検査で見通します。何を使いますか。 |
| [privacy-compliance 問2](../../exercises/privacy-compliance.md#q2) | 4.5.2 | Macie の検出結果に基づいて、自動で該当のテーブルをアナリストから隠します。どの流れですか。 |
| [privacy-compliance 問3](../../exercises/privacy-compliance.md#q3) | 4.5.2 | Macie が一部のバケットを検査できません。確認すべきものはどれですか。（2つ選択） |
| [privacy-compliance 問4](../../exercises/privacy-compliance.md#q4) | 4.5.3 | 規制で東京リージョンの外にデータを置けません。全アカウントで他のリージョンへの作成を防ぎます。何を使… |
| [privacy-compliance 問5](../../exercises/privacy-compliance.md#q5) | 4.5.3 | aws:RequestedRegion で他のリージョンを拒否する SCP を適用すると、IAM や… |
| [privacy-compliance 問6](../../exercises/privacy-compliance.md#q6) | 4.5.3 | 許可しないリージョンへのバックアップと複製を防ぐ確認で正しいものはどれですか。（2つ選択） |
| [privacy-compliance 問7](../../exercises/privacy-compliance.md#q7) | 4.5.4 | S3 バケットの設定がいつどう変わったかの履歴を確認し、基準に合うかを評価します。どのサービスですか… |
| [privacy-compliance 問8](../../exercises/privacy-compliance.md#q8) | 4.5.4 | S3 バケットが公開になったら検出して、自動で元に戻します。どの組み合わせですか。 |
| [privacy-compliance 問9](../../exercises/privacy-compliance.md#q9) | 4.5.4 | 複数のアカウントの設定の変更を集約し、誰が変えたかまで調べます。正しい組み合わせはどれですか。 |
| [privacy-compliance 問10](../../exercises/privacy-compliance.md#q10) | 4.5.5 | データを日本に留める要件です。データ主権の点で、有効にする前に確認すべき機能はどれですか。（2つ選択… |
| [privacy-compliance 問11](../../exercises/privacy-compliance.md#q11) | 4.5.5 | Bedrock で推論プロファイルを使います。データ主権の点で注意することはどれですか。 |
| [privacy-compliance 問12](../../exercises/privacy-compliance.md#q12) | 4.5.5 | 監査人に、AWS の準拠のレポートを提出します。どこで入手しますか。 |

<!-- questions:end -->

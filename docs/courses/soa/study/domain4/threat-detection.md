# 分野4: データ分類と検出結果

分類の実装と、検出結果の修復の流れを問います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [4.2.1](../../domain4.md#skill-4-2-1) | データ分類 |
| [4.2.5](../../domain4.md#skill-4-2-5) | 検出結果のレポートと修復 |

## 学習の順番 {#study-order}

1. [データ分類](../../../../services/secrets.md#data-classification)と[タグポリシー](../../../../services/governance.md#tag-policies): 分類をタグで示します。
2. [Macie](../../../../services/threat-detection.md#macie)と[識別子と許可リスト](../../../../services/threat-detection.md#macie-identifiers): 検出の方法を確認します。
3. [データ保護ポリシー](../../../../services/observability.md#logs-data-protection): ログのマスクを確認します。
4. [選び方の比較](../../../../services/threat-detection.md#choosing)と[製品の現在の形](../../../../services/threat-detection.md#security-hub-products): サービスの違いと製品の名前を確認します。
5. [イベント連携とエクスポート](../../../../services/threat-detection.md#guardduty-events)、[抑制ルールとリスト](../../../../services/threat-detection.md#guardduty-suppression)と[自動化](../../../../services/threat-detection.md#security-hub-automation): 修復と抑制を確認します。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| GuardDuty の更新の通知 | 既定 6 時間 | 15 分か 1 時間へ変更（管理者のみ） |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 社内の形式の値を検出する | カスタムデータ識別子 |
| Macie が検査できない | キーの権限とバケットポリシー |
| タグの値を統一する | タグポリシー |
| 脅威、脆弱性、機密データ | GuardDuty、Inspector、Macie |
| 全アカウントの結果で修復する | 委任管理者の EventBridge ルール |
| 重要度を自動で変える | Security Hub の自動化ルール |

## 引っかかりやすい点 {#traps}

- 抑制ルールは結果を隠すだけです。
- 古い教材の Security Hub は Security Hub CSPM を指します。
- 分類の基準を決めるのは範囲外です。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [threat-detection 問1](../../exercises/threat-detection.md#q1) | 4.2.1 | S3 に保存された社員番号 EMP- で始まる 6 桁の値を見つけたいです。どの機能を使いますか。 |
| [threat-detection 問2](../../exercises/threat-detection.md#q2) | 4.2.1 | Macie が一部のオブジェクトを検査できません。KMS のカスタマー管理キーで暗号化されています。… |
| [threat-detection 問3](../../exercises/threat-detection.md#q3) | 4.2.1 | DataClassification のタグの値を組織で統一し、タグのないリソースも見つけたいです。… |
| [threat-detection 問4](../../exercises/threat-detection.md#q4) | 4.2.1 | CloudWatch Logs のログに、メールアドレスやカード番号が混ざることがあります。ログの中… |
| [threat-detection 問5](../../exercises/threat-detection.md#q5) | 4.2.1 | DataClassification=confidential のタグが付いたリソースは、同じタグの… |
| [threat-detection 問6](../../exercises/threat-detection.md#q6) | 4.2.5 | 次の検出のサービスと対象の組み合わせとして正しいものを選んでください。（2つ選択） |
| [threat-detection 問7](../../exercises/threat-detection.md#q7) | 4.2.5 | GuardDuty が CryptoCurrency:EC2/BitcoinTool.B!DNS を… |
| [threat-detection 問8](../../exercises/threat-detection.md#q8) | 4.2.5 | 組織の全アカウントの GuardDuty の結果を受けて自動で修復します。どのアカウントにルールを作… |
| [threat-detection 問9](../../exercises/threat-detection.md#q9) | 4.2.5 | 検証用のスキャナーで GuardDuty の既知の誤検知が毎日出ます。修復の対象にしたくありません。… |
| [threat-detection 問10](../../exercises/threat-detection.md#q10) | 4.2.5 | Security Hub CSPM の検出結果の重要度を、開発環境のアカウントだけ自動で下げたいです… |
| [threat-detection 問11](../../exercises/threat-detection.md#q11) | 4.2.5 | 人の判断の後に修復を実行したい場面と、結果を隠したい場面の説明で正しいものを選んでください。（2つ選… |
| [threat-detection 問12](../../exercises/threat-detection.md#q12) | 4.2.5 | GuardDuty の結果の更新の通知が遅いので、早く受け取りたいです。既定は 6 時間です。どう変… |
| [threat-detection 問13](../../exercises/threat-detection.md#q13) | 4.2.5 | 製品の名前について正しい説明はどれですか。 |
| [threat-detection 問14](../../exercises/threat-detection.md#q14) | 4.2.5 | 開発中のアプリの設計とコードのレビュー、オンデマンドの侵入テストを行いたいです。どのサービスを使いま… |

<!-- questions:end -->

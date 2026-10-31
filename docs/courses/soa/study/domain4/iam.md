# 分野4: IAM とアクセスの調査

権限の評価と、拒否されたときの調べ方を問います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [4.1.1](../../domain4.md#skill-4-1-1) | IAM の機能 |
| [4.1.2](../../domain4.md#skill-4-1-2) | アクセスの問題の調査と監査 |

## 学習の順番 {#study-order}

1. [ポリシー評価](../../../../services/iam.md#policy-evaluation)と[アイデンティティベースとリソースベース](../../../../services/iam.md#identity-vs-resource): 拒否の優先と、許可の種類を確認します。
2. [クロスアカウントアクセス](../../../../services/iam.md#cross-account)と[条件とアクセス制御](../../../../services/iam.md#conditions): アカウントをまたぐ条件を確認します。
3. [アクセス拒否メッセージ](../../../../services/iam.md#access-denied-messages)と[DecodeAuthorizationMessage](../../../../services/iam.md#decode-authorization): メッセージの読み方を確認します。
4. [ポリシーシミュレーター](../../../../services/iam.md#policy-simulator)と[IAM Access Analyzer](../../../../services/identity-directory.md#access-analyzer): ツールの役割を区別します。
5. [CloudTrail の調査](../../../../services/threat-detection.md#investigate-cloudtrail)と[Config と CloudTrail の違い](../../../../services/governance.md#config-vs-cloudtrail): 履歴の調べ方を確認します。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| カスタムの最小の長さ | 6〜128 文字 | 既定は 8 文字以上 |
| 有効期限 | 1〜1,095 日 | すぐに効く |
| 再利用の禁止 | 過去 1〜24 個 | ルートは対象外 |
| CloudTrail のイベント履歴 | 90 日 | 配信は平均で約 5 分遅れる |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| MFA を要求する | `aws:MultiFactorAuthPresent` |
| 別アカウントのバケットを読む | 両側で許可する |
| 拒否のメッセージに SCP | IAM を足しても直らない |
| エンコードされたメッセージを読む | `DecodeAuthorizationMessage` |
| 未使用の権限を探す | Access Analyzer の未使用アクセス |

## 引っかかりやすい点 {#traps}

- ロックアウトは設定できません。MFA を組み合わせます。
- シミュレーターは RCP に対応していません。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [iam 問1](../../exercises/iam.md#q1) | 4.1.1 | aws:MultiFactorAuthPresent が false の要求を BoolIfExis… |
| [iam 問2](../../exercises/iam.md#q2) | 4.1.1 | アカウント A の IAM ロールが、アカウント B の S3 バケットを読みます。A のロールに … |
| [iam 問3](../../exercises/iam.md#q3) | 4.1.1 | 同じアカウントの IAM ユーザーに s3:* の許可が直接付いています。ユーザーが属するグループの… |
| [iam 問4](../../exercises/iam.md#q4) | 4.1.1 | EC2 のアプリケーションが S3 で AccessDenied になります。インスタンスプロファイ… |
| [iam 問5](../../exercises/iam.md#q5) | 4.1.1 | IAM のパスワードポリシーの説明として正しいものを選んでください。（2つ選択） |
| [iam 問6](../../exercises/iam.md#q6) | 4.1.1 | 社内の ID プロバイダーのアカウントで、1 つの AWS アカウントのコンソールへサインインさせた… |
| [iam 問7](../../exercises/iam.md#q7) | 4.1.2 | 管理者権限のロールでも EC2 の操作が拒否されます。拒否メッセージに service contro… |
| [iam 問8](../../exercises/iam.md#q8) | 4.1.2 | EC2 の API が Encoded authorization failure message … |
| [iam 問9](../../exercises/iam.md#q9) | 4.1.2 | 要件と調査のツールの組み合わせとして正しいものを選んでください。（2つ選択） |
| [iam 問10](../../exercises/iam.md#q10) | 4.1.2 | 90 日以上使っていないロールと権限を見つけて整理したいです。どの機能が適切ですか。 |
| [iam 問11](../../exercises/iam.md#q11) | 4.1.2 | 先週の AccessDenied のイベントを主体と操作で調べたいです。CloudTrail の説明… |
| [iam 問12](../../exercises/iam.md#q12) | 4.1.2 | セキュリティグループのルールがいつ、どう変わったかの時系列を見たいです。また、変更した人も特定します… |

<!-- questions:end -->

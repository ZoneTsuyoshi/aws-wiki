# 分野4: AWS Config

判定と修復の違い、修復の設計を問います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [Config ルール](../../domain4.md#t4-2-config-rules) | AWS Config ルール |
| [Config の修復](../../domain4.md#t4-3-config-remediation) | Config ルールによる修復 |

## 学習の順番 {#study-order}

1. [Config ルール](../../../../services/governance.md#config-rules): トリガーと評価モードを確認します。
2. [設定レコーダー](../../../../services/governance.md#config-recorder): 記録が前提であることを押さえます。
3. [修復](../../../../services/governance.md#config-remediation): 修復の設定を確認します。
4. [EventBridge による修復パターン](../../../../services/operations.md#eventbridge-remediation): 他の修復のパターンと比べます。

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 操作を止める | SCP やプロアクティブなコントロール |
| 独自の規則を評価する | カスタムルール |
| 修復が権限で失敗する | ランブックのロール |

## 引っかかりやすい点 {#traps}

- ルールは判定するだけで、操作を止めません。
- 修復が別の仕組みと競合すると、ループになります。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [config 問1](../../exercises/config.md#q1) | Config ルール | 新しい EBS ボリュームの暗号化の有無を AWS Config のマネージドルールで評価しています… |
| [config 問2](../../exercises/config.md#q2) | Config ルール | 次の要件に合うルールの設定を選びます。(1) タグの付け忘れを、リソースの変更のたびに評価する。(2… |
| [config 問3](../../exercises/config.md#q3) | Config ルール | Config のルールを有効にしたのに、すべて「評価なし」のままです。リージョンの他のアカウントでは… |
| [config 問4](../../exercises/config.md#q4) | Config の修復 | 公開された S3 バケットを自動で修復します。Config のルールで検出し、Automation … |
| [config 問5](../../exercises/config.md#q5) | Config の修復 | 公開の S3 バケットを自動で修復すると、別の仕組みが元に戻して、修復が延々と繰り返されました。適切… |
| [config 問6](../../exercises/config.md#q6) | Config の修復 | 90 日より古いアクセスキーを持つユーザーの検出は access-keys-rotated で行って… |

<!-- questions:end -->

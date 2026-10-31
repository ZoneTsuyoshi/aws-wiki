# 分野4: Inspector

評価テンプレートの時代からの変化を問います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [Inspector](../../domain4.md#t4-2-inspector) | Inspector と評価テンプレート |

## 学習の順番 {#study-order}

1. [Inspector](../../../../services/threat-detection.md#inspector): 現在の Inspector の動きを確認します。
2. [スキャンの種類](../../../../services/threat-detection.md#inspector-scan-types): 対象の種類を押さえます。
3. [検出結果と管理](../../../../services/threat-detection.md#inspector-findings): 検出結果の扱いを確認します。

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 組織全体を継続的に検査する | 委任管理者で有効にする |
| S3 の個人情報 | Macie |

## 引っかかりやすい点 {#traps}

- 評価テンプレートは Inspector Classic の用語で、サポートは終了しました。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [threat-detection 問1](../../exercises/threat-detection.md#q1) | Inspector | 組織の EC2、ECR のイメージ、Lambda の脆弱性を継続的に確認します。担当者は過去の資料を… |
| [threat-detection 問2](../../exercises/threat-detection.md#q2) | Inspector | EC2 の Inspector で一部のインスタンスがスキャンされません。修正のパッチを適用した後、… |
| [threat-detection 問3](../../exercises/threat-detection.md#q3) | Inspector | 次の検査のうち、Inspector の範囲に含まれないものはどれですか。パイプラインとコンテナの検査… |

<!-- questions:end -->

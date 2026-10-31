# 分野4: CI/CD の脆弱性の検査

コードとイメージの脆弱性を、デプロイの前に検査して止めます。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [4.3.1](../../domain4.md#skill-4-3-1) | CI/CD でのコードとイメージの脆弱性の検査 |

## 学習の順番 {#study-order}

1. [Inspector](../../../../services/threat-detection.md#inspector)と [ECR のスキャン](../../../../services/threat-detection.md#inspector-ecr): 拡張スキャンと EventBridge の連携を確認します。
2. [コードのスキャン](../../../../services/threat-detection.md#inspector-code)と [CodeGuru Security](../../../../services/threat-detection.md#codeguru-security): 現在の選択を覚えます。

## こう問われたらこう考える {#decisions}

| 対象 | サービス |
|---|---|
| コンテナイメージ | Inspector（ECR の拡張スキャン） |
| CI/CD でのイメージの検査 | Inspector の Scan API と SBOM Generator |
| コード | Inspector の Code Security |
| 重大な検出でデプロイを止める | CodeBuild のステップを失敗させる |

## 引っかかりやすい点 {#traps}

- CodeGuru Security は 2025-11-20 にサポートを終了しました。試験で CodeGuru が出たら、パイプラインでの静的スキャンの役割として読みます。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [cicd-iac 問10](../../exercises/cicd-iac.md#q10) | 4.3.1 | CI/CD の中でコンテナイメージの脆弱性を検査し、重大な検出があればデプロイを止めます。適切な実装… |
| [cicd-iac 問11](../../exercises/cicd-iac.md#q11) | 4.3.1 | ECR の拡張スキャンの結果をきっかけに、自動で担当者へ通知します。どの連携ですか。 |
| [cicd-iac 問12](../../exercises/cicd-iac.md#q12) | 4.3.1 | 新しいプロジェクトで学習コードの静的スキャンを導入します。CodeGuru Security を使う… |

<!-- questions:end -->

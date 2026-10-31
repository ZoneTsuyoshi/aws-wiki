# 分野2: マルチ VPC とマルチアカウント

Organizations と RAM で接続を広げる実装を問います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [Organizations と RAM](../../domain2.md#t2-1-org-ram) | Organizations と RAM（Transit Gateway、DX、VPC、Route 53） |
| [接続を広げる](../../domain2.md#t2-2-expansion) | 接続を広げる方法（Organizations、RAM） |

## 学習の順番 {#study-order}

1. [AWS Resource Access Manager](../../../../services/governance.md#ram): 組織の共有を確認します。
2. [Cloud WAN](../../../../services/network-connectivity.md#cloud-wan): タグの割り当てを押さえます。
3. [ネストされたスタックと StackSets](../../../../services/iac.md#nested-stacks-stacksets): 新しいアカウントへの展開を確認します。

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| アタッチメントが承認待ち | 所有者が承認、または自動承認 |
| OU を指定できない | 管理アカウントで組織の共有を有効に |

## 引っかかりやすい点 {#traps}

- Cloud WAN でタグの値がルールの条件と違うと、そのセグメントに関連付きません。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [multi-account 問13](../../exercises/multi-account.md#q13) | Organizations と RAM | RAM で Transit Gateway を共有しました。共有先のアカウントがアタッチメントを作り… |
| [multi-account 問14](../../exercises/multi-account.md#q14) | Organizations と RAM | RAM で Resolver ルールを OU へ共有したいと考えています。OU を指定できず、アカウ… |
| [multi-account 問15](../../exercises/multi-account.md#q15) | Organizations と RAM | ネットワークチームが、共有の仕組みを一覧にしています。リソースと仕組みの組み合わせで正しいものを選ん… |
| [multi-account 問16](../../exercises/multi-account.md#q16) | 接続を広げる | Cloud WAN でタグによる接続を運用しています。新しい VPC に segment=prod … |
| [multi-account 問17](../../exercises/multi-account.md#q17) | 接続を広げる | Control Tower で新しいアカウントを作るたびに、VPC を Transit Gatewa… |
| [multi-account 問18](../../exercises/multi-account.md#q18) | 接続を広げる | 6 リージョンで VPC を接続しています。Transit Gateway の共有を続けるか、Clo… |

<!-- questions:end -->

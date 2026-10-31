# 分野2: 責任共有モデル

具体的な作業を挙げて、AWS と利用者のどちらの担当かを問います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [モデルの全体像](../../domain2.md#t2-1-model) | クラウドのセキュリティとクラウドの中のセキュリティ |
| [利用者の責任](../../domain2.md#t2-1-customer) | データ、権限、設定 |
| [AWS の責任](../../domain2.md#t2-1-aws) | 物理施設、ハードウェア、仮想化層 |
| [共有する責任](../../domain2.md#t2-1-shared) | パッチ管理、構成管理、教育 |
| [サービスによる責任の変化](../../domain2.md#t2-1-by-service) | EC2、RDS、Lambda での違い |

## 学習の順番 {#study-order}

1. [責任共有モデル](../../../../services/cloud-foundations.md#shared-responsibility): 2 つの言葉と、担当の範囲を覚えます。
2. [サービスごとの違い](../../../../services/cloud-foundations.md#responsibility-by-service): EC2、RDS、Lambda の表を比べます。

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| データセンターの入退室、ディスクの廃棄 | AWS |
| S3 バケットの公開設定、IAM の権限 | 利用者 |
| EC2 のゲスト OS のパッチ | 利用者 |
| RDS の OS のパッチ | AWS |
| Lambda の基盤の OS | AWS |
| 自社の従業員の教育 | 利用者（AWS の従業員は AWS） |

## 引っかかりやすい点 {#traps}

- データと権限は、どのサービスでも利用者の担当です。
- RDS にしても、スキーマと SQL は利用者の担当です。
- AWS が利用者の設定を代わりに判断することはありません。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [shared-responsibility 問1](../../exercises/shared-responsibility.md#q1) | モデルの全体像 | 責任共有モデルで、AWS と利用者の担当を表す言葉の組み合わせとして正しいものはどれですか。 |
| [shared-responsibility 問2](../../exercises/shared-responsibility.md#q2) | モデルの全体像 | 責任共有モデルが分担の対象とするものはどれですか。 |
| [shared-responsibility 問3](../../exercises/shared-responsibility.md#q3) | モデルの全体像 | 責任共有モデルの理解として正しいものはどれですか。 |
| [shared-responsibility 問4](../../exercises/shared-responsibility.md#q4) | 利用者の責任 | 責任共有モデルで、利用者の責任に当たるものはどれですか。（2つ選択） |
| [shared-responsibility 問5](../../exercises/shared-responsibility.md#q5) | 利用者の責任 | S3 バケットを誤って公開にして、顧客情報が漏えいしました。責任共有モデルでは誰の責任ですか。 |
| [shared-responsibility 問6](../../exercises/shared-responsibility.md#q6) | 利用者の責任 | EC2 上のアプリで、通信を許可するポートをセキュリティグループで決める作業の担当はどれですか。 |
| [shared-responsibility 問7](../../exercises/shared-responsibility.md#q7) | AWS の責任 | 責任共有モデルで、AWS の責任に当たるものはどれですか。（2つ選択） |
| [shared-responsibility 問8](../../exercises/shared-responsibility.md#q8) | AWS の責任 | Lambda 関数を動かす基盤のサーバーのセキュリティ対策の担当はどれですか。 |
| [shared-responsibility 問9](../../exercises/shared-responsibility.md#q9) | AWS の責任 | AWS が担当する「クラウドのセキュリティ」の例として正しいものはどれですか。 |
| [shared-responsibility 問10](../../exercises/shared-responsibility.md#q10) | 共有する責任 | パッチ管理の分担として正しいものはどれですか。 |
| [shared-responsibility 問11](../../exercises/shared-responsibility.md#q11) | 共有する責任 | AWS と利用者の両方が、それぞれの層で担当する項目はどれですか。（2つ選択） |
| [shared-responsibility 問12](../../exercises/shared-responsibility.md#q12) | 共有する責任 | セキュリティの教育について、責任共有モデルに沿った説明はどれですか。 |
| [shared-responsibility 問13](../../exercises/shared-responsibility.md#q13) | サービスによる責任の変化 | EC2 にデータベースを自分で入れる構成から Amazon RDS に変えました。担当が利用者から … |
| [shared-responsibility 問14](../../exercises/shared-responsibility.md#q14) | サービスによる責任の変化 | Lambda で利用者の担当として残るものはどれですか。（2つ選択） |
| [shared-responsibility 問15](../../exercises/shared-responsibility.md#q15) | サービスによる責任の変化 | EC2、RDS、Lambda のうち、利用者がゲスト OS のパッチを担当するものはどれですか。 |
| [shared-responsibility 問16](../../exercises/shared-responsibility.md#q16) | サービスによる責任の変化 | 抽象度が高いサービスを選んだときの変化として正しいものはどれですか。 |

<!-- questions:end -->

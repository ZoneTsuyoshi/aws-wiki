# 分野4: SageMaker のガバナンス

Unified Studio の単位、プロジェクトによるアクセス管理、共有のパターンを問います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [4.1.7](../../domain4.md#skill-4-1-7) | SageMaker Unified Studio のドメイン、ドメインユニット、プロジェクト |
| [4.5.6](../../domain4.md#skill-4-5-6) | SageMaker Catalog のプロジェクトによるアクセスの管理 |
| [4.5.7](../../domain4.md#skill-4-5-7) | データガバナンスのフレームワークと共有パターン |

## 学習の順番 {#study-order}

1. [DataZone と Unified Studio](../../../../services/data-engineering.md#datazone-unified-studio): ドメイン、ドメインユニット、プロジェクトを区別します。
2. [データの共有](../../../../services/data-engineering.md#choosing-sharing): 要件と共有の方法を対応づけます。
3. [Clean Rooms](../../../../services/data-engineering.md#clean-rooms): 生データを見せない分析を確認します。
4. [マルチアカウントのパターン](../../../../services/governance.md#multi-account-patterns): 組織の型を確認します。

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 事業部ごとに権限を委任する | ドメインユニット |
| メタデータフォームを作れるプロジェクトを絞る | ドメインユニットの認可ポリシー |
| 個人ではなくチームで使う | プロジェクトのメンバーにする |
| 生データを見せず共同で分析する | Clean Rooms |
| 中央がボトルネック | データメッシュ |

## 引っかかりやすい点 {#traps}

- 権限の実体は Lake Formation や Redshift です。
- ユーザーとグループのポリシーと、プロジェクトのポリシーは別です。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [sagemaker-governance 問7](../../exercises/sagemaker-governance.md#q7) | 4.1.7 | 大きな組織で SageMaker Unified Studio を使います。事業部ごとにアセットを整… |
| [sagemaker-governance 問8](../../exercises/sagemaker-governance.md#q8) | 4.1.7 | ドメインユニットで、ユーザーとグループに割り当てるポリシーはどれですか。 |
| [sagemaker-governance 問9](../../exercises/sagemaker-governance.md#q9) | 4.1.7 | メタデータの品質を保つため、メタデータフォームを作れるプロジェクトを絞ります。どうしますか。 |
| [sagemaker-governance 問10](../../exercises/sagemaker-governance.md#q10) | 4.5.6 | SageMaker Catalog で、あるプロジェクトのアナリスト全員がアセットを読めるようにしま… |
| [sagemaker-governance 問11](../../exercises/sagemaker-governance.md#q11) | 4.5.6 | コンシューマーの申請を所有者が承認しました。実際の権限はどこで働きますか。 |
| [sagemaker-governance 問12](../../exercises/sagemaker-governance.md#q12) | 4.5.6 | 役割と動作の組み合わせとして正しいものはどれですか。（2つ選択） |
| [sagemaker-governance 問13](../../exercises/sagemaker-governance.md#q13) | 4.5.7 | 広告主と媒体社が、顧客の生データを互いに見せず、共通の顧客の数だけを集計します。何を選びますか。 |
| [sagemaker-governance 問14](../../exercises/sagemaker-governance.md#q14) | 4.5.7 | 事業部が 20 あり、中央のデータチームがボトルネックです。各部門がデータを所有して公開し、標準は中… |
| [sagemaker-governance 問15](../../exercises/sagemaker-governance.md#q15) | 4.5.7 | ガバナンスの 3 つの要素（発見、アクセス、監視）とサービスの組み合わせで、監視に当たるものはどれで… |

<!-- questions:end -->

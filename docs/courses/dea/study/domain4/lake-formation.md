# 分野4: Lake Formation と認可の方式

Lake Formation の設定と権限、認可の方式の選択を問います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [4.2.4](../../domain4.md#skill-4-2-4) | Lake Formation による権限の管理 |
| [4.2.5](../../domain4.md#skill-4-2-5) | 業務に合う認可の方式 |
| [4.3.1](../../domain4.md#skill-4-3-1) | データマスキングと匿名化 |

## 学習の順番 {#study-order}

1. [始めるときの設定](../../../../services/data-engineering.md#lake-formation-setup): 3 つの手順と症状を覚えます。
2. [権限](../../../../services/data-engineering.md#lake-formation-permissions): データフィルターを確認します。
3. [LF タグ](../../../../services/data-engineering.md#lake-formation-lf-tags): IAM タグとの違いを押さえます。
4. [条件とアクセス制御](../../../../services/iam.md#conditions): ABAC を確認します。

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 絞ったのに全員読める | `IAMAllowedPrincipals` の `Super` を外す |
| 既存のアクセスを止めずに移す | ハイブリッドアクセスモード |
| 列、行、セルで制限する | データフィルター |
| テーブルが多い | LF タグ |
| チームが増える | ABAC と `aws:PrincipalTag` |

## 引っかかりやすい点 {#traps}

- データフィルターは `SELECT` の付与にだけ使えます。
- LF タグは IAM ポリシーの条件に使えません。
- 統合していないエンジンには効きません。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [lake-formation 問1](../../exercises/lake-formation.md#q1) | 4.2.4 | Lake Formation でテーブルに列の権限を付けましたが、IAM で S3 の権限を持つ人が… |
| [lake-formation 問2](../../exercises/lake-formation.md#q2) | 4.2.4 | 既存のクエリを止めずに、選んだ主体だけ Lake Formation の権限へ移します。何を使います… |
| [lake-formation 問3](../../exercises/lake-formation.md#q3) | 4.2.4 | アナリストには ssn を除く列を、英国の担当者には country = 'UK' の行だけで ad… |
| [lake-formation 問4](../../exercises/lake-formation.md#q4) | 4.2.4 | Lake Formation の始め方で、次の手順を忘れたときの症状の組み合わせで正しいものはどれで… |
| [lake-formation 問5](../../exercises/lake-formation.md#q5) | 4.2.4 | Lake Formation の権限が効く範囲の説明で正しいものはどれですか。 |
| [lake-formation 問6](../../exercises/lake-formation.md#q6) | 4.2.5 | テーブルが数千あり、新しいテーブルの度に権限の付与が必要です。どの方式に変えますか。 |
| [lake-formation 問7](../../exercises/lake-formation.md#q7) | 4.2.5 | LF タグと IAM タグの説明で正しいものはどれですか。 |
| [lake-formation 問8](../../exercises/lake-formation.md#q8) | 4.2.5 | チームとプロジェクトが増え続けます。ロールを増やさず、プリンシパルのタグとリソースのタグの一致で S… |
| [lake-formation 問9](../../exercises/lake-formation.md#q9) | 4.2.5 | 組織の要件と方式の組み合わせで正しいものはどれですか。（2つ選択） |
| [lake-formation 問10](../../exercises/lake-formation.md#q10) | 4.3.1 | データレイクの email 列を、データをコピーせず特定のロールから隠します。何を使いますか。 |

<!-- questions:end -->

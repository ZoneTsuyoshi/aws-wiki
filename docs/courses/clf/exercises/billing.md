# 請求と費用管理 の問題集

対象の解説: [コスト管理](../../../services/cost-management.md)、[ガバナンス](../../../services/governance.md)

### 問1 {#q1}

請求書、支払い方法、クレジットを確認する場所として最も適切なものはどれですか。

- A. Billing and Cost Management のコンソール
- B. AWS Artifact
- C. AWS Trusted Advisor
- D. AWS Health Dashboard

??? success "答えと解説"
    **正解: A**

    請求の情報は Billing and Cost Management で確認します。

    - A: 正しい。
    - B: 誤り。監査レポートと契約の入手先。
    - C: 誤り。環境を点検するサービス。
    - D: 誤り。AWS 側の障害や予定を示すもの。

    **スキル:** [請求の情報](../domain4.md#t4-2-billing-info) / **参照:** [Billing and Cost Management](../../../services/cost-management.md#billing)

### 問2 {#q2}

今月の請求の内容について AWS に問い合わせたいと考えています。契約しているサポートプランは Basic です。正しい説明はどれですか。

- A. 請求の問い合わせには、Business Support+ が必要である
- B. 請求の問い合わせには、Enterprise が必要である
- C. AWS Trust & Safety に問い合わせる必要がある
- D. アカウントと請求の問い合わせは Basic でも受けられる

??? success "答えと解説"
    **正解: D**

    Basic には、アカウントと請求の問い合わせが含まれます。

    - A: 誤り。Basic でも問い合わせできる。
    - B: 誤り。Basic でも問い合わせできる。
    - C: 誤り。Trust & Safety は悪用の報告先。
    - D: 正しい。

    **スキル:** [請求の情報](../domain4.md#t4-2-billing-info) / **参照:** [Billing and Cost Management](../../../services/cost-management.md#billing)、[AWS Support プラン](../../../services/cloud-foundations.md#support-plans)

### 問3 {#q3}

Billing and Cost Management で確認できるものはどれですか。（2つ選択）

- A. AWS の SOC レポート
- B. 適用されているクレジット
- C. EC2 のゲスト OS のパッチの状況
- D. 他の利用者の請求額
- E. 請求書

??? success "答えと解説"
    **正解: B, E**

    請求、支払い、費用の分析をまとめたコンソールです。

    - A: 誤り。AWS Artifact で入手する。
    - B: 正しい。
    - C: 誤り。Systems Manager などで確認する。
    - D: 誤り。他の利用者の情報は確認できない。
    - E: 正しい。

    **スキル:** [請求の情報](../domain4.md#t4-2-billing-info) / **参照:** [Billing and Cost Management](../../../services/cost-management.md#billing)

### 問4 {#q4}

AWS のサービスの料金についての説明として正しいものはどれですか。

- A. サポートプランだけで決まる
- B. すべてのリージョンで同じである
- C. サービスごと、リージョンごとに異なる
- D. 一度契約すると、料金は永久に固定される

??? success "答えと解説"
    **正解: C**

    料金はサービスとリージョンで異なります。

    - A: 誤り。サービスとリージョンで異なる。
    - B: 誤り。リージョンごとに異なる。
    - C: 正しい。
    - D: 誤り。固定されない。

    **スキル:** [サービスの料金情報](../domain4.md#t4-2-pricing-info) / **参照:** [Pricing Calculator](../../../services/cost-management.md#pricing-calculator)

### 問5 {#q5}

ある EC2 インスタンスの東京リージョンの現在の単価を確認したいと考えています。最も適切な情報源はどれですか。

- A. CloudTrail のイベント履歴
- B. AWS の各サービスの料金ページ
- C. AWS Trust & Safety のフォーム
- D. AWS re:Post の投稿

??? success "答えと解説"
    **正解: B**

    料金は各サービスの料金ページで確認します。

    - A: 誤り。API の呼び出しの記録。
    - B: 正しい。
    - C: 誤り。悪用の報告のフォーム。
    - D: 誤り。コミュニティの Q&A で、公式の料金表ではない。

    **スキル:** [サービスの料金情報](../domain4.md#t4-2-pricing-info) / **参照:** [Pricing Calculator](../../../services/cost-management.md#pricing-calculator)

### 問6 {#q6}

同じインスタンスタイプを別のリージョンで動かす場合の費用の考え方として正しいものはどれですか。

- A. 単価はどのリージョンでも同じなので、料金の確認は不要である
- B. 利用者に近いリージョンの単価が必ず最も安い
- C. 新しいリージョンは必ず無料で使える
- D. リージョンで単価が異なるので、それぞれの料金を確認する

??? success "答えと解説"
    **正解: D**

    リージョンの選択では料金も観点の 1 つです。

    - A: 誤り。リージョンで異なる。
    - B: 誤り。距離で単価は決まらない。
    - C: 誤り。無料ではない。
    - D: 正しい。

    **スキル:** [サービスの料金情報](../domain4.md#t4-2-pricing-info) / **参照:** [Pricing Calculator](../../../services/cost-management.md#pricing-calculator)、[リージョン](../../../services/cloud-foundations.md#regions)

### 問7 {#q7}

月の費用が予算の 80% に達しそうなときに通知を受けたいと考えています。最も適切なものはどれですか。

- A. AWS Pricing Calculator
- B. AWS Artifact
- C. AWS Budgets
- D. AWS Cost Explorer

??? success "答えと解説"
    **正解: C**

    Budgets はしきい値を決めて、超えそうなときに通知します。

    - A: 誤り。作る前に費用を見積もる道具。
    - B: 誤り。監査レポートの入手先。
    - C: 正しい。
    - D: 誤り。費用と使用量をグラフで分析する道具。

    **スキル:** [Budgets と Cost Explorer](../domain4.md#t4-2-budgets-explorer) / **参照:** [AWS Budgets](../../../services/cost-management.md#budgets)

### 問8 {#q8}

先月からどのサービスの費用が増えたかをグラフで分析したいと考えています。最も適切なものはどれですか。

- A. Service Quotas
- B. AWS Cost Explorer
- C. AWS Budgets
- D. AWS Pricing Calculator

??? success "答えと解説"
    **正解: B**

    Cost Explorer は費用と使用量を分析します。

    - A: 誤り。サービスの上限を扱う。
    - B: 正しい。
    - C: 誤り。しきい値の通知の道具で、原因の分析は主な役割ではない。
    - D: 誤り。作る前の見積もりの道具。

    **スキル:** [Budgets と Cost Explorer](../domain4.md#t4-2-budgets-explorer) / **参照:** [Cost Explorer](../../../services/cost-management.md#cost-explorer)

### 問9 {#q9}

AWS Budgets と Cost Explorer の説明として正しいものはどれですか。（2つ選択）

- A. Budgets は予測の超過でも通知できる
- B. Budgets は予算を超えると EC2 を必ず自動で削除する
- C. Cost Explorer は過去の費用を表示できない
- D. Cost Explorer は今後の費用の予測もできる
- E. Cost Explorer はアカウントなしで使える公開の見積もりの道具である

??? success "答えと解説"
    **正解: A, D**

    Budgets は通知、Cost Explorer は分析です。

    - A: 正しい。
    - B: 誤り。必ず削除するものではない。
    - C: 誤り。過去の分析が主な機能。
    - D: 正しい。
    - E: 誤り。それは Pricing Calculator の公開の Web サイト。

    **スキル:** [Budgets と Cost Explorer](../domain4.md#t4-2-budgets-explorer) / **参照:** [AWS Budgets](../../../services/cost-management.md#budgets)、[Cost Explorer](../../../services/cost-management.md#cost-explorer)

### 問10 {#q10}

AWS を使い始める前に、計画中の構成の月額の費用を見積もりたいと考えています。最も適切なものはどれですか。

- A. AWS Pricing Calculator
- B. AWS Budgets
- C. AWS Cost and Usage Report
- D. AWS Cost Explorer

??? success "答えと解説"
    **正解: A**

    Pricing Calculator は構成の費用を作る前に見積もります。

    - A: 正しい。
    - B: 誤り。しきい値で通知する道具。
    - C: 誤り。実績の費用と使用量のデータ。
    - D: 誤り。実際にかかった費用の分析の道具。

    **スキル:** [Pricing Calculator](../domain4.md#t4-2-pricing-calculator) / **参照:** [Pricing Calculator](../../../services/cost-management.md#pricing-calculator)

### 問11 {#q11}

AWS Pricing Calculator の公開の Web サイトの説明として正しいものはどれですか。

- A. アカウントなしで、無料で使える
- B. 見積もりの件数に応じて料金がかかる
- C. 使うには Business Support+ が必要である
- D. 実際の請求額を保証する

??? success "答えと解説"
    **正解: A**

    公開の Web サイトはアカウント不要で無料です。

    - A: 正しい。
    - B: 誤り。無料で使える。
    - C: 誤り。サポートプランは不要。
    - D: 誤り。見積もりで、税も含まない。

    **スキル:** [Pricing Calculator](../domain4.md#t4-2-pricing-calculator) / **参照:** [Pricing Calculator](../../../services/cost-management.md#pricing-calculator)

### 問12 {#q12}

「移行前に見積もる」「作った後の実績を分析する」に合う道具の組み合わせはどれですか。

- A. 移行前: Trusted Advisor、実績: AWS Health Dashboard
- B. 移行前: AWS Budgets、実績: AWS Artifact
- C. 移行前: Cost Explorer、実績: Pricing Calculator
- D. 移行前: Pricing Calculator、実績: Cost Explorer

??? success "答えと解説"
    **正解: D**

    作る前か作った後かで道具を選びます。

    - A: 誤り。どちらも費用の見積もりや実績の分析の道具ではない。
    - B: 誤り。Artifact は費用の道具ではない。
    - C: 誤り。組み合わせが逆。
    - D: 正しい。

    **スキル:** [Pricing Calculator](../domain4.md#t4-2-pricing-calculator) / **参照:** [Pricing Calculator](../../../services/cost-management.md#pricing-calculator)、[Cost Explorer](../../../services/cost-management.md#cost-explorer)

### 問13 {#q13}

AWS Organizations の一括請求の説明として正しいものはどれですか。

- A. 一括請求を使うには、Enterprise のサポートプランの契約が必ず必要である
- B. 一括請求を使うと、アカウントごとの費用は確認できなくなる
- C. 管理アカウントがメンバーアカウントの費用をまとめて支払い、追加料金はかからない
- D. メンバーアカウントが管理アカウントの費用を支払い、追加料金がかかる

??? success "答えと解説"
    **正解: C**

    一括請求は追加料金なしで使えます。

    - A: 誤り。サポートプランは条件ではない。
    - B: 誤り。アカウントごとの費用を確認できる。
    - C: 正しい。
    - D: 誤り。管理アカウントが支払い、追加料金はかからない。

    **スキル:** [Organizations の一括請求](../domain4.md#t4-2-organizations) / **参照:** [一括請求](../../../services/cost-management.md#consolidated-billing)

### 問14 {#q14}

一括請求の利点はどれですか。（2つ選択）

- A. 使用量を合算してボリューム割引を組織全体で共有できる
- B. 組織のデータ転送の料金がすべて無料になる
- C. 請求書が 1 つにまとまる
- D. 全リソースが 1 つのアカウントへ自動で移動する
- E. 全アカウントの IAM ユーザーが自動で統合される

??? success "答えと解説"
    **正解: A, C**

    追跡のしやすさや、RI と Savings Plans の割引の共有も利点です。

    - A: 正しい。
    - B: 誤り。無料にはならない。
    - C: 正しい。
    - D: 誤り。リソースは移動しない。
    - E: 誤り。請求の機能で、ユーザーは統合しない。

    **スキル:** [Organizations の一括請求](../domain4.md#t4-2-organizations) / **参照:** [一括請求](../../../services/cost-management.md#consolidated-billing)

### 問15 {#q15}

各部門が別のアカウントを使っていますが、経理は請求を 1 か所にまとめたいと考えています。最も適切なサービスはどれですか。

- A. AWS Budgets
- B. AWS Organizations
- C. AWS Artifact
- D. AWS License Manager

??? success "答えと解説"
    **正解: B**

    Organizations の一括請求で、1 つの請求書にまとめられます。

    - A: 誤り。しきい値の通知の道具で、請求をまとめるものではない。
    - B: 正しい。
    - C: 誤り。監査レポートと契約の入手先。
    - D: 誤り。ライセンスの管理のサービス。

    **スキル:** [Organizations の一括請求](../domain4.md#t4-2-organizations) / **参照:** [一括請求](../../../services/cost-management.md#consolidated-billing)、[AWS Organizations](../../../services/governance.md#organizations)

### 問16 {#q16}

部門ごとの費用を分けるためにリソースへタグを付けましたが、Cost Explorer で選べません。何が足りませんか。

- A. リソースの再起動
- B. AWS Support のケースの作成
- C. コスト配分タグの有効化
- D. Enterprise へのプランの変更

??? success "答えと解説"
    **正解: C**

    タグは付けるだけでは請求データに出ず、有効化が必要です。

    - A: 誤り。再起動しても請求データには出ない。
    - B: 誤り。サポートのケースは不要。
    - C: 正しい。
    - D: 誤り。サポートプランは関係しない。

    **スキル:** [コスト配分タグとレポート](../domain4.md#t4-2-tags) / **参照:** [コスト配分タグ](../../../services/cost-management.md#cost-allocation-tags)

### 問17 {#q17}

コスト配分タグの種類と例の組み合わせとして正しいものはどれですか。

- A. どちらのタグも有効化せずに請求データに出る
- B. ユーザー定義タグ: `CostCenter`、AWS 生成タグ: `aws:createdBy`
- C. ユーザー定義タグ: `aws:createdBy`、AWS 生成タグ: `CostCenter`
- D. どちらのタグも AWS だけが付ける

??? success "答えと解説"
    **正解: B**

    付ける主体で種類が分かれます。

    - A: 誤り。どちらも有効化が必要。
    - B: 正しい。
    - C: 誤り。組み合わせが逆。
    - D: 誤り。ユーザー定義タグは利用者が付ける。

    **スキル:** [コスト配分タグとレポート](../domain4.md#t4-2-tags) / **参照:** [コスト配分タグ](../../../services/cost-management.md#cost-allocation-tags)

### 問18 {#q18}

部門ごとの費用を行単位で詳しく分析したいと考えています。最も適切なものはどれですか。

- A. CloudWatch のメトリクスを部門ごとに確認する
- B. タグを付けずに AWS Pricing Calculator の見積もりを使う
- C. タグを付けずに AWS Budgets を使う
- D. タグを有効化して AWS Cost and Usage Report を使う

??? success "答えと解説"
    **正解: D**

    CUR は最も詳しい費用と使用量のデータで、現在の推奨は Data Exports で作る CUR 2.0 です。

    - A: 誤り。費用の明細は分からない。
    - B: 誤り。作る前の見積もりの道具。
    - C: 誤り。通知の道具で、行単位の分析ではない。
    - D: 正しい。

    **スキル:** [コスト配分タグとレポート](../domain4.md#t4-2-tags) / **参照:** [Data Exports と Cost and Usage Reports](../../../services/cost-management.md#data-exports)、[コスト配分タグ](../../../services/cost-management.md#cost-allocation-tags)

### 問19 {#q19}

AWS Cost and Usage Report（CUR）の説明として正しいものはどれですか。

- A. 最も詳しい費用と使用量のデータで、S3 に配信される
- B. 使う前の構成の見積もりを作る公開の Web サイトである
- C. 使い方の相談を受け付けるサポートの窓口である
- D. AWS の監査レポートを PDF で配布する機能である

??? success "答えと解説"
    **正解: A**

    CUR は S3 に配信されます。

    - A: 正しい。
    - B: 誤り。それは Pricing Calculator。
    - C: 誤り。それは AWS Support。
    - D: 誤り。それは AWS Artifact。

    **スキル:** [コスト配分タグとレポート](../domain4.md#t4-2-tags) / **参照:** [Data Exports と Cost and Usage Reports](../../../services/cost-management.md#data-exports)

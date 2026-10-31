# クラウドの導入と移行 の問題集

対象の解説: [クラウドの基礎](../../../services/cloud-foundations.md)、[移行サービス](../../../services/migration.md)

### 問1 {#q1}

AWS CAF が示す、クラウドによる変革の 4 つのフェーズを順に並べたものはどれですか。

- A. Plan、Build、Test、Deploy
- B. Envision、Align、Launch、Scale
- C. Launch、Align、Scale、Envision
- D. Assess、Mobilize、Migrate、Modernize

??? success "答えと解説"
    **正解: B**

    機会の特定（Envision）、差の把握（Align）、試験導入（Launch）、本番への拡大（Scale）の順に進みます。

    - A: 誤り。CAF のフェーズの名前ではない。
    - B: 正しい。
    - C: 誤り。順序が違う。最初は機会を特定する Envision。
    - D: 誤り。これは移行のプログラムである MAP の段階に近い。

    **スキル:** [クラウド導入の戦略](../domain1.md#t1-3-adoption-strategies) / **参照:** [Cloud Adoption Framework](../../../services/cloud-foundations.md#caf)

### 問2 {#q2}

AWS CAF のフェーズのうち、小規模な試験導入を行って成果を確かめる段階はどれですか。

- A. Launch
- B. Scale
- C. Envision
- D. Align

??? success "答えと解説"
    **正解: A**

    Launch は試験導入の段階です。その後の Scale で本番に広げます。

    - A: 正しい。
    - B: 誤り。試験導入の結果を本番に広げる段階。
    - C: 誤り。機会を特定する段階で、まだ試験導入はしない。
    - D: 誤り。組織の差を把握する段階。

    **スキル:** [クラウド導入の戦略](../domain1.md#t1-3-adoption-strategies) / **参照:** [Cloud Adoption Framework](../../../services/cloud-foundations.md#caf)

### 問3 {#q3}

基幹システムはしばらく自社のデータセンターに残し、新しい Web サービスだけを AWS に置く方針にしました。この導入の形はどれですか。

- A. クラウド
- B. マルチリージョン
- C. オンプレミス
- D. ハイブリッド

??? success "答えと解説"
    **正解: D**

    オンプレミスとクラウドを接続して併用する形がハイブリッドです。

    - A: 誤り。すべてをクラウドで動かす形で、自社のデータセンターは残らない。
    - B: 誤り。AWS 内の配置の話で、自社施設との併用の話ではない。
    - C: 誤り。自社施設だけで動かす形で、AWS を使わない。
    - D: 正しい。

    **スキル:** [クラウド導入の戦略](../domain1.md#t1-3-adoption-strategies) / **参照:** [デプロイモデルとサービスモデル](../../../services/cloud-foundations.md#deployment-models)

### 問4 {#q4}

経営層が移行の判断のために、現状の環境をもとに費用対効果の試算を求めています。最も適切なものはどれですか。

- A. AWS Well-Architected Tool
- B. AWS Migration Hub
- C. Migration Evaluator
- D. AWS DMS

??? success "答えと解説"
    **正解: C**

    Migration Evaluator は、移行の費用対効果の試算に使います。

    - A: 誤り。動いているワークロードを質問形式でレビューするもの。
    - B: 誤り。移行の進み具合を追跡するもの。
    - C: 正しい。
    - D: 誤り。データベースのデータを移すサービス。

    **スキル:** [移行を支える情報源とプログラム](../domain1.md#t1-3-resources) / **参照:** [Migration Evaluator](../../../services/migration.md#migration-evaluator)

### 問5 {#q5}

移行の計画のために、オンプレミスのサーバーの一覧と依存関係を把握したいと考えています。試験ガイドの対象サービスのうち、この目的に合うものはどれですか。

- A. AWS Schema Conversion Tool
- B. AWS Migration Evaluator
- C. AWS Application Discovery Service
- D. AWS Trusted Advisor

??? success "答えと解説"
    **正解: C**

    Application Discovery Service は、サーバーの情報や依存関係を集めます。新規受付は終了していますが、試験ガイドの対象です。

    - A: 誤り。データベースのスキーマを変換するツール。
    - B: 誤り。費用対効果の試算のためのもの。
    - C: 正しい。
    - D: 誤り。AWS 上の環境を点検するもので、オンプレミスの調査には使わない。

    **スキル:** [移行を支える情報源とプログラム](../domain1.md#t1-3-resources) / **参照:** [Application Discovery Service](../../../services/migration.md#application-discovery)、[AWS Migration Hub](../../../services/migration.md#migration-hub)

### 問6 {#q6}

チームが移行の具体的な手順とパターンを文書で調べたいと考えています。最初に見るものとして最も適切なものはどれですか。

- A. AWS Prescriptive Guidance
- B. AWS Trust & Safety
- C. AWS Artifact
- D. AWS Health Dashboard

??? success "答えと解説"
    **正解: A**

    Prescriptive Guidance は、移行や実装の具体的な手順をまとめています。

    - A: 正しい。
    - B: 誤り。AWS リソースの悪用の報告先。
    - C: 誤り。監査レポートと契約を扱う。移行の手順はない。
    - D: 誤り。AWS 側の障害や予定の影響を示す。

    **スキル:** [移行を支える情報源とプログラム](../domain1.md#t1-3-resources) / **参照:** [サポートの情報源](../../../services/cloud-foundations.md#support-resources)

### 問7 {#q7}

AWS Migration Acceleration Program（MAP）の説明として正しいものはどれですか。

- A. データベースをダウンタイムなしで移行するための、専用のサービスである
- B. 評価、準備、移行とモダナイズの段階で進み、資金面の支援もある
- C. 移行後のリソースの設定を自動で修正する無料のツールである
- D. 有料のサポートプランの 1 つで、専任の TAM が付く

??? success "答えと解説"
    **正解: B**

    MAP は Assess、Mobilize、Migrate & Modernize の 3 段階で進む、移行を支えるプログラムです。ツール、研修、パートナーの知見に加えて、資金面の支援も含みます。

    - A: 誤り。それは AWS DMS の役割に近い。MAP はプログラム。
    - B: 正しい。
    - C: 誤り。MAP はツールではなく、修正も行わない。
    - D: 誤り。サポートプランではない。

    **スキル:** [移行を支える情報源とプログラム](../domain1.md#t1-3-resources) / **参照:** [サポートの情報源](../../../services/cloud-foundations.md#support-resources)

### 問8 {#q8}

試験ガイドが挙げる、AWS CAF を使って得られる成果の例はどれですか。（2つ選択）

- A. 運用効率の向上
- B. 責任共有モデルにおける利用者の責任の消滅
- C. データセンターの電力費の完全な無料化
- D. 全ワークロードの設定の誤りの自動修正
- E. ビジネスリスクの低減

??? success "答えと解説"
    **正解: A, E**

    ガイドの成果の例は、ビジネスリスクの低減、ESG の改善、収益の増加、運用効率の向上です。

    - A: 正しい。
    - B: 誤り。利用者の責任はなくならない。
    - C: 誤り。CAF の成果に挙げられていない。
    - D: 誤り。CAF は準備の枠組みで、設定を直すものではない。
    - E: 正しい。

    **スキル:** [AWS CAF の成果とパースペクティブ](../domain1.md#t1-3-caf) / **参照:** [Cloud Adoption Framework](../../../services/cloud-foundations.md#caf)

### 問9 {#q9}

クラウド移行に向けて、社員のスキルと組織の文化を整える計画を立てたいと考えています。AWS CAF のどのパースペクティブですか。

- A. ビジネス
- B. プラットフォーム
- C. オペレーション
- D. 人材

??? success "答えと解説"
    **正解: D**

    文化、組織構造、リーダーシップ、人材は人材パースペクティブの焦点です。

    - A: 誤り。クラウド投資を事業の成果につなげることを扱う。
    - B: 誤り。スケールする基盤や既存の刷新を扱う。
    - C: 誤り。事業の要求を満たすサービスの提供を扱う。
    - D: 正しい。

    **スキル:** [AWS CAF の成果とパースペクティブ](../domain1.md#t1-3-caf) / **参照:** [Cloud Adoption Framework](../../../services/cloud-foundations.md#caf)

### 問10 {#q10}

データとワークロードの機密性、完全性、可用性を確保することに焦点を当てた AWS CAF のパースペクティブはどれですか。

- A. ガバナンス
- B. 人材
- C. セキュリティ
- D. オペレーション

??? success "答えと解説"
    **正解: C**

    機密性、完全性、可用性はセキュリティパースペクティブの焦点です。

    - A: 誤り。効果を最大化し、変革のリスクを抑えることが焦点。
    - B: 誤り。文化やスキルを扱う。
    - C: 正しい。
    - D: 誤り。サービスの提供の水準を扱う。

    **スキル:** [AWS CAF の成果とパースペクティブ](../domain1.md#t1-3-caf) / **参照:** [Cloud Adoption Framework](../../../services/cloud-foundations.md#caf)

### 問11 {#q11}

AWS CAF のパースペクティブのうち、事業寄りのものはどれですか。（3つ選択）

- A. ガバナンス
- B. ビジネス
- C. オペレーション
- D. プラットフォーム
- E. セキュリティ
- F. 人材

??? success "答えと解説"
    **正解: A, B, F**

    前半のビジネス、人材、ガバナンスが事業寄り、後半のプラットフォーム、セキュリティ、オペレーションが技術寄りです。

    - A: 正しい。
    - B: 正しい。
    - C: 誤り。技術寄りのパースペクティブ。
    - D: 誤り。技術寄りのパースペクティブ。
    - E: 誤り。技術寄りのパースペクティブ。
    - F: 正しい。

    **スキル:** [AWS CAF の成果とパースペクティブ](../domain1.md#t1-3-caf) / **参照:** [Cloud Adoption Framework](../../../services/cloud-foundations.md#caf)

### 問12 {#q12}

期限まで時間がないので、数百台のサーバーをコードの変更なしで EC2 に移します。どの移行戦略ですか。

- A. Rehost
- B. Retire
- C. Refactor
- D. Repurchase

??? success "答えと解説"
    **正解: A**

    手を加えずに移すのが Rehost です。

    - A: 正しい。
    - B: 誤り。使わないものを止める戦略。
    - C: 誤り。クラウド向けに作り直すので時間がかかる。
    - D: 誤り。別の製品に買い替える戦略。

    **スキル:** [移行の戦略](../domain1.md#t1-3-migration-strategies) / **参照:** [移行の 7 つの R](../../../services/migration.md#seven-rs)

### 問13 {#q13}

自社で開発した顧客管理システムをやめて、SaaS の製品に切り替えます。どの移行戦略ですか。

- A. Relocate
- B. Replatform
- C. Rehost
- D. Repurchase

??? success "答えと解説"
    **正解: D**

    別の製品に買い替えるのが Repurchase です。

    - A: 誤り。同じ基盤のまま移す戦略。
    - B: 誤り。少し手を入れて移す戦略。
    - C: 誤り。変更せずに EC2 へ移す戦略。
    - D: 正しい。

    **スキル:** [移行の戦略](../domain1.md#t1-3-migration-strategies) / **参照:** [移行の 7 つの R](../../../services/migration.md#seven-rs)

### 問14 {#q14}

EC2 上で自前で運用する構成ではなく、アプリは変えずにデータベースだけ Amazon RDS に移して運用の手間を減らします。どの移行戦略ですか。

- A. Refactor
- B. Replatform
- C. Retain
- D. Rehost

??? success "答えと解説"
    **正解: B**

    少しだけ手を入れてマネージドサービスの利点を得るのが Replatform です。

    - A: 誤り。アプリをクラウド向けに作り直す戦略。
    - B: 正しい。
    - C: 誤り。今は移さない戦略。
    - D: 誤り。構成を変えずに移す戦略で、データベースの運用は自前のまま残る。

    **スキル:** [移行の戦略](../domain1.md#t1-3-migration-strategies) / **参照:** [移行の 7 つの R](../../../services/migration.md#seven-rs)

### 問15 {#q15}

規制の都合で、ある専用機器のシステムは当面オンプレミスに残すことにしました。どの移行戦略ですか。

- A. Retain
- B. Rehost
- C. Relocate
- D. Retire

??? success "答えと解説"
    **正解: A**

    今は移さずに残すのが Retain です。

    - A: 正しい。
    - B: 誤り。EC2 に移す戦略。
    - C: 誤り。基盤を変えずに AWS 側へ移す戦略。
    - D: 誤り。不要なので止める戦略で、残して動かし続けるものではない。

    **スキル:** [移行の戦略](../domain1.md#t1-3-migration-strategies) / **参照:** [移行の 7 つの R](../../../services/migration.md#seven-rs)

### 問16 {#q16}

本番のデータベースを動かしたままクラウドへ移し、切り替えの停止を短くしたいと考えています。最も適切な方法はどれですか。

- A. 毎晩のバックアップを手作業で S3 に置いて、翌朝に切り替える
- B. AWS DMS で全ロードの後に変更をレプリケートする
- C. AWS SCT だけを使ってデータをすべて移す
- D. データベースを停止してディスクを AWS に郵送する

??? success "答えと解説"
    **正解: B**

    DMS は全ロードの後に変更を流し続けるので、元のデータベースを動かしたまま移行できます。

    - A: 誤り。最後のバックアップ以降の変更を失うか、長い停止が必要になる。
    - B: 正しい。
    - C: 誤り。SCT はスキーマの変換ツールで、データの継続的な複製は DMS が行う。
    - D: 誤り。長い停止が発生する。

    **スキル:** [移行の戦略](../domain1.md#t1-3-migration-strategies) / **参照:** [AWS DMS](../../../services/migration.md#dms)、[移行タイプ](../../../services/migration.md#dms-migration-types)

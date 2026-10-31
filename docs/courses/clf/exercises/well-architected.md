# Well-Architected Framework の問題集

対象の解説: [クラウドの基礎](../../../services/cloud-foundations.md)

### 問1 {#q1}

AWS Well-Architected Framework の説明として最も適切なものはどれですか。

- A. AWS の監査レポートをダウンロードするためのサービス
- B. 設定の誤りを見つけて自動で修正する有料のサービス
- C. 組織のクラウド移行の準備を 6 つの視点で整理するための枠組み
- D. AWS 上のシステムを 6 つの柱で評価するための設計指針

??? success "答えと解説"
    **正解: D**

    Well-Architected Framework はシステムの設計を評価するための指針です。

    - A: 誤り。それは AWS Artifact の説明。
    - B: 誤り。指針であり、自動で修正するサービスではない。
    - C: 誤り。それは AWS CAF の説明。
    - D: 正しい。

    **スキル:** [Well-Architected Framework](../domain1.md#t1-2-wa-framework) / **参照:** [Well-Architected Framework](../../../services/cloud-foundations.md#well-architected)

### 問2 {#q2}

開発チームが、自分たちのワークロードを質問に答える形で見直し、改善点を記録したいと考えています。最も適切なものはどれですか。

- A. AWS Well-Architected Tool
- B. AWS Config
- C. Amazon Inspector
- D. AWS Artifact

??? success "答えと解説"
    **正解: A**

    Well-Architected Tool は、ワークロードを質問形式でレビューするコンソールのツールです。

    - A: 正しい。
    - B: 誤り。リソースの設定の変化と準拠を記録するサービス。
    - C: 誤り。ソフトウェアの脆弱性を検出するサービス。
    - D: 誤り。AWS の監査レポートと契約を扱うサービス。

    **スキル:** [Well-Architected Framework](../domain1.md#t1-2-wa-framework) / **参照:** [Well-Architected Tool](../../../services/cloud-foundations.md#wa-tool)

### 問3 {#q3}

AWS Well-Architected Tool の説明として正しいものはどれですか。

- A. Enterprise 以上のサポートプランでのみ使える有料の機能である
- B. 使用量に応じた料金がかかり、指摘した項目を自動で修正する
- C. 追加料金はかからず、指摘と記録を行うが、リソースを直接は修正しない
- D. 実行中のインスタンスに接続して、脆弱性をスキャンするものである

??? success "答えと解説"
    **正解: C**

    ツールはレビューと記録のためのもので、リソースの修正は利用者が行います。

    - A: 誤り。サポートプランを条件としない。
    - B: 誤り。追加料金はかからず、自動の修正も行わない。
    - C: 正しい。
    - D: 誤り。脆弱性のスキャンは Inspector の役割。

    **スキル:** [Well-Architected Framework](../domain1.md#t1-2-wa-framework) / **参照:** [Well-Architected Tool](../../../services/cloud-foundations.md#wa-tool)

### 問4 {#q4}

AWS Well-Architected Framework の柱に含まれるものはどれですか。（2つ選択）

- A. サステナビリティ
- B. 俊敏性
- C. コンプライアンス
- D. スケーラビリティ
- E. 信頼性

??? success "答えと解説"
    **正解: A, E**

    柱は、運用上の優秀性、セキュリティ、信頼性、パフォーマンス効率、コスト最適化、サステナビリティの 6 つです。

    - A: 正しい。
    - B: 誤り。クラウドの利点の 1 つで、柱ではない。
    - C: 誤り。柱の名前ではない。
    - D: 誤り。柱の名前ではない。
    - E: 正しい。

    **スキル:** [6 つの柱](../domain1.md#t1-2-pillars) / **参照:** [Well-Architected Framework](../../../services/cloud-foundations.md#well-architected)

### 問5 {#q5}

Well-Architected の柱のうち、「障害から復旧し、期待どおり動くか」を問うものはどれですか。

- A. 運用上の優秀性
- B. 信頼性
- C. パフォーマンス効率
- D. セキュリティ

??? success "答えと解説"
    **正解: B**

    信頼性の柱は、障害からの復旧と期待どおりの動作を扱います。

    - A: 誤り。運用を継続的に改善できるかを問う柱。
    - B: 正しい。
    - C: 誤り。リソースを効率よく使えるかを問う柱。
    - D: 誤り。データとシステムを守れるかを問う柱。

    **スキル:** [6 つの柱](../domain1.md#t1-2-pillars) / **参照:** [Well-Architected Framework](../../../services/cloud-foundations.md#well-architected)

### 問6 {#q6}

Well-Architected の柱のうち、「不要な費用を避けられるか」を問うものはどれですか。

- A. パフォーマンス効率
- B. コスト最適化
- C. サステナビリティ
- D. 信頼性

??? success "答えと解説"
    **正解: B**

    コスト最適化は、不要な費用を避ける柱です。

    - A: 誤り。リソースの効率のよい利用を問う柱で、費用そのものは問わない。
    - B: 正しい。
    - C: 誤り。環境への影響を減らせるかを問う柱。
    - D: 誤り。障害からの復旧を問う柱。

    **スキル:** [6 つの柱](../domain1.md#t1-2-pillars) / **参照:** [Well-Architected Framework](../../../services/cloud-foundations.md#well-architected)

### 問7 {#q7}

ある会社は、運用手順をコードにして、小さく元に戻せる変更を頻繁に行うようにしました。どの柱の考え方ですか。

- A. コスト最適化
- B. セキュリティ
- C. 運用上の優秀性
- D. 信頼性

??? success "答えと解説"
    **正解: C**

    小さく元に戻せる変更と手順のコード化は、運用上の優秀性の設計原則です。

    - A: 誤り。費用を減らすことを扱う柱。
    - B: 誤り。データとシステムの保護を扱う柱。
    - C: 正しい。
    - D: 誤り。障害からの復旧や復旧手順のテストを扱う柱。

    **スキル:** [柱の違いの見分け方](../domain1.md#t1-2-pillar-differences) / **参照:** [Well-Architected Framework](../../../services/cloud-foundations.md#well-architected)

### 問8 {#q8}

ある会社は、担当者が本番データに直接触らなくても済むように、ツールを整備しました。どの柱の考え方ですか。

- A. パフォーマンス効率
- B. 信頼性
- C. 運用上の優秀性
- D. セキュリティ

??? success "答えと解説"
    **正解: D**

    人をデータから遠ざけることは、セキュリティの柱の設計原則です。

    - A: 誤り。リソースの選び方と使い方の柱。
    - B: 誤り。障害からの復旧の柱。
    - C: 誤り。運用の改善の柱で、データへの接触を減らす話ではない。
    - D: 正しい。

    **スキル:** [柱の違いの見分け方](../domain1.md#t1-2-pillar-differences) / **参照:** [Well-Architected Framework](../../../services/cloud-foundations.md#well-architected)

### 問9 {#q9}

新しい世代のインスタンスに替えて使用率を上げ、消費電力を減らす取り組みをしています。目的は環境への影響を減らすことです。どの柱ですか。

- A. サステナビリティ
- B. コスト最適化
- C. 信頼性
- D. パフォーマンス効率

??? success "答えと解説"
    **正解: A**

    目的が環境への影響を減らすことなので、サステナビリティです。

    - A: 正しい。
    - B: 誤り。費用の削減が目的のときの柱で、この問題の目的は環境への影響。
    - C: 誤り。障害からの復旧の柱。
    - D: 誤り。リソースの選び方と使い方の柱で、環境負荷が目的ではない。

    **スキル:** [柱の違いの見分け方](../domain1.md#t1-2-pillar-differences) / **参照:** [Well-Architected Framework](../../../services/cloud-foundations.md#well-architected)

### 問10 {#q10}

本番の障害を想定して復旧手順を定期的にテストし、監視から自動で復旧するようにしました。どの柱の考え方ですか。

- A. サステナビリティ
- B. 信頼性
- C. 運用上の優秀性
- D. セキュリティ

??? success "答えと解説"
    **正解: B**

    障害からの自動復旧と復旧手順のテストは、信頼性の柱の設計原則です。

    - A: 誤り。環境への影響の柱。
    - B: 正しい。
    - C: 誤り。手順の改善の柱だが、復旧を目的とする設計原則は信頼性の柱にある。
    - D: 誤り。データとシステムの保護の柱。

    **スキル:** [柱の違いの見分け方](../domain1.md#t1-2-pillar-differences) / **参照:** [Well-Architected Framework](../../../services/cloud-foundations.md#well-architected)

### 問11 {#q11}

チームが、サーバーレスの構成を使い、頻繁に実験して最適な構成を選ぶようにしました。どの柱の考え方ですか。

- A. 運用上の優秀性
- B. 信頼性
- C. パフォーマンス効率
- D. コスト最適化

??? success "答えと解説"
    **正解: C**

    サーバーレスの利用と頻繁な実験は、パフォーマンス効率の柱の設計原則です。

    - A: 誤り。運用手順の改善を扱う柱。
    - B: 誤り。障害からの復旧を扱う柱。
    - C: 正しい。
    - D: 誤り。使った分だけ払う形や費用の分析を扱う柱。

    **スキル:** [柱の違いの見分け方](../domain1.md#t1-2-pillar-differences) / **参照:** [Well-Architected Framework](../../../services/cloud-foundations.md#well-architected)

### 問12 {#q12}

各部門の費用を分析して配賦し、使った分だけ払う形に切り替えました。どの柱の考え方ですか。

- A. パフォーマンス効率
- B. サステナビリティ
- C. セキュリティ
- D. コスト最適化

??? success "答えと解説"
    **正解: D**

    消費モデルの採用と、費用の分析と配賦は、コスト最適化の柱の設計原則です。

    - A: 誤り。リソースの選び方と使い方の柱。
    - B: 誤り。環境への影響を減らす柱で、費用の配賦は扱わない。
    - C: 誤り。保護と追跡の柱で、費用の追跡ではない。
    - D: 正しい。

    **スキル:** [柱の違いの見分け方](../domain1.md#t1-2-pillar-differences) / **参照:** [Well-Architected Framework](../../../services/cloud-foundations.md#well-architected)

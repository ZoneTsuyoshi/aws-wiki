# 分野4: コスト管理ツール

ツールの違いと、どの費用をどのツールで見るかを押さえます。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [コスト管理の機能とツール](../../domain4.md#t4-1-cost-tools) | コスト管理の機能、コスト管理ツールの適切な用途 |
| [コンピューティングの費用の把握](../../domain4.md#t4-2-tools) | コスト管理の機能、コスト管理ツールの適切な用途 |
| [データベースの費用の把握](../../domain4.md#t4-3-tools) | コスト管理の機能、コスト管理ツールの適切な用途 |
| [ネットワーク費用の把握と見直し](../../domain4.md#t4-4-tools) | コスト管理の機能、コスト管理ツールの適切な用途、既存のワークロードのネットワーク最適化の見直し |

## 学習の順番 {#study-order}

1. [Cost Explorer](../../../../services/cost-management.md#cost-explorer)と[AWS Budgets](../../../../services/cost-management.md#budgets): 分析と通知を区別します。
2. [Data Exports と Cost and Usage Reports](../../../../services/cost-management.md#data-exports)と[コスト配分タグ](../../../../services/cost-management.md#cost-allocation-tags): 行単位のデータとタグの有効化を確認します。
3. [一括請求](../../../../services/cost-management.md#consolidated-billing)と[予算の種類](../../../../services/cost-management.md#budget-types): 一括請求の利点と予算の種類を確認します。
4. [推奨を出すサービスの違い](../../../../services/cost-management.md#recommendation-tools)と[Compute Optimizer と適正サイズ](../../../../services/cost-management.md#compute-optimizer): 推奨を出すサービスの違いを比べます。
5. [データ転送の費用](../../../../services/cost-management.md#data-transfer)と[VPC フローログ](../../../../services/networking.md#flow-logs): 転送の費用の内訳と通信の調査を確認します。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| パブリック IPv4 | 0.005 USD/時 | 使用中でもアイドルでもかかる |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 過去の費用の分析と予測 | Cost Explorer |
| しきい値を超えそうなら通知 | Budgets |
| 行単位の最も詳しいデータ | Data Exports の CUR 2.0 |
| サイズの過剰を見つける | Compute Optimizer |
| 部門ごとに費用を分ける | コスト配分タグの有効化 |
| S3 への通信が NAT を通っている | ゲートウェイエンドポイント |

## 引っかかりやすい点 {#traps}

- コスト配分タグは付けるだけでは請求データに出ません。
- RDS のスナップショットのタグは、タグのコピーを有効にしないと付きません。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [cost-management 問1](../../exercises/cost-management.md#q1) | コスト管理ツール | 過去 12 か月の S3 の費用の推移をグラフで確認し、来月の予測を見ます。どれを使いますか。 |
| [cost-management 問2](../../exercises/cost-management.md#q2) | コスト管理ツール | S3 の月額がしきい値を超えそうなときに通知します。どれを使いますか。 |
| [cost-management 問3](../../exercises/cost-management.md#q3) | コスト管理ツール | 部門ごとの S3 の費用を請求データで分けます。バケットにタグ Department を付けましたが… |
| [cost-management 問4](../../exercises/cost-management.md#q4) | コンピューティングの費用 | 複数アカウントの Savings Plans の使用率が目標を下回ったら通知します。どれを使いますか… |
| [cost-management 問5](../../exercises/cost-management.md#q5) | コンピューティングの費用 | どのインスタンスがサイズ過剰かを、機械学習で分析した推奨で確認します。どれを使いますか。 |
| [cost-management 問6](../../exercises/cost-management.md#q6) | コンピューティングの費用 | 一括請求の利点として正しいものを選んでください。（2つ選択） |
| [cost-management 問7](../../exercises/cost-management.md#q7) | データベースの費用 | RDS の RI や Database Savings Plans の購入の推奨を確認します。どれを… |
| [cost-management 問8](../../exercises/cost-management.md#q8) | データベースの費用 | Aurora の I/O の費用が総額にどれだけ占めるかを、使用タイプの行単位で分析します。どれを使… |
| [cost-management 問9](../../exercises/cost-management.md#q9) | データベースの費用 | RDS のスナップショットの費用を DB ごとに分けます。正しい設定はどれですか。 |
| [cost-management 問10](../../exercises/cost-management.md#q10) | ネットワーク費用 | データ転送の費用が急に増えました。どのサービスの通信が増えたかを調べます。正しい組み合わせを選んでく… |
| [cost-management 問11](../../exercises/cost-management.md#q11) | ネットワーク費用 | プライベートサブネットの EC2 の S3 への通信が NAT を通り、費用が大きいと分かりました。… |
| [cost-management 問12](../../exercises/cost-management.md#q12) | ネットワーク費用 | アカウントにパブリック IPv4 アドレスが 10 個あり、3 個は未使用の Elastic IP … |

<!-- questions:end -->

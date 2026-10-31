# 分野1: 脅威の監視

守りたいものから監視するサービスを選び、組織全体に集約して、人や修復の処理へつなぐ判断を問います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [1.1.1](../../domain1.md#skill-1-1-1) | 監視要件の分析 |
| [1.1.2](../../domain1.md#skill-1-1-2) | ワークロードの監視戦略 |
| [1.1.3](../../domain1.md#skill-1-1-3) | セキュリティイベントの集約 |
| [1.1.4](../../domain1.md#skill-1-1-4) | メトリクス、アラート、ダッシュボード |
| [1.1.5](../../domain1.md#skill-1-1-5) | 定期的な評価と調査の自動化 |

## 学習の順番 {#study-order}

1. [サービスの選び方](../../../../services/threat-detection.md#choosing): 何を見るサービスかを表で区別します。
2. [GuardDuty のデータソース](../../../../services/threat-detection.md#guardduty-data-sources)と[保護プラン](../../../../services/threat-detection.md#guardduty-protection-plans): 証跡なしで分析できる理由と、Runtime Monitoring の役割を押さえます。
3. [GuardDuty の複数アカウント](../../../../services/threat-detection.md#guardduty-multi-account): 委任管理者がリージョンごとであることと、`ALL`、`NEW`、`NONE` の違いを覚えます。
4. [検出結果](../../../../services/threat-detection.md#guardduty-findings)と[イベント連携](../../../../services/threat-detection.md#guardduty-events): 重要度の値と、通知の頻度を確認します。
5. [Security Hub の組織と集約](../../../../services/threat-detection.md#security-hub-org): 中央設定とローカル設定の違いを理解します。
6. [Macie の検出方法](../../../../services/threat-detection.md#macie-discovery)と[検出結果](../../../../services/threat-detection.md#macie-findings): 自動検出とジョブの使い分け、CSPM への発行の既定を確認します。
7. [Inspector のスキャンの種類](../../../../services/threat-detection.md#inspector-scan-types): 継続的なスキャンと、対象のリソースを押さえます。
8. [ヘルスチェックとプローブ](../../../../services/observability.md#health-checks)と [Shield Advanced](../../../../services/threat-detection.md#shield-advanced): 層ごとの監視と、ヘルスベースの検出の前提を確認します。
9. [適合パック](../../../../services/governance.md#config-conformance-packs)、[Config の修復](../../../../services/governance.md#config-remediation)、[State Manager](../../../../services/operations.md#state-manager): 定期的な評価と修復の組み合わせを押さえます。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| GuardDuty の Critical | 9.0〜10.0 | 攻撃シーケンスを示す |
| GuardDuty の High | 7.0〜8.9 | EventBridge の絞り込みは数値で 7.0 以上 |
| GuardDuty の Medium | 4.0〜6.9 | 通常からの逸脱 |
| 検出結果の保持 | 90 日 | 長期の保管は S3 へエクスポート |
| 更新の通知の頻度 | 既定 6 時間。15 分、1 時間も可 | 変更は管理者アカウントだけ |
| Inspector のネットワーク到達性 | 12 時間ごと | EC2 だけが対象 |
| ALB のヘルスチェックの間隔 | 既定 30 秒（インスタンス、IP） | 全台が異常だと全台へ転送する |
| Macie のジョブ | 1 回、日次、週次、月次 | 初回の範囲は「既存のオブジェクトを含める」で決める |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 漏えいした認証情報を運用の負荷なしで検出する | GuardDuty。証跡がなくても管理イベントを分析する |
| 実行中の不審な振る舞いと既知の CVE の両方 | GuardDuty Runtime Monitoring と Inspector |
| 全バケットの機密データを安く把握し、一部を深く調べる | Macie の自動検出と定期ジョブ |
| 全リージョンの GuardDuty を組織でそろえる | 全リージョンで同じ委任管理者を指定する |
| 既存を含む全アカウントで GuardDuty を有効にする | 自動有効化を `ALL` にする |
| 全アカウントと全リージョンで CSPM の標準を統一する | 中央設定と設定ポリシー |
| 組織の検出結果の自動対応を 1 か所に置く | 委任管理者の EventBridge に、リージョンごとのルール |
| 特定の操作の件数の推移とアラーム | 証跡を CloudWatch Logs へ配信してメトリクスフィルター |
| 固定のしきい値を決められない API の急増 | CloudTrail Insights |
| 通知だけが必要 | User Notifications。修復まで動かすなら EventBridge |
| 非準拠を定期的に見つけて直す | Config ルールと Systems Manager Automation |
| ルールと修復を組織へ一括で展開する | 適合パック |
| エージェントの設定を保ち続ける | State Manager の関連付け |
| VPC 内のリソースを Route 53 の状態として扱う | CloudWatch アラームを監視するヘルスチェック |

## 引っかかりやすい点 {#traps}

- GuardDuty の委任管理者はリージョンごとの指定です。ただし、全リージョンで同じアカウントにします。
- 自動有効化の `NEW` は、すでに組織にあるアカウントを有効にしません。
- CSPM のローカル設定は、新しいアカウントと現在のリージョンだけが対象です。
- Config のアグリゲーターは読み取り専用です。ルールの展開や修復はできません。
- Config ルールは変更を止めません。操作を止めるなら SCP などを使います。
- Macie は既定で、ポリシーの検出結果だけを CSPM に発行します。機密データの検出結果は発行の設定を変えます。
- Inspector は新しい CVE で自動的に再評価します。評価の実行を計画する必要はありません。
- メトリクスフィルターは過去のログに遡りません。作成後のイベントだけが対象です。
- Inspector のネットワーク到達性は EC2 だけが対象で、S3 のバケットには使えません。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [threat-monitoring 問1](../../exercises/threat-monitoring.md#q1) | 1.1.1 | ある企業は 40 のアカウントに数千の S3 バケットを持っています。まず全バケットのどこに機密デー… |
| [threat-monitoring 問2](../../exercises/threat-monitoring.md#q2) | 1.1.1 | ある企業は EKS と EC2 でコンテナを運用しています。監査の指摘を受けて、次の 2 つを監視の… |
| [threat-monitoring 問3](../../exercises/threat-monitoring.md#q3) | 1.1.1 | 小規模なセキュリティチームが、IAM ユーザーのアクセスキーの漏えいと、普段と違う場所からの利用を検… |
| [threat-monitoring 問4](../../exercises/threat-monitoring.md#q4) | 1.1.1 | 組織に数百のバケットがあります。担当者は、公開設定になっているバケットのうち、機密データを含む可能性… |
| [threat-monitoring 問5](../../exercises/threat-monitoring.md#q5) | 1.1.2 | ある企業は CloudFront と ALB の Web アプリを Shield Advanced … |
| [threat-monitoring 問6](../../exercises/threat-monitoring.md#q6) | 1.1.2 | WAF のルールを変更したあと、ログイン画面の入力から完了までの操作だけが失敗する事象がありました。… |
| [threat-monitoring 問7](../../exercises/threat-monitoring.md#q7) | 1.1.2 | インシデント対応の演習で、誤った変更によりターゲットのセキュリティグループが ALB からの通信を拒… |
| [threat-monitoring 問8](../../exercises/threat-monitoring.md#q8) | 1.1.2 | 社内向けのアプリは VPC のプライベートサブネットだけで動いています。異常を Route 53 の… |
| [threat-monitoring 問9](../../exercises/threat-monitoring.md#q9) | 1.1.3 | 組織の GuardDuty を、東京リージョンで委任管理者のアカウント A に任せ、全メンバーが見え… |
| [threat-monitoring 問10](../../exercises/threat-monitoring.md#q10) | 1.1.3 | Security Hub CSPM の委任管理者がいる組織で、これまでローカル設定を使ってきました。… |
| [threat-monitoring 問11](../../exercises/threat-monitoring.md#q11) | 1.1.3 | 300 のメンバーアカウントを持つ組織で GuardDuty の委任管理者が自動有効化を NEW に… |
| [threat-monitoring 問12](../../exercises/threat-monitoring.md#q12) | 1.1.3 | GuardDuty の検出結果に応じた通知と自動対応を、組織全体で一か所に置きたいと考えています。メ… |
| [threat-monitoring 問13](../../exercises/threat-monitoring.md#q13) | 1.1.3 | 監査チームは、組織の全アカウントと全リージョンの Config ルールの準拠状況を 1 つのアカウン… |
| [threat-monitoring 問14](../../exercises/threat-monitoring.md#q14) | 1.1.4 | GuardDuty の新しい検出結果はすぐに通知されますが、同じ検出結果が繰り返し発生しても、次の通… |
| [threat-monitoring 問15](../../exercises/threat-monitoring.md#q15) | 1.1.4 | 統制の要件として、StopLogging とルートユーザーの利用の件数を、CloudWatch のダ… |
| [threat-monitoring 問16](../../exercises/threat-monitoring.md#q16) | 1.1.4 | ある本番アカウントでは、書き込みの管理 API の量が時間帯や日で大きく変わるので、固定のしきい値を… |
| [threat-monitoring 問17](../../exercises/threat-monitoring.md#q17) | 1.1.4 | 運用チームは、複数のアカウントとリージョンの CloudWatch アラームの通知を、メールとチャッ… |
| [threat-monitoring 問18](../../exercises/threat-monitoring.md#q18) | 1.1.4 | Macie と Security Hub CSPM を同じアカウントで有効にしました。S3 の公開設… |
| [threat-monitoring 問19](../../exercises/threat-monitoring.md#q19) | 1.1.4 | GuardDuty の検出結果のうち、重要度が High と Critical のものだけ当番を呼び… |
| [threat-monitoring 問20](../../exercises/threat-monitoring.md#q20) | 1.1.5 | ある企業は暗号化やログに関する Config ルール 20 個と、その修復の設定をまとめて、組織の全… |
| [threat-monitoring 問21](../../exercises/threat-monitoring.md#q21) | 1.1.5 | S3 バケットのパブリックアクセスブロックが外されたら、定期的な評価で見つけて、自動で元に戻したいと… |
| [threat-monitoring 問22](../../exercises/threat-monitoring.md#q22) | 1.1.5 | 数千台の EC2 で、CloudWatch エージェントと SSM Agent を最新の設定に保つ必… |
| [threat-monitoring 問23](../../exercises/threat-monitoring.md#q23) | 1.1.5 | Inspector を SSM の管理下の Linux インスタンスで使っています。担当者は、新しく… |
| [threat-monitoring 問24](../../exercises/threat-monitoring.md#q24) | 1.1.5 | 規制対象のバケットに毎日新しいファイルが届きます。Macie で毎日検査しますが、すでに監査済みの大… |

<!-- questions:end -->

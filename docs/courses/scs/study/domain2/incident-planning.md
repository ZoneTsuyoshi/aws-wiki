# 分野2: インシデント対応計画

攻撃を受ける前に用意するものと、それが動くことの確かめ方を問います。手順を実行できる形で残すこと、自動化と人の判断の境目を決めることが要点です。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [2.1.1](../../domain2.md#skill-2-1-1) | 対応計画とランブック |
| [2.1.2](../../domain2.md#skill-2-1-2) | インシデントへの備え |
| [2.1.3](../../domain2.md#skill-2-1-3) | 計画の有効性の検証 |
| [2.1.4](../../domain2.md#skill-2-1-4) | 自動修復 |

## 学習の順番 {#study-order}

1. [プレイブックと実行基盤](../../../../services/threat-detection.md#ir-playbooks): Automation、OpsCenter、ノートブック、Step Functions の役割を分けます。
2. [OpsCenter](../../../../services/operations.md#opscenter)と [Automation](../../../../services/operations.md#automation): OpsItem の作られ方、`AutomationAssumeRole`、`aws:approve` の制限を確認します。
3. [EC2 の隔離](../../../../services/threat-detection.md#ir-ec2-isolation): `AWSSupport-ContainEC2Instance` が何を代わりに行うかを押さえます。
4. [準備](../../../../services/threat-detection.md#ir-preparation): 対応用のロール、ログの保護、SCP を、なぜ事前に行うかと一緒に覚えます。
5. [Shield Advanced](../../../../services/threat-detection.md#shield-advanced)と [Shield Response Team](../../../../services/threat-detection.md#shield-srt): 保護は指定したリソースだけに効くことと、SRT の前提を確認します。
6. [計画のテスト](../../../../services/threat-detection.md#ir-testing)、[実験テンプレート](../../../../services/resilience.md#fis-template)、[AWS Resilience Hub](../../../../services/resilience.md#resilience-hub): 経路の確認、障害の注入、構成の評価の違いをつかみます。
7. [EventBridge による自動化](../../../../services/threat-detection.md#ir-eventbridge)と[人の承認](../../../../services/step-functions.md#human-approval): Lambda と Step Functions の選び方を確認します。
8. [Automated Forensics Orchestrator](../../../../services/threat-detection.md#forensics-orchestrator): ガイダンスであること、流れが取得、隔離、調査、報告であることを押さえます。
9. [ゾーンシフトとオートシフト](../../../../services/resilience.md#arc-zonal)と[ルーティングコントロール](../../../../services/resilience.md#arc-routing-control): AZ とリージョン、人の判断と AWS の判断で分けます。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| `aws:approve` のタイムアウト | 既定 7 日、最大 30 日 | 複数アカウント、複数リージョンの実行では使えない |
| FIS の `selectionMode` | `ALL`、`COUNT(n)`、`PERCENT(n)` | `ALL` は一致したものすべて。奇数の `PERCENT(50)` は切り捨て |
| FIS の停止条件 | CloudWatch アラーム | 止まった実験は再開できない |
| ゾーンシフトの有効期限 | 開始時に必須。最初は最大 3 日 | 後から更新できる |
| Shield Advanced | 1 年契約、月額 3,000 ドル | SRT とコスト保護が要件のときに選ぶ |
| プロアクティブエンゲージメントの連絡先 | 最大 10 件 | 1 件以上が必須 |
| SRT に見せる S3 バケット | 最大 10 個 | 平文か SSE-S3 で、同じアカウント |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 複数サービスの事象を担当者が追って閉じる | OpsCenter の OpsItem |
| 手順と分析を一緒に残して再実行する | SageMaker AI のノートブック |
| 決まった隔離の手順を、元に戻せる形で実行する | `AWSSupport-ContainEC2Instance` |
| 判断、待機、承認を含む複数の手順 | Step Functions。承認は `waitForTaskToken` |
| 1 回の短い処理 | Lambda |
| 検出結果の更新や抑制だけ | Security Hub CSPM の自動化ルール |
| 担当者が選んだ検出結果を対応へ送る | カスタムアクションと EventBridge |
| 特定の検出結果の経路だけ確かめる | `CreateSampleFindings` |
| 実在のリソースで検出結果を確かめる | 専用のアカウントでテスタースクリプト |
| 目標の RTO と RPO を満たす構成か | Resilience Hub。回復は FIS で確かめる |
| 検知と復旧の動きを障害で確かめる | FIS と停止条件 |
| 新しいリソースにも Shield Advanced を漏れなく | Firewall Manager のポリシー |
| 1 つの AZ を人の判断で外す | ゾーンシフト |
| リージョンを人の判断で切り替え、全停止を防ぐ | ルーティングコントロールとアサーションルール |
| 複数アカウントの EC2 のフォレンジックの流れ全体 | Automated Forensics Orchestrator |

## 引っかかりやすい点 {#traps}

- Shield Advanced は登録しただけでは保護されません。リソースを指定するか、Firewall Manager のポリシーで保護します。
- プロアクティブエンゲージメントには Route 53 ヘルスチェックが必要です。Anti-DDoS マネージドルールグループの検出では動きません。
- SRT は WAF の web ACL のログならアカウントのアクセスで読めます。他のログはバケットの追加が必要で、KMS で暗号化したバケットは読めません。
- Security Hub CSPM の自動化ルールは、リソースを操作しません。隔離は EventBridge の先で行います。
- `AutomationAssumeRole` を指定しないと、実行した主体の権限で動きます。
- Resilience Hub の評価は構成の分析です。評価に合格しても、実際に回復できることの証明にはなりません。
- サンプルの検出結果の値はプレースホルダーです。リソースを操作する処理の確認には使えません。
- ゾーンシフトの前に、残りの AZ の容量を確認します。足りないと過負荷になります。
- ゾーンオートシフトは AWS のテレメトリで動くので、「攻撃を受けた AZ を自動で判断する」機能ではありません。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [incident-planning 問1](../../exercises/incident-planning.md#q1) | 2.1.1 | あるセキュリティチームは、Security Hub CSPM の重大なアラートと CloudWatc… |
| [incident-planning 問2](../../exercises/incident-planning.md#q2) | 2.1.1 | 調査チームは、不審なロールの活動を調べる手順を残したいと考えています。手順の説明、Athena への… |
| [incident-planning 問3](../../exercises/incident-planning.md#q3) | 2.1.1 | EC2 の隔離手順を実行できる形で用意します。要件は 4 つです。実行前に影響を確認できること。隔離… |
| [incident-planning 問4](../../exercises/incident-planning.md#q4) | 2.1.1 | ある会社の対応計画は、検出結果の種類ごとに人が読む Word の文書です。深夜の対応で手順の抜けが続… |
| [incident-planning 問5](../../exercises/incident-planning.md#q5) | 2.1.1 | 中央のアカウントから、複数のアカウントとリージョンへ隔離のランブックを実行する計画です。途中に aw… |
| [incident-planning 問6](../../exercises/incident-planning.md#q6) | 2.1.2 | 会社は Shield Advanced に登録しました。ALB への攻撃で可用性が落ちたときに、Sh… |
| [incident-planning 問7](../../exercises/incident-planning.md#q7) | 2.1.2 | SRT に調査を頼むため、ロールを AssociateDRTRole で渡しました。SRT は WA… |
| [incident-planning 問8](../../exercises/incident-planning.md#q8) | 2.1.2 | 組織の全アカウントで Shield Advanced に登録済みです。ところが、新しいアカウントで作… |
| [incident-planning 問9](../../exercises/incident-planning.md#q9) | 2.1.2 | 調査担当者は、平時には本番アカウントの権限を持ちません。事象の発生時には、全メンバーアカウントですぐ… |
| [incident-planning 問10](../../exercises/incident-planning.md#q10) | 2.1.2 | メンバーアカウントで管理者権限を奪われても、CloudTrail の記録を止められず、保存済みのログ… |
| [incident-planning 問11](../../exercises/incident-planning.md#q11) | 2.1.3 | 検知と復旧の自動化が実際に動くか、検証環境で確かめます。Web 層のインスタンス 1 台だけを止めま… |
| [incident-planning 問12](../../exercises/incident-planning.md#q12) | 2.1.3 | ランサムウェアの被害に備えて、基幹アプリの目標を RTO 4 時間、RPO 1 時間と定めました。今… |
| [incident-planning 問13](../../exercises/incident-planning.md#q13) | 2.1.3 | GuardDuty の検出結果から EventBridge を経て通知する自動化を作りました。特定の… |
| [incident-planning 問14](../../exercises/incident-planning.md#q14) | 2.1.3 | サンプルの検出結果で経路は確認できました。次は、実際のリソースを対象にした検出結果を見て、ランブック… |
| [incident-planning 問15](../../exercises/incident-planning.md#q15) | 2.1.4 | GuardDuty の重要度 7 以上の検出結果で、隔離、スナップショットの取得、担当者の承認、結果… |
| [incident-planning 問16](../../exercises/incident-planning.md#q16) | 2.1.4 | SOC は、複数のアカウントとリージョンの EC2 で、検出から調査までのフォレンジックを自動化した… |
| [incident-planning 問17](../../exercises/incident-planning.md#q17) | 2.1.4 | ALB の配下にあるアプリで、1 つの AZ のインスタンスだけが攻撃を受けている可能性があります。… |
| [incident-planning 問18](../../exercises/incident-planning.md#q18) | 2.1.4 | 2 つのリージョンで動くサービスで、片方のリージョンが侵害されたと判断したら、人の判断で DNS の… |
| [incident-planning 問19](../../exercises/incident-planning.md#q19) | 2.1.4 | Security Hub CSPM で、次の処理を作ります。本番アカウントの検出結果は、取り込み時に… |
| [incident-planning 問20](../../exercises/incident-planning.md#q20) | 2.1.4 | 修復のランブックを作りました。担当者が手で実行すると成功しますが、自動化の中で権限の少ないプリンシパ… |

<!-- questions:end -->

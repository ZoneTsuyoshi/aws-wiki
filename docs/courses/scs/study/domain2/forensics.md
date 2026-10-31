# 分野2: フォレンジックとログ調査

証拠を失わない取得の順序、改ざんされない保管、複数のログをつなぐ手がかり、根本原因の調べ方を問います。「記録がない」ことと「起きていない」ことの区別も問われます。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [2.2.1](../../domain2.md#skill-2-2-1) | フォレンジックの証拠の取得と保管 |
| [2.2.2](../../domain2.md#skill-2-2-2) | ログの検索と関連付け |
| [2.2.5](../../domain2.md#skill-2-2-5) | 根本原因の分析 |

## 学習の順番 {#study-order}

1. [フォレンジックの証拠](../../../../services/threat-detection.md#ir-forensics): 証拠の種類ごとの取得方法と注意点を表で覚えます。
2. [EC2 の隔離](../../../../services/threat-detection.md#ir-ec2-isolation): メモリの取得が隔離や停止とどう前後するかを確認します。
3. [スナップショット](../../../../services/storage.md#ebs-snapshots): 別のアカウントとリージョンへの渡し方を確認します。
4. [保護プラン](../../../../services/threat-detection.md#guardduty-protection-plans): Malware Protection のスナップショットが既定で残らないことを押さえます。
5. [Object Lock](../../../../services/s3.md#object-lock)と [CloudTrail の調査](../../../../services/threat-detection.md#investigate-cloudtrail): ログの保護とログファイルの検証を確認します。
6. [どのログを見るか](../../../../services/threat-detection.md#log-sources): 知りたいことからログを選び、各ログに残らないものも覚えます。
7. [VPC フローログの調査](../../../../services/threat-detection.md#investigate-flow-logs)と [Security Lake](../../../../services/threat-detection.md#security-lake): 検索の手段を使い分けます。
8. [Detective](../../../../services/threat-detection.md#detective): データソース、最大 1 年分の履歴、検出結果グループを押さえます。
9. [Config と CloudTrail の違い](../../../../services/governance.md#config-vs-cloudtrail): 「何が変わったか」と「誰が変えたか」を分けます。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| GuardDuty の検出結果の保持 | 90 日 | 長く残すなら S3 へエクスポート |
| Detective の履歴 | 最大 1 年 | ログの収集やクエリの作成は不要 |
| Detective の検出結果グループ | 関連する検出結果の発生から 48 時間以内に作成 | 発生直後は表示されないことがある |
| CloudTrail のダイジェストファイル | 1 時間ごと | SHA-256 と署名。確認には `validate-logs` |
| `AKIA` と `ASIA` | 長期キーと一時キー | `ASIA` は `sessionIssuer` で発行元を追う |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| メモリも証拠に残す | 停止や再起動の前に、Run Command で取得 |
| AWS 管理キーで暗号化したスナップショットを渡す | カスタマー管理キーでコピーし、キーとコピーを共有 |
| 別のリージョンの調査環境へ渡す | そのリージョンへコピーしてから共有 |
| Malware Protection のスナップショットを残す | スキャンの前に保持を有効化。マルウェアが見つかったものだけ残る |
| ログの改ざんがないことを示す | ログファイルの検証と `validate-logs` |
| 保存期間中はルートユーザーでも消せない | Object Lock のコンプライアンスモード |
| 短命なインスタンスのログを残す | CloudWatch エージェントで常時送り、別のアカウントの S3 で保護 |
| 調査の環境 | フォレンジック用アカウントの隔離された VPC。スナップショットから作ったボリューム |
| 漏えいしたキーの操作をすべて調べる | Athena で `useridentity.accesskeyid` |
| `ASIA` の発行元のロールを調べる | `sessionContext.sessionIssuer` |
| DNS を使う持ち出しを調べる | Route 53 Resolver クエリログと `srcids` のインスタンス ID |
| 複数のログを共通の形式で横断する | Security Lake と OCSF |
| 主体の活動の変化を図で調べる | Detective |
| 複数の検出結果の関係を調べる | Detective の検出結果グループ |
| 設定の変更と操作した人を調べる | Config のタイムラインから CloudTrail へ |

## 引っかかりやすい点 {#traps}

- EBS スナップショットにメモリの内容は含まれません。再起動でも失われます。
- 終了保護は Auto Scaling による終了を防ぎません。ログも一緒に失われます。
- S3 の `GetObject` はデータイベントです。既定の証跡では記録されず、有効にしても過去の分は残りません。
- Amazon DNS への通信とインスタンスメタデータへの通信は、フローログに残りません。
- Detective のフローログのデータは EC2 のものだけです。NAT、RDS、Fargate は含まれません。
- Detective は独立したストリームでデータを取得するので、既存の CloudTrail やフローログの設定は要りません。
- Detective は調査のサービスです。検出結果の生成も修復もしません。
- ログファイルの検証は有効にするだけでは確認になりません。消されることも防げません。Object Lock と組み合わせます。
- GuardDuty の Malware Protection で保持の設定を後から有効にしても、過去のスキャンのスナップショットは戻りません。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [forensics 問1](../../exercises/forensics.md#q1) | 2.2.1 | GuardDuty が本番の EC2 で暗号通貨の採掘を検出しました。法務部は、メモリ上の証拠を含め… |
| [forensics 問2](../../exercises/forensics.md#q2) | 2.2.1 | 侵害された EC2 の EBS スナップショットを、同じリージョンのフォレンジック用アカウントへ渡し… |
| [forensics 問3](../../exercises/forensics.md#q3) | 2.2.1 | 東京リージョンの EC2 が侵害されました。調査環境は大阪リージョンのフォレンジック用アカウントにあ… |
| [forensics 問4](../../exercises/forensics.md#q4) | 2.2.1 | GuardDuty の Malware Protection for EC2 を使っています。マルウ… |
| [forensics 問5](../../exercises/forensics.md#q5) | 2.2.1 | 訴訟に備えて、CloudTrail のログが配信の後に変更も削除もされていないことを示し、保存期間中… |
| [forensics 問6](../../exercises/forensics.md#q6) | 2.2.1 | フォレンジック用アカウントで、侵害された EC2 のディスクを分析します。分析中に、マルウェアが外部… |
| [forensics 問7](../../exercises/forensics.md#q7) | 2.2.1 | Auto Scaling グループのインスタンスは、数時間で入れ替わることがあります。アプリケーショ… |
| [forensics 問8](../../exercises/forensics.md#q8) | 2.2.2 | 公開リポジトリに AKIA で始まるアクセスキーが見つかりました。組織の証跡は S3 にあり、Ath… |
| [forensics 問9](../../exercises/forensics.md#q9) | 2.2.2 | CloudTrail に ASIA で始まるキーの不審な操作が残っていました。どのロールから発行され… |
| [forensics 問10](../../exercises/forensics.md#q10) | 2.2.2 | S3 からのデータ持ち出しが疑われます。証跡を Athena で検索しましたが、GetObject … |
| [forensics 問11](../../exercises/forensics.md#q11) | 2.2.2 | EC2 からの DNS トンネリングが疑われます。VPC のフローログを調べましたが、Amazon … |
| [forensics 問12](../../exercises/forensics.md#q12) | 2.2.2 | 組織の複数のアカウントで、CloudTrail、VPC フローログ、Route 53 Resolve… |
| [forensics 問13](../../exercises/forensics.md#q13) | 2.2.5 | GuardDuty が High の検出結果を出しました。担当者は、この主体の普段の活動量と比べて何… |
| [forensics 問14](../../exercises/forensics.md#q14) | 2.2.5 | 同じロールのセッションと同じ送信元 IP に関わる GuardDuty の検出結果が、数日にわたって… |
| [forensics 問15](../../exercises/forensics.md#q15) | 2.2.5 | Detective を導入します。担当者の理解を確認しています。VPC にはフローログを設定していな… |
| [forensics 問16](../../exercises/forensics.md#q16) | 2.2.5 | 先週、本番のセキュリティグループに 0.0.0.0/0 の SSH が追加され、その後に侵入がありま… |

<!-- questions:end -->

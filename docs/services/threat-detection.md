# 脅威検出とインシデント対応

[:material-sprout: CLF](../courses/clf/services.md){ .exam-badge .exam-foundational } [:material-sprout: AIF](../courses/aif/services.md){ .exam-badge .exam-foundational } [:material-certificate: SAA](../courses/saa/services.md){ .exam-badge .exam-associate } [:material-certificate: SOA](../courses/soa/services.md){ .exam-badge .exam-associate } [:material-certificate: DEA](../courses/dea/services.md){ .exam-badge .exam-associate } [:material-certificate: MLA](../courses/mla/services.md){ .exam-badge .exam-associate } [:material-star-circle: SAP](../courses/sap/services.md){ .exam-badge .exam-professional } [:material-star-circle: DOP](../courses/dop/services.md){ .exam-badge .exam-professional } [:material-star-circle: AIP](../courses/aip/services.md){ .exam-badge .exam-professional } [:material-target: ANS](../courses/ans/services.md){ .exam-badge .exam-specialty } [:material-target: SCS](../courses/scs/services.md){ .exam-badge .exam-specialty }

AWS 環境の脅威を検出し、調査して封じ込めるためのサービスをまとめたページです。セキュリティ専門知識試験（SCS-C03）の分野 1、2、6 を主な読者に想定し、DDoS 防御とネットワークの防御も扱います。

[![検出結果を集約して自動対応する流れ](../assets/diagrams/threat-detection-response.png)](../assets/diagrams/threat-detection-response.png)

| サービス | 役割 | 見るもの | 代表的な問われ方 |
| --- | --- | --- | --- |
| [GuardDuty](#guardduty) | 脅威の検出 | CloudTrail、VPC フローログ、DNS ログなど | 不正利用、認証情報の悪用を検出したい |
| [Security Hub](#security-hub) | リスクの統合と優先度付け | 他サービスの検出結果、CSPM のチェック | 組織全体を 1 か所で見たい |
| [Inspector](#inspector) | 脆弱性の検出 | EC2、ECR、Lambda、コード | CVE と開いたネットワーク経路を見つけたい |
| [Macie](#macie) | 機密データの検出 | S3 のオブジェクトとバケット設定 | S3 の個人情報を見つけたい |
| [Detective](#detective) | 根本原因の調査 | CloudTrail、フローログ、GuardDuty の検出結果 | 検出結果の影響範囲を調べたい |
| [Security Lake](#security-lake) | セキュリティログの集約 | AWS と他社のログを OCSF で保管 | SIEM 向けにログを正規化したい |
| [Audit Manager](#audit-manager) | 監査の証跡集め | CloudTrail、Config、CSPM | 監査用の証拠を整理したい（新規受付は終了） |
| [Artifact](#artifact) | AWS の準拠資料 | SOC、PCI などの報告書と契約 | AWS 側の監査報告書がほしい |
| [Firewall Manager](#firewall-manager) | 防御設定の一元展開 | WAF、Shield、SG、Network Firewall | 組織全体に同じルールを強制したい |
| [Shield](#shield) | DDoS 防御 | L3、L4、L7 の攻撃 | DDoS に備えたい |
| [Network Firewall](#network-firewall) | VPC 境界の IPS | VPC を通るパケット | ドメインやシグネチャで通信を止めたい |

!!! warning "2026 年 10 月時点の状態の変更"
    - **Security Hub** は 2025 年 12 月に新しい統合製品が一般提供になり、従来のサービスは **Security Hub CSPM** という名前になりました。詳しくは [製品の現在の形](#security-hub-products) を参照してください。
    - **Audit Manager** は 2026 年 4 月 30 日で新規受付を終了し、保守モードです。
    - **CodeGuru Security** は 2025 年 11 月 20 日でサポートを終了しました。後継は Inspector の Code Security です。
    - **CloudTrail Lake** は 2026 年 5 月 31 日で、**Systems Manager Incident Manager** は 2025 年 11 月 7 日で新規受付を終了しました。

    SCS-C03 の試験ガイドには Audit Manager と CodeGuru Security の名前が残っています。出題された場合に備えて、役割は覚えておきます。

## GuardDuty {#guardduty}

[:material-sprout: CLF](../courses/clf/services.md){ .exam-badge .exam-foundational } [:material-certificate: SAA](../courses/saa/services.md){ .exam-badge .exam-associate } [:material-certificate: SOA](../courses/soa/services.md){ .exam-badge .exam-associate } [:material-star-circle: SAP](../courses/sap/services.md){ .exam-badge .exam-professional } [:material-star-circle: DOP](../courses/dop/services.md){ .exam-badge .exam-professional } [:material-target: SCS](../courses/scs/services.md){ .exam-badge .exam-specialty }

[提供単位](resource-scope.md#two-axes): リージョン。検出器はリージョンごとに有効にし、VPC の外です。VPC の中に何も置かずに、ログの複製を分析します。

ログとイベントを継続的に分析し、脅威インテリジェンスと機械学習で不審な活動を検出するサービスです。リージョン単位で有効にします。

検出はしますが、ブロックはしません。止める処理は [EventBridge で自動化](#ir-eventbridge) します。

### データソース {#guardduty-data-sources}

有効にするだけで、次の基本データソースの分析が始まります。

| データソース | 内容 | 注意点 |
| --- | --- | --- |
| CloudTrail 管理イベント | コントロールプレーンの API 呼び出し | 自分の証跡の設定とは無関係 |
| VPC フローログ | EC2 の通信 | 自分でフローログを作る必要はない |
| Route 53 Resolver DNS クエリログ | DNS の問い合わせと応答 | AWS のリゾルバーを使う場合だけ |

GuardDuty はこれらを独立した複製のストリームで受け取ります。そのため既存の設定に影響せず、課金や保持の設定も別です。ログは特徴を抽出したあと破棄されるので、調査用に残したいなら自分で証跡とフローログを作ります。

**設定を誤ったときの症状:** EC2 が OpenDNS や Google DNS、自前の DNS を使っていると、DNS ベースの検出が働きません。`Trojan:EC2/DNSDataExfiltration` のような検出結果が出ない場合は、まず DHCP オプションとリゾルバーを確認します。

- **例:** DHCP オプションの `domain-name-servers` が `AmazonProvidedDNS` なら DNS ログが分析されます。`192.0.2.53` のような自前の DNS にすると、そのインスタンスの DNS ベースの検出は止まります。
- **複製のストリームの例:** 証跡を 1 本も作っていないアカウントでも、管理イベントの検出は動きます。ただし、検出結果の根拠のログを後から読み返すには、自分で作った証跡が必要です。

全リージョンで有効にすることが推奨です。使っていないリージョンで攻撃者がリソースを作る場合や、IAM などのグローバルイベントを悪用する場合を検出できるからです。

### 保護プラン {#guardduty-protection-plans}

API では `features` と呼びます（2023 年 3 月より前のプランは `dataSources` でも設定できます）。

| プラン | 見るもの | 主な検出 |
| --- | --- | --- |
| S3 Protection | S3 の CloudTrail データイベント | 持ち出し、破壊の試み |
| EKS Protection | EKS の監査ログ | クラスターでの不審な操作 |
| Runtime Monitoring | エージェントが集める OS レベルのイベント | プロセス実行、ファイル、通信 |
| Malware Protection for EC2 | EC2 に接続された EBS | マルウェア |
| Malware Protection for S3 | 新しくアップロードされたオブジェクト | マルウェア |
| Malware Protection for AWS Backup | スナップショット、AMI、復旧ポイント | マルウェア |
| RDS Protection | RDS のログインとデータの活動 | Aurora、RDS for PostgreSQL への不審なアクセス |
| Lambda Protection | Lambda の通信ログ | 暗号通貨採掘、悪意あるサーバーとの通信 |
| AI Protection | Bedrock、AgentCore、SageMaker AI のデータイベント | 異常なモデル呼び出し、コストの搾取 |

- 初めて有効にしたときは、Runtime Monitoring 以外のプランが自動で有効になり、30 日の無料トライアルに含まれます。
- あとから登場したプランは、既存の利用者には自動で有効になりません。
- Runtime Monitoring は EKS、ECS の Fargate、EC2 に対応します。**EKS の Fargate は対象外** です。

プランごとの例です。

- **S3 Protection の例:** 普段アクセスのない送信元から深夜に大量の `GetObject` があると、`Exfiltration:S3/AnomalousBehavior` が出ます。無効だとデータイベントを見ないので出ません。
- **EKS Protection の例:** 匿名ユーザーがクラスターの API を呼ぶ操作を検出します。Runtime Monitoring はコンテナの中のプロセスを見るので、役割が違います。
- **RDS Protection の例:** Aurora に普段と違う場所から何度もログインに失敗すると検出します。
- **誤ると:** あとから登場したプランは自動で有効にならないので、古いアカウントでは新しい脅威の検出が抜けていることがあります。`list-detectors` のあと `get-detector` で `features` を確かめます。

Malware Protection for EC2 の 2 種類のスキャンです。

| 観点 | GuardDuty 起動 | オンデマンド |
| --- | --- | --- |
| 開始の条件 | マルウェアを示す検出結果 | インスタンスの ARN を指定 |
| 再スキャンの間隔 | 24 時間に 1 回 | 前回の開始から 1 時間後 |
| 無料トライアル | あり | なし |
| 除外 | タグで指定。`GuardDutyExcluded` は両方に効く | 同左の共通タグのみ |

エージェントレスで動き、Fargate のワークロードは対象外です。スナップショットの保持は既定で無効で、マルウェアが見つかった場合だけ残せます。証拠を残したいなら、**スキャンの前に** 有効にしておきます。

- **除外の例:** 検証用の EC2 に `GuardDutyExcluded=true` のタグを付けると、スキャンされません。
- **再スキャンの例:** 10:00 にオンデマンドで開始したら、次に開始できるのは 11:00 以降です。GuardDuty 起動のスキャンは 24 時間に 1 回です。
- **誤ると:** スナップショットの保持を有効にする前にスキャンすると、証拠のスナップショットは残りません。

Malware Protection for S3 は、GuardDuty 本体を有効にせず単独でも使えます。ただし単独利用では検出器 ID がないので、**検出結果が生成されません**。結果は EventBridge の既定のバスと CloudWatch のメトリクス、任意のオブジェクトタグで受け取ります。

```text
GuardDutyMalwareScanStatus = NO_THREATS_FOUND | THREATS_FOUND | UNSUPPORTED | ACCESS_DENIED | FAILED
```

このタグを条件にしたバケットポリシーで、スキャン前や感染したオブジェクトの読み取りを止められます。

```json
{
  "Effect": "Deny",
  "Principal": "*",
  "Action": "s3:GetObject",
  "Resource": "arn:aws:s3:::upload-example/*",
  "Condition": {
    "StringNotEquals": {
      "s3:ExistingObjectTag/GuardDutyMalwareScanStatus": "NO_THREATS_FOUND"
    },
    "ArnNotEquals": {
      "aws:PrincipalArn": "arn:aws:iam::111122223333:role/malware-scan-role"
    }
  }
}
```

- **例:** 利用者がアップロードした `a.pdf` はスキャンの前はタグがないので読めません。`NO_THREATS_FOUND` が付くと読めます。`THREATS_FOUND` なら読めないままです。
- **誤ると:** スキャン用のロールを例外にしないと、スキャン自体が `ACCESS_DENIED` になります。

### Extended Threat Detection {#guardduty-extended}

単独では目立たない複数の事象を、順序と時間で関連付けて **攻撃シーケンス** の検出結果にします。追加費用なしで自動的に有効です。

`AttackSequence:IAM/CompromisedCredentials` や `AttackSequence:S3/CompromisedData` のような名前で、重要度は最高の Critical になります。

S3 への攻撃を広く捉えたいなら S3 Protection も有効にします。プレビューの GuardDuty Investigation（AI による分析）や、CloudTrail と Runtime Monitoring のイベントを評価する Custom Detection Rules もあります。

- **例:** 「不審な API の呼び出し」「CloudTrail の無効化」「S3 からの大量の取得」が順に起きると、それぞれは Medium でも、全体が Critical の攻撃シーケンス 1 件になります。

### 検出結果 {#guardduty-findings}

検出結果の型は次の形式です。

```text
ThreatPurpose:ResourceTypeAffected/ThreatFamilyName.DetectionMechanism!Artifact
例: CryptoCurrency:EC2/BitcoinTool.B!DNS
```

| 重要度 | 値 | 意味 | 対応 |
| --- | --- | --- | --- |
| Critical | 9.0 - 10.0 | 攻撃シーケンスが進行中か直近で発生 | 最優先で切り分けと修復 |
| High | 7.0 - 8.9 | リソースが侵害され不正利用中 | すぐに修復 |
| Medium | 4.0 - 6.9 | 通常からの逸脱 | 早めに確認。説明できなければ侵害と扱う |
| Low | 1.0 - 3.9 | 試みのみで侵害なし（ポートスキャンなど） | 記録にとどめる |

- **しきい値の例:** EventBridge で `severity >= 7` とすると、7.0 と 8.5 と 9.5 は一致し、6.9 は一致しません。
- **誤ると:** 自動の隔離を `severity >= 4` にすると、調査が必要なだけの Medium でも本番の EC2 を隔離してしまいます。

検出結果の保持は **90 日** です。長く残すには S3 へエクスポートします。

- **例:** 10 月 1 日の検出結果は 12 月 30 日ごろに消えます。監査で 1 年残すなら、S3 へエクスポートし、ライフサイクルで 400 日後に削除します。

試験でよく出る検出結果です。

| 検出結果 | 意味 | 最初の対応 |
| --- | --- | --- |
| `UnauthorizedAccess:IAMUser/InstanceCredentialExfiltration.OutsideAWS` | EC2 のロールの認証情報が AWS の外から使われた | [ロールのセッションを失効](#ir-credentials) |
| `CryptoCurrency:EC2/BitcoinTool.B!DNS` | EC2 が暗号通貨関連のドメインへ問い合わせ | [インスタンスを隔離](#ir-ec2-isolation) |
| `Trojan:EC2/DNSDataExfiltration` | DNS を使った持ち出し | 隔離と調査 |
| `Recon:EC2/PortProbeUnprotectedPort` | 開いているポートへの探査 | セキュリティグループの見直し |
| `Exfiltration:S3/AnomalousBehavior` | S3 からの異常な取り出し | 主体の調査と権限の停止 |

### 抑制ルールとリスト {#guardduty-suppression}

| 機能 | 効果 | 使いどころ |
| --- | --- | --- |
| 抑制ルール | 条件に合う新しい検出結果を自動でアーカイブ | 既知の誤検知を減らす |
| 信頼リスト | その IP やドメインでは検出結果を出さない | 自社の送信元 |
| 脅威リスト | その相手との通信で検出結果を出す | 自社や他社の脅威情報 |

抑制された検出結果は生成はされ、アーカイブの状態で 90 日残ります。ただし **Security Hub CSPM、S3、Detective、EventBridge には送られず**、マルウェアスキャンも起動しません。

広すぎる抑制は危険です。たとえば EKS 関連をすべて抑制すると、Extended Threat Detection がそれらを関連付けに使えなくなり、攻撃シーケンスを見逃します。誤検知を繰り返し確認してから、絞った条件で作ります。

例: VPN 経由でオンプレミスから通信を出す構成では、`InstanceCredentialExfiltration.OutsideAWS` が誤検知になります。検出結果の型と、自社のゲートウェイの送信元 IP を条件に抑制します。

```bash
aws guardduty create-filter \
  --detector-id 12abc34d567e8fa901bc2d34e56789f0 \
  --name onprem-gateway \
  --action ARCHIVE \
  --finding-criteria '{"Criterion":{
    "type":{"Eq":["UnauthorizedAccess:IAMUser/InstanceCredentialExfiltration.OutsideAWS"]},
    "service.action.awsApiCallAction.remoteIpDetails.ipAddressV4":{"Eq":["198.51.100.6"]}}}'
```

脆弱性診断ツールが出す `Recon:EC2/Portscan` も、診断サーバーのインスタンス ID を条件に抑制します。

| リストの上限 | 値 |
| --- | --- |
| 信頼リスト | リージョンごとに、エンティティリストと IP リストをそれぞれ 1 つ |
| 脅威リスト | リージョンごとに、エンティティリストと IP リストをそれぞれ最大 6 つ |
| ファイルサイズ | 35 MB |
| 反映時間 | 目安 15 分、場合により最大 40 分 |

エンティティリスト（推奨）は IP、ドメイン、SHA-256 ハッシュを扱えます。従来の IP リストは IP のみです。

```text
192.0.2.10
198.51.100.0/24
malware.example.com
```

1 行に 1 件の平文（TXT）で書きます。形式は STIX なども選べます。

- **優先の例:** 同じ `192.0.2.10` が信頼リストと脅威リストの両方にあると、信頼リストが優先され、検出結果は出ません。
- **更新の例:** S3 のリストに 1 行足しただけでは反映されません。リストを再度アクティブにして、15 分（最大 40 分）待ちます。
- **対象の例:** パブリックな IP とドメインにだけ効き、`10.0.0.0/8` を書いても効きません。IPv4 のみで、IPv6 は書けません。SHA-256 は脅威のエンティティリストにだけ書けます。

### 複数アカウント {#guardduty-multi-account}

Organizations の管理アカウントが、委任管理者を指定します。招待方式は従来の方法で、Organizations との統合が推奨です。

| 設定 | 内容 | 誤ったときの症状 |
| --- | --- | --- |
| 委任管理者 | 全リージョンで同じアカウントにする | 別のアカウントは指定できない |
| 指定の単位 | **リージョンごと** に指定、追加する | 1 リージョンだけ指定すると他は未管理のまま |
| 自動有効化 `ALL` | 既存と新規の全メンバー | 意図しないアカウントにも費用が出る |
| 自動有効化 `NEW` | 新規メンバーのみ | 既存メンバーは有効にならない |
| 自動有効化 `NONE` | 新規メンバーは自動で有効にしない | 既存アカウントの状態は変わらない |
| 上限 | 委任管理者あたり 50,000 メンバー | 超えると通知が届く |

- **リージョンの例:** 東京、大阪、バージニア北部を使うなら、委任管理者の指定と自動有効化を 3 リージョンそれぞれで行います。
- **自動有効化の例:** 既存 40 アカウントに新規が 10 増えるなら、`ALL` は 50 全部、`NEW` は新規の 10 だけです。`NEW` では、既存の 40 は個別に有効にするまで無効のままです。

- 管理アカウントを委任管理者にすることはできますが、最小権限の観点で非推奨です。
- 委任管理者を変更しても、メンバーの GuardDuty は無効になりません。
- 抑制ルールと信頼、脅威リストは管理者が管理します。メンバーは作れません。
- `NEW` はオプトインリージョンで順序に注意が必要です。先に組織へ参加した既存のアカウントには効かないので、`ALL` を使うか個別に有効にします。
- Organizations の宣言型ポリシーでも有効化を管理できます。自動有効化とは別の仕組みです。

### イベント連携とエクスポート {#guardduty-events}

| 配信先 | 新しい検出結果 | 同じ検出結果の更新 |
| --- | --- | --- |
| EventBridge | ほぼリアルタイム | 既定は 6 時間ごと。15 分、1 時間に変更可 |
| S3 エクスポート | 約 5 分以内 | 同じ頻度の設定に従う |

頻度を変えられるのは管理者だけです。管理者の EventBridge にはメンバーの検出結果も届くので、対応の自動化は管理者アカウントに置けます。

```bash
aws guardduty update-detector \
  --detector-id 12abc34d567e8fa901bc2d34e56789f0 \
  --finding-publishing-frequency FIFTEEN_MINUTES
```

値は `FIFTEEN_MINUTES`、`ONE_HOUR`、`SIX_HOURS`（既定）です。

- **例:** 同じポートスキャンが続いて回数が 3 から 7 に増えても、既定では通知は 6 時間に 1 回です。ただし新しい検出結果は頻度の設定にかかわらず、すぐに届きます。

S3 エクスポートには KMS キーが必須で、キーポリシーとバケットポリシーの両方で GuardDuty を許可します。

- **配置の例:** バケットとキーは同じリージョンに置きます。東京の検出結果を大阪のバケットへ出すなら、キーも大阪です。通常のリージョンの検出結果を、オプトインのリージョンのバケットへは出せません。
- **誤ると:** キーポリシーで GuardDuty を許可していないと、エクスポートの設定でエラーになります。

## Security Hub {#security-hub}

[:material-sprout: CLF](../courses/clf/services.md){ .exam-badge .exam-foundational } [:material-certificate: SAA](../courses/saa/services.md){ .exam-badge .exam-associate } [:material-certificate: SOA](../courses/soa/services.md){ .exam-badge .exam-associate } [:material-star-circle: SAP](../courses/sap/services.md){ .exam-badge .exam-professional } [:material-star-circle: DOP](../courses/dop/services.md){ .exam-badge .exam-professional } [:material-target: SCS](../courses/scs/services.md){ .exam-badge .exam-specialty }

[提供単位](resource-scope.md#two-axes): リージョン。リージョンごとに有効にし、ホームリージョンへ集約します。VPC の外です。

### 製品の現在の形 {#security-hub-products}

現在は名前の似た 2 つの製品があります。古い教材の「Security Hub」は、今の **Security Hub CSPM** を指します。

| 観点 | Security Hub（2025 年 12 月 2 日に一般提供） | Security Hub CSPM（従来の製品） |
| --- | --- | --- |
| 目的 | 信号を関連付け、実際のリスクを優先付け | 基準に対する設定のチェックと検出結果の集約 |
| 主な成果物 | 露出（exposure）の検出結果、攻撃経路グラフ、修復計画 | コントロールの検出結果、セキュリティスコア |
| 検出結果の形式 | OCSF | ASFF |
| 入力 | CSPM、GuardDuty、Inspector、Macie、Access Analyzer | Config のルールによるチェック、AWS サービス、他社製品 |
| 自動化 | 自動化ルール（Jira Cloud、ServiceNow の起票を含む） | 自動化ルール、カスタムアクション、EventBridge |
| サービスリンクロール | `AWSServiceRoleForSecurityHubV2` | CSPM のロール |

両者は対立するものではなく、Security Hub は CSPM の結果も入力にします。設定の準拠をチェックするのは CSPM の役割です。

### Security Hub の機能 {#security-hub-unified}

| 機能 | 内容 |
| --- | --- |
| 露出の検出結果 | CSPM と Inspector などの結果を関連付け、悪用されうる状態を示す |
| 攻撃経路グラフ | 攻撃者がどうリソースに到達し制御するかを図示 |
| 未使用アクセスの分析 | 90 日間使われていないロール、ユーザー、キー、権限を検出。有効にすると Access Analyzer が作られる |
| 修復計画 | 関連する露出を根本原因でまとめ、1 回の修正で複数を解消 |
| AI インベントリ | AI と ML のリソースを一覧 |
| 自動化ルール | 検出結果の更新、リソースの重要度の設定、起票 |

組織への展開は 3 段階です。管理アカウントが委任管理者を指定し、委任管理者が自身で有効にして、ポリシーでメンバーに展開します。CSPM の委任管理者（管理アカウント以外）がすでにいる場合は、同じアカウントが自動で選ばれます。

- **未使用アクセスの例:** 90 日使っていないアクセスキーやロールが検出されます。
- **修復計画の例:** 「公開された EC2 に重大な CVE があり、強い権限のロールが付いている」露出が 3 件あり、原因が同じセキュリティグループなら、そのルールの修正 1 回でまとめて解消します。

自動化ルールはアカウントとリージョンごとに最大 100 個です。リージョン集約を使うと、ホームリージョンでしか作れません。

- **誤ると:** リンクリージョンで自動化ルールを作ろうとすると失敗します。ホームリージョンで作ります。

### Security Hub CSPM の標準とコントロール {#security-hub-cspm}

標準を有効にすると、属するコントロールも有効になり、チェックの結果がスコアになります。

| 標準 | 内容 |
| --- | --- |
| AWS Foundational Security Best Practices | AWS のベストプラクティス |
| CIS AWS Foundations Benchmark | CIS の設定基準 |
| NIST SP 800-53 Rev. 5、NIST SP 800-171 Rev. 2 | NIST の要件 |
| PCI DSS | カード業界の基準 |
| AWS Resource Tagging | タグの有無 |
| AI Security Best Practices | AI リソースの基準 |
| CRI Profile v2.2 | 金融業界の基準 |
| サービス管理標準（Control Tower） | Control Tower から設定する検出コントロール |

| 前提 | 内容 | 誤ったときの症状 |
| --- | --- | --- |
| AWS Config の有効化 | 大半のコントロールは Config のサービスリンクルールで動く | コントロールの結果が出ない。`Config.1` が失敗する |
| リージョン | 有効にしたリージョンの結果だけ処理 | CIS の完全な準拠には全リージョンが必要 |
| 遡及なし | 有効化後に生成された結果だけ集める | 過去の GuardDuty の検出結果は出てこない |
| 検出結果のプロバイダー | 他サービス側でも連携を確認する | Macie は既定で **ポリシーの検出結果だけ** を送る |

- **スコアの例:** スコアは、有効なコントロール（`Passed`、`Failed`、`Unknown`）のうち `Passed` の割合です。`No data` は計算から除きます。40 個が `Passed`、10 個が `Failed` なら 40 ÷ 50 = 80% です。更新は 24 時間ごとです。
- **標準の選び方の例:** カード情報を扱う決済のアカウントには PCI DSS を、それ以外には AWS Foundational Security Best Practices を有効にします。
- **遡及なしの例:** 10 月 1 日に有効にしたなら、9 月の GuardDuty の検出結果は Security Hub CSPM には現れません。

### 組織と集約 {#security-hub-org}

| 機能 | 内容 |
| --- | --- |
| 委任管理者 | Organizations の管理アカウントが指定 |
| 中央設定 | 設定ポリシーで、アカウント、OU、リージョンをまたいで標準とコントロールを管理 |
| ローカル設定 | 新規アカウントと現在のリージョンだけが対象で、既存アカウントには効かない |
| ホームリージョン | 以前の集約リージョン。検出結果、インサイト、準拠状態、スコアを集める |
| リンクリージョン | ホームへデータを送るリージョン |

「全アカウントの全リージョンで標準を統一したい」と問われたら、中央設定が答えです。

- **中央設定の例:** ホームを東京、リンクを大阪とバージニア北部にします。本番の OU に FSBP と CIS、開発の OU に FSBP だけのポリシーを関連付けます。後から本番の OU に入ったアカウントにも自動で適用されます。
- **self-managed の例:** 特定の OU を self-managed にすると、メンバーがリージョンごとに自分で設定します。
- **誤ると:** ローカル設定のまま標準を変えても、既存のアカウントには反映されず、準拠の状態がアカウントごとにばらつきます。

### 自動化 {#security-hub-automation}

| 機能 | 動き | 用途 |
| --- | --- | --- |
| 自動化ルール | Security Hub の中で検出結果を更新、抑制 | 重要度の変更、`SUPPRESSED` への変更 |
| EventBridge ルール | 外部へアクションを実行 | Lambda、Step Functions、SNS、起票 |
| カスタムアクション | 担当者が選んだ検出結果を EventBridge へ | 人の判断を挟む修復 |

**自動化ルールは EventBridge より先に適用** されます。CSPM の自動化ルールは管理者アカウントで、リージョンごとに最大 100 個作れます。

- **自動化ルールの例:** アカウント `111122223333`（本番）の `HIGH` を `CRITICAL` に上げます。`INFORMATIONAL` を `SUPPRESSED` にします。
- **順序の例:** API では `RuleOrder` の小さいルールから順に適用され、同じ項目を変えるルールは数値の大きいほうが最後に効きます。ルール 1 が `HIGH` にし、ルール 2 が `CRITICAL` にすれば、結果は `CRITICAL` です。
- **EventBridge の例:** 自動化ルールで `SUPPRESSED` にした検出結果を、イベントパターンの `Workflow.Status` で除くと、通知を減らせます。

CSPM のイベントの種類は `Security Hub Findings - Imported`（全件）と `Security Hub Findings - Custom Action` です。

## Inspector {#inspector}

[:material-sprout: CLF](../courses/clf/services.md){ .exam-badge .exam-foundational } [:material-sprout: AIF](../courses/aif/services.md){ .exam-badge .exam-foundational } [:material-certificate: SAA](../courses/saa/services.md){ .exam-badge .exam-associate } [:material-certificate: SOA](../courses/soa/services.md){ .exam-badge .exam-associate } [:material-certificate: MLA](../courses/mla/services.md){ .exam-badge .exam-associate } [:material-star-circle: SAP](../courses/sap/services.md){ .exam-badge .exam-professional } [:material-star-circle: DOP](../courses/dop/services.md){ .exam-badge .exam-professional } [:material-target: SCS](../courses/scs/services.md){ .exam-badge .exam-specialty }

[提供単位](resource-scope.md#two-axes): リージョン。リージョンごとに有効にし、VPC の外です。EC2 のエージェント方式は、VPC 内のインスタンスから SSM へ通信します。

ワークロードを自動で見つけ、ソフトウェアの脆弱性と意図しないネットワーク経路を継続的にスキャンします。修正が確認できると検出結果は自動で閉じられます。

### スキャンの種類 {#inspector-scan-types}

| 種類 | 対象 | 初回有効化時 |
| --- | --- | --- |
| EC2 | CVE、ネットワーク到達性 | 自動で有効 |
| ECR | コンテナイメージ | 自動で有効 |
| Lambda 標準 | 関数とレイヤーの依存関係 | 自動で有効 |
| Lambda コード | 独自コードの脆弱性 | 任意。標準が前提 |
| マシンイメージ | AMI | 任意 |
| Code Security | 自作コード、依存関係、IaC | 任意 |

Inspector のスコアは、NVD の基本スコアを環境に合わせて調整します。たとえばネットワークから悪用できる脆弱性でも、インターネットへの経路がなければ下がります。

- **例:** NVD の基本スコアが 9.8 のネットワーク経由の脆弱性でも、インターネットへの経路がない EC2 では Inspector のスコアが下がります。優先度は Inspector のスコアで判断します。

### EC2 のスキャン {#inspector-ec2}

| 方式 | 仕組み | 条件 |
| --- | --- | --- |
| エージェントベース | SSM の関連付けとプラグインで継続的に収集 | SSM の管理下にあること |
| エージェントレス | EBS スナップショットから収集 | 適格なインスタンス |
| ハイブリッド | 両方を使う。**有効化時の既定** | |

**症状:** SSM の管理下にないインスタンスは、ハイブリッドでなければスキャンされません。「カバレッジが低い」場合は、SSM Agent、インスタンスプロファイル、VPC エンドポイントを確認します。

- **VPC エンドポイントの例:** インターネットへの経路がないサブネットの EC2 には、`com.amazonaws.ap-northeast-1.ssm` と `com.amazonaws.ap-northeast-1.ssmmessages` などのエンドポイントが必要です。

### ECR のスキャン {#inspector-ecr}

ECR の基本スキャンは ECR が提供し、拡張スキャンが Inspector です。Inspector を有効にすると、プライベートレジストリのリポジトリは拡張スキャンに切り替わります。

| ECR の有効化時期 | 再スキャンの期間の既定 | 基準 |
| --- | --- | --- |
| 2026 年 10 月 15 日以降 | 7 日 | 最終利用日 |
| 2024 年 5 月 16 日 - 2026 年 10 月 14 日 | 14 日 | 最終利用日 |
| 2024 年 5 月 16 日より前 | 90 日 | 最終プル日 |

古いイメージが検査されない場合は、この期間を確認します。アーカイブされたイメージは対象外で、検出結果も閉じられます。

- **再スキャンの例:** 2026 年 10 月 15 日以降に有効にしたアカウントでは、10 月 20 日に最後に使われたイメージは、既定で 7 日後の 10 月 27 日まで監視されます。その後に見つかった CVE は、そのイメージの検出結果に出ません。
- **アーカイブの例:** イメージをアーカイブすると検出結果は閉じられ、3 日後に削除されます。戻すと新しいスキャンが始まります。

### Lambda とコードのスキャン {#inspector-code}

有効化時に、直近 90 日に呼び出しか更新があった関数をスキャンします。カスタマー管理キーで暗号化された関数は **対象外** です。

- **例:** 100 日前に更新して以来呼ばれていない関数は、有効化の時点ではスキャンされません。
- **誤ると:** カスタマー管理キーで暗号化した関数は、カバレッジに出ません。Lambda のスキャンの結果が足りないときは、暗号化の設定を確かめます。

CI/CD には SBOM Generator と Scan API を組み込みます。GitHub Actions、Jenkins、CodePipeline などのプラグインがあります。

Code Security は [CodeGuru Security](#codeguru-security) の後継で、Amazon Q Developer のスキャンエンジンを使います。

### ネットワーク到達性 {#inspector-network}

インターネットゲートウェイ、VPC ピアリング、VPN などの VPC の端から、EC2 の TCP や UDP のポートに届く経路を報告します。**12 時間ごと** に評価され、EC2 だけが対象です。

- **例:** 09:00 にセキュリティグループで `0.0.0.0/0` の 22 番を開けると、次の評価までに検出されます。最大で 21:00 ごろです。すぐ知りたいなら [Config のルール](governance.md#config) を併用します。

似たツールとの違いです。

| ツール | 目的 |
| --- | --- |
| Inspector のネットワーク到達性 | 開いた経路を自動で継続的に検出 |
| Network Access Analyzer | 自分で定義した要件に反する経路を検出 |
| Reachability Analyzer | 指定した 2 点間の接続をホップごとに確認 |
| [IAM Access Analyzer](identity-directory.md#access-analyzer) | ポリシーによる外部アクセスを検出 |

### 検出結果と管理 {#inspector-findings}

検出結果の種類は、パッケージの脆弱性、コードの脆弱性、ネットワーク到達性の 3 つです。EventBridge と Security Hub CSPM に送られます。

抑制ルールは表示を隠すだけで、検出結果を閉じません。作れるのは組織の委任管理者だけです。組織全体の有効化は委任管理者が行い、新しいメンバーを自動で有効にできます。委任管理者はメンバーのコードスニペットを見られません。

- **例:** 検証環境のタグが付いた EC2 の `LOW` を抑制すると、一覧から消えますが、検出結果は開いたままです。

## Macie {#macie}

[:material-sprout: CLF](../courses/clf/services.md){ .exam-badge .exam-foundational } [:material-sprout: AIF](../courses/aif/services.md){ .exam-badge .exam-foundational } [:material-certificate: SAA](../courses/saa/services.md){ .exam-badge .exam-associate } [:material-certificate: SOA](../courses/soa/services.md){ .exam-badge .exam-associate } [:material-certificate: DEA](../courses/dea/services.md){ .exam-badge .exam-associate } [:material-certificate: MLA](../courses/mla/services.md){ .exam-badge .exam-associate } [:material-star-circle: DOP](../courses/dop/services.md){ .exam-badge .exam-professional } [:material-star-circle: AIP](../courses/aip/services.md){ .exam-badge .exam-professional } [:material-target: SCS](../courses/scs/services.md){ .exam-badge .exam-specialty }

[提供単位](resource-scope.md#two-axes): リージョン。リージョンごとに有効にし、そのリージョンのバケットを検査します。VPC の外です。

S3 のバケットを監視し、オブジェクトの中の機密データを機械学習とパターンマッチで検出します。S3 以外のデータは、RDS のスナップショットを Parquet で出力するなどして S3 に移せば検査できます。

### 検出の方法 {#macie-discovery}

| 方式 | 動き | 向いている場面 |
| --- | --- | --- |
| 自動検出 | 毎日バケット一覧を評価し、サンプリングで検査 | 全体の見通し。ヒートマップで確認 |
| ジョブ | バケット、深さ、条件を指定し、1 回か定期で実行 | 特定バケットの詳しい検査 |

- **自動検出の例:** ログ用のバケットを除外リストに入れると、費用を抑えて他のバケットのサンプリングに回せます。
- **ジョブの例:** `customer-exports` を毎週、サンプリングの深さ 100% で検査します。頻度は 1 回、毎日、毎週、毎月から選びます。深さ 10% にすると対象のオブジェクトの 10% だけを検査するので、費用は下がりますが見逃しが増えます。

### 識別子と許可リスト {#macie-identifiers}

| 機能 | 内容 | 例 |
| --- | --- | --- |
| マネージドデータ識別子 | 組み込みの検出基準 | クレジットカード番号、AWS シークレットキー |
| カスタムデータ識別子 | 正規表現、文字列、近接ルールで定義 | 社員番号 `EMP-[0-9]{6}` |
| 許可リスト | 無視する文字列やパターン | 公開している代表電話番号 |

カスタムデータ識別子の値です。

| 項目 | 値 |
| --- | --- |
| 正規表現 | 512 文字まで |
| キーワード | 50 個まで。各 3〜90 文字。大文字小文字を区別しない |
| 除外の語 | 10 個まで。各 4〜90 文字。大文字小文字を区別する |
| 最大一致距離 | 1〜300 文字。既定は 50 文字 |
| 重要度の既定 | Medium。件数を問わず同じ |

- **例:** 正規表現 `EMP-[0-9]{6}`、キーワード `社員番号`、距離 50 にすると、「社員番号: EMP-123456」は一致します。キーワードから 200 文字離れた `EMP-123456` は一致しません。
- **除外の例:** 除外の語に `SAMPLE` を入れると、`SAMPLE EMP-000000` のようなテストデータを結果から外せます。
- **重要度の例:** 1 件以上で Low、100 件以上で High のように、件数に応じて分けられます。
- **誤ると:** 距離を正規表現が一致する文字数より短くすると、文字列の一部しか距離に収まらず、一致しません。

**検査できない場合の確認点です。**

- KMS で暗号化されたオブジェクトは、Macie がそのキーを使えること。
- 制限の強いバケットポリシーは、Macie のアクセスを許可していること。
- 対応するストレージクラスと形式であること。

- **例:** カスタマー管理キーで暗号化したオブジェクトなら、キーポリシーで Macie のサービスリンクロールに `kms:Decrypt` を許可します。ないと分類エラーになり、機密データがあっても検出結果が出ません。

### 検出結果 {#macie-findings}

| 種類 | 発生条件 | 例 |
| --- | --- | --- |
| ポリシー | バケットの設定やセキュリティの変化。有効化後の変更のみ | `Policy:IAMUser/S3BucketPublic`、`Policy:IAMUser/S3BlockPublicAccessDisabled` |
| 機密データ | オブジェクトで機密データを検出 | `SensitiveData:S3Object/Personal`、`SensitiveData:S3Object/Credentials` |

| 項目 | 値 |
| --- | --- |
| 検出結果の保持 | 90 日 |
| 機密データ検出結果（ログ） | 90 日。長期保存には KMS キーと S3 バケットを設定 |
| ポリシーの更新の配信頻度 | 既定 15 分。変更可 |
| Security Hub CSPM への送信の既定 | ポリシーの検出結果のみ |

抑制ルールは検出結果をアーカイブし、EventBridge と Security Hub CSPM へ送りません。ただし機密データ検出結果（ログ）は残ります。

- **保持の例:** 機密データ検出結果（ログ）を 1 年残すなら、S3 バケットと KMS キーを設定し、バケットのライフサイクルで 1 年後に削除します。設定しないと 90 日で消えます。

複数アカウントでは、管理アカウントが委任管理者を指定し、委任管理者がリージョンごとにメンバーを追加します。

## Detective {#detective}

[:material-sprout: CLF](../courses/clf/services.md){ .exam-badge .exam-foundational } [:material-certificate: SAA](../courses/saa/services.md){ .exam-badge .exam-associate } [:material-star-circle: DOP](../courses/dop/services.md){ .exam-badge .exam-professional } [:material-target: SCS](../courses/scs/services.md){ .exam-badge .exam-specialty }

[提供単位](resource-scope.md#two-axes): リージョン。行動グラフはリージョンごとで、VPC の外です。

ログから行動グラフを作り、検出結果の根本原因と影響範囲を調べるサービスです。検出や修復ではなく **調査** を担います。

| データ | 区分 | 補足 |
| --- | --- | --- |
| CloudTrail ログ | 中核 | 独立したストリームで取得。既存の設定に影響しない |
| VPC フローログ | 中核 | EC2 のみ。NAT、RDS、Fargate は対象外 |
| GuardDuty の検出結果 | 中核 | GuardDuty を使うアカウントのみ |
| EKS 監査ログ | 任意 | |
| AWS セキュリティの検出結果 | 任意 | Security Hub CSPM から |

- 最大 **1 年分** の履歴を可視化します。
- 検出結果グループは、関連する検出結果とエンティティをまとめ、一連の攻撃を図示します。
- 行動グラフの管理者が招待か Organizations でメンバーを追加します。上限は 1,200 アカウントです。
- 調査は検出結果、検出結果グループ、エンティティのどこからでも始められます。

- **例:** `InstanceCredentialExfiltration` の検出結果からロールを開くと、普段と違う IP、新しく呼んだ API、増えたデータ量を時間軸で確認できます。
- **対象の例:** Fargate や NAT ゲートウェイの通信はフローログの可視化に出ません。調べるなら VPC フローログを直接検索します。

## Security Lake {#security-lake}

[:material-star-circle: SAP](../courses/sap/services.md){ .exam-badge .exam-professional } [:material-target: SCS](../courses/scs/services.md){ .exam-badge .exam-specialty }

[提供単位](resource-scope.md#two-axes): リージョン。リージョンごとに S3 バケットができ、ロールアップリージョンへ集約します。VPC の外です。

セキュリティログを自分のアカウントの S3 に集約し、Parquet と OCSF に変換するデータレイクです。データの所有権は利用者にあります。

| 設定 | 内容 | 具体例 |
| --- | --- | --- |
| AWS のソース | CloudTrail 管理イベント、データイベント（S3、Lambda）、EKS 監査ログ、Route 53 Resolver クエリログ、Security Hub CSPM の検出結果、VPC フローログ、WAF ログ | ソースごとに有効化 |
| カスタムソース | OCSF の Parquet で S3 へ書き込む | 1 つのオブジェクトは 1 つの OCSF クラスのみ |
| ロールアップリージョン | 複数リージョンのデータを 1 つに集める | `ap-northeast-3` を `ap-northeast-1` へ |
| 保持とライフサイクル | リージョンごとに設定 | 45 日で `ONEZONE_IA`、500 日で失効 |
| 委任管理者 | 組織全体を有効化、設定 | ログアーカイブ系のアカウント |

ソースとして追加するときは、CloudTrail 管理イベント以外は各サービス側で別途ログを設定する必要がありません。

- **保持の例:** 45 日で `ONEZONE_IA` へ移し、500 日で失効させます。この設定は Security Lake のコンソール、API、CLI で行います。
- **誤ると:** S3 のライフサイクルを直接変えると、メタデータが消えてデータにアクセスできなくなることがあります。
- **Object Lock の罠:** Security Lake は S3 Object Lock に対応しません。既定の保持つきで有効にすると、正規化ログの配信が止まります。
- **ロールアップの例:** 大阪を東京へロールアップすると、東京のバケットに両方のデータが集まります。大阪のデータは大阪にも残るので、大阪の保持を短くすると費用を抑えられます。

| サブスクライバーの種類 | 受け取り方 | 用途 |
| --- | --- | --- |
| データアクセス | 新しいオブジェクトの通知を HTTPS か SQS で受け取る | SIEM への取り込み |
| クエリアクセス | Lake Formation のテーブルを Athena などで直接検索 | 分析 |

サブスクライバーは、作成したリージョンのデータしか見えません。複数リージョンのデータを渡すには、ロールアップリージョンで作ります。

- **例:** SIEM をデータアクセスのサブスクライバーにすると、新しいオブジェクトの通知を SQS で受け取ります。アナリストの Athena はクエリアクセスのサブスクライバーにします。

**症状:** カスタムソースのデータが検索できない場合は、Parquet 形式か、OCSF のクラスが混ざっていないかを確認します。AWS Glue のクローラーがパーティションを登録します。

## Audit Manager {#audit-manager}

[:material-target: SCS](../courses/scs/services.md){ .exam-badge .exam-specialty }

[提供単位](resource-scope.md#two-axes): リージョン。VPC の外です。

!!! warning "保守モード"
    2026 年 4 月 30 日から新しいアカウントで設定できません。既存の利用者は使い続けられますが、新しいリージョンやアカウントへは広げられず、新機能と新しいフレームワークは追加されません。AWS は代替として AWS Config の適合パックを案内しています。

監査フレームワークに沿って証拠を自動収集し、評価レポートにまとめます。

| 証拠のデータソース | 証拠の種類 | 頻度 |
| --- | --- | --- |
| CloudTrail | ユーザーの活動 | 継続 |
| AWS Config | 準拠チェック | ルールのトリガーに従う |
| Security Hub CSPM | 準拠チェック | チェックのスケジュールに従う |
| AWS API 呼び出し | 設定のスナップショット | 選択した頻度 |

評価レポートは選んだ証拠をまとめるものです。**証拠そのものの準拠を判定はしません。**

- **例:** PCI DSS のフレームワークで評価を作り、`RDS.3` の Config の評価結果と CloudTrail の操作を証拠として集めます。監査人にはレポートを渡します。準拠の判断は監査人と自社が行います。

## AWS Artifact {#artifact}

[提供単位](resource-scope.md#two-axes): 資料を受け取るサービスで、VPC の中にも外にもリソースを置きません。

AWS 自身の準拠資料と契約を扱う無料のサービスです。

- SOC、ISO、PCI などの報告書と認定書をダウンロードできます。
- HIPAA の BAA のような契約を確認、受諾、解除できます。Organizations では組織全体でまとめて受諾でき、既存と将来のメンバーが対象になります。
- AWS Marketplace の販売者の資料も入手できます。
- Assurance Assistant で、準拠に関する質問に AI の回答を生成できます。

自社のワークロードの準拠を示す資料は別です。それは自社で用意します。

- **例:** 監査人に AWS の SOC 2 を渡すならレポートをダウンロードします。自社のアプリの SOC 2 は、自社で監査を受けて用意します。

## Firewall Manager {#firewall-manager}

[:material-sprout: CLF](../courses/clf/services.md){ .exam-badge .exam-foundational } [:material-certificate: SAA](../courses/saa/services.md){ .exam-badge .exam-associate } [:material-target: ANS](../courses/ans/services.md){ .exam-badge .exam-specialty } [:material-target: SCS](../courses/scs/services.md){ .exam-badge .exam-specialty }

[提供単位](resource-scope.md#two-axes): リージョン。ポリシーはリージョンごとに作ります。CloudFront 向けはグローバルです。サービス自体は VPC の外で、展開先は VPC の中のこともあります。

保護の設定を組織全体に一元展開するサービスです。新しいアカウントやリソースにも自動で適用します。

| 前提 | 内容 | 誤ったときの症状 |
| --- | --- | --- |
| Organizations | すべての機能が有効 | 一括請求のみの組織では使えない |
| 管理者 | 管理アカウントが既定の管理者を作成。スコープを絞った複数の管理者も可 | 管理者以外はポリシーを作れない |
| AWS Config | 対象のアカウントとリージョンで有効 | 準拠状態を評価できない |
| AWS RAM | Network Firewall と DNS Firewall のポリシーで、Organizations との共有を有効化 | 展開に失敗する |

| ポリシーの種類 | 内容 |
| --- | --- |
| AWS WAF | 最初と最後に動くルールグループを強制し、その間にアカウント所有者が追加できる |
| Shield Advanced | 指定した種類のリソースを保護。Shield Advanced の利用者には追加料金なし |
| セキュリティグループ | 共通の適用、内容の監査、使用状況の監査（未使用や冗長の整理） |
| ネットワーク ACL | 基準の NACL を強制 |
| Network Firewall | 組織の VPC にファイアウォールを展開 |
| Route 53 Resolver DNS Firewall | 組織の VPC に DNS Firewall を適用 |
| 他社製ファイアウォール | Palo Alto Cloud NGFW、Fortigate CNF |

スコープはアカウント、OU、タグ、リソースの種類で決めます。修復は「不準拠の表示だけ」か「自動修復」を選びます。監査系のセキュリティグループのポリシーは、まず自動修復を無効にして影響を確認します。

- **WAF の例:** 本番の OU で `env=prod` の ALB に、先頭で `AWSManagedRulesCommonRuleSet` を適用します。新しい ALB を作ると、自動修復で WEB ACL が関連付けられます。アカウント所有者は間にだけルールを足せます。
- **セキュリティグループの例:** 内容の監査ポリシーで `0.0.0.0/0` の 22 番を禁止すると、該当する SG が不準拠になります。まず自動修復を無効にして件数を確かめます。
- **誤ると:** 自動修復をいきなり有効にすると、既存の例外の通信が切れることがあります。対象のアカウントで Config が無効なら、準拠の状態を評価できません。

## Shield {#shield}

[:material-sprout: CLF](../courses/clf/services.md){ .exam-badge .exam-foundational } [:material-certificate: SAA](../courses/saa/services.md){ .exam-badge .exam-associate } [:material-certificate: SOA](../courses/soa/services.md){ .exam-badge .exam-associate } [:material-certificate: DEA](../courses/dea/services.md){ .exam-badge .exam-associate } [:material-star-circle: SAP](../courses/sap/services.md){ .exam-badge .exam-professional } [:material-star-circle: DOP](../courses/dop/services.md){ .exam-badge .exam-professional } [:material-target: ANS](../courses/ans/services.md){ .exam-badge .exam-specialty } [:material-target: SCS](../courses/scs/services.md){ .exam-badge .exam-specialty }

[提供単位](resource-scope.md#two-axes): Standard はアカウントに自動で適用されます。Advanced はアカウントで登録し、保護対象はグローバル（CloudFront、Route 53、Global Accelerator）かリージョン（ALB、CLB、Elastic IP）のリソースです。サービス自体は VPC の外です。

### Shield Standard {#shield-standard}

全ユーザーに追加料金なしで自動適用される、ネットワーク層とトランスポート層（L3、L4）の DDoS 防御です。Route 53 のホストゾーン、CloudFront、Global Accelerator の標準アクセラレーターで特に効果が大きくなります。

- **例:** SYN フラッドや UDP リフレクションは、CloudFront の前で自動で緩和されます。設定はありません。HTTP の洪水には [WAF](certificates.md#waf) のレートルールを足します。

### Shield Advanced {#shield-advanced}

[:material-target: SCS](../courses/scs/services.md){ .exam-badge .exam-specialty }

| 項目 | 内容 |
| --- | --- |
| 料金 | 1 年の契約で月額 3,000 ドルと、データ転送の利用料 |
| 請求 | 組織の支払いアカウント。同じ一括請求ファミリーなら 1 契約で全アカウントを対象にできる |
| 登録 | 保護したいアカウントごとに登録 |
| 適用 | **指定したリソースだけ**。自動では保護されない |
| 対象 | CloudFront、Route 53 ホストゾーン、Global Accelerator の標準アクセラレーター、Elastic IP（EC2、NLB はこの関連付け）、ALB、CLB |
| IP | IPv4 のみ |

| 機能 | 内容 | 設定を誤ったときの症状 |
| --- | --- | --- |
| ヘルスベース検出 | Route 53 ヘルスチェックを検出に使う。ホストゾーン以外で利用可 | 誤検知が増え、検出が遅くなる |
| プロテクショングループ | リソースをまとめて検出、緩和 | 個別の閾値で小さな攻撃を見逃す |
| 可視化 | リアルタイムのメトリクスとレポート、CloudWatch | |
| WAF 費用 | 保護対象の標準的な WAF 料金を含む（1,500 WCU と既定の本文サイズまで、月 500 億リクエストまで） | Bot Control や CAPTCHA は別料金 |
| コスト保護 | 攻撃による増加分をクレジットで申請 | 対象はデータ転送、CloudFront、Route 53、ALB の LCU など |
| EC2 の保護 | 攻撃時に VPC の NACL を AWS ネットワークの境界に展開 | |

- **料金の計算の例:** 月額 3,000 ドル × 12 か月 = 年 36,000 ドルに、データ転送の利用料を足します。同じ一括請求ファミリーの 10 アカウントで登録しても、月額は 1 回分です（2026 年 10 月時点の公式の料金。変わることがあります）。
- **保護対象の例:** ALB を 3 台保護するなら、3 台それぞれを登録します。ALB を新しく作っただけでは保護されないので、[Firewall Manager](#firewall-manager) で自動化します。
- **プロテクショングループの例:** ALB 3 台をまとめて 1 グループにすると、1 台あたりは小さい攻撃でも、合計で検出できます。
- **コスト保護の例:** DDoS で CloudFront の転送料が増えたら、対象のリソースが保護されていれば、増加分のクレジットを申請できます。

### Shield Response Team {#shield-srt}

| 項目 | 内容 |
| --- | --- |
| 前提 | Business または Enterprise のサポートプラン |
| 権限付与 | `drt.shield.amazonaws.com` を信頼するロールに `AWSShieldDRTAccessPolicy` を付与し、`AssociateDRTRole` |
| できること | WAF ログの分析と、承認後の WEB ACL の変更、カスタム緩和 |
| ログの共有 | WEB ACL のログはロールの権限で読めるので、バケットの許可は不要。ALB や CloudFront など他のログを S3 で見せるには、バケットごとにアクセスを許可（10 個まで。平文か SSE-S3 に限り、KMS で暗号化したバケットは読めない） |
| プロアクティブエンゲージメント | ヘルスチェックが異常になると SRT から連絡。ヘルスベース検出が前提 |

```bash
aws shield associate-drt-role \
  --role-arn arn:aws:iam::111122223333:role/shield-srt-access
```

- **誤ると:** ロールを付けていないと、攻撃中に SRT が WEB ACL を見られず、権限の設定から始めることになります。
- **ヘルスチェックの例:** ALB の `/health` を見る Route 53 ヘルスチェックを保護に関連付けます。異常になると SRT から連絡が来ます。

プロアクティブエンゲージメントは、Anti-DDoS マネージドルールグループが検出したイベントでは起動しません。

### アプリケーション層の防御 {#shield-l7}

L3、L4 は自動で緩和されます。L7 は正当な通信を止めないよう、既定では自動緩和せず、CloudWatch アラームで通知します。

- **例:** ベースラインのない新しいサイトには、公開の前に通常の負荷を流します。従来の L7 自動緩和はベースラインに 24 時間から 30 日を使います。

| 仕組み | 状態 | 内容 |
| --- | --- | --- |
| Anti-DDoS マネージドルールグループ | 2026 年 3 月 26 日から既定 | 秒単位で検出、緩和。Shield Advanced にアクセスが含まれる |
| L7 自動緩和（従来） | 既存の利用者のみ継続。新規はサポートへ連絡 | WEB ACL に 150 WCU のルールグループを追加。ベースラインに 24 時間から 30 日 |

WAF のルールの詳細は [WAF のページ](certificates.md#waf) を参照してください。

## Network Firewall {#network-firewall}

[:material-certificate: SAA](../courses/saa/services.md){ .exam-badge .exam-associate } [:material-certificate: SOA](../courses/soa/services.md){ .exam-badge .exam-associate } [:material-star-circle: SAP](../courses/sap/services.md){ .exam-badge .exam-professional } [:material-star-circle: DOP](../courses/dop/services.md){ .exam-badge .exam-professional } [:material-target: ANS](../courses/ans/services.md){ .exam-badge .exam-specialty } [:material-target: SCS](../courses/scs/services.md){ .exam-badge .exam-specialty }

[提供単位](resource-scope.md#two-axes): リージョン。ファイアウォールは VPC に作り、エンドポイントは AZ ごとの専用サブネットに置きます。VPC の中です。

VPC 向けのマネージドなステートフルファイアウォール兼 IPS で、Suricata 互換のルールが使えます。

| 比較 | 層 | 代表的な用途 |
| --- | --- | --- |
| [セキュリティグループ](networking.md#security-groups-nacls) | ENI、ステートフル | 許可の最小化 |
| [NACL](networking.md#nacl-rules) | サブネット、ステートレス | 明示的な拒否、すぐ効く遮断 |
| Network Firewall | VPC の境界、L3 から L7 | ドメインの許可リスト、IPS シグネチャ、東西の検査 |
| [AWS WAF](certificates.md#waf) | HTTP（L7） | SQL インジェクション、レート制限 |
| Route 53 Resolver DNS Firewall | DNS クエリ | 悪性ドメインの名前解決を阻止 |

### 構成 {#nfw-architecture}

| 手順 | 内容 | 誤ったときの症状 |
| --- | --- | --- |
| サブネットの準備 | AZ ごとに専用のサブネットを作る | 同じサブネットのアプリは保護されない |
| ファイアウォール作成 | 各サブネットにエンドポイントができる | |
| ポリシー設定 | ルールグループと既定のアクション | |
| ルートテーブル変更 | 保護したいサブネットと外部の間に挟む | ルートがなければ検査されない。AZ をまたぐと非対称になる |

入ってくる通信は宛先と同じ AZ のエンドポイントへ送ります。集中型の検査では、ポリシー変数 `HOME_NET` を上書きします。既定は検査用 VPC の CIDR なので、そのままだと他の VPC の通信にルールが合いません。

- **`HOME_NET` の例:** 検査用 VPC が `10.100.0.0/16`、検査される VPC が `10.0.0.0/16` と `10.1.0.0/16` なら、`HOME_NET` を 3 つ全部にします。`$HOME_NET` を使うルールは、上書きしないと `10.0.0.0/16` からの通信に一致しません。`EXTERNAL_NET` はその否定になります。
- **ルートの例:** 1a の保護サブネットの `0.0.0.0/0` は、1a のファイアウォールエンドポイント（`vpce-`）へ向けます。IGW のエッジルートテーブルでは、`10.0.1.0/24` を同じ 1a のエンドポイントへ向けます。

### ルールの評価 {#nfw-rules}

パケットはまずステートレス、次にステートフルのエンジンで評価されます。

```mermaid
flowchart TD
    A["パケット"] --> B["ステートレスルール<br/>優先度の順"]
    B -- Pass --> P["通過"]
    B -- Drop --> D["破棄"]
    B -- "Forward" --> C["ステートフルルール"]
    B -- "一致なし" --> E["ステートレスの<br/>既定アクション"]
    E -- Forward --> C
    E -- Pass --> P
    E -- Drop --> D
    C --> F{"一致したルール"}
    F -- pass --> P
    F -- "drop / reject" --> D
    F -- alert --> G["記録して評価を続ける"]
```

| 設定 | 内容 | 既定と範囲 | 誤ったときの症状 |
| --- | --- | --- | --- |
| ステートレスの既定アクション | Pass、Drop、Forward | 指定が必須。通常は Forward | Pass だとステートフルの検査もログも効かない |
| 評価順 | アクション順か厳密順。厳密順を推奨 | 作成時にのみ指定可 | 後から変えられない |
| アクション順 | `pass`、`drop`、`reject`、`alert` の順で評価 | | `pass` に一致するとフローの残りを検査しない |
| 厳密順の既定アクション | 一致しない通信の扱い | 厳密順で設定 | |
| ストリーム例外ポリシー | 接続が途中で切れたときの扱い | Drop、Continue、Reject | Drop は既定で、変更時も既存接続に影響 |
| TCP アイドル時間 | 接続をアイドルと判断するまで | 既定 350 秒、60 - 6000 秒 | |
| 断片化パケット | UDP は設定可。他は黙って破棄 | | 断片化した通信が届かない |

- **ストリーム例外の例:** ファイアウォールの更新で接続が途中で切れると、`Drop` は以後の通信を破棄します。`Reject` は TCP の拒否を返すので、クライアントはすぐ再接続できます。`Continue` はそのまま通しますが、接続の開始を見ていないので、HTTP を止めるルールなどに一致しません。
- **TCP アイドルの例:** 既定の 350 秒のままだと、10 分間黙る DB の接続はアイドルと判断され、次のパケットがストリーム例外ポリシーの扱いになります。600 秒より長い 900 秒にします。値を更新すると、既存の接続もストリーム例外ポリシーに従います。
- **評価順の例:** アクション順で `pass` と `drop` の両方に一致すると、`pass` が先に効きます。厳密順なら、優先度の順に書いたとおりです。

ドメインリストの例です。

```text
pass tls any any -> any any (tls.sni; content:"packages.example.com"; startswith; nocase; endswith; msg:"allow"; sid:100; rev:1;)
drop tls any any -> any any (msg:"deny other"; flow:established,to_server; sid:200; rev:1;)
```

SNI の詐称に備える場合は、Route 53 の解決結果と照合する Resolved IP validation（`AWS_ROUTE_53_RESOLVED_DOMAIN`）が使えます。AWS 管理のルールグループには、マルウェアやボットネットなどの脅威シグネチャがあります。

- **ドメインの書き方の例:** `abc.example.com` はそのドメインだけに一致します。`.example.com` は `example.com` と全サブドメインに一致します。
- **`Allow` の例:** アクション順のドメインリストの `Allow` は、一致しない通信を拒否します。厳密順ではこの拒否は働かないので、既定のアクションで止めます。
- **誤ると:** アクション順で `Allow` のリストと `Alert` のリストを併用すると、`Allow` が追加する既定の拒否が先に効き、`Alert` が記録されません。

### ログと TLS {#nfw-logging}

| ログ | 内容 |
| --- | --- |
| フローログ | 通信のフロー |
| アラートログ | `DROP`、`ALERT`、`REJECT` に一致した通信 |
| TLS ログ | TLS 検査の事象 |

送信先は S3、CloudWatch Logs、Data Firehose です。ログは **ステートフルエンジンに転送した通信だけ** が対象です。ステートレスで Pass や Drop した通信は残りません。

- **例:** ステートレスの既定アクションを `Pass` にすると、全通信がステートフルに届かず、アラートログが空になります。`Forward` に戻すと記録されます。

TLS 検査の設定は、ACM の証明書を使って通信を復号し、ルールで検査したあと再暗号化します。インバウンド、アウトバウンド、両方を選べます。証明書の扱いは [証明書のページ](certificates.md) を参照してください。

## インシデント対応 {#incident-response}

AWS の対応ガイドは、準備、運用（検出、分析、封じ込め、根絶、復旧）、事後の活動に沿います。試験では特に、証拠を残しつつ被害を止める順序が問われます。

封じ込めは次の 3 種類に分けて考えます。

| 種類 | 内容 | 例 |
| --- | --- | --- |
| 送信元の封じ込め | フィルタリングやルーティングで送信元を止める | NACL、WAF で攻撃者の IP を拒否 |
| 手法とアクセスの封じ込め | 不正なアクセスの手段を取り除く | キーの無効化、セッションの失効、SCP での拒否 |
| 宛先の封じ込め | 対象のリソースへのアクセスを止める | 隔離用のセキュリティグループ |

- **例:** 攻撃者が `198.51.100.7` から EC2 のロールの認証情報を使っているなら、3 つを組み合わせます。NACL で IP を拒否し、セッションを失効し、インスタンスを隔離用 SG に移します。

### 準備 {#ir-preparation}

- 対応用のロールと、ログとフォレンジック専用のアカウントを用意します。
- GuardDuty、Security Hub、CloudTrail の組織の証跡を先に有効にします。
- ログの S3 バケットは [Object Lock](s3.md) で改ざんを防ぎます。
- [Shield Advanced](#shield-advanced) の保護と SRT の権限は、攻撃の前に設定します。
- SCP でログの停止を禁止し、影響範囲を限定します。

- **SCP の例:** `cloudtrail:StopLogging` と `cloudtrail:DeleteTrail` を全アカウントで `Deny` します。ルートでも止められません（管理アカウントを除く）。
- **ロールの例:** 平常時は使わない `incident-response` ロールを用意し、MFA を条件にします。障害のときに権限の申請から始めずに済みます。

### EC2 の隔離 {#ir-ec2-isolation}

```mermaid
flowchart TD
    A["検出結果を確認"] --> B["メタデータとタグを記録<br/>終了保護を有効化"]
    B --> C["メモリを取得"]
    C --> D["隔離用 SG に置き換え"]
    D --> E["既存の接続を<br/>NACL で遮断"]
    E --> F["EBS スナップショットを<br/>フォレンジック用アカウントへ共有"]
    F --> G["分析し、復旧または置き換え"]
```

メモリの内容は停止すると失われます。証拠が必要なら、**停止や終了の前に** 取得します。

| 手順 | 操作 | 注意点 |
| --- | --- | --- |
| 隔離用の SG を作る | 特定の IP だけ許可。`0.0.0.0/0` の全ポートは置かない | |
| SG を置き換える | 他の SG をすべて外す | **追跡中の接続は切れない** |
| NACL で遮断 | 攻撃者の IP や通信を拒否 | ステートレスなので即座に効く |
| Auto Scaling から外す | デタッチ、ELB から登録解除 | 入れ替えで証拠が消えるのを防ぐ。終了保護では Auto Scaling による終了を防げない |
| ロールを無効化 | セッションの失効 | IMDS の認証情報が盗まれた場合 |

**最重要の落とし穴:** セキュリティグループのルールを変えても、追跡中の接続は切れません。接続がタイムアウトするまで通信が続きます。すぐ止めるにはネットワーク ACL を使います。全開放のルール同士の通信は追跡されず、すぐ切れます。

- **時間の例:** TCP の確立済みの接続の追跡は、既定で 432,000 秒（5 日）のアイドルまで続きます（Nitro v6 の多くは 350 秒）。範囲は 60〜432,000 秒です。UDP は既定 30 秒（30〜60 秒）、UDP ストリームは既定 180 秒（60〜180 秒）です。
- **NACL の例:** ルール番号 50 で `198.51.100.7/32` の全通信を `DENY` にします。番号が小さいほど先に評価されるので、番号 100 の許可より前に止まります。

`AWSSupport-ContainEC2Instance` は、SG の設定を S3 に保存してから隔離する、元に戻せる Automation ランブックです。

### 認証情報の漏えい {#ir-credentials}

| キーの先頭 | 種類 | 対応 |
| --- | --- | --- |
| `AKIA` | IAM ユーザーやルートの長期キー | キーを無効化して削除、ローテーション |
| `ASIA` | STS の一時キー | セッションの失効、発行元の調査 |

ロールの認証情報は、一時キーが有効期限まで使えます。ロールの権限を変えるだけでは足りないことがあるので、IAM の **セッションの取り消し** を使います。取り消しを実行した時点（約 30 秒先まで）より前に発行されたセッションをすべて拒否する `AWSRevokeOlderSessions` のインラインポリシーがロールに付きます。

```json
{
  "Effect": "Deny",
  "Action": "*",
  "Resource": "*",
  "Condition": {
    "DateLessThan": {"aws:TokenIssueTime": "2026-10-31T03:00:00Z"}
  }
}
```

- **例:** 12 時間有効の一時キーが 09:00 に漏れて、10:00 に気づいたとします。ポリシーを変えないと 21:00 まで使われる恐れがあります。上の条件を付けると、指定時刻より前に発行されたセッションをすべて拒否します。
- **誤ると:** 正規のワークロードのセッションも拒否されます。EC2 のインスタンスプロファイルなら、新しい認証情報の取得まで失敗することがあります。

次の順で確認します。

1. 検出結果の API、時刻、送信元 IP を、本人に確認する。
2. `sessionIssuer` でロールの発行元を追う。
3. 作られたユーザー、キー、ロール、ポリシーを探す。
4. Access Advisor で実際の権限を確認する。

### EventBridge による自動化 {#ir-eventbridge}

```mermaid
sequenceDiagram
    participant G as GuardDuty
    participant E as EventBridge
    participant S as Step Functions
    participant M as Systems Manager
    G->>E: 検出結果のイベント
    E->>S: 重要度 7 以上で起動
    S->>M: 隔離ランブックを実行
    M-->>S: 実行結果
    S->>S: スナップショットと通知
```

```json
{
  "source": ["aws.guardduty"],
  "detail-type": ["GuardDuty Finding"],
  "detail": {
    "severity": [{"numeric": [">=", 7]}],
    "type": [{"prefix": "CryptoCurrency:EC2"}]
  }
}
```

| ターゲット | 向いている処理 |
| --- | --- |
| Lambda | 1 回の短い処理（SG の変更、キーの無効化） |
| Step Functions | 判断、待機、承認を含む複数の手順 |
| Systems Manager Automation | 定義済みランブックの実行 |
| SNS | 担当者への通知 |

**症状:** ルールが動かない場合、`detail-type` の綴り、リージョン（GuardDuty はリージョン単位）、ターゲットのリソースポリシーや実行ロールを確認します。抑制された検出結果はイベントになりません。

- **パターンの例:** 上のパターンは、`CryptoCurrency:EC2/BitcoinTool.B!DNS` の重要度 8 に一致します。`Recon:EC2/PortProbeUnprotectedPort` や、重要度 5 の暗号通貨の検出結果には一致しません。

### フォレンジックの証拠 {#ir-forensics}

| 証拠 | 取得方法 | 注意点 |
| --- | --- | --- |
| ディスク | EBS スナップショット | 暗号化された場合、共有にはカスタマー管理キーの共有が必要。AWS 管理キーのスナップショットは共有できない |
| メモリ | SSM Run Command で取得ツールを実行 | 停止前に取る |
| ログ | CloudTrail、フローログ、アプリログを専用アカウントの S3 へ | Object Lock と検証で保全 |
| 設定 | AWS Config の履歴 | 変更の時系列を確認 |
| CloudTrail の検証 | [ログファイルの検証](#investigate-cloudtrail) | 改ざんがないことを示す |

調査用の EC2 は、フォレンジック用アカウントの隔離された VPC で起動します。スナップショットから作ったボリュームを接続して分析します。

- **共有の例:** AWS 管理キーで暗号化したスナップショットは共有できません。カスタマー管理キーでコピーし直し、そのキーの `kms:Decrypt` をフォレンジック用アカウントに許可してから共有します。

### プレイブックと実行基盤 {#ir-playbooks}

| 手段 | 用途 |
| --- | --- |
| Systems Manager Automation | 定型手順の自動実行 |
| Systems Manager OpsCenter | 事象を OpsItem として集めて対応 |
| SageMaker AI のノートブック | 手順と分析を実行可能な形で残す |
| Step Functions | 複数手順の編成 |
| Incident Manager | 新規受付は終了。既存の利用者のみ |
| AWS Customer Playbook Framework（GitHub） | AWS の公開サンプルのプレイブック |

### 計画のテスト {#ir-testing}

| 手段 | 内容 |
| --- | --- |
| AWS Fault Injection Service | 障害を注入して対応を確認 |
| AWS Resilience Hub | 回復性を評価 |
| サンプルの検出結果 | GuardDuty のサンプルで自動化を確認 |
| テストスクリプト | GuardDuty が公開する、検出結果を発生させるスクリプトを専用アカウントで実行 |

- **サンプルの例:** `aws guardduty create-sample-findings --detector-id 12abc34d567e8fa901bc2d34e56789f0 --finding-types CryptoCurrency:EC2/BitcoinTool.B!DNS` で 1 件発生させ、EventBridge から Step Functions が動くかを確かめます。

復旧の設計は [resilience](resilience.md) も参照してください。

## Automated Forensics Orchestrator for Amazon EC2 and EKS {#forensics-orchestrator}

[:material-target: SCS](../courses/scs/services.md){ .exam-badge .exam-specialty }

[提供単位](resource-scope.md#two-axes): デプロイしたリージョンで動くソリューションです。調査用のインスタンスはフォレンジック用アカウントの VPC に置きます。

SOC 向けのフォレンジックの流れを自動化する、AWS のガイダンスです。マネージドサービスではなく、自分のアカウントにデプロイします。現在の名前は **Automated Forensics Orchestrator for Amazon EC2 and EKS** で、EC2 上の EKS にも対応します。

流れは取得、隔離、調査、報告です。

1. アプリケーションのアカウントで、Config、GuardDuty、他社ツールが検出します。
2. 検出結果をセキュリティアカウントの Security Hub に集めます。
3. EventBridge が、Step Functions のワークフローを起動します。
4. メモリの取得フローがメモリを S3 に保存し、その後 **新しい SG でインスタンスを隔離** します。
5. ディスクの取得フローが EBS スナップショットを取り、フォレンジック用アカウントへ共有します。
6. 調査フローがフォレンジック用 AMI からインスタンスを起動し、データを接続して、SSM Run Command でツールを実行します。
7. DynamoDB に状態を記録し、SNS で通知します。

複数アカウント、複数リージョンに対応します。事前にフォレンジック用 AMI（EC2 Image Builder で作成可）が必要です。対象のインスタンスに SSM Agent が必要です。

AWS は、取得した証拠が法廷で使えることを保証していません。

## AWS Security Incident Response {#security-incident-response}

[提供単位](resource-scope.md#two-axes): 組織のアカウントを対象にするサービスで、VPC の外です。

検出結果のトリアージと調査を支援するマネージドサービスです。GuardDuty や Security Hub CSPM 経由の他社ツールの検出結果を受け取り、対応が必要なものだけを知らせます。

- **自分では検出結果を生成しません。** GuardDuty などの置き換えにはなりません。
- 準拠や設定の検出結果はトリアージしません。
- 事前に許可すると、エンジニアが S3、EC2、IAM の封じ込めを代わりに実行します。すべて元に戻せる操作です。
- 対象は登録した組織または OU のアカウントです。

- **例:** GuardDuty の検出結果を受け取り、誤検知と判断したものは知らせず、対応が要るものだけケースにします。事前に許可していれば、エンジニアが SG の変更で EC2 を隔離します。

!!! note "試験ガイドとの関係"
    SCS-C03 の対象サービス一覧にこのサービスはありません。また、旧版の「AWS Security Incident Response Guide」の知識項目は C03 で削除されています。ただし、ガイドの考え方（封じ込めの分類など）は分野 2 の理解に役立ちます。

## ログの調査 {#log-investigation}

### どのログを見るか {#log-sources}

| 知りたいこと | ログ |
| --- | --- |
| 誰がどの API を呼んだか | [CloudTrail](observability.md#cloudtrail) |
| S3 や Lambda のデータ操作 | CloudTrail のデータイベント（別途有効化） |
| IP 通信の有無と許可、拒否 | [VPC フローログ](networking.md#flow-logs) |
| どのドメインを問い合わせたか | Route 53 Resolver クエリログ |
| Transit Gateway を通る通信 | Transit Gateway フローログ |
| HTTP リクエストの情報（送信元、メソッド、URL など。本文は残らない） | ALB、CloudFront、WAF のログ |
| 設定がいつ変わったか | AWS Config |
| 通常と違う API の呼び出し量 | [CloudTrail Insights](observability.md#cloudtrail-insights) |

検索は CloudWatch Logs Insights か Athena、正規化は OpenSearch や Lambda で行います。[CloudTrail Lake](observability.md#cloudtrail-lake) は新規受付を終了しています。AWS が勧める移行先は CloudWatch です。

### CloudTrail の調査 {#investigate-cloudtrail}

| フィールド | 分かること |
| --- | --- |
| `userIdentity.type`、`.arn` | 主体の種類と ARN |
| `userIdentity.accessKeyId` | 使われたキー（`AKIA` か `ASIA`） |
| `userIdentity.sessionContext.sessionIssuer` | ロールの発行元 |
| `eventSource`、`eventName` | サービスと操作 |
| `sourceIPAddress`、`userAgent` | 呼び出し元 |
| `errorCode` | `AccessDenied` などの失敗 |
| `requestParameters`、`responseElements` | 入力と結果 |

漏えいしたキーの活動を調べる Athena の例です。テーブルは証跡の S3 に対して作ってあるものとします。

```sql
SELECT eventtime, eventsource, eventname, sourceipaddress, errorcode
FROM cloudtrail_logs
WHERE useridentity.accesskeyid = 'AKIAIOSFODNN7EXAMPLE'
  AND eventtime BETWEEN '2026-10-01T00:00:00Z' AND '2026-10-02T00:00:00Z'
ORDER BY eventtime;
```

攻撃者の次の操作として、`CreateUser`、`CreateAccessKey`、`AttachUserPolicy`、`StopLogging`、`DeleteTrail` を探します。

- **読み方の例:** `userIdentity.accessKeyId` が `ASIAIOSFODNN7EXAMPLE` で `sessionIssuer.arn` が `arn:aws:iam::111122223333:role/web-role` なら、`web-role` の一時キーです。`errorCode` が `AccessDenied` の連続は、攻撃者が権限を試している合図です。

ログの改ざんがないことは、ログファイルの検証で示します。

```bash
aws cloudtrail validate-logs \
  --trail-arn arn:aws:cloudtrail:ap-northeast-1:111122223333:trail/org-trail \
  --start-time 2026-10-01T00:00:00Z
```

ダイジェストファイルは 1 時間ごとに配信され、前のダイジェストの署名を含みます。検証を有効にするだけではチェックされず、コマンドの実行が必要です。

- **例:** 10 月 1 日 00:00 以降のログを 1 つ書き換えると、`validate-logs` がそのファイルを `INVALID` と報告します。

### VPC フローログの調査 {#investigate-flow-logs}

既定の形式は次の順です。

```text
version account-id interface-id srcaddr dstaddr srcport dstport protocol packets bytes start end action log-status
2 111122223333 eni-0abc1234 198.51.100.7 10.0.1.5 49152 22 6 12 840 1793491200 1793491260 REJECT OK
```

この例は、外部の `198.51.100.7` から `10.0.1.5` の SSH（TCP、protocol 6）への通信が拒否されたことを示します。

```text
filter action = "REJECT"
| stats sum(packets) as pkts by srcAddr, dstAddr, dstPort
| sort pkts desc
| limit 20
```

| 調べたいこと | 使うフィールド |
| --- | --- |
| NAT の裏の元の送信元 | `pkt-srcaddr`、`pkt-dstaddr`（カスタム形式） |
| 通信の向き | `flow-direction` |
| 外への経路 | `traffic-path` |
| TCP の状態 | `tcp-flags`（FIN 1、SYN 2、RST 4、SYN-ACK 18） |

- **NAT の例:** NAT ゲートウェイの ENI のフローログでは `srcaddr` が NAT の IP です。`pkt-srcaddr` なら元の `10.0.1.5` が分かります。
- **`tcp-flags` の例:** 同じ送信元から多数のポートに `2`（SYN）だけが続くなら、ポートスキャンの疑いです。

**読み方の注意:**

- フローログに中身はありません。ペイロードが必要ならトラフィックミラーリングを使います。
- 拒否が SG か NACL かは、これだけでは分かりません。戻りの通信だけが `REJECT` なら NACL を疑います。
- `NODATA` は通信なし、`SKIPDATA` は取りこぼしです。

| ログに残らないもの | 代わりの手段 |
| --- | --- |
| Amazon DNS サーバーへの通信 | Route 53 Resolver クエリログ |
| `169.254.169.254` のメタデータへの通信 | OS 上の監視、Runtime Monitoring |
| `169.254.169.123` の Time Sync への通信 | |
| Windows のライセンス認証の通信 | |

作成後は形式を変更できません。必要なフィールドが足りないときは、作り直します。

- **例:** 既定の形式で作ったあとに `pkt-srcaddr` が必要になったら、カスタム形式で新しいフローログを作ります。古いログには入っていないので、過去の分は分かりません。

## CodeGuru Security {#codeguru-security}

[:material-certificate: MLA](../courses/mla/services.md){ .exam-badge .exam-associate } [:material-star-circle: DOP](../courses/dop/services.md){ .exam-badge .exam-professional } [:material-target: SCS](../courses/scs/services.md){ .exam-badge .exam-specialty }

!!! danger "サポート終了"
    Amazon CodeGuru Security は 2025 年 11 月 20 日にサポートを終了し、コンソールとドキュメントも利用できなくなりました。SCS-C03 のスキル 3.2.6 と対象サービス一覧には名前が残っています。

コードの脆弱性をスキャンするサービスでした。現在の選択肢は次のとおりです。

| 目的 | 現在のサービス |
| --- | --- |
| リポジトリやコードのスキャン | Inspector の [Code Security](#inspector-code) |
| Lambda のコードのスキャン | Inspector の Lambda コードスキャン |
| 開発者の IDE でのスキャン | Amazon Q Developer |
| CI/CD でのコンテナイメージ | Inspector の Scan API と SBOM Generator |

試験で CodeGuru Security が選択肢に出たら、パイプラインでの静的スキャンの役割として読みます。

## 選び方の比較 {#choosing}

| 迷う組み合わせ | 選び方 |
| --- | --- |
| GuardDuty と Inspector | 動いている脅威は GuardDuty、弱点（CVE）は Inspector |
| GuardDuty と Macie | S3 への異常なアクセスは GuardDuty、S3 の中身は Macie |
| GuardDuty と Detective | 発見は GuardDuty、原因の調査は Detective |
| Security Hub と Security Hub CSPM | 関連付けとリスクの優先度は Security Hub、基準への準拠チェックは CSPM |
| Security Hub と Security Lake | 検出結果の管理は Security Hub、生ログの長期保管と分析は Security Lake |
| Security Lake と CloudTrail の証跡 | 複数ソースの正規化は Security Lake、API の記録そのものは証跡 |
| Audit Manager と Artifact | 自社の証拠集めは Audit Manager、AWS の報告書は Artifact |
| Audit Manager と Config 適合パック | 新規の準拠チェックは Config の適合パック |
| Firewall Manager と Network Firewall | 展開と統制は Firewall Manager、検査そのものは Network Firewall |
| Shield Standard と Advanced | 既定の防御は Standard、SRT、コスト保護、L7 の支援は Advanced |
| Shield と WAF | 量の攻撃は Shield、リクエストの中身は WAF。L7 は併用 |
| Network Firewall と DNS Firewall | 全通信の IPS は Network Firewall、DNS クエリだけなら DNS Firewall |
| 自動化ルールと EventBridge | 検出結果の更新は自動化ルール、外部の操作は EventBridge |
| SG 変更と NACL | 新しい通信は SG、既存の接続を切るのは NACL |

## 既定値と上限のまとめ {#numbers}

| 項目 | 値 |
| --- | --- |
| GuardDuty の検出結果の保持 | 90 日 |
| GuardDuty の更新通知の頻度 | 既定 6 時間（15 分、1 時間） |
| GuardDuty の S3 エクスポート | 新規は約 5 分以内 |
| GuardDuty の委任管理者のメンバー数 | 50,000 |
| GuardDuty の重要度 | 1.0 - 10.0（Critical は 9.0 以上） |
| GuardDuty 起動のマルウェアスキャン | 24 時間に 1 回 |
| オンデマンドのマルウェアスキャン | 前回から 1 時間後 |
| GuardDuty、CSPM の無料トライアル | 30 日 |
| Security Hub、CSPM の自動化ルール | 100 |
| Inspector のネットワーク到達性 | 12 時間ごと |
| Inspector の ECR 再スキャンの既定（新規） | 7 日 |
| Inspector の Lambda の初回スキャン対象 | 直近 90 日 |
| Macie の検出結果の保持 | 90 日 |
| Macie のポリシー更新の配信 | 既定 15 分 |
| Detective の履歴 | 最大 1 年 |
| Detective のメンバー数 | 1,200 |
| Shield Advanced | 1 年契約、月額 3,000 ドル |
| Shield の WAF ルールグループ（従来の L7 自動緩和） | 150 WCU |
| Network Firewall の TCP アイドル | 既定 350 秒（60 - 6000） |
| CloudTrail のイベント履歴 | 90 日 |
| CloudTrail のダイジェスト | 1 時間ごと |
| フローログのサブスクリプション | リソースごとに 250 |

## 試験のポイント {#exam-points}

| こう問われたら | 答え |
| --- | --- |
| 自分でログを有効にせず脅威を検出したい | GuardDuty |
| GuardDuty が DNS の検出結果を出さない | 自前の DNS を使っていないか確認 |
| 組織全体で GuardDuty を自動有効化 | 委任管理者と自動有効化 `ALL`。リージョンごとに設定 |
| 既知の誤検知を消しつつ記録は残す | 抑制ルール |
| 検出結果を 90 日より長く保存 | S3 へエクスポート（KMS キーが必要） |
| 検出結果に応じて自動で隔離 | EventBridge と Step Functions、または Lambda、SSM |
| 全アカウントの全リージョンで標準を統一 | Security Hub CSPM の中央設定 |
| コントロールの結果が出ない | AWS Config の有効化を確認 |
| EC2 の CVE を継続的に検出 | Inspector |
| SSM Agent がない EC2 も CVE を確認 | Inspector のハイブリッドスキャン |
| S3 の個人情報を見つける | Macie |
| 検出結果の根本原因と関連を調べる | Detective |
| 複数ソースのログを OCSF で集約 | Security Lake |
| AWS の SOC 2 報告書や HIPAA の BAA | Artifact |
| 組織の全 ALB に同じ WAF ルールを強制 | Firewall Manager |
| DDoS の専門チームとコスト保護 | Shield Advanced（SRT にはサポートプランが必要） |
| SRT から連絡してほしい | プロアクティブエンゲージメントと Route 53 ヘルスチェック |
| 許可したドメインにだけ外向き通信 | Network Firewall のドメインリスト |
| Network Firewall のログが少ない | ステートフルへ転送した通信だけが対象 |
| SG を変えても攻撃者の通信が止まらない | 追跡中の接続は続く。NACL で遮断 |
| 証拠を残してインスタンスを隔離 | メモリとスナップショットの取得、隔離用 SG |
| 暗号化スナップショットを別アカウントへ共有 | カスタマー管理キーで、キーも共有 |
| 漏えいした一時認証情報を止める | ロールのセッションの取り消し |
| CloudTrail のログが改ざんされていない証明 | ログファイルの検証と `validate-logs` |
| フローログに DNS やメタデータの通信がない | 記録の対象外。Resolver クエリログなど |
| NAT の裏の元の IP を見たい | カスタム形式の `pkt-srcaddr` |
| パイプラインでコードの脆弱性をスキャン | Inspector Code Security（旧 CodeGuru Security）、Amazon Q Developer |

## 関連ページ {#related}

- [IAM と STS](iam.md)
- [ID とディレクトリ](identity-directory.md)
- [Cognito](cognito.md)
- [KMS](kms.md)
- [シークレットと設定](secrets.md)
- [証明書と WAF](certificates.md)
- [オブザーバビリティ](observability.md)
- [ネットワークと配信](networking.md)
- [ガバナンス](governance.md)
- [レジリエンス](resilience.md)

## 参考 {#references}

- [What is Amazon GuardDuty?](https://docs.aws.amazon.com/guardduty/latest/ug/what-is-guardduty.html)
- [GuardDuty foundational data sources](https://docs.aws.amazon.com/guardduty/latest/ug/guardduty_data-sources.html)
- [Suppression rules in GuardDuty](https://docs.aws.amazon.com/guardduty/latest/ug/findings_suppression-rule.html)
- [Severity levels of GuardDuty findings](https://docs.aws.amazon.com/guardduty/latest/ug/guardduty_findings-severity.html)
- [Managing GuardDuty accounts with AWS Organizations](https://docs.aws.amazon.com/guardduty/latest/ug/guardduty_organizations.html)
- [Malware Protection for EC2](https://docs.aws.amazon.com/guardduty/latest/ug/malware-protection.html)
- [Malware Protection for S3](https://docs.aws.amazon.com/guardduty/latest/ug/gdu-malware-protection-s3.html)
- [Remediating a potentially compromised EC2 instance](https://docs.aws.amazon.com/guardduty/latest/ug/compromised-ec2.html)
- [Remediating potentially compromised AWS credentials](https://docs.aws.amazon.com/guardduty/latest/ug/compromised-creds.html)
- [Introduction to AWS Security Hub](https://docs.aws.amazon.com/securityhub/latest/userguide/what-is-securityhub-v2.html)
- [Introduction to AWS Security Hub CSPM](https://docs.aws.amazon.com/securityhub/latest/userguide/what-is-securityhub.html)
- [Document history for the AWS Security Hub User Guide](https://docs.aws.amazon.com/securityhub/latest/userguide/doc-history.html)
- [Central configuration in Security Hub CSPM](https://docs.aws.amazon.com/securityhub/latest/userguide/central-configuration-intro.html)
- [What is Amazon Inspector?](https://docs.aws.amazon.com/inspector/latest/user/what-is-inspector.html)
- [Scanning EC2 instances with Amazon Inspector](https://docs.aws.amazon.com/inspector/latest/user/scanning-ec2.html)
- [Amazon Inspector Code Security](https://docs.aws.amazon.com/inspector/latest/user/code-security-assessments.html)
- [What is Amazon Macie?](https://docs.aws.amazon.com/macie/latest/user/what-is-macie.html)
- [What is Amazon Detective?](https://docs.aws.amazon.com/detective/latest/userguide/what-is-detective.html)
- [What is Amazon Security Lake?](https://docs.aws.amazon.com/security-lake/latest/userguide/what-is-security-lake.html)
- [AWS Audit Manager availability change](https://docs.aws.amazon.com/audit-manager/latest/userguide/audit-manager-availability-change.html)
- [What is AWS Artifact?](https://docs.aws.amazon.com/artifact/latest/ug/what-is-aws-artifact.html)
- [AWS Firewall Manager](https://docs.aws.amazon.com/waf/latest/developerguide/fms-chapter.html)
- [AWS Shield Advanced capabilities and options](https://docs.aws.amazon.com/waf/latest/developerguide/ddos-advanced-summary-capabilities.html)
- [AWS Shield pricing](https://aws.amazon.com/shield/pricing/)
- [Automating application layer DDoS mitigation](https://docs.aws.amazon.com/waf/latest/developerguide/ddos-automatic-app-layer-response.html)
- [What is AWS Network Firewall?](https://docs.aws.amazon.com/network-firewall/latest/developerguide/what-is-aws-network-firewall.html)
- [Firewall policy settings in AWS Network Firewall](https://docs.aws.amazon.com/network-firewall/latest/developerguide/firewall-policy-settings.html)
- [Security group connection tracking](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/security-group-connection-tracking.html)
- [AWSSupport-ContainEC2Instance](https://docs.aws.amazon.com/systems-manager-automation-runbooks/latest/userguide/automation-awssupport-containec2instance.html)
- [Revoke IAM role temporary security credentials](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_use_revoke-sessions.html)
- [Automated Forensics Orchestrator for Amazon EC2 and EKS](https://docs.aws.amazon.com/solutions/latest/automated-forensics-orchestrator-for-amazon-ec2/welcome.html)
- [What is AWS Security Incident Response?](https://docs.aws.amazon.com/security-ir/latest/userguide/what-is.html)
- [AWS Security Incident Response Guide](https://docs.aws.amazon.com/whitepapers/latest/aws-security-incident-response-guide/aws-security-incident-response-guide.html)
- [Validating CloudTrail log file integrity](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-log-file-validation-intro.html)
- [CloudTrail Lake availability change](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-lake-service-availability-change.html)
- [Flow log records](https://docs.aws.amazon.com/vpc/latest/userguide/flow-log-records.html)
- [Flow log limitations](https://docs.aws.amazon.com/vpc/latest/userguide/flow-logs-limitations.html)
- [AWS Systems Manager Incident Manager availability change](https://docs.aws.amazon.com/incident-manager/latest/userguide/incident-manager-availability-change.html)
- [What is Network Access Analyzer?](https://docs.aws.amazon.com/vpc/latest/network-access-analyzer/what-is-network-access-analyzer.html)

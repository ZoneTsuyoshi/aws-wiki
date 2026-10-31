# 分野3: インフラストラクチャのセキュリティ

配点は **18%** です。エッジ、コンピューティング、ネットワークの3層で、脅威に合う統制を選び、動かないときに直す力を問います。

似た機能の使い分けが中心です。WAF と Shield、セキュリティグループと NACL と Network Firewall、Client VPN と Verified Access を、要件から選べるようにします。

この分野に限らず、コース全体で使うサービスは[サービス一覧](services.md)から確認できます。

## タスク 3.1: エッジサービスのセキュリティ統制 {#task-3-1}

### 3.1.1 脅威に応じたエッジ戦略の選択 {#skill-3-1-1}

| 脅威 | 層 | 主な統制 |
|---|---|---|
| ネットワーク層の DDoS | L3、L4 | Shield Standard（自動）。CloudFront、Route 53、Global Accelerator の前置きで効果が大きい |
| HTTP フラッド | L7 | WAF のレートベースルール、Anti-DDoS マネージドルールグループ |
| SQL インジェクション、XSS | L7 | WAF のマネージドルールとステートメント |
| ボット、認証情報の総当たり | L7 | WAF の Bot Control、Account Takeover Prevention、CAPTCHA |
| オリジンの直接攻撃 | 構成 | S3 は OAC、ALB はカスタムヘッダーか VPC オリジン |
| 大規模な攻撃での費用と支援 | 契約 | Shield Advanced（SRT、コスト保護） |

Shield Advanced の判断は費用です。1年契約で月額 3,000 ドルなので、SRT の支援やコスト保護が要件に出たときに選びます。WAF だけで済む要件で選ぶと過剰になります。保護対象の標準的な WAF 料金は Shield Advanced に含まれますが、Bot Control や CAPTCHA は別料金です。

詳細: [Shield](../../services/threat-detection.md#shield)、[WAF と似た機能の比較](../../services/certificates.md#waf-comparison)、[アプリケーション層の防御](../../services/threat-detection.md#shield-l7)

### 3.1.2 エッジの保護の実装 {#skill-3-1-2}

**CloudFront のヘッダー:** 応答には**レスポンスヘッダーポリシー**で `Strict-Transport-Security`、`Content-Security-Policy`、`X-Frame-Options` などのセキュリティヘッダーを追加できます。オリジンのコードを変える必要はありません。

ALB をオリジンにするときは、CloudFront が付けるカスタムヘッダーを ALB のルールで検査すると、CloudFront を迂回した直接アクセスを拒否できます。ヘッダーの名前と値は秘密にします。漏れると、直接のリクエストでも通ってしまいます。新しい構成では、ALB をプライベートサブネットに置いたままオリジンにできる VPC オリジンも選べます。

**AWS WAF:** ウェブ ACL のルールは優先度の小さい順に評価します。`Allow` と `Block` で評価が終わり、`Count` は記録だけで次へ進みます。

| マネージドルールグループ | 防ぐもの |
|---|---|
| `AWSManagedRulesCommonRuleSet` | OWASP Top 10 に関連する一般的な攻撃 |
| `AWSManagedRulesSQLiRuleSet` | SQL インジェクション |
| `AWSManagedRulesKnownBadInputsRuleSet` | 既知の悪意ある入力 |
| `AWSManagedRulesAmazonIpReputationList` | 評判の悪い IP |
| `AWSManagedRulesBotControlRuleSet` | ボット |
| `AWSManagedRulesATPRuleSet` | アカウントの乗っ取り |

新しいルールはまず `Count` で動かし、正常なリクエストを止めないことを確認してから `Block` にします。OWASP Top 10 のすべてを WAF で防げるわけではありません。アクセス制御の不備などはアプリ側の対策が必要です。

WAF の本文の検査には上限があります。ALB は 8 KB で固定、CloudFront は既定で 16 KB です。後ろに攻撃文字列を置かれるとすり抜けるので、サイズ制約のルールで大きいリクエストを止めるか、上限を引き上げます。

**IoT ポリシー:** AWS IoT Core のデータプレーン（接続、MQTT の送受信、Device Shadow）を制御する JSON のポリシーです。X.509 証明書、Cognito ID、モノのグループに付けます。評価は IAM と同じで、既定は拒否、明示的な拒否が優先です。変更の反映には 6〜8 分かかることがあります。

**S3 の CORS:** ブラウザが別のオリジンからの呼び出しを許すかを決める設定です。**認可の仕組みではありません。** `AllowedOrigins` を `*` にしない、という設定の問題と、バケットポリシーでの認可を区別します。

**Shield Advanced:** 保護するリソースを指定し、関連するリソースをプロテクショングループでまとめます。EC2 と NLB は Elastic IP の関連付けで保護します。

詳細: [ウェブ ACL](../../services/certificates.md#web-acl)、[容量と本文の検査](../../services/certificates.md#waf-capacity-body)、[CloudFront と WAF](../../services/networking.md#cloudfront-waf)、[OAC](../../services/networking.md#oac)、[IoT Core](../../services/other-services.md#iot-core)、[S3 の CORS](../../services/s3.md#cors)

### 3.1.3 要件に基づくルールの設計 {#skill-3-1-3}

| 要件 | 手段 | 注意点 |
|---|---|---|
| 国単位で配信全体を制限 | CloudFront の地理的制限 | ディストリビューション全体に効く。拒否は 403 |
| 国とパスの組み合わせで制限 | WAF の地理的一致 | 他の条件と組み合わせられる |
| ログイン画面のレート制限 | WAF のレートベースルールと `ScopeDownStatement` | ウィンドウは 60、120、300、600 秒（既定 300）。最小 10 |
| 送信元 IP が変わるボット | JA3 または JA4 フィンガープリント | CloudFront と ALB のみ |
| 特定の ASN からの制限 | ASN の一致や集約キー | |

**クライアントのフィンガープリント:** JA3 と JA4 は TLS の Client Hello から計算するハッシュで、クライアントの TLS の構成を表します。IP を変えて攻撃するツールでも同じ値になりやすいのが利点です。値は WAF のログから取得するので、ログの有効化が必要です。計算できない場合のフォールバックの動作も指定します。レートベースルールの集約キーにも使えます。

**落とし穴:** CloudFront の背後の ALB に WAF を置くと、送信元 IP が CloudFront になります。CloudFront に WAF を付けるか、`X-Forwarded-For` などの転送 IP を集約キーにします。CloudFront 用のウェブ ACL は `us-east-1` で作ります。

詳細: [レートベースルール](../../services/certificates.md#rate-based-rules)、[地理的制限](../../services/networking.md#geo-restriction)、[スコープと関連付け](../../services/certificates.md#waf-scope)

### 3.1.4 エッジと他社サービスの統合 {#skill-3-1-4}

C03 で追加されたスキルです。

**OCSF の取り込み:** OCSF（Open Cybersecurity Schema Framework）は、セキュリティログの共通形式です。

| サービス | OCSF との関係 |
|---|---|
| Security Lake | WAF ログなどを OCSF に変換して保管。他社のログはカスタムソースとして OCSF の Parquet で書き込む |
| Security Hub | 検出結果の形式が OCSF。CSPM は ASFF |
| Verified Access | ログを OCSF で CloudWatch Logs、S3、Firehose へ出力 |

カスタムソースは 1 オブジェクトに 1 つの OCSF クラスです。データが検索できないなら、Parquet 形式か、クラスが混ざっていないかを確認します。

**他社の WAF ルール:** AWS Marketplace の販売者が管理するマネージドルールグループを、ウェブ ACL に追加できます。自社で攻撃パターンを保守する負担を減らせますが、ルール全体の WCU の上限と費用を確認します。

**Firewall Manager:** 組織に展開するポリシーで、Palo Alto Cloud NGFW と Fortigate CNF の他社製ファイアウォールも扱えます。

詳細: [Security Lake](../../services/threat-detection.md#security-lake)、[Security Hub の製品](../../services/threat-detection.md#security-hub-products)、[Firewall Manager](../../services/threat-detection.md#firewall-manager)、[WAF のログ](../../services/certificates.md#waf-logging)

## タスク 3.2: コンピューティングのセキュリティ統制 {#task-3-2}

### 3.2.1 AMI とコンテナイメージの強化 {#skill-3-2-1}

起動後に直すのではなく、イメージに統制を組み込みます。

| 工程 | 手段 | 効果 |
|---|---|---|
| ビルド | EC2 Image Builder のレシピとコンポーネント | AMI とコンテナイメージの作成を自動化 |
| テスト | Image Builder のコンポーネント、Inspector | 配布前に脆弱性を確認 |
| 配布 | 配布設定（別リージョン、別アカウント） | 承認済みのイメージだけ届ける |
| 廃棄 | ライフサイクルポリシー | 古いイメージを非推奨化、削除 |
| 共有 | Parameter Store に最新の AMI ID | 利用者が常に最新を使える |

ビルド用インスタンスのロールには `EC2InstanceProfileForImageBuilder` と `AmazonSSMManagedInstanceCore` が必要で、足りないとタイムアウトで失敗します。

コンテナでは、ECR のタグを不変にして上書きを防ぎ、拡張スキャンで検査します。

詳細: [EC2 Image Builder](../../services/operations.md#image-builder)、[AMI の管理](../../services/operations.md#amis)、[タグと不変タグ](../../services/containers.md#image-tags)、[ECR のイメージスキャン](../../services/containers.md#ecr-scanning)

### 3.2.2 ロールの適切な適用 {#skill-3-2-2}

| 対象 | ロール | 使う主体 |
|---|---|---|
| EC2 | インスタンスプロファイル | インスタンス上のアプリ |
| Lambda | 実行ロール | 関数のコード |
| ECS | タスクロール | コンテナのアプリ |
| ECS | タスク実行ロール | ECS エージェント（イメージの取得、シークレットの注入） |
| EKS | EKS Pod Identity か IRSA | Pod |
| サービス全般 | サービスロール | サービスが代わりに操作する |
| サービス全般 | サービスリンクロール | サービスが定義。SCP の制限を受けない |

ロールを渡す人には `iam:PassRole` が必要です。`Resource` を `*` にすると、管理者ロールを Lambda に渡して権限を昇格できてしまうので、ARN と `iam:PassedToService` で絞ります。

EKS では、IMDS へのアクセスを制限しないと、Pod からノードのロールを取得できます。Fargate の Pod には IRSA を使います。

EC2 では IMDSv2 を必須にして、SSRF による認証情報の窃取を防ぎます。

詳細: [インスタンスプロファイル](../../services/iam.md#instance-profile)、[Lambda の実行ロール](../../services/iam.md#lambda-execution-role)、[タスクロールと実行ロール](../../services/containers.md#task-role-vs-execution-role)、[Pod の IAM](../../services/containers.md#pod-identity)、[PassRole](../../services/iam.md#passrole)、[サービスロール](../../services/iam.md#service-linked-roles)、[IMDS](../../services/iam.md#imds)

### 3.2.3 脆弱性のスキャンと実行時の監視 {#skill-3-2-3}

| 観点 | Inspector | GuardDuty Runtime Monitoring |
|---|---|---|
| 見つけるもの | 既知の脆弱性（CVE）、開いたネットワーク経路 | 実行中の不審な振る舞い |
| 問い | 弱点はあるか | 今攻撃されているか |
| 対象 | EC2、ECR、Lambda、コード | EKS、ECS の Fargate、EC2（EKS の Fargate は対象外） |

**Inspector の EC2 スキャン:** 既定はハイブリッドで、SSM の管理下にあればエージェント、なければ EBS スナップショットから収集します。カバレッジが低いなら SSM Agent、インスタンスプロファイル、VPC エンドポイントを確認します。

**ECR の再スキャンの期間:** 2026年10月15日以降に有効にした場合の既定は 7 日です。古いイメージが検査されないなら、この期間を確認します。

**Lambda:** 有効化時に直近90日に呼び出しか更新があった関数をスキャンします。カスタマー管理キーで暗号化された関数は対象外です。

詳細: [Inspector のスキャンの種類](../../services/threat-detection.md#inspector-scan-types)、[EC2](../../services/threat-detection.md#inspector-ec2)、[ECR](../../services/threat-detection.md#inspector-ecr)、[Lambda とコード](../../services/threat-detection.md#inspector-code)、[GuardDuty の保護プラン](../../services/threat-detection.md#guardduty-protection-plans)

### 3.2.4 パッチの展開と継続的な検証 {#skill-3-2-4}

| 実行の方法 | 範囲 | 選ぶ場面 |
|---|---|---|
| パッチポリシー（Quick Setup） | Organizations の複数アカウント、複数リージョン | 推奨。組織全体 |
| Maintenance Windows | 1 アカウント、1 リージョン | 前後の処理と組み合わせる |
| State Manager の関連付け | 1 アカウント、1 リージョン | 定期スキャン |
| Patch now | 1 アカウント、1 リージョン | 即時の適用 |

**定義済みベースラインの落とし穴:** 多くの OS で、リリースの7日後に承認されます。緊急のパッチを7日以内に当てるならカスタムベースラインを作ります。準拠レベルも `Unspecified` です。

**継続的な検証:** Patch Manager の準拠レポートで適用を確認し、Inspector で脆弱性の状況を確認します。Inspector は修正を確認すると検出結果を自動で閉じます。

長く動かすインスタンスに当て続けるより、パッチ済みの AMI を Image Builder で作り、インスタンスの更新で入れ替える方法もあります。

詳細: [Patch Manager](../../services/operations.md#patch-manager)、[検出結果と管理](../../services/threat-detection.md#inspector-findings)、[インスタンスの更新](../../services/operations.md#instance-refresh)

### 3.2.5 安全な管理アクセス {#skill-3-2-5}

| 手段 | インバウンド | 認可 | ログ | 選ぶ場面 |
|---|---|---|---|---|
| Session Manager | 不要 | IAM | セッションの内容を S3 か CloudWatch Logs へ（既定はオフ） | 既定の選択。監査が要件 |
| EC2 Instance Connect | SSH を開ける | IAM | 接続の API 呼び出し | SSH クライアントを使いたい |
| EC2 Instance Connect Endpoint | パブリック IP 不要 | IAM | | プライベートのインスタンスに SSH や RDP |
| 踏み台と SSH 鍵 | 必要 | 鍵の管理 | 自前 | 他に手段がないとき |

**EC2 Instance Connect:** SSH の公開鍵をインスタンスメタデータに 60 秒だけ置き、その間に接続します。長期の鍵を配る必要はありません。接続後のセッションは、IAM の認証情報が切れても SSH を終了するまで続きます。

**Session Manager の落とし穴:** ポート転送と SSH のセッションは、内容をログに残せません。コマンドの中身まで監査するなら、シェルのセッションを使います。KMS キーで追加の暗号化もできますが、ノード側に復号の権限が必要です。アイドルタイムアウトの既定は 20 分です。

詳細: [Session Manager](../../services/operations.md#session-manager)、[EC2 の運用](../../services/operations.md#ec2-operations)

### 3.2.6 パイプラインでの脆弱性の検出 {#skill-3-2-6}

!!! note "CodeGuru Security と Q Developer の状況"
    **CodeGuru Security** は 2025年11月20日にサポートが終了しました。後継は Inspector の Code Security です。試験ガイドのスキルと対象一覧には名前が残っているので、選択肢に出たら「パイプラインの静的スキャン」の役割として読みます。**Q Developer** は IDE の部分が Kiro へ移行中で、新規サブスクリプションは 2026年5月15日に停止し、IDE プラグインと有料サブスクリプションのサポートは 2027年4月30日に終了します。

| 目的 | 現在の手段 |
|---|---|
| リポジトリのコード、依存関係、IaC のスキャン | Inspector の Code Security |
| Lambda のコードのスキャン | Inspector の Lambda コードスキャン |
| 開発者の IDE でのスキャン | Amazon Q Developer |
| CI/CD でのコンテナイメージの検査 | Inspector の Scan API と SBOM Generator |
| シークレットの混入の防止 | シークレットはコードに置かず Secrets Manager を使う |

Inspector の SBOM Generator と Scan API は、GitHub Actions、Jenkins、CodePipeline などのプラグインから使えます。重大な検出結果があればパイプラインを止めるのが基本です。

IAM ポリシーの確認も組み込めます。Access Analyzer の `ValidatePolicy` や `CheckNoNewAccess` をパイプラインで実行します。

詳細: [CodeGuru Security](../../services/threat-detection.md#codeguru-security)、[Lambda とコード](../../services/threat-detection.md#inspector-code)、[Q Developer の現状](../../services/ai.md#q-developer)、[ポリシーの検証](../../services/identity-directory.md#aa-policy-checks)

### 3.2.7 生成 AI アプリの保護 {#skill-3-2-7}

C03 で追加されたスキルです。[OWASP Top 10 for LLM Applications（2025年版）](https://genai.owasp.org/llm-top-10/)を、AWS の統制に対応させて押さえます。

| 項目 | リスク | AWS での対策の例 |
|---|---|---|
| LLM01 プロンプトインジェクション | 入力や文書でモデルを操る | Guardrails のプロンプト攻撃フィルター、ツールの権限制限 |
| LLM02 機密情報の開示 | 応答からの個人情報の漏えい | Guardrails の機密情報フィルター（`ANONYMIZE`）、Macie で学習データを確認 |
| LLM03 サプライチェーン | モデルや依存関係の改ざん | Inspector、承認済みモデルの IAM での限定 |
| LLM04 データとモデルの汚染 | 学習データや文書の改ざん | データソースの権限管理、S3 のバージョニング |
| LLM05 不適切な出力の処理 | 出力をそのまま後段に渡す | JSON Schema と業務ルールの検証、WAF |
| LLM06 過剰な自律性 | エージェントの過大な権限 | 最小権限のロール、AgentCore Policy、人による承認 |
| LLM07 システムプロンプトの漏えい | プロンプト内の秘密の流出 | プロンプトに秘密を置かない、Guardrails のプロンプト漏えいの検出 |
| LLM08 ベクトルと埋め込みの弱点 | 検索での権限の越境 | ベクトルストアのアクセス制御、メタデータでの絞り込み |
| LLM09 誤情報 | 根拠のない応答 | コンテキストグラウンディング、Automated Reasoning |
| LLM10 無制限の消費 | 費用の搾取や DoS | WAF と API Gateway のレート制限、GuardDuty の AI Protection |

**適用の強制:** 呼び出し側に任せると、指定し忘れで迂回されます。

| 方法 | 範囲 | 限界 |
|---|---|---|
| IAM の `bedrock:GuardrailIdentifier` | 指定なしの推論を拒否 | 入力タグで入力の評価を回避できる。`RetrieveAndGenerate` や `InvokeAgent` が拒否されることがある |
| Organizations の Bedrock ポリシー | 組織、OU、アカウント | 呼び出し側の指定が不要 |

**Guardrails の限界:** `guardrailConfig` はツール結果（`toolResult`）とツール引数（`toolUse.input`）を評価しません。ツール結果に仕込まれた間接的なプロンプトインジェクションは、アプリ側で `ApplyGuardrail` に通して検査します。

**AgentCore:** Policy は Gateway を通る呼び出しにしか効かないので、Runtime への直接呼び出しを禁止します。

詳細: [Guardrails のフィルター](../../services/ai.md#guardrail-filters)、[適用の強制と限界](../../services/ai.md#guardrail-enforcement)、[組織での強制](../../services/genai-apps.md#guardrail-org-enforcement)、[多層防御](../../services/genai-apps.md#defense-in-depth)、[エージェントの保護](../../services/ai.md#agent-security)

## タスク 3.3: ネットワークのセキュリティ統制 {#task-3-3}

### 3.3.1 通信の許可と拒否の設計 {#skill-3-3-1}

| 統制 | 適用先 | 状態 | 向いている用途 |
|---|---|---|---|
| セキュリティグループ | ENI | ステートフル。許可のみ | 主な通信制御。SG を送信元に指定できる |
| ネットワーク ACL | サブネット | ステートレス。番号順 | 特定の IP の拒否、既存の接続の遮断 |
| Network Firewall | VPC の境界 | ステートレスとステートフル | ドメインの許可リスト、IPS シグネチャ、東西の検査 |
| DNS Firewall | DNS クエリ | | 悪性ドメインの名前解決の阻止 |
| AWS WAF | HTTP | | リクエストの中身 |

**Network Firewall のよくある誤り:**

| 症状 | 原因 |
|---|---|
| 検査されない | ルートテーブルで経路を挟んでいない。同じサブネットのアプリは保護されない |
| ステートフルのルールとログが効かない | ステートレスの既定アクションが Pass |
| 集中型で他の VPC の通信にルールが合わない | `HOME_NET` の既定が検査用 VPC の CIDR |
| 順序が思いどおりでない | 評価順は作成時にのみ指定できる。厳密順が推奨 |
| 接続が切れる | AZ をまたぐ非対称なルート |

DNS Firewall は独自の DNS サーバーや IP 直接の通信をすり抜けられます。IP 宛も止めるなら Network Firewall です。

**NACL の落とし穴:** 戻り通信のエフェメラルポートを開け忘れると接続が失敗します。

詳細: [SG と NACL](../../services/networking.md#security-groups-nacls)、[接続できないときの切り分け](../../services/networking.md#vpc-troubleshooting)、[Network Firewall の構成](../../services/threat-detection.md#nfw-architecture)、[ルールの評価](../../services/threat-detection.md#nfw-rules)、[DNS Firewall](../../services/network-connectivity.md#dns-firewall)

### 3.3.2 ハイブリッドとマルチクラウドの安全な接続 {#skill-3-3-2}

Direct Connect は専用線ですが、**それだけでは暗号化されません**。

| 方法 | 暗号化の範囲 | 速度 | トレードオフ |
|---|---|---|---|
| Site-to-Site VPN | CGW ↔ VPN エンドポイント | トンネルあたり 1.25 または 5 Gbps | 導入が早いがインターネット経由 |
| MACsec | ルーター ↔ DX ロケーション（区間のみ） | ポート速度 | 10、100、400 Gbps の専用接続のみ。エンドツーエンドではない |
| プライベート IP VPN（トランジット VIF の上） | CGW ↔ Transit Gateway | 同上 | プライベートな経路のまま IP 層で暗号化する。トンネルの帯域が上限になる |
| 公開 VIF の上の VPN | CGW ↔ VPN エンドポイント | 同上 | 公開 IP を使う |

**MACsec のモード:** 既定の `should_encrypt` は、確立に失敗すると**暗号化せずに通信を続けます**。監査で暗号化なしを許さないなら `must_encrypt` です。ただし失敗すると通信が止まります。既定で開通させて、セッションの確立を確認してから変更します。CKN/CAK のローテーションは手動で、接続あたり3組まで保持できます。

他のクラウドとの接続も、基本は IPsec の VPN か専用線の組み合わせで考えます。

詳細: [MACsec](../../services/network-connectivity.md#dx-macsec)、[Site-to-Site VPN](../../services/network-connectivity.md#site-to-site-vpn)、[トンネルオプション](../../services/network-connectivity.md#vpn-tunnel-options)、[プライベート IP VPN](../../services/network-connectivity.md#vpn-private-ip)、[オンプレミスとの接続の選び方](../../services/network-connectivity.md#choosing-hybrid)

### 3.3.3 ハイブリッド環境の通信要件 {#skill-3-3-3}

人が社内アプリを使う場合は、ネットワークに入れるか、アプリに入れるかの判断です。

| 観点 | Client VPN | Verified Access | Site-to-Site VPN |
|---|---|---|---|
| 接続の範囲 | ネットワーク | アプリ単位 | 拠点のネットワーク全体 |
| 判定の頻度 | 接続時（デバイスの状態は5分ごと） | リクエストごと | なし |
| 利用者の VPN | 必要 | 不要（HTTP 以外は接続クライアントが必要） | 不要 |
| 向いている場面 | 端末から VPC 全体へ | ゼロトラストで社内アプリへ | 拠点間 |

**Verified Access の要点:** 信頼プロバイダーは、ID を 1 つ（IAM Identity Center、OIDC）と端末を複数（Jamf、CrowdStrike、JumpCloud）接続します。ポリシーは Cedar で書き、**ポリシーがなければ全拒否**です。ポリシーを通ったのにアプリに届かないなら、アプリ側の SG がエンドポイントからの通信を許可しているか確認します。

**Client VPN の要点:** 接続はできるのに届かないなら、ルートと認可ルールの両方を確認します。認可ルールは既定で何もなく、全部拒否です。

詳細: [Verified Access](../../services/identity-directory.md#verified-access)、[Client VPN](../../services/network-connectivity.md#client-vpn)

### 3.3.4 ネットワークの分割 {#skill-3-3-4}

| 通信の方向 | 意味 | 統制の例 |
|---|---|---|
| 南北（north/south） | インターネットや拠点との出入り | WAF、Network Firewall、NAT、VPC エンドポイント |
| 東西（east/west） | VPC やサブネットの間 | SG の参照、Transit Gateway のルートテーブル、Network Firewall |

| パターン | 内容 |
|---|---|
| 分離サブネット | インターネットへの経路がないサブネット。AWS サービスへは VPC エンドポイントで接続 |
| 階層の分割 | Web、アプリ、DB のサブネットと SG の参照 |
| VPC とアカウントの分割 | 本番と開発を分けて影響範囲を限定 |
| Transit Gateway のルートテーブル | VPC 間の到達性を分ける |
| 集中型の検査 VPC | Network Firewall か GWLB を Transit Gateway の間に置く |

**集中型の検査の落とし穴:** Transit Gateway は既定で送信元の AZ に留まるので、ステートフルなアプライアンスで行きと戻りが別の AZ になると破棄されます。**アプライアンスモード**を有効にします。

検査方式は、マネージドで済ませるなら Network Firewall、他社のファイアウォールをそのまま使うなら GWLB です。

詳細: [サブネットとルートテーブル](../../services/networking.md#subnets-route-tables)、[Transit Gateway のルートテーブル](../../services/network-connectivity.md#tgw-route-tables)、[アプライアンスモード](../../services/network-connectivity.md#tgw-appliance-mode)、[検査の配置](../../services/network-connectivity.md#choosing-inspection)、[GWLB による検査](../../services/network-connectivity.md#gwlb-inspection)

### 3.3.5 不要なネットワークアクセスの特定 {#skill-3-3-5}

| ツール | 目的 | 動き |
|---|---|---|
| Network Access Analyzer | 自分で定義した要件に反する経路を見つける | `MatchPaths` と `ExcludePaths` でスコープを定義 |
| Inspector のネットワーク到達性 | 開いた経路を自動で継続的に検出 | EC2 のみ。12時間ごとに評価 |
| Reachability Analyzer | 指定した2点間の接続を確認 | 1組ずつ。C03 の削除項目だが切り分けで役立つ |
| Verified Access | そもそもネットワーク全体へ入れない | VPN を置き換えて経路を減らす |
| IAM Access Analyzer | ポリシーによる外部アクセスを検出 | ネットワークではなく権限の分析 |
| Firewall Manager の SG 使用状況の監査 | 未使用や冗長な SG の整理 | 組織全体 |

「本番 VPC と開発 VPC が分離されていること」「IGW への経路に必ずファイアウォールがあること」を確かめるなら Network Access Analyzer です。

詳細: [Network Access Analyzer](../../services/network-connectivity.md#network-access-analyzer)、[ネットワーク到達性](../../services/threat-detection.md#inspector-network)、[Firewall Manager](../../services/threat-detection.md#firewall-manager)

## 確認問題 {#self-check}

??? question "問1: CloudFront の背後の ALB に WAF を付け、IP 単位のレート制限を設定しましたが、正常な利用者も遮断されます。原因と対策は？"
    ALB から見た送信元 IP が CloudFront になり、多数の利用者が同じ IP として数えられています。WAF を CloudFront に付けるか、`X-Forwarded-For` を集約キーにします。CloudFront に付けるウェブ ACL は `us-east-1` で作ります。

??? question "問2: 攻撃者が IP を次々に変えながらログイン API を総当たりしています。IP のレート制限が効きません。追加の投資を抑えて対策するには？"
    WAF のルールで JA3 または JA4 フィンガープリントを使います。TLS の構成から計算するので、IP を変えても同じ値になりやすく、レートベースルールの集約キーにも使えます。ログから値を確認し、`/login` に `ScopeDownStatement` で絞ります。CloudFront か ALB に付けている場合に使えます。ATP のマネージドルールグループも有効ですが、追加の料金がかかるので、この条件では次の候補です。Shield Advanced は要件に対して費用が過大です。

??? question "問3: Direct Connect の専用接続で、暗号化されていない通信を監査で一切認めないよう求められました。100 Gbps の帯域も必要です。どうしますか？"
    MACsec を `must_encrypt` で設定します。VPN はトンネルあたりの帯域が足りません。既定の `should_encrypt` は確立に失敗すると平文で通信を続けるので要件を満たしません。MACsec は区間の暗号化なので、エンドツーエンドの要件があるならアプリの TLS も必要です。

??? question "問4: 社員に社内の Web アプリを使わせています。VPN は VPC 全体に入れるので、アプリごとに端末の状態を含めて毎回判定したいです。何を選びますか？"
    AWS Verified Access です。ID と端末の信頼プロバイダーを接続し、Cedar のポリシーでリクエストごとに評価します。ポリシーがなければ全拒否なので、エンドポイントかグループにポリシーを設定します。Client VPN はネットワーク単位です。

??? question "問5: 中央の検査 VPC に Network Firewall を置き、Transit Gateway で各 VPC を接続しました。AZ が異なる VPC の間の通信だけが断続的に切れます。何を確認しますか？"
    検査 VPC のアタッチメントのアプライアンスモードです。無効だと、行きと戻りで別の AZ のエンドポイントを通り、ステートフルの検査で破棄されます。あわせて `HOME_NET` を各 VPC の CIDR まで広げているかも確認します。

??? question "問6: Bedrock を使うアプリで、外部の文書を読むツールを Agent に与えています。Converse の guardrailConfig でプロンプト攻撃フィルターを有効にしましたが、文書に仕込まれた指示で動作が変わりました。なぜですか？どうしますか？"
    `guardrailConfig` はツール結果（`toolResult`）を評価しません。ツールの結果をアプリ側で `ApplyGuardrail` に通して検査します。さらにツールのロールを最小権限にし、重要な操作は実行直前にアプリで認可します。これは OWASP の LLM01 と LLM06 に対応します。

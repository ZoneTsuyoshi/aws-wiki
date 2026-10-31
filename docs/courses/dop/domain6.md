# 分野6: セキュリティとコンプライアンス

配点は **17%** です。ID とアクセスの管理、セキュリティコントロールの自動化、監視と監査を扱います。

「深いセキュリティの助言」は範囲外です。セキュリティの設定を、複数アカウントに**自動で**広げ、維持する方法を選べるようにします。

## タスク 6.1: 大規模な ID とアクセス管理の手法を実装する {#task-6-1}

### IAM の要素の使い分け {#t6-1-entities}

**ガイドの項目:** 知識「人と機械のアクセスに使う IAM の要素（ユーザー、グループ、ロール、ID プロバイダー、ID ベースポリシー、リソースベースポリシー、セッションポリシー）」

| 使う人 | 推奨 | 避けるもの |
|---|---|---|
| 人 | Identity Center、ID プロバイダーのフェデレーション | IAM ユーザーの長期キー |
| AWS 上のアプリ | ロール（インスタンスプロファイル、タスクロールなど） | キーの埋め込み |
| AWS の外のサーバー | IAM Roles Anywhere | 長期のアクセスキー |
| パイプライン（GitHub など） | OIDC のフェデレーション | リポジトリに置くアクセスキー |

| ポリシー | 付ける先 | 使う場面 |
|---|---|---|
| ID ベース | ユーザー、グループ、ロール | 権限を与える |
| リソースベース | S3、KMS、SQS など | 別のアカウントからのアクセス |
| セッションポリシー | 引き受けの呼び出し | そのセッションだけ権限を絞る |
| 権限境界 | ユーザー、ロール | 権限の上限 |

詳細: [プリンシパルと権限の定義](../../services/iam.md#principals)、[ID ベースとリソースベース](../../services/iam.md#identity-vs-resource)、[セッションポリシー](../../services/iam.md#session-policies)、[プログラムからのアクセス](../../services/iam.md#programmatic-access)

### ID フェデレーション {#t6-1-federation}

**ガイドの項目:** 知識「ID フェデレーションの手法（IAM ID プロバイダー、IAM Identity Center の使用）」

| 手段 | 向く場面 |
|---|---|
| Identity Center | 複数アカウントへの人のアクセス。権限セットを割り当てる |
| IAM の SAML プロバイダー | アカウントごとに独自の連携を保つ |
| IAM の OIDC プロバイダー | GitHub Actions や EKS のサービスアカウントなど |
| Cognito | アプリの利用者。AWS の管理者ではない |

Identity Center の ID ソースには、組み込みのディレクトリ、Active Directory、外部の IdP を選べます。

詳細: [フェデレーション](../../services/iam.md#federation)、[IAM Identity Center](../../services/identity-directory.md#identity-center)、[ID ソース](../../services/identity-directory.md#idc-identity-sources)、[権限セット](../../services/identity-directory.md#idc-permission-sets)、[Directory Service](../../services/identity-directory.md#directory-service)

### 権限境界による権限管理の委任 {#t6-1-boundaries}

**ガイドの項目:** 知識「IAM の権限境界による権限管理の委任」

開発者にロールの作成を許しつつ、権限の昇格を防ぐ仕組みです。

| 手順 | 内容 |
|---|---|
| 1 | 上限を定めた権限境界のポリシーを作る |
| 2 | 開発者に `iam:CreateRole` を許可する |
| 3 | 条件 `iam:PermissionsBoundary` で、その境界の指定を必須にする |
| 4 | 境界自体の変更や削除を拒否する |

実際の権限は、ID ベースポリシーと権限境界の**重なり**です。

詳細: [権限境界の設定](../../services/iam.md#permissions-boundary)、[権限境界と SCP](../../services/iam.md#boundaries-scp)

### SCP {#t6-1-scp}

**ガイドの項目:** 知識「組織の SCP」

| 比較 | SCP | 権限境界 |
|---|---|---|
| 適用先 | OU、アカウント | ユーザー、ロール |
| 管理者 | 組織の管理者 | アカウントの管理者 |
| 役割 | 組織としての上限 | 委任の上限 |
| 権限を与えるか | 与えない | 与えない |

**例:** リージョンを制限する SCP では、グローバルサービスを `NotAction` で除きます。除かないと、IAM などの操作まで拒否されます。

詳細: [SCP](../../services/governance.md#scp)、[それぞれの効く場所](../../services/identity-directory.md#evaluation-layers)、[データ境界](../../services/identity-directory.md#data-perimeter)

### 最小権限のポリシー設計 {#t6-1-least-privilege}

**ガイドの項目:** スキル「最小権限を強制するポリシーの設計」

| 道具 | 使い方 |
|---|---|
| IAM Access Analyzer のポリシー生成 | CloudTrail の履歴から必要な権限を生成 |
| 未使用アクセスの検出 | 使っていないロールと権限を見つける |
| ポリシーの検証 | 書いたポリシーの問題を確認 |
| ポリシーシミュレーター | 許可と拒否をテスト |
| 条件 | `aws:PrincipalOrgID`、`aws:SourceArn` などで絞る |

パイプラインにポリシーの検証を組み込むと、広すぎる権限のデプロイを止められます。

詳細: [最小権限](../../services/iam.md#least-privilege)、[IAM Access Analyzer](../../services/identity-directory.md#access-analyzer)、[ポリシーの検証とチェック](../../services/identity-directory.md#aa-policy-checks)、[未使用アクセスの検出](../../services/identity-directory.md#aa-unused)、[ポリシーシミュレーター](../../services/iam.md#policy-simulator)

### RBAC と ABAC {#t6-1-rbac-abac}

**ガイドの項目:** スキル「ロールベース、属性ベースのアクセス制御パターンの実装」

| 比較 | RBAC | ABAC |
|---|---|---|
| 判断の材料 | 職務ごとのロール | タグなどの属性 |
| ポリシーの数 | 増えやすい | 少なくて済む |
| リソースの増加 | ポリシーの更新が必要 | タグで自動で対象になる |
| 向く場面 | 職務が固定 | チームやプロジェクトが増える |

```json
{
  "Effect": "Allow",
  "Action": "ec2:StartInstances",
  "Resource": "*",
  "Condition": {
    "StringEquals": {
      "aws:ResourceTag/Team": "${aws:PrincipalTag/Team}"
    }
  }
}
```

Identity Center からは、属性をセッションタグとして渡せます。タグを勝手に変更されないよう、タグの操作を制限します。

詳細: [条件とアクセス制御](../../services/iam.md#conditions)、[セッションタグ](../../services/iam.md#session-tags)、[Identity Center の ABAC](../../services/identity-directory.md#idc-abac)、[タグ戦略](../../services/governance.md#tagging-strategy)

### 機械の認証情報のローテーション {#t6-1-rotation}

**ガイドの項目:** スキル「機械の ID の認証情報のローテーションの自動化（Secrets Manager など）」

| 対象 | 方法 |
|---|---|
| データベースのパスワード | Secrets Manager の自動ローテーション |
| 独自のサービスの API キー | Lambda のローテーション関数 |
| EC2 などから AWS を呼ぶ | ロール（一時的な認証情報で、ローテーションが要らない） |
| やむを得ない長期のアクセスキー | Config の `access-keys-rotated` で検出 |

ローテーションの関数がデータベースに届くには、VPC の中に置くか、Secrets Manager のエンドポイントへの経路が必要です。ローテーションが失敗するときは、ネットワークとロールを確認します。

キャッシュしているアプリは、古い値のままになります。再取得するように作ります。

詳細: [ローテーション](../../services/secrets.md#rotation)、[Lambda ローテーションの動き](../../services/secrets.md#lambda-rotation-steps)、[ローテーションのスケジュール](../../services/secrets.md#rotation-schedule)、[取得とキャッシュ](../../services/secrets.md#retrieval-caching)

### MFA、STS、インスタンスプロファイル {#t6-1-mfa-sts}

**ガイドの項目:** スキル「人と機械の ID へのアクセス制御の権限管理（MFA の有効化、STS、IAM プロファイルなど）」

| 手段 | 使い方 |
|---|---|
| MFA | 条件 `aws:MultiFactorAuthPresent`、Identity Center の MFA |
| `AssumeRole` | 別のアカウント、別の権限で作業 |
| `GetSessionToken` | MFA 付きの一時的な認証情報 |
| インスタンスプロファイル | EC2 にロールを渡す |
| `iam:PassRole` | サービスに渡せるロールを制限 |

詳細: [GetSessionToken と MFA](../../services/iam.md#mfa)、[ロールの引き受け](../../services/iam.md#assume-role)、[API の比較](../../services/iam.md#sts-api-compare)、[インスタンスプロファイル](../../services/iam.md#instance-profile)、[iam:PassRole](../../services/iam.md#passrole)

## タスク 6.2: セキュリティコントロールとデータ保護を自動化する {#task-6-2}

### ネットワークセキュリティの要素 {#t6-2-network}

**ガイドの項目:** 知識「ネットワークセキュリティの要素（セキュリティグループ、ネットワーク ACL、ルーティング、Network Firewall、WAF、Shield）」

| 要素 | 層 | できること |
|---|---|---|
| セキュリティグループ | ENI | 許可だけ。ステートフル |
| ネットワーク ACL | サブネット | 許可と拒否。ステートレス |
| ルーティング | サブネット | 経路を決める。パブリックとプライベートを分ける |
| Network Firewall | VPC の境界 | ドメインやシグネチャで検査 |
| WAF | HTTP（L7） | SQL インジェクション、レート制限 |
| Shield | L3、L4、L7 | DDoS の防御 |

**例:** 特定の IP を遮断するならネットワーク ACL です。セキュリティグループには拒否のルールがありません。戻りの通信のために、ネットワーク ACL ではエフェメラルポートの許可も必要です。

詳細: [セキュリティグループとネットワーク ACL](../../services/networking.md#security-groups-nacls)、[サブネットとルートテーブル](../../services/networking.md#subnets-route-tables)、[Network Firewall](../../services/threat-detection.md#network-firewall)、[WAF](../../services/certificates.md#waf)、[Shield](../../services/threat-detection.md#shield)

### 証明書と PKI {#t6-2-certificates}

**ガイドの項目:** 知識「証明書と公開鍵基盤（PKI）」

| 比較 | ACM のパブリック証明書 | Private CA | インポートした証明書 |
|---|---|---|---|
| 用途 | 公開の HTTPS | 社内、mTLS | 既存の証明書を使う |
| 自動更新 | DNS 検証なら自動 | ACM 経由なら可 | されない |

- CloudFront で使う ACM の証明書は、米国東部（バージニア北部）に作ります。
- ALB の証明書は、ALB と同じリージョンに作ります。
- インポートした証明書は自動更新されません。`DaysToExpiry` メトリクスか Config の `acm-certificate-expiration-check` で監視します。

詳細: [ACM](../../services/certificates.md#acm)、[Private CA](../../services/certificates.md#private-ca)、[リージョンのルール](../../services/certificates.md#region-rules)、[更新の監視](../../services/certificates.md#renewal-monitoring)、[mTLS](../../services/certificates.md#mtls)

### データ管理 {#t6-2-data-management}

**ガイドの項目:** 知識「データ管理（データ分類、暗号化、キー管理、アクセス制御）」

| 工程 | 手段 |
|---|---|
| 分類 | Macie、タグ |
| 暗号化 | KMS、S3 のデフォルト暗号化 |
| キー管理 | キーポリシー、ローテーション、マルチリージョンキー |
| アクセス制御 | IAM、バケットポリシー、Lake Formation |
| マスク | CloudWatch Logs のデータ保護ポリシー |

詳細: [データ分類](../../services/secrets.md#data-classification)、[KMS キーの種類](../../services/kms.md#key-types)、[キーのローテーション](../../services/kms.md#key-rotation)、[キーポリシー、IAM、グラント](../../services/kms.md#access-control)、[サニタイズとマスキング](../../services/secrets.md#sanitization-masking)

### 複数アカウントへのコントロールの自動適用 {#t6-2-automation}

**ガイドの項目:** スキル「複数アカウント、複数リージョンへのセキュリティコントロールの適用の自動化（Security Hub、Organizations、Control Tower、Systems Manager など）」

| 要件 | 手段 |
|---|---|
| 全アカウント、全リージョンで標準を統一 | Security Hub CSPM の中央設定 |
| 操作を禁止する | Organizations の SCP |
| OU に統制を適用する | Control Tower のコントロール |
| サーバーの設定を揃える | Systems Manager の State Manager、Quick Setup |
| WAF やセキュリティグループを組織に配る | Firewall Manager |
| 検出結果に自動で対応する | EventBridge と Automation |

詳細: [組織と集約](../../services/threat-detection.md#security-hub-org)、[Security Hub の自動化](../../services/threat-detection.md#security-hub-automation)、[コントロール](../../services/governance.md#ct-controls)、[Firewall Manager](../../services/threat-detection.md#firewall-manager)、[Security Hub CSPM](../../services/threat-detection.md#security-hub-cspm)

### 多層防御 {#t6-2-defense-in-depth}

**ガイドの項目:** スキル「多層防御のためのセキュリティコントロールの組み合わせ（ACM、WAF、AWS Config、Config ルール、Security Hub、GuardDuty、セキュリティグループ、ネットワーク ACL、Detective、Network Firewall）」

1 つの防御が破られても、次で止まるように重ねます。

| 層 | コントロール |
|---|---|
| 通信の暗号化 | ACM |
| アプリケーション | WAF |
| ネットワークの境界 | Network Firewall |
| サブネット | ネットワーク ACL |
| インスタンス | セキュリティグループ |
| 設定の検証 | AWS Config、Config ルール |
| 脅威の検出 | GuardDuty |
| 集約と優先付け | Security Hub |
| 調査 | Detective |

| サービス | 問いへの答え |
|---|---|
| GuardDuty | 怪しい動きがあるか |
| Inspector | 脆弱性があるか |
| Config | 設定が基準に合っているか |
| Security Hub | 全体でどこが危ないか |
| Detective | なぜ起きて、影響はどこまでか |

詳細: [選び方の比較](../../services/threat-detection.md#choosing)、[GuardDuty](../../services/threat-detection.md#guardduty)、[Security Hub](../../services/threat-detection.md#security-hub)、[Detective](../../services/threat-detection.md#detective)、[ACM の統合サービス](../../services/certificates.md#integrated-services)

### 機密データの検出 {#t6-2-macie}

**ガイドの項目:** スキル「機密データの大規模な検出の自動化（Macie など）」

Macie は、S3 の機密データを検出します。

| 方法 | 向く場面 |
|---|---|
| 自動の機密データ検出 | 全体をサンプリングして、継続的に傾向を見る |
| 検出ジョブ | 特定のバケットを確実に調べる |
| カスタムの識別子 | 社員番号など独自の形式 |

組織の委任管理者が全アカウントを管理します。検出結果は EventBridge に流れるので、タグの付与や隔離を自動化できます。

詳細: [Macie](../../services/threat-detection.md#macie)、[検出の方法](../../services/threat-detection.md#macie-discovery)、[識別子と許可リスト](../../services/threat-detection.md#macie-identifiers)、[検出結果](../../services/threat-detection.md#macie-findings)

### 転送時と保存時の暗号化 {#t6-2-encryption}

**ガイドの項目:** スキル「転送時と保存時のデータの暗号化（KMS、CloudHSM、ACM など）」

| 比較 | KMS | CloudHSM |
|---|---|---|
| 管理 | AWS | 利用者が HSM のユーザーと鍵を管理 |
| 向く場面 | 多くの場合 | 専有の HSM が必須、独自の暗号処理 |
| AWS サービスとの統合 | 広い | KMS の CloudHSM キーストア経由 |

| 要件 | 方法 |
|---|---|
| HTTPS だけに限定する（S3） | バケットポリシーの `aws:SecureTransport` |
| 暗号化なしのアップロードを禁止する | バケットのデフォルト暗号化、ポリシー |
| EBS を必ず暗号化する | アカウントのデフォルト暗号化 |
| 複数のリージョンで同じキー | マルチリージョンキー |
| ロードバランサーで TLS を終端する | ACM の証明書と HTTPS リスナー |

詳細: [保存時と転送時の暗号化](../../services/kms.md#at-rest-in-transit)、[KMS との比較](../../services/identity-directory.md#cloudhsm-vs-kms)、[転送時の TLS](../../services/certificates.md#tls-in-transit)、[ポリシーによる強制](../../services/s3.md#enforcing-encryption)、[EBS の暗号化](../../services/storage.md#ebs-encryption)

## タスク 6.3: セキュリティの監視と監査のソリューションを実装する {#task-6-3}

### 監査のサービスと機能 {#t6-3-audit-services}

**ガイドの項目:** 知識「セキュリティ監査のサービスと機能（CloudTrail、AWS Config、VPC フローログ、CloudFormation のドリフト検出など）」、スキル「堅牢なセキュリティ監査の実装」

| サービス | 記録するもの | 問いへの答え |
|---|---|---|
| CloudTrail | API の呼び出し | 誰がいつ何をしたか |
| AWS Config | リソースの設定の履歴 | 設定がどう変わったか |
| VPC フローログ | 通信のメタデータ | どこからどこへ、許可か拒否か |
| ドリフト検出 | テンプレートとの差 | IaC の外で変更されたか |

監査の仕組みそのものを守ります。

- 組織の証跡を、全リージョンで有効にします。
- ログファイルの検証を有効にします。
- ログ保管アカウントの S3 に Object Lock を付けます。
- SCP で、CloudTrail と Config の停止を拒否します。

詳細: [CloudTrail の設定](../../services/observability.md#cloudtrail)、[Config と CloudTrail の違い](../../services/governance.md#config-vs-cloudtrail)、[VPC フローログ](../../services/networking.md#flow-logs)、[ドリフト検出](../../services/iac.md#drift)、[マルチアカウントのパターン](../../services/governance.md#multi-account-patterns)

### 脆弱性とイベントを見つけるサービス {#t6-3-vulnerability-services}

**ガイドの項目:** 知識「セキュリティの脆弱性とイベントを見つける AWS サービス（GuardDuty、Inspector、IAM Access Analyzer、AWS Config など）」

| サービス | 見つけるもの | 例 |
|---|---|---|
| GuardDuty | 脅威、不審な動き | 不審な API 呼び出し、暗号通貨のマイニング |
| Inspector | ソフトウェアの脆弱性、開いた経路 | CVE |
| IAM Access Analyzer | 外部へ公開されたリソース、未使用の権限 | 外部へ共有された S3、KMS |
| AWS Config | 基準に合わない設定 | 暗号化なしの EBS |

GuardDuty は、CloudTrail、VPC フローログ、DNS ログを独立して分析します。自分でこれらのログを有効にする必要はありません。

詳細: [GuardDuty のデータソース](../../services/threat-detection.md#guardduty-data-sources)、[Inspector](../../services/threat-detection.md#inspector)、[外部アクセスの検出](../../services/identity-directory.md#aa-external)、[AWS Config](../../services/governance.md#config)

### よくある脅威 {#t6-3-threats}

**ガイドの項目:** 知識「よくあるクラウドセキュリティの脅威（安全でない Web 通信、漏えいしたアクセスキー、公開アクセスが有効または暗号化が無効の S3 バケットなど）」

| 脅威 | 検出 | 予防、修復 |
|---|---|---|
| HTTP の通信 | Config の `alb-http-to-https-redirection-check` | ALB のリダイレクト、CloudFront のビューワーポリシー |
| アクセスキーの漏えい | GuardDuty、AWS Health のイベント | キーの無効化、セッションの失効、ロールへの移行 |
| S3 の公開 | Config の `s3-bucket-public-read-prohibited`、Access Analyzer | ブロックパブリックアクセス、組織の SCP |
| S3 の暗号化なし | Config、Security Hub CSPM | デフォルト暗号化、ポリシー |

**アクセスキーが漏れたときの順序:** キーを無効化し、CloudTrail で使われた操作を調べ、作られたリソースを消します。

詳細: [認証情報の漏えい](../../services/threat-detection.md#ir-credentials)、[ブロックパブリックアクセス](../../services/s3.md#block-public-access)、[アクセスキーの扱い](../../services/iam.md#access-key-handling)、[HTTPS](../../services/networking.md#cloudfront-https)

### 異常なセキュリティイベントの通知 {#t6-3-alerting}

**ガイドの項目:** スキル「想定外や異常なセキュリティイベントに基づく通知の設定」

| 検知の対象 | 方法 |
|---|---|
| GuardDuty の検出結果 | EventBridge で重要度に応じて SNS へ |
| ルートユーザーのログイン | CloudTrail、メトリクスフィルターとアラーム、または EventBridge |
| API の量の急増 | CloudTrail Insights |
| Config の非準拠 | `Config Rules Compliance Change` |
| Security Hub CSPM の検出結果 | `Security Hub Findings - Imported` |

大量の通知は無視されるようになります。Security Hub の自動化ルールで重要度を調整し、GuardDuty の抑制ルールで想定内のものを除きます。

詳細: [GuardDuty のイベント連携](../../services/threat-detection.md#guardduty-events)、[抑制ルール](../../services/threat-detection.md#guardduty-suppression)、[Security Hub の自動化](../../services/threat-detection.md#security-hub-automation)、[EventBridge による自動化](../../services/threat-detection.md#ir-eventbridge)、[CloudTrail Insights](../../services/observability.md#cloudtrail-insights)

### サービスとアプリのログの設定 {#t6-3-logging}

**ガイドの項目:** スキル「サービスとアプリケーションのログの設定（CloudTrail、CloudWatch Logs など）」

| ログ | 設定 |
|---|---|
| 管理イベント | 組織の証跡 |
| S3 のオブジェクト操作、Lambda の呼び出し | データイベント。費用がかかるので対象を絞る |
| CloudTrail の検索、通知 | CloudWatch Logs への送信 |
| アプリのログ | CloudWatch エージェント、`awslogs` |
| ALB、CloudFront、WAF | それぞれのアクセスログ |
| 機密情報 | データ保護ポリシーでマスク |

!!! note "CloudTrail Lake の状況"
    CloudTrail Lake は 2026 年 5 月 31 日に新規受付を終了しました。

詳細: [イベントの種類](../../services/observability.md#cloudtrail-events)、[証跡とイベント履歴](../../services/observability.md#cloudtrail-trails)、[CloudTrail Lake](../../services/observability.md#cloudtrail-lake)、[ロギング戦略](../../services/observability.md#logging-strategy)、[WAF のログ](../../services/certificates.md#waf-logging)、[どのログを見るか](../../services/threat-detection.md#log-sources)

### ログ、メトリクス、検出結果の分析 {#t6-3-analysis}

**ガイドの項目:** スキル「ログ、メトリクス、セキュリティの検出結果の分析」

| 問い | 手段 |
|---|---|
| 特定のキーが何をしたか | Athena で CloudTrail、または Logs Insights |
| 拒否された通信 | VPC フローログを `REJECT` で絞る |
| 検出結果の影響範囲 | Detective |
| 複数の検出結果の優先付け | Security Hub |
| ログを正規化して SIEM へ | Security Lake |

詳細: [CloudTrail の調査](../../services/threat-detection.md#investigate-cloudtrail)、[VPC フローログの調査](../../services/threat-detection.md#investigate-flow-logs)、[Detective](../../services/threat-detection.md#detective)、[Security Lake](../../services/threat-detection.md#security-lake)、[検出結果](../../services/threat-detection.md#guardduty-findings)

## 確認問題 {#self-check}

??? question "問1: 開発チームにアプリ用の IAM ロールを自分で作らせたいです。ただし、管理者の権限を持つロールを作って昇格することは防ぎます。どうしますか？"
    権限境界を使います。`iam:CreateRole` を、条件 `iam:PermissionsBoundary` で指定の境界が付く場合だけ許可します。境界の変更や削除は拒否します。

??? question "問2: プロジェクトが毎月増え、プロジェクトごとにロールとポリシーを追加する作業が負担です。リソースのタグは揃っています。どう変えますか？"
    ABAC にします。`aws:ResourceTag/Project` と `aws:PrincipalTag/Project` が一致するときに許可する 1 つのポリシーで済みます。新しいプロジェクトでも、タグを付けるだけで使えます。

??? question "問3: GitHub Actions から AWS へデプロイするのに、長期のアクセスキーをシークレットに置いています。これをやめたいです。どう変えますか？"
    IAM の OIDC プロバイダーを作り、GitHub を信頼するロールを引き受けます。信頼ポリシーの条件でリポジトリとブランチを絞ります。一時的な認証情報なので、キーの管理とローテーションが要らなくなります。

??? question "問4: 組織の全 S3 バケットから個人情報を見つけ、発見したら担当へ通知し、バケットにタグを付けたいです。どう構成しますか？"
    委任管理者で Macie を組織に有効にします。検出結果の EventBridge イベントを受け、SNS で通知し、Lambda でタグを付けます。

??? question "問5: ACM にインポートした証明書の期限切れで障害が起きました。パブリック証明書には切り替えられません。どう再発を防ぎますか？"
    インポートした証明書は自動更新されません。Config の `acm-certificate-expiration-check` か ACM の `DaysToExpiry` メトリクスで期限を監視し、EventBridge や SNS で通知して、更新の作業を自動化します。

??? question "問6: 管理者が誤って CloudTrail を停止し、監査の空白が生まれました。全アカウントで再発を防ぎ、改ざんも検知したいです。どうしますか？"
    組織の証跡を使い、メンバーアカウントから変更できないようにします。SCP で `cloudtrail:StopLogging` と `DeleteTrail` を拒否します。ログファイルの検証を有効にし、ログ保管アカウントの S3 に Object Lock を付けます。

# 証明書と AWS WAF

[:material-sprout: CLF](../courses/clf/services.md){ .exam-badge .exam-foundational } [:material-certificate: SAA](../courses/saa/services.md){ .exam-badge .exam-associate } [:material-certificate: DVA](../courses/dva/services.md){ .exam-badge .exam-associate } [:material-certificate: SOA](../courses/soa/services.md){ .exam-badge .exam-associate } [:material-certificate: DEA](../courses/dea/services.md){ .exam-badge .exam-associate } [:material-star-circle: SAP](../courses/sap/services.md){ .exam-badge .exam-professional } [:material-star-circle: DOP](../courses/dop/services.md){ .exam-badge .exam-professional } [:material-star-circle: AIP](../courses/aip/services.md){ .exam-badge .exam-professional } [:material-target: ANS](../courses/ans/services.md){ .exam-badge .exam-specialty } [:material-target: SCS](../courses/scs/services.md){ .exam-badge .exam-specialty }

ACM と AWS Private CA は TLS 証明書を発行、管理するサービスで、AWS WAF は Web リクエストを検査して攻撃を防ぐサービスです。HTTPS の公開、社内向けの証明書の発行、開発用の鍵の作成、不正なリクエストの遮断といった場面で使います。

[![証明書と WAF の配置](../assets/diagrams/certificates-tls.png)](../assets/diagrams/certificates-tls.png)

## 使いどころと具体例 {#use-cases}

このページの 3 つのサービスは、Web の入口で一緒に使われることが多いものです。ACM は「本物のサイトだと示す」、Private CA は「社内の相手を証明書で見分ける」、WAF は「入ってくるリクエストの中身で止める」役割です。

### 使う場面 {#use-cases-fit}

| 場面 | 具体例 | 使う機能 |
| --- | --- | --- |
| 公開サイトを HTTPS にする | 会員 50 万人のネットスーパーが、ALB の前の CloudFront で `www` を公開する | [ACM](#acm)、[リージョンのルール](#region-rules) |
| 証明書の期限切れを起こしたくない | 店舗ごとにサブドメインを持つ美容室の予約サイトが、更新を人の手から外す | [自動更新](#auto-renewal)、[DNS 検証](#domain-validation) |
| 決められた認証局の証明書を使う | ネット銀行が、社内規程で指定された CA の証明書を ALB で使う | [インポート](#import)、[更新の監視](#renewal-monitoring) |
| 社内だけの名前に証明書を付ける | 社員 2,000 人の製造業が、`hr.internal.example.com` の社内 ALB を HTTPS にする | [Private CA](#private-ca) |
| 端末や取引先を証明書で認証する | 物流会社が、倉庫のハンディ端末だけに出荷 API を使わせる | [mTLS](#mtls)、[Private CA](#private-ca) |
| SQL インジェクションや XSS を止める | 自治体の電子申請のフォームを、既知の攻撃の形から守る | [マネージドルールグループ](#waf-actions-details) |
| ログインの総当たりを止める | オンライン英会話のログイン画面で、1 つの IP からの大量の試行を止める | [レートベースルール](#rate-based-rules) |
| 発売開始のボットを減らす | チケット販売サイトの購入ボタンに、人かどうかの確認を挟む | [CAPTCHA、Challenge](#waf-actions-details) |
| 特定の国からのアクセスを止める | 国内向けの地域ポイントのサイトで、海外からの不正な登録を止める | [ウェブ ACL](#web-acl) の地理的一致 |
| 手元で HTTPS を試す | 開発者が、ローカルの API サーバーを `https://localhost` で動かす | [自己署名証明書](#self-signed) |

### 使わない方がよい場面 {#use-cases-avoid}

| 場面 | 理由 | 代わりの選択肢 |
| --- | --- | --- |
| EC2 の nginx に、通常の ACM の公開証明書を直接置きたい | 通常の公開証明書は秘密鍵を取り出せない | 前に ALB か CloudFront を置く。または[エクスポート可能な証明書か ACME](#integrated-services) |
| 一般の利用者向けのサイトに Private CA の証明書 | 利用者のブラウザが CA を信頼していないので警告が出る | ACM の公開証明書 |
| NLB や EC2 の前で WAF を使いたい | WAF を関連付けられない（[アタッチできる場所](#waf-resources)） | 前に CloudFront か ALB を置く。L3、L4 なら [Network Firewall](threat-detection.md#network-firewall) |
| 大量の通信で回線を埋める DDoS | WAF は HTTP のリクエストを 1 件ずつ見る仕組み | [Shield](threat-detection.md#shield) |
| 契約プランごとに API の呼び出し回数を決める | WAF のレート制限は攻撃を止めるためのもので、正確な回数を保証しない | API Gateway の使用量プラン（[似た機能との比較](#waf-comparison)） |
| IP とポートだけで十分な制限 | WAF を置くと、リクエスト数に応じた費用とルールの管理が増える | [セキュリティグループ](networking.md) |

### 例: ネットスーパーが CloudFront と ALB で HTTPS を公開する {#use-case-grocery}

**状況:** 会員 50 万人のネットスーパーです。夕方 17 時から 19 時に注文が集中し、平常時の 8 倍になります。アプリは東京の ALB の後ろの ECS で動き、画像は CloudFront で配ります。インフラの担当は 2 人で、証明書の更新に人手をかけたくありません。

**構成:**

```mermaid
flowchart LR
    U["会員"] -- "HTTPS<br/>us-east-1 の証明書" --> CF["CloudFront"]
    CF -- "HTTPS<br/>東京の証明書" --> ALB["ALB（東京）"]
    ALB --> ECS["ECS"]
    D["Route 53"] -. "検証の CNAME" .-> CF
```

**設定値:**

| 項目 | 値 | 理由 |
| --- | --- | --- |
| 証明書の数 | `us-east-1` に 1 枚、東京に 1 枚 | CloudFront 用は `us-east-1` にしか作れない（[リージョンのルール](#region-rules)） |
| ドメイン名 | `example.com` と `*.example.com` | ワイルドカードは `example.com` 自体を含まない |
| 検証 | DNS 検証。CNAME は Route 53 に置いたまま | 残しておけば 198 日ごとの更新が自動で進む |
| キーのアルゴリズム | `RSA_2048` | 古いスマートフォンのブラウザも会員にいるため |
| ビューワープロトコルポリシー | `redirect-to-https` | `http://` で来た会員を `https://` へ転送する |
| 監視 | `DaysToExpiry` が 30 を下回ったら SNS に通知 | 自動更新が止まったことに 1 か月前に気づく |

**なぜこのサービスか:** 外部の CA の証明書を買って入れると、更新のたびにインポートし直す作業が残ります。ACM の公開証明書は、統合サービスで使う限り追加料金がなく、更新も自動です。

**つまずきやすい点:**

- DNS の整理で「用途の分からない CNAME」として検証のレコードを消すと、次の更新で失敗します。レコードに説明のタグやコメントを残します。
- 東京で証明書を作っても、CloudFront の選択肢には出ません。
- CloudFront からオリジンへの区間を `https-only` にするなら、ALB にも信頼された CA の証明書が要ります。自己署名だと 502 になります（[転送時の TLS](#tls-in-transit)）。

### 例: ネット銀行が指定の CA の証明書を持ち込む {#use-case-netbank}

**状況:** 口座数 120 万のネット銀行です。社内規程で、公開サイトの証明書は特定の CA から発行すると決まっています。証明書は ALB 3 台で使い、更新は年 1 回です。期限切れは、全利用者がログインできなくなる重大な事故として扱います。

**構成:**

```mermaid
flowchart TD
    CA["指定の CA"] --> OP["運用担当が<br/>証明書を受け取る"]
    OP -- "import-certificate<br/>--certificate-arn" --> ACM["ACM（東京）"]
    ACM --> ALB["ALB 3 台"]
    ACM -- "期限切れが近い<br/>イベント" --> EB["EventBridge"]
    EB --> SNS["SNS で通知"]
```

**設定値:**

| 項目 | 値 | 理由 |
| --- | --- | --- |
| 証明書 | ACM にインポートする | ACM が発行していないので、自動更新はない（[インポート](#import)） |
| 再インポート | `--certificate-arn` で既存の ARN を指定する | ARN と ALB の関連付けを保つ |
| 通知 | `ACM Certificate Approaching Expiration` を EventBridge で受け、SNS へ | インポートした証明書は 45 日前から毎日届く（[更新の監視](#renewal-monitoring)） |
| 通知の開始日 | `PutAccountConfiguration` で 60 日前に早める | 社内の承認と CA の発行に 3 週間かかるため |
| 秘密鍵 | パスフレーズを外して PEM でインポートし、手元の平文の鍵は消す | ACM は暗号化された鍵を受け付けない（[インポートの条件](#import-requirements)） |

**なぜこのサービスか:** ALB に証明書を付けるには ACM を通します。インポートでも、3 台の ALB は同じ ARN を参照するので、1 回の再インポートで全台が切り替わります。

**つまずきやすい点:**

- `--certificate-arn` を付け忘れると、別の ARN の新しい証明書ができ、ALB は古い証明書のままです。期限の日に切れます。
- `--certificate-chain` を省くと、一部の端末で中間証明書が足りず、信頼できない証明書と表示されます。
- 期限切れのあとは `DaysToExpiry` のメトリクスが出なくなります。アラームの「データ不足」も通知の対象にします。

### 例: 物流会社が倉庫の端末だけに出荷 API を使わせる {#use-case-logistics}

**状況:** 全国 40 か所の倉庫で、ハンディ端末 3,000 台が出荷 API を呼びます。端末を盗まれたり、退職者が私物の PC から API を呼んだりするのを防ぎたいと考えています。端末は 1 年に 1 回、本社で入れ替えの点検をします。

**構成:**

| 要素 | 内容 |
| --- | --- |
| CA の階層 | ルート CA の下に、端末用と社内サーバー用の 2 つの下位 CA（[Private CA](#private-ca)） |
| 端末の証明書 | 端末用の下位 CA から `IssueCertificate` で発行し、端末に入れる |
| 出荷 API | API Gateway の REST API のカスタムドメインで mTLS を有効にする（[mTLS](#mtls)） |
| トラストストア | 端末用の下位 CA とルート CA の証明書を S3 に置く |
| 社内の管理画面 | 社内サーバー用の下位 CA から ACM で要求し、内部 ALB に付ける |

**設定値:**

| 項目 | 値 | 理由 |
| --- | --- | --- |
| CA のモード | 汎用 | 端末の証明書は 7 日より長くしたい。ACM で要求する社内サーバー用も汎用が必要（[Private CA の設定](#private-ca-settings)） |
| 端末の証明書の期間 | 395 日 | 年 1 回の点検で入れ替え、1 か月の余裕を持たせる |
| 失効 | CA で CRL を有効にし、Lambda オーソライザーで端末の証明書を失効リストと照合する | API Gateway は失効を確かめないので、盗まれた端末を止めるにはオーソライザーが要る |
| 既定のエンドポイント | `execute-api` を無効にする | mTLS を迂回されないようにする |

**なぜこのサービスか:**

| 選択肢 | 選ばなかった理由 |
| --- | --- |
| API キーだけ | キーは端末から抜き出してコピーできる。証明書の秘密鍵も抜き出せるが、失効で個別に止められる |
| オンプレミスの社内 CA | CA の秘密鍵の保護と冗長化を、情報システム部の 3 人で担うのは重い |

**つまずきやすい点:**

- `IssueCertificate` の証明書は自動で更新されません。点検の日に入れ替えを忘れた端末は、395 日目に出荷 API を呼べなくなります。発行日を台帳で管理します。
- トラストストアには、発行した下位 CA からルート CA までのチェーンをすべて入れます。ルート CA を入れ忘れると、端末の証明書の検証が失敗します。
- CRL に載せただけでは、API Gateway は盗まれた端末を拒否しません。オーソライザーでの照合を忘れないようにします。
- 端末用と社内サーバー用の CA を分けないと、社内サーバーの証明書で出荷 API に入れてしまいます。

### 例: チケット販売サイトが発売開始の買い占めを抑える {#use-case-ticket}

**状況:** コンサートのチケットを販売するサイトです。人気公演の発売開始の 10 時ちょうどに、平常時の 30 倍のアクセスが来ます。その多くがボットで、本当のファンが買えないという苦情が続いています。サイトは CloudFront と ALB で公開しています。

**構成:**

```mermaid
flowchart TD
    A["リクエスト"] --> R0["優先度 0: マネージドルール<br/>既知の攻撃を Block"]
    R0 --> R1["優先度 1: /login のレート制限<br/>IP ごとに 5 分 100 回"]
    R1 --> R2["優先度 2: /purchase に CAPTCHA"]
    R2 --> DEF["既定のアクション: Allow"]
```

**設定値:**

| 項目 | 値 | 理由 |
| --- | --- | --- |
| スコープ | `CLOUDFRONT`、`us-east-1` に作る | 送信元 IP をそのまま見られる。ALB に付けると IP が CloudFront になる（[レートベースルール](#rate-based-rules)） |
| `/login` のレート制限 | `Limit` 100、`EvaluationWindowSec` 300、集約は `IP` | 人が 5 分に 100 回ログインすることはない |
| `/purchase` | CAPTCHA、イミュニティ 1,800 秒 | 発売の 30 分の間に、何度もパズルを出さない |
| 新しいルールの入れ方 | 発売の 1 週間前から Count で動かし、`CountedRequests` を確認 | 本当のファンを止めないことを確かめる（[監視](#waf-monitoring)） |
| ログ | `aws-waf-logs-ticket` の S3 バケット。`authorization` ヘッダーは redaction | 調査に使い、トークンは残さない（[ログ](#waf-logging)） |

**なぜこのサービスか:** ボットの購入は、1 件ずつ見れば正しい形の HTTPS です。セキュリティグループや Shield では止められず、リクエストの中身と回数を見る WAF の役割です。

**つまずきやすい点:**

- スマートフォンのアプリの API にも CAPTCHA を付けると、アプリはパズルを表示できず、正常な購入が失敗します。CAPTCHA はブラウザ向けのパスだけに付けます。
- 大学や会社のように、多くの人が 1 つの IP から来ることがあります。レートの上限を下げすぎると、同じ IP の人がまとめて止まります。
- 発売の直前にルールを変えると、レートのカウントがリセットされ、最大 1 分ほど制限が止まることがあります。前日までに確定させます。

### 例: オンライン学習サービスが教材のアップロードを通す {#use-case-elearning}

**状況:** 全国 600 校が使う学習管理システムで、先生が教材の PDF をアップロードし、生徒が課題を提出します。ALB に WAF を付けたところ、10 KB を超える課題の提出が 403 になると問い合わせが来ました。

**構成:** ALB に関連付けたウェブ ACL で、`AWSManagedRulesCommonRuleSet` を使っています。このルールグループは、8 KB を超える本文を `SizeRestrictions_BODY` で止めます（[ルールのアクションの詳細](#waf-actions-details)）。

**設定値:**

| 項目 | 値 | 理由 |
| --- | --- | --- |
| `SizeRestrictions_BODY` | ルールアクションのオーバーライドで Count にする | 一致したことをラベルとして残し、ここでは止めない |
| 後に置くルール | ラベル `awswaf:managed:aws:core-rule-set:SizeRestrictions_Body` があり、パスが `/upload` と `/submit` 以外なら Block | 大きな本文は、アップロードのパスでだけ許す |
| アップロードの経路 | 大きな教材は、S3 の署名付き URL で直接アップロードさせる | ALB の WAF は本文の先頭 8 KB しか検査できない（[容量と本文の検査](#waf-capacity-body)） |

**なぜこのサービスか:** マネージドルールを丸ごと外すと、ほかのパスの攻撃も素通りします。ラベルを使えば、ルールグループの守りを残したまま、例外を 1 つのパスに閉じ込められます。

**つまずきやすい点:**

- 例外のパスでは、8 KB より後ろにある攻撃の文字列は検査されません。アップロードしたファイルは、アプリ側で形式を確かめます。
- オーバーライドを Count にしたまま、後のルールを足し忘れると、大きな本文はどのパスでも通ります。

## AWS Certificate Manager {#acm}

[:material-sprout: CLF](../courses/clf/services.md){ .exam-badge .exam-foundational } [:material-certificate: SAA](../courses/saa/services.md){ .exam-badge .exam-associate } [:material-certificate: DVA](../courses/dva/services.md){ .exam-badge .exam-associate } [:material-certificate: SOA](../courses/soa/services.md){ .exam-badge .exam-associate } [:material-star-circle: SAP](../courses/sap/services.md){ .exam-badge .exam-professional } [:material-star-circle: DOP](../courses/dop/services.md){ .exam-badge .exam-professional } [:material-target: SCS](../courses/scs/services.md){ .exam-badge .exam-specialty }

ACM は、公開証明書とプライベート証明書の発行、保存、更新を担います。統合サービスで使う限り、更新と配置を自動化できます。

#### なぜ必要か {#acm-why}

TLS 証明書には期限があり、切れた瞬間にすべての利用者のブラウザが警告を出します。証明書の作業自体は難しくありませんが、「年に数回、忘れたころにやってくる」ので、期限切れの事故が起きやすい作業です。

| 困りごと | 手作業だと起きること | ACM の仕組み |
| --- | --- | --- |
| 期限の管理 | 管理表の更新を忘れ、期限の日にサイトが警告画面になる | 統合サービスで使う証明書を自動で更新する |
| 秘密鍵の扱い | 鍵ファイルをメールや共有フォルダで受け渡す | 秘密鍵は ACM の中で管理し、通常は取り出せない |
| 配置 | 更新のたびに全サーバーへ証明書を配り、再起動する | ALB や CloudFront に ARN で関連付け、更新後も自動で差し替わる |

オンプレミスでの作業の流れと比べると、次のようになります。

| 作業 | オンプレミス | ACM |
| --- | --- | --- |
| 鍵と CSR の作成 | サーバーで `openssl` を実行する | ACM が行う |
| 所有権の確認 | 認証局の手順に沿って対応する | DNS に CNAME を 1 回追加する |
| サーバーへの配置 | 証明書と鍵をコピーし、Web サーバーを再起動する | ARN を指定するだけ |
| 更新 | 期限の前に同じ作業を繰り返す | CNAME が残っていれば自動 |

```mermaid
sequenceDiagram
    participant U as 管理者
    participant A as ACM
    participant D as DNS
    participant L as ALB
    U->>A: 証明書を要求（DNS 検証）
    A-->>U: CNAME レコードを提示
    U->>D: CNAME を追加
    A->>D: CNAME を確認
    A-->>U: 発行済み
    U->>L: HTTPS リスナーに ARN を指定
    Note over A,L: 期限が近づくと ACM が更新し、<br/>ALB の証明書も差し替わる
```

秘密鍵を取り出せない設計なのは、鍵が漏れる経路をなくすためです。その代わり、EC2 上の nginx のように ACM と統合していない場所では、通常の証明書をそのまま使えません（[統合サービス](#integrated-services)）。

**提供単位:** ACM の証明書はリージョンのリソースで、VPC の外にあります（[提供単位の一覧](resource-scope.md#scope-regional-outside)）。使うリソースと同じリージョンに作り、CloudFront 用は `us-east-1` に作ります。

| 観点 | 公開証明書 | プライベート証明書 |
| --- | --- | --- |
| 発行元 | Amazon の公開 CA | AWS Private CA のプライベート CA |
| 信頼される範囲 | ブラウザなど一般のクライアント | CA を信頼するよう設定したクライアントのみ |
| 所有権の確認 | ドメインの検証が必要 | 不要 |
| 用途 | 公開 Web サイト、公開 API | 社内サービス、サービス間通信 |
| 料金 | 統合サービスで使う証明書は追加料金なし（エクスポート可能な証明書と ACME の証明書は有料） | Private CA の料金がかかる |

- **公開証明書の例:** `www.example.com` を ALB で公開する。ブラウザは Amazon の CA を信頼しているので警告が出ない。
- **プライベート証明書の例:** 社内の `api.internal.example.com` を ALB で公開する。社員の PC と社内の API クライアントに、ルート CA を信頼させる。
- **誤ると:** プライベート証明書を一般向けのサイトに付けると、利用者のブラウザが CA を信頼しないので `NET::ERR_CERT_AUTHORITY_INVALID` のような警告が出る。

### ドメイン検証 {#domain-validation}

公開証明書は「このドメインの持ち主はこの人だ」と第三者が保証するものです。誰でも `www.example.com` の証明書を取れたら、なりすましのサイトが本物の鍵マークを表示できてしまいます。そこで CA は、発行の前に申請者がドメインを管理していることを確かめます。

DNS 検証は、ドメインの DNS に指定のレコードを書けることを、管理している証拠とする方法です。郵便でいえば、指定した住所の郵便受けに届いた合言葉を返してもらう確認に近いものです。

| 方式 | 手順 | 更新 |
| --- | --- | --- |
| DNS 検証（推奨） | ACM が示す CNAME レコードを DNS に追加 | レコードを残していれば自動 |
| メール検証 | ドメインの管理者にメールで承認を依頼 | メールでの承認が必要な場合がある |
| HTTP 検証 | ACM が示す URL へのリダイレクトを設定。CloudFront の Distribution Tenants でのみ利用可 | 自動 |

DNS 検証のポイントは次のとおりです。

- CNAME は 1 回追加すれば済み、削除すると自動更新が止まる。
- Route 53 ならコンソールから簡単にレコードを追加できる。
- 同じ CNAME が使えるので、別のリージョンでも再検証なしで同じドメインの証明書を作れる。
- メール検証で作った証明書は DNS 検証に切り替えられない。作り直す。

```bash
aws acm request-certificate \
  --domain-name example.com \
  --subject-alternative-names "*.example.com" \
  --validation-method DNS \
  --region us-east-1
```

ワイルドカードは一番左にだけ置け、1 階層だけを保護します。`*.example.com` は `www.example.com` を保護しますが、`a.www.example.com` や `example.com` 自体は保護しません。1 枚の証明書に入れられるドメインは既定で 10 個で、申請すると増やせます。

- **`--domain-name` と `--subject-alternative-names` の例:** 上のコマンドで `example.com` と `www.example.com` の両方が保護される。11 個のドメイン名を 1 枚に入れるには、既定の 10 個を超えるので引き上げを申請するか、ワイルドカードにまとめる。
- **例:** `*.example.com` と `example.com` の 2 つを申請しても、CNAME は `example.com` に対して同じ 1 組になることがある。ACM が示したレコードをそのまま追加する。
- **誤ると:** `*.*.example.com` は申請できない。`a.www.example.com` を守りたいなら `*.www.example.com` を足す。
- **誤ると:** Pending validation のまま 72 時間が過ぎると、検証はタイムアウトし、証明書は発行されない。同じ設定で要求し直す。

### 自動更新 {#auto-renewal}

ACM の公開証明書の有効期間は 198 日で、期限の 45 日前から更新を確認します。以前に発行された有効期間 395 日の証明書は、期限の 60 日前に更新され、更新後は 198 日になります。

| 証明書 | 自動更新 |
| --- | --- |
| 統合サービスに関連付けた Amazon 発行の証明書 | 対象 |
| エクスポート済みの Amazon 発行の証明書 | 対象 |
| ACM で要求し、関連付けまたはエクスポートしたプライベート証明書 | 対象 |
| Private CA の `IssueCertificate` API で発行した証明書 | 対象外 |
| インポートした証明書 | 対象外 |
| 期限切れの証明書 | 対象外 |

DNS 検証のものは自動で更新され、メール検証のものは更新の案内がメールで届きます。

- **計算の例:** 2026 年 1 月 1 日に発行した公開証明書は、198 日後の 7 月 18 日に切れる。45 日前の 6 月 3 日ごろから更新を確認する。ARN は変わらない。
- **誤ると:** CNAME を消したあとは、次の更新のときに検証できず、期限の日に HTTPS のエラーで全利用者に影響する。
- **誤ると:** ALB から外した証明書は「使っていない」ので自動更新されない。同じドメインで付け直す予定があるなら、期限を確認する。

### リージョンのルール {#region-rules}

ACM の証明書はリージョンのリソースです。リージョン間でコピーできないので、必要なリージョンごとに作ります。

秘密鍵をリージョンの外に出さないので、リージョンごとに証明書が分かれます。CloudFront はグローバルなサービスで、ACM の証明書は `us-east-1` にあるものだけを使える仕様です。

| サービス | 証明書を置くリージョン |
| --- | --- |
| CloudFront | `us-east-1`（バージニア北部）のみ |
| API Gateway のエッジ最適化カスタムドメイン | `us-east-1`（内部で CloudFront を使用） |
| API Gateway のリージョナルカスタムドメイン | API と同じリージョン |
| ALB、NLB | ロードバランサーと同じリージョン |
| Elastic Beanstalk | 環境のロードバランサーと同じリージョン |

!!! tip "CloudFront の証明書が選択肢に出ない"
    多くの場合、証明書を `us-east-1` 以外で作っています。東京リージョンで動くアプリでも、CloudFront 用の証明書は `us-east-1` に作ります。

- **例:** 東京の ALB、東京の API（リージョナル）、CloudFront の 3 つで `www.example.com` を使うなら、証明書は東京に 1 枚、`us-east-1` に 1 枚の計 2 枚を作る。同じ CNAME で検証できる。
- **誤ると:** CloudFront の前に ALB を置き、両方を同じドメインにするときに、東京の証明書だけを作ると CloudFront に設定できない。

### 統合サービス {#integrated-services}

ACM と統合している主なサービスは次のとおりです。

- Elastic Load Balancing
- Amazon CloudFront
- Amazon API Gateway
- AWS Elastic Beanstalk
- AWS Amplify
- Amazon Cognito（カスタムドメイン）
- AWS App Runner
- Amazon OpenSearch Service
- AWS Network Firewall
- AWS Nitro Enclaves
- AWS CloudFormation（証明書をリソースとして定義）

EC2 上のサーバーに直接置くには、エクスポート可能な公開証明書か、ACME プロトコルを使います。

- **エクスポート可能な公開証明書**: 要求時に有効にする。2025 年 6 月 17 日より前に作った証明書はエクスポートできない。
- **ACME**: Web サーバー上で発行と更新を自動化する。ACM のマネージド更新の対象外で、ACME クライアントが更新を担う。

ただし、一般的には EC2 の前に ALB や CloudFront を置いて、そこに証明書を設定するほうが簡単です。

- **ALB の例:** HTTPS リスナーの `Certificates` に証明書の ARN を指定する。
- **EC2 の例:** nginx が使う `fullchain.pem` と `privkey.pem` をエクスポート可能な公開証明書から取り出す。更新されたら再度エクスポートして配置し直す。
- **誤ると:** 通常の公開証明書は秘密鍵を取り出せない。`ExportCertificate` が拒否される。

### 証明書のインポート {#import}

他の CA が発行した証明書は ACM にインポートできます。

**使う場面:** グループ会社の規程で、決められた CA の証明書しか使えない。買った証明書を ALB で使うために、ACM へ取り込む（[ネット銀行の例](#use-case-netbank)）。

```bash
aws acm import-certificate \
  --certificate fileb://cert.pem \
  --private-key fileb://key.pem \
  --certificate-chain fileb://chain.pem
```

- ACM は自動更新しないので、新しい証明書を取得して再インポートする。ARN と関連付けは維持される。
- 期限の管理は自分の責任。EventBridge で期限切れが近いイベントを受け取り、通知する。
- 同じリージョンのルールが適用される。CloudFront 用は `us-east-1` にインポートする。
- **例:** 2027 年 3 月 31 日に切れる証明書をインポートすると、インポートした証明書は 45 日前の 2 月 14 日から毎日 `ACM Certificate Approaching Expiration` が届く。
- **誤ると:** 再インポートを `--certificate-arn` なしで実行すると、新しい ARN の別の証明書になり、ALB は古い証明書を使い続ける。

## AWS Private CA {#private-ca}

[:material-certificate: DVA](../courses/dva/services.md){ .exam-badge .exam-associate } [:material-target: SCS](../courses/scs/services.md){ .exam-badge .exam-specialty }

ルート CA と下位 CA からなるプライベート CA の階層を、自前の設備なしで運用するサービスです。

**提供単位:** プライベート CA はリージョンのリソースで、VPC の外にあります。

#### なぜ必要か {#private-ca-why}

社内のサービスや機器にも TLS の証明書が要ります。しかし公開 CA は、`api.internal.example.com` のような社内だけの名前には発行できず、端末の数だけ証明書を買うのも現実的ではありません。そこで、自社だけが信頼する CA を持ちます。

オンプレミスでは、Active Directory 証明書サービスなどで社内 CA を立てるのが一般的です。

| 観点 | オンプレミスの社内 CA | AWS Private CA |
| --- | --- | --- |
| 同じ点 | ルート CA と下位 CA の階層を作り、社内の端末にルートを信頼させる | 同じ |
| CA の秘密鍵の保護 | 自社で HSM を用意するか、サーバーのディスクに置く | AWS が管理する HSM に置く |
| 可用性とバックアップ | CA サーバーの冗長化、バックアップを自社で行う | AWS が行う |
| 失効の仕組み | CRL の配布先や OCSP サーバーを自社で立てる | CRL を S3 に出力、OCSP は設定で有効にする |
| 証明書の自動更新 | 自動登録の仕組みを作り込む | ACM 経由で要求すれば ACM が更新する |

```mermaid
flowchart TD
    R["ルート CA<br/>めったに使わない"] --> P["下位 CA: 本番"]
    R --> D["下位 CA: 開発"]
    P --> P1["api.internal.example.com"]
    P --> P2["クライアント証明書（mTLS）"]
    D --> D1["dev.internal.example.com"]
```

ルートと下位に分けるのは、日々の発行に使う鍵が漏れても、被害をその下位 CA だけに閉じ込めるためです。ルートが無事なら、下位 CA を失効させて作り直せます。

| 用途 | 例 |
| --- | --- |
| 社内の TLS | 内部 API、内部 ALB |
| クライアント、デバイスの認証 | mTLS、IoT デバイス |
| コード署名 | 内部のソフトウェアの署名 |
| 失効の確認 | OCSP |

証明書の発行の方法で、管理のしかたが変わります。

| 発行の方法 | 使える場所 | 自動更新 |
| --- | --- | --- |
| ACM で要求（`--certificate-authority-arn`） | ACM の統合サービス。エクスポートすれば他でも可 | 対象 |
| Private CA の API（`IssueCertificate`） | どこでも | 対象外。自分で管理 |

```bash
aws acm request-certificate \
  --domain-name api.internal.example.com \
  --certificate-authority-arn arn:aws:acm-pca:ap-northeast-1:111122223333:certificate-authority/EXAMPLE
```

プライベート CA はリージョンのリソースで、リージョン間でコピーできません。クライアント側には、ルート CA 証明書を信頼するよう設定します。

- **ACM で要求する例:** 上のコマンドで作ると、ALB に付けられ、自動で更新される。
- **`IssueCertificate` の例:** mTLS のクライアントに配る証明書を 90 日の有効期間で発行する。更新の仕組みは自分で作る。
- **誤ると:** 自前で更新を作らずに `IssueCertificate` の証明書を使うと、期限の日に通信が止まる。
- **誤ると:** クライアントがルート CA を信頼していないと、TLS のハンドシェイクで `unable to get local issuer certificate` のようなエラーになる。

## 開発用の証明書と SSH キーの生成 {#dev-certs-ssh}

開発やテストでは、CA を使わずに自分で作れます。本番の公開サイトには使いません。

| 用途 | ツール |
| --- | --- |
| ローカルの HTTPS、テスト環境の TLS | `openssl` の自己署名証明書 |
| EC2 への SSH | EC2 キーペア、`ssh-keygen` |
| 内部で信頼する証明書を本格的に発行 | AWS Private CA |
| SSH キーの管理を避ける | Systems Manager Session Manager |

### 自己署名証明書 {#self-signed}

```bash
# 秘密鍵と自己署名証明書を 1 回で作る
openssl req -x509 -newkey rsa:2048 -nodes -sha256 -days 90 \
  -keyout key.pem -out cert.pem \
  -subj "/CN=localhost" \
  -addext "subjectAltName=DNS:localhost,IP:127.0.0.1"

# 内容の確認
openssl x509 -in cert.pem -noout -subject -dates -ext subjectAltName
```

**使う場面:** スマートフォンのアプリの開発で、手元の API サーバーを `https://localhost` で動かし、本番と同じく HTTPS で通信を確かめる。

CA に署名を依頼する場合は、CSR を作ります。

```bash
openssl req -new -newkey rsa:2048 -nodes \
  -keyout server.key -out server.csr \
  -subj "/CN=dev.example.com"
```

- 自己署名証明書はクライアントから信頼されないので、ブラウザに警告が出る。
- 秘密鍵をリポジトリにコミットしない。`.gitignore` に入れ、必要なら [Secrets Manager](secrets.md) に置く。
- ALB でテストするには、ACM にインポートする。自動更新はされない。
- **例:** 上の `-days 90` は 90 日。91 日目にローカルのアプリがブラウザで期限切れの警告を出す。
- **例:** `-nodes` は秘密鍵を暗号化しない指定。CI で使うならこのままで、持ち運ぶならパスフレーズを付ける。ACM にはパスフレーズなしの鍵しかインポートできない。
- **誤ると:** `subjectAltName` を省くと、現代のブラウザは CN だけでは名前を確認しないので、`localhost` でも一致しないと表示される。

### SSH キーと EC2 キーペア {#ssh-keys}

**使う場面:** 検証用の EC2 に、開発者 3 人が自分の PC から SSH で入る。各自が `ssh-keygen` で作った公開鍵を登録し、秘密鍵は各自の PC から出さない。

EC2 キーペアでは、公開鍵を EC2 が持ち、秘密鍵は自分で保管します。AWS は秘密鍵を保存しないので、なくすと取り戻せません。

オンプレミスのサーバーで `~/.ssh/authorized_keys` に公開鍵を書くのと同じ仕組みです。違いは、インスタンスの起動時に EC2 が公開鍵を自動で書き込む点です。人が増えるほど鍵の配布と回収が大変になるので、鍵を使わずに IAM の権限で入れる Session Manager も選択肢になります。

- **例:** キーペアはリージョンのリソース。東京で作った `dev-key` は大阪では選べない。同じ公開鍵を大阪にも `import-key-pair` すれば、同じ秘密鍵で入れる。

| キーの種類 | Linux | Windows |
| --- | --- | --- |
| RSA 2048 ビット | 可 | 可 |
| ED25519 | 可 | 不可 |

AWS に作らせる方法です。秘密鍵はこの応答でしか得られません。

```bash
aws ec2 create-key-pair \
  --key-name dev-key \
  --key-type ed25519 \
  --query 'KeyMaterial' \
  --output text > dev-key.pem

chmod 400 dev-key.pem
ssh -i dev-key.pem ec2-user@<public-dns>
```

手元で作って公開鍵だけを登録する方法です。秘密鍵が AWS を通らないので、より安全です。

```bash
ssh-keygen -t ed25519 -f ~/.ssh/aws-dev -C "dev"

aws ec2 import-key-pair \
  --key-name aws-dev \
  --public-key-material fileb://~/.ssh/aws-dev.pub
```

| 症状 | 原因と対処 |
| --- | --- |
| `UNPROTECTED PRIVATE KEY FILE` | 秘密鍵の権限が広い。`chmod 400` にする |
| 秘密鍵をなくした | 取り戻せない。新しい公開鍵をインスタンスに追加する、または Session Manager で入る |
| Windows のパスワードが読めない | 秘密鍵で管理者パスワードを復号する |

- **`--key-type` の例:** Linux なら `ed25519`、Windows なら `rsa`。`ed25519` のキーペアは Windows インスタンスに指定できない。
- **`ssh-keygen -C` の例:** `-C "dev"` は公開鍵の末尾のコメント。誰の鍵かを示す。
- **誤ると:** `ssh -i dev-key.pem root@...` では入れない。Amazon Linux のユーザーは `ec2-user`。

## 転送時の TLS {#tls-in-transit}

TLS の終端の場所を決めるのが設計の中心です。

TLS を終端した場所では、通信が平文に戻ります。終端を前に寄せるほど証明書の管理は楽になり、後ろのサーバーの負荷も減りますが、その先の区間を平文で流すかどうかを決める必要があります。

```mermaid
flowchart LR
    U["利用者"] -- "HTTPS<br/>ACM（us-east-1）" --> CF["CloudFront"]
    CF -- "HTTPS<br/>オリジンの証明書" --> ALB["ALB"]
    ALB -- "HTTP または HTTPS<br/>自己署名でも可" --> EC2["EC2"]
    EC2 -- "TLS<br/>RDS の CA" --> RDS["RDS"]
```

オンプレミスでいえば、ロードバランサー（リバースプロキシ）で SSL を終端する構成と同じです。違いは、終端する ALB や CloudFront の証明書を ACM が自動で更新する点です。

| 区間 | 設定 | 証明書 |
| --- | --- | --- |
| 利用者から CloudFront | ビューワープロトコルポリシー（HTTPS にリダイレクトなど） | ACM（`us-east-1`） |
| CloudFront からオリジン | オリジンプロトコルポリシー | オリジンの証明書 |
| 利用者から ALB | HTTPS リスナーとセキュリティポリシー | ACM（同じリージョン） |
| ALB からターゲット | ターゲットグループの HTTPS | 自己署名でも可 |
| 利用者から API Gateway | カスタムドメインに証明書を設定 | エッジ最適化なら `us-east-1` |
| アプリから RDS | TLS で接続 | RDS の CA を信頼 |

データの暗号化の全体は [KMS](kms.md) を参照してください。

- **例:** CloudFront のビューワープロトコルポリシーを `redirect-to-https` にすると、`http://` のリクエストは 301 で `https://` に転送される。
- **例:** ALB から EC2 の間を HTTPS にするとき、ターゲットの証明書は検証されないので、自己署名でも通る。
- **誤ると:** CloudFront のオリジンプロトコルを `https-only` にして、オリジンに自己署名の証明書を置くと、CloudFront は `502` を返す。オリジンには信頼された CA の証明書が要る。

### 相互 TLS（mTLS） {#mtls}

サーバーだけでなく、クライアントも証明書で認証します。API Gateway のカスタムドメインでは、次のように設定します。

通常の TLS では、クライアントがサーバーの身元を確かめるだけです。取引先のシステムや IoT 機器のように、人がパスワードを入力しない相手を認証したいときは、クライアントにも証明書を持たせます。受付で、来訪者も社員証を見せる形です。

| 観点 | 通常の TLS | mTLS |
| --- | --- | --- |
| 証明書を出す側 | サーバーだけ | サーバーとクライアントの両方 |
| クライアントの認証 | アプリでパスワードやトークンを確認 | TLS の接続時に証明書で確認 |
| 主な用途 | 一般の Web サイト | 取引先との API 連携、IoT、サービス間通信 |

1. クライアント証明書を信頼する CA のトラストストアを S3 に置く。
2. カスタムドメインで mutual TLS を有効にする。
3. 既定の `execute-api` エンドポイントを無効にし、迂回を防ぐ。

クライアント証明書の発行には、AWS Private CA を使えます。

- **例:** トラストストアを `s3://my-trust/truststore.pem` に置き、`aws apigateway create-domain-name --domain-name api.example.com --mutual-tls-authentication truststoreUri=s3://my-trust/truststore.pem` のように指定する。
- **誤ると:** `execute-api` のエンドポイントを残すと、そちらから mTLS なしで呼べてしまう。

## AWS WAF {#waf}

[:material-sprout: CLF](../courses/clf/services.md){ .exam-badge .exam-foundational } [:material-certificate: SAA](../courses/saa/services.md){ .exam-badge .exam-associate } [:material-certificate: DVA](../courses/dva/services.md){ .exam-badge .exam-associate } [:material-certificate: SOA](../courses/soa/services.md){ .exam-badge .exam-associate } [:material-certificate: DEA](../courses/dea/services.md){ .exam-badge .exam-associate } [:material-star-circle: SAP](../courses/sap/services.md){ .exam-badge .exam-professional } [:material-star-circle: DOP](../courses/dop/services.md){ .exam-badge .exam-professional } [:material-star-circle: AIP](../courses/aip/services.md){ .exam-badge .exam-professional } [:material-target: ANS](../courses/ans/services.md){ .exam-badge .exam-specialty } [:material-target: SCS](../courses/scs/services.md){ .exam-badge .exam-specialty }

HTTP(S) リクエストを検査して、許可、ブロック、カウントなどを行うファイアウォールです。ウェブ ACL は、現在のコンソールでは protection pack とも呼ばれます。

**提供単位:** ウェブ ACL は、CloudFront 用がグローバルで `us-east-1` に作り、それ以外はリージョンごとに作ります。どちらも VPC の外にあります（[提供単位の一覧](resource-scope.md#scope-global)）。

#### なぜ必要か {#waf-why}

セキュリティグループや NACL は、IP アドレスとポートしか見ません。SQL インジェクションのような攻撃は、正規の利用者と同じ 443 番ポートに、正しい形の HTTPS で届きます。通信の中身（パス、ヘッダー、本文）を見なければ、攻撃と正常なリクエストを区別できません。

| 困りごと | WAF がないと起きること | WAF の仕組み |
| --- | --- | --- |
| SQL インジェクション、XSS | アプリのコードの抜けがそのまま攻撃される | マネージドルールで既知の攻撃の形を止める |
| ログインの総当たり | 1 つの IP から大量の試行が続く | レートベースルール |
| 特定の国や IP からの攻撃 | セキュリティグループに大量の IP を書くことになる | IP セット、地理的一致 |
| ボット | 在庫の買い占めや大量のスクレイピング | CAPTCHA、Challenge |

オンプレミスのネットワーク機器と対応させると、次のようになります。

| AWS | オンプレミスでの相当品 | 見るもの | 違う点 |
| --- | --- | --- | --- |
| セキュリティグループ | ホストのファイアウォール | IP、ポート | ENI 単位に付く。ステートフル |
| NACL | ルーターの ACL | IP、ポート | サブネット単位。ステートレス |
| AWS WAF | WAF アプライアンス、リバースプロキシの WAF | HTTP の中身 | 機器を置かない。CloudFront や ALB に関連付けるだけ |
| Network Firewall | 次世代ファイアウォール、IPS | パケット、ドメイン名、シグネチャ | VPC のルートで通信を通す（[脅威検出](threat-detection.md#network-firewall)） |
| Shield | ISP や専門業者の DDoS 対策 | 大量の通信 | Standard は全利用者に自動で適用 |

```mermaid
flowchart TD
    A["守りたいものは?"] --> B{"HTTP の中身<br/>（パス、本文、ヘッダー）で判断?"}
    B -- はい --> WAF["AWS WAF"]
    B -- いいえ --> C{"VPC を出入りする<br/>すべての通信を検査?"}
    C -- はい --> NFW["Network Firewall"]
    C -- いいえ --> D{"IP とポートで<br/>十分?"}
    D -- はい --> SG["セキュリティグループ、NACL"]
    D -- いいえ: 大量の通信 --> SH["Shield"]
```

機器を置かない設計なので、通信量に合わせて容量を増やす作業はありません。その代わり、WAF を関連付けられるのは対応するサービスだけで、EC2 や NLB には直接付けられません。

### アタッチできる場所 {#waf-resources}

| スコープ | リソース | 作成先 |
| --- | --- | --- |
| グローバル | CloudFront ディストリビューション | `us-east-1` |
| リージョナル | ALB | リソースと同じリージョン |
| リージョナル | API Gateway の REST API | 同上 |
| リージョナル | AppSync GraphQL API | 同上 |
| リージョナル | Cognito ユーザープール | 同上 |
| リージョナル | App Runner、Amplify、Verified Access、Bedrock AgentCore Gateway | 同上 |

対応一覧に、NLB、API Gateway の HTTP API、EC2 のインスタンスはありません。保護するには、前に CloudFront や ALB を置きます。

- **例:** HTTP API を守るなら、前に CloudFront を置いて、CloudFront のウェブ ACL で検査する。ALB の後ろの EC2 なら、ALB に付ければ足りる。
- **誤ると:** 東京の ALB に付けるウェブ ACL を `CLOUDFRONT` スコープで作ると、関連付けに失敗する。`REGIONAL` のスコープで東京に作る。

### ウェブ ACL の構成 {#web-acl}

```mermaid
flowchart TD
    A["リクエスト"] --> B["優先度の小さいルールから評価"]
    B --> C{"ルールに一致?"}
    C -- "Allow / Block" --> D["評価を終了して適用"]
    C -- "Count" --> E["記録して次のルールへ"]
    C -- "一致なし" --> E
    E --> F{"残りのルールは?"}
    F -- ある --> C
    F -- ない --> G["既定のアクションを適用"]
```

| 要素 | 内容 |
| --- | --- |
| ルール | 検査の条件（ステートメント）とアクション |
| 優先度 | 数値。小さいものから順に評価 |
| 既定のアクション | どのルールでも終了しなかったときの動作。`Allow` または `Block` |
| ルールグループ | ルールの再利用可能なまとまり |
| マネージドルールグループ | AWS や販売者が管理するルール |
| WCU | ルールの処理に必要な容量。ウェブ ACL の上限は 5,000 で、1,500 を超えると追加料金 |

| アクション | 動作 | 終了するか |
| --- | --- | --- |
| Allow | 転送する。カスタムヘッダーを追加可能 | する |
| Block | 既定で HTTP 403 を返す。応答はカスタマイズ可能 | する |
| Count | 数えて記録するだけ | しない |
| CAPTCHA, Challenge | ボットかどうかを確認する。トークンが有効なら次のルールへ | 状況による |

| 検査できるもの | 例 |
| --- | --- |
| 送信元 IP | IP セットで許可、ブロック |
| 国 | 地理的一致 |
| 文字列、正規表現 | パス、ヘッダー、本文 |
| サイズ | 本文が大きすぎるリクエスト |
| SQL インジェクション、XSS | 専用のステートメント |
| リクエストのレート | レートベースルール |

新しいルールはまず `Count` で動かし、正常なリクエストを止めないことを確認してから `Block` にします。

- **優先度の例:** 優先度 0 で社内の IP を `Allow`、優先度 1 で国の制限を `Block`、優先度 2 でマネージドルールにする。社内の IP からは優先度 0 で評価が終わるので、後のルールで止まらない。
- **既定のアクションの例:** 公開サイトは `Allow`。特定の IP だけに使わせる社内向けは `Block` にして、その IP の `Allow` ルールを置く。
- **WCU の計算の例:** `AWSManagedRulesCommonRuleSet` の 700 WCU と、レートベースルールの基本 2 WCU で 702 WCU。5,000 の上限に収まり、1,500 以下なので追加料金もかからない。
- **Block の例:** `CustomResponse` で 403 の代わりに `429` と本文を返せる。
- **誤ると:** 優先度の小さい `Allow` が広すぎると、後の `Block` まで評価されない。SQL インジェクションのルールを Allow の後に置くと、社内の IP では検査されない。

### レートベースルール {#rate-based-rules}

一定時間のリクエスト数が上限を超えた送信元などを、一時的に制限します。

ログインの総当たりやスクレイピングは、1 回ずつのリクエストを見ると正常と区別できません。「回数」を見て初めて分かる攻撃のための仕組みです。IP を手で書き足すブロックリストと違い、上限を下回れば自動で制限が解けます。

| 設定 | 内容 |
| --- | --- |
| 評価ウィンドウ | 60、120、300、600 秒。既定は 300 秒 |
| レート制限 | ウィンドウ内の上限のリクエスト数。最小 10 |
| 集約 | 送信元 IP、ヘッダー内の IP、カスタムキーなど。全リクエストのカウントも可 |
| アクション | Allow 以外 |
| スコープダウン | 対象を絞る条件。「すべてカウント」では必須 |

```json
{
  "Name": "ip-rate-limit",
  "Priority": 1,
  "Statement": {
    "RateBasedStatement": {
      "Limit": 100,
      "EvaluationWindowSec": 300,
      "AggregateKeyType": "IP"
    }
  },
  "Action": {"Block": {}},
  "VisibilityConfig": {
    "SampledRequestsEnabled": true,
    "CloudWatchMetricsEnabled": true,
    "MetricName": "ip-rate-limit"
  }
}
```

- `/login` だけを制限したいときは、`ScopeDownStatement` で対象を絞る。
- 上限の付近で制限されるが、正確な一致は保証されない。
- CloudFront の背後の ALB に WAF を置くと、送信元 IP が CloudFront になる。CloudFront に付けるか、`X-Forwarded-For` などの転送 IP を集約キーにする。
- **`Limit` の例:** `100` で `EvaluationWindowSec` が 300 なら、1 つの IP が 5 分間に約 100 回を超えると、それ以降のリクエストをブロックする。秒に直すと約 0.33 回/秒なので、普通の閲覧者にも当たりうる。
- **`ScopeDownStatement` の例:** `UriPath` が `/login` で始まるリクエストだけを数えるので、ログインの総当たりを止めつつ、画像の取得を数えない。
- **誤ると:** 反応には数分かかることがある。設定を変えるとカウントがリセットされ、最大 1 分ほど制限が止まる場合がある。短い間のスパイクを正確に止めたいなら、API Gateway のスロットリングを併用する。

### 似た機能との比較 {#waf-comparison}

| 機能 | 動作する層 | 使いどころ | 超過時の応答 |
| --- | --- | --- | --- |
| AWS WAF | HTTP（L7） | SQL インジェクション、XSS、IP やレートの制限 | 既定で HTTP 403 |
| API Gateway のスロットリング | API | API キーや使用量プランごとの呼び出し制限 | HTTP 429 |
| セキュリティグループ | IP とポート | インスタンスや ENI への通信制限 | 応答なしで破棄 |

ネットワーク側の制御は [ネットワーク](networking.md) を参照してください。

- **例:** 同じ `/orders` に WAF で 5 分 2,000 回の IP 制限を、API Gateway で秒間 100 回のスロットリングを設定する。前者は特定の IP を 403 で止め、後者は全体の負荷を 429 で止める。

### ウェブ ACL の関連付け {#waf-association}

```bash
# リージョナルリソースの関連付け
aws wafv2 associate-web-acl \
  --web-acl-arn arn:aws:wafv2:ap-northeast-1:111122223333:regional/webacl/app/EXAMPLE \
  --resource-arn arn:aws:elasticloadbalancing:ap-northeast-1:111122223333:loadbalancer/app/my-alb/EXAMPLE
```

CloudFront の場合は、ディストリビューション設定でウェブ ACL を指定します。CloudFormation でも、CloudFront のディストリビューション設定側に記述します。

- **`--scope` の例:** 一覧を見るときは `aws wafv2 list-web-acls --scope REGIONAL --region ap-northeast-1`、CloudFront 用は `--scope CLOUDFRONT --region us-east-1`。
- **誤ると:** `--region ap-northeast-1` で `--scope CLOUDFRONT` を指定すると、エラーになる。

## ACM の設定の詳細 {#acm-settings}

### 証明書の要求 {#request-settings}

| 項目 | 値 |
| --- | --- |
| `ValidationMethod` | `DNS`, `EMAIL`, `HTTP`（CloudFront の Distribution Tenants のみ）。後から変更できない |
| `KeyAlgorithm` | 既定は RSA。`RSA_2048`, `EC_prime256v1`, `EC_secp384r1` などから選ぶ |
| ドメイン名の数 | 既定 10 個。ACME で発行する証明書は 100 個で固定 |
| 有効期間 | 公開証明書は 198 日 |

連携先のサービスが対応するアルゴリズムしか使えません。証明書のキーが連携先に対応していないと、選択肢に出ないか、関連付けに失敗します。

- **`KeyAlgorithm` の例:** 応答を小さくしたいなら `EC_prime256v1`。`--key-algorithm EC_prime256v1` を付けて要求する。古いクライアントの互換性を優先するなら `RSA_2048`。
- **`ValidationMethod` の例:** Route 53 を使えるなら `DNS`。DNS を変更できず、`admin@example.com` のメールだけを受け取れるなら `EMAIL`。
- **誤ると:** `RSA_1024` は公開証明書には要求できない。

### DNS 検証の注意点 {#dns-validation-details}

- ACM はドメイン名ごとに CNAME を 1 つ指定する。`example.com` と `www.example.com` なら 2 つ。
- CNAME が残っていれば、同じドメインの別の証明書でも再検証は不要。
- CNAME のチェーンが 5 つを超えると解決に失敗する。それより長いチェーンが必要なら、メール検証を使う。
- **例:** `_a79865eb4cd1a6ab990a45779b4e0b96.example.com` のような名前に、`_424c7224e9b0146f9a8808af955727d0.acm-validations.aws.` のような値を持つ CNAME を追加する。Route 53 なら「Route 53 でレコードを作成」で足せる。
- **誤ると:** DNS の管理画面で名前の末尾にドメインが自動で付く場合、`example.com` まで入れると `...example.com.example.com` になり、検証が通らない。

### メール検証の注意点 {#email-validation-details}

送り先は `admin@`, `administrator@`, `hostmaster@`, `postmaster@`, `webmaster@` です。WHOIS の連絡先には送りません。古い教材の記述が残っているので注意します。

更新のメールも期限の 45 日前に届きます。リンクを選ばないと更新されません。

- **例:** `www.example.com` を申請すると、`www` を除いた `admin@example.com` などの 5 つに届く。`sub.example.com` のメールを受け取れないなら、検証ドメインに `example.com` を指定する。
- **例:** 検証メールのトークンは 72 時間で切れるので、切れたら再送する。
- **誤ると:** 担当者の退職で `admin@` を誰も見ていないと、更新の案内が届いても処理されず、198 日で切れる。

### 更新の監視 {#renewal-monitoring}

| 手段 | タイミングと内容 |
| --- | --- |
| `DaysToExpiry` メトリクス | 証明書ごとに 1 日 2 回。期限切れの後は発行しない |
| `ACM Certificate Approaching Expiration` | EventBridge のイベント。プライベートとインポートは 45 日前から、公開は 30 日前から毎日 |
| `ACM Certificate Expired` | 期限切れのイベント |
| 更新できないときの通知 | 期限の 30、15、7、3、1 日前に AWS Health と EventBridge に送る |

インポートした証明書を管理するなら、`DaysToExpiry` に CloudWatch アラームを付けるか、EventBridge から通知します。

- **`DaysToExpiry` の例:** しきい値を `30` にして、`DaysToExpiry < 30` で SNS に通知する。`AWS/CertificateManager` 名前空間の `CertificateArn` ディメンションで指定する。
- **EventBridge の例:** パターンの `detail-type` を `ACM Certificate Approaching Expiration` にして、Lambda で再インポートを自動化する。開始の日数は `PutAccountConfiguration` で変えられる。
- **誤ると:** 期限切れの後はメトリクスが出なくなるので、アラームの「データ不足」を無視すると、切れたことに気づけない。

自動更新は、統合サービスで使用中か、エクスポートされていること、DNS の CNAME が残っていることなどが条件です。使っていない証明書は更新されません。

### インポートの条件 {#import-requirements}

| 項目 | 条件 |
| --- | --- |
| 形式 | すべて PEM。DER はエラー |
| 秘密鍵 | 暗号化なしで、5 KB（5,120 バイト）まで |
| 証明書 | X.509 v3 |
| キー | RSA 1024, 2048, 3072, 4096、ECDSA 256, 384, 521 |
| 上限 | 2,500 枚。直近 365 日で 5,000 枚 |
| 更新 | 自動更新なし。再インポートで ARN と関連付けを維持 |

パスフレーズ付きの秘密鍵はそのままインポートできません。先に解除します。

- **例:** `openssl rsa -in encrypted.key -out key.pem` でパスフレーズを外し、インポートのあとで手元の平文の鍵を消す。
- **例:** DER 形式は `openssl x509 -inform der -in cert.der -out cert.pem` で PEM にする。
- **誤ると:** `--certificate-chain` を省くと、中間証明書が渡らず、クライアントによっては信頼できないと判断される。

## Private CA の設定の詳細 {#private-ca-settings}

| 設定 | 値 | 内容 |
| --- | --- | --- |
| CA の種類 | Root, Subordinate | 下位 CA には親の署名が必要。外部の CA に署名してもらうなら CSR を使う |
| モード | 汎用（既定）, 短期証明書 | 下の表 |
| キーのアルゴリズム | 既定 RSA 2048 | RSA 3072, 4096, ECDSA P256, P384 など |
| 失効 | CRL, OCSP | 短期証明書では省略できる場合がある |

| 観点 | 汎用 | 短期証明書 |
| --- | --- | --- |
| 証明書の期間 | 任意 | 最大 7 日 |
| 失効の仕組み | 通常は必要 | 短いので省略できる場合あり |
| 階層 | どこでも | 階層の最後に置く |
| 料金 | 高い | 低い |

**使う場面:** 社内のサービスメッシュで、コンテナ同士の mTLS に 1 日で切れる証明書を使う。失効の仕組みを持たずに、盗まれた証明書の影響を短く抑えられるので、短期証明書モードを選ぶ。

CA 1 つあたりの証明書は累計 100 万枚です。Private CA の証明書は、ACM の枚数の上限には数えません。

- **種類の例:** ルート CA の下に、本番用と開発用の 2 つの下位 CA を作る。下位 CA が侵害されても、ルートは無事なので下位だけを失効できる。
- **`UsageMode` の例:** `SHORT_LIVED_CERTIFICATE` なら 7 日以内で発行し、サービスメッシュの mTLS のように頻繁に自動更新する用途に使う。
- **キーの例:** 規格の要件に合わせて、`RSA_2048` の代わりに `EC_prime256v1` を選ぶ。作成後は変えられない。
- **誤ると:** ACM は短期証明書モードの CA からは発行できない。ALB で ACM の自動更新と組み合わせたいなら、汎用モードを選ぶ。

## WAF の設定の詳細 {#waf-settings}

### スコープと関連付け {#waf-scope}

**使う場面:** 東京で動く会員サイトの ALB と、同じ会員向けの REST API に、共通のウェブ ACL を 1 つ付けて、ルールの変更を 1 か所で済ませる。

- 1 つのリソースには、1 つのウェブ ACL だけ付けられる。
- 1 つのウェブ ACL は複数のリソースに付けられる。
- CloudFront に付けたウェブ ACL は、他の種類のリソースに付けられない。
- **例:** 東京の ALB と API Gateway に同じウェブ ACL を付けられる。大阪の ALB には、大阪のウェブ ACL を別に作る。
- **誤ると:** 1 つの ALB に 2 つのウェブ ACL を同時に効かせることはできない。チームごとのルールも、1 つのウェブ ACL にまとめる。

### 容量と本文の検査 {#waf-capacity-body}

| 項目 | 値 |
| --- | --- |
| WCU の上限 | ウェブ ACL あたり 5,000 |
| 追加料金 | 1,500 WCU を超えた分 |
| レートベースルールの WCU | 基本 2。カスタム集約キーごとに 30 を加算 |
| 本文の検査の上限（ALB, AppSync） | 8 KB で固定 |
| 本文の検査の上限（CloudFront, API Gateway, Cognito, App Runner, Verified Access, AgentCore Gateway） | 既定 16 KB。16、32、48、64 KB から選べる |
| 検査対象 | 上限を超えた部分は検査しない。`Oversize handling` で扱いを決める |

16 KB より大きい本文を受ける API では、攻撃文字列を 16 KB より後ろに置かれると、SQL インジェクションのルールを通過してしまいます。サイズ制約のルールで大きいリクエストを止めるか、上限を引き上げます。

- **オーバーサイズの例:** 検査の `OversizeHandling` は `CONTINUE`（検査できた範囲で評価）、`MATCH`（一致として扱う）、`NO_MATCH`（一致しないとして扱う）から選ぶ。SQL インジェクションのルールでは `MATCH` にすると、20 KB の本文は Block になる。
- **計算の例:** ALB で 20 KB の本文を受けると、検査できるのは先頭の 8 KB だけで、残りの 12 KB は検査されない。
- **誤ると:** CloudFront で上限を 64 KB にすると、16 KB を超える本文の検査には追加料金がかかる。

### ルールのアクションの詳細 {#waf-actions-details}

| アクション | 応答の詳細 |
| --- | --- |
| Allow | カスタムヘッダーを追加できる。ヘッダー名には `x-amzn-waf-` が付く |
| Block | 既定 403。カスタムの応答コードと本文を設定できる |
| Count | 続きのルールを評価する。ラベルを付けられる |
| CAPTCHA | トークンが無効なら HTTP 405 でパズルを返す |
| Challenge | トークンが無効なら HTTP 202 でサイレントチャレンジを返す |

| イミュニティ時間 | 既定 | 範囲 |
| --- | --- | --- |
| CAPTCHA | 300 秒 | 60〜259,200 秒 |
| Challenge | 300 秒 | 300〜259,200 秒 |

CAPTCHA と Challenge は HTTPS でブラウザからアクセスするときにしか動きません。API クライアントのルールに付けると、正常なリクエストが拒否されます。追加料金もかかります。

- **イミュニティの例:** CAPTCHA のイミュニティを 3,600 秒にすると、1 回解いた人は 1 時間パズルが出ない。既定の 300 秒だと 5 分ごとに解くことになり、利用者が離れやすい。
- **誤ると:** Challenge の 60 秒は範囲外で設定できない。下限は 300 秒。

**ラベル**は、一致したリクエストに付けるメタデータです。同じウェブ ACL の後のルールが、ラベルで判定できます。

**マネージドルールグループ**のルールは、ルールアクションのオーバーライドで Count にして試せます。代表的なものは `AWSManagedRulesCommonRuleSet`, `AWSManagedRulesSQLiRuleSet`, `AWSManagedRulesKnownBadInputsRuleSet` です。

- **ラベルの例:** マネージドルールが一致すると `awswaf:managed:aws:core-rule-set:SizeRestrictions_Body` のラベルが付く。Count にしておき、後のルールで「このラベルかつ `/upload` 以外」のときだけ Block する。
- **マネージドの例:** `AWSManagedRulesCommonRuleSet` は 700 WCU で、8 KB を超える本文を `SizeRestrictions_BODY` で止める。ファイルのアップロードが 403 になるのはこのルールが多い。

### レートベースルールの詳細 {#rate-based-details}

| 設定 | 値 |
| --- | --- |
| `EvaluationWindowSec` | 60、120、300、600。既定 300 |
| `Limit` | 最小 10 |
| `AggregateKeyType` | `IP`, `FORWARDED_IP`, `CUSTOM_KEYS`, `CONSTANT` |
| 他のステートメントの中に入れる | 不可 |

`Limit=100`、`EvaluationWindowSec=60` のルールは、IP ごとに直近 60 秒のリクエストを数えます。100 回を超えると、ルールのアクションを適用します。ウィンドウはチェックの間隔ではなく、振り返る長さです。

`FORWARDED_IP` は、どのヘッダーを使うかと、IP がないときの動作（`MATCH` か `NO_MATCH`）を指定します。

同じ設定のルールでも、2 つのウェブ ACL に置くとカウントは別々です。

`CONSTANT` はすべての一致するリクエストをまとめて数えるので、スコープダウンステートメントが必須です。

- **`AggregateKeyType` の例:** `IP` は送信元ごと。`FORWARDED_IP` は `X-Forwarded-For` の先頭の IP。`CUSTOM_KEYS` は `x-api-key` ヘッダーごと、のように数える。カスタムキーは 1 つごとに 30 WCU を加える。
- **`FORWARDED_IP` の例:** 欠けたときの動作を `MATCH` にすると、ヘッダーのないリクエストも制限の対象に数える。
- **誤ると:** ウェブ ACL あたりのレートベースルールは 10 個まで。

### ログ {#waf-logging}

**使う場面:** 不正な注文の問い合わせが来たとき、どの IP からどのルールで止めたか、または通したかを後から調べる。サンプルは一部しか残らないので、調査にはログを使う。

| 送信先 | 名前の条件 |
| --- | --- |
| CloudWatch Logs | ロググループ名が `aws-waf-logs-` で始まる |
| S3 | バケット名が `aws-waf-logs-` で始まる |
| Amazon Data Firehose | ストリーム名が `aws-waf-logs-` で始まる |

名前の接頭辞が違うと、送信先に選べません。これがよくある間違いです。

| 設定 | 内容 |
| --- | --- |
| フィールドの編集（redaction） | URI パス、クエリ文字列、単一のヘッダー、HTTP メソッドを隠せる |
| ログのフィルター | ルールのアクションや完全修飾ラベルで残すログを選ぶ |
| サンプルリクエスト | ログを有効にしなくても確認できる。ルールの `SampledRequestsEnabled` で設定 |

ログの redaction は、サンプルリクエストには影響しません。別に設定が必要です。

- **例:** 送信先に `arn:aws:logs:ap-northeast-1:111122223333:log-group:aws-waf-logs-prod` を指定する。CloudFront 用のウェブ ACL のログは `us-east-1` のロググループに送る。
- **redaction の例:** `authorization` ヘッダーを隠すと、ログには `REDACTED` と残る。トークンが漏れない。
- **フィルターの例:** `Block` のログだけを残すと、ログの量が減る。

### 監視 {#waf-monitoring}

ルールごとの `VisibilityConfig` で、CloudWatch のメトリクスとサンプルを有効にします。`CountedRequests`, `BlockedRequests`, `AllowedRequests` などのメトリクスで、ルールの影響を確認します。

新しいルールはまず Count で動かし、メトリクスと `CountedRequests` のサンプルを確認してから、Block に変えます。

- **例:** 新しいルールを 1 週間 Count にして、`CountedRequests` が 1 日 200 件、サンプルの中身がすべて攻撃なら Block に変える。正常な検索が混じっているなら、スコープダウンで除外する。
- **`MetricName` の例:** `ip-rate-limit` のように英数字とハイフンで書く。CloudWatch のメトリクス名になる。

## 既定値と上限のまとめ {#numbers}

| 項目 | 値 |
| --- | --- |
| ACM 公開証明書の有効期間 | 198 日 |
| 公開証明書の更新の開始 | 期限の 45 日前（旧 395 日のものは 60 日前） |
| ドメイン名の数 | 既定 10。ACME は 100 |
| 期限切れイベント | プライベート、インポートは 45 日前から。公開は 30 日前から |
| インポートした証明書の上限 | 2,500 枚 |
| インポートの秘密鍵 | 5 KB まで。暗号化なし |
| CNAME のチェーン | 5 つまで |
| 短期証明書モードの期間 | 最大 7 日 |
| Private CA あたりの証明書 | 累計 100 万枚 |
| ウェブ ACL の WCU | 5,000。1,500 超で追加料金 |
| ウェブ ACL の数 | 100（リージョンあたり） |
| ルールグループの数 | 100 |
| IP セットの数 | 100 |
| 正規表現パターンセット | 10 |
| ウェブ ACL の秒間リクエスト | 100,000 |
| レートベースルールのウィンドウ | 60、120、300、600 秒。既定 300 |
| レートベースルールの制限 | 最小 10 |
| 本文の検査 | ALB 8 KB。CloudFront など既定 16 KB、最大 64 KB |
| CAPTCHA のイミュニティ | 既定 300 秒。60〜259,200 秒 |
| Challenge のイミュニティ | 既定 300 秒。300〜259,200 秒 |

## 試験のポイント {#exam-points}

| こう問われたら | 答え |
| --- | --- |
| CloudFront 用の ACM 証明書のリージョン | `us-east-1` |
| ALB 用の ACM 証明書のリージョン | ALB と同じリージョン |
| エッジ最適化 API Gateway の証明書 | `us-east-1` |
| 証明書の更新を自動化する検証方法 | DNS 検証（CNAME を残す） |
| インポートした証明書の更新 | 自動ではない。再インポートする |
| インポートした証明書の期限の監視 | EventBridge のイベントで通知 |
| 社内サービス向けの証明書 | AWS Private CA |
| `*.example.com` で `example.com` は保護されるか | されない。SAN に追加する |
| 開発用の HTTPS の証明書を手元で作る | `openssl req -x509` の自己署名証明書 |
| EC2 用の SSH キーをなくした | 取り戻せない。新しい公開鍵を追加する |
| 既存の公開鍵を EC2 で使う | `aws ec2 import-key-pair` |
| Windows インスタンスのキーの種類 | RSA のみ |
| SQL インジェクションや XSS の遮断 | AWS WAF |
| 特定の IP からの大量アクセスを制限 | レートベースルール |
| WAF をアタッチできないもの | NLB、HTTP API、EC2 に直接など |
| CloudFront 用のウェブ ACL の作成先 | `us-east-1` |
| WAF の Block の既定の応答 | HTTP 403 |
| 新しいルールを影響なく試す | Count アクション |
| どのルールにも一致しないリクエスト | 既定のアクション |
| クライアントも証明書で認証する API | API Gateway の mutual TLS |
| WAF のログの送信先に選べない | 名前が `aws-waf-logs-` で始まっていない |
| ALB の本文で検査できるサイズ | 8 KB で固定 |
| 1 週間以内の証明書を発行し、失効を省く | Private CA の短期証明書モード |
| インポートする鍵の条件 | PEM で暗号化なし |

## 関連ページ {#related}

- [KMS](kms.md): 保存時と転送時の暗号化
- [ネットワーク](networking.md): CloudFront、ELB、Route 53
- [API Gateway](api-gateway.md): カスタムドメイン、スロットリング
- [EC2 と Elastic Beanstalk](ec2-beanstalk.md): インスタンスへの接続
- [IAM と STS](iam.md): サービス間の認証

## 参考 {#references}

- [What is AWS Certificate Manager?](https://docs.aws.amazon.com/acm/latest/userguide/acm-overview.html)
- [AWS Certificate Manager concepts](https://docs.aws.amazon.com/acm/latest/userguide/acm-concepts.html)
- [ACM certificate characteristics](https://docs.aws.amazon.com/acm/latest/userguide/acm-certificate-characteristics.html)
- [ACM DNS validation](https://docs.aws.amazon.com/acm/latest/userguide/dns-validation.html)
- [Managed certificate renewal](https://docs.aws.amazon.com/acm/latest/userguide/managed-renewal.html)
- [Renewal for domains validated by DNS](https://docs.aws.amazon.com/acm/latest/userguide/dns-renewal-validation.html)
- [Managed automation with integrated services](https://docs.aws.amazon.com/acm/latest/userguide/acm-services.html)
- [Import certificates into ACM](https://docs.aws.amazon.com/acm/latest/userguide/import-certificate.html)
- [Request a public certificate](https://docs.aws.amazon.com/acm/latest/userguide/acm-public-certificates.html)
- [Export an ACM public certificate](https://docs.aws.amazon.com/acm/latest/userguide/export-public-certificate.html)
- [ACM quotas](https://docs.aws.amazon.com/acm/latest/userguide/acm-limits.html)
- [What is AWS Private CA?](https://docs.aws.amazon.com/privateca/latest/userguide/PcaWelcome.html)
- [Using alternate domain names and HTTPS in CloudFront](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/cnames-and-https-requirements.html)
- [Edge-optimized custom domain names](https://docs.aws.amazon.com/apigateway/latest/developerguide/how-to-edge-optimized-custom-domain-name.html)
- [Regional custom domain names](https://docs.aws.amazon.com/apigateway/latest/developerguide/apigateway-regional-api-custom-domain-create.html)
- [Mutual TLS for REST APIs](https://docs.aws.amazon.com/apigateway/latest/developerguide/rest-api-mutual-tls.html)
- [Amazon EC2 key pairs](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-key-pairs.html)
- [Create a key pair for your EC2 instance](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/create-key-pairs.html)
- [What is AWS WAF?](https://docs.aws.amazon.com/waf/latest/developerguide/what-is-aws-waf.html)
- [Resources that you can protect with AWS WAF](https://docs.aws.amazon.com/waf/latest/developerguide/how-aws-waf-works-resources.html)
- [Configuring protection in AWS WAF](https://docs.aws.amazon.com/waf/latest/developerguide/web-acl.html)
- [Web ACL default action](https://docs.aws.amazon.com/waf/latest/developerguide/web-acl-default-action.html)
- [Setting rule priority](https://docs.aws.amazon.com/waf/latest/developerguide/web-acl-processing-order.html)
- [Using rule actions in AWS WAF](https://docs.aws.amazon.com/waf/latest/developerguide/waf-rule-action.html)
- [Rate-based rule statements](https://docs.aws.amazon.com/waf/latest/developerguide/waf-rule-statement-type-rate-based.html)
- [Rate-based rule high-level settings](https://docs.aws.amazon.com/waf/latest/developerguide/waf-rule-statement-type-rate-based-high-level-settings.html)
- [AWS WAF quotas](https://docs.aws.amazon.com/waf/latest/developerguide/limits.html)

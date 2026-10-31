# 分野3: エッジのセキュリティ

脅威に合わせて WAF、CloudFront、Shield を選び、ルールを設計する力を問います。他社の製品やログの形式との統合も範囲です。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [3.1.1](../../domain3.md#skill-3-1-1) | 脅威に応じたエッジ戦略の選択 |
| [3.1.2](../../domain3.md#skill-3-1-2) | エッジの保護の実装 |
| [3.1.3](../../domain3.md#skill-3-1-3) | 要件に基づくルールの設計 |
| [3.1.4](../../domain3.md#skill-3-1-4) | エッジと他社サービスの統合 |

## 学習の順番 {#study-order}

1. [Shield](../../../../services/threat-detection.md#shield)と[Shield Advanced](../../../../services/threat-detection.md#shield-advanced): Standard との違いと、SRT とコスト保護が要件のときに選ぶことを確認します。
2. [WAF と似た機能の比較](../../../../services/certificates.md#waf-comparison): どの攻撃をどの機能で止めるかを整理します。
3. [ウェブ ACL](../../../../services/certificates.md#web-acl)と[ルールのアクション](../../../../services/certificates.md#waf-actions-details): 優先度の順の評価と、`Count` が評価を終わらせないことを押さえます。
4. [容量と本文の検査](../../../../services/certificates.md#waf-capacity-body): ALB と CloudFront の上限と、オーバーサイズの処理を覚えます。
5. [レートベースルール](../../../../services/certificates.md#rate-based-rules): 評価期間、集約キー、スコープダウンを確認します。
6. [スコープと関連付け](../../../../services/certificates.md#waf-scope)と[地理的制限](../../../../services/networking.md#geo-restriction): CloudFront 用のウェブ ACL の場所と、パス単位の制限の違いを押さえます。
7. [CloudFront と WAF](../../../../services/networking.md#cloudfront-waf)と [OAC](../../../../services/networking.md#oac): オリジンの直接攻撃を防ぐ方法を比べます。
8. [IoT Core](../../../../services/other-services.md#iot-core)と [S3 の CORS](../../../../services/s3.md#cors): IoT ポリシーの反映の遅れと、CORS が認可ではないことを確認します。
9. [Security Lake](../../../../services/threat-detection.md#security-lake)と [Firewall Manager](../../../../services/threat-detection.md#firewall-manager): OCSF のカスタムソースと、他社のルールやファイアウォールの展開を確認します。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| レートベースの評価期間 | 60、120、300、600 秒。既定 300 | 30 秒は選べない |
| レート制限の最小値 | 10 | アクションに `Allow` は使えない |
| 本文の検査（ALB、AppSync） | 8 KB で固定 | 超過分は `Match` やサイズ制約で扱う |
| 本文の検査（CloudFront など） | 既定 16 KB。16 KB 単位で 64 KB まで | 増やすと追加料金 |
| ヘッダーと Cookie の検査 | 先頭 8 KB、200 個まで | 単一のヘッダーの検査は対象外 |
| IoT ポリシーの反映 | 6〜8 分 | 取り消した後も数分は使えることがある |
| ASN を判定できない通信 | ASN 0 | スコープダウンで除外できる |
| CloudFront のウェブ ACL | `us-east-1` | ALB 用はリソースと同じリージョン |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| SRT の支援やコスト保護が必要 | Shield Advanced。Business か Enterprise のサポートプランも必要 |
| L3、L4 の DDoS だけで予算が小さい | Shield Standard と CloudFront の前置き |
| 漏えいした認証情報でのログイン試行 | ATP のマネージドルールグループ |
| 国単位で配信全体を止める | CloudFront の地理的制限 |
| 国とパスの組み合わせで止める | WAF の地理的一致と URI の一致 |
| CloudFront の背後の ALB で IP のレート制限が誤動作 | WAF を CloudFront に付ける。`X-Forwarded-For` の先頭は利用者が変更できる |
| IP を変えるツールを止める | WAF のログの JA3、JA4 を文字列一致や集約キーに使う |
| ALB を公開せず CloudFront を唯一の入り口にする | VPC オリジン |
| コードを変えずにセキュリティヘッダーを付ける | レスポンスヘッダーポリシー |
| 他社のログを Security Lake に入れる | OCSF の Parquet。1 オブジェクトに 1 つのイベントクラス |
| 他社の WAF ルールを組織に配る | Marketplace のルールグループと Firewall Manager。各アカウントの購読が必要 |

## 引っかかりやすい点 {#traps}

- `Count` は評価を終わらせません。`Allow` と `Block` は終わらせるので、先に `Allow` があると後の `Block` は効きません。
- 本文の検査で `Continue` を選ぶと、上限を超えた部分は検査されません。
- NLB と EC2 は Elastic IP の関連付けを通じて Shield Advanced で保護します。GWLB は保護できません。
- Shield Advanced の料金に Bot Control や CAPTCHA の費用は含まれません。
- JA3 と JA4 の検査は CloudFront と ALB に限られます。
- Security Hub CSPM の検出結果は ASFF で、OCSF ではありません。
- CORS はブラウザのための設定で、認可の仕組みではありません。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [edge-security 問1](../../exercises/edge-security.md#q1) | 3.1.1 | ある会社は、インターネット向け ALB で EC サイトを公開しています。最近、HTTP フラッドと… |
| [edge-security 問2](../../exercises/edge-security.md#q2) | 3.1.1 | 金融機関の公開サイトは CloudFront と Route 53 で配信しています。経営層は次を求… |
| [edge-security 問3](../../exercises/edge-security.md#q3) | 3.1.1 | 会員制サイトのログイン画面に、他社から漏えいしたユーザー名とパスワードの組を次々に試す攻撃が来ていま… |
| [edge-security 問4](../../exercises/edge-security.md#q4) | 3.1.1 | あるアプリは CloudFront の背後のインターネット向け ALB で動いています。監査で、AL… |
| [edge-security 問5](../../exercises/edge-security.md#q5) | 3.1.2 | 監査で、CloudFront から配信する複数のアプリの応答に Strict-Transport-S… |
| [edge-security 問6](../../exercises/edge-security.md#q6) | 3.1.2 | CloudFront の背後のインターネット向け ALB について、CloudFront を経由しな… |
| [edge-security 問7](../../exercises/edge-security.md#q7) | 3.1.2 | ウェブ ACL に次のルールがあります。社内の IP から送られた、SQL インジェクションの文字列… |
| [edge-security 問8](../../exercises/edge-security.md#q8) | 3.1.2 | ALB に関連付けたウェブ ACL で、JSON の本文を SQL インジェクションのルールで検査し… |
| [edge-security 問9](../../exercises/edge-security.md#q9) | 3.1.2 | ある工場の IoT デバイスは X.509 証明書で IoT Core に接続しています。ある証明書… |
| [edge-security 問10](../../exercises/edge-security.md#q10) | 3.1.2 | 開発者がセキュリティ担当に説明しました。「S3 バケットの CORS の AllowedOrigin… |
| [edge-security 問11](../../exercises/edge-security.md#q11) | 3.1.2 | Shield Advanced を契約済みの会社が、インターネット向け NLB の背後のゲームサーバ… |
| [edge-security 問12](../../exercises/edge-security.md#q12) | 3.1.3 | 動画配信サイトは 1 つの CloudFront ディストリビューションで動いています。ライセンスの… |
| [edge-security 問13](../../exercises/edge-security.md#q13) | 3.1.3 | ログイン API の総当たり対策として、同じ IP から POST /login が 1 分間に 2… |
| [edge-security 問14](../../exercises/edge-security.md#q14) | 3.1.3 | CloudFront の背後の ALB に、東京リージョンのウェブ ACL を関連付け、送信元 IP… |
| [edge-security 問15](../../exercises/edge-security.md#q15) | 3.1.3 | 攻撃ツールが IP アドレスを次々に変えながら、CloudFront の背後の API を呼んでいま… |
| [edge-security 問16](../../exercises/edge-security.md#q16) | 3.1.3 | ホスティング事業者の複数の ASN から攻撃が来ているので、ASN を集約キーにしたレートベースルー… |
| [edge-security 問17](../../exercises/edge-security.md#q17) | 3.1.4 | 他社の CDN のログを Security Lake のカスタムソースとして取り込みました。変換用の… |
| [edge-security 問18](../../exercises/edge-security.md#q18) | 3.1.4 | セキュリティチームは、他社の販売者が保守する WAF のマネージドルールグループを AWS Mark… |
| [edge-security 問19](../../exercises/edge-security.md#q19) | 3.1.4 | SOC は、複数の製品のデータを OCSF で SIEM に取り込む計画です。独自の変換処理はできる… |
| [edge-security 問20](../../exercises/edge-security.md#q20) | 3.1.4 | ある会社はオンプレミスで Palo Alto の次世代ファイアウォールのルール体系を使っています。A… |

<!-- questions:end -->

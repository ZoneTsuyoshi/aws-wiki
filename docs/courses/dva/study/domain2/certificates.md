# 分野2: 証明書と WAF

ACM と Private CA の選び方、証明書を置くリージョン、開発用の証明書と SSH キーの作り方を問います。WAF は問題集ではアクセス制御（2.1.2）の問題として出てきます。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [2.1.2](../../domain2.md#skill-2-1-2) | WAF によるリクエストの制御 |
| [2.2.1](../../domain2.md#skill-2-2-1) | 転送時の TLS と終端の場所 |
| [2.2.2](../../domain2.md#skill-2-2-2) | ACM と Private CA |
| [2.2.5](../../domain2.md#skill-2-2-5) | 開発用の証明書と SSH キー |

## 学習の順番 {#study-order}

1. [AWS Certificate Manager](../../../../services/certificates.md#acm): 公開証明書とプライベート証明書の違いを確認します。
2. [ドメイン検証](../../../../services/certificates.md#domain-validation)と[自動更新](../../../../services/certificates.md#auto-renewal): DNS 検証を選ぶ理由と、更新の対象外を覚えます。
3. [リージョンのルール](../../../../services/certificates.md#region-rules): サービスごとの置き場所を表で覚えます。
4. [証明書のインポート](../../../../services/certificates.md#import)と[更新の監視](../../../../services/certificates.md#renewal-monitoring): 自動更新されない証明書の管理を学びます。
5. [AWS Private CA](../../../../services/certificates.md#private-ca): 発行の方法で管理のしかたが変わることを押さえます。
6. [開発用の証明書と SSH キー](../../../../services/certificates.md#dev-certs-ssh): `openssl` と `ssh-keygen` の使いどころを確認します。
7. [転送時の TLS](../../../../services/certificates.md#tls-in-transit)と [mTLS](../../../../services/certificates.md#mtls): 区間ごとの証明書と、クライアント認証の手順を見ます。
8. [AWS WAF](../../../../services/certificates.md#waf)と[レートベースルール](../../../../services/certificates.md#rate-based-rules): 付けられる場所、アクション、制限の設定を確認します。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| ACM 公開証明書の有効期間 | 198 日 | 期限の 45 日前から更新を確認 |
| CloudFront、エッジ最適化 API の証明書 | `us-east-1` | ALB とリージョナル API は同じリージョン |
| 1 枚のドメイン名 | 既定 10 個 | 申請すると増やせる |
| インポートの秘密鍵 | PEM、暗号化なし、5 KB まで | パスフレーズは先に解除する |
| Private CA の短期証明書 | 最大 7 日 | 失効の仕組みを省略できる場合がある |
| WAF の本文の検査 | ALB は 8 KB。CloudFront などは既定 16 KB、最大 64 KB | 超えた部分は検査しない |
| レートベースルール | ウィンドウ 60〜600 秒、既定 300 秒。制限は最小 10 | ウィンドウは振り返る長さ |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 東京のアプリの前に置く CloudFront に証明書を付ける | `us-east-1` の ACM に作る |
| 証明書の更新を自動化する | DNS 検証。CNAME を残す |
| インポートした証明書の期限を管理する | 再インポートで更新し、EventBridge や `DaysToExpiry` で通知する |
| 社内サービス向けの証明書を発行する | AWS Private CA |
| Private CA の証明書を自動更新する | ACM で要求する。`IssueCertificate` で発行したものは対象外 |
| クライアントも証明書で認証する API | API Gateway の mutual TLS。既定の `execute-api` エンドポイントは無効にする |
| ローカルの HTTPS 用の証明書を手元で作る | `openssl req -x509` の自己署名証明書 |
| 秘密鍵を AWS に通さず SSH キーを登録する | `ssh-keygen` で作り、`aws ec2 import-key-pair` |
| ログイン API を IP ごとに制限する | レートベースルールと `ScopeDownStatement` で `/login` に絞る |
| 新しい WAF ルールを影響なく試す | まず Count で動かし、確認してから Block にする |

## 引っかかりやすい点 {#traps}

- `*.example.com` は `example.com` 自体と `a.www.example.com` を保護しません。必要な名前を追加します。
- DNS 検証の CNAME を削除すると自動更新が止まります。メール検証の証明書は DNS 検証に切り替えられず、作り直します。
- EC2 キーペアの秘密鍵をなくすと取り戻せません。新しい公開鍵を追加するか Session Manager で入ります。Windows は RSA のみです。
- CloudFront の背後の ALB に WAF を置くと、送信元 IP が CloudFront になります。CloudFront に付けるか、`X-Forwarded-For` などを集約キーにします。
- CAPTCHA と Challenge はブラウザからの HTTPS でしか動きません。API クライアントのルールに付けると正常なリクエストが拒否されます。
- WAF は NLB、HTTP API、EC2 に直接付けられません。ログの送信先は名前が `aws-waf-logs-` で始まる必要があります。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [certificates 問1](../../exercises/certificates.md#q1) | 2.2.2 | 東京リージョンの ALB と、CloudFront の両方に同じドメインで ACM の公開証明書を使… |
| [certificates 問2](../../exercises/certificates.md#q2) | 2.2.2 | DNS 検証の ACM の公開証明書を ALB に付けています。証明書が自動更新されなくなる操作はど… |
| [certificates 問3](../../exercises/certificates.md#q3) | 2.2.2 | ACM の公開証明書の有効期間と更新について、現在の仕様として正しいものを選んでください。（2つ選択… |
| [certificates 問4](../../exercises/certificates.md#q4) | 2.2.2 | 他社の CA の証明書を ACM にインポートします。秘密鍵はパスフレーズで保護され、DER 形式で… |
| [certificates 問5](../../exercises/certificates.md#q5) | 2.2.2 | インポートした証明書の期限切れを 45 日前から毎日通知したいと考えています。最も運用負荷が低い方法… |
| [certificates 問6](../../exercises/certificates.md#q6) | 2.2.2 | コンテナ間の通信に、7 日で切れる証明書を大量に発行し、失効の仕組みは持ちたくありません。AWS P… |
| [certificates 問7](../../exercises/certificates.md#q7) | 2.1.2 | ウェブ ACL の関連付けの説明として正しいものを選んでください。（2つ選択） |
| [certificates 問8](../../exercises/certificates.md#q8) | 2.1.2 | ALB の WAF で本文の SQL インジェクションを検査しています。攻撃文字列を本文の 10 K… |
| [certificates 問9](../../exercises/certificates.md#q9) | 2.1.2 | REST クライアント（ブラウザではない）からも呼ばれる API に、WAF の CAPTCHA ア… |
| [certificates 問10](../../exercises/certificates.md#q10) | 2.1.2 | ログイン API に、IP ごとに 1 分間 100 回の制限を付けます。レートベースルールの設定と… |
| [certificates 問11](../../exercises/certificates.md#q11) | 2.1.2 | CloudFront の背後の ALB に WAF を付けました。レートベースルールが、全利用者をま… |
| [certificates 問12](../../exercises/certificates.md#q12) | 2.1.2 | WAF のログを S3 に送ろうとしましたが、バケットが送信先の選択肢に出ません。バケットは app… |
| [certificates 問13](../../exercises/certificates.md#q13) | 2.2.5 | ローカルの開発サーバーで HTTPS を試すために、localhost 用の秘密鍵と自己署名証明書を… |
| [certificates 問14](../../exercises/certificates.md#q14) | 2.2.5 | 開発者は EC2 への SSH に使うキーを用意します。セキュリティの方針で、秘密鍵は手元で生成し、… |
| [certificates 問15](../../exercises/certificates.md#q15) | 2.2.5 | EC2 キーペアについて、正しい説明はどれですか。（2つ選択） |

<!-- questions:end -->

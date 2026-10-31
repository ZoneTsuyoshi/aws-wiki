# 分野6: 脅威の検出と通知

検出のサービスの区別と、組織への展開、通知の調整を問います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [自動適用](../../domain6.md#t6-2-automation) | 複数アカウントへのコントロールの自動適用 |
| [検出のサービス](../../domain6.md#t6-3-vulnerability-services) | 脆弱性とイベントを見つけるサービス |
| [脅威](../../domain6.md#t6-3-threats) | よくある脅威 |
| [通知](../../domain6.md#t6-3-alerting) | 異常なイベントの通知 |
| [分析](../../domain6.md#t6-3-analysis) | ログ、メトリクス、検出結果の分析 |

## 学習の順番 {#study-order}

1. [組織と集約](../../../../services/threat-detection.md#security-hub-org): 中央設定を確認します。
2. [Firewall Manager](../../../../services/threat-detection.md#firewall-manager): 組織への配布を確認します。
3. [データソース](../../../../services/threat-detection.md#guardduty-data-sources): 独立して分析することを押さえます。
4. [抑制ルールとリスト](../../../../services/threat-detection.md#guardduty-suppression): 通知の調整を確認します。
5. [認証情報の漏えい](../../../../services/threat-detection.md#ir-credentials): キーが漏れたときの順序を覚えます。
6. [Detective](../../../../services/threat-detection.md#detective): 調査の手段を確認します。

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 全アカウントの WAF を揃える | Firewall Manager |
| 外部へ共有されたリソース | IAM Access Analyzer |
| 重要度で通知を分ける | EventBridge のルール |
| 想定内の検出結果を除く | 抑制ルール |
| ログを正規化して SIEM へ | Security Lake |

## 引っかかりやすい点 {#traps}

- GuardDuty のためにログを自分で有効にする必要はありません。
- アクセスキーが漏れたら、まず無効化します。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [threat-detection 問4](../../exercises/threat-detection.md#q4) | 自動適用 | 全アカウント、全リージョンの Security Hub CSPM の標準を統一します。例外の OU … |
| [threat-detection 問5](../../exercises/threat-detection.md#q5) | 自動適用 | 組織の全アカウントの ALB に同じ WAF のルールを適用します。新しい ALB にも自動で適用し… |
| [threat-detection 問6](../../exercises/threat-detection.md#q6) | 自動適用 | Security Hub CSPM の検出結果のうち、開発用アカウントの一部は重要度を下げて通知しま… |
| [threat-detection 問7](../../exercises/threat-detection.md#q7) | 検出のサービス | 担当者が GuardDuty を使い始めるために、VPC フローログと CloudTrail の証跡… |
| [threat-detection 問8](../../exercises/threat-detection.md#q8) | 検出のサービス | 次の検出の対象とサービスの組み合わせとして、適切なものはどれですか。(1) 組織の外へ共有された S… |
| [threat-detection 問9](../../exercises/threat-detection.md#q9) | 検出のサービス | EC2 の暗号通貨のマイニングや、不審な IP からの認証情報の利用を検出します。S3 の不審なデー… |
| [threat-detection 問10](../../exercises/threat-detection.md#q10) | 脅威 | 開発者の誤りで、公開リポジトリに本番の IAM ユーザーのアクセスキーが 3 時間前から載っていまし… |
| [threat-detection 問11](../../exercises/threat-detection.md#q11) | 脅威 | 組織の全 S3 バケットの公開を防ぎ、基準を変更できないようにします。公開済みのものも検出します。適… |
| [threat-detection 問12](../../exercises/threat-detection.md#q12) | 脅威 | 複数のアカウントの公開の Web アプリに HTTP のアクセスが残っています。監査では、安全でない… |
| [threat-detection 問13](../../exercises/threat-detection.md#q13) | 通知 | GuardDuty の結果を通知します。重要度の高いものは当番へ、それ以外は Slack へ送ります… |
| [threat-detection 問14](../../exercises/threat-detection.md#q14) | 通知 | ルートユーザーは緊急時しか使わない方針です。ログインがあれば、数分以内にセキュリティ担当へ通知します… |
| [threat-detection 問15](../../exercises/threat-detection.md#q15) | 通知 | 次の検知を設定します。(1) RunInstances の呼び出しの量が平常から急に増えた。(2) … |
| [threat-detection 問16](../../exercises/threat-detection.md#q16) | 分析 | インシデントの調査です。(1) 特定の EC2 への拒否された通信の送信元の一覧。(2) 漏れたキー… |
| [threat-detection 問17](../../exercises/threat-detection.md#q17) | 分析 | GuardDuty の検出結果の影響範囲を、関連する IP とロールのつながりから調べます。別に、複… |
| [threat-detection 問18](../../exercises/threat-detection.md#q18) | 分析 | GuardDuty、Inspector、Config から毎週数百件の検出結果があり、3 人の担当者… |

<!-- questions:end -->

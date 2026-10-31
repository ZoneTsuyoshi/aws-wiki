# 分野2: 検出結果の検証と封じ込め

検出結果をうのみにせず範囲を確かめ、証拠を残しながら被害を止め、作り直して復旧するまでを問います。セキュリティグループで接続が切れないこと、認証情報の種類で止め方が違うことが要点です。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [2.2.3](../../domain2.md#skill-2-2-3) | 検出結果の検証と影響範囲の評価 |
| [2.2.4](../../domain2.md#skill-2-2-4) | 封じ込め、根絶、復旧 |

## 学習の順番 {#study-order}

1. [検出結果](../../../../services/threat-detection.md#guardduty-findings): 重要度の意味と、主な検出結果の最初の対応を覚えます。
2. [抑制ルールとリスト](../../../../services/threat-detection.md#guardduty-suppression)と [Extended Threat Detection](../../../../services/threat-detection.md#guardduty-extended): 抑制の効果と、広すぎる抑制の害を確認します。
3. [Security Hub の機能](../../../../services/threat-detection.md#security-hub-unified): 露出の検出結果で優先度を決める方法を確認します。
4. [インシデント対応](../../../../services/threat-detection.md#incident-response): 封じ込めの 3 種類を押さえます。
5. [EC2 の隔離](../../../../services/threat-detection.md#ir-ec2-isolation)と[セキュリティグループとネットワーク ACL](../../../../services/networking.md#security-groups-nacls): 追跡中の接続と NACL の関係を理解します。
6. [認証情報の漏えい](../../../../services/threat-detection.md#ir-credentials): `AKIA` と `ASIA` の止め方を分けます。
7. [SCP](../../../../services/governance.md#scp): 組織の側から止める方法と、管理アカウントに効かないことを確認します。
8. [ランサムウェアと誤削除の防止](../../../../services/resilience.md#immutable-compare)と[論理的にエアギャップされたボールト](../../../../services/resilience.md#logically-air-gapped): 攻撃者に消されない復旧の経路を確認します。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| Critical | 9.0〜10.0 | 攻撃シーケンス |
| High | 7.0〜8.9 | 侵害され不正利用中 |
| Medium | 4.0〜6.9 | 通常からの逸脱。説明できなければ侵害と扱う |
| Low | 1.0〜3.9 | 試みのみ |
| 抑制された検出結果の保持 | アーカイブの状態で 90 日 | Security Hub CSPM、S3、Detective、EventBridge には送られない |
| セッションの取り消しの範囲 | 実行時点から約 30 秒先まで | それより後に引き受けたセッションは影響なし |
| Vault Lock の猶予期間 | 3 日以上 | コンプライアンスモードは期間の後は誰も解除できない |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 正当と確認できた活動の検出結果を減らす | 型と送信元 IP などに絞った抑制ルール |
| 検出結果が止まったが活動は続いている | 想定内と学習された可能性。CloudTrail で確認 |
| 実際に何をされ、何ができたかを調べる | CloudTrail と、権限、Access Advisor |
| 重なったリスクの優先度を決める | Security Hub の露出の検出結果 |
| SG を置き換えても接続が切れない | NACL で拒否 |
| Auto Scaling のインスタンスの証拠を残す | スタンバイかデタッチ。ELB から外す |
| `AKIA` のキーが漏えいした | 無効化し、攻撃者の作ったユーザーやキーも削除 |
| `ASIA` のキーが漏えいした | ロールのセッションの取り消し |
| 権限セットのセッションが不正に使われた | IAM Identity Center で取り消し |
| アカウント全体の操作をすぐ止める | SCP での拒否か Suspended OU |
| 本番のアカウントごと信頼できない | 別のアカウントへ共有したエアギャップのボールトから復元 |
| インスタンスから不正なものを除けたと言えない | 検証済みの AMI から作り直す |

## 引っかかりやすい点 {#traps}

- セキュリティグループのルールを変えても、追跡中の接続はタイムアウトするまで切れません。
- 全開放のルール同士の通信は追跡されず、ルールを変えるとすぐに切れます。隔離用の SG には全開放を置きません。
- 抑制された検出結果は Extended Threat Detection の関連付けに使われません。条件を広くしないようにします。
- 抑制ルールは GuardDuty が繰り返し誤検知と確認してから作るよう勧めています。
- 同じリモートホストの活動は想定内と学習され、`InstanceCredentialExfiltration.OutsideAWS` が止まることがあります。
- セッションの取り消しはロールを使う全員に効きます。正当な利用者も認証情報を取り直します。
- サービスリンクロールのセッションは取り消せません。権限セットのロールは IAM で編集できません。
- 終了保護と停止保護は、Auto Scaling による終了を防ぎません。
- SCP は管理アカウントに効きません。メンバーアカウントのルートユーザーには効きます。
- 読み取られたシークレットは漏えいしたものとして扱い、ローテーションします。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [containment 問1](../../exercises/containment.md#q1) | 2.2.3 | VPC のインターネット向けの通信を、VPN 経由でオンプレミスのゲートウェイから出す構成にしました… |
| [containment 問2](../../exercises/containment.md#q2) | 2.2.3 | EKS クラスターの定期ジョブが、GuardDuty の検出結果を毎日数件出しています。担当者は、E… |
| [containment 問3](../../exercises/containment.md#q3) | 2.2.3 | GuardDuty が、ある IAM ユーザーのキーについて Medium の検出結果を出しました。… |
| [containment 問4](../../exercises/containment.md#q4) | 2.2.3 | ある EC2 のロールの認証情報について、外部の IP からの利用を示す InstanceCrede… |
| [containment 問5](../../exercises/containment.md#q5) | 2.2.3 | 漏えいが確認されたロールについて、影響の範囲を評価します。このロールで実際に何をされたか、さらにこの… |
| [containment 問6](../../exercises/containment.md#q6) | 2.2.3 | Security Hub に複数の検出結果があります。同じ EC2 に、既知の脆弱性、パブリックから… |
| [containment 問7](../../exercises/containment.md#q7) | 2.2.4 | 攻撃者のリバースシェルが接続中の EC2 で、隔離用のセキュリティグループに置き換えましたが、接続が… |
| [containment 問8](../../exercises/containment.md#q8) | 2.2.4 | Auto Scaling グループのインスタンスが侵害されました。担当者は終了保護を有効にして隔離用… |
| [containment 問9](../../exercises/containment.md#q9) | 2.2.4 | IAM ユーザーの AKIA のキーが漏えいしました。CloudTrail には、そのキーで Cre… |
| [containment 問10](../../exercises/containment.md#q10) | 2.2.4 | 複数の担当者とアプリが同じ IAM ロールを使っています。そのロールの ASIA の一時キーが外部で… |
| [containment 問11](../../exercises/containment.md#q11) | 2.2.4 | IAM Identity Center の権限セットから作られたロールのセッションが不正に使われた疑… |
| [containment 問12](../../exercises/containment.md#q12) | 2.2.4 | メンバーアカウントで管理者権限が奪われ、攻撃者がリソースを次々に作っています。調査のため、ログと既存… |
| [containment 問13](../../exercises/containment.md#q13) | 2.2.4 | ランサムウェアの攻撃者が本番アカウントの管理者権限を得て、通常のバックアップボールトの復旧ポイントを… |
| [containment 問14](../../exercises/containment.md#q14) | 2.2.4 | Web サーバーが、既知の脆弱性を突かれて侵害されました。調査と証拠の取得は終わりました。ロールには… |

<!-- questions:end -->

# 分野2: コンプライアンス

規制の要件を、暗号化、アクセス制御、監査ログ、データの場所に分けて設計する力を問います。AWS の準拠と自社の準拠の区別も論点です。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [2.4.1](../../domain2.md#skill-2-4-1) | データ保護の要件 |
| [2.4.2](../../domain2.md#skill-2-4-2) | 規制要件とデータ主権 |
| [2.4.3](../../domain2.md#skill-2-4-3) | 規制対象のワークロードの監査証跡 |
| [2.4.4](../../domain2.md#skill-2-4-4) | データレジデンシーの制御 |
| [2.4.5](../../domain2.md#skill-2-4-5) | コンプライアンスの証拠の収集と報告 |
| [2.4.6](../../domain2.md#skill-2-4-6) | リスク評価と脅威モデリング |

## 学習の順番 {#study-order}

1. [バケットのデフォルト暗号化とポリシーによる強制](../../../../services/s3.md#enforcing-encryption)と [Object Lock](../../../../services/s3.md#object-lock): 暗号化の強制と、2 つのモードの違いを確認します。
2. [Macie](../../../../services/threat-detection.md#macie)と[データ保護ポリシー](../../../../services/observability.md#logs-data-protection): 機密データの発見とマスクを区別します。
3. [責任共有モデル](../../../../services/cloud-foundations.md#shared-responsibility)、[Outposts](../../../../services/cloud-foundations.md#outposts)、[鍵素材のインポート](../../../../services/kms.md#imported-key-material): データ主権の選択肢を整理します。
4. [イベントの種類](../../../../services/observability.md#cloudtrail-events)と[証跡とイベント履歴](../../../../services/observability.md#cloudtrail-trails): データイベントと、ログの検証を押さえます。
5. [CloudTrail Lake](../../../../services/observability.md#cloudtrail-lake)と[モデル呼び出しログ](../../../../services/ai.md#invocation-logging): 長期の検索の選択肢と、AI のログの扱いを確認します。
6. [SCP](../../../../services/governance.md#scp)、[コントロール](../../../../services/governance.md#ct-controls)、[モデル ID と推論プロファイル](../../../../services/ai.md#model-identifiers): リージョンの制限と、クロスリージョン推論の関係を理解します。
7. [AWS Artifact](../../../../services/threat-detection.md#artifact)、[Config と CloudTrail の違い](../../../../services/governance.md#config-vs-cloudtrail)、[Audit Manager](../../../../services/threat-detection.md#audit-manager): 証拠の取得先を分けます。
8. [Well-Architected Framework](../../../../services/cloud-foundations.md#well-architected): 脅威モデリングの考え方と STRIDE を確認します。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| ログファイルの検証 | SHA-256 のハッシュと SHA-256 with RSA の署名 | 変更と削除を検出する |
| CloudTrail Lake | 2026 年 5 月 31 日で新規受付を終了 | 新規は S3 と Athena、または CloudWatch |
| Audit Manager | 2026 年 4 月 30 日で新規受付を終了 | 新規は Config と CSPM |
| `AWS-GR_REGION_DENY` | ランディングゾーン全体 | OU ごとに設定できない |
| `CT.MULTISERVICE.PV.1` | 指定した OU | 一部の OU だけを制限 |
| STRIDE | 6 分類 | なりすまし、改ざん、否認、情報漏えい、サービス拒否、権限昇格 |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 特定のバケットのオブジェクトを誰が読んだかを記録する | 高度なイベントセレクターでデータイベントを絞る |
| S3 のどこに個人情報があるかを探す | Macie |
| ログの中の機密情報を隠す | CloudWatch Logs のデータ保護ポリシー |
| ルートユーザーも削除できない WORM | Object Lock のコンプライアンスモード |
| 国にリージョンがなく、データをローカルに置く | Outposts |
| 鍵を AWS の外に置いて使う | KMS の外部キーストア |
| 改ざんの検出と削除の防止 | ログファイルの検証と Object Lock |
| 長期ログの検索を安く | S3 と Athena |
| AI の処理リージョンの証跡 | CloudTrail の `additionalEventData.inferenceRegion` |
| 本文を残さず AI の呼び出しを記録する | `textDataDeliveryEnabled` を `false` に |
| 一部の OU だけリージョンを制限する | `CT.MULTISERVICE.PV.1` |
| EU の中で Bedrock の容量を増やす | EU の地理的プロファイル。SCP で送信先を許可する |
| AWS 自身の準拠の証拠 | AWS Artifact |
| 自社の設定の準拠の証拠 | Config と Security Hub CSPM |
| 組織全体で BAA を結ぶ | 管理アカウントの Artifact で組織の契約を受諾 |

## 引っかかりやすい点 {#traps}

- データイベントは既定で記録されません。後から有効にしても、過去の分は残りません。
- データ保護ポリシーは取り込み時に働きます。設定前に取り込んだログはマスクされません。
- Guardrails のマスクはモデル呼び出しログに効きません。入力は元のまま残ります。
- リージョンを制限する SCP では、グローバルサービスを `NotAction` で除外します。
- グローバルの推論プロファイルは世界の商用リージョンへ送られます。レジデンシーの要件には地理的プロファイルです。
- Artifact の報告書があっても、自社のワークロードが準拠するわけではありません。
- CloudFront の地理的制限は配信先の制限で、データの保管場所を決めません。
- フォレンジックや詳細な脅威の調査は、この試験の範囲外です。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [compliance 問1](../../exercises/compliance.md#q1) | 2.4.1 | ある製薬会社は、臨床試験のデータを置く 1 つの S3 バケットについて、誰がいつオブジェクトを読ん… |
| [compliance 問2](../../exercises/compliance.md#q2) | 2.4.1 | あるカード会社は規制への対応で、次の 2 つを実現します。S3 の大量のバケットのどこに個人情報があ… |
| [compliance 問3](../../exercises/compliance.md#q3) | 2.4.1 | ある金融機関の S3 バケットは、次の要件を満たす必要があります。HTTP でのアクセスを拒否します… |
| [compliance 問4](../../exercises/compliance.md#q4) | 2.4.1 | ある証券会社は、取引の記録を 7 年間、WORM で保存する規制を受けます。規制では、ルートユーザー… |
| [compliance 問5](../../exercises/compliance.md#q5) | 2.4.2 | ある国の公的機関は、住民のデータを自国の外に置けません。その国に AWS リージョンはなく、自社のデ… |
| [compliance 問6](../../exercises/compliance.md#q6) | 2.4.2 | ある規制業種の会社は、AWS のサービスの暗号化を使いたいものの、規制で「鍵は AWS の外の自社の… |
| [compliance 問7](../../exercises/compliance.md#q7) | 2.4.2 | ある会社の情報システム部は「AWS は PCI DSS に準拠しているので、AWS 上の決済システム… |
| [compliance 問8](../../exercises/compliance.md#q8) | 2.4.3 | ある証券会社は CloudTrail の組織の証跡を Log Archive アカウントの S3 に… |
| [compliance 問9](../../exercises/compliance.md#q9) | 2.4.3 | ある保険会社は、新たに監査ログを 10 年間保管します。検索は年に数回の監査のときだけです。Clou… |
| [compliance 問10](../../exercises/compliance.md#q10) | 2.4.3 | ある銀行は Bedrock の EU の地理的な推論プロファイルを使っています。監査人から、各リクエ… |
| [compliance 問11](../../exercises/compliance.md#q11) | 2.4.3 | ある医療機関では Bedrock でチャットを提供しています。利用状況の監査のため、モデル呼び出しの… |
| [compliance 問12](../../exercises/compliance.md#q12) | 2.4.4 | ある組織は aws:RequestedRegion が EU のリージョン以外の操作を拒否する SC… |
| [compliance 問13](../../exercises/compliance.md#q13) | 2.4.4 | ある多国籍企業は Control Tower のランディングゾーンを運用しています。EU の子会社の… |
| [compliance 問14](../../exercises/compliance.md#q14) | 2.4.4 | ある EU の企業は、データの処理を EU の中に限る社内規定を持ち、SCP でも EU のリージョ… |
| [compliance 問15](../../exercises/compliance.md#q15) | 2.4.4 | ある組織は、データを東京リージョンの外に出さないという要件のレビューをしています。SCP でリージョ… |
| [compliance 問16](../../exercises/compliance.md#q16) | 2.4.5 | ある SaaS 企業は、顧客の監査人から 2 種類の証拠を求められました。AWS のデータセンターの… |
| [compliance 問17](../../exercises/compliance.md#q17) | 2.4.5 | ある医療系の企業グループは 50 のアカウントで保護対象の医療情報を扱う予定です。HIPAA の B… |
| [compliance 問18](../../exercises/compliance.md#q18) | 2.4.5 | ある会社は四半期ごとの内部監査の証拠の収集を自動化します。これまで AWS Audit Manage… |
| [compliance 問19](../../exercises/compliance.md#q19) | 2.4.6 | ある決済サービスの脅威モデリングで、「運用担当者が返金の操作をしたのに、後から自分はしていないと主張… |
| [compliance 問20](../../exercises/compliance.md#q20) | 2.4.6 | ある会社は新しい決済システムの設計を始めます。セキュリティの費用を抑えるため、脅威モデリングのやり方… |
| [compliance 問21](../../exercises/compliance.md#q21) | 2.4.6 | あるサーバーレスのシステムの脅威モデリングで、次の脅威が挙がりました。「開発者が新しいロールを作り、… |

<!-- questions:end -->

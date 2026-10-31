# 分野5: IaC

何百ものアカウントへ、壊さずに展開する方法を問います。ツールの文法より、どの段階で何を止めるかが中心です。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [5.1.1](../../domain5.md#skill-5-1-1) | 宣言型と命令型の IaC、安全な更新 |
| [5.1.2](../../domain5.md#skill-5-1-2) | ポリシーアズコード |
| [5.1.3](../../domain5.md#skill-5-1-3) | IaC のシークレット管理 |
| [5.1.4](../../domain5.md#skill-5-1-4) | マルチアカウント、マルチリージョンのデプロイ |

## 学習の順番 {#study-order}

1. [どれを使うか](../../../../services/iac.md#choosing)と [CDK](../../../../services/iac.md#cdk): CDK のデプロイの実体が CloudFormation であることを確認します。
2. [変更セット](../../../../services/iac.md#change-sets)、[DeletionPolicy](../../../../services/iac.md#deletion-policy)、[UpdateReplacePolicy](../../../../services/iac.md#update-replace-policy): 置き換えと削除で働く属性の違いを覚えます。
3. [スタックポリシー](../../../../services/iac.md#stack-policy)と[ロールバックトリガー](../../../../services/iac.md#rollback-triggers): 更新の保護と、完了後の監視を押さえます。
4. [コントロール](../../../../services/governance.md#ct-controls)、[SCP](../../../../services/governance.md#scp)、[Config の修復](../../../../services/governance.md#config-remediation): 開発時、デプロイ前、API の時点、デプロイ後の防御を並べます。
5. [ドリフト検出](../../../../services/iac.md#drift)と[ドリフトの運用](../../../../services/operations.md#drift-operations): 明示したプロパティだけが対象という制限と、修復の方法を確認します。
6. [3 つのサービスの比較](../../../../services/secrets.md#comparison)と[動的参照](../../../../services/secrets.md#dynamic-references): 使えない場所と、値が更新されない条件を覚えます。
7. [StackSets の設定](../../../../services/iac.md#stacksets-settings)と [StackSets の運用](../../../../services/operations.md#stacksets-operations): 権限のモデル、自動デプロイ、同時実行のモードを判断できるようにします。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| ロールバックトリガー | 最大 5 個、監視時間は 0〜180 分（既定 0） | `INSUFFICIENT_DATA` では戻らない |
| Strict の実際の同時実行数 | `Maximum concurrent accounts` と `Failure tolerance` + 1 の小さい方 | 例: 20 と 4 なら 5 で始まる |
| `Failure tolerance` | リージョンごとに判定 | 超えると残りのリージョンを取り消す |
| Hook の失敗モード | `WARN`、`FAIL` | `WARN` で影響を調べてから `FAIL` |
| 動的参照 | テンプレートあたり 60 個 | `UserData` と `CloudFormation::Init` では使えない |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| ループや条件が多く、部品を社内へ配りたい | CDK のコンストラクト |
| 更新の前に置き換えの有無を見たい | 変更セット |
| 置き換えでも削除でもデータを残す | `UpdateReplacePolicy` と `DeletionPolicy` の両方 |
| 特定のリソースの更新だけ止める | スタックポリシー |
| 完了後のアラームで戻す | ロールバックトリガーと監視時間 |
| CloudFormation のデプロイ前に、コードなしで止める | Control Tower のプロアクティブコントロール |
| 経路を問わず API の時点で止める | SCP |
| 既存のリソースを検出して直す | Config ルールと修復 |
| 自動ローテーションと他リージョンへの複製 | Secrets Manager |
| 新しいアカウントへ自動で配る | サービスマネージド権限と自動デプロイ |
| 1 アカウントずつ確かめて止める | 順次のリージョン、`Failure tolerance` 0、同時実行 1 |

## 引っかかりやすい点 {#traps}

- `DeletionPolicy` は置き換えのときには働きません。`UpdateReplacePolicy` が別に必要です。
- `NoEcho` は表示を隠すだけで、テンプレートの平文を防ぎません。
- CDK Aspects は `Stage` の境界を越えません。`Stage` か配下に適用します。
- シークレットの値を更新しても、CloudFormation は再取得しません。そのリソースを変更する更新が必要です。
- ドリフト検出は検出だけです。既定値のままのプロパティの変更も見つけません。
- 自動デプロイはアカウントのフィルターを考慮しません。上書きしたパラメータも、後から加わるアカウントには適用されません。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [iac 問1](../../exercises/iac.md#q1) | 5.1.1 | ある小売企業のプラットフォームチームは、約 40 のマイクロサービスに同じ形の基盤を提供しています。… |
| [iac 問2](../../exercises/iac.md#q2) | 5.1.1 | 金融機関の本番スタックに RDS の DB インスタンスがあります。開発者がテンプレートでプロパティ… |
| [iac 問3](../../exercises/iac.md#q3) | 5.1.1 | 本番スタックの DynamoDB テーブルを、通常のパイプラインの更新で置き換えや削除できないように… |
| [iac 問4](../../exercises/iac.md#q4) | 5.1.1 | SaaS 企業は CloudFormation で API の基盤を更新しています。更新そのものは成… |
| [iac 問5](../../exercises/iac.md#q5) | 5.1.2 | あるチームは CDK で、S3 バケットのバージョニングを確認する Aspect を作りました。違反… |
| [iac 問6](../../exercises/iac.md#q6) | 5.1.2 | セキュリティチームは、暗号化されていない RDS の DB インスタンスが CloudFormati… |
| [iac 問7](../../exercises/iac.md#q7) | 5.1.2 | ある企業では、チームごとに CloudFormation、CDK、Terraform、マネジメントコ… |
| [iac 問8](../../exercises/iac.md#q8) | 5.1.2 | Control Tower で管理している組織で、本番の OU にあるすべてのアカウントに統一のルー… |
| [iac 問9](../../exercises/iac.md#q9) | 5.1.2 | 運用チームは、多数のアカウントのスタックで手作業の変更が放置されていることに悩んでいます。ドリフトを… |
| [iac 問10](../../exercises/iac.md#q10) | 5.1.3 | あるチームのテンプレートでは、DB のパスワードを NoEcho のパラメータで受け取り、既定値に値… |
| [iac 問11](../../exercises/iac.md#q11) | 5.1.3 | CloudFormation の AWS::RDS::DBInstance の MasterUser… |
| [iac 問12](../../exercises/iac.md#q12) | 5.1.3 | ある企業には、数千の非機密の設定値と、少数の DB 認証情報があります。DB 認証情報は定期的にロー… |
| [iac 問13](../../exercises/iac.md#q13) | 5.1.4 | ある組織には 300 のアカウントがあり、毎月新しいアカウントが増えます。全アカウントの 2 つのリ… |
| [iac 問14](../../exercises/iac.md#q14) | 5.1.4 | StackSets で 1 つのリージョンの多数のアカウントを更新します。同時実行モードは既定の S… |
| [iac 問15](../../exercises/iac.md#q15) | 5.1.4 | サービスマネージド権限の StackSets で OU に自動デプロイしています。ある事業の売却に伴… |
| [iac 問16](../../exercises/iac.md#q16) | 5.1.4 | グローバル企業は、StackSets で 5 つのリージョンのセキュリティ設定を更新します。テンプレ… |

<!-- questions:end -->

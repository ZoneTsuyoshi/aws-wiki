# 分野2: データベースのスケーリングと復元

容量の増やし方と、復元先の違いを問います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [2.1.3](../../domain2.md#skill-2-1-3) | マネージドデータベースのスケーリング |
| [2.2.2](../../domain2.md#skill-2-2-2) | 耐障害性のある構成 |
| [2.3.2](../../domain2.md#skill-2-3-2) | データベースの復元方法 |

## 学習の順番 {#study-order}

1. [リードレプリカと Multi-AZ](../../../../services/databases.md#read-replicas)と[Aurora](../../../../services/databases.md#aurora): 読み取りの増やし方を確認します。
2. [Aurora Serverless v2](../../../../services/databases.md#aurora-serverless-v2): ライターの負荷への選択肢を確認します。
3. [キャパシティモードと RCU/WCU](../../../../services/dynamodb.md#capacity)と[プロビジョンドと Auto Scaling](../../../../services/dynamodb.md#provisioned-auto-scaling): モードと Auto Scaling の設定を確認します。
4. [RTO と RPO](../../../../services/resilience.md#rto-rpo)と[バックアップと復元](../../../../services/dynamodb.md#backup): 復元の方法と再設定する項目を確認します。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| ストレージの自動スケーリング | 空き 10% 以下が 5 分以上 | 過去 24 時間の変更は 4 回未満 |
| 最大ストレージしきい値 | 現在の割り当て + 10% 以上 | 自動スケーリングの設定 |
| トランザクションログ | 5 分ごとに S3 へ | PITR の RPO の目安 |
| DynamoDB の目標使用率 | 20〜90%、推奨 70% | GSI は別に設定 |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| ストレージを自動で増やす | 自動スケーリングと最大ストレージしきい値 |
| 読み取りを自動で増減する | Aurora Auto Scaling |
| 急増が読めない | DynamoDB のオンデマンド |
| RDS で誤削除を戻す | PITR で新しいインスタンスを作る |
| 同じクラスターで戻す（Aurora MySQL） | バックトラック |
| 復元後の最初のクエリが遅い | 全表スキャンで先に読み込む |

## 引っかかりやすい点 {#traps}

- Aurora Auto Scaling はライターに効きません。
- リードレプリカやスタンバイには誤削除も複製されます。
- DynamoDB の PITR の後は、Auto Scaling、アラーム、タグ、TTL を再設定します。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [databases 問6](../../exercises/databases.md#q6) | 2.1.3 | 本番の RDS で空き容量が減り、人手で容量を増やしています。停止を避けて自動化します。正しいものを… |
| [databases 問7](../../exercises/databases.md#q7) | 2.1.3 | Aurora のレポートの負荷が平日の昼だけ増えます。読み取りの容量を自動で増減したいと考えています… |
| [databases 問8](../../exercises/databases.md#q8) | 2.1.3 | Aurora のライターの CPU が高くなりました。Aurora Auto Scaling を設定… |
| [databases 問9](../../exercises/databases.md#q9) | 2.1.3 | CloudFormation で作成したプロビジョンドの DynamoDB テーブルに、Auto S… |
| [databases 問10](../../exercises/databases.md#q10) | 2.1.3 | DynamoDB で短い急増のたびに ProvisionedThroughputExceededEx… |
| [databases 問11](../../exercises/databases.md#q11) | 2.3.2 | RDS で 10 分前に誤ってテーブルを削除しました。自動バックアップは有効です。Aurora では… |
| [databases 問12](../../exercises/databases.md#q12) | 2.3.2 | Aurora MySQL で、数分前の誤った更新を素早く戻したいです。クラスターはバックトラックを有… |
| [databases 問13](../../exercises/databases.md#q13) | 2.3.2 | DynamoDB の PITR で本番のテーブルを復元しました。復元後に確認し直す項目として正しいも… |
| [databases 問14](../../exercises/databases.md#q14) | 2.3.2 | RDS で RPO を数分に短くするよう求められました。現在は毎晩の手動スナップショットだけです。ど… |
| [databases 問15](../../exercises/databases.md#q15) | 2.3.2 | スナップショットから復元した RDS で、最初のクエリだけが遅くなっています。インスタンスクラスは元… |
| [databases 問16](../../exercises/databases.md#q16) | 2.2.2 | RDS の可用性の構成について正しいものはどれですか。 |

<!-- questions:end -->

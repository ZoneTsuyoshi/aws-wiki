# 分野2: アーキテクチャと設計

スケールする層の作り方と、要件からの技術の選択を扱います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [多層、マイクロサービス、イベント駆動の設計](../../domain2.md#t2-1-architectures) | マイクロサービスの設計原則、多層アーキテクチャ、要件に基づくイベント駆動、マイクロサービス、多層アーキテクチャの設計 |
| [水平スケーリングと垂直スケーリング](../../domain2.md#t2-1-scaling) | 水平スケーリングと垂直スケーリング、アーキテクチャの部品ごとのスケーリング戦略の判断 |
| [負荷分散の概念](../../domain2.md#t2-1-load-balancing) | 負荷分散の概念 |
| [キャッシュとエッジ](../../domain2.md#t2-1-caching) | キャッシュの戦略、エッジアクセラレーターの適切な使い方 |
| [マネージドサービスと専用サービス](../../domain2.md#t2-1-managed-services) | マネージドサービスの適切な用途、ワークロードに合う専用サービスの利用 |
| [要件からの技術の選択](../../domain2.md#t2-1-recommending) | 要件に基づくコンピューティング、ストレージ、ネットワーク、データベース技術の推奨 |
| [分散設計のパターン](../../domain2.md#t2-2-distributed) | 分散設計のパターン |

## 学習の順番 {#study-order}

1. [アーキテクチャパターン](../../../../services/sdk-resilience.md#architectural-patterns)と[ステートフルとステートレス](../../../../services/sdk-resilience.md#stateful-stateless): 3 つのパターンとステートレスの必要性を確認します。
2. [EC2 Auto Scaling](../../../../services/ec2-beanstalk.md#auto-scaling)と[同時実行とスケーリング](../../../../services/lambda.md#concurrency): 部品ごとのスケーリングの方法を比べます。
3. [Elastic Load Balancing](../../../../services/networking.md#elb)と[リスナーとルール](../../../../services/networking.md#alb-listeners): ロードバランサーの役割と、パスによる振り分けを確認します。
4. [キャッシュ戦略](../../../../services/databases.md#caching-strategies)と[DAX、ElastiCache、CloudFront の使い分け](../../../../services/databases.md#cache-comparison): キャッシュの戦略と場所を覚えます。
5. [データストアの選び方](../../../../services/databases.md#choosing-data-store)と[FSx の選び方](../../../../services/storage-advanced.md#fsx-selection): 要件から技術を絞る手順を確認します。
6. [指数バックオフとジッター](../../../../services/sdk-resilience.md#backoff-jitter)と[冪等性](../../../../services/sdk-resilience.md#idempotency): 再試行と冪等性の関係を理解します。
7. [サーキットブレーカー](../../../../services/sdk-resilience.md#circuit-breaker)と[グレースフルデグラデーション](../../../../services/sdk-resilience.md#graceful-degradation): 依存先の障害を局所化する方法を確認します。

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| セッションが切れてスケールできない | ElastiCache か DynamoDB に出す |
| 機能ごとに独立してデプロイする | マイクロサービス |
| 発生元と処理側を切り離す | イベント駆動 |
| RDS の読み取りを増やす | リードレプリカ |
| RDS の書き込みを増やす | サイズを上げる、Aurora に移す |
| 読まれるデータだけキャッシュする | 遅延読み込みと TTL |
| EC2 の SFTP サーバーをやめる | Transfer Family |
| cron サーバーをやめる | EventBridge のスケジュールと Lambda |
| 再試行が集中する | 指数バックオフとジッター |

## 引っかかりやすい点 {#traps}

- リードレプリカでは書き込みは増えません。
- CloudFront はキャッシュし、Global Accelerator はキャッシュしません。
- 「最小の運用負荷で」とあれば、EC2 に自分で構築する選択肢は落ちます。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [architecture 問1](../../exercises/architecture.md#q1) | 多層とマイクロサービス | ログインのたびに同じ EC2 に戻らないとセッションが切れるアプリで、スケールインで利用者が切断され… |
| [architecture 問2](../../exercises/architecture.md#q2) | 多層とマイクロサービス | 機能ごとに別のチームが独立してデプロイし、負荷の高い機能だけをスケールします。どのパターンが合います… |
| [architecture 問3](../../exercises/architecture.md#q3) | 多層とマイクロサービス | 表示、処理、データを分けて守り、インターネットからは入口だけを見せます。AWS での基本の形はどれで… |
| [architecture 問4](../../exercises/architecture.md#q4) | 多層とマイクロサービス | 画像が S3 に置かれたら、サムネイルの作成と検索の登録を自動で行います。発生元は処理の追加を意識し… |
| [architecture 問5](../../exercises/architecture.md#q5) | 水平と垂直のスケーリング | 部品ごとのスケーリングの方法の組み合わせとして、正しいものはどれですか。 |
| [architecture 問6](../../exercises/architecture.md#q6) | 水平と垂直のスケーリング | 水平スケーリングの説明として正しいものはどれですか。 |
| [architecture 問7](../../exercises/architecture.md#q7) | 水平と垂直のスケーリング | 既存の EC2 上の 1 台の DB の負荷が書き込みで上がっており、今夜すぐに対応します。短い停止… |
| [architecture 問8](../../exercises/architecture.md#q8) | 負荷分散の概念 | /api/* と /images/* を別のサービスに振り分け、1 つの入口で受けます。どれが適切で… |
| [architecture 問9](../../exercises/architecture.md#q9) | 負荷分散の概念 | ロードバランサーを間に置くと疎結合になる理由として、最も適切なものはどれですか。 |
| [architecture 問10](../../exercises/architecture.md#q10) | 負荷分散の概念 | ALB の後ろのインスタンスで障害が起きたときの動きとして正しいものはどれですか。 |
| [architecture 問11](../../exercises/architecture.md#q11) | キャッシュとエッジ | 同じ商品情報を何度も読みます。読まれるデータだけをキャッシュに入れ、キャッシュの障害でもアプリを動か… |
| [architecture 問12](../../exercises/architecture.md#q12) | キャッシュとエッジ | 世界中の利用者に画像を速く届け、オリジンの負荷も減らします。どれを選びますか。 |
| [architecture 問13](../../exercises/architecture.md#q13) | キャッシュとエッジ | データストアとキャッシュの組み合わせとして適切なものを選んでください。（2つ選択） |
| [architecture 問14](../../exercises/architecture.md#q14) | マネージドサービス | 取引先のファイル受け渡しが SFTP で、EC2 の SFTP サーバーのパッチが負担です。受け取っ… |
| [architecture 問15](../../exercises/architecture.md#q15) | マネージドサービス | cron サーバーで毎晩の小さな処理を実行しています。サーバーの管理をなくし、処理は数分で終わります… |
| [architecture 問16](../../exercises/architecture.md#q16) | マネージドサービス | 営業支援の SaaS のデータを毎日 S3 に取り込むスクリプトを保守しています。コードをなくしたい… |
| [architecture 問17](../../exercises/architecture.md#q17) | 技術の選択 | 複数の Linux サーバーで同じファイルを共有する 15 分以内のジョブがあります。次の要件に合う… |
| [architecture 問18](../../exercises/architecture.md#q18) | 技術の選択 | 要件は、キーでの読み書きが中心で、結合はなく、毎秒数十万リクエストまで遅延を一定に保つことです。どの… |
| [architecture 問19](../../exercises/architecture.md#q19) | 技術の選択 | UDP のアプリで、顧客のファイアウォールに固定 IP を登録する必要があります。世界の複数リージョ… |
| [architecture 問20](../../exercises/architecture.md#q20) | 分散設計のパターン | 多数のクライアントが一斉に失敗し、同時に再試行して障害を長引かせています。SDK の再試行の設定に加… |
| [architecture 問21](../../exercises/architecture.md#q21) | 分散設計のパターン | 決済 API の呼び出しが、ネットワークのタイムアウトで再試行されます。二重に課金しないためには何が… |
| [architecture 問22](../../exercises/architecture.md#q22) | 分散設計のパターン | 推薦機能の依存先が止まり、商品ページの全体が遅くなりました。推薦が止まっても商品ページを返します。正… |

<!-- questions:end -->

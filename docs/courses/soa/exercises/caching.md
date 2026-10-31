# キャッシュの問題集

対象の解説: [DAX、ElastiCache、CloudFront の使い分け](../../../services/databases.md#cache-comparison)、[ElastiCache](../../../services/databases.md#elasticache)、[DAX](../../../services/dynamodb.md#dax)、[キャッシュキーとポリシー](../../../services/networking.md#cache-keys)

### 問1 {#q1}

DynamoDB の読み取りが多いアプリケーションで、コードの変更を最小にしてマイクロ秒の応答にしたいです。どれを選びますか。

- A. DAX を DynamoDB の前に置く構成
- B. CloudFront のディストリビューションを DynamoDB の前に置く構成
- C. ElastiCache for Memcached とアプリケーションでのキャッシュ処理
- D. DynamoDB をオンデマンドへ変更する

??? success "答えと解説"
    **正解: A**

    DAX は DynamoDB の読み取りを、少ないコードの変更で速くします。

    - A: 正しい。
    - B: 誤り。DynamoDB の API の読み取りのキャッシュには向かない。
    - C: 誤り。アプリケーションのキャッシュ処理を自分で書く必要がある。
    - D: 誤り。容量の話で、応答はマイクロ秒にならない。

    **スキル:** [2.1.2](../domain2.md#skill-2-1-2) / **参照:** [DAX、ElastiCache、CloudFront の使い分け](../../../services/databases.md#cache-comparison)、[DAX](../../../services/dynamodb.md#dax)

### 問2 {#q2}

複数の EC2 でユーザーのセッションを共有し、RDS の重いクエリの結果もキャッシュしたいと考えています。どれが適切ですか。

- A. インスタンスストアに置いて、スティッキーセッションで固定する構成
- B. DAX のクラスターを RDS の前に置く構成
- C. CloudFront でクエリの結果をキャッシュする構成
- D. ElastiCache を共有のキャッシュとして置く構成

??? success "答えと解説"
    **正解: D**

    セッションの共有と RDS のクエリの結果のキャッシュには ElastiCache を使います。

    - A: 誤り。インスタンスの障害でセッションが失われ、共有にもならない。
    - B: 誤り。DAX は DynamoDB 専用である。
    - C: 誤り。世界中への配信のキャッシュで、セッションの共有には向かない。
    - D: 正しい。

    **スキル:** [2.1.2](../domain2.md#skill-2-1-2) / **参照:** [DAX、ElastiCache、CloudFront の使い分け](../../../services/databases.md#cache-comparison)

### 問3 {#q3}

キャッシュに、レプリカと Multi-AZ、ソート済みセットが必要です。どのエンジンを選びますか。

- A. Memcached
- B. Valkey か Redis OSS
- C. RDS Proxy
- D. DAX

??? success "答えと解説"
    **正解: B**

    レプリカ、Multi-AZ、永続化、ソート済みセットは Valkey と Redis OSS で使えます。

    - A: 誤り。Memcached にレプリケーションはない。
    - B: 正しい。
    - C: 誤り。接続のプールで、キャッシュではない。
    - D: 誤り。DynamoDB 専用で、汎用のキャッシュではない。

    **スキル:** [2.1.2](../domain2.md#skill-2-1-2) / **参照:** [Redis OSS、Valkey と Memcached](../../../services/databases.md#engines)

### 問4 {#q4}

ElastiCache（Valkey）でメモリと書き込みの容量が足りなくなりました。読み取りのレプリカは十分にあります。どう増やしますか。

- A. エンジンを Memcached に変更し、レプリケーションを無効にする
- B. レプリカをさらに追加する
- C. クラスターモードでシャードを追加する
- D. TTL をなくして、キーが消えないようにする

??? success "答えと解説"
    **正解: C**

    読み取りはレプリカ、書き込みやメモリはシャードで増やします。

    - A: 誤り。機能が失われ、既存の要件にも合わない。
    - B: 誤り。読み取りは増えるが、書き込みとメモリは増えない。
    - C: 正しい。
    - D: 誤り。メモリがさらに不足する。

    **スキル:** [2.1.2](../domain2.md#skill-2-1-2) / **参照:** [クラスターモード](../../../services/databases.md#cluster-mode)、[レプリケーションと Multi-AZ](../../../services/databases.md#elasticache-replication)

### 問5 {#q5}

`Evictions` のメトリクスが増え、キャッシュのヒット率が下がっています。対処として適切なものを選んでください。（2つ選択）

- A. `gp3` の IOPS を増やす
- B. CloudTrail のデータイベントを無効にする
- C. ノードを大きくする
- D. TTL を見直す
- E. 読み取りのレプリカだけを追加する

??? success "答えと解説"
    **正解: C, D**

    メモリが足りないと、キーが追い出されます。

    - A: 誤り。ElastiCache の追い出しは EBS の IOPS と関係がない。
    - B: 誤り。監査の設定で、キャッシュと関係がない。
    - C: 正しい。
    - D: 正しい。
    - E: 誤り。レプリカではメモリの総量が増えない。

    **スキル:** [2.1.2](../domain2.md#skill-2-1-2) / **参照:** [追い出しとメモリ](../../../services/databases.md#eviction)

### 問6 {#q6}

ElastiCache の戦略を選びます。必要なデータだけをキャッシュに載せたいと考えています。ミスの直後に遅くなることと、古い値が残ることは TTL で許容します。どれを選びますか。

- A. 複合アラーム
- B. オリジンフェイルオーバー
- C. 遅延読み込みと TTL の組み合わせ
- D. 書き込みスルー

??? success "答えと解説"
    **正解: C**

    遅延読み込みはミスのときにデータを載せます。

    - A: 誤り。アラームの機能で、キャッシュの戦略ではない。
    - B: 誤り。CloudFront の機能で、キャッシュの戦略ではない。
    - C: 正しい。
    - D: 誤り。使わないデータも載る。

    **スキル:** [2.1.2](../domain2.md#skill-2-1-2) / **参照:** [キャッシュ戦略](../../../services/databases.md#caching-strategies)

### 問7 {#q7}

読み取りのたびに常に新しい値を返したいです。書き込みが少し遅くなること、使わないデータも載ることは許容します。どの戦略が適切ですか。

- A. 遅延読み込みと長い TTL の組み合わせ
- B. ファイアウォールでキャッシュの通信を止める方式
- C. TTL を指定せずにキーを残し続ける方式
- D. 書き込みスルー

??? success "答えと解説"
    **正解: D**

    書き込みスルーは書き込みのときにキャッシュも更新します。

    - A: 誤り。ミスの直後は遅く、古い値が残る。
    - B: 誤り。キャッシュを使えなくするだけである。
    - C: 誤り。更新されなければ古い値が残り続ける。
    - D: 正しい。

    **スキル:** [2.1.2](../domain2.md#skill-2-1-2) / **参照:** [キャッシュ戦略](../../../services/databases.md#caching-strategies)

### 問8 {#q8}

ノードベースの Memcached クラスターのノードの障害の説明として正しいものはどれですか。

- A. Multi-AZ のスタンバイが自動で引き継ぐので、データは失われない
- B. ノードが落ちるとそのデータは消える
- C. レプリカが昇格して引き継ぐ
- D. データは自動で S3 に永続化されているので、起動時に戻る

??? success "答えと解説"
    **正解: B**

    データの損失を許容できる場合に使います。なお、ElastiCache Serverless はエンジンにかかわらずデータを複数の AZ に複製します。

    - A: 誤り。Memcached に Multi-AZ のフェイルオーバーはない。
    - B: 正しい。
    - C: 誤り。Memcached にレプリケーションはない。
    - D: 誤り。Memcached は永続化しない。

    **スキル:** [2.1.2](../domain2.md#skill-2-1-2) / **参照:** [Redis OSS、Valkey と Memcached](../../../services/databases.md#engines)、[レプリケーションと Multi-AZ](../../../services/databases.md#elasticache-replication)

### 問9 {#q9}

世界中の利用者へ、画像と API の GET の応答を速く配信したいです。応答は全員に共通です。どれを選びますか。

- A. CloudFront のディストリビューションを前に置く構成
- B. 各リージョンに RDS のリードレプリカを追加する構成
- C. ElastiCache をリージョンごとに作って、DNS で接続先を分ける構成
- D. DAX を各リージョンに配置して、画像を保存する構成

??? success "答えと解説"
    **正解: A**

    世界中へ画像や API の GET を速く配信するなら CloudFront です。

    - A: 正しい。
    - B: 誤り。データベースの読み取りの分散で、画像の配信には向かない。
    - C: 誤り。運用が複雑で、利用者の近くのエッジで配信できない。
    - D: 誤り。DAX は DynamoDB 専用である。

    **スキル:** [2.1.2](../domain2.md#skill-2-1-2) / **参照:** [CloudFront](../../../services/networking.md#cloudfront)、[キャッシュキーとポリシー](../../../services/networking.md#cache-keys)

### 問10 {#q10}

ElastiCache（Redis OSS）で、レプリカ 0 のノードが故障しました。起きることと予防として正しいものはどれですか。

- A. ノードの再起動で永続化の設定なしにデータが自動で戻る
- B. 全データを失うので、レプリカと Multi-AZ を構成する
- C. データは Multi-AZ のスタンバイに残るので影響はない
- D. データは CloudFront のキャッシュに残るので影響はない

??? success "答えと解説"
    **正解: B**

    レプリカ 0 のノードの故障では全データを失います。

    - A: 誤り。永続化していなければ戻らない。
    - B: 正しい。
    - C: 誤り。レプリカがなければスタンバイもない。
    - D: 誤り。別のサービスのキャッシュで、復旧には使えない。

    **スキル:** [2.1.2](../domain2.md#skill-2-1-2) / **参照:** [サービスごとの Multi-AZ と Multi-Region](../../../services/resilience.md#patterns-by-service)、[レプリケーションと Multi-AZ](../../../services/databases.md#elasticache-replication)

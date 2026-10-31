# Global Accelerator と分散の問題集

対象の解説: [Global Accelerator](../../../services/network-connectivity.md#global-accelerator), [クロスゾーン負荷分散](../../../services/networking.md#cross-zone), [Global Accelerator との比較](../../../services/resilience.md#global-accelerator)

### 問1 {#q1}

取引先がファイアウォールに接続先の IP を登録する必要がある MQTT のサービスを、東京とフランクフルトで提供します。片方のリージョンの障害時は数十秒で切り替えます。最も適切な構成はどれですか。

- A. CloudFront のディストリビューションと、各リージョンの ALB をオリジングループにする
- B. Route 53 のフェイルオーバーレコードと、各リージョンの NLB の Elastic IP を組み合わせる
- C. Global Accelerator の標準アクセラレーターと、各リージョンの NLB をエンドポイントにする
- D. S3 Transfer Acceleration と、各リージョンの API Gateway の WebSocket API

??? success "答えと解説"
    **正解: C**

    2 個の固定エニーキャスト IP で受け、正常なエンドポイントへ送ります。

    - A: 誤り。CloudFront は HTTP と HTTPS の CDN で、MQTT には向かない。
    - B: 誤り。固定の IP が 2 組になり、切り替えは DNS のキャッシュの影響を受ける。
    - C: 正しい。
    - D: 誤り。問題文の要件の固定 IP を提供しない。

    **スキル:** [グローバルなトラフィック管理](../domain1.md#t1-1-global-traffic) / **参照:** [Global Accelerator](../../../services/network-connectivity.md#global-accelerator)

### 問2 {#q2}

オンラインゲームで、マッチメイキングのサーバーが利用者を特定のセッションの EC2 へ決定的に割り当てます。EC2 は VPC のサブネットにあり、ヘルスチェックや負荷分散は不要です。最も適切な構成はどれですか。

- A. Route 53 の複数値回答で EC2 の IP を返し、クライアント側でセッションの EC2 を選ぶ
- B. カスタムルーティングアクセラレーターでポートを各 EC2 に決定的に割り当てる
- C. CloudFront の継続的デプロイのステージングで、セッションの Cookie に応じて振り分ける
- D. 標準アクセラレーターで NLB を置き、クライアントアフィニティを送信元 IP にする

??? success "答えと解説"
    **正解: B**

    ポートのマッピングで特定の EC2 とポートへ決定的に送ります。

    - A: 誤り。固定のエントリポイントにならず、キャッシュの影響も受ける。
    - B: 正しい。
    - C: 誤り。UDP のゲームのサーバーの選択に使えない。
    - D: 誤り。特定の EC2 を決定的に指定する仕組みではない。

    **スキル:** [グローバルなトラフィック管理](../domain1.md#t1-1-global-traffic) / **参照:** [Global Accelerator](../../../services/network-connectivity.md#global-accelerator)

### 問3 {#q3}

ある企業は Web アプリの配信の改善を検討しています。Global Accelerator と CloudFront の比較として正しいものはどれですか。（2つ選択）

- A. Global Accelerator は API Gateway を直接エンドポイントとして指定できる
- B. Global Accelerator は URL のパスでオリジンを選べる
- C. Global Accelerator はキャッシュを持たず、L4 の TCP と UDP を扱う
- D. CloudFront はコンテンツをエッジにキャッシュできる
- E. CloudFront は固定のエニーキャスト IP を 2 個提供し、取引先の許可リストに使える

??? success "答えと解説"
    **正解: C, D**

    向く通信が違います。

    - A: 誤り。エンドポイントは ALB、NLB、EC2、Elastic IP。
    - B: 誤り。パスの判定は L7 の機能で、CloudFront の機能。
    - C: 正しい。
    - D: 正しい。
    - E: 誤り。固定の IP は Global Accelerator の特徴。

    **スキル:** [グローバルなトラフィック管理](../domain1.md#t1-1-global-traffic) / **参照:** [Global Accelerator](../../../services/network-connectivity.md#global-accelerator), [Global Accelerator との比較](../../../services/resilience.md#global-accelerator)

### 問4 {#q4}

東京と大阪のエンドポイントグループを持つアクセラレーターで、大阪の ALB を保守します。保守の前に新しい接続を東京へ移し、既存の接続はそのまま終わらせたいと考えています。DNS の操作はしません。設定はどれですか。

- A. 大阪のエンドポイントグループのトラフィックダイヤルを 0% にする
- B. クライアントアフィニティを `Source IP` にして、大阪へ向かう通信を東京へ固定する
- C. アクセラレーターを無効にして、固定 IP を手放す前に DNS を切り替える
- D. 大阪の ALB の重みを 255 にする

??? success "答えと解説"
    **正解: A**

    ダイヤルは新しい接続にだけ効きます。

    - A: 正しい。
    - B: 誤り。同じ先へ送る設定で、保守の切り離しにならない。
    - C: 誤り。アクセラレーター全体の停止になり、東京も止まる。
    - D: 誤り。重みを上げると、大阪の中でその ALB へ増える。

    **スキル:** [Global Accelerator](../domain3.md#t3-3-global-accelerator) / **参照:** [Global Accelerator](../../../services/network-connectivity.md#global-accelerator)

### 問5 {#q5}

1 つのエンドポイントグループに同じ規模の ALB を 2 台登録しています。新しいバージョンの ALB へ全体の約 0.4% だけを流して検証します。重みの設定で正しいものはどれですか。

- A. ダイヤルを 0.4% にして、新と旧の両方を同じ重みにする
- B. 新の重みを `1`、旧の重みを既定の `128` のままにする
- C. 新の重みを `0`、旧の重みを `255` にして、ダイヤルで 0.4% を指定する
- D. 新の重みを `1`、旧の重みを `255` にする

??? success "答えと解説"
    **正解: D**

    重みは 0〜255 で、比率はグループの合計に対する割合です。`1/256` は約 0.4% です。

    - A: 誤り。グループ全体の割合で、新と旧の比率にならない。
    - B: 誤り。1/129 で、目標より大きくなる。
    - C: 誤り。重みが 0 の新には流れない。
    - D: 正しい。

    **スキル:** [Global Accelerator](../domain3.md#t3-3-global-accelerator) / **参照:** [Global Accelerator](../../../services/network-connectivity.md#global-accelerator)

### 問6 {#q6}

アクセラレーターの EC2 エンドポイントがすべて異常と表示されます。アプリは正常に応答しており、ALB は使っていません。ヘルスチェックのプロトコルも正しいです。最も可能性の高い原因はどれですか。

- A. トラフィックダイヤルが既定の 100% で、ヘルスチェックの通信が抑制されている
- B. EC2 の SG で、Route 53 のヘルスチェッカーの IP を許可していない
- C. エンドポイントの重みが既定の `128` で、ヘルスチェックの対象外になっている
- D. Global Accelerator は EC2 をエンドポイントに指定できないので、登録が無効になっている

??? success "答えと解説"
    **正解: B**

    EC2 のチェックには、Route 53 のヘルスチェッカーの IP を許可します。

    - A: 誤り。既定で問題ない。
    - B: 正しい。
    - C: 誤り。既定の重みでも対象。
    - D: 誤り。EC2 はエンドポイントに指定できる。

    **スキル:** [Global Accelerator](../domain3.md#t3-3-global-accelerator) / **参照:** [Global Accelerator](../../../services/network-connectivity.md#global-accelerator)

### 問7 {#q7}

保守で Global Accelerator を一時的に止める計画です。性能の測定の方法も運用の手順書に書きます。説明として正しいものはどれですか。

- A. 固定 IP への ping の応答時間で、エンドポイントまでの性能を測定できる
- B. ダイヤルを変えると既存の接続もすぐに移る
- C. エンドポイントが全部異常になると、通信をすべて破棄する
- D. 削除すると固定 IP を失うが、無効化なら保たれるので無効化を使う

??? success "答えと解説"
    **正解: D**

    固定 IP を保つなら、削除せず無効化します。

    - A: 誤り。ping にはエッジが応答する。
    - B: 誤り。新しい接続にのみ効く。
    - C: 誤り。グループ内の全エンドポイントへ送る。
    - D: 正しい。

    **スキル:** [Global Accelerator](../domain3.md#t3-3-global-accelerator) / **参照:** [Global Accelerator](../../../services/network-connectivity.md#global-accelerator), [Global Accelerator との比較](../../../services/resilience.md#global-accelerator)

### 問8 {#q8}

ALB のターゲットの処理時間のばらつきが大きく、一部のターゲットに処理中のリクエストが集中しています。セッションのスティッキーは使っていません。最も適切な変更はどれですか。

- A. アルゴリズムを `least_outstanding_requests` にする
- B. スロースタートを有効にして、新しいターゲットを 15 分かけて増やす
- C. 登録解除の待ちを 3,600 秒に延ばして、処理中のリクエストを完了させる
- D. `weighted_random` にしてから手動で各ターゲットに重みを設定し続ける

??? success "答えと解説"
    **正解: A**

    処理中のリクエストの少ないターゲットへ送ります。

    - A: 正しい。
    - B: 誤り。新しいターゲットの話で、処理時間のばらつきは解決しない。
    - C: 誤り。解除のときの動作で、分散の改善にならない。
    - D: 誤り。設定の仕組みがなく、運用の負担も大きい。

    **スキル:** [分散のパターン](../domain3.md#t3-3-lb) / **参照:** [リスナーとルール](../../../services/networking.md#alb-listeners), [クロスゾーン負荷分散](../../../services/networking.md#cross-zone)

### 問9 {#q9}

NLB の AZ A に 2 台、AZ B に 8 台のターゲットがあります。クロスゾーンは無効で、DNS は両方の AZ の IP を均等に返します。1 台あたりの通信の割合として正しいものはどれですか。

- A. A は各 50%、B は各 12.5%
- B. A も B も各 10%
- C. A は各 25%、B は各 6.25%
- D. A は各 5%、B は各 11.25%

??? success "答えと解説"
    **正解: C**

    無効なら AZ ごとに 50% で分け、その中で台数で割ります。

    - A: 誤り。合計が 200% になる。
    - B: 誤り。クロスゾーンを有効にしたときの計算。
    - C: 正しい。
    - D: 誤り。AZ 間の分割の仕組みに合わない。

    **スキル:** [分散のパターン](../domain3.md#t3-3-lb) / **参照:** [クロスゾーン負荷分散](../../../services/networking.md#cross-zone)

### 問10 {#q10}

ALB の加重ターゲットグループで新バージョンへ 10% を流しています。新のターゲットがすべて異常になりましたが、残りの 90% は正常です。この状態で起きることと対策として正しいものはどれですか。

- A. 新へ向かう 10% は自動で他方へ切り替わらないので、監視して重みを戻す
- B. リスナーのルールが無効になり、既定のアクションである 503 の固定応答に切り替わる
- C. Route 53 の加重レコードがこの状況を検知し、DNS の応答から ALB 全体を外す
- D. ALB が自動で重みを 0 にして、全部の通信を正常なターゲットグループへ流す

??? success "答えと解説"
    **正解: A**

    加重の先の片方が空、または異常のみでも、自動で他方へは切り替わりません。

    - A: 正しい。
    - B: 誤り。ルールが無効になることはない。
    - C: 誤り。ALB の中の重みは Route 53 には見えない。
    - D: 誤り。片方が異常でも自動では切り替わらない。

    **スキル:** [分散のパターン](../domain3.md#t3-3-lb) / **参照:** [リスナーとルール](../../../services/networking.md#alb-listeners)

### 問11 {#q11}

非 HTTP のサービスを複数のリージョンで提供しています。低遅延と固定 IP が必要で、AZ の台数が不均等なことも問題になっています。分散のパターンとして最も適切な組み合わせはどれですか。

- A. CloudFront と ALB、オリジングループで AZ の不均等を吸収する
- B. Route 53 の加重と ALB、ALB のアルゴリズムを `round_robin` にする
- C. Global Accelerator と ALB、ALB のターゲットをスティッキーにして偏らせる
- D. Global Accelerator と NLB、NLB のクロスゾーンを有効にする

??? success "答えと解説"
    **正解: D**

    固定 IP と高速な切り替えは Global Accelerator と NLB です。

    - A: 誤り。非 HTTP には使えない。
    - B: 誤り。非 HTTP には ALB を使えず、固定 IP もない。
    - C: 誤り。非 HTTP には ALB を使えず、偏りも増やす。
    - D: 正しい。

    **スキル:** [分散のパターン](../domain3.md#t3-3-lb) / **参照:** [Global Accelerator](../../../services/network-connectivity.md#global-accelerator), [ルーティングポリシー](../../../services/networking.md#routing-policies)

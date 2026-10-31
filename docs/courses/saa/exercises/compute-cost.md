# コンピューティングの費用の問題集

対象の解説: [コスト管理](../../../services/cost-management.md)、[EC2 と Elastic Beanstalk](../../../services/ec2-beanstalk.md)

### 問1 {#q1}

3 年間動きますが、将来 Fargate へ移す可能性がある定常の負荷です。最も合う割引はどれですか。

- A. Compute Savings Plans
- B. スタンダード RI
- C. EC2 Instance Savings Plans
- D. スポットインスタンス

??? success "答えと解説"
    **正解: A**

    Compute Savings Plans は EC2、Fargate、Lambda に適用されます。

    - A: 正しい。
    - B: 誤り。構成の変更に弱い。
    - C: 誤り。EC2 のファミリーに縛られる。
    - D: 誤り。中断される。

    **スキル:** [購入オプション](../domain4.md#t4-2-purchase) / **参照:** [Savings Plans](../../../services/cost-management.md#savings-plans)

### 問2 {#q2}

中断してもやり直せる夜間のバッチです。最も安い選択はどれですか。

- A. オンデマンドの Capacity Reservation
- B. Dedicated Hosts
- C. 3 年の Standard RI
- D. 複数のプールを指定したスポットインスタンス

??? success "答えと解説"
    **正解: D**

    最大 90% の割引です。中断は 2 分前に通知されます。

    - A: 誤り。割引がなく、容量の確保は要らない。
    - B: 誤り。高く、BYOL の要件もない。
    - C: 誤り。夜間だけのために確約すると、止めている時間も払う。
    - D: 正しい。

    **スキル:** [購入オプション](../domain4.md#t4-2-purchase) / **参照:** [スポットインスタンス](../../../services/cost-management.md#spot)

### 問3 {#q3}

スポットの中断の影響を減らす設定を選んでください。（2つ選択）

- A. 1 つのインスタンスタイプと 1 つの AZ に絞る
- B. 複数のインスタンスタイプと AZ を指定する
- C. 中断の通知を無視して処理を続ける
- D. `price-capacity-optimized` で配分する
- E. Savings Plans を追加する

??? success "答えと解説"
    **正解: B, D**

    容量のプールを広げます。

    - A: 誤り。容量の不足の影響を受けやすい。
    - B: 正しい。
    - C: 誤り。2 分後に中断される。
    - D: 正しい。
    - E: 誤り。中断の防止にならない。

    **スキル:** [購入オプション](../domain4.md#t4-2-purchase) / **参照:** [スポットの中断への対応](../../../services/operations.md#spot-interruptions)

### 問4 {#q4}

特定の AZ で必ず台数を確保したいと考えています。割引の Savings Plans は既に買っています。何を追加しますか。

- A. Savings Plans の金額の増額
- B. Compute Optimizer の有効化
- C. オンデマンドの Capacity Reservation
- D. スポットブロックの購入

??? success "答えと解説"
    **正解: C**

    Capacity Reservation は容量を確保します。割引は Savings Plans と併用します。

    - A: 誤り。Savings Plans に容量の確保はない。
    - B: 誤り。推奨の機能。
    - C: 正しい。
    - D: 誤り。スポットブロックは終了した機能で、容量の確保にもならない。

    **スキル:** [購入オプション](../domain4.md#t4-2-purchase) / **参照:** [購入オプション](../../../services/cost-management.md#purchase-options)

### 問5 {#q5}

ソケットやコア単位のライセンスを持ち込みます（BYOL）。どれを選びますか。

- A. Compute Savings Plans だけで対応する
- B. Dedicated Hosts に配置する
- C. 共有のオンデマンドインスタンスで対応する
- D. スポットの Fleet を使う

??? success "答えと解説"
    **正解: B**

    物理のサーバーのソケットとコアが見えます。

    - A: 誤り。ライセンスの要件を満たさない。
    - B: 正しい。
    - C: 誤り。ソケットやコアを見られない。
    - D: 誤り。物理の配置を制御できない。

    **スキル:** [購入オプション](../domain4.md#t4-2-purchase) / **参照:** [購入オプション](../../../services/cost-management.md#purchase-options)

### 問6 {#q6}

1 日に数百回、数秒だけ動く処理です。アイドルの時間が長いです。最も安いのはどれですか。

- A. 常時稼働の Fargate のタスク
- B. 専用の EMR クラスターで都度実行
- C. Lambda でイベントごとに実行する
- D. 常時稼働の小さな EC2 と Savings Plans

??? success "答えと解説"
    **正解: C**

    Lambda は実行の分だけ課金されます。

    - A: 誤り。アイドルの時間も課金される。
    - B: 誤り。過剰。
    - C: 正しい。
    - D: 誤り。アイドルの時間も課金される。

    **スキル:** [コンピューティングの選択](../domain4.md#t4-2-compute-choice) / **参照:** [実行モデル](../../../services/lambda.md#execution-model)

### 問7 {#q7}

常に高い負荷が続く定常のアプリです。最も安い可能性が高い組み合わせはどれですか。

- A. EC2 と Compute Savings Plans
- B. オンデマンドの EC2 を夜間も動かし続ける
- C. Lambda のプロビジョニング済み同時実行だけで処理する
- D. Fargate のオンデマンドで大きなタスクを動かす

??? success "答えと解説"
    **正解: A**

    定常の部分に確約割引を適用します。

    - A: 正しい。
    - B: 誤り。割引がない。
    - C: 誤り。定常の高負荷では EC2 より高くなることが多い。
    - D: 誤り。定常の高負荷では EC2 より高くなることが多い。

    **スキル:** [コンピューティングの選択](../domain4.md#t4-2-compute-choice) / **参照:** [向いているものの選び方](../../../services/cost-management.md#purchase-choice)

### 問8 {#q8}

静的な Web サイトを最も安く公開します。サーバーの管理もしません。どの組み合わせですか。

- A. Lambda と API Gateway で HTML を返す
- B. Fargate と NLB
- C. EC2 と ALB と Auto Scaling を複数 AZ に置く
- D. S3 と CloudFront の組み合わせ

??? success "答えと解説"
    **正解: D**

    静的なコンテンツにサーバーは要りません。

    - A: 誤り。静的サイトには不要な処理が増える。
    - B: 誤り。高い。
    - C: 誤り。高く、管理が必要。
    - D: 正しい。

    **スキル:** [コンピューティングの選択](../domain4.md#t4-2-compute-choice) / **参照:** [静的ウェブサイトホスティング](../../../services/s3.md#static-website)

### 問9 {#q9}

コンピューティングの利用率を上げ、費用を下げる方法として適切なものを選んでください。（2つ選択）

- A. 負荷の高い機能だけをスケールするマイクロサービスへの分割
- B. 複数のタスクを 1 台の EC2 に詰めるコンテナの集約
- C. 全環境を本番と同じ構成で常に動かす構成
- D. 使っていないインスタンスを残して、次の増加に備える運用
- E. 全機能を 1 つの大きなサーバーに載せて常に 2 倍の余裕を持たせる構成

??? success "答えと解説"
    **正解: A, B**

    余った容量を減らします。

    - A: 正しい。
    - B: 正しい。
    - C: 誤り。不要な費用がかかる。
    - D: 誤り。費用がかかり続ける。
    - E: 誤り。余った容量の費用がかかる。

    **スキル:** [コンピューティングの選択](../domain4.md#t4-2-compute-choice) / **参照:** [キャパシティプロバイダー](../../../services/containers.md#capacity-providers)

### 問10 {#q10}

動画のエンコードのバッチを M ファミリーで動かしており、CPU が足りずに大きなサイズを使っています。費用を下げるファミリーはどれですか。

- A. I ファミリーへ移して NVMe を増やす
- B. C ファミリーへ移して同じ vCPU 数にする
- C. T 系に移す
- D. R ファミリーへ移してメモリを 2 倍にする

??? success "答えと解説"
    **正解: B**

    CPU 重視のワークロードには C です。

    - A: 誤り。ストレージ重視。
    - B: 正しい。
    - C: 誤り。低負荷向け。
    - D: 誤り。メモリ重視。

    **スキル:** [ファミリーとサイズ](../domain4.md#t4-2-instances) / **参照:** [インスタンスタイプとメモリ、CPU の要件](../../../services/ec2-beanstalk.md#instance-types)

### 問11 {#q11}

`m6i.xlarge` で動く Java のアプリは、arm64 でも動くことを確認済みです。CPU とメモリの比率を変えずに、価格性能を上げて費用を下げます。どれに変更しますか。

- A. `r7i.xlarge`（メモリ最適化）
- B. `c7i.large`（CPU 重視）
- C. `m7g.xlarge`（Graviton）
- D. `m7i.2xlarge`（2 倍のサイズ）

??? success "答えと解説"
    **正解: C**

    `m7g.xlarge` は、m がファミリー、7 が世代、g が Graviton、xlarge がサイズです。Graviton は Arm ベースで、同じ M ファミリーのまま価格性能を上げられます。

    - A: 誤り。メモリの比率が変わり、要件に合わない。
    - B: 誤り。CPU とメモリの比率が変わる。
    - C: 正しい。
    - D: 誤り。サイズが増えて、費用も増える。

    **スキル:** [ファミリーとサイズ](../domain4.md#t4-2-instances) / **参照:** [インスタンスタイプとメモリ、CPU の要件](../../../services/ec2-beanstalk.md#instance-types)

### 問12 {#q12}

EC2 のサイズを小さくする前に確認すべきことを選んでください。（2つ選択）

- A. CPU が低ければ、メモリを調べずにすぐ半分にしてよい
- B. エージェントでメモリも収集する
- C. Compute Optimizer の推奨を確認する
- D. ルートユーザーでのログインの履歴を調べる
- E. 課金の明細だけで判断できる

??? success "答えと解説"
    **正解: B, C**

    `CPUUtilization` だけでは足りません。

    - A: 誤り。メモリが足りない可能性がある。
    - B: 正しい。
    - C: 正しい。
    - D: 誤り。関係ない。
    - E: 誤り。使用状況が必要。

    **スキル:** [ファミリーとサイズ](../domain4.md#t4-2-instances) / **参照:** [Compute Optimizer と適正サイズ](../../../services/cost-management.md#compute-optimizer)

### 問13 {#q13}

起動に 15 分かかるアプリを夜間に止め、翌朝はメモリの状態から再開します。正しい組み合わせを選んでください。（2つ選択）

- A. インスタンスストアにメモリの内容を保存する
- B. 既存のインスタンスの属性を変更して休止を有効にする
- C. 休止を起動時に有効にする
- D. ルートボリュームが暗号化されていなくても休止を使う
- E. ルートボリュームを暗号化する

??? success "答えと解説"
    **正解: C, E**

    `stopped` の間はインスタンス料金がかかりません。EBS の料金はかかります。

    - A: 誤り。EBS のルートボリュームに保存する。
    - B: 誤り。起動時のみ設定できる。
    - C: 正しい。
    - D: 誤り。暗号化が必須。
    - E: 正しい。

    **スキル:** [スケーリングと休止](../domain4.md#t4-2-scaling) / **参照:** [休止](../../../services/operations.md#hibernate)

### 問14 {#q14}

休止の条件として正しいものはどれですか。

- A. Linux の RAM は 16 GiB 以下、Windows は 150 GiB 未満
- B. 休止中もインスタンスの料金がかかり続ける
- C. RAM の大きさの制限はない
- D. Linux の RAM は 150 GiB 未満、Windows は 16 GiB 以下

??? success "答えと解説"
    **正解: D**

    ルートボリュームにも RAM が入る空きが必要です。

    - A: 誤り。逆。
    - B: 誤り。`stopped` の間はかからない。
    - C: 誤り。制限がある。
    - D: 正しい。

    **スキル:** [スケーリングと休止](../domain4.md#t4-2-scaling) / **参照:** [休止](../../../services/operations.md#hibernate)

### 問15 {#q15}

開発環境の EC2 20 台は、平日の日中（週 50 時間）だけ使います。購入の確約はせず、費用を最も簡単に下げます。どうしますか。

- A. 夜間と週末をスケジュールで止める
- B. サイズを大きくして処理を早く終わらせ、常に動かす
- C. 別のリージョンに移して常に動かす
- D. 3 年の RI を買って常に動かす

??? success "答えと解説"
    **正解: A**

    週 168 時間のうち 118 時間を止めると、インスタンスの料金は約 7 割減ります。EBS の料金は残ります。

    - A: 正しい。
    - B: 誤り。費用が増える。
    - C: 誤り。停止の効果を得られない。
    - D: 誤り。止めている時間の分も払う。

    **スキル:** [スケーリングと休止](../domain4.md#t4-2-scaling) / **参照:** [EC2 Auto Scaling](../../../services/ec2-beanstalk.md#auto-scaling)

### 問16 {#q16}

3 つのサービスで、各サービスが HTTP のパスで分かれています。今は ALB を 3 台使っています。費用を下げるにはどうしますか。

- A. Global Accelerator を 3 つ追加する
- B. 1 つの ALB のリスナールールにまとめる
- C. NLB を 3 台に置き換える
- D. GWLB にまとめる

??? success "答えと解説"
    **正解: B**

    パスで分けられるなら、ロードバランサーは 1 つで足ります。

    - A: 誤り。費用が増える。
    - B: 正しい。
    - C: 誤り。台数は減らず、パスで振り分けられない。
    - D: 誤り。ファイアウォール向け。

    **スキル:** [負荷分散の選択](../domain4.md#t4-2-lb) / **参照:** [リスナーとルール](../../../services/networking.md#alb-listeners)

### 問17 {#q17}

要件に合うロードバランサーの組み合わせはどれですか。TCP で固定 IP が必要なもの、HTTP のマイクロサービスの順です。

- A. 両方とも ALB
- B. GWLB、NLB の順
- C. NLB、ALB の順
- D. ALB、GWLB の順

??? success "答えと解説"
    **正解: C**

    要件に合う最小のものを選びます。

    - A: 誤り。ALB に固定 IP はなく、TCP も扱わない。
    - B: 誤り。GWLB はファイアウォール向け。
    - C: 正しい。
    - D: 誤り。固定 IP の TCP に合わない。

    **スキル:** [負荷分散の選択](../domain4.md#t4-2-lb) / **参照:** [ALB と NLB の違い](../../../services/networking.md#alb-vs-nlb)

### 問18 {#q18}

ファイアウォールの仮想アプライアンスを複数台で動かすときに最も合うものはどれですか。

- A. ALB のターゲットにアプライアンスを登録する構成
- B. NLB の TCP のターゲットにする構成
- C. Route 53 の加重レコードでアプライアンスに振り分ける構成
- D. GWLB とアプライアンスのターゲットグループ

??? success "答えと解説"
    **正解: D**

    GWLB はすべてのポートの IP パケットを扱います。

    - A: 誤り。HTTP の処理に限られる。
    - B: 誤り。透過的な挿入に向かない。
    - C: 誤り。パケットの経路に挟めない。
    - D: 正しい。

    **スキル:** [負荷分散の選択](../domain4.md#t4-2-lb) / **参照:** [GWLB](../../../services/networking.md#gwlb)

### 問19 {#q19}

本番と開発の構成の使い分けとして適切なものはどれですか。

- A. 開発に 3 年の Savings Plans を買い、本番はオンデマンドにする
- B. 本番は複数 AZ、開発は 1 AZ で夜間停止
- C. 本番は 1 AZ とスポットで動かし、開発は複数 AZ にする
- D. 本番と開発を同じ複数 AZ と Multi-AZ の DB で揃え、常に動かす

??? success "答えと解説"
    **正解: B**

    本番と同じ構成を全環境に持つ必要はありません。

    - A: 誤り。確約の向く先が逆。
    - B: 正しい。
    - C: 誤り。逆で、本番の可用性を失う。
    - D: 誤り。開発に不要な費用がかかる。

    **スキル:** [環境ごとの可用性](../domain4.md#t4-2-availability) / **参照:** [サービスごとの Multi-AZ と Multi-Region](../../../services/resilience.md#patterns-by-service)

### 問20 {#q20}

本番の Web 層を 2 AZ から 3 AZ に増やす案を評価します。可用性は上がります。増える費用として考慮するものはどれですか。

- A. AZ 間の転送料と、余分に持つ容量の費用
- B. AZ を増やすと、インターネットからの受信が有料になる
- C. IAM の料金の増加
- D. S3 の容量の単価の上昇

??? success "答えと解説"
    **正解: A**

    可用性は上がりますが、費用も増えます。

    - A: 正しい。
    - B: 誤り。受信は無料。
    - C: 誤り。IAM に追加料金はない。
    - D: 誤り。関係ない。

    **スキル:** [環境ごとの可用性](../domain4.md#t4-2-availability) / **参照:** [データ転送の費用](../../../services/cost-management.md#data-transfer)

### 問21 {#q21}

データの所在の制約がない夜間のバッチを東京リージョンで動かしています。結果は S3 に置くだけで、利用者との低遅延も要りません。費用の観点で検討することはどれですか。

- A. 料金の安いリージョンへの移動を、データの転送料も含めて比べる
- B. どのリージョンも料金は同じなので、移しても変わらない
- C. Global Accelerator で全リージョンに配置する
- D. 利用者の多い国のリージョンに必ず置く

??? success "答えと解説"
    **正解: A**

    所在の制約がなければ、料金は判断の材料です。

    - A: 正しい。
    - B: 誤り。リージョンで料金は違う。
    - C: 誤り。費用が増える。
    - D: 誤り。バッチには関係が薄い。

    **スキル:** [環境ごとの可用性](../domain4.md#t4-2-availability) / **参照:** [リージョン](../../../services/cloud-foundations.md#regions)

### 問22 {#q22}

CloudFront でビューワーのヘッダーを書き換えてオリジンへのリクエストを減らします。軽い処理で費用も抑えます。どれを選びますか。

- A. 各リージョンに EC2 を置いてプロキシにする構成
- B. Outposts を各国に置く構成
- C. CloudFront Functions
- D. Wavelength に Lambda を置く構成

??? success "答えと解説"
    **正解: C**

    エッジで処理すると、オリジンの負荷が減ります。

    - A: 誤り。費用も管理も増える。
    - B: 誤り。目的が違う。
    - C: 正しい。
    - D: 誤り。目的が違う。

    **スキル:** [エッジとハイブリッド](../domain4.md#t4-2-edge-hybrid) / **参照:** [Lambda@Edge と CloudFront Functions](../../../services/networking.md#edge-functions)

### 問23 {#q23}

既存のオンプレミスのサーバーを活かして ECS を動かし、コントロールプレーンは AWS を使います。どれを選びますか。

- A. Outposts のラックの購入
- B. ECS Anywhere の外部インスタンス
- C. Fargate のタスクをオンプレミスに指定
- D. EKS Distro を自分で運用

??? success "答えと解説"
    **正解: B**

    ECS Anywhere は外部のインスタンスを登録します。

    - A: 誤り。新しいハードウェアが必要。
    - B: 正しい。
    - C: 誤り。オンプレミスでは動かない。
    - D: 誤り。ECS ではない。

    **スキル:** [エッジとハイブリッド](../domain4.md#t4-2-edge-hybrid) / **参照:** [Amazon ECS Anywhere](../../../services/operations.md#ecs-anywhere)

### 問24 {#q24}

ソフトウェアのライセンスの使用数を追跡し、超過を防ぎます。どれを選びますか。

- A. Cost Explorer の予測
- B. Secrets Manager のローテーション
- C. Trusted Advisor のサービスリミット
- D. License Manager のルール

??? success "答えと解説"
    **正解: D**

    License Manager はライセンスのルールを設定し、超過を防げます。

    - A: 誤り。費用の分析。
    - B: 誤り。認証情報の機能。
    - C: 誤り。クォータの点検。
    - D: 正しい。

    **スキル:** [エッジとハイブリッド](../domain4.md#t4-2-edge-hybrid) / **参照:** [AWS License Manager](../../../services/governance.md#license-manager)

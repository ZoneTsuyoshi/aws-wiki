# 分野2: 高可用性と DR

単一障害点をなくし、要件の時間内に戻せる設計を選びます。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [グローバルインフラとルーティング](../../domain2.md#t2-2-global) | グローバルインフラストラクチャ、基本的なネットワークの概念 |
| [AZ とリージョンをまたぐ構成](../../domain2.md#t2-2-multi-az-region) | リージョンや AZ をまたぐ高可用性、耐障害性に必要なサービスの判断 |
| [単一障害点の排除](../../domain2.md#t2-2-spof) | 負荷分散の概念、単一障害点を軽減する設計の実装 |
| [フェイルオーバーの戦略](../../domain2.md#t2-2-failover) | フェイルオーバーの戦略 |
| [DR 戦略の選択](../../domain2.md#t2-2-dr) | DR 戦略、業務要件に合う DR 戦略の選択 |
| [不変インフラと自動化](../../domain2.md#t2-2-immutable) | 不変インフラストラクチャ、インフラの整合性を確保する自動化戦略の判断 |
| [サービスクォータとスロットリング](../../domain2.md#t2-2-quotas) | サービスクォータとスロットリング |
| [可視性と業務に基づくメトリクス](../../domain2.md#t2-2-visibility) | ワークロードの可視性、業務要件に基づく、高可用性のためのメトリクスの特定 |
| [レガシーアプリの信頼性の向上](../../domain2.md#t2-2-legacy) | レガシーアプリやクラウド向けでないアプリの信頼性を高めるサービスの利用 |

## 学習の順番 {#study-order}

1. [ルーティングポリシー](../../../../services/networking.md#routing-policies)と[Route 53 ヘルスチェック](../../../../services/networking.md#route53-health-checks): ルーティングポリシーとヘルスチェックを確認します。
2. [サービスごとの Multi-AZ と Multi-Region](../../../../services/resilience.md#patterns-by-service)と[高可用性のための Auto Scaling](../../../../services/resilience.md#auto-scaling-ha): サービスごとの Multi-AZ と Multi-Region を表で覚えます。
3. [静的安定性](../../../../services/resilience.md#static-stability)と[ヘルスチェック](../../../../services/ec2-beanstalk.md#asg-health-checks): 静的安定性と、ELB のヘルスチェックを押さえます。
4. [Route 53 のフェイルオーバー設計](../../../../services/resilience.md#route53-failover)と[Global Accelerator との比較](../../../../services/resilience.md#global-accelerator): DNS と固定 IP の切り替えの違いを比べます。
5. [RTO と RPO](../../../../services/resilience.md#rto-rpo)と[4 つの DR 戦略](../../../../services/resilience.md#dr-strategies): 4 つの戦略を RTO、RPO、費用で比べます。
6. [ドリフト検出](../../../../services/iac.md#drift)と[修復](../../../../services/governance.md#config-remediation): 変更の検出と自動修復を確認します。
7. [クォータの上限に近づいたとき](../../../../services/observability.md#quota-alerts)と[X-Ray によるトレース](../../../../services/observability.md#xray): クォータの監視と可視性の道具を確認します。
8. [スティッキーセッション](../../../../services/networking.md#stickiness)と[NLB の設定](../../../../services/networking.md#nlb-settings): アプリを変更できないときの対策を確認します。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| バックアップと復元 | RTO、RPO は時間単位 | 費用が最小 |
| パイロットライト | 数十分 | アプリは停止か未作成 |
| ウォームスタンバイ | 数分 | 縮小版が稼働し、すぐ処理できる |
| マルチサイト | ほぼゼロ | 費用が最大 |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 欧州の利用者に欧州のサイトだけを見せる | 位置情報ルーティング |
| DNS キャッシュの影響なしで切り替える | Global Accelerator |
| アプリの異常でインスタンスを置き換える | Auto Scaling のヘルスチェックに ELB を加える |
| 別リージョンの Aurora に複製する | Global Database |
| 手作業の変更を見つける | ドリフト検出 |
| DR リージョンで台数を増やせない | クォータを事前に引き上げる |
| 注文の処理の遅れを監視する | `ApproximateAgeOfOldestMessage` |
| セッションがサーバーにあり、コードを変えられない | スティッキーセッション |

## 引っかかりやすい点 {#traps}

- Multi-AZ の DB インスタンスのスタンバイは読めません。
- クォータはリージョンごとで、審査に時間がかかることがあります。
- CloudFront のオリジンフェイルオーバーは GET、HEAD、OPTIONS が対象です。
- Proton はサポートが終了しました。新しい設計の答えにしません。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [resilience 問1](../../exercises/resilience.md#q1) | インフラとルーティング | 欧州の利用者には規制のため欧州のサイトだけを見せます。Route 53 のどのルーティングポリシーを… |
| [resilience 問2](../../exercises/resilience.md#q2) | インフラとルーティング | 主系のリージョンが落ちたら副系へ切り替えます。Route 53 で必要な設定の組み合わせを選んでくだ… |
| [resilience 問3](../../exercises/resilience.md#q3) | インフラとルーティング | 3 つの AZ のプライベートサブネットに EC2 があり、AZ ごとに NAT ゲートウェイを置き… |
| [resilience 問4](../../exercises/resilience.md#q4) | AZ とリージョン | RDS MySQL の可用性を上げ、書き込みの切り替えは自動にします。同じリージョンの AZ の障害… |
| [resilience 問5](../../exercises/resilience.md#q5) | AZ とリージョン | 東京の Aurora MySQL のデータを別のリージョンにも持ち、リージョンの障害に備えます。別の… |
| [resilience 問6](../../exercises/resilience.md#q6) | AZ とリージョン | 複数リージョンにあるバケットに、1 つのグローバルなエンドポイントでアクセスし、最寄りのバケットへ送… |
| [resilience 問7](../../exercises/resilience.md#q7) | 単一障害点の排除 | 1 台の EC2 で動く Web アプリの単一障害点をなくします。正しい組み合わせはどれですか。（2… |
| [resilience 問8](../../exercises/resilience.md#q8) | 単一障害点の排除 | Auto Scaling グループの EC2 でアプリが応答を返さなくなりましたが、インスタンスは置… |
| [resilience 問9](../../exercises/resilience.md#q9) | 単一障害点の排除 | オンプレミスと AWS の接続の単一障害点を減らします。Direct Connect を 1 本使っ… |
| [resilience 問10](../../exercises/resilience.md#q10) | フェイルオーバーの戦略 | DNS のキャッシュの影響を受けずに、すばやく別のリージョンへ切り替えます。クライアントは固定 IP… |
| [resilience 問11](../../exercises/resilience.md#q11) | フェイルオーバーの戦略 | CloudFront のオリジンの S3 が止まったら、別のリージョンの S3 から読み取りを続けま… |
| [resilience 問12](../../exercises/resilience.md#q12) | フェイルオーバーの戦略 | Aurora のライターが切り替わってもアプリの設定を変えずに書き込み先に接続します。アプリが使うべ… |
| [resilience 問13](../../exercises/resilience.md#q13) | DR 戦略の選択 | RPO と RTO の説明として正しいものはどれですか。 |
| [resilience 問14](../../exercises/resilience.md#q14) | DR 戦略の選択 | 社内の日報システムの要件は RTO 24 時間、RPO 24 時間で、費用を最小にします。どの戦略を… |
| [resilience 問15](../../exercises/resilience.md#q15) | DR 戦略の選択 | RTO 数十分、RPO 数分の要件です。平時の費用を抑えるため、アプリのサーバーは動かさず、データだ… |
| [resilience 問16](../../exercises/resilience.md#q16) | DR 戦略の選択 | RTO 5 分で、切り替え後すぐに一部のリクエストを処理したいと考えています。全量の容量を平時に持つ… |
| [resilience 問17](../../exercises/resilience.md#q17) | DR 戦略の選択 | 2 つのリージョンの両方で常にリクエストを処理し、どちらかが落ちても RTO と RPO をほぼゼロ… |
| [resilience 問18](../../exercises/resilience.md#q18) | 不変インフラ | 不変インフラの考え方に合う更新を選んでください。（2つ選択） |
| [resilience 問19](../../exercises/resilience.md#q19) | 不変インフラ | CloudFormation で作った環境で、誰かが SG を手で変更しました。スタックとの差を見つ… |
| [resilience 問20](../../exercises/resilience.md#q20) | 不変インフラ | S3 バケットの暗号化が外れたら自動で直します。組織の標準として非準拠を検出して修復します。どの組み… |
| [resilience 問21](../../exercises/resilience.md#q21) | クォータとスロットリング | EC2 のフェイルオーバーの訓練で、DR リージョンの台数を増やせず InstanceLimitEx… |
| [resilience 問22](../../exercises/resilience.md#q22) | クォータとスロットリング | クォータの使用率が 80% に達したら通知します。どの仕組みを使いますか。 |
| [resilience 問23](../../exercises/resilience.md#q23) | クォータとスロットリング | 1 つの Lambda 関数が同時実行を使い切り、重要な別の関数がスロットリングされました。重要な関… |
| [resilience 問24](../../exercises/resilience.md#q24) | 可視性とメトリクス | マイクロサービスのリクエストのうち、どのサービスで遅くなっているかをたどります。何を使いますか。 |
| [resilience 問25](../../exercises/resilience.md#q25) | 可視性とメトリクス | 業務要件は「注文の処理が 5 分以上遅れないこと」です。ワーカーは SQS を読みます。どのメトリク… |
| [resilience 問26](../../exercises/resilience.md#q26) | 可視性とメトリクス | 応答時間の要件を「99% のリクエストが 1 秒以内」と定めました。ALB の TargetResp… |
| [resilience 問27](../../exercises/resilience.md#q27) | レガシーアプリ | アプリのセッションがサーバーのメモリにあり、コードを変更できません。ALB の後ろで複数台に分けます… |
| [resilience 問28](../../exercises/resilience.md#q28) | レガシーアプリ | 1 台でしか動かないライセンスのアプリです。インスタンスや AZ の障害で自動で置き換えたいと考えて… |
| [resilience 問29](../../exercises/resilience.md#q29) | レガシーアプリ | 古いアプリは固定 IP を許可リストに書いた顧客から接続を受けます。アプリは TCP のみで、変更で… |

<!-- questions:end -->

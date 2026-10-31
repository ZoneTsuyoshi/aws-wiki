# 分野3: MTU と性能の最適化

MTU、スループット、インターフェイス、サブネット、費用の最適化を問います。数値を覚える項目が多いページです。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [パケットサイズ](../../domain3.md#t3-2-mtu) | VPC のパケットサイズの不一致の解決 |
| [フレームサイズ](../../domain3.md#t3-3-frames) | 接続の種類ごとのフレームサイズの最適化、接続の種類ごとのジャンボフレームの構成 |
| [スループット](../../domain3.md#t3-3-throughput) | スループットの最適化 |
| [インターフェイス](../../domain3.md#t3-3-interfaces) | ネットワークインターフェイスの種類、性能に合うインターフェイスの選択（ENI、ENA、EFA） |
| [サブネット](../../domain3.md#t3-3-subnets) | VPC サブネットの最適化、Auto Scaling に合わせたサブネットの更新と最適化、IP の枯渇を防ぐサブネットの更新（セカンダリ CIDR） |
| [費用の低い接続](../../domain3.md#t3-3-cost) | VPC とオンプレミスの間の費用の低い接続 |

## 学習の順番 {#study-order}

1. [MTU とジャンボフレーム](../../../../services/network-connectivity.md#mtu): 経路ごとの MTU を表で覚えます。
2. [PMTUD とトラブルシューティング](../../../../services/network-connectivity.md#pmtud): PMTUD が働かない経路を確認します。
3. [トンネル](../../../../services/network-connectivity.md#vpn-tunnels): VPN の帯域を確認します。
4. [プレイスメントグループ](../../../../services/operations.md#placement-groups): クラスター配置と EFA の組み合わせを押さえます。
5. [VPC の CIDR](../../../../services/network-connectivity.md#vpc-cidr): セカンダリ CIDR の制限を確認します。
6. [データ転送の費用](../../../../services/cost-management.md#data-transfer): 接続ごとの料金の特徴を整理します。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| DX プライベート VIF | 1500 または 9001 | 公開 VIF と VPN はジャンボ不可 |
| DX トランジット VIF | 1500 または 8500 | 変更で最大 30 秒の中断 |
| シングルフロー | 5 Gbps | ENA Express で最大 25 Gbps |
| サブネットの予約 | 5 個 | `/24` で 251 個 |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 大きなパケットだけ止まる | MTU、ICMP、MSS |
| MPI の HPC ジョブ | EFA とクラスタープレイスメントグループ |
| IP が枯渇 | セカンダリ CIDR と新しいサブネット |
| 少量で短期 | VPN |
| 送信が多く安定 | DX |

## 引っかかりやすい点 {#traps}

- MSS クランプは TCP だけです。
- EFA の通信はルーティングできず、AZ も VPC も越えられません。
- サブネットの CIDR は変更できません。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [performance 問1](../../exercises/performance.md#q1) | パケットサイズ | EC2 から Transit Gateway と Site-to-Site VPN を経由してオンプ… |
| [performance 問2](../../exercises/performance.md#q2) | パケットサイズ | VPC 内の EC2 とインターネットの間で、大きな応答だけが返ってきません。ICMP の Type… |
| [performance 問3](../../exercises/performance.md#q3) | パケットサイズ | EC2 が VPC 内の通信で 9001 を使いつつ、DX 経由のオンプレミスへの通信だけで問題が出… |
| [performance 問4](../../exercises/performance.md#q4) | パケットサイズ | DF を立てて ping で確認します。経路は Transit Gateway の VPC アタッチ… |
| [performance 問5](../../exercises/performance.md#q5) | フレームサイズ | トランジット VIF のジャンボフレームを有効にします。既存の接続はまだジャンボに対応していません。… |
| [performance 問6](../../exercises/performance.md#q6) | フレームサイズ | DX のプライベート VIF の MTU を 9001 にしましたが、VPC の EC2 からの t… |
| [performance 問7](../../exercises/performance.md#q7) | フレームサイズ | ハイブリッドと VPC 間の経路で、ジャンボフレームの適用範囲を見直しています。接続の種類と MTU… |
| [performance 問8](../../exercises/performance.md#q8) | スループット | 同じ AZ の 2 台の EC2 の間で、アプリの 1 つの TCP 接続が 5 Gbps で頭打ち… |
| [performance 問9](../../exercises/performance.md#q9) | スループット | VPC とオンプレミスの間で 8 Gbps のスループットが必要です。DX はなく、VPN を使いま… |
| [performance 問10](../../exercises/performance.md#q10) | スループット | 16 vCPU の EC2 で、短時間は高い帯域が出ますが、数分で下がります。インスタンスの仕様は「… |
| [performance 問11](../../exercises/performance.md#q11) | インターフェイス | 緊密に結合した MPI の HPC ジョブを実行します。ノード間の遅延が最大の課題です。すべて 1 … |
| [performance 問12](../../exercises/performance.md#q12) | インターフェイス | EFA を使う ML のトレーニングで、一部のノードを別の AZ に置いて高可用性を確保する提案があ… |
| [performance 問13](../../exercises/performance.md#q13) | インターフェイス | EC2 に別のサブネットへの足を持たせて、管理ネットワークの通信を分離します。性能の要件は特にありま… |
| [performance 問14](../../exercises/performance.md#q14) | インターフェイス | インスタンスのネットワークの上限に当たっているか調べます。ethtool -S の統計で、接続追跡の… |
| [performance 問15](../../exercises/performance.md#q15) | サブネット | VPC の CIDR が 10.0.0.0/16 で、サブネットの IP が枯渇してきました。VPC… |
| [performance 問16](../../exercises/performance.md#q16) | サブネット | Auto Scaling グループが /24 のサブネットを 2 つ使っています。最大で AZ あた… |
| [performance 問17](../../exercises/performance.md#q17) | サブネット | 複数のアカウントで、IP の枯渇を事前に見つけ、重複しない CIDR を配りたいと考えています。最も… |
| [performance 問18](../../exercises/performance.md#q18) | 費用の低い接続 | 毎月 50 TB の送信があるオンプレミスとの接続を選びます。帯域は安定していて、今後も継続します。… |
| [performance 問19](../../exercises/performance.md#q19) | 費用の低い接続 | 同じリージョンの 2 つの VPC の間で、大量のデータを定常的に転送しています。今は Transi… |
| [performance 問20](../../exercises/performance.md#q20) | 費用の低い接続 | AWS のネットワーク費用が想定より大きいので、原因を調べます。データ転送、NAT、Transit … |

<!-- questions:end -->

# 分野2: VPC Resolver とハイブリッド DNS

ハイブリッドの DNS の実装の手順と症状を問います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [名前解決](../../domain2.md#t2-1-dns) | DNS（条件付き転送、ホストゾーン、リゾルバー）、既存のオンプレミスの名前解決との接続 |
| [名前解決](../../domain2.md#t2-2-name-resolution) | ホストとサービスの名前解決 |
| [名前解決でハイブリッド接続](../../domain2.md#t2-2-dns-hybrid) | ハイブリッド接続を成立させる DNS の構成 |
| [エンドポイント](../../domain2.md#t2-3-endpoints) | インバウンド、アウトバウンドの要件と実装、ハイブリッドの DNS の構成 |
| [共有と構成](../../domain2.md#t2-3-sharing) | アカウント間の DNS の共有（RAM）、集中型、分散型の DNS の構成 |
| [監視とログ](../../domain2.md#t2-3-logging) | Route 53 の監視とログの構成 |

## 学習の順番 {#study-order}

1. [エンドポイント](../../../../services/network-connectivity.md#resolver-endpoints): SG、IP、VPC の条件を確認します。
2. [転送ルール](../../../../services/network-connectivity.md#resolver-rules): ルールの関連付けと共有を確認します。
3. [ハイブリッド DNS](../../../../services/network-connectivity.md#hybrid-dns): 共有サービス VPC の手順を覚えます。
4. [プライベートホストゾーン](../../../../services/network-connectivity.md#private-hosted-zones): 別のアカウントとの関連付けの手順を押さえます。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| インバウンドの SG | 受信の TCP と UDP の 53 | アウトバウンドは送信 |
| エンドポイントの IP | API では最低 2 個 | 2 つの AZ を推奨 |
| PHZ の関連付け | ゾーンあたりの VPC の数に上限あり | 超えるなら Profiles |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| オンプレミスから VPC+2 へ転送 | 非対応。インバウンドエンドポイントへ |
| 多数の VPC へ DNS の設定を一括で | Route 53 Profiles |
| 動的に増減するサービスの発見 | AWS Cloud Map |

## 引っかかりやすい点 {#traps}

- 共有されたルールは、共有先で VPC に関連付けて初めて効きます。
- 独自の DNS サーバーを使う VPC では、PHZ の問い合わせを VPC+2 へ転送します。
- 別のアカウントの VPC との関連付けはコンソールではできません。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [resolver 問8](../../exercises/resolver.md#q8) | 名前解決 | オンプレミスの DNS で aws.example.com を AWS へ転送しています。現在は V… |
| [resolver 問9](../../exercises/resolver.md#q9) | 名前解決 | Forward ルールのターゲットとしてオンプレミスの DNS を 3 台指定しました。解決はできま… |
| [resolver 問10](../../exercises/resolver.md#q10) | 名前解決 | VPC からオンプレミスの corp.example.com を引くために、アウトバウンドエンドポイ… |
| [resolver 問11](../../exercises/resolver.md#q11) | 名前解決 | ECS のタスクが頻繁に増減するマイクロサービスで、呼び出し側は API で正常なインスタンスを取得… |
| [resolver 問12](../../exercises/resolver.md#q12) | 名前解決 | 2 つの VPC を接続しています。VPC A の EC2 から VPC B の EC2 の公開 D… |
| [resolver 問13](../../exercises/resolver.md#q13) | 名前解決 | 固定の名前 db.internal.example.com を、複数の VPC の EC2 から解決… |
| [resolver 問14](../../exercises/resolver.md#q14) | 名前解決でハイブリッド接続 | 複数のアカウントの VPC からオンプレミスの名前を解決でき、オンプレミスから各 VPC の PHZ… |
| [resolver 問15](../../exercises/resolver.md#q15) | 名前解決でハイブリッド接続 | Forward ルールを RAM で組織へ共有しました。新しいアカウントの EC2 からオンプレミス… |
| [resolver 問16](../../exercises/resolver.md#q16) | 名前解決でハイブリッド接続 | ある VPC が独自の DNS サーバー（EC2）を DHCP オプションセットで使っています。この… |
| [resolver 問17](../../exercises/resolver.md#q17) | エンドポイント | オンプレミスからインバウンドエンドポイントを使って PHZ の名前を解決します。ネットワークの経路は… |
| [resolver 問18](../../exercises/resolver.md#q18) | エンドポイント | アウトバウンドエンドポイントを作成します。自社で所有する VPC に、既定のテナンシーのものと専有テ… |
| [resolver 問19](../../exercises/resolver.md#q19) | エンドポイント | VPC からオンプレミスの example.com を解決する Forward ルールを使っています… |
| [resolver 問20](../../exercises/resolver.md#q20) | 共有と構成 | アカウント A の PHZ を、アカウント B の VPC に関連付けます。コンソールの VPC の… |
| [resolver 問21](../../exercises/resolver.md#q21) | 共有と構成 | 1,000 個の VPC に、PHZ、Resolver ルール、DNS Firewall のルールグ… |
| [resolver 問22](../../exercises/resolver.md#q22) | 共有と構成 | DNS エンドポイントを共有サービス VPC に集約する案と、VPC ごとに置く案を比較しています。… |
| [resolver 問23](../../exercises/resolver.md#q23) | 監視とログ | 公開ホストゾーンのクエリログを有効にしようとしたところ、権限のエラーで失敗しました。ロググループは … |
| [resolver 問24](../../exercises/resolver.md#q24) | 監視とログ | 組織の VPC の DNS の異常を調べます。応答コード NXDOMAIN や SERVFAIL の… |
| [resolver 問25](../../exercises/resolver.md#q25) | 監視とログ | Route 53 のヘルスチェックの異常を、運用チームへ自動で通知したいと考えています。追加のツール… |

<!-- questions:end -->

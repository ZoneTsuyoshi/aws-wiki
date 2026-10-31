# 分野3: グローバルインフラストラクチャ

リージョン、AZ、エッジロケーションの関係と、何に備えてどこに置くかを問います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [リージョン、AZ、エッジロケーションの関係](../../domain3.md#t3-2-components) | 3 つの関係とリージョンの選び方 |
| [複数 AZ による高可用性](../../domain3.md#t3-2-ha) | 複数 AZ の構成 |
| [AZ は単一障害点を共有しない](../../domain3.md#t3-2-az-isolation) | 単一障害点を共有しない |
| [複数リージョンを使う場面](../../domain3.md#t3-2-multi-region) | 災害復旧、低遅延、データ主権 |
| [エッジロケーションの利点](../../domain3.md#t3-2-edge) | 遅延の削減 |

## 学習の順番 {#study-order}

1. [グローバルインフラストラクチャ](../../../../services/cloud-foundations.md#global-infrastructure): 全体の図と表を確認します。
2. [リージョン](../../../../services/cloud-foundations.md#regions): リージョンを選ぶ 4 つの観点を覚えます。
3. [アベイラビリティーゾーン](../../../../services/cloud-foundations.md#availability-zones): AZ の分離を確認します。
4. [高可用性のための Auto Scaling](../../../../services/resilience.md#auto-scaling-ha)と[リードレプリカと Multi-AZ](../../../../services/databases.md#read-replicas): 複数 AZ の構成の例を確認します。
5. [エッジロケーション](../../../../services/cloud-foundations.md#edge-locations)と[Outposts](../../../../services/cloud-foundations.md#outposts): 他の場所との違いを確認します。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| リージョンあたりの AZ | 3 つ以上 | すべてのリージョン |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 1 つの AZ が止まっても続ける | 複数 AZ とロードバランサー |
| データベースの可用性を上げる | RDS の Multi-AZ |
| リージョン全体の障害に備える | 複数リージョン |
| 欧州と日本の利用者に低遅延で届ける | それぞれのリージョンに置く |
| 国内にデータを置く規制 | その国のリージョン |
| 自社施設で AWS の API を使う | AWS Outposts |
| 静的なコンテンツを速く届ける | CloudFront とエッジロケーション |

## 引っかかりやすい点 {#traps}

- AZ の障害には複数 AZ が基本です。複数リージョンは、それで足りないときに使います。
- エッジロケーションは利用者が個別に配置するものではありません。
- 1 つの AZ に台数を増やしても、その AZ の障害には備えられません。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [global-infrastructure 問1](../../exercises/global-infrastructure.md#q1) | リージョン、AZ、エッジロケーションの関係 | リージョンと AZ の関係の説明として正しいものはどれですか。 |
| [global-infrastructure 問2](../../exercises/global-infrastructure.md#q2) | リージョン、AZ、エッジロケーションの関係 | リージョンを選ぶときの観点として適切なものはどれですか。（2つ選択） |
| [global-infrastructure 問3](../../exercises/global-infrastructure.md#q3) | リージョン、AZ、エッジロケーションの関係 | エッジロケーションの説明として正しいものはどれですか。 |
| [global-infrastructure 問4](../../exercises/global-infrastructure.md#q4) | リージョン、AZ、エッジロケーションの関係 | 自社のデータセンターで、AWS と同じ API やツールを使いたいと考えています。最も適切なものはど… |
| [global-infrastructure 問5](../../exercises/global-infrastructure.md#q5) | 複数 AZ による高可用性 | 1 つの AZ が止まっても Web アプリを動かし続けたいと考えています。最も基本的な構成はどれで… |
| [global-infrastructure 問6](../../exercises/global-infrastructure.md#q6) | 複数 AZ による高可用性 | データベースを別の AZ のスタンバイに切り替えられるようにして、可用性を高めたいと考えています。最… |
| [global-infrastructure 問7](../../exercises/global-infrastructure.md#q7) | 複数 AZ による高可用性 | 複数の AZ に配置する理由として最も適切なものはどれですか。 |
| [global-infrastructure 問8](../../exercises/global-infrastructure.md#q8) | AZ は単一障害点を共有しない | AZ の設計の説明として正しいものはどれですか。 |
| [global-infrastructure 問9](../../exercises/global-infrastructure.md#q9) | AZ は単一障害点を共有しない | 全インスタンスを 1 つの AZ に置いています。この構成の問題点はどれですか。 |
| [global-infrastructure 問10](../../exercises/global-infrastructure.md#q10) | AZ は単一障害点を共有しない | 「AZ の障害に備えるために、別の AZ にも配置する」という対策が有効な理由はどれですか。 |
| [global-infrastructure 問11](../../exercises/global-infrastructure.md#q11) | 複数リージョンを使う場面 | 複数のリージョンを使う理由として適切なものはどれですか。（2つ選択） |
| [global-infrastructure 問12](../../exercises/global-infrastructure.md#q12) | 複数リージョンを使う場面 | 欧州と日本の利用者に、どちらも低い遅延でアプリを提供したいと考えています。最も適切な構成はどれですか… |
| [global-infrastructure 問13](../../exercises/global-infrastructure.md#q13) | 複数リージョンを使う場面 | 大規模な災害でも業務を止めないために、別のリージョンでも動かせるようにしました。これはどの目的の例で… |
| [global-infrastructure 問14](../../exercises/global-infrastructure.md#q14) | エッジロケーションの利点 | エッジロケーションの利点の説明として正しいものはどれですか。 |
| [global-infrastructure 問15](../../exercises/global-infrastructure.md#q15) | エッジロケーションの利点 | エッジロケーションの使い方の説明として正しいものはどれですか。 |
| [global-infrastructure 問16](../../exercises/global-infrastructure.md#q16) | エッジロケーションの利点 | エッジロケーションを使うサービスはどれですか。（2つ選択） |

<!-- questions:end -->

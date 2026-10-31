# 分野3: データ転送とネットワーク費用

どの経路に料金がかかるかを読み取り、可用性や要件を保ったまま費用を減らす判断を問います。多くの問題は、明細の症状から原因を見分ける形です。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [3.2.1](../../domain3.md#skill-3-2-1) | コンテンツ配信とキャッシュ戦略 |
| [3.2.2](../../domain3.md#skill-3-2-2) | プライベート接続と AZ、リージョンの転送費用 |
| [3.2.3](../../domain3.md#skill-3-2-3) | コストを考えたマルチリージョンのレプリケーション |
| [3.2.4](../../domain3.md#skill-3-2-4) | 費用対効果の高いネットワーク |
| [3.2.5](../../domain3.md#skill-3-2-5) | AI と ML のデータ転送費用 |

## 学習の順番 {#study-order}

1. [データ転送の費用](../../../../services/cost-management.md#data-transfer): 経路ごとの有料と無料を表で覚えます。
2. [キャッシュキーとポリシー](../../../../services/networking.md#cache-keys)と[オリジンの設定](../../../../services/networking.md#origin-settings): キーとオリジンへ渡す値を分ける理由をつかみます。
3. [VPC エンドポイントと PrivateLink](../../../../services/networking.md#vpc-endpoints)と [NAT ゲートウェイ](../../../../services/network-connectivity.md#nat-gateway): NAT の費用を減らす順序を確認します。
4. [レプリケーション](../../../../services/s3.md#replication)と[グローバルテーブル](../../../../services/dynamodb.md#global-tables): フィルターと複製先のクラス、複製の書き込みの課金を押さえます。
5. [Aurora グローバルデータベース](../../../../services/databases.md#aurora-global-database)と[リージョン間コピー](../../../../services/resilience.md#backup-cross-region): RPO に応じて複製とコピーを選びます。
6. [VPC 同士の接続](../../../../services/network-connectivity.md#choosing-multi-vpc)、[VPC ピアリング](../../../../services/network-connectivity.md#vpc-peering)、[Transit Gateway](../../../../services/network-connectivity.md#transit-gateway): 課金の違いを、通信量と VPC の数で比べます。
7. [Direct Connect](../../../../services/network-connectivity.md#direct-connect): 定常の大量通信と、VPN のバックアップを確認します。
8. [推論の容量とプロファイル](../../../../services/genai-apps.md#inference-profiles): 地理的プロファイルとグローバルプロファイルの違いを覚えます。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| インターネットから AWS へ | 無料 | 送信に料金がかかる |
| 同じ AZ 内の転送 | 無料 | AZ 間は送受信の両方に課金 |
| ゲートウェイエンドポイント | 追加料金なし | S3 と DynamoDB |
| zone-aware routing の条件 | エンドポイントが AZ 数の 2 倍以上 | 3 AZ なら 6 つ。下回るとラウンドロビン |
| S3 RTC | 新しいオブジェクトの 99.9% を 15 分以内 | 不要なら付けない |
| グローバルプロファイル | 約 10% 安い | モデルによる。ルーティングの追加料金はなし |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 世界の利用者が同じ変換結果を求め、オリジンの帯域が細い | Origin Shield を、オリジンに近いリージョンで有効にする |
| 動的、キャッシュしにくい、まれにしか要求されない | Origin Shield は効かない |
| 応答は変わらないが、オリジンは Cookie を必要とする | キーから外し、オリジンリクエストポリシーで渡す |
| S3 と DynamoDB への NAT の費用が高い | ゲートウェイエンドポイント |
| 1 つの NAT に全 AZ の通信が集まる | AZ ごとに NAT を置く。可用性も上がる |
| RPO が 24 時間なのに複製している | AWS Backup のコピーへ見直す |
| 2 つの VPC の間だけ大量に流れる | その区間だけピアリングを足す |
| 通信の少ない多数の VPC の NAT | 中央へ集約。通信の多い VPC は残す |
| 同じ組織で同じ VPC を使える | VPC 共有 |
| データレジデンシーの要件がある推論 | 地理的プロファイル |

## 引っかかりやすい点 {#traps}

- ライブレプリケーションは、設定の前からあるオブジェクトを複製しません。既存分は Batch Replication です。
- DynamoDB のリザーブドキャパシティは、複製の書き込み（rWCU）に購入できません。
- Transit Gateway は別のものにしてもデータ処理料金がかかります。
- NAT を中央へ集めると時間課金は減りますが、データ処理料金が増えます。
- Provisioned Throughput は推論プロファイルに対応しません。
- クロスリージョン推論の処理リージョンは、CloudTrail の `additionalEventData.inferenceRegion` で確認します。
- Savings Plans はデータ転送の費用を割り引きません。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [data-transfer 問1](../../exercises/data-transfer.md#q1) | 3.2.1 | ある出版社は、画像をその場で変換するオンプレミスのサーバーをオリジンにして、CloudFront で… |
| [data-transfer 問2](../../exercises/data-transfer.md#q2) | 3.2.1 | ある EC サイトの CloudFront は、すべての Cookie をキャッシュキーに含めていま… |
| [data-transfer 問3](../../exercises/data-transfer.md#q3) | 3.2.1 | あるメディア企業の CloudFront には、3 つのオリジンがあります。オリジン X は利用者ご… |
| [data-transfer 問4](../../exercises/data-transfer.md#q4) | 3.2.2 | ある会社のプライベートサブネットのアプリは、NAT ゲートウェイを経由して通信しています。月あたりの… |
| [data-transfer 問5](../../exercises/data-transfer.md#q5) | 3.2.2 | ある Web アプリは 3 つの AZ のプライベートサブネットで動いていますが、NAT ゲートウェ… |
| [data-transfer 問6](../../exercises/data-transfer.md#q6) | 3.2.2 | ある会社は、ECS Service Connect で通信するマイクロサービスを 3 つの AZ で… |
| [data-transfer 問7](../../exercises/data-transfer.md#q7) | 3.2.2 | ある分析チームは、夜間に Spark のバッチを EMR で実行しています。ジョブは失敗しても次の時… |
| [data-transfer 問8](../../exercises/data-transfer.md#q8) | 3.2.3 | ある保険会社は、S3 バケットに 500 TB のデータを持っています。規制で別のリージョンへの保管… |
| [data-transfer 問9](../../exercises/data-transfer.md#q9) | 3.2.3 | ある会社の受発注システムは、DynamoDB のグローバルテーブルと Aurora グローバルデータ… |
| [data-transfer 問10](../../exercises/data-transfer.md#q10) | 3.2.3 | ある会社は、Aurora グローバルデータベースのセカンダリリージョンに、プライマリと同じ大きさのイ… |
| [data-transfer 問11](../../exercises/data-transfer.md#q11) | 3.2.3 | ある会社は、DynamoDB の MREC グローバルテーブルを 3 つのリージョンで使っています。… |
| [data-transfer 問12](../../exercises/data-transfer.md#q12) | 3.2.4 | ある会社は、1 つのリージョンの 40 個の VPC を Transit Gateway でつないで… |
| [data-transfer 問13](../../exercises/data-transfer.md#q13) | 3.2.4 | ある会社には 60 個の VPC があり、Transit Gateway ですでに接続されています。… |
| [data-transfer 問14](../../exercises/data-transfer.md#q14) | 3.2.4 | ある会社は、同じ組織の 30 のアカウントで動くアプリを同じリージョンに置いています。アプリ間の通信… |
| [data-transfer 問15](../../exercises/data-transfer.md#q15) | 3.2.4 | ある会社は、AWS からオンプレミスへ毎月 80 TB を定常的に送っています。現在は Site-t… |
| [data-transfer 問16](../../exercises/data-transfer.md#q16) | 3.2.5 | ある銀行は、EU の顧客の文書を Bedrock で要約します。規制により、処理は EU の中にとど… |
| [data-transfer 問17](../../exercises/data-transfer.md#q17) | 3.2.5 | ある会社のアプリは東京リージョンから APAC の地理的プロファイルで Bedrock を呼び、一部… |
| [data-transfer 問18](../../exercises/data-transfer.md#q18) | 3.2.5 | ある会社は、us-west-2 の S3 に 10 TB の文書を保管しています。それを読むパイプラ… |

<!-- questions:end -->

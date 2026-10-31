# 分野3: 高可用性

条件を満たす中で最も安い構成を選ぶ力を問います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [Multi-AZ と Multi-Region](../../domain3.md#t3-1-multi-az-region) | Multi-AZ と Multi-Region のデプロイ、高可用性を実現する手法 |
| [SLA](../../domain3.md#t3-1-sla) | SLA |
| [ビジネス要件](../../domain3.md#t3-1-business-requirements) | ビジネス要件から技術的な要件へ |
| [単一障害点](../../domain3.md#t3-1-spof) | 単一障害点の特定と解消 |
| [ダウンタイムを抑える](../../domain3.md#t3-1-minimize-downtime) | ダウンタイムを抑えるアプリの構成 |

## 学習の順番 {#study-order}

1. [サービスごとの Multi-AZ と Multi-Region](../../../../services/resilience.md#patterns-by-service): サービスごとの Multi-AZ と Multi-Region を確認します。
2. [静的安定性](../../../../services/resilience.md#static-stability): AZ を失っても足りる台数の計算を覚えます。
3. [RTO と RPO](../../../../services/resilience.md#rto-rpo): ビジネスの言葉を数値に置き換えます。
4. [NAT ゲートウェイ](../../../../services/network-connectivity.md#nat-gateway): AZ ごとに作る理由を理解します。
5. [フェイルオーバーはデータプレーンで](../../../../services/resilience.md#failover-data-plane): コントロールプレーンに頼らない切り替えを確認します。
6. [Global Accelerator との比較](../../../../services/resilience.md#global-accelerator): 固定 IP と DNS に頼らない切り替えを押さえます。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| 直列の稼働率（99.9% が 3 つ） | 約 99.7% | 掛け算で下がる |
| 並列の稼働率（99.9% が 2 つ） | 99.9999% | 1 - 故障率の掛け算 |
| 静的安定性（必要 12 台、3 AZ） | 18 台 | 12 ÷ (3 - 1) × 3 |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 「1 件も失えない」 | RPO 0、同期レプリケーション |
| AZ の障害を素早く避ける | ARC のゾーンシフト |
| フェイルオーバーで接続が切れる | RDS Proxy |
| サーバーにセッションがある | ElastiCache か DynamoDB へ移す |
| 目標の RTO と RPO を評価する | Resilience Hub |

## 引っかかりやすい点 {#traps}

- DynamoDB と Lambda は標準で複数 AZ です。
- SLA は実際の稼働を保証しません。補償はサービスクレジットです。
- NAT ゲートウェイは AZ のリソースです。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [high-availability 問1](../../exercises/high-availability.md#q1) | Multi-AZ と Multi-Region | 社内の業務システムは東京リージョンだけで動かす規制があります。要件は AZ の障害でも数分以内に自動… |
| [high-availability 問2](../../exercises/high-availability.md#q2) | Multi-AZ と Multi-Region | 次のサービスの可用性の設定を見直します。担当者が追加の対応を計画している中で、不要な作業はどれですか… |
| [high-availability 問3](../../exercises/high-availability.md#q3) | Multi-AZ と Multi-Region | 3 AZ で動く EC2 の Web アプリで、AZ 障害でもスケールの処理を待たずに容量を保ちます… |
| [high-availability 問4](../../exercises/high-availability.md#q4) | SLA | API のリクエストは、ALB、ECS、RDS の 3 つを順に通ります。それぞれの可用性を 99.… |
| [high-availability 問5](../../exercises/high-availability.md#q5) | SLA | 2 つのリージョンで同じ API をアクティブ/アクティブで動かします。1 リージョンの可用性を 9… |
| [high-availability 問6](../../exercises/high-availability.md#q6) | SLA | ある担当者は、利用する AWS サービスの SLA が 99.99% なので、自社の API も障害… |
| [high-availability 問7](../../exercises/high-availability.md#q7) | ビジネス要件 | 経営層の要件は次のとおりです。「決済の記録は 1 件も失えない。AZ の障害では 2 分以内に再開す… |
| [high-availability 問8](../../exercises/high-availability.md#q8) | ビジネス要件 | 小売業の経営層は、リージョンが丸ごと使えなくなったときの要件を「1 時間以内にサービスを再開し、失う… |
| [high-availability 問9](../../exercises/high-availability.md#q9) | ビジネス要件 | 複数のチームが RTO と RPO の目標を持ちます。アプリの構成を定期的に評価し、目標を満たすか、… |
| [high-availability 問10](../../exercises/high-availability.md#q10) | 単一障害点 | 3 つの AZ のプライベートサブネットが、AZ-a の NAT ゲートウェイを 1 つ共有していま… |
| [high-availability 問11](../../exercises/high-availability.md#q11) | 単一障害点 | EC2 の Web 層を増やしたところ、利用者のログイン状態が消える問題が起きました。セッションはサ… |
| [high-availability 問12](../../exercises/high-availability.md#q12) | 単一障害点 | 既存のワークロードを確認したところ、次の点が見つかりました。単一障害点を解消する変更はどれですか。（… |
| [high-availability 問13](../../exercises/high-availability.md#q13) | ダウンタイムを抑える | Aurora のフェイルオーバーで、アプリの接続が切れ、再接続が一斉に発生してエラーが数分続きます。… |
| [high-availability 問14](../../exercises/high-availability.md#q14) | ダウンタイムを抑える | リージョン障害時の切り替えの手順は、担当者がコンソールから Route 53 のレコードを変更する内… |
| [high-availability 問15](../../exercises/high-availability.md#q15) | ダウンタイムを抑える | 取引先がファイアウォールの許可リストに IP を登録するので、固定の IP が必要です。別のリージョ… |

<!-- questions:end -->

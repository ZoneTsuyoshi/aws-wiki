# 分野2: 企業システムとの統合

基幹システムや SaaS に、影響を波及させずに生成 AI を組み込みます。データの所在の判断もここで扱います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [2.3.1](../../domain2.md#skill-2-3-1) | 既存の企業環境との接続 |
| [2.3.2](../../domain2.md#skill-2-3-2) | 既存のアプリに生成 AI を組み込む |
| [2.3.4](../../domain2.md#skill-2-3-4) | 法域をまたぐデータの準拠 |
| [2.5.2](../../domain2.md#skill-2-5-2) | 利用しやすい AI のインターフェイス |
| [2.5.3](../../domain2.md#skill-2-5-3) | 業務システムの強化 |
| [2.5.4](../../domain2.md#skill-2-5-4) | 開発者の生産性を高める |

## 学習の順番 {#study-order}

1. [非同期と統合](../../../../services/genai-apps.md#async-integration)と[疎結合](../../../../services/messaging.md#coupling): キューを挟む理由を理解します。
2. [変換](../../../../services/api-gateway.md#transformations)と[冪等性](../../../../services/sdk-resilience.md#idempotency): アダプターと Webhook の設計を押さえます。
3. [Outposts](../../../../services/network-connectivity.md#outposts)、[Wavelength](../../../../services/network-connectivity.md#wavelength)、[VPC エンドポイント](../../../../services/ai.md#privatelink): それぞれが守るものの違いを確認します。
4. [Amplify](../../../../services/cicd.md#amplify)と [Bedrock Flows](../../../../services/genai-apps.md#flows): UI と流れの構築を選べるようにします。
5. [Connect](../../../../services/other-services.md#connect)と [Lex](../../../../services/ai-managed-services.md#lex): コンタクトセンターの組み合わせを理解します。
6. [AI 開発ツール](../../../../services/ai.md#ai-dev-tools)と [Q Developer](../../../../services/ai.md#q-developer): Kiro への移行の状況を確認します。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| Q Developer の新規停止 | 2026-05-15 | IDE 向け。Free Tier と新規サブスクリプション |
| IDE プラグインのサポート終了 | 2027-04-30 | コンソールとチャットアプリは影響なし |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 基幹システムに影響させない | SQS で受けて非同期に |
| 変更できない XML の API | API Gateway の変換 |
| Webhook で再送がある | すぐに応答して冪等に処理 |
| 敷地の外に出せない | Outposts で処理して匿名化 |
| 端末の近くで超低遅延 | Wavelength |
| 文書、写真、音声を一括で構造化 | Bedrock Data Automation |

## 引っかかりやすい点 {#traps}

- PrivateLink は経路を守るだけで、処理のリージョンは別の話です。
- 同じ VPC でも、別の Wavelength Zone のインスタンスとは通信できません。
- AI の出力もレビューとテストを通します。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [enterprise-integration 問1](../../exercises/enterprise-integration.md#q1) | 2.3.1 | 基幹の受注システムから、受注ごとに FM で備考を分類します。FM の遅延やスロットリングで基幹シス… |
| [enterprise-integration 問2](../../exercises/enterprise-integration.md#q2) | 2.3.1 | 古い業務システムは XML の API しか話せず、変更もできません。このシステムから新しい生成 A… |
| [enterprise-integration 問3](../../exercises/enterprise-integration.md#q3) | 2.3.1 | 次の 3 つのデータを生成 AI の参照データと揃えます。(a) DynamoDB の商品情報の変更… |
| [enterprise-integration 問4](../../exercises/enterprise-integration.md#q4) | 2.3.2 | 外部の SaaS から Webhook で通知を受け、内容を FM で要約して社内に投稿します。Sa… |
| [enterprise-integration 問5](../../exercises/enterprise-integration.md#q5) | 2.3.2 | 受注、返品、問い合わせの各マイクロサービスが業務イベントを発行します。返品イベントのときだけ FM … |
| [enterprise-integration 問6](../../exercises/enterprise-integration.md#q6) | 2.3.2 | 既存の Web アプリに「画面の内容を要約」のボタンを追加します。利用者はその場で結果を見ます。アプ… |
| [enterprise-integration 問7](../../exercises/enterprise-integration.md#q7) | 2.3.4 | 欧州の工場に、敷地の外へ出せない検査記録があります。一部の匿名化された内容なら EU のリージョンで… |
| [enterprise-integration 問8](../../exercises/enterprise-integration.md#q8) | 2.3.4 | 5G の端末からの映像を、数ミリ秒の遅延で小さなモデルに推論させます。処理は通信事業者のネットワーク… |
| [enterprise-integration 問9](../../exercises/enterprise-integration.md#q9) | 2.3.4 | 監査で「データが国外に出ないことを PrivateLink で保証している」という説明が指摘を受けま… |
| [enterprise-integration 問10](../../exercises/enterprise-integration.md#q10) | 2.5.2 | スタートアップが生成 AI のチャットの Web 画面を数日で公開します。認証とホスティング、Bed… |
| [enterprise-integration 問11](../../exercises/enterprise-integration.md#q11) | 2.5.2 | フロントエンドとバックエンドのチームが別で、生成 AI の API の開発を同時に始めます。先に契約… |
| [enterprise-integration 問12](../../exercises/enterprise-integration.md#q12) | 2.5.2 | 業務部門の担当者が、コードを書かずに「検索して要約するプロンプトの流れ」を組み、完成した流れをアプリ… |
| [enterprise-integration 問13](../../exercises/enterprise-integration.md#q13) | 2.5.3 | 営業担当が顧客を開くと、CRM の画面に最新の取引の要約が出るようにします。CRM は SaaS で… |
| [enterprise-integration 問14](../../exercises/enterprise-integration.md#q14) | 2.5.3 | 保険の請求で、書類、写真、通話の録音が混在して届きます。プロンプトを細かく調整せずに構造化データにし… |
| [enterprise-integration 問15](../../exercises/enterprise-integration.md#q15) | 2.5.3 | コンタクトセンターの音声の自動応答で、定型の手続きはボットの意図で確実に処理し、それ以外の質問は社内… |
| [enterprise-integration 問16](../../exercises/enterprise-integration.md#q16) | 2.5.4 | 開発チームが IDE でのコード生成とテスト作成を効率化したいと考えています。新規に Amazon … |
| [enterprise-integration 問17](../../exercises/enterprise-integration.md#q17) | 2.5.4 | AI 開発ツールで生成したコードを本番に入れる運用を決めます。生産性は上げたいものの、品質と安全性を… |
| [enterprise-integration 問18](../../exercises/enterprise-integration.md#q18) | 2.5.4 | 生成 AI の API を使う既存の Python のコードがあります。チームは、API の使い方の… |

<!-- questions:end -->

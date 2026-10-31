# 分野3: 複数リージョン

サービスごとの複製の性質と、切り替えの方法を問います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [複製と切り替え](../../domain3.md#t3-1-replication) | ステートフルなサービスの複製と切り替え |
| [リージョンをまたぐ機能](../../domain3.md#t3-1-cross-region) | リージョンをまたぐ機能の有効化 |
| [グローバルなスケール](../../domain3.md#t3-2-global) | 複数リージョンへのワークロードの配置 |

## 学習の順番 {#study-order}

1. [リードレプリカと Multi-AZ](../../../../services/databases.md#read-replicas): Multi-AZ とリードレプリカの目的の違いを確認します。
2. [Aurora グローバルデータベース](../../../../services/databases.md#aurora-global-database): スイッチオーバーとフェイルオーバーを区別します。
3. [グローバルテーブル](../../../../services/dynamodb.md#global-tables): 全リージョンの書き込みと競合の解決を押さえます。
4. [レプリケーション](../../../../services/s3.md#replication): バージョニングの条件と既存オブジェクトの扱いを確認します。
5. [オリジンフェイルオーバー](../../../../services/networking.md#origin-failover): 対象のメソッドを覚えます。
6. [ルーティングポリシー](../../../../services/networking.md#routing-policies): 位置情報とレイテンシーの違いを確認します。

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 各リージョンで読み書きする | DynamoDB グローバルテーブル |
| 書き込みは 1 か所、読み取りは各地 | Aurora Global Database |
| データを失わず計画的に移す | スイッチオーバー |
| 利用者の国でリージョンを決める | Route 53 の位置情報 |
| 固定 IP で素早く AWS に入る | Global Accelerator |

## 引っかかりやすい点 {#traps}

- レプリケーションは破損や誤削除も伝わるので、時点へ戻せるバックアップを別に持ちます。
- オリジンフェイルオーバーは GET、HEAD、OPTIONS が対象です。
- KMS キーはリージョンごとです。別リージョンのレプリカにはそのリージョンのキーを指定します。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [multi-region 問1](../../exercises/multi-region.md#q1) | 複製と切り替え | 次の説明のうち、RDS の Multi-AZ DB インスタンス構成とリードレプリカの違いを正しく述… |
| [multi-region 問2](../../exercises/multi-region.md#q2) | 複製と切り替え | 東京のプライマリと大阪のセカンダリを持つ Aurora Global Database があります。… |
| [multi-region 問3](../../exercises/multi-region.md#q3) | 複製と切り替え | S3 のデータを別のリージョンへ複製し、誤削除やランサムウェアによる破壊に備えたいと考えています。担… |
| [multi-region 問4](../../exercises/multi-region.md#q4) | リージョンをまたぐ機能 | 東京とフランクフルトで同じ Web アプリを動かし、各リージョンで低遅延に読み書きします。同じ項目の… |
| [multi-region 問5](../../exercises/multi-region.md#q5) | リージョンをまたぐ機能 | CloudFront で S3 のオリジンを 2 つのリージョンに持ちます。画像の取得はプライマリの… |
| [multi-region 問6](../../exercises/multi-region.md#q6) | リージョンをまたぐ機能 | カスタマー管理キーで暗号化された RDS の東京のインスタンスから、大阪へリードレプリカを作ります。… |
| [multi-region 問7](../../exercises/multi-region.md#q7) | グローバルなスケール | 各国の利用者を、(1) 法規によりその国のデータがあるリージョンへ必ず送る、(2) 法規の対象外のサ… |
| [multi-region 問8](../../exercises/multi-region.md#q8) | グローバルなスケール | 世界中の利用者へ配信します。(1) 動画と画像はキャッシュして配信する。(2) ゲームの UDP の… |
| [multi-region 問9](../../exercises/multi-region.md#q9) | グローバルなスケール | 同じ Web アプリを 4 つのリージョンへ展開します。読み取りは各リージョンで低遅延に行い、書き込… |
| [multi-region 問10](../../exercises/multi-region.md#q10) | リージョンをまたぐ機能 | 東京とオレゴンの S3 バケットに同じデータを置き、アプリは 1 つのエンドポイントから近いほうを使… |

<!-- questions:end -->

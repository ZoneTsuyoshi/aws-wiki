# 分野4: 回復性と事業継続

組織全体のバックアップの統制、復旧時間の実測、自己修復、ランサムウェア対策、カオスエンジニアリングを問います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [4.3.1](../../domain4.md#skill-4-3-1) | バックアップの統制と組織のポリシー |
| [4.3.2](../../domain4.md#skill-4-3-2) | フェイルオーバーテストと復旧時間の計測 |
| [4.3.3](../../domain4.md#skill-4-3-3) | 冗長性、耐障害性、自己修復 |
| [4.3.4](../../domain4.md#skill-4-3-4) | ランサムウェアと誤削除からの保護 |
| [4.3.5](../../domain4.md#skill-4-3-5) | カオスエンジニアリング |

## 学習の順番 {#study-order}

1. [AWS Backup](../../../../services/resilience.md#backup)と[アカウント間コピーと組織での管理](../../../../services/resilience.md#backup-cross-account): 両側の権限と、ポリシーの統合を確認します。
2. [復元テストと監査](../../../../services/resilience.md#backup-testing): 復元できることの確認と、方針の準拠の監査を分けて覚えます。
3. [設計のポイント](../../../../services/resilience.md#route53-design)と [Route 53 ヘルスチェック](../../../../services/networking.md#route53-health-checks): 切り替えの時間を計算し、プライベートのリソースの扱いを押さえます。
4. [Synthetics](../../../../services/operations.md#synthetics): 利用者から見た復旧の時間の測り方を確認します。
5. [高可用性のための Auto Scaling](../../../../services/resilience.md#auto-scaling-ha): 最小容量の計算と ELB ヘルスチェックを確認します。
6. [ゾーンシフトとオートシフト](../../../../services/resilience.md#arc-zonal): 練習実行と事前の容量を押さえます。
7. [疎結合と耐障害性](../../../../services/resilience.md#loose-coupling)と[グレースフルデグラデーション](../../../../services/sdk-resilience.md#graceful-degradation): 障害の波及を止める方法を確認します。
8. [ランサムウェアと誤削除の防止](../../../../services/resilience.md#immutable-compare)、[Vault Lock](../../../../services/resilience.md#vault-lock)、[論理的にエアギャップされたボールト](../../../../services/resilience.md#logically-air-gapped)、[Object Lock](../../../../services/s3.md#object-lock): 対象とモードの違いを表で覚えます。
9. [キーの無効化と削除](../../../../services/kms.md#disable-delete): 暗号化のキーも保護の対象にします。
10. [AWS Fault Injection Service](../../../../services/resilience.md#fis)と[実験テンプレート](../../../../services/resilience.md#fis-template): 実験の手順と、停止条件を確認します。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| AZ あたりの台数 | 必要な台数 ÷（AZ の数 - 1） | 3 AZ で 30 台必要なら最小 45 台 |
| Route 53 の検知 | 30 秒 × 3 回。Fast は 10 秒 × 3 回 | 切り替えの時間は検知 + TTL |
| Vault Lock の猶予期間 | 3 日以上 | 確定後は誰も変更できない |
| 継続的バックアップ | 最大 35 日 | 時点復旧 |
| KMS キーの削除の待機期間 | 7〜30 日。既定は 30 日 | 待機中は取り消せる |
| ゾーンシフトの期限 | 1 分〜3 日。延長できる | 一時的な対応 |
| 練習実行 | 約週に 1 回、約 30 分 | オートシフトに必須 |
| FIS の実験の最大時間 | 12 時間 | Cross-Region シナリオの既定は 3 時間 |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 組織全体にバックアップを強制し、OU で足す | Organizations のバックアップポリシー |
| 別アカウントへのコピーが権限のエラーになる | ロールとボールトのポリシーの両方に `backup:CopyIntoBackupVault` |
| 管理アカウントを使わずに管理する | AWS Backup の委任管理者 |
| 基準への準拠のレポートを残す | Backup Audit Manager |
| VPC 内のプライベート IP を監視して切り替える | CloudWatch アラームのヘルスチェック |
| 実際の RTO を、再現できる形で測る | FIS と Synthetics カナリア |
| アプリが 500 を返しても置き換えたい | ELB ヘルスチェックと猶予期間 |
| AZ の障害で AWS の判断で移す | ゾーンオートシフト。練習実行と事前の容量 |
| 必須でない依存先で全体が止まる | 短いタイムアウト、サーキットブレーカー、機能の縮退 |
| アカウントごと乗っ取られても別のアカウントから復元する | 論理的にエアギャップされたボールト |
| EBS スナップショットの誤削除を戻す | Recycle Bin |
| 管理者でも消せない期間を作る | コンプライアンスモードのロック |
| AZ の電源喪失をまとめて再現する | FIS の AZ Availability: Power Interruption |
| リージョン間の接続と複製を止めて試す | FIS の Cross-Region: Connectivity |

## 引っかかりやすい点 {#traps}

- AWS 管理キーのポリシーは変更できません。アカウントをまたぐコピーには、カスタマー管理キーが必要なリソースがあります。
- S3 Object Lock は削除マーカーの追加を防ぎません。一覧から消えても、保護された版は残っています。
- コンプライアンスモードの Vault Lock は、確定後は AWS も解除できません。無期限の復旧ポイントがあると費用が続きます。
- Vault Lock の最小、最大の保持は、ロック後の新しいジョブに適用されます。
- Route 53 の CloudWatch アラームのヘルスチェックは、同じアカウントのアラームだけが対象です。高解像度のメトリクスや「M out of N」のアラームには対応しません。
- Resilience Hub の推定の RTO は実測ではありません。
- FIS で止まった実験は再開できません。新しく実行します。
- `selectionMode` を `ALL` にすると全台が対象になります。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [resilience 問1](../../exercises/resilience.md#q1) | 4.3.1 | 300 のアカウントを持つ企業が、全アカウントのタグ付きリソースを「毎日、7 日保持」で保護し、Fi… |
| [resilience 問2](../../exercises/resilience.md#q2) | 4.3.1 | AWS Backup で、本番アカウントのバックアップを同じ組織のバックアップ用アカウントへコピーし… |
| [resilience 問3](../../exercises/resilience.md#q3) | 4.3.1 | RDS のスナップショットを AWS Backup で別のアカウントへコピーしたいです。RDS は … |
| [resilience 問4](../../exercises/resilience.md#q4) | 4.3.1 | セキュリティチームが、組織のバックアップを管理します。管理アカウントは使わないことが社内の規則です。… |
| [resilience 問5](../../exercises/resilience.md#q5) | 4.3.2 | 2 つのリージョンのシステムを Route 53 のフェイルオーバーで切り替えています。ヘルスチェッ… |
| [resilience 問6](../../exercises/resilience.md#q6) | 4.3.2 | プライベートホストゾーンのレコードで、VPC 内のプライベート IP にある内部 API をフェイル… |
| [resilience 問7](../../exercises/resilience.md#q7) | 4.3.2 | 監査で、AZ の障害時の RTO 5 分の実測の値を求められました。アプリは ALB、Auto Sc… |
| [resilience 問8](../../exercises/resilience.md#q8) | 4.3.3 | Web 層の処理には常に 30 台が必要です。3 つの AZ を使います。AZ の 1 つが障害にな… |
| [resilience 問9](../../exercises/resilience.md#q9) | 4.3.3 | ALB 配下の Auto Scaling グループで、アプリのプロセスが異常になると 500 を返し… |
| [resilience 問10](../../exercises/resilience.md#q10) | 4.3.3 | ALB と Auto Scaling のアプリで、AZ の障害のときに、人の操作なしで AWS の判… |
| [resilience 問11](../../exercises/resilience.md#q11) | 4.3.3 | 3 つの AZ のアプリのレビューで、次の点が見つかりました。NAT ゲートウェイは AZ-a に … |
| [resilience 問12](../../exercises/resilience.md#q12) | 4.3.3 | 商品ページは、おすすめのサービスを同期で呼びます。おすすめのサービスが遅くなると、スレッドを使い切っ… |
| [resilience 問13](../../exercises/resilience.md#q13) | 4.3.4 | ランサムウェアで本番アカウントごと乗っ取られ、バックアップのアカウントの権限も失う場合を想定します。… |
| [resilience 問14](../../exercises/resilience.md#q14) | 4.3.4 | S3 バケットはバージョニングと Object Lock のコンプライアンスモードで保護しています。… |
| [resilience 問15](../../exercises/resilience.md#q15) | 4.3.4 | EBS スナップショットについて、2 つの要件があります。運用担当者が誤って消したものは 14 日以… |
| [resilience 問16](../../exercises/resilience.md#q16) | 4.3.4 | バックアップ用のアカウントでは、すべての復旧ポイントをカスタマー管理キーで暗号化しています。Vaul… |
| [resilience 問17](../../exercises/resilience.md#q17) | 4.3.4 | 規制の対応で、ボールトに Vault Lock のコンプライアンスモードを初めて設定します。プランに… |
| [resilience 問18](../../exercises/resilience.md#q18) | 4.3.5 | FIS で本番の ECS タスクを止める実験を計画しています。要件は次のとおりです。対象は全タスクで… |
| [resilience 問19](../../exercises/resilience.md#q19) | 4.3.5 | Multi-AZ のアプリが、AZ の完全な電源喪失でも動き続けることを確かめます。EC2 と EC… |
| [resilience 問20](../../exercises/resilience.md#q20) | 4.3.5 | 初めてカオスエンジニアリングに取り組みます。経営層からは、本番に影響を与えずに学びを得て、結果を設計… |
| [resilience 問21](../../exercises/resilience.md#q21) | 4.3.5 | 2 つのリージョンのアプリが、リージョン間の通信が切れても動き続けるかを確かめます。リージョンは T… |

<!-- questions:end -->

# 分野2: ストレージの種類と耐久性

アクセスの方法と共有の有無で種類を選び、データの失い方を確認します。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [ストレージの種類](../../domain2.md#t2-1-storage-types) | ストレージの種類と特徴 |
| [ストレージの耐久性とデータの保護](../../domain2.md#t2-2-data-durability) | ストレージの選択肢と特徴、データの耐久性と可用性を確保する戦略の実装 |

## 学習の順番 {#study-order}

1. [比較](../../../../services/storage.md#comparison)と[EBS、EFS、S3、FSx の比較](../../../../services/storage-advanced.md#storage-comparison): オブジェクト、ファイル、ブロックの違いを比べます。
2. [ストレージクラス](../../../../services/s3.md#storage-classes)と[インスタンスストア](../../../../services/storage-advanced.md#instance-store): 1 つの AZ のクラスと、揮発性のストレージを押さえます。
3. [スナップショット](../../../../services/storage.md#ebs-snapshots)と[復元テストと監査](../../../../services/resilience.md#backup-testing): スナップショットと復元のテストを確認します。

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 複数の Linux サーバーで共有する | EFS |
| 大量の画像を配信する | S3 |
| 失えないデータを S3 に置く | One Zone 以外のクラス |
| EBS を守る | スナップショットとリージョン間のコピー |

## 引っかかりやすい点 {#traps}

- EBS は 1 つの AZ の中で複製します。Multi-Attach も同じ AZ の中だけです。
- インスタンスストアは停止や終了で消えます。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [storage 問1](../../exercises/storage.md#q1) | ストレージの種類 | スケールアウトする Linux の Web サーバーで、アップロードされたファイルを全台で共有します… |
| [storage 問2](../../exercises/storage.md#q2) | ストレージの種類 | 大量の画像を HTTPS で世界中に配信します。容量の管理はしません。どの種類のストレージですか。 |
| [storage 問3](../../exercises/storage.md#q3) | ストレージの種類 | ストレージの種類の説明として正しいものはどれですか。 |
| [storage 問4](../../exercises/storage.md#q4) | ストレージの耐久性 | 再作成できない顧客データを S3 に保管します。次のうち、AZ の喪失でデータを失う可能性があるスト… |
| [storage 問5](../../exercises/storage.md#q5) | ストレージの耐久性 | インスタンスストアのデータの扱いとして正しいものはどれですか。 |
| [storage 問6](../../exercises/storage.md#q6) | ストレージの耐久性 | EBS ボリュームのデータを、AZ の障害や破損に備えて保護します。適切なものを選んでください。（2… |

<!-- questions:end -->

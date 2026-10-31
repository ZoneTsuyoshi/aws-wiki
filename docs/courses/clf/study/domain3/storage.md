# 分野3: ストレージ

種類の区別、S3 のクラスの選択、バックアップとオンプレミスとの連携を問います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [ストレージの全体像](../../domain3.md#t3-6-overview) | オブジェクト、ブロック、ファイル |
| [オブジェクトストレージの用途](../../domain3.md#t3-6-object) | S3 の用途 |
| [S3 のストレージクラス](../../domain3.md#t3-6-s3-classes) | 頻度と取り出しの速さ |
| [ブロックストレージ](../../domain3.md#t3-6-block) | EBS とインスタンスストア |
| [ファイルサービス](../../domain3.md#t3-6-file) | EFS と FSx |
| [キャッシュ付きのファイルシステム](../../domain3.md#t3-6-cached) | Storage Gateway |
| [ライフサイクルポリシーの用途](../../domain3.md#t3-6-lifecycle) | 移動と削除の自動化 |
| [AWS Backup の用途](../../domain3.md#t3-6-backup) | 一元管理 |

## 学習の順番 {#study-order}

1. [比較](../../../../services/storage.md#comparison): 3 つの種類を確認します。
2. [ストレージクラス](../../../../services/s3.md#storage-classes)と[S3 Glacier のデータ取得](../../../../services/s3.md#glacier-retrieval): 見分ける 3 つの点で覚えます。
3. [ライフサイクル](../../../../services/s3.md#lifecycle): 移動と削除の例を確認します。
4. [EBS のボリュームタイプ](../../../../services/storage.md#ebs-volume-types)と[インスタンスストア](../../../../services/storage-advanced.md#instance-store): 永続性の違いを覚えます。
5. [EFS の設定](../../../../services/storage.md#efs-settings)と[FSx の選び方](../../../../services/storage-advanced.md#fsx-selection): OS とプロトコルで選びます。
6. [AWS Storage Gateway](../../../../services/migration.md#storage-gateway)、[AWS Backup](../../../../services/resilience.md#backup)、[AWS Elastic Disaster Recovery(DRS)](../../../../services/resilience.md#drs): 役割を区別します。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| S3 Standard-IA、One Zone-IA | 月 1 回程度 | One Zone-IA は AZ の喪失に耐えられない |
| Glacier Instant Retrieval | 四半期に 1 回 | ミリ秒で取り出す |
| Glacier Flexible Retrieval | 年 1 回程度 | 数分から数時間 |
| Glacier Deep Archive | 年 1 回未満 | 数時間 |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| アクセスパターンが不明 | S3 Intelligent-Tiering |
| 再生成できるデータを安く置く | S3 One Zone-IA |
| ブートボリューム、データベース | EBS |
| 一時的なデータ、キャッシュ | インスタンスストア |
| Linux で共有する | EFS |
| Windows、SMB、Active Directory | FSx for Windows File Server |
| NetApp からの移行 | FSx for NetApp ONTAP |
| オンプレミスから低遅延で読む | Storage Gateway |
| 既存のテープのソフトを使う | Tape Gateway |
| バックアップを一元管理する | AWS Backup |
| サーバーを継続的に複製して素早く復旧する | Elastic Disaster Recovery |

## 引っかかりやすい点 {#traps}

- インスタンスストアは再起動では残りますが、停止や終了で消えます。
- S3 は OS をインストールするディスクには使えません。
- FSx for Lustre は、このガイドでは範囲外です。
- Amazon FSx File Gateway は新規受付を終了しています。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [storage 問1](../../exercises/storage.md#q1) | ストレージの全体像 | ストレージの種類とサービスの組み合わせとして正しいものはどれですか。 |
| [storage 問2](../../exercises/storage.md#q2) | ストレージの全体像 | 複数の Linux インスタンスから、同じファイルシステムをマウントして使いたいと考えています。スト… |
| [storage 問3](../../exercises/storage.md#q3) | ストレージの全体像 | アプリから HTTPS の API で読み書きするストレージのサービスはどれですか。 |
| [storage 問4](../../exercises/storage.md#q4) | オブジェクトストレージの用途 | Amazon S3 の用途として適切なものはどれですか。（2つ選択） |
| [storage 問5](../../exercises/storage.md#q5) | オブジェクトストレージの用途 | 静的な HTML と画像だけの Web サイトを、サーバーの管理なしで公開したいと考えています。最も… |
| [storage 問6](../../exercises/storage.md#q6) | オブジェクトストレージの用途 | S3 の容量の説明として正しいものはどれですか。 |
| [storage 問7](../../exercises/storage.md#q7) | S3 のストレージクラス | アクセスのパターンが不明で変わるデータを、手間なく安く保管したいと考えています。最も適切なストレージ… |
| [storage 問8](../../exercises/storage.md#q8) | S3 のストレージクラス | 月 1 回程度アクセスするデータで、再生成できるので AZ の喪失に耐える必要はありません。最も安く… |
| [storage 問9](../../exercises/storage.md#q9) | S3 のストレージクラス | 法律で 7 年保管する監査ログを、年 1 回未満しか読みません。取り出しに半日かかっても構いません。… |
| [storage 問10](../../exercises/storage.md#q10) | S3 のストレージクラス | 四半期に 1 回しか読みませんが、読むときはミリ秒で取り出したいアーカイブがあります。最も適切なクラ… |
| [storage 問11](../../exercises/storage.md#q11) | S3 のストレージクラス | AZ の喪失に耐えられないストレージクラスはどれですか。 |
| [storage 問12](../../exercises/storage.md#q12) | ブロックストレージ | EC2 インスタンスを止めてもデータを残したい、ブートボリュームに使えるストレージはどれですか。 |
| [storage 問13](../../exercises/storage.md#q13) | ブロックストレージ | インスタンスストアのデータの説明として正しいものはどれですか。 |
| [storage 問14](../../exercises/storage.md#q14) | ブロックストレージ | 一時的な処理のキャッシュを、インスタンスの料金の範囲で高速なローカルディスクに置きたいと考えています… |
| [storage 問15](../../exercises/storage.md#q15) | ファイルサービス | Linux の複数のインスタンスから同時に使うファイル共有がほしいと考えています。容量は自動で増減さ… |
| [storage 問16](../../exercises/storage.md#q16) | ファイルサービス | Windows のアプリで SMB と Active Directory を使うファイル共有が必要で… |
| [storage 問17](../../exercises/storage.md#q17) | ファイルサービス | オンプレミスの NetApp のストレージを移行して、複数のプロトコルで使いたいと考えています。最も… |
| [storage 問18](../../exercises/storage.md#q18) | キャッシュ付きのファイルシステム | オンプレミスのアプリから、よく使うデータを低遅延で読みながら、データは AWS に置きたいと考えてい… |
| [storage 問19](../../exercises/storage.md#q19) | キャッシュ付きのファイルシステム | 既存のテープのバックアップソフトを使い続けながら、保管先を AWS にしたいと考えています。最も適切… |
| [storage 問20](../../exercises/storage.md#q20) | キャッシュ付きのファイルシステム | オンプレミスのアプリがファイルとして書いたデータを、S3 にオブジェクトとして保存したいと考えていま… |
| [storage 問21](../../exercises/storage.md#q21) | ライフサイクルポリシーの用途 | ログを 30 日後に安いクラスへ移し、7 年後に削除したいと考えています。手作業を減らす方法はどれで… |
| [storage 問22](../../exercises/storage.md#q22) | ライフサイクルポリシーの用途 | S3 のライフサイクルルールでできることはどれですか。（2つ選択） |
| [storage 問23](../../exercises/storage.md#q23) | ライフサイクルポリシーの用途 | アクセスのパターンが読めず、いつ安いクラスに移せばよいか決められません。最も適切な方法はどれですか。 |
| [storage 問24](../../exercises/storage.md#q24) | AWS Backup の用途 | EBS、RDS、DynamoDB、EFS のバックアップを、1 か所のプランで一元管理したいと考えて… |
| [storage 問25](../../exercises/storage.md#q25) | AWS Backup の用途 | サーバーを別の場所へ継続的に複製して、障害時に素早く復旧したいと考えています。最も適切なサービスはど… |
| [storage 問26](../../exercises/storage.md#q26) | AWS Backup の用途 | チームごとにサービスの画面でばらばらに設定したバックアップに、抜け漏れが出ています。最も適切な改善は… |

<!-- questions:end -->

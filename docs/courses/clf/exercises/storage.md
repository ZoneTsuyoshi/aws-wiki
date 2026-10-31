# ストレージ の問題集

対象の解説: [ストレージ](../../../services/storage.md)、[S3](../../../services/s3.md)、[ストレージの詳細](../../../services/storage-advanced.md)、[レジリエンス](../../../services/resilience.md)、[移行サービス](../../../services/migration.md)

### 問1 {#q1}

ストレージの種類とサービスの組み合わせとして正しいものはどれですか。

- A. オブジェクト: FSx、ブロック: S3、ファイル: インスタンスストア
- B. オブジェクト: S3、ブロック: EBS、ファイル: EFS
- C. オブジェクト: EBS、ブロック: EFS、ファイル: S3
- D. オブジェクト: EFS、ブロック: S3、ファイル: EBS

??? success "答えと解説"
    **正解: B**

    S3 は HTTPS の API、EBS はインスタンスのディスク、EFS はマウントして使います。

    - A: 誤り。すべて組み合わせが違う。
    - B: 正しい。
    - C: 誤り。すべて組み合わせが違う。
    - D: 誤り。すべて組み合わせが違う。

    **スキル:** [ストレージの全体像](../domain3.md#t3-6-overview) / **参照:** [比較](../../../services/storage.md#comparison)

### 問2 {#q2}

複数の Linux インスタンスから、同じファイルシステムをマウントして使いたいと考えています。ストレージの種類はどれですか。

- A. オブジェクト
- B. ブロック
- C. アーカイブ
- D. ファイル

??? success "答えと解説"
    **正解: D**

    ファイルシステムとしてマウントするのがファイルストレージです。

    - A: 誤り。HTTPS の API でアクセスするもので、マウントして使う形ではない。
    - B: 誤り。主に 1 つのインスタンスのディスクとして使う。
    - C: 誤り。長期保管のためのクラスで、種類としてマウントはしない。
    - D: 正しい。

    **スキル:** [ストレージの全体像](../domain3.md#t3-6-overview) / **参照:** [比較](../../../services/storage.md#comparison)

### 問3 {#q3}

アプリから HTTPS の API で読み書きするストレージのサービスはどれですか。

- A. Amazon S3
- B. Amazon EBS
- C. Amazon EFS
- D. インスタンスストア

??? success "答えと解説"
    **正解: A**

    S3 はオブジェクトストレージです。

    - A: 正しい。
    - B: 誤り。インスタンスのディスクとして使う。
    - C: 誤り。ファイルシステムとしてマウントする。
    - D: 誤り。インスタンスのディスクとして使う。

    **スキル:** [ストレージの全体像](../domain3.md#t3-6-overview) / **参照:** [比較](../../../services/storage.md#comparison)

### 問4 {#q4}

Amazon S3 の用途として適切なものはどれですか。（2つ選択）

- A. バックアップの保管
- B. EC2 の OS をインストールするブートディスク
- C. データレイク
- D. リレーショナルデータベースのトランザクション
- E. インメモリのキャッシュ

??? success "答えと解説"
    **正解: A, C**

    S3 はファイル配信、バックアップ、データレイク、静的ウェブサイトに使います。

    - A: 正しい。
    - B: 誤り。OS のディスクには使えない。
    - C: 正しい。
    - D: 誤り。データベースのサービスではない。
    - E: 誤り。メモリのサービスではない。

    **スキル:** [オブジェクトストレージの用途](../domain3.md#t3-6-object) / **参照:** [基本と整合性](../../../services/s3.md#basics)

### 問5 {#q5}

静的な HTML と画像だけの Web サイトを、サーバーの管理なしで公開したいと考えています。最も適切なものはどれですか。

- A. インスタンスストアから公開する
- B. AWS Backup から公開する
- C. S3 の静的ウェブサイトホスティング
- D. EBS に HTML を置いて公開する

??? success "答えと解説"
    **正解: C**

    S3 は静的ウェブサイトのホスティングに使えます。

    - A: 誤り。インスタンスの管理が必要で、データも消える。
    - B: 誤り。バックアップの管理のサービス。
    - C: 正しい。
    - D: 誤り。EBS はインスタンスのディスクで、単独では公開できない。

    **スキル:** [オブジェクトストレージの用途](../domain3.md#t3-6-object) / **参照:** [静的ウェブサイトホスティング](../../../services/s3.md#static-website)

### 問6 {#q6}

S3 の容量の説明として正しいものはどれですか。

- A. 保存する量に合わせて容量が自動で増減し、先に確保しなくてよい
- B. 使う前に容量を GB 単位で確保する必要があり、後からは増やせない
- C. インスタンスの数に合わせて、確保した量が自動で決まる
- D. サブネットの大きさで、保存できる量の上限が決まる

??? success "答えと解説"
    **正解: A**

    S3 は容量を自動で増減します。

    - A: 正しい。
    - B: 誤り。先に確保する必要はない。
    - C: 誤り。インスタンスとは独立している。
    - D: 誤り。サブネットとは関係しない。

    **スキル:** [オブジェクトストレージの用途](../domain3.md#t3-6-object) / **参照:** [基本と整合性](../../../services/s3.md#basics)

### 問7 {#q7}

アクセスのパターンが不明で変わるデータを、手間なく安く保管したいと考えています。最も適切なストレージクラスはどれですか。

- A. S3 Glacier Flexible Retrieval
- B. S3 Glacier Deep Archive
- C. S3 Intelligent-Tiering
- D. S3 One Zone-IA

??? success "答えと解説"
    **正解: C**

    Intelligent-Tiering は、アクセスパターンが不明なデータに向きます。

    - A: 誤り。年 1 回程度のアーカイブ向けで、取り出しに時間がかかる。
    - B: 誤り。年 1 回未満の長期保管向けで、すぐには読めない。
    - C: 正しい。
    - D: 誤り。月 1 回程度の再生成できるデータ向け。

    **スキル:** [S3 のストレージクラス](../domain3.md#t3-6-s3-classes) / **参照:** [ストレージクラス](../../../services/s3.md#storage-classes)

### 問8 {#q8}

月 1 回程度アクセスするデータで、再生成できるので AZ の喪失に耐える必要はありません。最も安く保管できるクラスとして適切なものはどれですか。

- A. S3 Standard-IA
- B. S3 One Zone-IA
- C. S3 Intelligent-Tiering
- D. S3 Standard

??? success "答えと解説"
    **正解: B**

    One Zone-IA は 1 つの AZ だけに置きます。

    - A: 誤り。複数の AZ に保管するので、One Zone-IA より高い。
    - B: 正しい。
    - C: 誤り。アクセスパターンが不明なときに向く。
    - D: 誤り。頻繁なアクセス向け。

    **スキル:** [S3 のストレージクラス](../domain3.md#t3-6-s3-classes) / **参照:** [ストレージクラス](../../../services/s3.md#storage-classes)

### 問9 {#q9}

法律で 7 年保管する監査ログを、年 1 回未満しか読みません。取り出しに半日かかっても構いません。最も安いクラスとして適切なものはどれですか。

- A. S3 One Zone-IA
- B. S3 Standard
- C. S3 Glacier Instant Retrieval
- D. S3 Glacier Deep Archive

??? success "答えと解説"
    **正解: D**

    Deep Archive は年 1 回未満の長期保管に向きます。

    - A: 誤り。月 1 回程度のデータ向けで、AZ の喪失にも耐えられない。
    - B: 誤り。頻繁なアクセス向け。
    - C: 誤り。すぐ読むためのアーカイブで、この要件には必要以上。
    - D: 正しい。

    **スキル:** [S3 のストレージクラス](../domain3.md#t3-6-s3-classes) / **参照:** [ストレージクラス](../../../services/s3.md#storage-classes)、[S3 Glacier のデータ取得](../../../services/s3.md#glacier-retrieval)

### 問10 {#q10}

四半期に 1 回しか読みませんが、読むときはミリ秒で取り出したいアーカイブがあります。最も適切なクラスはどれですか。

- A. S3 Glacier Deep Archive
- B. S3 Standard
- C. S3 Glacier Instant Retrieval
- D. S3 Glacier Flexible Retrieval

??? success "答えと解説"
    **正解: C**

    Glacier Instant Retrieval は四半期に 1 回程度のアーカイブに向きます。

    - A: 誤り。取り出しに数時間かかる。
    - B: 誤り。読むのは速いが、この頻度のアーカイブには割高。
    - C: 正しい。
    - D: 誤り。取り出しに数分から数時間かかる。

    **スキル:** [S3 のストレージクラス](../domain3.md#t3-6-s3-classes) / **参照:** [ストレージクラス](../../../services/s3.md#storage-classes)

### 問11 {#q11}

AZ の喪失に耐えられないストレージクラスはどれですか。

- A. S3 Standard-IA
- B. S3 One Zone-IA
- C. S3 Standard
- D. S3 Glacier Deep Archive

??? success "答えと解説"
    **正解: B**

    One Zone-IA は 1 つの AZ だけに置くので、AZ の喪失に耐えられません。

    - A: 誤り。複数の AZ に保管する。
    - B: 正しい。
    - C: 誤り。複数の AZ に保管する。
    - D: 誤り。複数の AZ に保管する。

    **スキル:** [S3 のストレージクラス](../domain3.md#t3-6-s3-classes) / **参照:** [ストレージクラス](../../../services/s3.md#storage-classes)

### 問12 {#q12}

EC2 インスタンスを止めてもデータを残したい、ブートボリュームに使えるストレージはどれですか。

- A. Amazon EBS
- B. Amazon ElastiCache
- C. Amazon S3
- D. インスタンスストア

??? success "答えと解説"
    **正解: A**

    EBS はインスタンスを止めても残ります。

    - A: 正しい。
    - B: 誤り。インメモリのキャッシュ。
    - C: 誤り。OS のディスクには使えない。
    - D: 誤り。停止で消える。

    **スキル:** [ブロックストレージ](../domain3.md#t3-6-block) / **参照:** [EBS のボリュームタイプ](../../../services/storage.md#ebs-volume-types)、[インスタンスストア](../../../services/storage-advanced.md#instance-store)

### 問13 {#q13}

インスタンスストアのデータの説明として正しいものはどれですか。

- A. 再起動で消えるが、終了では残る
- B. 再起動でも停止でも、終了でも必ず残る
- C. 別のインスタンスへ付け替えて、いつでも読める
- D. 再起動では残るが、停止や終了では消える

??? success "答えと解説"
    **正解: D**

    インスタンスストアは一時的なデータに向きます。

    - A: 誤り。再起動で残り、終了で消える。
    - B: 誤り。停止や終了で消える。
    - C: 誤り。付け替えはできない。
    - D: 正しい。

    **スキル:** [ブロックストレージ](../domain3.md#t3-6-block) / **参照:** [インスタンスストア](../../../services/storage-advanced.md#instance-store)

### 問14 {#q14}

一時的な処理のキャッシュを、インスタンスの料金の範囲で高速なローカルディスクに置きたいと考えています。消えても構いません。最も適切なものはどれですか。

- A. AWS Backup
- B. Amazon S3 Glacier Deep Archive
- C. インスタンスストア
- D. Amazon EBS

??? success "答えと解説"
    **正解: C**

    料金はインスタンスに含まれ、一時的なデータに向きます。

    - A: 誤り。バックアップの管理のサービス。
    - B: 誤り。長期保管のストレージ。
    - C: 正しい。
    - D: 誤り。永続するディスクで、容量などに応じて別途料金がかかる。

    **スキル:** [ブロックストレージ](../domain3.md#t3-6-block) / **参照:** [EBS のボリュームタイプ](../../../services/storage.md#ebs-volume-types)、[インスタンスストア](../../../services/storage-advanced.md#instance-store)

### 問15 {#q15}

Linux の複数のインスタンスから同時に使うファイル共有がほしいと考えています。容量は自動で増減させたいです。最も適切なサービスはどれですか。

- A. Amazon EFS
- B. FSx for Windows File Server
- C. AWS Storage Gateway
- D. Amazon EBS

??? success "答えと解説"
    **正解: A**

    EFS は Linux の共有ファイルシステムです。

    - A: 正しい。
    - B: 誤り。Windows のファイル共有向け。
    - C: 誤り。オンプレミスと AWS をつなぐサービス。
    - D: 誤り。1 つの AZ のブロックストレージで、自動で増減しない。

    **スキル:** [ファイルサービス](../domain3.md#t3-6-file) / **参照:** [EFS の設定](../../../services/storage.md#efs-settings)

### 問16 {#q16}

Windows のアプリで SMB と Active Directory を使うファイル共有が必要です。最も適切なサービスはどれですか。

- A. Amazon S3
- B. FSx for Windows File Server
- C. Amazon EFS
- D. FSx for OpenZFS

??? success "答えと解説"
    **正解: B**

    Windows のファイル共有は FSx for Windows File Server です。

    - A: 誤り。オブジェクトストレージで、SMB の共有ではない。
    - B: 正しい。
    - C: 誤り。Linux の共有向け。
    - D: 誤り。ZFS や Linux のファイルサーバーの移行向け。

    **スキル:** [ファイルサービス](../domain3.md#t3-6-file) / **参照:** [FSx の選び方](../../../services/storage-advanced.md#fsx-selection)

### 問17 {#q17}

オンプレミスの NetApp のストレージを移行して、複数のプロトコルで使いたいと考えています。最も適切なサービスはどれですか。

- A. S3 Glacier Flexible Retrieval
- B. FSx for Windows File Server
- C. Amazon EBS
- D. FSx for NetApp ONTAP

??? success "答えと解説"
    **正解: D**

    NetApp からの移行には FSx for NetApp ONTAP が向きます。

    - A: 誤り。アーカイブ向け。
    - B: 誤り。Windows のファイル共有向け。
    - C: 誤り。ブロックストレージで、NetApp の機能は持たない。
    - D: 正しい。

    **スキル:** [ファイルサービス](../domain3.md#t3-6-file) / **参照:** [FSx の選び方](../../../services/storage-advanced.md#fsx-selection)

### 問18 {#q18}

オンプレミスのアプリから、よく使うデータを低遅延で読みながら、データは AWS に置きたいと考えています。最も適切なサービスはどれですか。

- A. AWS Storage Gateway
- B. AWS Direct Connect
- C. Amazon CloudFront
- D. Amazon EFS

??? success "答えと解説"
    **正解: A**

    Storage Gateway は、よく使うデータをローカルにキャッシュします。

    - A: 正しい。
    - B: 誤り。接続の手段で、キャッシュは行わない。
    - C: 誤り。利用者へのコンテンツ配信のサービス。
    - D: 誤り。AWS 上のファイルシステムで、オンプレミスのローカルキャッシュではない。

    **スキル:** [キャッシュ付きのファイルシステム](../domain3.md#t3-6-cached) / **参照:** [AWS Storage Gateway](../../../services/migration.md#storage-gateway)

### 問19 {#q19}

既存のテープのバックアップソフトを使い続けながら、保管先を AWS にしたいと考えています。最も適切なタイプはどれですか。

- A. AWS Backup のボールト
- B. S3 File Gateway
- C. Tape Gateway
- D. Volume Gateway

??? success "答えと解説"
    **正解: C**

    Tape Gateway は既存のテープのバックアップソフトで使えます。

    - A: 誤り。Storage Gateway のタイプではなく、既存のテープのソフトは使えない。
    - B: 誤り。ファイルとして書くタイプ。
    - C: 正しい。
    - D: 誤り。iSCSI のボリュームとして使うタイプ。

    **スキル:** [キャッシュ付きのファイルシステム](../domain3.md#t3-6-cached) / **参照:** [AWS Storage Gateway](../../../services/migration.md#storage-gateway)

### 問20 {#q20}

オンプレミスのアプリがファイルとして書いたデータを、S3 にオブジェクトとして保存したいと考えています。最も適切なものはどれですか。

- A. Tape Gateway
- B. Volume Gateway
- C. S3 Glacier Deep Archive
- D. S3 File Gateway

??? success "答えと解説"
    **正解: D**

    S3 File Gateway はファイルで書き、S3 に保存します。

    - A: 誤り。テープのバックアップソフト向け。
    - B: 誤り。iSCSI のボリュームとして使う。
    - C: 誤り。保管先のクラスで、ファイルで書く手段ではない。
    - D: 正しい。

    **スキル:** [キャッシュ付きのファイルシステム](../domain3.md#t3-6-cached) / **参照:** [AWS Storage Gateway](../../../services/migration.md#storage-gateway)

### 問21 {#q21}

ログを 30 日後に安いクラスへ移し、7 年後に削除したいと考えています。手作業を減らす方法はどれですか。

- A. S3 Intelligent-Tiering
- B. S3 のライフサイクルルール
- C. S3 の静的ホスティング
- D. AWS Backup のバックアッププラン

??? success "答えと解説"
    **正解: B**

    ライフサイクルルールで、移動と削除を自動にできます。

    - A: 誤り。アクセスに応じて層を移すクラスで、決めた日数での移動や削除は行わない。
    - B: 正しい。
    - C: 誤り。サイトの公開の機能。
    - D: 誤り。バックアップの管理のサービスで、オブジェクトのクラスの移動は行わない。

    **スキル:** [ライフサイクルポリシーの用途](../domain3.md#t3-6-lifecycle) / **参照:** [ライフサイクル](../../../services/s3.md#lifecycle)

### 問22 {#q22}

S3 のライフサイクルルールでできることはどれですか。（2つ選択）

- A. 期限を過ぎたオブジェクトを削除する
- B. オブジェクトの中の個人情報を検出する
- C. バケットを別のアカウントへ請求ごと移す
- D. 古くなったオブジェクトを安いクラスへ移す
- E. EBS ボリュームを S3 に自動で変換する

??? success "答えと解説"
    **正解: A, D**

    手作業なしで費用を抑えられます。

    - A: 正しい。
    - B: 誤り。それは Amazon Macie の役割。
    - C: 誤り。ライフサイクルルールの機能ではない。
    - D: 正しい。
    - E: 誤り。ライフサイクルルールの機能ではない。

    **スキル:** [ライフサイクルポリシーの用途](../domain3.md#t3-6-lifecycle) / **参照:** [ライフサイクル](../../../services/s3.md#lifecycle)

### 問23 {#q23}

アクセスのパターンが読めず、いつ安いクラスに移せばよいか決められません。最も適切な方法はどれですか。

- A. 全オブジェクトを手作業で週に 1 回移す
- B. 全オブジェクトを 1 日後に Deep Archive へ移す
- C. S3 Intelligent-Tiering を使う
- D. 全オブジェクトを One Zone-IA に置く

??? success "答えと解説"
    **正解: C**

    日数で決められないなら Intelligent-Tiering が候補です。

    - A: 誤り。手間がかかり、判断の根拠もない。
    - B: 誤り。取り出しに時間がかかり、取り出し料もかかる。
    - C: 正しい。
    - D: 誤り。AZ の喪失に耐えられない。

    **スキル:** [ライフサイクルポリシーの用途](../domain3.md#t3-6-lifecycle) / **参照:** [ライフサイクル](../../../services/s3.md#lifecycle)、[ストレージクラス](../../../services/s3.md#storage-classes)

### 問24 {#q24}

EBS、RDS、DynamoDB、EFS のバックアップを、1 か所のプランで一元管理したいと考えています。最も適切なサービスはどれですか。

- A. AWS License Manager
- B. AWS Storage Gateway
- C. Amazon S3
- D. AWS Backup

??? success "答えと解説"
    **正解: D**

    AWS Backup は複数のサービスのバックアップを 1 か所で管理します。

    - A: 誤り。ライセンスの管理のサービス。
    - B: 誤り。オンプレミスと AWS をつなぐサービス。
    - C: 誤り。オブジェクトストレージで、複数のサービスのバックアップを管理するものではない。
    - D: 正しい。

    **スキル:** [AWS Backup の用途](../domain3.md#t3-6-backup) / **参照:** [AWS Backup](../../../services/resilience.md#backup)

### 問25 {#q25}

サーバーを別の場所へ継続的に複製して、障害時に素早く復旧したいと考えています。最も適切なサービスはどれですか。

- A. Amazon S3 のライフサイクルルール
- B. AWS Elastic Disaster Recovery
- C. AWS Artifact
- D. AWS Backup

??? success "答えと解説"
    **正解: B**

    サーバーの継続的な複製と復旧は Elastic Disaster Recovery です。

    - A: 誤り。オブジェクトの移動と削除の機能。
    - B: 正しい。
    - C: 誤り。監査レポートを入手するサービス。
    - D: 誤り。バックアップの管理で、継続的な複製からの素早い復旧の専用サービスではない。

    **スキル:** [AWS Backup の用途](../domain3.md#t3-6-backup) / **参照:** [AWS Elastic Disaster Recovery(DRS)](../../../services/resilience.md#drs)、[AWS Backup](../../../services/resilience.md#backup)

### 問26 {#q26}

チームごとにサービスの画面でばらばらに設定したバックアップに、抜け漏れが出ています。最も適切な改善はどれですか。

- A. AWS Backup のバックアッププランで一元管理する
- B. CloudFront のキャッシュをバックアップの代わりにする
- C. 全データを EC2 のインスタンスストアに置く
- D. 各サービスの担当者に、毎週の手順の確認を頼む

??? success "答えと解説"
    **正解: A**

    「ばらばらのバックアップを一元管理したい」は AWS Backup です。

    - A: 正しい。
    - B: 誤り。キャッシュはバックアップではない。
    - C: 誤り。停止で消えるので、バックアップにならない。
    - D: 誤り。手作業が残り、抜け漏れは防げない。

    **スキル:** [AWS Backup の用途](../domain3.md#t3-6-backup) / **参照:** [AWS Backup](../../../services/resilience.md#backup)

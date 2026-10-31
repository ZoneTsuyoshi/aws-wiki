# EBS、EFS、FSx の問題集

対象の解説: [EBS のボリュームタイプ](../../../services/storage.md#ebs-volume-types)、[EFS の設定](../../../services/storage.md#efs-settings)、[FSx の選び方](../../../services/storage-advanced.md#fsx-selection)、[FSx のバックアップと世代管理](../../../services/storage-advanced.md#fsx-protection)

### 問1 {#q1}

100 GiB の `gp2` のデータベースのボリュームが昼だけ遅くなります。`BurstBalance` が 0 に近づいています。必要な IOPS は 5,000 です。費用を抑えて停止なしで直すにはどうしますか。

- A. `gp2` のサイズを 2,000 GiB へ増やして、ベースラインの IOPS を確保しておく
- B. `io2` Block Express へ変更して、最大の 256,000 IOPS を設定して運用する
- C. `gp3` へ変更し、5,000 IOPS を指定する
- D. `st1` へ変更し、順次読み取りで性能を出す

??? success "答えと解説"
    **正解: C**

    `gp3` はサイズと独立に IOPS を決められ、Elastic Volumes で稼働中に変更できます。

    - A: 誤り。必要以上の容量を買うことになり、費用が高い。
    - B: 誤り。この要件に対しては高価である。
    - C: 正しい。
    - D: 誤り。`st1` は順次アクセス向けで、データベースのランダム I/O に向かない。

    **スキル:** [1.3.2](../domain1.md#skill-1-3-2) / **参照:** [IOPS とスループットの設定](../../../services/storage.md#ebs-performance-settings)、[EBS のボリュームタイプ](../../../services/storage.md#ebs-volume-types)

### 問2 {#q2}

`gp3` のボリュームで `VolumeIOPSExceededCheck` は `0` のままですが、`InstanceEBSIOPSExceededCheck` が `1` になっています。アプリケーションの I/O が頭打ちです。どう直しますか。

- A. EBS の性能が高いインスタンスタイプへ変更する
- B. ボリュームのサイズを増やしたあと、OS でファイルシステムを拡張する
- C. ボリュームを `gp3` から `gp2` へ戻して、バーストのクレジットを使えるようにする
- D. ボリュームの IOPS を増やす

??? success "答えと解説"
    **正解: A**

    `InstanceEBSIOPSExceededCheck` はインスタンス側の EBS の IOPS の上限を示します。

    - A: 正しい。
    - B: 誤り。インスタンス側の上限は変わらない。
    - C: 誤り。インスタンス側の上限の問題で、ボリュームのタイプでは直らない。
    - D: 誤り。ボリューム側は超過しておらず、増やしても直らない。

    **スキル:** [1.3.2](../domain1.md#skill-1-3-2) / **参照:** [IOPS とスループットの設定](../../../services/storage.md#ebs-performance-settings)

### 問3 {#q3}

EBS のボリュームのサイズを増やす変更が完了しましたが、OS から見える容量が変わりません。何をしますか。

- A. スナップショットを作成して、別の AZ のインスタンスで復元する
- B. OS でファイルシステムを拡張する
- C. もう一度 `ModifyVolume` を実行して、変更を適用し直す
- D. インスタンスを終了して作り直す

??? success "答えと解説"
    **正解: B**

    容量を増やした後は、OS でファイルシステムを拡張します。

    - A: 誤り。AZ を移す手順で、この症状とは関係がない。
    - B: 正しい。
    - C: 誤り。ボリューム側の変更は完了している。
    - D: 誤り。終了は不要である。

    **スキル:** [1.3.2](../domain1.md#skill-1-3-2) / **参照:** [ボリュームの変更と AZ の制約](../../../services/storage.md#ebs-modify)

### 問4 {#q4}

EBS の Elastic Volumes について正しいものを選んでください。（2つ選択）

- A. 変更すると自動的に別の AZ に移すことができる
- B. 変更は 24 時間で 4 回までで、前の変更の完了を待つ
- C. `gp2` から `gp3` への変更には、インスタンスの停止が必要である
- D. サイズを減らす変更はできない
- E. サイズを増やすと、OS のファイルシステムも自動で拡張される

??? success "答えと解説"
    **正解: B, D**

    サイズの縮小はできないので、小さいボリュームへデータを移します。

    - A: 誤り。別の AZ で使うならスナップショットから作り直す。
    - B: 正しい。
    - C: 誤り。稼働中に変更できる。
    - D: 正しい。
    - E: 誤り。OS での拡張が別に必要である。

    **スキル:** [1.3.2](../domain1.md#skill-1-3-2) / **参照:** [ボリュームの変更と AZ の制約](../../../services/storage.md#ebs-modify)

### 問5 {#q5}

スナップショットから作ったボリュームで、最初の読み取りが遅くなります。本番の切り替えの直後から性能を出したいと考えています。どうしますか。

- A. スナップショットをコールドの階層に移して、復元の準備をしておく
- B. インスタンスを別のリージョンに移して読み取りの経路を短くする
- C. ボリュームを `sc1` へ変更する
- D. Fast Snapshot Restore を有効にする

??? success "答えと解説"
    **正解: D**

    Fast Snapshot Restore は、スナップショットからのボリュームで最初から全性能を出します。

    - A: 誤り。アーカイブすると復元はさらに遅くなる。
    - B: 誤り。リージョンを変えても初回の読み取りの問題は解決しない。
    - C: 誤り。`sc1` はアクセスの少ないデータ向けで、遅い。
    - D: 正しい。

    **スキル:** [1.3.2](../domain1.md#skill-1-3-2) / **参照:** [スナップショット](../../../services/storage.md#ebs-snapshots)、[ボリュームの変更と AZ の制約](../../../services/storage.md#ebs-modify)

### 問6 {#q6}

次の要件に合う EBS を選びます。ログの順次読み取りが中心の大きなデータを扱い、最小の費用ではなく、スループットを重視します。ブートには使いません。どれが適切ですか。

- A. `io2` Block Express
- B. `sc1`
- C. `st1`
- D. `gp2`

??? success "答えと解説"
    **正解: C**

    順次読み取りのログやビッグデータには `st1` が向きます。

    - A: 誤り。IOPS 重視の高価なタイプである。
    - B: 誤り。スループットより費用を優先するタイプで、要件に合わない。
    - C: 正しい。
    - D: 誤り。汎用で、大量の順次アクセスの費用対効果が低い。

    **スキル:** [1.3.2](../domain1.md#skill-1-3-2) / **参照:** [EBS のボリュームタイプ](../../../services/storage.md#ebs-volume-types)

### 問7 {#q7}

Windows のアプリケーションで、SMB の共有フォルダと NTFS の ACL が必要です。Active Directory に参加させます。どれを選びますか。

- A. EFS の Regional タイプ
- B. FSx for Windows File Server
- C. EBS の Multi-Attach を使う `io2`
- D. FSx for Lustre の Persistent

??? success "答えと解説"
    **正解: B**

    Windows の共有フォルダ、NTFS の ACL、AD の組み合わせは FSx for Windows File Server です。

    - A: 誤り。NFS で使う Linux 向けのサービスで、SMB を提供しない。
    - B: 正しい。
    - C: 誤り。ブロックストレージで、ファイル共有の機能を持たない。
    - D: 誤り。主に Linux で使う高速な並列ファイルシステムである。

    **スキル:** [1.3.4](../domain1.md#skill-1-3-4) / **参照:** [比較](../../../services/storage.md#comparison)、[FSx の選び方](../../../services/storage-advanced.md#fsx-selection)

### 問8 {#q8}

S3 にある数百 TB のデータを、ML の学習で多数のノードから高速に並列で読みたいと考えています。どれが適切ですか。

- A. S3 にリンクした FSx for Lustre
- B. EFS の Infrequent Access へ S3 のデータを移す構成
- C. FSx for Windows File Server を S3 にリンクする構成
- D. 各ノードの `gp3` へコピーする構成

??? success "答えと解説"
    **正解: A**

    Lustre は S3 とリンクして、必要なデータだけ読み込めます。

    - A: 正しい。
    - B: 誤り。高速な並列読み取りの要件に合わない。
    - C: 誤り。SMB のファイル共有で、並列処理の高速化には向かない。
    - D: 誤り。コピーと容量の管理の負担が大きい。

    **スキル:** [1.3.4](../domain1.md#skill-1-3-4) / **参照:** [FSx の選び方](../../../services/storage-advanced.md#fsx-selection)、[S3 との連携](../../../services/storage-advanced.md#fsx-lustre-s3)

### 問9 {#q9}

オンプレミスの NetApp から移行します。NFS、SMB、iSCSI を同時に使い、アクセスの少ないデータの費用を自動で下げたいです。何を選びますか。

- A. S3 Intelligent-Tiering と S3 Files を組み合わせた構成
- B. EFS のライフサイクル管理
- C. FSx for Lustre のスクラッチのデプロイ
- D. 階層化ポリシーを設定した FSx for NetApp ONTAP

??? success "答えと解説"
    **正解: D**

    ONTAP は複数のプロトコルに対応し、階層化ポリシーで安い階層へ移せます。

    - A: 誤り。iSCSI は提供しない。
    - B: 誤り。NFS のみで、SMB や iSCSI は使えない。
    - C: 誤り。並列処理の一時データ向けである。
    - D: 正しい。

    **スキル:** [1.3.4](../domain1.md#skill-1-3-4) / **参照:** [FSx の選び方](../../../services/storage-advanced.md#fsx-selection)、[ストレージ階層と階層化ポリシー](../../../services/storage-advanced.md#fsx-ontap-tiering)

### 問10 {#q10}

Linux の複数台で共有する EFS で、負荷の予測がしにくいアプリケーションを動かします。スループットモードの推奨はどれですか。

- A. Max I/O
- B. Bursting
- C. Elastic
- D. Provisioned

??? success "答えと解説"
    **正解: C**

    予測しにくいなら Elastic です。既定で推奨のモードです。

    - A: 誤り。スループットモードではない。
    - B: 誤り。クレジットが尽きると遅くなる。
    - C: 正しい。
    - D: 誤り。量が分かっているときに選ぶモードである。

    **スキル:** [1.3.4](../domain1.md#skill-1-3-4) / **参照:** [スループットモード](../../../services/storage.md#efs-throughput-mode)

### 問11 {#q11}

Bursting モードの EFS で、夕方から遅くなります。`BurstCreditBalance` がほぼ 0 です。データの容量は増やしたくありません。適切な対処はどれですか。

- A. マウントターゲットを作り直す
- B. スループットモードを Elastic に変更する
- C. ライフサイクルで全データを Archive に移し、クレジットを貯める
- D. NFS のマウントを `tls` に変えて、通信の性能を上げる

??? success "答えと解説"
    **正解: B**

    クレジットが尽きるとベースラインまで落ちます。容量に関係なく性能を使うなら Elastic に変えます。

    - A: 誤り。マウントターゲットの場所を変えてもクレジットは増えない。
    - B: 正しい。
    - C: 誤り。アクセスがさらに遅くなる。
    - D: 誤り。暗号化の設定で、クレジットは増えない。

    **スキル:** [1.3.4](../domain1.md#skill-1-3-4) / **参照:** [スループットモード](../../../services/storage.md#efs-throughput-mode)

### 問12 {#q12}

EFS のライフサイクルを設定しました。ほとんど読まれないファイルの費用を下げつつ、アクセスがあったファイルは Standard に戻したいと考えています。どの設定が必要ですか。

- A. 既定の設定のまま、IA のファイルは読むたびに自動でそのまま Standard に戻るので不要である
- B. バックアップのポリシーを無効に変更する
- C. Archive への移行を 1 日に設定する
- D. Standard への移行を「初回アクセス時」にする

??? success "答えと解説"
    **正解: D**

    既定は 30 日で IA、90 日で Archive です。「初回アクセス時」を選ぶと Standard へ戻ります。

    - A: 誤り。既定の Standard への移行は「なし」である。
    - B: 誤り。ストレージクラスの移動とは関係がない。
    - C: 誤り。Standard へ戻す設定ではない。
    - D: 正しい。

    **スキル:** [1.3.4](../domain1.md#skill-1-3-4) / **参照:** [ライフサイクルとストレージクラス](../../../services/storage.md#efs-lifecycle)

### 問13 {#q13}

正本は S3 に置いたまま、ファイルシステムとして共有したいと考えています。読まれないデータの高性能ストレージの費用も抑えたいです。どの設定が関係しますか。

- A. S3 Files のしきい値と、読まれないデータを外す期限
- B. EBS の Multi-Attach と Elastic Volumes の変更の回数
- C. Storage Gateway の FSx File Gateway の新規作成とキャッシュ
- D. FSx for OpenZFS のクローンの数

??? success "答えと解説"
    **正解: A**

    S3 Files は、高性能ストレージへ読み込むファイルサイズのしきい値（既定 128 KiB 未満）と、読まれないデータを外す期限（既定 30 日）で費用を調整します。1 MiB 以上の読み取りは S3 から直接読みます。

    - A: 正しい。
    - B: 誤り。S3 のデータの共有とは関係がない。
    - C: 誤り。FSx File Gateway は新規受付を終了している。
    - D: 誤り。このコースでは対象外のサービスである。

    **スキル:** [1.3.4](../domain1.md#skill-1-3-4) / **参照:** [S3 Files](../../../services/storage-advanced.md#s3-files)

### 問14 {#q14}

FSx for Windows File Server の利用者が、管理者に頼まず、自分で昨日のファイルを戻したいと考えています。何を有効にしますか。

- A. 自動バックアップの保持期間を 90 日にする設定
- B. SnapMirror によるリージョン間のレプリケーション
- C. シャドウコピーを有効にし、スケジュールを設定する
- D. S3 のバージョニングと FSx の連携

??? success "答えと解説"
    **正解: C**

    シャドウコピーは既定で無効です。有効にすると利用者が以前のバージョンを戻せます。

    - A: 誤り。復元は管理者の作業で、新しいファイルシステムになる。
    - B: 誤り。ONTAP の機能である。
    - C: 正しい。
    - D: 誤り。FSx for Windows File Server の機能ではない。

    **スキル:** [2.3.3](../domain2.md#skill-2-3-3) / **参照:** [Windows の機能](../../../services/storage-advanced.md#fsx-windows-features)、[FSx のバックアップと世代管理](../../../services/storage-advanced.md#fsx-protection)

### 問15 {#q15}

FSx の世代管理の説明として正しいものを選んでください。（2つ選択）

- A. FSx for Windows File Server の自動バックアップは既定で有効である
- B. FSx for Windows File Server のシャドウコピーは既定で有効である
- C. FSx for NetApp ONTAP はスナップショットで利用者が戻せる
- D. FSx for NetApp ONTAP は別のリージョンへ複製する機能を持たない
- E. FSx for Lustre にシャドウコピーがあり、利用者が戻せる

??? success "答えと解説"
    **正解: A, C**

    タイプごとに、利用者が戻す方法とバックアップの方法が違います。

    - A: 正しい。
    - B: 誤り。既定で無効である。
    - C: 正しい。
    - D: 誤り。SnapMirror を使える。
    - E: 誤り。シャドウコピーは Windows の機能である。

    **スキル:** [2.3.3](../domain2.md#skill-2-3-3) / **参照:** [FSx のバックアップと世代管理](../../../services/storage-advanced.md#fsx-protection)

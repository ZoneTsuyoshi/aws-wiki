# 移行とスキーマ変換の問題集

対象の解説: [移行と転送](../../../services/migration.md)、[SCT と DMS](../../../services/data-engineering.md#sct-dms)

### 問1 {#q1}

取引先は今の SFTP クライアントを変えられません。受け取ったファイルは S3 に保存し、到着で Glue ジョブを起動します。どの構成ですか。

- A. DataSync のエージェントを取引先に置き、NFS で共有したファイルを S3 へ同期してから Glue を起動する
- B. DMS のレプリケーションタスクで SFTP をソースにして、S3 へ複製し Glue を起動する
- C. Transfer Family で受け、S3 のイベントを EventBridge で受けて Glue を起動する
- D. Snow Family のデバイスを取引先に送り、毎回届いたファイルを Glue で処理する

??? success "答えと解説"
    **正解: C**

    Transfer Family はクライアントを変えずに S3 を受け口にできます。

    - A: 誤り。取引先のクライアントを変えることになります。
    - B: 誤り。DMS はデータベースの複製のサービスです。
    - C: 正しい。
    - D: 誤り。オフラインの移送で、日々の連携には向きません。

    **スキル:** [2.1.4](../domain2.md#skill-2-1-4) / **参照:** [AWS Transfer Family](../../../services/migration.md#transfer-family)、[サービスの比較](../../../services/migration.md#transfer-comparison)

### 問2 {#q2}

オンプレミスの NFS の 50 TB を S3 へ移し、その後も毎晩差分を転送します。回線の帯域は足ります。何を使いますか。

- A. DataSync
- B. DMS
- C. AppFlow
- D. Transfer Family

??? success "答えと解説"
    **正解: A**

    NFS、SMB、他のオブジェクトストレージからの定期的な転送に向きます。

    - A: 正しい。
    - B: 誤り。データベースの複製に使います。
    - C: 誤り。SaaS の連携に使います。
    - D: 誤り。SFTP などのプロトコルでの受け渡しに使います。

    **スキル:** [2.1.4](../domain2.md#skill-2-1-4) / **参照:** [AWS DataSync](../../../services/migration.md#datasync)、[サービスの比較](../../../services/migration.md#transfer-comparison)

### 問3 {#q3}

回線に乗らない規模のデータをオフラインで運びます。転送サービスの現在の状況として正しいものはどれですか。

- A. Transfer Family がデバイスの配送を担当するサービスになった
- B. Snow Family は新規の注文の受付を再開し、DataSync は提供を終了した
- C. DataSync は回線を使わないオフライン転送の専用サービスに変わった
- D. Snow Family は新規のお客様に提供されず、Data Transfer Terminal などを検討する

??? success "答えと解説"
    **正解: D**

    Snowball Edge は新規のお客様に提供されていません。物理的な転送には Data Transfer Terminal などを検討します。

    - A: 誤り。プロトコルでの受け渡しのサービスです。
    - B: 誤り。どちらも現状と異なります。
    - C: 誤り。回線を使うサービスです。
    - D: 正しい。

    **スキル:** [2.1.4](../domain2.md#skill-2-1-4) / **参照:** [Snow Family の現在の状況](../../../services/migration.md#snow-family)、[サービスの比較](../../../services/migration.md#transfer-comparison)

### 問4 {#q4}

移行のツールの選択で正しいものはどれですか。（2つ選択）

- A. SMB の共有から S3 への定期的な転送は DataSync を使う
- B. SaaS の増分の取得は Snow Family を使う
- C. データベースの CDC は Transfer Family を使う
- D. SFTP の受け口には DataSync のエージェントを使う
- E. データベースの全件と変更の複製は DMS を使う

??? success "答えと解説"
    **正解: A, E**

    転送する対象で選びます。

    - A: 正しい。ファイルの転送に向きます。
    - B: 誤り。オフラインの移送です。
    - C: 誤り。ファイルの受け渡しのサービスです。
    - D: 誤り。受け口は Transfer Family です。
    - E: 正しい。全件ロードと CDC に対応します。

    **スキル:** [2.1.4](../domain2.md#skill-2-1-4) / **参照:** [AWS DMS](../../../services/migration.md#dms)、[サービスの比較](../../../services/migration.md#transfer-comparison)

### 問5 {#q5}

Transfer Family の公開エンドポイントについて正しいものはどれですか。

- A. FTP と FTPS にも対応し、セキュリティグループで接続元を制限できる
- B. SFTP だけに対応し、セキュリティグループで接続元を制限できない
- C. SFTP だけに対応し、セキュリティグループの指定が作成時の必須項目である
- D. すべてのプロトコルに対応し、Elastic IP も必ず割り当てられる

??? success "答えと解説"
    **正解: B**

    接続元を限定するなら VPC に置きます。

    - A: 誤り。公開エンドポイントは SFTP だけです。
    - B: 正しい。
    - C: 誤り。公開エンドポイントでは指定できません。
    - D: 誤り。固定の IP を使うなら VPC に置きます。

    **スキル:** [2.1.4](../domain2.md#skill-2-1-4) / **参照:** [AWS Transfer Family](../../../services/migration.md#transfer-family)、[セキュリティグループのルール](../../../services/networking.md#security-group-rules)

### 問6 {#q6}

Oracle から Aurora PostgreSQL へ移ります。スキーマとコードの変換は誰が担い、データは何で移しますか。

- A. スキーマは DMS のタスクが自動で完全に変換するので、変換の評価は要らない
- B. スキーマは DMS Schema Conversion か AWS SCT で変換し、データは DMS で移す
- C. スキーマは Glue のクローラーで推定し、データは Glue のブックマークで移す
- D. スキーマもデータも AWS SCT の変換だけで移し、DMS は使わない

??? success "答えと解説"
    **正解: B**

    異種間の移行は先にスキーマを変換します。

    - A: 誤り。DMS のタスク自体は変換のためのものではありません。
    - B: 正しい。
    - C: 誤り。クローラーは Data Catalog のテーブルの推定に使います。
    - D: 誤り。変換はスキーマとコードだけを扱います。データ抽出エージェントは DWH の移行の話です。

    **スキル:** [2.4.3](../domain2.md#skill-2-4-3) / **参照:** [AWS SCT と DMS Schema Conversion](../../../services/migration.md#sct)、[SCT と DMS](../../../services/data-engineering.md#sct-dms)

### 問7 {#q7}

MySQL から Aurora MySQL へ移ります。スキーマの変換のツールはどう扱いますか。

- A. 同種間でも、DMS Schema Conversion の評価が通らないと移行できない
- B. Aurora MySQL は MySQL と互換がないので、アプリの SQL を書き直す
- C. 同種間なのでスキーマ変換は不要で、DMS などでデータを移す
- D. 異種間なので AWS SCT と拡張パックが必ず必要である

??? success "答えと解説"
    **正解: C**

    同種の移行はスキーマ変換が要りません。

    - A: 誤り。同種の移行に変換は要りません。
    - B: 誤り。MySQL 互換です。
    - C: 正しい。
    - D: 誤り。同じエンジンの系統の移行です。

    **スキル:** [2.4.3](../domain2.md#skill-2-4-3) / **参照:** [AWS SCT と DMS Schema Conversion](../../../services/migration.md#sct)

### 問8 {#q8}

Netezza の DWH を Redshift へ移します。データの抽出も含め、分散キーの提案も受けたいです。どのツールですか。

- A. Transfer Family の SFTP で、テーブルを 1 つずつ受け取る
- B. DataSync のエージェントで転送する
- C. Glue のクローラーで推定して、Redshift に自動で作る
- D. AWS SCT とデータ抽出エージェント

??? success "答えと解説"
    **正解: D**

    SCT は Redshift のキーの提案と抽出エージェントを持ちます。

    - A: 誤り。スキーマの変換はしません。
    - B: 誤り。スキーマの変換はしません。
    - C: 誤り。DWH の変換の機能ではありません。
    - D: 正しい。

    **スキル:** [2.4.3](../domain2.md#skill-2-4-3) / **参照:** [AWS SCT と DMS Schema Conversion](../../../services/migration.md#sct)、[分散スタイル](../../../services/data-engineering.md#redshift-distribution)

### 問9 {#q9}

変換のターゲットのデータベースがまだない段階で、移行の難しさを評価します。DMS Schema Conversion で何を使いますか。また変換できない機能はどこで分かりますか。

- A. 仮想ターゲットで評価し、変換できない機能は評価レポートで確認する
- B. データ抽出エージェントで評価し、変換できない機能は Macie の結果で確認する
- C. 拡張パックで評価し、変換できない機能は CloudTrail のイベントで確認する
- D. ターゲットの作成が先に必須で、Glue のログで確認する

??? success "答えと解説"
    **正解: A**

    評価レポートに手作業の箇所が残ります。

    - A: 正しい。
    - B: 誤り。抽出エージェントは評価の機能ではありません。
    - C: 誤り。拡張パックは変換できない機能を補うものです。
    - D: 誤り。仮想ターゲットを使えます。

    **スキル:** [2.4.3](../domain2.md#skill-2-4-3) / **参照:** [AWS SCT と DMS Schema Conversion](../../../services/migration.md#sct)

### 問10 {#q10}

AWS SCT と DMS Schema Conversion の違いとして正しいものはどれですか。（2つ選択）

- A. SCT は S3 のオブジェクトだけを変換するサービスである
- B. SCT はダウンロードするデスクトップアプリである
- C. DMS Schema Conversion はデータも移すので DMS のタスクが不要である
- D. どちらも新しいターゲットのデータを自動で検証し、修復する
- E. DMS Schema Conversion は DMS のマネージド機能である

??? success "答えと解説"
    **正解: B, E**

    どちらもスキーマとコードだけを変換します。

    - A: 誤り。データベースのスキーマとコードを変換します。
    - B: 正しい。ローカルにインストールします。
    - C: 誤り。データは DMS のタスクで移します。
    - D: 誤り。スキーマとコードの変換のツールです。
    - E: 正しい。コンソールから使います。

    **スキル:** [2.4.3](../domain2.md#skill-2-4-3) / **参照:** [AWS SCT と DMS Schema Conversion](../../../services/migration.md#sct)、[AWS DMS](../../../services/migration.md#dms)

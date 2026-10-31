# Secrets Manager、Parameter Store、AppConfig の問題集

対象の解説: [Secrets Manager、Parameter Store、AppConfig](../../../services/secrets.md)

### 問1 {#q1}

データベースのパスワードを、毎週日曜の日本時間 2:00 から 2 時間以内に自動でローテーションします。`RotationRules` の設定として最も適切なものはどれですか。

- A. `{"ScheduleExpression":"cron(0 17 ? * SAT *)","Duration":"2h"}`
- B. `{"ScheduleExpression":"cron(0 2 ? * SUN *)","Duration":"2h"}`
- C. `{"AutomaticallyAfterDays":7,"ScheduleExpression":"rate(7 days)"}`
- D. `{"AutomaticallyAfterDays":7,"Duration":"30m"}`

??? success "答えと解説"
    **正解: A**

    スケジュールは UTC です。日本時間の日曜 2:00 は、土曜 17:00 UTC です。

    - A: 正しい。
    - B: 誤り。UTC の日曜 2:00 は日本時間の日曜 11:00。
    - C: 誤り。`AutomaticallyAfterDays` と `ScheduleExpression` は同時に指定できない。
    - D: 誤り。ウィンドウの最短は 1 時間で、開始時刻も指定できない。

    **スキル:** C03 2.2.7 / **参照:** [ローテーションのスケジュール](../../../services/secrets.md#rotation-schedule)

### 問2 {#q2}

Lambda によるローテーションで、`testSecret` のステップが失敗しました。アプリの `GetSecretValue` が返す値はどれですか。

- A. `AWSPENDING` の新しい値
- B. `AWSPREVIOUS` の 1 つ前の値
- C. `AWSCURRENT` の元の値
- D. エラーになり、値は返らない

??? success "答えと解説"
    **正解: C**

    `AWSCURRENT` が移るのは `finishSecret` です。指定がなければ `AWSCURRENT` が返ります。

    - A: 誤り。明示的に指定したときだけ返る。
    - B: 誤り。ラベルはまだ移っていない。
    - C: 正しい。ただしシングルユーザーで `setSecret` が終わっていれば、データベース側のパスワードと不一致になりうる。
    - D: 誤り。シークレットの取得自体は成功する。

    **スキル:** C03 2.2.7 / **参照:** [Lambda ローテーションの動き](../../../services/secrets.md#lambda-rotation-steps)

### 問3 {#q3}

Secrets Manager のバージョンの説明として正しいものを選んでください。（2つ選択）

- A. ラベルが付いたバージョンは自動では削除されない
- B. 100 を超えると、作成から 24 時間以内のものも削除される
- C. ラベルなしのバージョンは非推奨の扱いになる
- D. ラベルはバージョンごとに 20 個まで付けられる
- E. `AWSPREVIOUS` は 3 世代前まで保持する

??? success "答えと解説"
    **正解: A, C**

    100 を超えるとラベルなしのものを削除しますが、24 時間以内のものは残します。ラベルはシークレット全体で 20 個です。

    - A: 正しい。
    - B: 誤り。24 時間以内のものは削除しない。
    - C: 正しい。
    - D: 誤り。全バージョンの合計で 20。
    - E: 誤り。1 つ前の値に付くラベル。

    **スキル:** C03 2.2.7 / **参照:** [バージョンの扱い](../../../services/secrets.md#version-stages)

### 問4 {#q4}

テストの後、同じ名前のシークレットをすぐに作り直したいと考えています。`DeleteSecret` の指定として最も適切なものはどれですか。

- A. `RecoveryWindowInDays=0`
- B. `RecoveryWindowInDays=7`
- C. `ForceDeleteWithoutRecovery=true`
- D. `RecoveryWindowInDays=7` と `ForceDeleteWithoutRecovery=true` の両方

??? success "答えと解説"
    **正解: C**

    復旧期間は 7〜30 日（既定 30 日）です。すぐ消すなら `ForceDeleteWithoutRecovery` を使います。実際の削除は非同期なので、直後の作成は再試行が必要な場合があります。

    - A: 誤り。範囲外。
    - B: 誤り。7 日間は削除待ちのままで、同じ名前を使えない。
    - C: 正しい。
    - D: 誤り。同時に指定できない。

    **スキル:** C03 2.2.7 / **参照:** [削除と復旧](../../../services/secrets.md#recovery-window)

### 問5 {#q5}

東京のシークレットをオレゴンに複製しています。プライマリのシークレットを削除しようとすると失敗します。最も適切な手順はどれですか。

- A. `RemoveRegionsFromReplication` でレプリカを消してから、プライマリを削除する
- B. レプリカ側で `RotateSecret` を実行してから、プライマリを削除する
- C. `ForceDeleteWithoutRecovery` を付けてプライマリを削除する
- D. キーを AWS 管理キーに変えてから、プライマリを削除する

??? success "答えと解説"
    **正解: A**

    複製先があるプライマリは削除できません。レプリカの削除はすぐに実行されます。

    - A: 正しい。
    - B: 誤り。ローテーションは削除と関係なく、プライマリで実行するもの。
    - C: 誤り。レプリカがあれば削除できない。
    - D: 誤り。キーは関係がない。

    **スキル:** C03 2.2.7 / **参照:** [他リージョンへの複製](../../../services/secrets.md#secret-replication)

### 問6 {#q6}

Lambda に Parameters and Secrets Lambda Extension を導入しました。ローテーションの直後に 1 分以内で新しい値を使うようにしたいと考えています。最も適切な設定はどれですか。

- A. `SECRETS_MANAGER_TTL` を `3600` にする
- B. `SECRETS_MANAGER_TTL` を `60` にする
- C. `PARAMETERS_SECRETS_EXTENSION_HTTP_PORT` を変更する
- D. `SECRETS_MANAGER_TIMEOUT_MILLIS` を `60000` にする

??? success "答えと解説"
    **正解: B**

    TTL は既定 300 秒で、0〜300 秒です。短くすると API 呼び出しは増えます。

    - A: 誤り。範囲外で、方向も逆。
    - B: 正しい。
    - C: 誤り。ポートはキャッシュと関係がない。
    - D: 誤り。リクエストのタイムアウトである。

    **スキル:** C03 2.2.7 / **参照:** [キャッシュの選び方](../../../services/secrets.md#caching-choice)

### 問7 {#q7}

CloudFormation で RDS のパスワードに `{{resolve:secretsmanager:prod/db:SecretString:password}}` を使っています。Secrets Manager で値を更新しましたが、変更がありません。正しい説明を選んでください。（2つ選択）

- A. シークレットの更新だけでは、CloudFormation は値を取り直さない
- B. そのプロパティを持つリソースの更新時に値を取得する
- C. CloudFormation はスタックを自動で更新する
- D. ドリフト検出で変更を検知できる
- E. テンプレートの動的参照を外して平文にするのが推奨である

??? success "答えと解説"
    **正解: A, B**

    動的参照はそのリソースの作成や更新の時だけ解決されます。

    - A: 正しい。
    - B: 正しい。
    - C: 誤り。自動では更新しない。
    - D: 誤り。動的参照はドリフト検出の対象外。
    - E: 誤り。平文を残すのは避ける。

    **スキル:** C03 2.2.7 / **参照:** [CloudFormation の動的参照](../../../services/secrets.md#dynamic-references)

### 問8 {#q8}

EC2 の `UserData` に `{{resolve:ssm-secure:/prod/token:1}}` を書きましたが、値が解決されません。最も適切な説明はどれですか。

- A. バージョン番号を省略していないため
- B. `SecureString` のキーがカスタマー管理キーでないため
- C. 動的参照は `UserData` では使えないため
- D. 動的参照の数が 60 を超えたため

??? success "答えと解説"
    **正解: C**

    `UserData` と `AWS::CloudFormation::Init` メタデータでは動的参照を使えません。

    - A: 誤り。バージョンの指定は問題ではない。
    - B: 誤り。キーの種類は関係がない。
    - C: 正しい。アプリの起動時に `GetParameter` で取得する。
    - D: 誤り。1 つなら上限に達しない。

    **スキル:** C03 2.2.7 / **参照:** [CloudFormation の動的参照](../../../services/secrets.md#dynamic-references)

### 問9 {#q9}

既定のパラメータティアに `Intelligent-Tiering` を設定しました。次のうち、Advanced で作成される条件を選んでください。（2つ選択）

- A. 値が 5 KB である
- B. `String` 型である
- C. パラメータポリシーを指定している
- D. 階層が 3 階層である
- E. 値が 3 KB の `SecureString` である

??? success "答えと解説"
    **正解: A, C**

    4 KB を超える値、パラメータポリシー、10,000 個を超えた状況で Advanced になります。

    - A: 正しい。
    - B: 誤り。型は条件ではない。
    - C: 正しい。
    - D: 誤り。階層の深さは条件ではない。
    - E: 誤り。4 KB 以下で、`SecureString` は条件ではない。

    **スキル:** C03 3.1.4 / **参照:** [ティアの選択](../../../services/secrets.md#tier-selection)

### 問10 {#q10}

90 日後に削除される API トークンを Parameter Store に置き、削除の 15 日前に担当者へ通知します。最も適切なものはどれですか。

- A. Standard ティアと `Expiration` ポリシー
- B. Standard ティアと EventBridge のスケジュール
- C. Advanced ティアと `NoChangeNotification`、`Expiration` ポリシー
- D. Advanced ティアと `Expiration`、`ExpirationNotification` ポリシー

??? success "答えと解説"
    **正解: D**

    ポリシーは Advanced のみです。`ExpirationNotification` は期限の前に EventBridge にイベントを送ります。

    - A: 誤り。Standard ではポリシーを使えない。
    - B: 誤り。削除も自前で実装することになる。
    - C: 誤り。`NoChangeNotification` は変更がない場合の通知。
    - D: 正しい。

    **スキル:** C03 3.1.4 / **参照:** [パラメータポリシー](../../../services/secrets.md#parameter-policies)

### 問11 {#q11}

コードで `get_parameters_by_path(Path="/prod/orders")` を呼ぶと、`/prod/orders/timeout` は返りますが、`/prod/orders/db/host` が返りません。最も適切な修正はどれですか。

- A. `Recursive=True` を指定する
- B. `MaxResults=100` を指定する
- C. `WithDecryption=True` を指定する
- D. `GetParameters` に置き換えて、パスを渡す

??? success "答えと解説"
    **正解: A**

    `Recursive` がないと、直下の階層だけを返します。結果が分割されるので、ページネーターも使います。

    - A: 正しい。
    - B: 誤り。`MaxResults` の範囲は 1〜10。
    - C: 誤り。`SecureString` の復号の指定である。
    - D: 誤り。`GetParameters` は名前で指定し、1 回 10 個まで。

    **スキル:** C03 3.1.4 / **参照:** [階層と取得](../../../services/secrets.md#parameter-retrieval)

### 問12 {#q12}

パラメータにはすでに 100 バージョンがあり、最古のバージョンにラベル `prod` が付いています。`PutParameter` で更新すると、どうなりますか。

- A. ラベルが外れて最古のバージョンが削除される
- B. 上限が自動で 200 に増える
- C. `ParameterMaxVersionLimitExceeded` で失敗する
- D. ラベルのない最新のバージョンが上書きされる

??? success "答えと解説"
    **正解: C**

    通常は最古のものを削除しますが、ラベルがあると削除しません。ラベルを移してから更新します。

    - A: 誤り。ラベルは自動で外れない。
    - B: 誤り。上限は 100。
    - C: 正しい。
    - D: 誤り。上書きしない。

    **スキル:** C03 3.1.4 / **参照:** [バージョンとラベル](../../../services/secrets.md#parameter-versions)

### 問13 {#q13}

100 個の Lambda が起動時に同時に `GetParameter` を呼ぶと、`ThrottlingException` が発生します。既定のスループットの設定です。最も運用負荷が低い対応はどれですか。

- A. パラメータを 1 つずつ Advanced に変更する
- B. パラメータごとに `Tier` を `Intelligent-Tiering` にする
- C. パラメータを別のリージョンに分散する
- D. 拡張でキャッシュし、それでも足りなければ高スループットを有効にする

??? success "答えと解説"
    **正解: D**

    取得は 3 つの API 合計で 40 TPS です。高スループットはティアではなく、アカウントとリージョンの設定です。

    - A: 誤り。ティアはスループットと関係がない。
    - B: 誤り。同じ理由で効果がない。
    - C: 誤り。運用が複雑になる。
    - D: 正しい。

    **スキル:** C03 3.1.4 / **参照:** [スループット](../../../services/secrets.md#parameter-throughput)

### 問14 {#q14}

AppConfig で `LINEAR`、`GrowthFactor=25`、`DeploymentDurationInMinutes=40`、`FinalBakeTimeInMinutes=10` の戦略を使います。環境にはアラームを設定しています。動作として最も適切なものはどれですか。

- A. 10 分ごとに 25% ずつ配布し、100% の後に 10 分監視する
- B. 25 分ごとに 40% ずつ配布する
- C. 配布が 40 分を超えるとタイムアウトで失敗する
- D. 100% 配布の後はアラームを見ない

??? success "答えと解説"
    **正解: A**

    4 ステップを 40 分で処理するので、10 分ごとです。デプロイ時間はタイムアウトではありません。

    - A: 正しい。
    - B: 誤り。項目の読み方が違う。
    - C: 誤り。処理する時間の幅であり、タイムアウトではない。
    - D: 誤り。ベイク時間の間は監視する。

    **スキル:** C03 3.1.4 / **参照:** [デプロイ戦略の項目](../../../services/secrets.md#strategy-fields)

### 問15 {#q15}

自前のコードで `GetLatestConfiguration` をポーリングすると、2 回目から設定が空になり、機能が停止しました。最も適切な修正はどれですか。

- A. 毎回 `StartConfigurationSession` を呼ぶ
- B. `RequiredMinimumPollIntervalInSeconds` を 5 にする
- C. 同じ `InitialConfigurationToken` を再利用する
- D. 空の応答では前回の値を使い続け、次のトークンで呼ぶ

??? success "答えと解説"
    **正解: D**

    空の応答は、すでに最新を持っているという意味です。トークンは 1 回限りで、`NextPollConfigurationToken` を次に使います。

    - A: 誤り。セッションは 1 回だけ作る。
    - B: 誤り。範囲は 15〜86,400 秒。
    - C: 誤り。トークンは再利用できない。
    - D: 正しい。

    **スキル:** C03 3.1.4 / **参照:** [取得とポーリング](../../../services/secrets.md#polling-settings)

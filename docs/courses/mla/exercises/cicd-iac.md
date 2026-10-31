# CI/CD、コンテナ、IaC の問題集

対象の解説: [CodeBuild](../../../services/cicd.md#codebuild)、[ECR](../../../services/containers.md#ecr)、[出力とエクスポート](../../../services/iac.md#outputs-exports)、[Inspector](../../../services/threat-detection.md#inspector)

### 問1 {#q1}

ネットワークのチームが管理するスタックの VPC ID を、ML のチームのスタックで使います。同じアカウントとリージョンです。どの方法ですか。

- A. `Export` と `ImportValue`
- B. VPC ID をテンプレートに直接書く
- C. Service Catalog の製品の一覧に記録する
- D. ネストされたスタックで親から子へ毎回渡す

??? success "答えと解説"
    **正解: A**

    別のチームが管理する VPC の ID などは `Export` と `ImportValue` で渡します。

    - A: 正しい。
    - B: 誤り。変更に追従できず、チーム間の依存も見えません。
    - C: 誤り。承認された構成をセルフサービスで作る機能で、値の受け渡しではありません。
    - D: 誤り。再利用する部品を親と一緒に更新する方法で、別のチームのスタックの連携には向きません。

    **スキル:** [3.2.2](../domain3.md#skill-3-2-2) / **参照:** [出力とエクスポート](../../../services/iac.md#outputs-exports)、[ネストとエクスポートの比較](../../../services/iac.md#nested-vs-exports)

### 問2 {#q2}

`Export` している値を別のスタックが参照しています。値を変更しようとすると失敗しました。正しい手順はどれですか。

- A. `DependsOn` を追加してから更新する
- B. `Export` の名前だけ変えて更新する
- C. `Export` の側のスタックを先に削除する
- D. 先に参照側のスタックを変更する

??? success "答えと解説"
    **正解: D**

    参照されている `Export` は値の変更もスタックの削除もできません。先に参照側を変えます。

    - A: 誤り。参照の制約は解除されません。
    - B: 誤り。参照されている `Export` は変更できません。
    - C: 誤り。参照されている間は削除できません。
    - D: 正しい。

    **スキル:** [3.2.2](../domain3.md#skill-3-2-2) / **参照:** [出力とエクスポート](../../../services/iac.md#outputs-exports)

### 問3 {#q3}

データサイエンティストが、承認された構成の学習環境を自分で作れるようにします。IAM の管理者の手間も減らします。どのサービスですか。

- A. CloudFormation StackSets
- B. AWS Config の適合パック
- C. Service Catalog
- D. Trusted Advisor のコスト最適化のチェック

??? success "答えと解説"
    **正解: C**

    Service Catalog は承認された構成をセルフサービスで作れるようにします。

    - A: 誤り。スタックを複数のアカウントへ配布する機能で、利用者のセルフサービスの仕組みではありません。
    - B: 誤り。準拠の評価の機能で、環境を作りません。
    - C: 正しい。
    - D: 誤り。幅広い点検です。

    **スキル:** [3.2.2](../domain3.md#skill-3-2-2) / **参照:** [Service Catalog](../../../services/governance.md#service-catalog)

### 問4 {#q4}

SageMaker AI のビルド済みのイメージに必要なパッケージがそろっていますが、OS のライブラリを 1 つ足します。手間の小さい順で最初に選ぶ方法はどれですか。

- A. 独自のコンテナをゼロから作る
- B. ビルド済みイメージを拡張する
- C. `requirements.txt` に OS のライブラリを書く
- D. 実行中のコンテナに SSH で入り、手で入れる

??? success "答えと解説"
    **正解: B**

    順に、そのまま使う、`requirements.txt`、ビルド済みイメージの拡張、独自のコンテナ、です。OS のライブラリなら拡張します。

    - A: 誤り。対応しないフレームワークのときの方法です。
    - B: 正しい。
    - C: 誤り。Python のパッケージを足す方法で、OS のライブラリは入りません。
    - D: 誤り。再現できず、SageMaker AI の動作でもありません。

    **スキル:** [3.2.3](../domain3.md#skill-3-2-3) / **参照:** [Dockerfile](../../../services/containers.md#dockerfile)

### 問5 {#q5}

ECR のモデルのイメージを維持します。適切な運用を選んでください。（2つ選択）

- A. 本番でも `latest` だけを使う
- B. 参照にはコミットタグかダイジェストを使う
- C. スキャンは初回のプッシュのときだけに限る
- D. 不要なイメージはライフサイクルポリシーで消す
- E. 全員に `ecr:*` を付ける

??? success "答えと解説"
    **正解: B, D**

    参照にはコミットタグかダイジェストを使います。ライフサイクルとスキャンで維持します。

    - A: 誤り。中身が変わるので、どの版が動いているか分からなくなります。
    - B: 正しい。どのイメージが動いているかを特定できます。
    - C: 誤り。新しい脆弱性を見逃します。
    - D: 正しい。ストレージの費用を抑えられます。
    - E: 誤り。最小権限に反します。

    **スキル:** [3.2.3](../domain3.md#skill-3-2-3) / **参照:** [ライフサイクル](../../../services/containers.md#ecr-lifecycle)、[スキャン](../../../services/containers.md#ecr-scanning)

### 問6 {#q6}

SageMaker AI のビルド済みのイメージを使っています。実行ロールに ECR を拒否する IAM ポリシーを付けました。イメージの取得はどうなりますか。

- A. 止まらない。ただし CPU のイメージに限る
- B. 必ず失敗する。ECR の VPC エンドポイントを追加して取得する
- C. 必ず失敗する。ポリシーを外す
- D. 止まらない。サービス側の認証情報で取得するため

??? success "答えと解説"
    **正解: D**

    ビルド済みのイメージは SageMaker AI のサービス側の認証情報で取得するので、ECR を拒否する IAM ポリシーがあっても止まりません。

    - A: 誤り。CPU か GPU かで変わる動作ではありません。
    - B: 誤り。権限の話で、VPC エンドポイントの問題ではありません。
    - C: 誤り。ビルド済みのイメージは SageMaker AI のサービス側の認証情報で取得します。
    - D: 正しい。

    **スキル:** [3.2.3](../domain3.md#skill-3-2-3) / **参照:** [ECR](../../../services/containers.md#ecr)

### 問7 {#q7}

CodeBuild で推論のコンテナをビルドして ECR にプッシュします。`docker build` と権限のエラーが続きます。確認する設定を選んでください。（2つ選択）

- A. CodeBuild のキャッシュが有効か
- B. ECR のライフサイクルポリシーの保持数
- C. サービスロールに ECR の権限があるか
- D. CodeCommit の新規受付が終了していないか
- E. 特権モードが有効か

??? success "答えと解説"
    **正解: C, E**

    CodeBuild ではロールに ECR の権限が必要で、Docker のビルドには特権モードが必要です。

    - A: 誤り。ビルドを速くする設定で、このエラーの原因ではありません。
    - B: 誤り。古いイメージを消す設定で、ビルドや権限のエラーの原因ではありません。
    - C: 正しい。プッシュに必要です。
    - D: 誤り。2025 年 11 月に一般提供へ戻りました。ビルドのエラーとも関係ありません。
    - E: 正しい。Docker のビルドに必要です。

    **スキル:** [3.3.2](../domain3.md#skill-3-3-2) / **参照:** [CodeBuild](../../../services/cicd.md#codebuild)

### 問8 {#q8}

GitHub のリポジトリをパイプラインのソースにしました。接続が「保留中」のままで動きません。原因として最も適切なものはどれですか。

- A. CodeDeploy のライフサイクルフックのスクリプトが失敗している
- B. CodeConnections の接続の承認が済んでいない
- C. `buildspec.yml` の書き方が誤っている
- D. ECR のスキャンが有効になっている

??? success "答えと解説"
    **正解: B**

    GitHub、GitLab、Bitbucket との接続には CodeConnections を使います。接続の承認が必要です。

    - A: 誤り。ソースより後の工程の話です。
    - B: 正しい。
    - C: 誤り。ビルドの工程の話で、接続の状態とは別です。
    - D: 誤り。ソースの接続に関係しません。

    **スキル:** [3.3.2](../domain3.md#skill-3-3-2) / **参照:** [ソース管理](../../../services/cicd.md#source-control)

### 問9 {#q9}

2026 年に新しい ML プロジェクトで CodeCommit を検討しています。「新規に使えないはず」という指摘が出ました。正しい説明はどれですか。

- A. 既存の顧客しか使えない
- B. 東京リージョンでしか使えない
- C. 2025 年 11 月に一般提供へ戻ったので使える
- D. 2024 年に新規受付を止めたので、今も新規には使えない

??? success "答えと解説"
    **正解: C**

    CodeCommit は 2025 年 11 月に一般提供へ戻りました。古い説明に注意します。大きなファイルやデータの置き場にはしません。

    - A: 誤り。2025 年 11 月に一般提供へ戻りました。
    - B: 誤り。リージョンの話ではありません。
    - C: 正しい。
    - D: 誤り。2024 年に新規受付を止めましたが、その後戻りました。

    **スキル:** [3.3.2](../domain3.md#skill-3-3-2) / **参照:** [CodeCommit の現状](../../../services/cicd.md#codecommit-status)

### 問10 {#q10}

CI/CD の中でコンテナイメージの脆弱性を検査し、重大な検出があればデプロイを止めます。適切な実装はどれですか。

- A. Inspector で検査し、CodeBuild のステップを失敗させる
- B. デプロイの後に CloudWatch のエラー率を確認して問題があれば戻す
- C. Macie でイメージを検査する
- D. CloudTrail のイベントを手で確認する

??? success "答えと解説"
    **正解: A**

    Inspector の Scan API などで検査し、重大な検出結果が出たら CodeBuild のステップを失敗させてデプロイを止めます。

    - A: 正しい。
    - B: 誤り。脆弱性の検査になりません。
    - C: 誤り。S3 の機密データの検出です。
    - D: 誤り。API の記録で、イメージの検査とは別です。

    **スキル:** [4.3.1](../domain4.md#skill-4-3-1) / **参照:** [Inspector](../../../services/threat-detection.md#inspector)、[ECR のスキャン](../../../services/threat-detection.md#inspector-ecr)

### 問11 {#q11}

ECR の拡張スキャンの結果をきっかけに、自動で担当者へ通知します。どの連携ですか。

- A. EventBridge のルールで SNS に送る
- B. ECR のライフサイクルポリシーで通知する
- C. CloudWatch Logs のサブスクリプションで送る
- D. CloudTrail のログを人が読む

??? success "答えと解説"
    **正解: A**

    拡張スキャンの結果は EventBridge に送られます。ルールで SNS などへ通知できます。

    - A: 正しい。
    - B: 誤り。イメージを消す機能で、通知しません。
    - C: 誤り。ログを配信する機能で、スキャンの結果のイベントを受ける仕組みではありません。
    - D: 誤り。自動の通知になりません。

    **スキル:** [4.3.1](../domain4.md#skill-4-3-1) / **参照:** [ECR のスキャン](../../../services/threat-detection.md#inspector-ecr)

### 問12 {#q12}

新しいプロジェクトで学習コードの静的スキャンを導入します。CodeGuru Security を使う案が出ました。正しい判断はどれですか。

- A. 適切である。新規機能が追加され続けている
- B. 適切でない。Inspector の Code Security を使う
- C. 適切でない。コードのスキャンは AWS にはない
- D. 適切である。CodeGuru Reviewer に新しいリポジトリを関連付ければ同じである

??? success "答えと解説"
    **正解: B**

    現在のコードのスキャンは Inspector の Code Security が担います。試験で CodeGuru が出たら、パイプラインでの静的スキャンの役割として読みます。

    - A: 誤り。CodeGuru Security は 2025-11-20 にサポートを終了しました。
    - B: 正しい。
    - C: 誤り。Inspector の Code Security が担います。
    - D: 誤り。Reviewer も新しいリポジトリを関連付けられません。

    **スキル:** [4.3.1](../domain4.md#skill-4-3-1) / **参照:** [コードのスキャン](../../../services/threat-detection.md#inspector-code)、[CodeGuru Security](../../../services/threat-detection.md#codeguru-security)

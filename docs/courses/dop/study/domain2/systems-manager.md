# 分野2: Systems Manager と自動化

対象と頻度から、適切な自動化の手段を選ぶ力を問います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [構成管理](../../domain2.md#t2-1-config-management) | 構成管理のサービスと戦略、最適な構成管理サービスの判断 |
| [自動化に使うサービス](../../domain2.md#t2-3-automation-services) | 自動化に使うサービス |
| [AWS を操作する方法](../../domain2.md#t2-3-interfaces) | AWS を操作する方法と戦略 |
| [インベントリとパッチ](../../domain2.md#t2-3-inventory-patch) | インベントリ、構成、パッチの自動化 |
| [望ましい状態](../../domain2.md#t2-3-desired-state) | ソフトウェアを望ましい状態に保つ |
| [準拠の維持](../../domain2.md#t2-3-compliance) | ソフトウェアの準拠の維持 |

## 学習の順番 {#study-order}

1. [Automation](../../../../services/operations.md#automation): AWS API と手順の定型作業、複数アカウントの実行を確認します。
2. [State Manager と Maintenance Windows の違い](../../../../services/operations.md#state-vs-maintenance): State Manager と Maintenance Windows の違いを押さえます。
3. [実行の設定方法](../../../../services/operations.md#patch-methods): パッチポリシーと他の方法の範囲を比べます。
4. [Inventory](../../../../services/operations.md#inventory): リソースデータ同期と Athena の流れを理解します。
5. [マネージドノードの条件](../../../../services/operations.md#managed-nodes): マネージドノードの 3 つの条件を覚えます。
6. [AWS AppConfig](../../../../services/secrets.md#appconfig): アプリの設定の段階的な配布を確認します。
7. [AWS License Manager](../../../../services/governance.md#license-manager): ライセンスの上限の仕組みを押さえます。

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 状態を保ち続ける | State Manager の関連付け |
| 決まった時間帯にだけ実行する | Maintenance Windows |
| 一度だけ全台で実行する | Run Command |
| 組織全体のパッチ | Quick Setup のパッチポリシー |
| 適用せずに報告だけ | `AWS-RunPatchBaseline` の `Scan` |
| 機能フラグを段階的に配り、アラームで戻す | AppConfig |
| ノードにある全パッケージを SQL で調べる | Inventory とリソースデータ同期と Athena |

## 引っかかりやすい点 {#traps}

- OpsWorks は終了しました。Chef のレシピは `AWS-ApplyChefRecipes` で実行できます。
- SSM Agent は外向きの通信を使うので、受信の許可は要りません。
- `--page-size` は全件を取得したまま、呼び出しごとの件数を減らします。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [systems-manager 問1](../../exercises/systems-manager.md#q1) | 構成管理 | 数百台のサーバーで動くアプリの機能フラグの値を、営業時間中に変更します。全サーバーへ段階的に反映し、… |
| [systems-manager 問2](../../exercises/systems-manager.md#q2) | 構成管理 | 次の 3 つの要件があります。(1) EC2 の中の NTP の設定を望ましい状態に保つ。(2) S… |
| [systems-manager 問3](../../exercises/systems-manager.md#q3) | 構成管理 | チーム内で「構成管理はどのサービスか」で議論になりました。担当者の発言のうち正しいものはどれですか。 |
| [systems-manager 問4](../../exercises/systems-manager.md#q4) | 自動化に使うサービス | 全リージョンと全アカウントの未使用の EBS を週 1 回調べて、スナップショットを取ってから削除し… |
| [systems-manager 問5](../../exercises/systems-manager.md#q5) | 自動化に使うサービス | 次の作業の手段を選びます。(1) 毎月第 2 日曜の深夜 2 時間の間に限り、本番サーバーでパッチの… |
| [systems-manager 問6](../../exercises/systems-manager.md#q6) | 自動化に使うサービス | EC2 の AMI の更新の手順があります。インスタンスの停止、AMI の作成、タグの付与の 3 工… |
| [systems-manager 問7](../../exercises/systems-manager.md#q7) | AWS を操作する方法 | 監査の要件で、SSH のポートを閉じ、踏み台を廃止します。操作の記録も残します。担当者はノート PC… |
| [systems-manager 問8](../../exercises/systems-manager.md#q8) | AWS を操作する方法 | AWS CLI のスクリプトを見直します。条件は次のとおりです。(1) 応答から必要な値だけを取り出… |
| [systems-manager 問9](../../exercises/systems-manager.md#q9) | AWS を操作する方法 | Lambda で組織の全アカウントのリソースの一覧を集める処理を作ります。Throttling でと… |
| [systems-manager 問10](../../exercises/systems-manager.md#q10) | インベントリとパッチ | 10 リージョン、200 アカウントのインスタンスに、スキャンと適用を別の日程でパッチを当てます。新… |
| [systems-manager 問11](../../exercises/systems-manager.md#q11) | インベントリとパッチ | 監査で、全アカウントの全ノードで openssl の特定のバージョンが入っているものの一覧を求められ… |
| [systems-manager 問12](../../exercises/systems-manager.md#q12) | インベントリとパッチ | パッチの報告で、プライベートサブネットの 30 台だけが「未管理」です。OS には SSM Agen… |
| [systems-manager 問13](../../exercises/systems-manager.md#q13) | 望ましい状態 | 全サーバーで、社内の EDR の設定ファイルとサービスの起動を保ちます。担当者が手で変更しても、1 … |
| [systems-manager 問14](../../exercises/systems-manager.md#q14) | 望ましい状態 | OpsWorks Stacks で運用していた Chef のクックブックを捨てずに、同じ構成の管理を… |
| [systems-manager 問15](../../exercises/systems-manager.md#q15) | 望ましい状態 | 夜間だけ止められるサーバーがあります。セキュリティエージェントの導入状態は常に確認したいのですが、再… |
| [systems-manager 問16](../../exercises/systems-manager.md#q16) | 準拠の維持 | ある企業は商用データベースのライセンスを 500 コアだけ持っています。契約を超えるインスタンスの起… |
| [systems-manager 問17](../../exercises/systems-manager.md#q17) | 準拠の維持 | 組織の方針で、禁止のソフトウェアが入ったノードを検出し、全社の準拠の状況を一か所で確認します。組織の… |
| [systems-manager 問18](../../exercises/systems-manager.md#q18) | 準拠の維持 | パッチの報告が必要な本番と、変更の凍結中のサーバーがあります。凍結の間は適用せずに報告だけを続けます… |

<!-- questions:end -->

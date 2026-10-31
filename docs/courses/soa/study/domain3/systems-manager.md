# 分野3: Systems Manager による自動化

マネージドノードの条件と、機能の選択を問います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [3.2.1](../../domain3.md#skill-3-2-1) | Systems Manager による自動化 |

## 学習の順番 {#study-order}

1. [マネージドノードの条件](../../../../services/operations.md#managed-nodes): 3 つの条件を覚えます。
2. [Run Command](../../../../services/operations.md#run-command)と[Session Manager](../../../../services/operations.md#session-manager): 実行とログインの機能を区別します。
3. [Patch Manager](../../../../services/operations.md#patch-manager)、[パッチベースライン](../../../../services/operations.md#patch-baselines)と[実行の設定方法](../../../../services/operations.md#patch-methods): ベースラインと設定の方法を確認します。
4. [State Manager と Maintenance Windows の違い](../../../../services/operations.md#state-vs-maintenance): State Manager と Maintenance Windows の違いを確認します。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| 定義済みのベースライン | 多くの OS でリリースから 7 日待つ | 早めるならカスタム |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| フリートに表示されない | Agent、ロール、エンドポイントへの経路 |
| SSH なしでログインする | Session Manager |
| 望ましい状態を保つ | State Manager |
| 土曜の深夜だけ実行 | Maintenance Windows |
| 組織全体のパッチ適用 | Quick Setup のパッチポリシー |

## 引っかかりやすい点 {#traps}

- ポート転送のセッションの内容はログに残せません。
- Change Manager と Incident Manager は新規受付を終了しています。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [systems-manager 問12](../../exercises/systems-manager.md#q12) | 3.2.1 | プライベートサブネットの EC2 が Fleet Manager に表示されません。SSM Agen… |
| [systems-manager 問13](../../exercises/systems-manager.md#q13) | 3.2.1 | 踏み台サーバーをなくし、ポート 22 を閉じたまま、Linux のインスタンスにログインして操作を記… |
| [systems-manager 問14](../../exercises/systems-manager.md#q14) | 3.2.1 | Session Manager のログの設定を有効にしましたが、データベースへのポート転送のセッショ… |
| [systems-manager 問15](../../exercises/systems-manager.md#q15) | 3.2.1 | 定義済みのパッチベースラインで運用しています。リリース直後のパッチを、7 日より早く適用するよう求め… |
| [systems-manager 問16](../../exercises/systems-manager.md#q16) | 3.2.1 | 新しく起動したインスタンスにも自動で CloudWatch エージェントの設定を当て、望ましい状態を… |
| [systems-manager 問17](../../exercises/systems-manager.md#q17) | 3.2.1 | 本番のパッチの適用を、毎週土曜の深夜 2 時間だけに限りたいと考えています。どれが適切ですか。 |
| [systems-manager 問18](../../exercises/systems-manager.md#q18) | 3.2.1 | 組織の複数のアカウントとリージョンのパッチ適用を、1 か所で設定したいと考えています。最も運用負荷の… |

<!-- questions:end -->

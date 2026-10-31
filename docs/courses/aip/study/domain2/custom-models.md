# 分野2: モデルのホスト

Bedrock と SageMaker AI の方式を選び、LLM に特有のスケーリングと資源の均衡を判断します。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [2.2.1](../../domain2.md#skill-2-2-1) | 要件に応じた FM のデプロイ |
| [2.2.2](../../domain2.md#skill-2-2-2) | LLM に特有のデプロイの課題 |
| [2.2.3](../../domain2.md#skill-2-2-3) | 性能と資源の均衡 |

## 学習の順番 {#study-order}

1. [デプロイ戦略](../../../../services/genai-apps.md#deployment)と[スループットの選択肢](../../../../services/ai.md#throughput-options): 方式ごとの課金と注意を比べます。
2. [自動スケーリング](../../../../services/sagemaker.md#autoscaling): 指標ごとの使いどころを覚えます。
3. [推論コンポーネント](../../../../services/sagemaker.md#multi-model): GPU の共有と 0 までの縮小を理解します。
4. [モデルカスタマイズ](../../../../services/genai-apps.md#customization)と[動的なモデル切り替え](../../../../services/genai-apps.md#dynamic-model-selection): 蒸留とカスケードの使いどころを確認します。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| Reserved の最小 | 入力 100,000 TPM、出力 10,000 TPM | アカウントチーム経由 |
| 同時リクエストの高解像度の指標 | 10 秒 | 急増に速く反応する |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 断続的な負荷 | Lambda からオンデマンド |
| ダウンタイムを許せない大きな負荷 | Reserved ティア |
| 独自の重み、GPU の制御 | SageMaker AI のエンドポイント |
| 応答が遅いのにスケールしない | 同時リクエスト数の指標へ |
| 上位の品質を保って安くする | 蒸留 |

## 引っかかりやすい点 {#traps}

- CPU 使用率は LLM の負荷を反映しません。
- Provisioned Throughput はコミットメントの期間中は削除できません。
- 0 まで縮小すると、起動中のリクエストは失敗します。
- カスケードは上位へ回す割合が高いと、2 回呼ぶ分だけ高くなります。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [custom-models 問5](../../exercises/custom-models.md#q5) | 2.2.1 | ある SaaS は、平日の日中に毎分大量のトークンを安定して消費します。ダウンタイムは契約上許されず… |
| [custom-models 問6](../../exercises/custom-models.md#q6) | 2.2.1 | ある社内アプリは、1 日に数回だけ呼ばれ、利用のない時間が長く続きます。チームは「本番なので」と P… |
| [custom-models 問7](../../exercises/custom-models.md#q7) | 2.2.1 | 通常の問い合わせは Bedrock の既製モデルで処理し、特殊な検査レポートの処理だけは社内で調整し… |
| [custom-models 問8](../../exercises/custom-models.md#q8) | 2.2.2 | SageMaker AI で LLM を自前でホストしています。CPU 使用率でターゲット追跡を設定… |
| [custom-models 問9](../../exercises/custom-models.md#q9) | 2.2.2 | 大きなモデルをホストしていて、スケールアウトしてから新しいインスタンスが処理を始めるまでに長い時間が… |
| [custom-models 問10](../../exercises/custom-models.md#q10) | 2.2.2 | 夜間はほとんど利用のない複数の LLM を SageMaker AI で提供しています。GPU のア… |
| [custom-models 問11](../../exercises/custom-models.md#q11) | 2.2.3 | 問い合わせの 80% は簡単で、小さなモデルで十分です。残りには上位のモデルが必要です。提供者をまた… |
| [custom-models 問12](../../exercises/custom-models.md#q12) | 2.2.3 | 上位のモデルで作った要約の品質は十分ですが、件数が多く費用が課題です。プロンプトと呼び出しログは揃っ… |
| [custom-models 問13](../../exercises/custom-models.md#q13) | 2.2.3 | 毎日大量の問い合わせを 5 つのカテゴリに分類します。今は最上位の FM を使っており、応答の品質は… |

<!-- questions:end -->

# 分野1: ストレージ

分野1では、S3、EBS、EFS の使い分けと、Lambda から EFS を使う設定を問われます。範囲が狭いので、短時間で済ませられます。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [1.2.1](../../domain1.md#skill-1-2-1) | VPC 内の EFS への Lambda からのアクセス |
| [1.3.1](../../domain1.md#skill-1-3-1) | データの保持 |
| [1.3.2](../../domain1.md#skill-1-3-2) | アクセスパターンに応じた選択 |

## 学習の順番 {#study-order}

1. [比較](../../../../services/storage.md#comparison): EBS、EFS、S3 の違いと、Lambda から使えるかを確認します。
2. [Lambda](../../../../services/storage.md#efs-lambda): マウントの要件、`FileSystemConfigs`、接続エラーを覚えます。
3. [データの保持](../../../../services/storage.md#retention): サービスごとの仕組みと `DeleteOnTermination` の既定を押さえます。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| EFS のポート | 2049 | セキュリティグループで許可します |
| Lambda のマウントパス | `/mnt/` で始まる | |
| EFS のライフサイクル | 30 日で IA、90 日で Archive | デフォルトでは Standard に戻りません |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 複数の EC2 と Lambda でファイルを共有する | EFS を使います |
| Lambda で `/tmp` では足りない、永続化したい | EFS を `/mnt/` にマウントするか、S3 を使います |
| EC2 の起動ディスク | EBS を使います |
| インスタンス終了後もデータを残す | `DeleteOnTermination` を `false` にします |
| EBS を別の AZ で使う | スナップショットから新しいボリュームを作ります |
| `EFSMountConnectivityException` が一部の呼び出しで出る | AZ ごとのマウントターゲットと 2049 番の通信を確認します |

## 引っかかりやすい点 {#traps}

- Lambda の `FileSystemConfigs` の `Arn` は EFS アクセスポイントの ARN です。ファイルシステムの ARN ではありません。
- `/tmp` は実行環境ごとの領域で、他の実行環境と共有できません。
- EBS は Lambda から使えません。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [storage 問3](../../exercises/storage.md#q3) | 1.3.2 | ap-northeast-1a の EBS ボリュームのデータを、ap-northeast-1c の… |
| [storage 問8](../../exercises/storage.md#q8) | 1.2.1 | Lambda 関数に EFS をマウントしたところ、呼び出しで EFSMountConnectivi… |

<!-- questions:end -->

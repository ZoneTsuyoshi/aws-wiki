# 分野5: 転送時の暗号化

「暗号化できる」と「暗号化しないと接続できない」の違いと、プライベートな経路、クラスターの内部の通信を問います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [5.1.1](../../domain5.md#skill-5-1-1) | 暗号化の強制 |
| [5.1.2](../../domain5.md#skill-5-1-2) | 安全でプライベートなアクセス |
| [5.1.3](../../domain5.md#skill-5-1-3) | リソース間の転送時暗号化 |

## 学習の順番 {#study-order}

1. [転送時の TLS](../../../../services/certificates.md#tls-in-transit): ELB のセキュリティポリシーの既定が作成方法で違うことを押さえます。
2. [RDS の SSL/TLS](../../../../services/databases.md#rds-ssl)と [EFS の暗号化](../../../../services/storage.md#efs-encryption): サービスごとの強制の方法を確認します。
3. [VPC エンドポイント](../../../../services/networking.md#vpc-endpoints)と[エンドポイントの選び方](../../../../services/networking.md#endpoint-settings): ゲートウェイとインターフェイスの違いを理解します。
4. [エンドポイントポリシー](../../../../services/networking.md#endpoint-policies): バケットポリシーとの組み合わせを覚えます。
5. [保存時と転送時](../../../../services/kms.md#at-rest-in-transit): 別の対策であることを確認します。
6. [SageMaker の IAM と暗号化](../../../../services/sagemaker.md#iam-encryption)、[EMR](../../../../services/data-engineering.md#emr)、[EKS](../../../../services/containers.md#eks): クラスターの内部の通信の暗号化を確認します。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| ALB の既定（コンソール） | `ELBSecurityPolicy-TLS13-1-2-Res-PQ-2025-09` | TLS 1.2 以上 |
| ALB の既定（CLI、IaC） | `ELBSecurityPolicy-2016-08` | TLS 1.0 と 1.1 も許可。IaC では明示する |
| `rds.force_ssl` の既定 | PostgreSQL 15 以降は 1、14 以前は 0 | 変更はカスタムパラメータグループ |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| IaC の ALB だけ古い TLS を受け入れる | `SslPolicy` の明示 |
| 組織全体の S3 で HTTPS を強制 | RCP で `aws:SecureTransport` が `false` を拒否 |
| 単一のバケットで HTTPS を強制 | バケットポリシー |
| オンプレミスから S3 へプライベートに | S3 のインターフェイスエンドポイント |
| 持ち出しの経路を減らす | `aws:SourceVpce` とエンドポイントポリシーの両方 |
| CIDR が重複する相手に特定のサービスだけ公開 | PrivateLink のエンドポイントサービス |
| インターフェイスエンドポイントを作ったのに公開 IP へ行く | プライベート DNS と VPC の DNS 属性 |
| 間に NLB がある通信の暗号化 | Nitro の対象外。アプリの TLS |
| SageMaker AI の分散学習のノード間 | コンテナ間のトラフィックの暗号化 |
| EMR で設定をそろえる | セキュリティ設定の再利用 |

## 引っかかりやすい点 {#traps}

- ゲートウェイエンドポイントは VPC の外から使えません。
- 保存時の暗号化を有効にしても、通信は暗号化されません。
- Kubernetes のシークレットの KMS 暗号化は保存時の統制で、Pod の通信とは別です。
- Nitro の自動の暗号化は、ロードバランサーや Transit Gateway を通ると対象外です。
- デフォルトのパラメータグループは変更できません。
- RCP は管理アカウントのリソースには効きません。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [encryption-in-transit 問1](../../exercises/encryption-in-transit.md#q1) | 5.1.1 | CloudFormation で作った ALB の HTTPS リスナーに、セキュリティスキャンで … |
| [encryption-in-transit 問2](../../exercises/encryption-in-transit.md#q2) | 5.1.1 | 組織の全アカウントの S3 で、HTTPS 以外のアクセスを確実に拒否します。バケットは数千個あり、… |
| [encryption-in-transit 問3](../../exercises/encryption-in-transit.md#q3) | 5.1.1 | RDS for PostgreSQL 14 の本番インスタンスで、暗号化しない接続を拒否するよう求め… |
| [encryption-in-transit 問4](../../exercises/encryption-in-transit.md#q4) | 5.1.1 | EC2 と Fargate から EFS をマウントするアプリで、NFS の通信の暗号化を監査で確認… |
| [encryption-in-transit 問5](../../exercises/encryption-in-transit.md#q5) | 5.1.2 | オンプレミスのサーバーが Direct Connect 経由で S3 に大量のファイルを送ります。イ… |
| [encryption-in-transit 問6](../../exercises/encryption-in-transit.md#q6) | 5.1.2 | VPC 内のアプリに機密データのバケットを読ませます。要件は 2 つです。バケットにはそのエンドポイ… |
| [encryption-in-transit 問7](../../exercises/encryption-in-transit.md#q7) | 5.1.2 | 自社の VPC の決済 API を、別の会社の VPC にだけ公開します。お互いの CIDR は重複… |
| [encryption-in-transit 問8](../../exercises/encryption-in-transit.md#q8) | 5.1.2 | インターフェイスエンドポイントを VPC に作りましたが、アプリは今も secretsmanager… |
| [encryption-in-transit 問9](../../exercises/encryption-in-transit.md#q9) | 5.1.3 | 同じ VPC の 2 台の EC2 は、自動で転送時に暗号化される対応インスタンスタイプです。担当者… |
| [encryption-in-transit 問10](../../exercises/encryption-in-transit.md#q10) | 5.1.3 | SageMaker AI の分散学習で医療データを扱います。5 ノードで学習します。監査でノード間の… |
| [encryption-in-transit 問11](../../exercises/encryption-in-transit.md#q11) | 5.1.3 | EMR のクラスターをチームごとに作ります。転送時と保存時の暗号化の設定を毎回そろえます。転送時の証… |
| [encryption-in-transit 問12](../../exercises/encryption-in-transit.md#q12) | 5.1.3 | EKS のチームが「Kubernetes のシークレットを KMS で暗号化したので、Pod 間の通… |

<!-- questions:end -->

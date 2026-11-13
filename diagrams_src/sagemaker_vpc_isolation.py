from diagrams import Cluster, Diagram, Edge
from diagrams.aws.compute import EC2
from diagrams.aws.database import RDS
from diagrams.aws.ml import Sagemaker, SagemakerTrainingJob
from diagrams.aws.network import Endpoint
from diagrams.aws.storage import S3

with Diagram(
    "SageMaker AI の学習ジョブを VPC に接続する",
    filename="docs/assets/diagrams/sagemaker-vpc-isolation",
    outformat="png",
    show=False,
    direction="LR",
    graph_attr={"dpi": "150", "pad": "0.5"},
):
    with Cluster("VPC（NAT なし）"):
        with Cluster("プライベートサブネット（2 つの AZ）"):
            app = EC2("VPC 内のアプリ\nジョブの作成、推論の呼び出し")
            job = SagemakerTrainingJob("学習ジョブの ENI\nVpcConfig")
            rds = RDS("社内データ RDS\nSG で許可")
        s3_ep = Endpoint("S3 ゲートウェイ\nエンドポイント\n（ルートテーブル）")
        api_ep = Endpoint("インターフェイス\nエンドポイント\nsagemaker.api / runtime")

    s3 = S3("学習データとモデル\nS3")
    sm = Sagemaker("SageMaker AI\nAPI と Runtime")

    job >> rds
    job >> s3_ep >> s3
    app >> api_ep >> sm

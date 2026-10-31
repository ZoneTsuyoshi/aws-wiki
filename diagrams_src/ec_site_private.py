from diagrams import Cluster, Diagram, Edge
from diagrams.aws.compute import ECR, Fargate
from diagrams.aws.management import Cloudwatch
from diagrams.aws.network import Endpoint, InternetGateway, NATGateway
from diagrams.aws.security import SecretsManager
from diagrams.aws.storage import S3
from diagrams.onprem.client import Client

with Diagram(
    "EC サイト: プライベートサブネットからの通信",
    filename="docs/assets/diagrams/ec-site-private",
    outformat="png",
    show=False,
    direction="TB",
    graph_attr={"dpi": "150", "pad": "0.5"},
):
    payment = Client("外部の決済 API")

    with Cluster("リージョン（東京）"):
        with Cluster("VPC"):
            igw = InternetGateway("インターネット\nゲートウェイ")
            nat = NATGateway("NAT ゲートウェイ")

            with Cluster("プライベートサブネット"):
                app = Fargate("Fargate タスク")
                vpce_if = Endpoint("インターフェイス\nエンドポイント")
                vpce_s3 = Endpoint("S3 ゲートウェイ\nエンドポイント")

        with Cluster("VPC の外（リージョンのサービス）"):
            registry = ECR("ECR")
            secrets = SecretsManager("Secrets Manager")
            logs = Cloudwatch("CloudWatch Logs")
            layers = S3("S3\nイメージのレイヤー")

    app >> Edge(label="外部 API") >> nat >> igw >> payment
    app >> vpce_if
    vpce_if >> registry
    vpce_if >> secrets
    vpce_if >> logs
    app >> vpce_s3 >> layers

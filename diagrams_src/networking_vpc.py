from diagrams import Cluster, Diagram
from diagrams.aws.compute import Lambda
from diagrams.aws.general import Users
from diagrams.aws.network import ALB, Endpoint, InternetGateway, NATGateway
from diagrams.aws.security import SecretsManager
from diagrams.aws.storage import S3

with Diagram(
    "VPC と VPC エンドポイント",
    filename="docs/assets/diagrams/networking-vpc",
    outformat="png",
    show=False,
    graph_attr={"dpi": "150", "pad": "0.5"},
):
    users = Users("利用者")
    igw = InternetGateway("インターネット\nゲートウェイ")
    bucket = S3("S3")
    secrets = SecretsManager("Secrets Manager")

    with Cluster("VPC"):
        with Cluster("パブリックサブネット"):
            alb = ALB("ALB")
            nat = NATGateway("NAT ゲートウェイ")
        with Cluster("プライベートサブネット"):
            app = Lambda("アプリケーション")
            gateway = Endpoint("ゲートウェイ\nエンドポイント")
            interface = Endpoint("インターフェイス\nエンドポイント")

    users >> igw >> alb >> app
    app >> nat >> igw
    app >> gateway >> bucket
    app >> interface >> secrets

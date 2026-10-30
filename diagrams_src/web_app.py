from diagrams import Cluster, Diagram
from diagrams.aws.compute import ECS
from diagrams.aws.database import RDS
from diagrams.aws.general import Users
from diagrams.aws.network import ALB, CloudFront
from diagrams.aws.storage import S3

with Diagram(
    "Webアプリ構成",
    filename="docs/assets/diagrams/web-app",
    outformat="png",
    show=False,
    graph_attr={"dpi": "150", "pad": "0.5"},
):
    users = Users("ユーザー")
    cdn = CloudFront("CloudFront")
    assets = S3("静的ファイル")

    with Cluster("VPC"):
        alb = ALB("ALB")
        app = ECS("アプリ")
        db = RDS("データベース")

    users >> cdn
    cdn >> assets
    cdn >> alb >> app >> db

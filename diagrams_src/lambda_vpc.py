from diagrams import Cluster, Diagram
from diagrams.aws.compute import Lambda
from diagrams.aws.database import RDS
from diagrams.aws.general import InternetAlt1
from diagrams.aws.network import Endpoint, InternetGateway, NATGateway
from diagrams.aws.storage import S3

with Diagram(
    "VPC に接続した Lambda",
    filename="docs/assets/diagrams/lambda-vpc",
    outformat="png",
    show=False,
    graph_attr={"dpi": "150", "pad": "0.5"},
):
    s3 = S3("S3")
    internet = InternetAlt1("インターネット")

    with Cluster("VPC"):
        with Cluster("プライベートサブネット"):
            fn = Lambda("関数 (ENI 経由)")
            db = RDS("RDS")
            endpoint = Endpoint("VPC エンドポイント")

        with Cluster("パブリックサブネット"):
            nat = NATGateway("NAT ゲートウェイ")

        igw = InternetGateway("インターネットゲートウェイ")

    fn >> db
    fn >> endpoint >> s3
    fn >> nat >> igw >> internet

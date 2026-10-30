from diagrams import Cluster, Diagram
from diagrams.aws.compute import EC2
from diagrams.aws.database import RDS, Aurora, ElastiCache
from diagrams.aws.general import Users
from diagrams.aws.network import ALB, CloudFront

with Diagram(
    "キャッシュの層とデータストア",
    filename="docs/assets/diagrams/databases-cache-layers",
    outformat="png",
    show=False,
    graph_attr={"dpi": "150", "pad": "0.5"},
):
    users = Users("利用者")
    cdn = CloudFront("CloudFront\nエッジでキャッシュ")

    with Cluster("VPC"):
        alb = ALB("ALB")
        app = EC2("アプリ\nプロセス内キャッシュ")
        cache = ElastiCache("ElastiCache\n共有キャッシュ")
        proxy = RDS("RDS Proxy\n接続プール")
        db = Aurora("Aurora / RDS")

    users >> cdn >> alb >> app
    app >> cache
    app >> proxy >> db

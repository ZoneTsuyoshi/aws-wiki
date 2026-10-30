from diagrams import Cluster, Diagram
from diagrams.aws.compute import EC2
from diagrams.aws.general import Users
from diagrams.aws.network import ALB, CloudFront, Route53
from diagrams.aws.security import CertificateManager
from diagrams.aws.storage import S3

with Diagram(
    "CloudFront の構成",
    filename="docs/assets/diagrams/networking-cloudfront",
    outformat="png",
    show=False,
    graph_attr={"dpi": "150", "pad": "0.5", "rankdir": "LR"},
):
    users = Users("利用者")
    dns = Route53("Route 53\nエイリアス")
    cdn = CloudFront("CloudFront\nビヘイビアで振り分け")
    cert = CertificateManager("ACM 証明書\nus-east-1")

    with Cluster("オリジン"):
        bucket = S3("S3\n静的ファイル (OAC)")
        alb = ALB("ALB\n/api/*")
        app = EC2("アプリケーション")

    users >> dns
    users >> cdn
    cert >> cdn
    cdn >> bucket
    cdn >> alb >> app

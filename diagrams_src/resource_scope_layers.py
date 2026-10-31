from diagrams import Cluster, Diagram, Edge
from diagrams.aws.compute import EC2
from diagrams.aws.database import Dynamodb
from diagrams.aws.network import CloudFront, Route53
from diagrams.aws.security import IAM
from diagrams.aws.storage import S3, EBS

with Diagram(
    "リソースの提供単位",
    filename="docs/assets/diagrams/resource-scope-layers",
    outformat="png",
    show=False,
    direction="TB",
    graph_attr={"dpi": "150", "pad": "0.5"},
):
    with Cluster("グローバル（リージョンの指定なし）"):
        iam = IAM("IAM")
        dns = Route53("Route 53")
        cdn = CloudFront("CloudFront")

    with Cluster("リージョン（東京）"):
        with Cluster("リージョン単位、VPC の外"):
            bucket = S3("S3 バケット")
            table = Dynamodb("DynamoDB")

        with Cluster("VPC（リージョン単位、AZ をまたぐ）"):
            with Cluster("サブネット（AZ 1a に収まる）"):
                server = EC2("EC2 インスタンス\nAZ 単位")

        with Cluster("AZ 1a、VPC の外"):
            volume = EBS("EBS ボリューム\nAZ 単位")

    hidden = Edge(style="invis")
    iam >> hidden >> bucket
    dns >> hidden >> table
    cdn >> hidden >> server
    server >> Edge(label="同じ AZ でだけ接続できる") >> volume

from diagrams import Cluster, Diagram
from diagrams.aws.compute import EC2, ECS, Lambda
from diagrams.aws.storage import EBS, EFS, S3

with Diagram(
    "EBS、EFS、S3の接続イメージ",
    filename="docs/assets/diagrams/storage-options",
    outformat="png",
    show=False,
    graph_attr={"dpi": "150", "pad": "0.5"},
):
    with Cluster("VPC"):
        instance = EC2("EC2")
        fn = Lambda("Lambda")
        task = ECS("ECSタスク")
        block = EBS("EBS\nブロック、同一AZ")
        shared = EFS("EFS\nNFSで共有")

    objects = S3("S3\nHTTPS APIでアクセス")

    instance >> block
    instance >> shared
    fn >> shared
    task >> shared
    instance >> objects
    fn >> objects

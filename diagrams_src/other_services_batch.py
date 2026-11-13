from diagrams import Cluster, Diagram, Edge
from diagrams.aws.compute import EC2, Batch, Fargate
from diagrams.aws.general import User
from diagrams.aws.storage import S3

with Diagram(
    "AWS Batch のジョブの流れ",
    filename="docs/assets/diagrams/other-services-batch",
    outformat="png",
    show=False,
    graph_attr={"dpi": "150", "pad": "0.5", "rankdir": "LR"},
):
    user = User("ジョブの投入\n(ジョブ定義を指定)")

    with Cluster("AWS Batch（リージョン）"):
        queue = Batch("ジョブキュー\n(優先度)")
        scheduler = Batch("スケジューラー")

    with Cluster("コンピューティング環境（VPC のサブネット）"):
        ondemand = EC2("EC2\nオンデマンド")
        spot = EC2("EC2\nSpot")
        fargate = Fargate("Fargate")

    data = S3("S3\n入力と出力")

    user >> queue >> scheduler
    scheduler >> Edge(label="必要な分だけ起動") >> ondemand
    scheduler >> spot
    scheduler >> fargate
    ondemand >> Edge(style="dashed") >> data
    spot >> Edge(style="dashed") >> data
    fargate >> Edge(style="dashed") >> data

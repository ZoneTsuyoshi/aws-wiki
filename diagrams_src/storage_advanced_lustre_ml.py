from diagrams import Cluster, Diagram, Edge
from diagrams.aws.compute import EC2
from diagrams.aws.storage import S3, FsxForLustre

with Diagram(
    "S3 と FSx for Lustre で学習する流れ",
    filename="docs/assets/diagrams/storage-advanced-lustre-ml",
    outformat="png",
    show=False,
    graph_attr={"dpi": "150", "pad": "0.5", "rankdir": "LR"},
):
    data = S3("学習データ\n(正本、100 TB)")
    result = S3("結果の保存先")

    with Cluster("VPC (1 つの AZ)"):
        lustre = FsxForLustre("FSx for Lustre\n(Scratch 2)")
        gpus = [EC2("GPU インスタンス 1"), EC2("GPU インスタンス 2")]

    data >> Edge(label="インポート\n(初回アクセスで取得)") >> lustre
    lustre >> Edge(label="並列に読む") >> gpus
    lustre >> Edge(label="エクスポート") >> result

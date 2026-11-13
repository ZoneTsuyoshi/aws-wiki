from diagrams import Cluster, Diagram, Edge
from diagrams.aws.security import IAMRole, KMS
from diagrams.aws.storage import S3

with Diagram(
    "S3 レプリケーション (CRR と SRR)",
    filename="docs/assets/diagrams/s3-replication",
    outformat="png",
    show=False,
    graph_attr={"dpi": "150", "pad": "0.5", "rankdir": "LR"},
):
    role = IAMRole("S3 が引き受ける\nIAM ロール")

    with Cluster("東京リージョン"):
        source = S3("送信元バケット\n(バージョニング有効)")
        srr = S3("別アカウントの\nバケット (SRR)")

    with Cluster("大阪リージョン"):
        dest = S3("送信先バケット\n(バージョニング有効)")
        key = KMS("送信先の KMS キー\n(SSE-KMS のとき)")

    role >> Edge(style="dashed", label="権限") >> source
    source >> Edge(label="CRR (非同期)") >> dest
    source >> Edge(label="SRR (非同期)") >> srr
    dest >> Edge(style="dashed") >> key

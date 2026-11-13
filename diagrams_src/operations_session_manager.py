from diagrams import Cluster, Diagram, Edge
from diagrams.aws.compute import EC2
from diagrams.aws.general import User
from diagrams.aws.management import CloudwatchLogs, SystemsManager
from diagrams.aws.network import Endpoint
from diagrams.aws.security import IAM
from diagrams.aws.storage import S3

with Diagram(
    "Session Manager でプライベートのノードへ接続",
    filename="docs/assets/diagrams/operations-session-manager",
    outformat="png",
    show=False,
    graph_attr={"dpi": "150", "pad": "0.5", "rankdir": "LR"},
):
    user = User("運用者\n(コンソール / CLI)")
    iam = IAM("IAM\nポリシー")
    ssm = SystemsManager("Session Manager")

    with Cluster("VPC"):
        with Cluster("プライベートサブネット\n(インバウンドの許可なし)"):
            node = EC2("EC2\nSSM Agent")
            endpoint = Endpoint("インターフェイス\nエンドポイント\nssm\nssmmessages")

    with Cluster("セッションのログ"):
        s3 = S3("S3")
        logs = CloudwatchLogs("CloudWatch Logs")

    user >> Edge(label="start-session") >> ssm
    iam >> Edge(style="dashed", label="権限の確認") >> ssm
    node >> Edge(label="HTTPS 443\n外向き") >> endpoint >> ssm
    node >> Edge(style="dashed") >> s3
    node >> Edge(style="dashed") >> logs

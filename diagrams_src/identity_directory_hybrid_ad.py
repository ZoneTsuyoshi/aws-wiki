from diagrams import Cluster, Diagram, Edge
from diagrams.aws.compute import EC2
from diagrams.aws.database import RDS
from diagrams.aws.enduser import Workspaces
from diagrams.aws.network import DirectConnect
from diagrams.aws.security import AdConnector, ManagedMicrosoftAd
from diagrams.generic.os import Windows
from diagrams.onprem.client import Users

with Diagram(
    "AWS で Active Directory を使う 2 つの形",
    filename="docs/assets/diagrams/identity-directory-hybrid-ad",
    outformat="png",
    show=False,
    direction="TB",
    graph_attr={"dpi": "150", "pad": "0.5"},
):
    with Cluster("オンプレミス"):
        users = Users("社員")
        onprem_ad = Windows("オンプレの AD\nユーザーの正本")

    link = DirectConnect("VPN か\nDirect Connect")

    with Cluster("VPC（2 つの AZ のサブネット）"):
        with Cluster("問い合わせを転送するだけ"):
            connector = AdConnector("AD Connector\nキャッシュなし")
            workspaces = Workspaces("WorkSpaces")

        with Cluster("AWS にドメインを置く"):
            managed = ManagedMicrosoftAd("Managed\nMicrosoft AD")
            ec2 = EC2("Windows の EC2\nドメイン参加")
            rds = RDS("RDS for\nSQL Server")

    users >> onprem_ad
    onprem_ad - link
    link >> Edge(label="認証のたびに転送") >> connector
    link >> Edge(label="信頼", style="dashed") >> managed
    connector >> workspaces
    managed >> ec2
    managed >> rds

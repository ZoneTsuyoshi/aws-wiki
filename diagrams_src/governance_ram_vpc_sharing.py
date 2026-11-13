from diagrams import Cluster, Diagram, Edge
from diagrams.aws.compute import EC2
from diagrams.aws.database import RDS
from diagrams.aws.management import OrganizationsAccount
from diagrams.aws.network import RouteTable
from diagrams.aws.security import ResourceAccessManager

with Diagram(
    "VPC サブネットの共有",
    filename="docs/assets/diagrams/governance-ram-vpc-sharing",
    outformat="png",
    show=False,
    direction="TB",
    graph_attr={"dpi": "150", "pad": "0.5", "splines": "spline"},
):
    with Cluster("ネットワークアカウント（オーナー）"):
        ram = ResourceAccessManager("RAM\nサブネットを共有")
        rt = RouteTable("ルートテーブル\nオーナーだけが変更")

    with Cluster("アプリのアカウント（参加者）"):
        acct_a = OrganizationsAccount("アプリ A")
        acct_b = OrganizationsAccount("アプリ B")

    with Cluster("オーナーの VPC"):
        with Cluster("共有サブネット A"):
            app_a = EC2("A の EC2\n費用は A")
        with Cluster("共有サブネット B"):
            app_b = RDS("B の RDS\n費用は B")

    ram >> Edge(label="共有") >> acct_a
    ram >> Edge(label="共有") >> acct_b
    rt >> Edge(style="invis") >> acct_b
    acct_a >> Edge(label="作成", style="dashed") >> app_a
    acct_b >> Edge(label="作成", style="dashed") >> app_b

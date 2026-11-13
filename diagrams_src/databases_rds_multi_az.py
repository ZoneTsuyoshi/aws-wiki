from diagrams import Cluster, Diagram, Edge
from diagrams.aws.compute import EC2
from diagrams.aws.database import RDS

with Diagram(
    "RDSのMulti-AZとリードレプリカ",
    filename="docs/assets/diagrams/databases-rds-multi-az",
    outformat="png",
    show=False,
    graph_attr={"dpi": "150", "pad": "0.5"},
):
    with Cluster("VPC（東京リージョン）"):
        with Cluster("AZ a"):
            app = EC2("アプリ")
            primary = RDS("プライマリ\n読み書き")
        with Cluster("AZ c"):
            standby = RDS("スタンバイ\n読めない")
        with Cluster("AZ d"):
            replica = RDS("リードレプリカ\n読み取り専用")
            report = EC2("レポート")

    app >> Edge(label="書き込みと読み取り") >> primary
    primary >> Edge(label="同期") >> standby
    primary >> Edge(label="非同期", style="dashed") >> replica
    replica << Edge(label="重い読み取り") << report

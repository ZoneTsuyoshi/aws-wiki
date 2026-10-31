from diagrams import Cluster, Diagram, Edge
from diagrams.aws.compute import AutoScaling
from diagrams.aws.database import Aurora
from diagrams.aws.network import ELB, Route53
from diagrams.aws.storage import Backup

with Diagram(
    "ウォームスタンバイの構成",
    filename="docs/assets/diagrams/resilience-warm-standby",
    outformat="png",
    show=False,
    graph_attr={"dpi": "150", "pad": "0.5"},
):
    dns = Route53("Route 53\nフェイルオーバー\nレコード")

    with Cluster("プライマリリージョン（全量で稼働）"):
        primary_lb = ELB("ALB")
        primary_app = AutoScaling("Auto Scaling\n希望 12 台")
        primary_db = Aurora("Aurora\nライター")

    with Cluster("DR リージョン（縮小して稼働）"):
        dr_lb = ELB("ALB")
        dr_app = AutoScaling("Auto Scaling\n希望 2 台")
        dr_db = Aurora("Aurora\nセカンダリ")

    vault = Backup("AWS Backup\n別リージョンの\nボールトにコピー")

    dns >> Edge(label="正常時") >> primary_lb >> primary_app >> primary_db
    dns >> Edge(label="障害時", style="dashed") >> dr_lb >> dr_app >> dr_db
    primary_db >> Edge(label="非同期レプリケーション") >> dr_db
    primary_db >> Edge(label="バックアップ", style="dashed") >> vault

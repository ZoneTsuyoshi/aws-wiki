from diagrams import Cluster, Diagram, Edge
from diagrams.aws.compute import Lambda
from diagrams.aws.database import Dynamodb
from diagrams.aws.general import Users
from diagrams.aws.network import Route53

with Diagram(
    "DynamoDB グローバルテーブル",
    filename="docs/assets/diagrams/dynamodb-global-tables",
    outformat="png",
    show=False,
    graph_attr={"dpi": "150", "pad": "0.5", "rankdir": "LR", "splines": "spline"},
):
    users = Users("世界中の利用者")
    dns = Route53("Route 53\n(近いリージョンへ)")

    with Cluster("東京リージョン"):
        app_tokyo = Lambda("アプリ")
        table_tokyo = Dynamodb("レプリカ\n(読み書き可)")

    with Cluster("バージニア北部リージョン"):
        app_virginia = Lambda("アプリ")
        table_virginia = Dynamodb("レプリカ\n(読み書き可)")

    users >> dns
    dns >> app_tokyo >> table_tokyo
    dns >> app_virginia >> table_virginia
    table_tokyo - Edge(label="双方向に複製\n(MREC は非同期)", forward=True, reverse=True, color="firebrick") - table_virginia

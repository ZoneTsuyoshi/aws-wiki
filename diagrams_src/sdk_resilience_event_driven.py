from diagrams import Cluster, Diagram
from diagrams.aws.compute import Lambda
from diagrams.aws.database import Dynamodb
from diagrams.aws.general import Users
from diagrams.aws.integration import SQS, Eventbridge
from diagrams.aws.network import APIGateway

with Diagram(
    "疎結合なイベント駆動マイクロサービス",
    filename="docs/assets/diagrams/sdk-resilience-event-driven",
    outformat="png",
    show=False,
    graph_attr={"dpi": "150", "pad": "0.5"},
):
    users = Users("クライアント")
    api = APIGateway("API Gateway")

    with Cluster("注文サービス"):
        order = Lambda("注文 API")
        orders = Dynamodb("注文テーブル")

    bus = Eventbridge("イベントバス")

    with Cluster("在庫サービス"):
        queue = SQS("バッファ")
        stock = Lambda("在庫更新")
        stocks = Dynamodb("在庫テーブル")

    users >> api >> order >> orders
    order >> bus >> queue >> stock >> stocks

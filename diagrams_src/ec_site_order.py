from diagrams import Cluster, Diagram, Edge
from diagrams.aws.compute import Fargate, Lambda
from diagrams.aws.database import Dynamodb
from diagrams.aws.engagement import SES
from diagrams.aws.integration import Eventbridge, SQS
from diagrams.aws.network import Endpoint

with Diagram(
    "EC サイト: 注文後の非同期処理",
    filename="docs/assets/diagrams/ec-site-order",
    outformat="png",
    show=False,
    direction="TB",
    graph_attr={"dpi": "150", "pad": "0.5"},
):
    with Cluster("リージョン（東京）"):
        with Cluster("VPC: プライベートサブネット"):
            app = Fargate("注文 API")
            vpce_ddb = Endpoint("ゲートウェイ\nエンドポイント")
            vpce_events = Endpoint("インターフェイス\nエンドポイント")

        with Cluster("VPC の外（リージョンのサービス）"):
            orders = Dynamodb("DynamoDB\n注文の履歴")
            bus = Eventbridge("EventBridge\nOrderPlaced")
            queue_mail = SQS("SQS\nメール用")
            queue_ship = SQS("SQS\n出荷用")
            mailer = Lambda("Lambda\nメール作成")
            shipper = Lambda("Lambda\n出荷指示")
            mail = SES("SES")

    app >> vpce_ddb >> orders
    app >> vpce_events >> Edge(label="PutEvents") >> bus
    bus >> queue_mail >> mailer >> mail
    bus >> queue_ship >> shipper

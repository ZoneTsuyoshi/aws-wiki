from diagrams import Cluster, Diagram
from diagrams.aws.compute import Lambda
from diagrams.aws.integration import SNS, SQS, Eventbridge, StepFunctions
from diagrams.aws.storage import S3

with Diagram(
    "EventBridge によるイベントルーティング",
    filename="docs/assets/diagrams/messaging-eventbridge",
    outformat="png",
    show=False,
    graph_attr={"dpi": "150", "pad": "0.5"},
):
    with Cluster("イベントの発生元"):
        app = Lambda("注文サービス")
        bucket = S3("S3")

    bus = Eventbridge("イベントバス + ルール")

    with Cluster("ターゲット"):
        flow = StepFunctions("Step Functions")
        queue = SQS("SQS")
        topic = SNS("SNS")

    dlq = SQS("ターゲットの DLQ")

    app >> bus
    bucket >> bus
    bus >> flow
    bus >> queue
    bus >> topic
    bus >> dlq

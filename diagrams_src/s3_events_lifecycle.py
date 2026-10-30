from diagrams import Diagram
from diagrams.aws.compute import Lambda
from diagrams.aws.general import Users
from diagrams.aws.integration import SNS, SQS, Eventbridge
from diagrams.aws.storage import S3, S3Glacier

with Diagram(
    "S3のアップロード、通知、ライフサイクル",
    filename="docs/assets/diagrams/s3-events-lifecycle",
    outformat="png",
    show=False,
    graph_attr={"dpi": "150", "pad": "0.5", "rankdir": "LR"},
):
    client = Users("クライアント\n(署名付きURL)")
    bucket = S3("S3 バケット")
    fn = Lambda("Lambda")
    queue = SQS("SQS")
    topic = SNS("SNS")
    bus = Eventbridge("EventBridge")
    archive = S3Glacier("S3 Glacier\nストレージクラス")

    client >> bucket
    bucket >> fn
    bucket >> queue
    bucket >> topic
    bucket >> bus
    bucket >> archive

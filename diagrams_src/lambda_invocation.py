from diagrams import Cluster, Diagram
from diagrams.aws.analytics import KinesisDataStreams
from diagrams.aws.compute import Lambda
from diagrams.aws.integration import SNS, SQS, Eventbridge
from diagrams.aws.network import APIGateway
from diagrams.aws.storage import S3

with Diagram(
    "Lambda の3つの呼び出し方",
    filename="docs/assets/diagrams/lambda-invocation",
    outformat="png",
    show=False,
    graph_attr={"dpi": "150", "pad": "0.5"},
):
    fn = Lambda("関数")

    with Cluster("同期"):
        api = APIGateway("API Gateway")

    with Cluster("非同期"):
        s3 = S3("S3")
        sns = SNS("SNS")

    with Cluster("イベントソースマッピング"):
        queue = SQS("SQS")
        stream = KinesisDataStreams("Kinesis")

    dest = Eventbridge("失敗時の送信先")

    api >> fn
    s3 >> fn
    sns >> fn
    fn << queue
    fn << stream
    fn >> dest

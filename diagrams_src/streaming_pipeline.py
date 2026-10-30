from diagrams import Cluster, Diagram
from diagrams.aws.analytics import AmazonOpensearchService, Athena, KinesisDataFirehose, KinesisDataStreams
from diagrams.aws.compute import Lambda
from diagrams.aws.general import Client
from diagrams.aws.storage import S3

with Diagram(
    "ストリーミングデータのパイプライン",
    filename="docs/assets/diagrams/streaming-pipeline",
    outformat="png",
    show=False,
    graph_attr={"dpi": "150", "pad": "0.5"},
):
    producer = Client("プロデューサー")
    stream = KinesisDataStreams("Kinesis Data Streams")

    with Cluster("リアルタイム処理"):
        fn = Lambda("Lambda")
        search = AmazonOpensearchService("OpenSearch Service")

    with Cluster("蓄積と分析"):
        firehose = KinesisDataFirehose("Data Firehose")
        bucket = S3("S3")
        athena = Athena("Athena")

    producer >> stream
    stream >> fn >> search
    stream >> firehose >> bucket >> athena

from diagrams import Cluster, Diagram
from diagrams.aws.compute import Lambda
from diagrams.aws.integration import SNS, SQS
from diagrams.aws.storage import S3

with Diagram(
    "SNS + SQS のファンアウト",
    filename="docs/assets/diagrams/messaging-fanout",
    outformat="png",
    show=False,
    graph_attr={"dpi": "150", "pad": "0.5"},
):
    bucket = S3("S3 イベント通知")
    topic = SNS("SNS トピック")

    with Cluster("画像処理"):
        q1 = SQS("キュー")
        f1 = Lambda("サムネイル作成")
        dlq1 = SQS("DLQ")

    with Cluster("分析"):
        q2 = SQS("キュー (フィルターあり)")
        f2 = Lambda("集計")
        dlq2 = SQS("DLQ")

    bucket >> topic
    topic >> q1 >> f1
    q1 >> dlq1
    topic >> q2 >> f2
    q2 >> dlq2

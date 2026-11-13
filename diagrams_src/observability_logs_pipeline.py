from diagrams import Cluster, Diagram, Edge
from diagrams.aws.analytics import KinesisDataFirehose
from diagrams.aws.compute import EC2, Lambda
from diagrams.aws.management import Cloudwatch, CloudwatchAlarm, CloudwatchLogs
from diagrams.aws.storage import S3

with Diagram(
    "CloudWatch Logs に集めたログの使い道",
    filename="docs/assets/diagrams/observability-logs-pipeline",
    outformat="png",
    show=False,
    graph_attr={"dpi": "150", "pad": "0.5", "rankdir": "LR"},
):
    with Cluster("ログの発生元"):
        sources = [EC2("EC2\n(エージェント)"), Lambda("Lambda")]

    group = CloudwatchLogs("ロググループ\n(保持期間)")

    with Cluster("数値にする"):
        metric = Cloudwatch("メトリクス\nフィルター")
        alarm = CloudwatchAlarm("アラーム")

    with Cluster("すぐ流す"):
        firehose = KinesisDataFirehose("サブスクリプション\n→ Firehose")

    insights = CloudwatchLogs("Logs Insights\n(後から検索)")
    archive = S3("S3\n(長期保管)")

    sources >> group
    group >> metric >> alarm
    group >> firehose >> archive
    group >> Edge(style="dashed") >> insights
    group >> Edge(style="dashed", label="エクスポート") >> archive

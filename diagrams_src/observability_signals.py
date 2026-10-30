from diagrams import Cluster, Diagram
from diagrams.aws.compute import EC2, Lambda
from diagrams.aws.devtools import XRay
from diagrams.aws.integration import SNS
from diagrams.aws.management import Cloudwatch, CloudwatchAlarm, CloudwatchLogs
from diagrams.aws.network import ALB

with Diagram(
    "メトリクス・ログ・トレースの流れ",
    filename="docs/assets/diagrams/observability-signals",
    outformat="png",
    show=False,
    graph_attr={"dpi": "150", "pad": "0.5", "rankdir": "LR"},
):
    with Cluster("アプリケーション"):
        apps = [ALB("ALB"), EC2("EC2"), Lambda("Lambda")]

    logs = CloudwatchLogs("CloudWatch Logs\nログ")
    metrics = Cloudwatch("CloudWatch\nメトリクス")
    traces = XRay("X-Ray\nトレース")
    alarm = CloudwatchAlarm("アラーム")
    topic = SNS("SNS\n通知")

    apps >> logs
    apps >> metrics
    apps >> traces
    logs >> metrics
    metrics >> alarm >> topic

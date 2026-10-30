from diagrams import Cluster, Diagram
from diagrams.aws.devtools import Codedeploy, Codepipeline
from diagrams.aws.integration import Eventbridge, SNS
from diagrams.aws.management import Cloudwatch, CloudwatchAlarm

with Diagram(
    "クォータとデプロイ完了の通知",
    filename="docs/assets/diagrams/observability-alerts",
    outformat="png",
    show=False,
    graph_attr={"dpi": "150", "pad": "0.5", "rankdir": "LR"},
):
    with Cluster("デプロイ完了"):
        deploys = [Codedeploy("CodeDeploy"), Codepipeline("CodePipeline")]
        rule = Eventbridge("EventBridge ルール")

    with Cluster("クォータ"):
        usage = Cloudwatch("AWS/Usage\n使用量メトリクス")
        alarm = CloudwatchAlarm("アラーム\n上限の 80%")

    topic = SNS("SNS\nメール / Chat")

    deploys >> rule >> topic
    usage >> alarm >> topic

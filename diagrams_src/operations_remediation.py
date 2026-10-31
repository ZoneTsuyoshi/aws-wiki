from diagrams import Cluster, Diagram
from diagrams.aws.compute import EC2
from diagrams.aws.integration import Eventbridge, SNS
from diagrams.aws.management import (
    CloudwatchAlarm,
    Config,
    PersonalHealthDashboard,
    SystemsManagerAutomation,
    SystemsManagerOpscenter,
)

with Diagram(
    "イベントから自動修復へ",
    filename="docs/assets/diagrams/operations-remediation",
    outformat="png",
    show=False,
    graph_attr={"dpi": "150", "pad": "0.5", "rankdir": "LR"},
):
    with Cluster("検知"):
        alarm = CloudwatchAlarm("CloudWatch\nアラーム")
        health = PersonalHealthDashboard("AWS Health\nイベント")
        config = Config("AWS Config\nルール")

    rule = Eventbridge("EventBridge\nルール")

    with Cluster("対応"):
        automation = SystemsManagerAutomation("Automation\nランブック")
        opsitem = SystemsManagerOpscenter("OpsCenter\nOpsItem")
        topic = SNS("SNS\n通知")

    target = EC2("修復先の\nリソース")

    alarm >> rule
    health >> rule
    config >> automation
    rule >> automation >> target
    rule >> opsitem
    rule >> topic

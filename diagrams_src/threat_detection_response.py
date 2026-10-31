from diagrams import Diagram
from diagrams.aws.compute import Lambda
from diagrams.aws.integration import Eventbridge, SNS, StepFunctions
from diagrams.aws.management import SSM
from diagrams.aws.security import Detective, Guardduty, Inspector, Macie, SecurityHub

with Diagram(
    "検出結果の集約と自動対応",
    filename="docs/assets/diagrams/threat-detection-response",
    outformat="png",
    show=False,
    direction="TB",
    graph_attr={"dpi": "150", "pad": "0.5"},
):
    hub = SecurityHub("Security Hub")
    duty = Guardduty("GuardDuty")
    bus = Eventbridge("EventBridge")
    flow = StepFunctions("Step Functions")

    duty >> hub
    Inspector("Inspector") >> hub
    Macie("Macie") >> hub
    duty >> Detective("Detective\n調査")
    hub >> bus
    bus >> flow
    flow >> Lambda("Lambda")
    flow >> SSM("Systems Manager\n隔離")
    flow >> SNS("SNS\n通知")

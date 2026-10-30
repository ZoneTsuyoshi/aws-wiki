from diagrams import Cluster, Diagram
from diagrams.aws.compute import EC2AutoScaling
from diagrams.aws.general import Users
from diagrams.aws.integration import SQS
from diagrams.aws.network import ALB

with Diagram(
    "Elastic Beanstalkのウェブ環境とワーカー環境",
    filename="docs/assets/diagrams/ec2-beanstalk-tiers",
    outformat="png",
    show=False,
    graph_attr={"dpi": "150", "pad": "0.5", "rankdir": "LR"},
):
    users = Users("利用者")

    with Cluster("ウェブサーバー環境"):
        alb = ALB("ALB")
        web = EC2AutoScaling("Auto Scaling\nグループ")

    queue = SQS("SQSキュー")

    with Cluster("ワーカー環境"):
        worker = EC2AutoScaling("Auto Scaling\nグループ\n(sqsdデーモン)")

    users >> alb >> web >> queue >> worker

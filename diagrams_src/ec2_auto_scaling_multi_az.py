from diagrams import Cluster, Diagram, Edge
from diagrams.aws.compute import EC2
from diagrams.aws.general import Users
from diagrams.aws.management import Cloudwatch
from diagrams.aws.network import ALB

with Diagram(
    "Auto Scalingグループを2つのAZに分けた構成",
    filename="docs/assets/diagrams/ec2-auto-scaling-multi-az",
    outformat="png",
    show=False,
    graph_attr={"dpi": "150", "pad": "0.5", "rankdir": "TB"},
):
    users = Users("利用者")
    alb = ALB("ALB")
    alarm = Cloudwatch("CloudWatch\n平均CPU")

    with Cluster("Auto Scaling グループ（最小 2、希望 4、最大 10）"):
        with Cluster("AZ a"):
            a1 = EC2("EC2")
            a2 = EC2("EC2")
        with Cluster("AZ c"):
            c1 = EC2("EC2")
            c2 = EC2("EC2")

    users >> alb
    alb >> [a1, a2, c1, c2]
    a2 >> Edge(label="メトリクス", style="dashed") >> alarm
    c2 >> Edge(style="dashed") >> alarm

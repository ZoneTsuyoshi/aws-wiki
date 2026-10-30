from diagrams import Cluster, Diagram, Edge
from diagrams.aws.compute import ECR, Fargate
from diagrams.aws.database import Dynamodb
from diagrams.aws.general import Users
from diagrams.aws.network import ALB
from diagrams.aws.security import SecretsManager

with Diagram(
    "ECSタスクと2つのロールの役割",
    filename="docs/assets/diagrams/containers-ecs-flow",
    outformat="png",
    show=False,
    graph_attr={"dpi": "150", "pad": "0.5", "rankdir": "LR"},
):
    users = Users("利用者")
    registry = ECR("ECR")
    secrets = SecretsManager("Secrets Manager")

    with Cluster("ECSサービス"):
        alb = ALB("ALB")
        task = Fargate("タスク")

    data = Dynamodb("DynamoDB")

    users >> alb >> task
    registry >> Edge(label="実行ロールでプル") >> task
    secrets >> Edge(label="実行ロールで取得") >> task
    task >> Edge(label="タスクロールで呼び出し") >> data

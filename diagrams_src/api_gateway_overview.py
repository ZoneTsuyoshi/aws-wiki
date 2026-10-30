from diagrams import Cluster, Diagram
from diagrams.aws.compute import Lambda
from diagrams.aws.database import Dynamodb
from diagrams.aws.general import Users
from diagrams.aws.network import APIGateway
from diagrams.aws.security import Cognito

with Diagram(
    "API Gateway の基本構成",
    filename="docs/assets/diagrams/api-gateway-overview",
    outformat="png",
    show=False,
    graph_attr={"dpi": "150", "pad": "0.5"},
):
    users = Users("クライアント")
    pool = Cognito("Cognito ユーザープール")
    api = APIGateway("REST API (stage: prod)")

    with Cluster("統合先"):
        fn = Lambda("Lambda (プロキシ統合)")
        table = Dynamodb("DynamoDB (AWS 統合)")

    authorizer = Lambda("Lambda オーソライザー")

    users >> pool
    users >> api
    api >> authorizer
    api >> fn
    api >> table

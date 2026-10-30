from diagrams import Cluster, Diagram
from diagrams.aws.compute import Lambda
from diagrams.aws.general import Users
from diagrams.aws.network import APIGateway
from diagrams.aws.security import Cognito, IAMAWSSts
from diagrams.aws.storage import S3

with Diagram(
    "ユーザープールと ID プール",
    filename="docs/assets/diagrams/cognito-pools",
    outformat="png",
    show=False,
    graph_attr={"dpi": "150", "pad": "0.5"},
):
    users = Users("利用者")
    user_pool = Cognito("ユーザープール\n(JWT を発行)")

    with Cluster("JWT で自作 API を呼ぶ"):
        api = APIGateway("API Gateway")
        func = Lambda("Lambda")

    with Cluster("AWS 認証情報で直接呼ぶ"):
        identity_pool = Cognito("ID プール")
        sts = IAMAWSSts("STS")
        bucket = S3("S3")

    users >> user_pool
    user_pool >> api >> func
    user_pool >> identity_pool >> sts >> bucket

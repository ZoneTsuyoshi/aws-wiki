from diagrams import Cluster, Diagram
from diagrams.aws.compute import Lambda
from diagrams.aws.database import Dynamodb
from diagrams.aws.security import IAMAWSSts, IAMRole

with Diagram(
    "クロスアカウントの AssumeRole",
    filename="docs/assets/diagrams/iam-cross-account",
    outformat="png",
    show=False,
    graph_attr={"dpi": "150", "pad": "0.5"},
):
    sts = IAMAWSSts("STS")

    with Cluster("アカウント A (呼び出し側)"):
        exec_role = IAMRole("実行ロール\nsts:AssumeRole を許可")
        app = Lambda("アプリ")

    with Cluster("アカウント B (リソース側)"):
        target_role = IAMRole("対象ロール\n信頼ポリシーで A を許可")
        table = Dynamodb("DynamoDB")

    exec_role >> app
    app >> sts
    sts >> target_role
    app >> table

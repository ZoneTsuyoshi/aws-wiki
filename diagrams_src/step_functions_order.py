from diagrams import Diagram
from diagrams.aws.compute import Lambda
from diagrams.aws.database import Dynamodb
from diagrams.aws.general import User
from diagrams.aws.integration import SNS, SQS, StepFunctions
from diagrams.aws.network import APIGateway

with Diagram(
    "Step Functions のオーケストレーション",
    filename="docs/assets/diagrams/step-functions-order",
    outformat="png",
    show=False,
    graph_attr={"dpi": "150", "pad": "0.5"},
):
    flow = StepFunctions("ステートマシン")
    validate = Lambda("検証")
    table = Dynamodb("注文を保存")
    queue = SQS("配送依頼")
    notify = SNS("承認依頼 (タスクトークン付き)")
    approver = User("承認者")
    api = APIGateway("承認 API")
    resume = Lambda("SendTaskSuccess")

    flow >> validate
    flow >> table
    flow >> queue
    flow >> notify >> approver >> api >> resume >> flow

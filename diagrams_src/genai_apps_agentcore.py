from diagrams import Cluster, Diagram, Edge
from diagrams.aws.compute import Lambda
from diagrams.aws.management import Cloudwatch
from diagrams.aws.ml import Bedrock
from diagrams.aws.network import APIGateway
from diagrams.aws.security import Cognito
from diagrams.onprem.client import User

with Diagram(
    "AgentCore の構成",
    filename="docs/assets/diagrams/genai-apps-agentcore",
    outformat="png",
    show=False,
    direction="TB",
    graph_attr={"dpi": "150", "pad": "0.5"},
):
    user = User("利用者")
    idp = Cognito("IdP\nJWT を発行")

    with Cluster("Amazon Bedrock AgentCore"):
        runtime = Bedrock("Runtime\nセッションごとの microVM")
        memory = Bedrock("Memory\n短期と長期")
        gateway = Bedrock("Gateway + Policy\nツール呼び出しの統制")

    tool = Lambda("ツール\nLambda / API / MCP")
    api = APIGateway("既存の API")
    obs = Cloudwatch("Observability\nCloudWatch")

    user >> idp >> runtime
    runtime >> memory
    runtime >> gateway
    gateway >> tool
    gateway >> api
    runtime >> Edge(style="dashed") >> obs

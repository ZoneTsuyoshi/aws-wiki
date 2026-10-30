from diagrams import Cluster, Diagram
from diagrams.aws.compute import Lambda
from diagrams.aws.devtools import Codedeploy, ToolsAndSdks
from diagrams.aws.management import Cloudformation, Cloudwatch
from diagrams.aws.network import APIGateway
from diagrams.aws.storage import S3

with Diagram(
    "SAM でのデプロイの流れ",
    filename="docs/assets/diagrams/iac-sam-deploy",
    outformat="png",
    show=False,
    graph_attr={"dpi": "150", "pad": "0.5"},
):
    cli = ToolsAndSdks("sam build\nsam deploy")
    bucket = S3("S3\nパッケージ")
    cfn = Cloudformation("CloudFormation\n変更セットを実行")

    with Cluster("作成されるスタック"):
        api = APIGateway("API Gateway")
        function = Lambda("Lambda\nエイリアス live")
        codedeploy = Codedeploy("CodeDeploy\nカナリア")
        alarm = Cloudwatch("CloudWatch アラーム")

    cli >> bucket >> cfn
    cfn >> [api, function, codedeploy]
    api >> function
    codedeploy >> function
    alarm >> codedeploy

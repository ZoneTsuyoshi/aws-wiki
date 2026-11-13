from diagrams import Cluster, Diagram, Edge
from diagrams.aws.devtools import Codebuild, Codepipeline
from diagrams.aws.management import Cloudformation
from diagrams.aws.security import IAMRole, KMS
from diagrams.aws.storage import S3

with Diagram(
    "CodePipeline の別アカウントへのデプロイ",
    filename="docs/assets/diagrams/cicd-cross-account",
    outformat="png",
    show=False,
    direction="TB",
    graph_attr={"dpi": "150", "pad": "0.5"},
):
    with Cluster("ツール用アカウント"):
        pipeline = Codepipeline("CodePipeline")
        build = Codebuild("CodeBuild\nビルドとテスト")
        bucket = S3("アーティファクトバケット\nバケットポリシーで本番を許可")
        key = KMS("カスタマー管理 KMS キー\nキーポリシーで本番を許可")

    with Cluster("本番アカウント"):
        role = IAMRole("デプロイ用ロール\n（引き受けられる）")
        stack = Cloudformation("CloudFormation\nスタック")

    pipeline >> build >> Edge(label="成果物") >> bucket
    key >> Edge(label="暗号化", style="dashed") >> bucket
    pipeline >> Edge(label="AssumeRole") >> role
    role >> Edge(label="成果物を読み\nキーで復号", style="dashed") >> bucket
    role >> Edge(label="デプロイ") >> stack

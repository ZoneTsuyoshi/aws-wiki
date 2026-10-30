from diagrams import Cluster, Diagram
from diagrams.aws.compute import ECS, EC2, Lambda
from diagrams.aws.devtools import Codeartifact, Codebuild, Codecommit, Codedeploy, Codepipeline
from diagrams.aws.storage import S3

with Diagram(
    "CI/CD パイプラインの全体像",
    filename="docs/assets/diagrams/cicd-pipeline",
    outformat="png",
    show=False,
    graph_attr={"dpi": "150", "pad": "0.5"},
):
    source = Codecommit("ソース\nCodeCommit / GitHub など")
    pipeline = Codepipeline("CodePipeline\n全体の流れを制御")
    build = Codebuild("CodeBuild\nビルドとテスト")
    packages = Codeartifact("CodeArtifact\n依存パッケージ")
    artifacts = S3("S3\nアーティファクト")
    deploy = Codedeploy("CodeDeploy\nリビジョンを配布")

    with Cluster("デプロイ先"):
        targets = [EC2("EC2 / オンプレミス"), Lambda("Lambda"), ECS("ECS")]

    source >> pipeline >> build >> artifacts >> deploy >> targets
    packages >> build

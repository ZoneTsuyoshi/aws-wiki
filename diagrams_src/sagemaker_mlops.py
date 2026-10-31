from diagrams import Cluster, Diagram, Edge
from diagrams.aws.integration import Eventbridge
from diagrams.aws.management import Cloudwatch
from diagrams.aws.ml import Sagemaker, SagemakerModel, SagemakerTrainingJob
from diagrams.aws.storage import S3

with Diagram(
    "SageMaker AI の MLOps",
    filename="docs/assets/diagrams/sagemaker-mlops",
    outformat="png",
    show=False,
    direction="TB",
    graph_attr={"dpi": "150", "pad": "0.5"},
):
    data = S3("学習データ\nS3")

    with Cluster("SageMaker Pipelines"):
        processing = Sagemaker("Processing\n前処理と評価")
        training = SagemakerTrainingJob("Training / Tuning\n学習")
        registry = Sagemaker("Model Registry\nPendingManualApproval")

    event = Eventbridge("EventBridge\nApproved を検知")
    endpoint = SagemakerModel("エンドポイント\nブルー/グリーン")
    monitor = Cloudwatch("CloudWatch\nアラームと監視")

    data >> processing >> training >> registry
    registry >> Edge(label="承認") >> event >> endpoint
    endpoint >> monitor
    monitor >> Edge(label="自動ロールバック\n再学習の起動", style="dashed") >> endpoint

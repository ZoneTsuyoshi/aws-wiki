from diagrams import Diagram, Edge
from diagrams.aws.analytics import Glue
from diagrams.aws.management import Cloudwatch
from diagrams.aws.ml import Sagemaker, SagemakerModel, SagemakerTrainingJob
from diagrams.aws.storage import S3

with Diagram(
    "ML ライフサイクルと AWS サービス",
    filename="docs/assets/diagrams/ai-fundamentals-lifecycle",
    outformat="png",
    show=False,
    direction="TB",
    graph_attr={"dpi": "150", "pad": "0.5"},
):
    data = S3("データ収集\nS3")
    prep = Glue("前処理\nGlue / Processing")
    train = SagemakerTrainingJob("学習と評価\nSageMaker AI")
    registry = Sagemaker("承認とバージョン管理\nModel Registry")
    endpoint = SagemakerModel("推論\nエンドポイント")
    monitor = Cloudwatch("監視\nCloudWatch / MLflow")

    data >> prep >> train >> registry >> endpoint >> monitor
    monitor >> Edge(label="ドリフトで再学習", style="dashed") >> train

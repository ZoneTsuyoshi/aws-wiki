from diagrams import Diagram
from diagrams.aws.compute import Lambda
from diagrams.aws.database import Dynamodb
from diagrams.aws.security import KMS, SecretsManager
from diagrams.aws.storage import S3

with Diagram(
    "KMS を使うサービスの例",
    filename="docs/assets/diagrams/kms-services",
    outformat="png",
    show=False,
    direction="TB",
    graph_attr={"dpi": "150", "pad": "0.5"},
):
    kms = KMS("KMS キー")

    S3("S3\nSSE-KMS") >> kms
    Dynamodb("DynamoDB") >> kms
    Lambda("Lambda\n環境変数") >> kms
    SecretsManager("Secrets\nManager") >> kms

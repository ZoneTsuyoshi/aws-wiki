from diagrams import Cluster, Diagram
from diagrams.aws.compute import Lambda
from diagrams.aws.database import RDS
from diagrams.aws.management import (
    Cloudwatch,
    SystemsManagerAppConfig,
    SystemsManagerParameterStore,
)
from diagrams.aws.security import KMS, SecretsManager

with Diagram(
    "シークレットと設定の取得",
    filename="docs/assets/diagrams/secrets-config",
    outformat="png",
    show=False,
    graph_attr={"dpi": "150", "pad": "0.5", "rankdir": "LR"},
):
    app = Lambda("アプリ\n(拡張でキャッシュ)")

    with Cluster("値の置き場所"):
        secrets = SecretsManager("Secrets Manager\n資格情報")
        params = SystemsManagerParameterStore("Parameter Store\n設定値")
        appconfig = SystemsManagerAppConfig("AppConfig\nフラグ / 動的設定")

    kms = KMS("KMS")
    db = RDS("RDS")
    alarm = Cloudwatch("CloudWatch アラーム")

    app >> secrets
    app >> params
    app >> appconfig
    secrets >> kms
    params >> kms
    secrets >> db
    alarm >> appconfig

from diagrams import Cluster, Diagram, Edge
from diagrams.aws.compute import Lambda
from diagrams.aws.management import CloudwatchLogs
from diagrams.aws.ml import Bedrock
from diagrams.aws.network import Endpoint
from diagrams.aws.storage import S3

with Diagram(
    "Bedrock へのプライベートアクセス",
    filename="docs/assets/diagrams/ai-bedrock-private-access",
    outformat="png",
    show=False,
    graph_attr={"dpi": "150", "pad": "0.5"},
):
    with Cluster("VPC（インターネットゲートウェイ / NAT 不要）"):
        with Cluster("プライベートサブネット"):
            app = Lambda("アプリ\n（IAM ロール）")
            vpce = Endpoint("インターフェイスエンドポイント\nbedrock-runtime")

    bedrock = Bedrock("Bedrock Runtime\n＋ Guardrails")
    logs = CloudwatchLogs("呼び出しログ\n（データ保護ポリシーでマスク）")
    bucket = S3("呼び出しログ\n（100 KB 超の本文もここへ）")

    app >> Edge(label="HTTPS / プライベート DNS") >> vpce
    vpce >> Edge(label="PrivateLink\nエンドポイントポリシー") >> bedrock
    bedrock >> Edge(label="ログ配信", style="dashed") >> logs
    bedrock >> Edge(label="ログ配信", style="dashed") >> bucket

from diagrams import Cluster, Diagram, Edge
from diagrams.aws.compute import EC2
from diagrams.aws.general import Users
from diagrams.aws.network import CloudFront

with Diagram(
    "AWS のグローバルインフラストラクチャ",
    filename="docs/assets/diagrams/cloud-foundations-global-infra",
    outformat="png",
    show=False,
    graph_attr={"dpi": "150", "pad": "0.5"},
):
    users = Users("利用者")
    edge = CloudFront("エッジロケーション\n（CloudFront など）")

    with Cluster("リージョン（3 つ以上の AZ）"):
        az1 = EC2("AZ a")
        az2 = EC2("AZ b")
        az3 = EC2("AZ c")

    local = EC2("Local Zone\n（大都市の近く）")
    wave = EC2("Wavelength Zone\n（通信事業者の 5G 網内）")
    outpost = EC2("Outposts\n（自社の施設内）")

    users >> Edge(label="キャッシュ / 高速経路") >> edge
    edge >> Edge(label="AWS のネットワーク") >> az1
    az1 - Edge(label="低遅延の専用回線") - az2
    az2 - az3
    az1 >> Edge(label="VPC を拡張", style="dashed") >> local
    az2 >> Edge(label="VPC を拡張", style="dashed") >> wave
    az3 >> Edge(label="親リージョンに接続", style="dashed") >> outpost

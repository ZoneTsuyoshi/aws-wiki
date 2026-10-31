from diagrams import Cluster, Diagram
from diagrams.aws.compute import EC2
from diagrams.aws.network import (
    ELB,
    Endpoint,
    InternetGateway,
    TransitGateway,
    VPC,
)

with Diagram(
    "Transit Gateway と GWLB による集中検査",
    filename="docs/assets/diagrams/network-connectivity-inspection",
    outformat="png",
    show=False,
    graph_attr={"dpi": "150", "pad": "0.5"},
):
    spoke_a = VPC("スポーク VPC A")
    spoke_b = VPC("スポーク VPC B")
    tgw = TransitGateway("Transit Gateway")

    with Cluster("検査 VPC（アプライアンスモード）"):
        endpoint = Endpoint("GWLB\nエンドポイント")
        gwlb = ELB("GWLB")
        appliance_a = EC2("アプライアンス\nAZ-a")
        appliance_b = EC2("アプライアンス\nAZ-b")

    igw = InternetGateway("インターネット\nゲートウェイ")

    spoke_a >> tgw
    spoke_b >> tgw
    tgw >> endpoint >> gwlb
    gwlb >> appliance_a
    gwlb >> appliance_b
    endpoint >> igw

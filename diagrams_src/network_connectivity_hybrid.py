from diagrams import Cluster, Diagram
from diagrams.aws.network import (
    DirectConnect,
    SiteToSiteVpn,
    TransitGateway,
    VPC,
    VPCCustomerGateway,
)

with Diagram(
    "Direct Connect と VPN から Transit Gateway へ",
    filename="docs/assets/diagrams/network-connectivity-hybrid",
    outformat="png",
    show=False,
    graph_attr={"dpi": "150", "pad": "0.5"},
):
    with Cluster("オンプレミス"):
        router = VPCCustomerGateway("ルーター\nCGW")

    location = DirectConnect("DX ロケーション\nトランジット VIF")
    dxgw = DirectConnect("Direct Connect\nゲートウェイ")
    vpn = SiteToSiteVpn("Site-to-Site VPN\nバックアップ")

    with Cluster("AWS リージョン"):
        tgw = TransitGateway("Transit Gateway")
        prod = VPC("本番 VPC")
        dev = VPC("開発 VPC")
        shared = VPC("共有 VPC")

    router >> location >> dxgw >> tgw
    router >> vpn >> tgw
    tgw >> prod
    tgw >> dev
    tgw >> shared

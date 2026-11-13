from diagrams import Cluster, Diagram, Edge
from diagrams.aws.compute import EC2
from diagrams.aws.network import DirectConnect, Endpoint, Route53, Route53HostedZone
from diagrams.onprem.network import Bind9

with Diagram(
    "ハイブリッド DNS",
    filename="docs/assets/diagrams/network-connectivity-hybrid-dns",
    outformat="png",
    show=False,
    direction="LR",
    graph_attr={"dpi": "150", "pad": "0.5"},
):
    with Cluster("オンプレミス"):
        dns = Bind9("社内 DNS\n条件付き転送")

    line = DirectConnect("DX または VPN")

    with Cluster("共有サービス VPC"):
        inbound = Endpoint("インバウンド\nエンドポイント")
        outbound = Endpoint("アウトバウンド\nエンドポイント")
        resolver = Route53("VPC Resolver\n転送ルール")
        ec2 = EC2("EC2")

    phz = Route53HostedZone("プライベート\nホストゾーン")

    dns >> Edge(label="aws.example.com を引く") >> line
    line >> inbound >> resolver >> phz
    line << Edge(label="corp.example.com を転送") << outbound
    outbound << resolver
    resolver << ec2

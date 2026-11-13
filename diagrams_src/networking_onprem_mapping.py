from diagrams import Cluster, Diagram, Edge
from diagrams.aws.compute import EC2
from diagrams.aws.network import InternetGateway, Nacl, RouteTable
from diagrams.generic.network import Firewall, Router, Switch
from diagrams.onprem.compute import Server

with Diagram(
    "オンプレミスのネットワークと VPC の対応",
    filename="docs/assets/diagrams/networking-onprem-mapping",
    outformat="png",
    show=False,
    direction="TB",
    graph_attr={"dpi": "150", "pad": "0.5", "nodesep": "1.2"},
):
    with Cluster("自社データセンター"):
        o_router = Router("出口のルーター\nインターネット回線")
        o_l3 = Switch("L3 スイッチ\nVLAN 間の経路")
        o_fw = Firewall("ACL\nセグメントの境界")
        o_srv = Server("サーバー\nホストのファイアウォール")
        o_router >> o_l3 >> o_fw >> o_srv

    with Cluster("VPC"):
        a_igw = InternetGateway("インターネット\nゲートウェイ")
        a_rt = RouteTable("ルートテーブル\nVPC ルーター")
        a_nacl = Nacl("ネットワーク ACL\nサブネットの境界")
        a_ec2 = EC2("EC2\nセキュリティグループ")
        a_igw >> a_rt >> a_nacl >> a_ec2

    for left, right in [
        (o_router, a_igw),
        (o_l3, a_rt),
        (o_fw, a_nacl),
        (o_srv, a_ec2),
    ]:
        left - Edge(style="dashed", color="gray", constraint="false") - right

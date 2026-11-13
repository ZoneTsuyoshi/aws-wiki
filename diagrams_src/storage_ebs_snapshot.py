from diagrams import Cluster, Diagram, Edge
from diagrams.aws.compute import EC2
from diagrams.aws.storage import EBS, ElasticBlockStoreEBSSnapshot as Snapshot

with Diagram(
    "EBS スナップショットによる AZ とリージョンをまたぐ復元",
    filename="docs/assets/diagrams/storage-ebs-snapshot",
    outformat="png",
    show=False,
    graph_attr={"dpi": "150", "pad": "0.5", "splines": "spline"},
):
    with Cluster("東京リージョン"):
        with Cluster("AZ a"):
            src_ec2 = EC2("EC2")
            src_vol = EBS("EBS\nAZ 内で複製")
        snap = Snapshot("スナップショット\n(複数 AZ に保存)")
        with Cluster("AZ c"):
            new_vol = EBS("復元した EBS")
            new_ec2 = EC2("EC2")

    with Cluster("DR 用のリージョン"):
        dr_snap = Snapshot("コピーした\nスナップショット")
        dr_vol = EBS("復元した EBS")

    src_ec2 >> src_vol
    src_vol >> Edge(label="増分で取得") >> snap
    snap >> Edge(label="別の AZ に作成") >> new_vol
    new_vol >> new_ec2
    snap >> Edge(label="copy-snapshot") >> dr_snap
    dr_snap >> dr_vol

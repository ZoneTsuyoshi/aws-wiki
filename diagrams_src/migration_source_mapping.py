from diagrams import Cluster, Diagram, Edge
from diagrams.aws.compute import EC2
from diagrams.aws.database import Aurora
from diagrams.aws.migration import CloudendureMigration, DatabaseMigrationService, Datasync
from diagrams.aws.storage import EFS, S3Glacier, StorageGateway
from diagrams.generic.storage import Storage
from diagrams.onprem.compute import Server
from diagrams.onprem.database import Oracle

with Diagram(
    "移行元と移行先の対応",
    filename="docs/assets/diagrams/migration-source-mapping",
    outformat="png",
    show=False,
    direction="LR",
    graph_attr={"dpi": "150", "pad": "0.5", "nodesep": "0.6", "ranksep": "1.0"},
):
    with Cluster("オンプレミス"):
        server = Server("物理サーバー、VM")
        database = Oracle("DB サーバー")
        nas = Storage("NAS\nNFS、SMB")
        tape = Storage("テープ装置")

    with Cluster("移行のサービス"):
        mgn = CloudendureMigration("Transform MGN")
        dms = DatabaseMigrationService("DMS")
        datasync = Datasync("DataSync")
        gateway = StorageGateway("Tape Gateway")

    with Cluster("AWS"):
        ec2 = EC2("EC2")
        aurora = Aurora("RDS、Aurora")
        efs = EFS("EFS、FSx、S3")
        glacier = S3Glacier("S3、Glacier")

    server >> Edge(label="ブロック複製") >> mgn >> ec2
    database >> Edge(label="全ロード + CDC") >> dms >> aurora
    nas >> Edge(label="差分転送") >> datasync >> efs
    tape >> Edge(label="仮想テープ") >> gateway >> glacier

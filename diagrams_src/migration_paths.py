from diagrams import Cluster, Diagram, Edge
from diagrams.aws.compute import EC2
from diagrams.aws.database import RDS
from diagrams.aws.migration import CloudendureMigration, DatabaseMigrationService, Datasync
from diagrams.aws.storage import S3
from diagrams.onprem.compute import Server
from diagrams.onprem.database import Oracle

with Diagram(
    "移行の経路とサービス",
    filename="docs/assets/diagrams/migration-paths",
    outformat="png",
    show=False,
    graph_attr={"dpi": "150", "pad": "0.5"},
):
    with Cluster("オンプレミス"):
        server = Server("サーバー")
        database = Oracle("データベース")
        files = Server("NFS / SMB 共有")

    mgn = CloudendureMigration("AWS Transform MGN\nブロック単位の複製")
    dms = DatabaseMigrationService("AWS DMS\n全ロード + CDC")
    datasync = Datasync("DataSync\nファイルの転送")

    server >> Edge(label="エージェント") >> mgn >> EC2("EC2")
    database >> Edge(label="ログを読む") >> dms >> RDS("RDS / Aurora")
    files >> Edge(label="エージェント") >> datasync >> S3("S3 / EFS / FSx")

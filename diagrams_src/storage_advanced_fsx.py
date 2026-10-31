from diagrams import Cluster, Diagram, Edge
from diagrams.aws.compute import EC2
from diagrams.aws.storage import S3, Fsx, FsxForLustre, FsxForWindowsFileServer
from diagrams.onprem.client import Client

with Diagram(
    "FSx の 4 種類と接続",
    filename="docs/assets/diagrams/storage-advanced-fsx",
    outformat="png",
    show=False,
    graph_attr={"dpi": "150", "pad": "0.5"},
):
    windows_client = Client("Windows クライアント")
    linux_client = EC2("Linux の EC2")

    with Cluster("Amazon FSx"):
        windows = FsxForWindowsFileServer("Windows File Server\nSMB + AD")
        lustre = FsxForLustre("Lustre\nHPC、機械学習")
        ontap = Fsx("NetApp ONTAP\nNFS、SMB、iSCSI、NVMe")
        openzfs = Fsx("OpenZFS\nNFS")

    bucket = S3("S3 バケット")

    windows_client >> Edge(label="SMB") >> windows
    windows_client >> Edge(label="SMB") >> ontap
    linux_client >> Edge(label="Lustre クライアント") >> lustre
    linux_client >> Edge(label="NFS") >> ontap
    linux_client >> Edge(label="NFS") >> openzfs
    lustre >> Edge(label="データリポジトリ") >> bucket

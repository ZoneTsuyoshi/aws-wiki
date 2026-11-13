from diagrams import Cluster, Diagram, Edge
from diagrams.aws.analytics import GlueDataCatalog, Quicksight, Redshift
from diagrams.aws.storage import S3

with Diagram(
    "Redshift の構成とデータの置き場",
    filename="docs/assets/diagrams/data-engineering-redshift",
    outformat="png",
    show=False,
    graph_attr={"dpi": "150", "pad": "0.5", "splines": "spline"},
):
    bi = Quicksight("BI、SQL クライアント")

    with Cluster("Redshift クラスター(VPC 内)"):
        leader = Redshift("リーダーノード\n実行計画と集約")
        compute1 = Redshift("コンピュートノード\nスライスで並列")
        compute2 = Redshift("コンピュートノード\nスライスで並列")

    rms = S3("RMS\n計算と別に増える")

    with Cluster("データレイク"):
        catalog = GlueDataCatalog("Data Catalog")
        lake = S3("S3\n古いデータ")

    bi >> leader
    leader >> [compute1, compute2]
    compute1 >> rms
    compute2 >> rms
    leader >> Edge(label="Spectrum", style="dashed") >> catalog
    catalog >> Edge(style="dashed") >> lake

from diagrams import Cluster, Diagram
from diagrams.aws.analytics import Athena, Glue, GlueCrawlers, GlueDataCatalog, LakeFormation, Quicksight, Redshift
from diagrams.aws.storage import S3

with Diagram(
    "データレイクと分析の基本構成",
    filename="docs/assets/diagrams/data-engineering-pipeline",
    outformat="png",
    show=False,
    graph_attr={"dpi": "150", "pad": "0.5"},
):
    with Cluster("S3 データレイク"):
        raw = S3("raw（CSV、JSON）")
        curated = S3("curated（Parquet）")

    with Cluster("Glue"):
        crawler = GlueCrawlers("クローラー")
        catalog = GlueDataCatalog("Data Catalog")
        job = Glue("ETL ジョブ")

    lf = LakeFormation("Lake Formation")

    with Cluster("利用"):
        athena = Athena("Athena")
        redshift = Redshift("Redshift")
        quick = Quicksight("Quick Sight")

    raw >> job >> curated
    curated >> crawler >> catalog
    lf >> catalog
    catalog >> athena >> quick
    catalog >> redshift >> quick

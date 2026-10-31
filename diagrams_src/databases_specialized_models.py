from diagrams import Cluster, Diagram
from diagrams.aws.database import (
    Aurora,
    Database,
    DocumentDB,
    Dynamodb,
    ElastiCache,
    KeyspacesManagedApacheCassandraService,
    Neptune,
    RDS,
    Redshift,
    Timestream,
)

with Diagram(
    "データモデル別のデータベース",
    filename="docs/assets/diagrams/databases-specialized-models",
    outformat="png",
    show=False,
    graph_attr={"dpi": "150", "pad": "0.5"},
):
    with Cluster("リレーショナル"):
        rds = RDS("RDS")
        aurora = Aurora("Aurora")

    with Cluster("キーバリュー、ワイドカラム、ドキュメント"):
        dynamodb = Dynamodb("DynamoDB")
        keyspaces = KeyspacesManagedApacheCassandraService("Keyspaces")
        documentdb = DocumentDB("DocumentDB")

    with Cluster("インメモリ"):
        elasticache = ElastiCache("ElastiCache")
        memorydb = Database("MemoryDB")

    with Cluster("グラフ、時系列、分析"):
        neptune = Neptune("Neptune")
        timestream = Timestream("Timestream")
        redshift = Redshift("Redshift")

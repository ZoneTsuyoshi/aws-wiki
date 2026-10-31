from diagrams import Cluster, Diagram, Edge
from diagrams.aws.analytics import AmazonOpensearchService
from diagrams.aws.compute import Lambda
from diagrams.aws.ml import Bedrock
from diagrams.aws.storage import S3

with Diagram(
    "Knowledge Bases の取り込みと検索",
    filename="docs/assets/diagrams/genai-apps-rag",
    outformat="png",
    show=False,
    direction="TB",
    graph_attr={"dpi": "150", "pad": "0.5"},
):
    source = S3("データソース\n文書と .metadata.json")

    with Cluster("取り込み（同期）"):
        parser = Bedrock("解析とチャンク化\n＋埋め込みモデル")

    store = AmazonOpensearchService("ベクトルストア\nOpenSearch / pgvector / S3 Vectors")
    app = Lambda("アプリ\nRetrieve / RetrieveAndGenerate")
    generate = Bedrock("リランクと生成\nFM ＋ Guardrails")

    source >> parser >> store
    app >> Edge(label="質問") >> store
    store >> Edge(label="チャンク") >> generate
    generate >> Edge(label="回答と引用") >> app

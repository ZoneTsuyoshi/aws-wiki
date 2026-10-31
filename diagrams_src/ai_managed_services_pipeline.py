from diagrams import Diagram, Edge
from diagrams.aws.compute import Lambda
from diagrams.aws.ml import Bedrock, Comprehend, Textract, Transcribe
from diagrams.aws.storage import S3

with Diagram(
    "マネージド AI サービスの組み合わせ",
    filename="docs/assets/diagrams/ai-managed-services-pipeline",
    outformat="png",
    show=False,
    direction="TB",
    graph_attr={"dpi": "150", "pad": "0.5"},
):
    bucket = S3("入力\n通話音声 / 申込書 PDF")
    orchestrator = Lambda("Lambda\nイベントで起動")
    speech = Transcribe("Transcribe\n音声を文字に")
    document = Textract("Textract\nPDF から抽出")
    nlp = Comprehend("Comprehend\nPII と感情")
    fm = Bedrock("Bedrock\n要約と回答案")
    output = S3("出力\nJSON")

    bucket >> orchestrator
    orchestrator >> speech >> nlp
    orchestrator >> document >> nlp
    nlp >> Edge(label="マスク済みの文") >> fm >> output

from diagrams import Diagram, Edge
from diagrams.aws.analytics import Athena
from diagrams.aws.cost import Budgets, CostAndUsageReport, CostExplorer
from diagrams.aws.general import Users
from diagrams.aws.integration import SNS
from diagrams.aws.management import Organizations
from diagrams.aws.storage import S3

with Diagram(
    "コスト管理ツールの役割",
    filename="docs/assets/diagrams/cost-management-tools",
    outformat="png",
    show=False,
    graph_attr={"dpi": "150", "pad": "0.5"},
):
    payer = Organizations("課金データ\n（一括請求）")
    explorer = CostExplorer("Cost Explorer\n過去の分析と予測")
    budgets = Budgets("Budgets / 異常検出\nしきい値の通知")
    exports = CostAndUsageReport("Data Exports\n（CUR 2.0）")
    bucket = S3("S3")
    athena = Athena("Athena で明細を分析")
    topic = SNS("SNS / メール")
    finops = Users("担当者")

    payer >> explorer >> finops
    payer >> budgets >> Edge(label="通知") >> topic >> finops
    payer >> exports >> Edge(label="定期配信") >> bucket >> athena >> finops

from diagrams import Diagram
from diagrams.aws.compute import EC2, Lambda
from diagrams.aws.database import Dynamodb, DynamodbDax, DynamodbGlobalSecondaryIndex
from diagrams.aws.general import Users

with Diagram(
    "DynamoDBの読み書きと周辺機能",
    filename="docs/assets/diagrams/dynamodb-read-write",
    outformat="png",
    show=False,
    graph_attr={"dpi": "150", "pad": "0.5"},
):
    users = Users("利用者")
    app = EC2("アプリ")
    dax = DynamodbDax("DAX\n結果整合性の読み取りをキャッシュ")
    table = Dynamodb("テーブル")
    gsi = DynamodbGlobalSecondaryIndex("GSI\n非同期で更新")
    consumer = Lambda("Streamsの処理\n(イベントソースマッピング)")

    users >> app >> dax >> table
    table >> gsi
    table >> consumer

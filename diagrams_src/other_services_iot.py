from diagrams import Cluster, Diagram
from diagrams.aws.database import Dynamodb
from diagrams.aws.iot import IotCore, IotDeviceDefender, IotDeviceManagement, IotGreengrass, IotRule, IotSitewise
from diagrams.aws.storage import S3

with Diagram(
    "AWS IoT サービスの役割",
    filename="docs/assets/diagrams/other-services-iot",
    outformat="png",
    show=False,
    graph_attr={"dpi": "150", "pad": "0.5", "rankdir": "LR"},
):
    with Cluster("現場"):
        edge = IotGreengrass("Greengrass\nエッジの実行環境")
        site = IotSitewise("SiteWise\n産業機器のデータ")

    core = IotCore("IoT Core\nMQTT ブローカー")
    rule = IotRule("ルールエンジン")

    with Cluster("保存先の例"):
        table = Dynamodb("DynamoDB")
        bucket = S3("S3")

    with Cluster("フリート管理"):
        manage = IotDeviceManagement("Device Management")
        defend = IotDeviceDefender("Device Defender")

    edge >> core >> rule
    rule >> table
    rule >> bucket
    site >> bucket
    manage >> core
    defend >> core

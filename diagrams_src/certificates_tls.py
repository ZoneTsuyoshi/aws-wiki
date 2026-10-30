from diagrams import Cluster, Diagram
from diagrams.aws.compute import EC2
from diagrams.aws.general import Users
from diagrams.aws.network import ALB, CloudFront
from diagrams.aws.security import ACM, WAF

with Diagram(
    "証明書と WAF の配置",
    filename="docs/assets/diagrams/certificates-tls",
    outformat="png",
    show=False,
    graph_attr={"dpi": "150", "pad": "0.5", "rankdir": "LR"},
):
    users = Users("利用者")

    with Cluster("us-east-1 に作成"):
        edge_cert = ACM("ACM 証明書")
        edge_waf = WAF("WAF\nprotection pack")

    cdn = CloudFront("CloudFront")

    with Cluster("アプリのリージョン"):
        origin_cert = ACM("ACM 証明書")
        alb = ALB("ALB")
        app = EC2("EC2")

    users >> cdn >> alb >> app
    edge_cert >> cdn
    edge_waf >> cdn
    origin_cert >> alb

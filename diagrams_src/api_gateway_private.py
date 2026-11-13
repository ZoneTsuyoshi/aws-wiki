from diagrams import Cluster, Diagram, Edge
from diagrams.aws.compute import EC2, ECS, Lambda
from diagrams.aws.general import Users
from diagrams.aws.network import APIGateway, ElbApplicationLoadBalancer, Endpoint

with Diagram(
    "API Gateway のプライベート統合とプライベート API",
    filename="docs/assets/diagrams/api-gateway-private",
    outformat="png",
    show=False,
    graph_attr={"dpi": "150", "pad": "0.5", "rankdir": "LR"},
):
    users = Users("インターネットの\nクライアント")
    public_api = APIGateway("リージョン API\n(VPC の外)")
    private_api = APIGateway("プライベート API\n(VPC の外)")
    fn = Lambda("Lambda")

    with Cluster("VPC"):
        with Cluster("プライベートサブネット"):
            alb = ElbApplicationLoadBalancer("内部 ALB")
            app = ECS("ECS のサービス")
            internal = EC2("社内システム\nの EC2")
            vpce = Endpoint("インターフェイス\nエンドポイント\n(execute-api)")

    users >> public_api
    public_api >> Edge(label="VPC リンク") >> alb >> app
    internal >> vpce >> private_api >> fn

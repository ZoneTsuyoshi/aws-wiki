from diagrams import Cluster, Diagram, Edge
from diagrams.aws.compute import Fargate
from diagrams.aws.database import Aurora, ElastiCache
from diagrams.aws.network import ALB, CloudFront, Route53
from diagrams.aws.storage import S3
from diagrams.onprem.client import Users

with Diagram(
    "EC サイト: 商品ページと購入のリクエスト",
    filename="docs/assets/diagrams/ec-site-web",
    outformat="png",
    show=False,
    direction="TB",
    graph_attr={"dpi": "150", "pad": "0.5"},
):
    users = Users("購入者")

    with Cluster("グローバル"):
        dns = Route53("Route 53\nshop.example.com")
        cdn = CloudFront("CloudFront + WAF")

    with Cluster("リージョン（東京）"):
        images = S3("S3: 商品画像\nVPC の外")

        with Cluster("VPC 10.0.0.0/16"):
            alb = ALB("ALB\nパブリックサブネット 2 つ")

            with Cluster("AZ 1a"):
                app_a = Fargate("Fargate タスク\n10.0.10.0/24")
                db_a = Aurora("Aurora ライター\n10.0.20.0/24")
                cache_a = ElastiCache("ElastiCache\nプライマリ")

            with Cluster("AZ 1c"):
                app_c = Fargate("Fargate タスク\n10.0.11.0/24")
                db_c = Aurora("Aurora リーダー\n10.0.21.0/24")
                cache_c = ElastiCache("ElastiCache\nレプリカ")

    users >> dns
    users >> cdn
    cdn >> Edge(label="/images/*") >> images
    cdn >> Edge(label="それ以外") >> alb
    alb >> app_a
    alb >> app_c
    app_a >> db_a
    app_c >> db_a
    app_c >> db_c
    app_a >> cache_a
    app_c >> cache_a
    cache_a >> Edge(style="dashed") >> cache_c
    db_a >> Edge(style="dashed") >> db_c

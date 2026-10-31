from diagrams import Cluster, Diagram, Edge
from diagrams.aws.management import (
    ControlTower,
    Organizations,
    OrganizationsAccount,
    OrganizationsOrganizationalUnit,
)

with Diagram(
    "マルチアカウント構成の例",
    filename="docs/assets/diagrams/governance-multi-account",
    outformat="png",
    show=False,
    graph_attr={"dpi": "150", "pad": "0.5"},
):
    with Cluster("管理アカウント（ワークロードを置かない）"):
        org = Organizations("Organizations")
        ct = ControlTower("Control Tower")

    with Cluster("Security OU"):
        security_ou = OrganizationsOrganizationalUnit("SCP / RCP")
        log = OrganizationsAccount("ログ保管")
        audit = OrganizationsAccount("監査 / 委任管理者")

    with Cluster("Infrastructure OU"):
        network = OrganizationsAccount("ネットワーク\n（RAM で共有）")

    with Cluster("Workloads OU"):
        prod = OrganizationsAccount("本番")
        dev = OrganizationsAccount("開発")

    org >> Edge(label="ポリシーの継承") >> security_ou
    ct >> Edge(label="統制の適用", style="dashed") >> security_ou
    security_ou >> log
    security_ou >> audit
    org >> network
    org >> prod
    org >> dev

from diagrams import Cluster, Diagram
from diagrams.aws.management import OrganizationsAccount
from diagrams.aws.security import AdConnector, IAMRole, ManagedMicrosoftAd, SingleSignOn
from diagrams.onprem.client import Users

with Diagram(
    "IAM Identity Center の ID ソースとアカウント",
    filename="docs/assets/diagrams/identity-directory-sources",
    outformat="png",
    show=False,
    direction="TB",
    graph_attr={"dpi": "150", "pad": "0.5"},
):
    idc = SingleSignOn("IAM Identity Center")

    with Cluster("ID ソース（いずれか 1 つ）"):
        idp = Users("外部 IdP\nSAML と SCIM")
        managed = ManagedMicrosoftAd("Managed\nMicrosoft AD")
        connector = AdConnector("AD Connector\nオンプレ AD へ")

    with Cluster("メンバーアカウント"):
        role_a = IAMRole("権限セットの\nロール")
        account_a = OrganizationsAccount("開発アカウント")
        role_b = IAMRole("権限セットの\nロール")
        account_b = OrganizationsAccount("本番アカウント")

    idp >> idc
    managed >> idc
    connector >> idc
    idc >> role_a >> account_a
    idc >> role_b >> account_b

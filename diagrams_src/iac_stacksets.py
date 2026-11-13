from diagrams import Cluster, Diagram, Edge
from diagrams.aws.devtools import ToolsAndSdks
from diagrams.aws.management import Cloudformation, Organizations

with Diagram(
    "StackSets で複数のアカウントとリージョンへ展開する",
    filename="docs/assets/diagrams/iac-stacksets",
    outformat="png",
    show=False,
    direction="TB",
    graph_attr={"dpi": "150", "pad": "0.5", "splines": "spline"},
):
    with Cluster("管理アカウント(東京)"):
        template = ToolsAndSdks("テンプレート")
        stackset = Cloudformation("StackSet")
        org = Organizations("Organizations\nOU を指定")

    with Cluster("アカウント A"):
        a_tokyo = Cloudformation("東京の\nスタックインスタンス")
        a_osaka = Cloudformation("大阪の\nスタックインスタンス")

    with Cluster("アカウント B"):
        b_tokyo = Cloudformation("東京の\nスタックインスタンス")
        b_osaka = Cloudformation("大阪の\nスタックインスタンス")

    template >> stackset
    org - Edge(style="dashed", label="展開先") - stackset
    stackset >> [a_tokyo, a_osaka, b_tokyo, b_osaka]

# 分野1: ロードバランサー

どのロードバランサーを選ぶかと、設定の違いで起きる症状を問います。層と機能の対応から順に押さえます。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [L3、L4、L7 と選択](../../domain1.md#t1-3-choose) | L3、L4、L7 の負荷分散の仕組み、ロードバランサーの種類と要件、用途に合うロードバランサーの選択 |
| [内部と外部](../../domain1.md#t1-3-patterns) | 内部、外部の接続パターン |
| [スケーリング](../../domain1.md#t1-3-scaling) | スケーリングの要因、Auto Scaling との統合 |
| [他のサービスとの統合](../../domain1.md#t1-3-integrations) | 他サービスとの統合、既存のアプリへの統合 |
| [ロードバランサーの設定](../../domain1.md#t1-3-config) | 設定（プロキシプロトコル、クロスゾーン、スティッキー、アルゴリズム） |
| [ターゲットグループの設定](../../domain1.md#t1-3-target-groups) | ターゲットグループの設定（TCP、GENEVE、IP と instance） |
| [AWS Load Balancer Controller](../../domain1.md#t1-3-lbc) | AWS Load Balancer Controller |
| [暗号化と認証](../../domain1.md#t1-3-tls) | 暗号化と認証（TLS の終端、パススルー） |

## 学習の順番 {#study-order}

1. [ALB と NLB の違い](../../../../services/networking.md#alb-vs-nlb): 層、固定 IP、WAF の可否を表で覚えます。
2. [GWLB](../../../../services/networking.md#gwlb): 全ポートの透過と GENEVE の位置付けを確認します。
3. [ターゲットタイプ](../../../../services/networking.md#target-types): `instance` と `ip` で変わる送信元 IP とターゲットの範囲を押さえます。
4. [NLB の設定](../../../../services/networking.md#nlb-settings): クライアント IP の保持、プロキシプロトコル、TLS と TCP のリスナーを整理します。
5. [クロスゾーン負荷分散](../../../../services/networking.md#cross-zone): AZ の台数が偏ったときの割合を計算できるようにします。
6. [スティッキーセッション](../../../../services/networking.md#stickiness): スティッキーとアルゴリズムの併用の制限を確認します。
7. [EKS](../../../../services/containers.md#eks): AWS Load Balancer Controller と作られるリソースの対応を覚えます。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| ALB のサブネット | `/27` 以上、空き 8 個以上 | 足りないとスケールできない |
| NLB の接続数 | ターゲットあたり約 55,000 | クライアント IP の保持が無効のとき |
| GWLB のプロトコル | GENEVE、6081 | アプライアンスの MTU は 8568 以上 |
| 登録解除の待ち | 既定 300 秒 | 処理中の接続を待つ |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| URL のパス、Cognito、Lambda | ALB |
| 固定 IP、UDP、PrivateLink の提供 | NLB |
| 全ポートで第三者のアプライアンスを挟む | GWLB |
| ロードバランサーで復号してはならない | NLB の TCP パススルー |
| 固定 IP と L7 の両方 | NLB のターゲットに ALB、または Global Accelerator と ALB |
| Fargate の Pod を NLB に登録 | ターゲットは `ip` |

## 引っかかりやすい点 {#traps}

- スキームは作成後に変更できません。
- ターゲットの AZ にロードバランサーのサブネットがないと送れません。
- プロキシプロトコルを有効にするとヘルスチェックにもヘッダーが付きます。
- WAF は NLB に付けられません。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [elb 問1](../../exercises/elb.md#q1) | L3、L4、L7 と選択 | 次の 3 つの要件に対するロードバランサーの組み合わせとして正しいものはどれですか。要件 1: UR… |
| [elb 問2](../../exercises/elb.md#q2) | L3、L4、L7 と選択 | 既存の Web アプリは ALB のパスベースのルーティングに依存しています。新しい取引先は IP … |
| [elb 問3](../../exercises/elb.md#q3) | L3、L4、L7 と選択 | gRPC のマイクロサービスを、ヘッダーで振り分けます。また、ログのためにクライアント IP を X… |
| [elb 問4](../../exercises/elb.md#q4) | 内部と外部 | データセンターの古いサーバーから VPC へアプリを段階的に移します。移行の間、同じ ALB から新… |
| [elb 問5](../../exercises/elb.md#q5) | 内部と外部 | 3 層の Web アプリで、Web 層から App 層へのロードバランサーを設計します。App 層は… |
| [elb 問6](../../exercises/elb.md#q6) | 内部と外部 | インターネット向け ALB を AZ A と AZ B のパブリックサブネットに置きました。ターゲッ… |
| [elb 問7](../../exercises/elb.md#q7) | スケーリング | ALB を /28 のサブネットに置いており、大きなセールの最中に一部の AZ で 5xx が出まし… |
| [elb 問8](../../exercises/elb.md#q8) | スケーリング | Auto Scaling グループのインスタンスがアプリの異常で HTTP 500 を返し続けていま… |
| [elb 問9](../../exercises/elb.md#q9) | スケーリング | NLB の TCP ターゲットグループでクライアント IP の保持を無効にしました。1 台のターゲッ… |
| [elb 問10](../../exercises/elb.md#q10) | 他のサービスとの統合 | 既存の VM 上のアプリに ALB を入れます。ダウンタイムを避け、問題があればすぐ戻せるようにしま… |
| [elb 問11](../../exercises/elb.md#q11) | 他のサービスとの統合 | 非 HTTP の NLB の前に Global Accelerator を置き、ALB の前には C… |
| [elb 問12](../../exercises/elb.md#q12) | 他のサービスとの統合 | ALB をオリジンにした構成で、Route 53 のレコードが ALB の異常時に自動で別のリージョ… |
| [elb 問13](../../exercises/elb.md#q13) | ロードバランサーの設定 | NLB の ip ターゲットで、ターゲットは Transit Gateway の先のオンプレミスにあ… |
| [elb 問14](../../exercises/elb.md#q14) | ロードバランサーの設定 | NLB のターゲットグループでプロキシプロトコル v2 を有効にしました。アプリを未対応のまま有効に… |
| [elb 問15](../../exercises/elb.md#q15) | ロードバランサーの設定 | ショッピングサイトの ALB の設定を見直します。カートの情報をサーバーに持つアプリがあり、新しいタ… |
| [elb 問16](../../exercises/elb.md#q16) | ターゲットグループの設定 | GWLB のターゲットグループを作成します。仮想ファイアウォールの通信を受けるプロトコルとポートで正… |
| [elb 問17](../../exercises/elb.md#q17) | ターゲットグループの設定 | GWLB の検査を入れてから、大きなパケットだけが消えるようになりました。インターフェイスの MTU… |
| [elb 問18](../../exercises/elb.md#q18) | ターゲットグループの設定 | NLB の背後のアプリがクライアント IP をログに残します。ターゲットを EC2 と Fargat… |
| [elb 問19](../../exercises/elb.md#q19) | AWS Load Balancer Controller | EKS で Kubernetes の Service（type: LoadBalancer）を AW… |
| [elb 問20](../../exercises/elb.md#q20) | AWS Load Balancer Controller | AWS Load Balancer Controller を導入しましたが、Ingress を作って… |
| [elb 問21](../../exercises/elb.md#q21) | AWS Load Balancer Controller | Kubernetes のリソースと、AWS Load Balancer Controller が作る… |
| [elb 問22](../../exercises/elb.md#q22) | 暗号化と認証 | 規制で「ロードバランサーで復号してはならない」とされ、ターゲットが証明書と TLS の終端を持ちます… |
| [elb 問23](../../exercises/elb.md#q23) | 暗号化と認証 | ALB の HTTPS リスナーで終端したあと、ターゲットとの区間も暗号化します。ターゲットの証明書… |
| [elb 問24](../../exercises/elb.md#q24) | 暗号化と認証 | ALB のリスナーで、社内の OIDC プロバイダーを使って利用者を認証します。アプリは認証済みのリ… |

<!-- questions:end -->

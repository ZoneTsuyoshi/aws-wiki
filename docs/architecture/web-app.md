# Webアプリ構成（サンプル）

ページの書き方を示すサンプルです。実在の環境ではありません。

## 構成図

[![Webアプリ構成](../assets/diagrams/web-app.png)](../assets/diagrams/web-app.png)

## API リクエストの流れ

画像や CSS などの静的ファイルは、CloudFront が S3 から取得して返します。

```mermaid
sequenceDiagram
    actor U as ユーザー
    participant CF as CloudFront
    participant ECS as ALB / ECS
    participant RDS as RDS

    U->>CF: リクエスト
    CF->>ECS: 転送
    ECS->>RDS: クエリ
    RDS-->>ECS: 結果
    ECS-->>CF: レスポンス
    CF-->>U: レスポンス
```

## 各リソースの役割

| リソース | 役割 |
|---|---|
| CloudFront | HTTPS の終端、キャッシュ、パスごとの振り分け |
| S3 | 静的ファイルの保存 |
| ALB | ECS タスクへの負荷分散 |
| ECS | アプリケーションの実行 |
| RDS | データの保存 |

# 分野6: サービス別の学習

分野6（セキュリティの基盤とガバナンス）は SCS-C03 の配点の 14% です。マルチアカウントの土台、一貫した展開、準拠の評価を扱います。「止める」のか「見つける」のか「展開する」のかで、選ぶものが変わります。

```mermaid
flowchart TD
    A["1. Organizations と OU"] --> B["2. SCP と RCP と宣言型ポリシー"]
    B --> C["3. Control Tower"]
    C --> D["4. 委任管理者"]
    D --> E["5. ルートの管理"]
    E --> F["6. StackSets と Guard と Hooks"]
    F --> G["7. タグ"]
    G --> H["8. Firewall Manager と RAM"]
    H --> I["9. Config と修復"]
    I --> J["10. 監査と評価のツール"]
```

| 順番 | サービス | 問われること | 重要度 |
|---|---|---|---|
| 1 | [Organizations と Control Tower](organizations.md) | ポリシーの効く範囲、コントロール、委任管理者、ルート | 高 |
| 2 | [一貫した展開](deployment.md) | StackSets、検証ツール、タグ、Firewall Manager、共有 | 中 |
| 3 | [準拠の評価](compliance.md) | Config と修復、Artifact と Audit Manager、ベストプラクティスの評価 | 中 |

重要度は公式のスキル一覧を見たこの wiki の判断で、公式の数字ではありません。

## 他のサービスにまたがる問題 {#other-questions}

<!-- questions:start -->

この分野の問題は、すべてサービス別のページに載っています。

<!-- questions:end -->

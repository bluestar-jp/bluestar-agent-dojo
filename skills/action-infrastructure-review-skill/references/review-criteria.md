# Infrastructure Review Criteria

- Purpose: インフラ観点からのコードレビュー詳細基準
- Scope: 設定管理、デプロイメント戦略、リソース管理、ロギング、シークレット管理

## Critical/High チェック項目（必須）

### シークレット管理

| 項目 | チェック内容 |
| ---- | ------------ |
| ハードコード | APIキー、パスワードがコードに埋め込まれていないか |
| .envファイル | .envがgit管理外か |
| 暗号化 | シークレットが保存時・転送時に暗号化されているか |

### リソース管理

| 項目 | チェック内容 |
| ---- | ------------ |
| リソースリミット | CPU、メモリのリミットが設定されているか（K8s、Docker） |
| リソースリクエスト | 必要なリソース量が適切に要求されているか |
| オートスケーリング | 負荷に応じた自動スケーリングが設定されているか |

### ヘルスチェック

| 項目 | チェック内容 |
| ---- | ------------ |
| ヘルスチェック実装 | デプロイ後のヘルスチェックが実装されているか |
| プローブ設定 | liveness/readinessプローブが適切か |

## コード例

### リソースリミット

```yaml
# NG: リソースリミット未設定
apiVersion: v1
kind: Pod
spec:
  containers:
  - name: app
    image: myapp:latest

# OK: 適切なリソースリミット
apiVersion: v1
kind: Pod
spec:
  containers:
  - name: app
    image: myapp:latest
    resources:
      requests:
        memory: "256Mi"
        cpu: "250m"
      limits:
        memory: "512Mi"
        cpu: "500m"
```

### ヘルスチェック

```dockerfile
# NG: ヘルスチェック未設定
FROM node:18
CMD ["node", "server.js"]

# OK: ヘルスチェック実装
FROM node:18
HEALTHCHECK --interval=30s --timeout=3s --retries=3 \
  CMD curl -f http://localhost:3000/health || exit 1
CMD ["node", "server.js"]
```

## 重要度判定基準

| 重要度 | 条件 |
| ------ | ---- |
| Critical | シークレットがコードに露出、リソースリミット未設定でノード影響 |
| High | オートスケーリングの欠如、ヘルスチェックの不足 |
| Medium | ログ集約の欠如、デプロイ戦略の不明瞭さ |
| Low | コスト最適化の提案、軽微なリソース調整 |

## 参考リソース

- [12 Factor App](https://12factor.net/)
- [Kubernetes Best Practices](https://kubernetes.io/docs/concepts/configuration/overview/)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)

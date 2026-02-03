# Infrastructure Review Guidelines

- Purpose: インフラ観点からのコードレビュー基準
- Scope: 設定管理、デプロイメント戦略、リソース管理、ロギング・モニタリング、環境変数・シークレット管理

## レビュー観点

### 1. 設定管理 (Configuration Management)

#### チェック項目

- [ ] **Infrastructure as Code**: インフラがコード化されているか（Terraform、CloudFormation、Pulumi）
- [ ] **設定の外部化**: アプリケーション設定が環境変数や設定ファイルで管理されているか
- [ ] **環境分離**: 開発、ステージング、本番環境の設定が適切に分離されているか
- [ ] **設定のバージョン管理**: 設定ファイルがバージョン管理されているか
- [ ] **デフォルト値**: 適切なデフォルト値が設定されているか
- [ ] **設定の検証**: 起動時に設定値が検証されているか
- [ ] **機密情報の分離**: 機密情報が設定ファイルに含まれていないか

#### 重要度判定基準

- **Critical**: 本番環境設定の漏洩、設定ミスによるサービス停止
- **High**: 環境分離の欠如、機密情報のハードコード
- **Medium**: 設定の外部化不足、デフォルト値の不適切さ
- **Low**: 設定の構造改善、将来的なIaC化提案

### 2. デプロイメント戦略 (Deployment Strategy)

#### チェック項目

- [ ] **デプロイメント自動化**: CI/CDパイプラインが適切に設定されているか
- [ ] **ローリングアップデート**: ダウンタイムなしでデプロイできるか
- [ ] **ロールバック戦略**: 問題発生時に即座にロールバックできるか
- [ ] **ヘルスチェック**: デプロイ後のヘルスチェックが実装されているか
- [ ] **Blue-Green/Canary**: 段階的デプロイ戦略が適用されているか（必要に応じて）
- [ ] **データベースマイグレーション**: スキーマ変更が適切に管理されているか
- [ ] **依存関係の管理**: デプロイ順序や依存関係が明確か

#### 重要度判定基準

- **Critical**: デプロイ時のサービス停止、ロールバック不可
- **High**: デプロイ自動化の欠如、ヘルスチェックの不足
- **Medium**: ローリングアップデートの未実装、データベースマイグレーション戦略の不明瞭さ
- **Low**: デプロイプロセスの改善余地、将来的なCanary導入提案

### 3. リソース管理 (Resource Management)

#### チェック項目

- [ ] **リソースリミット**: CPU、メモリのリミットが適切に設定されているか（Kubernetes、Docker）
- [ ] **リソースリクエスト**: 必要なリソース量が適切に要求されているか
- [ ] **オートスケーリング**: 負荷に応じた自動スケーリングが設定されているか（HPA、ASG）
- [ ] **リソース効率**: 不要なリソース消費がないか（メモリリーク、CPU使用率）
- [ ] **ストレージ管理**: 永続化データの適切なストレージ戦略があるか
- [ ] **ネットワークリソース**: 帯域幅、接続数の制限が考慮されているか
- [ ] **コスト最適化**: リソース使用がコスト効率的か

#### 重要度判定基準

- **Critical**: リソースリミット未設定でノード全体に影響、重大なメモリリーク
- **High**: オートスケーリングの欠如、不適切なリソース配分
- **Medium**: リソース効率の改善余地、ストレージ戦略の不明瞭さ
- **Low**: コスト最適化の提案、軽微なリソース調整

### 4. ロギングとモニタリング (Logging & Monitoring)

#### チェック項目

- [ ] **構造化ログ**: ログがJSON等の構造化形式で出力されているか
- [ ] **ログレベル**: 適切なログレベル（DEBUG、INFO、WARN、ERROR）が使用されているか
- [ ] **ログの集約**: ログが中央集約システム（ELK、CloudWatch、Datadog）に送信されているか
- [ ] **メトリクス収集**: 重要なメトリクス（レスポンスタイム、エラー率）が収集されているか
- [ ] **アラート設定**: 異常検知時のアラートが適切に設定されているか
- [ ] **トレーシング**: 分散トレーシングが実装されているか（OpenTelemetry、Jaeger）
- [ ] **ダッシュボード**: 運用状況を可視化するダッシュボードがあるか

#### 重要度判定基準

- **Critical**: ログ記録の欠如、重大なエラーがアラートされない
- **High**: 構造化ログの未実装、メトリクス収集の不足
- **Medium**: ログ集約の欠如、アラート設定の不十分さ
- **Low**: ダッシュボードの改善、トレーシングの追加提案

### 5. 環境変数とシークレット管理 (Environment Variables & Secrets Management)

#### チェック項目

- [ ] **シークレット管理**: APIキー、パスワードが専用のシークレット管理サービスで管理されているか（AWS Secrets Manager、Vault、KMS）
- [ ] **環境変数の使用**: 設定が環境変数で渡されているか
- [ ] **シークレットのローテーション**: 定期的なシークレットローテーションが計画されているか
- [ ] **最小権限の原則**: 必要最小限の権限でシークレットにアクセスしているか
- [ ] **シークレットの暗号化**: 保存時・転送時に暗号化されているか
- [ ] **監査ログ**: シークレットアクセスが監査ログに記録されているか
- [ ] **.envファイルの管理**: .envファイルがgit管理外か、テンプレートのみコミットされているか

#### 重要度判定基準

- **Critical**: シークレットがコードやログに露出、アクセス制御の欠如
- **High**: シークレット管理サービスの未使用、暗号化の欠如
- **Medium**: ローテーション計画の不足、過剰な権限
- **Low**: .envファイル管理の改善、監査ログの追加

## レビュー出力形式

各ファインディングは以下の形式で出力してください：

```json
{
  "severity": "critical|high|medium|low",
  "category": "configuration|deployment|resource_management|logging_monitoring|secrets",
  "file": "relative/path/to/file.ext",
  "line": 45,
  "issue": "明確な問題の説明",
  "code_snippet": "該当するコードの抜粋（任意）",
  "suggestion": "具体的な改善提案",
  "references": [
    "https://12factor.net/...",
    "https://kubernetes.io/docs/..."
  ]
}
```

## コード例によるベストプラクティス

### ❌ 悪い例: リソースリミット未設定

```yaml
# POOR: リソースリミット未設定（Kubernetes）
apiVersion: v1
kind: Pod
spec:
  containers:
  - name: app
    image: myapp:latest
```

### ✅ 良い例: 適切なリソースリミット

```yaml
# GOOD: リソースリミット設定
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

### ❌ 悪い例: 非構造化ログ

```python
# POOR: 非構造化ログ、パースが困難
print(f"User {user_id} logged in at {timestamp}")
```

### ✅ 良い例: 構造化ログ

```python
# GOOD: JSON形式の構造化ログ
import json
import logging

logging.info(json.dumps({
    "event": "user_login",
    "user_id": user_id,
    "timestamp": timestamp,
    "ip_address": request.remote_addr
}))
```

### ❌ 悪い例: 環境変数の直接アクセス

```javascript
// POOR: 環境変数が存在しない場合のエラーハンドリングなし
const apiKey = process.env.API_KEY;
```

### ✅ 良い例: バリデーション付き環境変数アクセス

```javascript
// GOOD: 起動時に環境変数を検証
const requiredEnvVars = ['API_KEY', 'DATABASE_URL', 'REDIS_HOST'];
requiredEnvVars.forEach(envVar => {
  if (!process.env[envVar]) {
    throw new Error(`Missing required environment variable: ${envVar}`);
  }
});

const apiKey = process.env.API_KEY;
```

### ❌ 悪い例: ヘルスチェックの欠如

```dockerfile
# POOR: ヘルスチェック未設定
FROM node:18
COPY . /app
CMD ["node", "server.js"]
```

### ✅ 良い例: ヘルスチェック実装

```dockerfile
# GOOD: ヘルスチェックを実装
FROM node:18
COPY . /app
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:3000/health || exit 1
CMD ["node", "server.js"]
```

### ❌ 悪い例: シークレットをコンテナイメージに含める

```dockerfile
# DANGEROUS: シークレットがイメージレイヤーに残る
COPY .env /app/.env
```

### ✅ 良い例: ランタイムでシークレットを注入

```yaml
# GOOD: Kubernetes Secretsからランタイムで注入
apiVersion: v1
kind: Pod
spec:
  containers:
  - name: app
    image: myapp:latest
    env:
    - name: API_KEY
      valueFrom:
        secretKeyRef:
          name: app-secrets
          key: api-key
```

## 参考リソース

- [12 Factor App](https://12factor.net/)
- [Kubernetes Best Practices](https://kubernetes.io/docs/concepts/configuration/overview/)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- [AWS Well-Architected Framework](https://aws.amazon.com/architecture/well-architected/)
- [CNCF Cloud Native Landscape](https://landscape.cncf.io/)
- [Site Reliability Engineering](https://sre.google/books/)

---
name: infrastructure-review
description: インフラ観点（設定管理、リソース管理、シークレット管理）でコード差分をレビューし、JSON形式で結果を出力する。インフラコード（Docker、K8s、Terraform、CI/CD）のレビュー時に使用する。
---

# Infrastructure Code Review

- Purpose: インフラ観点でコード変更をレビュー
- Scope: 単一観点のコードレビュー

## 対象ファイルパターン

- `Dockerfile`, `docker-compose*.yml`
- `*.yaml`, `*.yml`（K8s manifests）
- `*.tf`, `*.tfvars`（Terraform）
- `.github/workflows/**`, `.gitlab-ci.yml`, `Jenkinsfile`
- `k8s/**`, `kubernetes/**`, `helm/**`

## レビュー観点（優先度順）

### Critical/High（必須チェック）

1. **シークレット管理**
   - ハードコードされた認証情報
   - .envファイルのコミット
   - 暗号化されていない機密情報

2. **リソースリミット**
   - CPU/メモリ制限の欠如（K8s）
   - OOMキラーの可能性

3. **ヘルスチェック**
   - 可用性確保の欠如
   - 不適切なプローブ設定

### Medium/Low（推奨チェック）

- 構造化ログ
- デプロイメント戦略（Blue-Green, Canary）
- 環境分離

## Claude Code ツール活用

- `Grep`: シークレットパターン、リソース設定の検索
- `Read`: 設定ファイルの詳細確認
- 不明確な場合: ユーザーに確認を求める

## 出力形式

```json
{
  "aspect": "infrastructure",
  "findings": [
    {
      "severity": "critical|high|medium|low",
      "category": "configuration|deployment|resource_management|logging_monitoring|secrets",
      "file": "path/to/file",
      "line": 45,
      "issue": "問題の説明",
      "suggestion": "改善提案"
    }
  ]
}
```

## 自己修正

- **本番/開発環境の判別が不確実**: 環境変数を確認
- **リソースリミットの妥当性が不明**: 一般的な推奨値と比較
- **誤検知の可能性**: コンテキストを追加確認

## 参照

詳細基準: `references/review-criteria.md`

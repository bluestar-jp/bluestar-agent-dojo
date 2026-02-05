# Security Review Criteria

- Purpose: セキュリティ観点からのコードレビュー詳細基準
- Scope: 認証/認可、入力検証、OWASP対策、機密情報管理

## Critical/High チェック項目（必須）

### 認証・認可

| 項目 | チェック内容 |
| ---- | ------------ |
| 認証バイパス | デバッグモードやテスト用の認証スキップが本番に含まれていないか |
| JWT検証 | トークンの署名検証が正しく実装されているか |
| 権限チェック | リソースアクセス前に適切な権限確認が行われているか |

### 入力検証

| 項目 | チェック内容 |
| ---- | ------------ |
| SQLインジェクション | ユーザー入力が直接SQLクエリに組み込まれていないか |
| XSS | ユーザー入力がエスケープされずにHTMLに埋め込まれていないか |
| コマンドインジェクション | ユーザー入力がシェルコマンドに直接渡されていないか |

### 機密情報

| 項目 | チェック内容 |
| ---- | ------------ |
| ハードコード | APIキー、パスワードがコードに直接埋め込まれていないか |
| ログ出力 | 機密情報がログに出力されていないか |
| エラーメッセージ | 内部実装の詳細が含まれていないか |

## コード例

### 認証バイパス

```javascript
// NG: デバッグモードで認証をスキップ
if (process.env.DEBUG === 'true') {
  return next(); // 認証バイパス
}

// OK: 常に認証を実行
const token = req.headers.authorization?.split(' ')[1];
if (!token || !verifyJWT(token)) {
  return res.status(401).json({ error: 'Unauthorized' });
}
return next();
```

### SQLインジェクション

```python
# NG: ユーザー入力を直接埋め込み
query = f"SELECT * FROM users WHERE username = '{username}'"

# OK: パラメータ化クエリ
query = "SELECT * FROM users WHERE username = ?"
cursor.execute(query, (username,))
```

### ハードコードされた認証情報

```go
// NG: APIキーがコードに直接埋め込み
const apiKey = "sk-1234567890abcdef"

// OK: 環境変数から読み込み
apiKey := os.Getenv("API_KEY")
if apiKey == "" {
  log.Fatal("API_KEY not set")
}
```

## 重要度判定基準

| 重要度 | 条件 |
| ------ | ---- |
| Critical | 認証バイパス、SQLインジェクション、コマンドインジェクション |
| High | XSS、パストラバーサル、弱いハッシュ関数 |
| Medium | 不完全な型チェック、エラーメッセージに過剰な情報 |
| Low | ログイン試行回数制限の欠如、軽微な脆弱性 |

## 参考リソース

- [OWASP Top 10 (2021)](https://owasp.org/Top10/)
- [OWASP Cheat Sheet Series](https://cheatsheetseries.owasp.org/)
- [CWE/SANS Top 25](https://cwe.mitre.org/top25/)

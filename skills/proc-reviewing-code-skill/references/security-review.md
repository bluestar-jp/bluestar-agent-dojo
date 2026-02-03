# Security Review Guidelines

- Purpose: セキュリティ観点からのコードレビュー基準
- Scope: 認証/認可、入力検証、OWASP対策、機密情報管理

## レビュー観点

### 1. 認証・認可 (Authentication & Authorization)

#### チェック項目

- [ ] **認証バイパス**: デバッグモードやテスト用の認証スキップが本番環境に含まれていないか
- [ ] **JWT検証**: トークンの署名検証が正しく実装されているか
- [ ] **セッション管理**: セッションIDが適切にランダム生成され、有効期限が設定されているか
- [ ] **パスワード保存**: パスワードがハッシュ化され、ソルト付きで保存されているか（bcrypt、Argon2など）
- [ ] **権限チェック**: リソースアクセス前に適切な権限確認が行われているか
- [ ] **多要素認証**: 重要な操作に対してMFA/2FAが実装されているか（該当する場合）

#### 重要度判定基準

- **Critical**: 認証バイパス、権限チェックの欠如、平文パスワード
- **High**: 弱いハッシュ関数（MD5、SHA1）、セッションハイジャック可能性
- **Medium**: 不適切なセッション有効期限、不十分なパスワードポリシー
- **Low**: ログイン試行回数制限の欠如、ログアウト機能の不備

### 2. 入力検証とサニタイゼーション (Input Validation & Sanitization)

#### チェック項目

- [ ] **SQLインジェクション**: ユーザー入力が直接SQLクエリに組み込まれていないか
- [ ] **XSS（クロスサイトスクリプティング）**: ユーザー入力がエスケープされずにHTMLに埋め込まれていないか
- [ ] **コマンドインジェクション**: ユーザー入力がシェルコマンドに直接渡されていないか
- [ ] **パストラバーサル**: ファイルパスにユーザー入力が使われ、検証が不十分でないか
- [ ] **LDAP/XMLインジェクション**: 外部システムへの入力が適切にエスケープされているか
- [ ] **型チェック**: 入力データの型が期待通りか検証されているか

#### 重要度判定基準

- **Critical**: SQLインジェクション、コマンドインジェクション、任意のコード実行
- **High**: XSS、パストラバーサル、LDAP/XMLインジェクション
- **Medium**: 不完全な型チェック、ファイルアップロード検証の不備
- **Low**: エラーメッセージに過剰な情報が含まれる

### 3. OWASP Top 10対策

#### チェック項目

- [ ] **A01:2021 - Broken Access Control**: 適切なアクセス制御が実装されているか
- [ ] **A02:2021 - Cryptographic Failures**: 暗号化が適切に実装されているか（TLS、暗号化アルゴリズム）
- [ ] **A03:2021 - Injection**: インジェクション攻撃への対策があるか
- [ ] **A04:2021 - Insecure Design**: セキュアな設計原則が適用されているか
- [ ] **A05:2021 - Security Misconfiguration**: セキュリティ設定が適切か（デフォルト設定、不要な機能の無効化）
- [ ] **A06:2021 - Vulnerable Components**: 既知の脆弱性を持つ依存関係を使用していないか
- [ ] **A07:2021 - Identification Failures**: 認証・識別メカニズムが適切か
- [ ] **A08:2021 - Software Integrity Failures**: ソフトウェアの整合性が保たれているか
- [ ] **A09:2021 - Security Logging Failures**: セキュリティイベントが適切にログ記録されているか
- [ ] **A10:2021 - SSRF**: サーバーサイドリクエストフォージェリへの対策があるか

#### 重要度判定基準

- **Critical**: A01（アクセス制御の破綻）、A03（インジェクション）
- **High**: A02（暗号の失敗）、A07（認証の失敗）
- **Medium**: A04（安全でない設計）、A05（セキュリティ設定ミス）
- **Low**: A09（ログ記録の失敗）

### 4. 機密情報の取り扱い (Sensitive Data Handling)

#### チェック項目

- [ ] **ハードコードされた認証情報**: APIキー、パスワード、秘密鍵がコードに直接埋め込まれていないか
- [ ] **環境変数の使用**: 機密情報が環境変数から読み込まれているか
- [ ] **ログ出力**: 機密情報（パスワード、トークン、個人情報）がログに出力されていないか
- [ ] **エラーメッセージ**: エラーメッセージに内部実装の詳細や機密情報が含まれていないか
- [ ] **データ暗号化**: 機密データが保存時・転送時に暗号化されているか
- [ ] **データマスキング**: 表示時にクレジットカード番号、電話番号などがマスキングされているか

#### 重要度判定基準

- **Critical**: ハードコードされた認証情報、平文での機密情報保存
- **High**: ログへの機密情報出力、暗号化されていない転送
- **Medium**: 不適切なエラーメッセージ、データマスキングの欠如
- **Low**: コメントに含まれる古い認証情報、過剰なデバッグ情報

### 5. 依存関係の脆弱性 (Dependency Vulnerabilities)

#### チェック項目

- [ ] **既知の脆弱性**: CVEデータベースに登録されている脆弱性を持つライブラリを使用していないか
- [ ] **古いバージョン**: EOL（End of Life）に達したライブラリやフレームワークを使用していないか
- [ ] **依存関係の更新**: package.json、requirements.txt、go.modなどで脆弱なバージョンが指定されていないか
- [ ] **トランジティブ依存**: 間接的な依存関係に脆弱性がないか
- [ ] **ライセンス**: 使用しているライブラリのライセンスが適切か

#### 重要度判定基準

- **Critical**: RCE（リモートコード実行）、認証バイパス、SQL インジェクションの脆弱性
- **High**: XSS、CSRF、権限昇格の脆弱性
- **Medium**: DoS（サービス拒否）、情報漏洩の脆弱性
- **Low**: 低リスクの脆弱性、ライセンス問題

## レビュー出力形式

各ファインディングは以下の形式で出力してください：

```json
{
  "severity": "critical|high|medium|low",
  "category": "authentication|input_validation|owasp|sensitive_data|dependencies",
  "file": "relative/path/to/file.ext",
  "line": 45,
  "issue": "明確な問題の説明",
  "code_snippet": "該当するコードの抜粋（任意）",
  "suggestion": "具体的な改善提案",
  "references": [
    "https://owasp.org/...",
    "https://cwe.mitre.org/..."
  ]
}
```

## コード例によるベストプラクティス

### ❌ 悪い例: 認証バイパス

```javascript
// DANGEROUS: デバッグモードで認証をスキップ
if (process.env.DEBUG === 'true') {
  return next(); // 認証バイパス
}
```

### ✅ 良い例: 適切な認証

```javascript
// 常に認証を実行
const token = req.headers.authorization?.split(' ')[1];
if (!token || !verifyJWT(token)) {
  return res.status(401).json({ error: 'Unauthorized' });
}
return next();
```

### ❌ 悪い例: SQLインジェクション

```python
# DANGEROUS: ユーザー入力を直接SQLに埋め込み
query = f"SELECT * FROM users WHERE username = '{username}'"
cursor.execute(query)
```

### ✅ 良い例: パラメータ化クエリ

```python
# プリペアドステートメントを使用
query = "SELECT * FROM users WHERE username = ?"
cursor.execute(query, (username,))
```

### ❌ 悪い例: ハードコードされた認証情報

```go
// DANGEROUS: APIキーがコードに直接埋め込まれている
const apiKey = "sk-1234567890abcdef"
```

### ✅ 良い例: 環境変数からの読み込み

```go
// 環境変数から読み込み
apiKey := os.Getenv("API_KEY")
if apiKey == "" {
  log.Fatal("API_KEY environment variable not set")
}
```

## 参考リソース

- [OWASP Top 10 (2021)](https://owasp.org/Top10/)
- [OWASP Cheat Sheet Series](https://cheatsheetseries.owasp.org/)
- [CWE/SANS Top 25](https://cwe.mitre.org/top25/)
- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)
- [Common Vulnerability Scoring System (CVSS)](https://www.first.org/cvss/)

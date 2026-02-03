# Backend Review Guidelines

- Purpose: バックエンド観点からのコードレビュー基準
- Scope: API設計、データベース最適化、エラーハンドリング、ビジネスロジック、スケーラビリティ

## レビュー観点

### 1. API設計とRESTful原則 (API Design & RESTful Principles)

#### チェック項目

- [ ] **RESTful命名**: エンドポイントがRESTful原則に従っているか（リソース名、HTTPメソッド）
- [ ] **HTTPステータスコード**: 適切なステータスコードを返しているか（200、201、400、404、500など）
- [ ] **リクエスト/レスポンス形式**: 一貫したJSON構造を使用しているか
- [ ] **バージョニング**: APIバージョン管理が適切か（/v1/、ヘッダーベースなど）
- [ ] **ペジネーション**: 大量データの取得に適切なペジネーションがあるか
- [ ] **フィルタリング/ソート**: クエリパラメータで適切にフィルタリング・ソートできるか
- [ ] **エンドポイントの一貫性**: 命名規則、レスポンス形式が統一されているか

#### 重要度判定基準

- **Critical**: APIが正常に動作しない、重大なセキュリティホール
- **High**: RESTful原則の重大な違反、不適切なHTTPステータスコード
- **Medium**: 命名規則の不一致、ペジネーションの欠如
- **Low**: 軽微なレスポンス形式の改善、将来的なバージョニング提案

### 2. データベースクエリ最適化 (Database Query Optimization)

#### チェック項目

- [ ] **N+1問題**: ループ内でクエリを実行していないか（eager loading、JOIN使用）
- [ ] **インデックス**: 頻繁に検索されるカラムにインデックスがあるか
- [ ] **SELECT文**: 必要なカラムのみを取得しているか（SELECT * の回避）
- [ ] **トランザクション**: 複数の更新操作が適切にトランザクション化されているか
- [ ] **クエリの複雑さ**: 過度に複雑なクエリがないか（分割やビュー化を検討）
- [ ] **接続管理**: データベース接続が適切にプール管理されているか
- [ ] **クエリキャッシュ**: 頻繁に実行されるクエリがキャッシュされているか

#### 重要度判定基準

- **Critical**: N+1問題で大量クエリ、トランザクション不整合
- **High**: インデックスの欠如、SELECT *の使用、接続リーク
- **Medium**: クエリの最適化余地、キャッシュの未使用
- **Low**: 軽微なクエリ改善、将来的なパフォーマンス向上

### 3. エラーハンドリング (Error Handling)

#### チェック項目

- [ ] **例外処理**: 適切なtry-catch、error handlingが実装されているか
- [ ] **エラーメッセージ**: ユーザーフレンドリーで、デバッグ可能なエラーメッセージか
- [ ] **ログ記録**: エラーが適切にログ記録されているか（スタックトレース、コンテキスト）
- [ ] **リトライロジック**: 一時的な障害に対するリトライメカニズムがあるか
- [ ] **グレースフルデグラデーション**: エラー時に適切なフォールバック処理があるか
- [ ] **エラーレスポンス**: 一貫したエラーレスポンス形式を使用しているか
- [ ] **バリデーションエラー**: 入力バリデーションエラーが適切に処理されているか

#### 重要度判定基準

- **Critical**: 例外が捕捉されずアプリケーションクラッシュ、機密情報の漏洩
- **High**: 不適切なエラーハンドリング、ログ記録の欠如
- **Medium**: エラーメッセージの改善余地、リトライロジックの欠如
- **Low**: エラーレスポンス形式の統一、軽微な改善

### 4. ビジネスロジックの妥当性 (Business Logic Validity)

#### チェック項目

- [ ] **ドメインモデル**: ビジネスロジックが適切なレイヤーに配置されているか
- [ ] **バリデーション**: ビジネスルールが適切にバリデーションされているか
- [ ] **データ整合性**: データの一貫性が保たれているか（外部キー、制約）
- [ ] **計算ロジック**: 金額計算、日付計算などが正確か（浮動小数点の扱いなど）
- [ ] **状態遷移**: ワークフローや状態遷移が適切に管理されているか
- [ ] **権限チェック**: ビジネスロジック実行前に権限が確認されているか
- [ ] **冪等性**: 重複実行しても問題ない設計か（POST、PUTなど）

#### 重要度判定基準

- **Critical**: ビジネスロジックの致命的な誤り、データ破壊の可能性
- **High**: バリデーション不足、データ整合性の問題
- **Medium**: ドメインモデルの改善余地、状態遷移の不明瞭さ
- **Low**: 軽微なロジック改善、コードの可読性向上

### 5. スケーラビリティ (Scalability)

#### チェック項目

- [ ] **非同期処理**: 重い処理が非同期化されているか（キュー、ワーカー）
- [ ] **キャッシュ戦略**: 適切なキャッシュレイヤーが使用されているか（Redis、Memcachedなど）
- [ ] **レート制限**: API呼び出しにレート制限が実装されているか
- [ ] **バッチ処理**: 大量データ処理が適切にバッチ化されているか
- [ ] **水平スケーリング**: ステートレス設計で水平スケーリング可能か
- [ ] **リソース管理**: メモリ、CPU使用量が適切か、リソースリークがないか
- [ ] **ボトルネック**: 処理のボトルネックが特定され、最適化されているか

#### 重要度判定基準

- **Critical**: リソースリーク、スケーラビリティの致命的な問題
- **High**: 同期的な重い処理、キャッシュの未使用
- **Medium**: レート制限の欠如、バッチ処理の改善余地
- **Low**: 軽微なパフォーマンス改善、将来的なスケーリング提案

## レビュー出力形式

各ファインディングは以下の形式で出力してください：

```json
{
  "severity": "critical|high|medium|low",
  "category": "api_design|database|error_handling|business_logic|scalability",
  "file": "relative/path/to/file.ext",
  "line": 45,
  "issue": "明確な問題の説明",
  "code_snippet": "該当するコードの抜粋（任意）",
  "suggestion": "具体的な改善提案",
  "references": [
    "https://restfulapi.net/...",
    "https://use-the-index-luke.com/..."
  ]
}
```

## コード例によるベストプラクティス

### ❌ 悪い例: N+1問題

```python
# POOR: ループ内でクエリを実行（N+1問題）
users = User.query.all()
for user in users:
    posts = Post.query.filter_by(user_id=user.id).all()  # N回のクエリ
```

### ✅ 良い例: Eager loading

```python
# GOOD: JOINで一度に取得
users = User.query.options(joinedload(User.posts)).all()
for user in users:
    posts = user.posts  # 追加クエリなし
```

### ❌ 悪い例: 不適切なエラーハンドリング

```javascript
// POOR: エラーが捕捉されず、詳細が失われる
app.post('/api/users', async (req, res) => {
  const user = await createUser(req.body);  // エラー時にクラッシュ
  res.json(user);
});
```

### ✅ 良い例: 適切なエラーハンドリング

```javascript
// GOOD: エラーを捕捉し、適切にログ記録・レスポンス
app.post('/api/users', async (req, res) => {
  try {
    const user = await createUser(req.body);
    res.status(201).json(user);
  } catch (error) {
    logger.error('Failed to create user', { error, body: req.body });
    res.status(500).json({ error: 'Failed to create user' });
  }
});
```

### ❌ 悪い例: 同期的な重い処理

```go
// POOR: 重いメール送信処理が同期的に実行され、レスポンスを遅延
func CreateOrder(w http.ResponseWriter, r *http.Request) {
    order := saveOrder(r.Body)
    sendConfirmationEmail(order)  // ブロッキング
    json.NewEncoder(w).Write(order)
}
```

### ✅ 良い例: 非同期処理

```go
// GOOD: メール送信を非同期キューに投入
func CreateOrder(w http.ResponseWriter, r *http.Request) {
    order := saveOrder(r.Body)
    queue.Enqueue("send_email", order.ID)  // 非同期
    json.NewEncoder(w).Write(order)
}
```

### ❌ 悪い例: SELECT *の使用

```sql
-- POOR: すべてのカラムを取得（不要なデータ転送）
SELECT * FROM users WHERE active = true;
```

### ✅ 良い例: 必要なカラムのみ取得

```sql
-- GOOD: 必要なカラムのみ指定
SELECT id, name, email FROM users WHERE active = true;
```

## 参考リソース

- [RESTful API Design Best Practices](https://restfulapi.net/)
- [Use The Index, Luke](https://use-the-index-luke.com/)
- [12 Factor App](https://12factor.net/)
- [Database Design Patterns](https://www.enterpriseintegrationpatterns.com/)
- [Microservices Patterns](https://microservices.io/patterns/)

# Backend Review Criteria

- Purpose: バックエンド観点からのコードレビュー詳細基準
- Scope: API設計、データベース最適化、エラーハンドリング、ビジネスロジック、スケーラビリティ

## Critical/High チェック項目（必須）

### データベース

| 項目 | チェック内容 |
| ---- | ------------ |
| N+1問題 | ループ内でクエリを実行していないか |
| インデックス | 頻繁に検索されるカラムにインデックスがあるか |
| SELECT * | 必要なカラムのみを取得しているか |
| トランザクション | 複数の更新操作が適切にトランザクション化されているか |

### エラーハンドリング

| 項目 | チェック内容 |
| ---- | ------------ |
| 例外処理 | 適切なtry-catch、error handlingが実装されているか |
| ログ記録 | エラーが適切にログ記録されているか |
| エラーレスポンス | 一貫したエラーレスポンス形式を使用しているか |

### API設計

| 項目 | チェック内容 |
| ---- | ------------ |
| RESTful命名 | エンドポイントがRESTful原則に従っているか |
| HTTPステータス | 適切なステータスコードを返しているか |
| ペジネーション | 大量データの取得に適切なペジネーションがあるか |

## コード例

### N+1問題

```python
# NG: ループ内でクエリを実行
users = User.query.all()
for user in users:
    posts = Post.query.filter_by(user_id=user.id).all()  # N回のクエリ

# OK: JOINで一度に取得
users = User.query.options(joinedload(User.posts)).all()
for user in users:
    posts = user.posts  # 追加クエリなし
```

### エラーハンドリング

```javascript
// NG: エラーが捕捉されない
app.post('/api/users', async (req, res) => {
  const user = await createUser(req.body);
  res.json(user);
});

// OK: 適切なエラーハンドリング
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

## 重要度判定基準

| 重要度 | 条件 |
| ------ | ---- |
| Critical | N+1問題で大量クエリ、トランザクション不整合 |
| High | インデックスの欠如、SELECT *の使用、接続リーク |
| Medium | クエリの最適化余地、キャッシュの未使用 |
| Low | 軽微なクエリ改善、将来的なパフォーマンス向上 |

## 参考リソース

- [RESTful API Design](https://restfulapi.net/)
- [Use The Index, Luke](https://use-the-index-luke.com/)
- [12 Factor App](https://12factor.net/)

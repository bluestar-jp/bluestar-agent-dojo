# Frontend Review Criteria

- Purpose: フロントエンド観点からのコードレビュー詳細基準
- Scope: UI/UX、アクセシビリティ、パフォーマンス、状態管理、コンポーネント設計

## Critical/High チェック項目（必須）

### アクセシビリティ

| 項目 | チェック内容 |
| ---- | ------------ |
| セマンティックHTML | `<button>`, `<nav>`, `<main>`等の適切な要素を使用 |
| キーボード操作 | すべてのインタラクティブ要素がキーボードで操作可能 |
| ARIA属性 | 必要に応じて`role`, `aria-label`を付与 |
| フォーカス管理 | フォーカスインジケーターが明確で論理的な順序 |

### パフォーマンス

| 項目 | チェック内容 |
| ---- | ------------ |
| 再レンダリング | 不要な再レンダリングが発生していないか |
| バンドルサイズ | 新規依存関係が過大なサイズ増加を引き起こしていないか |
| メモ化 | 高コストな計算が`useMemo`/`useCallback`でメモ化されているか |

### 状態管理

| 項目 | チェック内容 |
| ---- | ------------ |
| 状態の配置 | ローカル/グローバル状態が適切に分離 |
| 不変性 | 状態更新が不変的に行われている |
| エラー状態 | ローディング、エラー、成功の状態が適切に処理 |

## コード例

### アクセシビリティ

```jsx
// NG: divをボタンとして使用
<div onClick={handleClick}>Click me</div>

// OK: セマンティックHTML
<button onClick={handleClick} aria-label="Submit form">Click me</button>
```

### パフォーマンス

```jsx
// NG: 毎回新しいオブジェクトを作成
<ChildComponent config={{ theme: 'dark' }} />

// OK: メモ化
const config = useMemo(() => ({ theme: 'dark' }), []);
<ChildComponent config={config} />
```

## 重要度判定基準

| 重要度 | 条件 |
| ------ | ---- |
| Critical | ユーザー操作を阻害、重要なコンテンツが表示されない |
| High | レスポンシブデザインの重大な崩れ、キーボード操作不可 |
| Medium | 軽微なスタイルの不一致、メモ化の欠如 |
| Low | 細かいスタイル調整、将来的な改善提案 |

## 参考リソース

- [WCAG 2.1 Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)
- [React Performance](https://react.dev/learn/render-and-commit)
- [A11y Project](https://www.a11yproject.com/)

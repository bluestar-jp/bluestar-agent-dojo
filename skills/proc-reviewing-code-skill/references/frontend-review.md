# Frontend Review Guidelines

- Purpose: フロントエンド観点からのコードレビュー基準
- Scope: UI/UX、アクセシビリティ、パフォーマンス、状態管理、コンポーネント設計

## レビュー観点

### 1. UI/UXの一貫性 (UI/UX Consistency)

#### チェック項目

- [ ] **デザインシステム準拠**: 既存のデザインシステムやスタイルガイドに従っているか
- [ ] **レスポンシブデザイン**: モバイル、タブレット、デスクトップで適切に表示されるか
- [ ] **レイアウトの一貫性**: マージン、パディング、フォントサイズが統一されているか
- [ ] **カラーパレット**: 定義されたカラーパレットを使用しているか
- [ ] **タイポグラフィ**: フォントファミリー、サイズ、行間が適切か
- [ ] **インタラクティブ要素**: ボタン、リンク、フォームの状態（hover、active、disabled）が適切か

#### 重要度判定基準

- **Critical**: ユーザー操作を阻害する問題、重要なコンテンツが表示されない
- **High**: レスポンシブデザインの重大な崩れ、ブランドイメージの不一致
- **Medium**: 軽微なスタイルの不一致、改善の余地があるUX
- **Low**: 細かいスタイル調整、将来的な改善提案

### 2. アクセシビリティ (Accessibility)

#### チェック項目

- [ ] **セマンティックHTML**: 適切なHTML要素を使用しているか（`<button>`、`<nav>`、`<main>`など）
- [ ] **ARIA属性**: 必要に応じてARIA属性が付与されているか（`role`、`aria-label`など）
- [ ] **キーボード操作**: すべてのインタラクティブ要素がキーボードで操作可能か
- [ ] **フォーカス管理**: フォーカスインジケーターが明確で、論理的な順序か
- [ ] **スクリーンリーダー**: スクリーンリーダーで適切に読み上げられるか
- [ ] **カラーコントラスト**: WCAG基準（AA以上）を満たすコントラスト比か
- [ ] **代替テキスト**: 画像に適切なalt属性が設定されているか

#### 重要度判定基準

- **Critical**: キーボード操作不可、スクリーンリーダーで重要な情報が伝わらない
- **High**: セマンティックHTMLの欠如、カラーコントラスト不足
- **Medium**: ARIA属性の不足、フォーカス順序の問題
- **Low**: 代替テキストの改善、より良いARIAの使用

### 3. パフォーマンス (Performance)

#### チェック項目

- [ ] **レンダリングパフォーマンス**: 不要な再レンダリングが発生していないか
- [ ] **バンドルサイズ**: 新規依存関係が過大なバンドルサイズ増加を引き起こしていないか
- [ ] **コード分割**: ルートベースのコード分割が適用されているか
- [ ] **遅延読み込み**: 画像やコンポーネントが適切に遅延読み込みされているか
- [ ] **メモ化**: 高コストな計算が適切にメモ化されているか（useMemo、useCallbackなど）
- [ ] **リソース最適化**: 画像、フォント、CSSが最適化されているか
- [ ] **キャッシュ戦略**: 適切なキャッシュヘッダーやストレージ戦略が使われているか

#### 重要度判定基準

- **Critical**: ページロードが著しく遅延、ユーザー操作がブロックされる
- **High**: バンドルサイズの大幅増加、頻繁な不要再レンダリング
- **Medium**: 最適化されていない画像、メモ化の欠如
- **Low**: 軽微なパフォーマンス改善の余地

### 4. 状態管理の適切性 (State Management)

#### チェック項目

- [ ] **状態の配置**: ローカル状態とグローバル状態が適切に分離されているか
- [ ] **状態の構造**: 状態が正規化され、冗長性がないか
- [ ] **不変性**: 状態更新が不変的に行われているか
- [ ] **非同期処理**: API呼び出しやデータフェッチが適切に管理されているか
- [ ] **エラー状態**: ローディング、エラー、成功の状態が適切に処理されているか
- [ ] **状態の永続化**: 必要に応じて状態がlocalStorage/sessionStorageに保存されているか

#### 重要度判定基準

- **Critical**: 状態が破壊される、データ不整合が発生する
- **High**: 不適切なグローバル状態の使用、非同期処理の不備
- **Medium**: 状態構造の改善余地、エラー状態の不足
- **Low**: 状態の最適化、将来的なリファクタリング提案

### 5. コンポーネント設計 (Component Design)

#### チェック項目

- [ ] **単一責任の原則**: 各コンポーネントが単一の責任を持っているか
- [ ] **再利用性**: コンポーネントが適切に抽象化され、再利用可能か
- [ ] **Props設計**: Props名が明確で、型定義が適切か
- [ ] **コンポーネント分割**: 大きすぎるコンポーネントが適切に分割されているか
- [ ] **副作用の管理**: useEffect等の副作用が適切に管理されているか
- [ ] **テスタビリティ**: コンポーネントがテストしやすい設計か
- [ ] **命名規則**: コンポーネント名、関数名、変数名が一貫しているか

#### 重要度判定基準

- **Critical**: コンポーネントが正常に動作しない、メモリリーク
- **High**: 単一責任の原則違反、副作用の不適切な管理
- **Medium**: 再利用性の欠如、コンポーネント分割の必要性
- **Low**: 命名の改善、軽微なリファクタリング提案

## レビュー出力形式

各ファインディングは以下の形式で出力してください：

```json
{
  "severity": "critical|high|medium|low",
  "category": "ui_ux|accessibility|performance|state_management|component_design",
  "file": "relative/path/to/file.ext",
  "line": 45,
  "issue": "明確な問題の説明",
  "code_snippet": "該当するコードの抜粋（任意）",
  "suggestion": "具体的な改善提案",
  "references": [
    "https://web.dev/...",
    "https://www.w3.org/WAI/..."
  ]
}
```

## コード例によるベストプラクティス

### ❌ 悪い例: アクセシビリティの欠如

```jsx
// POOR: divをボタンとして使用、キーボード操作不可
<div onClick={handleClick}>Click me</div>
```

### ✅ 良い例: セマンティックHTML

```jsx
// GOOD: buttonタグを使用、キーボード操作可能
<button onClick={handleClick} aria-label="Submit form">
  Click me
</button>
```

### ❌ 悪い例: 不要な再レンダリング

```jsx
// POOR: 毎回新しいオブジェクトを作成
<ChildComponent config={{ theme: 'dark' }} />
```

### ✅ 良い例: メモ化

```jsx
// GOOD: メモ化して不要な再レンダリングを防止
const config = useMemo(() => ({ theme: 'dark' }), []);
<ChildComponent config={config} />
```

### ❌ 悪い例: 不適切な状態管理

```jsx
// POOR: 複数の関連する状態を個別に管理
const [loading, setLoading] = useState(false);
const [error, setError] = useState(null);
const [data, setData] = useState(null);
```

### ✅ 良い例: 統合された状態管理

```jsx
// GOOD: 関連する状態をまとめて管理
const [state, setState] = useState({
  loading: false,
  error: null,
  data: null
});
```

## 参考リソース

- [Web Vitals](https://web.dev/vitals/)
- [WCAG 2.1 Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)
- [React Performance Optimization](https://react.dev/learn/render-and-commit)
- [Lighthouse](https://developers.google.com/web/tools/lighthouse)
- [A11y Project](https://www.a11yproject.com/)

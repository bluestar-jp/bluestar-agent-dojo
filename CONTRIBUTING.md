# 開発者ガイド

このプロジェクトの開発に参加する際のガイドラインです。

## 必須ツール (Prerequisites)

このプロジェクトでは、コード品質を保つために以下のツールを使用しています。
macOS (Homebrew) 環境を前提としたセットアップ手順です。

### 1. ツールのインストール

以下のコマンドを実行して、LintツールとGitフック管理ツールをインストールしてください。

```bash
# Python (3.13推奨), Node.js (未インストールの場合)
brew install python node

# Lint & Hook Tools
# - lefthook: Gitフック管理
# - shellcheck: シェルスクリプト解析
# - ruff: Python高速Lint/Format
# - yamllint: YAML構文チェック
brew install lefthook shellcheck ruff yamllint
```

### 2. Gitフックの有効化

インストールした `lefthook` をGitリポジトリに紐付けます。これにより、コミット時に自動チェックが走るようになります。

```bash
lefthook install
```

## CI/CD パイプラインとローカルチェック

GitHub Actions上のCIパイプラインと同じチェックを、ローカルのGitフックで実行します。
これにより、プッシュ前のフィードバックループを高速化できます。

| ツール | 対象ファイル | 説明 |
| --- | --- | --- |
| **ShellCheck** | `*.sh` | シェルスクリプトの静的解析を行い、バグや危険な記述を検出します。 |
| **Ruff** | `*.py` | PythonコードのLintと自動修正を行います。 |
| **Yamllint** | `*.yml`, `*.yaml` | YAMLファイルの構文とフォーマットをチェックします。 |
| **Markdownlint** | `*.md` | ドキュメントのスタイルチェックを行います (npx経由で実行)。 |
| **Validate Plugin** | `plugin.json` 等 | プロジェクト独自の構造と命名規則を検証します。 |

### 手動でのチェック実行

特定のチェックを手動で実行することも可能です。

```bash
# すべてのフックを実行
lefthook run pre-commit

# 特定のフックのみ実行 (例: Pythonのチェック)
lefthook run pre-commit --commands ruff
```

## ディレクトリ構成の規則

新しいエージェントやスキルを追加する際は、以下の命名規則と構造に従ってください。
詳細は `scripts/verify-best-practices.py` によって検証されます。

- **Agents**: `agents/(shihan|deshi)-[name].md`
- **Skills**: `skills/(proc|action|cond)-[name]-skill/SKILL.md`

## 開発プロセス

### 1. Issue / Pull Request

1. **Issue作成**: 大きな変更を加える前には、まずIssueを作成して方針を議論してください。
2. **Branch作成**: `feature/xxx` や `fix/xxx` のような記述的なブランチ名を使用してください。
3. **Pull Request**: 作業が完了したらPRを作成し、レビューを依頼してください。提供されるテンプレートに従って内容を記述し、CIがパスすることを確認してください。

### 2. コミットメッセージ規約

本プロジェクトでは **Conventional Commits** 仕様を採用しています。
コミット時に `lefthook` の `commit-msg` フックにより自動的に検証されます。

**形式:**

```text
type(scope): subject
```

**Types:**

- `feat`: 新機能 (A new feature)
- `fix`: バグ修正 (A bug fix)
- `docs`: ドキュメントのみの変更 (Documentation only changes)
- `style`: コードの意味に影響しない変更 (formatting, spacing, etc)
- `refactor`: バグ修正も機能追加も行わないコードの変更 (A code change that neither fixes a bug nor adds a feature)
- `perf`: パフォーマンスを向上させる変更 (A code change that improves performance)
- `test`: テストの追加・修正 (Adding missing tests or correcting existing tests)
- `chore`: ビルドプロセスやツールの変更 (Changes to the build process or auxiliary tools)

**例:**

- `feat(skill): add new proc-reviewing-code-skill`
- `fix(ci): update workflow to use correct python version`
- `docs: update CONTRIBUTING.md with setup instructions`

### 3. スタイルガイド

- **言語**: ドキュメント、コメント、コミットメッセージは原則として **日本語** を使用してください。
- **ドキュメント**:
  - 明確で簡潔な表現を心がけてください。
  - 「です・ます」調（敬体）を基本としますが、仕様書やリスト内では「だ・である」調（常体）の使用も許容されます（統一されていれば可）。
- **世界観の維持**:
  - 「師範 (Shihan)」「弟子 (Deshi)」「巻物 (Makimono)」といったプロジェクト固有の用語・メタファーを正しく使用し、世界観を壊さないように配慮してください。

押忍 🥋

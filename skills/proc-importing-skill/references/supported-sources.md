# サポートされる取得元

- Purpose: 外部定義ファイルの取得元とその方法を定義する
- Scope: proc-importing-skillがサポートする全ての取得元タイプ

## 取得元タイプの分類

### 1. GitHub リポジトリ

#### 1.1 公開リポジトリ

### 取得元タイプの分類の形式

```text
https://github.com/{owner}/{repo}
https://github.com/{owner}/{repo}/tree/{branch}/{path}
```text

### 取得元タイプの分類の取得方法

```bash
# gh CLIを使用（推奨）
gh repo view {owner}/{repo} --json description,topics,readme
gh api repos/{owner}/{repo}/contents/{path}

# または git clone
git clone https://github.com/{owner}/{repo}.git /tmp/import_staging
```text

### メタデータ取得

- リポジトリの説明文（description）
- トピック（topics）
- README.md
- ライセンス情報
- 最終更新日時

### 取得元タイプの分類の例

```text
https://github.com/anthropics/anthropic-cookbook
https://github.com/langchain-ai/langchain/tree/master/templates
```text

#### 1.2 プライベートリポジトリ

### 取得元タイプの分類の認証方法

```bash
# GitHub Personal Access Tokenを使用
export GH_TOKEN="ghp_xxxxxxxxxxxx"
gh auth status

# または SSH鍵
git clone git@github.com:{owner}/{repo}.git
```text

### 取得元タイプの分類の注意事項

- トークンのスコープ: `repo` 権限が必要
- セキュリティ: トークンは環境変数で管理、ハードコードしない

### 2. HTTP(S) URL

#### 2.1 直接ファイルリンク

### 取得元タイプの分類の形式

```text
https://example.com/path/to/skill.md
https://raw.githubusercontent.com/{owner}/{repo}/{branch}/path/to/file.md
```text

### 取得元タイプの分類の取得方法

```bash
# curlを使用
curl -L -o /tmp/import_staging/skill.md \
  "https://example.com/path/to/skill.md"

# または WebFetchツール（Claude Code）
# 自動的にMarkdown変換とコンテンツ抽出
```text

### 取得元タイプの分類の対応形式

- Markdown (.md)
- JSON (.json)
- YAML (.yaml, .yml)
- HTML (自動的にMarkdownに変換)

### 取得元タイプの分類の例

```text
https://raw.githubusercontent.com/anthropics/claude-code/main/examples/skill-example.md
https://gist.githubusercontent.com/username/gist-id/raw/skill.md
```text

#### 2.2 アーカイブファイル

### 取得元タイプの分類の形式

```text
https://example.com/skills/package.zip
https://example.com/skills/package.tar.gz
```text

### 取得元タイプの分類の取得方法

```bash
# ZIPファイル
curl -L -o /tmp/import.zip "https://example.com/package.zip"
unzip /tmp/import.zip -d /tmp/import_staging

# tar.gzファイル
curl -L "https://example.com/package.tar.gz" | \
  tar xz -C /tmp/import_staging
```text

### 取得元タイプの分類の対応形式

- .zip
- .tar.gz
- .tar.bz2

### 3. ローカルファイルシステム

#### 3.1 ディレクトリ

### 取得元タイプの分類の形式

```text
/path/to/skill-directory
~/Downloads/custom-agent
```text

### 取得元タイプの分類の取得方法

```bash
# Readツール（Claude Code）
# または cp コマンド
cp -r /path/to/skill-directory /tmp/import_staging
```text

### 取得元タイプの分類の検証

```bash
# ディレクトリの存在確認
if [ -d "/path/to/skill-directory" ]; then
  echo "Directory exists"
else
  echo "Directory not found"
  exit 1
fi
```text

#### 3.2 単一ファイル

### 取得元タイプの分類の形式

```text
/path/to/skill.md
~/Documents/agent-definition.json
```text

### 取得元タイプの分類の取得方法

```bash
# Readツール（Claude Code）で直接読み込み
# または cp コマンド
cp /path/to/skill.md /tmp/import_staging/
```text

### 4. Git リモートURL

#### 4.1 HTTPS Git URL

### 取得元タイプの分類の形式

```text
https://github.com/{owner}/{repo}.git
https://gitlab.com/{owner}/{repo}.git
https://bitbucket.org/{owner}/{repo}.git
```text

### 取得元タイプの分類の取得方法

```bash
git clone --depth 1 \
  https://github.com/{owner}/{repo}.git \
  /tmp/import_staging
```text

### オプション

- `--depth 1`: 最新のコミットのみ取得（高速化）
- `--branch {branch}`: 特定のブランチを指定
- `--single-branch`: 単一ブランチのみ

#### 4.2 SSH Git URL

### 取得元タイプの分類の形式

```text
git@github.com:{owner}/{repo}.git
git@gitlab.com:{owner}/{repo}.git
```text

### 取得元タイプの分類の取得方法

```bash
# SSH鍵が設定されている前提
git clone --depth 1 \
  git@github.com:{owner}/{repo}.git \
  /tmp/import_staging
```text

### 5. パッケージマネージャー

#### 5.1 npm パッケージ

### 取得元タイプの分類の形式

```text
npm:{package-name}
npm:{package-name}@{version}
```text

### 取得元タイプの分類の取得方法

```bash
# npmでインストール
npm pack {package-name} --pack-destination /tmp
tar xzf /tmp/{package-name}-{version}.tgz -C /tmp/import_staging
```text

### 対象

- AIエージェント関連のnpmパッケージ
- ツールキットやユーティリティ

#### 5.2 PyPI パッケージ

### 取得元タイプの分類の形式

```text
pypi:{package-name}
pypi:{package-name}=={version}
```text

### 取得元タイプの分類の取得方法

```bash
# pipでダウンロード
pip download {package-name} --dest /tmp --no-deps
unzip /tmp/{package-name}-{version}.whl -d /tmp/import_staging
```text

### 6. コミュニティプラットフォーム

#### 6.1 Gist

### 取得元タイプの分類の形式

```text
https://gist.github.com/{username}/{gist-id}
```text

### 取得元タイプの分類の取得方法

```bash
# gh CLI
gh gist view {gist-id} > /tmp/import_staging/skill.md

# または git clone
git clone https://gist.github.com/{gist-id}.git /tmp/import_staging
```text

#### 6.2 HuggingFace Spaces

### 取得元タイプの分類の形式

```text
https://huggingface.co/spaces/{username}/{space-name}
```text

### 取得元タイプの分類の取得方法

```bash
# git clone (HuggingFaceはGitベース)
git clone https://huggingface.co/spaces/{username}/{space-name} \
  /tmp/import_staging
```text

### 取得元タイプの分類の注意事項

- スペースの構造は多様なため、追加の変換が必要

#### 6.3 Notion（エクスポート）

### 取得元タイプの分類の形式

```text
/path/to/notion-export.zip
```text

### 取得元タイプの分類の取得方法

```bash
# NotionからエクスポートしたZIPファイル
unzip notion-export.zip -d /tmp/import_staging

# Markdownファイルを抽出
find /tmp/import_staging -name "*.md"
```text

### 変換

- Notionの独自Markdown記法を標準Markdownに変換
- 画像リンクを相対パスに修正

## 取得元の自動検出

### URL判定ロジック

```python
import re
from urllib.parse import urlparse

def detect_source_type(source: str) -> str:
    """取得元のタイプを自動判定"""

    # GitHub URL
    if 'github.com' in source:
        return 'github'

    # GitLab URL
    if 'gitlab.com' in source or 'gitlab' in source:
        return 'gitlab'

    # Gist URL
    if 'gist.github.com' in source:
        return 'gist'

    # HuggingFace URL
    if 'huggingface.co' in source:
        return 'huggingface'

    # Git URL (.git拡張子)
    if source.endswith('.git'):
        return 'git'

    # HTTP(S) URL
    if source.startswith('http://') or source.startswith('https://'):
        parsed = urlparse(source)
        if parsed.path.endswith(('.zip', '.tar.gz', '.tar.bz2')):
            return 'archive'
        else:
            return 'http'

    # npm パッケージ
    if source.startswith('npm:'):
        return 'npm'

    # PyPI パッケージ
    if source.startswith('pypi:'):
        return 'pypi'

    # ローカルパス
    if source.startswith('/') or source.startswith('~/'):
        return 'local'

    # 不明
    return 'unknown'
```text

## 取得の優先順位

複数の方法が利用可能な場合の優先順位:

1. **gh CLI** - GitHub リポジトリの場合（最も信頼性が高い）
2. **git clone** - Gitリポジトリ全般（履歴も取得可能）
3. **WebFetch** - HTTP(S) URL（自動変換機能あり）
4. **curl** - 直接ダウンロード（シンプル）
5. **Read/cp** - ローカルファイル（最速）

## エラーハンドリング

### ネットワークエラー

```bash
# リトライロジック（最大3回）
for i in {1..3}; do
  if curl -f -L -o /tmp/file.md "https://example.com/file.md"; then
    break
  else
    echo "Retry $i/3..."
    sleep 2
  fi
done
```text

### 認証エラー

```bash
# GitHub認証の確認
if ! gh auth status 2>/dev/null; then
  echo "GitHub authentication required."
  echo "Run: gh auth login"
  exit 1
fi
```text

### ファイルが見つからない

```bash
# 404エラーの処理
if ! curl -f -s -o /dev/null "https://example.com/file.md"; then
  echo "File not found at URL."
  echo "Please verify the URL and try again."
  exit 1
fi
```text

## セキュリティ考慮事項

### 信頼できるソースの確認

- 公式リポジトリまたはコミュニティで実績のあるソースを優先
- 不明なスクリプトは実行前に内容を確認
- マルウェアスキャンの推奨

### トークンとクレデンシャルの管理

```bash
# 環境変数で管理
export GH_TOKEN="token_here"
export GITLAB_TOKEN="token_here"

# ハードコードしない
# ❌ gh auth login --with-token <<< "ghp_xxxxx"
# ✅ gh auth login --with-token < ~/.gh_token
```text

### SSL/TLS検証

```bash
# SSL証明書の検証を強制
curl --ssl-reqd -L "https://example.com/file.md"

# 自己署名証明書の場合のみ --insecure を使用（非推奨）
```text

## 使用例

### GitHub リポジトリから取得

```bash
@skills/proc-importing-skill

Import from:
https://github.com/anthropics/claude-code-examples/tree/main/skills/formatter

Type: skill
```text

### HTTP URLから取得

```bash
@skills/proc-importing-skill

Import from:
https://raw.githubusercontent.com/user/repo/main/agent-definition.md

Type: agent
```text

### ローカルディレクトリから取得

```bash
@skills/proc-importing-skill

Import from:
/Users/aono/Downloads/custom-skill

Type: skill
```text

### Gistから取得

```bash
@skills/proc-importing-skill

Import from:
https://gist.github.com/username/abc123def456

Type: skill
```text

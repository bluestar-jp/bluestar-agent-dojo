---
name: action-publishing-article-skill
description: 生成されたブログ記事MarkdownファイルをGitHubリポジトリにコミット・プッシュする。Zenn連携用ディレクトリ構造に対応。
---

# Article Publishing Skill (GitHub + Zenn)

- Purpose: 生成された記事をGitHubリポジトリに公開
- Scope: ファイル配置、Gitコミット・プッシュ、Zenn連携確認

## 入力形式

```json
{
  "generated_file": {
    "filename": "2024-03-15-nextjs-ogp-generation.md",
    "content": "<生成されたMarkdownの全文>",
    "frontmatter": {
      "title": "Next.jsでOGP画像を動的生成する方法",
      "published": false
    }
  },
  "repository": {
    "path": "/path/to/zenn-repo",
    "remote": "origin",
    "branch": "main"
  }
}
```

## 前提条件

### GitHubリポジトリの準備

1. Zenn連携済みのGitHubリポジトリが存在すること
2. `articles/` ディレクトリが存在すること（なければ作成）
3. Gitリポジトリが初期化されていること

### Zenn CLIのセットアップ（オプション）

```bash
# Zenn CLIのインストール（初回のみ）
npm install -g zenn-cli

# Zennリポジトリの初期化（初回のみ）
npx zenn init
```

## ワークフロー

### Step 1: ディレクトリ構造の確認

```bash
# articles/ ディレクトリの存在確認
ls -la <repo-path>/articles/

# 存在しない場合は作成
mkdir -p <repo-path>/articles/
```

### Step 2: ファイルの配置

```bash
# 生成されたMarkdownファイルをコピー
cp <generated-file> <repo-path>/articles/<filename>
```

**配置先**:

```text
<repo-path>/
  articles/
    2024-03-15-nextjs-ogp-generation.md
```

### Step 3: Gitコミット

```bash
cd <repo-path>

# ファイルをステージング
git add articles/<filename>

# コミットメッセージの生成
git commit -m "feat: Add blog post - <title>

<summary>

Co-authored-by: Claude Sonnet 4.5 <noreply@anthropic.com>"
```

**コミットメッセージの構造**:

- **プレフィックス**: `feat:` （新規記事追加）
- **タイトル**: `Add blog post - <記事タイトル>`
- **本文**: 記事の簡単な説明（オプション）
- **トレーラー**: `Co-authored-by: Claude Sonnet 4.5 <noreply@anthropic.com>`

**例**:

```text
feat: Add blog post - Next.jsでOGP画像を動的生成する方法

Next.jsでOGP画像を動的生成する手法を解説。
Vercel OG Imageライブラリの使い方と実装例を紹介。

Co-authored-by: Claude Sonnet 4.5 <noreply@anthropic.com>
```

### Step 4: Gitプッシュ

```bash
# リモートブランチへプッシュ
git push origin <branch>
```

### Step 5: Zenn連携確認

1. GitHubリポジトリのコミット履歴を確認
2. Zennダッシュボードで記事が表示されるか確認（<https://zenn.dev/dashboard）>
3. 下書き状態で正しく反映されているか確認

**確認ポイント**:

- [ ] GitHubにコミットが反映されている
- [ ] Zennダッシュボードに記事が表示されている
- [ ] frontmatterの`published: false`により下書き状態
- [ ] タイトル、絵文字、トピックスが正しく表示されている

## 出力形式

```json
{
  "published_article": {
    "filename": "2024-03-15-nextjs-ogp-generation.md",
    "path": "articles/2024-03-15-nextjs-ogp-generation.md",
    "git_commit_hash": "a1b2c3d4",
    "repository_url": "https://github.com/username/zenn-content",
    "commit_url": "https://github.com/username/zenn-content/commit/a1b2c3d4",
    "zenn_preview_url": "https://zenn.dev/username/articles/<slug>",
    "published_status": "draft"
  },
  "operations_performed": [
    "ファイル配置完了: articles/2024-03-15-nextjs-ogp-generation.md",
    "Gitコミット完了: a1b2c3d4",
    "Gitプッシュ完了: origin/main"
  ]
}
```

## エラーハンドリング

### ファイル配置失敗

**症状**: `articles/` ディレクトリが存在しない、権限エラー

**対応**:

1. ディレクトリを作成（`mkdir -p articles/`）
2. 権限を確認（`ls -la`）
3. それでも失敗なら、ユーザーに手動配置を依頼

### Gitコミット失敗

**症状**: 変更がない、コンフリクト、認証エラー

**対応**:

1. 変更内容を確認（`git status`）
2. コンフリクトがあれば、ユーザーに解決を依頼
3. 認証エラーの場合、ユーザーにGit設定を確認依頼

### Gitプッシュ失敗

**症状**: リモートブランチが存在しない、認証エラー、コンフリクト

**対応**:

1. リモートブランチを確認（`git branch -r`）
2. 認証エラーの場合、ユーザーにGitHub認証を確認依頼
3. コンフリクトの場合、`git pull --rebase` を提案
4. それでも失敗なら、ローカルにMarkdownファイルを保存し、手動プッシュを依頼

### Zenn連携が反映されない

**症状**: GitHubにはプッシュできたが、Zennダッシュボードに表示されない

**対応**:

1. Zenn連携設定を確認（<https://zenn.dev/dashboard/deploys）>
2. リポジトリとブランチが正しいか確認
3. 数分待ってから再確認（Zennの反映には時間がかかる場合あり）
4. それでも反映されない場合、Zennのドキュメントを参照しユーザーに確認依頼

## セーフティチェック

### プッシュ前の確認

- [ ] `published: false` であることを確認（意図しない公開を防ぐ）
- [ ] コミットメッセージが適切
- [ ] プッシュ先のブランチが正しい（`main` または `master`）

### ユーザー確認が必要なケース

以下の場合、ユーザーに確認を求める：

- `published: true` でプッシュしようとしている
- リモートブランチが `main` 以外
- 既に同名のファイルが存在する

## 自己修正

### ファイル名の重複

**症状**: 同名の記事ファイルが既に存在

**対応**:

1. ファイル名にサフィックスを追加（`-v2` 等）
2. ユーザーに確認を求める

### コミットメッセージの誤り

**症状**: コミットメッセージが不適切

**対応**:

1. `git commit --amend` で修正
2. ただし、プッシュ前のみ（プッシュ後は修正しない）

## スクリプト例

`scripts/publish.sh`:

```bash
#!/bin/bash

# 引数: <filename> <repo-path> <title>
FILENAME=$1
REPO_PATH=$2
TITLE=$3

# ディレクトリ確認
mkdir -p "$REPO_PATH/articles"

# ファイル配置
cp "$FILENAME" "$REPO_PATH/articles/"

# Git操作
cd "$REPO_PATH" || exit 1

git add "articles/$(basename "$FILENAME")"

git commit -m "feat: Add blog post - $TITLE

Co-authored-by: Claude Sonnet 4.5 <noreply@anthropic.com>"

git push origin main

echo "Published: articles/$(basename "$FILENAME")"
```

## 参照

- **Zenn CLI公式ガイド**: <https://zenn.dev/zenn/articles/zenn-cli-guide>
- **GitHubリポジトリ連携**: <https://zenn.dev/zenn/articles/connect-to-github>
- **コミットルール**: `makimono/ryunomaki/guidelines/project_structure_standards.md`（CLAUDE.mdのバージョン管理セクション）

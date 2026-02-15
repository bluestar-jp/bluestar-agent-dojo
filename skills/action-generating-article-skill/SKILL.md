---
name: action-generating-article-skill
description: 承認済みのブログ記事コンテンツからZenn対応のMarkdownファイルを生成する。frontmatter、本文フォーマット、ファイル名の生成を含む。
---

# Article Generation Skill (Zenn Markdown)

- Purpose: 承認済みコンテンツからZenn対応Markdown記事を生成
- Scope: Zenn frontmatter、Markdown構造、ファイル生成

## 入力形式

```json
{
  "approved_content": {
    "frontmatter": {
      "title": "記事タイトル",
      "emoji": "📝",
      "type": "tech",
      "topics": ["react", "typescript"],
      "published": false
    },
    "content": "<承認済みの本文（Markdown形式）>",
    "template_type": "how-to",
    "metadata": {
      "author": "執筆者名（オプション）",
      "created_at": "2024-03-15"
    }
  }
}
```

## ワークフロー

### Step 1: Frontmatterの生成

`makimono/ryunomaki/specs/blog_article_output_format.md` に基づきfrontmatterを生成：

```yaml
---
title: "記事タイトル（60文字以内）"
emoji: "📝"
type: "tech"
topics: ["react", "typescript", "nextjs"]
published: false
---
```

#### フィールド検証

- **title**: 60文字以内（超過時は警告）
- **emoji**: 1文字のUnicode絵文字（検証: `/^.$/u`）
- **type**: `tech` または `idea` のみ
- **topics**: 1-5個、小文字英数字とハイフンのみ（`/^[a-z0-9-]+$/`）
- **published**: boolean、初稿は`false`推奨

### Step 2: 本文のフォーマット

#### 見出し階層の調整

- H1は自動生成されるため、本文ではH2から開始
- 見出し階層が正しいか確認（H2→H3、H2の下にH4が直接来ない）

**検証**:

```bash
Grep: "^#{1,4} " で見出しレベルを抽出
```

#### コードブロックの検証

- すべてのコードブロックに言語指定があるか確認
- 言語指定がない場合は `text` を付与

**検証**:

```bash
Grep: "^```$" で言語指定なしコードブロックを検出
```

#### 画像パスの検証

- 相対パスまたはHTTPS URLであることを確認
- ローカルパス（`file://`）は警告

**検証**:

```bash
Grep: "!\[.*\]\((.*)\)" で画像パスを抽出
```

#### Zenn特有の記法サポート

Zennの埋め込み記法をサポート：

```markdown
# YouTube埋め込み
@[youtube](動画ID)

# Tweet埋め込み
@[tweet](ツイートID)

# CodePen埋め込み
@[codepen](https://codepen.io/...)

# スライド埋め込み
@[speakerdeck](スライドID)
```

### Step 3: ファイル名の生成

```text
<yyyy-mm-dd>-<slug>.md
```

- **日付**: 記事作成日（YYYY-MM-DD形式）
- **slug**: 記事を識別する短い文字列
  - タイトルから生成（日本語→ローマ字変換またはキーワード抽出）
  - 小文字英数字とハイフン
  - 20-50文字推奨

**slug生成ロジック**:

```text
例1:
  title: "Next.jsでOGP画像を動的生成する方法"
  slug: "nextjs-ogp-dynamic-generation"
  filename: "2024-03-15-nextjs-ogp-dynamic-generation.md"

例2:
  title: "ReactのパフォーマンスチューニングTips"
  slug: "react-performance-tuning-tips"
  filename: "2024-03-15-react-performance-tuning-tips.md"
```

### Step 4: ファイル生成

#### ディレクトリ構造

```text
articles/
  <yyyy-mm-dd>-<slug>.md
```

#### ファイル内容

```markdown
---
title: "記事タイトル"
emoji: "📝"
type: "tech"
topics: ["react", "typescript"]
published: false
---

## はじめに

<本文>

## まとめ

<本文>
```

#### 改行コード

- LF (`\n`) のみ使用（Zenn仕様）
- CRLF (`\r\n`) は変換

## 品質チェックリスト

生成後、以下を確認：

- [ ] Frontmatterが仕様に準拠している
- [ ] `title`が60文字以内
- [ ] `emoji`が1文字
- [ ] `type`が`tech`または`idea`
- [ ] `topics`が1-5個、小文字英数字とハイフンのみ
- [ ] `published`がboolean
- [ ] 見出し階層が正しい（H2から開始、H2→H3）
- [ ] コードブロックに言語指定がある
- [ ] 画像パスが相対パスまたはHTTPS URL
- [ ] ファイル名が規則に従っている（`[a-z0-9-]+\.md`）
- [ ] 改行コードがLF

## 出力形式

```json
{
  "generated_file": {
    "filename": "2024-03-15-nextjs-ogp-generation.md",
    "path": "articles/2024-03-15-nextjs-ogp-generation.md",
    "content": "<生成されたMarkdownの全文>",
    "frontmatter": {
      "title": "Next.jsでOGP画像を動的生成する方法",
      "emoji": "🖼️",
      "type": "tech",
      "topics": ["nextjs", "typescript", "ogp"],
      "published": false
    },
    "word_count": 1450,
    "validation_results": {
      "frontmatter_valid": true,
      "heading_hierarchy_valid": true,
      "code_blocks_valid": true,
      "image_paths_valid": true,
      "filename_valid": true
    }
  },
  "warnings": [
    "title is 65 characters (recommend < 60)"
  ]
}
```

## エラーハンドリング

### Frontmatter不正

**症状**: 必須フィールドが欠けている、値が不正

**対応**:

1. デフォルト値を補完（`published: false` 等）
2. 不正な値を修正（`topics`の大文字を小文字に変換）
3. 修正内容をwarningsに記載

### 見出し階層の乱れ

**症状**: H2の下にH4が直接来る等

**対応**:

1. H4をH3に調整
2. warningsに記載
3. ユーザーに確認を推奨

### コードブロックに言語指定なし

**症状**: ` ```\n<code>\n``` `

**対応**:

1. `text` を付与（` ```text\n<code>\n``` `）
2. warningsに記載

### ファイル名生成失敗

**症状**: タイトルから適切なslugを生成できない

**対応**:

1. フォールバック: `article-<timestamp>`
2. ユーザーにslugの提案を依頼

## 自己修正

### タイトルが長すぎる（60文字超）

- warningsに記載し、短縮案を提示
- ユーザー判断を仰ぐ

### topicsが不適切

- 小文字英数字とハイフン以外の文字を削除
- 5個超の場合、最初の5個を採用
- warningsに記載

### 画像パスが不正

- ローカルパスの場合、警告を表示
- 相対パスまたはHTTPS URLへの変更を推奨

## 参照

- **出力形式仕様**: `makimono/ryunomaki/specs/blog_article_output_format.md`
- **Zenn公式ドキュメント**: <https://zenn.dev/zenn/articles/zenn-cli-guide>
- **Markdown記法**: <https://zenn.dev/zenn/articles/markdown-guide>

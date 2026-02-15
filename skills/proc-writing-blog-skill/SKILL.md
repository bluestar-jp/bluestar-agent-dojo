---
name: proc-writing-blog-skill
description: 技術ブログ記事執筆のPAVEワークフロー全体（Plan→Agree→Execute→Verify→Generate & Publish）を実行する。並列レビュー（構造・読みやすさ + AIっぽさ除去）の統合を含む。
disable-model-invocation: false
---

# Blog Writing Workflow Skill

- Purpose: 技術ブログ記事執筆の全体ワークフロー（PAVE）を実行
- Scope: Plan → Agree → Execute → Verify → Generate & Publish

## 概要

このスキルは、技術ブログ記事の執筆を以下のフェーズで実行します：

1. **Plan**: テーマ分析とアウトライン構造化
2. **Agree**: ユーザー確認・調整
3. **Execute**: 段落執筆（sequential）
4. **Verify**: 並列セルフレビュー（2系統）+ 人間レビュー
5. **Generate & Publish**: Markdown記事生成・GitHub公開

## ワークフロー詳細

### Phase 1: Plan - テーマ分析とアウトライン構造化

#### 入力

- ユーザー提供のテーマ
- 段落構成案（段落数と各段落の概要）
- 対象読者（オプション）

#### 実行内容

1. **テーマ分析**
   - テーマの明確化
   - 対象読者の特定
   - 記事のゴール設定

2. **テンプレート選択**

   `makimono/ryunomaki/specs/blog_article_output_format.md` を参照し、最適なテンプレートを選択：
   - How-to: 特定の実装手順や問題解決
   - Deep Dive: 技術の内部仕組みや詳細分析
   - 比較: 複数技術の比較検討
   - 振り返り/事例: プロジェクト実践での学び
   - コンセプト解説: 抽象的な概念の説明

3. **アウトライン構造化**

   ```json
   {
     "theme": "記事テーマ",
     "article_type": "how-to",
     "template": {
       "sections": [
         {"heading": "はじめに", "level": 2},
         {"heading": "前提条件", "level": 2},
         {"heading": "手順", "level": 2}
       ]
     },
     "paragraphs": [
       {
         "id": "P1",
         "section": "はじめに",
         "outline": "課題の明示と記事のゴール",
         "key_points": ["課題の具体化", "記事で解決すること"],
         "estimated_words": 150
       }
     ]
   }
   ```

#### 出力

構造化されたアウトラインと実行計画（JSON形式）

---

### Phase 2: Agree - ユーザー確認

#### 実行内容

1. **アウトラインの提示**
   - 選択したテンプレートと理由
   - セクション構成
   - 各段落の概要とキーポイント
   - 推定文字数

2. **フィードバック収集**
   - セクションの追加/削除/順序変更
   - 段落の追加/削除/内容調整
   - キーポイントの修正

3. **アウトライン確定**
   - フィードバックを反映
   - 最終アウトラインを確定

#### 出力

確定したアウトライン（JSON形式）

---

### Phase 3: Execute - 段落執筆

#### 実行内容

1. **段落の順次執筆**

   `@action-composing-paragraph-skill` を使用して各段落を**sequential**に執筆：

   ```text
   P1執筆 → P2執筆（P1のコンテキスト使用） → P3執筆（P1, P2のコンテキスト使用） → ...
   ```

   **重要**: 前段落のコンテキストを次段落に渡すため、並列実行は不可。

2. **各段落の入力**:

   ```json
   {
     "paragraph_id": "P1",
     "section": "はじめに",
     "outline": "課題の明示と記事のゴール",
     "key_points": ["課題の具体化", "記事で解決すること"],
     "preceding_content": "<前段落までの内容>",
     "following_outline": "<次段落の概要>",
     "estimated_words": 150
   }
   ```

3. **ドラフト記事の組み立て**

   全段落を統合し、Markdown形式のドラフト記事を生成。

#### 出力

ドラフト記事（Markdown形式）

---

### Phase 4: Verify - 並列セルフレビュー

#### 実行内容

**重要**: 以下の2系統のレビューを**並列**実行（`Task`ツールの`run_in_background: true`）：

#### レビュー系統A: 構造・読みやすさレビュー

- **スキル**: `@action-reviewing-article-skill`
- **観点**:
  - 文章の流れ
  - 段落間の繋がり
  - 読みやすさ
  - 構成品質
- **出力**:

  ```json
  {
    "review_type": "structure_readability",
    "overall_quality": "good|needs_revision",
    "findings": [
      {
        "severity": "critical|high|medium|low",
        "category": "structure|flow|paragraph|...",
        "issue": "問題の説明",
        "suggestion": "改善提案"
      }
    ]
  }
  ```

#### レビュー系統B: AIっぽさ除去レビュー

- **スキル**: `@action-humanizing-article-skill`
- **観点**:
  - テンプレ感・説明書感
  - 記号過多
  - 過剰な丁寧さ
  - 前置き宣言
  - 抽象語の空回り
- **出力**:

  ```json
  {
    "review_type": "humanize",
    "overall_quality": "natural|needs_humanizing",
    "findings": [...],
    "rewritten_full_text": "書き換え後の全文"
  }
  ```

#### レビュー結果の統合

両系統の結果を統合：

```json
{
  "combined_review": {
    "structure_review": {...},
    "humanize_review": {...},
    "overall_status": "ok|needs_minor_revision|needs_major_revision",
    "revision_plan": [
      {
        "priority": "high",
        "action": "humanizer の書き換え提案を適用（P1, P3）",
        "affected_paragraphs": ["P1", "P3"]
      }
    ]
  }
}
```

#### 自己修正（最大2ラウンド）

1. **高優先度の問題から修正**
   - humanizerの書き換え提案を適用
   - 構造的な問題（トランジション、段落順序等）を修正

2. **修正後の検証**
   - 技術的正確性が維持されているか
   - 文字数が±20%以内か
   - 段落構成が維持されているか

3. **再レビュー（必要に応じて）**
   - 修正後も問題が残る場合、最大2ラウンドまで再実行

#### 人間レビューへの引き渡し

統合後のドラフトと両系統のレビュー結果をユーザーに提示。

---

### Phase 5: Human Review - 人間レビュー

#### 実行内容

1. **ドラフトの提示**
   - 修正後のドラフト記事
   - 両系統のレビュー結果
   - 自己修正内容

2. **フィードバック処理**

   `@action-revising-article-skill` を使用してフィードバックを処理：

   - **OK**: Phase 6へ進む
   - **NG**: 修正プラン策定 → Phase 3またはPhase 1へループバック

3. **修正ループ（NGの場合）**
   - 修正対象段落のみを再執筆（Phase 3へ）
   - 再レビュー実施（Phase 4へ）
   - 人間レビュー再実施

#### 出力

- 承認済みドラフト（OKの場合）
- 修正プラン（NGの場合）

---

### Phase 6: Generate & Publish - 記事生成・公開

#### 実行内容

1. **Markdown記事生成**

   `@action-generating-article-skill` を使用：

   - Zenn frontmatterの生成
   - 本文のフォーマット
   - ファイル名の生成

2. **GitHubリポジトリ公開**

   `@action-publishing-article-skill` を使用：

   - ファイル配置（`articles/`）
   - Git操作（add, commit, push）
   - Zenn連携確認

#### 出力

- 生成されたMarkdownファイル
- GitHubリポジトリURL
- Zenn記事プレビューURL

---

## エラーハンドリング

### 段落執筆失敗（Phase 3）

**症状**: 特定の段落が生成できない

**対応**:

1. アウトラインを簡略化して再試行
2. 前段落のコンテキストを調整
3. 最大2回リトライ後、ユーザーに報告

### レビュー失敗（Phase 4）

**症状**: レビュー系統の一方が失敗

**対応**:

1. 成功した系統の結果を保持
2. 失敗した系統を再実行（最大2回）
3. 片方のみでも人間レビューへ進む

### 自己修正失敗（Phase 4）

**症状**: 修正後も品質基準を満たさない

**対応**:

1. 修正前のドラフトを保持
2. レビュー結果を明示して人間レビューへ
3. ユーザー判断を仰ぐ

### 公開失敗（Phase 6）

**症状**: GitHubプッシュやZenn連携が失敗

**対応**:

1. ローカルにMarkdownファイルを保存
2. エラー詳細をユーザーに報告
3. 手動公開の手順を提示

---

## 並列実行の重要ポイント

### Phase 4で並列実行する理由

- **効率性**: 2つのレビューを同時実行することで時間短縮
- **独立性**: 構造レビューとAIっぽさ除去レビューは互いに独立
- **結果の統合**: 両系統の結果を統合することで包括的なレビュー

### 並列実行の方法（Claude Code本体向け）

Claude Code本体は以下の手順で並列実行：

```text
Phase 4 (Verify):

Claude Code本体:
  ├── Task(action-reviewing-article-skill, run_in_background: true)
  ├── Task(action-humanizing-article-skill, run_in_background: true)
  └── 両結果を収集 → 統合ロジック実行
```

### Phase 3でsequential実行する理由

- **コンテキスト依存**: 前段落の内容を次段落が参照する必要がある
- **一貫性**: 段落間のトランジションや繋がりを保つため
- **並列実行不可**: 前段落が完成しないと次段落を書けない

---

## ベストプラクティス

### 認知負荷の最小化

- SKILL.mdは簡潔に（ワークフローの概要のみ）
- 詳細は`makimono/`に切り出し
- 必要な知識ファイルのみ動的に読み込み

### ツールへのオフロード

- 複雑なロジックはaction-*スキルに委任
- Plan → Agree → Execute → Verify ループを明示
- 検証済みスキルで予測可能な動作

### 自律性の制御（Medium Autonomy）

- 手順は明確、解釈には柔軟性
- レビュー観点の適用はエージェントが判断
- ユーザーインタラクションは自由度高く

---

## 関連リソース

### 竜の巻（知識）

- `makimono/ryunomaki/guidelines/blog_writing_best_practices.md`
- `makimono/ryunomaki/guidelines/blog_review_criteria.md`
- `makimono/ryunomaki/guidelines/blog_humanize_rules.md`
- `makimono/ryunomaki/specs/blog_article_output_format.md`

### 虎の巻（手順）

- `makimono/toranomaki/procedure/blog_writing_workflow.md`
- `makimono/toranomaki/conditional_instructions/handling_blog_review_feedback.md`
- `makimono/toranomaki/single_action/blog_paragraph_scaffolding.md`

### スキル

- `skills/action-composing-paragraph-skill/`
- `skills/action-reviewing-article-skill/`
- `skills/action-humanizing-article-skill/`
- `skills/action-generating-article-skill/`
- `skills/action-publishing-article-skill/`
- `skills/action-revising-article-skill/`

### エージェント

- `agents/shihan-blog-writing.md` - このワークフローをオーケストレーション
- `agents/deshi-blog-composer.md` - 段落執筆を担当
- `agents/deshi-blog-reviewer.md` - 構造レビューを担当
- `agents/deshi-blog-humanizer.md` - AIっぽさ除去を担当

---

## 使用例

### 基本的な使用方法

```text
ユーザー: 「Reactのパフォーマンス最適化に関するHow-to記事を書きたい。段落は導入、前提条件、手順3つ、トラブルシューティング、まとめの7段落で。」

Claude Code:
  Phase 1: テーマ分析とアウトライン構造化
  Phase 2: アウトラインをユーザーに提示→確認
  Phase 3: 7段落を順次執筆
  Phase 4: 並列レビュー（構造 + AIっぽさ除去）→ 自己修正
  Phase 5: ドラフトをユーザーに提示→承認
  Phase 6: Markdown生成→GitHubプッシュ
```

### 修正ループの例

```text
ユーザー: 「段落P3のコード例の説明が不足している」

Claude Code:
  action-revising-article-skill → minor_revision判定
  Phase 3へループバック: P3のみ再執筆
  Phase 4へ: 再レビュー
  Phase 5へ: 再度ユーザー確認
```

---

## 出力形式

最終的な出力：

```json
{
  "published_article": {
    "filename": "2024-03-15-react-performance-tuning.md",
    "path": "articles/2024-03-15-react-performance-tuning.md",
    "git_commit_hash": "a1b2c3d4",
    "repository_url": "https://github.com/username/zenn-content",
    "zenn_preview_url": "https://zenn.dev/username/articles/react-performance-tuning",
    "published_status": "draft"
  },
  "workflow_summary": {
    "phases_completed": ["Plan", "Agree", "Execute", "Verify", "Generate & Publish"],
    "revision_rounds": 1,
    "total_paragraphs": 7,
    "word_count": 1800,
    "review_issues_resolved": 12
  }
}
```

# エージェント・スキルレビュー基準 (Agent & Skill Review Criteria)

このドキュメントは、AIエージェント（サブエージェント）およびスキルの定義をレビューする際の「良し悪し」を判断するための基準を定義します。エージェントが自律的に、かつ高品質な成果を出すための「巻物」としての質を評価します。

## 1. エージェント定義の評価軸

### 良い例の基準 (Success Patterns)

- **役割の明確化**: 「何者か」だけでなく「何のために存在し、何を優先するか（Mission）」が記述されている。
- **具体的ツールの活用**: どのツールを、どのようなコマンド（例：psql, grepの正規表現）で使うべきか具体的に示されている。
- **ワークフローの段階的定義**: 手順が「CRITICAL」「HIGH」などの優先度付きで整理されている。
- **知識の集約 (Patterns & Anti-Patterns)**: 単なる指示ではなく、具体的な「良いコードパターン」と「避けるべきコードパターン」がコード例と共に記載されている。
- **自己検証能力**: 自分の出力や判断をどう検証すべきか（Checklist）が含まれている。

### 悪い例の基準 (Anti-patterns)

- **抽象的な指示**: 「コードを良くしてください」「セキュリティを確認してください」といった、判断基準がAI任せの記述。
- **情報の不足**: どのディレクトリを見るべきか、どのコマンドを使うべきかの具体的指定がない。
- **長すぎる記述**: 一般的なプログラミング知識（AIが既に知っていること）を長々と書き、プロジェクト固有のルールが埋もれている。
- **ツールの誤用**: 本来スクリプトで自動化すべき手順を、エージェントに手動で推論させようとしている。

---

## 2. 代表的な良い例 (Exemplary Agent Definition)

以下の `database-reviewer` は、専門知識、具体的なツール使用法、そしてレビューのチェックリストが完璧に融合した、本プロジェクトにおける「免許皆伝」レベルの定義例です。

```markdown
---
name: database-reviewer
description: PostgreSQL database specialist for query optimization, schema design, security, and performance. Use PROACTIVELY when writing SQL, creating migrations, designing schemas, or troubleshooting database performance. Incorporates Supabase best practices.
tools: ["Read", "Write", "Edit", "Bash", "Grep", "Glob"]
model: opus
---

# Database Reviewer

You are an expert PostgreSQL database specialist focused on query optimization, schema design, security, and performance...

## Core Responsibilities
1. **Query Performance** - Optimize queries, add proper indexes, prevent table scans
...

## Tools at Your Disposal
### Database Analysis Commands
```bash
# Find missing indexes on foreign keys
psql -c "SELECT conrelid::regclass, a.attname FROM pg_constraint c JOIN pg_attribute a ON a.attrelid = c.conrelid AND a.attnum = ANY(c.conkey) WHERE c.contype = 'f' AND NOT EXISTS (SELECT 1 FROM pg_index i WHERE i.indrelid = c.conrelid AND a.attnum = ANY(i.indkey));"
```

## Index Patterns

### 1. Add Indexes on WHERE and JOIN Columns

**Impact:** 100-1000x faster queries on large tables

```sql
-- ❌ BAD: No index on foreign key
CREATE TABLE orders ( customer_id bigint REFERENCES customers(id) );
-- ✅ GOOD: Index on foreign key
CREATE INDEX orders_customer_id_idx ON orders (customer_id);
```

## Review Checklist

- [ ] All WHERE/JOIN columns indexed
- [ ] RLS policies use `(SELECT auth.uid())` pattern
...

```sql

---

## 3. 悪い例と改善策 (Bad Examples & Refactoring)

### ❌ 例1: 抽象的なセキュリティエージェント
> 「あなたはセキュリティの専門家です。コードを読み、脆弱性があれば指摘してください。」
>
> **なぜ悪いか**: 「脆弱性」の定義が広すぎ、エージェントは何を探せばいいか迷います。

### ✅ 改善後:
> 「あなたはWebアプリケーションのセキュリティ専門家です。特に**OWASP Top 10**に基づき、以下の3点を重点的にレビューしてください。
> 1. **SQL Injection**: `cursor.execute` に文字列結合が使われていないか。
> 2. **Broken Auth**: `JWT`の検証に `HS256` ではなく `RS256` が使われているか。
> 3. **Sensitive Data Exposure**: ログに `password` や `email` が出力されていないか。
> ツール `Grep` を使い `".*password.*"` などを検索してください。」

---

## 4. レビュー用チェックリスト (Reviewer's Checklist)

レビューアは以下の項目を確認し、一つでも「いいえ」があれば改善を促します。

1. [ ] **実行可能性**: エージェントは「最初にどのコマンドを叩くか」を迷わず判断できるか？
2. [ ] **独自性**: AIが元々持っている知識以上の「プロジェクト固有の知識・パターン」が含まれているか？
3. [ ] **具体性**: ❌（Bad）と ✅（Good）の対比コードが含まれているか？
4. [ ] **参照の適切さ**: スキルやドキュメントへのパス（例：`makimono/ryunomaki/...`）は正しいか？
5. [ ] **コンテキスト効率**: 冗長な丁寧語や、一般的すぎる説明でトークンを浪費していないか？

---
*このガイドラインは、道場の門下生が作成する全てのエージェント・スキルの品質を保証するための「目利き」の基準となります。*

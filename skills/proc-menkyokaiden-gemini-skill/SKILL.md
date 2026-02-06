---
name: menkyokaiden-gemini
description: Gemini Extensionsとしての設定を検証し、公開準備を行うワークフロー。フロントマター、context.md、ディレクトリ構造の整合性をチェックする。
disable-model-invocation: true
---

# Menkyokaiden Gemini - Extensions検証ワークフロー

> **Status**: Draft - 将来対応

- Purpose: Gemini Extensions としての設定を検証し、公開準備を行う
- Scope: フロントマター、context.md、ディレクトリ構造の整合性チェック

## 概要

このスキルは Gemini CLI / Gemini Extensions 向けのプラグイン検証を行います。
現在はドラフト状態であり、Gemini Extensions の仕様確定後に実装予定です。

## Gemini Extensions の要件（予定）

### フロントマターの差異

Claude Code との主な差異:

- `tools:` フィールドが配列形式
- `context:` フィールドでコンテキストファイルを指定

### context.md

プロジェクト全体のコンテキストを定義:

```markdown
# Project Context

このプロジェクトは...
```

### ディレクトリ構造

```text
.gemini/
├── context.md              # プロジェクトコンテキスト
├── agents/                 # エージェントアダプター
├── skills/                 # スキルアダプター
└── config.yaml             # 設定ファイル
```

## 実装予定

1. Gemini Extensions の仕様確定を待機
2. フロントマター差異の吸収ロジック実装
3. context.md の自動生成サポート
4. 検証スクリプトの追加

## 参照

- **プラグイン公開ガイド**: `menkyokaiden/README.md`

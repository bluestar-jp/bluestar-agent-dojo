---
name: proc-menkyokaiden-claude-skill
description: Claude Codeプラグインとしての設定を検証し、公開準備を行うワークフロー。plugin.json、フロントマター、ディレクトリ構造の整合性をチェックする。
disable-model-invocation: true
---

# Menkyokaiden Claude - プラグイン検証ワークフロー

- Purpose: Claude Code プラグインとしての設定を検証し、公開準備を行う
- Scope: plugin.json、フロントマター、ディレクトリ構造の整合性チェック

## ワークフロー (PAVE)

### Phase 1: Plan（検証計画）

以下の項目を検証対象として特定する:

1. **plugin.json の検証**
   - `.claude-plugin/plugin.json` の存在確認
   - 必須フィールド（name, version, description）の存在
   - agents/ と skills/ パスの正しい参照

2. **エージェントのフロントマター検証**
   - `agents/*.md` のフロントマター存在確認
   - 必須フィールド（name, description）の存在
   - ドラフト状態のエージェントは検証スキップ

3. **スキルのフロントマター検証**
   - `skills/*/SKILL.md` のフロントマター存在確認
   - 必須フィールド（name, description）の存在
   - proc-* スキルの `disable-model-invocation: true` 確認
   - ドラフト状態のスキルは検証スキップ

4. **マーケットプレイス検証**
   - `.claude-plugin/marketplace.json` の存在確認
   - `claude plugin validate .` による整合性チェック
   - すべての非ドラフトスキルがマーケットプレイスに登録されていること

5. **バージョン検証**
   - plugin.json のバージョンがセマンティックバージョニング形式であること

### Phase 2: Agree（確認）

検証対象を提示し、ユーザーの確認を得る:

- 検証対象のエージェント数
- 検証対象のスキル数
- マーケットプレイスに登録されているプラグイン数
- ドラフトとしてスキップするリソース

### Phase 3: Execute（検証実行）

```bash
# プラグイン構造の検証
./scripts/validate-plugin.sh

# フロントマター検証
python .github/scripts/verify_plugin_sync.py

# Markdownリント
npx markdownlint-cli2 "**/*.md"
```

### Phase 4: Verify（結果確認）

検証結果を報告:

- 成功: 公開準備完了
- 失敗: 問題点と修正方法を提示

## 検証チェックリスト

### plugin.json / marketplace.json

- [ ] `.claude-plugin/plugin.json` が存在する
- [ ] `.claude-plugin/marketplace.json` が存在する
- [ ] `claude plugin validate .` がパスする
- [ ] `name` フィールドが設定されている
- [ ] `version` フィールドがセマンティックバージョニング形式
- [ ] `agents` と `skills` パスが正しい

### エージェント / スキル

- [ ] すべての非ドラフトエージェントにフロントマターがある
- [ ] すべての非ドラフトスキルにフロントマターがある
- [ ] すべてのスキルが `marketplace.json` に登録されている
- [ ] `name` フィールドがファイル名またはディレクトリ名と一致
- [ ] `description` フィールドが設定されている

## エラーハンドリング

### plugin.json が見つからない

```bash
# 作成
mkdir -p .claude-plugin
echo '{"name": "bluestar-dojo", "version": "1.0.0"}' > .claude-plugin/plugin.json
```

### フロントマターが欠落

該当ファイルを編集し、以下の形式でフロントマターを追加:

```yaml
---
name: proc-menkyokaiden-claude-skill
description: リソースの説明。
---
```

## 参照

- **プラグイン公開ガイド**: `menkyokaiden/README.md`
- **検証スクリプト**: `.github/scripts/verify_plugin_sync.py`

# proc-importing-skill

外部リポジトリやコミュニティから良質なスキル・エージェント定義を取得し、bluestar-agent-dojoの構造に適合させて統合するスキルです。

## クイックスタート

### 基本的な使用方法

```bash
# GitHubからスキルをインポート
./scripts/import_workflow.sh \
  --source "https://github.com/example/ai-skill" \
  --type skill

# ローカルファイルからエージェントをインポート
./scripts/import_workflow.sh \
  --source "/path/to/agent-definition" \
  --type agent
```

### 自動承認モード

```bash
# ユーザー確認をスキップ（注意して使用）
./scripts/import_workflow.sh \
  --source "https://github.com/example/ai-skill" \
  --type skill \
  --auto-approve
```

## 機能

### サポートされる取得元

- **GitHub リポジトリ**: 公開/プライベートリポジトリ
- **HTTP(S) URL**: Markdown、JSON、YAMLファイル
- **アーカイブファイル**: ZIP、tar.gz
- **ローカルファイル**: ディレクトリまたは単一ファイル
- **Git リモート**: HTTPS/SSH Git URL
- **Gist**: GitHub Gist

詳細は `references/supported-sources.md` を参照してください。

### 主な処理

1. **取得**: 外部定義を自動取得
2. **分析**: 構造とメタデータを解析
3. **変換**: bluestar-agent-dojo標準に変換
4. **競合検出**: 既存リソースとの重複を確認
5. **検証**: 構造と依存関係を検証

## ワークフロー

### Phase 1: Plan（計画）

1. 取得元のタイプを自動判定
2. 定義ファイルを取得
3. 構造を分析
4. 命名規則を適用

### Phase 2: Agree（確認）

1. インポート計画を提示
2. 競合をチェック
3. ユーザーの承認を取得

### Phase 3: Execute（実行）

1. ディレクトリ構造を変換
2. ファイルを適切な場所に配置
3. メタデータを生成

### Phase 4: Verify（検証）

1. 構造の妥当性を検証
2. 依存関係を確認
3. 結果レポートを生成

## スクリプト

### 個別スクリプト

各フェーズを個別に実行可能:

```bash
# 1. 取得
python3 scripts/fetch_definition.py \
  --source "URL" \
  --type skill \
  --output-dir /tmp/import

# 2. 分析
python3 scripts/analyze_definition.py \
  --input-dir /tmp/import \
  --type skill \
  --output /tmp/analysis.json

# 3. 命名規則適用
python3 scripts/apply_naming.py \
  --input /tmp/analysis.json \
  --output /tmp/renamed.json

# 4. 構造変換
python3 scripts/convert_structure.py \
  --input /tmp/import \
  --output /tmp/converted \
  --config /tmp/renamed.json

# 5. 類似性チェック
python3 scripts/check_similarity.py \
  --new /tmp/converted/skills/new-skill \
  --existing ./skills

# 6. 構造検証
python3 scripts/validate_structure.py \
  --path ./skills/new-skill \
  --type skill

# 7. 依存関係チェック
python3 scripts/check_dependencies.py \
  --path ./skills/new-skill
```

### 統合スクリプト

すべてのフェーズを自動実行:

```bash
./scripts/import_workflow.sh \
  --source "URL or path" \
  --type skill
```

## 依存関係

### 必須

- **Python 3.7+**: スクリプト実行
- **Bash**: ワークフローシェルスクリプト
- **jq**: JSON処理

### オプション（取得元による）

- **gh CLI**: GitHub リポジトリから取得
- **git**: Gitリポジトリのクローン
- **curl**: HTTP(S)からのダウンロード

### インストール方法

```bash
# macOS
brew install python3 jq gh git

# Ubuntu/Debian
apt-get install python3 jq git curl
gh auth login

# Python依存なし（標準ライブラリのみ使用）
```

## ディレクトリ構造

```
proc-importing-skill/
├── SKILL.md                          # メインドキュメント
├── README.md                         # このファイル
├── scripts/                          # 実行スクリプト
│   ├── import_workflow.sh           # 統合ワークフロー
│   ├── fetch_definition.py          # 外部定義の取得
│   ├── analyze_definition.py        # 構造分析
│   ├── apply_naming.py              # 命名規則適用
│   ├── convert_structure.py         # ディレクトリ構造変換
│   ├── check_similarity.py          # 類似性チェック
│   ├── validate_structure.py        # 構造検証
│   └── check_dependencies.py        # 依存関係確認
└── references/                       # 参照ドキュメント
    ├── naming-conversion.md         # 命名規則変換ルール
    ├── structure-template.json      # ディレクトリ構造テンプレート
    ├── supported-sources.md         # サポートされる取得元
    ├── skill-template.md            # スキルテンプレート
    └── agent-template.md            # エージェントテンプレート
```

## 使用例

### 例1: GitHubからスキルをインポート

```bash
cd /Users/aono/develop/bluestar/bluestar-agent-dojo

./skills/proc-importing-skill/scripts/import_workflow.sh \
  --source "https://github.com/anthropics/claude-code-examples/tree/main/skills/formatter" \
  --type skill
```

出力:
```
[INFO] Starting import workflow
[INFO] Source: https://github.com/anthropics/claude-code-examples/tree/main/skills/formatter
[INFO] Type: skill

========================================
Phase 1: PLAN - Fetch and Analyze
========================================

[INFO] Fetching definition from source...
[SUCCESS] Fetched 5 files

[INFO] Analyzing definition...
[INFO] Original name: formatter
[INFO] Description: Code formatting tool

[INFO] Applying naming conventions...
[SUCCESS] Name conversion: formatter → action-formatting-code-skill

========================================
Phase 2: AGREE - User Confirmation
========================================

Import Plan:
  Source:        https://github.com/...
  Type:          skill
  Original name: formatter
  New name:      action-formatting-code-skill
  Target path:   /Users/.../skills/action-formatting-code-skill

[INFO] Checking similarity with existing resources...
[INFO] No conflicts detected

Proceed with import? [y/N]: y

========================================
Phase 3: EXECUTE - Convert and Deploy
========================================

[INFO] Converting directory structure...
[INFO] Deploying converted resource...
[SUCCESS] Resource deployed

========================================
Phase 4: VERIFY - Validation
========================================

[INFO] Validating structure...
✓ Validation PASSED

[INFO] Checking dependencies...
✓ All dependencies satisfied

========================================
Import Complete!
========================================
```

### 例2: ローカルファイルからエージェントをインポート

```bash
./skills/proc-importing-skill/scripts/import_workflow.sh \
  --source "/Users/aono/Downloads/security-analyst" \
  --type agent
```

### 例3: 自動承認モードでインポート

```bash
./skills/proc-importing-skill/scripts/import_workflow.sh \
  --source "https://gist.github.com/username/abc123" \
  --type skill \
  --auto-approve
```

## トラブルシューティング

### エラー: GitHub認証が必要

```
[ERROR] GitHub authentication required
```

解決方法:
```bash
gh auth login
```

### エラー: 依存関係が不足

```
[WARNING] Some dependencies are missing
```

解決方法:
```bash
# macOS
brew install jq gh git

# Ubuntu
apt-get install jq git curl
```

### エラー: 既存リソースと競合

```
[WARNING] Target directory already exists
```

解決方法:
- オプション1: 既存リソースを削除してから再実行
- オプション2: 異なる名前を指定
- オプション3: インポートをキャンセル

### エラー: 構造検証失敗

```
[ERROR] SKILL.md missing required field: Purpose
```

解決方法:
- インポート後に手動でSKILL.mdを編集
- 必須フィールド（Purpose, Scope）を追加

## ベストプラクティス

### 取得元の選択

- 公式リポジトリやコミュニティで実績のあるソースを優先
- プライベートリポジトリは信頼できるソースのみ使用
- 不明なスクリプトは実行前に内容を確認

### インポート後の作業

1. **レビュー**: SKILL.md/AGENT.mdの内容を確認
2. **調整**: 必要に応じて修正や追加
3. **テスト**: 機能が正常に動作するか確認
4. **ドキュメント**: 使用例や注意事項を追記
5. **コミット**: Gitにコミットして変更を記録

### セキュリティ

- 実行前にスクリプトの内容を確認
- 認証トークンは環境変数で管理
- 機密情報を含むファイルは除外

## 制限事項

- **認証が必要なサービス**: プライベートリポジトリは適切な認証が必要
- **大容量ファイル**: 非常に大きなファイルは処理に時間がかかる
- **特殊な構造**: 標準的でない構造は手動調整が必要な場合がある
- **バイナリファイル**: 実行可能ファイルはセキュリティ上注意が必要

## ライセンス

このスキルでインポートする外部定義のライセンスは各ソースに従います。インポート時にライセンス情報を確認してください。

## 貢献

このスキルへの改善提案やバグ報告は、プロジェクトのIssueトラッカーにお願いします。

## 関連ドキュメント

- `SKILL.md`: 詳細なワークフロー説明
- `references/naming-conversion.md`: 命名規則の詳細
- `references/supported-sources.md`: サポートされる取得元の一覧
- `/CLAUDE.md`: プロジェクト全体の構造とルール

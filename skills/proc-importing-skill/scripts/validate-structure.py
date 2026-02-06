#!/usr/bin/env python3
"""
変換後のディレクトリ構造を検証する

Usage:
    validate-structure.py --path <resource_path> --type <skill|agent>
"""

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Dict


class StructureValidator:
    """構造検証クラス"""

    def __init__(self, path: str, resource_type: str):
        self.path = Path(path)
        self.resource_type = resource_type
        self.errors = []
        self.warnings = []
        self.info_messages = []

    def validate(self) -> Dict:
        """検証を実行"""
        print(f"[INFO] Validating structure: {self.path}")
        print(f"[INFO] Resource type: {self.resource_type}")

        # ディレクトリの存在確認
        if not self.path.exists():
            self.errors.append(f"Path does not exist: {self.path}")
            return self._build_result()

        if not self.path.is_dir():
            self.errors.append(f"Path is not a directory: {self.path}")
            return self._build_result()

        # 命名規則の検証
        self._validate_naming()

        # ディレクトリ構造の検証
        if self.resource_type == 'skill':
            self._validate_skill_structure()
        elif self.resource_type == 'agent':
            self._validate_agent_structure()
        else:
            self.errors.append(f"Unknown resource type: {self.resource_type}")

        # 結果を表示
        self._print_results()

        return self._build_result()

    def _validate_naming(self):
        """命名規則を検証"""
        name = self.path.name

        if self.resource_type == 'skill':
            # proc-*, action-*, cond-* のいずれかで始まる
            if not re.match(r'^(proc|action|cond)-.+-skill$', name):
                self.errors.append(
                    f"Invalid skill name format: {name}\n"
                    f"  Expected: [proc|action|cond]-[action]-skill"
                )
            else:
                self.info_messages.append(f"✓ Skill naming convention: {name}")

        elif self.resource_type == 'agent':
            # shihan-*, deshi-* のいずれかで始まる
            if not re.match(r'^(shihan|deshi)-.+$', name):
                self.errors.append(
                    f"Invalid agent name format: {name}\n"
                    f"  Expected: [shihan|deshi]-[specialty]"
                )
            else:
                self.info_messages.append(f"✓ Agent naming convention: {name}")

    def _validate_skill_structure(self):
        """スキル構造を検証"""
        # 必須ファイル: SKILL.md
        skill_md = self.path / 'SKILL.md'
        if not skill_md.exists():
            self.errors.append("Required file missing: SKILL.md")
        else:
            self.info_messages.append("✓ SKILL.md exists")
            self._validate_skill_md(skill_md)

        # オプションディレクトリ
        optional_dirs = ['scripts', 'references', 'assets']
        for dir_name in optional_dirs:
            dir_path = self.path / dir_name
            if dir_path.exists():
                if not dir_path.is_dir():
                    self.warnings.append(f"{dir_name} exists but is not a directory")
                else:
                    self.info_messages.append(f"✓ Optional directory: {dir_name}/")

        # ファイル命名規則
        self._check_file_naming()

    def _validate_agent_structure(self):
        """エージェント構造を検証"""
        # 必須ファイル: AGENT.md
        agent_md = self.path / 'AGENT.md'
        if not agent_md.exists():
            self.errors.append("Required file missing: AGENT.md")
        else:
            self.info_messages.append("✓ AGENT.md exists")
            self._validate_agent_md(agent_md)

        # オプションディレクトリ
        optional_dirs = ['rules', 'knowledge', 'verification', 'collection', 'generation']
        for dir_name in optional_dirs:
            dir_path = self.path / dir_name
            if dir_path.exists():
                if not dir_path.is_dir():
                    self.warnings.append(f"{dir_name} exists but is not a directory")
                else:
                    self.info_messages.append(f"✓ Optional directory: {dir_name}/")

        # ファイル命名規則
        self._check_file_naming()

    def _validate_skill_md(self, skill_md: Path):
        """SKILL.mdの内容を検証"""
        content = skill_md.read_text(encoding='utf-8', errors='ignore')

        # ヘッダーの検証
        if not content.startswith('#'):
            self.errors.append("SKILL.md must start with a title (# Title)")

        # 必須フィールドの検証
        required_fields = ['Purpose', 'Scope']
        for field in required_fields:
            pattern = rf'[-*]\s*{field}:\s*.+'
            if not re.search(pattern, content, re.MULTILINE | re.IGNORECASE):
                self.errors.append(f"SKILL.md missing required field: {field}")
            else:
                self.info_messages.append(f"✓ Field present: {field}")

        # ワークフローセクションの確認
        workflow_keywords = ['workflow', 'ワークフロー', 'plan', 'execute', 'verify']
        has_workflow = any(keyword in content.lower() for keyword in workflow_keywords)
        if not has_workflow:
            self.warnings.append("SKILL.md does not contain workflow section")
        else:
            self.info_messages.append("✓ Workflow section detected")

        # Markdown構文の検証
        self._validate_markdown(content, skill_md)

    def _validate_agent_md(self, agent_md: Path):
        """AGENT.mdの内容を検証"""
        content = agent_md.read_text(encoding='utf-8', errors='ignore')

        # ヘッダーの検証
        if not content.startswith('#'):
            self.errors.append("AGENT.md must start with a title (# Title)")

        # 必須フィールドの検証
        required_fields = ['Purpose', 'Scope']
        for field in required_fields:
            pattern = rf'[-*]\s*{field}:\s*.+'
            if not re.search(pattern, content, re.MULTILINE | re.IGNORECASE):
                self.errors.append(f"AGENT.md missing required field: {field}")
            else:
                self.info_messages.append(f"✓ Field present: {field}")

        # Markdown構文の検証
        self._validate_markdown(content, agent_md)

    def _validate_markdown(self, content: str, file_path: Path):
        """Markdown構文を検証"""
        lines = content.split('\n')

        # コードブロックの対応をチェック
        code_block_count = content.count('```')
        if code_block_count % 2 != 0:
            self.warnings.append(f"{file_path.name}: Unclosed code block detected")

        # リストのインデント
        for i, line in enumerate(lines, start=1):
            # 不適切なリストマーカー
            if re.match(r'^\s*[-*]\s*[-*]', line):
                self.warnings.append(
                    f"{file_path.name}:{i}: Double list marker detected"
                )

    def _check_file_naming(self):
        """ファイル命名規則をチェック"""
        # scriptsディレクトリ
        scripts_dir = self.path / 'scripts'
        if scripts_dir.exists():
            for file in scripts_dir.rglob('*'):
                if file.is_file():
                    # snake_caseを推奨
                    if not re.match(r'^[a-z0-9_]+\.[a-z0-9]+$', file.name):
                        self.warnings.append(
                            f"Script file not in snake_case: {file.relative_to(self.path)}"
                        )

        # referencesディレクトリ
        refs_dir = self.path / 'references'
        if refs_dir.exists():
            for file in refs_dir.rglob('*.md'):
                # kebab-caseを推奨
                stem = file.stem
                if not re.match(r'^[a-z0-9-]+$', stem):
                    self.warnings.append(
                        f"Reference file not in kebab-case: {file.relative_to(self.path)}"
                    )

        # knowledgeディレクトリ
        knowledge_dir = self.path / 'knowledge'
        if knowledge_dir.exists():
            for file in knowledge_dir.rglob('*.md'):
                # kebab-caseまたはsnake_caseを許容
                stem = file.stem
                if not re.match(r'^[a-z0-9_-]+$', stem):
                    self.warnings.append(
                        f"Knowledge file naming: {file.relative_to(self.path)}"
                    )

    def _print_results(self):
        """結果を表示"""
        print("\n" + "=" * 60)
        print("VALIDATION RESULTS")
        print("=" * 60)

        if self.errors:
            print(f"\n❌ ERRORS ({len(self.errors)}):")
            for error in self.errors:
                print(f"  {error}")

        if self.warnings:
            print(f"\n⚠️  WARNINGS ({len(self.warnings)}):")
            for warning in self.warnings:
                print(f"  {warning}")

        if self.info_messages:
            print(f"\n✓ INFO ({len(self.info_messages)}):")
            for msg in self.info_messages:
                print(f"  {msg}")

        print("\n" + "=" * 60)

        if not self.errors:
            print("✓ Validation PASSED")
        else:
            print("❌ Validation FAILED")

        print("=" * 60 + "\n")

    def _build_result(self) -> Dict:
        """結果を構築"""
        return {
            'path': str(self.path),
            'resource_type': self.resource_type,
            'valid': len(self.errors) == 0,
            'errors': self.errors,
            'warnings': self.warnings,
            'info': self.info_messages
        }


def main():
    parser = argparse.ArgumentParser(description='Validate resource structure')
    parser.add_argument('--path', required=True, help='Path to resource directory')
    parser.add_argument('--type', required=True, choices=['skill', 'agent'], help='Resource type')
    parser.add_argument('--output', help='Output JSON file')

    args = parser.parse_args()

    try:
        validator = StructureValidator(args.path, args.type)
        result = validator.validate()

        # 結果を保存
        if args.output:
            output_path = Path(args.output)
            output_path.parent.mkdir(parents=True, exist_ok=True)

            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2, ensure_ascii=False)

            print(f"[INFO] Result saved to: {output_path}")

        # 終了コード
        sys.exit(0 if result['valid'] else 1)

    except Exception as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(2)


if __name__ == '__main__':
    main()

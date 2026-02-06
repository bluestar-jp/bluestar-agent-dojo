#!/usr/bin/env python3
"""
ディレクトリ構造をbluestar-agent-dojo標準に変換する

Usage:
    convert-structure.py --input <input_dir> --output <output_dir> --config <renamed.json>
"""

import argparse
import json
import shutil
import sys
from pathlib import Path
from typing import Dict, List


class StructureConverter:
    """ディレクトリ構造変換クラス"""

    def __init__(self, input_dir: str, output_dir: str, config: Dict):
        self.input_dir = Path(input_dir)
        self.output_dir = Path(output_dir)
        self.config = config
        self.resource_type = config['resource_type']
        self.new_name = config['new_name']
        self.base_path = Path(config['base_path'])

    def convert(self) -> Dict:
        """変換を実行"""
        print(f"[INFO] Converting structure for: {self.new_name}")
        print(f"[INFO] Input: {self.input_dir}")
        print(f"[INFO] Output: {self.output_dir}")

        # 出力ディレクトリを作成
        target_dir = self.output_dir / self.base_path
        target_dir.mkdir(parents=True, exist_ok=True)

        # リソースタイプ別に変換
        if self.resource_type == 'skill':
            result = self._convert_skill_structure(target_dir)
        elif self.resource_type == 'agent':
            result = self._convert_agent_structure(target_dir)
        else:
            raise ValueError(f"Unknown resource type: {self.resource_type}")

        return result

    def _convert_skill_structure(self, target_dir: Path) -> Dict:
        """スキル構造に変換"""
        print("[INFO] Converting to skill structure")

        # 標準ディレクトリを作成
        scripts_dir = target_dir / 'scripts'
        references_dir = target_dir / 'references'
        assets_dir = target_dir / 'assets'

        created_files = []

        # ファイルマッピング
        file_mappings = {
            'README.md': 'SKILL.md',
            'readme.md': 'SKILL.md',
            'index.md': 'SKILL.md',
            'SKILL.md': 'SKILL.md',
        }

        # メインファイルをマッピング
        main_file_found = False
        for src_name, dst_name in file_mappings.items():
            src_file = self.input_dir / src_name
            if src_file.exists():
                dst_file = target_dir / dst_name
                self._copy_and_transform(src_file, dst_file)
                created_files.append(str(dst_file.relative_to(self.output_dir)))
                main_file_found = True
                break

        # SKILL.mdが見つからない場合は生成
        if not main_file_found:
            skill_md = self._generate_skill_md()
            skill_file = target_dir / 'SKILL.md'
            skill_file.write_text(skill_md, encoding='utf-8')
            created_files.append(str(skill_file.relative_to(self.output_dir)))
            print("[INFO] Generated SKILL.md from template")

        # スクリプトファイルを移動
        script_sources = [
            self.input_dir / 'scripts',
            self.input_dir / 'bin',
            self.input_dir / 'tools',
        ]

        for src_dir in script_sources:
            if src_dir.exists() and src_dir.is_dir():
                scripts_dir.mkdir(exist_ok=True)
                for src_file in src_dir.rglob('*'):
                    if src_file.is_file():
                        rel_path = src_file.relative_to(src_dir)
                        dst_file = scripts_dir / rel_path
                        dst_file.parent.mkdir(parents=True, exist_ok=True)
                        shutil.copy2(src_file, dst_file)
                        created_files.append(str(dst_file.relative_to(self.output_dir)))
                        print(f"[INFO] Copied script: {rel_path}")

        # ドキュメントファイルを references に移動
        doc_sources = [
            self.input_dir / 'docs',
            self.input_dir / 'documentation',
            self.input_dir / 'references',
        ]

        for src_dir in doc_sources:
            if src_dir.exists() and src_dir.is_dir():
                references_dir.mkdir(exist_ok=True)
                for src_file in src_dir.rglob('*.md'):
                    rel_path = src_file.relative_to(src_dir)
                    dst_file = references_dir / rel_path
                    dst_file.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(src_file, dst_file)
                    created_files.append(str(dst_file.relative_to(self.output_dir)))

        # アセットファイルを移動
        asset_patterns = ['*.png', '*.jpg', '*.jpeg', '*.svg', '*.gif', '*.csv', '*.json']
        asset_sources = [
            self.input_dir / 'assets',
            self.input_dir / 'images',
            self.input_dir / 'data',
        ]

        for src_dir in asset_sources:
            if src_dir.exists() and src_dir.is_dir():
                assets_dir.mkdir(exist_ok=True)
                for pattern in asset_patterns:
                    for src_file in src_dir.rglob(pattern):
                        rel_path = src_file.relative_to(src_dir)
                        dst_file = assets_dir / rel_path
                        dst_file.parent.mkdir(parents=True, exist_ok=True)
                        shutil.copy2(src_file, dst_file)
                        created_files.append(str(dst_file.relative_to(self.output_dir)))

        return {
            'target_directory': str(target_dir),
            'created_files': created_files,
            'structure': 'skill'
        }

    def _convert_agent_structure(self, target_dir: Path) -> Dict:
        """エージェント構造に変換"""
        print("[INFO] Converting to agent structure")

        # 標準ディレクトリを作成
        rules_dir = target_dir / 'rules'
        knowledge_dir = target_dir / 'knowledge'
        verification_dir = target_dir / 'verification'
        collection_dir = target_dir / 'collection'
        generation_dir = target_dir / 'generation'

        created_files = []

        # ファイルマッピング
        file_mappings = {
            'README.md': 'AGENT.md',
            'readme.md': 'AGENT.md',
            'index.md': 'AGENT.md',
            'AGENT.md': 'AGENT.md',
        }

        # メインファイルをマッピング
        main_file_found = False
        for src_name, dst_name in file_mappings.items():
            src_file = self.input_dir / src_name
            if src_file.exists():
                dst_file = target_dir / dst_name
                self._copy_and_transform(src_file, dst_file)
                created_files.append(str(dst_file.relative_to(self.output_dir)))
                main_file_found = True
                break

        # AGENT.mdが見つからない場合は生成
        if not main_file_found:
            agent_md = self._generate_agent_md()
            agent_file = target_dir / 'AGENT.md'
            agent_file.write_text(agent_md, encoding='utf-8')
            created_files.append(str(agent_file.relative_to(self.output_dir)))
            print("[INFO] Generated AGENT.md from template")

        # ルールファイルを移動
        rule_sources = [
            self.input_dir / 'rules',
            self.input_dir / 'policies',
        ]

        for src_dir in rule_sources:
            if src_dir.exists() and src_dir.is_dir():
                rules_dir.mkdir(exist_ok=True)
                for src_file in src_dir.rglob('*.md'):
                    rel_path = src_file.relative_to(src_dir)
                    dst_file = rules_dir / rel_path
                    dst_file.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(src_file, dst_file)
                    created_files.append(str(dst_file.relative_to(self.output_dir)))

        # 知識ファイルを移動
        knowledge_sources = [
            self.input_dir / 'knowledge',
            self.input_dir / 'docs',
            self.input_dir / 'documentation',
        ]

        for src_dir in knowledge_sources:
            if src_dir.exists() and src_dir.is_dir():
                knowledge_dir.mkdir(exist_ok=True)
                for src_file in src_dir.rglob('*.md'):
                    rel_path = src_file.relative_to(src_dir)
                    dst_file = knowledge_dir / rel_path
                    dst_file.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(src_file, dst_file)
                    created_files.append(str(dst_file.relative_to(self.output_dir)))

        # 検証スクリプトを移動
        verification_sources = [
            self.input_dir / 'verification',
            self.input_dir / 'tests',
            self.input_dir / 'scripts',
        ]

        for src_dir in verification_sources:
            if src_dir.exists() and src_dir.is_dir():
                verification_dir.mkdir(exist_ok=True)
                for src_file in src_dir.rglob('*'):
                    if src_file.is_file() and src_file.suffix in ['.py', '.sh', '.js', '.md']:
                        rel_path = src_file.relative_to(src_dir)
                        dst_file = verification_dir / rel_path
                        dst_file.parent.mkdir(parents=True, exist_ok=True)
                        shutil.copy2(src_file, dst_file)
                        created_files.append(str(dst_file.relative_to(self.output_dir)))

        return {
            'target_directory': str(target_dir),
            'created_files': created_files,
            'structure': 'agent'
        }

    def _copy_and_transform(self, src: Path, dst: Path):
        """ファイルをコピーして変換"""
        content = src.read_text(encoding='utf-8', errors='ignore')

        # ヘッダーを追加・修正
        content = self._ensure_header(content)

        dst.write_text(content, encoding='utf-8')
        print(f"[INFO] Transformed: {src.name} → {dst.name}")

    def _ensure_header(self, content: str) -> str:
        """ヘッダーを確保"""
        analysis = self.config.get('analysis', {})
        purpose = analysis.get('purpose', '') or analysis.get('description', 'Imported resource')
        scope = analysis.get('scope', '') or 'External definition'

        # 既存のヘッダーを探す
        if content.startswith('# '):
            lines = content.split('\n')
            title_line = lines[0]

            # Purpose/Scope があるか確認
            has_purpose = any('Purpose:' in line for line in lines[:10])
            has_scope = any('Scope:' in line for line in lines[:10])

            if has_purpose and has_scope:
                return content

            # ヘッダーを挿入
            header_lines = [title_line, '']
            if not has_purpose:
                header_lines.append(f"- Purpose: {purpose}")
            if not has_scope:
                header_lines.append(f"- Scope: {scope}")
            header_lines.append('')

            # 既存のPurpose/Scopeの次から本文開始
            body_start = 1
            for i, line in enumerate(lines[1:], start=1):
                if line and not line.startswith('-') and not line.startswith('*'):
                    body_start = i
                    break

            return '\n'.join(header_lines + lines[body_start:])

        else:
            # ヘッダーがない場合は新規作成
            title = self.new_name.replace('-', ' ').title()
            header = f"# {title}\n\n- Purpose: {purpose}\n- Scope: {scope}\n\n"
            return header + content

    def _generate_skill_md(self) -> str:
        """SKILL.mdを生成"""
        analysis = self.config.get('analysis', {})
        purpose = analysis.get('purpose', '') or analysis.get('description', 'Imported skill')
        scope = analysis.get('scope', '') or 'External skill definition'

        template = f"""# {self.new_name}

- Purpose: {purpose}
- Scope: {scope}

## 概要

このスキルは外部から取得された定義を基にしています。

## ワークフロー

### 1. Plan

（実行計画を記述）

### 2. Agree

（ユーザー確認項目を記述）

### 3. Execute

（実行手順を記述）

### 4. Verify

（検証方法を記述）

## 依存関係

"""

        # 依存関係を追加
        dependencies = analysis.get('dependencies', [])
        if dependencies:
            for dep in dependencies:
                template += f"- {dep}\n"
        else:
            template += "- なし\n"

        template += """
## 使用例

```bash
# 使用例をここに記述
```

## 注意事項

このスキルは外部定義から自動生成されました。必要に応じて内容を調整してください。
"""

        return template

    def _generate_agent_md(self) -> str:
        """AGENT.mdを生成"""
        analysis = self.config.get('analysis', {})
        purpose = analysis.get('purpose', '') or analysis.get('description', 'Imported agent')
        scope = analysis.get('scope', '') or 'External agent definition'

        template = f"""# {self.new_name}

- Purpose: {purpose}
- Scope: {scope}

## 役割

このエージェントは外部から取得された定義を基にしています。

## 専門領域

（専門領域を記述）

## ワークフロー

### タスクの受領

（タスク受領方法を記述）

### 実行

（実行手順を記述）

### 報告

（報告方法を記述）

## 使用するリソース

"""

        # 依存関係を追加
        dependencies = analysis.get('dependencies', [])
        if dependencies:
            for dep in dependencies:
                template += f"- {dep}\n"
        else:
            template += "- なし\n"

        template += """
## 他エージェントとの連携

（連携方法を記述）

## 注意事項

このエージェントは外部定義から自動生成されました。必要に応じて内容を調整してください。
"""

        return template


def main():
    parser = argparse.ArgumentParser(description='Convert directory structure')
    parser.add_argument('--input', required=True, help='Input directory')
    parser.add_argument('--output', required=True, help='Output directory')
    parser.add_argument('--config', required=True, help='Renamed config JSON file')

    args = parser.parse_args()

    try:
        # 設定を読み込み
        with open(args.config, 'r', encoding='utf-8') as f:
            config = json.load(f)

        # 構造を変換
        converter = StructureConverter(args.input, args.output, config)
        result = converter.convert()

        print(f"\n[SUCCESS] Structure conversion complete")
        print(f"[INFO] Target directory: {result['target_directory']}")
        print(f"[INFO] Created {len(result['created_files'])} files")

        # 結果を保存
        result_file = Path(args.output) / 'conversion_result.json'
        with open(result_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)

        print(f"[INFO] Result saved to: {result_file}")

    except Exception as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()

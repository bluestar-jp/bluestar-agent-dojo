#!/usr/bin/env python3
"""
取得した定義ファイルを分析し、メタデータを抽出する

Usage:
    analyze-definition.py --input-dir <path> --type <skill|agent> --output <json_file>
"""

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional


class DefinitionAnalyzer:
    """定義ファイルを分析するクラス"""

    def __init__(self, input_dir: str, resource_type: str):
        self.input_dir = Path(input_dir)
        self.resource_type = resource_type

    def analyze(self) -> Dict:
        """分析を実行"""
        print(f"[INFO] Analyzing files in: {self.input_dir}")

        # メインのマークダウンファイルを探す
        main_file = self._find_main_file()

        if main_file:
            print(f"[INFO] Main file found: {main_file.name}")
            content = main_file.read_text(encoding='utf-8', errors='ignore')
        else:
            print("[WARNING] No main file found, using empty content")
            content = ""

        # 分析結果
        result = {
            'resource_type': self.resource_type,
            'original_name': self._extract_name(main_file, content),
            'description': self._extract_description(content),
            'purpose': self._extract_purpose(content),
            'scope': self._extract_scope(content),
            'files': self._list_all_files(),
            'dependencies': self._extract_dependencies(content),
            'autonomy_level': self._detect_autonomy_level(content),
            'has_scripts': self._has_scripts(),
            'has_workflow': self._has_workflow(content),
            'characteristics': self._analyze_characteristics(content)
        }

        return result

    def _find_main_file(self) -> Optional[Path]:
        """メインファイルを探す"""
        # 優先順位順に探す
        candidates = [
            'SKILL.md',
            'AGENT.md',
            'README.md',
            'readme.md',
            'index.md',
            'main.md'
        ]

        for candidate in candidates:
            file_path = self.input_dir / candidate
            if file_path.exists():
                return file_path

        # .mdファイルをサイズでソート（最大のものを選択）
        md_files = list(self.input_dir.glob('*.md'))
        if md_files:
            return max(md_files, key=lambda f: f.stat().st_size)

        # ディレクトリ内を再帰的に探す
        for md_file in self.input_dir.rglob('*.md'):
            if 'node_modules' not in str(md_file) and '.git' not in str(md_file):
                return md_file

        return None

    def _extract_name(self, main_file: Optional[Path], content: str) -> str:
        """リソース名を抽出"""
        if main_file:
            # ファイル名から推測
            name = main_file.stem
            if name.upper() in ['README', 'INDEX', 'MAIN', 'SKILL', 'AGENT']:
                # 親ディレクトリ名を使用
                name = main_file.parent.name
        else:
            name = self.input_dir.name

        # タイトルから抽出を試みる
        title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        if title_match:
            title = title_match.group(1).strip()
            # クリーンアップ
            title = re.sub(r'\s*\[.*?\]', '', title)  # リンクを削除
            title = re.sub(r'\s*\(.*?\)', '', title)  # 括弧を削除
            if title and len(title) < 100:
                name = title

        return name

    def _extract_description(self, content: str) -> str:
        """説明を抽出"""
        # Purposeフィールドを探す
        purpose_match = re.search(r'[-*]\s*Purpose:\s*(.+)$', content, re.MULTILINE | re.IGNORECASE)
        if purpose_match:
            return purpose_match.group(1).strip()

        # descriptionフィールドを探す
        desc_match = re.search(r'description:\s*(.+)$', content, re.MULTILINE | re.IGNORECASE)
        if desc_match:
            return desc_match.group(1).strip()

        # 最初の段落を使用
        lines = content.split('\n')
        for i, line in enumerate(lines):
            line = line.strip()
            # ヘッダーをスキップ
            if line.startswith('#'):
                continue
            # メタデータをスキップ
            if line.startswith('---') or line.startswith('-') or line.startswith('*'):
                continue
            # 空行をスキップ
            if not line:
                continue
            # 最初の実質的な段落
            if len(line) > 10:
                return line[:200]  # 最大200文字

        return "No description available"

    def _extract_purpose(self, content: str) -> str:
        """Purposeを抽出"""
        purpose_match = re.search(r'[-*]\s*Purpose:\s*(.+)$', content, re.MULTILINE | re.IGNORECASE)
        if purpose_match:
            return purpose_match.group(1).strip()
        return ""

    def _extract_scope(self, content: str) -> str:
        """Scopeを抽出"""
        scope_match = re.search(r'[-*]\s*Scope:\s*(.+)$', content, re.MULTILINE | re.IGNORECASE)
        if scope_match:
            return scope_match.group(1).strip()
        return ""

    def _list_all_files(self) -> List[str]:
        """全ファイルをリスト"""
        files = []
        for item in self.input_dir.rglob('*'):
            if item.is_file() and '.git' not in str(item):
                files.append(str(item.relative_to(self.input_dir)))
        return sorted(files)

    def _extract_dependencies(self, content: str) -> List[str]:
        """依存関係を抽出"""
        dependencies = []

        # 依存関係セクションを探す
        dep_section = re.search(
            r'##\s+依存関係|##\s+Dependencies(.+?)(?=##|$)',
            content,
            re.DOTALL | re.IGNORECASE
        )

        if dep_section:
            dep_text = dep_section.group(1)
            # リスト項目を抽出
            for line in dep_text.split('\n'):
                line = line.strip()
                if line.startswith('-') or line.startswith('*'):
                    dep = re.sub(r'^[-*]\s*\*\*(.+?)\*\*.*', r'\1', line)
                    dep = re.sub(r'^[-*]\s*`(.+?)`.*', r'\1', line)
                    dep = re.sub(r'^[-*]\s*(.+?):.*', r'\1', line)
                    dep = re.sub(r'^[-*]\s*', '', dep)
                    if dep and len(dep) < 50:
                        dependencies.append(dep.strip())

        # コードブロックから推測
        code_blocks = re.findall(r'```(?:bash|sh|python)\n(.+?)```', content, re.DOTALL)
        for block in code_blocks:
            # よく使われるコマンド
            for cmd in ['gh', 'git', 'jq', 'curl', 'python', 'node', 'npm', 'pip']:
                if re.search(rf'\b{cmd}\b', block):
                    if cmd not in dependencies:
                        dependencies.append(cmd)

        return dependencies

    def _detect_autonomy_level(self, content: str) -> str:
        """自律性レベルを検出"""
        # スクリプトが多い場合はLow Autonomy
        script_files = list(self.input_dir.glob('scripts/*'))
        if len(script_files) > 3:
            return 'low'

        # 詳細な手順が記述されている場合はMedium Autonomy
        if re.search(r'(Step \d+|## \d+\.|### \d+\.)', content):
            return 'medium'

        # 抽象的な指示のみの場合はHigh Autonomy
        if len(content) < 1000 and not script_files:
            return 'high'

        # デフォルト
        return 'medium'

    def _has_scripts(self) -> bool:
        """スクリプトが含まれているか"""
        script_dirs = ['scripts', 'bin', 'tools']
        for dir_name in script_dirs:
            script_dir = self.input_dir / dir_name
            if script_dir.exists() and script_dir.is_dir():
                script_files = list(script_dir.glob('*'))
                if script_files:
                    return True
        return False

    def _has_workflow(self, content: str) -> bool:
        """ワークフローが定義されているか"""
        workflow_keywords = [
            'workflow',
            'ワークフロー',
            'step 1',
            'step 2',
            'plan',
            'execute',
            'verify'
        ]

        content_lower = content.lower()
        return any(keyword in content_lower for keyword in workflow_keywords)

    def _analyze_characteristics(self, content: str) -> Dict:
        """特徴を分析"""
        characteristics = {
            'is_procedural': False,
            'is_single_action': False,
            'is_conditional': False,
            'is_orchestrator': False,
            'is_specialist': False
        }

        content_lower = content.lower()

        # Procedural (手順型)
        if re.search(r'(step \d+|## \d+\.|workflow|procedure)', content_lower):
            characteristics['is_procedural'] = True

        # Single Action (単一アクション)
        if not characteristics['is_procedural'] and len(content) < 2000:
            characteristics['is_single_action'] = True

        # Conditional (条件判断型)
        if_count = len(re.findall(r'\bif\b', content_lower))
        condition_count = len(re.findall(r'(条件|condition|判断|判定)', content_lower))
        if if_count > 5 or condition_count > 3:
            characteristics['is_conditional'] = True

        # Orchestrator (統合型)
        orchestrator_keywords = [
            'orchestrat', 'coordinat', 'delegat', 'routing', 'parallel',
            'オーケストレーション', '統合', '振り分け', '委任'
        ]
        if any(keyword in content_lower for keyword in orchestrator_keywords):
            characteristics['is_orchestrator'] = True

        # Specialist (専門型)
        specialist_keywords = [
            'expert', 'specialist', 'analyst', 'specific', 'domain',
            '専門家', 'エキスパート', '専門', 'ドメイン'
        ]
        if any(keyword in content_lower for keyword in specialist_keywords):
            characteristics['is_specialist'] = True

        return characteristics


def main():
    parser = argparse.ArgumentParser(description='Analyze external definition files')
    parser.add_argument('--input-dir', required=True, help='Input directory with fetched files')
    parser.add_argument('--type', required=True, choices=['skill', 'agent'], help='Resource type')
    parser.add_argument('--output', required=True, help='Output JSON file')

    args = parser.parse_args()

    try:
        analyzer = DefinitionAnalyzer(args.input_dir, args.type)
        result = analyzer.analyze()

        # 結果を保存
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)

        print("\n[SUCCESS] Analysis complete")
        print(f"[INFO] Original name: {result['original_name']}")
        print(f"[INFO] Description: {result['description'][:100]}...")
        print(f"[INFO] Autonomy level: {result['autonomy_level']}")
        print(f"[INFO] Has scripts: {result['has_scripts']}")
        print(f"[INFO] Has workflow: {result['has_workflow']}")
        print(f"[INFO] Result saved to: {output_path}")

    except Exception as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()

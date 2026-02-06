#!/usr/bin/env python3
"""
命名規則を適用して新しい名前を生成する

Usage:
    apply-naming.py --input <analysis.json> --output <renamed.json>
"""

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Dict


class NamingConverter:
    """命名規則変換クラス"""

    def __init__(self, analysis: Dict):
        self.analysis = analysis
        self.resource_type = analysis['resource_type']
        self.original_name = analysis['original_name']
        self.characteristics = analysis.get('characteristics', {})

    def convert(self) -> Dict:
        """変換を実行"""
        print(f"[INFO] Converting name: {self.original_name}")
        print(f"[INFO] Resource type: {self.resource_type}")

        # ケバブケースに変換
        kebab_name = self._to_kebab_case(self.original_name)
        print(f"[INFO] Kebab case: {kebab_name}")

        # リソースタイプ別に処理
        if self.resource_type == 'skill':
            new_name, sub_type = self._convert_skill_name(kebab_name)
        elif self.resource_type == 'agent':
            new_name, sub_type = self._convert_agent_name(kebab_name)
        else:
            raise ValueError(f"Unknown resource type: {self.resource_type}")

        result = {
            'original_name': self.original_name,
            'kebab_name': kebab_name,
            'new_name': new_name,
            'resource_type': self.resource_type,
            'sub_type': sub_type,
            'base_path': self._get_base_path(new_name)
        }

        print(f"[INFO] New name: {new_name}")
        print(f"[INFO] Sub type: {sub_type}")

        return result

    def _to_kebab_case(self, name: str) -> str:
        """任意のケースからケバブケースに変換"""
        # 既存のプレフィックス・サフィックスを除去
        name = re.sub(r'^(proc|action|cond|shihan|deshi)-', '', name, flags=re.IGNORECASE)
        name = re.sub(r'-skill$', '', name, flags=re.IGNORECASE)
        name = re.sub(r'-agent$', '', name, flags=re.IGNORECASE)

        # PascalCase/CamelCase → kebab-case
        name = re.sub('([a-z0-9])([A-Z])', r'\1-\2', name)
        name = re.sub('([A-Z]+)([A-Z][a-z])', r'\1-\2', name)

        # snake_case → kebab-case
        name = name.replace('_', '-')

        # スペースやその他の記号をハイフンに
        name = re.sub(r'[^\w-]', '-', name)

        # 連続するハイフンを1つに
        name = re.sub(r'-+', '-', name)

        # 前後のハイフンを削除
        name = name.strip('-')

        # 小文字化
        return name.lower()

    def _convert_skill_name(self, kebab_name: str) -> tuple:
        """スキル名を変換"""
        # 特徴から type を判定
        sub_type = self._determine_skill_type()

        # 動名詞形に変換
        action_name = self._to_gerund_form(kebab_name)

        # 命名規則を適用
        new_name = f"{sub_type}-{action_name}-skill"

        return new_name, sub_type

    def _convert_agent_name(self, kebab_name: str) -> tuple:
        """エージェント名を変換"""
        # 特徴から role を判定
        sub_type = self._determine_agent_role()

        # specialty は名詞形
        specialty = self._extract_specialty(kebab_name)

        # 命名規則を適用
        new_name = f"{sub_type}-{specialty}"

        return new_name, sub_type

    def _determine_skill_type(self) -> str:
        """スキルのタイプを判定"""
        chars = self.characteristics

        # Conditional Instructions (条件判断型)
        if chars.get('is_conditional', False):
            return 'cond'

        # Procedure (手順型)
        if chars.get('is_procedural', False) or self.analysis.get('has_workflow', False):
            return 'proc'

        # Single Action (単一アクション型)
        if chars.get('is_single_action', False):
            return 'action'

        # デフォルトは procedure
        return 'proc'

    def _determine_agent_role(self) -> str:
        """エージェントのロールを判定"""
        chars = self.characteristics

        # Shihan (師範 - 統合型)
        if chars.get('is_orchestrator', False):
            return 'shihan'

        # Deshi (弟子 - 専門型)
        if chars.get('is_specialist', False):
            return 'deshi'

        # デフォルトは deshi
        return 'deshi'

    def _to_gerund_form(self, name: str) -> str:
        """動名詞形（-ing形）に変換"""
        # 既に -ing で終わっている場合
        if name.endswith('ing'):
            return name

        # よくある動詞のパターンを検出して変換
        verb_patterns = {
            r'\b(format|lint|valid|deploy|test|review|analyz|creat|generat|execut|run|build|compil)': r'\1ing',
            r'\b(format)$': 'formatting',
            r'\b(lint)$': 'linting',
            r'\b(valid)': 'validating',
            r'\b(validate)$': 'validating',
            r'\b(deploy)$': 'deploying',
            r'\b(test)$': 'testing',
            r'\b(review)$': 'reviewing',
            r'\b(analyze)$': 'analyzing',
            r'\b(analyz)': 'analyzing',
            r'\b(create)$': 'creating',
            r'\b(creat)': 'creating',
            r'\b(generate)$': 'generating',
            r'\b(generat)': 'generating',
            r'\b(execute)$': 'executing',
            r'\b(execut)': 'executing',
            r'\b(run)$': 'running',
            r'\b(build)$': 'building',
            r'\b(compile)$': 'compiling',
            r'\b(compil)': 'compiling',
            r'\b(import)$': 'importing',
            r'\b(export)$': 'exporting',
            r'\b(fetch)$': 'fetching',
            r'\b(parse)$': 'parsing',
            r'\b(transform)$': 'transforming',
            r'\b(convert)$': 'converting',
            r'\b(handle)$': 'handling',
            r'\b(process)$': 'processing',
            r'\b(manage)$': 'managing',
            r'\b(orchestrat)': 'orchestrating',
            r'\b(coordinat)': 'coordinating',
        }

        for pattern, replacement in verb_patterns.items():
            if re.search(pattern, name, re.IGNORECASE):
                return re.sub(pattern, replacement, name, flags=re.IGNORECASE)

        # 名詞の場合はそのまま（例: code-formatter → formatting-code）
        parts = name.split('-')
        if len(parts) >= 2:
            # 最初の単語が動詞っぽい場合は -ing を追加
            first = parts[0]
            if first in ['code', 'data', 'file', 'text', 'json', 'yaml']:
                # 名詞なのでそのまま
                return name
            # 動詞の可能性が高い場合
            if not first.endswith('ing'):
                return f"{first}ing-{'-'.join(parts[1:])}"

        return name

    def _extract_specialty(self, name: str) -> str:
        """エージェントの specialty を抽出"""
        # よくあるサフィックスを除去
        name = re.sub(r'-(expert|specialist|analyst|manager|handler)$', r'-\1', name)

        # 既に適切な形式の場合はそのまま
        if re.match(r'^[a-z]+(-[a-z]+)*$', name):
            return name

        return name

    def _get_base_path(self, new_name: str) -> str:
        """ベースパスを取得"""
        if self.resource_type == 'skill':
            return f"skills/{new_name}"
        elif self.resource_type == 'agent':
            return f"agents/{new_name}"
        else:
            raise ValueError(f"Unknown resource type: {self.resource_type}")


def main():
    parser = argparse.ArgumentParser(description='Apply naming conventions')
    parser.add_argument('--input', required=True, help='Input analysis JSON file')
    parser.add_argument('--output', required=True, help='Output renamed JSON file')

    args = parser.parse_args()

    try:
        # 分析結果を読み込み
        with open(args.input, 'r', encoding='utf-8') as f:
            analysis = json.load(f)

        # 命名規則を適用
        converter = NamingConverter(analysis)
        result = converter.convert()

        # 元の分析結果とマージ
        result.update({
            'analysis': analysis
        })

        # 結果を保存
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)

        print(f"\n[SUCCESS] Naming conversion complete")
        print(f"[INFO] {result['original_name']} → {result['new_name']}")
        print(f"[INFO] Base path: {result['base_path']}")
        print(f"[INFO] Result saved to: {output_path}")

    except Exception as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()

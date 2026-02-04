#!/usr/bin/env python3
"""
既存リソースとの類似性をチェックする

Usage:
    check_similarity.py --new <new_skill_path> --existing <existing_dir> --threshold <0.0-1.0>
"""

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple


class SimilarityChecker:
    """類似性チェッククラス"""

    def __init__(self, new_path: str, existing_dir: str, threshold: float = 0.7):
        self.new_path = Path(new_path)
        self.existing_dir = Path(existing_dir)
        self.threshold = threshold

    def check(self) -> Dict:
        """類似性チェックを実行"""
        print(f"[INFO] Checking similarity with existing resources")
        print(f"[INFO] New resource: {self.new_path}")
        print(f"[INFO] Existing directory: {self.existing_dir}")
        print(f"[INFO] Threshold: {self.threshold}")

        # 新規リソースの情報を抽出
        new_info = self._extract_resource_info(self.new_path)

        # 既存リソースの情報を抽出
        existing_resources = []
        for item in self.existing_dir.iterdir():
            if item.is_dir() and not item.name.startswith('.'):
                info = self._extract_resource_info(item)
                if info:
                    existing_resources.append(info)

        # 類似性を計算
        similarities = []
        for existing in existing_resources:
            similarity = self._calculate_similarity(new_info, existing)
            if similarity > 0.1:  # 最低限の関連性がある場合のみ記録
                similarities.append({
                    'path': existing['path'],
                    'name': existing['name'],
                    'similarity': similarity,
                    'details': self._get_similarity_details(new_info, existing)
                })

        # 類似度でソート
        similarities.sort(key=lambda x: x['similarity'], reverse=True)

        # 競合を判定
        conflicts = [s for s in similarities if s['similarity'] >= self.threshold]

        result = {
            'new_resource': {
                'path': str(self.new_path),
                'name': new_info['name']
            },
            'similarities': similarities[:10],  # 上位10件
            'conflicts': conflicts,
            'has_conflict': len(conflicts) > 0,
            'threshold': self.threshold
        }

        # 結果を表示
        if conflicts:
            print(f"\n[WARNING] Found {len(conflicts)} potential conflicts:")
            for conflict in conflicts:
                print(f"  - {conflict['name']} (similarity: {conflict['similarity']:.2%})")
        else:
            print(f"\n[INFO] No conflicts detected")

        if similarities:
            print(f"\n[INFO] Top similar resources:")
            for sim in similarities[:5]:
                print(f"  - {sim['name']} (similarity: {sim['similarity']:.2%})")

        return result

    def _extract_resource_info(self, path: Path) -> Dict:
        """リソースの情報を抽出"""
        # メインファイルを探す
        main_files = ['SKILL.md', 'AGENT.md', 'README.md']
        main_content = ""

        for filename in main_files:
            file_path = path / filename
            if file_path.exists():
                main_content = file_path.read_text(encoding='utf-8', errors='ignore')
                break

        if not main_content:
            return None

        # 情報を抽出
        info = {
            'path': str(path),
            'name': path.name,
            'title': self._extract_title(main_content),
            'purpose': self._extract_field(main_content, 'Purpose'),
            'description': self._extract_field(main_content, 'Description'),
            'keywords': self._extract_keywords(main_content),
            'content_length': len(main_content)
        }

        return info

    def _extract_title(self, content: str) -> str:
        """タイトルを抽出"""
        match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        if match:
            return match.group(1).strip()
        return ""

    def _extract_field(self, content: str, field_name: str) -> str:
        """フィールドを抽出"""
        pattern = rf'[-*]\s*{field_name}:\s*(.+)$'
        match = re.search(pattern, content, re.MULTILINE | re.IGNORECASE)
        if match:
            return match.group(1).strip()
        return ""

    def _extract_keywords(self, content: str) -> List[str]:
        """キーワードを抽出"""
        # 小文字化して単語を抽出
        content_lower = content.lower()

        # 特殊文字を削除
        content_clean = re.sub(r'[^\w\s-]', ' ', content_lower)

        # 単語に分割
        words = content_clean.split()

        # ストップワード（一般的すぎる単語）を除外
        stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'be',
            'been', 'this', 'that', 'these', 'those', 'it', 'its', 'use', 'using',
            'used', 'can', 'will', 'would', 'should', 'may', 'might', 'must'
        }

        # 頻出単語を抽出（長さ3文字以上、ストップワードでない）
        word_freq = {}
        for word in words:
            if len(word) >= 3 and word not in stop_words:
                word_freq[word] = word_freq.get(word, 0) + 1

        # 頻度順にソート
        keywords = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)

        # 上位20個のキーワードを返す
        return [word for word, freq in keywords[:20]]

    def _calculate_similarity(self, info1: Dict, info2: Dict) -> float:
        """類似度を計算（0.0-1.0）"""
        if not info1 or not info2:
            return 0.0

        # 名前の類似度（重み: 0.3）
        name_similarity = self._string_similarity(info1['name'], info2['name'])

        # タイトルの類似度（重み: 0.2）
        title_similarity = self._string_similarity(info1['title'], info2['title'])

        # Purposeの類似度（重み: 0.3）
        purpose_similarity = self._string_similarity(info1['purpose'], info2['purpose'])

        # キーワードの類似度（重み: 0.2）
        keyword_similarity = self._keyword_similarity(info1['keywords'], info2['keywords'])

        # 加重平均
        total_similarity = (
            name_similarity * 0.3 +
            title_similarity * 0.2 +
            purpose_similarity * 0.3 +
            keyword_similarity * 0.2
        )

        return total_similarity

    def _string_similarity(self, s1: str, s2: str) -> float:
        """文字列の類似度（Jaccard係数）"""
        if not s1 or not s2:
            return 0.0

        # 単語に分割
        words1 = set(re.findall(r'\w+', s1.lower()))
        words2 = set(re.findall(r'\w+', s2.lower()))

        if not words1 or not words2:
            return 0.0

        # Jaccard係数
        intersection = len(words1 & words2)
        union = len(words1 | words2)

        return intersection / union if union > 0 else 0.0

    def _keyword_similarity(self, keywords1: List[str], keywords2: List[str]) -> float:
        """キーワードの類似度"""
        if not keywords1 or not keywords2:
            return 0.0

        set1 = set(keywords1)
        set2 = set(keywords2)

        intersection = len(set1 & set2)
        union = len(set1 | set2)

        return intersection / union if union > 0 else 0.0

    def _get_similarity_details(self, info1: Dict, info2: Dict) -> Dict:
        """類似度の詳細を取得"""
        return {
            'name_similarity': self._string_similarity(info1['name'], info2['name']),
            'title_similarity': self._string_similarity(info1['title'], info2['title']),
            'purpose_similarity': self._string_similarity(info1['purpose'], info2['purpose']),
            'keyword_overlap': len(set(info1['keywords']) & set(info2['keywords']))
        }


def main():
    parser = argparse.ArgumentParser(description='Check similarity with existing resources')
    parser.add_argument('--new', required=True, help='Path to new resource')
    parser.add_argument('--existing', required=True, help='Directory with existing resources')
    parser.add_argument('--threshold', type=float, default=0.7, help='Similarity threshold (0.0-1.0)')
    parser.add_argument('--output', help='Output JSON file')

    args = parser.parse_args()

    try:
        checker = SimilarityChecker(args.new, args.existing, args.threshold)
        result = checker.check()

        # 結果を保存
        if args.output:
            output_path = Path(args.output)
            output_path.parent.mkdir(parents=True, exist_ok=True)

            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2, ensure_ascii=False)

            print(f"\n[INFO] Result saved to: {output_path}")

        # 終了コード
        sys.exit(1 if result['has_conflict'] else 0)

    except Exception as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(2)


if __name__ == '__main__':
    main()

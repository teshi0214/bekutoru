# import_terms.py

import json
from term_db import TermDatabase
from models import Term

def import_from_json(json_file_path: str):
    """JSONファイルから造語を一括インポート"""
    
    # JSONファイル読み込み
    try:
        with open(json_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"❌ ファイルが見つかりません: {json_file_path}")
        return
    except json.JSONDecodeError as e:
        print(f"❌ JSON形式エラー: {str(e)}")
        return
    
    db = TermDatabase()
    
    print(f"📚 {len(data)}件の造語をインポート開始...")
    
    success_count = 0
    error_count = 0
    
    # インポート実行
    for i, item in enumerate(data, 1):
        try:
            term = Term(
                term=item['term'],
                category=item['category'],
                reading=item['reading'],
                description=item['description']
            )
            db.add_term(term)
            success_count += 1
            print(f"[{i}/{len(data)}] {item['term']}")
        except Exception as e:
            print(f"❌ エラー: {item.get('term', 'unknown')} - {str(e)}")
            error_count += 1
    
    print(f"\n✅ インポート完了!")
    print(f"   成功: {success_count}件")
    print(f"   失敗: {error_count}件")

# 実行
if __name__ == "__main__":
    import_from_json("terms.json")
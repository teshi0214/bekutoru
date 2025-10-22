# term_db.py

from google.cloud import firestore
from models import Term
from embedding_utils import create_embedding
from typing import List, Optional
from datetime import datetime

db = firestore.Client()
COLLECTION_NAME = 'terms'

class TermDatabase:
    """造語データベース操作クラス"""
    
    def __init__(self):
        self.collection = db.collection(COLLECTION_NAME)
    
    def add_term(self, term: Term) -> str:
        """造語を追加"""
        # エンベディング生成
        text_for_embedding = f"{term.term} {term.reading} {term.description}"
        term.embedding = create_embedding(text_for_embedding)
        
        # Firestoreに保存
        doc_ref = self.collection.document()
        doc_ref.set(term.to_dict())
        
        print(f"✅ 追加完了: {term.term} (ID: {doc_ref.id})")
        return doc_ref.id
    
    def get_term(self, term_id: str) -> Optional[Term]:
        """IDで造語を取得"""
        doc = self.collection.document(term_id).get()
        if doc.exists:
            return Term.from_dict(doc.to_dict(), term_id)
        return None
    
    def get_term_by_name(self, term_name: str) -> Optional[Term]:
        """名前で造語を取得"""
        docs = self.collection.where('term', '==', term_name).limit(1).stream()
        for doc in docs:
            return Term.from_dict(doc.to_dict(), doc.id)
        return None
    
    def update_term(self, term_id: str, updates: dict):
        """造語を更新"""
        # エンベディングも再計算する場合
        if any(key in updates for key in ['term', 'reading', 'description']):
            doc = self.collection.document(term_id).get()
            if doc.exists:
                data = doc.to_dict()
                data.update(updates)
                text_for_embedding = f"{data['term']} {data['reading']} {data['description']}"
                updates['embedding'] = create_embedding(text_for_embedding)
        
        updates['updated_at'] = datetime.utcnow()
        self.collection.document(term_id).update(updates)
        print(f"✅ 更新完了: {term_id}")
    
    def delete_term(self, term_id: str):
        """造語を削除"""
        self.collection.document(term_id).delete()
        print(f"✅ 削除完了: {term_id}")
    
    def get_all_terms(self) -> List[Term]:
        """全ての造語を取得"""
        docs = self.collection.stream()
        return [Term.from_dict(doc.to_dict(), doc.id) for doc in docs]
    
    def get_terms_by_category(self, category: str) -> List[Term]:
        """カテゴリで絞り込み"""
        docs = self.collection.where('category', '==', category).stream()
        return [Term.from_dict(doc.to_dict(), doc.id) for doc in docs]
    
    def search_terms(self, query: str, top_k: int = 5) -> List[dict]:
        """類似検索（シンプル版）"""
        query_embedding = create_embedding(query)
        
        # 全件取得して類似度計算
        all_terms = self.get_all_terms()
        results = []
        
        from embedding_utils import cosine_similarity
        
        for term in all_terms:
            if term.embedding:
                similarity = cosine_similarity(query_embedding, term.embedding)
                results.append({
                    'term_id': term.term_id,
                    'term': term.term,
                    'category': term.category,
                    'reading': term.reading,
                    'description': term.description,
                    'similarity': similarity
                })
        
        # スコア順にソート
        results.sort(key=lambda x: x['similarity'], reverse=True)
        return results[:top_k]
# models.py

from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List

@dataclass
class Term:
    """造語データクラス"""
    term: str
    category: str
    reading: str
    description: str
    embedding: Optional[List[float]] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    term_id: Optional[str] = None
    
    def to_dict(self):
        """Firestore保存用の辞書に変換"""
        return {
            'term': self.term,
            'category': self.category,
            'reading': self.reading,
            'description': self.description,
            'embedding': self.embedding,
            'created_at': self.created_at or datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }
    
    @classmethod
    def from_dict(cls, data: dict, term_id: str = None):
        """Firestoreから取得した辞書をオブジェクトに変換"""
        return cls(
            term=data.get('term'),
            category=data.get('category'),
            reading=data.get('reading'),
            description=data.get('description'),
            embedding=data.get('embedding'),
            created_at=data.get('created_at'),
            updated_at=data.get('updated_at'),
            term_id=term_id
        )
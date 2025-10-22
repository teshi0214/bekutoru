# embedding_utils.py

from sentence_transformers import SentenceTransformer
import numpy as np

# エンベディングモデル初期化（初回は自動ダウンロード）
print("エンベディングモデルをロード中...")
model = SentenceTransformer('all-MiniLM-L6-v2')
print("✅ モデルロード完了")

def create_embedding(text: str) -> list:
    """テキストをベクトル化"""
    embedding = model.encode(text)
    return embedding.tolist()

def cosine_similarity(vec1: list, vec2: list) -> float:
    """コサイン類似度計算"""
    vec1 = np.array(vec1)
    vec2 = np.array(vec2)
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))
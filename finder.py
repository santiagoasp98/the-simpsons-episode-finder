# ------------------------------------------------- #
# Imports
# ------------------------------------------------- #

import pickle
from pathlib import Path
from sentence_transformers import SentenceTransformer
from typing import List, Dict, Any

# ------------------------------------------------- #
# Recreate EpisodeFinder class to load the model
# ------------------------------------------------- #

class EpisodeFinder:
    def __init__(self, model_path: str, data_path: str):
        # Load the model
        self.model = SentenceTransformer(model_path)
        
        # Load other attributes
        with open(data_path, "rb") as f:
            data = pickle.load(f)
            self.episodes = data['episodes']
            self.episode_embeddings = data['episode_embeddings']
            self.chunk_size = data['chunk_size']
    
    def find_episode(self, description: str, top_k: int = 3) -> List[Dict[str, Any]]:
        # Get embedding for the query
        query_embedding = self.model.encode([description])[0]
        
        # Calculate similarities using dot product
        similarities = self.episode_embeddings.dot(query_embedding)
        
        # Get top matches
        top_indices = similarities.argsort()[-top_k:][::-1]
        
        results = []
        for idx in top_indices:
            episode = self.episodes.iloc[idx]
            results.append({
                'title': episode['title'],
                'season': int(episode['season']),
                'episode': int(episode['number_in_season']),
                'similarity_score': float(similarities[idx]),
                'description': episode['normalized_text'][:200] + '...'  # Preview
            })
        
        return results
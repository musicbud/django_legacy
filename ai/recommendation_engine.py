"""
LightFM-based Recommendation Engine for Movies and Manga
This module provides collaborative filtering recommendations using LightFM
"""
import numpy as np
import logging
from typing import Dict, List, Tuple, Optional
from pathlib import Path
import joblib

try:
    import pandas as pd
    from lightfm import LightFM
    from lightfm.evaluation import precision_at_k, auc_score
    from scipy.sparse import coo_matrix, csr_matrix
    LIGHTFM_AVAILABLE = True
except ImportError as e:
    LIGHTFM_AVAILABLE = False
    # Define placeholder types when not available
    csr_matrix = object
    coo_matrix = object
    logger = logging.getLogger(__name__)
    logger.warning(f"LightFM or dependencies not available: {e}. Using simple recommendations.")

logger = logging.getLogger(__name__)


class RecommendationEngine:
    """
    LightFM-based recommendation engine supporting movies and manga
    """
    
    def __init__(self, model_dir: str = '/tmp/musicbud_models'):
        """
        Initialize the recommendation engine
        
        Args:
            model_dir: Directory to save/load trained models
        """
        self.model_dir = Path(model_dir)
        self.model_dir.mkdir(parents=True, exist_ok=True)
        
        # Models for different content types
        self.models = {}
        self.interaction_matrices = {}
        self.user_id_mappings = {}
        self.item_id_mappings = {}
        
        logger.info(f"RecommendationEngine initialized with model_dir: {model_dir}")
    
    def create_interaction_matrix(
        self,
        interactions: List[Tuple[str, str, float]],
        content_type: str
    ) -> Tuple[csr_matrix, Dict, Dict]:
        """
        Create a sparse interaction matrix from user-item interactions
        
        Args:
            interactions: List of (user_id, item_id, rating) tuples
            content_type: Type of content ('movie' or 'manga')
        
        Returns:
            Tuple of (interaction_matrix, user_id_map, item_id_map)
        """
        logger.info(f"Creating interaction matrix for {content_type} with {len(interactions)} interactions")
        
        if not interactions:
            logger.warning(f"No interactions provided for {content_type}")
            # Return empty matrix with minimal structure
            empty_matrix = csr_matrix((1, 1))
            return empty_matrix, {}, {}
        
        # Convert to DataFrame for easier processing
        df = pd.DataFrame(interactions, columns=['user_id', 'item_id', 'rating'])
        
        # Create mappings
        unique_users = df['user_id'].unique()
        unique_items = df['item_id'].unique()
        
        user_id_map = {uid: idx for idx, uid in enumerate(unique_users)}
        item_id_map = {iid: idx for idx, iid in enumerate(unique_items)}
        
        # Map IDs to indices
        user_indices = df['user_id'].map(user_id_map).values
        item_indices = df['item_id'].map(item_id_map).values
        ratings = df['rating'].values
        
        # Create sparse matrix
        matrix = coo_matrix(
            (ratings, (user_indices, item_indices)),
            shape=(len(unique_users), len(unique_items))
        )
        
        logger.info(f"Created matrix shape: {matrix.shape} with {matrix.nnz} non-zero entries")
        
        return matrix.tocsr(), user_id_map, item_id_map
    
    def train_model(
        self,
        interactions: List[Tuple[str, str, float]],
        content_type: str,
        n_components: int = 30,
        loss: str = 'warp',
        epochs: int = 30,
        n_jobs: int = 4
    ) -> None:
        """
        Train a LightFM model for the given content type
        
        Args:
            interactions: List of (user_id, item_id, rating) tuples
            content_type: Type of content ('movie' or 'manga')
            n_components: Number of latent dimensions
            loss: Loss function to use
            epochs: Number of training epochs
            n_jobs: Number of parallel jobs
        """
        logger.info(f"Training {content_type} model with {len(interactions)} interactions")
        
        if not LIGHTFM_AVAILABLE:
            logger.warning(f"LightFM not available. Storing interactions for popularity-based recommendations.")
            # Store interactions for simple popularity-based recommendations
            self.interaction_matrices[content_type] = interactions
            return
        
        # Create interaction matrix
        matrix, user_map, item_map = self.create_interaction_matrix(interactions, content_type)
        
        if matrix.nnz == 0:
            logger.warning(f"No interactions for {content_type}, skipping model training")
            return
        
        # Store mappings
        self.user_id_mappings[content_type] = user_map
        self.item_id_mappings[content_type] = item_map
        self.interaction_matrices[content_type] = matrix
        
        # Create and train model
        model = LightFM(no_components=n_components, loss=loss)
        
        logger.info(f"Training LightFM model for {content_type}...")
        model.fit(matrix, epochs=epochs, num_threads=n_jobs, verbose=True)
        
        # Store model
        self.models[content_type] = model
        
        logger.info(f"Model training completed for {content_type}")
        
        # Save model
        self.save_model(content_type)
    
    def get_recommendations(
        self,
        user_id: str,
        content_type: str,
        n_recommendations: int = 10,
        filter_known_items: bool = True
    ) -> List[Tuple[str, float]]:
        """
        Get recommendations for a user
        
        Args:
            user_id: User ID to get recommendations for
            content_type: Type of content ('movie' or 'manga')
            n_recommendations: Number of recommendations to return
            filter_known_items: Whether to filter out items the user has already interacted with
        
        Returns:
            List of (item_id, score) tuples
        """
        logger.info(f"Getting {n_recommendations} {content_type} recommendations for user {user_id}")
        
        if not LIGHTFM_AVAILABLE:
            logger.info(f"Using popularity-based recommendations for {content_type}")
            return self.get_popular_items(content_type, n_recommendations)
        
        # Check if model exists
        if content_type not in self.models:
            logger.warning(f"No model found for {content_type}, attempting to load")
            self.load_model(content_type)
            
            if content_type not in self.models:
                logger.error(f"No trained model available for {content_type}")
                return self.get_popular_items(content_type, n_recommendations)
        
        model = self.models[content_type]
        user_map = self.user_id_mappings.get(content_type, {})
        item_map = self.item_id_mappings.get(content_type, {})
        
        # Check if user exists in mapping
        if user_id not in user_map:
            logger.warning(f"User {user_id} not found in {content_type} training data")
            # Return popular items for cold start
            return self.get_popular_items(content_type, n_recommendations)
        
        user_idx = user_map[user_id]
        n_items = len(item_map)
        
        # Get scores for all items
        item_indices = np.arange(n_items)
        scores = model.predict(user_idx, item_indices)
        
        # Filter out known items if requested
        if filter_known_items and content_type in self.interaction_matrices:
            known_items = self.interaction_matrices[content_type][user_idx].indices
            scores[known_items] = -np.inf
        
        # Get top N items
        top_indices = np.argsort(-scores)[:n_recommendations]
        
        # Convert back to item IDs
        item_id_reverse_map = {idx: iid for iid, idx in item_map.items()}
        recommendations = [
            (item_id_reverse_map[idx], float(scores[idx]))
            for idx in top_indices
            if scores[idx] > -np.inf
        ]
        
        logger.info(f"Generated {len(recommendations)} recommendations for user {user_id}")
        
        return recommendations
    
    def get_popular_items(self, content_type: str, n_items: int = 10) -> List[Tuple[str, float]]:
        """
        Get popular items for cold start scenarios
        
        Args:
            content_type: Type of content
            n_items: Number of items to return
        
        Returns:
            List of (item_id, score) tuples
        """
        if content_type not in self.interaction_matrices:
            return []
        
        matrix = self.interaction_matrices[content_type]
        
        # Handle different data structures
        if LIGHTFM_AVAILABLE and isinstance(matrix, csr_matrix):
            item_map = self.item_id_mappings.get(content_type, {})
            
            # Count interactions per item
            item_popularity = np.array(matrix.sum(axis=0)).flatten()
            
            # Get top N items
            top_indices = np.argsort(-item_popularity)[:n_items]
            
            # Convert back to item IDs
            item_id_reverse_map = {idx: iid for iid, idx in item_map.items()}
            popular_items = [
                (item_id_reverse_map[idx], float(item_popularity[idx]))
                for idx in top_indices
            ]
            
            return popular_items
        elif isinstance(matrix, list):
            # Simple popularity count from interaction list
            from collections import Counter
            item_counts = Counter()
            for user_id, item_id, rating in matrix:
                item_counts[item_id] += rating
            
            # Get top N items
            popular_items = [
                (item_id, float(count))
                for item_id, count in item_counts.most_common(n_items)
            ]
            
            return popular_items
        
        return []
    
    def get_similar_items(
        self,
        item_id: str,
        content_type: str,
        n_similar: int = 10
    ) -> List[Tuple[str, float]]:
        """
        Get items similar to the given item
        
        Args:
            item_id: Item ID to find similar items for
            content_type: Type of content
            n_similar: Number of similar items to return
        
        Returns:
            List of (item_id, similarity_score) tuples
        """
        if content_type not in self.models:
            logger.warning(f"No model found for {content_type}")
            return []
        
        model = self.models[content_type]
        item_map = self.item_id_mappings.get(content_type, {})
        
        if item_id not in item_map:
            logger.warning(f"Item {item_id} not found in {content_type} training data")
            return []
        
        item_idx = item_map[item_id]
        
        # Get item embeddings
        item_embeddings = model.item_embeddings
        item_biases = model.item_biases
        
        # Calculate cosine similarity
        target_embedding = item_embeddings[item_idx]
        similarities = np.dot(item_embeddings, target_embedding)
        
        # Normalize by magnitude
        norms = np.linalg.norm(item_embeddings, axis=1)
        target_norm = np.linalg.norm(target_embedding)
        similarities = similarities / (norms * target_norm + 1e-10)
        
        # Get top N similar items (excluding the item itself)
        similarities[item_idx] = -np.inf
        top_indices = np.argsort(-similarities)[:n_similar]
        
        # Convert back to item IDs
        item_id_reverse_map = {idx: iid for iid, idx in item_map.items()}
        similar_items = [
            (item_id_reverse_map[idx], float(similarities[idx]))
            for idx in top_indices
        ]
        
        return similar_items
    
    def save_model(self, content_type: str) -> None:
        """
        Save model and mappings to disk
        
        Args:
            content_type: Type of content to save
        """
        if content_type not in self.models:
            logger.warning(f"No model to save for {content_type}")
            return
        
        model_path = self.model_dir / f"{content_type}_model.pkl"
        user_map_path = self.model_dir / f"{content_type}_user_map.pkl"
        item_map_path = self.model_dir / f"{content_type}_item_map.pkl"
        matrix_path = self.model_dir / f"{content_type}_matrix.pkl"
        
        joblib.dump(self.models[content_type], model_path)
        joblib.dump(self.user_id_mappings[content_type], user_map_path)
        joblib.dump(self.item_id_mappings[content_type], item_map_path)
        joblib.dump(self.interaction_matrices[content_type], matrix_path)
        
        logger.info(f"Saved {content_type} model to {model_path}")
    
    def load_model(self, content_type: str) -> bool:
        """
        Load model and mappings from disk
        
        Args:
            content_type: Type of content to load
        
        Returns:
            True if successful, False otherwise
        """
        model_path = self.model_dir / f"{content_type}_model.pkl"
        user_map_path = self.model_dir / f"{content_type}_user_map.pkl"
        item_map_path = self.model_dir / f"{content_type}_item_map.pkl"
        matrix_path = self.model_dir / f"{content_type}_matrix.pkl"
        
        if not model_path.exists():
            logger.warning(f"Model file not found: {model_path}")
            return False
        
        try:
            self.models[content_type] = joblib.load(model_path)
            self.user_id_mappings[content_type] = joblib.load(user_map_path)
            self.item_id_mappings[content_type] = joblib.load(item_map_path)
            self.interaction_matrices[content_type] = joblib.load(matrix_path)
            
            logger.info(f"Loaded {content_type} model from {model_path}")
            return True
        except Exception as e:
            logger.error(f"Error loading {content_type} model: {e}")
            return False


# Global instance
_recommendation_engine = None


def get_recommendation_engine() -> RecommendationEngine:
    """
    Get or create the global recommendation engine instance
    """
    global _recommendation_engine
    if _recommendation_engine is None:
        _recommendation_engine = RecommendationEngine()
    return _recommendation_engine

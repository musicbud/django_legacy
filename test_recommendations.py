#!/usr/bin/env python
"""
Test script for movie and manga recommendation system
"""
import asyncio
import sys
import os

# Add project to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'musicbud.settings')
import django
django.setup()

from app.services.recommendation_service import get_recommendation_service
from app.services.recommendation_data_service import RecommendationDataService


async def test_data_extraction():
    """Test data extraction from Neo4j"""
    print("\n" + "="*50)
    print("Testing Data Extraction")
    print("="*50 + "\n")
    
    data_service = RecommendationDataService()
    
    # Test movie interactions
    print("Extracting movie interactions...")
    movie_interactions = await data_service.get_movie_interactions()
    print(f"  Found {len(movie_interactions)} movie interactions")
    if movie_interactions:
        print(f"  Sample: {movie_interactions[0]}")
    
    # Test manga interactions
    print("\nExtracting manga interactions...")
    manga_interactions = await data_service.get_manga_interactions()
    print(f"  Found {len(manga_interactions)} manga interactions")
    if manga_interactions:
        print(f"  Sample: {manga_interactions[0]}")
    
    # Test anime interactions
    print("\nExtracting anime interactions...")
    anime_interactions = await data_service.get_anime_interactions()
    print(f"  Found {len(anime_interactions)} anime interactions")
    if anime_interactions:
        print(f"  Sample: {anime_interactions[0]}")
    
    # Test popular movies
    print("\nGetting popular movies...")
    popular_movies = await data_service.get_popular_movies(limit=5)
    print(f"  Found {len(popular_movies)} popular movies")
    for movie in popular_movies[:3]:
        print(f"  - {movie.get('title', 'Unknown')}")
    
    # Test popular manga
    print("\nGetting popular manga...")
    popular_manga = await data_service.get_popular_manga(limit=5)
    print(f"  Found {len(popular_manga)} popular manga")
    for manga in popular_manga[:3]:
        print(f"  - {manga.get('title', 'Unknown')}")
    
    return movie_interactions, manga_interactions, anime_interactions


async def test_model_training(movie_interactions, manga_interactions, anime_interactions):
    """Test model training"""
    print("\n" + "="*50)
    print("Testing Model Training")
    print("="*50 + "\n")
    
    rec_service = get_recommendation_service()
    
    # Train movie model
    if movie_interactions:
        print("Training movie model...")
        result = await rec_service.train_movie_model()
        print(f"  Movie model training result: {result}")
    else:
        print("  Skipping movie model - no interactions")
    
    # Train manga model
    if manga_interactions:
        print("\nTraining manga model...")
        result = await rec_service.train_manga_model()
        print(f"  Manga model training result: {result}")
    else:
        print("  Skipping manga model - no interactions")
    
    # Train anime model
    if anime_interactions:
        print("\nTraining anime model...")
        result = await rec_service.train_anime_model()
        print(f"  Anime model training result: {result}")
    else:
        print("  Skipping anime model - no interactions")


async def test_recommendations():
    """Test getting recommendations"""
    print("\n" + "="*50)
    print("Testing Recommendations")
    print("="*50 + "\n")
    
    rec_service = get_recommendation_service()
    
    # Get a test user ID (using a dummy one for testing)
    test_user_id = "test_user_1"
    
    # Test movie recommendations
    print(f"Getting movie recommendations for user {test_user_id}...")
    try:
        movie_recs = await rec_service.get_movie_recommendations(test_user_id, n_recommendations=5)
        print(f"  Got {len(movie_recs)} movie recommendations")
        for i, rec in enumerate(movie_recs[:3], 1):
            print(f"  {i}. {rec.get('title', 'Unknown')} (score: {rec.get('recommendation_score', 0):.2f})")
    except Exception as e:
        print(f"  Error: {e}")
    
    # Test manga recommendations
    print(f"\nGetting manga recommendations for user {test_user_id}...")
    try:
        manga_recs = await rec_service.get_manga_recommendations(test_user_id, n_recommendations=5)
        print(f"  Got {len(manga_recs)} manga recommendations")
        for i, rec in enumerate(manga_recs[:3], 1):
            print(f"  {i}. {rec.get('title', 'Unknown')} (score: {rec.get('recommendation_score', 0):.2f})")
    except Exception as e:
        print(f"  Error: {e}")
    
    # Test anime recommendations
    print(f"\nGetting anime recommendations for user {test_user_id}...")
    try:
        anime_recs = await rec_service.get_anime_recommendations(test_user_id, n_recommendations=5)
        print(f"  Got {len(anime_recs)} anime recommendations")
        for i, rec in enumerate(anime_recs[:3], 1):
            print(f"  {i}. {rec.get('title', 'Unknown')} (score: {rec.get('recommendation_score', 0):.2f})")
    except Exception as e:
        print(f"  Error: {e}")


async def main():
    """Main test function"""
    print("\n" + "="*70)
    print(" Movie & Manga Recommendation System Test")
    print("="*70)
    
    # Test data extraction
    movie_interactions, manga_interactions, anime_interactions = await test_data_extraction()
    
    # Test model training (only if we have data)
    if movie_interactions or manga_interactions or anime_interactions:
        await test_model_training(movie_interactions, manga_interactions, anime_interactions)
    else:
        print("\nSkipping model training - no data available")
    
    # Test recommendations
    await test_recommendations()
    
    print("\n" + "="*70)
    print(" Test Complete!")
    print("="*70 + "\n")


if __name__ == "__main__":
    asyncio.run(main())

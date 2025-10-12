# Recommendation System Usage Guide

## Quick Start

### 1. Seed Sample Data

Create sample movies, manga, anime, and user interactions:

```bash
cd /home/mahmoud/Documents/GitHub/backend
source venv/bin/activate
python manage.py seed_recommendations --users 10 --movies 50 --manga 30 --anime 30
```

**Options:**
- `--users N` - Number of users to create (default: 10)
- `--movies N` - Number of movies to create (default: 50)
- `--manga N` - Number of manga to create (default: 30)
- `--anime N` - Number of anime to create (default: 30)
- `--clear` - Clear existing data before seeding

### 2. Train Recommendation Models

Train models on the seeded data:

```bash
python manage.py train_recommendations --type all
```

**Options:**
- `--type [movie|manga|anime|all]` - Type of model to train (default: all)
- `--force` - Force retraining even if models exist

### 3. Test Recommendations

Run the test script to verify everything works:

```bash
python test_recommendations.py
```

## Management Commands

### seed_recommendations

Populates Neo4j with sample data for testing the recommendation system.

**What it creates:**
- IMDB users with movie interactions (likes, watches, watchlist)
- MAL users with manga/anime interactions
- Sample movies with metadata (title, year, rating, genres, director)
- Sample manga with cover images
- Sample anime with scores and cover images

**Example:**
```bash
# Create 20 users with 100 movies
python manage.py seed_recommendations --users 20 --movies 100 --manga 50 --anime 50

# Clear and reseed
python manage.py seed_recommendations --clear --users 5 --movies 20
```

### train_recommendations

Trains LightFM recommendation models using data from Neo4j.

**What it does:**
1. Extracts user-item interactions from Neo4j
2. Creates sparse interaction matrices
3. Trains LightFM models (or uses popularity-based fallback)
4. Saves trained models to disk

**Example:**
```bash
# Train all models
python manage.py train_recommendations

# Train only movie model
python manage.py train_recommendations --type movie

# Force retrain
python manage.py train_recommendations --force
```

## API Usage

### Authentication

All recommendation endpoints require authentication. Get a token first:

```bash
TOKEN=$(curl -X POST http://localhost:8000/v1/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "your_username", "password": "your_password"}' \
  | jq -r '.access')
```

### Get All Recommendations

```bash
curl -X GET http://localhost:8000/v1/recommendations/ \
  -H "Authorization: Bearer $TOKEN" \
  | jq
```

**Response:**
```json
{
  "success": true,
  "message": "Recommendations fetched successfully",
  "data": {
    "movies": [...],
    "manga": [...],
    "anime": [...],
    "tracks": [],
    "artists": [],
    "albums": [],
    "genres": [],
    "buds": []
  }
}
```

### Get Movie Recommendations

```bash
curl -X GET http://localhost:8000/v1/recommendations/movies/ \
  -H "Authorization: Bearer $TOKEN" \
  | jq
```

**Response:**
```json
{
  "success": true,
  "message": "Movies recommendations fetched successfully",
  "data": [
    {
      "id": "tt1234567",
      "title": "Example Movie",
      "year": 2020,
      "rating": 8.5,
      "genres": ["Action", "Sci-Fi"],
      "plot": "An exciting adventure...",
      "director": "John Doe",
      "recommendation_score": 4.5
    }
  ]
}
```

### Get Manga Recommendations

```bash
curl -X GET http://localhost:8000/v1/recommendations/manga/ \
  -H "Authorization: Bearer $TOKEN" \
  | jq
```

### Get Anime Recommendations

```bash
curl -X GET http://localhost:8000/v1/recommendations/anime/ \
  -H "Authorization: Bearer $TOKEN" \
  | jq
```

### Train Models (Admin Only)

```bash
curl -X POST http://localhost:8000/v1/recommendations/train/models/ \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  | jq
```

## Python API

### Direct Service Usage

```python
import asyncio
from app.services.recommendation_service import get_recommendation_service

async def get_recommendations():
    rec_service = get_recommendation_service()
    
    # Get movie recommendations
    movies = await rec_service.get_movie_recommendations(
        user_id='user_123',
        n_recommendations=10
    )
    
    # Get manga recommendations
    manga = await rec_service.get_manga_recommendations(
        user_id='user_123',
        n_recommendations=10
    )
    
    # Train models
    results = await rec_service.train_all_models()
    
    return movies, manga

# Run
movies, manga = asyncio.run(get_recommendations())
```

### Data Service Usage

```python
import asyncio
from app.services.recommendation_data_service import RecommendationDataService

async def get_data():
    data_service = RecommendationDataService()
    
    # Get all movie interactions
    interactions = await data_service.get_movie_interactions()
    
    # Get popular movies
    popular = await data_service.get_popular_movies(limit=10)
    
    # Get movie by ID
    movie = await data_service.get_movie_by_id('tt1234567')
    
    return interactions, popular, movie

# Run
interactions, popular, movie = asyncio.run(get_data())
```

## Recommendation Engine

### Direct Engine Usage

```python
from ai.recommendation_engine import get_recommendation_engine

# Get engine instance
engine = get_recommendation_engine()

# Train a model
interactions = [
    ('user1', 'item1', 5.0),
    ('user1', 'item2', 3.0),
    ('user2', 'item1', 4.0),
    # ...
]
engine.train_model(interactions, content_type='movie')

# Get recommendations
recs = engine.get_recommendations(
    user_id='user1',
    content_type='movie',
    n_recommendations=10
)

# Get popular items
popular = engine.get_popular_items(content_type='movie', n_items=10)

# Get similar items
similar = engine.get_similar_items(
    item_id='item1',
    content_type='movie',
    n_similar=10
)
```

## Workflow Examples

### Complete Setup Workflow

```bash
#!/bin/bash
# Complete setup and test

cd /home/mahmoud/Documents/GitHub/backend
source venv/bin/activate

echo "1. Seeding data..."
python manage.py seed_recommendations --users 20 --movies 100 --manga 50 --anime 50

echo "2. Training models..."
python manage.py train_recommendations --type all

echo "3. Testing recommendations..."
python test_recommendations.py

echo "4. Starting server..."
python manage.py runserver
```

### Periodic Retraining

```bash
#!/bin/bash
# Retrain models periodically (add to cron)

cd /home/mahmoud/Documents/GitHub/backend
source venv/bin/activate

python manage.py train_recommendations --type all --force

# Log results
echo "$(date): Models retrained" >> /var/log/musicbud_training.log
```

### Add to Crontab

```bash
# Retrain models daily at 2 AM
0 2 * * * /home/mahmoud/Documents/GitHub/backend/retrain_models.sh
```

## Configuration

### Model Parameters

Edit `app/services/recommendation_service.py`:

```python
# Training parameters
n_components = 30      # Latent dimensions
epochs = 30            # Training epochs
n_recommendations = 10 # Default count
```

### Storage Location

Edit `ai/recommendation_engine.py`:

```python
model_dir = '/tmp/musicbud_models'  # Model storage
```

### Recommendation Counts

In API views (`app/views/recommendations_views.py`):

```python
# Default recommendations per type
n_recommendations=10  # For GET /recommendations/
n_recommendations=20  # For GET /recommendations/<type>/
```

## Troubleshooting

### No Recommendations Returned

**Problem:** Empty recommendation list

**Solutions:**
1. Check if models are trained:
   ```bash
   ls -la /tmp/musicbud_models/
   ```

2. Check if data exists:
   ```bash
   python test_recommendations.py
   ```

3. Train models:
   ```bash
   python manage.py train_recommendations
   ```

### Training Fails

**Problem:** Model training returns False

**Solutions:**
1. Check Neo4j connection
2. Verify data exists in Neo4j
3. Check logs for errors
4. Seed sample data first

### LightFM Not Available

**Problem:** "LightFM not available" warning

**Solution:** System automatically uses popularity-based recommendations as fallback. To use LightFM:
- Fix system library dependencies
- Install LightFM precompiled wheels
- Use Docker with proper base image

### Server Not Starting

**Problem:** Django server fails to start

**Solutions:**
1. Check port availability:
   ```bash
   netstat -tulnp | grep 8000
   ```

2. Kill existing process:
   ```bash
   pkill -f "manage.py runserver"
   ```

3. Check error logs:
   ```bash
   tail -f /tmp/django_server.log
   ```

## Performance Tips

### Caching Recommendations

Use Django cache framework:

```python
from django.core.cache import cache

# Cache recommendations for 1 hour
cache_key = f'recs_{user_id}_{content_type}'
recs = cache.get(cache_key)
if not recs:
    recs = await rec_service.get_movie_recommendations(user_id)
    cache.set(cache_key, recs, 3600)
```

### Batch Processing

Process multiple users in parallel:

```python
import asyncio

async def batch_recommendations(user_ids):
    tasks = [
        rec_service.get_movie_recommendations(uid)
        for uid in user_ids
    ]
    return await asyncio.gather(*tasks)
```

### Model Updates

Retrain models periodically but not too frequently:
- Development: On demand
- Staging: Daily
- Production: Weekly or when significant new data

## Monitoring

### Check Model Status

```bash
# Check if models exist
ls -la /tmp/musicbud_models/

# Check model size
du -h /tmp/musicbud_models/
```

### View Logs

```bash
# Django logs
tail -f /tmp/django_server.log

# Training logs (if using cron)
tail -f /var/log/musicbud_training.log
```

### Test Endpoints

```bash
# Health check
curl -X GET http://localhost:8000/v1/recommendations/ \
  -H "Authorization: Bearer $TOKEN" \
  | jq '.success'
```

## Best Practices

1. **Regular Training**: Retrain models weekly or when user base grows significantly
2. **Data Quality**: Ensure interactions are meaningful (likes, watches, not just views)
3. **Cold Start**: New users get popular items until they have enough interactions
4. **Diversity**: Consider implementing diversity algorithms to avoid echo chambers
5. **A/B Testing**: Test different recommendation strategies before production deployment
6. **Monitoring**: Track recommendation click-through rates and user engagement
7. **Privacy**: Anonymize user data in models, don't store sensitive information
8. **Scaling**: Use Redis caching for high-traffic scenarios
9. **Versioning**: Version models and track performance across versions
10. **Feedback Loop**: Incorporate user feedback (clicks, ratings) into future training

## Advanced Features

### Custom Scoring

Modify recommendation scores:

```python
def boost_recent_items(recs):
    """Boost items from recent years"""
    for rec in recs:
        if rec.get('year', 0) >= 2020:
            rec['recommendation_score'] *= 1.2
    return sorted(recs, key=lambda x: x['recommendation_score'], reverse=True)
```

### Filtering

Filter recommendations by criteria:

```python
def filter_by_genre(recs, preferred_genres):
    """Filter recommendations by user's preferred genres"""
    return [
        rec for rec in recs
        if any(g in rec.get('genres', []) for g in preferred_genres)
    ]
```

### Hybrid Recommendations

Combine collaborative and content-based:

```python
def hybrid_recommendations(user_id, n=10):
    """Mix collaborative filtering and content-based recommendations"""
    collab_recs = await rec_service.get_movie_recommendations(user_id, n//2)
    content_recs = await get_content_based_recommendations(user_id, n//2)
    return collab_recs + content_recs
```

## Support

For issues or questions:
1. Check this guide
2. Review RECOMMENDATIONS_IMPLEMENTATION.md
3. Check logs for errors
4. Test with sample data
5. Verify Neo4j connectivity

## Version History

- **v1.0** (2025-01-12): Initial implementation
  - LightFM collaborative filtering
  - Popularity-based fallback
  - Movie, manga, anime support
  - Management commands
  - REST API endpoints
  - Sample data seeder

# Guest Mode Implementation Summary

## Overview
This document describes the implementation of guest/public access to the MusicBud platform, allowing unauthenticated users to browse trending content and popular items without requiring authentication.

## Backend Implementation

### 1. Public API Endpoints

The following public endpoints have been implemented at `/v1/discover/public/` and `/v1/recommendations/public/`:

#### Available Endpoints:
- **`GET /v1/discover/public/`** - Returns discover content for guests
  - Popular movies, manga, anime
  - Trending tracks and artists
  - Available genres

- **`GET /v1/discover/public/trending/?type={type}`** - Returns trending content
  - Parameters: `type` (all, tracks, artists, movies, manga)
  - Returns mock trending data for each type

- **`GET /v1/recommendations/public/?type={type}`** - Returns popular items (not personalized)
  - Parameters: `type` (all, movies, manga)
  - Returns popularity-based recommendations

- **`GET /v1/discover/public/genres/`** - Returns available genres
  - Music genres (Pop, Rock, Hip Hop, etc.)
  - Movie genres (Action, Comedy, Drama, etc.)
  - Anime genres (Shonen, Shojo, Seinen, etc.)

### 2. Authentication & Rate Limiting

#### Middleware Updates
- **JWT Middleware** (`app/middlewares/jwt_auth_middleware.py`):
  - Added `PUBLIC_PATHS` list to bypass authentication for guest endpoints
  - Public paths are explicitly excluded from JWT authentication checks

#### Rate Limiting
- Guest endpoints currently have throttling **disabled** (set to `[]`)
- To enable rate limiting later, uncomment the `GuestRateThrottle` class
- Default rate: 100 requests/hour per IP

#### Caching
- Caching is temporarily **disabled** due to Redis authentication issues
- To re-enable caching:
  1. Configure Redis properly in Django settings
  2. Uncomment cache checks in `app/views/public_views.py`

### 3. Public Views Implementation

Location: `app/views/public_views.py`

**Classes:**
- `PublicDiscoverView` - Main discover endpoint
- `PublicTrendingView` - Trending content by type
- `PublicRecommendationsView` - Popular items (not personalized)
- `PublicGenresView` - Available genres/categories

**Features:**
- All views use `permission_classes = [AllowAny]`
- Graceful error handling with fallback responses
- Async data fetching from Neo4j (where applicable)
- Mock data fallback when real data unavailable

### 4. URL Configuration

Added to `app/urls.py`:
```python
# Public/Guest endpoints (no authentication required)
path('v1/discover/public/', PublicDiscoverView.as_view(), name='public_discover'),
path('v1/discover/public/trending/', PublicTrendingView.as_view(), name='public_trending'),
path('v1/recommendations/public/', PublicRecommendationsView.as_view(), name='public_recommendations'),
path('v1/discover/public/genres/', PublicGenresView.as_view(), name='public_genres'),
```

## Flutter/Frontend Implementation

### 1. Guest Service

Location: `lib/services/guest_service.dart`

**Features:**
- Singleton pattern for consistent instance management
- Dio-based HTTP client with interceptors
- No authentication headers required
- Comprehensive error handling

**Methods:**
- `getPublicDiscover()` - Fetch all discover content
- `getTrendingContent({type})` - Fetch trending items by type
- `getPublicRecommendations({type})` - Fetch popular items
- `getGenres()` - Fetch all available genres
- Helper methods: `getTrendingTracks()`, `getTrendingArtists()`, etc.

### 2. Guest Discover Screen Updates

Location: `lib/presentation/screens/discover/guest_discover_screen.dart`

**Changes:**
- Integrated `GuestService` to fetch real API data
- Added loading states with `CircularProgressIndicator`
- Added error handling with retry functionality
- Fallback to mock data when API unavailable
- Pull-to-refresh functionality on all tabs

**UI Features:**
- Three tabs: Artists, Tracks, Genres
- Real-time data loading from backend APIs
- Graceful degradation to mock data
- Sign-in prompts for authenticated features

## Testing

### Manual Testing

Test the backend public endpoints:

```bash
# Test genres endpoint
curl -X GET http://localhost:8000/v1/discover/public/genres/

# Test trending content (movies)
curl -X GET "http://localhost:8000/v1/discover/public/trending/?type=movies"

# Test public recommendations
curl -X GET "http://localhost:8000/v1/recommendations/public/?type=all"

# Test public discover
curl -X GET http://localhost:8000/v1/discover/public/
```

### Expected Responses

All successful responses follow this format:
```json
{
  "success": true,
  "message": "...",
  "data": { ... }
}
```

## Future Enhancements

### Backend:
1. **Redis Configuration**: Set up Redis with proper authentication for caching
2. **Rate Limiting**: Enable throttling for guest endpoints to prevent abuse
3. **Real Data Integration**: Connect to actual data sources for movies, manga, anime
4. **Analytics**: Track guest usage patterns and conversion rates

### Frontend:
1. **Offline Support**: Cache guest data locally for offline browsing
2. **Enhanced UI**: Add animations and better loading states
3. **Content Details**: Implement detail views for trending items
4. **Search**: Add search functionality for guest users
5. **Conversion Prompts**: Strategic sign-in prompts at key interaction points

## Configuration Notes

### Redis Setup (Optional)
To enable caching and rate limiting:

1. Install and start Redis:
   ```bash
   sudo apt-get install redis-server
   sudo systemctl start redis
   ```

2. Update Django settings (`musicbud/settings.py`):
   ```python
   CACHES = {
       "default": {
           "BACKEND": "django_redis.cache.RedisCache",
           "LOCATION": "redis://127.0.0.1:6379/1",
           "OPTIONS": {
               "CLIENT_CLASS": "django_redis.client.DefaultClient",
               # Add authentication if needed:
               # "PASSWORD": "your-redis-password",
           }
       }
   }
   ```

3. Uncomment caching code in `app/views/public_views.py`
4. Re-enable throttling by uncommenting `throttle_classes = [GuestRateThrottle]`

### Flutter Configuration
Update base URL if deploying to production:

```dart
GuestService(baseUrl: 'https://your-production-api.com')
```

## Deployment Checklist

- [ ] Configure Redis with authentication
- [ ] Enable rate limiting on guest endpoints
- [ ] Update CORS settings for production domain
- [ ] Set up monitoring for guest endpoint usage
- [ ] Configure CDN for static content
- [ ] Test all endpoints with production data
- [ ] Update Flutter app with production API URL
- [ ] Implement analytics tracking
- [ ] Add error reporting (Sentry, etc.)

## Security Considerations

1. **Rate Limiting**: Prevent API abuse by implementing request throttling
2. **CORS**: Restrict allowed origins in production
3. **Data Exposure**: Ensure guest endpoints don't expose sensitive information
4. **DDoS Protection**: Consider using Cloudflare or similar services
5. **Monitoring**: Set up alerts for unusual traffic patterns

## Support & Maintenance

### Logs
- Backend logs: `/tmp/django_server.log`
- Check logs for errors: `tail -f /tmp/django_server.log`

### Common Issues

**Issue**: "Authentication required" error on public endpoints
- **Solution**: Verify JWT middleware `PUBLIC_PATHS` includes the endpoint
- **Solution**: Restart Django server after middleware changes

**Issue**: Empty responses from public endpoints
- **Solution**: Check if Neo4j database contains data
- **Solution**: Verify recommendation service is working
- **Solution**: Check if mock data fallback is functioning

**Issue**: Flutter connection errors
- **Solution**: Verify Django server is running on correct port
- **Solution**: Check Flutter `baseUrl` configuration
- **Solution**: Verify network connectivity

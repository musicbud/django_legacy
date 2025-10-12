# Guest Mode - Quick Start Guide

## What's Been Implemented

✅ Backend public/guest API endpoints  
✅ JWT middleware updates to bypass auth for public paths  
✅ Flutter guest service for API calls  
✅ Updated guest discover screen with real data  
✅ Comprehensive error handling and fallbacks  
✅ Test script to verify endpoints  

## Quick Test

Run the test script to verify all endpoints are working:

```bash
bash /home/mahmoud/Documents/GitHub/backend/test_guest_endpoints.sh
```

Or test individual endpoints:

```bash
# Genres
curl http://localhost:8000/v1/discover/public/genres/

# Trending artists
curl "http://localhost:8000/v1/discover/public/trending/?type=artists"

# All trending content
curl "http://localhost:8000/v1/discover/public/trending/?type=all"

# Recommendations
curl "http://localhost:8000/v1/recommendations/public/?type=all"

# Content details
curl "http://localhost:8000/v1/content/public/movie/movie_1/"
curl "http://localhost:8000/v1/content/public/track/track_1/"
```

## API Endpoints Summary

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/v1/discover/public/` | GET | Get all discover content |
| `/v1/discover/public/trending/` | GET | Get trending content by type |
| `/v1/recommendations/public/` | GET | Get popular recommendations |
| `/v1/discover/public/genres/` | GET | Get available genres |
| `/v1/content/public/<type>/<id>/` | GET | Get detailed info for specific content |

### Query Parameters

- **trending endpoint**: `?type={all|tracks|artists|movies|manga}`
- **recommendations endpoint**: `?type={all|movies|manga}`

### URL Parameters

- **content details endpoint**: 
  - `<type>`: {movie|manga|anime|track|artist|album}
  - `<id>`: content identifier (e.g., movie_1, track_1, artist_1)

## Flutter Integration

### Using Guest Service

```dart
import 'package:your_app/services/guest_service.dart';

final guestService = GuestService();

// Get trending tracks
final tracks = await guestService.getTrendingTracks();

// Get genres
final genres = await guestService.getGenres();

// Get public recommendations
final recommendations = await guestService.getPublicRecommendations(type: 'movies');

// Get content details
final movieDetails = await guestService.getMovieDetails('movie_1');
final trackDetails = await guestService.getTrackDetails('track_1');
final artistDetails = await guestService.getArtistDetails('artist_1');
```

### Guest Discover Screen

The guest discover screen is located at:
```
lib/presentation/screens/discover/guest_discover_screen.dart
```

Features:
- Real API integration with fallback to mock data
- Loading states and error handling
- Pull-to-refresh on all tabs
- Sign-in prompts for authenticated features

## Files Modified/Created

### Backend
- ✅ `app/views/public_views.py` - Public API views (already existed, updated)
- ✅ `app/urls.py` - Added public URL routes
- ✅ `app/middlewares/jwt_auth_middleware.py` - Updated to allow public paths
- ✅ `GUEST_MODE_IMPLEMENTATION.md` - Comprehensive documentation
- ✅ `test_guest_endpoints.sh` - Test script

### Flutter
- ✅ `lib/services/guest_service.dart` - New guest API service
- ✅ `lib/presentation/screens/discover/guest_discover_screen.dart` - Updated with real API calls

## Current Status

### Working ✅
- All public API endpoints responding correctly
- Authentication bypass for public paths
- Genres endpoint with music/movies/anime categories
- Trending content endpoints (tracks, artists, movies, manga)
- Public recommendations endpoints
- Error handling and fallback responses

### Temporarily Disabled ⚠️
- **Caching**: Disabled due to Redis authentication issues
  - To enable: Configure Redis and uncomment cache code
- **Rate Limiting**: Disabled for development
  - To enable: Uncomment `throttle_classes = [GuestRateThrottle]`

### Not Yet Implemented 🔜
- Real movie/manga data (currently using mock data)
- Redis caching configuration
- Rate limiting for production
- Analytics tracking for guest users

## Next Steps

1. **For Development**:
   - Test Flutter app with the new guest service
   - Verify all screens handle loading/error states
   - Test on different devices/emulators

2. **For Production**:
   - Set up Redis with authentication
   - Enable rate limiting
   - Add analytics tracking
   - Populate real movie/manga data
   - Configure CDN for static assets

3. **Optional Enhancements**:
   - Add more content types (albums, playlists)
   - Implement guest search functionality
   - Add content detail views for guests
   - Track guest-to-user conversion rates

## Troubleshooting

**Problem**: Endpoints return authentication errors  
**Solution**: Restart Django server and verify JWT middleware changes

**Problem**: Empty data in responses  
**Solution**: Check if backend has real data or is using mock fallbacks

**Problem**: Flutter connection errors  
**Solution**: Verify Django server is running on `http://localhost:8000`

**Problem**: Redis connection errors  
**Solution**: Caching is disabled by default, no action needed for development

## Documentation

For detailed documentation, see:
- `GUEST_MODE_IMPLEMENTATION.md` - Complete implementation details
- `PROJECT_ANALYSIS_AND_PLAN.md` - Original project analysis

## Testing Flutter App

To test the Flutter app with guest mode:

1. Ensure Django backend is running:
   ```bash
   python manage.py runserver 0.0.0.0:8000
   ```

2. Run Flutter app:
   ```bash
   cd /path/to/flutter/app
   flutter run
   ```

3. Navigate to guest discover screen and verify:
   - Data loads from API (not mock)
   - Pull-to-refresh works
   - Error states display correctly
   - Sign-in prompts appear when needed

## Support

For issues or questions:
1. Check server logs: `tail -f /tmp/django_server.log`
2. Run test script: `bash test_guest_endpoints.sh`
3. Review documentation in `GUEST_MODE_IMPLEMENTATION.md`

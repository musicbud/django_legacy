# Guest Mode API Reference Card

Quick reference for all public/guest endpoints.

---

## Base URL

```
http://localhost:8000  (Development)
https://api.musicbud.com  (Production - TBD)
```

---

## 🌟 Discovery Endpoints

### Get Discover Content
```http
GET /v1/discover/public/
```

**Response:**
```json
{
  "success": true,
  "message": "Public discover content fetched successfully",
  "data": {
    "trending_tracks": [],
    "popular_artists": [],
    "popular_movies": [],
    "popular_manga": [],
    "popular_anime": [],
    "genres": [...]
  }
}
```

### Get Trending Content
```http
GET /v1/discover/public/trending/?type={type}
```

**Parameters:**
- `type`: all | tracks | artists | movies | manga

**Response:**
```json
{
  "success": true,
  "message": "Trending content fetched successfully",
  "data": {
    "tracks": [...],
    "artists": [...],
    "movies": [...],
    "manga": [...]
  }
}
```

### Get Genres
```http
GET /v1/discover/public/genres/
```

**Response:**
```json
{
  "success": true,
  "message": "Genres fetched successfully",
  "data": {
    "music": [...],
    "movies": [...],
    "anime": [...]
  }
}
```

---

## 🎯 Recommendations Endpoints

### Get Public Recommendations
```http
GET /v1/recommendations/public/?type={type}
```

**Parameters:**
- `type`: all | movies | manga

**Response:**
```json
{
  "success": true,
  "message": "Public recommendations fetched successfully",
  "data": {
    "movies": [...],
    "manga": [...]
  },
  "is_personalized": false
}
```

---

## 🎬 Content Detail Endpoints

### Get Movie Details
```http
GET /v1/content/public/movie/{movie_id}/
```

**Response:**
```json
{
  "success": true,
  "message": "Movie details fetched successfully",
  "data": {
    "id": "movie_1",
    "title": "The Shawshank Redemption",
    "year": 1994,
    "rating": 9.3,
    "duration": "2h 22min",
    "genres": ["Drama"],
    "director": "Frank Darabont",
    "cast": ["Tim Robbins", "Morgan Freeman"],
    "plot": "...",
    "poster": null,
    "trailer_url": null
  }
}
```

### Get Manga Details
```http
GET /v1/content/public/manga/{manga_id}/
```

**Response:**
```json
{
  "success": true,
  "message": "Manga details fetched successfully",
  "data": {
    "id": "manga_1",
    "title": "One Piece",
    "author": "Eiichiro Oda",
    "chapters": 1100,
    "volumes": 107,
    "status": "Ongoing",
    "rating": 9.0,
    "genres": ["Action", "Adventure"],
    "synopsis": "...",
    "cover": null,
    "published": "1997-present"
  }
}
```

### Get Anime Details
```http
GET /v1/content/public/anime/{anime_id}/
```

**Response:**
```json
{
  "success": true,
  "message": "Anime details fetched successfully",
  "data": {
    "id": "anime_1",
    "title": "Fullmetal Alchemist: Brotherhood",
    "episodes": 64,
    "rating": 9.1,
    "status": "Completed",
    "genres": ["Action", "Adventure"],
    "studio": "Bones",
    "synopsis": "...",
    "cover": null,
    "aired": "2009-2010"
  }
}
```

### Get Track Details
```http
GET /v1/content/public/track/{track_id}/
```

**Response:**
```json
{
  "success": true,
  "message": "Track details fetched successfully",
  "data": {
    "id": "track_1",
    "name": "Anti-Hero",
    "artist": "Taylor Swift",
    "album": "Midnights",
    "duration": "3:20",
    "release_date": "2022-10-21",
    "popularity": 95,
    "genres": ["Pop"],
    "preview_url": null,
    "lyrics_available": false
  }
}
```

### Get Artist Details
```http
GET /v1/content/public/artist/{artist_id}/
```

**Response:**
```json
{
  "success": true,
  "message": "Artist details fetched successfully",
  "data": {
    "id": "artist_1",
    "name": "Taylor Swift",
    "genre": "Pop",
    "followers": 1500000,
    "popularity": 95,
    "bio": "...",
    "top_tracks": ["Anti-Hero", "Blank Space"],
    "image": null
  }
}
```

### Get Album Details
```http
GET /v1/content/public/album/{album_id}/
```

**Response:**
```json
{
  "success": true,
  "message": "Album details fetched successfully",
  "data": {
    "id": "album_1",
    "name": "Midnights",
    "artist": "Taylor Swift",
    "release_date": "2022-10-21",
    "total_tracks": 13,
    "genres": ["Pop"],
    "cover": null,
    "tracks": [...]
  }
}
```

---

## ⚠️ Error Responses

### 400 Bad Request
```json
{
  "success": false,
  "message": "Invalid content type. Must be one of: ['movie', 'manga', 'anime', 'track', 'artist', 'album']"
}
```

### 404 Not Found
```json
{
  "success": false,
  "message": "Movie not found"
}
```

### 500 Internal Server Error
```json
{
  "success": false,
  "message": "Error fetching content details: {error_message}"
}
```

---

## 📋 Available IDs (Mock Data)

### Movies
- `movie_1`: The Shawshank Redemption
- `movie_2`: The Godfather

### Manga
- `manga_1`: One Piece
- `manga_2`: Attack on Titan

### Anime
- `anime_1`: Fullmetal Alchemist: Brotherhood
- `anime_2`: Steins;Gate

### Tracks
- `track_1`: Anti-Hero
- `track_2`: Blinding Lights
- `track_3`: What Was I Made For?

### Artists
- `artist_1`: Taylor Swift
- `artist_2`: The Weeknd
- `artist_3`: Billie Eilish

### Albums
- `album_1`: Midnights

---

## 🔑 Authentication

**None required!** All endpoints are public and accessible without authentication.

---

## 📊 Rate Limiting

**Currently disabled** for development.

When enabled:
- **Rate**: 100 requests per hour per IP
- **Response Headers**: 
  - `X-RateLimit-Limit`
  - `X-RateLimit-Remaining`
  - `X-RateLimit-Reset`

---

## 🧪 Testing

### cURL Examples

```bash
# Get trending movies
curl -X GET "http://localhost:8000/v1/discover/public/trending/?type=movies"

# Get movie details
curl -X GET "http://localhost:8000/v1/content/public/movie/movie_1/"

# Get all genres
curl -X GET "http://localhost:8000/v1/discover/public/genres/"
```

### Flutter Example

```dart
import 'package:musicbud/services/guest_service.dart';

final service = GuestService();

// Get trending
final tracks = await service.getTrendingTracks();

// Get details
final movie = await service.getMovieDetails('movie_1');
final artist = await service.getArtistDetails('artist_1');
```

---

## 📖 Full Documentation

- **Implementation Details**: `GUEST_MODE_IMPLEMENTATION.md`
- **Quick Start Guide**: `GUEST_MODE_QUICKSTART.md`
- **Final Summary**: `GUEST_MODE_FINAL_SUMMARY.md`
- **This Reference**: `GUEST_API_REFERENCE.md`

---

*Last Updated: 2025-10-12*

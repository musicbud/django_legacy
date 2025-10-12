# MusicBud FastAPI Backend - Complete API Documentation

## Overview
This document provides a comprehensive overview of all available endpoints in the MusicBud FastAPI backend, organized by feature area.

**Base URL**: `http://localhost:8000`  
**API Version**: v1  
**Prefix**: `/v1`

---

## 🎵 Public/Guest Endpoints
No authentication required. Accessible to all users.

### Discovery & Trending

#### GET `/v1/discover/public/`
Get public discover content with trending tracks, popular artists, movies, manga, anime, and genres.

**Response:**
```json
{
  "success": true,
  "message": "Public discover content fetched successfully",
  "data": {
    "trending_tracks": [...],
    "popular_artists": [...],
    "popular_movies": [...],
    "popular_manga": [...],
    "popular_anime": [...],
    "genres": [...]
  }
}
```

#### GET `/v1/discover/public/trending/`
Get trending content by type.

**Query Parameters:**
- `type` (string): `all`, `tracks`, `artists`, `movies`, `manga`

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

#### GET `/v1/discover/public/genres/`
Get available genres for music, movies, and anime.

**Response:**
```json
{
  "success": true,
  "message": "Genres fetched successfully",
  "data": {
    "music": [{"id": "pop", "name": "Pop", "color": "#FF6B6B"}, ...],
    "movies": [{"id": "action", "name": "Action", "color": "#FF4500"}, ...],
    "anime": [{"id": "shonen", "name": "Shonen", "color": "#FF6347"}, ...]
  }
}
```

### Content Details

#### GET `/v1/content/public/{content_type}/{content_id}/`
Get detailed information about specific content.

**Path Parameters:**
- `content_type` (string): `track`, `artist`, `album`, `movie`, `anime`, `manga`
- `content_id` (string): Unique identifier for the content

**Response:** Content-specific details including metadata, ratings, and related information.

### Recommendations

#### GET `/v1/recommendations/public/`
Get public recommendations (non-personalized).

**Response:**
```json
{
  "success": true,
  "message": "Recommendations fetched successfully",
  "data": {
    "movies": [...],
    "manga": [...]
  },
  "is_personalized": false
}
```

---

## 👤 User Profile & Settings Endpoints
Authentication required.

### Profile Management

#### GET `/v1/users/profile`
Get current user's profile information.

**Response:**
```json
{
  "id": "user_123",
  "username": "musiclover",
  "display_name": "Music Lover",
  "bio": "Passionate about indie rock and anime OSTs 🎵",
  "avatar_url": null,
  "cover_image_url": null,
  "location": "San Francisco, CA",
  "age": 25,
  "gender": "non-binary",
  "interests": ["Music", "Anime", "Movies", "Gaming"],
  "favorite_genres": {
    "music": ["Rock", "Indie", "Alternative"],
    "movies": ["Sci-Fi", "Drama"],
    "anime": ["Shonen", "Slice of Life"]
  },
  "is_verified": true,
  "created_at": "2024-01-15T10:30:00Z",
  "stats": {
    "tracks_played": 1247,
    "playlists": 12,
    "friends": 43,
    "matches": 28
  }
}
```

#### GET `/v1/users/profile/{user_id}`
Get another user's public profile.

**Path Parameters:**
- `user_id` (string): Target user's ID

#### PUT `/v1/users/profile`
Update current user's profile.

**Request Body:**
```json
{
  "display_name": "New Name",
  "bio": "Updated bio",
  "location": "New York, NY",
  "avatar_url": "https://example.com/avatar.jpg"
}
```

### User Preferences

#### GET `/v1/users/preferences`
Get user content preferences.

**Response:**
```json
{
  "music_genres": ["Rock", "Indie", "Alternative"],
  "movie_genres": ["Sci-Fi", "Drama", "Thriller"],
  "anime_genres": ["Shonen", "Seinen"],
  "favorite_artists": ["Arctic Monkeys", "Tame Impala"],
  "favorite_movies": ["Inception", "Interstellar"],
  "favorite_anime": ["Attack on Titan", "Steins;Gate"]
}
```

#### PUT `/v1/users/preferences`
Update user content preferences.

**Request Body:** Same structure as GET response.

### Matching Preferences

#### GET `/v1/users/matching/preferences`
Get user matching/discovery preferences.

**Response:**
```json
{
  "age_range": {"min": 21, "max": 35},
  "distance_range": 50,
  "gender_preference": "all",
  "looking_for": ["friends", "music_buddies", "concert_partners"],
  "match_by_music": true,
  "match_by_movies": true,
  "match_by_anime": true,
  "min_compatibility": 75
}
```

#### PUT `/v1/users/matching/preferences`
Update matching preferences.

### Privacy Settings

#### GET `/v1/users/settings/privacy`
Get privacy settings.

**Response:**
```json
{
  "profile_visibility": "public",
  "show_age": true,
  "show_location": true,
  "show_last_seen": true,
  "allow_messages_from": "friends",
  "show_listening_activity": true
}
```

#### PUT `/v1/users/settings/privacy`
Update privacy settings.

### Notification Settings

#### GET `/v1/users/settings/notifications`
Get notification preferences.

**Response:**
```json
{
  "push_enabled": true,
  "email_enabled": true,
  "new_matches": true,
  "new_messages": true,
  "friend_requests": true,
  "recommendations": true,
  "trending_updates": false
}
```

#### PUT `/v1/users/settings/notifications`
Update notification settings.

### App Settings

#### GET `/v1/users/settings/app`
Get app preferences.

**Response:**
```json
{
  "theme": "dark",
  "language": "en",
  "auto_play": true,
  "data_saver": false,
  "download_quality": "high"
}
```

#### PUT `/v1/users/settings/app`
Update app settings.

### User Statistics

#### GET `/v1/users/stats`
Get user statistics and listening activity.

**Response:**
```json
{
  "total_listening_time": 12480,
  "tracks_played": 1247,
  "favorite_genre": "Indie Rock",
  "top_artists": [...],
  "top_tracks": [...],
  "listening_history": [...],
  "playlists_created": 12,
  "friends": 43,
  "matches": 28
}
```

#### GET `/v1/users/activity/recent`
Get user's recent activity.

**Query Parameters:**
- `limit` (int): Number of items to return (default: 20, max: 100)

---

## 🎯 Matching & Buds Endpoints
Find and connect with music buddies.

### Discovery & Swiping

#### GET `/v1/matching/discover`
Get potential matches for swiping.

**Query Parameters:**
- `limit` (int): Number of profiles to return (default: 10, max: 50)

**Response:**
```json
[
  {
    "id": "user_456",
    "username": "indierocklover",
    "display_name": "Alex",
    "age": 26,
    "location": "San Francisco, CA",
    "bio": "Indie rock enthusiast, concert junkie 🎸",
    "avatar_url": null,
    "distance": 2.5,
    "compatibility_score": 87,
    "common_interests": ["Indie Rock", "Concerts", "Anime"],
    "music_compatibility": 92,
    "movie_compatibility": 78,
    "anime_compatibility": 91,
    "top_artists": ["Arctic Monkeys", "The Strokes"],
    "top_genres": ["Indie", "Rock", "Alternative"],
    "is_verified": true
  }
]
```

#### POST `/v1/matching/swipe`
Swipe on a user (like, pass, or super_like).

**Request Body:**
```json
{
  "user_id": "user_456",
  "action": "like"
}
```

**Response:**
```json
{
  "success": true,
  "action": "like",
  "is_match": true,
  "match": {
    "id": "match_123",
    "user_id": "user_456",
    "username": "indierocklover",
    "display_name": "Alex",
    "compatibility_score": 87,
    "matched_at": "2024-10-12T10:04:00Z",
    "message": "It's a match! Start chatting now! 🎉"
  }
}
```

### Matches Management

#### GET `/v1/matching/matches`
Get user's matches.

**Query Parameters:**
- `status` (string): `pending`, `matched`, `unmatched`
- `limit` (int): Number of matches to return (default: 50, max: 100)

**Response:**
```json
[
  {
    "id": "match_001",
    "user_id": "user_456",
    "username": "indierocklover",
    "display_name": "Alex",
    "avatar_url": null,
    "compatibility_score": 87,
    "matched_at": "2024-10-12T10:04:00Z",
    "last_message": "Hey! Love your music taste!",
    "last_message_at": "2024-10-12T10:15:00Z",
    "unread_count": 2
  }
]
```

#### GET `/v1/matching/matches/{match_id}`
Get detailed information about a specific match.

#### DELETE `/v1/matching/matches/{match_id}`
Unmatch with a user.

### Connections/Friends

#### GET `/v1/matching/connections`
Get user's connections/friends.

**Query Parameters:**
- `limit` (int): Number of connections (default: 100, max: 200)

**Response:**
```json
[
  {
    "id": "conn_001",
    "user_id": "user_456",
    "username": "indierocklover",
    "display_name": "Alex",
    "avatar_url": null,
    "bio": "Indie rock enthusiast 🎸",
    "compatibility_score": 87,
    "connected_at": "2024-09-15T12:00:00Z",
    "common_interests": ["Indie Rock", "Concerts", "Anime"],
    "is_online": true,
    "last_seen": null
  }
]
```

#### POST `/v1/matching/connections/{user_id}`
Add a user as a connection/friend.

#### DELETE `/v1/matching/connections/{user_id}`
Remove a connection/friend.

### Compatibility

#### GET `/v1/matching/compatibility/{user_id}`
Get detailed compatibility breakdown with a specific user.

**Response:**
```json
{
  "success": true,
  "user_id": "user_456",
  "data": {
    "overall_score": 87,
    "music_compatibility": {
      "score": 92,
      "common_genres": ["Indie", "Rock", "Alternative"],
      "common_artists": ["Arctic Monkeys", "The Strokes"],
      "shared_top_tracks": 12
    },
    "movie_compatibility": {...},
    "anime_compatibility": {...},
    "personality_match": {
      "score": 85,
      "matching_traits": ["Creative", "Outgoing", "Passionate"]
    }
  }
}
```

#### GET `/v1/matching/stats`
Get user's matching statistics.

---

## 💬 Chat & Messaging Endpoints
Real-time messaging and content sharing.

### Conversations Management

#### GET `/v1/chat/conversations`
Get user's conversations.

**Query Parameters:**
- `status` (string): `active`, `archived`, `muted`, `blocked`
- `limit` (int): Number of conversations (default: 50, max: 100)

**Response:**
```json
[
  {
    "id": "conv_001",
    "user_id": "user_456",
    "username": "indierocklover",
    "display_name": "Alex",
    "avatar_url": null,
    "last_message": "Hey! Love your music taste!",
    "last_message_at": "2024-10-12T10:15:00Z",
    "last_message_type": "text",
    "unread_count": 2,
    "is_online": true,
    "status": "active",
    "created_at": "2024-10-12T10:04:00Z"
  }
]
```

#### GET `/v1/chat/conversations/{conversation_id}`
Get specific conversation details.

#### POST `/v1/chat/conversations`
Create a new conversation.

**Request Body:**
```json
{
  "user_id": "user_456",
  "initial_message": "Hey! Love your profile!"
}
```

#### PUT `/v1/chat/conversations/{conversation_id}/status`
Update conversation status (archive, mute, block).

**Query Parameters:**
- `status` (string): `active`, `archived`, `muted`, `blocked`

#### DELETE `/v1/chat/conversations/{conversation_id}`
Delete a conversation.

### Messages

#### GET `/v1/chat/conversations/{conversation_id}/messages`
Get messages from a conversation.

**Query Parameters:**
- `before` (string): Get messages before this message ID (pagination)
- `limit` (int): Number of messages (default: 50, max: 100)

**Response:**
```json
[
  {
    "id": "msg_001",
    "conversation_id": "conv_001",
    "sender_id": "user_456",
    "sender_name": "Alex",
    "sender_avatar": null,
    "message_type": "text",
    "content": "Hey! Love your music taste!",
    "metadata": null,
    "timestamp": "2024-10-12T10:15:00Z",
    "is_read": true,
    "is_delivered": true
  }
]
```

#### POST `/v1/chat/messages`
Send a message.

**Request Body:**
```json
{
  "conversation_id": "conv_001",
  "message_type": "text",
  "content": "Hey! Great to connect!",
  "metadata": null
}
```

#### PUT `/v1/chat/messages/{message_id}/read`
Mark a message as read.

#### PUT `/v1/chat/conversations/{conversation_id}/read-all`
Mark all messages in a conversation as read.

#### DELETE `/v1/chat/messages/{message_id}`
Delete a message.

### Content Sharing

#### POST `/v1/chat/share/track`
Share a music track.

**Request Body:**
```json
{
  "conversation_id": "conv_001",
  "track_id": "track_123",
  "message": "Check out this track!"
}
```

#### POST `/v1/chat/share/playlist`
Share a playlist.

#### POST `/v1/chat/share/movie`
Share a movie.

#### POST `/v1/chat/share/anime`
Share an anime.

### Typing Indicators

#### POST `/v1/chat/conversations/{conversation_id}/typing`
Send typing indicator.

**Query Parameters:**
- `is_typing` (bool): true to start typing, false to stop

### Chat Statistics

#### GET `/v1/chat/stats`
Get user's chat statistics.

**Response:**
```json
{
  "total_conversations": 28,
  "active_conversations": 18,
  "archived_conversations": 10,
  "total_messages_sent": 1247,
  "total_messages_received": 1893,
  "unread_messages": 5,
  "average_response_time": "5 minutes",
  "most_active_conversation": {
    "user_id": "user_456",
    "display_name": "Alex",
    "message_count": 342
  }
}
```

---

## 📊 Message Types

### Supported Message Types:
- `text` - Plain text message
- `image` - Image attachment
- `audio` - Audio file
- `video` - Video file
- `track_share` - Shared music track (with metadata)
- `playlist_share` - Shared playlist
- `movie_share` - Shared movie
- `anime_share` - Shared anime

### Shared Content Metadata Structure:

**Track Share:**
```json
{
  "track_id": "track_123",
  "track_name": "Song Title",
  "artist": "Artist Name",
  "album": "Album Name",
  "cover_url": "https://..."
}
```

**Playlist Share:**
```json
{
  "playlist_id": "playlist_123",
  "playlist_name": "My Playlist",
  "tracks_count": 24,
  "cover_url": "https://..."
}
```

---

## 🔐 Authentication

All endpoints except those under `/v1/discover/public/`, `/v1/recommendations/public/`, and `/v1/content/public/` require authentication.

**Header:**
```
Authorization: Bearer <JWT_TOKEN>
```

---

## 🚀 Getting Started

1. **Start the FastAPI server:**
```bash
cd /home/mahmoud/Documents/GitHub/backend/fastapi_backend
uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload
```

2. **Access the interactive API documentation:**
   - Swagger UI: `http://localhost:8001/docs`
   - ReDoc: `http://localhost:8001/redoc`

3. **Test the endpoints:**
```bash
# Public endpoint (no auth required)
curl http://localhost:8001/v1/discover/public/

# Protected endpoint (auth required)
curl -H "Authorization: Bearer YOUR_TOKEN" http://localhost:8001/v1/users/profile
```

---

## 📝 Notes

- All timestamps are in ISO 8601 format (UTC)
- All IDs are strings
- Pagination is supported on list endpoints
- Rate limiting may be implemented in production
- WebSocket support for real-time chat will be added in future

---

## 🎨 Flutter Integration

To use these endpoints in your Flutter app:

1. Import the components library:
```dart
import 'package:musicbud_flutter/core/components/musicbud_components.dart';
```

2. Use the new Figma-inspired screens:
```dart
import 'package:musicbud_flutter/presentation/screens/home/figma_home_screen.dart';

// In your routing
FigmaHomeScreen()
```

3. Call the API endpoints using your HTTP client (dio, http, etc.)

---

**End of Documentation**

For updates and more information, visit the project repository.

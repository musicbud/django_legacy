"""
User endpoints - authentication required
Handles profile, preferences, matching settings, and user data
"""
from fastapi import APIRouter, HTTPException, Depends, Query
from typing import List, Optional, Dict, Any
from pydantic import BaseModel
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/users", tags=["users"])

# ============================================================================
# REQUEST/RESPONSE SCHEMAS
# ============================================================================

class UserProfile(BaseModel):
    """User profile schema"""
    id: str
    username: str
    display_name: str
    bio: Optional[str] = None
    avatar_url: Optional[str] = None
    cover_image_url: Optional[str] = None
    location: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None
    interests: List[str] = []
    favorite_genres: Dict[str, List[str]] = {}
    is_verified: bool = False
    created_at: str
    stats: Dict[str, int] = {}


class UpdateProfileRequest(BaseModel):
    """Update profile request"""
    display_name: Optional[str] = None
    bio: Optional[str] = None
    location: Optional[str] = None
    avatar_url: Optional[str] = None
    cover_image_url: Optional[str] = None


class UserPreferences(BaseModel):
    """User preferences schema"""
    music_genres: List[str] = []
    movie_genres: List[str] = []
    anime_genres: List[str] = []
    favorite_artists: List[str] = []
    favorite_movies: List[str] = []
    favorite_anime: List[str] = []


class MatchingPreferences(BaseModel):
    """Matching preferences schema"""
    age_range: Dict[str, int] = {"min": 18, "max": 99}
    distance_range: int = 50  # in km
    gender_preference: Optional[str] = "all"
    looking_for: List[str] = ["friends", "music_buddies"]
    match_by_music: bool = True
    match_by_movies: bool = True
    match_by_anime: bool = True
    min_compatibility: int = 70  # percentage


class PrivacySettings(BaseModel):
    """Privacy settings schema"""
    profile_visibility: str = "public"  # public, friends, private
    show_age: bool = True
    show_location: bool = True
    show_last_seen: bool = True
    allow_messages_from: str = "everyone"  # everyone, friends, no_one
    show_listening_activity: bool = True


class NotificationSettings(BaseModel):
    """Notification settings schema"""
    push_enabled: bool = True
    email_enabled: bool = True
    new_matches: bool = True
    new_messages: bool = True
    friend_requests: bool = True
    recommendations: bool = True
    trending_updates: bool = False


class AppSettings(BaseModel):
    """App settings schema"""
    theme: str = "dark"  # dark, light, auto
    language: str = "en"
    auto_play: bool = True
    data_saver: bool = False
    download_quality: str = "high"  # low, medium, high


# ============================================================================
# PROFILE ENDPOINTS
# ============================================================================

@router.get("/profile", response_model=UserProfile)
async def get_user_profile():
    """
    Get current user profile
    """
    try:
        # TODO: Get from authenticated user context
        profile = UserProfile(
            id="user_123",
            username="musiclover",
            display_name="Music Lover",
            bio="Passionate about indie rock and anime OSTs 🎵",
            avatar_url=None,
            cover_image_url=None,
            location="San Francisco, CA",
            age=25,
            gender="non-binary",
            interests=["Music", "Anime", "Movies", "Gaming"],
            favorite_genres={
                "music": ["Rock", "Indie", "Alternative"],
                "movies": ["Sci-Fi", "Drama"],
                "anime": ["Shonen", "Slice of Life"]
            },
            is_verified=True,
            created_at="2024-01-15T10:30:00Z",
            stats={
                "tracks_played": 1247,
                "playlists": 12,
                "friends": 43,
                "matches": 28
            }
        )
        
        return profile
    except Exception as e:
        logger.error(f"Error fetching user profile: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/profile/{user_id}", response_model=UserProfile)
async def get_user_profile_by_id(user_id: str):
    """
    Get user profile by ID (public view)
    """
    try:
        # TODO: Fetch from database
        profile = UserProfile(
            id=user_id,
            username=f"user_{user_id}",
            display_name="Sample User",
            bio="Music enthusiast",
            avatar_url=None,
            location="New York, NY",
            age=28,
            interests=["Music", "Concerts"],
            favorite_genres={
                "music": ["Pop", "Electronic"]
            },
            is_verified=False,
            created_at="2024-02-20T15:45:00Z",
            stats={
                "tracks_played": 842,
                "playlists": 8,
                "friends": 35,
                "matches": 18
            }
        )
        
        return profile
    except Exception as e:
        logger.error(f"Error fetching user profile {user_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/profile")
async def update_user_profile(request: UpdateProfileRequest):
    """
    Update current user profile
    """
    try:
        # TODO: Update in database
        return {
            "success": True,
            "message": "Profile updated successfully",
            "data": request.dict(exclude_none=True)
        }
    except Exception as e:
        logger.error(f"Error updating profile: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# PREFERENCES ENDPOINTS
# ============================================================================

@router.get("/preferences", response_model=UserPreferences)
async def get_user_preferences():
    """
    Get user content preferences
    """
    try:
        prefs = UserPreferences(
            music_genres=["Rock", "Indie", "Alternative", "Electronic"],
            movie_genres=["Sci-Fi", "Drama", "Thriller"],
            anime_genres=["Shonen", "Seinen", "Slice of Life"],
            favorite_artists=["Arctic Monkeys", "Tame Impala", "The Strokes"],
            favorite_movies=["Inception", "Interstellar", "The Matrix"],
            favorite_anime=["Attack on Titan", "Steins;Gate", "Cowboy Bebop"]
        )
        
        return prefs
    except Exception as e:
        logger.error(f"Error fetching preferences: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/preferences")
async def update_user_preferences(request: UserPreferences):
    """
    Update user content preferences
    """
    try:
        # TODO: Update in database
        return {
            "success": True,
            "message": "Preferences updated successfully",
            "data": request.dict()
        }
    except Exception as e:
        logger.error(f"Error updating preferences: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# MATCHING ENDPOINTS
# ============================================================================

@router.get("/matching/preferences", response_model=MatchingPreferences)
async def get_matching_preferences():
    """
    Get user matching preferences
    """
    try:
        prefs = MatchingPreferences(
            age_range={"min": 21, "max": 35},
            distance_range=50,
            gender_preference="all",
            looking_for=["friends", "music_buddies", "concert_partners"],
            match_by_music=True,
            match_by_movies=True,
            match_by_anime=True,
            min_compatibility=75
        )
        
        return prefs
    except Exception as e:
        logger.error(f"Error fetching matching preferences: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/matching/preferences")
async def update_matching_preferences(request: MatchingPreferences):
    """
    Update user matching preferences
    """
    try:
        # TODO: Update in database
        return {
            "success": True,
            "message": "Matching preferences updated successfully",
            "data": request.dict()
        }
    except Exception as e:
        logger.error(f"Error updating matching preferences: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# SETTINGS ENDPOINTS
# ============================================================================

@router.get("/settings/privacy", response_model=PrivacySettings)
async def get_privacy_settings():
    """
    Get user privacy settings
    """
    try:
        settings = PrivacySettings(
            profile_visibility="public",
            show_age=True,
            show_location=True,
            show_last_seen=True,
            allow_messages_from="friends",
            show_listening_activity=True
        )
        
        return settings
    except Exception as e:
        logger.error(f"Error fetching privacy settings: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/settings/privacy")
async def update_privacy_settings(request: PrivacySettings):
    """
    Update user privacy settings
    """
    try:
        # TODO: Update in database
        return {
            "success": True,
            "message": "Privacy settings updated successfully",
            "data": request.dict()
        }
    except Exception as e:
        logger.error(f"Error updating privacy settings: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/settings/notifications", response_model=NotificationSettings)
async def get_notification_settings():
    """
    Get user notification settings
    """
    try:
        settings = NotificationSettings(
            push_enabled=True,
            email_enabled=True,
            new_matches=True,
            new_messages=True,
            friend_requests=True,
            recommendations=True,
            trending_updates=False
        )
        
        return settings
    except Exception as e:
        logger.error(f"Error fetching notification settings: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/settings/notifications")
async def update_notification_settings(request: NotificationSettings):
    """
    Update user notification settings
    """
    try:
        # TODO: Update in database
        return {
            "success": True,
            "message": "Notification settings updated successfully",
            "data": request.dict()
        }
    except Exception as e:
        logger.error(f"Error updating notification settings: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/settings/app", response_model=AppSettings)
async def get_app_settings():
    """
    Get app settings
    """
    try:
        settings = AppSettings(
            theme="dark",
            language="en",
            auto_play=True,
            data_saver=False,
            download_quality="high"
        )
        
        return settings
    except Exception as e:
        logger.error(f"Error fetching app settings: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/settings/app")
async def update_app_settings(request: AppSettings):
    """
    Update app settings
    """
    try:
        # TODO: Update in database
        return {
            "success": True,
            "message": "App settings updated successfully",
            "data": request.dict()
        }
    except Exception as e:
        logger.error(f"Error updating app settings: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# USER STATS & ACTIVITY
# ============================================================================

@router.get("/stats")
async def get_user_stats():
    """
    Get user statistics and listening activity
    """
    try:
        stats = {
            "total_listening_time": 12480,  # minutes
            "tracks_played": 1247,
            "favorite_genre": "Indie Rock",
            "top_artists": [
                {"name": "Arctic Monkeys", "plays": 342},
                {"name": "Tame Impala", "plays": 287},
                {"name": "The Strokes", "plays": 245}
            ],
            "top_tracks": [
                {"name": "Do I Wanna Know?", "artist": "Arctic Monkeys", "plays": 87},
                {"name": "The Less I Know The Better", "artist": "Tame Impala", "plays": 76},
                {"name": "Reptilia", "artist": "The Strokes", "plays": 65}
            ],
            "listening_history": [
                {"date": "2024-10-12", "minutes": 145},
                {"date": "2024-10-11", "minutes": 198},
                {"date": "2024-10-10", "minutes": 167}
            ],
            "playlists_created": 12,
            "friends": 43,
            "matches": 28
        }
        
        return {
            "success": True,
            "message": "Stats fetched successfully",
            "data": stats
        }
    except Exception as e:
        logger.error(f"Error fetching user stats: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/activity/recent")
async def get_recent_activity(limit: int = Query(20, ge=1, le=100)):
    """
    Get user's recent activity
    """
    try:
        activities = [
            {
                "id": "act_1",
                "type": "track_play",
                "title": "Played 'Do I Wanna Know?'",
                "artist": "Arctic Monkeys",
                "timestamp": "2024-10-12T09:45:00Z"
            },
            {
                "id": "act_2",
                "type": "new_match",
                "title": "New match with MusicFan42",
                "compatibility": 87,
                "timestamp": "2024-10-12T08:30:00Z"
            },
            {
                "id": "act_3",
                "type": "playlist_created",
                "title": "Created playlist 'Indie Vibes'",
                "tracks_count": 24,
                "timestamp": "2024-10-11T20:15:00Z"
            }
        ]
        
        return {
            "success": True,
            "message": "Recent activity fetched successfully",
            "data": activities[:limit]
        }
    except Exception as e:
        logger.error(f"Error fetching recent activity: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

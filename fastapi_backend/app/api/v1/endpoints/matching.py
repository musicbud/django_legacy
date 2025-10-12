"""
Matching and Buds endpoints
Handles user matching, swipes, matches, and connections
"""
from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from pydantic import BaseModel
from enum import Enum
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/matching", tags=["matching"])

# ============================================================================
# ENUMS & SCHEMAS
# ============================================================================

class SwipeAction(str, Enum):
    """Swipe action types"""
    LIKE = "like"
    PASS = "pass"
    SUPER_LIKE = "super_like"


class MatchStatus(str, Enum):
    """Match status types"""
    PENDING = "pending"
    MATCHED = "matched"
    UNMATCHED = "unmatched"


class BudCard(BaseModel):
    """Bud card schema for swipe interface"""
    id: str
    username: str
    display_name: str
    age: int
    location: str
    bio: Optional[str] = None
    avatar_url: Optional[str] = None
    cover_image_url: Optional[str] = None
    distance: float  # in km
    compatibility_score: int  # 0-100
    common_interests: List[str] = []
    music_compatibility: int = 0
    movie_compatibility: int = 0
    anime_compatibility: int = 0
    top_artists: List[str] = []
    top_genres: List[str] = []
    is_verified: bool = False


class SwipeRequest(BaseModel):
    """Swipe action request"""
    user_id: str
    action: SwipeAction
    

class Match(BaseModel):
    """Match schema"""
    id: str
    user_id: str
    username: str
    display_name: str
    avatar_url: Optional[str] = None
    compatibility_score: int
    matched_at: str
    last_message: Optional[str] = None
    last_message_at: Optional[str] = None
    unread_count: int = 0


class Connection(BaseModel):
    """Connection/friend schema"""
    id: str
    user_id: str
    username: str
    display_name: str
    avatar_url: Optional[str] = None
    bio: Optional[str] = None
    compatibility_score: int
    connected_at: str
    common_interests: List[str] = []
    is_online: bool = False
    last_seen: Optional[str] = None


# ============================================================================
# DISCOVERY & SWIPE ENDPOINTS
# ============================================================================

@router.get("/discover", response_model=List[BudCard])
async def get_potential_matches(limit: int = Query(10, ge=1, le=50)):
    """
    Get potential matches for swiping
    Returns list of user cards based on preferences and compatibility
    """
    try:
        # TODO: Fetch from database based on user preferences
        potential_matches = [
            BudCard(
                id="user_456",
                username="indierocklover",
                display_name="Alex",
                age=26,
                location="San Francisco, CA",
                bio="Indie rock enthusiast, concert junkie, and anime lover 🎸",
                avatar_url=None,
                cover_image_url=None,
                distance=2.5,
                compatibility_score=87,
                common_interests=["Indie Rock", "Concerts", "Anime"],
                music_compatibility=92,
                movie_compatibility=78,
                anime_compatibility=91,
                top_artists=["Arctic Monkeys", "The Strokes", "Tame Impala"],
                top_genres=["Indie", "Rock", "Alternative"],
                is_verified=True
            ),
            BudCard(
                id="user_789",
                username="musicandmovies",
                display_name="Sam",
                age=24,
                location="Oakland, CA",
                bio="Film buff and music producer. Let's vibe! 🎬🎵",
                avatar_url=None,
                distance=8.3,
                compatibility_score=82,
                common_interests=["Electronic Music", "Movies", "Production"],
                music_compatibility=85,
                movie_compatibility=88,
                anime_compatibility=73,
                top_artists=["Daft Punk", "Justice", "Deadmau5"],
                top_genres=["Electronic", "House", "Techno"],
                is_verified=False
            ),
            BudCard(
                id="user_321",
                username="animevibes",
                display_name="Jordan",
                age=27,
                location="Berkeley, CA",
                bio="Anime OST collector, J-Rock fan 🎌",
                avatar_url=None,
                distance=5.7,
                compatibility_score=79,
                common_interests=["Anime", "J-Rock", "Gaming"],
                music_compatibility=81,
                movie_compatibility=75,
                anime_compatibility=95,
                top_artists=["RADWIMPS", "Yoasobi", "Eve"],
                top_genres=["J-Rock", "J-Pop", "Anime OST"],
                is_verified=True
            )
        ]
        
        return potential_matches[:limit]
    except Exception as e:
        logger.error(f"Error fetching potential matches: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/swipe")
async def swipe_user(request: SwipeRequest):
    """
    Swipe on a user (like, pass, or super_like)
    Returns match status if it's a mutual match
    """
    try:
        # TODO: Process swipe and check for mutual match
        is_mutual_match = request.action in [SwipeAction.LIKE, SwipeAction.SUPER_LIKE]
        
        response = {
            "success": True,
            "action": request.action.value,
            "is_match": is_mutual_match,
        }
        
        if is_mutual_match:
            response["match"] = {
                "id": "match_123",
                "user_id": request.user_id,
                "username": "indierocklover",
                "display_name": "Alex",
                "avatar_url": None,
                "compatibility_score": 87,
                "matched_at": "2024-10-12T10:04:00Z",
                "message": "It's a match! Start chatting now! 🎉"
            }
        
        return response
    except Exception as e:
        logger.error(f"Error processing swipe: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# MATCHES ENDPOINTS
# ============================================================================

@router.get("/matches", response_model=List[Match])
async def get_matches(
    status: Optional[MatchStatus] = Query(None),
    limit: int = Query(50, ge=1, le=100)
):
    """
    Get user's matches
    Can filter by status (pending, matched, unmatched)
    """
    try:
        matches = [
            Match(
                id="match_001",
                user_id="user_456",
                username="indierocklover",
                display_name="Alex",
                avatar_url=None,
                compatibility_score=87,
                matched_at="2024-10-12T10:04:00Z",
                last_message="Hey! Love your music taste!",
                last_message_at="2024-10-12T10:15:00Z",
                unread_count=2
            ),
            Match(
                id="match_002",
                user_id="user_789",
                username="musicandmovies",
                display_name="Sam",
                avatar_url=None,
                compatibility_score=82,
                matched_at="2024-10-11T18:30:00Z",
                last_message="That concert was amazing!",
                last_message_at="2024-10-11T20:45:00Z",
                unread_count=0
            ),
            Match(
                id="match_003",
                user_id="user_321",
                username="animevibes",
                display_name="Jordan",
                avatar_url=None,
                compatibility_score=79,
                matched_at="2024-10-10T14:20:00Z",
                last_message=None,
                last_message_at=None,
                unread_count=0
            )
        ]
        
        return matches[:limit]
    except Exception as e:
        logger.error(f"Error fetching matches: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/matches/{match_id}", response_model=Match)
async def get_match_details(match_id: str):
    """
    Get detailed information about a specific match
    """
    try:
        match = Match(
            id=match_id,
            user_id="user_456",
            username="indierocklover",
            display_name="Alex",
            avatar_url=None,
            compatibility_score=87,
            matched_at="2024-10-12T10:04:00Z",
            last_message="Hey! Love your music taste!",
            last_message_at="2024-10-12T10:15:00Z",
            unread_count=2
        )
        
        return match
    except Exception as e:
        logger.error(f"Error fetching match {match_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/matches/{match_id}")
async def unmatch_user(match_id: str):
    """
    Unmatch with a user
    """
    try:
        # TODO: Remove match from database
        return {
            "success": True,
            "message": "Successfully unmatched",
            "match_id": match_id
        }
    except Exception as e:
        logger.error(f"Error unmatching {match_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# CONNECTIONS/FRIENDS ENDPOINTS
# ============================================================================

@router.get("/connections", response_model=List[Connection])
async def get_connections(limit: int = Query(100, ge=1, le=200)):
    """
    Get user's connections/friends
    """
    try:
        connections = [
            Connection(
                id="conn_001",
                user_id="user_456",
                username="indierocklover",
                display_name="Alex",
                avatar_url=None,
                bio="Indie rock enthusiast 🎸",
                compatibility_score=87,
                connected_at="2024-09-15T12:00:00Z",
                common_interests=["Indie Rock", "Concerts", "Anime"],
                is_online=True,
                last_seen=None
            ),
            Connection(
                id="conn_002",
                user_id="user_789",
                username="musicandmovies",
                display_name="Sam",
                avatar_url=None,
                bio="Film buff and music producer 🎬",
                compatibility_score=82,
                connected_at="2024-08-22T09:30:00Z",
                common_interests=["Electronic Music", "Movies"],
                is_online=False,
                last_seen="2024-10-12T08:45:00Z"
            ),
            Connection(
                id="conn_003",
                user_id="user_321",
                username="animevibes",
                display_name="Jordan",
                avatar_url=None,
                bio="Anime OST collector 🎌",
                compatibility_score=79,
                connected_at="2024-07-10T15:20:00Z",
                common_interests=["Anime", "J-Rock", "Gaming"],
                is_online=True,
                last_seen=None
            )
        ]
        
        return connections[:limit]
    except Exception as e:
        logger.error(f"Error fetching connections: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/connections/{user_id}")
async def add_connection(user_id: str):
    """
    Add a user as a connection/friend
    """
    try:
        # TODO: Add connection to database
        return {
            "success": True,
            "message": "Connection added successfully",
            "user_id": user_id
        }
    except Exception as e:
        logger.error(f"Error adding connection {user_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/connections/{user_id}")
async def remove_connection(user_id: str):
    """
    Remove a connection/friend
    """
    try:
        # TODO: Remove connection from database
        return {
            "success": True,
            "message": "Connection removed successfully",
            "user_id": user_id
        }
    except Exception as e:
        logger.error(f"Error removing connection {user_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# COMPATIBILITY ENDPOINTS
# ============================================================================

@router.get("/compatibility/{user_id}")
async def get_compatibility_details(user_id: str):
    """
    Get detailed compatibility breakdown with a specific user
    """
    try:
        compatibility = {
            "overall_score": 87,
            "music_compatibility": {
                "score": 92,
                "common_genres": ["Indie", "Rock", "Alternative"],
                "common_artists": ["Arctic Monkeys", "The Strokes", "Tame Impala"],
                "shared_top_tracks": 12
            },
            "movie_compatibility": {
                "score": 78,
                "common_genres": ["Sci-Fi", "Drama"],
                "common_movies": ["Inception", "Interstellar"],
                "shared_watchlist": 8
            },
            "anime_compatibility": {
                "score": 91,
                "common_genres": ["Shonen", "Seinen"],
                "common_anime": ["Attack on Titan", "Steins;Gate"],
                "shared_watchlist": 15
            },
            "personality_match": {
                "score": 85,
                "matching_traits": ["Creative", "Outgoing", "Passionate"]
            }
        }
        
        return {
            "success": True,
            "user_id": user_id,
            "data": compatibility
        }
    except Exception as e:
        logger.error(f"Error fetching compatibility for {user_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# STATISTICS ENDPOINTS
# ============================================================================

@router.get("/stats")
async def get_matching_stats():
    """
    Get user's matching statistics
    """
    try:
        stats = {
            "total_swipes": 142,
            "likes_sent": 87,
            "likes_received": 93,
            "super_likes_sent": 12,
            "super_likes_received": 8,
            "total_matches": 28,
            "active_matches": 18,
            "total_connections": 43,
            "average_compatibility": 79,
            "match_rate": 32.0,  # percentage
            "response_rate": 85.0  # percentage
        }
        
        return {
            "success": True,
            "message": "Matching stats fetched successfully",
            "data": stats
        }
    except Exception as e:
        logger.error(f"Error fetching matching stats: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

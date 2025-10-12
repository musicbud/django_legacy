"""
Chat and Messaging endpoints
Handles conversations, messages, and real-time chat functionality
"""
from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from pydantic import BaseModel
from enum import Enum
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/chat", tags=["chat"])

# ============================================================================
# ENUMS & SCHEMAS
# ============================================================================

class MessageType(str, Enum):
    """Message types"""
    TEXT = "text"
    IMAGE = "image"
    AUDIO = "audio"
    VIDEO = "video"
    TRACK_SHARE = "track_share"
    PLAYLIST_SHARE = "playlist_share"
    MOVIE_SHARE = "movie_share"
    ANIME_SHARE = "anime_share"


class ConversationStatus(str, Enum):
    """Conversation status"""
    ACTIVE = "active"
    ARCHIVED = "archived"
    MUTED = "muted"
    BLOCKED = "blocked"


class Message(BaseModel):
    """Message schema"""
    id: str
    conversation_id: str
    sender_id: str
    sender_name: str
    sender_avatar: Optional[str] = None
    message_type: MessageType
    content: str
    metadata: Optional[dict] = None  # For shared content
    timestamp: str
    is_read: bool = False
    is_delivered: bool = True


class Conversation(BaseModel):
    """Conversation schema"""
    id: str
    user_id: str
    username: str
    display_name: str
    avatar_url: Optional[str] = None
    last_message: Optional[str] = None
    last_message_at: Optional[str] = None
    last_message_type: Optional[MessageType] = None
    unread_count: int = 0
    is_online: bool = False
    status: ConversationStatus = ConversationStatus.ACTIVE
    created_at: str


class SendMessageRequest(BaseModel):
    """Send message request"""
    conversation_id: str
    message_type: MessageType = MessageType.TEXT
    content: str
    metadata: Optional[dict] = None


class CreateConversationRequest(BaseModel):
    """Create conversation request"""
    user_id: str
    initial_message: Optional[str] = None


# ============================================================================
# CONVERSATION ENDPOINTS
# ============================================================================

@router.get("/conversations", response_model=List[Conversation])
async def get_conversations(
    status: Optional[ConversationStatus] = Query(None),
    limit: int = Query(50, ge=1, le=100)
):
    """
    Get user's conversations
    Can filter by status (active, archived, muted)
    """
    try:
        conversations = [
            Conversation(
                id="conv_001",
                user_id="user_456",
                username="indierocklover",
                display_name="Alex",
                avatar_url=None,
                last_message="Hey! Love your music taste!",
                last_message_at="2024-10-12T10:15:00Z",
                last_message_type=MessageType.TEXT,
                unread_count=2,
                is_online=True,
                status=ConversationStatus.ACTIVE,
                created_at="2024-10-12T10:04:00Z"
            ),
            Conversation(
                id="conv_002",
                user_id="user_789",
                username="musicandmovies",
                display_name="Sam",
                avatar_url=None,
                last_message="Check out this track!",
                last_message_at="2024-10-11T20:45:00Z",
                last_message_type=MessageType.TRACK_SHARE,
                unread_count=0,
                is_online=False,
                status=ConversationStatus.ACTIVE,
                created_at="2024-10-11T18:30:00Z"
            ),
            Conversation(
                id="conv_003",
                user_id="user_321",
                username="animevibes",
                display_name="Jordan",
                avatar_url=None,
                last_message="Have you seen this anime?",
                last_message_at="2024-10-10T16:20:00Z",
                last_message_type=MessageType.TEXT,
                unread_count=0,
                is_online=True,
                status=ConversationStatus.ACTIVE,
                created_at="2024-10-10T14:20:00Z"
            )
        ]
        
        # Filter by status if provided
        if status:
            conversations = [c for c in conversations if c.status == status]
        
        return conversations[:limit]
    except Exception as e:
        logger.error(f"Error fetching conversations: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/conversations/{conversation_id}", response_model=Conversation)
async def get_conversation_details(conversation_id: str):
    """
    Get detailed information about a specific conversation
    """
    try:
        conversation = Conversation(
            id=conversation_id,
            user_id="user_456",
            username="indierocklover",
            display_name="Alex",
            avatar_url=None,
            last_message="Hey! Love your music taste!",
            last_message_at="2024-10-12T10:15:00Z",
            last_message_type=MessageType.TEXT,
            unread_count=2,
            is_online=True,
            status=ConversationStatus.ACTIVE,
            created_at="2024-10-12T10:04:00Z"
        )
        
        return conversation
    except Exception as e:
        logger.error(f"Error fetching conversation {conversation_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/conversations")
async def create_conversation(request: CreateConversationRequest):
    """
    Create a new conversation with a user
    """
    try:
        conversation = Conversation(
            id="conv_new",
            user_id=request.user_id,
            username="newuser",
            display_name="New User",
            avatar_url=None,
            last_message=request.initial_message,
            last_message_at="2024-10-12T10:30:00Z" if request.initial_message else None,
            last_message_type=MessageType.TEXT if request.initial_message else None,
            unread_count=0,
            is_online=False,
            status=ConversationStatus.ACTIVE,
            created_at="2024-10-12T10:30:00Z"
        )
        
        return {
            "success": True,
            "message": "Conversation created successfully",
            "data": conversation.dict()
        }
    except Exception as e:
        logger.error(f"Error creating conversation: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/conversations/{conversation_id}/status")
async def update_conversation_status(
    conversation_id: str,
    status: ConversationStatus
):
    """
    Update conversation status (archive, mute, block)
    """
    try:
        return {
            "success": True,
            "message": f"Conversation status updated to {status.value}",
            "conversation_id": conversation_id,
            "status": status.value
        }
    except Exception as e:
        logger.error(f"Error updating conversation status: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/conversations/{conversation_id}")
async def delete_conversation(conversation_id: str):
    """
    Delete a conversation
    """
    try:
        return {
            "success": True,
            "message": "Conversation deleted successfully",
            "conversation_id": conversation_id
        }
    except Exception as e:
        logger.error(f"Error deleting conversation: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# MESSAGE ENDPOINTS
# ============================================================================

@router.get("/conversations/{conversation_id}/messages", response_model=List[Message])
async def get_messages(
    conversation_id: str,
    before: Optional[str] = Query(None, description="Get messages before this message ID"),
    limit: int = Query(50, ge=1, le=100)
):
    """
    Get messages from a conversation
    Supports pagination with 'before' parameter
    """
    try:
        messages = [
            Message(
                id="msg_001",
                conversation_id=conversation_id,
                sender_id="user_456",
                sender_name="Alex",
                sender_avatar=None,
                message_type=MessageType.TEXT,
                content="Hey! Love your music taste!",
                timestamp="2024-10-12T10:15:00Z",
                is_read=True,
                is_delivered=True
            ),
            Message(
                id="msg_002",
                conversation_id=conversation_id,
                sender_id="user_123",
                sender_name="Music Lover",
                sender_avatar=None,
                message_type=MessageType.TEXT,
                content="Thanks! Your profile is amazing too!",
                timestamp="2024-10-12T10:16:30Z",
                is_read=True,
                is_delivered=True
            ),
            Message(
                id="msg_003",
                conversation_id=conversation_id,
                sender_id="user_456",
                sender_name="Alex",
                sender_avatar=None,
                message_type=MessageType.TRACK_SHARE,
                content="Check out this track!",
                metadata={
                    "track_id": "track_123",
                    "track_name": "Do I Wanna Know?",
                    "artist": "Arctic Monkeys",
                    "album": "AM",
                    "cover_url": None
                },
                timestamp="2024-10-12T10:18:00Z",
                is_read=True,
                is_delivered=True
            ),
            Message(
                id="msg_004",
                conversation_id=conversation_id,
                sender_id="user_123",
                sender_name="Music Lover",
                sender_avatar=None,
                message_type=MessageType.TEXT,
                content="Love this song! Arctic Monkeys are the best 🎸",
                timestamp="2024-10-12T10:20:15Z",
                is_read=False,
                is_delivered=True
            )
        ]
        
        return messages[:limit]
    except Exception as e:
        logger.error(f"Error fetching messages: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/messages")
async def send_message(request: SendMessageRequest):
    """
    Send a message in a conversation
    """
    try:
        message = Message(
            id="msg_new",
            conversation_id=request.conversation_id,
            sender_id="user_123",
            sender_name="Music Lover",
            sender_avatar=None,
            message_type=request.message_type,
            content=request.content,
            metadata=request.metadata,
            timestamp="2024-10-12T10:30:00Z",
            is_read=False,
            is_delivered=True
        )
        
        return {
            "success": True,
            "message": "Message sent successfully",
            "data": message.dict()
        }
    except Exception as e:
        logger.error(f"Error sending message: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/messages/{message_id}/read")
async def mark_message_read(message_id: str):
    """
    Mark a message as read
    """
    try:
        return {
            "success": True,
            "message": "Message marked as read",
            "message_id": message_id
        }
    except Exception as e:
        logger.error(f"Error marking message as read: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/conversations/{conversation_id}/read-all")
async def mark_all_messages_read(conversation_id: str):
    """
    Mark all messages in a conversation as read
    """
    try:
        return {
            "success": True,
            "message": "All messages marked as read",
            "conversation_id": conversation_id
        }
    except Exception as e:
        logger.error(f"Error marking all messages as read: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/messages/{message_id}")
async def delete_message(message_id: str):
    """
    Delete a message
    """
    try:
        return {
            "success": True,
            "message": "Message deleted successfully",
            "message_id": message_id
        }
    except Exception as e:
        logger.error(f"Error deleting message: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# TYPING & PRESENCE ENDPOINTS
# ============================================================================

@router.post("/conversations/{conversation_id}/typing")
async def send_typing_indicator(conversation_id: str, is_typing: bool = True):
    """
    Send typing indicator to conversation
    """
    try:
        return {
            "success": True,
            "message": f"Typing indicator {'started' if is_typing else 'stopped'}",
            "conversation_id": conversation_id,
            "is_typing": is_typing
        }
    except Exception as e:
        logger.error(f"Error sending typing indicator: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# SHARE CONTENT ENDPOINTS
# ============================================================================

@router.post("/share/track")
async def share_track(
    conversation_id: str,
    track_id: str,
    message: Optional[str] = None
):
    """
    Share a music track in a conversation
    """
    try:
        share_message = Message(
            id="msg_share_track",
            conversation_id=conversation_id,
            sender_id="user_123",
            sender_name="Music Lover",
            sender_avatar=None,
            message_type=MessageType.TRACK_SHARE,
            content=message or "Check out this track!",
            metadata={
                "track_id": track_id,
                "track_name": "Sample Track",
                "artist": "Sample Artist",
                "album": "Sample Album",
                "cover_url": None
            },
            timestamp="2024-10-12T10:30:00Z",
            is_read=False,
            is_delivered=True
        )
        
        return {
            "success": True,
            "message": "Track shared successfully",
            "data": share_message.dict()
        }
    except Exception as e:
        logger.error(f"Error sharing track: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/share/playlist")
async def share_playlist(
    conversation_id: str,
    playlist_id: str,
    message: Optional[str] = None
):
    """
    Share a playlist in a conversation
    """
    try:
        share_message = Message(
            id="msg_share_playlist",
            conversation_id=conversation_id,
            sender_id="user_123",
            sender_name="Music Lover",
            sender_avatar=None,
            message_type=MessageType.PLAYLIST_SHARE,
            content=message or "Check out this playlist!",
            metadata={
                "playlist_id": playlist_id,
                "playlist_name": "Sample Playlist",
                "tracks_count": 24,
                "cover_url": None
            },
            timestamp="2024-10-12T10:30:00Z",
            is_read=False,
            is_delivered=True
        )
        
        return {
            "success": True,
            "message": "Playlist shared successfully",
            "data": share_message.dict()
        }
    except Exception as e:
        logger.error(f"Error sharing playlist: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/share/movie")
async def share_movie(
    conversation_id: str,
    movie_id: str,
    message: Optional[str] = None
):
    """
    Share a movie in a conversation
    """
    try:
        share_message = Message(
            id="msg_share_movie",
            conversation_id=conversation_id,
            sender_id="user_123",
            sender_name="Music Lover",
            sender_avatar=None,
            message_type=MessageType.MOVIE_SHARE,
            content=message or "Have you seen this?",
            metadata={
                "movie_id": movie_id,
                "movie_title": "Sample Movie",
                "year": 2024,
                "rating": 8.5,
                "poster_url": None
            },
            timestamp="2024-10-12T10:30:00Z",
            is_read=False,
            is_delivered=True
        )
        
        return {
            "success": True,
            "message": "Movie shared successfully",
            "data": share_message.dict()
        }
    except Exception as e:
        logger.error(f"Error sharing movie: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/share/anime")
async def share_anime(
    conversation_id: str,
    anime_id: str,
    message: Optional[str] = None
):
    """
    Share an anime in a conversation
    """
    try:
        share_message = Message(
            id="msg_share_anime",
            conversation_id=conversation_id,
            sender_id="user_123",
            sender_name="Music Lover",
            sender_avatar=None,
            message_type=MessageType.ANIME_SHARE,
            content=message or "You should watch this!",
            metadata={
                "anime_id": anime_id,
                "anime_title": "Sample Anime",
                "episodes": 24,
                "rating": 9.0,
                "cover_url": None
            },
            timestamp="2024-10-12T10:30:00Z",
            is_read=False,
            is_delivered=True
        )
        
        return {
            "success": True,
            "message": "Anime shared successfully",
            "data": share_message.dict()
        }
    except Exception as e:
        logger.error(f"Error sharing anime: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# STATISTICS ENDPOINTS
# ============================================================================

@router.get("/stats")
async def get_chat_stats():
    """
    Get user's chat statistics
    """
    try:
        stats = {
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
        
        return {
            "success": True,
            "message": "Chat stats fetched successfully",
            "data": stats
        }
    except Exception as e:
        logger.error(f"Error fetching chat stats: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

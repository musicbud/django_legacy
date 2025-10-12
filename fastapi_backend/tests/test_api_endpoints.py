"""
Comprehensive API endpoint tests for MusicBud FastAPI backend
Tests all endpoints: public, users, matching, and chat
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# ============================================================================
# PUBLIC ENDPOINTS TESTS
# ============================================================================

class TestPublicEndpoints:
    """Test public/guest endpoints - no authentication required"""
    
    def test_root_endpoint(self):
        """Test root endpoint returns correct info"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "version" in data
        assert "docs" in data
        assert data["message"] == "MusicBud API - FastAPI Version"
    
    def test_health_check(self):
        """Test health check endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
    
    def test_public_discover(self):
        """Test public discover endpoint"""
        response = client.get("/v1/discover/public/")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "data" in data
        assert "trending_tracks" in data["data"]
        assert "popular_artists" in data["data"]
        assert "genres" in data["data"]
    
    def test_public_trending_all(self):
        """Test trending endpoint with type=all"""
        response = client.get("/v1/discover/public/trending/?type=all")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "tracks" in data["data"]
        assert "artists" in data["data"]
    
    def test_public_trending_tracks(self):
        """Test trending endpoint with type=tracks"""
        response = client.get("/v1/discover/public/trending/?type=tracks")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "tracks" in data["data"]
        assert len(data["data"]["tracks"]) > 0
    
    def test_public_trending_artists(self):
        """Test trending endpoint with type=artists"""
        response = client.get("/v1/discover/public/trending/?type=artists")
        assert response.status_code == 200
        data = response.json()
        assert "artists" in data["data"]
    
    def test_public_genres(self):
        """Test genres endpoint"""
        response = client.get("/v1/discover/public/genres/")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "music" in data["data"]
        assert "movies" in data["data"]
        assert "anime" in data["data"]
        # Check genre structure
        assert len(data["data"]["music"]) > 0
        genre = data["data"]["music"][0]
        assert "id" in genre
        assert "name" in genre
        assert "color" in genre
    
    def test_public_recommendations(self):
        """Test public recommendations endpoint"""
        response = client.get("/v1/recommendations/public/")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["is_personalized"] is False
        assert "movies" in data["data"]
        assert "manga" in data["data"]


# ============================================================================
# USER ENDPOINTS TESTS
# ============================================================================

class TestUserEndpoints:
    """Test user profile and settings endpoints"""
    
    def test_get_user_profile(self):
        """Test getting current user profile"""
        response = client.get("/v1/users/profile")
        assert response.status_code == 200
        data = response.json()
        assert "id" in data
        assert "username" in data
        assert "display_name" in data
        assert "stats" in data
        assert data["id"] == "user_123"
    
    def test_get_user_profile_by_id(self):
        """Test getting another user's profile"""
        response = client.get("/v1/users/profile/user_456")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == "user_456"
        assert "username" in data
    
    def test_update_user_profile(self):
        """Test updating user profile"""
        update_data = {
            "display_name": "New Display Name",
            "bio": "Updated bio",
            "location": "New York, NY"
        }
        response = client.put("/v1/users/profile", json=update_data)
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["message"] == "Profile updated successfully"
    
    def test_get_user_preferences(self):
        """Test getting user preferences"""
        response = client.get("/v1/users/preferences")
        assert response.status_code == 200
        data = response.json()
        assert "music_genres" in data
        assert "movie_genres" in data
        assert "anime_genres" in data
        assert isinstance(data["music_genres"], list)
    
    def test_update_user_preferences(self):
        """Test updating user preferences"""
        prefs_data = {
            "music_genres": ["Rock", "Pop"],
            "movie_genres": ["Action", "Sci-Fi"],
            "anime_genres": ["Shonen"]
        }
        response = client.put("/v1/users/preferences", json=prefs_data)
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
    
    def test_get_matching_preferences(self):
        """Test getting matching preferences"""
        response = client.get("/v1/users/matching/preferences")
        assert response.status_code == 200
        data = response.json()
        assert "age_range" in data
        assert "distance_range" in data
        assert "looking_for" in data
        assert "min_compatibility" in data
    
    def test_update_matching_preferences(self):
        """Test updating matching preferences"""
        prefs_data = {
            "age_range": {"min": 25, "max": 40},
            "distance_range": 30,
            "min_compatibility": 80
        }
        response = client.put("/v1/users/matching/preferences", json=prefs_data)
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
    
    def test_get_privacy_settings(self):
        """Test getting privacy settings"""
        response = client.get("/v1/users/settings/privacy")
        assert response.status_code == 200
        data = response.json()
        assert "profile_visibility" in data
        assert "show_age" in data
        assert "allow_messages_from" in data
    
    def test_update_privacy_settings(self):
        """Test updating privacy settings"""
        settings = {
            "profile_visibility": "friends",
            "show_age": False,
            "allow_messages_from": "friends"
        }
        response = client.put("/v1/users/settings/privacy", json=settings)
        assert response.status_code == 200
    
    def test_get_notification_settings(self):
        """Test getting notification settings"""
        response = client.get("/v1/users/settings/notifications")
        assert response.status_code == 200
        data = response.json()
        assert "push_enabled" in data
        assert "new_matches" in data
        assert "new_messages" in data
    
    def test_update_notification_settings(self):
        """Test updating notification settings"""
        settings = {
            "push_enabled": True,
            "new_matches": True,
            "new_messages": False
        }
        response = client.put("/v1/users/settings/notifications", json=settings)
        assert response.status_code == 200
    
    def test_get_app_settings(self):
        """Test getting app settings"""
        response = client.get("/v1/users/settings/app")
        assert response.status_code == 200
        data = response.json()
        assert "theme" in data
        assert "language" in data
        assert "auto_play" in data
    
    def test_update_app_settings(self):
        """Test updating app settings"""
        settings = {
            "theme": "light",
            "language": "es",
            "auto_play": False
        }
        response = client.put("/v1/users/settings/app", json=settings)
        assert response.status_code == 200
    
    def test_get_user_stats(self):
        """Test getting user statistics"""
        response = client.get("/v1/users/stats")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "total_listening_time" in data["data"]
        assert "top_artists" in data["data"]
        assert "top_tracks" in data["data"]
    
    def test_get_recent_activity(self):
        """Test getting recent activity"""
        response = client.get("/v1/users/activity/recent?limit=10")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert isinstance(data["data"], list)
        assert len(data["data"]) <= 10


# ============================================================================
# MATCHING ENDPOINTS TESTS
# ============================================================================

class TestMatchingEndpoints:
    """Test matching and buds endpoints"""
    
    def test_get_potential_matches(self):
        """Test getting potential matches for swiping"""
        response = client.get("/v1/matching/discover?limit=5")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) <= 5
        if len(data) > 0:
            match = data[0]
            assert "id" in match
            assert "username" in match
            assert "compatibility_score" in match
            assert "distance" in match
    
    def test_swipe_like(self):
        """Test swiping like on a user"""
        swipe_data = {
            "user_id": "user_456",
            "action": "like"
        }
        response = client.post("/v1/matching/swipe", json=swipe_data)
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["action"] == "like"
        assert "is_match" in data
    
    def test_swipe_pass(self):
        """Test swiping pass on a user"""
        swipe_data = {
            "user_id": "user_789",
            "action": "pass"
        }
        response = client.post("/v1/matching/swipe", json=swipe_data)
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["action"] == "pass"
    
    def test_swipe_super_like(self):
        """Test super liking a user"""
        swipe_data = {
            "user_id": "user_321",
            "action": "super_like"
        }
        response = client.post("/v1/matching/swipe", json=swipe_data)
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
    
    def test_get_matches(self):
        """Test getting user's matches"""
        response = client.get("/v1/matching/matches?limit=10")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        if len(data) > 0:
            match = data[0]
            assert "id" in match
            assert "user_id" in match
            assert "compatibility_score" in match
            assert "matched_at" in match
    
    def test_get_match_details(self):
        """Test getting specific match details"""
        response = client.get("/v1/matching/matches/match_001")
        assert response.status_code == 200
        data = response.json()
        assert "id" in data
        assert "compatibility_score" in data
    
    def test_unmatch_user(self):
        """Test unmatching a user"""
        response = client.delete("/v1/matching/matches/match_999")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["message"] == "Successfully unmatched"
    
    def test_get_connections(self):
        """Test getting connections/friends"""
        response = client.get("/v1/matching/connections?limit=20")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        if len(data) > 0:
            conn = data[0]
            assert "id" in conn
            assert "user_id" in conn
            assert "is_online" in conn
    
    def test_add_connection(self):
        """Test adding a connection"""
        response = client.post("/v1/matching/connections/user_999")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["message"] == "Connection added successfully"
    
    def test_remove_connection(self):
        """Test removing a connection"""
        response = client.delete("/v1/matching/connections/user_999")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
    
    def test_get_compatibility(self):
        """Test getting compatibility details"""
        response = client.get("/v1/matching/compatibility/user_456")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "overall_score" in data["data"]
        assert "music_compatibility" in data["data"]
        assert "movie_compatibility" in data["data"]
    
    def test_get_matching_stats(self):
        """Test getting matching statistics"""
        response = client.get("/v1/matching/stats")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "total_swipes" in data["data"]
        assert "total_matches" in data["data"]
        assert "match_rate" in data["data"]


# ============================================================================
# CHAT ENDPOINTS TESTS
# ============================================================================

class TestChatEndpoints:
    """Test chat and messaging endpoints"""
    
    def test_get_conversations(self):
        """Test getting user conversations"""
        response = client.get("/v1/chat/conversations?limit=10")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        if len(data) > 0:
            conv = data[0]
            assert "id" in conv
            assert "user_id" in conv
            assert "display_name" in conv
            assert "status" in conv
    
    def test_get_conversations_filtered(self):
        """Test getting filtered conversations"""
        response = client.get("/v1/chat/conversations?status=active&limit=5")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
    
    def test_get_conversation_details(self):
        """Test getting specific conversation details"""
        response = client.get("/v1/chat/conversations/conv_001")
        assert response.status_code == 200
        data = response.json()
        assert "id" in data
        assert "user_id" in data
    
    def test_create_conversation(self):
        """Test creating a new conversation"""
        conv_data = {
            "user_id": "user_999",
            "initial_message": "Hey! Let's chat!"
        }
        response = client.post("/v1/chat/conversations", json=conv_data)
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "data" in data
    
    def test_update_conversation_status(self):
        """Test updating conversation status"""
        response = client.put(
            "/v1/chat/conversations/conv_001/status?status=archived"
        )
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
    
    def test_delete_conversation(self):
        """Test deleting a conversation"""
        response = client.delete("/v1/chat/conversations/conv_999")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
    
    def test_get_messages(self):
        """Test getting messages from conversation"""
        response = client.get("/v1/chat/conversations/conv_001/messages?limit=20")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        if len(data) > 0:
            msg = data[0]
            assert "id" in msg
            assert "sender_id" in msg
            assert "content" in msg
            assert "message_type" in msg
            assert "timestamp" in msg
    
    def test_send_text_message(self):
        """Test sending a text message"""
        msg_data = {
            "conversation_id": "conv_001",
            "message_type": "text",
            "content": "Hello! This is a test message."
        }
        response = client.post("/v1/chat/messages", json=msg_data)
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["message"] == "Message sent successfully"
    
    def test_mark_message_read(self):
        """Test marking a message as read"""
        response = client.put("/v1/chat/messages/msg_001/read")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
    
    def test_mark_all_messages_read(self):
        """Test marking all messages as read"""
        response = client.put("/v1/chat/conversations/conv_001/read-all")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
    
    def test_delete_message(self):
        """Test deleting a message"""
        response = client.delete("/v1/chat/messages/msg_999")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
    
    def test_send_typing_indicator(self):
        """Test sending typing indicator"""
        response = client.post(
            "/v1/chat/conversations/conv_001/typing?is_typing=true"
        )
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["is_typing"] is True
    
    def test_share_track(self):
        """Test sharing a music track"""
        response = client.post(
            "/v1/chat/share/track",
            params={
                "conversation_id": "conv_001",
                "track_id": "track_123",
                "message": "Check this out!"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["message"] == "Track shared successfully"
    
    def test_share_playlist(self):
        """Test sharing a playlist"""
        response = client.post(
            "/v1/chat/share/playlist",
            params={
                "conversation_id": "conv_001",
                "playlist_id": "playlist_123"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
    
    def test_share_movie(self):
        """Test sharing a movie"""
        response = client.post(
            "/v1/chat/share/movie",
            params={
                "conversation_id": "conv_001",
                "movie_id": "movie_123"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
    
    def test_share_anime(self):
        """Test sharing an anime"""
        response = client.post(
            "/v1/chat/share/anime",
            params={
                "conversation_id": "conv_001",
                "anime_id": "anime_123"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
    
    def test_get_chat_stats(self):
        """Test getting chat statistics"""
        response = client.get("/v1/chat/stats")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "total_conversations" in data["data"]
        assert "total_messages_sent" in data["data"]
        assert "unread_messages" in data["data"]


# ============================================================================
# ERROR HANDLING TESTS
# ============================================================================

class TestErrorHandling:
    """Test error handling and edge cases"""
    
    def test_invalid_endpoint(self):
        """Test accessing non-existent endpoint"""
        response = client.get("/v1/invalid/endpoint")
        assert response.status_code == 404
    
    def test_invalid_trending_type(self):
        """Test invalid trending type parameter"""
        response = client.get("/v1/discover/public/trending/?type=invalid")
        assert response.status_code == 422  # Validation error
    
    def test_invalid_swipe_action(self):
        """Test invalid swipe action"""
        swipe_data = {
            "user_id": "user_456",
            "action": "invalid_action"
        }
        response = client.post("/v1/matching/swipe", json=swipe_data)
        assert response.status_code == 422  # Validation error
    
    def test_missing_required_field(self):
        """Test missing required field in request"""
        incomplete_data = {
            "conversation_id": "conv_001"
            # Missing 'content' field
        }
        response = client.post("/v1/chat/messages", json=incomplete_data)
        assert response.status_code == 422


# ============================================================================
# PAGINATION TESTS
# ============================================================================

class TestPagination:
    """Test pagination functionality"""
    
    def test_matches_pagination_limit(self):
        """Test matches endpoint respects limit parameter"""
        response = client.get("/v1/matching/matches?limit=5")
        assert response.status_code == 200
        data = response.json()
        assert len(data) <= 5
    
    def test_connections_pagination(self):
        """Test connections endpoint pagination"""
        response = client.get("/v1/matching/connections?limit=10")
        assert response.status_code == 200
        data = response.json()
        assert len(data) <= 10
    
    def test_messages_pagination(self):
        """Test messages endpoint pagination"""
        response = client.get(
            "/v1/chat/conversations/conv_001/messages?limit=15"
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data) <= 15
    
    def test_activity_pagination(self):
        """Test activity endpoint pagination"""
        response = client.get("/v1/users/activity/recent?limit=5")
        assert response.status_code == 200
        data = response.json()
        assert len(data["data"]) <= 5


# ============================================================================
# RUN ALL TESTS
# ============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])

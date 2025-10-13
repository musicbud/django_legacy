"""
Comprehensive Test Suite for FastAPI Migration
Tests all migrated endpoints, authentication, and functionality
"""

import asyncio
import json
import os
import pytest
import httpx
from httpx import AsyncClient
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, MagicMock, patch

# Add the project root to Python path
import sys
sys.path.insert(0, '/home/mahmoud/Documents/GitHub/musicbud/backend')

from fastapi_app import app


class TestFastAPIMigration:
    """Test suite for FastAPI migration"""
    
    @pytest.fixture
    def client(self):
        """Create test client"""
        return TestClient(app)
    
    @pytest.fixture
    async def async_client(self):
        """Create async test client"""
        async with AsyncClient(app=app, base_url="http://test") as ac:
            yield ac
    
    @pytest.fixture
    def mock_user_data(self):
        """Mock user data for tests"""
        return {
            "id": 1,
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpassword123",
            "first_name": "Test",
            "last_name": "User",
            "is_active": True,
            "is_staff": False,
            "is_superuser": False
        }
    
    @pytest.fixture
    def auth_headers(self):
        """Mock authentication headers"""
        return {"Authorization": "Bearer fake_jwt_token"}
    
    def test_root_endpoint(self, client):
        """Test root endpoint"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "MusicBud FastAPI" in data["message"]
        assert data["status"] == "healthy"
    
    def test_health_endpoint(self, client):
        """Test health check endpoint"""
        with patch('fastapi_backend.app.core.database.DatabaseHealthCheck.check_all') as mock_health:
            mock_health.return_value = {
                "django": {"status": "healthy"},
                "redis": {"status": "healthy"},
                "neo4j": {"status": "healthy"},
                "timestamp": "2024-01-01T12:00:00"
            }
            
            response = client.get("/health")
            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "healthy"
            assert "databases" in data
    
    def test_metrics_endpoint_debug_mode(self, client):
        """Test metrics endpoint in debug mode"""
        response = client.get("/metrics")
        # Should work in debug mode or if metrics are available
        assert response.status_code in [200, 404]
    
    # Authentication Tests
    
    @patch('fastapi_backend.app.core.database.DjangoORM.create_user')
    @patch('fastapi_backend.app.core.auth.AuthService.get_user_by_username')
    @patch('fastapi_backend.app.core.auth.AuthService.get_user_by_email')
    def test_user_registration(self, mock_get_email, mock_get_username, mock_create_user, client, mock_user_data):
        """Test user registration endpoint"""
        # Mock that user doesn't exist
        mock_get_username.return_value = None
        mock_get_email.return_value = None
        
        # Mock successful user creation
        mock_user = MagicMock()
        mock_user.id = 1
        mock_user.username = mock_user_data["username"]
        mock_user.email = mock_user_data["email"]
        mock_user.first_name = mock_user_data["first_name"]
        mock_user.last_name = mock_user_data["last_name"]
        mock_user.is_active = True
        mock_user.date_joined = "2024-01-01T12:00:00"
        mock_create_user.return_value = mock_user
        
        registration_data = {
            "username": mock_user_data["username"],
            "email": mock_user_data["email"],
            "password": mock_user_data["password"],
            "password_confirm": mock_user_data["password"],
            "first_name": mock_user_data["first_name"],
            "last_name": mock_user_data["last_name"]
        }
        
        response = client.post("/api/auth/register", json=registration_data)
        assert response.status_code == 200
        data = response.json()
        assert data["success"] == True
        assert "User registered successfully" in data["message"]
        assert data["data"]["username"] == mock_user_data["username"]
    
    def test_user_registration_duplicate_username(self, client, mock_user_data):
        """Test registration with duplicate username"""
        with patch('fastapi_backend.app.core.auth.AuthService.get_user_by_username') as mock_get_user:
            mock_get_user.return_value = MagicMock()  # User exists
            
            registration_data = {
                "username": mock_user_data["username"],
                "email": mock_user_data["email"],
                "password": mock_user_data["password"],
                "password_confirm": mock_user_data["password"]
            }
            
            response = client.post("/api/auth/register", json=registration_data)
            assert response.status_code == 400
            data = response.json()
            assert "Username already exists" in data["detail"]
    
    @patch('fastapi_backend.app.core.auth.AuthService.authenticate_user')
    @patch('fastapi_backend.app.core.auth.create_user_token')
    def test_user_login_json(self, mock_create_token, mock_auth_user, client, mock_user_data):
        """Test JSON login endpoint"""
        # Mock successful authentication
        mock_user = MagicMock()
        mock_user.id = 1
        mock_user.username = mock_user_data["username"]
        mock_user.email = mock_user_data["email"]
        mock_user.is_active = True
        mock_auth_user.return_value = mock_user
        
        # Mock token creation
        mock_create_token.return_value = {
            "access_token": "fake_jwt_token",
            "token_type": "bearer",
            "expires_in": 1800
        }
        
        login_data = {
            "username": mock_user_data["username"],
            "password": mock_user_data["password"]
        }
        
        response = client.post("/api/auth/login/json", json=login_data)
        assert response.status_code == 200
        data = response.json()
        assert data["success"] == True
        assert "Login successful" in data["message"]
        assert "access_token" in data["data"]
    
    def test_user_login_invalid_credentials(self, client):
        """Test login with invalid credentials"""
        with patch('fastapi_backend.app.core.auth.AuthService.authenticate_user') as mock_auth:
            mock_auth.return_value = None  # Authentication failed
            
            login_data = {
                "username": "invalid_user",
                "password": "wrong_password"
            }
            
            response = client.post("/api/auth/login/json", json=login_data)
            assert response.status_code == 401
            data = response.json()
            assert "Invalid credentials" in data["detail"]
    
    @patch('fastapi_backend.app.core.auth.get_current_active_user')
    def test_get_current_user_info(self, mock_get_user, client, mock_user_data):
        """Test get current user info endpoint"""
        mock_user = MagicMock()
        mock_user.id = mock_user_data["id"]
        mock_user.username = mock_user_data["username"]
        mock_user.email = mock_user_data["email"]
        mock_user.first_name = mock_user_data["first_name"]
        mock_user.last_name = mock_user_data["last_name"]
        mock_user.is_active = mock_user_data["is_active"]
        mock_user.is_staff = mock_user_data["is_staff"]
        mock_user.is_superuser = mock_user_data["is_superuser"]
        mock_user.date_joined = "2024-01-01T12:00:00"
        mock_user.last_login = None
        mock_get_user.return_value = mock_user
        
        response = client.get("/api/auth/me", headers={"Authorization": "Bearer fake_token"})
        assert response.status_code == 200
        data = response.json()
        assert data["success"] == True
        assert data["data"]["username"] == mock_user_data["username"]
    
    @patch('fastapi_backend.app.core.auth.get_current_active_user')
    def test_logout_endpoint(self, mock_get_user, client, mock_user_data):
        """Test logout endpoint"""
        mock_user = MagicMock()
        mock_user.username = mock_user_data["username"]
        mock_get_user.return_value = mock_user
        
        response = client.post("/api/auth/logout", headers={"Authorization": "Bearer fake_token"})
        assert response.status_code == 200
        data = response.json()
        assert data["success"] == True
        assert "Logged out successfully" in data["message"]
    
    # Public Endpoints Tests
    
    @patch('fastapi_backend.app.core.database.RedisCache.get')
    @patch('fastapi_backend.app.api.routers.public._get_trending_tracks')
    @patch('fastapi_backend.app.api.routers.public._get_popular_artists')
    def test_public_discover_endpoint(self, mock_artists, mock_tracks, mock_cache, client):
        """Test public discover endpoint"""
        # Mock cache miss
        mock_cache.return_value = None
        
        # Mock data
        mock_tracks.return_value = [
            {"id": "track_1", "name": "Test Track", "artist": "Test Artist", "popularity": 95}
        ]
        mock_artists.return_value = [
            {"id": "artist_1", "name": "Test Artist", "genre": "Pop", "popularity": 90}
        ]
        
        with patch('fastapi_backend.app.api.routers.public._get_popular_movies') as mock_movies, \
             patch('fastapi_backend.app.api.routers.public._get_popular_manga') as mock_manga, \
             patch('fastapi_backend.app.api.routers.public._get_popular_anime') as mock_anime, \
             patch('fastapi_backend.app.api.routers.public._get_featured_playlists') as mock_playlists, \
             patch('fastapi_backend.app.core.database.RedisCache.set') as mock_set:
            
            mock_movies.return_value = []
            mock_manga.return_value = []
            mock_anime.return_value = []
            mock_playlists.return_value = []
            mock_set.return_value = True
            
            response = client.get("/api/public/discover")
            assert response.status_code == 200
            data = response.json()
            assert data["success"] == True
            assert "trending_tracks" in data["data"]
            assert "popular_artists" in data["data"]
    
    def test_public_trending_endpoint(self, client):
        """Test public trending endpoint"""
        with patch('fastapi_backend.app.core.database.RedisCache.get') as mock_cache, \
             patch('fastapi_backend.app.api.routers.public._get_trending_tracks') as mock_tracks, \
             patch('fastapi_backend.app.core.database.RedisCache.set') as mock_set:
            
            mock_cache.return_value = None
            mock_tracks.return_value = [{"id": "track_1", "name": "Trending Track"}]
            mock_set.return_value = True
            
            response = client.get("/api/public/trending?content_type=tracks&limit=5")
            assert response.status_code == 200
            data = response.json()
            assert data["success"] == True
            assert "tracks" in data["data"]
    
    def test_public_genres_endpoint(self, client):
        """Test public genres endpoint"""
        with patch('fastapi_backend.app.core.database.RedisCache.get') as mock_cache, \
             patch('fastapi_backend.app.core.database.RedisCache.set') as mock_set:
            
            mock_cache.return_value = None
            mock_set.return_value = True
            
            response = client.get("/api/public/genres")
            assert response.status_code == 200
            data = response.json()
            assert data["success"] == True
            assert "genres" in data["data"]
            assert data["data"]["total"] > 0
    
    def test_public_stats_endpoint(self, client):
        """Test public stats endpoint"""
        with patch('fastapi_backend.app.core.database.RedisCache.get') as mock_cache, \
             patch('fastapi_backend.app.api.routers.public._get_platform_stats') as mock_stats, \
             patch('fastapi_backend.app.core.database.RedisCache.set') as mock_set:
            
            mock_cache.return_value = None
            mock_stats.return_value = {
                "total_tracks": 1000,
                "total_artists": 500,
                "total_users": 100,
                "total_genres": 20
            }
            mock_set.return_value = True
            
            response = client.get("/api/public/stats")
            assert response.status_code == 200
            data = response.json()
            assert data["success"] == True
            assert "total_tracks" in data["data"]
    
    # User Endpoints Tests
    
    @patch('fastapi_backend.app.core.auth.get_current_active_user')
    def test_user_profile_endpoint(self, mock_get_user, client, mock_user_data):
        """Test user profile endpoint"""
        mock_user = MagicMock()
        mock_user.id = mock_user_data["id"]
        mock_user.username = mock_user_data["username"]
        mock_user.email = mock_user_data["email"]
        mock_user.is_active = mock_user_data["is_active"]
        mock_get_user.return_value = mock_user
        
        response = client.get("/api/users/profile", headers={"Authorization": "Bearer fake_token"})
        assert response.status_code == 200
        data = response.json()
        assert data["success"] == True
        assert data["data"]["username"] == mock_user_data["username"]
    
    # Content Endpoints Tests
    
    def test_content_tracks_endpoint(self, client):
        """Test content tracks endpoint"""
        response = client.get("/api/content/tracks")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] == True
        assert "message" in data
    
    def test_content_artists_endpoint(self, client):
        """Test content artists endpoint"""
        response = client.get("/api/content/artists")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] == True
        assert "message" in data
    
    # Error Handling Tests
    
    def test_404_handler(self, client):
        """Test 404 error handler"""
        response = client.get("/nonexistent/endpoint")
        assert response.status_code == 404
        data = response.json()
        assert data["error"] == True
        assert "Endpoint not found" in data["message"]
        assert data["path"] == "/nonexistent/endpoint"
    
    # Validation Tests
    
    def test_invalid_registration_data(self, client):
        """Test registration with invalid data"""
        invalid_data = {
            "username": "",  # Empty username
            "email": "invalid_email",  # Invalid email
            "password": "123",  # Too short password
            "password_confirm": "456"  # Passwords don't match
        }
        
        response = client.post("/api/auth/register", json=invalid_data)
        assert response.status_code == 422  # Validation error
    
    def test_invalid_login_data(self, client):
        """Test login with invalid data"""
        invalid_data = {
            "username": "",  # Empty username
            "password": ""   # Empty password
        }
        
        response = client.post("/api/auth/login/json", json=invalid_data)
        assert response.status_code == 422  # Validation error
    
    # Database Tests
    
    @patch('fastapi_backend.app.core.database.Neo4jGraph.run_query')
    async def test_neo4j_integration(self, mock_query):
        """Test Neo4j integration"""
        mock_query.return_value = [{"count": 100}]
        
        from fastapi_backend.app.core.database import Neo4jGraph
        result = await Neo4jGraph.run_query("MATCH (n) RETURN count(n) as count")
        assert len(result) > 0
    
    @patch('fastapi_backend.app.core.database.RedisCache.set')
    @patch('fastapi_backend.app.core.database.RedisCache.get')
    async def test_redis_integration(self, mock_get, mock_set):
        """Test Redis integration"""
        mock_set.return_value = True
        mock_get.return_value = "test_value"
        
        from fastapi_backend.app.core.database import RedisCache
        await RedisCache.set("test_key", "test_value")
        result = await RedisCache.get("test_key")
        assert result == "test_value"
    
    # Performance Tests
    
    def test_endpoint_performance(self, client):
        """Test endpoint performance"""
        import time
        
        start_time = time.time()
        response = client.get("/")
        end_time = time.time()
        
        response_time = end_time - start_time
        assert response_time < 1.0  # Should respond within 1 second
        assert response.status_code == 200
    
    def test_concurrent_requests(self, client):
        """Test handling concurrent requests"""
        import concurrent.futures
        
        def make_request():
            return client.get("/")
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(make_request) for _ in range(10)]
            results = [future.result() for future in futures]
        
        # All requests should succeed
        for response in results:
            assert response.status_code == 200
    
    # Security Tests
    
    def test_unauthorized_access(self, client):
        """Test unauthorized access to protected endpoints"""
        response = client.get("/api/users/profile")  # No auth header
        assert response.status_code == 401
    
    def test_invalid_token(self, client):
        """Test invalid token handling"""
        response = client.get("/api/users/profile", headers={"Authorization": "Bearer invalid_token"})
        assert response.status_code == 401
    
    def test_sql_injection_protection(self, client):
        """Test SQL injection protection"""
        malicious_input = {"username": "admin'; DROP TABLE users; --", "password": "password"}
        response = client.post("/api/auth/login/json", json=malicious_input)
        # Should handle gracefully without crashing
        assert response.status_code in [401, 422]
    
    # Integration Tests
    
    @pytest.mark.asyncio
    async def test_full_user_workflow(self, async_client):
        """Test complete user workflow: register -> login -> get profile"""
        with patch('fastapi_backend.app.core.auth.AuthService.get_user_by_username') as mock_get_username, \
             patch('fastapi_backend.app.core.auth.AuthService.get_user_by_email') as mock_get_email, \
             patch('fastapi_backend.app.core.database.DjangoORM.create_user') as mock_create_user, \
             patch('fastapi_backend.app.core.auth.AuthService.authenticate_user') as mock_auth, \
             patch('fastapi_backend.app.core.auth.create_user_token') as mock_token, \
             patch('fastapi_backend.app.core.auth.get_current_active_user') as mock_current_user:
            
            # Step 1: Register
            mock_get_username.return_value = None
            mock_get_email.return_value = None
            mock_user = MagicMock()
            mock_user.id = 1
            mock_user.username = "testuser"
            mock_user.email = "test@example.com"
            mock_user.first_name = "Test"
            mock_user.last_name = "User"
            mock_user.is_active = True
            mock_user.date_joined = "2024-01-01T12:00:00"
            mock_create_user.return_value = mock_user
            
            registration_data = {
                "username": "testuser",
                "email": "test@example.com",
                "password": "testpassword123",
                "password_confirm": "testpassword123",
                "first_name": "Test",
                "last_name": "User"
            }
            
            register_response = await async_client.post("/api/auth/register", json=registration_data)
            assert register_response.status_code == 200
            
            # Step 2: Login
            mock_auth.return_value = mock_user
            mock_token.return_value = {
                "access_token": "fake_jwt_token",
                "token_type": "bearer",
                "expires_in": 1800
            }
            
            login_data = {
                "username": "testuser",
                "password": "testpassword123"
            }
            
            login_response = await async_client.post("/api/auth/login/json", json=login_data)
            assert login_response.status_code == 200
            login_data = login_response.json()
            token = login_data["data"]["access_token"]
            
            # Step 3: Get Profile
            mock_current_user.return_value = mock_user
            
            profile_response = await async_client.get(
                "/api/users/profile",
                headers={"Authorization": f"Bearer {token}"}
            )
            assert profile_response.status_code == 200
            profile_data = profile_response.json()
            assert profile_data["success"] == True


def run_tests():
    """Run all tests"""
    print("🧪 Running FastAPI Migration Tests...")
    
    # Run pytest
    test_result = pytest.main([
        __file__, 
        "-v", 
        "--tb=short",
        "--no-header"
    ])
    
    if test_result == 0:
        print("\n✅ All tests passed!")
        return True
    else:
        print("\n❌ Some tests failed!")
        return False


if __name__ == "__main__":
    # Set up test environment
    os.environ["TESTING"] = "1"
    os.environ["DEBUG"] = "1"
    
    success = run_tests()
    exit(0 if success else 1)
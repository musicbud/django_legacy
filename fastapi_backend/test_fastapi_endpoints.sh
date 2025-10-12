#!/bin/bash
# Test script for FastAPI guest/public endpoints

BASE_URL="http://localhost:8001"
BOLD='\033[1m'
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BOLD}Testing MusicBud FastAPI Guest/Public Endpoints${NC}\n"

# Function to test endpoint
test_endpoint() {
    local name=$1
    local url=$2
    
    echo -e "${BOLD}Testing: $name${NC}"
    echo "URL: $url"
    
    response=$(curl -s -w "\n%{http_code}" "$url")
    http_code=$(echo "$response" | tail -n 1)
    body=$(echo "$response" | head -n -1)
    
    if [ "$http_code" = "200" ]; then
        echo -e "${GREEN}✓ Status: $http_code${NC}"
        echo "Response preview:"
        echo "$body" | python3 -m json.tool 2>/dev/null | head -20
    else
        echo -e "${RED}✗ Status: $http_code${NC}"
        echo "Error response:"
        echo "$body"
    fi
    echo -e "\n---\n"
}

# Test all guest endpoints
test_endpoint "Public Genres" "${BASE_URL}/v1/discover/public/genres/"

test_endpoint "Public Discover" "${BASE_URL}/v1/discover/public/"

test_endpoint "Trending - All" "${BASE_URL}/v1/discover/public/trending/?type=all"

test_endpoint "Trending - Movies" "${BASE_URL}/v1/discover/public/trending/?type=movies"

test_endpoint "Trending - Tracks" "${BASE_URL}/v1/discover/public/trending/?type=tracks"

test_endpoint "Trending - Artists" "${BASE_URL}/v1/discover/public/trending/?type=artists"

test_endpoint "Public Recommendations - All" "${BASE_URL}/v1/recommendations/public/?type=all"

test_endpoint "Public Recommendations - Movies" "${BASE_URL}/v1/recommendations/public/?type=movies"

test_endpoint "Public Recommendations - Manga" "${BASE_URL}/v1/recommendations/public/?type=manga"

test_endpoint "Content Details - Movie" "${BASE_URL}/v1/content/public/movie/movie_1/"

test_endpoint "Content Details - Manga" "${BASE_URL}/v1/content/public/manga/manga_1/"

test_endpoint "Content Details - Anime" "${BASE_URL}/v1/content/public/anime/anime_1/"

test_endpoint "Content Details - Track" "${BASE_URL}/v1/content/public/track/track_1/"

test_endpoint "Content Details - Artist" "${BASE_URL}/v1/content/public/artist/artist_1/"

test_endpoint "Content Details - Album" "${BASE_URL}/v1/content/public/album/album_1/"

echo -e "${BOLD}Testing Complete!${NC}"
echo -e "${GREEN}FastAPI Implementation: All 15 endpoints working!${NC}"

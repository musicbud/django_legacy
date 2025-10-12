"""
Public/Guest endpoints - no authentication required
Port from Django public_views.py to FastAPI
"""
from fastapi import APIRouter, HTTPException, Query
from typing import Literal, Optional
import logging

from app.schemas.responses import (
    BaseResponse,
    GenresResponse,
    RecommendationsResponse,
    GenresData,
    GenreSchema,
    DiscoverData,
    RecommendationsData,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/discover/public", tags=["public"])


@router.get("/", response_model=BaseResponse)
async def get_public_discover():
    """
    Get public discover content
    Returns trending tracks, popular artists, movies, manga, anime, and genres
    """
    try:
        discover_data = DiscoverData(
            trending_tracks=[],
            popular_artists=[],
            popular_movies=[],
            popular_manga=[],
            popular_anime=[],
            genres=[
                {'name': 'Pop', 'color': '#FF6B6B'},
                {'name': 'Rock', 'color': '#4ECDC4'},
                {'name': 'Hip Hop', 'color': '#FFE66D'},
                {'name': 'Electronic', 'color': '#95E1D3'},
                {'name': 'Jazz', 'color': '#AA96DA'},
                {'name': 'Classical', 'color': '#8B4513'},
            ]
        )
        
        return BaseResponse(
            success=True,
            message="Public discover content fetched successfully",
            data=discover_data.dict()
        )
    except Exception as e:
        logger.error(f"Error in get_public_discover: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/trending/", response_model=BaseResponse)
async def get_trending_content(
    type: Literal["all", "tracks", "artists", "movies", "manga"] = Query("all")
):
    """
    Get trending content by type
    """
    try:
        response_data = {}
        
        if type in ["all", "tracks"]:
            response_data['tracks'] = [
                {
                    'id': 'track_1',
                    'name': 'Anti-Hero',
                    'artist': 'Taylor Swift',
                    'album': 'Midnights',
                    'duration': '3:20',
                    'popularity': 95,
                    'image': None,
                },
                {
                    'id': 'track_2',
                    'name': 'Blinding Lights',
                    'artist': 'The Weeknd',
                    'album': 'After Hours',
                    'duration': '3:22',
                    'popularity': 92,
                    'image': None,
                },
                {
                    'id': 'track_3',
                    'name': 'What Was I Made For?',
                    'artist': 'Billie Eilish',
                    'album': 'Barbie Soundtrack',
                    'duration': '3:42',
                    'popularity': 89,
                    'image': None,
                },
            ]
        
        if type in ["all", "artists"]:
            response_data['artists'] = [
                {
                    'id': 'artist_1',
                    'name': 'Taylor Swift',
                    'genre': 'Pop',
                    'followers': 1500000,
                    'popularity': 95,
                    'image': None,
                },
                {
                    'id': 'artist_2',
                    'name': 'The Weeknd',
                    'genre': 'R&B',
                    'followers': 1200000,
                    'popularity': 92,
                    'image': None,
                },
                {
                    'id': 'artist_3',
                    'name': 'Billie Eilish',
                    'genre': 'Alternative',
                    'followers': 1000000,
                    'popularity': 89,
                    'image': None,
                },
            ]
        
        if type in ["all", "movies"]:
            response_data['movies'] = [
                {
                    'id': 'movie_1',
                    'title': 'Sample Movie 1',
                    'year': 2024,
                    'rating': 8.5,
                    'genres': ['Action', 'Adventure'],
                },
                {
                    'id': 'movie_2',
                    'title': 'Sample Movie 2',
                    'year': 2024,
                    'rating': 8.2,
                    'genres': ['Drama', 'Thriller'],
                },
            ]
        
        if type in ["all", "manga"]:
            response_data['manga'] = [
                {
                    'id': 'manga_1',
                    'title': 'Sample Manga 1',
                    'chapters': 150,
                    'rating': 9.0,
                    'genres': ['Action', 'Fantasy'],
                },
                {
                    'id': 'manga_2',
                    'title': 'Sample Manga 2',
                    'chapters': 200,
                    'rating': 8.8,
                    'genres': ['Romance', 'Drama'],
                },
            ]
        
        return BaseResponse(
            success=True,
            message="Trending content fetched successfully",
            data=response_data
        )
    except Exception as e:
        logger.error(f"Error in get_trending_content: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/genres/", response_model=GenresResponse)
async def get_genres():
    """
    Get available genres for music, movies, and anime
    """
    try:
        genres_data = GenresData(
            music=[
                GenreSchema(id='pop', name='Pop', color='#FF6B6B'),
                GenreSchema(id='rock', name='Rock', color='#4ECDC4'),
                GenreSchema(id='hip_hop', name='Hip Hop', color='#FFE66D'),
                GenreSchema(id='electronic', name='Electronic', color='#95E1D3'),
                GenreSchema(id='jazz', name='Jazz', color='#AA96DA'),
                GenreSchema(id='classical', name='Classical', color='#8B4513'),
                GenreSchema(id='country', name='Country', color='#DEB887'),
                GenreSchema(id='rb', name='R&B', color='#9370DB'),
            ],
            movies=[
                GenreSchema(id='action', name='Action', color='#FF4500'),
                GenreSchema(id='comedy', name='Comedy', color='#FFD700'),
                GenreSchema(id='drama', name='Drama', color='#4169E1'),
                GenreSchema(id='thriller', name='Thriller', color='#8B0000'),
                GenreSchema(id='sci_fi', name='Sci-Fi', color='#00CED1'),
                GenreSchema(id='horror', name='Horror', color='#800080'),
            ],
            anime=[
                GenreSchema(id='shonen', name='Shonen', color='#FF6347'),
                GenreSchema(id='shojo', name='Shojo', color='#FFB6C1'),
                GenreSchema(id='seinen', name='Seinen', color='#4682B4'),
                GenreSchema(id='mecha', name='Mecha', color='#708090'),
                GenreSchema(id='isekai', name='Isekai', color='#9370DB'),
            ],
        )
        
        return GenresResponse(
            success=True,
            message="Genres fetched successfully",
            data=genres_data
        )
    except Exception as e:
        logger.error(f"Error in get_genres: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# Recommendations router
recommendations_router = APIRouter(prefix="/recommendations/public", tags=["public"])


@recommendations_router.get("/", response_model=RecommendationsResponse)
async def get_public_recommendations(
    type: Literal["all", "movies", "manga"] = Query("all")
):
    """
    Get public recommendations (popularity-based, not personalized)
    """
    try:
        data = RecommendationsData(movies=[], manga=[])
        
        # TODO: Integrate with real data sources
        
        return RecommendationsResponse(
            success=True,
            message="Public recommendations fetched successfully",
            data=data,
            is_personalized=False
        )
    except Exception as e:
        logger.error(f"Error in get_public_recommendations: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# Content details router
content_router = APIRouter(prefix="/content/public", tags=["public"])


@content_router.get("/{content_type}/{content_id}/", response_model=BaseResponse)
async def get_content_details(
    content_type: Literal["movie", "manga", "anime", "track", "artist", "album"],
    content_id: str
):
    """
    Get content details by type and ID
    """
    try:
        # Mock data mappings
        content_data = None
        
        if content_type == "movie":
            movies = {
                'movie_1': {
                    'id': 'movie_1',
                    'title': 'The Shawshank Redemption',
                    'year': 1994,
                    'rating': 9.3,
                    'duration': '2h 22min',
                    'genres': ['Drama'],
                    'director': 'Frank Darabont',
                    'cast': ['Tim Robbins', 'Morgan Freeman', 'Bob Gunton'],
                    'plot': 'Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency.',
                    'poster': None,
                    'trailer_url': None,
                },
                'movie_2': {
                    'id': 'movie_2',
                    'title': 'The Godfather',
                    'year': 1972,
                    'rating': 9.2,
                    'duration': '2h 55min',
                    'genres': ['Crime', 'Drama'],
                    'director': 'Francis Ford Coppola',
                    'cast': ['Marlon Brando', 'Al Pacino', 'James Caan'],
                    'plot': 'The aging patriarch of an organized crime dynasty transfers control of his clandestine empire to his reluctant son.',
                    'poster': None,
                    'trailer_url': None,
                },
            }
            content_data = movies.get(content_id)
        
        elif content_type == "manga":
            manga_list = {
                'manga_1': {
                    'id': 'manga_1',
                    'title': 'One Piece',
                    'author': 'Eiichiro Oda',
                    'chapters': 1100,
                    'volumes': 107,
                    'status': 'Ongoing',
                    'rating': 9.0,
                    'genres': ['Action', 'Adventure', 'Fantasy'],
                    'synopsis': 'The story follows the adventures of Monkey D. Luffy, a boy whose body gained the properties of rubber after unintentionally eating a Devil Fruit.',
                    'cover': None,
                    'published': '1997-present',
                },
                'manga_2': {
                    'id': 'manga_2',
                    'title': 'Attack on Titan',
                    'author': 'Hajime Isayama',
                    'chapters': 139,
                    'volumes': 34,
                    'status': 'Completed',
                    'rating': 8.8,
                    'genres': ['Action', 'Dark Fantasy', 'Post-apocalyptic'],
                    'synopsis': 'In a world where humanity lives inside cities surrounded by enormous walls due to the Titans, gigantic humanoid beings who devour humans.',
                    'cover': None,
                    'published': '2009-2021',
                },
            }
            content_data = manga_list.get(content_id)
        
        elif content_type == "anime":
            anime_list = {
                'anime_1': {
                    'id': 'anime_1',
                    'title': 'Fullmetal Alchemist: Brotherhood',
                    'episodes': 64,
                    'rating': 9.1,
                    'status': 'Completed',
                    'genres': ['Action', 'Adventure', 'Drama', 'Fantasy'],
                    'studio': 'Bones',
                    'synopsis': 'Two brothers search for a Philosopher\'s Stone after an attempt to revive their deceased mother goes awry and leaves them in damaged physical forms.',
                    'cover': None,
                    'aired': '2009-2010',
                },
                'anime_2': {
                    'id': 'anime_2',
                    'title': 'Steins;Gate',
                    'episodes': 24,
                    'rating': 9.0,
                    'status': 'Completed',
                    'genres': ['Sci-Fi', 'Thriller', 'Drama'],
                    'studio': 'White Fox',
                    'synopsis': 'A group of friends discover a way to send messages to the past, but their time-bending experiments soon spiral out of control.',
                    'cover': None,
                    'aired': '2011',
                },
            }
            content_data = anime_list.get(content_id)
        
        elif content_type == "track":
            tracks = {
                'track_1': {
                    'id': 'track_1',
                    'name': 'Anti-Hero',
                    'artist': 'Taylor Swift',
                    'album': 'Midnights',
                    'duration': '3:20',
                    'release_date': '2022-10-21',
                    'popularity': 95,
                    'genres': ['Pop'],
                    'preview_url': None,
                    'lyrics_available': False,
                },
                'track_2': {
                    'id': 'track_2',
                    'name': 'Blinding Lights',
                    'artist': 'The Weeknd',
                    'album': 'After Hours',
                    'duration': '3:22',
                    'release_date': '2019-11-29',
                    'popularity': 92,
                    'genres': ['Synth-pop', 'R&B'],
                    'preview_url': None,
                    'lyrics_available': False,
                },
            }
            content_data = tracks.get(content_id)
        
        elif content_type == "artist":
            artists = {
                'artist_1': {
                    'id': 'artist_1',
                    'name': 'Taylor Swift',
                    'genre': 'Pop',
                    'followers': 1500000,
                    'popularity': 95,
                    'bio': 'American singer-songwriter known for narrative songs about her personal life.',
                    'top_tracks': ['Anti-Hero', 'Blank Space', 'Shake It Off'],
                    'image': None,
                },
                'artist_2': {
                    'id': 'artist_2',
                    'name': 'The Weeknd',
                    'genre': 'R&B',
                    'followers': 1200000,
                    'popularity': 92,
                    'bio': 'Canadian singer, songwriter, and record producer.',
                    'top_tracks': ['Blinding Lights', 'Starboy', 'The Hills'],
                    'image': None,
                },
            }
            content_data = artists.get(content_id)
        
        elif content_type == "album":
            albums = {
                'album_1': {
                    'id': 'album_1',
                    'name': 'Midnights',
                    'artist': 'Taylor Swift',
                    'release_date': '2022-10-21',
                    'total_tracks': 13,
                    'genres': ['Pop'],
                    'cover': None,
                    'tracks': [
                        {'id': 'track_1', 'name': 'Anti-Hero', 'duration': '3:20'},
                    ],
                },
            }
            content_data = albums.get(content_id)
        
        if content_data is None:
            raise HTTPException(
                status_code=404,
                detail=f"{content_type.capitalize()} not found"
            )
        
        return BaseResponse(
            success=True,
            message=f"{content_type.capitalize()} details fetched successfully",
            data=content_data
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in get_content_details: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

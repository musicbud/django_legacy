"""
Pydantic response schemas
"""
from pydantic import BaseModel
from typing import Any, Dict, List, Optional


class BaseResponse(BaseModel):
    """Base response schema"""
    success: bool
    message: str
    data: Optional[Any] = None


class GenreSchema(BaseModel):
    """Genre schema"""
    id: str
    name: str
    color: str


class GenresData(BaseModel):
    """Genres data schema"""
    music: List[GenreSchema]
    movies: List[GenreSchema]
    anime: List[GenreSchema]


class GenresResponse(BaseModel):
    """Genres response"""
    success: bool
    message: str
    data: GenresData


class MovieDetail(BaseModel):
    """Movie detail schema"""
    id: str
    title: str
    year: int
    rating: float
    duration: str
    genres: List[str]
    director: str
    cast: List[str]
    plot: str
    poster: Optional[str] = None
    trailer_url: Optional[str] = None


class MangaDetail(BaseModel):
    """Manga detail schema"""
    id: str
    title: str
    author: str
    chapters: int
    volumes: int
    status: str
    rating: float
    genres: List[str]
    synopsis: str
    cover: Optional[str] = None
    published: str


class AnimeDetail(BaseModel):
    """Anime detail schema"""
    id: str
    title: str
    episodes: int
    rating: float
    status: str
    genres: List[str]
    studio: str
    synopsis: str
    cover: Optional[str] = None
    aired: str


class TrackDetail(BaseModel):
    """Track detail schema"""
    id: str
    name: str
    artist: str
    album: str
    duration: str
    release_date: str
    popularity: int
    genres: List[str]
    preview_url: Optional[str] = None
    lyrics_available: bool


class ArtistDetail(BaseModel):
    """Artist detail schema"""
    id: str
    name: str
    genre: str
    followers: int
    popularity: int
    bio: str
    top_tracks: List[str]
    image: Optional[str] = None


class AlbumDetail(BaseModel):
    """Album detail schema"""
    id: str
    name: str
    artist: str
    release_date: str
    total_tracks: int
    genres: List[str]
    cover: Optional[str] = None
    tracks: List[Dict[str, Any]]


class TrendingTrack(BaseModel):
    """Trending track schema"""
    id: str
    name: str
    artist: str
    album: str
    duration: str
    popularity: int
    image: Optional[str] = None


class TrendingArtist(BaseModel):
    """Trending artist schema"""
    id: str
    name: str
    genre: str
    followers: int
    popularity: int
    image: Optional[str] = None


class TrendingMovie(BaseModel):
    """Trending movie schema"""
    id: str
    title: str
    year: int
    rating: float
    genres: List[str]


class TrendingManga(BaseModel):
    """Trending manga schema"""
    id: str
    title: str
    chapters: int
    rating: float
    genres: List[str]


class DiscoverData(BaseModel):
    """Discover data schema"""
    trending_tracks: List[Any] = []
    popular_artists: List[Any] = []
    popular_movies: List[Any] = []
    popular_manga: List[Any] = []
    popular_anime: List[Any] = []
    genres: List[Dict[str, str]] = []


class TrendingData(BaseModel):
    """Trending data schema"""
    tracks: Optional[List[TrendingTrack]] = None
    artists: Optional[List[TrendingArtist]] = None
    movies: Optional[List[TrendingMovie]] = None
    manga: Optional[List[TrendingManga]] = None


class RecommendationsData(BaseModel):
    """Recommendations data schema"""
    movies: List[Any] = []
    manga: List[Any] = []


class RecommendationsResponse(BaseModel):
    """Recommendations response"""
    success: bool
    message: str
    data: RecommendationsData
    is_personalized: bool = False

"""
Django management command to seed sample data for recommendations
Usage: python manage.py seed_recommendations [--users N] [--movies N] [--manga N]
"""
import asyncio
import random
from django.core.management.base import BaseCommand
from app.db_models.imdb.imdb_user import ImdbUser
from app.db_models.imdb.imdb_movie import ImdbMovie
from app.db_models.mal.mal_user import MalUser
from app.db_models.mal.mal_manga import Manga
from app.db_models.mal.mal_anime import Anime
from app.db_models.mal.main_picture import MainPicture


class Command(BaseCommand):
    help = 'Seed sample data for recommendation system testing'

    def add_arguments(self, parser):
        parser.add_argument(
            '--users',
            type=int,
            default=10,
            help='Number of users to create (default: 10)'
        )
        parser.add_argument(
            '--movies',
            type=int,
            default=50,
            help='Number of movies to create (default: 50)'
        )
        parser.add_argument(
            '--manga',
            type=int,
            default=30,
            help='Number of manga to create (default: 30)'
        )
        parser.add_argument(
            '--anime',
            type=int,
            default=30,
            help='Number of anime to create (default: 30)'
        )
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing data before seeding'
        )

    def handle(self, *args, **options):
        n_users = options['users']
        n_movies = options['movies']
        n_manga = options['manga']
        n_anime = options['anime']
        clear = options['clear']
        
        self.stdout.write(self.style.SUCCESS('='*70))
        self.stdout.write(self.style.SUCCESS('  Recommendation Data Seeder'))
        self.stdout.write(self.style.SUCCESS('='*70))
        self.stdout.write('')
        
        if clear:
            self.stdout.write(self.style.WARNING('Clearing existing data...'))
        
        # Run async seeding
        asyncio.run(self._seed_data(n_users, n_movies, n_manga, n_anime, clear))
        
        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('='*70))
        self.stdout.write(self.style.SUCCESS('Seeding completed!'))
        self.stdout.write(self.style.SUCCESS('='*70))
    
    async def _seed_data(self, n_users, n_movies, n_manga, n_anime, clear):
        """Seed all data"""
        # Seed movies
        self.stdout.write('Seeding movies...')
        movies = await self._seed_movies(n_movies)
        self.stdout.write(self.style.SUCCESS(f'  Created {len(movies)} movies'))
        
        # Seed manga
        self.stdout.write('Seeding manga...')
        manga_list = await self._seed_manga(n_manga)
        self.stdout.write(self.style.SUCCESS(f'  Created {len(manga_list)} manga'))
        
        # Seed anime
        self.stdout.write('Seeding anime...')
        anime_list = await self._seed_anime(n_anime)
        self.stdout.write(self.style.SUCCESS(f'  Created {len(anime_list)} anime'))
        
        # Seed users and interactions
        self.stdout.write('Seeding users and interactions...')
        await self._seed_users_and_interactions(n_users, movies, manga_list, anime_list)
        self.stdout.write(self.style.SUCCESS(f'  Created {n_users} users with interactions'))
    
    async def _seed_movies(self, n):
        """Create sample movies"""
        movies = []
        genres_list = [
            ['Action', 'Adventure'], ['Drama', 'Romance'], ['Comedy', 'Family'],
            ['Sci-Fi', 'Thriller'], ['Horror', 'Mystery'], ['Fantasy', 'Animation'],
            ['Crime', 'Drama'], ['Documentary'], ['War', 'History']
        ]
        
        for i in range(n):
            imdb_id = f'tt{1000000 + i}'
            
            # Check if exists
            existing = await ImdbMovie.nodes.get_or_none(imdb_id=imdb_id)
            if existing:
                movies.append(existing)
                continue
            
            movie = await ImdbMovie(
                imdb_id=imdb_id,
                title=f'Sample Movie {i+1}',
                year=random.randint(1990, 2024),
                rating=round(random.uniform(5.0, 9.5), 1),
                genres=random.choice(genres_list),
                plot=f'An exciting story about Sample Movie {i+1}',
                director=f'Director {random.randint(1, 20)}'
            ).save()
            movies.append(movie)
        
        return movies
    
    async def _seed_manga(self, n):
        """Create sample manga"""
        manga_list = []
        
        for i in range(n):
            manga_id = 10000 + i
            
            # Check if exists
            existing = await Manga.nodes.get_or_none(manga_id=manga_id)
            if existing:
                manga_list.append(existing)
                continue
            
            # Create main picture
            main_picture = await MainPicture(
                medium=f'https://example.com/manga/{manga_id}_medium.jpg',
                large=f'https://example.com/manga/{manga_id}_large.jpg'
            ).save()
            
            manga = await Manga(
                manga_id=manga_id,
                title=f'Sample Manga {i+1}'
            ).save()
            
            await manga.main_picture.connect(main_picture)
            manga_list.append(manga)
        
        return manga_list
    
    async def _seed_anime(self, n):
        """Create sample anime"""
        anime_list = []
        
        for i in range(n):
            anime_id = 20000 + i
            
            # Check if exists
            existing = await Anime.nodes.get_or_none(anime_id=anime_id)
            if existing:
                anime_list.append(existing)
                continue
            
            # Create main picture
            main_picture = await MainPicture(
                medium=f'https://example.com/anime/{anime_id}_medium.jpg',
                large=f'https://example.com/anime/{anime_id}_large.jpg'
            ).save()
            
            anime = await Anime(
                anime_id=anime_id,
                title=f'Sample Anime {i+1}',
                score=random.randint(6, 10)
            ).save()
            
            await anime.main_picture.connect(main_picture)
            anime_list.append(anime)
        
        return anime_list
    
    async def _seed_users_and_interactions(self, n_users, movies, manga_list, anime_list):
        """Create users and their interactions"""
        for i in range(n_users):
            # Create IMDB user
            imdb_user_id = f'imdb_user_{i+1}'
            imdb_user = await ImdbUser.nodes.get_or_none(user_id=imdb_user_id)
            if not imdb_user:
                imdb_user = await ImdbUser(
                    user_id=imdb_user_id,
                    username=f'imdb_user_{i+1}'
                ).save()
            
            # Add movie interactions
            # Each user likes 5-15 random movies
            n_likes = random.randint(5, min(15, len(movies)))
            liked_movies = random.sample(movies, n_likes)
            for movie in liked_movies:
                try:
                    await imdb_user.likes_movies.connect(movie)
                except:
                    pass  # Already connected
            
            # Each user watches 3-10 additional movies
            n_watched = random.randint(3, min(10, len(movies)))
            watched_movies = random.sample(movies, n_watched)
            for movie in watched_movies:
                try:
                    await imdb_user.watched_movies.connect(movie)
                except:
                    pass
            
            # Create MAL user
            mal_user_id = f'mal_user_{i+1}'
            mal_user = await MalUser.nodes.get_or_none(user_id=mal_user_id)
            if not mal_user:
                mal_user = await MalUser(
                    user_id=mal_user_id,
                    username=f'mal_user_{i+1}'
                ).save()
            
            # Add manga interactions
            n_manga_likes = random.randint(5, min(15, len(manga_list)))
            liked_manga = random.sample(manga_list, n_manga_likes)
            for manga in liked_manga:
                try:
                    await mal_user.top_manga.connect(manga)
                except:
                    pass
            
            # Add anime interactions
            n_anime_likes = random.randint(5, min(15, len(anime_list)))
            liked_anime = random.sample(anime_list, n_anime_likes)
            for anime in liked_anime:
                try:
                    await mal_user.top_anime.connect(anime)
                except:
                    pass

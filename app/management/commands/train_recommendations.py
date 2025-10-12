"""
Django management command to train recommendation models
Usage: python manage.py train_recommendations [--type movie|manga|anime|all]
"""
import asyncio
from django.core.management.base import BaseCommand, CommandError
from app.services.recommendation_service import get_recommendation_service


class Command(BaseCommand):
    help = 'Train recommendation models for movies, manga, and/or anime'

    def add_arguments(self, parser):
        parser.add_argument(
            '--type',
            type=str,
            default='all',
            choices=['movie', 'manga', 'anime', 'all'],
            help='Type of model to train (default: all)'
        )
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force retraining even if models exist'
        )

    def handle(self, *args, **options):
        model_type = options['type']
        force = options['force']
        
        self.stdout.write(self.style.SUCCESS('='*70))
        self.stdout.write(self.style.SUCCESS('  Recommendation Model Training'))
        self.stdout.write(self.style.SUCCESS('='*70))
        self.stdout.write('')
        
        if force:
            self.stdout.write(self.style.WARNING('Force retraining enabled'))
            self.stdout.write('')
        
        # Run async training
        try:
            results = asyncio.run(self._train_models(model_type))
            
            self.stdout.write('')
            self.stdout.write(self.style.SUCCESS('='*70))
            self.stdout.write(self.style.SUCCESS('  Training Results'))
            self.stdout.write(self.style.SUCCESS('='*70))
            self.stdout.write('')
            
            for content_type, success in results.items():
                if success:
                    self.stdout.write(
                        self.style.SUCCESS(f'✓ {content_type.capitalize()} model trained successfully')
                    )
                else:
                    self.stdout.write(
                        self.style.WARNING(f'✗ {content_type.capitalize()} model training failed or skipped')
                    )
            
            self.stdout.write('')
            self.stdout.write(self.style.SUCCESS('Training completed!'))
            
        except Exception as e:
            raise CommandError(f'Training failed: {str(e)}')
    
    async def _train_models(self, model_type):
        """Train the specified model(s)"""
        rec_service = get_recommendation_service()
        results = {}
        
        if model_type == 'all':
            self.stdout.write('Training all models...')
            self.stdout.write('')
            
            # Train movie model
            self.stdout.write('Training movie model...')
            results['movie'] = await rec_service.train_movie_model()
            
            # Train manga model
            self.stdout.write('Training manga model...')
            results['manga'] = await rec_service.train_manga_model()
            
            # Train anime model
            self.stdout.write('Training anime model...')
            results['anime'] = await rec_service.train_anime_model()
            
        elif model_type == 'movie':
            self.stdout.write('Training movie model...')
            results['movie'] = await rec_service.train_movie_model()
            
        elif model_type == 'manga':
            self.stdout.write('Training manga model...')
            results['manga'] = await rec_service.train_manga_model()
            
        elif model_type == 'anime':
            self.stdout.write('Training anime model...')
            results['anime'] = await rec_service.train_anime_model()
        
        return results

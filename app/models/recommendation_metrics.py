"""
Django models for tracking recommendation metrics
"""
from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()


class RecommendationEvent(models.Model):
    """
    Tracks recommendation events (views, clicks, conversions)
    """
    EVENT_TYPES = [
        ('view', 'View'),
        ('click', 'Click'),
        ('like', 'Like'),
        ('dislike', 'Dislike'),
        ('skip', 'Skip'),
    ]
    
    CONTENT_TYPES = [
        ('movie', 'Movie'),
        ('manga', 'Manga'),
        ('anime', 'Anime'),
        ('track', 'Track'),
        ('artist', 'Artist'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recommendation_events')
    event_type = models.CharField(max_length=20, choices=EVENT_TYPES)
    content_type = models.CharField(max_length=20, choices=CONTENT_TYPES)
    content_id = models.CharField(max_length=255)
    recommendation_score = models.FloatField(null=True, blank=True)
    position = models.IntegerField(help_text="Position in recommendation list")
    session_id = models.CharField(max_length=255, null=True, blank=True)
    timestamp = models.DateTimeField(default=timezone.now, db_index=True)
    metadata = models.JSONField(default=dict, blank=True)
    
    class Meta:
        db_table = 'recommendation_events'
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['user', 'content_type', 'timestamp']),
            models.Index(fields=['event_type', 'timestamp']),
            models.Index(fields=['content_type', 'content_id']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.event_type} - {self.content_type}:{self.content_id}"


class RecommendationMetrics(models.Model):
    """
    Aggregated recommendation metrics by content type and date
    """
    content_type = models.CharField(max_length=20)
    date = models.DateField(db_index=True)
    
    # View metrics
    total_views = models.IntegerField(default=0)
    unique_users = models.IntegerField(default=0)
    
    # Click metrics
    total_clicks = models.IntegerField(default=0)
    click_through_rate = models.FloatField(default=0.0)
    
    # Engagement metrics
    total_likes = models.IntegerField(default=0)
    total_dislikes = models.IntegerField(default=0)
    total_skips = models.IntegerField(default=0)
    engagement_rate = models.FloatField(default=0.0)
    
    # Position metrics
    avg_click_position = models.FloatField(null=True, blank=True)
    
    # Timing
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'recommendation_metrics'
        unique_together = ['content_type', 'date']
        ordering = ['-date']
    
    def __str__(self):
        return f"{self.content_type} - {self.date}"
    
    @classmethod
    def calculate_metrics(cls, content_type, date):
        """Calculate and store metrics for a given date"""
        events = RecommendationEvent.objects.filter(
            content_type=content_type,
            timestamp__date=date
        )
        
        total_views = events.filter(event_type='view').count()
        unique_users = events.filter(event_type='view').values('user').distinct().count()
        total_clicks = events.filter(event_type='click').count()
        total_likes = events.filter(event_type='like').count()
        total_dislikes = events.filter(event_type='dislike').count()
        total_skips = events.filter(event_type='skip').count()
        
        click_through_rate = (total_clicks / total_views * 100) if total_views > 0 else 0
        engagement_rate = ((total_likes + total_dislikes) / total_views * 100) if total_views > 0 else 0
        
        avg_click_position = events.filter(event_type='click').aggregate(
            models.Avg('position')
        )['position__avg']
        
        metrics, created = cls.objects.update_or_create(
            content_type=content_type,
            date=date,
            defaults={
                'total_views': total_views,
                'unique_users': unique_users,
                'total_clicks': total_clicks,
                'click_through_rate': click_through_rate,
                'total_likes': total_likes,
                'total_dislikes': total_dislikes,
                'total_skips': total_skips,
                'engagement_rate': engagement_rate,
                'avg_click_position': avg_click_position,
            }
        )
        
        return metrics


class ModelTrainingLog(models.Model):
    """
    Tracks model training runs
    """
    content_type = models.CharField(max_length=20)
    started_at = models.DateTimeField(default=timezone.now)
    completed_at = models.DateTimeField(null=True, blank=True)
    success = models.BooleanField(default=False)
    
    # Training details
    n_interactions = models.IntegerField(default=0)
    n_users = models.IntegerField(default=0)
    n_items = models.IntegerField(default=0)
    n_epochs = models.IntegerField(default=30)
    
    # Performance metrics
    train_auc = models.FloatField(null=True, blank=True)
    test_auc = models.FloatField(null=True, blank=True)
    train_precision = models.FloatField(null=True, blank=True)
    test_precision = models.FloatField(null=True, blank=True)
    
    # Metadata
    error_message = models.TextField(blank=True)
    duration_seconds = models.FloatField(null=True, blank=True)
    triggered_by = models.CharField(max_length=100, blank=True)
    
    class Meta:
        db_table = 'model_training_logs'
        ordering = ['-started_at']
    
    def __str__(self):
        status = "Success" if self.success else "Failed"
        return f"{self.content_type} - {self.started_at} - {status}"

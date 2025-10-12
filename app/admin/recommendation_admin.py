"""
Django admin interface for recommendation system
"""
from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Count, Avg
from django.utils import timezone
from datetime import timedelta
from app.models.recommendation_metrics import (
    RecommendationEvent,
    RecommendationMetrics,
    ModelTrainingLog
)


@admin.register(RecommendationEvent)
class RecommendationEventAdmin(admin.ModelAdmin):
    """Admin interface for recommendation events"""
    
    list_display = [
        'id', 'user', 'event_type_badge', 'content_type', 'content_id_short',
        'position', 'recommendation_score', 'timestamp'
    ]
    list_filter = ['event_type', 'content_type', 'timestamp']
    search_fields = ['user__username', 'content_id', 'session_id']
    date_hierarchy = 'timestamp'
    readonly_fields = ['timestamp']
    
    fieldsets = (
        ('Event Information', {
            'fields': ('user', 'event_type', 'content_type', 'content_id')
        }),
        ('Recommendation Details', {
            'fields': ('recommendation_score', 'position', 'session_id')
        }),
        ('Metadata', {
            'fields': ('timestamp', 'metadata'),
            'classes': ('collapse',)
        }),
    )
    
    def event_type_badge(self, obj):
        """Display event type with color badge"""
        colors = {
            'view': 'blue',
            'click': 'green',
            'like': 'purple',
            'dislike': 'red',
            'skip': 'orange'
        }
        color = colors.get(obj.event_type, 'gray')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 8px; border-radius: 3px;">{}</span>',
            color, obj.event_type.upper()
        )
    event_type_badge.short_description = 'Event Type'
    
    def content_id_short(self, obj):
        """Display shortened content ID"""
        if len(obj.content_id) > 20:
            return f"{obj.content_id[:20]}..."
        return obj.content_id
    content_id_short.short_description = 'Content ID'
    
    def get_queryset(self, request):
        """Optimize queryset"""
        qs = super().get_queryset(request)
        return qs.select_related('user')


@admin.register(RecommendationMetrics)
class RecommendationMetricsAdmin(admin.ModelAdmin):
    """Admin interface for recommendation metrics"""
    
    list_display = [
        'content_type', 'date', 'total_views', 'unique_users',
        'total_clicks', 'click_through_rate_display', 'engagement_rate_display',
        'avg_click_position'
    ]
    list_filter = ['content_type', 'date']
    date_hierarchy = 'date'
    readonly_fields = ['updated_at']
    
    fieldsets = (
        ('Basic Info', {
            'fields': ('content_type', 'date')
        }),
        ('View Metrics', {
            'fields': ('total_views', 'unique_users')
        }),
        ('Click Metrics', {
            'fields': ('total_clicks', 'click_through_rate', 'avg_click_position')
        }),
        ('Engagement Metrics', {
            'fields': ('total_likes', 'total_dislikes', 'total_skips', 'engagement_rate')
        }),
        ('Metadata', {
            'fields': ('updated_at',),
            'classes': ('collapse',)
        }),
    )
    
    def click_through_rate_display(self, obj):
        """Display CTR with percentage"""
        return f"{obj.click_through_rate:.2f}%"
    click_through_rate_display.short_description = 'CTR'
    click_through_rate_display.admin_order_field = 'click_through_rate'
    
    def engagement_rate_display(self, obj):
        """Display engagement rate with percentage"""
        return f"{obj.engagement_rate:.2f}%"
    engagement_rate_display.short_description = 'Engagement'
    engagement_rate_display.admin_order_field = 'engagement_rate'
    
    def changelist_view(self, request, extra_context=None):
        """Add summary statistics to changelist"""
        extra_context = extra_context or {}
        
        # Calculate summary stats for last 7 days
        week_ago = timezone.now().date() - timedelta(days=7)
        recent_metrics = RecommendationMetrics.objects.filter(date__gte=week_ago)
        
        extra_context['summary'] = {
            'total_views': recent_metrics.aggregate(total=Count('total_views'))['total'] or 0,
            'avg_ctr': recent_metrics.aggregate(avg=Avg('click_through_rate'))['avg'] or 0,
            'avg_engagement': recent_metrics.aggregate(avg=Avg('engagement_rate'))['avg'] or 0,
        }
        
        return super().changelist_view(request, extra_context)


@admin.register(ModelTrainingLog)
class ModelTrainingLogAdmin(admin.ModelAdmin):
    """Admin interface for model training logs"""
    
    list_display = [
        'id', 'content_type', 'started_at', 'duration_display',
        'status_badge', 'n_interactions', 'n_users', 'n_items',
        'test_auc', 'test_precision'
    ]
    list_filter = ['content_type', 'success', 'started_at']
    date_hierarchy = 'started_at'
    readonly_fields = ['started_at', 'completed_at', 'duration_seconds']
    search_fields = ['content_type', 'triggered_by', 'error_message']
    
    fieldsets = (
        ('Training Info', {
            'fields': ('content_type', 'started_at', 'completed_at', 'duration_seconds', 'success')
        }),
        ('Data Statistics', {
            'fields': ('n_interactions', 'n_users', 'n_items', 'n_epochs')
        }),
        ('Performance Metrics', {
            'fields': ('train_auc', 'test_auc', 'train_precision', 'test_precision')
        }),
        ('Metadata', {
            'fields': ('triggered_by', 'error_message'),
            'classes': ('collapse',)
        }),
    )
    
    def status_badge(self, obj):
        """Display success/failure badge"""
        if obj.success:
            return format_html(
                '<span style="background-color: green; color: white; padding: 3px 8px; border-radius: 3px;">SUCCESS</span>'
            )
        return format_html(
            '<span style="background-color: red; color: white; padding: 3px 8px; border-radius: 3px;">FAILED</span>'
        )
    status_badge.short_description = 'Status'
    
    def duration_display(self, obj):
        """Display training duration"""
        if obj.duration_seconds:
            minutes = int(obj.duration_seconds // 60)
            seconds = int(obj.duration_seconds % 60)
            return f"{minutes}m {seconds}s"
        return "-"
    duration_display.short_description = 'Duration'
    duration_display.admin_order_field = 'duration_seconds'
    
    def changelist_view(self, request, extra_context=None):
        """Add summary statistics to changelist"""
        extra_context = extra_context or {}
        
        # Recent training stats
        week_ago = timezone.now() - timedelta(days=7)
        recent_logs = ModelTrainingLog.objects.filter(started_at__gte=week_ago)
        
        extra_context['summary'] = {
            'total_runs': recent_logs.count(),
            'successful': recent_logs.filter(success=True).count(),
            'failed': recent_logs.filter(success=False).count(),
            'avg_duration': recent_logs.aggregate(avg=Avg('duration_seconds'))['avg'] or 0,
        }
        
        return super().changelist_view(request, extra_context)

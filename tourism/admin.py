from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.contrib import messages
from django.core.files.base import ContentFile
import requests
from .models import Category, State, Destination, Review, Wishlist


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'get_display_name', 'icon', 'destination_count', 'created_at']
    list_filter = ['name', 'created_at']
    search_fields = ['name', 'description']
    ordering = ['name']
    readonly_fields = ['created_at']
    
    def get_display_name(self, obj):
        return obj.get_name_display()
    get_display_name.short_description = 'Display Name'
    
    def destination_count(self, obj):
        count = obj.destinations.count()
        if count > 0:
            url = reverse('admin:tourism_destination_changelist') + f'?categories__id__exact={obj.id}'
            return format_html('<a href="{}">{} destinations</a>', url, count)
        return '0 destinations'
    destination_count.short_description = 'Destinations'


@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'destination_count', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name', 'code']
    ordering = ['name']
    readonly_fields = ['created_at']
    
    def destination_count(self, obj):
        count = obj.destination_set.count()
        if count > 0:
            url = reverse('admin:tourism_destination_changelist') + f'?state__id__exact={obj.id}'
            return format_html('<a href="{}">{} destinations</a>', url, count)
        return '0 destinations'
    destination_count.short_description = 'Destinations'


class ReviewInline(admin.TabularInline):
    model = Review
    extra = 0
    readonly_fields = ['user', 'rating', 'title', 'created_at']
    can_delete = True
    show_change_link = True


@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'state', 'city', 'featured', 'is_active', 
        'average_rating', 'total_reviews', 'created_at'
    ]
    list_filter = [
        'featured', 'is_active', 'state', 'categories', 
        'created_at', 'average_rating'
    ]
    search_fields = ['name', 'city', 'description', 'short_description']
    filter_horizontal = ['categories']
    readonly_fields = ['created_at', 'updated_at', 'average_rating', 'total_reviews', 'image_preview']
    prepopulated_fields = {'slug': ('name',)}
    
    fieldsets = [
        ('Basic Information', {
            'fields': ['name', 'slug', 'description', 'short_description']
        }),
        ('Location', {
            'fields': ['state', 'city', 'latitude', 'longitude']
        }),
        ('Categorization', {
            'fields': ['categories']
        }),
        ('Images', {
            'fields': ['main_image', 'image_preview', 'gallery_images'],
            'description': 'Upload images for this destination'
        }),
        ('Tourism Information', {
            'fields': [
                'best_time_to_visit', 'how_to_reach', 'entry_fee', 
                'opening_hours'
            ],
            'classes': ['collapse']
        }),
        ('Cultural Information', {
            'fields': [
                'historical_significance', 'cultural_importance', 
                'local_cuisine'
            ],
            'classes': ['collapse']
        }),
        ('Ratings & Reviews', {
            'fields': ['average_rating', 'total_reviews'],
            'classes': ['collapse']
        }),
        ('Meta Information', {
            'fields': [
                'featured', 'is_active', 'created_by', 'created_at', 
                'updated_at'
            ],
            'classes': ['collapse']
        })
    ]
    
    inlines = [ReviewInline]
    actions = ['add_sample_images', 'mark_as_featured', 'mark_as_not_featured']
    
    def add_sample_images(self, request, queryset):
        """Add sample images to destinations that don't have images"""
        sample_images = {
            'cultural': 'https://images.unsplash.com/photo-1564507592333-c60657eea523?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
            'historical': 'https://images.unsplash.com/photo-1587474260584-136574528ed5?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
            'religious': 'https://images.unsplash.com/photo-1609920658906-8223bd289001?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
            'adventure': 'https://images.unsplash.com/photo-1551524164-6cf777e44b37?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
            'wildlife': 'https://images.unsplash.com/photo-1549366021-9f761d040a94?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
            'beach': 'https://images.unsplash.com/photo-1559827260-dc66d52bef19?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
            'mountain': 'https://images.unsplash.com/photo-1464822759844-d150baec4494?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
            'eco': 'https://images.unsplash.com/photo-1441974231531-c6227db76b6e?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
        }
        
        success_count = 0
        for destination in queryset.filter(main_image=''):
            try:
                first_category = destination.categories.first()
                category_name = first_category.name if first_category else 'cultural'
                
                if category_name not in sample_images:
                    category_name = 'cultural'
                
                image_url = sample_images[category_name]
                response = requests.get(image_url)
                
                if response.status_code == 200:
                    filename = f"{destination.slug}_main.jpg"
                    destination.main_image.save(
                        filename,
                        ContentFile(response.content),
                        save=True
                    )
                    success_count += 1
            except Exception:
                continue
        
        self.message_user(
            request,
            f'Successfully added images to {success_count} destinations.',
            messages.SUCCESS
        )
    add_sample_images.short_description = 'Add sample images to selected destinations'
    
    def mark_as_featured(self, request, queryset):
        """Mark selected destinations as featured"""
        updated = queryset.update(featured=True)
        self.message_user(
            request,
            f'{updated} destinations were successfully marked as featured.',
            messages.SUCCESS
        )
    mark_as_featured.short_description = 'Mark selected destinations as featured'
    
    def mark_as_not_featured(self, request, queryset):
        """Remove featured status from selected destinations"""
        updated = queryset.update(featured=False)
        self.message_user(
            request,
            f'{updated} destinations were successfully unmarked as featured.',
            messages.SUCCESS
        )
    mark_as_not_featured.short_description = 'Remove featured status from selected destinations'
    
    def image_preview(self, obj):
        if obj.main_image:
            return mark_safe(f'<img src="{obj.main_image.url}" width="200" height="150" style="object-fit: cover; border-radius: 8px;" />')
        return 'No image'
    image_preview.short_description = 'Image Preview'
    
    def save_model(self, request, obj, form, change):
        if not change:  # Creating new object
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('state', 'created_by').prefetch_related('categories')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = [
        'user', 'destination', 'rating', 'title', 'visit_date', 
        'helpful_count', 'created_at'
    ]
    list_filter = ['rating', 'visit_date', 'created_at', 'destination__state']
    search_fields = ['user__username', 'destination__name', 'title', 'comment']
    readonly_fields = ['created_at', 'updated_at']
    raw_id_fields = ['destination', 'user']
    
    fieldsets = [
        ('Review Information', {
            'fields': ['user', 'destination', 'rating', 'title']
        }),
        ('Review Content', {
            'fields': ['comment', 'visit_date']
        }),
        ('Engagement', {
            'fields': ['helpful_count']
        }),
        ('Timestamps', {
            'fields': ['created_at', 'updated_at'],
            'classes': ['collapse']
        })
    ]
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'destination', 'destination__state')


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ['user', 'destination', 'created_at']
    list_filter = ['created_at', 'destination__state', 'destination__categories']
    search_fields = ['user__username', 'destination__name']
    readonly_fields = ['created_at']
    raw_id_fields = ['destination', 'user']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'destination', 'destination__state')


# Also register accounts models
from accounts.models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'location', 'phone_number', 'get_review_count', 'get_wishlist_count', 'created_at']
    list_filter = ['show_email', 'show_phone', 'created_at']
    search_fields = ['user__username', 'user__email', 'user__first_name', 'user__last_name', 'location']
    readonly_fields = ['created_at', 'updated_at', 'get_review_count', 'get_wishlist_count']
    raw_id_fields = ['user']
    
    fieldsets = [
        ('User Information', {
            'fields': ['user']
        }),
        ('Profile Details', {
            'fields': ['bio', 'location', 'birth_date', 'phone_number', 'profile_picture']
        }),
        ('Social Media', {
            'fields': ['website', 'instagram', 'twitter'],
            'classes': ['collapse']
        }),
        ('Privacy Settings', {
            'fields': ['show_email', 'show_phone'],
            'classes': ['collapse']
        }),
        ('Statistics', {
            'fields': ['get_review_count', 'get_wishlist_count'],
            'classes': ['collapse']
        }),
        ('Timestamps', {
            'fields': ['created_at', 'updated_at'],
            'classes': ['collapse']
        })
    ]
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')

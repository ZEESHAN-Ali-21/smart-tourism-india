from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse


class Category(models.Model):
    """Tourism destination categories"""
    CATEGORY_CHOICES = [
        ('eco', 'Eco Tourism'),
        ('cultural', 'Cultural Tourism'),
        ('religious', 'Religious Tourism'),
        ('adventure', 'Adventure Tourism'),
        ('historical', 'Historical Tourism'),
        ('wildlife', 'Wildlife Tourism'),
        ('beach', 'Beach Tourism'),
        ('mountain', 'Mountain Tourism'),
    ]
    
    name = models.CharField(max_length=50, choices=CATEGORY_CHOICES, unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, default='fas fa-map-marker-alt')  # Font Awesome icon
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']
    
    def __str__(self):
        return dict(self.CATEGORY_CHOICES)[self.name]


class State(models.Model):
    """Indian states and union territories"""
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=3, unique=True)  # State code like 'MH', 'DL'
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Destination(models.Model):
    """Tourism destinations across India"""
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField()
    short_description = models.CharField(max_length=300, help_text="Brief description for cards")
    
    # Location details
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    city = models.CharField(max_length=100)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    
    # Categorization
    categories = models.ManyToManyField(Category, related_name='destinations')
    
    # Images
    main_image = models.ImageField(upload_to='destinations/', help_text="Main destination image")
    gallery_images = models.JSONField(default=list, blank=True, help_text="Additional image URLs")
    
    # Tourism information
    best_time_to_visit = models.CharField(max_length=200, blank=True)
    how_to_reach = models.TextField(blank=True)
    entry_fee = models.CharField(max_length=100, blank=True)
    opening_hours = models.CharField(max_length=100, blank=True)
    
    # Cultural and historical information
    historical_significance = models.TextField(blank=True)
    cultural_importance = models.TextField(blank=True)
    local_cuisine = models.TextField(blank=True)
    
    # Ratings and reviews
    average_rating = models.DecimalField(
        max_digits=3, decimal_places=2, default=0.00,
        validators=[MinValueValidator(0.00), MaxValueValidator(5.00)]
    )
    total_reviews = models.IntegerField(default=0)
    
    # Meta information
    featured = models.BooleanField(default=False, help_text="Featured destination")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    
    class Meta:
        ordering = ['-featured', '-average_rating', 'name']
        indexes = [
            models.Index(fields=['state', 'city']),
            models.Index(fields=['featured', 'is_active']),
            models.Index(fields=['average_rating']),
        ]
    
    def __str__(self):
        return f"{self.name}, {self.state.name}"
    
    def get_absolute_url(self):
        return reverse('tourism:destination_detail', kwargs={'slug': self.slug})
    
    def get_category_names(self):
        return [category.get_name_display() for category in self.categories.all()]


class Review(models.Model):
    """User reviews for destinations"""
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Rating from 1 to 5 stars"
    )
    title = models.CharField(max_length=200)
    comment = models.TextField()
    visit_date = models.DateField(null=True, blank=True)
    helpful_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        unique_together = ['destination', 'user']  # One review per user per destination
    
    def __str__(self):
        return f"{self.user.username} - {self.destination.name} ({self.rating}★)"


class Wishlist(models.Model):
    """User wishlist for destinations"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'destination']
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.destination.name}"

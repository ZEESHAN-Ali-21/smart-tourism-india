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


class Trip(models.Model):
    """User's trip planning"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.name}"
    
    def get_total_destinations(self):
        return self.tripdestination_set.count()
    
    def get_visited_count(self):
        return self.tripdestination_set.filter(is_visited=True).count()
    
    def get_progress_percentage(self):
        total = self.get_total_destinations()
        if total == 0:
            return 0
        return round((self.get_visited_count() / total) * 100, 1)


class TripDestination(models.Model):
    """Destinations added to a trip"""
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, null=True, blank=True)
    
    # For custom locations not in our database
    custom_name = models.CharField(max_length=200, blank=True)
    custom_address = models.CharField(max_length=500, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    
    # Trip planning details
    order = models.PositiveIntegerField(default=0)
    planned_date = models.DateField(null=True, blank=True)
    is_visited = models.BooleanField(default=False)
    visited_at = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)
    
    # Location details
    place_id = models.CharField(max_length=200, blank=True)  # Google Places ID
    place_types = models.JSONField(default=list, blank=True)  # Types from Google Places
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['trip', 'order']
        unique_together = ['trip', 'order']
    
    def __str__(self):
        name = self.destination.name if self.destination else self.custom_name
        return f"{self.trip.name} - {name} (#{self.order})"
    
    def get_name(self):
        return self.destination.name if self.destination else self.custom_name
    
    def get_address(self):
        if self.destination:
            return f"{self.destination.city}, {self.destination.state.name}"
        return self.custom_address


class PlaceWeatherCache(models.Model):
    """Cache weather information for places"""
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    
    # Weather data
    temperature = models.FloatField()
    description = models.CharField(max_length=200)
    humidity = models.IntegerField()
    wind_speed = models.FloatField()
    icon = models.CharField(max_length=10)
    
    # Cache management
    cached_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['latitude', 'longitude']),
            models.Index(fields=['cached_at']),
        ]
    
    def __str__(self):
        return f"Weather at {self.latitude}, {self.longitude} - {self.temperature}°C"
    
    def is_fresh(self):
        """Check if weather data is less than 1 hour old"""
        from django.utils import timezone
        return (timezone.now() - self.cached_at).seconds < 3600

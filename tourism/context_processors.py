"""
Context processors for tourism app
"""
from django.conf import settings


def api_keys(request):
    """
    Add API keys to template context
    """
    return {
        'MAPBOX_ACCESS_TOKEN': getattr(settings, 'MAPBOX_ACCESS_TOKEN', 'pk.YOUR_MAPBOX_ACCESS_TOKEN_HERE'),
        'GEOAPIFY_API_KEY': getattr(settings, 'GEOAPIFY_API_KEY', 'YOUR_GEOAPIFY_API_KEY'),
        'OPENWEATHER_API_KEY': getattr(settings, 'OPENWEATHER_API_KEY', 'YOUR_OPENWEATHER_API_KEY'),
        'GOOGLE_MAPS_API_KEY': getattr(settings, 'GOOGLE_MAPS_API_KEY', 'YOUR_GOOGLE_MAPS_API_KEY'),
    }
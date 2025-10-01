from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.db import transaction
from django.core.paginator import Paginator
import json
import requests
from decimal import Decimal
from datetime import datetime, timedelta

from .models import Trip, TripDestination, Destination, PlaceWeatherCache
from .forms import TripForm
from django.conf import settings


class TripListView(LoginRequiredMixin, ListView):
    """List user's trips"""
    model = Trip
    template_name = 'tourism/trips/trip_list.html'
    context_object_name = 'trips'
    paginate_by = 12
    
    def get_queryset(self):
        return Trip.objects.filter(
            user=self.request.user, 
            is_active=True
        ).prefetch_related('tripdestination_set__destination')


class TripDetailView(LoginRequiredMixin, DetailView):
    """Detailed view of a trip with map and planning features"""
    model = Trip
    template_name = 'tourism/trips/trip_detail.html'
    context_object_name = 'trip'
    
    def get_queryset(self):
        return Trip.objects.filter(user=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        trip = self.get_object()
        
        # Get trip destinations in order
        destinations = trip.tripdestination_set.select_related(
            'destination__state'
        ).order_by('order')
        
        context.update({
            'trip_destinations': destinations,
            'weather_api_key': settings.OPENWEATHER_API_KEY,
        })
        return context


class TripPlannerView(LoginRequiredMixin, DetailView):
    """Interactive trip planner with map"""
    model = Trip
    template_name = 'tourism/trips/trip_planner.html'
    context_object_name = 'trip'
    
    def get_queryset(self):
        return Trip.objects.filter(user=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        trip = self.get_object()
        
        # Get all destinations for the trip
        trip_destinations = trip.tripdestination_set.select_related(
            'destination__state'
        ).order_by('order')
        
        # Convert to JSON for JavaScript
        destinations_data = []
        for td in trip_destinations:
            destinations_data.append({
                'id': td.id,
                'name': td.get_name(),
                'address': td.get_address(),
                'latitude': float(td.latitude),
                'longitude': float(td.longitude),
                'order': td.order,
                'is_visited': td.is_visited,
                'place_id': td.place_id,
                'planned_date': td.planned_date.isoformat() if td.planned_date else None,
                'notes': td.notes,
            })
        
        context.update({
            'trip_destinations': trip_destinations,
            'destinations_json': json.dumps(destinations_data),
            'weather_api_key': settings.OPENWEATHER_API_KEY,
        })
        return context


@login_required
def create_trip(request):
    """Create a new trip"""
    if request.method == 'POST':
        form = TripForm(request.POST)
        if form.is_valid():
            trip = form.save(commit=False)
            trip.user = request.user
            trip.save()
            messages.success(request, f'Trip "{trip.name}" created successfully!')
            return redirect('tourism:trip_planner', pk=trip.pk)
    else:
        form = TripForm()
    
    return render(request, 'tourism/trips/create_trip.html', {
        'form': form
    })


@require_POST
@login_required
def add_destination_to_trip(request):
    """Add a destination to a trip via AJAX"""
    try:
        data = json.loads(request.body)
        trip_id = data.get('trip_id')
        destination_id = data.get('destination_id')
        custom_name = data.get('custom_name', '')
        custom_address = data.get('custom_address', '')
        latitude = data.get('latitude')
        longitude = data.get('longitude')
        place_id = data.get('place_id', '')
        
        trip = get_object_or_404(Trip, id=trip_id, user=request.user)
        
        # Get the next order number
        last_destination = trip.tripdestination_set.order_by('-order').first()
        next_order = (last_destination.order + 1) if last_destination else 1
        
        # Create trip destination
        trip_destination = TripDestination.objects.create(
            trip=trip,
            destination_id=destination_id if destination_id else None,
            custom_name=custom_name,
            custom_address=custom_address,
            latitude=Decimal(str(latitude)),
            longitude=Decimal(str(longitude)),
            place_id=place_id,
            order=next_order
        )
        
        return JsonResponse({
            'success': True,
            'message': f'Added {trip_destination.get_name()} to your trip!',
            'destination_id': trip_destination.id,
            'order': trip_destination.order,
        })
    
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Error adding destination: {str(e)}'
        }, status=400)


@require_POST
@login_required
def mark_destination_visited(request):
    """Mark a destination as visited"""
    try:
        data = json.loads(request.body)
        destination_id = data.get('destination_id')
        is_visited = data.get('is_visited', True)
        
        trip_destination = get_object_or_404(
            TripDestination, 
            id=destination_id, 
            trip__user=request.user
        )
        
        trip_destination.is_visited = is_visited
        if is_visited:
            trip_destination.visited_at = timezone.now()
        else:
            trip_destination.visited_at = None
        trip_destination.save()
        
        status = "visited" if is_visited else "unvisited"
        return JsonResponse({
            'success': True,
            'message': f'Marked {trip_destination.get_name()} as {status}!',
            'is_visited': trip_destination.is_visited,
        })
    
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Error updating destination: {str(e)}'
        }, status=400)


@require_POST
@login_required
def remove_destination_from_trip(request):
    """Remove a destination from a trip"""
    try:
        data = json.loads(request.body)
        destination_id = data.get('destination_id')
        
        trip_destination = get_object_or_404(
            TripDestination,
            id=destination_id,
            trip__user=request.user
        )
        
        destination_name = trip_destination.get_name()
        trip_destination.delete()
        
        return JsonResponse({
            'success': True,
            'message': f'Removed {destination_name} from your trip!',
        })
    
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Error removing destination: {str(e)}'
        }, status=400)


@require_POST
@login_required
def reorder_destinations(request):
    """Reorder destinations in a trip"""
    try:
        data = json.loads(request.body)
        trip_id = data.get('trip_id')
        destination_orders = data.get('destination_orders')  # List of {id: order}
        
        trip = get_object_or_404(Trip, id=trip_id, user=request.user)
        
        with transaction.atomic():
            for dest_data in destination_orders:
                TripDestination.objects.filter(
                    id=dest_data['id'],
                    trip=trip
                ).update(order=dest_data['order'])
        
        return JsonResponse({
            'success': True,
            'message': 'Destinations reordered successfully!',
        })
    
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Error reordering destinations: {str(e)}'
        }, status=400)


@login_required
def clear_all_trips(request):
    """Clear all user trips by deactivating them"""
    try:
        print(f"Clear trips called by user: {request.user}")
        
        # Check current active trips before clearing
        current_trips = Trip.objects.filter(
            user=request.user, 
            is_active=True
        )
        current_count = current_trips.count()
        print(f"Found {current_count} active trips to clear")
        
        # Set all user trips to inactive instead of deleting them
        trips_count = Trip.objects.filter(
            user=request.user, 
            is_active=True
        ).update(is_active=False)
        
        print(f"Updated {trips_count} trips to inactive")
        
        if trips_count > 0:
            messages.success(request, f'Successfully cleared {trips_count} trip(s)!')
        else:
            messages.info(request, 'No trips to clear.')
        
        return redirect('tourism:trip_list')
    
    except Exception as e:
        print(f"Error clearing trips: {str(e)}")
        messages.error(request, f'Error clearing trips: {str(e)}')
        return redirect('tourism:trip_list')


def get_weather_for_location(request):
    """Get weather information for a location"""
    try:
        latitude = float(request.GET.get('lat'))
        longitude = float(request.GET.get('lng'))
        
        # Check if we have cached weather data
        cache_obj = PlaceWeatherCache.objects.filter(
            latitude=Decimal(str(latitude)),
            longitude=Decimal(str(longitude))
        ).first()
        
        if cache_obj and cache_obj.is_fresh():
            return JsonResponse({
                'success': True,
                'temperature': cache_obj.temperature,
                'description': cache_obj.description,
                'humidity': cache_obj.humidity,
                'wind_speed': cache_obj.wind_speed,
                'icon': cache_obj.icon,
            })
        
        # Fetch from OpenWeather API
        api_key = settings.OPENWEATHER_API_KEY
        url = f"http://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={api_key}&units=metric"
        
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            
            weather_data = {
                'temperature': data['main']['temp'],
                'description': data['weather'][0]['description'].title(),
                'humidity': data['main']['humidity'],
                'wind_speed': data['wind']['speed'],
                'icon': data['weather'][0]['icon'],
            }
            
            # Cache the weather data
            if cache_obj:
                for key, value in weather_data.items():
                    setattr(cache_obj, key, value)
                cache_obj.cached_at = timezone.now()
                cache_obj.save()
            else:
                PlaceWeatherCache.objects.create(
                    latitude=Decimal(str(latitude)),
                    longitude=Decimal(str(longitude)),
                    **weather_data
                )
            
            return JsonResponse({
                'success': True,
                **weather_data
            })
        else:
            return JsonResponse({
                'success': False,
                'message': 'Weather data unavailable'
            }, status=400)
    
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Error fetching weather: {str(e)}'
        }, status=400)


def get_nearby_places(request):
    """Get nearby places using Google Places API"""
    try:
        latitude = request.GET.get('lat')
        longitude = request.GET.get('lng')
        place_type = request.GET.get('type', 'tourist_attraction')
        radius = request.GET.get('radius', '5000')  # 5km default
        
        # Google Places API implementation
        api_key = settings.GOOGLE_MAPS_API_KEY
        
        if api_key and api_key != 'YOUR_GOOGLE_MAPS_API_KEY':
            url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json'
            params = {
                'location': f'{latitude},{longitude}',
                'radius': radius,
                'type': place_type,
                'key': api_key
            }
            
            response = requests.get(url, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                
                nearby_places = []
                for place in data.get('results', [])[:10]:  # Limit to 10 results
                    nearby_places.append({
                        'name': place.get('name', 'Unknown'),
                        'type': place.get('types', [''])[0] if place.get('types') else '',
                        'rating': place.get('rating', 0),
                        'vicinity': place.get('vicinity', ''),
                        'place_id': place.get('place_id', ''),
                        'price_level': place.get('price_level', 0),
                        'is_open': place.get('opening_hours', {}).get('open_now', None)
                    })
                
                return JsonResponse({
                    'success': True,
                    'places': nearby_places
                })
            else:
                return JsonResponse({
                    'success': False,
                    'message': 'Google Places API error'
                }, status=400)
        else:
            # Fallback to mock data if no API key
            nearby_places = [
                {
                    'name': 'Sample Hotel',
                    'type': 'lodging',
                    'rating': 4.5,
                    'vicinity': 'Near your destination',
                    'place_id': 'sample_place_id_1'
                },
                {
                    'name': 'Sample Restaurant', 
                    'type': 'restaurant',
                    'rating': 4.2,
                    'vicinity': 'Local area',
                    'place_id': 'sample_place_id_2'
                }
            ]
            
            return JsonResponse({
                'success': True,
                'places': nearby_places,
                'message': 'Using sample data - configure Google Maps API key for real data'
            })
    
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Error fetching nearby places: {str(e)}'
        }, status=400)


def get_place_details(request):
    """Get detailed information about a place"""
    try:
        place_id = request.GET.get('place_id')
        
        if not place_id:
            return JsonResponse({
                'success': False,
                'message': 'Place ID is required'
            }, status=400)
        
        # Google Places Details API implementation
        api_key = settings.GOOGLE_MAPS_API_KEY
        
        if api_key and api_key != 'YOUR_GOOGLE_MAPS_API_KEY':
            url = 'https://maps.googleapis.com/maps/api/place/details/json'
            params = {
                'place_id': place_id,
                'fields': 'name,formatted_address,formatted_phone_number,website,opening_hours,rating,user_ratings_total,price_level,photos',
                'key': api_key
            }
            
            response = requests.get(url, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                
                if data.get('status') == 'OK':
                    result = data.get('result', {})
                    
                    # Format opening hours
                    opening_hours = []
                    if 'opening_hours' in result:
                        opening_hours = result['opening_hours'].get('weekday_text', [])
                    
                    place_details = {
                        'name': result.get('name', 'Unknown Place'),
                        'address': result.get('formatted_address', 'Address not available'),
                        'phone': result.get('formatted_phone_number', ''),
                        'website': result.get('website', ''),
                        'opening_hours': opening_hours,
                        'rating': result.get('rating', 0),
                        'reviews_count': result.get('user_ratings_total', 0),
                        'price_level': result.get('price_level', 0)
                    }
                    
                    return JsonResponse({
                        'success': True,
                        'place': place_details
                    })
                else:
                    return JsonResponse({
                        'success': False,
                        'message': f'Places API error: {data.get("status")}'
                    }, status=400)
            else:
                return JsonResponse({
                    'success': False,
                    'message': 'Google Places API request failed'
                }, status=400)
        else:
            # Fallback to mock data if no API key
            place_details = {
                'name': 'Sample Place',
                'address': 'Sample Address',
                'phone': '+91 12345 67890',
                'website': 'https://example.com',
                'opening_hours': [
                    'Monday: 9:00 AM – 6:00 PM',
                    'Tuesday: 9:00 AM – 6:00 PM',
                    'Wednesday: 9:00 AM – 6:00 PM',
                    'Thursday: 9:00 AM – 6:00 PM',
                    'Friday: 9:00 AM – 6:00 PM',
                    'Saturday: 9:00 AM – 6:00 PM',
                    'Sunday: Closed'
                ],
                'rating': 4.5,
                'reviews_count': 1234,
                'price_level': 2
            }
            
            return JsonResponse({
                'success': True,
                'place': place_details,
                'message': 'Using sample data - configure Google Maps API key for real data'
            })
    
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Error fetching place details: {str(e)}'
        }, status=400)

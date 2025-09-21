from django.urls import path
from . import views, trip_views

app_name = 'tourism'

urlpatterns = [
    # Home page
    path('', views.HomeView.as_view(), name='home'),
    
    # Destinations
    path('destinations/', views.DestinationListView.as_view(), name='destinations'),
    path('destinations/<slug:slug>/', views.DestinationDetailView.as_view(), name='destination_detail'),
    path('destinations/category/<str:category>/', views.DestinationsByCategoryView.as_view(), name='destinations_by_category'),
    path('destinations/state/<str:state>/', views.DestinationsByStateView.as_view(), name='destinations_by_state'),
    
    # Categories
    path('categories/', views.CategoriesView.as_view(), name='categories'),
    
    # Search
    path('search/', views.SearchView.as_view(), name='search'),
    
    # User-specific views
    path('wishlist/', views.WishlistView.as_view(), name='wishlist'),
    path('my-reviews/', views.MyReviewsView.as_view(), name='my_reviews'),
    
    # AJAX endpoints
    path('api/wishlist/toggle/', views.toggle_wishlist, name='toggle_wishlist'),
    path('api/review/add/', views.add_review, name='add_review'),
    path('api/search/suggestions/', views.search_suggestions, name='search_suggestions'),
    
    # Trip Planning
    path('trips/', trip_views.TripListView.as_view(), name='trip_list'),
    path('trips/create/', trip_views.create_trip, name='create_trip'),
    path('trips/<int:pk>/', trip_views.TripDetailView.as_view(), name='trip_detail'),
    path('trips/<int:pk>/planner/', trip_views.TripPlannerView.as_view(), name='trip_planner'),
    
    # Trip AJAX endpoints
    path('api/trips/add-destination/', trip_views.add_destination_to_trip, name='add_destination_to_trip'),
    path('api/trips/mark-visited/', trip_views.mark_destination_visited, name='mark_destination_visited'),
    path('api/trips/remove-destination/', trip_views.remove_destination_from_trip, name='remove_destination_from_trip'),
    path('api/trips/reorder/', trip_views.reorder_destinations, name='reorder_destinations'),
    
    # Map and weather APIs
    path('api/weather/', trip_views.get_weather_for_location, name='get_weather'),
    path('api/nearby-places/', trip_views.get_nearby_places, name='get_nearby_places'),
    path('api/place-details/', trip_views.get_place_details, name='get_place_details'),
]

from django.urls import path
from . import views

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
]
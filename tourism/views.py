from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, TemplateView
from django.db.models import Q, Count, Avg
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
import json

from .models import Destination, Category, State, Review, Wishlist
from .forms import ReviewForm


class HomeView(TemplateView):
    """Homepage view with featured destinations"""
    template_name = 'tourism/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'featured_destinations': Destination.objects.filter(
                featured=True, is_active=True
            ).select_related('state').prefetch_related('categories')[:6],
            'categories': Category.objects.all().annotate(
                destination_count=Count('destinations')
            ),
            'total_destinations': Destination.objects.filter(is_active=True).count(),
            'total_states': State.objects.annotate(
                destination_count=Count('destination')
            ).filter(destination_count__gt=0).count(),
        })
        return context


class DestinationListView(ListView):
    """List all destinations with filtering and pagination"""
    model = Destination
    template_name = 'tourism/destinations.html'
    context_object_name = 'destinations'
    paginate_by = 12
    
    def get_queryset(self):
        queryset = Destination.objects.filter(
            is_active=True
        ).select_related('state').prefetch_related('categories')
        
        # Search functionality
        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) |
                Q(city__icontains=search_query) |
                Q(state__name__icontains=search_query) |
                Q(description__icontains=search_query) |
                Q(short_description__icontains=search_query)
            )
        
        # Category filtering
        category = self.request.GET.get('category')
        if category:
            queryset = queryset.filter(categories__name=category)
        
        # State filtering
        state = self.request.GET.get('state')
        if state:
            queryset = queryset.filter(state__name=state)
        
        # Rating filtering
        min_rating = self.request.GET.get('rating')
        if min_rating:
            try:
                min_rating = float(min_rating)
                queryset = queryset.filter(average_rating__gte=min_rating)
            except (ValueError, TypeError):
                pass
        
        # Sorting
        sort_by = self.request.GET.get('sort', '-featured')
        valid_sorts = ['-featured', 'name', '-average_rating', '-total_reviews', '-created_at']
        if sort_by in valid_sorts:
            queryset = queryset.order_by(sort_by, 'name')
        
        return queryset.distinct()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'categories': Category.objects.all().annotate(
                destination_count=Count('destinations')
            ),
            'states': State.objects.all().annotate(
                destination_count=Count('destination')
            ).filter(destination_count__gt=0),
            'search_query': self.request.GET.get('search', ''),
            'selected_category': self.request.GET.get('category', ''),
            'selected_state': self.request.GET.get('state', ''),
            'selected_rating': self.request.GET.get('rating', ''),
            'sort_by': self.request.GET.get('sort', '-featured'),
        })
        return context


class DestinationDetailView(DetailView):
    """Detailed view of a single destination"""
    model = Destination
    template_name = 'tourism/destination_detail.html'
    context_object_name = 'destination'
    
    def get_queryset(self):
        return Destination.objects.filter(
            is_active=True
        ).select_related('state').prefetch_related('categories', 'reviews__user')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        destination = self.get_object()
        
        # Get reviews with pagination
        reviews = destination.reviews.select_related('user').order_by('-created_at')
        paginator = Paginator(reviews, 10)
        page_number = self.request.GET.get('page')
        page_reviews = paginator.get_page(page_number)
        
        # Check if user has this in wishlist
        in_wishlist = False
        user_review = None
        if self.request.user.is_authenticated:
            in_wishlist = Wishlist.objects.filter(
                user=self.request.user, destination=destination
            ).exists()
            try:
                user_review = Review.objects.get(
                    user=self.request.user, destination=destination
                )
            except Review.DoesNotExist:
                pass
        
        # Similar destinations
        similar_destinations = Destination.objects.filter(
            categories__in=destination.categories.all(),
            is_active=True
        ).exclude(id=destination.id).distinct()[:4]
        
        context.update({
            'reviews': page_reviews,
            'in_wishlist': in_wishlist,
            'user_review': user_review,
            'review_form': ReviewForm(),
            'similar_destinations': similar_destinations,
        })
        return context


class DestinationsByCategoryView(ListView):
    """Filter destinations by category"""
    model = Destination
    template_name = 'tourism/destinations_by_category.html'
    context_object_name = 'destinations'
    paginate_by = 12
    
    def get_queryset(self):
        self.category = get_object_or_404(Category, name=self.kwargs['category'])
        return Destination.objects.filter(
            categories=self.category, is_active=True
        ).select_related('state').prefetch_related('categories')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context


class DestinationsByStateView(ListView):
    """Filter destinations by state"""
    model = Destination
    template_name = 'tourism/destinations_by_state.html'
    context_object_name = 'destinations'
    paginate_by = 12
    
    def get_queryset(self):
        self.state = get_object_or_404(State, name=self.kwargs['state'])
        return Destination.objects.filter(
            state=self.state, is_active=True
        ).select_related('state').prefetch_related('categories')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['state'] = self.state
        return context


class CategoriesView(TemplateView):
    """Show all tourism categories"""
    template_name = 'tourism/categories.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all().annotate(
            destination_count=Count('destinations', filter=Q(destinations__is_active=True))
        )
        return context


class SearchView(ListView):
    """Advanced search functionality"""
    model = Destination
    template_name = 'tourism/search_results.html'
    context_object_name = 'destinations'
    paginate_by = 12
    
    def get_queryset(self):
        query = self.request.GET.get('q', '').strip()
        if not query:
            return Destination.objects.none()
        
        return Destination.objects.filter(
            Q(name__icontains=query) |
            Q(city__icontains=query) |
            Q(state__name__icontains=query) |
            Q(description__icontains=query) |
            Q(categories__name__icontains=query) |
            Q(local_cuisine__icontains=query) |
            Q(cultural_importance__icontains=query),
            is_active=True
        ).select_related('state').prefetch_related('categories').distinct()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('q', '')
        return context


# User-specific views
class WishlistView(LoginRequiredMixin, ListView):
    """User's wishlist"""
    model = Wishlist
    template_name = 'tourism/wishlist.html'
    context_object_name = 'wishlist_items'
    paginate_by = 12
    
    def get_queryset(self):
        return Wishlist.objects.filter(
            user=self.request.user
        ).select_related('destination__state').prefetch_related('destination__categories')


class MyReviewsView(LoginRequiredMixin, ListView):
    """User's reviews"""
    model = Review
    template_name = 'tourism/my_reviews.html'
    context_object_name = 'reviews'
    paginate_by = 10
    
    def get_queryset(self):
        return Review.objects.filter(
            user=self.request.user
        ).select_related('destination__state').order_by('-created_at')


# AJAX Views
@require_POST
@login_required
def toggle_wishlist(request):
    """Toggle destination in user's wishlist"""
    try:
        data = json.loads(request.body)
        destination_id = data.get('destination_id')
        destination = get_object_or_404(Destination, id=destination_id, is_active=True)
        
        wishlist_item, created = Wishlist.objects.get_or_create(
            user=request.user,
            destination=destination
        )
        
        if created:
            return JsonResponse({
                'success': True,
                'added': True,
                'message': f'Added {destination.name} to your wishlist!'
            })
        else:
            wishlist_item.delete()
            return JsonResponse({
                'success': True,
                'added': False,
                'message': f'Removed {destination.name} from your wishlist!'
            })
    
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': 'Error updating wishlist. Please try again.'
        }, status=400)


@require_POST
@login_required
def add_review(request):
    """Add a review for a destination"""
    try:
        data = json.loads(request.body)
        destination_id = data.get('destination_id')
        rating = data.get('rating')
        title = data.get('title')
        comment = data.get('comment')
        
        destination = get_object_or_404(Destination, id=destination_id, is_active=True)
        
        # Check if user already reviewed this destination
        if Review.objects.filter(user=request.user, destination=destination).exists():
            return JsonResponse({
                'success': False,
                'message': 'You have already reviewed this destination.'
            }, status=400)
        
        # Create review
        review = Review.objects.create(
            user=request.user,
            destination=destination,
            rating=int(rating),
            title=title,
            comment=comment
        )
        
        # Update destination rating
        reviews = Review.objects.filter(destination=destination)
        avg_rating = reviews.aggregate(avg=Avg('rating'))['avg']
        destination.average_rating = round(avg_rating, 2)
        destination.total_reviews = reviews.count()
        destination.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Review added successfully!',
            'review_id': review.id
        })
    
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': 'Error adding review. Please try again.'
        }, status=400)


def search_suggestions(request):
    """AJAX endpoint for search suggestions"""
    query = request.GET.get('q', '').strip()
    suggestions = []
    
    if len(query) >= 2:
        # Get destination suggestions
        destinations = Destination.objects.filter(
            Q(name__icontains=query) | Q(city__icontains=query),
            is_active=True
        ).values_list('name', flat=True)[:5]
        
        # Get state suggestions
        states = State.objects.filter(
            name__icontains=query
        ).values_list('name', flat=True)[:3]
        
        suggestions.extend([{'type': 'destination', 'name': name} for name in destinations])
        suggestions.extend([{'type': 'state', 'name': name} for name in states])
    
    return JsonResponse({'suggestions': suggestions})

# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Project Overview

Smart Digital Tourism Platform for India is a Django 5.2.6 web application that promotes eco, cultural, and heritage tourism across India. The platform features an AI-powered chatbot with voice-to-text capabilities, interactive Google Maps integration, and comprehensive user authentication with destination management.

## Common Commands

### Environment Setup
```powershell
# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Database Management
```powershell
# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Populate database with sample Indian tourism data
python manage.py populate_tourism_data

# Clear existing data and repopulate (use with caution)
python manage.py populate_tourism_data --clear
```

### Development Server
```powershell
# Start development server
python manage.py runserver

# Access points:
# - Main site: http://127.0.0.1:8000/
# - Admin panel: http://127.0.0.1:8000/admin/
```

### Testing and Maintenance
```powershell
# Run tests
python manage.py test

# Run tests for specific app
python manage.py test tourism
python manage.py test accounts
python manage.py test chatbot

# Collect static files (for production)
python manage.py collectstatic

# Check for issues
python manage.py check
```

## Architecture Overview

### Application Structure
The project follows Django's modular app architecture with three main apps:

- **`tourism/`** - Core tourism functionality (destinations, categories, reviews, wishlists)
- **`accounts/`** - User authentication and profile management with extended UserProfile model
- **`chatbot/`** - AI chatbot with voice-to-text integration and analytics tracking

### Key Models Architecture

**Tourism App:**
- `Destination` - Central model with location data, categories (ManyToMany), ratings, and rich tourism information
- `Category` - Tourism types (eco, cultural, religious, adventure, historical, wildlife, beach, mountain)
- `State` - Indian states with code mappings
- `Review` - User reviews with ratings (unique constraint per user/destination)
- `Wishlist` - User favorite destinations

**Accounts App:**
- `UserProfile` - Extended user model with travel preferences, privacy settings, and social media links
- Automatic profile creation via Django signals

**Chatbot App:**
- `ChatSession` - Session management with user context and preferences
- `ChatMessage` - Individual messages with voice/text input types, confidence scores, and entity extraction
- `ChatFeedback` - User feedback on bot responses
- `ChatAnalytics` - Performance metrics and popular topics tracking

### URL Structure
- `/` - Homepage with featured destinations
- `/destinations/` - All destinations with advanced filtering
- `/destinations/<slug>/` - Destination detail pages
- `/destinations/category/<category>/` - Category-filtered destinations
- `/accounts/` - Authentication (login, signup, profile)
- `/chatbot/` - AI assistant interface
- `/admin/` - Django admin panel

## Development Guidelines

### Database Configuration
- Development uses SQLite (`db.sqlite3`)
- Models are optimized with database indexes on frequently queried fields
- Time zone set to `Asia/Kolkata`
- Media files stored in `media/` directory

### Key Features Implementation
- **Search & Filtering**: Advanced QuerySet filtering on destinations by name, location, category, rating
- **Google Maps Integration**: Configured via `GOOGLE_MAPS_API_KEY` environment variable
- **Voice-to-Text**: Web Speech API integration in chatbot
- **Image Handling**: Pillow for image processing, separate main_image and gallery_images fields
- **Ratings System**: Decimal field with validators (0.00-5.00), automatic average calculation

### Template Structure
- Base template at `templates/base.html`
- App-specific templates in `templates/<app_name>/`
- Bootstrap 5 and Font Awesome 6 for styling
- Responsive design with custom CSS animations

### Management Commands
Custom command `populate_tourism_data` creates sample data including:
- Indian states with proper codes
- Tourism categories with Font Awesome icons
- Featured destinations with complete metadata (Taj Mahal, Goa Beaches, Kerala Backwaters, etc.)
- Proper latitude/longitude coordinates for map integration

### API Endpoints
AJAX endpoints for dynamic functionality:
- `/api/wishlist/toggle/` - Add/remove destinations from wishlist
- `/api/review/add/` - Submit destination reviews
- `/api/search/suggestions/` - Search autocomplete

### Production Considerations
- Switch from SQLite to PostgreSQL for production
- Configure static files serving and MEDIA_ROOT
- Set up proper SECRET_KEY and security settings
- Enable SSL with CSRF_COOKIE_SECURE and SESSION_COOKIE_SECURE

### Authentication Flow
- Custom UserProfile automatically created via post_save signals
- Login redirects to homepage, logout to homepage
- Profile includes travel preferences stored as JSON field
- Privacy controls for email and phone visibility

When working with this codebase, remember that destinations are the central entity with rich metadata including cultural significance, historical context, and local cuisine information. The platform emphasizes Indian tourism promotion with pre-populated authentic destination data.
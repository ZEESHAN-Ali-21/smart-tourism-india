# Smart Tourism India

A Django web application for exploring tourist destinations across India with AI-powered assistance and interactive mapping.

## Features

- **Interactive Maps**: Geoapify-powered maps with destination markers
- **Search Functionality**: Live search with location-based results  
- **AI Assistant**: Chatbot for tourism recommendations
- **Destination Catalog**: Browse destinations by categories and states
- **Trip Planning**: Create and manage multi-destination trips
- **User Authentication**: Registration, login, and profile management

## Quick Start

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure API Key**
   - Get free API key from https://www.geoapify.com/
   - Update `geoapify_config.py`:
     ```python
     GEOAPIFY_API_KEY = 'your-actual-api-key-here'
     ```

3. **Run Application**
   ```bash
   python manage.py migrate
   python manage.py runserver
   ```

4. **Access Application**
   - Open http://127.0.0.1:8000 in your browser

## Project Structure

```
smart-tourism-india/
├── accounts/           # User authentication
├── chatbot/           # AI assistant functionality  
├── tourism/           # Main tourism features
│   ├── models.py      # Database models
│   ├── views.py       # View controllers
│   └── templates/     # HTML templates
├── static/            # CSS, JS, images
├── templates/         # Base templates
└── manage.py          # Django management
```

## Technology Stack

- **Backend**: Django 4.2
- **Frontend**: HTML5, CSS3, JavaScript
- **Database**: SQLite (development)
- **Maps**: Geoapify API
- **UI**: Bootstrap 5, Font Awesome

---

Built with Django for exploring India's incredible destinations.

# 🇮🇳 Smart Tourism India

> Discover Incredible India with AI-powered tourism platform featuring beautiful destinations, interactive maps, and personalized recommendations.

[![Django](https://img.shields.io/badge/Django-5.2.6-green.svg)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## ✨ Features

🎥 **Video Background** - Stunning nature videos on homepage  
🗺️ **Interactive Maps** - OpenStreetMap integration with Leaflet.js  
🎨 **Travel Colors** - Ocean blue, forest green, sunset orange theme  
🔍 **Smart Search** - Find destinations with advanced filtering  
⭐ **Reviews & Ratings** - Community-driven destination reviews  
❤️ **Wishlist** - Save favorite destinations  
🤖 **AI Chatbot** - Smart tourism assistance  
📱 **Responsive** - Perfect on all devices  

## 🚀 Quick Start

```bash
# Clone repository
git clone https://github.com/yourusername/smart-tourism-india.git
cd smart-tourism-india

# Setup virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Setup database
python manage.py migrate
python manage.py setup_categories
python manage.py complete_setup

# Run server
python manage.py runserver
```

Visit: http://localhost:8000

## 📸 Screenshots

### 🏠 Homepage with Video Background
Stunning video background with glassmorphism hero section and travel-themed colors.

### 🗺️ Interactive Maps
OpenStreetMap integration with category-based colored markers and destination details.

### 📱 Mobile Responsive
Beautiful responsive design that works perfectly on all screen sizes.

## 🛠️ Tech Stack

- **Backend**: Django 5.2.6, Python 3.8+
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Maps**: OpenStreetMap, Leaflet.js
- **Database**: SQLite (development), PostgreSQL (production)
- **Styling**: Custom CSS with CSS Variables

## 📂 Project Structure

```
smart-tourism-india/
├── 🎯 tourism/          # Main app
├── 👤 accounts/         # Authentication
├── 🤖 chatbot/          # AI features
├── 📄 templates/        # HTML templates
├── 🎨 static/          # CSS, JS, media
│   ├── css/
│   ├── js/
│   ├── images/
│   └── videos/
└── ⚙️ smart_tourism_platform/
```

## 🎨 Color Palette

- **Ocean Blue** (`#0EA5E9`) - Primary color
- **Forest Green** (`#059669`) - Secondary color
- **Sunset Orange** (`#F59E0B`) - Accent color
- **Coral Pink** (`#FB7185`) - Accent color

## 📖 Documentation

For detailed setup instructions, see [SETUP_GUIDE.md](SETUP_GUIDE.md)

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- OpenStreetMap for free mapping data
- Unsplash for beautiful images
- Bootstrap for responsive framework
- Leaflet.js for interactive maps

---

**Made with ❤️ for India's incredible tourism** 🇮🇳

# Smart Digital Tourism Platform for India

A comprehensive web application that promotes eco, cultural, and heritage tourism across India, featuring an AI-powered chatbot with voice-to-text capabilities and interactive Google Maps integration.

## 🌟 Features

### Core Features
- **Secure User Authentication**: Complete registration and login system with user profiles
- **Extensive Tourism Database**: Pre-populated with famous Indian destinations
- **Interactive Google Maps**: Location visualization and navigation features
- **AI-Powered Chatbot**: Voice-to-text enabled assistant for tourism queries
- **Advanced Filtering**: Filter destinations by type (eco, cultural, religious, adventure, historical)
- **Responsive Design**: Modern UI with Bootstrap 5 and custom animations
- **Review System**: User reviews and ratings for destinations
- **Wishlist Functionality**: Save favorite destinations

### Technical Highlights
- **Django 5.2.6**: Modern Python web framework
- **SQLite Database**: Development-ready (PostgreSQL-ready for production)
- **Bootstrap 5**: Responsive frontend framework
- **Font Awesome**: Beautiful UI icons
- **Web Speech API**: Voice-to-text integration
- **Custom CSS Animations**: Smooth user experience
- **AJAX Integration**: Dynamic content loading

## 🛠️ Technology Stack

### Backend
- **Django 5.2.6**: Web framework
- **Python 3.12**: Programming language
- **SQLite**: Database (development)
- **Pillow**: Image processing

### Frontend
- **HTML5**: Markup
- **CSS3**: Styling with custom animations
- **JavaScript (ES6+)**: Interactive functionality
- **Bootstrap 5**: CSS framework
- **Font Awesome 6**: Icons

### APIs & Integrations
- **Google Maps API**: Location services
- **Web Speech API**: Voice recognition

## 🚀 Quick Start

### Prerequisites
- Python 3.8+ installed
- Git installed
- Modern web browser

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd smart-tourism-india
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   ```

3. **Activate virtual environment**
   
   **Windows:**
   ```bash
   venv\Scripts\activate
   ```
   
   **macOS/Linux:**
   ```bash
   source venv/bin/activate
   ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Run database migrations**
   ```bash
   python manage.py migrate
   ```

6. **Populate with sample data**
   ```bash
   python manage.py populate_tourism_data
   ```

7. **Create superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

8. **Run development server**
   ```bash
   python manage.py runserver
   ```

9. **Access the application**
   - Main site: http://127.0.0.1:8000/
   - Admin panel: http://127.0.0.1:8000/admin/

## 📱 Usage

### For Visitors
1. **Browse Destinations**: Explore featured destinations on the homepage
2. **Search & Filter**: Use search bar and category filters to find specific places
3. **View Details**: Click on destinations for detailed information
4. **Interactive Maps**: View locations on Google Maps
5. **AI Assistant**: Use the chatbot for tourism queries with voice input

### For Registered Users
1. **Create Account**: Sign up with email and password
2. **Manage Wishlist**: Save favorite destinations
3. **Write Reviews**: Rate and review visited places
4. **Profile Management**: Update personal information and preferences

### For Administrators
1. **Admin Panel**: Access Django admin at `/admin/`
2. **Manage Content**: Add/edit destinations, categories, and states
3. **User Management**: Monitor user accounts and reviews
4. **Analytics**: View chatbot usage and feedback

## 🗂️ Project Structure

```
smart-tourism-india/
├── accounts/                 # User authentication app
│   ├── models.py            # User profile models
│   ├── views.py             # Authentication views
│   ├── forms.py             # User forms
│   └── urls.py              # Auth URL patterns
├── chatbot/                 # AI chatbot app
│   ├── models.py            # Chat session models
│   ├── views.py             # Chatbot views
│   └── urls.py              # Chatbot URL patterns
├── tourism/                 # Main tourism app
│   ├── models.py            # Destination models
│   ├── views.py             # Tourism views
│   ├── admin.py             # Admin configuration
│   ├── urls.py              # Tourism URL patterns
│   └── management/          # Management commands
│       └── commands/
│           └── populate_tourism_data.py
├── templates/               # HTML templates
│   └── base.html           # Base template
├── static/                  # Static files
│   ├── css/                # Custom stylesheets
│   ├── js/                 # JavaScript files
│   └── images/             # Image assets
├── media/                   # User uploaded files
├── smart_tourism_platform/  # Django project settings
│   ├── settings.py         # Project settings
│   └── urls.py             # Main URL configuration
├── requirements.txt         # Python dependencies
├── manage.py               # Django management script
└── README.md               # This file
```

## 🎯 Key Features Explained

### Destination Categories
- **Eco Tourism**: Nature reserves and eco-friendly destinations
- **Cultural Tourism**: Heritage sites and cultural monuments
- **Religious Tourism**: Temples and pilgrimage sites
- **Adventure Tourism**: Adventure sports and activities
- **Historical Tourism**: Historical monuments and forts
- **Wildlife Tourism**: National parks and sanctuaries
- **Beach Tourism**: Coastal destinations
- **Mountain Tourism**: Hill stations and mountain destinations

### Sample Destinations Included
- Taj Mahal (Uttar Pradesh)
- Goa Beaches (Goa)
- Kerala Backwaters (Kerala)
- Jaipur City Palace (Rajasthan)
- Manali Hill Station (Himachal Pradesh)
- Hampi Archaeological Site (Karnataka)
- Jim Corbett National Park (Uttarakhand)
- Golden Temple (Punjab)
- Leh Ladakh (Jammu & Kashmir)
- Mysore Palace (Karnataka)

### AI Chatbot Capabilities
- **Voice Recognition**: Speak your queries using Web Speech API
- **Tourism Information**: Get details about destinations, culture, food
- **Natural Language Processing**: Understands conversational queries
- **Context Awareness**: Maintains conversation context
- **Feedback System**: Rate chatbot responses

## 🔧 Configuration

### Google Maps Integration
1. Get a Google Maps API key from Google Cloud Console
2. Add the API key to your settings:
   ```python
   GOOGLE_MAPS_API_KEY = 'your-api-key-here'
   ```
3. Enable the following APIs:
   - Maps JavaScript API
   - Places API
   - Geocoding API

### Environment Variables
Create a `.env` file for production settings:
```env
SECRET_KEY=your-secret-key
DEBUG=False
ALLOWED_HOSTS=your-domain.com
DATABASE_URL=your-database-url
GOOGLE_MAPS_API_KEY=your-google-maps-key
```

## 🚀 Deployment

### For Production
1. **Database**: Switch to PostgreSQL
2. **Static Files**: Configure for production serving
3. **Environment**: Set DEBUG=False
4. **Security**: Update SECRET_KEY and security settings

### Recommended Hosting
- **Backend**: Heroku, DigitalOcean, AWS
- **Database**: PostgreSQL on cloud providers
- **Static Files**: AWS S3 or similar CDN

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make changes and commit: `git commit -m 'Add feature'`
4. Push to branch: `git push origin feature-name`
5. Submit a pull request

## 📝 License

This project is developed for educational and tourism promotion purposes.

## 🆘 Support

For issues and questions:
1. Check the documentation
2. Look through existing issues
3. Create a new issue with details

## 🎉 Acknowledgments

- Django community for the excellent framework
- Bootstrap team for the responsive framework
- Font Awesome for beautiful icons
- Indian tourism destinations for inspiration

---

**Made with ❤️ for promoting Indian tourism heritage**
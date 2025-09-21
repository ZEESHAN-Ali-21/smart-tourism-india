# API Setup Guide for Smart Tourism India Trip Planner

This document provides step-by-step instructions for setting up the required API keys for the trip planning functionality.

## Required APIs

### 1. Google Maps API
The trip planner uses several Google Maps services:
- **Maps JavaScript API** - For displaying interactive maps
- **Places API** - For searching and autocomplete functionality
- **Directions API** - For route calculation and navigation
- **Geocoding API** - For address to coordinates conversion

### 2. OpenWeather API
For real-time weather information at destination locations.

---

## Google Maps API Setup

### Step 1: Create Google Cloud Project
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable billing for the project (required for Maps API)

### Step 2: Enable Required APIs
1. Go to **APIs & Services > Library**
2. Search for and enable these APIs:
   - Maps JavaScript API
   - Places API
   - Directions API
   - Geocoding API

### Step 3: Create API Key
1. Go to **APIs & Services > Credentials**
2. Click **+ CREATE CREDENTIALS > API key**
3. Copy the generated API key
4. Click **RESTRICT KEY** to configure restrictions

### Step 4: Configure API Key Restrictions
For security, restrict your API key:

**Application restrictions:**
- Select "HTTP referrers (web sites)"
- Add your domain: `http://localhost:8000/*` (for development)
- Add your production domain when deploying

**API restrictions:**
- Select "Restrict key"
- Choose the APIs you enabled:
  - Maps JavaScript API
  - Places API  
  - Directions API
  - Geocoding API

### Step 5: Configure in Django Settings

Add to your `settings.py`:
```python
# Google Maps API Key
GOOGLE_MAPS_API_KEY = 'YOUR_GOOGLE_MAPS_API_KEY_HERE'
```

Or use environment variables (recommended):
```python
import os
GOOGLE_MAPS_API_KEY = os.getenv('GOOGLE_MAPS_API_KEY', 'YOUR_DEFAULT_KEY')
```

---

## OpenWeather API Setup

### Step 1: Create Account
1. Go to [OpenWeatherMap](https://openweathermap.org/api)
2. Sign up for a free account
3. Verify your email address

### Step 2: Get API Key
1. Go to **API keys** in your account
2. Copy your default API key
3. The free plan includes:
   - 1,000 calls/day
   - Current weather data
   - 5-day forecast

### Step 3: Configure in Django Settings

Add to your `settings.py`:
```python
# OpenWeather API Key
OPENWEATHER_API_KEY = 'YOUR_OPENWEATHER_API_KEY_HERE'
```

Or use environment variables (recommended):
```python
import os
OPENWEATHER_API_KEY = os.getenv('OPENWEATHER_API_KEY', 'YOUR_DEFAULT_KEY')
```

---

## Environment Variables Setup

### Create .env file (Recommended)
Create a `.env` file in your project root:

```env
# Google Maps API
GOOGLE_MAPS_API_KEY=your_google_maps_api_key_here

# OpenWeather API
OPENWEATHER_API_KEY=your_openweather_api_key_here

# Django Settings
SECRET_KEY=your_django_secret_key_here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

### Install python-decouple
```bash
pip install python-decouple
```

### Update settings.py
```python
from decouple import config

# API Keys
GOOGLE_MAPS_API_KEY = config('GOOGLE_MAPS_API_KEY')
OPENWEATHER_API_KEY = config('OPENWEATHER_API_KEY')

# Django Settings
SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost,127.0.0.1').split(',')
```

### Update .gitignore
Add to `.gitignore` to keep API keys secure:
```
.env
*.env
```

---

## Code Updates Required

### Update trip_views.py
Replace the placeholder API keys:

```python
# In get_weather_for_location function
api_key = settings.OPENWEATHER_API_KEY

# In trip planner templates
def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context.update({
        'google_maps_api_key': settings.GOOGLE_MAPS_API_KEY,
        'weather_api_key': settings.OPENWEATHER_API_KEY,
    })
    return context
```

### Update settings.py imports
```python
from django.conf import settings
import os
from decouple import config

# API Configuration
GOOGLE_MAPS_API_KEY = config('GOOGLE_MAPS_API_KEY')
OPENWEATHER_API_KEY = config('OPENWEATHER_API_KEY')
```

---

## Testing the APIs

### Test Google Maps API
1. Open browser developer tools
2. Go to trip planner page
3. Check console for any Maps API errors
4. Test place search functionality

### Test OpenWeather API  
1. Click on any destination marker
2. Select "Weather" from dropdown
3. Verify weather information displays

### Test Places API
1. Use the destination search box
2. Verify autocomplete suggestions appear
3. Test adding destinations to trip

---

## API Usage Limits

### Google Maps API (Free Tier)
- Maps JavaScript API: 28,000 loads/month
- Places API: $17/1000 requests (first $200/month free)
- Directions API: $5/1000 requests (first $200/month free)
- Geocoding API: $5/1000 requests (first $200/month free)

### OpenWeather API (Free Tier)
- 1,000 calls/day
- 60 calls/minute
- Current weather data included

---

## Troubleshooting

### Common Google Maps Issues
1. **Map not loading**: Check API key and referrer restrictions
2. **Search not working**: Verify Places API is enabled
3. **No routes showing**: Check Directions API is enabled
4. **Quota exceeded**: Monitor usage in Google Cloud Console

### Common Weather API Issues
1. **Weather not loading**: Verify API key is correct
2. **Location not found**: Check coordinates format
3. **Rate limited**: Wait or upgrade plan

### Debug Tips
1. Check browser console for JavaScript errors
2. Verify API keys in network requests
3. Test APIs directly with curl/Postman
4. Check Django debug toolbar for backend errors

---

## Security Best Practices

1. **Never commit API keys** to version control
2. **Use environment variables** for all sensitive data
3. **Restrict API keys** to specific domains/IPs
4. **Monitor API usage** regularly
5. **Rotate API keys** periodically
6. **Use HTTPS** in production
7. **Enable API quotas** to prevent abuse

---

## Production Deployment

### Update API Key Restrictions
1. Add your production domain to Google Maps referrer restrictions
2. Update CORS settings for API requests
3. Use environment variables on your hosting platform

### Environment Variables on Common Platforms

**Heroku:**
```bash
heroku config:set GOOGLE_MAPS_API_KEY=your_key_here
heroku config:set OPENWEATHER_API_KEY=your_key_here
```

**DigitalOcean App Platform:**
Add in app spec or environment variables section

**AWS Elastic Beanstalk:**
Set in Configuration > Software > Environment properties

---

## Cost Estimation

### Development (Free Tiers)
- Google Maps: $200 credit (enough for development)
- OpenWeather: Free up to 1,000 calls/day

### Production (Estimated Monthly)
- Google Maps: $20-50/month (depends on usage)
- OpenWeather: $0-40/month (depends on calls)

### Optimization Tips
1. Cache weather data for 1 hour
2. Limit map reloads
3. Use batch requests when possible
4. Implement request throttling
5. Monitor and set usage alerts

---

## Support

For API-specific issues:
- [Google Maps Platform Support](https://developers.google.com/maps/support)
- [OpenWeather Support](https://openweathermap.org/support)

For application issues:
- Check the Django logs
- Review browser console errors
- Test individual API endpoints
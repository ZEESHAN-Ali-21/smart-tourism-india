from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
import json
import uuid
import re
from datetime import datetime

from .models import ChatSession, ChatMessage, ChatFeedback
from tourism.models import Destination, Category, State


class ChatView(TemplateView):
    """Main chatbot interface"""
    template_name = 'chatbot/chat.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'AI Tourism Assistant'
        return context


@csrf_exempt
@require_POST
def send_message(request):
    """Process user messages and return AI responses"""
    try:
        data = json.loads(request.body)
        user_message = data.get('message', '').strip()
        session_id = data.get('session_id')
        input_type = data.get('input_type', 'text')  # 'text' or 'voice'
        
        if not user_message:
            return JsonResponse({
                'success': False,
                'message': 'Message cannot be empty'
            }, status=400)
        
        # Get or create chat session
        if not session_id:
            session_id = str(uuid.uuid4())
        
        chat_session, created = ChatSession.objects.get_or_create(
            session_id=session_id,
            defaults={
                'user': request.user if request.user.is_authenticated else None,
                'user_location': request.META.get('HTTP_X_FORWARDED_FOR', ''),
            }
        )
        
        # Save user message
        user_chat_message = ChatMessage.objects.create(
            session=chat_session,
            message_type='user',
            input_type=input_type,
            message=user_message
        )
        
        # Generate AI response
        ai_response, intent, entities = generate_ai_response(user_message)
        
        # Save AI response
        bot_chat_message = ChatMessage.objects.create(
            session=chat_session,
            message_type='bot',
            message=ai_response,
            intent_detected=intent,
            entities_extracted=entities,
            confidence_score=0.85  # Simulated confidence
        )
        
        return JsonResponse({
            'success': True,
            'response': ai_response,
            'session_id': session_id,
            'message_id': bot_chat_message.id,
            'intent': intent
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': 'Sorry, I\'m having trouble right now. Please try again.'
        }, status=500)


@csrf_exempt
def voice_to_text(request):
    """Handle voice-to-text conversion (placeholder for Web Speech API)"""
    # In a real implementation, this would process audio data
    # For now, we'll return a success response as the Web Speech API
    # handles the voice-to-text conversion on the frontend
    return JsonResponse({
        'success': True,
        'message': 'Voice recognition ready'
    })


def get_chat_history(request):
    """Retrieve chat history for a session"""
    session_id = request.GET.get('session_id')
    if not session_id:
        return JsonResponse({'messages': []})
    
    try:
        chat_session = ChatSession.objects.get(session_id=session_id)
        messages = chat_session.messages.order_by('created_at').values(
            'message_type', 'message', 'created_at', 'input_type'
        )
        
        return JsonResponse({
            'success': True,
            'messages': list(messages)
        })
    except ChatSession.DoesNotExist:
        return JsonResponse({'messages': []})


@require_POST
def submit_feedback(request):
    """Submit feedback for bot responses"""
    try:
        data = json.loads(request.body)
        message_id = data.get('message_id')
        feedback_type = data.get('feedback_type')
        comment = data.get('comment', '')
        
        message = ChatMessage.objects.get(id=message_id, message_type='bot')
        
        ChatFeedback.objects.create(
            message=message,
            user=request.user if request.user.is_authenticated else None,
            feedback_type=feedback_type,
            comment=comment
        )
        
        return JsonResponse({
            'success': True,
            'message': 'Thank you for your feedback!'
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': 'Error submitting feedback'
        }, status=400)


def generate_ai_response(user_message):
    """Generate AI response based on user input"""
    user_message_lower = user_message.lower()
    intent = 'general'
    entities = {}
    
    # Intent detection and response generation
    if any(word in user_message_lower for word in ['hello', 'hi', 'hey', 'good morning', 'good afternoon']):
        intent = 'greeting'
        response = "Hello! I'm your AI tourism assistant for India. I can help you discover amazing destinations, learn about Indian culture, food, and plan your travels. What would you like to know?"
    
    elif any(word in user_message_lower for word in ['destination', 'place', 'visit', 'travel', 'go']):
        intent = 'destination_inquiry'
        response = get_destination_response(user_message_lower)
        entities = extract_destination_entities(user_message_lower)
    
    elif any(word in user_message_lower for word in ['food', 'cuisine', 'eat', 'dish', 'restaurant']):
        intent = 'food_inquiry'
        response = get_food_response(user_message_lower)
    
    elif any(word in user_message_lower for word in ['culture', 'festival', 'tradition', 'custom']):
        intent = 'culture_inquiry'
        response = get_culture_response(user_message_lower)
    
    elif any(word in user_message_lower for word in ['weather', 'climate', 'temperature', 'season']):
        intent = 'weather_inquiry'
        response = get_weather_response(user_message_lower)
    
    elif any(word in user_message_lower for word in ['hotel', 'accommodation', 'stay', 'book']):
        intent = 'accommodation_inquiry'
        response = "For accommodations, I recommend checking popular booking platforms. Most Indian destinations offer a range of options from budget guesthouses to luxury hotels. Would you like recommendations for a specific destination?"
    
    elif any(word in user_message_lower for word in ['transport', 'how to reach', 'train', 'flight', 'bus']):
        intent = 'transport_inquiry'
        response = "India has an extensive transportation network. You can travel by trains (Indian Railways), flights (domestic airlines), buses (state and private), or taxis. Which destination are you planning to visit? I can provide specific transport details."
    
    elif any(word in user_message_lower for word in ['thank', 'thanks']):
        intent = 'gratitude'
        response = "You're welcome! I'm happy to help you explore India's amazing destinations. Feel free to ask me anything else about Indian tourism!"
    
    elif any(word in user_message_lower for word in ['bye', 'goodbye', 'see you']):
        intent = 'farewell'
        response = "Goodbye! Have a wonderful time exploring India. Remember, I'm here whenever you need tourism advice. Safe travels!"
    
    else:
        intent = 'general'
        response = "I'm here to help with Indian tourism! You can ask me about destinations, food, culture, weather, or travel tips. Try asking something like 'Tell me about Taj Mahal' or 'What's the best food in Kerala?'"
    
    return response, intent, entities


def get_destination_response(user_message):
    """Generate response for destination queries"""
    # Try to find specific destinations mentioned
    destinations = Destination.objects.filter(is_active=True)
    
    # Check for specific destination names
    for destination in destinations[:20]:  # Limit to avoid performance issues
        if destination.name.lower() in user_message or destination.city.lower() in user_message:
            return f"""✈️ **{destination.name}** is a {', '.join([cat.get_name_display() for cat in destination.categories.all()])} destination in {destination.state.name}!

📍 **Location**: {destination.city}, {destination.state.name}
⭐ **Rating**: {destination.average_rating}/5.0 ({destination.total_reviews} reviews)

📝 **About**: {destination.short_description}

🕒 **Best time to visit**: {destination.best_time_to_visit or 'Year-round'}
💰 **Entry fee**: {destination.entry_fee or 'Varies'}

Would you like to know more about the local culture, food, or how to reach there?"""
    
    # Check for categories
    categories = Category.objects.all()
    for category in categories:
        category_display = category.get_name_display().lower()
        if category_display in user_message or category.name in user_message:
            destinations_count = category.destinations.filter(is_active=True).count()
            sample_destinations = category.destinations.filter(is_active=True)[:3]
            
            response = f"🌟 **{category.get_name_display()}** destinations in India:\n\n"
            response += f"We have {destinations_count} amazing {category_display} destinations! Here are some highlights:\n\n"
            
            for dest in sample_destinations:
                response += f"• **{dest.name}** in {dest.state.name} - {dest.short_description}\n"
            
            response += "\nWould you like detailed information about any of these places?"
            return response
    
    # Check for states
    states = State.objects.filter(destination__is_active=True).distinct()
    for state in states:
        if state.name.lower() in user_message:
            destinations_count = state.destination_set.filter(is_active=True).count()
            sample_destinations = state.destination_set.filter(is_active=True)[:3]
            
            response = f"🏛️ **{state.name}** has {destinations_count} wonderful destinations:\n\n"
            
            for dest in sample_destinations:
                response += f"• **{dest.name}** - {dest.short_description}\n"
            
            response += f"\nWould you like to know more about any destination in {state.name}?"
            return response
    
    # General destination response
    return """🇮🇳 India offers incredible diversity in tourism! We have destinations for:

🌿 **Eco Tourism** - Kerala Backwaters, Jim Corbett National Park
🏛️ **Historical Sites** - Taj Mahal, Hampi, Red Fort
⛩️ **Religious Places** - Golden Temple, Varanasi, Tirupati
🏔️ **Adventure Sports** - Manali, Leh Ladakh, Rishikesh
🏖️ **Beach Destinations** - Goa, Andaman Islands
🎭 **Cultural Heritage** - Rajasthan, Tamil Nadu

What type of experience are you looking for?"""


def get_food_response(user_message):
    """Generate response for food queries"""
    # Check for specific states/regions
    if any(word in user_message for word in ['kerala', 'south indian']):
        return """🍛 **Kerala Cuisine** is famous for:
• **Appam with Stew** - Fermented rice pancakes
• **Fish Curry** - Coconut-based curry
• **Puttu** - Steamed rice cake
• **Payasam** - Traditional dessert
• **Toddy** - Palm wine (alcoholic)

Kerala cuisine uses lots of coconut, spices, and fresh seafood! 🥥🐟"""
    
    elif any(word in user_message for word in ['rajasthan', 'rajasthani']):
        return """🍽️ **Rajasthani Cuisine** highlights:
• **Dal Baati Churma** - Lentils with baked wheat balls
• **Laal Maas** - Spicy red meat curry
• **Gatte ki Sabzi** - Gram flour dumplings
• **Ghevar** - Traditional sweet
• **Ker Sangri** - Desert vegetable curry

Perfect for the desert climate with rich, hearty flavors! 🌶️🔥"""
    
    else:
        return """🍛 **Indian Cuisine** is incredibly diverse! Each region has specialties:

**North India**: Butter Chicken, Naan, Biryani
**South India**: Dosa, Idli, Sambar, Coconut Curries
**West India**: Dhokla, Vada Pav, Thali
**East India**: Fish Curry, Rasgulla, Mishti Doi

Which region's cuisine interests you most? I can share specific dishes and where to try them! 🌶️✨"""


def get_culture_response(user_message):
    """Generate response for culture queries"""
    return """🎭 **Indian Culture** is rich and diverse:

**Festivals**: Diwali (Festival of Lights), Holi (Colors), Eid, Christmas, Durga Puja
**Languages**: 22 official languages, Hindi and English widely spoken
**Arts**: Classical dance (Bharatanatyam, Kathak), Music (Hindustani, Carnatic)
**Architecture**: Mughal, Dravidian, Indo-Islamic styles
**Traditions**: Yoga, Ayurveda, meditation originated here

**Regional Diversity**:
• North: Bollywood, vibrant festivals
• South: Classical arts, temple architecture
• West: Business hub, diverse communities
• East: Literature, intellectual traditions

Which aspect of Indian culture would you like to explore? 🕉️🎨"""


def get_weather_response(user_message):
    """Generate response for weather queries"""
    return """🌤️ **India's Climate** varies by region and season:

**Seasons**:
• **Winter** (Nov-Feb): Cool, pleasant - Best for most travel
• **Summer** (Mar-May): Hot, dry - Hill stations are popular
• **Monsoon** (Jun-Sep): Rain, humid - Great for nature lovers

**Regional Weather**:
• **North**: Extreme temperatures, cold winters
• **South**: Tropical, moderate temperatures
• **Coastal**: Humid, sea breeze
• **Mountains**: Cool, snow in winter

**Best Travel Times**:
• **Golden Triangle**: October-March
• **Kerala**: September-March
• **Goa**: November-February
• **Himalayas**: April-June, September-November

Which destination's weather would you like to know about? 🌡️❄️☀️"""


def extract_destination_entities(user_message):
    """Extract destination-related entities from user message"""
    entities = {
        'destinations': [],
        'categories': [],
        'states': [],
    }
    
    # Extract destination names
    destinations = Destination.objects.filter(is_active=True)
    for dest in destinations:
        if dest.name.lower() in user_message:
            entities['destinations'].append(dest.name)
    
    # Extract categories
    categories = Category.objects.all()
    for cat in categories:
        if cat.name in user_message or cat.get_name_display().lower() in user_message:
            entities['categories'].append(cat.name)
    
    # Extract states
    states = State.objects.all()
    for state in states:
        if state.name.lower() in user_message:
            entities['states'].append(state.name)
    
    return entities

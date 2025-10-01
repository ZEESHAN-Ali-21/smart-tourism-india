from django import template
from django.templatetags.static import static
import hashlib

register = template.Library()

# Beautiful gradient colors for different destination categories
CATEGORY_GRADIENTS = {
    'eco': 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
    'cultural': 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
    'religious': 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)',
    'adventure': 'linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)',
    'historical': 'linear-gradient(135deg, #fa709a 0%, #fee140 100%)',
    'wildlife': 'linear-gradient(135deg, #30cfd0 0%, #91a7ff 100%)',
    'beach': 'linear-gradient(135deg, #a8edea 0%, #fed6e3 100%)',
    'mountain': 'linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%)',
}

# Icons for different categories
CATEGORY_ICONS = {
    'eco': 'fas fa-leaf',
    'cultural': 'fas fa-university', 
    'religious': 'fas fa-place-of-worship',
    'adventure': 'fas fa-mountain',
    'historical': 'fas fa-monument',
    'wildlife': 'fas fa-paw',
    'beach': 'fas fa-umbrella-beach',
    'mountain': 'fas fa-mountain',
}

# Unsplash image URLs for destinations
DESTINATION_IMAGES = {
    'taj-mahal': 'https://images.unsplash.com/photo-1564507592333-c60657eea523?w=800&q=80',
    'goa-beaches': 'https://images.unsplash.com/photo-1512343879784-a960bf40e7f2?w=800&q=80', 
    'kerala-backwaters': 'https://images.unsplash.com/photo-1602216056096-3b40cc0c9944?w=800&q=80',
    'jaipur-city-palace': 'https://images.unsplash.com/photo-1599661046827-dacde6a26d6f?w=800&q=80',
    'manali-hill-station': 'https://images.unsplash.com/photo-1583160225469-5c6c6b74c6dc?w=800&q=80',
    'red-fort': 'https://images.unsplash.com/photo-1587474260584-136574528ed5?w=800&q=80',
    'varanasi-ghats': 'https://images.unsplash.com/photo-1561361513-2d000a50f0dc?w=800&q=80',
    'ranthambore-national-park': 'https://images.unsplash.com/photo-1614027164847-1b28cfe1df60?w=800&q=80',
    'munnar-tea-gardens': 'https://images.unsplash.com/photo-1610375461246-83df859d849d?w=800&q=80',
    'ajanta-ellora-caves': 'https://images.unsplash.com/photo-1578895210033-6c8cac14a4e0?w=800&q=80',
    'ooty-hill-station': 'https://images.unsplash.com/photo-1594736797933-d0301ba6fe65?w=800&q=80',
    'andaman-islands': 'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=800&q=80',
    'hampi-archaeological-site': 'https://images.unsplash.com/photo-1578895210033-6c8cac14a4e0?w=800&q=80',
    'jim-corbett-national-park': 'https://images.unsplash.com/photo-1580330119133-203d1c37b519?w=800&q=80',
    'golden-temple': 'https://images.unsplash.com/photo-1599837565318-67429bde7162?w=800&q=80',
    'leh-ladakh': 'https://images.unsplash.com/photo-1583160225469-5c6c6b74c6dc?w=800&q=80',
    'mysore-palace': 'https://images.unsplash.com/photo-1599661046827-dacde6a26d6f?w=800&q=80',
}


@register.filter
def destination_image_url(destination):
    """Get the image URL for a destination with fallback to high-quality stock images"""
    
    # If destination has a real uploaded image, use it
    if destination.main_image and hasattr(destination.main_image, 'url'):
        return destination.main_image.url
    
    # Use predefined high-quality images for known destinations
    if destination.slug in DESTINATION_IMAGES:
        return DESTINATION_IMAGES[destination.slug]
    
    # Fallback to placeholder service with destination name
    destination_name = destination.name.replace(' ', '+')
    return f"https://via.placeholder.com/800x400/4F46E5/FFFFFF?text={destination_name}"


@register.filter
def destination_gradient(destination):
    """Get gradient background for destination based on its categories"""
    if not destination.categories.exists():
        return CATEGORY_GRADIENTS.get('cultural', CATEGORY_GRADIENTS['cultural'])
    
    # Use the first category's gradient
    first_category = destination.categories.first()
    return CATEGORY_GRADIENTS.get(first_category.name, CATEGORY_GRADIENTS['cultural'])


@register.filter
def category_icon(category):
    """Get icon class for category"""
    if hasattr(category, 'name'):
        return CATEGORY_ICONS.get(category.name, 'fas fa-map-marker-alt')
    return CATEGORY_ICONS.get(category, 'fas fa-map-marker-alt')


@register.filter
def destination_thumbnail(destination, size="400x300"):
    """Get thumbnail URL for destination with specified size"""
    
    # If destination has a real uploaded image, use it
    if destination.main_image and hasattr(destination.main_image, 'url'):
        return destination.main_image.url
    
    # Use predefined images with size parameter
    if destination.slug in DESTINATION_IMAGES:
        base_url = DESTINATION_IMAGES[destination.slug]
        # Replace size in Unsplash URL
        if 'unsplash.com' in base_url:
            return base_url.replace('w=800&q=80', f'w={size.split("x")[0]}&h={size.split("x")[1]}&q=80&fit=crop')
    
    # Fallback placeholder
    width, height = size.split('x')
    destination_name = destination.name.replace(' ', '+')
    return f"https://via.placeholder.com/{width}x{height}/4F46E5/FFFFFF?text={destination_name}"


@register.simple_tag
def destination_gallery_images(destination, count=3):
    """Get gallery images for destination"""
    if destination.gallery_images:
        return destination.gallery_images[:count]
    
    # Generate multiple images with different filters for variety
    base_slug = destination.slug
    gallery = []
    
    for i in range(count):
        if base_slug in DESTINATION_IMAGES:
            url = DESTINATION_IMAGES[base_slug]
            # Add variation parameters to Unsplash URLs
            if 'unsplash.com' in url:
                variations = ['&sat=-20', '&con=20', '&bright=10']
                if i < len(variations):
                    url += variations[i]
            gallery.append(url)
        else:
            # Fallback variations
            colors = ['4F46E5', '7C3AED', '059669']
            color = colors[i % len(colors)]
            gallery.append(f"https://via.placeholder.com/600x400/{color}/FFFFFF?text={destination.name.replace(' ', '+')}")
    
    return gallery


@register.inclusion_tag('tourism/includes/destination_card.html')
def destination_card(destination, show_description=True, card_class=""):
    """Render a beautiful destination card"""
    return {
        'destination': destination,
        'show_description': show_description,
        'card_class': card_class,
    }
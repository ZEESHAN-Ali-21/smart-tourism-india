from django.core.management.base import BaseCommand
from tourism.models import Category


class Command(BaseCommand):
    help = 'Setup categories with proper icons and descriptions'

    def handle(self, *args, **options):
        # Define category data with icons and descriptions
        categories_data = {
            'cultural': {
                'icon': 'fas fa-landmark',
                'description': 'Explore rich cultural heritage, traditions, and local customs. Experience authentic Indian culture through festivals, art, music, and traditional practices.',
                'color': '#667eea'
            },
            'historical': {
                'icon': 'fas fa-monument', 
                'description': 'Discover ancient monuments, forts, palaces, and archaeological sites that tell the story of India\'s glorious past.',
                'color': '#f093fb'
            },
            'religious': {
                'icon': 'fas fa-place-of-worship',
                'description': 'Visit sacred temples, monasteries, churches, and spiritual centers that showcase India\'s diverse religious traditions.',
                'color': '#4facfe'
            },
            'adventure': {
                'icon': 'fas fa-hiking',
                'description': 'Experience thrilling activities like trekking, mountaineering, rafting, and extreme sports in India\'s diverse landscapes.',
                'color': '#43e97b'
            },
            'wildlife': {
                'icon': 'fas fa-paw',
                'description': 'Encounter exotic wildlife in national parks and sanctuaries. See tigers, elephants, leopards, and diverse bird species.',
                'color': '#fa709a'
            },
            'beach': {
                'icon': 'fas fa-umbrella-beach',
                'description': 'Relax on pristine beaches, enjoy water sports, and experience coastal life along India\'s extensive coastline.',
                'color': '#a8edea'
            },
            'mountain': {
                'icon': 'fas fa-mountain',
                'description': 'Explore majestic hill stations, snow-capped peaks, and scenic mountain landscapes from the Himalayas to Western Ghats.',
                'color': '#d299c2'
            },
            'eco': {
                'icon': 'fas fa-leaf',
                'description': 'Experience sustainable tourism in pristine natural environments, forest reserves, and eco-friendly destinations.',
                'color': '#89f7fe'
            }
        }

        for category_name, data in categories_data.items():
            category, created = Category.objects.get_or_create(name=category_name)
            
            # Update category data
            category.icon = data['icon']
            category.description = data['description']
            category.save()
            
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Created category: {category.get_name_display()}')
                )
            else:
                self.stdout.write(f'Updated category: {category.get_name_display()}')

        self.stdout.write(
            self.style.SUCCESS('Successfully setup all categories!')
        )
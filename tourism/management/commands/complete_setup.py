from django.core.management.base import BaseCommand
from django.core.management import call_command


class Command(BaseCommand):
    help = 'Complete setup of tourism data with images and categories'

    def handle(self, *args, **options):
        self.stdout.write('🚀 Starting complete tourism setup...\n')
        
        # Step 1: Create sample destinations
        self.stdout.write('📍 Creating sample destinations...')
        call_command('create_sample_destinations')
        
        # Step 2: Setup categories
        self.stdout.write('\n🏷️  Setting up categories...')
        call_command('setup_categories')
        
        # Step 3: Create local placeholder images
        self.stdout.write('\n🎨 Creating beautiful placeholder images...')
        call_command('create_local_placeholders')
        
        # Step 4: Try to add real images from external sources
        self.stdout.write('\n🖼️  Attempting to add real images...')
        try:
            call_command('add_sample_destination_images')
        except Exception as e:
            self.stdout.write(
                self.style.WARNING(f'Some external images failed to load: {e}')
            )
        
        self.stdout.write('\n✅ Complete setup finished!')
        self.stdout.write('🎉 Your Smart Tourism India app is ready with beautiful destination cards!')
        
        # Display summary
        from tourism.models import Destination, Category
        dest_count = Destination.objects.count()
        dest_with_images = Destination.objects.exclude(main_image='').count()
        cat_count = Category.objects.count()
        
        self.stdout.write(f'\n📊 Setup Summary:')
        self.stdout.write(f'   • {dest_count} destinations created')
        self.stdout.write(f'   • {dest_with_images} destinations have images')
        self.stdout.write(f'   • {cat_count} categories configured')
        self.stdout.write(f'\n🌟 Run "python manage.py runserver" to see your beautiful destination cards!')
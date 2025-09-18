from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from tourism.models import Category, State, Destination
from decimal import Decimal
import random


class Command(BaseCommand):
    help = 'Populate the database with sample Indian tourism destinations'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing tourism data before populating',
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write(self.style.WARNING('Clearing existing tourism data...'))
            Destination.objects.all().delete()
            Category.objects.all().delete()
            State.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('Cleared existing data.'))

        self.create_categories()
        self.create_states()
        self.create_destinations()
        
        self.stdout.write(
            self.style.SUCCESS('Successfully populated tourism database!')
        )

    def create_categories(self):
        """Create tourism categories"""
        categories_data = [
            ('eco', 'Eco-friendly destinations and nature reserves', 'fas fa-leaf'),
            ('cultural', 'Cultural heritage sites and monuments', 'fas fa-university'),
            ('religious', 'Religious temples and pilgrimage sites', 'fas fa-place-of-worship'),
            ('adventure', 'Adventure sports and activities', 'fas fa-mountain'),
            ('historical', 'Historical monuments and forts', 'fas fa-monument'),
            ('wildlife', 'National parks and wildlife sanctuaries', 'fas fa-paw'),
            ('beach', 'Coastal destinations and beaches', 'fas fa-umbrella-beach'),
            ('mountain', 'Hill stations and mountain destinations', 'fas fa-mountain'),
        ]
        
        for name, description, icon in categories_data:
            category, created = Category.objects.get_or_create(
                name=name,
                defaults={'description': description, 'icon': icon}
            )
            if created:
                self.stdout.write(f'Created category: {category.get_name_display()}')

    def create_states(self):
        """Create Indian states"""
        states_data = [
            ('Andhra Pradesh', 'AP'),
            ('Arunachal Pradesh', 'AR'),
            ('Assam', 'AS'),
            ('Bihar', 'BR'),
            ('Chhattisgarh', 'CG'),
            ('Delhi', 'DL'),
            ('Goa', 'GA'),
            ('Gujarat', 'GJ'),
            ('Haryana', 'HR'),
            ('Himachal Pradesh', 'HP'),
            ('Jammu and Kashmir', 'JK'),
            ('Jharkhand', 'JH'),
            ('Karnataka', 'KA'),
            ('Kerala', 'KL'),
            ('Madhya Pradesh', 'MP'),
            ('Maharashtra', 'MH'),
            ('Manipur', 'MN'),
            ('Meghalaya', 'ML'),
            ('Mizoram', 'MZ'),
            ('Nagaland', 'NL'),
            ('Odisha', 'OR'),
            ('Punjab', 'PB'),
            ('Rajasthan', 'RJ'),
            ('Sikkim', 'SK'),
            ('Tamil Nadu', 'TN'),
            ('Telangana', 'TG'),
            ('Tripura', 'TR'),
            ('Uttar Pradesh', 'UP'),
            ('Uttarakhand', 'UK'),
            ('West Bengal', 'WB'),
        ]
        
        for name, code in states_data:
            state, created = State.objects.get_or_create(
                name=name,
                defaults={'code': code}
            )
            if created:
                self.stdout.write(f'Created state: {name}')

    def create_destinations(self):
        """Create sample destinations"""
        destinations_data = [
            {
                'name': 'Taj Mahal',
                'slug': 'taj-mahal',
                'state': 'Uttar Pradesh',
                'city': 'Agra',
                'categories': ['historical', 'cultural'],
                'description': 'The Taj Mahal is an ivory-white marble mausoleum on the right bank of the river Yamuna in the Indian city of Agra. It was commissioned in 1632 by the Mughal emperor Shah Jahan to house the tomb of his favourite wife, Mumtaz Mahal.',
                'short_description': 'Iconic white marble mausoleum and UNESCO World Heritage Site',
                'latitude': Decimal('27.1751'),
                'longitude': Decimal('78.0421'),
                'best_time_to_visit': 'October to March',
                'entry_fee': '₹50 for Indians, ₹1100 for foreigners',
                'opening_hours': '6:00 AM to 6:30 PM (Closed on Fridays)',
                'historical_significance': 'Built by Emperor Shah Jahan as a symbol of eternal love for his wife Mumtaz Mahal.',
                'cultural_importance': 'Symbol of India and Mughal architecture, UNESCO World Heritage Site.',
                'local_cuisine': 'Agra Petha, Bedai, Jalebi, Mughlai cuisine',
                'featured': True,
                'average_rating': Decimal('4.8'),
                'total_reviews': 12543,
            },
            {
                'name': 'Goa Beaches',
                'slug': 'goa-beaches',
                'state': 'Goa',
                'city': 'Panaji',
                'categories': ['beach', 'adventure'],
                'description': 'Goa is known for its pristine beaches, vibrant nightlife, and Portuguese colonial architecture. The state offers a perfect blend of sun, sand, and sea along with rich cultural heritage.',
                'short_description': 'Pristine beaches with vibrant nightlife and Portuguese heritage',
                'latitude': Decimal('15.2993'),
                'longitude': Decimal('74.1240'),
                'best_time_to_visit': 'November to March',
                'entry_fee': 'Free',
                'opening_hours': '24 hours',
                'historical_significance': 'Former Portuguese colony with 450 years of Portuguese rule.',
                'cultural_importance': 'Unique Indo-Portuguese culture, churches, and festivals.',
                'local_cuisine': 'Fish Curry Rice, Bebinca, Feni, Vindaloo',
                'featured': True,
                'average_rating': Decimal('4.6'),
                'total_reviews': 8934,
            },
            {
                'name': 'Kerala Backwaters',
                'slug': 'kerala-backwaters',
                'state': 'Kerala',
                'city': 'Alappuzha',
                'categories': ['eco', 'adventure'],
                'description': 'The Kerala backwaters are a network of brackish lagoons and lakes lying parallel to the Arabian Sea coast. These interconnected waterways provide a unique ecosystem and tourism experience.',
                'short_description': 'Serene network of lagoons, lakes, and canals through lush landscapes',
                'latitude': Decimal('9.4981'),
                'longitude': Decimal('76.3388'),
                'best_time_to_visit': 'September to March',
                'entry_fee': 'Varies by tour operator',
                'opening_hours': 'Sunrise to sunset',
                'historical_significance': 'Ancient trading route connecting inland areas to the sea.',
                'cultural_importance': 'Traditional houseboat culture and coconut farming.',
                'local_cuisine': 'Fish Curry, Appam, Puttu, Toddy',
                'featured': True,
                'average_rating': Decimal('4.7'),
                'total_reviews': 6521,
            },
            {
                'name': 'Jaipur City Palace',
                'slug': 'jaipur-city-palace',
                'state': 'Rajasthan',
                'city': 'Jaipur',
                'categories': ['historical', 'cultural'],
                'description': 'The City Palace in Jaipur is a remarkable complex of palaces, gardens and courtyards, as well as the Chandra Mahal and Mubarak Mahal palaces and other buildings, which form the outer wall.',
                'short_description': 'Royal palace complex showcasing Rajasthani architecture',
                'latitude': Decimal('26.9255'),
                'longitude': Decimal('75.8235'),
                'best_time_to_visit': 'October to March',
                'entry_fee': '₹500 for Indians, ₹2000 for foreigners',
                'opening_hours': '9:30 AM to 5:00 PM',
                'historical_significance': 'Built by Maharaja Sawai Jai Singh II, founder of Jaipur.',
                'cultural_importance': 'Finest example of Rajasthani architecture and royal heritage.',
                'local_cuisine': 'Dal Baati Churma, Laal Maas, Gatte ki Sabzi',
                'featured': False,
                'average_rating': Decimal('4.5'),
                'total_reviews': 4326,
            },
            {
                'name': 'Manali Hill Station',
                'slug': 'manali-hill-station',
                'state': 'Himachal Pradesh',
                'city': 'Manali',
                'categories': ['mountain', 'adventure'],
                'description': 'Manali is a high-altitude Himalayan resort town known for its cool climate and snow-capped mountains. It is a popular destination for adventure sports and honeymoon couples.',
                'short_description': 'Himalayan hill station perfect for adventure and relaxation',
                'latitude': Decimal('32.2396'),
                'longitude': Decimal('77.1887'),
                'best_time_to_visit': 'March to June, September to December',
                'entry_fee': 'Free',
                'opening_hours': '24 hours',
                'historical_significance': 'Named after the lawgiver Manu, mentioned in Hindu scriptures.',
                'cultural_importance': 'Blend of Tibetan and Indian cultures, ancient temples.',
                'local_cuisine': 'Dhaam, Chana Madra, Siddu, Trout Fish',
                'featured': False,
                'average_rating': Decimal('4.4'),
                'total_reviews': 7834,
            },
            {
                'name': 'Hampi Archaeological Site',
                'slug': 'hampi-archaeological-site',
                'state': 'Karnataka',
                'city': 'Hampi',
                'categories': ['historical', 'cultural'],
                'description': 'Hampi is a UNESCO World Heritage Site located in Karnataka. It was the capital of the Vijayanagara Empire and contains numerous temples, palaces, and market streets.',
                'short_description': 'Ancient ruins of the Vijayanagara Empire, UNESCO World Heritage Site',
                'latitude': Decimal('15.3350'),
                'longitude': Decimal('76.4600'),
                'best_time_to_visit': 'October to February',
                'entry_fee': '₹40 for Indians, ₹600 for foreigners',
                'opening_hours': '6:00 AM to 6:00 PM',
                'historical_significance': 'Capital of the mighty Vijayanagara Empire (14th-16th century).',
                'cultural_importance': 'Outstanding example of Dravidian architecture and culture.',
                'local_cuisine': 'South Indian thali, Jolada Rotti, Bisi Bele Bath',
                'featured': True,
                'average_rating': Decimal('4.6'),
                'total_reviews': 3876,
            },
            {
                'name': 'Jim Corbett National Park',
                'slug': 'jim-corbett-national-park',
                'state': 'Uttarakhand',
                'city': 'Nainital',
                'categories': ['wildlife', 'eco'],
                'description': 'Jim Corbett National Park is India\'s oldest national park and was established in 1936 to protect the endangered Bengal tiger. It is located in Nainital district of Uttarakhand.',
                'short_description': 'India\'s oldest national park, famous for Bengal tigers',
                'latitude': Decimal('29.5319'),
                'longitude': Decimal('78.8434'),
                'best_time_to_visit': 'November to June',
                'entry_fee': '₹1500 per person for safari',
                'opening_hours': '6:00 AM to 6:00 PM (varies by season)',
                'historical_significance': 'First national park established in India under British rule.',
                'cultural_importance': 'Conservation pioneer, named after hunter-naturalist Jim Corbett.',
                'local_cuisine': 'Kumaoni cuisine, Aloo Gutke, Dubuk, Bhatt ki Churkani',
                'featured': True,
                'average_rating': Decimal('4.3'),
                'total_reviews': 5432,
            },
            {
                'name': 'Golden Temple',
                'slug': 'golden-temple',
                'state': 'Punjab',
                'city': 'Amritsar',
                'categories': ['religious', 'cultural'],
                'description': 'The Golden Temple, also known as Harmandir Sahib, is a Gurdwara located in Amritsar, Punjab. It is the holiest Gurdwara and the most important pilgrimage site of Sikhism.',
                'short_description': 'Holiest Gurdwara of Sikhism with stunning golden architecture',
                'latitude': Decimal('31.6200'),
                'longitude': Decimal('74.8765'),
                'best_time_to_visit': 'October to March',
                'entry_fee': 'Free',
                'opening_hours': '24 hours',
                'historical_significance': 'Built in 1589 by Guru Arjan, fifth Sikh Guru.',
                'cultural_importance': 'Spiritual center of Sikhism, serves free meals to all visitors.',
                'local_cuisine': 'Langar (free community kitchen), Amritsari Kulcha, Makki di Roti',
                'featured': True,
                'average_rating': Decimal('4.9'),
                'total_reviews': 15678,
            },
            {
                'name': 'Leh Ladakh',
                'slug': 'leh-ladakh',
                'state': 'Jammu and Kashmir',
                'city': 'Leh',
                'categories': ['mountain', 'adventure'],
                'description': 'Leh Ladakh is a region in northern India known for its stark landscapes, Buddhist monasteries, and adventure tourism. It is often called "Little Tibet" due to its Tibetan cultural influence.',
                'short_description': 'High-altitude desert region with Buddhist monasteries and stunning landscapes',
                'latitude': Decimal('34.1526'),
                'longitude': Decimal('77.5771'),
                'best_time_to_visit': 'May to September',
                'entry_fee': 'Free',
                'opening_hours': '24 hours',
                'historical_significance': 'Ancient trade route between India, Tibet, and Central Asia.',
                'cultural_importance': 'Tibetan Buddhist culture, ancient monasteries and festivals.',
                'local_cuisine': 'Thukpa, Momos, Tsampa, Chang',
                'featured': True,
                'average_rating': Decimal('4.7'),
                'total_reviews': 9234,
            },
            {
                'name': 'Mysore Palace',
                'slug': 'mysore-palace',
                'state': 'Karnataka',
                'city': 'Mysore',
                'categories': ['historical', 'cultural'],
                'description': 'The Mysore Palace is a historical palace and a royal residence at Mysore in Karnataka. It is the official residence of the Wadiyar dynasty and the seat of the Kingdom of Mysore.',
                'short_description': 'Royal palace famous for its Indo-Saracenic architecture',
                'latitude': Decimal('12.3051'),
                'longitude': Decimal('76.6551'),
                'best_time_to_visit': 'October to March',
                'entry_fee': '₹70 for Indians, ₹200 for foreigners',
                'opening_hours': '10:00 AM to 5:30 PM',
                'historical_significance': 'Former seat of the Wadiyar dynasty rulers of Mysore.',
                'cultural_importance': 'Indo-Saracenic architecture, Dasara festival celebrations.',
                'local_cuisine': 'Mysore Pak, Masala Dosa, Filter Coffee, Ragi Mudde',
                'featured': False,
                'average_rating': Decimal('4.4'),
                'total_reviews': 6789,
            },
        ]
        
        # Create admin user if it doesn't exist
        admin_user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@smarttourismindia.com',
                'is_staff': True,
                'is_superuser': True,
                'first_name': 'Admin',
                'last_name': 'User'
            }
        )
        if created:
            admin_user.set_password('admin123')
            admin_user.save()
            self.stdout.write(f'Created admin user: {admin_user.username}')
        
        for dest_data in destinations_data:
            try:
                # Get the state
                state = State.objects.get(name=dest_data['state'])
                
                # Create destination
                destination, created = Destination.objects.get_or_create(
                    slug=dest_data['slug'],
                    defaults={
                        'name': dest_data['name'],
                        'description': dest_data['description'],
                        'short_description': dest_data['short_description'],
                        'state': state,
                        'city': dest_data['city'],
                        'latitude': dest_data['latitude'],
                        'longitude': dest_data['longitude'],
                        'best_time_to_visit': dest_data['best_time_to_visit'],
                        'entry_fee': dest_data['entry_fee'],
                        'opening_hours': dest_data['opening_hours'],
                        'historical_significance': dest_data['historical_significance'],
                        'cultural_importance': dest_data['cultural_importance'],
                        'local_cuisine': dest_data['local_cuisine'],
                        'featured': dest_data['featured'],
                        'average_rating': dest_data['average_rating'],
                        'total_reviews': dest_data['total_reviews'],
                        'created_by': admin_user,
                    }
                )
                
                if created:
                    # Add categories
                    for cat_name in dest_data['categories']:
                        try:
                            category = Category.objects.get(name=cat_name)
                            destination.categories.add(category)
                        except Category.DoesNotExist:
                            self.stdout.write(
                                self.style.ERROR(f'Category {cat_name} not found for {dest_data["name"]}')
                            )
                    
                    self.stdout.write(
                        self.style.SUCCESS(f'Created destination: {destination.name}')
                    )
                else:
                    self.stdout.write(f'Destination {destination.name} already exists')
                    
            except State.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(f'State {dest_data["state"]} not found for {dest_data["name"]}')
                )
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'Error creating {dest_data["name"]}: {str(e)}')
                )
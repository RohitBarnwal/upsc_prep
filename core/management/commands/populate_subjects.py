from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from core.models import Subject, Topic
from django.db import transaction

User = get_user_model()

class Command(BaseCommand):
    help = 'Populates the database with UPSC CSE subjects and topics'

    def handle(self, *args, **kwargs):
        # Get or create admin user
        admin_user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@example.com',
                'is_staff': True,
                'is_superuser': True
            }
        )
        if created:
            admin_user.set_password('admin123')
            admin_user.save()
            self.stdout.write(self.style.SUCCESS('Created admin user'))

        # Define subjects and their topics
        subjects_data = {
            'Essay Paper': [
                'Current Affairs Essays',
                'Social Issues Essays',
                'Political Essays',
                'Economic Essays',
                'Philosophical Essays',
                'Abstract Topic Essays',
                'Science & Technology Essays',
                'Environmental Essays'
            ],
            'GS-I: Indian Heritage and Culture, History and Geography': [
                'Indian Culture - Art Forms, Literature, Architecture (Ancient to Modern)',
                'Modern Indian History (18th Century onwards)',
                'Freedom Struggle and its Stages',
                'Post-Independence Consolidation',
                'World History (18th Century onwards)',
                'Indian Society and Diversity',
                'Women and Women\'s Organizations',
                'Population and Development Issues',
                'Urbanization and Related Issues',
                'World Physical Geography',
                'Natural Resources Distribution',
                'Important Geophysical Phenomena'
            ],
            'GS-II: Governance, Constitution, Polity, and International Relations': [
                'Indian Constitution - Evolution and Features',
                'Federal Structure and Challenges',
                'Separation of Powers',
                'Parliament and State Legislatures',
                'Executive and Judiciary',
                'Constitutional Bodies',
                'Government Policies and Interventions',
                'Social Justice and Welfare Schemes',
                'International Relations',
                'India and its Neighbors',
                'Bilateral and Global Agreements',
                'Important International Institutions'
            ],
            'GS-III: Technology, Economic Development, Environment': [
                'Indian Economy and Planning',
                'Inclusive Growth',
                'Government Budgeting',
                'Agriculture and Food Security',
                'Infrastructure Development',
                'Science and Technology Developments',
                'IT and Space Technology',
                'Environmental Conservation',
                'Disaster Management',
                'Internal Security Challenges',
                'Cybersecurity',
                'Money Laundering'
            ],
            'GS-IV: Ethics, Integrity, and Aptitude': [
                'Ethics and Human Interface',
                'Human Values',
                'Civil Service Values',
                'Emotional Intelligence',
                'Moral Thinkers and Philosophers',
                'Public Service Ethics',
                'Probity in Governance',
                'Case Studies in Ethics'
            ],
            'CSAT - Civil Services Aptitude Test': [
                'Comprehension',
                'Interpersonal Skills',
                'Logical Reasoning',
                'Analytical Ability',
                'Decision Making',
                'Problem Solving',
                'Basic Numeracy',
                'Data Interpretation'
            ],
            'Optional Subject - Paper 1': [
                'Agriculture',
                'Animal Husbandry & Veterinary Science',
                'Anthropology',
                'Botany',
                'Chemistry',
                'Civil Engineering',
                'Commerce & Accountancy',
                'Economics',
                'Electrical Engineering',
                'Geography',
                'Geology',
                'History',
                'Law',
                'Management',
                'Mathematics',
                'Mechanical Engineering',
                'Medical Science',
                'Philosophy',
                'Physics',
                'Political Science & IR',
                'Psychology',
                'Public Administration',
                'Sociology',
                'Statistics',
                'Zoology',
                'Literature'
            ],
            'Optional Subject - Paper 2': [
                'Advanced Topics in Selected Optional Subject',
                'Case Studies in Optional Subject',
                'Current Developments in Optional Field',
                'Applied Aspects of Optional Subject',
                'Field-Specific Problems and Solutions',
                'Contemporary Debates in Optional Subject',
                'Research and Development in Optional Field',
                'Practical Applications'
            ]
        }

        try:
            with transaction.atomic():
                # Delete existing subjects and topics
                Subject.objects.all().delete()
                
                # Create new subjects and topics
                for subject_name, topics_list in subjects_data.items():
                    # Create subject
                    subject = Subject.objects.create(
                        name=subject_name,
                        description=f"Topics covered:\n" + "\n".join(f"- {topic}" for topic in topics_list),
                        created_by=admin_user
                    )
                    self.stdout.write(self.style.SUCCESS(f'Created subject: {subject.name}'))
                    
                    # Create topics for this subject
                    for order, topic_name in enumerate(topics_list, 1):
                        Topic.objects.create(
                            name=topic_name,
                            subject=subject,
                            order=order
                        )
                        self.stdout.write(self.style.SUCCESS(f'Created topic: {topic_name}'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error occurred: {str(e)}'))
            return

        self.stdout.write(self.style.SUCCESS('Successfully populated subjects and topics')) 
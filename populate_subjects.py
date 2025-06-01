from django.contrib.auth import get_user_model
from core.models import Subject

User = get_user_model()

# Get the first admin user (or create one if doesn't exist)
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

# UPSC CSE Syllabus subjects
subjects_data = [
    {
        "name": "General Studies I - Indian Heritage and Culture",
        "description": "Indian culture: art forms, literature and architecture from ancient to modern times. Indian History: significant events, issues, personalities. Modern Indian history from mid-18th century. Post-independence consolidation and reorganization. Geography of India and World. Indian Society and diversity."
    },
    {
        "name": "General Studies II - Governance",
        "description": "Indian Constitution, political system, Panchayati Raj, Public Policy, Rights Issues, etc. Comparison of Indian constitutional scheme with other countries. Separation of powers, dispute redressal mechanisms and institutions. Government policies and interventions. Development processes and development industry."
    },
    {
        "name": "General Studies III - Technology & Economic Development",
        "description": "Indian Economy and issues relating to planning, mobilization of resources, growth, development and employment. Inclusive growth and issues arising from it. Government Budgeting. Major crops, irrigation systems, storage, transport and marketing of agricultural produce, e-technology in aid of farmers."
    },
    {
        "name": "General Studies IV - Ethics & Integrity",
        "description": "Ethics and Human Interface: Essence, determinants and consequences of Ethics in human actions. Dimensions of ethics. Ethics in private and public relationships. Human Values. Role of family, society and educational institutions in inculcating values."
    },
    {
        "name": "CSAT - Civil Services Aptitude Test",
        "description": "Comprehension, interpersonal skills including communication skills, logical reasoning and analytical ability, decision-making and problem-solving, general mental ability, basic numeracy, data interpretation."
    },
    {
        "name": "Indian History",
        "description": "Ancient India: Prehistoric Cultures, Indus Valley Civilization, Vedic Period, Buddhism and Jainism. Medieval India: Delhi Sultanate, Mughal Empire, Bhakti and Sufi Movements. Modern India: British Rule, Indian National Movement, Post-Independence India."
    },
    {
        "name": "Indian Geography",
        "description": "Physical Geography: Major landforms, climate, soil types, natural vegetation. Human Geography: Population distribution, urbanization. Economic Geography: Agriculture, industry, trade, transport. Environmental Geography: Biodiversity, climate change, disaster management."
    },
    {
        "name": "Indian Polity",
        "description": "Constitutional Framework, Fundamental Rights and Duties, Union and State Executive, Judiciary, Local Government, Constitutional Bodies, Electoral Process, Amendment Process, Emergency Provisions, Centre-State Relations."
    },
    {
        "name": "Indian Economy",
        "description": "Economic Development since Independence, Five Year Plans, Economic Reforms, Banking System, Monetary Policy, Fiscal Policy, Inflation, Poverty and Unemployment, Agricultural and Industrial Development, Foreign Trade."
    },
    {
        "name": "International Relations",
        "description": "India's Foreign Policy, Relations with Neighboring Countries, International Organizations (UN, World Bank, IMF, WTO), Regional Organizations (SAARC, ASEAN), Global Issues and India's Role."
    },
    {
        "name": "Science & Technology",
        "description": "Basic concepts in science, Recent developments in science and technology, Indigenous technologies, Space technology, Nuclear technology, IT and computers, Robotics and AI, Environmental science and ecology."
    },
    {
        "name": "Environment & Ecology",
        "description": "Basic ecological concepts, Biodiversity, Environmental pollution and control, Climate change and global warming, Environmental conservation, International environmental agreements, Sustainable development."
    }
]

# Create subjects
for subject_data in subjects_data:
    Subject.objects.get_or_create(
        name=subject_data["name"],
        defaults={
            "description": subject_data["description"],
            "created_by": admin_user
        }
    )

print("Subjects have been populated successfully!") 
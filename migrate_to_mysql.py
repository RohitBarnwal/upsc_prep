import os
import django
from django.core.management import call_command
from django.conf import settings

def migrate_to_mysql():
    # Backup SQLite data
    print("Creating JSON dump of current data...")
    call_command('dumpdata', '--exclude', 'auth.permission', '--exclude', 'contenttypes', 
                '--indent', '2', output='data_backup.json')
    
    # Switch to MySQL
    os.environ['USE_MYSQL'] = 'True'
    
    # Migrate schema to MySQL
    print("Migrating schema to MySQL...")
    call_command('migrate')
    
    # Load data into MySQL
    print("Loading data into MySQL...")
    call_command('loaddata', 'data_backup.json')
    
    print("Migration completed successfully!")

if __name__ == "__main__":
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'upsc_project.settings')
    django.setup()
    migrate_to_mysql() 
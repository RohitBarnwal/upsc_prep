import os
from dotenv import load_dotenv

def test_env_variables():
    load_dotenv()
    
    # List of variables to check
    variables = [
        'DJANGO_SECRET_KEY',
        'DJANGO_DEBUG',
        'DJANGO_ALLOWED_HOSTS',
        'DJANGO_LOG_LEVEL',
        'DB_NAME',
        'DB_USER',
        'DB_PASSWORD',
        'DB_HOST',
        'DB_PORT'
    ]
    
    print("Testing environment variables:")
    print("-" * 50)
    
    for var in variables:
        value = os.getenv(var)
        if value is not None:
            # Mask sensitive information
            if 'SECRET' in var or 'PASSWORD' in var:
                print(f"{var}: {'*' * len(value)}")
            else:
                print(f"{var}: {value}")
        else:
            print(f"{var}: NOT SET")
    
    print("-" * 50)

if __name__ == "__main__":
    test_env_variables() 
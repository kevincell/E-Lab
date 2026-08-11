from django.test.client import Client
from django.contrib.auth import get_user_model
import traceback
import sys

try:
    User = get_user_model()
    c = Client()
    u = User.objects.filter(username='student').first()
    if not u:
        print("Student user not found!")
        sys.exit(1)
    
    c.force_login(u)
    response = c.get('/overview/')
    print('Status:', response.status_code)
    if response.status_code == 500:
        # Django's test client will actually raise the exception if it's an unhandled 500 error!
        # Wait, the test client raises exceptions by default in tests, but in shell it might just return 500 response.
        print("GOT 500 ERROR. Content:")
        print(response.content.decode('utf-8')[:2000]) # Print first 2000 chars of debug page
except Exception as e:
    traceback.print_exc()

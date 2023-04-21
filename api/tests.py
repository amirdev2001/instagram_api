from django.test import TestCase

from rest_framework.test import APIRequestFactory


factory = APIRequestFactory()
request = factory.get('/amir')
print(request.method)
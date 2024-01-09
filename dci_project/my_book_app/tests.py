from rest_framework.test import APIClient,APITestCase
from rest_framework import status
from django.urls import reverse
from datetime import date,timedelta
from django.utils.text import slugify
from .models import Book
from .serializers import BookSerializer
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

class BookTests(APITestCase):
    
    
    def setUp(self) :
        
        self.client = APIClient()
        self.admin_user = User.objects.create_superuser(
            'admin','admin@test.py','testpassword'
        )
        self.token = Token.objects.create(user = self.admin_user)
        self.user = User.objects.create_user("user", "admin@test.com", "testpassword")
        self.user_token = Token.objects.create(user=self.user)
        self.book = Book.objects.create(
            title="The Alchemist",
            author="Paulo Coelho",
            description="A book about following your dreams",
            published_date=date.today() - timedelta(days=7),
            is_published=False,
        )
        self.valid_payload = {
            "title": "The Alchemist 1",
            "author": "Paulo Coelho",
            "description": "A book about following your dreams",
            "published_date": date.today() - timedelta(days=7),
            "is_published": False,
        }
        self.invalid_payload = {
            "title": "",
            "author": "",
            "description": "",
            "published_date": date.today() + timedelta(days=7),
            "is_published": False,
        }
        
    def test_get_all_books(self):
        response = self.client.get(reverse('book_list'))
        books = Book.objects.all()
        serializer = BookSerializer(books,many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        
    def test_get_single_book(self):
        
        response = self.client.get(reverse('book_detail',args=[self.book.id]))
        book = Book.objects.get(id=self.book.id)
        serializer = BookSerializer(book)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    
        

from django.shortcuts import render
from rest_framework import generics,permissions
from .models import Book
from .serializers import BookSerializer  
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .permissions import IsAdminOrReadOnly
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import ValidationError
from drf_yasg.utils import swagger_auto_schema
import django_filters.rest_framework
import django_filters
# Create your views here.

# class BookFilter(django_filters.FilterSet):
#     class Meta :
#         model = Book
#         fields = ['title','author','published_date','is_published']

class BookList(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminOrReadOnly,permissions.IsAuthenticatedOrReadOnly]
    #filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ['title','author','published_date','is_published']
    #filter_class = BookFilter
    
    @swagger_auto_schema(operation_description='Retrieve the list of books')
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    
    @swagger_auto_schema(operation_description='Create a new book')
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
    
    
    def perform_create(self, serializer):
        try :
            serializer.save()           
        except ValidationError as e:
            raise ValidationError(detail=e.detail)
            
    
class BookDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminOrReadOnly,permissions.IsAuthenticatedOrReadOnly]
    
    @swagger_auto_schema(operation_description='Retrieve a book by id')
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    
    @swagger_auto_schema(operation_description='Update a single book')
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)
    
    @swagger_auto_schema(operation_description='Delete a book')
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)
    
    
    def perform_update(self, serializer):
        try:
            serializer.save()
        except ValidationError as e:
            raise ValidationError(detail=e.detail)
        
    def perform_destroy(self, instance):
        instance.delete()
        





@api_view(['GET','POST'])
def book_list(request):
    if request.method == 'GET':
        print(request.user.is_staff)
        books = Book.objects.all()
        serializer = BookSerializer(books,many = True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

@api_view(['GET','PUT','DELETE'])    
def book_detail(request,pk):
    try:
        book = Book.objects.get(pk=pk)
    except Book.DoesNotExist:
        return Response(status=404)
    
    if request.method == 'GET':
        serializer = BookSerializer(book)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = BookSerializer(book, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    
    elif request.method == 'DELETE':
        book.delete()
        return Response(status=204)
    
        
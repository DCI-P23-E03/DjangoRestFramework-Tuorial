from django.shortcuts import render
from rest_framework import generics,permissions
from .models import Book
from .serializers import BookSerializer  
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .permissions import IsAdminOrReadOnly
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import ValidationError
# Create your views here.


class BookList(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminOrReadOnly,permissions.IsAuthenticatedOrReadOnly]
    
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
    
        
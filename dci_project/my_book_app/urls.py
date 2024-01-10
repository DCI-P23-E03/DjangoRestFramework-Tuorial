from django.urls import path
from .views import BookList,BookDetail,book_list,book_detail
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.authentication import TokenAuthentication
from rest_framework import generics,permissions
from .permissions import IsAdminOrReadOnly
schema_view = get_schema_view(
    openapi.Info(
    title='Book API',
    default_version = 'v1',
    description = 'API for books',
    terms_of_service="https://www.google.com/policies/terms/",
    contact=openapi.Contact(email="contact@bookapi.local"),
    license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes = [],
    authentication_classes=[]
    )


urlpatterns = [
    path('books/',BookList.as_view(),name='book_list'),
    path('books/<int:pk>/',BookDetail.as_view(),name='book_detail'),
    path('openapi/',schema_view.without_ui(cache_timeout=0)),
    path('swagger/',schema_view.with_ui('swagger',cache_timeout=0),name='schema-swagger-ui'),
    path('redoc/',schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc') 
]

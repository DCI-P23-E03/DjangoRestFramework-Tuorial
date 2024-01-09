from django.urls import path
from .views import BookList,BookDetail,book_list,book_detail


urlpatterns = [
    path('books/',BookList.as_view(),name='book_list'),
    path('books/<int:pk>/',BookDetail.as_view(),name='book_detail'),
    # path('lib/',book_list),
    # path('lib/<int:pk>/',book_detail)
]


from django.urls import path
from catalog import views
from django.views.generic.base import TemplateView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('',views.index,name='index'),
    path('books/',views.BookListView.as_view(),name='books'),
    path('book/<int:pk>',views.BookDetailedView.as_view(),name='book-detail'),
    path('authors/',views.AuthorListView.as_view(),name='authors'),
    path('author/<int:pk>',views.AuthorDetailedView.as_view(),name='author-detail'),  
    path('mybooks/', views.LoanedBooksByUserListView.as_view(), name='my-borrowed'),
    path('logout/', auth_views.LogoutView,{'template_name':'logged_out.html'}, name='logout'),

]

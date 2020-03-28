from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('books', views.BookListView.as_view(), name='books'),
    path('book/<uuid:id>', views.BookDetailView.as_view(), name='book-detail'),
    path('authors/', views.AuthorListView.as_view(), name='authors'),
    path('author/<int:id>', views.AuthorDetailView.as_view(), name='author-detail'),
    path('mybooks', views.LoanedBooksByUserListView.as_view(),
         name='borrowed-books'),
    path('borrowed', views.LibrairianListView.as_view(), name='borrowed'),
    path('book/<uuid:id>/renew', views.renew_book_librairian,
         name='renew-book-librairian'),
    path('author/create', views.AuthorCreate.as_view(), name='author_create'),
    path('author/<int:id>/update',
         views.AuthorUpdate.as_view(), name='author_update'),
    path('author/<int:id>/delete',
         views.AuthorDelete.as_view(), name='author_delete'),
    path('book/create', views.CreateBook.as_view(), name='book_create')
]

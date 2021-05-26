from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home_favoritesApp'),
    path('register', views.register, name='register_favoritesApp'),
    path('login', views.login, name='login_favoritesApp'),
    path('logout', views.logout, name='logout_favoritesApp'),

    path('books', views.books, name='books'),
    path('addBooks', views.add_book, name='addBook'),
    path('update_all_books_fav', views.update_all_books_fav, name='update_all_books_fav'),
    path('load_books_user/<int:id_user>', views.update_all_books_fav, name='update_all_books_fav'),
    path('show_book/<int:id_book>', views.show_book, name='show_book'),
    path('add_favorite/<int:id_book>', views.add_favorite, name='add_favorite'),
    path('edit_delete_book/<int:id_book>', views.edit_delete_book, name='edit_delete_book'),
    path('un_favorite_book/<int:id_book>', views.un_favorite_book, name='un_favorite_book'),
    path('all_favorites', views.all_favorites, name='all_favorites'),
]
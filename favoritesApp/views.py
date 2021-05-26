from typing import ContextManager
from django.shortcuts import render, redirect
from .forms.favoritesApp.user import UserForm, UserLoginForm
from .forms.favoritesApp.book import BookForm
from django.contrib import messages
from favoritesApp.models import *
from datetime import datetime, timezone, timedelta
from django.http import HttpResponse, JsonResponse
# Create your views here.

APP_NAME = 'favoritesApp'
HOME = 'home_'+APP_NAME
def index(request):
    #return render(request, f'{APP_NAME}/index.html')
    return redirect(f'register_{APP_NAME}')

def register(request):
    if request.method == 'GET':
        user_form = UserForm()
        user_login_form = UserLoginForm()
        context = {
            'user_form' : user_form,
            'user_login_form' : user_login_form,
        }
        print('va a register nuevo')
        return render(request, f'{APP_NAME}/register.html', context)
    
    if request.method == 'POST':
        print(request.POST)
        errors = User.objects.validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            context = {
                'user_form' : UserForm(request.POST),
                'user_login_form' : UserLoginForm(),
            }
            return render(request, f'{APP_NAME}/register.html', context)

        if User.ifExists(request.POST['email']):
            messages.error(request, 'Usuario ya existe')
            context = {
                'user_form' : UserForm(request.POST),
                'user_login_form' : UserLoginForm(),
            }
            return render(request, f'{APP_NAME}/register.html', context)

        user_form = UserForm(request.POST)
        if user_form.is_valid():
            user = user_form.save()
            request.session['logged_user'] = user.email
        else:
            context = {
                'user_form' : UserForm(request.POST),
                'user_login_form' : UserLoginForm(),
            }
            return render(request, f'{APP_NAME}/register.html', context)

    return redirect('books')

def login(request):
    if request.method == 'GET':
        user_form = UserForm()
        user_login_form = UserLoginForm(request.POST)
        context = {
            'user_form' : user_form,
            'user_login_form' : user_login_form,
            }
        return render(request, f'{APP_NAME}/register.html', context)

    if request.method == 'POST':
        loginForm = UserLoginForm(request.POST)
        if loginForm.is_valid():
            logged_user = loginForm.login(request.POST)
            if logged_user:
                request.session['logged_user_name'] = logged_user.first_name + ' ' + logged_user.last_name
                request.session['logged_user'] = logged_user.email
                print('logged_user: ', request.session['logged_user'])
                return redirect('books')
            
        user_form = UserForm()
        user_login_form = UserLoginForm(request.POST)
        context = {
            'user_form' : user_form,
            'user_login_form' : user_login_form,
        }
        return render(request, f'{APP_NAME}/register.html', context)

def logout(request):
    try:
        del request.session['logged_user']
        del request.session['logged_user_name']
    except:
        print('Error')
    return redirect(HOME)


def books(request):
    if 'logged_user' not in request.session:
        return redirect(login)

    context = {
        'bookForm'  : BookForm(),
        'all_books' : Book.objects.all().order_by('id')[::-1],
        'my_favorites' : Book.objects.filter(users_who_like__in=User.objects.filter(email=request.session['logged_user'])),
        'users' : User.objects.all(),
    }
    return render(request, f'{APP_NAME}/index.html', context)

def add_book(request):
    if request.method == 'GET':
        return redirect(books)

    context = {
            'bookForm'  : BookForm(),
            'all_books' : Book.objects.all(),
    }
    if request.method == 'POST':
        bookForm = BookForm(request.POST)
        if bookForm.is_valid():
            users = User.objects.filter(email=request.session['logged_user'])
            if len(users) == 1:
                user = users[0]
                errors = Book.objects.validator(request.POST)
                if len(errors) == 0:
                    #book = Book(title=request.POST['title'], desc=request.POST['desc'], uploaded_by=user)
                    #book.save()
                    book = bookForm.save(commit=False)
                    book.uploaded_by = user
                    #book.users_who_like.add(user)
                    book.save()
                    book.users_who_like.add(user)
                    #book.save()
                    #user.liked_books.add(book)
                    #user.save()
                    print('funciona!')
                    return redirect(books)
                else:
                    for key, value in errors.items():
                        messages.error(request, value)
                        context = {
                                'bookForm'  : BookForm(request.POST),
                                'all_books' : Book.objects.all()
                                }
    
    return render(request, f'{APP_NAME}/index.html', context)

def update_all_books_fav(request):
    if 'logged_user' not in request.session:
        return redirect(login)

    if request.method == 'GET':
        return redirect(books)

    if request.method == 'POST':
        print(request.POST)
        
        users = User.objects.filter(email=request.session['logged_user'])

        if len(users) != 1:
            # si el usuario esta deslogueado o se elimino de la bdd
            return redirect(login)
        else:
            user = users[0]
            if 'chk_all_books' in request.POST and request.POST['chk_all_books'] == 'on':
                if 'user_selected' in request.POST:
                    messages.error(request, 'Todos los libros del usuario son sus favoritos!')
                    user.liked_books.add(*Book.objects.filter(uploaded_by=User.objects.get(id=request.POST['user_selected'])))
                else:
                    messages.error(request, 'Todos los libros son sus favoritos!')
                    user.liked_books.add(*Book.objects.all())
            else:
                messages.error(request, 'Ningún de los libros son sus favoritos!')
                user.liked_books.remove(*Book.objects.all())

    return redirect(books)

def add_favorite(request, id_book):
    if 'logged_user' not in request.session:
        return redirect(login)

    if request.method == 'GET':
        users = User.objects.filter(email=request.session['logged_user'])

        if len(users) != 1:
            # si el usuario esta deslogueado o se elimino de la bdd
            return redirect(login)
        else:
            user = users[0]
            books = Book.objects.filter(id=id_book)
            if len(books) == 1:
                book = books[0]
                users = User.objects.filter(liked_books=book)
                if user not in users:
                    book.users_who_like.add(user)
                    book.save()
                else:
                    messages.error(request, 'El libro ya es su favorito!')
            else:
                messages.error(request, 'Libro no existe!')

    return redirect('books')

def show_book(request, id_book):
    print('show EDIT*****')
    if 'logged_user' not in request.session:
        return redirect(login)

    if request.method == 'GET':
        users = User.objects.filter(email=request.session['logged_user'])

        if len(users) != 1:
            # si el usuario esta deslogueado o se elimino de la bdd
            return redirect(login)
        else:
            user = users[0]
            books = Book.objects.filter(id=id_book)
            b = Book()
            if len(books) == 1:
                book = books[0]
                context = {
                        'book'  : book,
                        'book_liked'  : User.objects.filter(liked_books__in=Book.objects.filter(id=book.id)),
                        'my_favorites' : Book.objects.filter(users_who_like__in=User.objects.filter(email=request.session['logged_user'])),
                        # 'id_book' : book.id,
                        # 'title' : book.title,
                        # 'desc' : book.desc,
                        'edit' : True if user == book.uploaded_by else False,
                        # 'bookEditForm'  : BookForm(book.__dict__),
                    }
                return render(request, f'{APP_NAME}/show_edit_book.html', context)
            else:
                messages.error(request, 'Libro no existe!')
            
    return redirect('books')

def edit_delete_book(request, id_book):
    if 'logged_user' not in request.session:
        return redirect(login)

    if request.method == 'POST':
        users = User.objects.filter(email=request.session['logged_user'])

        if len(users) != 1:
            # si el usuario esta deslogueado o se elimino de la bdd
            return redirect(login)
        else:
            user = users[0]
            books = Book.objects.filter(id=id_book)
            if len(books) == 1:
                book = books[0]
                if user == book.uploaded_by:
                    form = BookForm(request.POST)
                    if 'btnAction' in request.POST and 'title' in request.POST and 'desc' in request.POST:
                        if form.is_valid():
                            if request.POST['btnAction'] == 'update':
                                if not book.ifExists(request.POST['title']):
                                    book.title = request.POST['title']
                                    book.desc = request.POST['desc']
                                    book.save()
                                else:
                                    messages.error(request, 'Título ya existe!')
                                    context = {
                                            'book'  : book,
                                            'edit' : True if user == book.uploaded_by else False,
                                            
                                        }
                                    return render(request, f'{APP_NAME}/show_edit_book.html', context)
                            if request.POST['btnAction'] == 'delete':
                                book.delete()
                        else:
                            if len(request.POST['title']) < 2:
                                messages.error(request, 'Título muy corto!')
                            context = {
                                    'book'  : book,
                                    'edit' : True if user == book.uploaded_by else False,
                                }
                            return render(request, f'{APP_NAME}/show_edit_book.html', context)
                    else:
                        messages.error(request, 'Datos de formulario incorrectos!')
                        
                else:
                    messages.error(request, 'No tiene permisos sobre este libro!')
            else:
                messages.error(request, 'Libro no existe!')

    return redirect('books')

def un_favorite_book(request, id_book):
    if 'logged_user' not in request.session:
        return redirect(login)

    if request.method == 'POST':
        return redirect('books')

    if request.method == 'GET':
        
        users = User.objects.filter(email=request.session['logged_user'])

        if len(users) != 1:
            # si el usuario esta deslogueado o se elimino de la bdd
            return redirect(login)
        else:
            user = users[0]
            books = Book.objects.filter(id=id_book)
            if len(books) == 1:
                book = books[0]
                book.users_who_like.remove(user)
            else:
                messages.error(request, 'Libro no existe!')

    return redirect(show_book, id_book)

def all_favorites(request):
    if 'logged_user' not in request.session:
        return redirect(login)

    if request.method == 'POST':
        return redirect('books')

    if request.method == 'GET':
        
        users = User.objects.filter(email=request.session['logged_user'])

        if len(users) != 1:
            # si el usuario esta deslogueado o se elimino de la bdd
            return redirect(login)
        else:
            user = users[0]
            context = {
                'all_favorites' : Book.objects.filter(users_who_like=user)
            }
            return render(request, f'{APP_NAME}/all_favorites.html', context)

    return redirect('books')
from django.db import models
from datetime import datetime, timedelta
from django.core import validators
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages
import re
import bcrypt


class UserManager(models.Manager):
    def validator(self, postData):
        errors  = {}
        
        errorsEmail = self.checkEmail(postData['email'])
        if len(errorsEmail) > 0:
            errors['email'] = errorsEmail

        errorsPass = self.checkPassword(postData['password'])
        if len(errorsPass) > 0:
            errors['email'] = errorsPass
        

        return errors
    
    def checkPassword(self, password):
        errors  = {}
        regex = re.compile(r"""(?#!py password Rev:20160831_2100)
                                    # Validate password: 2 upper, 1 special, 2 digit, 1 lower, 8 chars.
                                ^                        # Anchor to start of string.
                                (?=(?:[^A-Z]*[A-Z]){2})  # At least two uppercase.
                                (?=[^!@#$&*]*[!@#$&*])   # At least one "special".
                                (?=(?:[^0-9]*[0-9]){1})  # At least two digit.
                                .{8,}                    # Password length is 8 or more.
                                $                        # Anchor to end of string.
                                """, re.VERBOSE)
        EMAIL_REGEX = re.compile(r'^(?=(?:[^A-Z]*[A-Z]){2})(?=[^!@#$&*]*[!@#$&*])(?=(?:[^0-9]*[0-9]){1}).{8,}$')
        if not EMAIL_REGEX.match(password):
            errors['password'] = 'Password inválido, Minimo 8 caracteres, Al menos una letra mayúscula y una letra minucula, Al menos un dígito, Al menos 1 caracter especial'
        return errors

    def checkEmail(self, email):
        errors  = {}
        EMAIL_REGEX = re.compile(r'^[A-Za-z0-9.+_-]+@[A-Za-z0-9.+_-]+\.[A-Za-z]+$')
        if not EMAIL_REGEX.match(email):
            errors['email'] = 'Correo Inválido'
        return errors

class User(models.Model):
    first_name      = models.CharField(max_length=45)
    last_name       = models.CharField(max_length=45)
    email           = models.CharField(max_length=100)
    birth_date      = models.DateField()
    password        = models.CharField(max_length=254)
    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)
    objects         = UserManager()

    def __str__(self):
        return '%s %s' % (self.first_name, self.last_name)

    def save(self, *args, **kwargs):
        self.password = make_password(self.password)
        super(User, self).save(*args, **kwargs)
    
    @staticmethod
    def ifExists(email):
        users    = User.objects.filter(email = email)
        if len(users) > 0:
            return True
        else:
            return False

    @staticmethod
    def authenticate(email, password):
        users    = User.objects.filter(email = email)
        if len(users) > 0:
            user = users[0]
            bd_password = user.password
            if check_password(password, bd_password):
                return user
        return None

class BookManager(models.Manager):
    def validator(self, postData):
        errors  = {}

        book    = Book.objects.filter(title = postData['title'])
        if len(book) > 0:
            errors['book'] = 'Titulo ya existe'

        return errors

class Book(models.Model):
    title           = models.CharField(max_length=255)
    desc            = models.TextField()
    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)
    uploaded_by     = models.ForeignKey(User, related_name='books_uploaded', on_delete=models.CASCADE)
    users_who_like  = models.ManyToManyField(User, related_name='liked_books')
    objects         = BookManager()

    @staticmethod
    def ifExists(title):
        books    = Book.objects.filter(title = title)
        if len(books) > 0:
            return True
        else:
            return False
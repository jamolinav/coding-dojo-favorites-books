# Generated by Django 3.2.3 on 2021-05-21 21:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('favoritesApp', '0003_rename_user_book_uploaded_by_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='users_who_like',
            field=models.ManyToManyField(related_name='liked_books', to='favoritesApp.User'),
        ),
        migrations.AlterField(
            model_name='book',
            name='uploaded_by_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='books_uploaded', to='favoritesApp.user'),
        ),
        migrations.DeleteModel(
            name='Favorites',
        ),
    ]

from django.db import models


class User(models.Model):
    user_email = models.EmailField()
    user_password = models.CharField(max_length=18)

    user_name = models.CharField(max_length=32, blank=True,null=True)
    user_age = models.IntegerField(blank=True, null=True)
    user_gender = models.CharField(max_length=32, blank=True, null=True)
    user_photo = models.ImageField(upload_to='images', blank=True, null=True)
    phone_number = models.CharField(max_length=11, blank=True, null=True)
    user_address = models.TextField(max_length=254, blank=True, null=True)


class Author(models.Model):
    author_name = models.CharField(max_length=32)
    author_age = models.IntegerField(blank=True, null=True)
    author_gender = models.CharField(max_length=32, blank=True, null=True)
    author_birthday = models.DateField(blank=True, null=True)
    author_email = models.EmailField(blank=True, null=True)
    author_address = models.TextField(max_length=254, blank=True, null=True)
    author_photo = models.ImageField(upload_to='images', blank=True, null=True)


class ArticleType(models.Model):
    label = models.CharField(max_length=32)
    description = models.TextField()


class Article(models.Model):
    article_name = models.CharField(max_length=32)
    article_description = models.TextField()
    content = models.TextField()
    article_author = models.ForeignKey(to=Author, on_delete=models.CASCADE)
    article_public_time = models.DateField(auto_now=True)
    article_picture = models.ImageField(upload_to='images')
    article_article_type = models.ManyToManyField(to=ArticleType)


# Create your models here.

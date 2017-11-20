from __future__ import unicode_literals
from django.db import models
import re
import bcrypt
from datetime import datetime, timedelta


EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX = re.compile("^[^0-9]+$")
PASSWORD_REGEX = re.compile("^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$")


class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}

        if postData['name'] == '':
            errors['name'] = 'Name can not be blank.'
        else:
            if not NAME_REGEX.match(postData['name']):
                errors['name'] = 'Please input valid name. No numbers.'

        if postData['alias'] == '':
            errors['alias'] = 'Alias can not be blank.'
        else:
            if len(self.filter(alias=postData['alias'])) > 0:
                    errors['alias'] = 'Alias already in use.'

        if postData['email'] == '':
            errors['email'] = 'Email can not be blank.'
        else:
            if not EMAIL_REGEX.match(postData['email']):
                errors['email'] = 'Please input valid email.'
            else:
                if len(self.filter(email=postData['email'])) > 0:
                    errors['email'] = 'email already in use.'

        if postData['password'] == '':
            errors['password'] = 'Password can not be blank.'
        else:
            if len(postData['password']) < 2:
                errors['password'] = 'Password can not be less than 8 characters.'
            else:
                # if not PASSWORD_REGEX.match(postData['password']):
                #     errors['password'] = 'Please input valid password.'
                if postData['password'] != postData['cpassword']:
                    errors['password'] = 'Password does not match.'

        if len(errors) == 0:
            hashpw = bcrypt.hashpw(
                postData['password'].encode(), bcrypt.gensalt())
            user = self.create(name=postData['name'], alias=postData['alias'],
                               email=postData['email'], password=hashpw)
            return (True, user)
        return (False, errors)
        # return dictionary

    def login_validator(self, postData):
        errors = {}

        try:
            user = self.get(email=postData['email'])
        except:
            errors['email'] = "Email and password input are invalid."

        if len(errors) == 0:

            if not bcrypt.checkpw(postData['password'].encode(), user.password.encode()):
                errors['password'] = "Password input is invalid."
            else:
                return (True, user)
                
        return (False, errors)

class BookManager(models.Manager):
    def book_validator(self, postData, id):
        errors = {}

        if postData['title']=="":
            errors['title'] = "Title can't be blank."

        else:
            title = Book.objects.filter(title=postData['title'])
            if len(title) > 0:
                errors['title'] = "The Book already exist."
                

        if postData['author']=="" and postData['newauthor']=="":
            errors['author'] = "Author part can't be blank."

        else: 
            if postData['author'] and postData['newauthor']:
                errors['author'] = "Please don't input two authors."

            else:

                author = Author.objects.filter(name=postData['newauthor'])
                if len(author) > 0:
                    errors['author'] = "Author already exist."
                        
        if postData['comment']=="":
            errors['comment'] = "Review can't be blank."

        if len(errors) == 0:
            user = User.objects.get(id=id)
            if postData['author']:
                newauthor = Author.objects.create(name = postData['author'])
            else:
                newauthor = Author.objects.create(name = postData['newauthor'])

            newbook = Book.objects.create(title = postData['title'], author = newauthor, uploader=user)
            newreview = Review.objects.create(comment = postData['comment'], rating = postData['rating'],reviewer=user, reviewedbook=newbook)
            

            return (True, newbook)


        return (False, errors)
class ReviewManager(models.Manager):
    def review_validator(self,postData,userid,bookid):
        errors = {}

        if postData['comment'] == "":
            errors['comment'] = "Review can't be blank."
        
        if len(errors) == 0:
            book = Book.objects.get(id = bookid)
            user = User.objects.get(id= userid)
            newreview = Review.objects.create(comment = postData['comment'], rating = postData['rating'],reviewer=user, reviewedbook=book)
            return (True, newreview)

        return (False, errors)

class User(models.Model):
    name = models.CharField(max_length=255)
    alias = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = UserManager()

class Author(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)  

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(Author, related_name="write_book")
    uploader = models.ForeignKey(User, related_name="books_uploaded")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = BookManager()

class Review(models.Model):
    comment = models.TextField()
    rating = models.CharField(max_length=255)
    reviewer = models.ForeignKey(User, related_name="reviewed")
    reviewedbook = models.ForeignKey(Book, related_name="reviews_on_book")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = ReviewManager()






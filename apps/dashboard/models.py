from __future__ import unicode_literals
from django.db import models
from datetime import datetime
import re

# create a regular expression object that we can use run operations on
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
ZIPCODE_REGEX = re.compile(r'^([0-9]){5}(([ ]|[-])?([0-9]){4})?$')
WORD_SPACE_REGEX = re.compile(r'^[A-Za-z ]+')

class UserManager(models.Manager):
    def basic_validator(slef, postData):
        errors = {}
        # validation for firstname
        if 'first_name' in postData:
            if len(postData['first_name']) == 0:
                errors['first_name'] = "*First Name is required"
            elif len(postData['first_name']) < 3:
                errors['first_name'] = "*Must be more than 2 characters"
            elif not postData['first_name'].isalpha():
                errors['first_name'] = "*Alphabets characters only"
        
        # validation for lastname
        if 'last_name' in postData:
            if len(postData['last_name']) == 0:
                errors['last_name'] = "*Last Name is required"
            elif len(postData['last_name']) < 3:
                errors['last_name'] = "*Must be more than 2 characters"
            elif not postData['last_name'].isalpha():
                errors['last_name'] = "*Alphabets characters only"
        
        # validation for email
        if 'email' in postData:
            if len(postData['email']) == 0:
                errors['email'] = "*Email is required"
            elif not EMAIL_REGEX.match(postData['email']):
                errors['email'] = "*Invalid email"

        # validation for password
        if 'password' in postData:
            if len(postData['password']) == 0:
                errors['password'] = "*Password is required"
            elif len(postData['password']) < 8:
                errors['password'] = '*Password must be at least 8 characters'
            elif not re.search('[0-9]', postData['password']):
                errors['password'] = '*Password must have at leat one number'
            elif not re.search('[A-Z]', postData['password']):
                errors['password'] = '*Password must have at least one Caplital letter'
            elif postData['password'] != postData['confirm_password']:
                errors['confirm_password'] = '*Password must be match'
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    desc = models.TextField()
    user_level = models.IntegerField(max_length=1, default=0)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    objects = UserManager()


class Message(models.Model):
    message = models.TextField()
    sender = models.ForeignKey(User, related_name="sent_messages")
    receiver = models.ForeignKey(User, related_name="received_messages")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)


class Comment(models.Model):
    comment = models.CharField(max_length=255)
    message = models.ForeignKey(Message, related_name="message_comments")
    commenter = models.ForeignKey(User, related_name="post_comments")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)



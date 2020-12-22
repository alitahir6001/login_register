from django.db import models
import re
import bcrypt

# Create your models here.


class user_manager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
### All this below will change based on the name of the form fields
        if len(postData['first_name']) < 2:
            errors['first_name'] = "First name is too short"

        if len(postData['last_name']) < 2:
            errors['last_name'] = "Last Name is too short"

        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Invalid email address!"
        if len(postData['email']) == 0:
            errors['email'] = "Email is required"

        if len(postData['password']) < 8:
            errors['password'] = "Password is too short"

        return errors

    def login_validator(self, postData):

        errors = {}
        user = User.objects.filter(email=postData['email']) #might change this because the exam might make you login with a username instead of an email
        if user:
            log_user = user[0]
            if not bcrypt.checkpw(postData['password'].encode(), log_user.password.encode()):
                errors['password'] = "Invalid login attempt"
        else:
            errors['password'] = "Invalid login attempt"

        return errors


class User(models.Model):
    first_name = models.CharField(max_length=45)  # These might change,
    last_name = models.CharField(max_length=45)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = user_manager()
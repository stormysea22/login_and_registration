from django.db import models
import re
from datetime import datetime, timedelta, date

# Create your models here.
class UserManager(models.Manager):
    
    def calculate_age(self, birth_date): 
        today = date.today() 
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        return age 
    
    def user_validator(self, post_data):
        errors = {}
        birth_date = datetime.strptime(post_data['birth_date'], '%Y-%m-%d').date()
        print(birth_date)

        if (len(post_data['first_name']) < 2) and (post_data['first_name'] != str.isalpha()):
            errors["f_name"] = "First name should be 2 letters or more and consist of letters only."
        
        if (len(post_data['last_name']) < 2) and (post_data['last_name'] != str.isalpha()):
            errors["l_name"] = "First name should be 2 letters or more and consist of letters only."
        
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        
        if not EMAIL_REGEX.match(post_data['email_address']):          
            errors['email'] = "Invalid email address!"
        
        try:
            User.objects.get(email_address = post_data['email_address'])
            errors['email_unique'] = "A user already exist with this email"
        
        except:
            pass
        
        if len(post_data['password']) < 8:
            errors['password_length'] = "Password should be longer the 8 characters"
        
        if post_data['password'] != post_data['password_confirm']:
            errors['password_match'] = "Please check that password and confirm password match"
        
        if self.calculate_age(birth_date) < 13 :
            errors['dob'] = "Come back when your over 13 years old kiddo!"
        
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email_address = models.CharField(max_length=255)
    password = models.CharField(max_length=60)
    birth_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
# username, mail, password

class UserInfo(models.Model):
    # creating one to one relation with admin --> User with UserInfo class
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    facebook_id = models.URLField(blank=True)
    profile_pic = models.ImageField(upload_to = 'profile_pics', blank=True)

    def __str__(self):
        return self.user.username

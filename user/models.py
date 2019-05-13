from django.contrib.auth.models import AbstractUser


# Create your models here.


class CustomUser(AbstractUser):
    """ Custom User model (to login with email instead of username) """
    # add additional fields in here

    def __str__(self):
        return self.email

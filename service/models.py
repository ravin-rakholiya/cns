from django.contrib.auth.models import User
from django.db import models

def service_path(instance, filename):
    return 'service/{}/{}'.format(
        instance.id,
        filename
    )

# Create your models here.
class ServiceCategory(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.id


class Country(models.Model):
    country = models.CharField(max_length=20)

    def __str__(self):
        return self.country


class State(models.Model):
    state = models.CharField(max_length=20)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)

    def __str__(self):
        return self.state


class City(models.Model):
    city = models.CharField(max_length=20)
    state = models.ForeignKey(State, on_delete=models.CASCADE)

    def __str__(self):
        return self.city


class ServicePost(models.Model):
    title = models.CharField(max_length=255, null=False, blank=False)
    category = models.ForeignKey(ServiceCategory, on_delete=models.CASCADE, null=False, blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    desc = models.TextField(null=True, blank=True)
    price = models.FloatField(default=0)
    duration = models.FloatField(default=0)
    address = models.CharField(max_length=100, null=False, blank=False, default='')  # Set default value here
    country = models.ForeignKey(Country, null=False, blank=False, on_delete=models.CASCADE)
    city = models.ForeignKey(City, null=False, blank=False, on_delete=models.CASCADE)
    state = models.ForeignKey(State, null=False, blank=False, on_delete=models.CASCADE)
    pincode = models.CharField(max_length=100, null=False, blank=False)
    picture = models.ImageField(upload_to=service_path, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)


class ServiceProviderAvailability(models.Model):
    day = models.CharField(max_length=20)
    available = models.BooleanField(default=False)
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    service_post = models.ForeignKey(ServicePost, on_delete=models.CASCADE)

    def _str_(self):
        return f"{self.user.username}'s availability on {self.day}"

class UserService(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    category = models.ForeignKey(ServiceCategory, on_delete=models.CASCADE, null=False, blank=False)
    desc = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.id


class UserServiceRating(models.Model):
    user_service = models.ForeignKey(UserService, on_delete=models.CASCADE, null=False, blank=False)
    rate = models.FloatField(default=0.0, null=False, blank=False)
    comment = models.TextField(null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.id


class Provider(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(default="")

    phone = models.CharField(max_length=20)
    password = models.CharField(max_length=255)


    def __str__(self):
        return self.id


class ServicePostComment(models.Model):
    comment = models.TextField(null=False, blank=False)
    interested = models.BooleanField(default=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.id

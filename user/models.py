from django.db import models


class UserType(models.Model):
    USER_TYPE_CHOICES = (
        ('user', 'User'),
        ('service_provider', 'Service Provider')
    )
    user_type = models.CharField(max_length=100, choices=USER_TYPE_CHOICES, default='user', null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user_type

    def __repr__(self):
        return f'<UserType: {self.user_type}>'


class User(models.Model):
    user_type = models.ForeignKey(UserType, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    user_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=30)
    phone_number = models.CharField(max_length=20)
    password = models.CharField(max_length=128)
    profile_picture = models.ImageField(upload_to='media/profile_pictures/', null=True, blank=True)
    availability = models.FloatField(default=0.0)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    rating = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    def __repr__(self):
        return f'<User: {self.user_name}>'

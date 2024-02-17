from django.db import models

# Create your models here.
from datetime import datetime


class UserAddress:
    def __init__(self, add1: str, add2: str, user: str, city: str, provision: str, country: str,
                 postal_code: str, created_at: datetime, updated_at: datetime):
        self.add1 = add1
        self.add2 = add2
        self.user = user
        self.city = city
        self.provision = provision
        self.country = country
        self.postal_code = postal_code
        self.created_at = created_at
        self.updated_at = updated_at


class Feedback:
    def __init__(self, user: str, feedback: str, created_at: datetime, updated_at: datetime):
        self.user = user
        self.feedback = feedback
        self.created_at = created_at
        self.updated_at = updated_at

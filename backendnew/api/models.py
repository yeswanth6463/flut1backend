from django.db import models
import hashlib
import secrets

# Create your models here.
class sailor_users(models.Model):
    email = models.EmailField(max_length=254, unique=True)
    password = models.CharField(max_length=128)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)   
    last_login = models.DateTimeField(null=True, blank=True)  
    
    def __str__(self):
        return self.email

    def set_password(self, raw_password):
        self.password = hashlib.sha256(raw_password.encode()).hexdigest()

    def check_password(self, raw_password):
        return self.password == hashlib.sha256(raw_password.encode()).hexdigest()


class EmailVerificationToken(models.Model):
    user = models.ForeignKey(sailor_users, on_delete=models.CASCADE)
    token = models.CharField(max_length=64, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    
    
    
class sailors(models.Model):
    email = models.ForeignKey(sailor_users,on_delete=models.CASCADE, related_name='sailors')
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    rank = models.CharField(max_length=50)
    experience_years = models.IntegerField()
    spouse_name = models.CharField(max_length=100, blank=True, null=True)
    childern_names = models.CharField(max_length=200, blank=True, null=True)
    home_location = models.CharField(max_length=200, blank=True, null=True)
    hobbies = models.TextField(blank=True, null=True)
    company_name = models.CharField(max_length=100, blank=True, null=True)
    
    

    def __str__(self):
        return  f"{self.name} - {self.rank} ({self.company_name})"

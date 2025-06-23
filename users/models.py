from django.db import models
from authapp.models import CustomUser  # Import your custom User model

class UserProfile(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    
    BODY_TYPE_CHOICES = [
        ('slim', 'Slim'),
        ('athletic', 'Athletic'),
        ('average', 'Average'),
        ('heavy', 'Heavy'),
    ]

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    height = models.FloatField(null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    body_type = models.CharField(max_length=20, choices=BODY_TYPE_CHOICES, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

class UserImage(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='user_images/')
    is_profile = models.BooleanField(default=False)  # True if it's their DP
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {'Profile' if self.is_profile else 'Gallery'}"

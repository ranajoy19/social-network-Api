from django.db import models
from .constants import status
# Create your models here.
from django.utils import timezone


from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email = models.EmailField(unique=True)




class FriendRequest(models.Model):
    sender = models.ForeignKey(User, related_name='sent_requests', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_requests', on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=status, default='pending')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(null=True)

    class Meta:
        verbose_name = "FriendRequest"
        db_table = 'friendsbook_friend_request'

    def __str__(self):
        return self.sender.first_name

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        timestamp = timezone.now()
        if not self.id:
            self.created_at = timestamp
        self.updated_at = timestamp
        return super(FriendRequest, self).save(*args, **kwargs)
from django.db import models

from django.db import models

class TelegramAuthToken(models.Model):
    token = models.CharField(max_length=64, unique=True)
    user_id = models.BigIntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


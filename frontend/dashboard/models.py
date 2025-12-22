from django.db import models

class Voter(models.Model):
    voter_address = models.CharField(max_length=42, unique=True)
    private_key = models.CharField(max_length=66)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.voter_address

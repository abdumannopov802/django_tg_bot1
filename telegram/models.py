from django.db import models

# Create your models here.
class Quiz(models.Model):
    question = models.CharField(max_length=100)
    answer = models.CharField(max_length=50)
    update = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.question